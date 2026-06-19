# agent_08 main 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 121
- source_commit: `6b3819fad50a89fffae899b240ad1ce065c51d23`

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-008 `file` `.fallowrc.jsonc`
- cursor: `[_]`
- core_role: Workspace-level dead-code/duplicate analysis configuration for Fallow.
- algorithmic_behavior: Defines test/script/bench entry roots at lines 9-14 so Fallow treats shared test helpers as reachable; ignores selected dependency and generated/template duplicates at lines 15-29.
- inputs_outputs_state: Input is repository file graph plus this JSONC config; output is Fallow reachability/duplicate decisions; state is static config only.
- gates_or_invariants: Test helpers imported only by tests must remain reachable; generated/native/template files are excluded from duplicate checks; `ignoreImports` avoids import duplicate noise.
- dependencies_and_callers: Consumed by `fallow` CLI/config loader during tooling runs.
- edge_cases_or_failure_modes: Missing test globs would cause `fallow fix` to strip legitimate exports; stale duplicate ignores can hide real duplicate drift.
- validation_or_tests: No direct test file; comments document known failure mode for shared test utilities.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-038 `directory` `packages/utils`
- cursor: `[_]`
- core_role: Shared runtime utility package used across CLI, TUI, AI, catalog, and agent packages.
- algorithmic_behavior: Provides environment filtering/loading, worker-host entrypoint discovery, stream readers, retry/fetch helpers, file peeking with pooled buffers, tab/editorconfig indentation resolution, path-tree rendering, logger, color math, frontmatter parsing, temp/runtime install helpers, process-tree wrappers, and vendored Mermaid-to-ASCII parsing/rendering.
- inputs_outputs_state: Inputs include process env, `.env` files, files/streams, terminal strings, Mermaid text, paths, HTTP calls, and process metadata; outputs are normalized env maps, sanitized/rendered text, retry results, logs, path trees, stream text/lines, and rendering artifacts; state includes caches in env/tab-spacing/worker-host/logger/mermaid tests.
- gates_or_invariants: Env names/values are validated; unsafe process env keys are filtered; file peeking caps buffers and waiter counts; tab width clamps to configured min/max; `index.ts` uses star exports plus namespace logger/postmortem/procmgr/prompt/ptree.
- dependencies_and_callers: Used heavily by `packages/coding-agent`, `packages/tui`, `packages/ai`, native worker spawning, logging, prompt rendering, and tests.
- edge_cases_or_failure_modes: Overlong paths, malformed env files, invalid frontmatter, broken streams, terminal width with ANSI/OSC, fullwidth Mermaid labels, async pool exhaustion, and worker-host behavior outside CLI.
- validation_or_tests: Broad package tests cover env, format, prompt, stream, worker-host, snowflake, logger serialization/startup, install id, runtime install, peek-file, path-tree, ring, loop phase, Mermaid golden/formatting/class arrows/multiline/xychart, and more.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-068 `file` `docs/resolve-tool-runtime.md`
- cursor: `[_]`
- core_role: Runtime architecture document for the hidden `resolve` tool and pending preview actions.
- algorithmic_behavior: Documents `apply` vs `discard`, one-shot tool-choice queue ownership, standing resolve handler fallback, custom tool `pushPendingAction`, and forced resolve behavior.
- inputs_outputs_state: Inputs are queued pending actions with label/source/apply/reject callbacks and optional `extra`; outputs are apply/reject `AgentToolResult`s or no-op discard messages; state resides in the session tool-choice queue rather than a separate stack.
- gates_or_invariants: Apply with no pending action fails; discard with no pending action succeeds; failed apply requeues the resolve directive; custom runtime without the hook throws an explicit unavailable error.
- dependencies_and_callers: Refers to `src/tools/resolve.ts`, `ast-edit.ts`, custom tool loader/types, and SDK APIs.
- edge_cases_or_failure_modes: Multiple pending previews obey queue order; `ast_edit` ignores reason/extra; custom `details` are public but not forwarded into resolve metadata.
- validation_or_tests: Covered indirectly by resolve, plan approval, custom tool, and ACP mode tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-098 `file` `scripts/eval-bench-runs.ts`
- cursor: `[_]`
- core_role: Benchmark report summarizer for edit/eval runs.
- algorithmic_behavior: Parses CLI flags, scans report directories for markdown reports, extracts metrics using table-cell/row regexes, optionally aggregates rows, sorts, and emits table/markdown/CSV/JSON.
- inputs_outputs_state: Inputs are report directories and flags `--aggregate`, `--format`, `--sort`; outputs are formatted summaries to stdout; state is in-memory `ReportRow[]`.
- gates_or_invariants: Requires at least one directory and exits `2` otherwise; defaults missing metrics to `0` or `NaN`; separator display maps slug to printable token.
- dependencies_and_callers: Uses `node:fs/promises`, `node:path`, and `Bun.file()` for report reads; called manually for benchmark analysis.
- edge_cases_or_failure_modes: Regex parsing is tied to markdown table labels; unknown formats/sort values are type-cast rather than validated; missing report cells can produce `NaN`.
- validation_or_tests: No direct test found; behavior is observable via generated report summaries.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-128 `directory` `packages/catalog/scripts`
- cursor: `[_]`
- core_role: Model catalog generation and generated policy application.
- algorithmic_behavior: `generate-models.ts` reads provider descriptors/discovery, applies global models.dev fallback, premium multiplier overrides, Codex pricing fallback, context/max-token caps, provider drop/normalization rules, account extraction, and writes bundled model metadata; `generated-policies.ts` mutates generated specs for Cloudflare fallback, Copilot limits, OpenAI promotion targets, canonical limits, thinking policies, Anthropic/OpenAI policies, and apply-patch tool inference.
- inputs_outputs_state: Inputs are upstream provider catalogs, descriptors, local policy tables, and access tokens; outputs are generated catalog JSON/policies; state is generation-time only.
- gates_or_invariants: Generated `models.json` must not be hand-edited; discovery-only providers are handled specially; provider-specific unusable or wire-only IDs are dropped.
- dependencies_and_callers: Invoked by `bun --cwd=packages/catalog run generate-models`; consumed by catalog package and provider identity code.
- edge_cases_or_failure_modes: Upstream schema drift, missing costs, provider alias collisions, stale premium multipliers, token parsing failures, and provider-specific model ID quirks.
- validation_or_tests: Regression tests should target descriptors/resolvers/policies rather than bundled JSON per repo rule.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-158 `directory` `packages/typescript-edit-benchmark/test`
- cursor: `[_]`
- core_role: Contract tests for edit-benchmark runner and verifier behavior.
- algorithmic_behavior: `runner.test.ts` builds synthetic tasks/runs and validates report/aggregation behavior; `verify.test.ts` exercises expected-vs-actual file subset verification, formatted equivalence, missing/extra file handling, whitespace normalization, diff stats, and indentation scoring.
- inputs_outputs_state: Inputs are temp task fixtures and `TaskRunResult` objects; outputs are verification results/report data; state is temp dirs cleaned by tests.
- gates_or_invariants: Verification should fail for semantic formatted differences, tolerate whitespace-only equivalence where intended, surface missing/unexpected files, and compute compact diffs.
- dependencies_and_callers: Tests `packages/typescript-edit-benchmark/src/runner` and `src/verify.ts`.
- edge_cases_or_failure_modes: CRLF/blank-line normalization, formatter effects masking raw differences, partial file subsets, indentation distance pairing.
- validation_or_tests: Directory is itself validation coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-188 `file` `docs/tools/eval.md`
- cursor: `[_]`
- core_role: Architecture/runtime contract for the `eval` tool.
- algorithmic_behavior: Defines structured `cells` input, per-language backend selection, sequential cell execution, idle timeout pausing around host operations, output streaming/capture, renderer behavior, JS/Python helper surfaces, `completion()`, `agent()`, `parallel()`/`pipeline()`, side effects, limits, and error handling.
- inputs_outputs_state: Inputs are JSON cell array with `language`, `code`, optional `title`, `reset`, `timeout`; outputs are text/image/JSON/markdown content plus detailed per-cell metadata and artifacts; state persists per language/runtime until reset/disposal.
- gates_or_invariants: Python/JS gated by settings/env; timeout schema range and runtime clamp are `1..3600`; interactive stdin rejected; non-`local://` writes rejected; eval is exclusive per session.
- dependencies_and_callers: Documents `src/tools/eval.ts`, backend adapters, JS worker core, Python kernel/prelude, streaming output, completion/subagent bridges.
- edge_cases_or_failure_modes: Kernel restart retry, cancellation, truncation with artifact spill, import rewriting in browser-evaluated functions, disabled backends, invalid structured output.
- validation_or_tests: Backed by eval, Python executor streaming, bridge timeout, and workflow/eval tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-218 `file` `scripts/session-stats/audit.test.ts`
- cursor: `[_]`
- core_role: Regression tests for session stats audit parsing.
- algorithmic_behavior: Tests `parseSince`, `normalizeReadPath`, and `scanFile` recovery of usage, turns, spawns, residency, and pruned tool result sizes from synthetic session entries.
- inputs_outputs_state: Inputs are temporary JSONL-like session messages/tool results; outputs are audit statistics; state is temp directory/files.
- gates_or_invariants: Relative/home paths normalize consistently; tool result pruning is counted; assistant/tool event timestamps drive residency and turn metrics.
- dependencies_and_callers: Tests sibling audit script helpers.
- edge_cases_or_failure_modes: Missing path fields, home-dir aliases, errored tool results, pruned output sizes.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-248 `directory` `packages/coding-agent/src/autoresearch`
- cursor: `[_]`
- core_role: Coding-agent extension for iterative experiment management and dashboarding.
- algorithmic_behavior: Registers autoresearch extension/tools; manages git branch setup and dirty-path parsing; stores sessions/runs in SQLite; reconstructs experiment state; parses `METRIC`/`ASI` lines; runs harness processes; logs keep/discard/crash/checks_failed outcomes; commits kept experiments or reverts failures; appends notes; renders an experiment dashboard.
- inputs_outputs_state: Inputs are cwd, session entries, tool params, harness output, git status, metrics, ASI JSON, notes; outputs are tool results, DB rows, git commits/reverts, dashboard lines, and control custom entries; state includes SQLite storage cache, runtime store, active process summaries, session/runs.
- gates_or_invariants: Requires harness file unless explicitly set up; branch prefix `autoresearch/`; dirty worktree blocks initial branch creation; scope/off-limits deviations require justification; metric comparison respects direction; confidence uses median/MAD and needs enough kept runs.
- dependencies_and_callers: Integrated through extension factory, `ToolSession`, git helpers, `@oh-my-pi/pi-utils`, TUI components, prompt templates, and agent session entries.
- edge_cases_or_failure_modes: Abandoned pending runs, dirty branch states, process timeout/cancellation, malformed ASI, unsafe object keys, scope violations, commit/revert failures, missing storage/session.
- validation_or_tests: Covered by autoresearch tests where present and by tool-level behavior; no tests executed in this read-only pass.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-278 `directory` `packages/coding-agent/src/secrets`
- cursor: `[_]`
- core_role: Secret detection, loading, obfuscation, and deobfuscation for provider context.
- algorithmic_behavior: Loads global/project secret entries, collects env secrets by key-pattern/length, validates plain/regex entries, enforces regex global flag, creates deterministic replacements/placeholders, obfuscates/deobfuscates messages/context/tools by walking strings deeply.
- inputs_outputs_state: Inputs are secrets JSON files, env vars, messages, provider context/tool definitions; outputs are redacted/placeholder text and deobfuscated context; state is per-obfuscator replacement maps.
- gates_or_invariants: Env values shorter than minimum ignored; duplicate env secret values deduped; invalid entries skipped with logging; regex flags force global matching; replacement mode only accepts valid replacement strings.
- dependencies_and_callers: Used by coding-agent provider pipeline and context preparation; depends on logger, regex compiler, message/context types.
- edge_cases_or_failure_modes: Bad regex patterns, malformed secrets file, ENOENT, prototype-pollution keys in walked objects, placeholder collision, non-string content blocks.
- validation_or_tests: Covered indirectly by provider-context and secret obfuscation tests; no direct assigned test in this set.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-308 `directory` `packages/coding-agent/test/plan-mode`
- cursor: `[_]`
- core_role: Tests for plan-mode approval, handoff, and protection behavior.
- algorithmic_behavior: Validates plan approval flow through standing resolve handler, write/edit protection while plan mode is active, plan handoff prompts/state transitions, and approved plan artifact/reference behavior.
- inputs_outputs_state: Inputs are fake sessions, plan files, tool calls, resolve actions; outputs are mode state, tool availability/protection results, artifacts, and session messages.
- gates_or_invariants: Write-capable tools remain blocked until approval; approval clears plan mode and records plan reference; discard/refinement keeps mode active; standing resolve handler must persist or clear according to action.
- dependencies_and_callers: Exercises plan-mode runtime, `resolve`, tool-choice/standing handler integration, and session artifact APIs.
- edge_cases_or_failure_modes: Missing plan title/path, rejected approval, mode toggles, protection bypass attempts.
- validation_or_tests: Directory is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-338 `file` `crates/pi-ast/src/ops.rs`
- cursor: `[_]`
- core_role: Rust AST search/rewrite operations used by native AST tools.
- algorithmic_behavior: Resolves language/strictness, compiles search/rewrite patterns, adds Rust contextual expression wrapping, collects matches with offsets/line/column/kind/text, rewrites source, applies non-overlapping edits in reverse order, walks files with ignore/glob filters.
- inputs_outputs_state: Inputs are source text, file paths, language hints, patterns, replacement rules, glob lists; outputs are matches, rewritten source, matched files, or errors; state is local per operation.
- gates_or_invariants: Explicit lang bypasses extension support; unknown lang returns supported list error; edits are sorted and overlap/out-of-bounds checked; glob syntax controls literal vs glob matching.
- dependencies_and_callers: Uses `ast_grep_core`, `ast_grep_language`, `globset`, `ignore`; called by native AST grep/edit bindings.
- edge_cases_or_failure_modes: Invalid pattern/glob, unsupported extension, overlapping edits, UTF-8 column math, Rust expression patterns needing context.
- validation_or_tests: Contains unit test for Rust contextual pattern; higher-level AST tool tests cover runtime.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-368 `file` `crates/pi-natives/src/pty.rs`
- cursor: `[_]`
- core_role: Native PTY session runner with streaming output, stdin, timeout, and kill support.
- algorithmic_behavior: Starts a PTY command with cwd/env/shell options, registers a control channel before async spawn, streams UTF-8 chunks from reader thread, handles stdin/kill messages, polls process exit, drains output after cancel/exit, and tears down platform-specific PTY resources.
- inputs_outputs_state: Inputs are `PtyStartOptions`, command, shell, env, timeout, abort signal, write/kill controls; outputs are streamed chunks and `PtyRunResult`; state is `PtySessionCore` guarded by mutex plus reader/control channels.
- gates_or_invariants: One active session per `PtySession`; Windows openpty has startup timeout; cancellation/kill terminates process group and child; invalid UTF-8 emits lossy replacement after buffering.
- dependencies_and_callers: Uses `portable_pty`, NAPI threadsafe functions, task cancel token, process-group signaling helpers.
- edge_cases_or_failure_modes: ConPTY hangs/deadlocks, reader EOF races, kill after exit, timeout before setup/spawn/reader, process group unavailable, partial UTF-8 boundaries.
- validation_or_tests: Covered by native PTY/bash integration tests; no direct assigned test here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-398 `file` `packages/agent/test/agent.test.ts`
- cursor: `[_]`
- core_role: Core agent runtime tests for tool calling, state transitions, message flow, and mutation safety.
- algorithmic_behavior: Exercises agent turns, tool-call validation/execution, streaming, stop reasons, retry/error paths, and F3 in-place state mutation behavior.
- inputs_outputs_state: Inputs are fake models/tools/messages; outputs are agent state/messages/tool results/events; state is agent session state under test.
- gates_or_invariants: Tool results pair with calls; state mutation does not corrupt transcript; stop/tool-use transitions are preserved; errors surface predictably.
- dependencies_and_callers: Tests `packages/agent` runtime consumed by coding-agent and other packages.
- edge_cases_or_failure_modes: Tool exceptions, malformed tool calls, repeated turns, in-place updates, streaming deltas.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-428 `file` `packages/ai/src/usage.ts`
- cursor: `[_]`
- core_role: Provider-neutral usage/quota reporting contract.
- algorithmic_behavior: Defines usage windows, amounts, scopes, limits, reset credits, reports, history/cost entries, providers, credential ranking strategy, and Arktype schemas for wire validation; `resolveUsedFraction` derives utilization by precedence.
- inputs_outputs_state: Inputs are provider usage objects and limit amounts; outputs are normalized usage reports and fractions; state is type/schema definitions only.
- gates_or_invariants: Used fraction precedence is explicit fraction, used/limit, percent-unit used, inverted remaining; schemas constrain units/status/shape for broker endpoint.
- dependencies_and_callers: Used by auth broker, usage CLI, provider usage fetchers such as OpenAI Codex, and credential ranking.
- edge_cases_or_failure_modes: Missing/zero limit returns undefined; unknown raw provider payload accepted as `raw`; history may lack resolvable fraction/reset.
- validation_or_tests: Usage CLI tests and provider usage tests exercise consumer behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-458 `file` `packages/ai/test/auth-broker-snapshot-cache.test.ts`
- cursor: `[_]`
- core_role: Tests auth-broker snapshot cache behavior.
- algorithmic_behavior: Creates synthetic snapshot responses and temp cache paths, verifies cache use, generated time handling, and broker URL/token behavior.
- inputs_outputs_state: Inputs are fake fetch/cache JSON and broker env/config; outputs are snapshot objects and fetch/cache side effects; state is temp cache file.
- gates_or_invariants: Valid cache should satisfy lookup without unnecessary network; invalid/stale/missing cache should fetch or fail according to contract.
- dependencies_and_callers: Tests auth broker snapshot cache code.
- edge_cases_or_failure_modes: ENOENT cache, malformed JSON, timestamp age, network fetch errors.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-488 `file` `packages/ai/test/aws-eventstream.test.ts`
- cursor: `[_]`
- core_role: Tests AWS eventstream frame parsing.
- algorithmic_behavior: Encodes string headers/frames, streams chunks, collects parser output, and verifies frame/header/payload handling.
- inputs_outputs_state: Inputs are synthetic Uint8Array chunks; outputs are parsed eventstream messages; state is stream reader progress.
- gates_or_invariants: Chunk boundaries must not affect parse; header strings and payload bytes must round trip; invalid frames should surface errors.
- dependencies_and_callers: Tests provider AWS eventstream decoding used by Bedrock-style integrations.
- edge_cases_or_failure_modes: Split frames, bad lengths/checksums/header encodings, empty stream.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-518 `file` `packages/ai/test/google-gemini-cli-variant-routing.test.ts`
- cursor: `[_]`
- core_role: Tests Gemini CLI variant routing.
- algorithmic_behavior: Builds model/context variants and verifies provider routing selects the correct Gemini CLI API variant and request path.
- inputs_outputs_state: Inputs are model metadata, base URL/context, fake fetch; outputs are request captures and generated responses; state is mocked fetch calls.
- gates_or_invariants: Variant-specific routing must not fall through to the wrong provider dialect; auth and model IDs must be preserved.
- dependencies_and_callers: Tests Google/Gemini provider registry and routing logic.
- edge_cases_or_failure_modes: Unsupported variant, missing base URL, wrong endpoint path.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-548 `file` `packages/ai/test/issue-912-repro.test.ts`
- cursor: `[_]`
- core_role: Regression test for GitHub Copilot abort propagation through OpenAI Responses-compatible provider.
- algorithmic_behavior: Creates Copilot responses model/context and verifies an abort signal reaches fetch/provider execution rather than being lost.
- inputs_outputs_state: Inputs are fake model, context, abort controller, fetch; outputs are aborted provider call/error; state is signal lifecycle.
- gates_or_invariants: Abort must propagate to underlying fetch; provider should not hang after cancellation.
- dependencies_and_callers: Tests GitHub Copilot registry/provider path.
- edge_cases_or_failure_modes: Abort before request, abort during streaming, fetch ignoring signal.
- validation_or_tests: File is direct issue regression.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-578 `file` `packages/ai/test/openai-codex-stream.test.ts`
- cursor: `[_]`
- core_role: Large regression matrix for OpenAI Codex SSE/WebSocket streaming.
- algorithmic_behavior: Mocks tokens, SSE streams, WebSocket lifecycle, retry budgets, idle/first-event/ping-pong timeouts, stateful/stateless response IDs, usage events, tool calls, and abort behavior.
- inputs_outputs_state: Inputs are fake Codex model/context, env flags, mocked fetch/WebSocket events; outputs are streamed assistant messages/tool calls/usage/errors; state includes env restoration, mocked WebSocket instances, response IDs.
- gates_or_invariants: Streaming must emit ordered deltas, handle usage, recover/retry only within configured budgets, close sockets safely, and preserve statelessness where required.
- dependencies_and_callers: Tests OpenAI Codex provider implementation and usage/stream abstractions.
- edge_cases_or_failure_modes: No-progress streams, socket errors/closes, retry exhaustion, pong timeout, idle reuse, malformed events, abort propagation, stateless SSE.
- validation_or_tests: File is direct comprehensive test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-608 `file` `packages/ai/test/owned-stream-fabrication.test.ts`
- cursor: `[_]`
- core_role: Tests owned-stream fabrication behavior.
- algorithmic_behavior: Verifies fabricated streams from non-streaming or owned output maintain expected message/ownership shape.
- inputs_outputs_state: Inputs are synthetic provider outputs; outputs are stream events; state is in-memory stream collection.
- gates_or_invariants: Fabricated stream must not lose ownership metadata or alter final content semantics.
- dependencies_and_callers: Tests AI streaming utility/provider adapters.
- edge_cases_or_failure_modes: Empty output, multiple chunks, finalization ordering.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-638 `file` `packages/ai/test/tool-argument-coercion.test.ts`
- cursor: `[_]`
- core_role: Broad contract tests for tool-call argument coercion and validation.
- algorithmic_behavior: Validates booleans/numbers/arrays/objects/unions/defaults/nulls, JSON-stringified and double-encoded inputs, glob strings, malformed JSON repair boundaries, strict Zod extra-key tolerance, JSON Schema draft upgrade, and union re-coercion.
- inputs_outputs_state: Inputs are synthetic tool definitions and tool calls; outputs are coerced args or validation errors; state is none beyond schema objects.
- gates_or_invariants: Coercion occurs only when schema expects it; glob-looking brackets are preserved when not JSON; invalid normalized values do not leak in errors; defaults are not shared mutably.
- dependencies_and_callers: Tests `validateToolArguments` used by all provider tool-call execution.
- edge_cases_or_failure_modes: Nested JSON strings, raw newlines, null required fields, numeric strings, singleton-to-array, object arrays, strict extras, union alternatives.
- validation_or_tests: File is direct exhaustive test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-668 `file` `packages/catalog/src/utils.ts`
- cursor: `[_]`
- core_role: Small catalog utility module.
- algorithmic_behavior: Provides model ID segmentation/affix helpers and bracket-stripping candidates used by catalog identity/model matching.
- inputs_outputs_state: Inputs are model-like strings; outputs are segment arrays, longest segment, candidate IDs; state is none.
- gates_or_invariants: Should preserve meaningful model segments while stripping display affixes/brackets only where safe.
- dependencies_and_callers: Used by catalog tests and provider/model identity code.
- edge_cases_or_failure_modes: Nested brackets, punctuation separators, IDs with slashes/colons, empty strings.
- validation_or_tests: `packages/catalog/test/model-id-affixes.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-698 `file` `packages/catalog/test/model-id-affixes.test.ts`
- cursor: `[_]`
- core_role: Tests model ID affix parsing utilities.
- algorithmic_behavior: Exercises segment extraction, longest model-like segment selection, and bracket-stripped candidate generation.
- inputs_outputs_state: Inputs are model display names/IDs; outputs are expected candidate arrays/strings; state is none.
- gates_or_invariants: Bracketed suffix/prefix handling must not destroy actual IDs; longest segment selection must be deterministic.
- dependencies_and_callers: Tests `packages/catalog/src/utils.ts`.
- edge_cases_or_failure_modes: Bracket-only names, multi-segment names, ambiguous affixes.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-728 `file` `packages/coding-agent/src/cursor.ts`
- cursor: `[_]`
- core_role: Bridge between Cursor exec/MCP handlers and coding-agent tools.
- algorithmic_behavior: Maps Cursor read/ls/grep/write/delete/shell/shellStream/diagnostics/MCP calls into internal tools, creates tool result messages, emits tool execution events, sanitizes update/final text, streams append-only sanitized shell deltas, and decodes MCP raw args.
- inputs_outputs_state: Inputs are Cursor handler args, tool map, cwd, optional context/event emitter; outputs are `ToolResultMessage`s and events; state is per-call raw/sanitized shell stream buffers.
- gates_or_invariants: Unknown tools return error result; delete only removes files; missing toolCallId becomes UUID; shell stream stops delta callbacks once sanitized output is no longer prefix-extending.
- dependencies_and_callers: Implements `CursorExecHandlers` from `@oh-my-pi/pi-ai`; depends on tool/session infrastructure and path utilities.
- edge_cases_or_failure_modes: Non-file delete, JSON decode fallback to string, unavailable MCP tool, sanitization altering stream prefix, tool exceptions.
- validation_or_tests: Covered by Cursor/ACP/tool integration tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-758 `file` `packages/coding-agent/test/agent-session-compaction.test.ts`
- cursor: `[_]`
- core_role: Tests session compaction behavior.
- algorithmic_behavior: Builds session histories and verifies compaction preserves required messages/context while pruning/summarizing according to contract.
- inputs_outputs_state: Inputs are fake session entries/messages; outputs are compacted session state; state is temp/in-memory session manager.
- gates_or_invariants: Compaction must not drop authentication fallback/context needed for continuation; message ordering and tool result pairing remain valid.
- dependencies_and_callers: Tests coding-agent session compaction logic.
- edge_cases_or_failure_modes: Long histories, tool-call/result boundaries, missing auth context.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-788 `file` `packages/coding-agent/test/agent-session-tree-navigation.test.ts`
- cursor: `[_]`
- core_role: Tests session tree navigation/fork traversal.
- algorithmic_behavior: Creates branching session histories and verifies navigation to tree nodes/forks and active session state transitions.
- inputs_outputs_state: Inputs are branch/fork entries and target IDs; outputs are navigation results and current session state; state is session tree.
- gates_or_invariants: Navigation targets must exist; branch/fork lineage is preserved; cancelled/invalid navigation does not corrupt current state.
- dependencies_and_callers: Tests session manager/tree navigation APIs.
- edge_cases_or_failure_modes: Missing target ID, repeated forks, parent/child ordering.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-818 `file` `packages/coding-agent/test/cli-cwd-flag.test.ts`
- cursor: `[_]`
- core_role: Tests CLI `--cwd` parsing and project directory mutation.
- algorithmic_behavior: Parses args with cwd flag and verifies project dir changes/restores as expected.
- inputs_outputs_state: Inputs are CLI argv arrays; outputs are parsed options/project dir state; state is global project dir restored after tests.
- gates_or_invariants: `--cwd` should affect runtime cwd/project root without leaking across tests.
- dependencies_and_callers: Tests CLI args/config helpers.
- edge_cases_or_failure_modes: Missing value, relative paths, restoration after parse.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-848 `file` `packages/coding-agent/test/editor-max-height.test.ts`
- cursor: `[_]`
- core_role: Tests editor maximum height calculation.
- algorithmic_behavior: Verifies terminal/editor sizing helper returns bounded heights for viewport constraints.
- inputs_outputs_state: Inputs are terminal/layout dimensions; outputs are computed max height; state is none.
- gates_or_invariants: Editor height must not exceed available space or shrink below usable minimum.
- dependencies_and_callers: Tests TUI/editor sizing helper.
- edge_cases_or_failure_modes: Very small terminal heights and large content.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-878 `file` `packages/coding-agent/test/hook-input-timeout.test.ts`
- cursor: `[_]`
- core_role: Tests hook input timeout behavior.
- algorithmic_behavior: Simulates hook input waits and verifies timeout/cancellation paths resolve without hanging.
- inputs_outputs_state: Inputs are fake hook prompts/timeouts; outputs are timeout results/errors; state is timer-controlled test state.
- gates_or_invariants: Hook input must respect timeout and not leak pending resolvers.
- dependencies_and_callers: Tests hook/input prompt infrastructure.
- edge_cases_or_failure_modes: No user response, abort while waiting, repeated prompts.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-908 `file` `packages/coding-agent/test/issue-1011-repro.test.ts`
- cursor: `[_]`
- core_role: Regression test for tab worker CLI re-entry.
- algorithmic_behavior: Verifies worker spawn contract uses CLI entrypoint/worker-host dispatch instead of separate broken binary worker entries.
- inputs_outputs_state: Inputs are worker host entry metadata; outputs are assertions about tab worker wiring; state is env/runtime introspection.
- gates_or_invariants: Compiled/source workers must re-enter CLI dispatch table; fallback direct-module branch remains for tests/embedding.
- dependencies_and_callers: Tests issue #1011 worker-host contract in coding-agent.
- edge_cases_or_failure_modes: Compiled binaries silently failing workers, missing selector in `cli.ts`.
- validation_or_tests: File is direct issue regression.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-938 `file` `packages/coding-agent/test/issue-986-compaction-auth-fallback.test.ts`
- cursor: `[_]`
- core_role: Regression tests for compaction with authentication fallback context.
- algorithmic_behavior: Builds sessions requiring auth fallback and verifies compaction preserves enough provider/auth information to continue.
- inputs_outputs_state: Inputs are synthetic auth/session histories; outputs are compacted messages/context; state is temp session data.
- gates_or_invariants: Auth fallback material must survive compaction when needed; compacted transcript remains valid.
- dependencies_and_callers: Tests session compaction/provider auth fallback interaction.
- edge_cases_or_failure_modes: Missing auth entries, compacting too aggressively, restored sessions.
- validation_or_tests: File is direct issue regression.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-968 `file` `packages/coding-agent/test/mcp-roots-list.test.ts`
- cursor: `[_]`
- core_role: Tests MCP roots/list behavior.
- algorithmic_behavior: Verifies root list construction, path normalization, and server-visible workspace roots.
- inputs_outputs_state: Inputs are cwd/root settings/MCP requests; outputs are roots list responses; state is fake MCP/session config.
- gates_or_invariants: Roots must not omit active workspace and should avoid leaking invalid paths.
- dependencies_and_callers: Tests MCP manager/protocol root handling.
- edge_cases_or_failure_modes: Multiple roots, missing cwd, path normalization.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-998 `file` `packages/coding-agent/test/plugin-config.test.ts`
- cursor: `[_]`
- core_role: Tests plugin configuration parsing/loading.
- algorithmic_behavior: Builds plugin config inputs and verifies accepted/ignored values and resulting plugin state.
- inputs_outputs_state: Inputs are config objects/files; outputs are plugin configuration objects; state is temp config.
- gates_or_invariants: Invalid plugin config should not crash runtime or enable unintended plugins.
- dependencies_and_callers: Tests extensibility/plugin config loader.
- edge_cases_or_failure_modes: Missing fields, invalid types, defaults.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1028 `file` `packages/coding-agent/test/rpc.test.ts`
- cursor: `[_]`
- core_role: Tests coding-agent RPC behavior.
- algorithmic_behavior: Exercises RPC request/response routing, method behavior, errors, and session interaction.
- inputs_outputs_state: Inputs are fake RPC messages; outputs are RPC results/errors/events; state is in-memory harness.
- gates_or_invariants: Unknown methods fail predictably; valid methods preserve response shape and session state.
- dependencies_and_callers: Tests RPC server/client layer.
- edge_cases_or_failure_modes: Invalid payloads, async errors, event ordering.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1058 `file` `packages/coding-agent/test/settings-reload-cwd.test.ts`
- cursor: `[_]`
- core_role: Tests settings reload when cwd changes.
- algorithmic_behavior: Creates temp cwd/settings files and verifies `Settings.reloadForCwd` resolves project/user layers correctly.
- inputs_outputs_state: Inputs are cwd paths and settings files/env; outputs are loaded settings; state is temp directories and settings singleton state.
- gates_or_invariants: Reload must honor new cwd and not retain stale project settings.
- dependencies_and_callers: Tests coding-agent settings loader.
- edge_cases_or_failure_modes: Nested dirs, missing settings, env overrides.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1088 `file` `packages/coding-agent/test/strip-images-from-message.test.ts`
- cursor: `[_]`
- core_role: Tests message image stripping utility.
- algorithmic_behavior: Builds text/image content blocks and verifies image blocks are removed while text and message shape remain valid.
- inputs_outputs_state: Inputs are message content arrays; outputs are stripped messages; state is none.
- gates_or_invariants: Text content must be preserved; images must not leak to contexts that disallow them.
- dependencies_and_callers: Tests message preprocessing for providers/tools.
- edge_cases_or_failure_modes: Image-only messages, mixed content, empty arrays.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1118 `file` `packages/coding-agent/test/usage-cli.test.ts`
- cursor: `[_]`
- core_role: Tests usage CLI formatting, redaction, account aggregation, and history rendering.
- algorithmic_behavior: Creates synthetic usage reports/limits, computes provider window stats, collects unreported accounts, formats breakdown/history, and verifies redaction map output.
- inputs_outputs_state: Inputs are usage reports/history limits and accounts; outputs are display strings/stats; state is in-memory.
- gates_or_invariants: Account identifiers are redacted consistently; window stats compute from primary/secondary durations; missing reports are surfaced.
- dependencies_and_callers: Tests coding-agent usage CLI and `packages/ai/src/usage` consumers.
- edge_cases_or_failure_modes: Empty limits, unknown windows, exhausted/warning statuses, duplicate accounts.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1148 `file` `packages/hashline/src/index.ts`
- cursor: `[_]`
- core_role: Public barrel for hashline modules.
- algorithmic_behavior: Re-exports apply/block/diff-preview/format/fs/input/location/map/parse/preview/scanner/store/snapshot/snapshot-store/types.
- inputs_outputs_state: Inputs are module exports; outputs are aggregate package API; state is none.
- gates_or_invariants: Barrel must expose modules without duplicate ambiguity.
- dependencies_and_callers: Consumed by coding-agent edit/hashline tooling.
- edge_cases_or_failure_modes: Missing export breaks package API; duplicate export names can create ambiguity.
- validation_or_tests: Covered by hashline consumers/build.
- skip_candidate: `yes: pure re-export barrel with no local algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1178 `file` `packages/mnemopi/src/types.ts`
- cursor: `[_]`
- core_role: Type contract for memory rows, recall, facts, triples, annotations, embeddings, and vector search.
- algorithmic_behavior: Defines normalized memory interfaces and JSON/vector metadata shapes used by mnemopi storage/search implementations.
- inputs_outputs_state: Inputs/outputs are structural TypeScript types; runtime state is none.
- gates_or_invariants: Memory IDs/timestamps/text/metadata/vector types have stable fields for downstream storage/search.
- dependencies_and_callers: Used by mnemopi core and tests.
- edge_cases_or_failure_modes: Type-only file cannot enforce runtime validation; vector variants depend on implementation.
- validation_or_tests: mnemopi tests use these contracts.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1208 `file` `packages/mnemopi/test/fastembed-runtime.test.ts`
- cursor: `[_]`
- core_role: Tests FastEmbed runtime version/environment pins.
- algorithmic_behavior: Verifies runtime metadata/environment resolves to expected pinned values.
- inputs_outputs_state: Inputs are runtime env/package metadata; outputs are assertions; state is process env snapshot.
- gates_or_invariants: FastEmbed runtime pin should not drift unexpectedly.
- dependencies_and_callers: Tests `src/core/fastembed-runtime.ts`.
- edge_cases_or_failure_modes: Missing binary/package, version mismatch, env override.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1238 `file` `packages/mnemopi/test/temporal-parser.test.ts`
- cursor: `[_]`
- core_role: Tests temporal expression parsing for memory queries.
- algorithmic_behavior: Exercises relative/absolute date parsing, range construction, and invalid/ambiguous expression handling.
- inputs_outputs_state: Inputs are natural-language temporal strings and reference dates; outputs are parsed ranges/metadata; state is deterministic reference time.
- gates_or_invariants: Parser must produce stable ranges around reference date and reject unsupported expressions.
- dependencies_and_callers: Tests mnemopi temporal parser.
- edge_cases_or_failure_modes: Time zones, relative words, incomplete dates, invalid dates.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1268 `file` `packages/snapcompact/research/diag_glm_probe.py`
- cursor: `[_]`
- core_role: Research probe for image/text model routes in snapcompact experiments.
- algorithmic_behavior: Posts OpenRouter/Z.ai chat requests, builds base64 image blocks, selects frames, and runs smoke/bill/frame/AB modes for diagnostic comparisons.
- inputs_outputs_state: Inputs are CLI args, API keys, local PNG frames/prompts; outputs are printed responses/usage snippets; state is none beyond network calls.
- gates_or_invariants: Route must be valid; HTTP errors are captured as JSON; image blocks embed PNG data URLs.
- dependencies_and_callers: Uses stdlib `urllib`, local prompt/frame assets; research-only script.
- edge_cases_or_failure_modes: Missing keys/files, API balance errors, long network timeout, list-vs-string response content.
- validation_or_tests: No automated test; manual research probe.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1298 `file` `packages/snapcompact/research/parity_check.py`
- cursor: `[_]`
- core_role: Pixel-class parity checker between production Rust renderer and research PIL renderer.
- algorithmic_behavior: Renders each shape variant with research renderer, invokes Bun production `parity_render.ts`, classifies pixels into background/band/dim/ink, compares cell/pixel classes, and reports failures.
- inputs_outputs_state: Inputs are normalized text, font/shape configs, production renderer output PNG; outputs are PASS/FAIL and optional kept artifacts; state is temp files/cache.
- gates_or_invariants: Dimensions and pixel classes must match; black/colored ink exactness is preserved by classification.
- dependencies_and_callers: Depends on PIL, local `bdf`, Bun renderer script, shape definitions.
- edge_cases_or_failure_modes: Production render errors, printed region shorter than full square, first differing pixel diagnostics.
- validation_or_tests: Script is itself validation for renderer parity.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1328 `file` `packages/snapcompact/research/snapcompact_token_entry_dump.py`
- cursor: `[_]`
- core_role: Research diagnostic for token/embedding entries in snapcompact vision/text pipeline.
- algorithmic_behavior: Loads tokenizer/processor/model inputs, maps token offsets to answer spans, dumps vector heads for text/image answer tokens and pixel/value metadata as JSON.
- inputs_outputs_state: Inputs are model paths, snippets/images, answer marker args; outputs are JSON diagnostics; state includes loaded tokenizer/processor tensors.
- gates_or_invariants: Answer token indices are derived from offset mapping; embedding slices are rounded/capped by CLI dimensions.
- dependencies_and_callers: Uses PyTorch/transformers/PIL and local research assets.
- edge_cases_or_failure_modes: Missing model/image, no answer tokens, device mismatch, offset mapping quirks.
- validation_or_tests: Manual research diagnostic; no automated test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1358 `file` `packages/stats/test/db-range.test.ts`
- cursor: `[_]`
- core_role: Tests stats database range bucketing/query behavior.
- algorithmic_behavior: Inserts synthetic rows and verifies time-range bucket aggregation/window behavior.
- inputs_outputs_state: Inputs are temp DB rows/timestamps; outputs are query results; state is temporary SQLite DB.
- gates_or_invariants: Range boundaries and bucket sizes must match expected metadata; empty windows handled consistently.
- dependencies_and_callers: Tests stats DB/query layer.
- edge_cases_or_failure_modes: Off-by-one timestamp boundaries, empty buckets, timezone-independent formatting.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1388 `file` `packages/tui/src/utils.ts`
- cursor: `[_]`
- core_role: Core TUI text measurement, wrapping, tab replacement, word navigation, slicing, and rendering utilities.
- algorithmic_behavior: Encodes OSC66 text sizing, delegates truncate/slice/wrap to native helpers, computes visible widths with Bun/native-compatible width rules, expands tabs by project indentation, normalizes terminal output, classifies graphemes for word navigation, moves cursor by word, applies backgrounds, and slices by visible columns.
- inputs_outputs_state: Inputs are terminal strings, ANSI/OSC content, file paths, cursor positions, widths; outputs are strings/segments/cursor indices; state includes global tight-mode flag and segmenter.
- gates_or_invariants: ANSI/OSC must count zero except OSC66 sizing metadata; tabs add configured width; cursor movement stays within `[0,text.length]`; truncate defaults mirror Rust helper defaults.
- dependencies_and_callers: Used throughout TUI components and coding-agent renderers; depends on `@oh-my-pi/pi-natives` and `pi-utils`.
- edge_cases_or_failure_modes: Fullwidth graphemes, Thai/Lao AM normalization, CJK word nav, joiners, tabs, strict wide-char boundaries.
- validation_or_tests: TUI tests for settings/kitty plus utility consumers; no single utility test assigned except related files.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1418 `file` `packages/tui/test/kitty-graphics.test.ts`
- cursor: `[_]`
- core_role: Tests Kitty graphics feature detection and placeholder encoding.
- algorithmic_behavior: Verifies Unicode placeholder sequences, feature state toggles, and detection behavior under mocked terminal capabilities.
- inputs_outputs_state: Inputs are mocked Kitty config/env/terminal responses; outputs are encoded strings/state flags; state is restored original kitty graphics state.
- gates_or_invariants: Encoding must be byte-stable; unsupported terminals disable placeholders; detection should not leak state across tests.
- dependencies_and_callers: Tests TUI terminal graphics module.
- edge_cases_or_failure_modes: Missing capability, unsafe terminal state, env restoration.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1448 `file` `packages/tui/test/settings-list.test.ts`
- cursor: `[_]`
- core_role: Tests settings list TUI component rendering and interaction.
- algorithmic_behavior: Builds a test theme and settings rows, verifies rendering, navigation, selection/edit states, and layout behavior.
- inputs_outputs_state: Inputs are settings options/theme/key events; outputs are rendered lines and component state; state is component instance.
- gates_or_invariants: Rows should align/truncate correctly; navigation should stay bounded; edit state must reflect selected setting.
- dependencies_and_callers: Tests TUI `SettingsList`.
- edge_cases_or_failure_modes: Long labels/descriptions, small widths, empty lists, option boundaries.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1478 `file` `packages/typescript-edit-benchmark/src/verify.ts`
- cursor: `[_]`
- core_role: Edit benchmark expected-file verifier.
- algorithmic_behavior: Compares expected and actual directories, optionally as subset, normalizes line endings/blank lines, restores whitespace-only line diffs, formats both sides, computes compact diff and diff stats, and measures indentation distance.
- inputs_outputs_state: Inputs are expected/actual directories and optional file subset; outputs are `VerificationResult` with pass/error/diff/indent stats; state is local lists/content.
- gates_or_invariants: Missing expected fixture files fail; unexpected actual files fail only for full comparison; formatted mismatch fails; whitespace-only differences can be restored/ignored semantically.
- dependencies_and_callers: Used by TypeScript edit benchmark runner; depends on formatter and `diff`.
- edge_cases_or_failure_modes: CRLF, multiple blank lines, whitespace-only line pairs, formatter errors, files missing from either side.
- validation_or_tests: Covered by `packages/typescript-edit-benchmark/test/verify.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1508 `file` `packages/utils/src/snowflake.ts`
- cursor: `[_]`
- core_role: Snowflake-style unique ID generation/parsing utility.
- algorithmic_behavior: Generates sortable numeric/string IDs from timestamp/node/sequence fields and provides parse/format helpers.
- inputs_outputs_state: Inputs are current time/options; outputs are unique IDs and decoded components; state includes sequence/last timestamp.
- gates_or_invariants: Sequence increments within same millisecond; clock/field bounds must be respected.
- dependencies_and_callers: Used wherever compact sortable IDs are required; tested in utils.
- edge_cases_or_failure_modes: Clock rollback, sequence overflow, invalid IDs, node ID bounds.
- validation_or_tests: `packages/utils/test/snowflake.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1538 `file` `packages/utils/test/worker-host.test.ts`
- cursor: `[_]`
- core_role: Tests worker-host inbox/entrypoint helpers.
- algorithmic_behavior: Verifies declaring worker host entry and worker inbox lookup behavior for CLI re-entry workers.
- inputs_outputs_state: Inputs are env/runtime host state; outputs are entrypoint/inbox values; state is module-level worker-host state restored by tests.
- gates_or_invariants: Host entry should be available only when declared; worker selectors/inbox should not collide.
- dependencies_and_callers: Tests `packages/utils/src/worker-host.ts`; supports coding-agent worker contract.
- edge_cases_or_failure_modes: Multiple declarations, missing host, test runtime fallback.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1568 `file` `python/robomp/src/sandbox.py`
- cursor: `[_]`
- core_role: Python sandbox/workspace manager for repo issue automation.
- algorithmic_behavior: Builds workspace keys/branches, validates branch slugs, renames branches, abstracts git transport, clones/fetches/checks out workspaces, manages slot UID permissions, reaps slot processes via `/proc`, prepares temp/runtime dirs, shares git metadata, and cleans/pushes safely.
- inputs_outputs_state: Inputs are repo names, issue/PR numbers, titles, branch slug, git token, pool/root paths, slot UID; outputs are `Workspace` objects, git refs, filesystem workspaces, pushes; state is workspace directories and git metadata.
- gates_or_invariants: Branch slugs must match kebab regex and length; push refuses drift via expected head; slot permission path only on Linux root; credentials redacted from captured output.
- dependencies_and_callers: Used by `robomp` automation; depends on stdlib subprocess/path/os/stat and `GitCommandError`.
- edge_cases_or_failure_modes: Git command failures, missing PR refs, stale workspaces, slot UID process cleanup, chown/chmod failures, bare/worktree git dirs, stash/push conflicts.
- validation_or_tests: Python package tests not assigned here; behavior has strong internal validation/error raising.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1598 `directory` `packages/ai/src/providers/__tests__`
- cursor: `[_]`
- core_role: Provider-specific AI tests colocated with provider implementations.
- algorithmic_behavior: `google-auth.test.ts` validates service-account/impersonated ADC token exchange and IAM calls; `openai-codex-error.test.ts` validates Codex provider error mapping/handling.
- inputs_outputs_state: Inputs are generated PEMs, mocked env/fetch calls, provider contexts; outputs are tokens, requests, thrown errors; state is env restored after tests.
- gates_or_invariants: Google auth must use JWT bearer for source credential and IAM impersonation with source token; provider errors must classify into expected surfaced errors.
- dependencies_and_callers: Tests provider auth/error modules inside `packages/ai/src/providers`.
- edge_cases_or_failure_modes: Invalid credential file, malformed PEM, HTTP failures, unexpected provider payloads.
- validation_or_tests: Directory is direct provider test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1628 `directory` `packages/coding-agent/src/lsp/clients`
- cursor: `[_]`
- core_role: LSP/linter client adapters for diagnostics.
- algorithmic_behavior: `index.ts` caches clients by server/config/cwd and chooses Biome/SwiftLint/generic LSP; `biome-client.ts` runs/parses Biome diagnostics with offset-to-position conversion and warn-once failures; `swiftlint-client.ts` parses SwiftLint diagnostics; `lsp-linter-client.ts` bridges generic language-server diagnostics to `LinterClient`.
- inputs_outputs_state: Inputs are server config, cwd, source files, linter JSON output; outputs are normalized diagnostics; state is client cache and reported Biome failure set.
- gates_or_invariants: Unknown server falls back to LSP linter; severity strings map to diagnostic severities; failures warn once to avoid log spam.
- dependencies_and_callers: Used by coding-agent LSP tool and diagnostics ledger.
- edge_cases_or_failure_modes: Invalid JSON, missing offsets, unknown severity, unavailable executable, stale cache.
- validation_or_tests: LSP/diagnostics tests cover consumers; no direct assigned client test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1658 `directory` `packages/stats/src/client/components`
- cursor: `[_]`
- core_role: Shared stats dashboard React components and range metadata.
- algorithmic_behavior: Provides chart theme/colors, model table shell/header/body/name/expandable rows, mini sparklines, chart plugins/scales, empty states, and range metadata/tick formatting.
- inputs_outputs_state: Inputs are chart series/model/provider/range values; outputs are React nodes and formatted ticks; state is component props only.
- gates_or_invariants: Range metadata defines bucket size/count/tick format; table grid columns align; empty states render stable placeholders.
- dependencies_and_callers: Used by stats client pages; depends on React/chart.js/date-fns.
- edge_cases_or_failure_modes: Empty data, long model names, dual-axis scaling, unsupported range key.
- validation_or_tests: `packages/stats/test/db-range.test.ts` covers matching server ranges; UI component tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1688 `file` `packages/ai/src/auth-broker/index.ts`
- cursor: `[_]`
- core_role: Auth-broker barrel export.
- algorithmic_behavior: Re-exports auth broker submodules for package API.
- inputs_outputs_state: Inputs are submodule exports; output is public namespace; state is none.
- gates_or_invariants: Export surface must remain stable.
- dependencies_and_callers: Used by AI/coding-agent auth broker consumers.
- edge_cases_or_failure_modes: Missing export breaks imports.
- validation_or_tests: Auth broker tests cover consumers.
- skip_candidate: `yes: pure index barrel with no local algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1718 `file` `packages/ai/src/dialect/rendering.ts`
- cursor: `[_]`
- core_role: Tool/message rendering helpers for provider dialects.
- algorithmic_behavior: Normalizes/render tool schemas/messages into provider-compatible shapes, including schema transformations and text/tool-call formatting.
- inputs_outputs_state: Inputs are internal messages/tools/schema fragments; outputs are dialect-specific rendered payloads; state is local transform traversal.
- gates_or_invariants: Provider payloads must preserve call/result pairing and avoid invalid schema constructs.
- dependencies_and_callers: Used by AI provider adapters.
- edge_cases_or_failure_modes: Unsupported content blocks, malformed schema, nested tool calls/results.
- validation_or_tests: Tool argument coercion and provider stream tests cover dialect consumers.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1748 `file` `packages/ai/src/providers/openai-chat-server-schema.ts`
- cursor: `[_]`
- core_role: Server-side schema conversion for OpenAI Chat-compatible providers.
- algorithmic_behavior: Converts/normalizes tool and response schemas to OpenAI Chat server-accepted JSON Schema subset, handling strictness and unsupported keywords.
- inputs_outputs_state: Inputs are JSON Schema/tool definitions; outputs are sanitized schema objects; state is recursive traversal.
- gates_or_invariants: OpenAI server schema must not contain unsupported or unresolved constructs; required/property shapes stay coherent.
- dependencies_and_callers: Used by OpenAI Chat provider rendering.
- edge_cases_or_failure_modes: Circular refs, `$defs`, nullable/union fields, empty properties, unsupported draft keywords.
- validation_or_tests: Schema validation and tool coercion tests exercise related behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1778 `file` `packages/ai/src/registry/github-copilot.ts`
- cursor: `[_]`
- core_role: Provider descriptor for GitHub Copilot.
- algorithmic_behavior: Exports provider metadata/config for Copilot-compatible models.
- inputs_outputs_state: Inputs are registry lookup; outputs are provider descriptor; state is static.
- gates_or_invariants: Provider ID/defaults must match downstream routing/auth expectations.
- dependencies_and_callers: Used by AI registry and issue #912/Copilot tests.
- edge_cases_or_failure_modes: Wrong provider API variant or endpoint breaks routing.
- validation_or_tests: `issue-912-repro.test.ts` and provider routing tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1808 `file` `packages/ai/src/registry/perplexity.ts`
- cursor: `[_]`
- core_role: Provider descriptor for Perplexity.
- algorithmic_behavior: Exports static provider metadata/config for Perplexity-compatible requests.
- inputs_outputs_state: Inputs are registry lookup; outputs are provider descriptor; state is static.
- gates_or_invariants: Provider ID/API endpoint/defaults must align with catalog and auth.
- dependencies_and_callers: Used by AI registry/model catalog.
- edge_cases_or_failure_modes: Endpoint/default mismatch.
- validation_or_tests: Covered by registry/catalog tests indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1838 `file` `packages/ai/src/usage/openai-codex.ts`
- cursor: `[_]`
- core_role: OpenAI Codex usage/quota fetcher and ranking strategy.
- algorithmic_behavior: Normalizes Codex base URLs, parses JWT account/email, parses `/wham/usage` rate-limit windows/additional limits/reset credits, builds normalized `UsageReport`, fetches with bearer token, and ranks/scopes credentials by primary/secondary windows/model family.
- inputs_outputs_state: Inputs are OAuth credential/access token, base URL, fetch context, usage payload; outputs are `UsageReport`, `UsageLimit`s, ranking decisions; state is none.
- gates_or_invariants: ChatGPT URLs gain `/backend-api`; malformed JWT/payload returns fallback/nulls; reset credits truncated to non-negative integer; failed fetch logs/returns null per provider contract.
- dependencies_and_callers: Implements `UsageProvider` and `CredentialRankingStrategy`; used by usage CLI/auth broker.
- edge_cases_or_failure_modes: Missing access token, non-record payload, absent windows, additional limit shape changes, expired token, enterprise URL.
- validation_or_tests: Covered by OpenAI Codex stream/usage-related tests and usage CLI tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1868 `file` `packages/catalog/src/compat/apply.ts`
- cursor: `[_]`
- core_role: Compatibility application helper for catalog model specs.
- algorithmic_behavior: Applies compatibility transforms/policies to model/catalog entries.
- inputs_outputs_state: Inputs are model specs/compat rules; outputs are adjusted specs; state is none or in-place mutation depending caller.
- gates_or_invariants: Compat transforms must be deterministic and preserve required model fields.
- dependencies_and_callers: Used by catalog generation/runtime compatibility layer.
- edge_cases_or_failure_modes: Missing fields, duplicate transforms, provider mismatch.
- validation_or_tests: Catalog resolver/compat tests cover indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1898 `file` `packages/coding-agent/src/advisor/advise-tool.ts`
- cursor: `[_]`
- core_role: Advisor agent tool and routing helpers.
- algorithmic_behavior: Defines advise schema, formats XML advisory batches, decides interruption channel based on severity/streaming/abort suppression/immune turns, derives telemetry for advisor identity, exposes read-only tool names, and records advice via `AdviseTool`.
- inputs_outputs_state: Inputs are advice note/severity and runtime state; outputs are advisory XML/tool result/delivery channel/telemetry config; state is callback side effect.
- gates_or_invariants: `concern`/`blocker` interrupt unless suppressed/immune; nits queue as aside; XML text is escaped; tool result is `useless`.
- dependencies_and_callers: Used by advisor loop, yield queue, steering channel, telemetry pipeline.
- edge_cases_or_failure_modes: Auto-resume suppression while idle/aborting, active streaming after user resume, invalid severity blocked by schema.
- validation_or_tests: Advisor tests not assigned; behavior has exported pure helpers suitable for tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1928 `file` `packages/coding-agent/src/capability/ssh.ts`
- cursor: `[_]`
- core_role: SSH capability detection/config helper.
- algorithmic_behavior: Resolves whether SSH-related tools/capabilities should be available from settings/environment/runtime.
- inputs_outputs_state: Inputs are config/capability environment; outputs are boolean/capability state; state is none.
- gates_or_invariants: SSH tool should only activate when prerequisites are present and allowed.
- dependencies_and_callers: Used by tool loading/session refresh for SSH.
- edge_cases_or_failure_modes: Missing binary/config, disabled setting, stale capability state.
- validation_or_tests: Covered indirectly by SSH/tool registry tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1958 `file` `packages/coding-agent/src/cli/shell-cli.ts`
- cursor: `[_]`
- core_role: Shell-mode CLI entry logic.
- algorithmic_behavior: Parses shell CLI invocation, creates session/runtime, routes command input through coding-agent shell experience, and handles process exit.
- inputs_outputs_state: Inputs are argv/stdin/env/cwd; outputs are CLI stdout/stderr/session changes; state is session instance.
- gates_or_invariants: Must respect cwd/settings and not corrupt TUI/log output.
- dependencies_and_callers: Used by main CLI command registry.
- edge_cases_or_failure_modes: Missing command, non-interactive stdin, session startup failure.
- validation_or_tests: CLI cwd and shell tests cover indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1988 `file` `packages/coding-agent/src/commands/join.ts`
- cursor: `[_]`
- core_role: CLI command to join/attach to an existing session.
- algorithmic_behavior: Resolves target session and hands control to session UI/loader.
- inputs_outputs_state: Inputs are command args/session id/path; outputs are joined session or error; state is active session selection.
- gates_or_invariants: Target session must exist/resolve.
- dependencies_and_callers: CLI command registry, session loader.
- edge_cases_or_failure_modes: Missing session, ambiguous target, stale session file.
- validation_or_tests: Session loader/RPC tests cover related paths.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2018 `file` `packages/coding-agent/src/config/keybindings.ts`
- cursor: `[_]`
- core_role: Keybinding parsing, defaults, and command mapping.
- algorithmic_behavior: Defines default keybindings, parses user key specs, normalizes chords, detects conflicts/invalid keys, and resolves runtime actions.
- inputs_outputs_state: Inputs are settings keybinding maps and key events; outputs are action mappings/errors; state is config object.
- gates_or_invariants: Invalid or duplicate bindings should be rejected or resolved deterministically; defaults remain available unless overridden.
- dependencies_and_callers: Used by TUI input handling/settings.
- edge_cases_or_failure_modes: Modifier ordering, aliases, empty bindings, platform-specific keys.
- validation_or_tests: Keybinding/settings tests cover indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2048 `file` `packages/coding-agent/src/discovery/builtin-defaults.ts`
- cursor: `[_]`
- core_role: Built-in discovery defaults for coding-agent features/tools.
- algorithmic_behavior: Supplies static defaults used by discovery mode/tool loading.
- inputs_outputs_state: Inputs are settings/discovery mode; outputs are default lists/config; state is static.
- gates_or_invariants: Defaults should align with actual available built-ins.
- dependencies_and_callers: Tool discovery and registry.
- edge_cases_or_failure_modes: Stale default name, mismatch with tool registry.
- validation_or_tests: Tool discovery tests cover related behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2078 `file` `packages/coding-agent/src/eval/bridge-timeout.ts`
- cursor: `[_]`
- core_role: Timeout bridge utilities for eval host operations.
- algorithmic_behavior: Pauses/resumes eval idle timeout around bridge operations and emits status events so host-side `agent()`/tool calls do not consume runtime-work budget.
- inputs_outputs_state: Inputs are timeout controller/status callback/operation; outputs are operation result and pause/resume events; state is timer pause state.
- gates_or_invariants: Resume must occur after operation even on failure; cell cancellation must still propagate.
- dependencies_and_callers: Used by eval JS/Python bridges documented in `docs/tools/eval.md`.
- edge_cases_or_failure_modes: Nested pauses, thrown bridge errors, abort during pause.
- validation_or_tests: Eval bridge timeout tests cover behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2108 `file` `packages/coding-agent/src/hindsight/bank.ts`
- cursor: `[_]`
- core_role: Hindsight memory/bank storage and retrieval logic.
- algorithmic_behavior: Stores, scores, and retrieves hindsight entries for session learning/context reuse.
- inputs_outputs_state: Inputs are hindsight notes/session data/query; outputs are selected bank entries; state is persisted/in-memory bank data.
- gates_or_invariants: Entries must be normalized and scoped to relevant sessions/projects.
- dependencies_and_callers: Used by hindsight session state/tooling.
- edge_cases_or_failure_modes: Duplicate entries, stale scope, malformed bank file.
- validation_or_tests: Hindsight tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2138 `file` `packages/coding-agent/src/lsp/diagnostics-ledger.ts`
- cursor: `[_]`
- core_role: Ledger for tracking LSP diagnostics across edits.
- algorithmic_behavior: Records diagnostic snapshots/late diagnostics and exposes update/lookup helpers.
- inputs_outputs_state: Inputs are file paths, mutation counters, diagnostics; outputs are ledger entries for render/tool feedback; state is in-memory map/list.
- gates_or_invariants: Diagnostics must be tied to correct file/mutation generation to avoid stale warnings.
- dependencies_and_callers: Used by edit/write/LSP tool pipeline.
- edge_cases_or_failure_modes: Late diagnostics after file mutation, duplicate diagnostics, path normalization.
- validation_or_tests: LSP/edit tests cover indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2168 `file` `packages/coding-agent/src/mcp/types.ts`
- cursor: `[_]`
- core_role: MCP type/schema contract for coding-agent integration.
- algorithmic_behavior: Defines MCP server/tool/resource/config/session types and protocol-shaped data structures.
- inputs_outputs_state: Inputs/outputs are typed MCP configs/messages/tool descriptors; runtime state is none.
- gates_or_invariants: Type shapes must match MCP manager/runtime expectations.
- dependencies_and_callers: Used by MCP manager, tools, root list tests.
- edge_cases_or_failure_modes: Type-only drift from protocol, optional field mismatches.
- validation_or_tests: MCP tests including roots list cover consumers.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2198 `file` `packages/coding-agent/src/modes/turn-budget.ts`
- cursor: `[_]`
- core_role: Turn budget calculations for modes.
- algorithmic_behavior: Computes allowed/remaining turn counts from configured mode budget and current completed turns.
- inputs_outputs_state: Inputs are budget settings and counters; outputs are budget state/booleans; state is none.
- gates_or_invariants: Budgets should not go negative except as explicit exhausted state; undefined budget means unbounded.
- dependencies_and_callers: Used by plan/goal/mode controllers.
- edge_cases_or_failure_modes: Zero budget, off-by-one after current turn, missing config.
- validation_or_tests: Mode tests cover indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2228 `file` `packages/coding-agent/src/session/session-loader.ts`
- cursor: `[_]`
- core_role: Session file/path loader.
- algorithmic_behavior: Resolves session identifiers/paths, reads session metadata/history, and returns load results for CLI/session switching.
- inputs_outputs_state: Inputs are cwd/session path/id; outputs are loaded session data or errors; state is filesystem session store.
- gates_or_invariants: Loader must distinguish missing/unreadable/invalid sessions.
- dependencies_and_callers: Used by join command, session switching, RPC/ACP session list.
- edge_cases_or_failure_modes: Corrupt JSON, stale symlink, missing active session.
- validation_or_tests: Session manager/navigation/RPC tests cover related behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2258 `file` `packages/coding-agent/src/stt/models.ts`
- cursor: `[_]`
- core_role: Speech-to-text model definitions/resolution.
- algorithmic_behavior: Defines available STT models/providers and helper lookup/formatting logic.
- inputs_outputs_state: Inputs are configured model IDs/provider names; outputs are model descriptors or errors; state is static tables.
- gates_or_invariants: Unknown STT model should fail or fall back consistently; descriptors must include provider requirements.
- dependencies_and_callers: Used by STT/login/settings flows.
- edge_cases_or_failure_modes: Deprecated model IDs, missing API key/provider capability.
- validation_or_tests: STT tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2288 `file` `packages/coding-agent/src/tools/ask.ts`
- cursor: `[_]`
- core_role: User-input request tool for plan/interactive flows.
- algorithmic_behavior: Validates short questions/options, renders prompts, enqueues user input requests through session/client bridge, supports auto-resolution windows, and returns selected/freeform answers.
- inputs_outputs_state: Inputs are question specs, options, autoResolutionMs, context/session bridge; outputs are tool text/details with answers or timeout/default; state is pending request in UI bridge.
- gates_or_invariants: Questions capped and options constrained; auto-resolution must be within allowed range; input request must be unavailable-safe outside supported runtimes.
- dependencies_and_callers: Used by plan mode and interactive tools; depends on Arktype schema, TUI rendering, `ClientBridge`.
- edge_cases_or_failure_modes: No bridge/UI, timeout, invalid option count, freeform "Other", abort while waiting.
- validation_or_tests: Ask/plan-mode tests cover related behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2318 `file` `packages/coding-agent/src/tools/index.ts`
- cursor: `[_]`
- core_role: Central tool registry/session contract and tool loading policy.
- algorithmic_behavior: Defines `ToolSession`, built-in exports, essential/discoverable load modes, default essential tools, discovery filtering, built-in/hidden tool factories, and context hooks for eval, MCP, plan, artifacts, diagnostics, mutation counters, etc.
- inputs_outputs_state: Inputs are settings, session services, model/config, discovery state; outputs are active tool factories and filtered tool lists; state is session-provided services.
- gates_or_invariants: Essential tools load unless explicitly filtered; discoverable tools can be withheld until search; forced/restored/requested tools bypass discovery filtering.
- dependencies_and_callers: Used by session startup, tool discovery, all built-in tool implementations.
- edge_cases_or_failure_modes: Tool name drift, discovery mode hiding required tool, missing session hook for a tool, hidden tool exposure.
- validation_or_tests: Tool schema/discovery/plan/RPC tests cover registry behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2348 `file` `packages/coding-agent/src/tools/sqlite-reader.ts`
- cursor: `[_]`
- core_role: SQLite file reader/query/mutation helper for tool path selectors.
- algorithmic_behavior: Detects SQLite files, parses `db.sqlite[:table[/key]?query]` selectors, lists tables, renders schema/sample/table/row output, validates safe `where`/order/limit/offset, executes raw read queries, and supports insert/update/delete helpers.
- inputs_outputs_state: Inputs are file paths, URL query params, table/key/data, SQLite DB; outputs are rendered tables/rows/schema or mutation counts; state is DB connection scope.
- gates_or_invariants: Raw query cannot combine with selectors/pagination; `where` forbids comments/terminators and dangerous keywords; identifiers are quoted; row lookup rejects composite PK and WITHOUT ROWID as needed.
- dependencies_and_callers: Used by read/write style database tooling; depends on `bun:sqlite`, render-utils, `ToolError`.
- edge_cases_or_failure_modes: Invalid numeric limits/offsets, unsupported query params, non-scalar writes, large raw query truncation, missing table/column, unsafe `where`.
- validation_or_tests: Tool schema/database tests cover behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2378 `file` `packages/coding-agent/src/utils/block-context.ts`
- cursor: `[_]`
- core_role: Block/context extraction utility for source snippets.
- algorithmic_behavior: Resolves surrounding blocks/line contexts around target locations for display or edit context.
- inputs_outputs_state: Inputs are file text, line/range hints, options; outputs are block snippets/context metadata; state is none.
- gates_or_invariants: Context windows should remain bounded and line-index safe.
- dependencies_and_callers: Used by read/edit/search renderers or diagnostics.
- edge_cases_or_failure_modes: Empty files, out-of-range lines, nested braces/blocks, very long lines.
- validation_or_tests: Utility tests not assigned; covered by tools consuming block context.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2408 `file` `packages/coding-agent/src/web/parallel.ts`
- cursor: `[_]`
- core_role: Parallel web/search task runner.
- algorithmic_behavior: Runs multiple web operations with bounded concurrency, aggregates results, preserves association/order, and handles abort/error behavior.
- inputs_outputs_state: Inputs are task specs/fetch/search operations/concurrency; outputs are result arrays/errors; state is in-flight task set.
- gates_or_invariants: Abort should cancel outstanding work; failures should be represented consistently without dropping other results.
- dependencies_and_callers: Used by web search/open/scraper tooling.
- edge_cases_or_failure_modes: Partial failures, rate limits, concurrency zero/unbounded, abort races.
- validation_or_tests: Web/search tests cover indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2438 `file` `packages/coding-agent/src/workflow/shell-script-runtime.ts`
- cursor: `[_]`
- core_role: Shell script runtime adapter for workflow execution.
- algorithmic_behavior: Executes workflow shell scripts, captures stdout/stderr/status, and maps process results into workflow state/errors.
- inputs_outputs_state: Inputs are script/cwd/env/runtime options; outputs are execution result; state is child process lifecycle.
- gates_or_invariants: Nonzero exit and spawn errors must surface; env/cwd should be controlled.
- dependencies_and_callers: Used by workflow engine; tested by workflow shell-script runtime tests.
- edge_cases_or_failure_modes: Timeout/abort, missing shell/script, large output.
- validation_or_tests: `packages/coding-agent/src/workflow/__tests__/shell-script-runtime.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2468 `file` `packages/coding-agent/test/core/python-executor-streaming.test.ts`
- cursor: `[_]`
- core_role: Tests Python executor streaming behavior.
- algorithmic_behavior: Runs/uses Python executor harness and verifies streamed chunks/status rather than only final output.
- inputs_outputs_state: Inputs are Python code/cell options; outputs are streamed text/events; state is executor/kernel session.
- gates_or_invariants: Streaming must arrive incrementally and final result must include complete output.
- dependencies_and_callers: Tests eval Python executor/kernel.
- edge_cases_or_failure_modes: Buffered output, subprocess startup, kernel teardown.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2498 `file` `packages/coding-agent/test/discovery/github-skills.test.ts`
- cursor: `[_]`
- core_role: Tests GitHub skill discovery.
- algorithmic_behavior: Mocks/discovers GitHub skill metadata and verifies filtering/normalization.
- inputs_outputs_state: Inputs are fake GitHub skill sources; outputs are discovered skill descriptors; state is temp/user extension filtering.
- gates_or_invariants: Skill names/URLs must normalize and unsafe/unwanted extensions are filtered.
- dependencies_and_callers: Tests discovery/skills subsystem.
- edge_cases_or_failure_modes: Invalid repo URL, duplicate skill, missing metadata.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2528 `file` `packages/coding-agent/test/helpers/settings-test-state.ts`
- cursor: `[_]`
- core_role: Test helper for isolating settings state.
- algorithmic_behavior: Saves/restores settings-related globals/env/temp dirs around tests.
- inputs_outputs_state: Inputs are test callbacks/options; outputs are isolated settings context; state is captured/restored settings.
- gates_or_invariants: Tests must not leak settings/cwd/env across files.
- dependencies_and_callers: Used by coding-agent settings tests.
- edge_cases_or_failure_modes: Restore failure, nested helper calls, temp cleanup.
- validation_or_tests: Helper supports tests; no direct assertions inside.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2558 `file` `packages/coding-agent/test/modes/markdown-prose.test.ts`
- cursor: `[_]`
- core_role: Tests markdown/prose mode behavior.
- algorithmic_behavior: Verifies mode output/instruction handling for markdown prose constraints.
- inputs_outputs_state: Inputs are mode config/text; outputs are rendered or validated prose behavior; state is mode object.
- gates_or_invariants: Markdown prose mode should preserve required formatting and avoid inappropriate tool behavior.
- dependencies_and_callers: Tests modes subsystem.
- edge_cases_or_failure_modes: Empty markdown, headings/lists, mode switching.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2588 `file` `packages/coding-agent/test/session/session-manager-fork.test.ts`
- cursor: `[_]`
- core_role: Tests session manager fork behavior.
- algorithmic_behavior: Creates sessions and verifies forked sessions inherit expected messages/state while receiving new IDs/paths.
- inputs_outputs_state: Inputs are session manager state and fork request; outputs are fork result/session files; state is temp session store.
- gates_or_invariants: Fork must not mutate original; lineage/history preserved enough for continuation.
- dependencies_and_callers: Tests session manager.
- edge_cases_or_failure_modes: Missing source session, fork from branch point, file write failure.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2618 `file` `packages/coding-agent/test/task/executor-warnings.test.ts`
- cursor: `[_]`
- core_role: Tests task/subagent executor warning behavior.
- algorithmic_behavior: Simulates subagent execution warnings and verifies warnings are surfaced/deduped/formatted correctly.
- inputs_outputs_state: Inputs are fake executor outputs/warnings; outputs are warnings in result/transcript; state is task executor harness.
- gates_or_invariants: Warnings must not be swallowed or duplicated; severe failures still fail task.
- dependencies_and_callers: Tests task executor/output manager.
- edge_cases_or_failure_modes: Multiple warnings, concurrent tasks, warnings with failure.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2648 `file` `packages/coding-agent/test/tools/bash-skill-urls.test.ts`
- cursor: `[_]`
- core_role: Tests bash tool handling of skill URLs/references.
- algorithmic_behavior: Feeds bash/tool rendering inputs containing skill URLs and verifies safe parsing/rendering/rewriting behavior.
- inputs_outputs_state: Inputs are command strings/skill metadata; outputs are rendered command/tool results; state is test harness.
- gates_or_invariants: URLs should not break command preview or skill resolution; unsafe expansion avoided.
- dependencies_and_callers: Tests bash tool and skill URL integration.
- edge_cases_or_failure_modes: Quoted URLs, multiple URLs, malformed skill refs.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2678 `file` `packages/coding-agent/test/tools/image-gen.test.ts`
- cursor: `[_]`
- core_role: Tests image generation tool behavior.
- algorithmic_behavior: Mocks image generation calls and verifies tool args, output blocks, artifacts, and error paths.
- inputs_outputs_state: Inputs are prompts/options/mock provider responses; outputs are image content/tool result; state is temp artifacts.
- gates_or_invariants: Generated images must include correct MIME/data/artifact metadata; failures surface cleanly.
- dependencies_and_callers: Tests image-gen tool.
- edge_cases_or_failure_modes: Missing provider/key, invalid image data, artifact write failure.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2708 `file` `packages/coding-agent/test/tools/schema-validation.test.ts`
- cursor: `[_]`
- core_role: Tests tool schema validation contracts.
- algorithmic_behavior: Builds tool schemas and verifies argument validation, strict/lenient behavior, output schema conversion, and error messages.
- inputs_outputs_state: Inputs are schemas/tool calls; outputs are accepted args or validation errors; state is none.
- gates_or_invariants: Schema validation must reject invalid shapes while allowing intended loose/coerced cases.
- dependencies_and_callers: Tests tool layer/schema utilities.
- edge_cases_or_failure_modes: `$ref`, arrays, nulls, extra keys, malformed schemas.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2738 `file` `packages/coding-agent/test/utils/filter-user-extensions.ts`
- cursor: `[_]`
- core_role: Test utility for filtering user extensions.
- algorithmic_behavior: Filters extension lists to isolate tests from user-local extensions.
- inputs_outputs_state: Inputs are extension descriptors; outputs are filtered arrays; state is none.
- gates_or_invariants: Tests should only see controlled fixtures, not user-installed extensions.
- dependencies_and_callers: Used by discovery/plugin tests.
- edge_cases_or_failure_modes: Source/name mismatch, empty lists.
- validation_or_tests: Helper supports tests; no standalone assertions.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2768 `file` `packages/coding-agent/test/workflow/state.test.ts`
- cursor: `[_]`
- core_role: Tests workflow state transitions.
- algorithmic_behavior: Creates workflow state machines and verifies transitions, persistence, and invalid transition handling.
- inputs_outputs_state: Inputs are workflow definitions/events; outputs are workflow state snapshots/results; state is in-memory workflow store.
- gates_or_invariants: Invalid transitions rejected; valid transitions preserve required fields.
- dependencies_and_callers: Tests workflow state module.
- edge_cases_or_failure_modes: Missing step, repeated completion, failed step recovery.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2798 `file` `packages/mnemopi/src/core/fastembed-runtime.ts`
- cursor: `[_]`
- core_role: FastEmbed runtime configuration/pinning.
- algorithmic_behavior: Resolves FastEmbed runtime package/version/executable/environment details for embedding operations.
- inputs_outputs_state: Inputs are env/package runtime metadata; outputs are runtime descriptor; state is static/cache.
- gates_or_invariants: Runtime pins must match tested expected values.
- dependencies_and_callers: Used by mnemopi embedding core.
- edge_cases_or_failure_modes: Missing dependency, wrong version, incompatible platform.
- validation_or_tests: `packages/mnemopi/test/fastembed-runtime.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2828 `file` `packages/mnemopi/src/util/env.ts`
- cursor: `[_]`
- core_role: Mnemopi environment helper.
- algorithmic_behavior: Reads/normalizes env flags/paths relevant to memory/embedding runtime.
- inputs_outputs_state: Inputs are process env; outputs are typed config values; state is none.
- gates_or_invariants: Env parsing should be deterministic and validate expected values.
- dependencies_and_callers: Used by mnemopi core.
- edge_cases_or_failure_modes: Invalid booleans/numbers/paths, missing env.
- validation_or_tests: Covered indirectly by mnemopi runtime tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2858 `file` `packages/utils/test/mermaid/class-arrows.test.ts`
- cursor: `[_]`
- core_role: Tests Mermaid ASCII class-diagram arrow parsing/rendering.
- algorithmic_behavior: Exercises class relationship arrows, inheritance/association/dependency variants, marker direction, and rendered ASCII expectations.
- inputs_outputs_state: Inputs are Mermaid class diagrams; outputs are parsed relationships/rendered ASCII; state is none.
- gates_or_invariants: Arrow semantics and direction markers must be stable across parser/renderer.
- dependencies_and_callers: Tests vendored Mermaid ASCII parser/renderer.
- edge_cases_or_failure_modes: Reverse arrows, labels, all relationship types, duplicate class refs.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2888 `directory` `packages/coding-agent/src/modes/components/extensions`
- cursor: `[_]`
- core_role: TUI extension management dashboard components.
- algorithmic_behavior: `extension-dashboard.ts` renders two-column extension management UI, handles navigation/toggle/provider selection; `extension-list.ts` renders lists; `inspector-panel.ts` displays details; `state-manager.ts` manages extension enable/disable/provider state; `types.ts` defines shared types; `index.ts` re-exports.
- inputs_outputs_state: Inputs are extension descriptors/settings/key events/theme; outputs are TUI components/rendered lines and updated extension state; state is selected index, filters, provider choice, manager state.
- gates_or_invariants: Toggle/provider changes must map to valid extension IDs/providers; rendering truncates/wraps text; empty lists handled.
- dependencies_and_callers: Used by coding-agent modes/settings UI and extension registry.
- edge_cases_or_failure_modes: No extensions, long names/descriptions, invalid provider, stale selection after filter.
- validation_or_tests: Extension/dashboard tests cover indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2918 `file` `crates/pi-shell/src/minimizer/filters/pkg.rs`
- cursor: `[_]`
- core_role: Shell minimizer package-filter logic.
- algorithmic_behavior: Parses and filters package-manager command output/metadata to reduce irrelevant noise while preserving semantically important package operations.
- inputs_outputs_state: Inputs are shell output/command lines/package text; outputs are minimized text/tokens; state is filter-local.
- gates_or_invariants: Must not remove error lines or package names needed to understand install/build failures.
- dependencies_and_callers: Used by `pi-shell` minimizer in command output processing.
- edge_cases_or_failure_modes: Multiple package managers, lockfile messages, warnings vs progress bars, localized/noisy output.
- validation_or_tests: Shell/minimizer tests cover package filtering.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2948 `file` `packages/ai/src/utils/schema/dereference.ts`
- cursor: `[_]`
- core_role: JSON Schema `$ref` dereferencing helper.
- algorithmic_behavior: Recursively inlines local `$defs`/definitions references, detects circular/deep schemas, and returns dereferenced schema or failure.
- inputs_outputs_state: Inputs are JSON Schema objects; outputs are cloned/dereferenced schema or error/fallback signal; state is traversal stack/seen set.
- gates_or_invariants: External refs should remain unresolved/fail safely; circular refs must not recurse forever.
- dependencies_and_callers: Used by yield/output schema and provider schema rendering.
- edge_cases_or_failure_modes: Circular `$ref`, external URI, missing definition, very deep schema.
- validation_or_tests: Yield/schema validation tests exercise dereferencing/fallback.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2978 `file` `packages/coding-agent/src/cli/gallery-fixtures/misc.ts`
- cursor: `[_]`
- core_role: Miscellaneous gallery fixture definitions for CLI/TUI demos.
- algorithmic_behavior: Provides static examples of tool/session/render states for gallery output.
- inputs_outputs_state: Inputs are gallery selection; outputs are fixture objects/rendered demos; state is static.
- gates_or_invariants: Fixtures should match renderer schemas to avoid gallery crashes.
- dependencies_and_callers: Used by gallery CLI.
- edge_cases_or_failure_modes: Stale fixture shape after renderer changes.
- validation_or_tests: Gallery/snapshot tests cover indirectly.
- skip_candidate: `yes: fixture data, not core algorithm, though it validates renderer shapes`

### OH_MY_HUMANIZE_MAIN-HZ-3008 `file` `packages/coding-agent/src/edit/hashline/block-resolver.ts`
- cursor: `[_]`
- core_role: Hashline block resolver for edit targets.
- algorithmic_behavior: Resolves hashline block identifiers/locations into concrete file block ranges for edit operations.
- inputs_outputs_state: Inputs are block IDs/hashline map/file content; outputs are resolved block/range or failure; state is none.
- gates_or_invariants: Ambiguous or missing block IDs must not edit the wrong range.
- dependencies_and_callers: Used by coding-agent edit/hashline integration.
- edge_cases_or_failure_modes: Stale hashlines after file mutation, duplicate hashes, missing snapshot.
- validation_or_tests: Hashline/edit tests cover indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3038 `file` `packages/coding-agent/src/eval/py/prelude.py`
- cursor: `[_]`
- core_role: Python helper prelude injected into eval kernels.
- algorithmic_behavior: Defines display/output helpers, filesystem/text helpers, tool/completion/agent bridge calls, concurrency helpers, status event emission, JSON/image/markdown capture, and path/protocol handling.
- inputs_outputs_state: Inputs are user Python cell code, helper calls, injected env/bridge variables; outputs are NDJSON/status/display artifacts and return values; state persists in Python kernel globals.
- gates_or_invariants: Interactive stdin unsupported; helper paths restrict protocol writes; bridge errors raise exceptions; parallel/pipeline preserve order and propagate exceptions.
- dependencies_and_callers: Loaded by eval Python executor/kernel; documented in `docs/tools/eval.md`.
- edge_cases_or_failure_modes: Missing artifacts dir/session file, bridge unavailable, invalid JSON/schema, file path protocol mismatch, cancellation.
- validation_or_tests: Python executor streaming/eval tests cover behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3068 `file` `packages/coding-agent/src/extensibility/plugins/git-url.ts`
- cursor: `[_]`
- core_role: Git URL/spec parser for plugin installation.
- algorithmic_behavior: Strips URL credentials, parses known hosts/shorthands/SCP-like/HTTP/SSH/git URLs, splits refs, normalizes repo/host/path/ref, marks pinned specs, and identifies valid git specs.
- inputs_outputs_state: Inputs are user plugin source strings; outputs are `GitSource` descriptors or null; state is none.
- gates_or_invariants: Credentials must not persist in repo strings; known host path extraction rejects archive/subpaths; invalid host/path/ref combinations return null.
- dependencies_and_callers: Used by plugin installer/config discovery.
- edge_cases_or_failure_modes: Hash refs in URLs, `git@host:path#ref`, namespaced shorthands, localhost/private hosts, project names containing `@`.
- validation_or_tests: Plugin config/GitHub skills tests cover related parsing.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3098 `file` `packages/coding-agent/src/modes/components/agent-dashboard.ts`
- cursor: `[_]`
- core_role: TUI dashboard for browsing, editing, and creating subagents.
- algorithmic_behavior: Filters/sorts agents by source/query, renders list/inspector/tabs, resolves default/effective model patterns, validates generated agent specs, drives agent-creation prompts through a model, writes agent files, and handles create/review/edit states.
- inputs_outputs_state: Inputs are cwd/settings/model registry/agents/key events/user descriptions/model responses; outputs are TUI lines, created/edited agent specs/files, notices; state includes selected index, tab/filter/search, create state/spec.
- gates_or_invariants: Agent identifier pattern is constrained; generated JSON is extracted/validated; model resolution must use configured/default patterns; created agents directory must resolve before write.
- dependencies_and_callers: Used by modes UI; depends on agent registry, model resolver, prompts, TUI utilities.
- edge_cases_or_failure_modes: Malformed model JSON, unresolved agents dir, long descriptions/prompts, small terminal widths, stale selection after filtering.
- validation_or_tests: Component tests include tree-selector and render initial message utilities; direct dashboard tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3128 `file` `packages/coding-agent/src/modes/components/login-dialog.ts`
- cursor: `[_]`
- core_role: TUI login/OAuth dialog component.
- algorithmic_behavior: Renders login flow, opens browser best-effort, prompts for pasted codes/input via `Promise.withResolvers`, handles cancellation and completion callbacks.
- inputs_outputs_state: Inputs are login URL/provider/user input; outputs are rendered dialog lines and resolved input string; state is input resolver/pending promise.
- gates_or_invariants: Resolver must be cleared on completion/cancel; browser open failure should not block manual flow.
- dependencies_and_callers: Used by login mode/components.
- edge_cases_or_failure_modes: User cancels, multiple prompts, browser open failure, repeated input after resolver cleared.
- validation_or_tests: Login/UI tests cover indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3158 `file` `packages/coding-agent/src/modes/components/usage-row.ts`
- cursor: `[_]`
- core_role: Small TUI component/helper for usage rows.
- algorithmic_behavior: Formats usage display row content for model/quota UI.
- inputs_outputs_state: Inputs are usage values/theme; outputs are rendered text row; state is none.
- gates_or_invariants: Should handle missing/unknown usage without layout break.
- dependencies_and_callers: Used by usage/dashboard components.
- edge_cases_or_failure_modes: Long labels, undefined fraction, exhausted status.
- validation_or_tests: Usage CLI/component tests cover indirectly.
- skip_candidate: `yes: presentational formatting helper with minimal algorithmic surface`

### OH_MY_HUMANIZE_MAIN-HZ-3188 `file` `packages/coding-agent/src/modes/setup-wizard/lazy.ts`
- cursor: `[_]`
- core_role: Lazy loader/export for setup wizard.
- algorithmic_behavior: Defers setup wizard module loading behind a small wrapper.
- inputs_outputs_state: Inputs are caller request; outputs are loaded setup wizard factory/module; state is module cache.
- gates_or_invariants: Lazy import path must remain valid.
- dependencies_and_callers: Used by modes/setup entry.
- edge_cases_or_failure_modes: Broken module path, load-time errors.
- validation_or_tests: Setup wizard tests/build cover indirectly.
- skip_candidate: `yes: lazy-loading glue with no substantive algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3218 `file` `packages/coding-agent/src/tools/browser/render.ts`
- cursor: `[_]`
- core_role: TUI renderer for browser tool calls/results.
- algorithmic_behavior: Describes browser backend, renders run/open/close status lines, extracts text output, renders code-cell previews with cached width/key, appends URL/browser/tab metadata, and handles expanded/partial/error states.
- inputs_outputs_state: Inputs are browser args/details/result content/theme/render context; outputs are TUI components/lines; state is per-render cached lines.
- gates_or_invariants: Run action gets cell renderer; open/close compact line; tabs/paths are shortened/sanitized; cache key includes output/details/width.
- dependencies_and_callers: Used by browser tool renderer pipeline and TUI code-cell utilities.
- edge_cases_or_failure_modes: Missing details, partial output, long URLs, different browser backends, stale cache.
- validation_or_tests: Browser render/tool tests cover indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3248 `file` `packages/coding-agent/src/web/scrapers/go-pkg.ts`
- cursor: `[_]`
- core_role: Special web scraper for `pkg.go.dev`.
- algorithmic_behavior: Recognizes pkg.go.dev URLs, fetches Go proxy latest/version metadata, fetches/parses page DOM, extracts module/package/version/synopsis/overview/imports/documentation sections, and returns markdown result with metadata.
- inputs_outputs_state: Inputs are URL/fetch/scraper context; outputs are special handler result markdown/notes; state is network responses only.
- gates_or_invariants: Only handles `pkg.go.dev`; failed page fetch returns diagnostic result; proxy metadata used when module/version derivable.
- dependencies_and_callers: Used by web open/search scraping pipeline; depends on HTML parser utilities and Go proxy.
- edge_cases_or_failure_modes: Non-module pages, missing DOM selectors, proxy 404, version badge absence, encoded module paths.
- validation_or_tests: Web scraper tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3278 `file` `packages/coding-agent/src/web/scrapers/reddit.ts`
- cursor: `[_]`
- core_role: Special web scraper for Reddit.
- algorithmic_behavior: Converts Reddit URLs to JSON API fetches, renders post/listing metadata and comments/posts into markdown, and returns method metadata.
- inputs_outputs_state: Inputs are Reddit URL/fetch context; outputs are markdown result with fetchedAt/notes; state is network response only.
- gates_or_invariants: Only handles reddit.com hosts; JSON API failures fall back through scraper error path.
- dependencies_and_callers: Used by web scraping pipeline.
- edge_cases_or_failure_modes: Listing vs post JSON shape, deleted authors/content, empty listings, rate limiting.
- validation_or_tests: Web scraper tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3308 `file` `packages/coding-agent/src/workflow/__tests__/shell-script-runtime.test.ts`
- cursor: `[_]`
- core_role: Tests workflow shell script runtime.
- algorithmic_behavior: Executes temporary shell scripts and verifies success, failure, stdout/stderr, env/cwd, and error mapping.
- inputs_outputs_state: Inputs are temp scripts/options; outputs are runtime results; state is child process/temp dirs.
- gates_or_invariants: Exit codes and output must map exactly enough for workflow decisions.
- dependencies_and_callers: Tests `src/workflow/shell-script-runtime.ts`.
- edge_cases_or_failure_modes: Nonzero exit, missing script, env propagation.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3338 `file` `packages/coding-agent/test/modes/components/tree-selector-empty-state-1909.test.ts`
- cursor: `[_]`
- core_role: Regression test for tree selector empty state.
- algorithmic_behavior: Renders tree selector with no items and verifies stable empty-state output/selection behavior.
- inputs_outputs_state: Inputs are empty tree/list props; outputs are rendered lines/state; state is component instance.
- gates_or_invariants: Empty tree must not crash or select invalid item.
- dependencies_and_callers: Tests modes component tree selector.
- edge_cases_or_failure_modes: Zero height/width, no selectable rows.
- validation_or_tests: File is direct issue regression.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3368 `file` `packages/coding-agent/test/modes/utils/render-initial-messages.test.ts`
- cursor: `[_]`
- core_role: Tests initial message rendering utilities.
- algorithmic_behavior: Builds initial/system/user/tool messages and verifies rendered output, filtering, ordering, and formatting.
- inputs_outputs_state: Inputs are message arrays/context; outputs are rendered initial messages; state is none.
- gates_or_invariants: Important startup messages must remain visible while hidden/internal messages are filtered.
- dependencies_and_callers: Tests modes rendering utilities.
- edge_cases_or_failure_modes: Empty messages, custom/tool messages, ordering.
- validation_or_tests: File is direct test coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3398 `file` `packages/collab-web/src/components/shell/Composer.tsx`
- cursor: `[_]`
- core_role: Web collaboration composer component.
- algorithmic_behavior: Tracks textarea draft, auto-resizes up to 8 rows, sends prompt through client, disables/badges busy/queued state.
- inputs_outputs_state: Inputs are client and snapshot; outputs are React textarea/button UI and client send call; state is React local draft/ref.
- gates_or_invariants: Busy/streaming state disables send; height clamps between single-row and max; queued count reflects snapshot.
- dependencies_and_callers: Used by collab web shell.
- edge_cases_or_failure_modes: Empty send, rapidly changing snapshot, long drafts.
- validation_or_tests: Web component tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3428 `file` `packages/collab-web/src/tool-render/tools/resolve.tsx`
- cursor: `[_]`
- core_role: Web renderer for `resolve` tool.
- algorithmic_behavior: Renders summary/body for apply/discard actions, reason text, source label, resolved status, and result text with truncation/normalization.
- inputs_outputs_state: Inputs are tool args/result/details; outputs are React nodes; state is none.
- gates_or_invariants: Long text is truncated; whitespace normalized; tone reflects action/status.
- dependencies_and_callers: Used by collab web tool-render registry.
- edge_cases_or_failure_modes: Missing args/result/details, unknown action, long reason/result.
- validation_or_tests: Tool renderer tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3458 `file` `packages/stats/src/client/components/range-meta.ts`
- cursor: `[_]`
- core_role: Client-side time-range metadata for stats charts.
- algorithmic_behavior: Maps `TimeRange` to duration, bucket size, expected buckets, tick format, and formats tick timestamps with date-fns.
- inputs_outputs_state: Inputs are range enum and timestamp; outputs are `RangeMeta` or formatted tick string; state is static table.
- gates_or_invariants: Client bucket metadata must match server DB range query assumptions.
- dependencies_and_callers: Used by stats chart/table components; related to DB range tests.
- edge_cases_or_failure_modes: Unknown range key, timezone/local formatting differences.
- validation_or_tests: `packages/stats/test/db-range.test.ts` covers server-side alignment indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3488 `file` `packages/utils/src/vendor/mermaid-ascii/text-metrics.ts`
- cursor: `[_]`
- core_role: Text display-width/cell conversion for Mermaid ASCII renderer.
- algorithmic_behavior: Uses `Intl.Segmenter` and `Bun.stringWidth` to measure grapheme display width as 1 or 2 cells, and converts text to cell array with `WIDE_PAD` placeholders for second fullwidth cell.
- inputs_outputs_state: Inputs are label strings; outputs are display column counts and cell arrays; state is segmenter.
- gates_or_invariants: Wide/fullwidth/emoji graphemes occupy two cells; ambiguous structural glyphs stay narrow; renderer grid alignment depends on `WIDE_PAD`.
- dependencies_and_callers: Used by vendored Mermaid ASCII renderer.
- edge_cases_or_failure_modes: ZWJ emoji, regional flags, CJK, combining marks.
- validation_or_tests: Mermaid golden/class/multiline/xychart tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3518 `file` `packages/coding-agent/src/eval/js/shared/prelude.ts`
- cursor: `[_]`
- core_role: Tiny JS eval prelude module entry.
- algorithmic_behavior: Re-exports or references shared JS prelude content for eval runtime.
- inputs_outputs_state: Inputs are eval JS worker import; outputs are prelude string/helpers; state is none.
- gates_or_invariants: Import path/content must stay valid for eval worker.
- dependencies_and_callers: Used by JS eval executor/worker.
- edge_cases_or_failure_modes: Broken export causes JS eval helper injection failure.
- validation_or_tests: Eval JS tests cover indirectly.
- skip_candidate: `yes: two-line glue module; substantive algorithm lives in shared prelude/helpers`

### OH_MY_HUMANIZE_MAIN-HZ-3548 `file` `packages/coding-agent/src/modes/components/status-line/index.ts`
- cursor: `[_]`
- core_role: Status-line component barrel.
- algorithmic_behavior: Re-exports status-line submodules for mode components.
- inputs_outputs_state: Inputs are submodule exports; output is aggregate API; state is none.
- gates_or_invariants: Public component exports remain available.
- dependencies_and_callers: Used by TUI mode components.
- edge_cases_or_failure_modes: Missing export breaks imports.
- validation_or_tests: Component render tests cover consumers.
- skip_candidate: `yes: pure barrel/export glue`

### OH_MY_HUMANIZE_MAIN-HZ-3578 `file` `packages/coding-agent/src/web/search/providers/synthetic.ts`
- cursor: `[_]`
- core_role: Synthetic.new web search provider implementation.
- algorithmic_behavior: Resolves API key from auth storage/env, POSTs query to Synthetic search endpoint, classifies HTTP/auth errors, maps returned results into common `SearchResponse`, and exposes provider availability.
- inputs_outputs_state: Inputs are search params, auth storage/session ID, fetch implementation, signal; outputs are normalized search results or provider errors; state is none.
- gates_or_invariants: Missing key message is explicit; provider availability checks auth/env; HTTP errors are classified before throwing.
- dependencies_and_callers: Used by web search provider registry; depends on auth storage and provider error helpers.
- edge_cases_or_failure_modes: Missing credentials, non-OK response, malformed response result entries, abort signal.
- validation_or_tests: Web search provider tests not assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3608 `file` `packages/coding-agent/src/extensibility/custom-commands/bundled/review/index.ts`
- cursor: `[_]`
- core_role: Bundled `/review` custom command implementation.
- algorithmic_behavior: Parses git/jj diffs, excludes generated/lock/binary-like paths, computes diff stats and recommended agent count, builds prompts from templates, parses GitHub/pr:// PR refs, discovers recent PR refs from transcript, offers UI choices, and returns review prompts/instructions.
- inputs_outputs_state: Inputs are command args, git/jj state, transcript entries, UI selections, diff output; outputs are prompt text or UI notifications; state is command-local choices.
- gates_or_invariants: Empty diffs warn/return undefined; repo/PR segments and positive PR numbers validated; large diffs use instructions instead of inline huge diff; UI-less mode returns headless prompt.
- dependencies_and_callers: Used by custom command registry; depends on git/jj utilities, prompt templates, hook command context.
- edge_cases_or_failure_modes: No repo/diff, invalid PR URL, huge diff/file count, excluded-only changes, no base branch/commit selected, malformed transcript refs.
- validation_or_tests: Custom command/review tests not assigned; behavior is template-driven and observable by command execution.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 121 item-evidence headings were written, one per assigned row, using the assigned paths and types.
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`