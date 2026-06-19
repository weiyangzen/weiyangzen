# agent_25 main 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 120
- source_commit: `6b3819fad50a89fffae899b240ad1ce065c51d23`
- notes: read-only branch export inspected only; no files modified and no validation commands were run beyond static source/symbol inspection.

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-025 `directory` `packages/agent`
- cursor: `[_]`
- core_role: Core agent runtime package: owns the turn loop, tool calling, streaming message handling, context persistence, telemetry/run collection, compaction, pruning, shaking, and branch summaries.
- algorithmic_behavior: `src/agent-loop.ts` drives model streaming, validates malformed tool results at boundaries, snapshots assistant deltas, handles pause/continue limits, steering interruption polling, dialect ownership, and tool execution. `src/agent.ts` wraps session-level orchestration. `src/append-only-context.ts` maintains stable prefix-cacheable message history and detects rewrite/compaction by digest. `src/compaction/*` handles summary generation, remote OpenAI compaction, token thresholds, pruning, shake elision, file-operation tracking, tool-result protection, and durable entry shapes.
- inputs_outputs_state: Inputs are model/tool/session settings, message streams, tool calls/results, token estimates, and persisted session entries. Outputs are normalized assistant/user/tool messages, telemetry events, compaction entries, branch summaries, and pruned/shaken context. State is append-only session entry history plus mutable runtime loop status.
- gates_or_invariants: Tool results must match open tool calls; cached prefix stability is protected by append-only digest checks; compaction must preserve recent context and protected tool outputs; remote compaction must preserve encrypted compaction items or fall back; workers should yield through `utils/yield.ts`.
- dependencies_and_callers: Depends on `@oh-my-pi/pi-ai` model APIs, `@oh-my-pi/pi-utils`, tokenizer/native helpers, and prompt `.md` assets. Called by `packages/coding-agent` sessions and tests under `packages/agent/test`.
- edge_cases_or_failure_modes: Covers disconnected proxy streams, superseded/pruned tool outputs, tool-protection for skill reads, compaction errors/status, pause-turn continuation caps, and OpenAI remote compaction failure fallback.
- validation_or_tests: Package tests cover agent loop, append-only context, handoff, remote compaction, pruning, shake, telemetry, serialization, prompt-tool loops, and skill-result protection.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-055 `file` `docs/memory.md`
- cursor: `[_]`
- core_role: Architecture/runtime documentation for autonomous memory integration.
- algorithmic_behavior: Defines how memory guidance is injected, how local memory roots expose `memory://root`, how `/memory` commands operate, and how extraction/consolidation split into stages with leases, heartbeat, and backend state.
- inputs_outputs_state: Inputs are session transcript messages, user memory operations, local backend config, and command invocations. Outputs are recalled context, retained facts, memory summary files, and command-visible memory status.
- gates_or_invariants: Memory backends must respect redaction, scope/bank isolation, lease ownership, and model-role selection. `memory://` access is constrained to memory roots.
- dependencies_and_callers: Relates to `packages/coding-agent/src/tools/memory-retain.ts`, `src/internal-urls/memory-protocol.ts`, `src/hindsight/*`, and `packages/mnemopi/*`.
- edge_cases_or_failure_modes: Notes stale leases, failed heartbeats, redaction risk, backend unavailability, and consolidation conflicts.
- validation_or_tests: Documentation is exercised indirectly by memory protocol, Hindsight, and mnemopi tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-085 `file` `scripts/ci-concurrency.test.ts`
- cursor: `[_]`
- core_role: Standalone CI workflow concurrency validator.
- algorithmic_behavior: Implements a small GitHub Actions expression evaluator (`GhaEval` around lines 34-230) to parse the `.github/workflows/ci.yml` concurrency group/cancel expressions and test representative event contexts.
- inputs_outputs_state: Input is workflow YAML plus synthetic `github` contexts for push, PR, tag, and release commit scenarios. Output is pass/fail assertions about rendered group and cancel-in-progress values.
- gates_or_invariants: Release pushes and tag dispatches must use per-SHA groups and `cancel-in-progress=false`; normal branch/PR runs should group by branch/ref and allow cancellation.
- dependencies_and_callers: Uses Bun file APIs and local `.github/workflows/ci.yml`; intended to run as a script-level test.
- edge_cases_or_failure_modes: Expression parser supports literals, booleans, null, `&&`, `||`, equality, parentheses, property dereference, and template substitution; malformed workflow expressions fail tests.
- validation_or_tests: This file is itself the validator for CI concurrency behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-115 `file` `scripts/tool-prompt-usage.ts`
- cursor: `[_]`
- core_role: Tool prompt token-usage estimator for coding-agent prompt assets.
- algorithmic_behavior: Collects prompt `.md` paths, renders representative Handlebars context including bundled agents/read limits, counts tokens using native tokenizer encodings, and prints a table or JSON (`estimatePrompt`, `printTable`, `run` around lines 207-253).
- inputs_outputs_state: Inputs are CLI args, prompt paths, encoding choice, and built-in prompt context. Outputs are prompt byte/token estimates and rendered prompt text length metadata.
- gates_or_invariants: Only known encodings are accepted; read-only tool names are classified through `READ_ONLY_TOOL_NAMES`; positional paths are resolved under the repo.
- dependencies_and_callers: Depends on `@oh-my-pi/pi-natives`, prompt helper code, coding-agent prompt directories, and bundled agent definitions.
- edge_cases_or_failure_modes: Handles empty/no positionals by scanning prompt dir; invalid encoding or CLI args print usage and fail.
- validation_or_tests: Manual/CI utility; validation is deterministic rendering plus tokenizer count.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-145 `directory` `packages/natives/scripts`
- cursor: `[_]`
- core_role: Native package build, embedding, enum generation, and optional npm package generation scripts.
- algorithmic_behavior: `build-native.ts` chooses target/platform/arch/variant, handles x64 modern/baseline, zigbuild target-dir symlinks, RUSTFLAGS/cargo target resolution, binary install, and ELF strip verification. `embed-native.ts` creates/reset embedded addon archive metadata. `gen-enums.ts` parses native `.d.ts` exports and rewrites generated JS/DTS blocks. `gen-npm-packages.ts` generates per-platform optional dependency leaf packages.
- inputs_outputs_state: Inputs are environment target variables, built `.node` artifacts, package version, declaration files, and CLI tags. Outputs are native addon files, embedded archive JS, generated export blocks, and leaf package manifests/readmes.
- gates_or_invariants: Expected addon filename must exist; generated block markers must be present; target tags must map to known leaf targets; strip verification rejects forbidden ELF sections.
- dependencies_and_callers: Called from package build/release flows; depends on Bun APIs, node path/fs, napi build output, Rust crate `crates/pi-natives`.
- edge_cases_or_failure_modes: Handles stale temp dirs, missing native files, variant mismatch, unsupported target tag, cross-compile symlink oddities, and non-ELF files.
- validation_or_tests: Build scripts validate by file existence, manifest content, and ELF inspection.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-175 `file` `docs/toolconv/glm-4.5.md`
- cursor: `[_]`
- core_role: Tool-conversation format specification for GLM-4.5/4.6.
- algorithmic_behavior: Documents prompt envelope, role markers, `<think>` handling, XML-like `<tool_call>`/`<tool_response>` blocks, EOS behavior, and parser mapping for vLLM/SGLang.
- inputs_outputs_state: Inputs are chat messages, tools, arguments, and tool results. Outputs are serialized model prompts and parsed tool calls/results.
- gates_or_invariants: String arguments are raw text while non-string args remain JSON-like; tool responses are positional; prompt must include `[gMASK]<sop>` and role markers.
- dependencies_and_callers: Guides dialect/provider implementations in `packages/ai` and any GLM-compatible tool parser.
- edge_cases_or_failure_modes: Calls out parser ambiguity around raw strings, EOS/tool-call termination, thinking text separation, and server parser differences.
- validation_or_tests: Spec document; behavior should be validated by dialect/tool-conversation tests when implemented.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-205 `file` `docs/tools/todo.md`
- cursor: `[_]`
- core_role: Todo tool contract and state-machine documentation.
- algorithmic_behavior: Defines ordered operations `init`, `start`, `done`, `drop`, `rm`, `append`, and `view`; describes normalization, markdown roundtrip, UI/session integration, and batch mutation semantics.
- inputs_outputs_state: Inputs are todo operation batches and existing todo state. Outputs are normalized todo lists, markdown renderings, and mutation results. State is the current ordered todo list with statuses/details.
- gates_or_invariants: Batch error discards all mutations; only one item may be `in_progress`; IDs and completion transitions are validated; idempotency rules are explicit.
- dependencies_and_callers: Guides coding-agent todo tool/session/UI behavior.
- edge_cases_or_failure_modes: Covers duplicate IDs, invalid transitions, append/drop behavior, completion details, and parse/render roundtrip concerns.
- validation_or_tests: Documentation-level contract, likely exercised by tool/session tests elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-235 `directory` `packages/ai/src/registry`
- cursor: `[_]`
- core_role: Single-source provider registry, login/OAuth routing, API-key validation, and provider descriptor definitions.
- algorithmic_behavior: `registry.ts` imports provider definitions into `PROVIDER_REGISTRY`; `derived.ts` builds downstream provider maps; `oauth/index.ts` derives built-ins, custom registrations, refresh dispatch, and `getOAuthApiKey`; provider files define login/auth models for OpenAI, Anthropic, Gemini, GitLab Duo, Xiaomi, Kimi, etc.
- inputs_outputs_state: Inputs are provider IDs, auth storage credentials, env/API keys, login controller prompts, and refresh tokens. Outputs are provider metadata, OAuth credentials, API keys, refresh results, and derived login lists.
- gates_or_invariants: Provider IDs must be unique; OAuth providers require handlers; expired credentials are refused unless refreshed; provider definitions must include api/name/auth shape.
- dependencies_and_callers: Used by model registry, AuthStorage, CLI login flows, catalog discovery, and provider clients.
- edge_cases_or_failure_modes: Handles broker sentinel credentials, Perplexity JWT expiry, custom OAuth provider unregister by source, region-specific Xiaomi token-plan providers, and non-login providers such as Mistral.
- validation_or_tests: Covered by auth-storage credential tests, Xiaomi issue tests, registry runtime cleanup tests, and provider-specific login tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-265 `directory` `packages/coding-agent/src/hindsight`
- cursor: `[_]`
- core_role: Hindsight memory backend adapter for coding-agent.
- algorithmic_behavior: `backend.ts` starts primary/alias state, injects memory instructions, coalesces scope rebuilds, flushes retain queues before state replacement, and flattens messages for recall. `client.ts` implements fetch API methods for retain/recall/reflect/banks/docs/mental-models with query/body shaping. `bank.ts` computes global/project/tagged scopes and idempotent bank creation. `config.ts` resolves settings and `HINDSIGHT_*` env overrides.
- inputs_outputs_state: Inputs are session messages, memory retain calls, cwd/project tags, config/env, and Hindsight HTTP responses. Outputs are recall text, queued retain operations, bank/docs state, and backend status.
- gates_or_invariants: Undefined body fields are pruned; selected 404s map to null; bank creation is capped by `banksSet`; retain queues flush before replacing backend state.
- dependencies_and_callers: Called by memory backend/session code and `memory-retain` tool; depends on fetch, settings, session registry, and memory docs.
- edge_cases_or_failure_modes: Handles alias state, backend errors wrapped as `HindsightError`, missing config, bank existence races, and retain queue replacement.
- validation_or_tests: Memory backend behavior is indirectly covered by memory-retain, protocol, and managed memory tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-295 `directory` `packages/coding-agent/test/core`
- cursor: `[_]`
- core_role: Core coding-agent algorithm regression suite for patching, hashline editing, JS/Python execution bridges, kernel lifecycle, turn budgets, and display/result mapping.
- algorithmic_behavior: Tests parse/apply patch seeking, indentation, ambiguity, line hints, Codex patch envelope parsing, hashline v4 edit semantics, Python kernel reuse/cancellation/streaming/display, JS import rewriting/execution, session tool bridge calls, and budget accounting.
- inputs_outputs_state: Inputs are synthetic files, patch bodies, JS/Python code cells, kernel sessions, and session managers. Outputs are edited file content, tool bridge responses, result objects, displays, and lifecycle state.
- gates_or_invariants: Patch application must reject ambiguous edits and preserve context; hashline loop guard blocks no-op repetition; Python sessions clean by owner and timeout; JS imports are rewritten safely.
- dependencies_and_callers: Exercises `src/edit/apply-patch`, eval tools, kernel/executor code, hashline, workflow helpers, and session manager.
- edge_cases_or_failure_modes: Adversarial patches, trailing context accidental deletion, nested anchors, long-line substring edits, stale anchors, per-call executor isolation, kernel cancellation, and environment filtering.
- validation_or_tests: This directory is validation coverage for the core algorithms.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-325 `directory` `packages/mnemopi/src/dr`
- cursor: `[_]`
- core_role: Disaster recovery subsystem for mnemopi SQLite memory stores.
- algorithmic_behavior: `recovery.ts` serializes SQLite database bytes, gzips backups, writes metadata/checksums, restores from binary DB or SQL dump, checks integrity, rotates backups, and attempts emergency restore from newest valid backups. `index.ts` exports the subsystem.
- inputs_outputs_state: Inputs are DB paths, backup dirs, metadata, checksums, and sidecar files. Outputs are backup artifacts, restored DB files, health reports, and rotated backup sets.
- gates_or_invariants: Backup metadata checksum must match; restore validates SQLite integrity; sidecar copying is controlled; rotation preserves configured retention.
- dependencies_and_callers: Used by mnemopi persistence/maintenance workflows; depends on Bun/node fs, gzip, SQLite.
- edge_cases_or_failure_modes: Handles corrupt backups, SQL dump fallback, missing sidecars, failed integrity check, and emergency restore ordering.
- validation_or_tests: Covered indirectly by mnemopi persistence and pre-experiment fidelity tests; no direct DR test observed in assignment.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-355 `file` `crates/pi-natives/src/fd.rs`
- cursor: `[_]`
- core_role: Native fuzzy file/path discovery for autocomplete and `@` mention resolution.
- algorithmic_behavior: Normalizes query/path text, scores basename/path exact/prefix/substring/subsequence matches, boosts directories, scans through `fs_cache`, sorts by score then path, and exposes async NAPI `fuzzyFind` (`fuzzy_find` around line 242).
- inputs_outputs_state: Inputs are query, search path, hidden/gitignore/cache/max/timeout/signal options. Outputs are `FuzzyFindResult` with matches and total count.
- gates_or_invariants: Symlinks are skipped; `max_results=0` returns no matches; non-empty queries that normalize to empty return no matches; cached empty results can force rescan after cache age.
- dependencies_and_callers: Depends on `fs_cache`, `task::CancelToken`, NAPI. Called by JS native package consumers for file discovery.
- edge_cases_or_failure_modes: Handles cancellation heartbeats, cache staleness, path-style queries vs basename-only queries, and clamped total counts.
- validation_or_tests: Native fuzzy behavior is validated indirectly by coding-agent file discovery/autocomplete tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-385 `file` `crates/pi-shell/tests/minimizer_fixtures.rs`
- cursor: `[_]`
- core_role: Fixture-driven regression gate for shell-output minimizer behavior.
- algorithmic_behavior: Discovers fixtures, runs minimizer with config, compares minimized output to expected snapshots, enforces a savings ratio gate for large outputs (`SAVINGS_RATIO`/`GATE_MIN_BYTES`).
- inputs_outputs_state: Inputs are fixture input/expected files and minimizer config. Outputs are assertion failures with diff excerpts or savings failures.
- gates_or_invariants: Large fixtures must achieve at least 40% byte savings; expected minimized text must match exactly.
- dependencies_and_callers: Depends on pi-shell minimizer implementation and fixture tree.
- edge_cases_or_failure_modes: Reports missing/invalid fixture metadata, exact output mismatches, and insufficient compression.
- validation_or_tests: This file is the validation harness for minimizer fixtures.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-415 `file` `packages/agent/test/tool-protection.test.ts`
- cursor: `[_]`
- core_role: Regression test for protected tool results during pruning/shake.
- algorithmic_behavior: Constructs read tool-call/result pairs and verifies `skill://` reads are retained while ordinary read outputs can be pruned/shaken.
- inputs_outputs_state: Inputs are synthetic session messages with tool calls/results. Outputs are pruned/shaken message lists.
- gates_or_invariants: Skill reads must remain available after context reduction; unprotected read outputs may be removed according to pruning policy.
- dependencies_and_callers: Exercises `packages/agent/src/compaction/tool-protection.ts`, `pruning.ts`, and `shake.ts`.
- edge_cases_or_failure_modes: Protects paired read call/result matching and prevents accidental loss of skill instructions.
- validation_or_tests: File itself is the targeted test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-445 `file` `packages/ai/test/anthropic-prior-turn-thinking.test.ts`
- cursor: `[_]`
- core_role: Anthropic provider regression tests for preserving prior-turn thinking blocks.
- algorithmic_behavior: Builds synthetic Anthropic models/messages with thinking, assistant content, tool calls, and tool results; drains provider request construction and asserts prior thinking is carried where required.
- inputs_outputs_state: Inputs are Anthropic message histories and model options. Outputs are serialized Anthropic request bodies.
- gates_or_invariants: Prior-turn thinking must not be dropped in cases needed for Anthropic continuity; tool-result chains remain valid.
- dependencies_and_callers: Exercises Anthropic message serialization in `packages/ai`.
- edge_cases_or_failure_modes: Covers regressions #2257/#2265 around thinking preservation across tool-use turns.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-475 `file` `packages/ai/test/auth-storage-check-credentials.test.ts`
- cursor: `[_]`
- core_role: Credential checking and refresh-contract tests for AuthStorage.
- algorithmic_behavior: Creates fake stored OAuth/API-key rows and stores, probes `checkCredentials`, refresh behavior, identity detection, and local-only validation.
- inputs_outputs_state: Inputs are stored auth credentials, provider IDs, expiry flags, mocked refresh/probe outcomes. Outputs are credential status reports and refreshed records.
- gates_or_invariants: Expired OAuth rows require refresh; broker sentinel and local-only credentials have distinct handling; probe identity must map to user/account fields.
- dependencies_and_callers: Exercises `AuthStorage`, provider registry/OAuth helpers, and auth broker sentinel constants.
- edge_cases_or_failure_modes: Covers missing credentials, expired tokens, refresh failure, API key probe errors, and credential identity mismatches.
- validation_or_tests: File itself is focused validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-505 `file` `packages/ai/test/gemini-gemma-dialect.test.ts`
- cursor: `[_]`
- core_role: Dialect parser/render tests for Gemini Pythonic and Gemma token-delimited tool calls.
- algorithmic_behavior: Streams text into in-band scanners, parses tool calls, extracts visible text, and checks render roundtrips for tool calls/results/transcripts.
- inputs_outputs_state: Inputs are model output fragments, tool-code fences, token-delimited calls, and tool result payloads. Outputs are `InbandScanEvent` sequences and rendered transcript strings.
- gates_or_invariants: Tool-code fences must emit calls without leaking code text; char-by-char streaming should match batch scanning; Python literals must parse correctly.
- dependencies_and_callers: Exercises `packages/ai/src/dialect/gemini.ts` and Gemma dialect code.
- edge_cases_or_failure_modes: Covers nested strings/comments, malformed calls, streaming partial fences, and visible text preservation.
- validation_or_tests: File itself is validation coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-535 `file` `packages/ai/test/issue-1417-repro.test.ts`
- cursor: `[_]`
- core_role: Regression test for synthetic model deprecation lifecycle.
- algorithmic_behavior: Builds synthetic `ModelSpec` entries with TTL and checks deprecation/expiry behavior for runtime synthetic models.
- inputs_outputs_state: Inputs are synthetic model IDs and timestamps. Outputs are model availability/deprecation assertions.
- gates_or_invariants: Synthetic models should expire/deprecate according to TTL instead of remaining indefinitely valid.
- dependencies_and_callers: Exercises catalog/model registry synthetic model handling.
- edge_cases_or_failure_modes: Prevents stale synthetic model entries from surviving beyond intended lifetime.
- validation_or_tests: File is the issue #1417 reproduction.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-565 `file` `packages/ai/test/models-cost.test.ts`
- cursor: `[_]`
- core_role: Cost calculation tests for model token accounting.
- algorithmic_behavior: Asserts `calculateCost` handles input/output/cache pricing shapes and missing cost values.
- inputs_outputs_state: Inputs are model cost metadata and token counts. Outputs are numeric cost calculations.
- gates_or_invariants: Cost math must distinguish input, output, cache read/write pricing and avoid charging missing dimensions incorrectly.
- dependencies_and_callers: Exercises cost helper in `packages/ai`.
- edge_cases_or_failure_modes: Handles zero/missing cost fields and mixed token buckets.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-595 `file` `packages/ai/test/openai-responses-omit-max-output-tokens.test.ts`
- cursor: `[_]`
- core_role: OpenAI Responses request-shaping regression test.
- algorithmic_behavior: Mocks SSE fetch, drains a responses request, and asserts `max_output_tokens` can be omitted for models/options where that is required.
- inputs_outputs_state: Inputs are model specs and streaming context. Outputs are captured OpenAI request JSON.
- gates_or_invariants: Provider must not always emit `max_output_tokens`; opt-out path must preserve other required fields.
- dependencies_and_callers: Exercises OpenAI Responses provider serialization in `packages/ai`.
- edge_cases_or_failure_modes: Prevents unsupported parameter errors on models that reject max-output settings.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-625 `file` `packages/ai/test/schema-helpers.test.ts`
- cursor: `[_]`
- core_role: JSON schema adaptation/merge helper tests.
- algorithmic_behavior: Tests object detection, JSON equality, enum merging, property schema merging, combiner stripping, and strict-schema adaptation.
- inputs_outputs_state: Inputs are JSON schema fragments and values. Outputs are merged/adapted schema objects.
- gates_or_invariants: Incompatible enums/properties must not merge unsafely; residual combiners are stripped for strict providers; object checks exclude arrays/null.
- dependencies_and_callers: Exercises schema helper code used in tool/function calling.
- edge_cases_or_failure_modes: Covers enum conflicts, required property propagation, nested combiners, and strict-mode unsupported schema forms.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-655 `file` `packages/catalog/scripts/generate-models.ts`
- cursor: `[_]`
- core_role: Generated model catalog builder.
- algorithmic_behavior: Fetches models.dev and provider discovery catalogs, merges descriptor output and previous snapshot fallbacks, applies provider-specific fixups, pricing multipliers, Codex/OAuth discovery, Kimi caps, Fireworks/Z.AI/Xiaomi cleanup, generated policies, deduping, sorting, and writes `models.json`.
- inputs_outputs_state: Inputs are upstream model metadata, provider descriptors, API keys/OAuth credentials, previous catalog snapshot, and env. Outputs are normalized model specs in bundled catalog.
- gates_or_invariants: Discovery-only providers are treated specially; provider fixups must run before output; unusable/wire/audio-only IDs are dropped; generated policies are applied before write.
- dependencies_and_callers: Depends on `provider-models/*`, `model-thinking`, OAuth storage, GitLab Duo, Antigravity/Codex discovery, and Bun file/fetch APIs.
- edge_cases_or_failure_modes: Handles failed provider discovery, missing API keys, fallback pricing, OAuth absence, premium multiplier overrides, and stale previous snapshots.
- validation_or_tests: Regression coverage includes catalog issue tests and generated resolver tests; per repo rules, source changes require regenerating `models.json`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-685 `file` `packages/catalog/test/issue-1846-repro.test.ts`
- cursor: `[_]`
- core_role: Xiaomi Token Plan provider support regression test.
- algorithmic_behavior: Builds a Mimo openai-completions model, assistant tool-call messages, and validates reasoning-content/tool-call handling for the Xiaomi token-plan endpoint.
- inputs_outputs_state: Inputs are model specs, base URL, tool calls, and reasoning content. Outputs are serialized provider request expectations.
- gates_or_invariants: Xiaomi token-plan models must map to OpenAI-compatible completions behavior without dropping reasoning/tool-call content.
- dependencies_and_callers: Exercises catalog provider resolution and AI message conversion for Xiaomi.
- edge_cases_or_failure_modes: Covers issue #1846 provider compatibility, endpoint mapping, and reasoning-content message shape.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-715 `file` `packages/coding-agent/bench/rendering.ts`
- cursor: `[_]`
- core_role: Rendering performance benchmark for TUI components.
- algorithmic_behavior: Builds representative welcome and markdown assistant message corpora, repeatedly renders with fixed width/iterations, and times reveal/checkpoint rendering paths.
- inputs_outputs_state: Inputs are synthetic messages, grapheme corpus size, width, iteration count, and component instances. Outputs are timing measurements.
- gates_or_invariants: Benchmark uses stable `ITERATIONS`, `WIDTH`, and corpus checkpoints to compare renderer changes.
- dependencies_and_callers: Depends on coding-agent TUI components and assistant message renderers.
- edge_cases_or_failure_modes: Captures regressions in long markdown reveal, thinking-plus-text rendering, and large text wrapping.
- validation_or_tests: Benchmark only; not a correctness test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-745 `file` `packages/coding-agent/test/active-oauth-account.test.ts`
- cursor: `[_]`
- core_role: Tests account-scoped usage-limit/report matching.
- algorithmic_behavior: Creates usage limits/reports and active account identities, then checks `limitMatchesActiveAccount` and `reportMatchesActiveAccount`.
- inputs_outputs_state: Inputs are usage reports/limits with scope fields and active account metadata. Outputs are boolean match decisions.
- gates_or_invariants: Account/email/provider scope must match active account before applying limits or reports.
- dependencies_and_callers: Exercises active OAuth account helper in coding-agent session/model logic.
- edge_cases_or_failure_modes: Covers absent scopes, partial scopes, email mismatch, provider mismatch, and unrestricted reports.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-775 `file` `packages/coding-agent/test/agent-session-plan-reference-compaction.test.ts`
- cursor: `[_]`
- core_role: Regression test for approved-plan reference reinjection after compaction.
- algorithmic_behavior: Stubs compaction, emits high usage turns, and verifies session continuation includes a reference to the latest approved plan after compaction.
- inputs_outputs_state: Inputs are agent session messages, plan content, compaction stubs, and token usage events. Outputs are continuation messages/prompts.
- gates_or_invariants: Compaction must not permanently lose approved-plan context; resume marker should be present for user’s latest intent.
- dependencies_and_callers: Exercises coding-agent `AgentSession` compaction/plan-reference logic.
- edge_cases_or_failure_modes: Covers issue #1246 where plan state could be compacted away.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-805 `file` `packages/coding-agent/test/autolearn-managed-skills.test.ts`
- cursor: `[_]`
- core_role: Managed skill storage safety tests.
- algorithmic_behavior: Exercises managed skill primitives for create/read/list with path resolution, symlink/hardlink protections, byte caps, and concurrent creation.
- inputs_outputs_state: Inputs are skill names, filesystem paths, content bytes, and concurrent operations. Outputs are created skill files or validation errors.
- gates_or_invariants: Skill paths must remain inside managed root; symlink/hardlink traversal is rejected; file size caps are enforced.
- dependencies_and_callers: Exercises autolearn/managed skill filesystem helpers.
- edge_cases_or_failure_modes: Covers traversal attempts, symlink attacks, hardlink hazards, oversized files, and races.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-835 `file` `packages/coding-agent/test/compaction-thinking-model.test.ts`
- cursor: `[_]`
- core_role: Compaction model/thinking selection test.
- algorithmic_behavior: Checks how compaction chooses model/thinking settings under available auth conditions.
- inputs_outputs_state: Inputs are model/auth availability flags and settings. Outputs are selected compaction model and thinking behavior.
- gates_or_invariants: Compaction should use intended model scopes and not require unavailable OAuth in local test environments.
- dependencies_and_callers: Exercises compaction configuration in coding-agent sessions.
- edge_cases_or_failure_modes: Handles absent Antigravity auth and optional Anthropic API keys.
- validation_or_tests: File itself is validation, partly gated by env availability.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-865 `file` `packages/coding-agent/test/gallery-cli.test.ts`
- cursor: `[_]`
- core_role: Gallery CLI harness tests.
- algorithmic_behavior: Verifies fixture resolution and rendering states for tool-render gallery output.
- inputs_outputs_state: Inputs are gallery fixture names, state args, width args, and fake tools. Outputs are rendered terminal/gallery sections.
- gates_or_invariants: Unknown fixture falls back/errors consistently; requested state names must be in allowed set.
- dependencies_and_callers: Exercises `src/cli/gallery-cli.ts` and tool renderer fixture registry.
- edge_cases_or_failure_modes: Covers missing fixture, width resolution, and state rendering variants.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-895 `file` `packages/coding-agent/test/input-controller-thinking-visibility.test.ts`
- cursor: `[_]`
- core_role: Input controller test for thinking visibility toggles.
- algorithmic_behavior: Verifies input-controller state changes that expose/hide thinking content in the TUI.
- inputs_outputs_state: Inputs are controller actions/settings; outputs are visibility state/render flags.
- gates_or_invariants: Thinking visibility must track configured user action without corrupting input state.
- dependencies_and_callers: Exercises `InputController` in coding-agent interactive mode.
- edge_cases_or_failure_modes: Prevents regressions where thinking state remains hidden or visible incorrectly.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-925 `file` `packages/coding-agent/test/issue-849-repro.test.ts`
- cursor: `[_]`
- core_role: Regression test for explicit default model persistence.
- algorithmic_behavior: Simulates assistant-message inference after an explicit default model and asserts later inference does not overwrite the explicit default.
- inputs_outputs_state: Inputs are settings/model scope changes and assistant messages. Outputs are model selection state.
- gates_or_invariants: User-explicit default model wins over later inference from assistant messages.
- dependencies_and_callers: Exercises model registry/settings inference in coding-agent.
- edge_cases_or_failure_modes: Covers issue #849 model scope notification/inference regression.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-955 `file` `packages/coding-agent/test/main-model-scope-notification.test.ts`
- cursor: `[_]`
- core_role: Tests model-scope notification message construction.
- algorithmic_behavior: Builds scoped model fixtures and asserts notification text/shape for main-model scope changes.
- inputs_outputs_state: Inputs are scoped model IDs/providers. Outputs are notification strings or message payloads.
- gates_or_invariants: Scope notifications should be emitted only with meaningful model/provider scope data.
- dependencies_and_callers: Exercises `buildModelScopeNotification`.
- edge_cases_or_failure_modes: Covers missing provider/model metadata and scope mismatch.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-985 `file` `packages/coding-agent/test/model-registry-runtime-cleanup.test.ts`
- cursor: `[_]`
- core_role: Model registry runtime-source cleanup test.
- algorithmic_behavior: Ensures runtime-added model sources/providers are removed/reset when cleanup occurs.
- inputs_outputs_state: Inputs are model registry runtime additions. Outputs are registry state after cleanup.
- gates_or_invariants: Runtime sources should not leak between sessions/tests.
- dependencies_and_callers: Exercises coding-agent model registry.
- edge_cases_or_failure_modes: Prevents stale dynamically discovered models from polluting later operations.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1015 `file` `packages/coding-agent/test/read-tool-group.test.ts`
- cursor: `[_]`
- core_role: Renderer and internal URL tests for grouped read tool output.
- algorithmic_behavior: Renders grouped read outputs, extracts markdown links/text, and validates `readArgsTargetInternalUrl` behavior for internal URLs.
- inputs_outputs_state: Inputs are read tool args/results and internal URL targets. Outputs are rendered grouped lines and link URIs/texts.
- gates_or_invariants: Read grouping must preserve target visibility, avoid malformed links, and handle internal URL classification correctly.
- dependencies_and_callers: Exercises `ReadToolGroupComponent` and internal URL helper code.
- edge_cases_or_failure_modes: Covers multiple reads, failed reads, truncated previews, and internal target parsing.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1045 `file` `packages/coding-agent/test/secrets-obfuscator.test.ts`
- cursor: `[_]`
- core_role: Secret regex compilation and obfuscation tests.
- algorithmic_behavior: Tests secret regex generation and redaction behavior over sample strings.
- inputs_outputs_state: Inputs are secret values/patterns and log text. Outputs are obfuscated strings.
- gates_or_invariants: Secret values must be escaped safely and redacted without overmatching unrelated content.
- dependencies_and_callers: Exercises secrets obfuscator used in logging/debug/reporting.
- edge_cases_or_failure_modes: Handles regex metacharacters, short/empty secrets, and repeated occurrences.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1075 `file` `packages/coding-agent/test/status-line-git-utils.test.ts`
- cursor: `[_]`
- core_role: Status-line GitHub parsing/cache tests.
- algorithmic_behavior: Tests GitHub remote parsing, default branch parsing, PR-cache context equality, and cache reuse decisions.
- inputs_outputs_state: Inputs are git remote URLs, branch output, PR cache metadata. Outputs are parsed repo/default branch and boolean cache reuse.
- gates_or_invariants: PR cache can be reused only when repo/branch/head context matches.
- dependencies_and_callers: Exercises status line git utility functions.
- edge_cases_or_failure_modes: Covers SSH/HTTPS remotes, malformed URLs, missing branch, and stale cache contexts.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1105 `file` `packages/coding-agent/test/tiny-title-generator.test.ts`
- cursor: `[_]`
- core_role: Tiny title generation routing and subprocess tests.
- algorithmic_behavior: Tests local/online title race, first-non-null selection, fallback delays, cancellation, tiny worker spawn args, provider schema, progress UI, and tiny-models CLI.
- inputs_outputs_state: Inputs are conversation text, model registry/settings, tiny model IDs, mocked worker/online responses. Outputs are generated titles, progress events, and CLI results.
- gates_or_invariants: Fastest non-null title wins; cancellation stops pending paths; schema must accept/validate tiny model acceleration settings.
- dependencies_and_callers: Exercises title generator, tiny model subprocess worker, settings schema, and CLI.
- edge_cases_or_failure_modes: Covers null online result, local worker failure, fallback timing, invalid tiny model config, and progress rendering.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1135 `file` `packages/collab-web/src/env.d.ts`
- cursor: `[_]`
- core_role: Vite/client ambient type declaration.
- algorithmic_behavior: No runtime algorithm; declares environment types for collab web build.
- inputs_outputs_state: Input/output/state are compile-time only.
- gates_or_invariants: Must remain compatible with Vite type expectations.
- dependencies_and_callers: Consumed by TypeScript compiler for `packages/collab-web`.
- edge_cases_or_failure_modes: Misclassification as core runtime; runtime behavior unaffected.
- validation_or_tests: Type checking validates it.
- skip_candidate: `yes: ambient .d.ts only, no runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1165 `file` `packages/hashline/test/format-v2.test.ts`
- cursor: `[_]`
- core_role: Hashline format v4/v2-style edit contract tests.
- algorithmic_behavior: Applies hashline diffs to text and verifies replace/delete/insert, bare row auto-piping, and trailing blank sentinel behavior.
- inputs_outputs_state: Inputs are source text and hashline diff strings. Outputs are patched text.
- gates_or_invariants: Hashline edit format must map anchors/rows deterministically and preserve trailing blank sentinel semantics.
- dependencies_and_callers: Exercises hashline parser/executor.
- edge_cases_or_failure_modes: Covers delete/insert edge rows, omitted pipe syntax, and blank-line termination.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1195 `file` `packages/mnemopi/test/consolidate-fact-id-collision.test.ts`
- cursor: `[_]`
- core_role: Veracity consolidator fact-ID collision tests.
- algorithmic_behavior: Uses a temp DB and `VeracityConsolidator` to check deterministic `compute_fact_id` behavior and collision handling during consolidation.
- inputs_outputs_state: Inputs are facts/entities/evidence in DB. Outputs are consolidated fact rows and IDs.
- gates_or_invariants: Fact IDs must be stable and collision resolution must not overwrite unrelated facts.
- dependencies_and_callers: Exercises mnemopi consolidation logic.
- edge_cases_or_failure_modes: Covers duplicate/colliding fact identities and consolidation merge behavior.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1225 `file` `packages/mnemopi/test/pre-experiment-fidelity.test.ts`
- cursor: `[_]`
- core_role: No-LLM pre-experiment memory fidelity tests.
- algorithmic_behavior: Builds beam memory fixtures and checks pre-experiment extraction/retrieval behavior without requiring LLM calls.
- inputs_outputs_state: Inputs are synthetic beam memories. Outputs are retrieved/extracted memory structures.
- gates_or_invariants: Baseline memory fidelity must hold without remote model variability.
- dependencies_and_callers: Exercises mnemopi beam/pre-experiment logic.
- edge_cases_or_failure_modes: Prevents accidental dependence on LLM output for deterministic fidelity checks.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1255 `file` `packages/natives/scripts/gen-npm-packages.ts`
- cursor: `[_]`
- core_role: Native optional dependency leaf-package generator.
- algorithmic_behavior: Selects target tags, discovers expected `.node` files, chooses primary addon variant, builds package manifests/readmes, supports dry-run and `--tag` filtering.
- inputs_outputs_state: Inputs are target tags, native addon directory, package version, and CLI flags. Outputs are generated package directories/manifests/readmes.
- gates_or_invariants: Tags must be known; expected addon filenames must exist; x64 default/modern/baseline selection must be deterministic.
- dependencies_and_callers: Part of native release packaging; depends on Bun/node fs/path.
- edge_cases_or_failure_modes: Handles missing artifacts, unsupported tags, multiple variant files, and dry-run no-write behavior.
- validation_or_tests: Validated by release packaging and internal file checks.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1285 `file` `packages/snapcompact/research/exp13_extractive.py`
- cursor: `[_]`
- core_role: Research baseline for extractive context compaction.
- algorithmic_behavior: Caches LLM extraction calls, frames session chunks, extracts verbatim spans, scores QA/gold survival, aggregates token/cost metrics, and writes JSONL/CSV/summary outputs.
- inputs_outputs_state: Inputs are chunk text, model name, cache payload, QA/gold data, and pricing. Outputs are extraction records, aggregate metrics, and reports.
- gates_or_invariants: Extracted evidence should remain verbatim enough for gold-survival checks; cached responses are keyed by model/tag/payload.
- dependencies_and_callers: Research script under snapcompact, likely run manually for experiments.
- edge_cases_or_failure_modes: Handles failed extraction, missing gold spans, cache freshness, and cost aggregation skew.
- validation_or_tests: Research script, not production test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1315 `file` `packages/snapcompact/research/snapcompact_materialize_sweep.py`
- cursor: `[_]`
- core_role: Research sweep for materialized visual-token compaction experiments.
- algorithmic_behavior: Builds text layouts, maps answer token indices, renders conditions, runs model inference, tracks answer-token probability across layers/logit lens, and writes image/summary artifacts.
- inputs_outputs_state: Inputs are condition parameters, chunk text, layout dimensions, and model settings. Outputs are rendered images and probability summaries.
- gates_or_invariants: Token-index mapping must align with layout geometry; conditions are dataclass-defined and deterministic.
- dependencies_and_callers: Research-only Python script for snapcompact experiments.
- edge_cases_or_failure_modes: Handles layout overflow, token alignment errors, and model/logit-lens availability.
- validation_or_tests: Research script, not production test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1345 `file` `packages/stats/src/aggregator.ts`
- cursor: `[_]`
- core_role: Stats synchronization and dashboard aggregation engine.
- algorithmic_behavior: Spawns parser workers, dispatches session-file parse jobs, applies parse results into stats DB offsets, smoke-tests worker host entry, syncs all sessions, and provides dashboard/time-range query functions.
- inputs_outputs_state: Inputs are session files, last-modified times, worker parse responses, DB state, and range filters. Outputs are processed counts, DB updates, dashboard stats, recent requests/errors, and request details.
- gates_or_invariants: Main thread owns SQLite writes; worker requests time out/reject on failure; worker host entry selector `__omp_worker_stats_sync` is used when available.
- dependencies_and_callers: Used by `omp stats` and smoke tests; depends on worker host utilities, stats DB, parsers, and Bun Worker.
- edge_cases_or_failure_modes: Handles worker spawn failure, parse errors, offset updates, invalid time ranges, and no session files.
- validation_or_tests: Smoke test `smokeTestSyncWorker` plus stats/dashboard tests elsewhere.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1375 `file` `packages/tui/src/keys.ts`
- cursor: `[_]`
- core_role: Terminal key parsing and matching utilities.
- algorithmic_behavior: Defines typed `Key` IDs, Kitty protocol state, release/repeat detection, CSI-u parsing, modifyOtherKeys decoding, printable text extraction, keypad mapping, and raw backspace heuristics.
- inputs_outputs_state: Inputs are raw terminal byte strings and key IDs. Outputs are parsed key labels, printable text, release/repeat booleans, and match decisions.
- gates_or_invariants: Kitty lock modifiers are masked; Windows raw backspace gets special handling; control chars are excluded from printable extraction.
- dependencies_and_callers: Used by TUI input controllers and terminal event processing.
- edge_cases_or_failure_modes: Handles shifted keypad operators, Alt/Ctrl/Super modifiers, Kitty release/repeat markers, malformed CSI-u, and Windows terminal sessions.
- validation_or_tests: Covered by TUI key/input tests and rendering/input controller tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1405 `file` `packages/tui/test/issue-1765-repro.test.ts`
- cursor: `[_]`
- core_role: TUI synchronized-output/cursor regression tests.
- algorithmic_behavior: Uses virtual terminals and probe terminals to verify synchronized-output opt-out, DECRQM probing, cursor no-op renders, autowrap handling, and write capture behavior.
- inputs_outputs_state: Inputs are terminal env patches, renderer components, terminal writes, and focus/cursor state. Outputs are captured escape sequences and viewport assertions.
- gates_or_invariants: Terminals that opt out or fail probe must not receive synchronized-output sequences; cursor-only no-op renders should avoid unnecessary writes.
- dependencies_and_callers: Exercises TUI renderer and `VirtualTerminal`.
- edge_cases_or_failure_modes: Covers issue #1765, ED3-risk terminals, probe results, and cursor render stability.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1435 `file` `packages/tui/test/render-regressions.test.ts`
- cursor: `[_]`
- core_role: Large terminal-state regression suite for TUI renderer.
- algorithmic_behavior: Drives virtual terminal rendering across component updates, resize, scrollback, tmux behavior, Windows behavior, synchronized output, overlays, graphemes, BCE/SGR containment, pending-wrap, hardware cursor, and foreground-tool streaming.
- inputs_outputs_state: Inputs are synthetic components/terminal modes/render operations. Outputs are terminal viewport/style/cursor assertions and captured writes.
- gates_or_invariants: Renderer must keep terminal state coherent across diff renders, not leak styles, and avoid unsafe ED3 operations on risky terminals.
- dependencies_and_callers: Exercises `packages/tui` renderer internals and `virtual-terminal.ts`.
- edge_cases_or_failure_modes: Covers thousands of regressions around wrapping, alternate modes, cursor positions, combining chars, scrollback, and streaming tools.
- validation_or_tests: File itself is broad validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1465 `file` `packages/tui/test/virtual-terminal.ts`
- cursor: `[_]`
- core_role: Ghostty WASM-backed virtual terminal test harness.
- algorithmic_behavior: Loads/reloads Ghostty WASM, creates terminal engines, writes chunks with unsafe combining mark stripping, compacts/replays event logs on OOM, and exposes viewport/style/cursor helpers.
- inputs_outputs_state: Inputs are terminal write strings, dimensions, scrollback limits, and mode changes. Outputs are terminal screen snapshots, style cells, cursor state, and captured logs.
- gates_or_invariants: Max write chunk size is bounded; event log compaction budget prevents runaway memory; sync-output and OSC sequences are handled for test stability.
- dependencies_and_callers: Used by TUI regression tests.
- edge_cases_or_failure_modes: Handles Ghostty OOM by recompiling/replaying, unsafe combining marks, scrollback/viewport translation, and terminal mode escape sequences.
- validation_or_tests: It is a test utility backing render regression validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1495 `file` `packages/utils/src/loop-phase.ts`
- cursor: `[_]`
- core_role: Lightweight loop-phase tracking utility.
- algorithmic_behavior: Maintains a stack of phase labels, exposes push/pop/current, and records a recent phase for later diagnostic retrieval.
- inputs_outputs_state: Inputs are phase labels and pop calls. Outputs are current/recent phase strings.
- gates_or_invariants: Stack order determines current phase; `takeRecentLoopPhase` consumes the saved recent value.
- dependencies_and_callers: Used by utilities/runtime diagnostics to annotate async loop phases.
- edge_cases_or_failure_modes: Unbalanced pops can clear stack entries; recent phase is intentionally single-consume.
- validation_or_tests: No direct assigned test, but logger/startup diagnostics may consume it.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1525 `file` `packages/utils/test/logger-startup.test.ts`
- cursor: `[_]`
- core_role: Logger startup marker and span-path tests.
- algorithmic_behavior: Captures startup marker output under `PI_DEBUG_STARTUP` and tests `openSpanPath` behavior.
- inputs_outputs_state: Inputs are env patches and logger calls. Outputs are captured marker strings/path results.
- gates_or_invariants: Startup debugging must emit expected markers without poisoning global env across tests.
- dependencies_and_callers: Exercises utils logger startup diagnostics.
- edge_cases_or_failure_modes: Covers missing/disabled env, marker ordering, and span path creation/opening.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1555 `file` `python/robomp/src/git_ops.py`
- cursor: `[_]`
- core_role: Git operation layer for robomp automation/proxy workflows.
- algorithmic_behavior: Runs git with credential redaction/basic auth, safe.directory handling, clone/fetch/fetch-pr/push, bad-ref repair, alternate pruning, worktree cleanup, dirty-state inspection, and head-drift detection.
- inputs_outputs_state: Inputs are repo paths, remote URLs, refs, tokens, slot UID permissions, and push options. Outputs are completed subprocess results, `PushResult`, `DirtyState`, or `GitCommandError`.
- gates_or_invariants: Commands redact credentials in errors; ref names are safety-checked; head drift raises `HeadDriftError`; safe.directory is appended for local remotes.
- dependencies_and_callers: Used by robomp service/proxy client for GitHub/workspace operations.
- edge_cases_or_failure_modes: Handles missing alternates, bad remote refs, refs held by worktrees, push rejection/drift, dirty tracked/untracked files, and credential leakage risk.
- validation_or_tests: Covered by `python/robomp/tests/test_proxy_client.py` and likely git-op unit tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1585 `file` `python/robomp/tests/test_proxy_client.py`
- cursor: `[_]`
- core_role: Proxy client integration tests for robomp HTTP/git transport.
- algorithmic_behavior: Builds temporary settings/repos, bridges ASGI app to httpx transport, stages workspaces, attaches fake GitHub handlers, and tests push happy path, head drift, slot UID payloads, and header verification.
- inputs_outputs_state: Inputs are upstream git repos, proxy settings, HTTP requests, GitHub mock responses. Outputs are HTTP responses, bare-branch state, and assertions.
- gates_or_invariants: Proxy push must update expected branch only when head matches; slot UID and auth headers must be forwarded/validated.
- dependencies_and_callers: Exercises robomp proxy app/client plus `git_ops.py`.
- edge_cases_or_failure_modes: Covers head drift, malformed headers, body slot UID, and transport roundtrip through ASGI bridge.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1615 `directory` `packages/coding-agent/src/edit/apply-patch`
- cursor: `[_]`
- core_role: Codex-style apply-patch parser and executor.
- algorithmic_behavior: `parser.ts` parses `*** Begin Patch` envelopes, heredoc wrappers, add/delete/update/move hunks, and streaming-tolerant partial patches. `index.ts` applies hunks sequentially, performs line/context matching, records added/modified/deleted summaries, and is intentionally non-atomic.
- inputs_outputs_state: Inputs are patch text, cwd/filesystem content, and hunks. Outputs are file edits and patch summary.
- gates_or_invariants: Patch grammar requires begin/end markers; updates need matching context; path operations are sequential and can partially apply by design.
- dependencies_and_callers: Used by coding-agent edit tools and heavily tested in `packages/coding-agent/test/core/apply-patch*`.
- edge_cases_or_failure_modes: Handles indentation adjustment, ambiguous context-less hunks, line hints, wrapped patches, EOF markers, long-line substring matches, and move/delete conflicts.
- validation_or_tests: Extensive apply-patch tests in `test/core`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1645 `directory` `packages/coding-agent/test/modes/controllers`
- cursor: `[_]`
- core_role: Interactive-mode controller regression suite.
- algorithmic_behavior: Tests command controllers, selector deletion/logout, MCP authorization links, event-controller message starts, interrupt/abort guards, loader recovery, idle compaction teardown, read grouping, args reveal pacing, superseded agent ends, handoff/bash shortcuts, OMFG/TAN/BTW controllers, and input expansion.
- inputs_outputs_state: Inputs are controller fixtures, session events, commands, TUI actions, and mocked session managers. Outputs are UI state, command results, event records, loader states, and notifications.
- gates_or_invariants: Controllers must preserve event ordering, avoid stale loaders, synthesize needed message starts, handle aborts safely, and keep destructive actions behind confirmation.
- dependencies_and_callers: Exercises `src/modes/controllers/*`, interactive mode components, MCP link UI, and command handlers.
- edge_cases_or_failure_modes: Covers mid-stream tool arg finalization, aborted turns, superseded `agent_end`, session deletion, authorization prompt links, and overflow maintenance recovery.
- validation_or_tests: Directory itself is validation coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1675 `file` `packages/agent/src/compaction/entries.ts`
- cursor: `[_]`
- core_role: Durable session-entry type schema for agent compaction/session history.
- algorithmic_behavior: Defines discriminated entry interfaces for messages, compactions, branch summaries, custom entries, model/thinking/service tier changes, labels, TTSR injection, MCP tool selection, session init, and mode changes.
- inputs_outputs_state: Inputs are runtime events converted to entries. Outputs are typed persisted session entries consumed by session managers/compaction.
- gates_or_invariants: Each entry carries timestamp and stable `type`; session init records initial model/thinking/settings; extension custom entries are type-extensible.
- dependencies_and_callers: Used by `packages/agent` context/session serialization and coding-agent session storage.
- edge_cases_or_failure_modes: Type drift would break replay/compaction; custom entries require stable type names.
- validation_or_tests: Covered indirectly by session serialization and compaction tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1705 `file` `packages/ai/src/dialect/gemini.ts`
- cursor: `[_]`
- core_role: Gemini/Gemma dialect implementation for in-band tool calls and transcript rendering.
- algorithmic_behavior: `GeminiInbandScanner` buffers `tool_code`/thinking fences, parses Python call expressions, skips strings/comments, parses Python literals/lists/dicts, and renders calls/results/thinking/transcripts.
- inputs_outputs_state: Inputs are streamed text chunks and message/tool structures. Outputs are in-band scan events and rendered prompt transcript strings.
- gates_or_invariants: Tool-code content is converted into calls, not visible text; Python parser respects top-level splitting and string escaping; transcript role wrappers are stable.
- dependencies_and_callers: Used by Gemini/Gemma providers and dialect tests.
- edge_cases_or_failure_modes: Handles partial fences, comments, raw/escaped Python strings, nested lists/dicts, malformed calls, and thinking fence separation.
- validation_or_tests: Covered by `packages/ai/test/gemini-gemma-dialect.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1735 `file` `packages/ai/src/providers/gitlab-duo.ts`
- cursor: `[_]`
- core_role: GitLab Duo provider bridge and model mapping.
- algorithmic_behavior: Maps Duo model IDs to Anthropic/OpenAI proxy targets, fetches and caches 25-minute direct access tokens, exposes Duo models, and routes streaming calls to Anthropic, OpenAI Responses, or OpenAI Chat Completions proxy with GitLab headers/options.
- inputs_outputs_state: Inputs are Duo credentials, model IDs, stream contexts, and provider options. Outputs are normalized model specs and streaming provider responses.
- gates_or_invariants: Direct access cache is keyed by API key/base URL; Duo model must resolve to a mapping; proxy headers must include GitLab auth/access token.
- dependencies_and_callers: Depends on Anthropic/OpenAI provider streamers and provider-response notification utilities.
- edge_cases_or_failure_modes: Handles missing mapping, token fetch failure, cached token expiry, and API-type routing differences.
- validation_or_tests: Covered indirectly by provider and registry tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1765 `file` `packages/ai/src/registry/alibaba-coding-plan.ts`
- cursor: `[_]`
- core_role: Alibaba Coding Plan login provider definition.
- algorithmic_behavior: Prompts user for international/China/custom endpoint, validates OpenAI-compatible API key against a validation model, and returns OAuth-style credentials with `enterpriseUrl`.
- inputs_outputs_state: Inputs are `OAuthController` prompts, API key, endpoint choice/custom URL. Outputs are `OAuthCredentials`.
- gates_or_invariants: Endpoint must be chosen/valid; API key is validated before storage; provider ID/metadata registered as login provider.
- dependencies_and_callers: Used by provider registry login flow.
- edge_cases_or_failure_modes: Handles custom endpoint, China endpoint, validation failure, and aborted prompts.
- validation_or_tests: Covered indirectly by registry/auth tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1795 `file` `packages/ai/src/registry/mistral.ts`
- cursor: `[_]`
- core_role: Mistral provider registry descriptor.
- algorithmic_behavior: Exports a provider definition with ID/name/auth metadata; no custom login algorithm.
- inputs_outputs_state: Inputs are provider lookup requests. Outputs are static provider metadata.
- gates_or_invariants: Provider ID must match catalog/auth expectations.
- dependencies_and_callers: Imported by `registry.ts`.
- edge_cases_or_failure_modes: Minimal; wrong ID/name would break provider lookup.
- validation_or_tests: Registry tests indirectly validate inclusion.
- skip_candidate: `yes: static descriptor only, minimal algorithmic behavior`

### OH_MY_HUMANIZE_MAIN-HZ-1825 `file` `packages/ai/src/registry/xiaomi-token-plan-cn.ts`
- cursor: `[_]`
- core_role: Xiaomi Token Plan China provider descriptor.
- algorithmic_behavior: Exports provider metadata with lazy OAuth login import configured for region `"cn"`.
- inputs_outputs_state: Inputs are login requests. Outputs are OAuth credentials from Xiaomi login flow.
- gates_or_invariants: Region must be `"cn"` and provider ID must match catalog descriptors.
- dependencies_and_callers: Imported by registry and delegates to `oauth/xiaomi`.
- edge_cases_or_failure_modes: Broken lazy import or region mismatch would route auth incorrectly.
- validation_or_tests: Related coverage in Xiaomi token-plan tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1855 `file` `packages/ai/src/utils/provider-response.ts`
- cursor: `[_]`
- core_role: Provider response normalization/notification helper.
- algorithmic_behavior: Normalizes provider response metadata and forwards it to callbacks/observers via `notifyProviderResponse`.
- inputs_outputs_state: Inputs are provider-specific response objects. Outputs are normalized response payloads delivered to stream context.
- gates_or_invariants: Undefined/missing response fields are handled safely; notification should not mutate provider payloads.
- dependencies_and_callers: Used by providers such as GitLab Duo and OpenAI/Anthropic bridges.
- edge_cases_or_failure_modes: Prevents inconsistent provider-response shapes from breaking observers.
- validation_or_tests: Covered indirectly by provider stream tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1885 `file` `packages/catalog/src/identity/reference.ts`
- cursor: `[_]`
- core_role: Model reference index/resolution helper for proxy/reseller model IDs.
- algorithmic_behavior: Builds exact and suffix alias maps, prefers richer references, skips zero-cost xAI OAuth refs, generates candidate IDs by stripping brackets/suffixes/markers/provider prefixes and colon-to-dash normalization, then resolves references.
- inputs_outputs_state: Inputs are bundled model list and arbitrary model IDs. Outputs are reference models or undefined.
- gates_or_invariants: Existing reference replacement prefers larger limits/cache pricing/OpenAI references; zero-cost xAI OAuth candidates are filtered.
- dependencies_and_callers: Used by catalog/model identity resolution.
- edge_cases_or_failure_modes: Handles bracketed labels, provider prefixes, trailing markers, duplicate suffixes, and case normalization.
- validation_or_tests: Covered by catalog identity/resolver tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1915 `file` `packages/coding-agent/src/capability/extension-module.ts`
- cursor: `[_]`
- core_role: Capability definition for extension modules.
- algorithmic_behavior: Defines `ExtensionModule` shape and registers `extensionModuleCapability` through capability infrastructure.
- inputs_outputs_state: Inputs are loaded extension module objects. Outputs are typed capability availability.
- gates_or_invariants: Extensions must satisfy expected optional command/tool hooks.
- dependencies_and_callers: Used by extensibility loader/runtime.
- edge_cases_or_failure_modes: Minimal; malformed extension modules fail capability matching elsewhere.
- validation_or_tests: Indirectly covered by extensibility tests.
- skip_candidate: `yes: small type/capability adapter, not a standalone algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1945 `file` `packages/coding-agent/src/cli/gallery-cli.ts`
- cursor: `[_]`
- core_role: CLI renderer for tool gallery fixtures.
- algorithmic_behavior: Resolves fixture/state/width, creates fake tools, renders summary/body for streaming/progress/success/error states, and prints sectioned terminal output.
- inputs_outputs_state: Inputs are CLI args, fixture registry, requested state, width. Outputs are gallery-rendered text to stdout.
- gates_or_invariants: State must be one of `streaming`, `progress`, `success`, `error`; width is normalized; missing fixture returns generic error fixture.
- dependencies_and_callers: Used by gallery command/tests; depends on tool renderer registry and TUI formatting.
- edge_cases_or_failure_modes: Handles unknown fixture names, invalid widths, and renderer errors.
- validation_or_tests: Covered by `packages/coding-agent/test/gallery-cli.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1975 `file` `packages/coding-agent/src/commands/agents.ts`
- cursor: `[_]`
- core_role: CLI command adapter for agent asset actions.
- algorithmic_behavior: Defines allowed actions such as `unpack` and maps CLI invocation to the implementation.
- inputs_outputs_state: Inputs are CLI args/options. Outputs are unpacked agent assets or command errors.
- gates_or_invariants: Action must be in allowed `ACTIONS`.
- dependencies_and_callers: Used by command registry.
- edge_cases_or_failure_modes: Invalid actions should be rejected by CLI parser.
- validation_or_tests: Indirect command tests.
- skip_candidate: `yes: thin CLI adapter`

### OH_MY_HUMANIZE_MAIN-HZ-2005 `file` `packages/coding-agent/src/commands/worktree.ts`
- cursor: `[_]`
- core_role: CLI command adapter for worktree features.
- algorithmic_behavior: Declares command class and delegates to worktree command implementation.
- inputs_outputs_state: Inputs are CLI args. Outputs are worktree operation results or errors.
- gates_or_invariants: Command options must pass parser validation.
- dependencies_and_callers: Used by CLI command registry.
- edge_cases_or_failure_modes: Minimal adapter-level behavior.
- validation_or_tests: Indirect CLI/worktree tests.
- skip_candidate: `yes: thin command wrapper`

### OH_MY_HUMANIZE_MAIN-HZ-2035 `file` `packages/coding-agent/src/debug/log-formatting.ts`
- cursor: `[_]`
- core_role: Debug log formatting/parsing helper for TUI-safe display.
- algorithmic_behavior: Formats a log line to width, expands wrapped lines, parses timestamp milliseconds, and parses PID from log text.
- inputs_outputs_state: Inputs are raw log lines and max width. Outputs are truncated/wrapped display lines plus parsed timestamp/PID.
- gates_or_invariants: Display width must be bounded; parse functions return undefined on non-matching lines.
- dependencies_and_callers: Used by debug log UI.
- edge_cases_or_failure_modes: Handles malformed timestamps, absent PIDs, and long lines.
- validation_or_tests: Indirectly covered by debug UI/log tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2065 `file` `packages/coding-agent/src/discovery/substitute-plugin-root.ts`
- cursor: `[_]`
- core_role: Recursive plugin-root placeholder substitution helper.
- algorithmic_behavior: Walks strings/arrays/objects and substitutes `${CLAUDE_PLUGIN_ROOT}` and `${OMP_PLUGIN_ROOT}` with a root path.
- inputs_outputs_state: Inputs are arbitrary JSON-like config values and root path. Outputs are copied values with substitutions.
- gates_or_invariants: Should preserve non-string primitives and recursively traverse objects/arrays.
- dependencies_and_callers: Used by plugin discovery/config loading.
- edge_cases_or_failure_modes: Handles nested structures and avoids mutating primitive values.
- validation_or_tests: Indirect plugin discovery tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2095 `file` `packages/coding-agent/src/extensibility/legacy-pi-ai-shim.ts`
- cursor: `[_]`
- core_role: Legacy extension compatibility shim for old `pi-ai` imports and TypeBox enum helpers.
- algorithmic_behavior: Implements `StringEnum` wrapper schema and re-exports `@oh-my-pi/pi-ai` plus `Type` for legacy packages.
- inputs_outputs_state: Inputs are enum values/options from extensions. Outputs are TypeBox schemas and re-exported symbols.
- gates_or_invariants: Wire schema must preserve allowed values and optional descriptions.
- dependencies_and_callers: Used by extension compatibility remapping.
- edge_cases_or_failure_modes: Prevents legacy extension type import failures.
- validation_or_tests: Covered by `legacy-pi-ai-type-remap.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2125 `file` `packages/coding-agent/src/internal-urls/memory-protocol.ts`
- cursor: `[_]`
- core_role: Internal `memory://` protocol handler.
- algorithmic_behavior: Collects memory roots from active sessions, resolves `memory://root` and relative paths, realpath-checks containment, reads target files, and returns markdown/plain resources.
- inputs_outputs_state: Inputs are `InternalUrl` values and memory roots. Outputs are `InternalResource` content or undefined/errors.
- gates_or_invariants: Only `memory://root` namespace is valid; target and parent realpaths must stay under memory root; default file is `memory_summary.md`.
- dependencies_and_callers: Used by internal URL/read tooling and memory UI.
- edge_cases_or_failure_modes: Handles traversal, missing files, invalid namespace, symlinks escaping root, and multiple roots.
- validation_or_tests: Covered indirectly by read/internal URL tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2155 `file` `packages/coding-agent/src/mcp/loader.ts`
- cursor: `[_]`
- core_role: MCP discovery/loading coordinator.
- algorithmic_behavior: Resolves optional MCP tool cache, constructs manager, loads custom tools, collects connected server names/Exa keys/errors, and returns empty result on discovery failure.
- inputs_outputs_state: Inputs are cwd, storage, settings/options. Outputs are `MCPToolsLoadResult` with manager/tools/errors/server names.
- gates_or_invariants: Whole discovery failure should not crash session startup; cache resolution tolerates missing storage.
- dependencies_and_callers: Used by session startup/tool discovery and slash MCP helpers.
- edge_cases_or_failure_modes: Handles manager creation errors, partial server failures, missing cache, and unavailable Exa credentials.
- validation_or_tests: MCP controller/helper tests cover downstream behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2185 `file` `packages/coding-agent/src/modes/interactive-mode.ts`
- cursor: `[_]`
- core_role: Main interactive TUI mode coordinator.
- algorithmic_behavior: Manages editor height, input/controller wiring, loop/goal/plan modes, todos, loaders, subagent HUD/session focus, STT cursor animation, slash commands, compaction/handoff/shake dispatch, and extension UI hooks.
- inputs_outputs_state: Inputs are keyboard commands, session events, settings, slash commands, tool events, and UI dimensions. Outputs are TUI renders, session commands, notifications, and mode state transitions.
- gates_or_invariants: UI must avoid corrupting render state during streaming/maintenance; loaders must clear on completion/errors; session focus must retarget events coherently.
- dependencies_and_callers: Central consumer of controllers, components, AgentSession, MCP/tooling, settings, and TUI renderer.
- edge_cases_or_failure_modes: Handles interrupted turns, idle compaction, plan/todo synchronization, focused subagent disappearance, and extension command failures.
- validation_or_tests: Covered by many `test/modes/controllers/*`, input-controller, and interactive-mode related tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2215 `file` `packages/coding-agent/src/session/auth-storage.ts`
- cursor: `[_]`
- core_role: AuthStorage re-export compatibility module.
- algorithmic_behavior: Re-exports `AuthStorage`, credential store, sentinel constants, and auth-related types from `@oh-my-pi/pi-ai`.
- inputs_outputs_state: No runtime state beyond delegated exports.
- gates_or_invariants: Export surface must stay compatible for coding-agent imports.
- dependencies_and_callers: Used throughout coding-agent session/auth code.
- edge_cases_or_failure_modes: Mis-export would break imports, but no local algorithm.
- validation_or_tests: Auth behavior validated in `packages/ai/test/auth-storage-check-credentials.test.ts`.
- skip_candidate: `yes: implementation-less shim/re-export`

### OH_MY_HUMANIZE_MAIN-HZ-2245 `file` `packages/coding-agent/src/slash-commands/marketplace-install-parser.ts`
- cursor: `[_]`
- core_role: Parser for marketplace/plugin install slash command arguments.
- algorithmic_behavior: Parses `/marketplace install [--force] [--scope user|project] <name@marketplace>` and generic plugin-scope args, returning structured args or usage errors.
- inputs_outputs_state: Inputs are raw slash-command rest strings. Outputs are parsed names/force/scope or error objects.
- gates_or_invariants: Scope must be `user` or `project`; exactly one package target is expected; unknown flags produce usage errors.
- dependencies_and_callers: Used by marketplace slash command handlers.
- edge_cases_or_failure_modes: Handles missing target, duplicate/invalid flags, absent flag value, and invalid scope.
- validation_or_tests: Covered by marketplace manager/parser tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2275 `file` `packages/coding-agent/src/task/subprocess-tool-registry.ts`
- cursor: `[_]`
- core_role: Registry for subprocess-originated tool events/data.
- algorithmic_behavior: Registers handlers by tool/event name, records/extracts tool event data, and exposes a singleton registry.
- inputs_outputs_state: Inputs are subprocess tool events with handler names/data. Outputs are extracted grouped data and handler dispatch results.
- gates_or_invariants: Tool handlers are keyed by name; extraction returns arrays per data key.
- dependencies_and_callers: Used by task/subagent subprocess tooling.
- edge_cases_or_failure_modes: Handles missing handlers, unknown event data, and multiple events per key.
- validation_or_tests: Covered indirectly by task/subagent tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2305 `file` `packages/coding-agent/src/tools/eval-render.ts`
- cursor: `[_]`
- core_role: Renderer for eval tool calls/results.
- algorithmic_behavior: Normalizes language/cells, coalesces agent status events by ID, renders agent progress trees, formats filesystem/git/status events, and renders JSON/text cell outputs with preview truncation.
- inputs_outputs_state: Inputs are eval args, result details/status events, theme, expanded state, and spinner frame. Outputs are summary/body terminal render lines.
- gates_or_invariants: Renderer is split from runtime to avoid circular imports; preview lines are bounded by `EVAL_DEFAULT_PREVIEW_LINES`; status events are normalized.
- dependencies_and_callers: Used by eval tool UI renderer and tests.
- edge_cases_or_failure_modes: Handles partial/missing args, unknown event values, failed/aborted agents, huge JSON outputs, and expanded vs compact render paths.
- validation_or_tests: Covered by eval fallback and renderer-related tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2335 `file` `packages/coding-agent/src/tools/memory-retain.ts`
- cursor: `[_]`
- core_role: Agent tool for retaining memories.
- algorithmic_behavior: Defines a typed `retain` schema; for mnemopi calls scoped remember; for Hindsight enqueues retain; returns stored/queued count text/details.
- inputs_outputs_state: Inputs are memory text/scope and active memory backend. Outputs are tool result content and memory backend mutations/queue entries.
- gates_or_invariants: Tool is only meaningful when backend is `hindsight` or `mnemopi`; schema requires retainable content.
- dependencies_and_callers: Used by tool registry/session memory integration; depends on Hindsight/mnemopi backends.
- edge_cases_or_failure_modes: Handles disabled/unsupported memory backend and backend failures.
- validation_or_tests: Memory integration tests indirectly validate.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2365 `file` `packages/coding-agent/src/tts/tts-worker.ts`
- cursor: `[_]`
- core_role: Local text-to-speech worker runtime.
- algorithmic_behavior: Lazily installs/configures `kokoro-js`/transformers runtime, stubs sharp, caches model promises, chooses device/dtype with fallback, serializes synthesis queue, and supports streaming sessions that buffer text before splitter readiness.
- inputs_outputs_state: Inputs are TTS requests, stream push/end/cancel events, model keys, voice/speed config. Outputs are audio/progress/error/log events through `TtsTransport`.
- gates_or_invariants: Requests are serialized; model loads are cached; device fallback tries safer alternatives; stream sessions are tracked by ID and cleaned on end/cancel/error.
- dependencies_and_callers: Used by TTS feature worker host; depends on tiny model device config, transformers/Kokoro runtime, and transport protocol.
- edge_cases_or_failure_modes: Handles runtime install failure, model load failure, webgpu/cpu fallback, cancelled streams, splitter initialization lag, and queued request errors.
- validation_or_tests: Covered indirectly by TTS/tiny runtime tests if present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2395 `file` `packages/coding-agent/src/utils/markit.ts`
- cursor: `[_]`
- core_role: Markit document conversion wrapper.
- algorithmic_behavior: Installs MuPDF WASM logging and embedded module, normalizes extensions/errors, runs Markit conversions under optional abort signals, and finalizes markdown result metadata.
- inputs_outputs_state: Inputs are file paths/buffers, extensions, and abort signals. Outputs are markdown conversion results.
- gates_or_invariants: MuPDF logger is installed once; unsupported/failed conversions normalize error text; markdown output is optional but result shape is stable.
- dependencies_and_callers: Used by document/web/file conversion paths; depends on `markit` and embedded MuPDF WASM.
- edge_cases_or_failure_modes: Handles aborts, bad extension, missing markdown, WASM logger output, and conversion exceptions.
- validation_or_tests: Markit converter tests indirectly cover.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2425 `file` `packages/coding-agent/src/workflow/monitor-display-mode.ts`
- cursor: `[_]`
- core_role: Workflow monitor display-mode parser/labeler.
- algorithmic_behavior: Parses string inputs into `full`, `compact`, or `collapsed`, and maps modes to user-facing labels.
- inputs_outputs_state: Inputs are display mode strings. Outputs are typed mode or label.
- gates_or_invariants: Unknown strings return undefined.
- dependencies_and_callers: Used by workflow monitor UI/settings.
- edge_cases_or_failure_modes: Handles invalid or missing mode values.
- validation_or_tests: Covered indirectly by workflow monitor tests.
- skip_candidate: `yes: tiny parser/label helper`

### OH_MY_HUMANIZE_MAIN-HZ-2455 `file` `packages/coding-agent/test/core/hashline-loop-guard.test.ts`
- cursor: `[_]`
- core_role: Hashline no-op loop guard regression tests.
- algorithmic_behavior: Creates repeated/no-op hashline edit attempts and asserts the loop guard blocks unproductive repeated edits.
- inputs_outputs_state: Inputs are file content, hashline edit params, and repeated execution state. Outputs are success/error results and guard state.
- gates_or_invariants: Repeated no-op edits should not loop indefinitely; meaningful edits remain allowed.
- dependencies_and_callers: Exercises hashline executor/guard in core edit tooling.
- edge_cases_or_failure_modes: Covers stale anchors and repeated identical no-op operations.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2485 `file` `packages/coding-agent/test/debug/raw-sse-report-bundle.test.ts`
- cursor: `[_]`
- core_role: Raw SSE debug report bundle test.
- algorithmic_behavior: Builds report bundle fixtures and asserts raw SSE/debug artifacts are included or shaped correctly.
- inputs_outputs_state: Inputs are synthetic raw SSE/session/debug data. Outputs are report bundle objects/files.
- gates_or_invariants: Debug bundle must preserve enough raw SSE context for diagnosis without missing required metadata.
- dependencies_and_callers: Exercises debug report bundle code.
- edge_cases_or_failure_modes: Handles missing raw data, empty streams, and bundle metadata.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2515 `file` `packages/coding-agent/test/extensibility/legacy-pi-ai-type-remap.test.ts`
- cursor: `[_]`
- core_role: Legacy extension import remapping tests.
- algorithmic_behavior: Verifies old `@scope/pi-ai` root `Type` and legacy pi package root imports remap to compatibility shims.
- inputs_outputs_state: Inputs are synthetic extension source/import paths. Outputs are resolved/remapped module paths or compiled extension behavior.
- gates_or_invariants: Legacy extensions must keep working without dynamic/inline import failures.
- dependencies_and_callers: Exercises extensibility loader/remapper and `legacy-pi-ai-shim.ts`.
- edge_cases_or_failure_modes: Covers issue #1437 and #1474 legacy import surfaces.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2545 `file` `packages/coding-agent/test/marketplace/manager.test.ts`
- cursor: `[_]`
- core_role: Marketplace manager installation/update tests.
- algorithmic_behavior: Exercises marketplace plugin lookup, install/update/remove behavior, manifests, scope handling, force installs, and filesystem outputs.
- inputs_outputs_state: Inputs are fake marketplace packages, plugin scopes, manager config, and install args. Outputs are installed plugin files/manifests and manager state.
- gates_or_invariants: Scope isolation, manifest validation, force overwrite rules, and package identity must be enforced.
- dependencies_and_callers: Exercises marketplace manager and install parser.
- edge_cases_or_failure_modes: Covers missing packages, invalid manifests, existing installs, forced replacement, and project/user scope differences.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2575 `file` `packages/coding-agent/test/session-manager/session-id.test.ts`
- cursor: `[_]`
- core_role: Session ID generation tests.
- algorithmic_behavior: Asserts `SessionManager` emits UUIDv7-like IDs matching a regex and distinct session identities.
- inputs_outputs_state: Inputs are new `SessionManager` instances. Outputs are session ID strings.
- gates_or_invariants: Session IDs must be UUIDv7 format with correct version/variant bits.
- dependencies_and_callers: Exercises session manager construction.
- edge_cases_or_failure_modes: Prevents non-sortable/non-UUID session ID regressions.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2605 `file` `packages/coding-agent/test/slash-commands/shake.test.ts`
- cursor: `[_]`
- core_role: `/shake` slash command dispatch tests.
- algorithmic_behavior: Tests ACP and TUI slash-command paths dispatch shake compaction actions with expected session calls/results.
- inputs_outputs_state: Inputs are slash command invocations and mocked runtimes. Outputs are command results and session shake calls.
- gates_or_invariants: ACP and TUI command paths should both trigger the same shake behavior.
- dependencies_and_callers: Exercises slash-command dispatch and session compaction/shake entry point.
- edge_cases_or_failure_modes: Handles missing session capability or failed shake call.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2635 `file` `packages/coding-agent/test/tool-discovery/subagent.test.ts`
- cursor: `[_]`
- core_role: Subagent discovery mode resolution tests.
- algorithmic_behavior: Checks effective discovery mode calculation for subagent/tool discovery settings.
- inputs_outputs_state: Inputs are configured discovery modes and subagent settings. Outputs are resolved effective modes.
- gates_or_invariants: Explicit settings override defaults; disabled modes remain disabled.
- dependencies_and_callers: Exercises tool discovery/subagent logic.
- edge_cases_or_failure_modes: Covers unset/default/disabled combinations.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2665 `file` `packages/coding-agent/test/tools/eval-fallback.test.ts`
- cursor: `[_]`
- core_role: Eval tool language dispatch fallback tests.
- algorithmic_behavior: Mocks eval runtimes and asserts language selection/fallback behavior when executing eval tool calls.
- inputs_outputs_state: Inputs are eval tool args/language fields and mocked executor availability. Outputs are selected executor calls and tool results.
- gates_or_invariants: Unknown/missing language must route to safe defaults or return clear errors.
- dependencies_and_callers: Exercises eval tool dispatch.
- edge_cases_or_failure_modes: Handles unsupported languages and executor failure.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2695 `file` `packages/coding-agent/test/tools/plan-mode-guard-local.test.ts`
- cursor: `[_]`
- core_role: Plan-mode filesystem guard tests.
- algorithmic_behavior: Tests `local://` path resolution and `enforcePlanModeWrite` behavior for working tree vs local sandbox paths.
- inputs_outputs_state: Inputs are file paths/URLs, cwd, local sandbox config, and plan-mode state. Outputs are resolved paths or guard errors.
- gates_or_invariants: Working-tree writes are blocked in plan mode; `local://` sandbox writes are allowed when contained.
- dependencies_and_callers: Exercises plan-mode write guard and path resolver.
- edge_cases_or_failure_modes: Covers literal path resolution, absolute local-sandbox paths, traversal, and working-tree rejection.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2725 `file` `packages/coding-agent/test/tools/web-search-exa.test.ts`
- cursor: `[_]`
- core_role: Exa web-search request/answer synthesis tests.
- algorithmic_behavior: Tests search type normalization, Exa request body construction, answer synthesis from results, `searchExa` transport behavior, MCP fallback, AuthStorage credentials, and error surfaces.
- inputs_outputs_state: Inputs are search args, credentials, fake Exa/MCP responses. Outputs are request JSON, synthesized markdown/text, and tool errors.
- gates_or_invariants: Search types must normalize to allowed Exa values; credential source/fallback must be deterministic; summaries should cite result content semantically.
- dependencies_and_callers: Exercises web search tool Exa integration.
- edge_cases_or_failure_modes: Handles missing API key, MCP fallback, empty results, fetch errors, and malformed summaries.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2755 `file` `packages/coding-agent/test/workflow/lifecycle-store.test.ts`
- cursor: `[_]`
- core_role: Workflow lifecycle event-store tests.
- algorithmic_behavior: Builds/replays workflow events and asserts reconstruction of attempts, checkpoints, restarts, approvals, and lifecycle state.
- inputs_outputs_state: Inputs are event records and store operations. Outputs are reconstructed workflow lifecycle views.
- gates_or_invariants: Event replay must be deterministic; change approval and restart/checkpoint gates must preserve ordering.
- dependencies_and_callers: Exercises workflow lifecycle store.
- edge_cases_or_failure_modes: Covers missing events, repeated attempts, checkpoint ordering, and approval/restart transitions.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2785 `file` `packages/collab-web/src/tool-render/types.ts`
- cursor: `[_]`
- core_role: Shared React tool-render contract types.
- algorithmic_behavior: Defines result block shapes, host callbacks, render props, and renderer interface; no runtime logic.
- inputs_outputs_state: Inputs/outputs are compile-time renderer prop/result shapes.
- gates_or_invariants: Renderers depend on stable optional `details`, `args`, and host capabilities.
- dependencies_and_callers: Used by collab web tool renderers including `generate-image.tsx`.
- edge_cases_or_failure_modes: Runtime unaffected unless type contract drifts from actual renderer data.
- validation_or_tests: Type checking and renderer tests validate.
- skip_candidate: `yes: type-only contract file`

### OH_MY_HUMANIZE_MAIN-HZ-2815 `file` `packages/mnemopi/src/core/temporal-parser.ts`
- cursor: `[_]`
- core_role: Natural-language temporal parser for memory/query text.
- algorithmic_behavior: Parses references, relative days, named weekdays, deltas, absolute dates/months/years, named times, tags, and extracts date info from text.
- inputs_outputs_state: Inputs are text and optional reference time. Outputs are `TemporalInfo`, parsed date tuples, ISO date strings, and temporal tags.
- gates_or_invariants: Dates are UTC/date-only normalized; invalid dates return null/unknown; relative calculations use reference date.
- dependencies_and_callers: Used by mnemopi extraction/query memory logic.
- edge_cases_or_failure_modes: Handles leap/invalid dates, week/month/year precision, ambiguous named days, and absent temporal content.
- validation_or_tests: Temporal parsing likely covered by mnemopi core tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2845 `file` `packages/tui/src/components/cancellable-loader.ts`
- cursor: `[_]`
- core_role: Loader component with cancel affordance.
- algorithmic_behavior: Extends `Loader` and adds cancellation label/hint behavior for cancellable long-running operations.
- inputs_outputs_state: Inputs are loader props and cancel state. Outputs are rendered loader lines.
- gates_or_invariants: Should preserve base loader animation while exposing cancel indication.
- dependencies_and_callers: Used by TUI operations that can be interrupted.
- edge_cases_or_failure_modes: Minimal; render contract could break if base loader API changes.
- validation_or_tests: Covered indirectly by TUI render tests.
- skip_candidate: `yes: small UI component wrapper`

### OH_MY_HUMANIZE_MAIN-HZ-2875 `file` `python/robomp/web/src/env.d.ts`
- cursor: `[_]`
- core_role: Vite/client ambient type declaration for robomp web.
- algorithmic_behavior: No runtime algorithm; declares frontend env types.
- inputs_outputs_state: Compile-time only.
- gates_or_invariants: Must remain compatible with Vite type expectations.
- dependencies_and_callers: Consumed by TypeScript in robomp web.
- edge_cases_or_failure_modes: None at runtime.
- validation_or_tests: Type checking validates.
- skip_candidate: `yes: ambient .d.ts only`

### OH_MY_HUMANIZE_MAIN-HZ-2905 `file` `crates/pi-shell/src/minimizer/filters/dotnet.rs`
- cursor: `[_]`
- core_role: .NET CLI output minimizer filter.
- algorithmic_behavior: Detects supported `dotnet` subcommands, filters build/test/format/general output, extracts diagnostics/failures/summaries, compacts JSON format output, and removes boilerplate/noise.
- inputs_outputs_state: Inputs are program/subcommand, command output, and exit code. Outputs are minimized text plus minimizer metadata.
- gates_or_invariants: Failure signals and summaries must be preserved; boilerplate and path noise can be removed; JSON format rows are compacted only when parse succeeds.
- dependencies_and_callers: Used by pi-shell minimizer pipeline and fixture tests.
- edge_cases_or_failure_modes: Handles MSBuild diagnostics, test failure sections, format JSON schema variants, path-looking lines, and successful noisy output.
- validation_or_tests: Covered by `crates/pi-shell/tests/minimizer_fixtures.rs`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2935 `file` `packages/ai/src/registry/oauth/index.ts`
- cursor: `[_]`
- core_role: OAuth provider registry and credential-to-API-key resolver.
- algorithmic_behavior: Derives built-in OAuth providers from `PROVIDER_REGISTRY`, registers/unregisters custom providers, dispatches refresh calls, parses Perplexity JWT expiry, resolves OAuth API key from `AuthStorage`, and lists providers.
- inputs_outputs_state: Inputs are provider IDs, auth storage rows, refresh tokens, and custom provider registrations. Outputs are OAuth access/API keys, refreshed credentials, and provider info lists.
- gates_or_invariants: Expired credentials are refused unless refresh succeeds; custom providers are source-scoped for unregister; Perplexity expiry is decoded from JWT payload.
- dependencies_and_callers: Used by AuthStorage, login flows, model providers, and catalog generator OAuth discovery.
- edge_cases_or_failure_modes: Handles missing provider, missing auth storage, expired JWT/token, refresh failure, and malformed JWT payload.
- validation_or_tests: Covered by auth-storage credential tests and provider registry tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2965 `file` `packages/coding-agent/src/autoresearch/tools/init-experiment.ts`
- cursor: `[_]`
- core_role: Autoresearch experiment initialization tool.
- algorithmic_behavior: Validates init params, requires/creates `autoresearch.sh` for new sessions/segments, auto-commits harness setup on `autoresearch/*` branches when dirty, updates storage/runtime/dashboard, and renders tool call label.
- inputs_outputs_state: Inputs are experiment name/goal/session/segment params, cwd git state, storage/runtime. Outputs are initialized experiment state, commit info, and tool result details.
- gates_or_invariants: New session/segment requires harness command; dirty harness setup commit is branch-gated; head SHA/pending changes are detected before state update.
- dependencies_and_callers: Used by autoresearch custom tool system; depends on Bun shell/git, storage/runtime.
- edge_cases_or_failure_modes: Handles missing harness, dirty repo, non-autoresearch branch, failed git commands, and invalid params.
- validation_or_tests: Autoresearch tests likely cover; no direct assigned test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2995 `file` `packages/coding-agent/src/commit/changelog/detect.ts`
- cursor: `[_]`
- core_role: Changelog boundary detector for commit agent.
- algorithmic_behavior: For staged non-changelog files, walks upward from each path to cwd looking for nearest `CHANGELOG.md`, groups files by changelog boundary, and returns boundary records.
- inputs_outputs_state: Inputs are cwd and staged file paths. Outputs are `ChangelogBoundary[]`.
- gates_or_invariants: Existing changelog files are skipped as inputs; upward search stops at cwd root; missing changelog returns null/no boundary.
- dependencies_and_callers: Used by commit/changelog tooling.
- edge_cases_or_failure_modes: Handles nested packages, files outside package changelog, and path normalization.
- validation_or_tests: Covered indirectly by commit-agent changelog tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3025 `file` `packages/coding-agent/src/eval/__tests__/kernel-spawn.test.ts`
- cursor: `[_]`
- core_role: Kernel process spawn/window visibility tests.
- algorithmic_behavior: Tests `shouldHideKernelWindow`, console-attached TTY fallback heuristic, and host inheritable console detection.
- inputs_outputs_state: Inputs are platform/env/TTY conditions and mocked FFI availability. Outputs are booleans for spawn window behavior.
- gates_or_invariants: Kernel windows should be hidden only when safe for host console behavior.
- dependencies_and_callers: Exercises eval kernel spawn helpers.
- edge_cases_or_failure_modes: Covers Windows console attachment, FFI fallback, and non-TTY hosts.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3055 `file` `packages/coding-agent/src/extensibility/extensions/get-commands-handler.ts`
- cursor: `[_]`
- core_role: Dynamic slash-command aggregation for extensions/session.
- algorithmic_behavior: Collects commands from extension runner, prompt custom commands, and skills when enabled; excludes built-ins and maps command source location.
- inputs_outputs_state: Inputs are command-capable session state and extension/custom/skill command definitions. Outputs are `SlashCommandInfo[]`.
- gates_or_invariants: Built-in commands are excluded from dynamic list; location/source metadata is normalized.
- dependencies_and_callers: Used by slash command UI/help/autocomplete.
- edge_cases_or_failure_modes: Handles missing extension runner, disabled skill commands, and unknown custom command source.
- validation_or_tests: Covered by extensibility/command tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3085 `file` `packages/coding-agent/src/markit/converters/mammoth.d.ts`
- cursor: `[_]`
- core_role: Type declarations for Mammoth converter integration.
- algorithmic_behavior: No runtime algorithm; declares external module/types for converter use.
- inputs_outputs_state: Compile-time only.
- gates_or_invariants: Must match consumed Mammoth API enough for type checking.
- dependencies_and_callers: Used by markit/mammoth converter TypeScript code.
- edge_cases_or_failure_modes: Type drift could hide runtime API mismatch.
- validation_or_tests: Type checking validates.
- skip_candidate: `yes: declaration file only`

### OH_MY_HUMANIZE_MAIN-HZ-3115 `file` `packages/coding-agent/src/modes/components/dynamic-border.ts`
- cursor: `[_]`
- core_role: Dynamic border TUI component.
- algorithmic_behavior: Implements a component that renders border visuals based on current state/theme.
- inputs_outputs_state: Inputs are component props/theme/frame state. Outputs are TUI render lines.
- gates_or_invariants: Must implement `Component` render contract.
- dependencies_and_callers: Used by interactive-mode components.
- edge_cases_or_failure_modes: UI-only; risk is visual mismatch under width/theme changes.
- validation_or_tests: Covered indirectly by TUI/component render tests.
- skip_candidate: `yes: small UI rendering component`

### OH_MY_HUMANIZE_MAIN-HZ-3145 `file` `packages/coding-agent/src/modes/components/settings-defs.ts`
- cursor: `[_]`
- core_role: Settings UI definition resolver.
- algorithmic_behavior: Maps setting paths/metadata into boolean, enum, submenu, or text-input definitions; resolves options/conditions/tabs/default display values.
- inputs_outputs_state: Inputs are settings metadata/path definitions and runtime condition flags. Outputs are setting definition arrays for tabs or individual paths.
- gates_or_invariants: Unsupported metadata returns null; runtime options are preserved as `"runtime"`; display defaults are stringified predictably.
- dependencies_and_callers: Used by settings TUI components.
- edge_cases_or_failure_modes: Handles conditionally hidden settings, missing defaults, runtime-populated option lists, and unknown paths.
- validation_or_tests: Covered by settings UI tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3175 `file` `packages/coding-agent/src/modes/controllers/session-focus-controller.ts`
- cursor: `[_]`
- core_role: UI controller for focusing parent/subagent sessions.
- algorithmic_behavior: Retargets UI to subagent session, supports parent/unfocus, subscribes to registry removal/dead status, and synthesizes missing assistant `message_start` when attaching mid-turn.
- inputs_outputs_state: Inputs are session IDs, registry events, parent session, and focus actions. Outputs are focused session state and synthetic UI events.
- gates_or_invariants: Focused session must exist and remain alive; removal/dead status triggers unfocus; mid-turn attach must have a message-start boundary.
- dependencies_and_callers: Used by interactive mode subagent focus/HUD features.
- edge_cases_or_failure_modes: Handles missing subagent, parent disappearance, already-focused session, and mid-stream attach.
- validation_or_tests: Covered by session focus/controller tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3205 `file` `packages/coding-agent/src/slash-commands/helpers/mcp.ts`
- cursor: `[_]`
- core_role: ACP/TUI `/mcp` slash-command helper.
- algorithmic_behavior: Parses add/search args, validates MCP config, prepares OAuth-backed temporary connections, lists/redacts configured servers, tests connections, lists resources/prompts, enables/disables/removes servers, and dispatches help/errors.
- inputs_outputs_state: Inputs are slash command rest strings, runtime settings/storage, MCP config. Outputs are `SlashCommandResult` text and config mutations.
- gates_or_invariants: URLs are redacted in list output; temp connections disconnect reliably; unsupported TUI-only verbs are rejected in ACP path; scope must be user/project.
- dependencies_and_callers: Used by slash-command runtime and MCP loader/manager.
- edge_cases_or_failure_modes: Handles invalid add args, OAuth preparation failure, search no results, test connection failure, remove missing server, and redaction of userinfo/query.
- validation_or_tests: Covered by MCP authorization/link/controller tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3235 `file` `packages/coding-agent/src/web/scrapers/crates-io.ts`
- cursor: `[_]`
- core_role: Special web scraper for crates.io package pages.
- algorithmic_behavior: Detects crate name from URL, fetches crates.io API metadata and optional docs.rs README, and formats markdown summary.
- inputs_outputs_state: Inputs are crates.io URLs, timeout, abort signal. Outputs are scraped markdown/resource result.
- gates_or_invariants: URL must identify a crate; fetches respect timeout/signal; missing README is optional.
- dependencies_and_callers: Used by web fetch/scraper system.
- edge_cases_or_failure_modes: Handles invalid crate URL, API errors, missing docs README, and aborted fetch.
- validation_or_tests: Web scraper tests cover similar special handlers.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3265 `file` `packages/coding-agent/src/web/scrapers/nvd.ts`
- cursor: `[_]`
- core_role: Special web scraper for NVD CVE pages/API.
- algorithmic_behavior: Extracts CVE ID, fetches NVD API, selects descriptions, CVSS metrics, CWEs, affected CPEs, and references, then formats markdown.
- inputs_outputs_state: Inputs are NVD/CVE URLs, timeout, signal. Outputs are markdown CVE summaries.
- gates_or_invariants: CVE ID must be valid; CPE extraction walks nested configurations; output should tolerate missing CVSS/CWE fields.
- dependencies_and_callers: Used by web scraper dispatch.
- edge_cases_or_failure_modes: Handles no vulnerabilities, missing metrics, API errors, nested CPE trees, and aborts.
- validation_or_tests: Web scraper tests indirectly validate special handlers.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3295 `file` `packages/coding-agent/src/web/scrapers/vimeo.ts`
- cursor: `[_]`
- core_role: Special web scraper for Vimeo video metadata.
- algorithmic_behavior: Extracts Vimeo video ID from URL, fetches oEmbed/config data, collects metadata and progressive stream URLs, and formats result text.
- inputs_outputs_state: Inputs are Vimeo URLs, timeout, signal. Outputs are video metadata/stream markdown.
- gates_or_invariants: Video ID extraction must match supported URL forms; fetches respect timeout/signal.
- dependencies_and_callers: Used by web scraper dispatch.
- edge_cases_or_failure_modes: Handles invalid URLs, private/missing config, no streams, and fetch errors.
- validation_or_tests: Web scraper tests cover the dispatch style.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3325 `file` `packages/coding-agent/test/modes/components/plan-toc.test.ts`
- cursor: `[_]`
- core_role: Plan table-of-contents parser/render tests.
- algorithmic_behavior: Tests section parsing, heading stripping, section joining, deletion span calculation, and inline markdown stripping.
- inputs_outputs_state: Inputs are markdown plan text. Outputs are parsed `PlanSection[]`, joined text, deletion ranges, and stripped titles.
- gates_or_invariants: Heading levels/order must be preserved; deletion spans should remove exactly the selected section.
- dependencies_and_callers: Exercises plan TOC component helpers.
- edge_cases_or_failure_modes: Covers nested headings, markdown emphasis/code in titles, and first/last section deletion.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3355 `file` `packages/coding-agent/test/modes/controllers/event-controller-toolcall-finalize.test.ts`
- cursor: `[_]`
- core_role: Event controller streaming tool-call finalization test.
- algorithmic_behavior: Builds streaming assistant messages with tool-call args updates and asserts final assistant block is finalized when args stream completes.
- inputs_outputs_state: Inputs are streaming assistant message deltas and fixture controller. Outputs are finalized UI/message state.
- gates_or_invariants: Tool-call arg streaming must not leave assistant block in partial/unfinished state.
- dependencies_and_callers: Exercises event controller.
- edge_cases_or_failure_modes: Covers mid-stream args reveal/finalize race.
- validation_or_tests: File itself is validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3385 `file` `packages/coding-agent/test/tools/web-scrapers/wikipedia.test.ts`
- cursor: `[_]`
- core_role: Optional integration test for Wikipedia web scraper.
- algorithmic_behavior: Runs only when `WEB_FETCH_INTEGRATION` is set and validates Wikipedia scraper/fetch output.
- inputs_outputs_state: Inputs are live/fixture Wikipedia URLs. Outputs are scraped page summaries.
- gates_or_invariants: Skips by default without env to keep suite network-free.
- dependencies_and_callers: Exercises web scraper integration path.
- edge_cases_or_failure_modes: Handles live network variability by env gating.
- validation_or_tests: File itself is gated validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3415 `file` `packages/collab-web/src/tool-render/tools/generate-image.tsx`
- cursor: `[_]`
- core_role: React renderer for generate-image tool calls/results.
- algorithmic_behavior: Merges `details.images` into result images, renders prompt/size/aspect/changes summary fields, and displays generated images or fallback text.
- inputs_outputs_state: Inputs are tool args, result blocks/details, and host render props. Outputs are React nodes for summary/body.
- gates_or_invariants: Partial JSON args must be tolerated; images can come from result content or details.
- dependencies_and_callers: Uses shared tool-render types and collab web renderer registry.
- edge_cases_or_failure_modes: Handles missing result, failed generation, no images, multiple images, and partial args.
- validation_or_tests: Renderer tests/snapshots indirectly validate.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3445 `file` `packages/mnemopi/src/core/extraction/diagnostics.ts`
- cursor: `[_]`
- core_role: Extraction diagnostics/statistics accumulator for memory extraction tiers.
- algorithmic_behavior: Tracks attempts/success/no-output/failure by tier, records capped sanitized error samples, computes total success rate, snapshots state, and exposes singleton getters/reset.
- inputs_outputs_state: Inputs are tier names, success/failure/no-output events, exceptions/reasons. Outputs are `ExtractionStatsSnapshot`.
- gates_or_invariants: Tier names must be one of `host`, `remote`, `local`, `cloud`, `wrapper`; error messages are capped/sanitized; samples capped at 10 per tier.
- dependencies_and_callers: Used by mnemopi extraction pipeline and diagnostics endpoints.
- edge_cases_or_failure_modes: Handles unknown tiers by throwing, non-Error exceptions, control characters in logs, and reset semantics.
- validation_or_tests: Covered indirectly by mnemopi extraction tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3475 `file` `packages/stats/src/client/ui/ErrorState.tsx`
- cursor: `[_]`
- core_role: Stats web UI error display component.
- algorithmic_behavior: Renders an error message with optional retry callback/button and optional class name.
- inputs_outputs_state: Inputs are `error`, `onRetry`, and `className` props. Outputs are React UI.
- gates_or_invariants: Retry affordance is conditional on callback.
- dependencies_and_callers: Used by stats dashboard client UI.
- edge_cases_or_failure_modes: UI-only; handles absent retry.
- validation_or_tests: Component/UI tests indirectly validate.
- skip_candidate: `yes: simple presentational component, not core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3505 `file` `packages/coding-agent/src/commit/agentic/tools/analyze-file.ts`
- cursor: `[_]`
- core_role: Commit-agent tool that fans out file analysis to quick_task subagents.
- algorithmic_behavior: Builds a `ToolSession`, renders static prompt template with file/goal/related files, spawns one `TaskTool` call per file, flattens results, and aggregates duration/details.
- inputs_outputs_state: Inputs are file list, optional goal, commit-agent numstat state, auth/model/settings/session context. Outputs are analysis text and subagent result details.
- gates_or_invariants: Params require at least one file; output schema enforces summary/highlights/risks; session suppresses spawn advisory and uses sync fallback.
- dependencies_and_callers: Used by commit agentic workflow; depends on `TaskTool`, prompt template, and git-file priority helpers.
- edge_cases_or_failure_modes: Handles no subagent output, missing numstat entries, binary/test/config file type inference, and signal cancellation.
- validation_or_tests: Commit-agent/tool tests indirectly validate.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3535 `file` `packages/coding-agent/src/markit/converters/pdf/headers.ts`
- cursor: `[_]`
- core_role: PDF running header/footer removal algorithm.
- algorithmic_behavior: Buckets top/bottom zone text per page, computes global frequency and longest consecutive run, marks repeated texts, and removes matching text boxes in place.
- inputs_outputs_state: Inputs are `PageContent[]` with text boxes/bounds. Outputs are mutated pages with repeated headers/footers removed.
- gates_or_invariants: Requires at least 5 pages; top zone `midY>=700`, bottom zone `midY<=80`; repeated if on at least max(3, 20% pages) or 8 consecutive pages.
- dependencies_and_callers: Used by PDF-to-markdown converter.
- edge_cases_or_failure_modes: Handles chapter-level repeated headers, whitespace normalization, empty text, and avoids removing body-zone text.
- validation_or_tests: Converter/PDF tests indirectly validate.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3565 `file` `packages/coding-agent/src/tools/browser/cmux/socket-client.ts`
- cursor: `[_]`
- core_role: Line-oriented Unix socket client for cmux browser tooling.
- algorithmic_behavior: Opens socket, optionally authenticates, queues JSON request jobs, processes one active job at a time, waits for newline responses with timeouts, parses `{ok,result,error}`, and rejects pending work on close/error.
- inputs_outputs_state: Inputs are socket path/password, method/params, timeout options. Outputs are parsed result records or `ToolError`.
- gates_or_invariants: Closed client rejects requests; connect/request timeouts destroy socket to avoid desync; response errors are formatted with code/message/details.
- dependencies_and_callers: Used by browser/cmux tools.
- edge_cases_or_failure_modes: Handles unknown `auth` command tolerance, socket close mid-request, malformed JSON/response, timeout, desync, and queued request rejection.
- validation_or_tests: Browser/cmux tool tests indirectly validate.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3595 `file` `packages/utils/src/vendor/mermaid-ascii/ascii/types.ts`
- cursor: `[_]`
- core_role: Vendored Mermaid ASCII graph type and coordinate utilities.
- algorithmic_behavior: Defines graph/node/edge/subgraph/style/theme types, direction constants, role canvas types, and helper functions for coordinate equality, direction movement, and grid keys.
- inputs_outputs_state: Inputs are coordinates/directions/graph model objects. Outputs are equality booleans, moved coordinates, and key strings.
- gates_or_invariants: Direction constants use 3x3 drawing-grid offsets; graph model types must match vendored renderer expectations.
- dependencies_and_callers: Used by vendored mermaid-ascii renderer utilities.
- edge_cases_or_failure_modes: Mostly type/model drift risk; coordinate helpers are simple deterministic functions.
- validation_or_tests: Mermaid ASCII renderer tests indirectly validate.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 120
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`