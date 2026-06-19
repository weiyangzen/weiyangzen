# agent_07 main 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 121
- source_commit: `6b3819fad50a89fffae899b240ad1ce065c51d23`
- scope: read-only research under `/Users/wangweiyang/GitHub/oh_my_humanize_branch_worktrees/main`; no files modified.
- inspection_method: recursive inventories with `rg --files`/`find`, direct file reads, symbol/test extraction, and targeted line-range reads for large runtime files.

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-007 `directory` `scripts`
- cursor: `[_]`
- core_role: Repository automation surface for CI, release, native builds, install verification, edit benchmarking, changelog normalization, prompt rewriting, and session-stat analytics.
- algorithmic_behavior: Recursively contains TypeScript CLIs (`release.ts`, `ci-test-ts.ts`, `fix-changelogs.ts`, `inline-functions.ts`), Python benchmark/stat analysis (`edit_benchmark_common.py`, `session-stats/*.py`), shell installers/signing scripts, Docker install-test fixtures, and generated stat plots. The key algorithms route process orchestration, parse logs/session JSONL, classify edit failures, normalize changelogs, and gate package publishing.
- inputs_outputs_state: Inputs are CLI args, env vars, git state, package metadata, session logs, benchmark fixtures, and release artifacts; outputs are process exit codes, generated reports/plots, rewritten files when used outside this read-only run, and CI/release logs. Stateful scripts track temp dirs, SQLite/session-stat DBs, benchmark run folders, and git refs.
- gates_or_invariants: CI scripts gate on command exit codes; changelog fixer preserves immutable released sections and normalizes only `[Unreleased]`; install tests exercise source/tarball/binary paths; benchmark scripts enforce retry/timeout/provider failure categories.
- dependencies_and_callers: Called by package scripts, CI workflows, release operators, and benchmark entrypoints. Depends on Bun, Python, matplotlib/numpy for stats, git, Docker/Podman test environments, and local packages.
- edge_cases_or_failure_modes: Git unavailable or dirty state, missing external binaries, malformed session JSON, auth/provider failures during benchmarks, huge logs, release artifact mismatches, platform-specific signing/upload failures.
- validation_or_tests: Includes `*.test.ts` files for changelog, inline functions, release notes, brew formula, concurrency, and session-stat audit; no test commands were run in this read-only pass.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-037 `directory` `packages/typescript-edit-benchmark`
- cursor: `[_]`
- core_role: Package-level benchmark harness for measuring coding-agent edit accuracy across generated TypeScript/JavaScript mutation tasks.
- algorithmic_behavior: Coordinates fixture generation, task loading, formatting, mutation generation, RPC/in-process agent execution, retry prompting, result aggregation, and report generation. `src/runner.ts` is the core loop; `src/generate.ts` builds mutation cases; `src/verify.ts` checks expected outcomes; `src/report.ts` renders summaries.
- inputs_outputs_state: Inputs are `fixtures.tar.gz`, extracted fixture directories, CLI config, model/provider settings, prompts, and run counts. Outputs are per-task run results, token/tool-call stats, conversation dumps, markdown/JSON reports, and temporary run directories.
- gates_or_invariants: Tasks require `instructions.md`, `expected/`, `initial/`, and metadata coherence; runs are bounded by timeout/turn limits; best-run selection favors success and lower failure severity; fixture validation rejects missing/extra expected files.
- dependencies_and_callers: Depends on `@oh-my-pi/pi-coding-agent`, Bun, Prettier, package-local prompt md files, and fixture archive. Called via package CLI/test scripts.
- edge_cases_or_failure_modes: Provider auth failures, transport failures, no-change mutations, formatting errors, multi-file fixture mismatch, turn-limit/timeouts, unstable generated tasks.
- validation_or_tests: Package has `test/runner.test.ts` and `test/verify.test.ts`; no tests executed.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-067 `file` `docs/porting-to-natives.md`
- cursor: `[_]`
- core_role: Architecture documentation for deciding when and how to port hot JS/TS algorithms to `pi-natives` N-API.
- algorithmic_behavior: Defines the porting decision algorithm: port only CPU-bound synchronous loops with low cross-boundary overhead, keep JS parity tests, expose Rust via `#[napi]`, regenerate platform artifacts, and benchmark against JS baselines. Key sections are “When to port” at line 5, “Anatomy of a native export” at line 28, and “Verification checklist” at line 161.
- inputs_outputs_state: Inputs are candidate JS implementations, Rust/N-API signatures, generated `.d.ts`/platform binaries, and benchmarks; outputs are native exports plus parity/performance evidence.
- gates_or_invariants: Must keep JS fallback semantics, generated types aligned with loaded binary, clean platform artifacts, and benchmarks that separate native work from startup/import overhead.
- dependencies_and_callers: Guides `crates/pi-natives`, package consumers, and benchmark scripts.
- edge_cases_or_failure_modes: Stale platform artifacts, Rust signature/type mismatch, enum export mismatches, misleading benchmarks, excessive JS/native boundary crossings.
- validation_or_tests: The doc prescribes `bun check`, package tests, native build, import smoke, and benchmark template execution; no validation run here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-097 `file` `scripts/edit_benchmark_common.py`
- cursor: `[_]`
- core_role: Shared Python harness for edit benchmark runs against the `omp` coding-agent CLI/RPC.
- algorithmic_behavior: Defines embedded Rust fixtures, benchmark dataclasses, verbose logging, retry prompt construction, model iteration, RPC event collection, timeout/retry behavior, and aggregate run output. Core functions: `_compute_edit_diff()` line 460, `run_benchmark_for_model()` line 706, `run_all()` line 819, `parse_args()` line 882, `run_benchmark_main()` line 924.
- inputs_outputs_state: Inputs are model names, CLI args, benchmark specs, current/target file content, `omp` binary path, and RPC event streams. Outputs are `BenchmarkResult` records with success, attempts, elapsed time, diffs, logs, and JSON summary.
- gates_or_invariants: Resolves repo-local `omp` when available, enforces per-model timeout/attempt limits, builds retry prompts from current content, treats validation as comparing final content/diff to expected.
- dependencies_and_callers: Depends on Python stdlib, `omp_rpc`, local CLI, and benchmark-specific scripts such as `edit-benchmark.py`.
- edge_cases_or_failure_modes: Missing `omp`, RPC startup failure, model stalls, malformed event streams, retry exhaustion, temp file cleanup, false success if content changes without matching expected diff.
- validation_or_tests: Embedded Rust fixture has its own test modules; no Python benchmark executed.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-127 `directory` `packages/ai/test`
- cursor: `[_]`
- core_role: Contract suite for the `packages/ai` provider layer, streaming protocols, auth storage, schema compatibility, model routing, token accounting, and regression bugs.
- algorithmic_behavior: Recursively covers provider-specific request shaping and stream parsing for Anthropic, OpenAI Responses/Completions/Codex, Gemini CLI/Antigravity, GitHub Copilot, Ollama, AWS, xAI, Xiaomi, OpenRouter, auth gateway, and schema normalization. It simulates SSE/events/fetches and asserts observable payloads, retry behavior, usage, and tool-call handling.
- inputs_outputs_state: Inputs are mocked `FetchImpl`s, fake OAuth/API credentials, model specs, streaming event bodies, JSON schemas, and fixture images/corpora. Outputs are assertions over request bodies, generated assistant events, stored credentials, retries, errors, and usage metadata.
- gates_or_invariants: Ensures no duplicate/orphan tool results, correct auth precedence, timeout/abort propagation, strict schema conversions, effort mapping, streaming terminal handling, cache affinity, and provider compatibility flags.
- dependencies_and_callers: Depends on `bun:test`, `@oh-my-pi/pi-ai`, catalog builders/models, local helpers, and fixture data. It is called by package-local verification.
- edge_cases_or_failure_modes: Racey auth refresh, malformed SSE, context overflow detection, rejected previous response IDs, provider-specific 429/401/413 handling, image limits, surrogate Unicode, stale cached models.
- validation_or_tests: This directory is itself validation; no suite run in this research pass.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-157 `directory` `packages/typescript-edit-benchmark/src`
- cursor: `[_]`
- core_role: Source implementation for the TypeScript edit benchmark engine.
- algorithmic_behavior: `tasks.ts` loads/validates tasks; `generate.ts` scores source files and creates mutation cases; `mutations.ts` mutates code; `runner.ts` executes models, collects tool telemetry, categorizes failures, retries, and summarizes; `verify.ts` compares workspace to expected; `report.ts` formats results; `in-process-client.ts` runs agent sessions without spawning the CLI.
- inputs_outputs_state: Inputs are fixture roots, mutation seeds, CLI options, model/auth config, prompt templates, and agent RPC events. Outputs are `BenchmarkResult`, reports, conversation dumps, per-run directories, and validation issues.
- gates_or_invariants: Fixture structure must be complete; prompt delivery must respect single/multi-file modes; run summaries preserve token/tool stats; retry contexts are built only from concrete failure telemetry.
- dependencies_and_callers: Package CLI (`src/index.ts`), generation scripts, tests, coding-agent CLI/RPC, Bun, Prettier.
- edge_cases_or_failure_modes: Tar extraction failures, unsupported extensions, malformed metadata, provider auth errors, no-op edit attempts, oversized summaries, multi-file expected mismatch.
- validation_or_tests: `test/runner.test.ts` and `test/verify.test.ts`; no test execution here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-187 `file` `docs/tools/edit.md`
- cursor: `[_]`
- core_role: User/tool contract specification for the `edit` tool and hashline/apply_patch accepted shapes.
- algorithmic_behavior: Defines source, inputs, tolerated lenient parsing, outputs, examples, limits, errors, and warnings. Key sections: “Inputs” line 19, hashline mode line 21, tolerated shapes line 49, outputs line 68, limits line 153, errors line 159.
- inputs_outputs_state: Inputs are file path, hashline patch sections, optional hashes/ranges, or apply_patch envelope variants; outputs are structured edit results, warnings, diff previews, and failures.
- gates_or_invariants: Preserves exact matching semantics, path normalization, hash validation, edit caps, no partial application on parse failure, and warning exposure for autocorrections.
- dependencies_and_callers: Documents coding-agent edit tool, hashline parser, streaming preview tests, and apply_patch parser.
- edge_cases_or_failure_modes: Incomplete edit payloads, ambiguous anchors, stale hashes, malformed headers, over-limit edits, line-ending and tab-sensitive patches.
- validation_or_tests: Covered by edit streaming/preview and hashline tests; no tests run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-217 `file` `scripts/session-stats/analyze_selector_reads.py`
- cursor: `[_]`
- core_role: Session-stat analyzer for read selector follow-up coverage and tool-read behavior.
- algorithmic_behavior: Parses read selectors into intervals, merges coverage, classifies follow-up reads, queries SQLite tool-call records, computes per-session/file coverage metrics, prints reports, plots stats, and dumps examples. Core functions: `parse_selector()` line 53, `args_to_interval()` line 82, `analyze()` line 174, `report()` line 262, `plot()` line 335, `main()` line 494.
- inputs_outputs_state: Inputs are stats SQLite DB, `since` timestamp, read tool args JSON, selector/path strings, optional plotting args. Outputs are console stats, PNG plots, and example records.
- gates_or_invariants: Default bare reads assume 500 lines; interval merge treats line ranges as inclusive/exclusive windows; follow-up classification compares new read coverage against previous intervals.
- dependencies_and_callers: Depends on sqlite3, matplotlib, numpy, and session-stat DB schema populated by sync scripts.
- edge_cases_or_failure_modes: Malformed JSON args, selectors without explicit ranges, overlapping intervals, missing DB rows, timezone parsing, plotting unavailable.
- validation_or_tests: Related session-stat audit tests exist; no analyzer run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-247 `directory` `packages/coding-agent/src/autolearn`
- cursor: `[_]`
- core_role: Runtime subsystem that nudges and manages agent-created skills.
- algorithmic_behavior: `controller.ts` builds auto-learn instructions and gates them by available tools/minimum tool calls; `managed-skills.ts` sanitizes names/descriptions, writes/delete managed `SKILL.md` files, serializes mutations per skill, enforces byte limits, and protects against unsafe symlink/root updates.
- inputs_outputs_state: Inputs are agent dir, raw skill name/description/body, settings/tool availability, session tool counts. Outputs are managed skill files under the agent skill provider and optional auto-learn instructions.
- gates_or_invariants: Skill names match `^[a-z0-9][a-z0-9-]{0,63}$`; max bytes 64,000; writes are serialized; update opens avoid following symlinks; managed root must be safe.
- dependencies_and_callers: Depends on `@oh-my-pi/pi-utils`, fs APIs, skill manager flows, and coding-agent prompt assembly.
- edge_cases_or_failure_modes: Invalid/suspicious names, oversized skill content, concurrent writes, symlink attacks, missing managed root, delete of nonexistent skill.
- validation_or_tests: No direct tests inspected in this directory, but skill tooling tests likely cover caller behavior; no tests run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-277 `directory` `packages/coding-agent/src/registry`
- cursor: `[_]`
- core_role: Agent registry and lifecycle data structures for runtime agent/session tracking.
- algorithmic_behavior: `agent-registry.ts` manages registration, lookup, parent/child relationships, snapshots, progress, and lifecycle state; `agent-lifecycle.ts` defines state transitions and event metadata for spawned/background agents.
- inputs_outputs_state: Inputs are agent definitions, IDs, parent IDs, progress/status updates, lifecycle events. Outputs are registry snapshots, agent state records, and UI/session metadata.
- gates_or_invariants: Agent IDs must be stable; parent/child linkage must not self-parent; lifecycle transitions keep finished/errored/active states distinguishable.
- dependencies_and_callers: Used by interactive mode, RPC subagents, tan/background job controller, and agent hub displays.
- edge_cases_or_failure_modes: Orphaned child agents, duplicate IDs, stale progress after completion, parent resolution during forks.
- validation_or_tests: Covered by `rpc-subagents.test.ts` and mode controller tests; no tests run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-307 `directory` `packages/coding-agent/test/modes`
- cursor: `[_]`
- core_role: Contract test suite for interactive mode UI/controller behavior.
- algorithmic_behavior: Recursively covers markdown prose masking, magic/orchestrate keywords, workflow UI, image references, theme rendering, event-controller streaming/abort/read grouping, selector deletion/logout/session operations, copy targets, settings selectors, tree rendering, and tool execution display.
- inputs_outputs_state: Inputs are mocked sessions, settings, UI components, key events, transcript messages, tool-call events, fake timers, and rendered component output. Outputs are assertions over rendered text, controller state, dispatched actions, timers, and session mutations.
- gates_or_invariants: Rendering must preserve visible text width, ignore keywords inside code/XML, avoid duplicate notifications, keep optimistic submissions ordered, and maintain selector/tree viewport contracts.
- dependencies_and_callers: Depends on `bun:test`, `pi-tui`, coding-agent controllers/components/settings/session modules.
- edge_cases_or_failure_modes: Aborted/error stops, duplicate IRC events, in-flight turn mutations, viewport overflow, stale session deletion, image replay on cold-start rebuild.
- validation_or_tests: Directory is validation; no suite run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-337 `file` `crates/pi-ast/src/lib.rs`
- cursor: `[_]`
- core_role: Rust crate barrel for AST support modules.
- algorithmic_behavior: Exports `block`, `language`, `ops`, `summary`, and re-exports `SupportLang`. No local algorithm beyond module surface declaration.
- inputs_outputs_state: Inputs/outputs are compile-time module exports.
- gates_or_invariants: Module names must exist and preserve public API shape.
- dependencies_and_callers: Used by Rust consumers importing `pi_ast`.
- edge_cases_or_failure_modes: Broken module path or unintended public API churn.
- validation_or_tests: Covered by crate compilation/tests when run; not run here.
- skip_candidate: `yes: re-export surface only, not an algorithm implementation`

### OH_MY_HUMANIZE_MAIN-HZ-367 `file` `crates/pi-natives/src/ps.rs`
- cursor: `[_]`
- core_role: N-API process tree binding for JavaScript callers.
- algorithmic_behavior: Wraps `pi_shell::process::Process` with exported `from_pid`, `from_path`, PID/PPID/args, `kill_tree`, async `terminate`, `wait_for_exit`, `group_id`, `children`, and `status`. It maps core `ProcessStatus` to N-API string enum and schedules async waits through `task::future`.
- inputs_outputs_state: Inputs are PID/path, terminate/wait options (`group`, `graceful_ms`, `timeout_ms`, abort signal), and optional signals. Outputs are process references, booleans, status strings, child lists, and killed counts.
- gates_or_invariants: Defaults to graceful 1000ms and timeout 5000ms; abort signal must cancel waits; Windows ignores POSIX signal; process references are stable wrappers.
- dependencies_and_callers: Depends on `napi`, `napi_derive`, `pi_shell::process`, and native task bridge. Called by JS process-management code.
- edge_cases_or_failure_modes: PID gone before open, process group unsupported, timeout/cancel during termination, permission-denied process inspection, platform signal differences.
- validation_or_tests: Native/process tests would validate; none run here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-397 `file` `packages/agent/test/agent-loop.test.ts`
- cursor: `[_]`
- core_role: Core behavior test suite for `agentLoop` and `agentLoopContinue`.
- algorithmic_behavior: Exercises message conversion, streaming assistant events, tool call/result sequencing, missing results, tool refresh, same-turn model calls, whitespace loop recovery, useless-flag propagation, abort/error handling, and loop continuation. Key top-level blocks begin at lines 23, 1435, and 1489.
- inputs_outputs_state: Inputs are mock model responses/events, tool definitions, agent messages, and stream converters. Outputs are emitted `AgentMessage` sequences, returned detailed loop state, tool invocations, and error/stop reasons.
- gates_or_invariants: Tool calls must pair with results; system prompt/tools refresh between calls; provider recovery must not duplicate assistant messages; useless flags propagate only through intended paths.
- dependencies_and_callers: Depends on `@oh-my-pi/pi-agent-core/agent-loop`, mock provider, `AssistantMessageEventStream`, arktype schemas.
- edge_cases_or_failure_modes: Missing tool results, abandoned tool use, repeated whitespace, provider abort, same-turn tool refresh, malformed event ordering.
- validation_or_tests: Test file itself; not executed.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-427 `file` `packages/ai/src/types.ts`
- cursor: `[_]`
- core_role: Central public type and small policy helper surface for `pi-ai`.
- algorithmic_behavior: Re-exports catalog effort/types, defines provider options map, message/content/tool schemas, context/stream options, service tier helpers, `Tool` schema typing, usage/metadata, and stream function signatures. Runtime helpers include `resolveServiceTier()` line 128, `shouldSendServiceTier()` line 149, and `getPriorityPremiumRequests()` line 166.
- inputs_outputs_state: Inputs are API/provider choices, service tier flags, model/request options, messages, tools, and contexts. Outputs are typed option narrowing, resolved tiers, provider payloads, events, and message structures.
- gates_or_invariants: Api options map must be exhaustive for known APIs; service-tier aliases like `openai-only`/`claude-only` resolve before wire use; tool/result messages preserve call IDs.
- dependencies_and_callers: Used across all providers, agent runtime, catalog model construction, and tests.
- edge_cases_or_failure_modes: New API missing map entry, `any` leakage in tool details, wrong service tier sent to incompatible provider, mismatched content block shape.
- validation_or_tests: Many `packages/ai/test` files depend on this contract; no tests run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-457 `file` `packages/ai/test/auth-broker-remote-store.test.ts`
- cursor: `[_]`
- core_role: Contract tests for remote auth credential store SSE integration.
- algorithmic_behavior: Mints OAuth credentials, configures temp auth storage, simulates remote refresh sentinel behavior, and verifies `RemoteAuthCredentialStore` integration with `SqliteAuthCredentialStore`. Main block starts line 37.
- inputs_outputs_state: Inputs are temp DB paths, env overrides, fake OAuth credentials with expiry, remote broker messages. Outputs are selected/refreshed credentials and stored auth state.
- gates_or_invariants: Remote sentinel must trigger broker refresh instead of treating local store as complete; env keys are restored after tests.
- dependencies_and_callers: Depends on auth storage classes and broker remote store.
- edge_cases_or_failure_modes: Missing refresh sentinel, stale expiry, env leakage, remote stream failure.
- validation_or_tests: Test file not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-487 `file` `packages/ai/test/aws-credentials.test.ts`
- cursor: `[_]`
- core_role: Contract tests for AWS credential process tokenization/resolution.
- algorithmic_behavior: Verifies shell-like tokenization, quoted/backslash behavior, Version 1 credential envelope parsing, caching by profile, unsupported version rejection, stderr surfacing, and aborting long helpers. Test blocks start lines 35 and 77.
- inputs_outputs_state: Inputs are temp credential config files, helper scripts, env vars, abort signals. Outputs are resolved AWS credentials, cached results, or surfaced errors.
- gates_or_invariants: Unterminated quotes reject; expiration is honored; non-zero helper includes stderr; caller abort must stop helper.
- dependencies_and_callers: Depends on AWS credential resolver and Bun test temp filesystem.
- edge_cases_or_failure_modes: Windows backslashes in quotes, empty input, unsupported envelope, helper hang.
- validation_or_tests: Test file not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-517 `file` `packages/ai/test/google-gemini-cli-alignment.test.ts`
- cursor: `[_]`
- core_role: Contract tests for Gemini CLI/Antigravity provider wire alignment.
- algorithmic_behavior: Builds provider models and context, simulates validation-required responses, OAuth key retrieval, streaming fetches, tool schemas, and provider-specific request/response behavior. Main describe starts line 57.
- inputs_outputs_state: Inputs are fake models, OAuth tokens, validation URLs, fetch mocks, tool schemas. Outputs are assistant events, auth handling, and request body assertions.
- gates_or_invariants: Gemini CLI and Antigravity providers must align on auth/validation flows while preserving provider-specific IDs; validation URL extraction must be stable.
- dependencies_and_callers: Depends on `providers/google-gemini-cli`, OAuth registry, catalog `buildModel`.
- edge_cases_or_failure_modes: Validation-required body, missing OAuth, malformed stream, tool schema mismatch.
- validation_or_tests: Test file not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-547 `file` `packages/ai/test/issue-911-repro.test.ts`
- cursor: `[_]`
- core_role: Regression test for Mistral/OpenAI completions array content parts.
- algorithmic_behavior: Creates SSE response/fetch mock, base context, and validates `streamOpenAICompletions` handles array content parts without mis-shaping messages. Helpers at lines 6, 16, 22; describe at line 41.
- inputs_outputs_state: Inputs are synthetic SSE events and bundled model. Outputs are streamed assistant/tool events and assertions.
- gates_or_invariants: Provider must accept content parts arrays and not collapse or reject valid multimodal/text structure.
- dependencies_and_callers: Depends on OpenAI completions provider and catalog model lookup.
- edge_cases_or_failure_modes: Array content parsing regressions, malformed SSE, provider compatibility flags.
- validation_or_tests: Test not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-577 `file` `packages/ai/test/openai-codex-responses-lite.test.ts`
- cursor: `[_]`
- core_role: Contract tests for OpenAI Codex Responses Lite request shaping and metadata.
- algorithmic_behavior: Creates Codex test token/context/SSE, captures fetch requests, and verifies `reasoning.context`, Lite input shaping, client metadata wire format, response metadata moderation, and websocket append behavior. Describe blocks at lines 81, 113, 161, 200, 242.
- inputs_outputs_state: Inputs are fake tokens, response events, model helper, fetch mock. Outputs are request body/header assertions and streamed events.
- gates_or_invariants: Client metadata must be sent in the expected field; moderation metadata must be handled; Lite input format must match Codex expectations.
- dependencies_and_callers: Depends on `streamOpenAICodexResponses` and helper model creation.
- edge_cases_or_failure_modes: Missing account ID, malformed SSE, wrong reasoning context, websocket metadata mismatch.
- validation_or_tests: Test not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-607 `file` `packages/ai/test/overflow-utils.test.ts`
- cursor: `[_]`
- core_role: Contract tests for context-overflow error classification.
- algorithmic_behavior: Builds assistant error messages and checks `isContextOverflow` for model context-window errors, HTTP 413 variants, and 400/413 no-body provider wrappers. Blocks start lines 26, 44, 61.
- inputs_outputs_state: Inputs are assistant messages with error text/status metadata. Outputs are boolean overflow classification.
- gates_or_invariants: Must detect true context overflow without overmatching generic provider errors.
- dependencies_and_callers: Depends on `@oh-my-pi/pi-ai/utils/overflow`.
- edge_cases_or_failure_modes: Mistral/Cerebras/proxy wrappers, no response body, provider-specific wording.
- validation_or_tests: Test not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-637 `file` `packages/ai/test/tokens.test.ts`
- cursor: `[_]`
- core_role: Token usage/statistics tests across real or OAuth-backed provider paths.
- algorithmic_behavior: Resolves OAuth/API keys for multiple providers, streams requests, and asserts usage/token statistics on abort behavior. Main describe begins line 71.
- inputs_outputs_state: Inputs are OAuth tokens/API keys, contexts, models, stream options. Outputs are streamed events and usage/abort statistics.
- gates_or_invariants: Abort must preserve available token stats; provider-specific options must resolve correctly.
- dependencies_and_callers: Depends on `stream`, `resolveApiKey`, catalog models, OAuth helpers.
- edge_cases_or_failure_modes: Missing credentials, provider abort timing, partial usage metadata.
- validation_or_tests: Test not run; may require credentials.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-667 `file` `packages/catalog/src/types.ts`
- cursor: `[_]`
- core_role: Catalog type model for APIs, providers, compatibility metadata, usage, and model specs.
- algorithmic_behavior: Defines known API union, thinking config, fetch/usage shapes, OpenAI/Anthropic/OpenRouter/Vercel compatibility knobs, resolved compat types, and `Model`/`ModelSpec`. Key sections: `OpenAICompat` line 163, `ResolvedOpenAISharedCompat` line 416, `Model` line 580.
- inputs_outputs_state: Inputs are generated/provider model descriptors and compat configs. Outputs are strongly typed model records used by ai/coding-agent.
- gates_or_invariants: Compat config type must align with API; generated specs omit resolved compat; usage tokens/pricing fields retain optionality.
- dependencies_and_callers: Used by catalog generator/resolvers and `packages/ai`.
- edge_cases_or_failure_modes: New provider/API not reflected, compat flags conflicting, generated JSON shape drift.
- validation_or_tests: Catalog and provider tests cover consumers; no tests run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-697 `file` `packages/catalog/test/minimax-bundled-catalog.test.ts`
- cursor: `[_]`
- core_role: Small bundled-catalog smoke/regression test for MiniMax entries.
- algorithmic_behavior: Imports generated `models.json` and asserts expected MiniMax catalog availability/shape. Describe starts line 4.
- inputs_outputs_state: Input is bundled JSON; output is assertions.
- gates_or_invariants: Generated catalog must include MiniMax entry expected by downstream code.
- dependencies_and_callers: Depends on generated catalog JSON.
- edge_cases_or_failure_modes: Upstream generation drops/renames MiniMax model.
- validation_or_tests: Test not run.
- skip_candidate: `yes: generated-catalog smoke only, not runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-727 `file` `packages/coding-agent/src/config.ts`
- cursor: `[_]`
- core_role: Configuration discovery and path-resolution entrypoint for coding-agent.
- algorithmic_behavior: Walks up from cwd to find package dir (`walkUpForPackageDir()` line 30), resolves package/changelog paths, constructs user/project config base lists, returns config dirs with level/path metadata, finds nearest config file, and enumerates project config dirs.
- inputs_outputs_state: Inputs are cwd, subpath, include options, env/global agent dir utilities. Outputs are config paths/entries and optional file metadata.
- gates_or_invariants: Config precedence follows priority list; project dirs walk upward; tilde expansion applies to configured base dirs; missing dirs/files return undefined/empty rather than throwing.
- dependencies_and_callers: Depends on `@oh-my-pi/pi-utils`, `node:fs/os/path`, and path utils. Used by settings, model registry, capabilities, plugins.
- edge_cases_or_failure_modes: Nonexistent cwd ancestors, multiple config layers, home/config env overrides, project root mismatch.
- validation_or_tests: Covered by settings/config tests; no tests run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-757 `file` `packages/coding-agent/test/agent-session-btw-branch.test.ts`
- cursor: `[_]`
- core_role: Contract tests for branching from “btw” assistant state.
- algorithmic_behavior: Builds a BTW assistant message, creates mock sessions/models/storage, and verifies `AgentSession.branchFromBtw` behavior. Helper at line 17; describe at line 40.
- inputs_outputs_state: Inputs are session transcripts, mock model handler, temp session storage. Outputs are branched session state and assistant/user message assertions.
- gates_or_invariants: Branching must preserve relevant transcript, create isolated session file, and not corrupt source session.
- dependencies_and_callers: Depends on `AgentSession`, `SessionManager`, `AuthStorage`, mock provider, model registry.
- edge_cases_or_failure_modes: Missing BTW message, temp file cleanup, auth/model fallback, extension runner interactions.
- validation_or_tests: Test not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-787 `file` `packages/coding-agent/test/agent-session-tool-rebuild-skip.test.ts`
- cursor: `[_]`
- core_role: Contract tests for MCP/custom tool refresh rebuild skipping.
- algorithmic_behavior: Creates mock model/basic tools/MCP tools and validates `AgentSession.refreshMCPTools` skips unnecessary agent rebuilds while rebuilding when tool identity/description changes. Helpers at lines 16, 31, 44; describe at line 59.
- inputs_outputs_state: Inputs are tool lists, session settings, timestamps. Outputs are agent tool inventories and rebuild counters/state.
- gates_or_invariants: Tool rebuild must be skipped only when effective tool set is unchanged; custom MCP tool identity includes server/tool name.
- dependencies_and_callers: Depends on `Agent`, `AgentSession`, `SessionManager`, settings, arktype.
- edge_cases_or_failure_modes: Stale descriptions, duplicate tool names, time-based refresh, MCP custom tool mismatch.
- validation_or_tests: Test not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-817 `file` `packages/coding-agent/test/cli-advisor-flag.test.ts`
- cursor: `[_]`
- core_role: Tiny CLI parser contract test for `--advisor`.
- algorithmic_behavior: Calls `parseArgs` and verifies advisor flag parsing. Describe at line 4.
- inputs_outputs_state: Inputs are argv arrays; outputs are parsed CLI config.
- gates_or_invariants: Advisor option must set intended mode without breaking other args.
- dependencies_and_callers: Depends on coding-agent CLI args parser.
- edge_cases_or_failure_modes: Flag omitted, flag combined with other args.
- validation_or_tests: Test not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-847 `file` `packages/coding-agent/test/edit-streaming-preview.test.ts`
- cursor: `[_]`
- core_role: Contract tests for edit/apply_patch streaming preview rendering and incomplete edit dropping.
- algorithmic_behavior: Exercises `dropIncompleteLastEdit`, hashline multi-section/single-op previews, monotonic preview growth, apply_patch trailing partial lines, and `matcherDigest`. Describe blocks at lines 8, 37, 100, 189, 248, 305.
- inputs_outputs_state: Inputs are temp files, hashline headers, partial tool payloads, snapshot store state. Outputs are preview text, dropped/kept edit sections, and digest strings.
- gates_or_invariants: Streaming previews must not show incomplete trailing edits as committed; growth should be monotonic; hashline warnings/digests stable.
- dependencies_and_callers: Depends on `@oh-my-pi/hashline`, coding-agent edit strategies, fs temp dirs.
- edge_cases_or_failure_modes: Partial JSON/tool args, trailing payload without newline, autocorrect warnings, multi-section patch ordering.
- validation_or_tests: Test not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-877 `file` `packages/coding-agent/test/hook-editor.test.ts`
- cursor: `[_]`
- core_role: Contract tests for hook editor component and extension UI controller dialogs.
- algorithmic_behavior: Renders hook/prompt-style editors, simulates input/paste/keybindings, abort flows, and dialog serialization. Helper functions at lines 22, 32, 36; describe blocks at lines 83, 174, 375, 439.
- inputs_outputs_state: Inputs are TUI key events, large paste text, controller contexts, theme/keybinding setup. Outputs are rendered lines, editor state, controller results.
- gates_or_invariants: Large paste handling, prompt-style layout, abort behavior, and serialized dialogs must remain stable.
- dependencies_and_callers: Depends on `HookEditorComponent`, `ExtensionUiController`, `pi-tui`, keybindings/theme.
- edge_cases_or_failure_modes: Paste overflow, abort while dialog active, focus/keybinding conflicts, text wrapping.
- validation_or_tests: Test not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-907 `file` `packages/coding-agent/test/interactive-mode-working-accent.test.ts`
- cursor: `[_]`
- core_role: Contract tests for working-message session accent cache.
- algorithmic_behavior: Builds `InteractiveMode` harness, starts stable loader, shadows accent luminance, and checks rendered loader accent behavior. Helpers at lines 19, 52, 57, 61; describe at line 81.
- inputs_outputs_state: Inputs are settings, session manager state, mocked session color. Outputs are rendered loader text/styles and cache behavior.
- gates_or_invariants: Working message should use stable session accent without recomputing inconsistently across render frames.
- dependencies_and_callers: Depends on `InteractiveMode`, settings/theme/session manager, session color utility.
- edge_cases_or_failure_modes: Missing session, theme init order, accent luminance undefined, stale cache.
- validation_or_tests: Test not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-937 `file` `packages/coding-agent/test/issue-985-subagent-auth-fallback.test.ts`
- cursor: `[_]`
- core_role: Regression tests for subagent dispatch model auth fallback.
- algorithmic_behavior: Builds parent/task/shared models, mock registry, and verifies fallback from unauthenticated task model to shared/parent model behavior. Model constants start line 24; mock registry line 68; describe line 78.
- inputs_outputs_state: Inputs are model registry states with `kNoAuth`, subagent dispatch options. Outputs are selected model/auth fallback assertions.
- gates_or_invariants: Subagent should not fail solely because task-specific model is unauthenticated when a valid fallback exists; explicit no-auth remains respected.
- dependencies_and_callers: Depends on catalog `buildModel`, model registry, subagent dispatch code.
- edge_cases_or_failure_modes: Shared model missing, parent model unauthenticated, fallback disabled.
- validation_or_tests: Test not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-967 `file` `packages/coding-agent/test/mcp-resource-templates-missing.test.ts`
- cursor: `[_]`
- core_role: Regression tests for MCP servers lacking `resources/templates/list`.
- algorithmic_behavior: Builds mock transport returning method errors, constructs resource connection, and verifies `listResourceTemplates` handles `-32601` plus `MCPManager` loads resources from templates-less fixture server. Helpers at lines 26, 35; describes at lines 45, 74.
- inputs_outputs_state: Inputs are mocked MCP JSON-RPC methods and fixture server path. Outputs are resource/template lists and manager state.
- gates_or_invariants: Missing template method must degrade to empty templates, not block resources.
- dependencies_and_callers: Depends on MCP client/manager/types and fixture server.
- edge_cases_or_failure_modes: Method-not-found vs other errors, stdio server lifecycle, fixture resource URI mismatch.
- validation_or_tests: Test not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-997 `file` `packages/coding-agent/test/plugin-command.test.ts`
- cursor: `[_]`
- core_role: Minimal parser test for plugin command scope parsing.
- algorithmic_behavior: Instantiates plugin command with test config and validates command scope behavior. Describe at line 11.
- inputs_outputs_state: Inputs are plugin command args/config; outputs are parsed command scope/action.
- gates_or_invariants: Scope parsing must remain stable for plugin CLI command routing.
- dependencies_and_callers: Depends on `commands/plugin` and CLI config type.
- edge_cases_or_failure_modes: Missing/invalid scope, default scope mismatch.
- validation_or_tests: Test not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1027 `file` `packages/coding-agent/test/rpc-subagents.test.ts`
- cursor: `[_]`
- core_role: Contract tests for RPC subagent registry, transcript reading, and frame protocol.
- algorithmic_behavior: Creates progress snapshots, registry/session stubs, temp transcript paths, and tests registry snapshot updates, transcript parsing, and `RpcClient` subagent frames. Describe blocks at lines 83, 318, 359.
- inputs_outputs_state: Inputs are JSONL frames, progress objects, event bus events, temp files. Outputs are registry snapshots, read transcripts, and client frame handling assertions.
- gates_or_invariants: Frames must preserve IDs/status/progress; transcript reading must handle complete and partial records; registry snapshot must update predictably.
- dependencies_and_callers: Depends on RPC client/subagents/types, EventBus, session manager types.
- edge_cases_or_failure_modes: Missing transcript, malformed frame, duplicate agent IDs, stale progress.
- validation_or_tests: Test not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1057 `file` `packages/coding-agent/test/settings-manager.test.ts`
- cursor: `[_]`
- core_role: Contract tests for settings initialization, persistence, YAML handling, and override precedence.
- algorithmic_behavior: Uses temp dirs and settings test state to verify settings load/save/defaults across project/user scopes, model/effort config, and YAML parsing. Describe at line 19.
- inputs_outputs_state: Inputs are temp config files, env/config dir overrides, YAML content. Outputs are `Settings` values and persisted files.
- gates_or_invariants: In-memory tests must restore state; project agent dir resolution stable; settings precedence correct.
- dependencies_and_callers: Depends on `Settings`, `SettingsManager`, `getProjectAgentDir`, YAML.
- edge_cases_or_failure_modes: Invalid YAML, missing dirs, env leakage, stale singleton state.
- validation_or_tests: Test not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1087 `file` `packages/coding-agent/test/streaming-reveal.test.ts`
- cursor: `[_]`
- core_role: Contract tests for assistant streaming reveal controller behavior.
- algorithmic_behavior: Builds message/content helpers, recording component, and controller to validate smooth reveal, thinking hiding, render requests, text/thinking block updates. Helpers at lines 13, 24, 37, 45, 71; describe at line 81.
- inputs_outputs_state: Inputs are assistant messages with text/thinking content and reveal options. Outputs are component message mutations and render callbacks.
- gates_or_invariants: Text/thinking should reveal in order, respect hide-thinking, and avoid corrupting usage/content blocks.
- dependencies_and_callers: Depends on streaming reveal utilities/components.
- edge_cases_or_failure_modes: Fast streaming, empty content, hidden thinking, concurrent render requests.
- validation_or_tests: Test not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1117 `file` `packages/coding-agent/test/update-cli.test.ts`
- cursor: `[_]`
- core_role: Contract tests for CLI self-update install target detection and binary replacement.
- algorithmic_behavior: Uses temp dirs and fs spies to test install target detection, package-manager command construction, Bun install command, binary replacement, locked backups, and stale backup sweep. Describe blocks at lines 27, 83, 95, 141, 187, 229.
- inputs_outputs_state: Inputs are fake executable paths, package manager state, temp binary files. Outputs are command selections, backup files, replaced binaries, cleanup behavior.
- gates_or_invariants: Must not overwrite locked backup unsafely; stale backups removed; package manager commands correct per install source.
- dependencies_and_callers: Depends on update CLI internals and fs/path/os.
- edge_cases_or_failure_modes: Locked file, missing target, platform differences, stale backup naming.
- validation_or_tests: Test not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1147 `file` `packages/hashline/src/fs.ts`
- cursor: `[_]`
- core_role: Filesystem abstraction layer for hashline edit/snapshot operations.
- algorithmic_behavior: Defines `NotFoundError`, `isNotFound`, abstract `Filesystem`, `InMemoryFilesystem`, and `BunFilesystem`. `exists()` uses read/error semantics in base class; in-memory stores a map; Bun implementation reads/writes text and resolves canonical paths.
- inputs_outputs_state: Inputs are paths/content; outputs are read text, write results, existence booleans, canonical paths, and map state for memory implementation.
- gates_or_invariants: `readText` must throw `NotFoundError`-compatible errors for missing files; write result returns resulting text; canonical path default is identity.
- dependencies_and_callers: Used by hashline apply/snapshot stores and edit tooling.
- edge_cases_or_failure_modes: Missing file, ENOENT structural errors, stale snapshots due noncanonical paths, Bun write failures.
- validation_or_tests: Covered by hashline/edit tests; not run here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1177 `file` `packages/mnemopi/src/mcp-tools.ts`
- cursor: `[_]`
- core_role: MCP tool schema and dispatch implementation for mnemopi memory operations.
- algorithmic_behavior: Defines JSON schemas and `TOOLS`, argument coercion helpers, BeamMemory creation/routing, shared memory surface, scratchpad, triples, import/export, validation, diagnosis, graph query/link, and `handleToolCall()` at line 963.
- inputs_outputs_state: Inputs are MCP tool names/arguments, env/session/bank IDs, DB paths, memory content/query/metadata. Outputs are tool result objects with status, IDs, serialized memories, stats, export/import stats, or errors.
- gates_or_invariants: Required args return `{ error }`; bank defaults from args/env/default; Beam instances are closed in `finally`; shared memory restricts kind to `meta|preference|correction|identity`; graph APIs are capability-checked.
- dependencies_and_callers: Depends on `BeamMemory`, `BankManager`, triples store, config `dataDir`. Called by MCP server.
- edge_cases_or_failure_modes: Unknown tool throws, missing input file, invalid shared kind/action, graph unavailable, non-object metadata ignored, JSON import parse errors.
- validation_or_tests: Covered by mnemopi tests; no tests run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1207 `file` `packages/mnemopi/test/extraction.test.ts`
- cursor: `[_]`
- core_role: Tests for mnemopi structured fact extraction.
- algorithmic_behavior: Restores env after tests, checks prompt building, parse facts, heuristic extraction, diagnostics stats, and safe extraction behavior. Describe starts line 38.
- inputs_outputs_state: Inputs are raw model outputs/text/env flags; outputs are fact arrays and diagnostic counters.
- gates_or_invariants: Extraction should parse JSON/fenced output, fall back heuristically, and keep diagnostics coherent.
- dependencies_and_callers: Depends on extraction module and diagnostics.
- edge_cases_or_failure_modes: Empty input, malformed LLM output, env override leakage.
- validation_or_tests: Test not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1237 `file` `packages/mnemopi/test/telemetry-env-followups.test.ts`
- cursor: `[_]`
- core_role: Tests for telemetry/env follow-up parity in BeamMemory.
- algorithmic_behavior: Creates temp DB roots, sets env, instantiates `BeamMemory`, and verifies telemetry/follow-up behavior parity. Temp helper at line 9; describe at line 23.
- inputs_outputs_state: Inputs are temp DB path and env variables. Outputs are memory DB side effects and assertions.
- gates_or_invariants: Env configuration must match explicit runtime behavior; temp roots cleaned.
- dependencies_and_callers: Depends on `BeamMemory`.
- edge_cases_or_failure_modes: Env leakage, temp DB cleanup, telemetry mismatch.
- validation_or_tests: Test not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1267 `file` `packages/snapcompact/research/diag_glm_mono.py`
- cursor: `[_]`
- core_role: Research script for monolithic GLM diagnostic scoring over Snapcompact/SQuAD batches.
- algorithmic_behavior: Robustly parses answers, converts messages to chat format, scores answers, runs batch completion with GLM/ZAI helpers, and writes results. Core functions: `parse_robust()` line 32, `to_chat()` line 43, `score()` line 56, `main()` line 81.
- inputs_outputs_state: Inputs are questions, image/message batches, API key env, optional output dir. Outputs are scores, JSON/results artifacts.
- gates_or_invariants: Parser must return exactly expected answer count or salvage robustly; scoring compares predicted answers to references.
- dependencies_and_callers: Depends on local research modules `squad`, `diag_glm_forensics`, `diag_glm_probe`, `providers`, `run`.
- edge_cases_or_failure_modes: Missing API key, model output format drift, answer count mismatch, thread pool/API failures.
- validation_or_tests: Research script, no tests run.
- skip_candidate: `yes: research/diagnostic script, not production runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1297 `file` `packages/snapcompact/research/mono_prod.py`
- cursor: `[_]`
- core_role: Research/production-like Snapcompact monolithic prompt experiment.
- algorithmic_behavior: Runs text/image compare experiments, builds prompts, calls provider, parses outputs, and records metrics for monolithic compression/QA behavior.
- inputs_outputs_state: Inputs are document chunks/images/questions/provider env; outputs are experiment JSON/metrics.
- gates_or_invariants: Must preserve answer alignment and deterministic output file naming for comparisons.
- dependencies_and_callers: Depends on local snapcompact research helper modules and provider APIs.
- edge_cases_or_failure_modes: Missing model credentials, malformed response, image load failure, inconsistent answer count.
- validation_or_tests: Research-only; not run.
- skip_candidate: `yes: research experiment rather than package runtime`

### OH_MY_HUMANIZE_MAIN-HZ-1327 `file` `packages/snapcompact/research/snapcompact_text_image_compare.py`
- cursor: `[_]`
- core_role: Research visualization/comparison script for Snapcompact text/image attention or heat-grid outputs.
- algorithmic_behavior: Loads arrays/images, computes summaries, draws wrapped text and heat grids, renders visual comparison images, and runs CLI main. Key functions include `draw_wrapped()` line 206, `render_heat_grid()` line 227, `render_visual()` line 252, `main()` line 354.
- inputs_outputs_state: Inputs are summaries, numpy arrays, original image, text chunk, output path. Outputs are rendered PNG/visual artifacts.
- gates_or_invariants: Grid dimensions and answer indices must align; text wrapping must fit chart boxes.
- dependencies_and_callers: Depends on PIL, numpy, local research data.
- edge_cases_or_failure_modes: Missing fonts/images, array shape mismatch, out-of-range answer indices.
- validation_or_tests: Research script; not run.
- skip_candidate: `yes: research visualization, not production runtime`

### OH_MY_HUMANIZE_MAIN-HZ-1357 `file` `packages/stats/test/db-cost.test.ts`
- cursor: `[_]`
- core_role: Contract test for stats DB request cost correction.
- algorithmic_behavior: Creates temp stats DB, inserts GPT/Codex message stats, and checks corrected cost returned by `getRecentRequests`. Helpers at lines 33 and 57; describe at line 70.
- inputs_outputs_state: Inputs are temp agent dir/env, `MessageStats`, bundled model cost. Outputs are DB rows and cost assertions.
- gates_or_invariants: Cost calculation must match bundled model pricing and correct GPT/Codex handling.
- dependencies_and_callers: Depends on `bun:sqlite`, stats DB module, catalog model lookup.
- edge_cases_or_failure_modes: Env/config dir leakage, stale DB handle, pricing metadata drift.
- validation_or_tests: Test not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1387 `file` `packages/tui/src/tui.ts`
- cursor: `[_]`
- core_role: Core terminal UI rendering engine with diffing, native scrollback, overlays, input, image budget, resize handling, and cursor control.
- algorithmic_behavior: `Container` composes children; `TUI` maintains committed prefix/window state, stable segment reuse, SGR coalescing, cursor markers, overlay composition, resize viewport fast path, alt-screen modal rendering, and differential terminal writes. Key algorithms include `render()` at line 562 for containers, `coalesceAdjacentSgr()` line 725, `findCommittedPrefixResync()` line 829, `TUI.render()` line 1090, `requestRender()` line 1791, `#doRender()` line 2421, and diff emit around line 3343.
- inputs_outputs_state: Inputs are components, terminal dimensions/input bytes, render requests, resize events, overlay options, image budget. Outputs are terminal escape sequences, frame/window state, committed rows, focus and cursor state.
- gates_or_invariants: Committed rows are immutable; live-region boundaries cap scrollback commits; width changes force re-render; overlays do not mutate normal-screen accounting; resize viewport paints are throwaway and must not advance commit ledger.
- dependencies_and_callers: Depends on terminal abstraction, `pi-tui` utils, image budget, deccara, keys, loop watchdog. Called by coding-agent interactive UI and tests.
- edge_cases_or_failure_modes: Multiplexer resize races, Ghostty initial image drops, ConPTY post-paint drift, ANSI width miscount, stale committed prefix, cursor marker leakage, overlay focus conflicts.
- validation_or_tests: Covered by TUI tests and coding-agent mode/component tests; no tests run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1417 `file` `packages/tui/test/keys.test.ts`
- cursor: `[_]`
- core_role: Contract tests for terminal key parsing/matching and printable extraction.
- algorithmic_behavior: Tests `matchesKey`, `parseKey`, Kitty protocol handling, and `extractPrintableText`. Describe blocks at lines 4, 108, 180.
- inputs_outputs_state: Inputs are raw escape/key sequences and expected key specs. Outputs are parsed key objects/booleans/printable text.
- gates_or_invariants: Modifier matching and Kitty release handling must be stable; printable extraction must not treat control sequences as text.
- dependencies_and_callers: Depends on `pi-tui/keys`.
- edge_cases_or_failure_modes: Kitty protocol toggles, releases, composed modifiers, printable/control ambiguity.
- validation_or_tests: Test not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1447 `file` `packages/tui/test/select-list.test.ts`
- cursor: `[_]`
- core_role: Contract tests for SelectList rendering, filtering, wrapping, alignment, and scrollbar.
- algorithmic_behavior: Renders lists under widths/maxVisible settings and asserts no embedded newlines, aligned descriptions, custom truncation, search filtering/status, right-edge scrollbar, and wrapped item behavior. Describe at line 54.
- inputs_outputs_state: Inputs are list items, search terms, widths, theme/keybindings. Outputs are rendered rows and visible-width positions.
- gates_or_invariants: Descriptions align across truncated primary text; rendered row count respects maxVisible; scrollbar appears only on overflow; wrapped rows preserve indentation.
- dependencies_and_callers: Depends on `SelectList`, keybindings, visible-width utility.
- edge_cases_or_failure_modes: Very long primary text, filtered list without overflow, wrapped selected item, narrow width.
- validation_or_tests: Test not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1477 `file` `packages/typescript-edit-benchmark/src/tasks.ts`
- cursor: `[_]`
- core_role: Task loader and fixture validator for edit benchmark fixtures.
- algorithmic_behavior: Recursively lists files, loads each task from fixture directories, titleizes IDs, reads instructions/metadata, maps initial/expected files, and validates fixture structural issues. Key functions: `listFiles()` line 42, `loadTasksFromDir()` line 64, `validateFixturesFromDir()` line 114, `parseTaskMetadata()` line 212.
- inputs_outputs_state: Inputs are fixture root paths and metadata JSON. Outputs are `EditTask[]` and validation issue lists.
- gates_or_invariants: Tasks must include instructions, initial and expected directories; files are sorted; metadata fields are parsed only if valid type.
- dependencies_and_callers: Used by benchmark CLI/runner/generator tests.
- edge_cases_or_failure_modes: Missing directories, empty expected set, malformed metadata, hidden files, nested path sorting.
- validation_or_tests: Covered by benchmark verify/runner tests; not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1507 `file` `packages/utils/src/sanitize-text.ts`
- cursor: `[_]`
- core_role: Bun-native text sanitizer replacing former native sanitizer.
- algorithmic_behavior: `sanitizeText()` line 23 ensures well-formed strings and removes replacement chars created by malformed UTF-16; `sanitizeWellFormedText()` strips control characters except allowed whitespace/escape handling; `escapeHtml()` escapes `&`, `<`, `>`.
- inputs_outputs_state: Inputs are arbitrary strings; outputs are sanitized text or HTML-escaped strings.
- gates_or_invariants: Preserve valid text fast path; remove disallowed controls; avoid double work when no escapable chars.
- dependencies_and_callers: Used by utils consumers, TUI/log/rendering paths.
- edge_cases_or_failure_modes: Lone surrogates, replacement char removal, ANSI/control bytes, HTML injection chars.
- validation_or_tests: Covered by utils tests; no tests run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1537 `file` `packages/utils/test/stream.test.ts`
- cursor: `[_]`
- core_role: Contract tests for stream utilities and SSE parsing.
- algorithmic_behavior: Builds byte streams and async collectors to test stream reading, line reading, SSE event parsing with CRLF/chunk splits/trailing events, and large one-byte chunk behavior. SSE assertions appear around lines 255-314.
- inputs_outputs_state: Inputs are `ReadableStream<Uint8Array>` chunks. Outputs are collected text/lines/SSE events.
- gates_or_invariants: SSE parser must handle split frames, CRLF, missing final blank line, and many tiny chunks.
- dependencies_and_callers: Depends on utils stream helpers.
- edge_cases_or_failure_modes: Decoder boundary splits, trailing event without terminator, large chunk counts.
- validation_or_tests: Test not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1567 `file` `python/robomp/src/queue.py`
- cursor: `[_]`
- core_role: Durable async worker pool draining GitHub/webhook events into robomp task coroutines.
- algorithmic_behavior: `WorkerPool` claims unique events, gates concurrency through `SlotPool` when root or semaphore otherwise, resets stuck running rows, tracks inflight tasks, supports operator cancellation, graceful shutdown drain/kill, periodic native-cache GC, retry scheduling, and event/action dispatch to task handlers. Core methods: `start()` line 92, `stop()` line 104, `_dispatch_loop()` line 189, `_claim_next_unique()` line 210, `_run_event()` line 271, `_dispatch()` line 342.
- inputs_outputs_state: Inputs are `Settings`, SQLite `Database`, GitHub backend, sandbox manager, queue rows, cancellation requests. Outputs are DB status transitions (`done`, `failed`, retry), spawned task execution, slot cleanup, logs.
- gates_or_invariants: Same issue key cannot run concurrently; shutdown-interrupted events remain running for recovery; retries obey max/delay; slot UIDs are reaped/released.
- dependencies_and_callers: Depends on `robomp.tasks`, cancellation contextvars, sandbox/slot pool/db/github modules. Called by robomp service runner.
- edge_cases_or_failure_modes: Duplicate hook pop in `cancel_event`, task crash during drain, slot acquisition before shutdown, DB claim/requeue races, cache GC exceptions, unsupported event/action no-op.
- validation_or_tests: Not run; behavior likely covered by robomp integration tests outside assigned scope.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1597 `directory` `crates/pi-shell/src/minimizer/filters`
- cursor: `[_]`
- core_role: Rust command-output minimizer filter set for compressing shell/tool output while preserving actionable diagnostics.
- algorithmic_behavior: Contains filters for Bun, Cargo, Go, Python, JVM/Gradle/Maven, Docker, Git/GH/GLab/Graphite, package managers, lint, cloud/SQL, listings/source outlines, system commands, node tests, Ruby, C++, binary tools, plus fixtures. Each module provides `supports`/`filter` functions and helpers to strip noise, group failures, summarize successes, compact listings, redact sensitive env values, and preserve diagnostics.
- inputs_outputs_state: Inputs are `MinimizerCtx`, command/program/subcommand, raw stdout/stderr text, exit code. Outputs are `MinimizerOutput` compact text with retained failure/signal lines.
- gates_or_invariants: Preserve raw/machine-readable modes where configured; keep errors/failures/summaries; avoid leaking sensitive env values; treat success differently from failure; fixtures anchor expected output shapes.
- dependencies_and_callers: Called by `pi-shell` minimizer dispatcher; depends on primitives and context types.
- edge_cases_or_failure_modes: Localized Maven output, JSON/NDJSON package trees, noisy progress bars, multi-failure test logs, path listings with NUL output, SQL table truncation, Playwright numbered failures.
- validation_or_tests: Many module-local Rust tests plus assigned `node_tests.rs`; not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1627 `directory` `packages/coding-agent/src/goals/tools`
- cursor: `[_]`
- core_role: Goal management tool surface exposed to agent/tool runtime.
- algorithmic_behavior: `goal-tool.ts` defines arktype schema, validates create params, invokes goal session operations, builds goal response details, renders status/badges, and describes operations. Key sections: schema line 17, `GoalTool` line 58, renderer line 164.
- inputs_outputs_state: Inputs are tool params (`op`, objective, token budget, goal IDs/status). Outputs are `GoalToolResponse`, detail metadata, and TUI-rendered goal status.
- gates_or_invariants: Create requires non-empty objective; token budget parsed/validated; renderer colors follow goal status.
- dependencies_and_callers: Depends on `pi-agent-core` tool interface, goal session/status types, theme/TUI rendering.
- edge_cases_or_failure_modes: Unknown op, invalid token budget, missing goal session, stale status.
- validation_or_tests: Goal tool likely covered by workflow/goal tests; no tests run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1657 `directory` `packages/stats/src/client/app`
- cursor: `[_]`
- core_role: React application shell for the local stats dashboard.
- algorithmic_behavior: `AppLayout.tsx` composes nav/top/content layout; `NavRail.tsx` switches active sections; `RangeControl.tsx` controls time range; `SyncButton.tsx` triggers sync and tracks loading/completion; `ThemeToggle.tsx` cycles theme preferences; `routes.ts` defines app route metadata.
- inputs_outputs_state: Inputs are active section/range/theme/sync callbacks. Outputs are React elements and callback invocations.
- gates_or_invariants: Theme toggle cycles deterministic preference order; sync button must not double-submit during active sync; nav selection emits section changes.
- dependencies_and_callers: Used by stats client root, depends on React and dashboard components.
- edge_cases_or_failure_modes: Sync callback errors, invalid active route, theme preference mismatch.
- validation_or_tests: UI tests not inspected; no tests run.
- skip_candidate: `yes: dashboard UI shell, limited core algorithm content`

### OH_MY_HUMANIZE_MAIN-HZ-1687 `file` `packages/ai/src/auth-broker/client.ts`
- cursor: `[_]`
- core_role: Client for remote auth broker wire protocol and credential store integration.
- algorithmic_behavior: Defines arktype wire schemas, broker request/response types, SSE parsing via `readSseEvents`, remote credential fetch/refresh flows, credential mapping, and error handling for broker replies.
- inputs_outputs_state: Inputs are broker URL/fetch implementation, provider/account identifiers, auth credential records, SSE events. Outputs are credentials, remote store snapshots, refresh sentinel handling, or errors.
- gates_or_invariants: Wire messages must schema-validate; remote errors map to explicit failures; SSE stream must finish with expected credential payload.
- dependencies_and_callers: Depends on `readSseEvents`, arktype, auth-storage types. Used by remote auth store tests and auth gateway.
- edge_cases_or_failure_modes: Broker timeout, malformed SSE JSON, missing credential fields, remote refresh sentinel, fetch rejection.
- validation_or_tests: Covered by auth-broker remote/wire tests; not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1717 `file` `packages/ai/src/dialect/qwen3.ts`
- cursor: `[_]`
- core_role: In-band tool-call dialect scanner/renderer for Qwen3 chat-template style.
- algorithmic_behavior: `Qwen3InbandScanner` incrementally scans `<think>` and `<tool_call>` tags, buffers partial JSON, repairs/parses tool calls, emits thinking/text/tool events, and render helpers output tool calls/results/transcripts. Scanner starts line 27; render helpers start line 203; definition line 229.
- inputs_outputs_state: Inputs are streaming text chunks, messages, tool calls/results. Outputs are dialect events, rendered transcript strings, parsed `ToolCall`s.
- gates_or_invariants: Must tolerate tag splits and partial JSON; tool-call IDs minted when absent; thinking/tool states must close correctly before outside text resumes.
- dependencies_and_callers: Depends on dialect coercion/rendering utilities, qwen3 prompt md, message types.
- edge_cases_or_failure_modes: Unterminated tags, malformed JSON args, overlapping suffixes, hallucinated tags inside text.
- validation_or_tests: Covered by in-band tool dialect tests; no tests run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1747 `file` `packages/ai/src/providers/openai-auth-headers.ts`
- cursor: `[_]`
- core_role: Authorization header helper for OpenAI-compatible providers.
- algorithmic_behavior: Defines model-authorization header API key constant, blocks configured Authorization header for official OpenAI/GitHub Copilot, detects existing Authorization case-insensitively, and sets Bearer header while removing prior variants.
- inputs_outputs_state: Inputs are provider ID, headers record, API key, override flag. Outputs are mutated headers or booleans.
- gates_or_invariants: Do not allow configured Authorization override for official `openai`/`github-copilot`; case-insensitive header cleanup; `overrideExisting=false` preserves existing auth.
- dependencies_and_callers: Used by OpenAI-compatible request builders.
- edge_cases_or_failure_modes: Mixed-case duplicate Authorization headers, empty API key, proxy providers needing custom headers.
- validation_or_tests: Covered by openai auth header precedence tests; not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1777 `file` `packages/ai/src/registry/fireworks.ts`
- cursor: `[_]`
- core_role: Provider registry entry and API-key login flow for Fireworks.
- algorithmic_behavior: Uses `createApiKeyLogin` with Fireworks settings URL, prompt text, placeholder, and models-endpoint validation; exports `fireworksProvider`.
- inputs_outputs_state: Inputs are OAuth/login callbacks and pasted API key. Outputs are validated API key and provider definition.
- gates_or_invariants: Validation must hit Fireworks models endpoint; provider ID/name stable.
- dependencies_and_callers: Depends on api-key login helper and provider registry.
- edge_cases_or_failure_modes: Empty key, validation endpoint error, missing prompt callback.
- validation_or_tests: Provider registry/login tests may cover; not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1807 `file` `packages/ai/src/registry/parallel.ts`
- cursor: `[_]`
- core_role: Provider registry entry and prompt-based API-key login flow for Parallel.
- algorithmic_behavior: Emits auth URL/instructions via `onAuth`, prompts for API key, respects abort signal after prompt, trims/rejects empty keys, and exports provider definition.
- inputs_outputs_state: Inputs are OAuth controller callbacks and signal. Outputs are API key string or errors.
- gates_or_invariants: Requires `onPrompt`; empty trimmed keys reject; aborted login rejects.
- dependencies_and_callers: Used by provider registry/login UI.
- edge_cases_or_failure_modes: User cancels after prompt, missing callback, whitespace key.
- validation_or_tests: Login tests not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1837 `file` `packages/ai/src/usage/openai-codex-reset.ts`
- cursor: `[_]`
- core_role: Parser/normalizer for OpenAI Codex usage reset/quota metadata.
- algorithmic_behavior: Extracts reset windows, premium request quotas, and usage limit metadata from Codex-specific response payloads/headers, mapping provider shapes to normalized usage reset information.
- inputs_outputs_state: Inputs are raw usage metadata/headers/response objects. Outputs are reset timestamps, quota counters, and normalized usage state.
- gates_or_invariants: Must distinguish absent metadata from zero quota; date parsing must be conservative; malformed values ignored rather than poisoning usage.
- dependencies_and_callers: Used by OpenAI Codex provider and usage display/tests.
- edge_cases_or_failure_modes: Missing headers, string/number mismatch, invalid timestamps, reset period rollover.
- validation_or_tests: Covered by `openai-codex-reset.test.ts` and usage tests; not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1867 `file` `packages/catalog/src/compat/anthropic.ts`
- cursor: `[_]`
- core_role: Anthropic compatibility resolver for catalog models.
- algorithmic_behavior: Builds resolved Anthropic compat by applying defaults and config overrides for thinking, tool schema, cache, streaming, and message constraints.
- inputs_outputs_state: Inputs are model/provider compat config. Outputs are `ResolvedAnthropicCompat`.
- gates_or_invariants: Required compat fields must be present after resolution; generated model configs must not leak undefined where providers expect defaults.
- dependencies_and_callers: Used by catalog compat resolution and Anthropic provider request shaping.
- edge_cases_or_failure_modes: Missing cache/tool flags, new Anthropic capability not represented, override conflict.
- validation_or_tests: Covered by Anthropic alignment/provider tests; not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1897 `file` `packages/catalog/src/wire/github-copilot.ts`
- cursor: `[_]`
- core_role: GitHub Copilot wire/capability helpers for catalog/provider integration.
- algorithmic_behavior: Parses/constructs Copilot model wire metadata such as premium multipliers, plan-tier behavior, initiator/vision flags, or endpoint classification for Copilot-compatible requests.
- inputs_outputs_state: Inputs are model specs, plan/account metadata, request context. Outputs are Copilot wire values/headers/metadata helpers.
- gates_or_invariants: Paid/free tier multiplier behavior must stay compatible; unknown models default safely; vision flag depends on actual image input.
- dependencies_and_callers: Used by Copilot provider headers/tests and catalog metadata.
- edge_cases_or_failure_modes: Enterprise Copilot domains, included zero-multiplier models, missing plan tier.
- validation_or_tests: Covered by `github-copilot-headers.test.ts`; not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1927 `file` `packages/coding-agent/src/capability/slash-command.ts`
- cursor: `[_]`
- core_role: Capability definition for file-based custom slash commands.
- algorithmic_behavior: Defines `SlashCommand` shape and `slashCommandCapability` with ID/display/key/extension ID and validation for name/path/content/level.
- inputs_outputs_state: Inputs are discovered markdown command records. Outputs are capability entries or validation error strings.
- gates_or_invariants: Level must be `user`, `project`, or `native`; name/path/content required; extension ID is `slash-command:<name>`.
- dependencies_and_callers: Used by capability discovery and slash command registry.
- edge_cases_or_failure_modes: Empty name/path, invalid source level, duplicate names handled by capability layer.
- validation_or_tests: Covered by slash-command/workflow tests; not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1957 `file` `packages/coding-agent/src/cli/setup-model-picker.ts`
- cursor: `[_]`
- core_role: Standalone TUI model picker lifecycle helper.
- algorithmic_behavior: Creates a promise resolver, mounts a model list into TUI, selects current model index, resolves on select/cancel, and starts/tears down UI.
- inputs_outputs_state: Inputs are available models/current model/TUI instance. Outputs are selected model ID or null.
- gates_or_invariants: Promise resolves once; current index honored when found; UI lifecycle starts with focus.
- dependencies_and_callers: Depends on TUI/select list model picker components.
- edge_cases_or_failure_modes: Empty model list, double resolution, cancel before start.
- validation_or_tests: Covered indirectly by setup/model picker UI tests if present; not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1987 `file` `packages/coding-agent/src/commands/install.ts`
- cursor: `[_]`
- core_role: CLI command for plugin/local install routing.
- algorithmic_behavior: `looksLikeLocalPath()` line 31 detects local paths by absolute/relative/path separators; `Install` command initializes theme and delegates plugin install action through `runPluginCommand`.
- inputs_outputs_state: Inputs are CLI args/flags/current cwd. Outputs are plugin command execution results and CLI exit behavior.
- gates_or_invariants: Local path detection must distinguish package names from filesystem paths; plugin CLI receives correct action/scope.
- dependencies_and_callers: Depends on `pi-utils/cli`, plugin CLI, theme init.
- edge_cases_or_failure_modes: Windows path separators, nonexistent path, scoped package names with slash.
- validation_or_tests: Plugin/install command tests cover parts; not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2017 `file` `packages/coding-agent/src/config/file-lock.ts`
- cursor: `[_]`
- core_role: Cooperative lockfile utility for serialized config writes.
- algorithmic_behavior: Computes `.lock` path, writes token/pid/time, reads/validates lock info, detects stale locks by pid/age, tries exclusive create, retries until timeout, and releases only matching token. Exports `withFileLock()` line 140 and testing internals.
- inputs_outputs_state: Inputs are target file path and lock options (`timeoutMs`, `pollMs`, `staleMs`). Outputs are release function or timeout error; lockfile side effects.
- gates_or_invariants: Existing live lock blocks; stale locks are removed; release must not delete another holder’s token.
- dependencies_and_callers: Depends on fs promises, `randomUUID`, logger, `isEnoent`. Used by settings/config persistence.
- edge_cases_or_failure_modes: Process death, PID reuse, lockfile JSON corruption, concurrent stale removal, release after stolen lock.
- validation_or_tests: Settings/file-lock tests likely cover; not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2047 `file` `packages/coding-agent/src/discovery/at-imports.ts`
- cursor: `[_]`
- core_role: Recursive `@path` import expander for prompt/discovery text.
- algorithmic_behavior: `expandAtImports()` line 64 recursively expands text segments up to depth 5, ignores imports inside fenced/inline code, resolves relative/tilde paths, strips trailing punctuation, reads files, and logs failures. Markdown segmentation starts line 201.
- inputs_outputs_state: Inputs are content, base dir/home, readFile capability, depth. Outputs are expanded content and included file text.
- gates_or_invariants: Max depth 5 prevents recursion; code fences/inline code are not expanded; paths normalize relative to current file/base.
- dependencies_and_callers: Used by capability/discovery loaders and prompt inclusion. Depends on `readFile` capability and logger.
- edge_cases_or_failure_modes: Cyclic imports, missing files, punctuation-adjacent paths, unterminated fences, inline code backticks.
- validation_or_tests: Discovery tests cover related surfaces; not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2077 `file` `packages/coding-agent/src/eval/backend.ts`
- cursor: `[_]`
- core_role: Eval backend interface and URL root resolver.
- algorithmic_behavior: Defines execution request/result/status interfaces and `resolveEvalUrlRoots()` line 65, deriving local protocol URL roots from tool session configuration.
- inputs_outputs_state: Inputs are eval language/code/cwd/session, timeout and local protocol options. Outputs are backend result objects and URL roots.
- gates_or_invariants: Backend implementations must return exit code/output/error/artifacts and status events consistently.
- dependencies_and_callers: Used by eval tool/runtime JS/Python/shell backends.
- edge_cases_or_failure_modes: Missing local protocol session, unsupported language, timeout semantics delegated to backend.
- validation_or_tests: Eval backend tests elsewhere; not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2107 `file` `packages/coding-agent/src/hindsight/backend.ts`
- cursor: `[_]`
- core_role: Memory backend adapter for hindsight/mnemopi integration in agent sessions.
- algorithmic_behavior: Starts backend, builds developer instructions, records prompt/session events, clears/enqueues memory work, injects pre-compaction context, schedules and installs primary memory state, rebuilds on scope changes, and flattens messages for recall. Core functions: `schedulePrimaryStateRebuild()` line 161, `installPrimaryState()` line 198, `rebuildPrimaryStateOnScopeChange()` line 276.
- inputs_outputs_state: Inputs are agent dir, settings, session messages/scope, prompts. Outputs are memory instructions/context, primary state updates, queued memory operations.
- gates_or_invariants: Scope equality checks prevent unnecessary rebuilds; primary state install is scheduled asynchronously; pre-compaction context must be bounded and relevant.
- dependencies_and_callers: Depends on mnemopi/hindsight modules, `AgentSession`, message types.
- edge_cases_or_failure_modes: Scope changes during rebuild, missing memory backend, stale queued work, flattening non-text/tool messages.
- validation_or_tests: Memory/settings tests cover parts; not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2137 `file` `packages/coding-agent/src/lsp/config.ts`
- cursor: `[_]`
- core_role: Language-server configuration resolver.
- algorithmic_behavior: Defines language/server config structures, default server command mappings, file extension/language matching, and config resolution/normalization for LSP startup.
- inputs_outputs_state: Inputs are settings/project config, file paths/languages. Outputs are resolved LSP server configs and language IDs.
- gates_or_invariants: Disabled/missing servers should not start; command/args/env mapping must remain deterministic; extension matching should be case/path safe.
- dependencies_and_callers: Used by coding-agent LSP manager/diagnostics.
- edge_cases_or_failure_modes: Unknown extension, missing binary, malformed config, conflicting language entries.
- validation_or_tests: LSP tests not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2167 `file` `packages/coding-agent/src/mcp/tool-cache.ts`
- cursor: `[_]`
- core_role: MCP tool inventory cache.
- algorithmic_behavior: Caches server/tool metadata with freshness/version checks, invalidation, and lookups so agent tool rebuilding can skip expensive MCP reloads.
- inputs_outputs_state: Inputs are MCP server/tool lists and cache keys. Outputs are cached tool snapshots or misses.
- gates_or_invariants: Cache invalidates on server/tool identity changes; stale entries must not be used for active tools.
- dependencies_and_callers: Used by MCP manager/session tool refresh.
- edge_cases_or_failure_modes: Server reconnect with same name but changed tools, duplicate tool names, stale descriptions.
- validation_or_tests: Covered by tool rebuild skip and MCP tests; not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2197 `file` `packages/coding-agent/src/modes/shared.ts`
- cursor: `[_]`
- core_role: Shared interactive mode helpers/constants.
- algorithmic_behavior: Provides common mode-level utility types/functions for rendering, session, or controller coordination.
- inputs_outputs_state: Inputs/outputs are shared mode values imported by controllers/components.
- gates_or_invariants: Shared helpers must remain dependency-light to avoid UI initialization cycles.
- dependencies_and_callers: Used by interactive mode components/controllers.
- edge_cases_or_failure_modes: Circular imports, stale shared constants.
- validation_or_tests: Mode tests cover consumers; not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2227 `file` `packages/coding-agent/src/session/session-listing.ts`
- cursor: `[_]`
- core_role: Fast session discovery, status derivation, and resume matching.
- algorithmic_behavior: Sanitizes names, formats ages, extracts text from content, derives status from tail messages/tool calls, scans JSONL session files with header/prefix parsing, parallelizes file collection by stride, sorts/filters sessions, and resolves resume arguments. Key functions: `parseSessionListHeader()` line 273, `scanSessionFile()` line 321, `collectSessionsFromFiles()` line 405, `listSessions()` line 502.
- inputs_outputs_state: Inputs are session dir/file storage, JSONL file content, resume arg, withStatus flag. Outputs are `SessionInfo[]`, derived names/status/timestamps, resolved session.
- gates_or_invariants: Malformed/incomplete session files degrade safely; worker count scales by file count; status from suffix/tail is conservative.
- dependencies_and_callers: Used by session selector, CLI resume, workflow slash-command tests.
- edge_cases_or_failure_modes: Huge session dirs, malformed JSON fragments, missing first user message, duplicate/similar names, tool-call tail status.
- validation_or_tests: Covered by session history/listing and workflow tests; not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2257 `file` `packages/coding-agent/src/stt/index.ts`
- cursor: `[_]`
- core_role: Barrel export for speech-to-text subsystem.
- algorithmic_behavior: Re-exports ASR client/protocol/downloader/models/controller/transcriber/wav modules; no local runtime algorithm.
- inputs_outputs_state: Compile-time export surface only.
- gates_or_invariants: Export paths must remain valid.
- dependencies_and_callers: Used by consumers importing STT package surface.
- edge_cases_or_failure_modes: Missing module or accidental export removal.
- validation_or_tests: Compilation would validate; not run.
- skip_candidate: `yes: re-export index only`

### OH_MY_HUMANIZE_MAIN-HZ-2287 `file` `packages/coding-agent/src/tools/approval.ts`
- cursor: `[_]`
- core_role: Tool approval request/decision helper.
- algorithmic_behavior: Models approval states, request payloads, policy gates, and conversion of user decisions into tool execution allow/deny outcomes.
- inputs_outputs_state: Inputs are tool calls, policy mode, approval decision. Outputs are approval requests/results and execution gate flags.
- gates_or_invariants: Denied approvals must prevent execution; auto-approved policies must still record reason/context.
- dependencies_and_callers: Used by tool execution/session runtime.
- edge_cases_or_failure_modes: Missing approval handler, stale decision after abort, policy mismatch.
- validation_or_tests: Tool approval tests not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2317 `file` `packages/coding-agent/src/tools/image-gen.ts`
- cursor: `[_]`
- core_role: Multi-provider image generation/edit tool implementation.
- algorithmic_behavior: Builds prompts from structured params (`assemblePrompt()` line 93), resolves image credentials/provider preference, loads input images from paths/URLs/data URLs, validates aspect ratios, builds OpenAI/OpenRouter/Gemini/Antigravity/xAI requests, parses SSE/image responses, saves generated images to temp paths, and renders tool summaries. Execution method starts around line 1040.
- inputs_outputs_state: Inputs are tool params, cwd, model registry/auth storage/fetch, optional input images, abort signal. Outputs are generated image temp paths, inline image data, text summary, provider/model metadata, or errors.
- gates_or_invariants: Provider aspect-ratio support enforced; image data needs MIME type; OpenAI/xAI edit payloads distinguish text-only/single/multi-image; credentials searched in preference order.
- dependencies_and_callers: Depends on `pi-ai` auth/model registry, arktype, image metadata utils, temp files, prompts. Called by coding-agent tool system.
- edge_cases_or_failure_modes: Unsupported image URL content type, empty base64, missing API key, provider block reason, SSE parse failure, no image returned, invalid aspect ratio.
- validation_or_tests: Image tool/result tests cover pieces; no tests run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2347 `file` `packages/coding-agent/src/tools/search.ts`
- cursor: `[_]`
- core_role: Core local/internal search tool with rg/native search, archive path resolution, virtual resource search, result rendering, and preview compaction.
- algorithmic_behavior: Parses path specs/ranges, resolves archive/internal virtual resources, builds line indexes, supports multiline regex, merges grep/virtual results, records seen lines, formats grouped display with context and budgeted previews. Key functions: `toPathList()` line 81, `parsePathSpecs()` line 119, `searchVirtualResources()` line 483, `SearchTool.execute()` line 676, render helpers line 1323 onward.
- inputs_outputs_state: Inputs are pattern, paths, include/exclude/range options, cwd/session, internal resources, max counts. Outputs are tool result text/details, match groups, previews, and seen-line tracking.
- gates_or_invariants: Ranges merge by absolute path; context lines respect allowed ranges; max counts cap output; virtual search uses safe regex compilation and multiline handling.
- dependencies_and_callers: Depends on native grep/search utilities, tool session, render utils, archive/internal resource expansion.
- edge_cases_or_failure_modes: Invalid regex, archive path mismatch, multiline line-number mapping, too many matches, inaccessible files, duplicated results from rg+virtual merge.
- validation_or_tests: Search/tool path tests cover related behavior; not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2377 `file` `packages/coding-agent/src/tui/width-aware-text.ts`
- cursor: `[_]`
- core_role: TUI component that renders text with parent-width awareness.
- algorithmic_behavior: Wraps `Text` and padding calculations to choose/truncate/wrap content based on render width.
- inputs_outputs_state: Inputs are text/options and render width. Outputs are rendered row strings.
- gates_or_invariants: Width calculation must account for padding and visible width, not raw string length.
- dependencies_and_callers: Depends on `pi-tui` `Text`, `getPaddingX`, component interface.
- edge_cases_or_failure_modes: Narrow widths, ANSI/styled text, zero/negative content width.
- validation_or_tests: UI rendering tests cover consumers; not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2407 `file` `packages/coding-agent/src/web/kagi.ts`
- cursor: `[_]`
- core_role: Kagi web search API adapter.
- algorithmic_behavior: Builds Kagi search request bodies, maps recency to date filters, parses error payloads into `KagiApiError`, collects direct/related sources, and runs authenticated search with hard timeout. Key functions: `parseKagiErrorResponse()` line 136, `buildRequestBody()` line 204, `searchWithKagi()` line 237.
- inputs_outputs_state: Inputs are query, recency/domain/options, auth storage/fetch, timeout. Outputs are normalized search results/sources or typed API errors.
- gates_or_invariants: Auth must use Kagi credentials; HTTP errors classify with useful messages; source collection avoids empty items.
- dependencies_and_callers: Depends on `withAuth`, fetch, search provider utils. Used by web search provider selection.
- edge_cases_or_failure_modes: Non-JSON error body, missing API key, timeout, empty search data, malformed related questions.
- validation_or_tests: Web search tests not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2437 `file` `packages/coding-agent/src/workflow/session-runtime.ts`
- cursor: `[_]`
- core_role: Runtime host adapter for workflow nodes inside an agent session.
- algorithmic_behavior: Creates node runtime host for agent/script/human/review nodes, delegates to injected runners, wraps eval scripts with context, parses structured activation outputs from JSON or last JSON line, bounds summaries by byte budget, maps task artifacts, and parses review verdicts/gates. Key functions: `createSessionWorkflowRuntimeHost()` line 104, `runEvalWorkflowScript()` line 201, `parseStructuredActivationOutput()` line 319, `parseReviewTaskOutput()` line 484.
- inputs_outputs_state: Inputs are workflow node activation data, script code/language/context, runner outputs, gates/fallback verdicts. Outputs are `WorkflowActivationOutput` or `WorkflowReviewNodeOutput`.
- gates_or_invariants: Missing adapters throw `WorkflowNodeRuntimeError`; nonzero script/task exit throws; review nodes must return a verdict; summaries are byte-bounded and artifacts deduplicated.
- dependencies_and_callers: Depends on workflow definition/state/node-runtime/display modules. Used by workflow slash-command runtime and tests.
- edge_cases_or_failure_modes: Top-level return wrapping, invalid structured JSON, object summary fallback, gate prefix/suffix parsing, oversized multibyte summaries, missing verdict.
- validation_or_tests: Covered by workflow session-runtime tests and long slash-command tests; not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2467 `file` `packages/coding-agent/test/core/python-executor-per-call.test.ts`
- cursor: `[_]`
- core_role: Contract tests for per-call Python execution lifecycle/cancellation.
- algorithmic_behavior: Stubs `PythonKernel.start`, creates cancellation errors, rejects startup on abort/timeout, and verifies `executePython` starts per call and cleans up. Helpers at lines 18, 24; describe at line 51.
- inputs_outputs_state: Inputs are code snippets, kernel start options, abort/timeout signals. Outputs are execution results/errors and kernel lifecycle assertions.
- gates_or_invariants: Startup cancellation must propagate as abort/timeout; per-call execution should not reuse invalid kernel.
- dependencies_and_callers: Depends on Python executor and `PythonKernel`.
- edge_cases_or_failure_modes: Abort before start, timeout on startup, cleanup after failure.
- validation_or_tests: Test not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2497 `file` `packages/coding-agent/test/discovery/github-copilot.test.ts`
- cursor: `[_]`
- core_role: Contract tests for GitHub Copilot user-global discovery surfaces.
- algorithmic_behavior: Writes temp Copilot instruction/rule files, loads capabilities, resets active rules, and verifies discovery of context files, instructions, prompts, and rules through Copilot env dirs. Describe begins line 35.
- inputs_outputs_state: Inputs are `COPILOT_HOME`, `COPILOT_CUSTOM_INSTRUCTIONS_DIRS`, temp files. Outputs are loaded capability records and rule protocol behavior.
- gates_or_invariants: Env is restored; disabled providers honored; discovered files must map to correct capability level/source.
- dependencies_and_callers: Depends on capability registry, GitHub discovery, rule protocol.
- edge_cases_or_failure_modes: Missing env dirs, duplicate files, disabled providers, stale active rule cache.
- validation_or_tests: Test not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2527 `file` `packages/coding-agent/test/helpers/fetch-mock.ts`
- cursor: `[_]`
- core_role: Shared test helper for typed fetch mocks.
- algorithmic_behavior: Wraps a handler into `FetchImpl` and global `fetch` compatible functions; exports `FetchInput`.
- inputs_outputs_state: Inputs are mock handler functions; outputs are fetch-compatible functions.
- gates_or_invariants: Signature must match `FetchImpl`/global fetch enough for tests.
- dependencies_and_callers: Used by coding-agent web/provider tests.
- edge_cases_or_failure_modes: Handler throwing, Request vs URL/string inputs.
- validation_or_tests: Helper only.
- skip_candidate: `yes: test helper adapter, not core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-2557 `file` `packages/coding-agent/test/modes/magic-keywords.test.ts`
- cursor: `[_]`
- core_role: Contract tests for magic keyword detection/highlighting.
- algorithmic_behavior: Initializes theme, tests `highlightMagicKeywords` and `hasMagicKeyword` over word boundaries, casing, and prose/code handling. Describe blocks at lines 10 and 67.
- inputs_outputs_state: Inputs are prompt text strings. Outputs are highlighted strings and booleans.
- gates_or_invariants: Keywords should only match intended standalone prose, preserving visible text.
- dependencies_and_callers: Depends on mode magic-keyword utilities/theme.
- edge_cases_or_failure_modes: Embedded/path words, code spans, punctuation boundaries.
- validation_or_tests: Test not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2587 `file` `packages/coding-agent/test/session/session-history-format.test.ts`
- cursor: `[_]`
- core_role: Contract tests for formatting session history markdown.
- algorithmic_behavior: Builds mixed message arrays and verifies `formatSessionHistoryMarkdown` output shape/content. Helper at line 14; describe at line 58.
- inputs_outputs_state: Inputs are user/assistant/tool messages. Outputs are markdown transcript strings.
- gates_or_invariants: Formatting must preserve roles/order and represent tool content without corrupting markdown.
- dependencies_and_callers: Depends on session-history-format module.
- edge_cases_or_failure_modes: Non-string content, tool-only messages, empty history.
- validation_or_tests: Test not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2617 `file` `packages/coding-agent/test/task/executor-wall-clock.test.ts`
- cursor: `[_]`
- core_role: Contract tests for task subprocess wall-clock max runtime.
- algorithmic_behavior: Mocks `createAgentSession`, creates hanging session, runs `runSubprocess`, and verifies timeout abort/cleanup based on `task.maxRuntimeMs`. Helpers at lines 29 and 62; describe at line 71.
- inputs_outputs_state: Inputs are task definitions/settings/model registry stubs. Outputs are subprocess result/error and session abort behavior.
- gates_or_invariants: Wall-clock limit must fire even when session hangs; EventBus/session listeners cleaned up.
- dependencies_and_callers: Depends on task executor and SDK module spy.
- edge_cases_or_failure_modes: Hanging session, fake timers, abort propagation.
- validation_or_tests: Test not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2647 `file` `packages/coding-agent/test/tools/bash-sixel-render.test.ts`
- cursor: `[_]`
- core_role: Contract tests for bash tool sixel/image rendering.
- algorithmic_behavior: Builds bash tool render inputs and verifies sixel/image output rendering paths, truncation, and display behavior.
- inputs_outputs_state: Inputs are tool outputs with sixel/image sequences and settings. Outputs are rendered TUI rows/details.
- gates_or_invariants: Binary/image escape sequences must not corrupt terminal rendering; text fallback remains bounded.
- dependencies_and_callers: Depends on bash tool renderer and TUI image components.
- edge_cases_or_failure_modes: Partial sixel, disabled image display, long output, ANSI mixing.
- validation_or_tests: Test not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2677 `file` `packages/coding-agent/test/tools/grouped-file-output.test.ts`
- cursor: `[_]`
- core_role: Contract tests for grouped file output formatting/classification.
- algorithmic_behavior: Tests `formatGroupedFiles`, `classifyGroupedLines`, and `groupLineIndicesByBlank` in describe blocks at lines 8, 38, 70.
- inputs_outputs_state: Inputs are file/line groups and raw lines. Outputs are formatted grouped output and classification/group arrays.
- gates_or_invariants: Blank-line grouping and file classifications must be stable for renderer consumers.
- dependencies_and_callers: Depends on tool render-utils.
- edge_cases_or_failure_modes: Empty groups, multiple blank runs, ambiguous line prefixes.
- validation_or_tests: Test not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2707 `file` `packages/coding-agent/test/tools/root-path-alias.test.ts`
- cursor: `[_]`
- core_role: Contract tests for tool path root alias resolution.
- algorithmic_behavior: Creates test tool sessions/temp cwd, calls `resolveToCwd` and tools using root alias, and verifies path behavior. Helpers at lines 10 and 21; describe at line 28.
- inputs_outputs_state: Inputs are cwd, tool path args, settings/session overrides. Outputs are resolved paths and tool result text.
- gates_or_invariants: Root alias must resolve inside cwd/root as intended and avoid accidental home/path escape.
- dependencies_and_callers: Depends on createTools, ToolSession, path utils.
- edge_cases_or_failure_modes: Relative paths, alias path separators, nonexistent files.
- validation_or_tests: Test not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2737 `file` `packages/coding-agent/test/utils/enhanced-paste.test.ts`
- cursor: `[_]`
- core_role: Contract tests for enhanced paste OSC packet parser/controller.
- algorithmic_behavior: Builds OSC 5522 packets and tests `EnhancedPasteController` metadata/payload parsing, BEL/ST terminators, and state behavior. Packet helper at line 8; describe at line 12.
- inputs_outputs_state: Inputs are terminal escape packet strings. Outputs are parsed paste events/controller state.
- gates_or_invariants: Must distinguish metadata from payload and handle both terminators without leaking raw OSC to editor text.
- dependencies_and_callers: Depends on enhanced paste utility.
- edge_cases_or_failure_modes: Unterminated packets, split packets, missing payload, malformed metadata.
- validation_or_tests: Test not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2767 `file` `packages/coding-agent/test/workflow/slash-command.test.ts`
- cursor: `[_]`
- core_role: Large integration-style contract suite for `/workflow` slash command parsing, execution, persistence, graph display, review gates, artifacts, resume, and UI/runtime integration.
- algorithmic_behavior: Builds temp dirs, runtime hosts, TUI runtime, workflow definitions, checkpoint waiters, graph previews, and many test cases under `/workflow slash command` starting line 289. Helpers for artifact and freeze definitions are near lines 5991 onward.
- inputs_outputs_state: Inputs are workflow markdown/YAML definitions, fake sessions, tool/session runtimes, models, plugin/marketplace managers, graph state. Outputs are persisted checkpoints, graph views, activation state, node outputs, slash-command responses.
- gates_or_invariants: DAG execution order, freeze/resume state, review gate verdict parsing, artifact references, human/script/agent node adapters, and checkpoint persistence must remain stable.
- dependencies_and_callers: Depends on workflow parser/runtime/store, slash command registries, session listing, session runtime, shell script runner.
- edge_cases_or_failure_modes: Interrupted workflow, missing adapters, malformed definition, failed review verdict, stale checkpoint, graph connector rendering.
- validation_or_tests: Test not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2797 `file` `packages/mnemopi/src/core/extraction.ts`
- cursor: `[_]`
- core_role: Fact extraction engine for mnemopi memory ingestion.
- algorithmic_behavior: Reads env/runtime flags, builds extraction prompt, strips code fences, normalizes facts, parses JSON/line output, heuristic-extracts facts from prose, optionally calls host/local LLM, tracks diagnostics, and exposes safe wrapper. Key functions: `buildExtractionPrompt()` line 75, `parseFacts()` line 94, `heuristicExtractFacts()` line 160, `extractFacts()` line 235.
- inputs_outputs_state: Inputs are text, detected language, env/options, LLM output. Outputs are normalized fact strings and diagnostic counters.
- gates_or_invariants: Empty input returns empty; duplicate/blank facts removed; host LLM can be disabled; safe wrapper catches failures.
- dependencies_and_callers: Depends on diagnostics, LLM backends, runtime options. Called by BeamMemory extraction paths.
- edge_cases_or_failure_modes: Malformed JSON/fenced LLM output, disabled LLM, host backend failure, overly short heuristic sentences.
- validation_or_tests: Covered by extraction tests; not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2827 `file` `packages/mnemopi/src/util/datetime.ts`
- cursor: `[_]`
- core_role: Date/time parsing and temporal decay utility for mnemopi ranking.
- algorithmic_behavior: Parses ISO/date-only strings as UTC, normalizes dates, caches parsed timestamps, outputs UTC ISO, computes exponential recency decay and temporal boost. Key functions: `parseIsoDateTimeUtc()` line 10, `parseTsFast()` line 31, `recencyDecay()` line 48, `temporalBoost()` line 63.
- inputs_outputs_state: Inputs are string/Date/null query times, memory timestamps, halflife. Outputs are `Date`, ISO string, numeric decay/boost.
- gates_or_invariants: Date-only is UTC; cache bounded by LRU; invalid parsing behavior follows `Date`.
- dependencies_and_callers: Depends on config halflife and LRU cache. Used by memory ranking/recall.
- edge_cases_or_failure_modes: Missing timezone, invalid date string, future timestamps, cache churn.
- validation_or_tests: Mnemopi tests may cover; not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2857 `file` `packages/tui/src/components/truncated-text.ts`
- cursor: `[_]`
- core_role: TUI text component for width-bounded truncation.
- algorithmic_behavior: Renders text to visible-width limit with ellipsis/truncation while preserving component contract.
- inputs_outputs_state: Inputs are text/style/options and width. Outputs are rendered line array.
- gates_or_invariants: Must use visible width rather than code-unit length; narrow widths must not overflow.
- dependencies_and_callers: Depends on TUI text/width utils.
- edge_cases_or_failure_modes: ANSI text, wide Unicode, width zero/one.
- validation_or_tests: TUI/component tests cover rendering; not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2887 `directory` `packages/coding-agent/src/markit/converters/pdf`
- cursor: `[_]`
- core_role: PDF-to-Markdown conversion pipeline for markit.
- algorithmic_behavior: `extract.ts` loads MuPDF, extracts text boxes, segments, images, content stream drawing ops, and page content; `columns.ts` detects multi-column layout; `grid.ts` detects table grids; `headers.ts` strips repeated headers/footers; `render.ts` converts tables/free text/images to Markdown; `index.ts` orchestrates page processing through `PdfConverter`.
- inputs_outputs_state: Inputs are PDF bytes and converter options. Outputs are markdown text, image blocks/regions, tables, page content structures.
- gates_or_invariants: Thin rects become line segments only under aspect/thickness thresholds; repeated headers require page/min-consecutive thresholds; table rendering escapes pipes; image regions require minimum area.
- dependencies_and_callers: Depends on MuPDF package, markit converter interface, PDF content stream parsing.
- edge_cases_or_failure_modes: Multi-column ordering, sparse shifted tables, page numbers, full-width ASCII, nested graphics state/CTM parsing, image crop/render failures.
- validation_or_tests: Markit PDF tests not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2917 `file` `crates/pi-shell/src/minimizer/filters/node_tests.rs`
- cursor: `[_]`
- core_role: Rust minimizer filter for Node/Jest/Vitest/Playwright-style test output.
- algorithmic_behavior: `filter()` line 6 drops passed lines on success or keeps failures only on failure; helpers classify summary/noise/pass/failure blocks, error context, and Playwright numbered failures. Tests start line 212.
- inputs_outputs_state: Inputs are raw test output and exit code. Outputs are compacted output preserving summaries/failures.
- gates_or_invariants: Passing noise removed; failure blocks and context retained; empty compaction falls back to original where needed.
- dependencies_and_callers: Called by minimizer dispatcher; uses minimizer primitives.
- edge_cases_or_failure_modes: Multiple failure blocks, numbered Playwright failures, summary-only failures, noisy pass lines mixed with stack traces.
- validation_or_tests: Module-local Rust tests present; not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2947 `file` `packages/ai/src/utils/schema/compatibility.ts`
- cursor: `[_]`
- core_role: JSON schema compatibility transformer for provider-specific tool schema restrictions.
- algorithmic_behavior: Normalizes/dereferences schemas, enforces/relaxes strictness, removes unsupported constructs, handles unions/enums/additionalProperties, and maps schema shapes to target provider compatibility modes.
- inputs_outputs_state: Inputs are JSON/Zod/Ark schemas and compatibility options. Outputs are transformed JSON schema and warnings/metadata.
- gates_or_invariants: Must preserve semantic required fields where possible; provider-incompatible schema constructs are rewritten deterministically; strict mode must not leak impossible schemas.
- dependencies_and_callers: Used by provider request builders and schema tests.
- edge_cases_or_failure_modes: Recursive `$ref`, `anyOf`/`oneOf` unions, nullable optional fields, empty object schemas, unsupported formats.
- validation_or_tests: Covered by schema compatibility/strict/wire tests; not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2977 `file` `packages/coding-agent/src/cli/gallery-fixtures/memory.ts`
- cursor: `[_]`
- core_role: Static gallery fixture data for memory/hindsight UI demos.
- algorithmic_behavior: Exports `memoryFixtures` object with prebuilt gallery scenarios; no dynamic algorithm.
- inputs_outputs_state: Inputs none at runtime beyond import; outputs fixture definitions.
- gates_or_invariants: Fixture shape must satisfy `GalleryFixture`.
- dependencies_and_callers: Used by CLI gallery/demo commands.
- edge_cases_or_failure_modes: Fixture drift against type/schema.
- validation_or_tests: Type check would validate; not run.
- skip_candidate: `yes: static fixture data, not core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3007 `file` `packages/coding-agent/src/edit/apply-patch/parser.ts`
- cursor: `[_]`
- core_role: Parser for Codex `*** Begin Patch` apply_patch envelope into single-file patch inputs.
- algorithmic_behavior: Strips optional heredoc wrapper, validates begin/end markers, parses add/delete/update/move hunks, preserves update diff body, supports streaming preview mode that tolerates missing end markers and incomplete hunks. Main parser at lines 37 and 46.
- inputs_outputs_state: Inputs are patch envelope text and streaming flag. Outputs are `PatchInput[]` with op/path/rename/diff or `ParseError`.
- gates_or_invariants: Non-streaming requires exact begin/end markers; add-file lines must start `+`; update hunks cannot be empty; line numbers are tracked for errors.
- dependencies_and_callers: Depends on edit diff `ParseError` and patch mode types. Used by apply_patch tool and streaming preview.
- edge_cases_or_failure_modes: Blank separators, heredoc quoting, missing diff, unknown hunk header, partial streamed update.
- validation_or_tests: Covered by edit streaming preview tests; not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3037 `file` `packages/coding-agent/src/eval/py/kernel.ts`
- cursor: `[_]`
- core_role: Managed Python kernel subprocess for eval execution.
- algorithmic_behavior: Ensures runner script, probes availability, starts Python subprocess, initializes cwd/env, sends JSON line execution requests, tracks pending executions, handles abort/timeout, interrupts/shuts down process, reads stdout/stderr frames, drains/flushes frames, and kills on budget expiry. Key methods: `PythonKernel` line 239, `execute()` line 336, `shutdown()` line 456, `#handleFrame()` line 617.
- inputs_outputs_state: Inputs are code, cwd/interpreter/env, timeout/abort signal. Outputs are `KernelExecuteResult`, display/status events, errors, shutdown result.
- gates_or_invariants: One pending execution per request ID; abort/timeout must settle promise once; subprocess exit aborts pending executions; initialization injects cwd/env safely.
- dependencies_and_callers: Used by Python eval executor/tool. Depends on Bun subprocess streams and runner script.
- edge_cases_or_failure_modes: Startup timeout, invalid JSON frames, subprocess exit mid-call, stderr backpressure, interrupt unsupported, deadline shorter than startup.
- validation_or_tests: Covered by Python executor per-call tests; not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3067 `file` `packages/coding-agent/src/extensibility/plugins/doctor.ts`
- cursor: `[_]`
- core_role: Plugin/system doctor checks and result formatter.
- algorithmic_behavior: Checks external tools (`sd`, `sg`, `git`) via `$which`, checks common API-key env vars, and formats status lines with theme icons and summary counts.
- inputs_outputs_state: Inputs are PATH and Bun env. Outputs are `DoctorCheck[]` and formatted text.
- gates_or_invariants: Missing tools/API keys are warnings, not hard errors; formatter counts ok/warnings/errors.
- dependencies_and_callers: Used by plugin doctor command/CLI.
- edge_cases_or_failure_modes: `$which` unavailable/path weirdness, env false positives, theme not initialized.
- validation_or_tests: Doctor tests not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3097 `file` `packages/coding-agent/src/modes/components/advisor-message.ts`
- cursor: `[_]`
- core_role: TUI renderer for advisor diagnostics/messages.
- algorithmic_behavior: Wraps note text with different first/subsequent widths, maps severity to UI colors, truncates note lines, and builds advisor message card. Core functions: `wrapVarying()` line 16, `createAdvisorMessageCard()` line 48.
- inputs_outputs_state: Inputs are advisor details/severity/theme. Outputs are TUI component/rendered card lines.
- gates_or_invariants: Collapsed notes capped; line width uses visible-width truncation; severity color defaults safely.
- dependencies_and_callers: Used by advisor UI in interactive mode.
- edge_cases_or_failure_modes: Long notes, unknown severity, narrow terminal.
- validation_or_tests: Advisor flag/UI tests cover parts; not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3127 `file` `packages/coding-agent/src/modes/components/late-diagnostics-message.ts`
- cursor: `[_]`
- core_role: TUI component for late diagnostics grouped by file.
- algorithmic_behavior: Accepts diagnostic file groups, formats diagnostics through shared renderer, applies language detection/theme, and renders collapsible/capped diagnostic output.
- inputs_outputs_state: Inputs are file path plus diagnostics arrays. Outputs are TUI container rows.
- gates_or_invariants: Empty diagnostics render nothing; multiple files grouped under headers; collapsed output caps with expansion behavior.
- dependencies_and_callers: Depends on `formatDiagnostics`, theme language utilities, TUI.
- edge_cases_or_failure_modes: Many diagnostics, unknown file language, long messages.
- validation_or_tests: Covered by late-diagnostics component tests; not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3157 `file` `packages/coding-agent/src/modes/components/ttsr-notification.ts`
- cursor: `[_]`
- core_role: TUI notification component for TTSR/rule suggestions.
- algorithmic_behavior: Renders matched rule notifications, caps collapsed rules at `MAX_COLLAPSED_RULES = 4`, and composes boxes/spacers/text with theme colors.
- inputs_outputs_state: Inputs are rule lists/expanded state. Outputs are TUI component rows.
- gates_or_invariants: Collapsed state must not render unbounded rule list; expanded state reveals more.
- dependencies_and_callers: Depends on rule types, TUI components, theme.
- edge_cases_or_failure_modes: No rules, long rule descriptions, narrow width.
- validation_or_tests: Component tests not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3187 `file` `packages/coding-agent/src/modes/setup-wizard/index.ts`
- cursor: `[_]`
- core_role: Setup wizard mode/component entrypoint.
- algorithmic_behavior: Coordinates setup wizard steps for model/auth/settings initialization and exposes wizard component/controller.
- inputs_outputs_state: Inputs are settings/model/auth state and user selections. Outputs are updated settings/auth choices and UI transitions.
- gates_or_invariants: Wizard must advance only with valid choices; cancellation leaves settings coherent.
- dependencies_and_callers: Used by CLI startup/setup flow.
- edge_cases_or_failure_modes: No provider selected, auth failure, terminal resize during wizard.
- validation_or_tests: Setup wizard tests not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3217 `file` `packages/coding-agent/src/tools/browser/registry.ts`
- cursor: `[_]`
- core_role: Browser/CDP handle registry for browser tools.
- algorithmic_behavior: Keys browser kinds, acquires/reuses handles, normalizes CDP URLs, opens Puppeteer or cmux browser handles, tracks ref counts/holds, releases/kills handles, and disposes browser process/client resources. Core functions: `acquireBrowser()` line 65, `openBrowserHandle()` line 90, `releaseBrowser()` line 197.
- inputs_outputs_state: Inputs are browser kind/options, cwd/user agent, abort signal. Outputs are `BrowserHandle`s, CDP sessions, process refs, registry map mutations.
- gates_or_invariants: Same kind key reuses handle; release decrements refs; kill option controls process teardown; CDP URL normalized.
- dependencies_and_callers: Depends on Puppeteer/core launch/attach utilities and cmux socket client. Used by browser tools.
- edge_cases_or_failure_modes: Stale CDP port, launch timeout, process kill failure, refcount leak, cmux disconnect.
- validation_or_tests: Browser registry tests not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3247 `file` `packages/coding-agent/src/web/scrapers/gitlab.ts`
- cursor: `[_]`
- core_role: Special web scraper/renderer for GitLab URLs.
- algorithmic_behavior: Parses GitLab repo/file/tree/issue/MR URLs, resolves project ID via API, renders repo/tree/file/issue/MR content to markdown/basic result, and dispatches handler by URL kind. Key functions: `parseGitLabUrl()` line 24, `renderGitLabRepo()` line 106, `renderGitLabIssue()` line 222, `handleGitLab()` line 324.
- inputs_outputs_state: Inputs are GitLab URLs, timeout, abort signal. Outputs are `RenderResult` markdown or null fallback.
- gates_or_invariants: Only supported GitLab URL shapes handled; API fetch timeout honored; JSON parse failures degrade.
- dependencies_and_callers: Depends on scraper type utilities and `tryParseJson`.
- edge_cases_or_failure_modes: Self-hosted paths, private repos, API 404/rate limit, branch/path ambiguity, MR vs issue URL parsing.
- validation_or_tests: Web scraper tests not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3277 `file` `packages/coding-agent/src/web/scrapers/readthedocs.ts`
- cursor: `[_]`
- core_role: Special web scraper for Read the Docs pages.
- algorithmic_behavior: Loads page, extracts documentation content via HTML-to-basic-markdown, builds normalized render result. Handler exported at line 6.
- inputs_outputs_state: Inputs are ReadTheDocs URL/fetch options. Outputs are markdown `RenderResult`.
- gates_or_invariants: Should prefer documentation body over navigation/chrome; timeout and signal passed through loader.
- dependencies_and_callers: Depends on scraper `types` utilities.
- edge_cases_or_failure_modes: Theme/layout variations, missing body content, private docs.
- validation_or_tests: Scraper tests not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3307 `file` `packages/coding-agent/src/workflow/__tests__/session-runtime.test.ts`
- cursor: `[_]`
- core_role: Unit tests for workflow session runtime output parsing and adapters.
- algorithmic_behavior: Builds workflow definitions for script/task/review/context/frozen-resource cases and asserts activation outputs, review verdict parsing, retry behavior, and context injection. Definition helpers appear around lines 261, 293, 317, 334.
- inputs_outputs_state: Inputs are fake runners and workflow definitions. Outputs are activation/review output assertions.
- gates_or_invariants: Structured JSON output, fallback summaries, gates, and context variables must parse consistently.
- dependencies_and_callers: Depends on `createSessionWorkflowRuntimeHost` and workflow state definitions.
- edge_cases_or_failure_modes: Invalid JSON, missing verdict, top-level return context wrapper, frozen resource context.
- validation_or_tests: Test not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3337 `file` `packages/coding-agent/test/modes/components/tree-selector-developer.test.ts`
- cursor: `[_]`
- core_role: Component test for tree selector developer-facing rendering behavior.
- algorithmic_behavior: Renders tree selector scenarios and checks developer details/branching display.
- inputs_outputs_state: Inputs are tree nodes and selected state. Outputs are rendered rows.
- gates_or_invariants: Developer metadata must not break tree alignment or selection rendering.
- dependencies_and_callers: Depends on tree selector component.
- edge_cases_or_failure_modes: Deep nesting, missing developer labels, narrow width.
- validation_or_tests: Test not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3367 `file` `packages/coding-agent/test/modes/utils/copy-targets.test.ts`
- cursor: `[_]`
- core_role: Contract tests for copy-target extraction from transcript content.
- algorithmic_behavior: Tests code block extraction, quote block extraction, last command extraction, and `buildCopyTargets` ordering/drill-down behavior. Describe blocks at lines 35, 49, 66, 94.
- inputs_outputs_state: Inputs are markdown messages, tool/eval command records, handoff context. Outputs are copy target trees with content/language metadata.
- gates_or_invariants: Code/quote blocks preserve document order; tool-only assistant turns skipped; fallback to handoff only when no assistant messages.
- dependencies_and_callers: Depends on copy target utilities.
- edge_cases_or_failure_modes: Quotes inside fenced code, single-block messages, interleaved code/quote, eval cell language.
- validation_or_tests: Test not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3397 `file` `packages/collab-web/src/components/shell/Banners.tsx`
- cursor: `[_]`
- core_role: Collaboration web shell banner/ended-session state component.
- algorithmic_behavior: Renders status banners for connecting/waiting/reconnecting phases and an alertdialog with rejoin/new-link actions for ended sessions; returns null for normal phase.
- inputs_outputs_state: Inputs are connection phase, ended reason, callbacks. Outputs are React nodes and button callback invocations.
- gates_or_invariants: Ended state uses alertdialog semantics; transient phases use `role=status`.
- dependencies_and_callers: Used by collab web shell.
- edge_cases_or_failure_modes: Null ended reason, callback missing behavior delegated by props, unknown phase returns null.
- validation_or_tests: UI component tests not run.
- skip_candidate: `yes: presentational state component, not core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3427 `file` `packages/collab-web/src/tool-render/tools/report-tool-issue.tsx`
- cursor: `[_]`
- core_role: Web renderer for `report_tool_issue` tool calls.
- algorithmic_behavior: Extracts `tool` and `report` args, renders invalid arg when both absent, truncates normalized summary to 80 chars, and renders note/result body.
- inputs_outputs_state: Inputs are tool args/result. Outputs are React summary/body nodes.
- gates_or_invariants: Missing both args is invalid; long report truncated; result text capped to four lines.
- dependencies_and_callers: Depends on collab web tool-render parts/util.
- edge_cases_or_failure_modes: Non-string args, huge result, whitespace-only report.
- validation_or_tests: Renderer tests not run.
- skip_candidate: `yes: renderer adapter, not core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3457 `file` `packages/stats/src/client/components/models-table-shared.tsx`
- cursor: `[_]`
- core_role: Shared stats table sparkline/model metric UI helpers.
- algorithmic_behavior: Exports chart themes/colors, builds line series styles, renders mini sparklines, formats model table metrics and trend charts with date formatting and chart.js.
- inputs_outputs_state: Inputs are model rows/time series/theme. Outputs are React chart/table cells.
- gates_or_invariants: Sparkline options must stay small/noninteractive; date labels formatted consistently; sorting indicators reflect state.
- dependencies_and_callers: Used by stats client model tables; depends on `date-fns`, lucide icons, chart.js React wrapper.
- edge_cases_or_failure_modes: Empty series, missing colors, invalid dates, tiny chart dimensions.
- validation_or_tests: Stats UI tests not run.
- skip_candidate: `yes: UI presentation helper, not core runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3487 `file` `packages/utils/src/vendor/mermaid-ascii/parser.ts`
- cursor: `[_]`
- core_role: Vendored Mermaid flowchart/state diagram parser for ASCII rendering.
- algorithmic_behavior: `parseMermaid()` dispatches to flowchart/state parsing, handles direction, subgraphs, styles/classes, nodes/shapes, arrows/labels, state transitions, node registration, and edge styles. Key functions: `parseFlowchart()` line 43, `parseStateDiagram()` line 182, `parseEdgeLine()` line 450, `consumeNode()` line 561.
- inputs_outputs_state: Inputs are Mermaid source text. Outputs are `MermaidGraph` with nodes/edges/subgraphs/direction/styles.
- gates_or_invariants: Br tags normalized; node IDs registered once; subgraph membership tracked; arrow operators map to style; parser tolerates unsupported lines by skipping.
- dependencies_and_callers: Used by mermaid ASCII renderer utilities.
- edge_cases_or_failure_modes: Nested subgraphs, text arrows, class shorthand, state aliases, labels containing brackets, unsupported Mermaid syntax.
- validation_or_tests: Mermaid utility tests not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3517 `file` `packages/coding-agent/src/eval/js/shared/local-module-loader.ts`
- cursor: `[_]`
- core_role: Local CommonJS-like module loader for JS/TS eval sandbox.
- algorithmic_behavior: Resolves local import specifiers, strips TypeScript syntax, wraps module source, executes in VM context with custom `require`, caches module entries, handles relative exports/imports, and delegates external requires to Node `createRequire`. Core class starts line 20; helpers at lines 286 onward.
- inputs_outputs_state: Inputs are cwd/module paths/source imports. Outputs are loaded module exports or external resolution targets.
- gates_or_invariants: Only local path specifiers are managed; TS/TSX stripped before execution; module cache prevents repeat execution; path normalization protects loader ownership.
- dependencies_and_callers: Used by JS eval backend/shared runtime. Depends on fs/path/url/vm and rewrite-imports helpers.
- edge_cases_or_failure_modes: Circular imports, unsupported TS syntax after stripping, extension resolution ambiguity, external package failure, managed path false positive.
- validation_or_tests: Eval JS tests not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3547 `file` `packages/coding-agent/src/modes/components/status-line/git-utils.ts`
- cursor: `[_]`
- core_role: GitHub PR cache context utilities for status line.
- algorithmic_behavior: Parses GitHub repo remote URLs, parses default branch refs, creates PR cache context, compares contexts, and decides whether cached PR info can be reused.
- inputs_outputs_state: Inputs are remote URL, branch/ref, cached context. Outputs are repo ID/context booleans.
- gates_or_invariants: Cache reuse requires same branch/repo context; unknown repo disables safe reuse.
- dependencies_and_callers: Used by status-line PR display.
- edge_cases_or_failure_modes: SSH vs HTTPS remotes, enterprise hosts, branch ref formats.
- validation_or_tests: Status-line tests not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3577 `file` `packages/coding-agent/src/web/search/providers/searxng.ts`
- cursor: `[_]`
- core_role: SearXNG web search provider adapter.
- algorithmic_behavior: Resolves endpoint/token/basic auth from settings/env, rejects control characters in auth, builds GET/POST search requests with categories/language/safesearch/time range, calls provider with hard timeout, maps results to normalized search response, and implements `SearXNGProvider`. Key functions: `findEndpoint()` line 77, `buildRequest()` line 154, `callSearXNGSearch()` line 201, `searchSearXNG()` line 232.
- inputs_outputs_state: Inputs are search params, auth storage/fetch, settings/env. Outputs are normalized `SearchResponse` or `SearchProviderError`.
- gates_or_invariants: Num results clamped to 20; recency maps to SearXNG time range; basic auth rejects control chars; HTTP errors classified.
- dependencies_and_callers: Depends on search provider base/types/utils and settings.
- edge_cases_or_failure_modes: Missing endpoint, bad JSON, unauthorized provider, timeout, result without URL/title, auth injection chars.
- validation_or_tests: Search provider tests not run.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3607 `file` `packages/coding-agent/src/extensibility/custom-commands/bundled/ci-green/index.ts`
- cursor: `[_]`
- core_role: Bundled custom command that generates a CI-green remediation prompt.
- algorithmic_behavior: Reads current branch, head tag, and push remote with git helpers, falls back to `HEAD`/`origin`, then renders `ci-green-request.md` prompt template. `GreenCommand.execute()` starts line 44.
- inputs_outputs_state: Inputs are command API cwd and hook context. Outputs are rendered prompt string.
- gates_or_invariants: Git failures degrade to fallback values; prompt construction stays in static markdown template.
- dependencies_and_callers: Depends on custom command API, hook context, prompt renderer, git utils.
- edge_cases_or_failure_modes: Detached HEAD, missing remote, no tags, git command failure.
- validation_or_tests: Custom command tests not run.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 121 evidence headings in `## Item Evidence`
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`