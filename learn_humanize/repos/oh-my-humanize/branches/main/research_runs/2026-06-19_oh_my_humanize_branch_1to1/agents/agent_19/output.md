# agent_19 main 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 121
- source_commit: `6b3819fad50a89fffae899b240ad1ce065c51d23`

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-019 `directory` `crates/pi-ast`
- cursor: `[_]`
- core_role: Rust AST service for structural language detection, ast-grep search/rewrite, block boundary discovery, and code summarization.
- algorithmic_behavior: Recursively covers `src/block.rs`, `src/language/*`, `src/ops.rs`, and `src/summary.rs`; `block_range_at` maps 1-indexed lines to outer named tree-sitter nodes, `ops.rs` compiles ast-grep patterns/rewrite rules and applies ordered edits, and `summary.rs` builds elidable span forests with breadth-first unfolding.
- inputs_outputs_state: Inputs are source text, optional file path/language, line/range/options, glob roots, and rewrite rules; outputs are matches, rewritten source, block ranges, summary segments, or soft `None` for unsupported/unsafe cases. State is parser-local plus language tables.
- gates_or_invariants: Unknown language and parse errors short-circuit structural operations; `apply_edits` rejects overlapping/out-of-bounds edits and invalid UTF-8; block lookup ignores blanks, closer-only lines, and nodes with syntax errors.
- dependencies_and_callers: Depends on tree-sitter grammars, ast-grep, globset, ignore, and language alias tables; exposed through `pi-natives` to coding-agent edit/search/read context features.
- edge_cases_or_failure_modes: Shell rc dotfiles infer Bash; HTML script/style injections are parsed specially; syntax errors degrade summaries to raw/unparsed segments; BFS summary expansion avoids overlarge spans.
- validation_or_tests: Inline tests in `src/block.rs`, `src/ops.rs`, and `src/summary.rs` cover TS blocks, shell rc detection, edit rejection, and summary span behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-049 `file` `docs/fs-scan-cache-architecture.md`
- cursor: `[_]`
- core_role: Architecture contract for the native filesystem scan cache used by file discovery and invalidation consumers.
- algorithmic_behavior: Defines cache key dimensions, scan collection semantics, TTL behavior, empty-result rechecks, and explicit invalidation responsibilities.
- inputs_outputs_state: Inputs are scan root, `include_hidden`, `use_gitignore`, `skip_node_modules`, detail settings, and consumer context; outputs are cached directory/file listings and invalidation events.
- gates_or_invariants: Consumers must share the documented key shape and invalidate on mutating writes; empty cache entries have recheck policy to avoid masking newly created files.
- dependencies_and_callers: Documents coordination between `pi-natives` fs scanning and coding-agent file/search consumers.
- edge_cases_or_failure_modes: Stale results are possible if mutating call sites skip invalidation; empty-directory caching is treated separately because it is more failure-prone.
- validation_or_tests: Validation is by contract and consumer tests around fs-scan cache behavior, not directly executable from the doc.
- skip_candidate: `yes: documentation-only, but it defines runtime cache invariants for core discovery behavior`

### OH_MY_HUMANIZE_MAIN-HZ-079 `file` `infra/reload-runner.sh`
- cursor: `[_]`
- core_role: Infrastructure rollout script for rebuilding/reloading the remote runner image and Kubernetes deployment.
- algorithmic_behavior: Reads environment knobs, copies context over SSH, bootstraps containerd/buildkit tools, builds with containerd or Docker fallback, pushes/loads image, runs Helm upgrade, and verifies rollout.
- inputs_outputs_state: Inputs are env vars such as remote host, namespace, image tag, build backend, and kube context; outputs are remote build artifacts, container image updates, Helm release changes, and rollout status.
- gates_or_invariants: Verifies required tools before build, selects backend based on availability, and fails if rollout verification fails.
- dependencies_and_callers: Depends on SSH, containerd/buildkit or Docker, Helm, kubectl, and runner deployment manifests.
- edge_cases_or_failure_modes: Remote tool absence triggers bootstrap/fallback paths; image build or Helm rollout failures stop the script; bad env values can target the wrong cluster.
- validation_or_tests: Operational validation is embedded in command checks and rollout status checks.
- skip_candidate: `yes: infra script rather than product algorithm, but it implements runtime deployment workflow`

### OH_MY_HUMANIZE_MAIN-HZ-109 `file` `scripts/release.ts`
- cursor: `[_]`
- core_role: Release workflow coordinator for versioning, changelog finalization, checks, tagging, push, and CI watching.
- algorithmic_behavior: `watchCI` polls GitHub runs/jobs and tails logs on failure; `cmdRelease` preflights branch/clean tree/version, bumps package and Rust versions, bumps pi-natives sentinel, regenerates lockfile, fixes changelogs, runs `bun run check`, commits, tags, pushes atomically, then watches CI.
- inputs_outputs_state: Inputs are release version and repo state; outputs are modified manifests/changelogs/lockfile, commit/tag refs, pushed branch/tag, and CI status.
- gates_or_invariants: Requires main branch, clean worktree, valid semver-ish version, successful check command, and atomic push success before CI watch.
- dependencies_and_callers: Uses Bun, git, `gh`, package manifests, Rust manifests, changelog fixer, and CI workflows.
- edge_cases_or_failure_modes: Dirty tree, non-main branch, invalid version, failed check, failed push, or failed CI job halt the workflow with retry guidance.
- validation_or_tests: Runtime validation is in preflight gates plus `bun run check`; no direct test file was assigned.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-139 `directory` `packages/hashline/src`
- cursor: `[_]`
- core_role: Hashline patch language engine: tokenize, parse, normalize, apply, preview, repair, snapshot, and recover anchored edits.
- algorithmic_behavior: `tokenizer.ts` parses range/header/hunk tokens; `parser.ts` lowers tokens to edit operations; `apply.ts` applies line edits with replacement boundary repair, phantom delete handling, delimiter balance repair, and landing correction; `patcher.ts` orchestrates preflight and commit; `recovery.ts` replays stale snapshots through a 3-way style repair path.
- inputs_outputs_state: Inputs are patch text, current file contents, optional snapshots and block resolver; outputs are parsed sections, edits, apply results, mismatch diagnostics, compact diffs, and filesystem writes through injected FS.
- gates_or_invariants: Rejects overlapping deletes, invalid ranges, malformed headers, unsafe stale snapshot recovery, and failed boundary matching; all-or-nothing `Patcher` commit preserves preflight/commit separation.
- dependencies_and_callers: Used by coding-agent edit flows; depends on local tokenizer/parser/fs/snapshot abstractions and optional block AST resolver.
- edge_cases_or_failure_modes: Handles CRLF/BOM normalization, fuzzy landing, duplicate prefix/suffix echoes, dropped closers, stale session snapshots, same-path section merging, and partial streaming patches.
- validation_or_tests: Covered by hashline package tests and by coding-agent edit-diff/tool tests that consume patch behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-169 `file` `crates/pi-natives/build.rs`
- cursor: `[_]`
- core_role: Native crate build script that prepares N-API metadata and bundled shell-minimizer filter definitions.
- algorithmic_behavior: Calls `napi_build::setup()`, reads minimizer TOML files, strips duplicate `schema_version`, concatenates them into `OUT_DIR/builtin_filters.toml`, and emits Cargo rerun directives.
- inputs_outputs_state: Inputs are filter TOML files and Cargo build env; output is generated built-in filter bundle in `OUT_DIR`.
- gates_or_invariants: Build fails if filter files cannot be read or output cannot be written; duplicate schema lines are intentionally removed before concatenation.
- dependencies_and_callers: Used by `crates/pi-natives` build; consumed by runtime shell minimizer native code.
- edge_cases_or_failure_modes: Missing filters or malformed build paths break compilation; stale rerun directives would miss changes, so each source is registered.
- validation_or_tests: Validated by native crate compilation and smoke tests using pi-natives.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-199 `file` `docs/tools/retain.md`
- cursor: `[_]`
- core_role: Runtime contract documentation for the `retain` memory tool.
- algorithmic_behavior: Defines tool sources/collaborators, input schema, output shape, flow, memory scoping modes, side effects, limits, and error behavior.
- inputs_outputs_state: Inputs are memory text, optional scope/context/mode; outputs are retention confirmations, stored memory records, and backend side effects.
- gates_or_invariants: Scoping and backend availability determine storage target; failures are expected to surface as tool errors rather than silent drops.
- dependencies_and_callers: Documents coding-agent memory tool behavior and Mnemopi/Hindsight backend interactions.
- edge_cases_or_failure_modes: Covers backend unavailability, oversized/ambiguous input, and scoping surprises.
- validation_or_tests: Cross-referenced by `packages/coding-agent/test/memory-tools.test.ts`.
- skip_candidate: `yes: documentation-only, but it is assigned because it defines the retain tool contract`

### OH_MY_HUMANIZE_MAIN-HZ-229 `directory` `packages/agent/src/utils`
- cursor: `[_]`
- core_role: Agent-runtime utility directory; currently contains yield/backoff utilities for cooperative async loops.
- algorithmic_behavior: `yield.ts` exposes an `ExponentialYield` pattern used to avoid busy waiting while racing async work.
- inputs_outputs_state: Inputs are promises/loop progress; outputs are delayed/raced continuations. State is per-yield instance backoff counters.
- gates_or_invariants: Backoff should yield frequently enough for responsiveness without hot loops.
- dependencies_and_callers: Imported by coding-agent executor paths such as `bash-executor.ts`.
- edge_cases_or_failure_modes: Incorrect yield timing can starve cancellation or waste CPU.
- validation_or_tests: Covered indirectly by executor cancellation/timeout tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-259 `directory` `packages/coding-agent/src/eval`
- cursor: `[_]`
- core_role: Evaluation runtime subsystem for JS/Python execution, completion bridge, agent bridge, budget bridge, timeout control, and worker transport.
- algorithmic_behavior: `agent-bridge.ts` validates agent-eval permissions and launches subprocess agents; `completion-bridge.ts` resolves model/API key/schema and parses structured outputs; `idle-timeout.ts` implements pauseable abort timers; JS runtime rewrites imports, loads local modules, wraps code, captures display values; Python kernel/runner/tool bridge provide analogous execution.
- inputs_outputs_state: Inputs are eval code, model/completion args, session context, timeout/budget, and tool bridge calls; outputs are displays, structured values, errors, usage/budget readings, and subprocess artifacts.
- gates_or_invariants: Blocks nested eval-session deadlocks, depth overruns, plan-mode agent spawning, missing API keys, timed-out bridges, invalid schemas, and disabled agent bridge features.
- dependencies_and_callers: Used by `eval` tool and browser tool JS execution; depends on Bun workers, local-module loader, Python runner, model registry, and session tool bridge.
- edge_cases_or_failure_modes: Worker spawn failures, import rewrite misses, timeout pause/resume leaks, schema tool fallback failures, and parent/child eval session deadlocks.
- validation_or_tests: Directory includes `__tests__` for agent/completion/budget/idle/kernel/js context and assigned `bridge-timeout.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-289 `directory` `packages/coding-agent/src/utils`
- cursor: `[_]`
- core_role: Shared coding-agent utility directory for git/jj operations, file/display mode, archive handling, images, shell snapshots, clipboard/editor integration, event bus, block context, and model/tool helpers.
- algorithmic_behavior: Includes `git.ts` command API with repo locks/ref resolution/diff/status/stage/commit/push/worktree/stash operations; `block-context.ts` mixes native AST and lexical bracket context; `zip.ts` reads/writes zip/tar archives; image utilities normalize/resize/load and handle WebP exclusions; shell snapshot caches interactive shell env startup.
- inputs_outputs_state: Inputs vary by utility: repo paths, files, images, terminal text, archives, env, model metadata; outputs are normalized paths, command results, diagnostics, archive entries, image payloads, and cached snapshot paths.
- gates_or_invariants: Git writes are serialized per repo, image size/type limits are enforced, block context truncates/normalizes text, archive parsers validate central directory/member bounds, and editor/open helpers respect platform differences.
- dependencies_and_callers: Used across tools, TUI, session management, command execution, and commit workflows.
- edge_cases_or_failure_modes: Reftable refs, detached heads, WSL path opening, non-UTF image/archive metadata, too-large images, shell startup failures, and Unicode width handling.
- validation_or_tests: Covered by focused tests such as external-editor, input paste, edit mode/rendering, git-dependent integration tests, and archive/read consumers.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-319 `directory` `packages/coding-agent/test/web`
- cursor: `[_]`
- core_role: Web-search/scraper provider contract tests for request shaping, auth, rendering, provider chains, aborts, and timeouts.
- algorithmic_behavior: Recursively covers `test/web/search/*`; tests exercise Anthropic broker request bodies, Tavily, Perplexity OAuth/API/anonymous paths, Codex broker auth, provider-chain selection, result rendering, and hard timeout/abort propagation.
- inputs_outputs_state: Inputs are mocked provider settings, query strings, fetch responses, and abort signals; outputs are normalized search results, rendered markdown, or expected errors.
- gates_or_invariants: Provider-specific auth headers/body shape must match contracts; timeout and abort must propagate; provider chain must skip unavailable providers and preserve result ordering.
- dependencies_and_callers: Tests coding-agent web search providers and renderer code.
- edge_cases_or_failure_modes: Missing credentials, anonymous fallback, slow providers, aborted fetch, malformed responses, and rendering empty snippets.
- validation_or_tests: This item is itself the validation surface.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-349 `file` `crates/pi-iso/src/zfs.rs`
- cursor: `[_]`
- core_role: ZFS-backed filesystem isolation backend for snapshot/clone workspaces.
- algorithmic_behavior: Dispatches backend availability, snapshots a source dataset, clones a sibling dataset at a mountpoint, and destroys clone/origin on stop while verifying ownership.
- inputs_outputs_state: Inputs are source path/dataset, clone name, mountpoint, and backend mode; outputs are clone dataset/mount state and cleanup actions.
- gates_or_invariants: Refuses unknown/unrelated datasets, cleans up partial clone creation, and only destroys clones it created.
- dependencies_and_callers: Depends on Unix ZFS commands and isolation orchestration.
- edge_cases_or_failure_modes: Missing dataset, stale clone collision, failed mountpoint setup, or cleanup command failure.
- validation_or_tests: Validated through crate integration/smoke behavior on ZFS-capable hosts.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-379 `file` `crates/pi-shell/src/fixup.rs`
- cursor: `[_]`
- core_role: AST-driven shell command fixup layer for safer/cleaner bash execution.
- algorithmic_behavior: `apply_bash_fixups` skips multiline/parse-error commands, strips safe trailing `head`/`tail` from pipelines, removes redundant `2>&1`, and uses char-to-byte offset mapping for edits.
- inputs_outputs_state: Input is a shell command string; output is a rewritten command plus metadata. State is parser AST and planned edits.
- gates_or_invariants: Only safe simple patterns are stripped; multiline and unparseable commands are left unchanged; redirects are removed only when redundant.
- dependencies_and_callers: Used by pi-shell/native execution and coding-agent bash executor.
- edge_cases_or_failure_modes: Unicode byte offsets, complex pipelines, unsafe args, and parse failures are guarded.
- validation_or_tests: Rust tests in pi-shell cover pipeline/head/tail/redirection cases.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-409 `file` `packages/agent/test/remote-compaction.test.ts`
- cursor: `[_]`
- core_role: Contract tests for remote OpenAI-native compaction history building and failure handling.
- algorithmic_behavior: Tests custom tool call conversion, call-id tracking, input trimming, abort propagation, timeout behavior, and `compact()` fallback on remote failure.
- inputs_outputs_state: Inputs are synthetic agent histories, tool calls/results, abort signals, and mocked remote responses; outputs are compacted messages or surfaced failures.
- gates_or_invariants: Tool call IDs must remain correlated; oversized inputs are trimmed; abort/timeout must reject without corrupting local context.
- dependencies_and_callers: Tests agent compaction code that integrates with remote OpenAI-compatible endpoints.
- edge_cases_or_failure_modes: Missing tool result, duplicate IDs, aborted request, slow response, and remote errors.
- validation_or_tests: This file is the validation surface; describe blocks begin at lines 30, 170, 206, 234, 266, and 291.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-439 `file` `packages/ai/test/anthropic-fable-request-shaping.test.ts`
- cursor: `[_]`
- core_role: Request-shaping tests for Anthropic-compatible Fable/Mythos/MiniMax variants.
- algorithmic_behavior: Verifies forced `tool_choice` behavior for Fable/Mythos, adaptive-only thinking disablement, and MiniMax Anthropic thinking handling.
- inputs_outputs_state: Inputs are model/provider descriptors and request contexts; outputs are HTTP request bodies sent to mocked fetch.
- gates_or_invariants: Thinking/tool-choice fields must be included or omitted according to provider/model capabilities.
- dependencies_and_callers: Tests `packages/ai` Anthropic dialect/provider request builder.
- edge_cases_or_failure_modes: Unsupported thinking config, adaptive-only settings, and forced tool use on incompatible models.
- validation_or_tests: Describe blocks at lines 82, 105, and 122.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-469 `file` `packages/ai/test/auth-gateway-pi-native.test.ts`
- cursor: `[_]`
- core_role: Tests canonical pi-native auth gateway request parsing, stream encoding, and error formatting.
- algorithmic_behavior: Exercises `parseRequest` validation for model/context/options, `encodeStream` SSE canonicalization/cancellation/error behavior, and `formatError` output.
- inputs_outputs_state: Inputs are JSON request bodies and async event iterators; outputs are parsed request objects and SSE frames.
- gates_or_invariants: Only allow-listed options pass; stream defaults are normalized; malformed model/context payloads reject.
- dependencies_and_callers: Tests `packages/ai/src/providers/pi-native-server.ts`.
- edge_cases_or_failure_modes: Unknown option keys, cancellation mid-stream, iterator errors, and non-Error thrown values.
- validation_or_tests: Describe blocks at lines 68, 184, and 273.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-499 `file` `packages/ai/test/deepseek-reasoning-content.test.ts`
- cursor: `[_]`
- core_role: Regression tests for DeepSeek reasoning content replay around tool calls.
- algorithmic_behavior: Ensures `reasoning_content` is preserved/mapped correctly when tool calls are replayed through OpenAI-family streaming/message conversion.
- inputs_outputs_state: Inputs are simulated DeepSeek streaming/message chunks with reasoning and tool calls; outputs are normalized assistant messages.
- gates_or_invariants: Reasoning content must not be lost or duplicated, and tool-call replay must keep call/result alignment.
- dependencies_and_callers: Tests AI OpenAI-compatible dialect handling.
- edge_cases_or_failure_modes: Empty reasoning chunks, interleaved tool call deltas, and replay after tool result.
- validation_or_tests: Describe block at line 66.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-529 `file` `packages/ai/test/inband-tools.test.ts`
- cursor: `[_]`
- core_role: Tests XML/in-band tool dialect parsing and rendering.
- algorithmic_behavior: Feeds in-band tool text through dialect scanners and asserts tool invocation extraction, parameter handling, transcript rendering, and malformed tag behavior.
- inputs_outputs_state: Inputs are model text streams containing XML-like tags; outputs are assistant content/tool call structures.
- gates_or_invariants: Tags must be complete and well-scoped before invocation; partial/malformed content remains text or errors predictably.
- dependencies_and_callers: Tests Anthropic/in-band dialect implementation.
- edge_cases_or_failure_modes: Nested/partial tags, invalid parameters, thinking sections, and final cleanup.
- validation_or_tests: Describe block at line 98.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-559 `file` `packages/ai/test/kagi-login.test.ts`
- cursor: `[_]`
- core_role: Provider login test for Kagi credential collection.
- algorithmic_behavior: Exercises login callback/prompt behavior and resulting credential serialization.
- inputs_outputs_state: Inputs are mocked login callbacks; output is credential/token value.
- gates_or_invariants: Login requires expected callback and returns the entered credential without silent mutation.
- dependencies_and_callers: Tests Kagi provider registry login flow.
- edge_cases_or_failure_modes: Missing callback or empty credential paths.
- validation_or_tests: Describe block at line 4.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-589 `file` `packages/ai/test/openai-first-event-timeout.test.ts`
- cursor: `[_]`
- core_role: Tests first-event and idle timeout behavior for OpenAI-family streaming.
- algorithmic_behavior: Simulates delayed/empty/active streams and asserts first-event timeout, idle timeout, terminal grace, and semantic progress handling.
- inputs_outputs_state: Inputs are async iterators/fetch streams and timeout settings; outputs are yielded chunks or timeout errors.
- gates_or_invariants: First event must arrive within configured deadline unless disabled; progress resets idle watchdog; terminal chunks enter grace handling.
- dependencies_and_callers: Tests `idle-iterator.ts` and OpenAI provider stream consumption.
- edge_cases_or_failure_modes: Never-yielding iterator, terminal chunk silence, abort races, and upstream close.
- validation_or_tests: Describe block at line 334.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-619 `file` `packages/ai/test/remote-auth-store.test.ts`
- cursor: `[_]`
- core_role: Auth storage integration tests for remote credential store behavior.
- algorithmic_behavior: Validates credential retrieval/persistence/rotation through `RemoteAuthCredentialStore` and `AuthStorage`.
- inputs_outputs_state: Inputs are provider IDs and stored credential payloads; outputs are active credentials and storage mutations.
- gates_or_invariants: Provider credentials must be found consistently and rotation must not leak stale values.
- dependencies_and_callers: Tests AI auth storage integration used by coding-agent model registry.
- edge_cases_or_failure_modes: Missing credentials, multiple accounts, and stale storage snapshots.
- validation_or_tests: Describe block at line 17.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-649 `file` `packages/ai/test/wafer.live.ts`
- cursor: `[_]`
- core_role: Live/provider probe for Wafer AI integration.
- algorithmic_behavior: Exercises real or environment-gated Wafer provider request path and validates completion/stream behavior.
- inputs_outputs_state: Inputs are Wafer credentials/env and model request; outputs are live completion events.
- gates_or_invariants: Runs only when live env is available; provider must conform to common AI client event shape.
- dependencies_and_callers: Tests Wafer registry/provider integration.
- edge_cases_or_failure_modes: Missing env, network/auth failure, and provider schema drift.
- validation_or_tests: Live test file itself.
- skip_candidate: `yes: live integration probe, not a deterministic core algorithm test`

### OH_MY_HUMANIZE_MAIN-HZ-679 `file` `packages/catalog/test/github-copilot-model-limits.test.ts`
- cursor: `[_]`
- core_role: Model catalog tests for GitHub Copilot model context/output limit mapping.
- algorithmic_behavior: Validates limit mapping and tiered context window derivation for Copilot models.
- inputs_outputs_state: Inputs are model IDs/catalog entries; outputs are resolved limit metadata.
- gates_or_invariants: Known Copilot model IDs must map to expected limits and tier classifications.
- dependencies_and_callers: Tests catalog provider/resolver code used by model selection.
- edge_cases_or_failure_modes: New upstream model IDs, tier suffix changes, and default-limit fallback.
- validation_or_tests: Describe blocks at lines 60 and 362.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-709 `file` `packages/catalog/test/wafer.test.ts`
- cursor: `[_]`
- core_role: Catalog tests for Wafer Pass, Wafer Serverless, and dynamic discovery mapping.
- algorithmic_behavior: Verifies provider descriptors, default models, discovered model normalization, and mapper behavior.
- inputs_outputs_state: Inputs are Wafer provider catalog/discovery payloads; outputs are normalized catalog model entries.
- gates_or_invariants: Provider-specific IDs and pricing/limits must be mapped consistently.
- dependencies_and_callers: Tests catalog Wafer descriptor/resolver logic.
- edge_cases_or_failure_modes: Missing metadata, serverless/pass differences, and discovery schema drift.
- validation_or_tests: Describe blocks at lines 32, 88, and 155.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-739 `file` `packages/coding-agent/test/acp-client-bridge.test.ts`
- cursor: `[_]`
- core_role: Tests ACP client bridge permission request conversion.
- algorithmic_behavior: Verifies bridge maps ACP permission prompts into coding-agent approval/request behavior.
- inputs_outputs_state: Inputs are ACP client permission messages; outputs are bridge decisions/responses.
- gates_or_invariants: Permission prompts must not be dropped or misclassified.
- dependencies_and_callers: Tests ACP client bridge in coding-agent.
- edge_cases_or_failure_modes: Unknown permission kind and missing request fields.
- validation_or_tests: Describe block at line 5.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-769 `file` `packages/coding-agent/test/agent-session-manual-retry.test.ts`
- cursor: `[_]`
- core_role: Regression tests for manual retry behavior in agent sessions.
- algorithmic_behavior: Exercises retry state transitions after failed/aborted assistant turns and verifies message reconstruction.
- inputs_outputs_state: Inputs are synthetic session messages and retry triggers; outputs are updated session history and retry attempts.
- gates_or_invariants: Manual retry must not duplicate permanent messages or lose retry context.
- dependencies_and_callers: Tests coding-agent `AgentSession` retry logic.
- edge_cases_or_failure_modes: Aborted turn, failed tool call, and retry after partial stream.
- validation_or_tests: Describe block at line 22.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-799 `file` `packages/coding-agent/test/auth-storage-rotation.test.ts`
- cursor: `[_]`
- core_role: Tests account rotation in coding-agent auth storage.
- algorithmic_behavior: Ensures credential account selection rotates/updates active accounts correctly.
- inputs_outputs_state: Inputs are multiple provider credentials/accounts; outputs are selected active credential state.
- gates_or_invariants: Rotation must not erase unrelated providers and must update active account deterministically.
- dependencies_and_callers: Tests SDK auth storage/model registry usage.
- edge_cases_or_failure_modes: Missing active account, removed account, and duplicate account keys.
- validation_or_tests: Describe block at line 11.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-829 `file` `packages/coding-agent/test/commit-shared-llm.test.ts`
- cursor: `[_]`
- core_role: Tests shared LLM response parsing for commit analysis tooling.
- algorithmic_behavior: Verifies tool-call/text parsing converts model responses into conventional commit analysis payloads.
- inputs_outputs_state: Inputs are mocked assistant messages; outputs are parsed commit metadata.
- gates_or_invariants: Tool-call responses must take precedence and malformed payloads must fail predictably.
- dependencies_and_callers: Tests `commit/shared-llm` helpers used by commit analysis.
- edge_cases_or_failure_modes: Text fallback, missing fields, and invalid tool schema.
- validation_or_tests: Describe block at line 8.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-859 `file` `packages/coding-agent/test/external-editor.test.ts`
- cursor: `[_]`
- core_role: Tests external editor command resolution.
- algorithmic_behavior: Validates `$EDITOR`/platform command parsing into executable plus args.
- inputs_outputs_state: Inputs are env variables and platform assumptions; outputs are editor command descriptors.
- gates_or_invariants: Empty env must fall back safely; quoted args should parse as expected.
- dependencies_and_callers: Tests `utils/external-editor.ts`.
- edge_cases_or_failure_modes: Missing editor, whitespace/quoted command values, and platform-specific defaults.
- validation_or_tests: Describe block at line 12.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-889 `file` `packages/coding-agent/test/input-controller-large-paste.test.ts`
- cursor: `[_]`
- core_role: Tests large-paste gating and menu actions in input controller.
- algorithmic_behavior: Exercises size threshold detection, menu action dispatch, and file attachment behavior for large pasted text.
- inputs_outputs_state: Inputs are pasted text and mocked UI/menu/session state; outputs are editor changes, attachments, or prompt decisions.
- gates_or_invariants: Large paste must ask before insertion/attachment and cancel cleanly.
- dependencies_and_callers: Tests interactive input controller and paste handling.
- edge_cases_or_failure_modes: Very large text, menu cancellation, attach-to-file path, and repeated paste.
- validation_or_tests: Describe blocks at lines 42, 68, and 115.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-919 `file` `packages/coding-agent/test/issue-2750-subagent-runtime-fallback.test.ts`
- cursor: `[_]`
- core_role: Regression tests for subagent runtime model fallback.
- algorithmic_behavior: Ensures subagent spawning resolves fallback models when requested runtime model is unavailable.
- inputs_outputs_state: Inputs are model registry state and subagent requests; outputs are chosen model/runtime config.
- gates_or_invariants: Fallback must preserve task execution without selecting an unauthenticated/unavailable model.
- dependencies_and_callers: Tests task/subagent runtime model selection.
- edge_cases_or_failure_modes: Missing primary model, unavailable API key, and default fallback ordering.
- validation_or_tests: Describe block at line 63.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-949 `file` `packages/coding-agent/test/lm-studio-fix.test.ts`
- cursor: `[_]`
- core_role: Tests LM Studio model registry fixes.
- algorithmic_behavior: Validates registry/model resolution behavior for LM Studio-specific model IDs and endpoints.
- inputs_outputs_state: Inputs are LM Studio provider config/model entries; outputs are normalized available models.
- gates_or_invariants: Local provider models must not be misclassified or hidden by catalog defaults.
- dependencies_and_callers: Tests `ModelRegistry` provider handling.
- edge_cases_or_failure_modes: Empty discovery, local base URL, and model ID aliases.
- validation_or_tests: Describe block at line 10.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-979 `file` `packages/coding-agent/test/memory-tools.test.ts`
- cursor: `[_]`
- core_role: Comprehensive tests for retain/recall/reflect/memory_edit tools across Hindsight and Mnemopi backends.
- algorithmic_behavior: Exercises tool factories, retain execution, Mnemopi lifecycle, recall queries, memory edits, and reflection behavior.
- inputs_outputs_state: Inputs are tool params, mocked memory backends, session settings, and query text; outputs are tool results, backend writes/reads, and rendered summaries.
- gates_or_invariants: Backend availability, scoping, validation, and errors must map to observable tool results.
- dependencies_and_callers: Tests coding-agent memory tool implementations and Mnemopi adapter.
- edge_cases_or_failure_modes: Backend disabled, invalid inputs, empty recall, edit failures, lifecycle start/stop, and cross-backend behavior differences.
- validation_or_tests: Describe blocks at lines 180, 208, 248, 336, 433, 803, 871, 992, 1104, and 1145.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1009 `file` `packages/coding-agent/test/prompt-templates.test.ts`
- cursor: `[_]`
- core_role: Tests slash prompt template argument parsing/substitution.
- algorithmic_behavior: Validates `substituteArgs`, `parseCommandArgs`, integration behavior, and template expansion fallback.
- inputs_outputs_state: Inputs are template strings and command argument text; outputs are substituted prompt text and parsed arg arrays.
- gates_or_invariants: Quoting/escaping/defaults must be deterministic; fallback must produce usable prompt expansion.
- dependencies_and_callers: Tests custom prompt command/template utilities.
- edge_cases_or_failure_modes: Missing args, quoted spaces, escapes, and malformed template placeholders.
- validation_or_tests: Describe blocks at lines 20, 149, 205, and 236.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1039 `file` `packages/coding-agent/test/sdk-model-selection.test.ts`
- cursor: `[_]`
- core_role: Tests deferred model-pattern resolution in SDK session creation.
- algorithmic_behavior: Ensures `createAgentSession` resolves model patterns against registry only when needed and selects expected model/API key.
- inputs_outputs_state: Inputs are SDK options, model patterns, and mocked registry availability; outputs are session model selection.
- gates_or_invariants: Deferred resolution must honor unavailable models and not eagerly fail when later context resolves.
- dependencies_and_callers: Tests coding-agent SDK session creation.
- edge_cases_or_failure_modes: Ambiguous patterns, missing credentials, and default model fallback.
- validation_or_tests: Describe block at line 13.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1069 `file` `packages/coding-agent/test/startup-import-graph.test.ts`
- cursor: `[_]`
- core_role: Startup import graph regression test.
- algorithmic_behavior: Asserts selected startup modules do not eagerly import heavyweight/runtime-sensitive modules.
- inputs_outputs_state: Inputs are module graph/import text; outputs are pass/fail import graph assertions.
- gates_or_invariants: Startup path must avoid prohibited imports to keep CLI startup fast and side-effect-light.
- dependencies_and_callers: Tests coding-agent entry/startup module boundaries.
- edge_cases_or_failure_modes: Accidental barrel import expansion and hidden heavy dependency pull-in.
- validation_or_tests: Describe block at line 6.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1099 `file` `packages/coding-agent/test/theme-epoch-fallback.test.ts`
- cursor: `[_]`
- core_role: Tests theme epoch fallback behavior.
- algorithmic_behavior: Verifies `setTheme` fallback when theme epoch/current theme state is missing or invalid.
- inputs_outputs_state: Inputs are theme settings/state; outputs are selected theme and success/error result.
- gates_or_invariants: Invalid theme state should not crash TUI initialization.
- dependencies_and_callers: Tests theme manager.
- edge_cases_or_failure_modes: Missing theme files and stale epoch metadata.
- validation_or_tests: Describe block at line 17.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1129 `file` `packages/coding-agent/test/xiaomi-tp-discovery-merge.test.ts`
- cursor: `[_]`
- core_role: Tests discovered model merge behavior for Xiaomi TP/provider discovery.
- algorithmic_behavior: Validates merging discovered model metadata into existing registry entries without losing known fields.
- inputs_outputs_state: Inputs are base model entries and discovery payloads; outputs are merged model descriptors.
- gates_or_invariants: Discovery must update dynamic fields while preserving configured metadata.
- dependencies_and_callers: Tests model discovery/registry merge logic.
- edge_cases_or_failure_modes: Duplicate IDs, missing limits, provider-specific overrides.
- validation_or_tests: Describe block at line 32.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1159 `file` `packages/hashline/src/tokenizer.ts`
- cursor: `[_]`
- core_role: Tokenizer for the hashline patch language.
- algorithmic_behavior: Splits lines/cursors, scans ranges, unions block targets, parses hunk/header lines, classifies body tokens, and exposes a stateful `Tokenizer`.
- inputs_outputs_state: Inputs are raw patch text and split options; outputs are token stream with cursor/range metadata.
- gates_or_invariants: Range/header parsing must be strict enough to avoid ambiguous edits; cursor cloning keeps positions stable.
- dependencies_and_callers: Called by `parser.ts` and streaming patch flows.
- edge_cases_or_failure_modes: Partial hunks, ambiguous headers, block target boundaries, and malformed ranges.
- validation_or_tests: Covered by hashline parser/apply tests and coding-agent edit tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1189 `file` `packages/mnemopi/test/c25-deltasync-allowlist.test.ts`
- cursor: `[_]`
- core_role: Tests DeltaSync table/column allowlist and checkpoint compatibility.
- algorithmic_behavior: Verifies C25 synchronization only permits allowed tables/columns and handles checkpoint formats.
- inputs_outputs_state: Inputs are test SQLite/state rows and sync allowlist config; outputs are accepted/rejected sync records and checkpoints.
- gates_or_invariants: Non-allowlisted data must not sync; checkpoint compatibility must preserve migration continuity.
- dependencies_and_callers: Tests Mnemopi DeltaSync migration/sync code.
- edge_cases_or_failure_modes: Unknown tables, extra columns, stale checkpoint schema.
- validation_or_tests: Describe blocks at lines 32, 81, and 193.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1219 `file` `packages/mnemopi/test/optional-embeddings.test.ts`
- cursor: `[_]`
- core_role: Tests optional embedding dependency behavior.
- algorithmic_behavior: Exercises memory flows when embeddings are available, unavailable, or explicitly disabled.
- inputs_outputs_state: Inputs are embedding config and mocked dependencies; outputs are memory records/query behavior with or without vectors.
- gates_or_invariants: Missing optional embedding stack must not break non-vector memory functionality.
- dependencies_and_callers: Tests Mnemopi core storage/query behavior.
- edge_cases_or_failure_modes: Import failure, disabled embeddings, and fallback ranking.
- validation_or_tests: Describe block at line 87.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1249 `file` `packages/natives/native/index.js`
- cursor: `[_]`
- core_role: JavaScript loader/export surface for the native `pi-natives` addon.
- algorithmic_behavior: Loads the native binding, exports generated functions/classes/constants, and exposes fs scan cache invalidation and version sentinel.
- inputs_outputs_state: Inputs are runtime platform/native package resolution; outputs are JS-callable native functions.
- gates_or_invariants: Native addon must load successfully and version sentinel must match release expectations.
- dependencies_and_callers: Consumed by coding-agent, pi-shell, pi-ast, and native utilities.
- edge_cases_or_failure_modes: Missing binary, ABI mismatch, stale sentinel, or missing generated export.
- validation_or_tests: Covered by native smoke/import tests and release sentinel bump in `scripts/release.ts`.
- skip_candidate: `yes: generated/native binding surface, but it defines runtime export availability`

### OH_MY_HUMANIZE_MAIN-HZ-1279 `file` `packages/snapcompact/research/exp07_readtax.py`
- cursor: `[_]`
- core_role: Research experiment script for snapcompact read-tax evaluation.
- algorithmic_behavior: Builds image chunks, probes minimum effort, calls models, runs condition cells, aggregates latency/cost/accuracy records, and writes CSV/JSON experiment output.
- inputs_outputs_state: Inputs are SQuAD/sample data, API keys, model/condition args, and pricing config; outputs are per-cell records and aggregate metrics.
- gates_or_invariants: Requires keys/model availability; limits chunk sizes and records timing/cost consistently.
- dependencies_and_callers: Depends on Python, PIL/image utilities, SQuAD helper module, and model API calls.
- edge_cases_or_failure_modes: Missing keys, failed model call, image generation failure, and inconsistent records.
- validation_or_tests: Research script has no assigned automated test.
- skip_candidate: `yes: research experiment, not shipped runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-1309 `file` `packages/snapcompact/research/snapcompact_convergence_3d.py`
- cursor: `[_]`
- core_role: Research visualization script for 3D convergence paths.
- algorithmic_behavior: Loads arrays, centers/smooths paths, maps question hues, renders strands to a PIL image/matplotlib output.
- inputs_outputs_state: Inputs are JSON/NumPy experiment arrays and CLI args; output is rendered convergence visualization.
- gates_or_invariants: Expects compatible array shapes and available fonts/rendering backend.
- dependencies_and_callers: Depends on NumPy, Matplotlib, PIL, and snapcompact experiment artifacts.
- edge_cases_or_failure_modes: Missing arrays, shape mismatch, font fallback, and rendering backend issues.
- validation_or_tests: No direct test; used as research artifact generation.
- skip_candidate: `yes: visualization research script`

### OH_MY_HUMANIZE_MAIN-HZ-1339 `file` `packages/snapcompact/research/snapcompact_viz_waterfall.py`
- cursor: `[_]`
- core_role: Research visualization script for snapcompact waterfall metrics.
- algorithmic_behavior: Smooths metric rows, normalizes robust units, loads summary/arrays, builds waterfall data, draws glow lines and annotated multi-panel plot.
- inputs_outputs_state: Inputs are experiment summary and arrays; output is plotted waterfall figure.
- gates_or_invariants: Data keys/array dimensions must match expected schema; normalization clamps by robust high percentile.
- dependencies_and_callers: Depends on NumPy and Matplotlib.
- edge_cases_or_failure_modes: Missing source data, empty arrays, and plotting failures.
- validation_or_tests: No direct test; research output validation is visual/manual.
- skip_candidate: `yes: visualization research script`

### OH_MY_HUMANIZE_MAIN-HZ-1369 `file` `packages/tui/src/bracketed-paste.ts`
- cursor: `[_]`
- core_role: Terminal bracketed-paste parser and control-sequence decoder.
- algorithmic_behavior: Detects paste start/end markers, accumulates content across chunks, decodes re-encoded Ctrl CSI-u/xterm sequences, and returns handled/remaining text.
- inputs_outputs_state: Inputs are terminal input strings; outputs are paste content plus remaining unconsumed input. State is active paste buffer.
- gates_or_invariants: Only content between `\x1b[200~` and `\x1b[201~` is paste; incomplete paste remains buffered.
- dependencies_and_callers: Used by TUI input controller/editor paste handling.
- edge_cases_or_failure_modes: Split markers across chunks, embedded control bytes, cancellation, and multiple pastes in one input.
- validation_or_tests: Covered by paste/input controller tests and TUI text/input tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1399 `file` `packages/tui/test/focus-menu-regression.test.ts`
- cursor: `[_]`
- core_role: Regression test for focus-changing menu teardown.
- algorithmic_behavior: Exercises menu focus transitions and verifies teardown/removal does not leave stale focus state.
- inputs_outputs_state: Inputs are synthetic focus/menu operations; outputs are TUI focus/container state assertions.
- gates_or_invariants: Focus target must remain valid after menu closes.
- dependencies_and_callers: Tests TUI menu/focus management.
- edge_cases_or_failure_modes: Closing a focused menu while focus changes.
- validation_or_tests: Describe block at line 41.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1429 `file` `packages/tui/test/notifications.test.ts`
- cursor: `[_]`
- core_role: Tests terminal notification behavior.
- algorithmic_behavior: Verifies notification rendering/emission based on terminal support/config.
- inputs_outputs_state: Inputs are notification options and mocked terminal environment; outputs are emitted escape sequences or suppressed events.
- gates_or_invariants: Unsupported/disabled notifications should not emit.
- dependencies_and_callers: Tests TUI notification utilities.
- edge_cases_or_failure_modes: Missing env, unsupported terminal, and repeated notification.
- validation_or_tests: Describe block at line 62.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1459 `file` `packages/tui/test/text-utils.test.ts`
- cursor: `[_]`
- core_role: Tests text measurement/truncation/wrapping utilities.
- algorithmic_behavior: Validates visible width handling, truncation, ANSI-aware behavior, and text transformations.
- inputs_outputs_state: Inputs are plain/ANSI/Unicode strings and width limits; outputs are formatted strings and measured widths.
- gates_or_invariants: Width functions must not split visual cells incorrectly.
- dependencies_and_callers: Tests TUI text utilities used throughout coding-agent rendering.
- edge_cases_or_failure_modes: ANSI codes, wide Unicode, zero/negative widths, and truncation ellipsis.
- validation_or_tests: Describe block at line 10.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1489 `file` `packages/utils/src/frontmatter.ts`
- cursor: `[_]`
- core_role: YAML frontmatter parser/normalizer for utility consumers.
- algorithmic_behavior: Strips HTML comments, parses frontmatter with Bun YAML, normalizes kebab-case keys to camelCase, truncates error context, and returns body/data or throws `FrontmatterError`.
- inputs_outputs_state: Input is document content plus parser options; output is parsed metadata/body. No persistent state.
- gates_or_invariants: Frontmatter delimiters and YAML validity determine parse success; malformed data logs/throws according to options.
- dependencies_and_callers: Uses `bun:YAML`, utility logger, and format truncation; consumed by config/plugin/docs loaders.
- edge_cases_or_failure_modes: Missing closing delimiter, invalid YAML, non-object metadata, HTML comments before frontmatter.
- validation_or_tests: Utility tests cover env; frontmatter behavior likely covered by consumers.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1519 `file` `packages/utils/test/env.test.ts`
- cursor: `[_]`
- core_role: Tests environment parsing/filtering utilities.
- algorithmic_behavior: Validates `.env` parsing and process env filtering behavior.
- inputs_outputs_state: Inputs are env file text and process env objects; outputs are parsed key/value maps or filtered env.
- gates_or_invariants: Comments/quotes/empty values must parse consistently; filtered env must remove disallowed values.
- dependencies_and_callers: Tests `packages/utils` env helpers used across CLI.
- edge_cases_or_failure_modes: Quoted values, comments, blank lines, and inherited env leakage.
- validation_or_tests: Describe blocks at lines 23 and 54.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1549 `file` `python/robomp/src/autoclose.py`
- cursor: `[_]`
- core_role: Robomp autoclose scheduler for delayed issue/PR cleanup actions.
- algorithmic_behavior: `AutocloseScheduler` tracks scheduled close tasks, computes UTC timestamps, asynchronously sleeps/wakes, and runs close operations through configured GitHub/client hooks.
- inputs_outputs_state: Inputs are issue/PR identifiers, delay/config, and event loop; outputs are scheduled tasks and close attempts.
- gates_or_invariants: Tasks should be cancellable/idempotent and not close before configured delay.
- dependencies_and_callers: Used by robomp GitHub automation event handling.
- edge_cases_or_failure_modes: Restart loses in-memory tasks unless persisted elsewhere, GitHub close failure, task cancellation, and clock skew.
- validation_or_tests: Covered indirectly by robomp event route tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1579 `file` `python/robomp/tests/test_github_events.py`
- cursor: `[_]`
- core_role: Comprehensive tests for robomp GitHub webhook routing, auth, rate limits, maintainer directives, and bot filtering.
- algorithmic_behavior: Verifies signature checking, issue/PR/comment/review event routing, disallowed repo skipping, self/bot skipping, submitter capture, rate-limit caps, mention extraction, maintainer/authorizer logic, and directive parsing.
- inputs_outputs_state: Inputs are synthetic GitHub webhook payloads/headers/config; outputs are queued action calls, skip decisions, cleanup actions, and directive metadata.
- gates_or_invariants: Only allowed repos/users/events route; bots/self-comments are skipped except reviewer-bot directive cases; signatures must match.
- dependencies_and_callers: Tests robomp GitHub event router.
- edge_cases_or_failure_modes: Draft PRs, synchronized PRs, pull_request issues events, merged PR cleanup, case-insensitive logins, pragma stripping, and reviewer bot comments.
- validation_or_tests: Test functions span lines 19 through 841.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1609 `directory` `packages/coding-agent/src/commit/analysis`
- cursor: `[_]`
- core_role: Commit-message analysis subsystem for conventional commit type/scope/details/summary validation.
- algorithmic_behavior: `conventional.ts` renders static prompt templates and parses LLM tool response; `scope.ts` derives scope candidates from numstat path/line weights and wide-change heuristics; `summary.ts` asks LLM for a constrained summary and strips type prefixes; `validation.ts` validates scope and detail formatting.
- inputs_outputs_state: Inputs are model/API key, thinking level, diff/stat/context/recent commits, numstat, and user context; outputs are conventional analysis objects, scope suggestions, summary strings, and validation errors.
- gates_or_invariants: Prompts come from `.md` templates; scope is at most two lowercase segments; summary is single-line and bounded; detail text must end with periods and stay under 120 chars.
- dependencies_and_callers: Used by coding-agent commit flow; depends on `completeSimple`, commit prompt templates, shared LLM tool schema, and exclusions.
- edge_cases_or_failure_modes: Wide multi-component changes, rename path syntax, placeholder dirs, excluded files, malformed LLM output, and invalid summary prefix.
- validation_or_tests: Covered by `commit-shared-llm.test.ts` plus commit workflow tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1639 `directory` `packages/coding-agent/src/tools/browser`
- cursor: `[_]`
- core_role: Browser automation tool subsystem for acquiring browsers/tabs, running page actions/eval, extracting snapshots/readable text, rendering results, and cmux integration.
- algorithmic_behavior: `launch.ts` resolves/launches Chromium and injects stealth/user-agent patches; `attach.ts` finds reusable CDP ports/pages; `registry.ts` reference-counts browser handles; `tab-supervisor.ts` serializes tab sessions/workers; `tab-worker.ts` implements Puppeteer actions and AX/screenshot/eval handling; `cmux/*` maps cmux RPC snapshots/actions into the same run protocol.
- inputs_outputs_state: Inputs are browser kind/app/session, URL/action/eval/screenshot args, abort signals, and tool session; outputs are observations, screenshots, text/readable content, displays, or tool errors. State is browser handle map, tab map, worker inflight ops, and cached element refs.
- gates_or_invariants: CDP readiness timeout, actionability checks for clicks, screenshot format/path handling, release/kill refcounts, worker timeout, dialog policy, and redaction of URL credentials.
- dependencies_and_callers: Used by the `browser` tool, eval JS runtime, Puppeteer, cmux socket client, image resize, and TUI/collab renderers.
- edge_cases_or_failure_modes: Browser binary missing, stale CDP port, orphan target, page close during run, split worker initialization, cmux protocol errors, unreadable HTML, and screenshot path/format mismatch.
- validation_or_tests: Covered by browser/web tests and render tests; test hooks include `initializeTabWorkerForTest`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1669 `file` `crates/pi-shell/src/minimizer/engine.rs`
- cursor: `[_]`
- core_role: Shell output minimizer engine for compacting command output while preserving useful success/failure signals.
- algorithmic_behavior: Chooses `MinimizerMode`, applies max-capture and structural guards, dispatches filters, handles chain passthrough and identity mode, and labels pipeline/chain outputs.
- inputs_outputs_state: Inputs are command/output/filter config and captured bytes; outputs are minimized text plus metadata about filter, input bytes, and output bytes.
- gates_or_invariants: Refuses unsafe chain minimization when fd mutations or structural risks are present; success-visible guard avoids hiding important successful output.
- dependencies_and_callers: Consumed by pi-natives shell execution and coding-agent `bash-executor.ts`.
- edge_cases_or_failure_modes: Too-large captures, chained commands, pipelines, binary output, fd redirections, and no-op minimizer.
- validation_or_tests: Rust minimizer tests and coding-agent bash output tests cover behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1699 `file` `packages/ai/src/dialect/anthropic.ts`
- cursor: `[_]`
- core_role: Anthropic XML/in-band tool dialect scanner and renderer.
- algorithmic_behavior: Maintains scanner state for outside text, sections, invoke tags, parameters, and thinking; `feed`/`flush` consume streamed chunks and emit content/tool call events; rendering helpers serialize calls/results/transcripts.
- inputs_outputs_state: Inputs are streamed model text and tool dialect config; outputs are normalized assistant content, tool calls, thinking content, and transcript strings. State tracks current tag, parameter buffer, and invocation fields.
- gates_or_invariants: Only complete/valid tags become tool calls; malformed/partial tags flush as text or errors; state resets after final cleanup.
- dependencies_and_callers: Used by AI Anthropic-compatible providers and in-band tool tests.
- edge_cases_or_failure_modes: Split tags across chunks, nested thinking/invoke sections, invalid JSON-ish params, unknown tags, and trailing partial content.
- validation_or_tests: Covered by `inband-tools.test.ts` and Anthropic request-shaping tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1729 `file` `packages/ai/src/providers/aws-eventstream.ts`
- cursor: `[_]`
- core_role: AWS eventstream frame decoder for Bedrock-style streaming providers.
- algorithmic_behavior: Implements CRC32, validates total/header lengths and prelude/message CRCs, parses typed headers, and yields decoded messages across arbitrary stream chunk boundaries.
- inputs_outputs_state: Inputs are `ReadableStream<Uint8Array>` eventstream bytes; outputs are decoded headers/payload frames.
- gates_or_invariants: Invalid frame sizes or CRC mismatches throw; stream cancellation releases reader.
- dependencies_and_callers: Used by AWS/Bedrock provider code.
- edge_cases_or_failure_modes: Partial chunks, unknown header types, truncated frames, corrupt CRC, and cancellation.
- validation_or_tests: Provider tests cover streaming decode via AWS-compatible paths.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1759 `file` `packages/ai/src/providers/pi-native-server.ts`
- cursor: `[_]`
- core_role: Canonical pi-ai auth gateway server wire-format parser and SSE encoder.
- algorithmic_behavior: `parseRequest` validates model/modelId, context, allowed options, and stream default; `encodeStream` frames canonical events as SSE; `formatError` maps thrown values.
- inputs_outputs_state: Inputs are HTTP JSON body and event iterator; outputs are parsed completion request and encoded SSE byte stream.
- gates_or_invariants: Unknown option keys and malformed context/model shapes reject; cancellation and iterator errors emit best-effort terminal events.
- dependencies_and_callers: Used by pi-native auth gateway and tested by `auth-gateway-pi-native.test.ts`.
- edge_cases_or_failure_modes: Non-object JSON, missing model, bad stream flag, cancellation race, and thrown non-Error.
- validation_or_tests: Direct tests in assigned auth-gateway file.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1789 `file` `packages/ai/src/registry/kimi-code.ts`
- cursor: `[_]`
- core_role: Kimi Code provider registry definition.
- algorithmic_behavior: Defines provider ID/name and lazy login/refresh callbacks that import OAuth implementation on demand.
- inputs_outputs_state: Inputs are OAuth callbacks or refresh credentials; outputs are OAuth credentials from Kimi auth functions.
- gates_or_invariants: Lazy import keeps heavy OAuth modules out of eager registry graph; refresh requires `credentials.refresh`.
- dependencies_and_callers: Used by AI provider registry/model auth.
- edge_cases_or_failure_modes: Missing refresh token or OAuth module failure.
- validation_or_tests: Covered by provider registry/auth tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1819 `file` `packages/ai/src/registry/vllm.ts`
- cursor: `[_]`
- core_role: vLLM local OpenAI-compatible provider login definition.
- algorithmic_behavior: Prompts for optional API key, emits auth URL/instructions, returns default local token when empty, and aborts on signal after prompt.
- inputs_outputs_state: Inputs are OAuth login callbacks and optional signal; output is API key string.
- gates_or_invariants: Requires `onPrompt`; empty input maps to `vllm-local`.
- dependencies_and_callers: Used by provider registry/auth flows.
- edge_cases_or_failure_modes: Missing prompt callback and cancellation.
- validation_or_tests: Provider login behavior is covered by registry tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1849 `file` `packages/ai/src/utils/idle-iterator.ts`
- cursor: `[_]`
- core_role: Streaming iterator watchdog utilities for first-event, idle-timeout, and terminal grace behavior.
- algorithmic_behavior: Computes timeout env/config, arms pre-response timeout, races upstream iterator progress against first/idle timers, remints racers periodically, aborts on semantic inactivity, and optionally waits terminal grace after terminal chunk.
- inputs_outputs_state: Inputs are async iterables, timeout settings, progress predicate, and abort controller; outputs are yielded chunks or timeout/abort errors.
- gates_or_invariants: First event and idle deadlines must reset on progress; upstream close/return must be called; terminal grace should end after silence.
- dependencies_and_callers: Used by AI streaming providers, especially OpenAI-family streams.
- edge_cases_or_failure_modes: Never-yielding upstream, terminal chunk without close, abort race, and huge streams requiring racer refresh.
- validation_or_tests: Covered by `openai-first-event-timeout.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1879 `file` `packages/catalog/src/identity/equivalence.ts`
- cursor: `[_]`
- core_role: Canonical model identity equivalence/index builder for catalog deduplication and alias resolution.
- algorithmic_behavior: Builds reference data and suffix aliases, compiles overrides/exclusions, generates cheap/heavy heuristic candidates, strips markers/provider/date/version suffixes, normalizes Claude/Anthropic aliases, scores candidates with penalties, caches resolution, and builds canonical records/selector maps.
- inputs_outputs_state: Inputs are `Model<Api>` iterables, reference data, and equivalence config; outputs are canonical records, by-id map, and by-selector map. State includes bounded heuristic/suffix caches and weak resolution caches.
- gates_or_invariants: Overrides win, exclusions fallback to original ID, official IDs outrank heuristics, and candidate preference penalizes namespaced/date/provider/uppercase/marker forms.
- dependencies_and_callers: Used by catalog model manager/UI to group equivalent provider model IDs.
- edge_cases_or_failure_modes: Claude family latest/date aliases, `hf:` synthetic prefixes, compact minor versions, wrapper prefixes, namespace suffix ambiguity, and stale cache poisoning avoided by config/reference keyed caches.
- validation_or_tests: Covered by catalog identity/model limit tests and provider discovery tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1909 `file` `packages/coding-agent/src/autoresearch/helpers.ts`
- cursor: `[_]`
- core_role: Helper algorithms for autoresearch metric parsing, ASI metadata sanitization, path matching, formatting, and git probes.
- algorithmic_behavior: Parses `METRIC name=value` lines into finite numbers, parses `ASI key=value` lines into JSON/scalars, rejects prototype-pollution keys, merges/sanitizes ASI, formats numbers/time, kills process groups, compares metric direction, infers units, normalizes path specs, and best-effort reads git status/prefix.
- inputs_outputs_state: Inputs are subprocess output, ASI objects, paths, pids, and cwd; outputs are metric maps, sanitized ASI, formatted strings, match booleans, and git strings.
- gates_or_invariants: Denies `__proto__`, `constructor`, `prototype`; metrics must be finite; empty/invalid git probes return empty string.
- dependencies_and_callers: Used by autoresearch runners and dashboards; depends on `utils/git`.
- edge_cases_or_failure_modes: Malformed JSON values, Windows path separators, negative process group kill fallback, and invalid metric names.
- validation_or_tests: Covered by autoresearch feature tests if present; no assigned direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1939 `file` `packages/coding-agent/src/cli/completion-gen.ts`
- cursor: `[_]`
- core_role: Shell completion generator for bash, zsh, and fish.
- algorithmic_behavior: Builds a completion spec from CLI command metadata, classifies flag/arg value sources, generates per-shell handlers, static enum/list completions, and dynamic model/session completions via `__complete`.
- inputs_outputs_state: Inputs are CLI config, root command name, alias map, and shell kind; output is a complete shell script string.
- gates_or_invariants: Hidden commands excluded; boolean flags do not consume values; model/session/tool/path flags map to correct completion sources.
- dependencies_and_callers: Used by `omp completions`; depends on CLI descriptors and `BUILTIN_TOOL_NAMES`.
- edge_cases_or_failure_modes: Command aliases, repeatable flags, comma-list completion, fish positional limitations, zsh quoting, and file/dir completion modes.
- validation_or_tests: Completion tests likely cover generated strings; no assigned direct test.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1969 `file` `packages/coding-agent/src/collab/crypto.ts`
- cursor: `[_]`
- core_role: AES-GCM sealing/opening for collab relay frames.
- algorithmic_behavior: Generates random room keys/write tokens, imports AES-GCM key, seals JSON frames as `[12B IV][ciphertext+tag]`, opens sealed bytes, and copies subarrays into strict ArrayBuffers when needed.
- inputs_outputs_state: Inputs are raw room key bytes, collab frame objects, and sealed bytes; outputs are CryptoKey, sealed byte arrays, or parsed frames.
- gates_or_invariants: Room key byte length must equal `ROOM_KEY_BYTES`; sealed data must exceed IV length; auth failure throws.
- dependencies_and_callers: Depends on WebCrypto and `@oh-my-pi/pi-wire`; used by collab session/link protocol.
- edge_cases_or_failure_modes: Wrong key length, truncated frame, JSON parse failure, and AES auth failure.
- validation_or_tests: Covered by collab/steer queue and protocol tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1999 `file` `packages/coding-agent/src/commands/token.ts`
- cursor: `[_]`
- core_role: CLI command for retrieving provider API/OAuth credentials.
- algorithmic_behavior: Parses provider/raw/force-refresh args, discovers auth storage, resolves credential through model registry, lists configured providers on failure, optionally extracts nested JSON `.token`, and writes credential to stdout.
- inputs_outputs_state: Inputs are CLI args/flags and auth storage; outputs are stdout credential or stderr error plus nonzero exit code.
- gates_or_invariants: Provider must be authenticated; `--raw` disables JSON token extraction; force-refresh passes through to registry.
- dependencies_and_callers: Uses `PROVIDER_REGISTRY`, `ModelRegistry`, `discoverAuthStorage`, and CLI framework.
- edge_cases_or_failure_modes: Unknown provider, unauthenticated provider, nested JSON credential, refresh failure.
- validation_or_tests: Covered by slash/login/auth storage tests and command smoke behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2029 `file` `packages/coding-agent/src/dap/client.ts`
- cursor: `[_]`
- core_role: Debug Adapter Protocol client transport/state machine.
- algorithmic_behavior: Spawns stdio or socket-mode adapters, frames `Content-Length` JSON messages, tracks pending requests by seq, dispatches events and reverse requests, supports wait-for-event predicates/timeouts, handles process exit, and wraps Bun sockets into streams/sinks.
- inputs_outputs_state: Inputs are resolved adapter command/cwd, DAP request args, event handlers, abort signals, and socket mode; outputs are request responses, events, reverse responses, capabilities, and errors. State includes request seq, pending map, message buffer, handlers, capabilities, disposed flag.
- gates_or_invariants: Requests fail when disposed; timeouts and aborts reject pending promises; socket readiness is polled with process-exit detection; malformed messages resync without killing reader.
- dependencies_and_callers: Used by debug tooling; depends on `ptree`, Bun spawn/listen/connect, DAP protocol types, and noninteractive env.
- edge_cases_or_failure_modes: Adapter stdout junk, partial frames, missing `Content-Length`, socket timeout, adapter exit before ready, unsupported reverse request, and process stderr surfaced on exit.
- validation_or_tests: Covered by `debug/dap-launch-failures.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2059 `file` `packages/coding-agent/src/discovery/mcp-json.ts`
- cursor: `[_]`
- core_role: Capability discovery provider for standalone `mcp.json` and `.mcp.json`.
- algorithmic_behavior: Reads project-root MCP config files, parses JSON, transforms `mcpServers` into canonical `MCPServer` entries, validates `enabled` and `timeout`, expands env vars deeply, and registers provider with priority 5.
- inputs_outputs_state: Inputs are cwd and config file contents; outputs are MCP server items and warnings.
- gates_or_invariants: Invalid JSON yields warning; invalid boolean/timeout values are ignored with logger warnings; missing files produce empty results.
- dependencies_and_callers: Used by capability discovery; depends on discovery helpers, capability fs, and MCP capability registry.
- edge_cases_or_failure_modes: Malformed config, wrong field types, env expansion in nested auth/oauth/header values.
- validation_or_tests: Covered by discovery/capability tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2089 `file` `packages/coding-agent/src/exec/bash-executor.ts`
- cursor: `[_]`
- core_role: Bash/shell execution orchestrator with persistent sessions, snapshots, minimizer integration, output sink, cancellation, and timeout handling.
- algorithmic_behavior: Resolves shell config/user shell, creates shell startup snapshot, builds noninteractive env, chooses persistent `Shell` vs one-shot `executeShell`, serializes session reuse by key, races command result with abort/timeout via `ExponentialYield`, quarantines broken sessions, minimizes output and stores raw artifacts.
- inputs_outputs_state: Inputs are command, cwd/env/session key/timeout/signal/settings; outputs are exit code, cancelled flag, visible output, truncation/artifact metadata. State includes global shell session maps, broken/quarantine sets, and in-use keys.
- gates_or_invariants: Aborted commands return cancelled output; persistent sessions are single-owner; timed-out/async sessions are reset/quarantined; minimizer settings are part of session key.
- dependencies_and_callers: Used by bash tool and subprocess paths; depends on `pi-natives` shell/minimizer, settings, output sink, shell snapshot, noninteractive env.
- edge_cases_or_failure_modes: Parallel same-key commands degrade to one-shot, aborted persistent session cleanup, timeout race, minimized raw-output artifact save failure, non-Bash user shell wrapping.
- validation_or_tests: Covered by bash/tool execution tests and shell minimizer tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2119 `file` `packages/coding-agent/src/internal-urls/history-protocol.ts`
- cursor: `[_]`
- core_role: Internal `history://` protocol handler for agent transcript resources.
- algorithmic_behavior: Resolves empty host to an agent index, resolves agent IDs against `AgentRegistry`, reads live session messages or parked session JSONL read-only, formats transcript markdown, and offers completion candidates.
- inputs_outputs_state: Inputs are internal URL and registry state; outputs are markdown `InternalResource` or URL completions.
- gates_or_invariants: Unknown agents throw with known list; parked refs require retained session file; live refs use in-memory messages.
- dependencies_and_callers: Used by read/internal URL tooling; depends on agent registry and session history formatter/loader.
- edge_cases_or_failure_modes: Gone session without retained file, stale registry IDs, and last-activity humanization.
- validation_or_tests: Internal URL tests cover related protocols; history behavior is covered indirectly.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2149 `file` `packages/coding-agent/src/markit/types.ts`
- cursor: `[_]`
- core_role: Type contract for Markit-style conversion pipeline.
- algorithmic_behavior: Defines stream metadata, conversion result, optional image/audio callbacks, and converter accept/convert interface.
- inputs_outputs_state: Inputs/outputs are type-level only: buffer plus `StreamInfo` to markdown/title result.
- gates_or_invariants: Converter implementations must quick-check `accepts` before `convert`.
- dependencies_and_callers: Used by markit conversion adapters.
- edge_cases_or_failure_modes: Type-only file does not implement runtime failure handling.
- validation_or_tests: Converter implementations are tested elsewhere.
- skip_candidate: `yes: pure type/interface contract`

### OH_MY_HUMANIZE_MAIN-HZ-2179 `file` `packages/coding-agent/src/mnemopi/index.ts`
- cursor: `[_]`
- core_role: Barrel export for coding-agent Mnemopi backend/config/state modules.
- algorithmic_behavior: Re-exports backend, config, and state modules.
- inputs_outputs_state: No direct runtime inputs; output is module export surface.
- gates_or_invariants: Export paths must remain valid and unambiguous.
- dependencies_and_callers: Used by consumers importing coding-agent Mnemopi helpers.
- edge_cases_or_failure_modes: Broken export path or ambiguous barrel exports.
- validation_or_tests: Covered by TypeScript/package import checks.
- skip_candidate: `yes: barrel only, no algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-2209 `file` `packages/coding-agent/src/secrets/obfuscator.ts`
- cursor: `[_]`
- core_role: Secret obfuscation/deobfuscation engine for provider-visible context and tool schemas.
- algorithmic_behavior: Builds plain and regex secret mappings, generates deterministic placeholders/replacements, obfuscates text with longest-first plain replacements plus regex match discovery, deobfuscates placeholders, and deep-walks plain objects/arrays/strings.
- inputs_outputs_state: Inputs are secret entries, messages/context/tools, and arbitrary objects; outputs are obfuscated/deobfuscated clones or original references when unchanged. State includes mapping maps and next regex index.
- gates_or_invariants: Invalid regex entries are skipped; replace-mode is one-way; tool schemas are converted to wire JSON schema before obfuscation; only plain records are deep-walked.
- dependencies_and_callers: Used by session/provider request interception; depends on secret regex compiler and `toolWireSchema`.
- edge_cases_or_failure_modes: Placeholder collision, zero-length regex matches, overlapping secrets, invalid regex, and non-plain objects.
- validation_or_tests: Covered by secret/tool/provider context tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2239 `file` `packages/coding-agent/src/session/tool-choice-queue.ts`
- cursor: `[_]`
- core_role: Queue/state machine for forced tool-choice directives across LLM turns.
- algorithmic_behavior: Pushes single/sequence generators, serves next tool choice as in-flight, resolves only after invocation when required, rejects with optional requeue, supports label removal/clear, and exposes last served label.
- inputs_outputs_state: Inputs are `ToolChoice` iterables and lifecycle callbacks; outputs are next choice, callback invocations, and queue inspection. State is directive queue, in-flight item, and last resolved label.
- gates_or_invariants: At most one in-flight choice; `onInvoked` directives are rejected as `not_invoked` unless tool actually runs; requeue replays only lost yield.
- dependencies_and_callers: Used by agent session/tool routing to force or schedule tools.
- edge_cases_or_failure_modes: Turn aborts, unavailable tool, removed label while in-flight, repeated requeue, and sequence generator exhaustion.
- validation_or_tests: Covered by session/tool-choice tests and collab/todo steering behavior.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2269 `file` `packages/coding-agent/src/task/omp-command.ts`
- cursor: `[_]`
- core_role: Resolver for invoking the `omp` command from task/subprocess contexts.
- algorithmic_behavior: Uses `PI_SUBPROCESS_CMD` when set, otherwise re-enters current `.ts/.js` entry via `process.execPath`, otherwise falls back to platform default `omp`/`omp.cmd`.
- inputs_outputs_state: Inputs are env var, `process.argv`, and platform; output is `{cmd,args,shell}`.
- gates_or_invariants: Windows default uses shell; source/bundled JS entry uses direct exec path without shell.
- dependencies_and_callers: Used by task/subagent subprocess launch.
- edge_cases_or_failure_modes: Missing argv entry, custom env command with spaces, Windows shell behavior.
- validation_or_tests: Covered by task/subagent runtime fallback tests.
- skip_candidate: `yes: small resolver, but runtime-critical for subprocess routing`

### OH_MY_HUMANIZE_MAIN-HZ-2299 `file` `packages/coding-agent/src/tools/builtin-names.ts`
- cursor: `[_]`
- core_role: Canonical list/type of built-in tool names.
- algorithmic_behavior: Exports `BUILTIN_TOOL_NAMES` and derived union type.
- inputs_outputs_state: No inputs; output is static tool-name list.
- gates_or_invariants: Names must match actual built-in tool registry for completion/config selection.
- dependencies_and_callers: Used by completion generator and tool configuration.
- edge_cases_or_failure_modes: Drift from actual tool registry.
- validation_or_tests: Covered by tool capability/completion tests.
- skip_candidate: `yes: constant list only, though it gates tool completion/config`

### OH_MY_HUMANIZE_MAIN-HZ-2329 `file` `packages/coding-agent/src/tools/manage-skill.ts`
- cursor: `[_]`
- core_role: Agent tool for creating/updating/deleting isolated managed skills.
- algorithmic_behavior: Defines strict ArkType schema with cross-field create/update requirements, gates tool creation on `autolearn.enabled`, deletes or writes managed skills, refuses create when authored skill already claims the sanitized name, and returns structured details.
- inputs_outputs_state: Inputs are action/name/description/body and session settings; outputs are tool results and managed skill filesystem changes.
- gates_or_invariants: Create/update require description and body; authored skills cannot be shadowed by managed skills; tool only exists when autolearn is enabled.
- dependencies_and_callers: Depends on managed skill storage, authored skill discovery, prompt markdown, and tool session.
- edge_cases_or_failure_modes: Missing fields, invalid names, delete of nonexistent skill, authored-name collision.
- validation_or_tests: Covered by skill/manage/autolearn tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2359 `file` `packages/coding-agent/src/tts/models.ts`
- cursor: `[_]`
- core_role: Local TTS model/voice registry and resolver.
- algorithmic_behavior: Defines Kokoro voice catalog, default model/voice, registry value lists/options, compile-time registry/value consistency check, and resolver functions for repo and valid voice fallback.
- inputs_outputs_state: Inputs are optional model key and voice ID; outputs are Hugging Face repo ID or valid voice ID.
- gates_or_invariants: Unknown model key throws in repo resolver; unknown/legacy/default voice falls back to model default.
- dependencies_and_callers: Used by TTS worker/settings.
- edge_cases_or_failure_modes: Empty registry, unknown voice, legacy `"default"` sentinel, and stale settings value list.
- validation_or_tests: Covered by TTS settings/worker tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2389 `file` `packages/coding-agent/src/utils/git.ts`
- cursor: `[_]`
- core_role: Comprehensive git command API for coding-agent workflows.
- algorithmic_behavior: Wraps git spawn with env/config/lock handling, serializes repo writes, resolves repo roots and refs including reftable, validates hunks, and exposes diff/status/stage/commit/push/checkout/fetch/read-tree/write-tree/show/log/branch/remote/ref/config/worktree/patch/cherry-pick/stash/clone/restore/reset/clean/ls/head/repo/github APIs.
- inputs_outputs_state: Inputs are cwd, git args/options, patches, refs, and env; outputs are command text/status, parsed refs/logs/status, or mutations in git repo. State includes per-repo locks and command configuration.
- gates_or_invariants: Write operations use repo lock; patch/hunk validation rejects unsafe diffs; optional locks/config are applied consistently; command errors are surfaced.
- dependencies_and_callers: Used throughout coding-agent session, commit, workflow, autoresearch, task, and tools.
- edge_cases_or_failure_modes: Reftable refs, unborn/detached HEAD, worktrees, pathspecs, binary patches, lock contention, and GitHub remote parsing.
- validation_or_tests: Covered by commit/workflow/task/git-dependent tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2419 `file` `packages/coding-agent/src/workflow/graph-view.ts`
- cursor: `[_]`
- core_role: Workflow graph view builder and terminal renderer.
- algorithmic_behavior: Builds graph node/edge/status/topology/focus/frontier views, lays out ranks and loop rails, renders ASCII graph connectors/boxes/labels, formats route conditions and active agent progress, and produces overview/on-flight/recent/focus/control lines.
- inputs_outputs_state: Inputs are workflow definition/run family snapshots, state patches, width, and render options; outputs are `WorkflowGraphView`, text diagrams, and operator guidance strings.
- gates_or_invariants: Widths are clamped, topology detects back edges/roots, selected routes derive from activation output, and focus selects active/failing/relevant nodes.
- dependencies_and_callers: Used by workflow mode/UI; depends on workflow definition/display/lifecycle/state helpers and TUI width utilities.
- edge_cases_or_failure_modes: Loops/back edges, omitted aborted outputs, structured detail JSON, narrow terminals, multi-agent generations, and checkpoint frontier migration.
- validation_or_tests: Covered by `packages/coding-agent/test/workflow/definition.test.ts` and workflow view tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2449 `file` `packages/coding-agent/test/collab/steer-queue.test.ts`
- cursor: `[_]`
- core_role: Tests mid-turn collab guest prompt steering queue.
- algorithmic_behavior: Exercises guest prompt queuing while assistant turns/tools are active and verifies prompts are delivered at safe boundaries.
- inputs_outputs_state: Inputs are collab messages, session state, and mocked queue/timing; outputs are queued user messages or steering actions.
- gates_or_invariants: Mid-turn guest prompts must not corrupt in-flight tool/assistant state.
- dependencies_and_callers: Tests collab session integration and steering queue.
- edge_cases_or_failure_modes: Multiple guest prompts, session abort/idle transitions, and cleanup.
- validation_or_tests: Describe block at line 176.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2479 `file` `packages/coding-agent/test/debug/dap-launch-failures.test.ts`
- cursor: `[_]`
- core_role: Tests DAP launch validation and failure surfacing.
- algorithmic_behavior: Exercises adapter spawn/connect failures, stderr/error formatting, launch validation, and debug tool failure paths.
- inputs_outputs_state: Inputs are mocked adapter configs/processes; outputs are user-visible debug errors and validation results.
- gates_or_invariants: Missing/broken adapters should fail clearly and not hang.
- dependencies_and_callers: Tests DAP client/debug tool integration.
- edge_cases_or_failure_modes: Socket readiness timeout, adapter exit before ready, invalid launch config.
- validation_or_tests: Describe blocks at lines 160 and 347.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2509 `file` `packages/coding-agent/test/eval/console-table.test.ts`
- cursor: `[_]`
- core_role: Tests JS eval console.table bridge rendering.
- algorithmic_behavior: Verifies console.table calls are captured and formatted into expected display/output structures.
- inputs_outputs_state: Inputs are eval code using `console.table`; outputs are display records/text.
- gates_or_invariants: Table output must preserve meaningful rows/columns without crashing runtime.
- dependencies_and_callers: Tests eval JS bridge.
- edge_cases_or_failure_modes: Empty arrays/objects and mixed row shapes.
- validation_or_tests: Describe block at line 29.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2539 `file` `packages/coding-agent/test/internal-urls/vault-protocol.test.ts`
- cursor: `[_]`
- core_role: Tests internal vault URL protocol handler.
- algorithmic_behavior: Exercises resolving/listing vault resources, completion, and error cases.
- inputs_outputs_state: Inputs are `vault://` URLs and mocked vault state; outputs are internal resources or errors.
- gates_or_invariants: Unknown/malformed vault paths must fail predictably; resources should be read-only where appropriate.
- dependencies_and_callers: Tests internal URL protocol infrastructure.
- edge_cases_or_failure_modes: Missing resources, bad URL encoding, and completion filtering.
- validation_or_tests: Describe block at line 34.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2569 `file` `packages/coding-agent/test/session-manager/helpers.ts`
- cursor: `[_]`
- core_role: Test helper module for session-manager tests.
- algorithmic_behavior: Provides reusable helper functions/fixtures for session-manager test setup.
- inputs_outputs_state: Inputs are test temp dirs/session parameters; outputs are constructed test state.
- gates_or_invariants: Helpers must isolate test state and avoid leaking session files.
- dependencies_and_callers: Used by session-manager test files.
- edge_cases_or_failure_modes: Temp path collision and stale helper assumptions.
- validation_or_tests: Exercised by importing tests.
- skip_candidate: `yes: test helper, not production algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-2599 `file` `packages/coding-agent/test/slash-commands/login.test.ts`
- cursor: `[_]`
- core_role: Tests `/login` slash command flow.
- algorithmic_behavior: Validates command parsing, provider selection, login invocation, and user-facing results.
- inputs_outputs_state: Inputs are slash command strings and mocked auth/model registry; outputs are command action/results.
- gates_or_invariants: Unknown provider and login failures must surface; successful login updates auth state.
- dependencies_and_callers: Tests slash command registry/login command.
- edge_cases_or_failure_modes: Missing provider, cancelled login, provider-specific callbacks.
- validation_or_tests: Describe block at line 47.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2629 `file` `packages/coding-agent/test/task/task-prompt-role.test.ts`
- cursor: `[_]`
- core_role: Tests task tool description role parameter behavior.
- algorithmic_behavior: Ensures generated task tool descriptions include/handle role parameter semantics.
- inputs_outputs_state: Inputs are task tool metadata; outputs are description strings/schema expectations.
- gates_or_invariants: Role parameter must be exposed accurately for downstream agents.
- dependencies_and_callers: Tests task tool prompt/description generation.
- edge_cases_or_failure_modes: Missing role text or stale schema description.
- validation_or_tests: Describe block at line 21.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2659 `file` `packages/coding-agent/test/tools/edit-diff.test.ts`
- cursor: `[_]`
- core_role: Tests edit diff string generation.
- algorithmic_behavior: Verifies generated diff strings for edits across path/content cases.
- inputs_outputs_state: Inputs are before/after file text and edit metadata; outputs are unified/compact diff strings.
- gates_or_invariants: Diff output must preserve changed lines and headers expected by renderers.
- dependencies_and_callers: Tests edit tool diff utilities.
- edge_cases_or_failure_modes: Empty files, trailing newline differences, and multi-hunk edits.
- validation_or_tests: Describe block at line 4.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2689 `file` `packages/coding-agent/test/tools/memory-renderer.test.ts`
- cursor: `[_]`
- core_role: Tests TUI renderers for memory tools.
- algorithmic_behavior: Verifies retain/recall/reflect renderers summarize result details and error states.
- inputs_outputs_state: Inputs are tool result payloads/details; outputs are rendered component/text lines.
- gates_or_invariants: Renderer must sanitize/format without assuming optional details.
- dependencies_and_callers: Tests coding-agent memory tool renderers.
- edge_cases_or_failure_modes: Empty results, error result, missing fields.
- validation_or_tests: Describe blocks at lines 19, 71, and 114.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2719 `file` `packages/coding-agent/test/tools/task-agent-capabilities.test.ts`
- cursor: `[_]`
- core_role: Tests task agent capability descriptions.
- algorithmic_behavior: Ensures task tool exposes accurate capability descriptions for subagents.
- inputs_outputs_state: Inputs are agent capability definitions; outputs are description text/schema.
- gates_or_invariants: Capability descriptions must stay synchronized with actual supported task behavior.
- dependencies_and_callers: Tests task tool metadata.
- edge_cases_or_failure_modes: Missing capabilities and stale tool descriptions.
- validation_or_tests: Describe block at line 25.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2749 `file` `packages/coding-agent/test/workflow/definition.test.ts`
- cursor: `[_]`
- core_role: Tests workflow definition parsing.
- algorithmic_behavior: Parses workflow definitions, validates graph/condition/task structures, and asserts error behavior.
- inputs_outputs_state: Inputs are workflow definition documents/objects; outputs are parsed workflow nodes/edges or validation errors.
- gates_or_invariants: Definitions must be structurally valid, acyclic/consistent where required, and reject malformed conditions.
- dependencies_and_callers: Tests workflow definition subsystem consumed by graph view/runtime.
- edge_cases_or_failure_modes: Missing nodes, invalid edges, bad condition syntax, duplicate IDs.
- validation_or_tests: Describe block at line 34.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2779 `file` `packages/collab-web/src/tool-render/element.tsx`
- cursor: `[_]`
- core_role: Custom element wrapper for rendering tool views in collab web.
- algorithmic_behavior: Defines `OmpToolViewElement`, attaches React root, reads payload store key/props, renders `ToolView`, updates on attribute changes, and unmounts on disconnect.
- inputs_outputs_state: Inputs are element attributes and payload store; output is rendered React UI in shadow/element root. State is React root and current props.
- gates_or_invariants: Missing payload should not crash rendering; custom element definition is idempotent.
- dependencies_and_callers: Used by collab web tool render embedding; depends on React DOM and `ToolView`.
- edge_cases_or_failure_modes: Attribute changes before connection, missing payload key, repeated define.
- validation_or_tests: Covered by collab-web UI tests if present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2809 `file` `packages/mnemopi/src/core/query-intent.ts`
- cursor: `[_]`
- core_role: Query intent classifier and retrieval weight adjuster for memory search.
- algorithmic_behavior: Applies regex pattern groups for temporal/factual/entity/preference/procedural intents, selects highest score, attaches bias weights, and normalizes adjusted vector/FTS/importance weights.
- inputs_outputs_state: Input is query string and optional base weights; output is intent category/confidence/signals and normalized weight tuple.
- gates_or_invariants: General intent defaults to neutral weights; total positive weight is normalized to sum to 1.
- dependencies_and_callers: Used by Mnemopi retrieval/ranking.
- edge_cases_or_failure_modes: Multiple category matches, zero total base weights, dates/natural language ambiguity.
- validation_or_tests: Covered by Mnemopi query/retrieval tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2839 `file` `packages/swarm-extension/src/swarm/executor.ts`
- cursor: `[_]`
- core_role: Swarm extension executor for launching coding-agent subprocess agents.
- algorithmic_behavior: Builds agent-specific system prompt, calls `runSubprocess`, tracks state transitions, and reports completion/failure back to swarm state.
- inputs_outputs_state: Inputs are swarm agent schema, options, cwd/session context, and state tracker; outputs are subprocess results and state updates.
- gates_or_invariants: Agent execution must resolve paths and preserve configured model/role/task metadata.
- dependencies_and_callers: Depends on `@oh-my-pi/pi-coding-agent` subprocess API and swarm state/schema.
- edge_cases_or_failure_modes: Subprocess failure, missing cwd/model, and prompt construction mismatch.
- validation_or_tests: Covered by swarm extension tests if present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2869 `file` `python/robomp/src/proxy/__init__.py`
- cursor: `[_]`
- core_role: Python package marker/export surface for robomp proxy module.
- algorithmic_behavior: Minimal package initialization only.
- inputs_outputs_state: No meaningful runtime inputs/outputs beyond importability.
- gates_or_invariants: Package import path must remain valid.
- dependencies_and_callers: Used by robomp proxy imports.
- edge_cases_or_failure_modes: Broken package export if removed.
- validation_or_tests: Import exercised by robomp tests.
- skip_candidate: `yes: package init only`

### OH_MY_HUMANIZE_MAIN-HZ-2899 `file` `crates/pi-shell/src/minimizer/filters/binary_tools.rs`
- cursor: `[_]`
- core_role: Built-in minimizer filter for binary-inspection command output.
- algorithmic_behavior: Supports tools such as `xxd`, `strings`, and `od`, compacts output to head/tail slices, and respects legacy kill switch.
- inputs_outputs_state: Inputs are command identity/output/config; outputs are minimized binary-tool text or no-op.
- gates_or_invariants: Only recognized binary tools are minimized; legacy disable flag bypasses behavior.
- dependencies_and_callers: Used by minimizer engine and pi-natives shell execution.
- edge_cases_or_failure_modes: Very short outputs, unrecognized binary tools, and head/tail boundary calculation.
- validation_or_tests: Rust minimizer filter tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2929 `file` `packages/ai/src/registry/oauth/cursor.ts`
- cursor: `[_]`
- core_role: Cursor OAuth/PKCE login and token refresh flow.
- algorithmic_behavior: Generates PKCE challenge/UUID/login URL, polls Cursor auth endpoint with exponential backoff and consecutive error cap, refreshes tokens, derives expiry from JWT `exp`, and detects expiring tokens.
- inputs_outputs_state: Inputs are callback handlers, UUID/verifier, refresh token/API key, and threshold; outputs are OAuth credentials with access/refresh/expires.
- gates_or_invariants: Polling caps at 150 attempts, 3 consecutive errors, and 10s max delay; refresh requires OK response.
- dependencies_and_callers: Used by Cursor provider auth registry; depends on `fetch`, `Bun.sleep`, and PKCE helper.
- edge_cases_or_failure_modes: 404 pending poll, network errors, invalid JWT payload, missing refresh token in response.
- validation_or_tests: Covered by OAuth/auth storage tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2959 `file` `packages/ai/src/utils/schema/types.ts`
- cursor: `[_]`
- core_role: JSON object type guard helpers for schema utilities.
- algorithmic_behavior: Checks non-null object/non-array and own-key emptiness.
- inputs_outputs_state: Inputs are unknown values or JSON objects; outputs are boolean type guards.
- gates_or_invariants: Arrays are explicitly excluded from `JsonObject`.
- dependencies_and_callers: Used by schema/tool conversion utilities.
- edge_cases_or_failure_modes: Class instances pass object guard; emptiness only checks enumerable own keys.
- validation_or_tests: Covered indirectly by schema/provider tests.
- skip_candidate: `yes: tiny type guard helper`

### OH_MY_HUMANIZE_MAIN-HZ-2989 `file` `packages/coding-agent/src/commit/agentic/validation.ts`
- cursor: `[_]`
- core_role: Agentic commit validation and prioritization rules.
- algorithmic_behavior: Normalizes summaries, enforces summary formatting/past-tense verb, warns on filler/meta phrases, caps detail items by risk score, and checks type consistency against changed paths/diff/details.
- inputs_outputs_state: Inputs are summary/type/scope/details/files/diff; outputs are normalized summary, errors, warnings, and capped details.
- gates_or_invariants: Summary max is 72 chars and must start with past-tense verb; details cap at 6; docs/test/ci/build types require matching files.
- dependencies_and_callers: Used by agentic commit workflow; depends on commit analysis validation and Unicode normalization.
- edge_cases_or_failure_modes: Past-tense false positives, details with security/perf/breaking priority, wide file changes, and perf commits without evidence.
- validation_or_tests: Covered by commit/agentic tests and commit-shared LLM tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3019 `file` `packages/coding-agent/src/eval/__tests__/bridge-timeout.test.ts`
- cursor: `[_]`
- core_role: Tests eval bridge timeout behavior.
- algorithmic_behavior: Exercises bridge timeout wrapper and ensures long-running bridge calls abort/reject as expected.
- inputs_outputs_state: Inputs are timed promises/bridge calls; outputs are timeout errors or successful values.
- gates_or_invariants: Timeout must fire deterministically and cleanup timers.
- dependencies_and_callers: Tests eval `bridge-timeout.ts`.
- edge_cases_or_failure_modes: Race between completion and timeout.
- validation_or_tests: This file is the direct validation.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3049 `file` `packages/coding-agent/src/extensibility/custom-commands/types.ts`
- cursor: `[_]`
- core_role: Type contract for TypeScript custom slash commands.
- algorithmic_behavior: Defines injected command API, command shape, factory return types, load metadata, and load result errors.
- inputs_outputs_state: Type-level inputs are command args/context/API; outputs are optional prompt strings or fire-and-forget void.
- gates_or_invariants: Runtime loaders should provide cwd/exec/typebox/arktype/zod/pi API and track source/resolved paths.
- dependencies_and_callers: Used by custom command loader/executor and extension hooks.
- edge_cases_or_failure_modes: Type-only file does not implement runtime checks; loader must validate actual exports.
- validation_or_tests: Covered by custom command loader tests.
- skip_candidate: `yes: type/interface contract only`

### OH_MY_HUMANIZE_MAIN-HZ-3079 `file` `packages/coding-agent/src/lsp/clients/biome-client.ts`
- cursor: `[_]`
- core_role: Biome CLI-based linter/formatter client.
- algorithmic_behavior: Runs Biome with Bun spawn, formats files by write/readback, parses JSON diagnostics, filters diagnostics to target file, converts byte offsets to zero-based LSP ranges in one pass per source, maps severity, and logs broken CLI/parse failures once.
- inputs_outputs_state: Inputs are file path/content/server config/cwd; outputs are formatted content or diagnostic arrays.
- gates_or_invariants: Empty stdout with nonzero exit means CLI failure; diagnostics for other files are ignored; parse failures return no diagnostics with warning.
- dependencies_and_callers: Used by LSP/linter system; depends on Biome CLI and logger.
- edge_cases_or_failure_modes: Multibyte UTF-8 byte offsets, missing Biome binary, invalid JSON, cross-file diagnostics.
- validation_or_tests: Covered by lsp/debug/lint integration tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3109 `file` `packages/coding-agent/src/modes/components/copy-selector.ts`
- cursor: `[_]`
- core_role: Fullscreen TUI copy-target selector with tree navigation and preview.
- algorithmic_behavior: Flattens copy-target tree with ancestor connector state, handles up/down/page/enter/cancel keys, centers selection window, wraps/syntax-highlights preview, and renders bordered tree/preview/footer.
- inputs_outputs_state: Inputs are `CopyTarget` roots, terminal key data, and terminal dimensions; outputs are rendered lines and pick/cancel callbacks. State is cursor target ID and tree row count.
- gates_or_invariants: Empty tree ignores navigation; Enter only picks targets with content; text is tab-replaced and width-truncated/wrapped.
- dependencies_and_callers: Used by `/copy` mode; depends on TUI utilities and theme.
- edge_cases_or_failure_modes: Narrow terminals, long labels/hints, empty targets, and preview overflow.
- validation_or_tests: Covered by modes/component tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3139 `file` `packages/coding-agent/src/modes/components/plugin-settings.ts`
- cursor: `[_]`
- core_role: TUI plugin settings navigation and detail components.
- algorithmic_behavior: Builds unified npm/marketplace plugin list, computes stable entry values/status badges, shows detail/config submenus, toggles enable/features/config, and top-level component asynchronously loads both registries while handling failures.
- inputs_outputs_state: Inputs are cwd, plugin registries, key input, and callbacks; outputs are rendered settings panels and plugin manager mutations.
- gates_or_invariants: Marketplace missing `enabled` means enabled; stable values distinguish scope/kind; Escape closes even before async list mounts.
- dependencies_and_callers: Used by settings UI; depends on `PluginManager`, marketplace manager/registry, TUI lists, logger, and theme.
- edge_cases_or_failure_modes: Corrupt registry, duplicated plugin IDs across scopes, shadowed marketplace plugins, async list failure, and invalid config edits.
- validation_or_tests: Covered by plugin/settings component tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3169 `file` `packages/coding-agent/src/modes/controllers/extension-ui-controller.ts`
- cursor: `[_]`
- core_role: Bridge between extensions/hooks/custom tools and interactive TUI/session actions.
- algorithmic_behavior: Creates UI context for select/confirm/input/editor/widgets/theme/status, initializes extension actions/context/command actions, manages hook widgets, queues dialogs, sends custom/user messages, handles session reload/new/branch/tree/switch/compact, and emits session events.
- inputs_outputs_state: Inputs are extension calls, TUI context, session manager, and user dialog input; outputs are UI components, session mutations, extension events, and status/errors. State includes terminal-input unsubscribers, widget maps, and dialog queue.
- gates_or_invariants: Single dialog at a time; extension model switch requires API key; shutdown deferred to idle; widgets are disposed/rebuilt safely.
- dependencies_and_callers: Used by interactive mode extension runner; depends on hooks/types, keybindings, theme, session APIs, custom command APIs.
- edge_cases_or_failure_modes: Extension action rejection, concurrent dialogs, session switch during widgets, custom message display after streaming.
- validation_or_tests: Covered by extension UI/controller tests and idle-compaction/event tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3199 `file` `packages/coding-agent/src/modes/utils/ui-helpers.ts`
- cursor: `[_]`
- core_role: Interactive TUI transcript rendering/rebuild helper.
- algorithmic_behavior: Converts session messages to components, coalesces status messages, handles custom message renderers, reconstructs tool call/result components during transcript rebuild, groups read results, defers usage rows, collapses displaceable job polls, and propagates images/expanded state.
- inputs_outputs_state: Inputs are agent/session messages, render options, UI settings, pending tool maps; outputs are chat container components and editor history updates. State is through `InteractiveModeContext`.
- gates_or_invariants: Tool results render inline with tool calls; read groups seal before non-read content; pending tool map cleared on rebuild; text/images are materialized safely.
- dependencies_and_callers: Used by interactive mode startup/reload/compaction; depends on many TUI components and tool renderers.
- edge_cases_or_failure_modes: Aborted assistant turns, missing tool result, image-only read result, repeated job polls, late diagnostics, custom renderer absence.
- validation_or_tests: Covered by event-controller/rebuild/tool-renderer tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3229 `file` `packages/coding-agent/src/web/scrapers/cheatsh.ts`
- cursor: `[_]`
- core_role: Special web scraper for cheat.sh/cht.sh URLs.
- algorithmic_behavior: Recognizes host/topic, fetches `https://cheat.sh/<topic>?T`, detects code-like content, wraps response in markdown code block with inferred language, and returns render metadata.
- inputs_outputs_state: Inputs are URL, timeout, abort signal; output is `RenderResult` or `null`.
- gates_or_invariants: Non-cheat hosts, missing topic, failed fetch, or empty content return `null`.
- dependencies_and_callers: Used by web research/scraper pipeline.
- edge_cases_or_failure_modes: Encoded topics, ANSI stripping flag, network failure, and non-code prose.
- validation_or_tests: Covered by web scraper research tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3259 `file` `packages/coding-agent/src/web/scrapers/maven.ts`
- cursor: `[_]`
- core_role: Special web scraper for Maven artifact URLs.
- algorithmic_behavior: Recognizes search.maven.org and mvnrepository artifact paths, extracts group/artifact/version, queries Maven Central Solr API, formats metadata plus Maven/Gradle snippets and links.
- inputs_outputs_state: Inputs are artifact URL, timeout, abort signal; outputs are markdown render result or `null`.
- gates_or_invariants: Requires valid artifact path, successful JSON API response, and at least one doc.
- dependencies_and_callers: Used by web research/scraper pipeline; depends on `tryParseJson`, `loadPage`, format helpers.
- edge_cases_or_failure_modes: Missing version, no API result, malformed JSON, classifiers/extensions, timestamp formatting.
- validation_or_tests: Covered by web scraper tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3289 `file` `packages/coding-agent/src/web/scrapers/stackoverflow.ts`
- cursor: `[_]`
- core_role: Special Stack Exchange scraper via official API.
- algorithmic_behavior: Maps standalone and `*.stackexchange.com` hosts to API site params, extracts question ID, fetches question and top answers with body filter, converts HTML to markdown, and returns annotated result.
- inputs_outputs_state: Inputs are Stack Exchange URL, timeout, abort signal; output is markdown render result or `null`.
- gates_or_invariants: Unrecognized host/path, failed question fetch, or empty items return `null`; answers are limited to top 5.
- dependencies_and_callers: Used by web research/scraper pipeline; depends on `htmlToBasicMarkdown` and `loadPage`.
- edge_cases_or_failure_modes: Network/API throttling, no accepted answer, subdomain mapping, HTML conversion quirks.
- validation_or_tests: Covered by web scraper tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3319 `file` `packages/coding-agent/test/modes/components/history-search.test.ts`
- cursor: `[_]`
- core_role: Tests history search component behavior.
- algorithmic_behavior: Exercises query input, result navigation, selection, and rendering in history search UI.
- inputs_outputs_state: Inputs are history entries and key events; outputs are selected entry callbacks and rendered lines.
- gates_or_invariants: Search results should update deterministically and handle empty matches.
- dependencies_and_callers: Tests mode component for session/history navigation.
- edge_cases_or_failure_modes: Empty query, no matches, keyboard wrap/cancel.
- validation_or_tests: Describe block at line 42.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3349 `file` `packages/coding-agent/test/modes/controllers/event-controller-idle-compaction.test.ts`
- cursor: `[_]`
- core_role: Tests event controller idle compaction teardown.
- algorithmic_behavior: Verifies idle compaction lifecycle cleans up timers/listeners/state when controller tears down.
- inputs_outputs_state: Inputs are mocked event controller/session state; outputs are cleanup/compaction calls.
- gates_or_invariants: Idle compaction must not fire after teardown.
- dependencies_and_callers: Tests interactive event controller.
- edge_cases_or_failure_modes: Race between idle timer and disposal.
- validation_or_tests: Describe block at line 27.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3379 `file` `packages/coding-agent/test/tools/web-scrapers/research.test.ts`
- cursor: `[_]`
- core_role: Network-gated tests for research web scrapers.
- algorithmic_behavior: Exercises Wikidata, OpenLibrary, and BioRxiv special handlers when not skipped.
- inputs_outputs_state: Inputs are real or mocked research URLs; outputs are render results.
- gates_or_invariants: Tests are skip-gated by env/network setting.
- dependencies_and_callers: Tests web scraper research handlers.
- edge_cases_or_failure_modes: Network unavailability, external API schema changes.
- validation_or_tests: `describe.skipIf(SKIP)` blocks at lines 8, 38, and 65.
- skip_candidate: `yes: network-gated integration tests`

### OH_MY_HUMANIZE_MAIN-HZ-3409 `file` `packages/collab-web/src/tool-render/tools/browser.tsx`
- cursor: `[_]`
- core_role: Collab web renderer for browser tool calls/results.
- algorithmic_behavior: Extracts browser details/images/text from tool result, classifies action tone, describes target app/action, and renders summary/body with badges/code/images.
- inputs_outputs_state: Inputs are browser tool args/result; output is React nodes for summary/body.
- gates_or_invariants: Missing/invalid details fall back safely; paths are shortened and text truncated.
- dependencies_and_callers: Used by collab-web tool render registry.
- edge_cases_or_failure_modes: Result with only images, unknown action, malformed details record.
- validation_or_tests: Covered by collab-web render tests if present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3439 `file` `packages/mnemopi/src/core/beam/index.ts`
- cursor: `[_]`
- core_role: Beam memory orchestrator for Mnemopi graph/vector/FTS retrieval.
- algorithmic_behavior: Normalizes config, opens/migrates SQLite databases, initializes Beam schema, wires annotation store and episodic graph, and exposes memory operations such as ingest/recall/enhanced recall/fact recall/context formatting.
- inputs_outputs_state: Inputs are database path/options, memory episodes/facts/query; outputs are stored records, recall results, formatted context, and lifecycle state.
- gates_or_invariants: Auto-migration checks pending annotation/triplestore migrations; default weights/config are normalized; database resources close quietly.
- dependencies_and_callers: Used by coding-agent memory backend; depends on `bun:sqlite`, Mnemopi config/db/annotations/episodic graph/beam recall modules.
- edge_cases_or_failure_modes: Missing DB path, pending migration failure, optional embedding absence, corrupt DB, and close errors.
- validation_or_tests: Covered by Mnemopi optional embedding and DeltaSync tests plus memory tools tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3469 `file` `packages/stats/src/client/routes/ProjectsRoute.tsx`
- cursor: `[_]`
- core_role: Stats dashboard route for project/folder usage overview.
- algorithmic_behavior: Fetches folder stats with `useResource`, builds folder row view models, memoizes rows, and renders async boundary/data table/status pills for cost/duration/count metrics.
- inputs_outputs_state: Inputs are active flag, time range, refresh trigger, and API data; output is React UI table.
- gates_or_invariants: Data loads only through resource hook and formats numbers/percent/cost consistently.
- dependencies_and_callers: Used by stats web client routing; depends on API/data/view-model/ui modules.
- edge_cases_or_failure_modes: Empty stats, loading/error states, inactive route, refresh race.
- validation_or_tests: Covered by stats client tests if present.
- skip_candidate: `yes: UI route, light algorithmic content`

### OH_MY_HUMANIZE_MAIN-HZ-3499 `file` `python/robomp/web/src/components/Trigger.tsx`
- cursor: `[_]`
- core_role: Robomp web UI trigger component.
- algorithmic_behavior: Renders trigger controls and dispatches configured trigger actions through props/state.
- inputs_outputs_state: Inputs are component props/user interaction; outputs are UI events/callback invocations.
- gates_or_invariants: Button/control state should reflect disabled/loading state where implemented.
- dependencies_and_callers: Used by robomp web frontend.
- edge_cases_or_failure_modes: Missing callback/invalid props and repeated clicks.
- validation_or_tests: Covered by web UI tests if present.
- skip_candidate: `yes: frontend component with limited core algorithm behavior`

### OH_MY_HUMANIZE_MAIN-HZ-3529 `file` `packages/coding-agent/src/extensibility/plugins/marketplace/registry.ts`
- cursor: `[_]`
- core_role: Persistent registry read/write and pure CRUD helpers for plugin marketplace system.
- algorithmic_behavior: Computes registry/cache paths, atomically writes JSON via temp+rename with Windows EPERM fallback, reads/validates marketplaces and installed plugin registries with default empty fallback, and transforms registry state for add/remove/get/collect paths.
- inputs_outputs_state: Inputs are registry file paths and registry entries; outputs are registry objects and JSON files.
- gates_or_invariants: Invalid/missing registries return empty defaults; duplicate marketplace add and missing remove throw; installed registry accepts numeric forward-compatible versions but normalizes to version 2.
- dependencies_and_callers: Used by marketplace manager, plugin settings, and plugin install/remove commands.
- edge_cases_or_failure_modes: Corrupt JSON, Windows rename EPERM, stale temp file, duplicate names, and shared install paths across registries.
- validation_or_tests: Covered by plugin marketplace registry/manager tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3559 `file` `packages/coding-agent/src/modes/setup-wizard/scenes/theme.ts`
- cursor: `[_]`
- core_role: Setup wizard scene for theme/symbol/colorblind selection with live preview.
- algorithmic_behavior: Renders mock status/editor preview, drives curated/all-theme `SelectList`, handles quick keys/mouse/wheel, previews themes with request sequencing, commits auto/colorblind/ANSI/theme choices to settings, and restores original preview on skip.
- inputs_outputs_state: Inputs are key/mouse events, available themes, settings, and scene host; outputs are rendered lines, settings changes, preview theme updates, and scene finish status.
- gates_or_invariants: Nothing is saved until select/commit; stale preview requests are ignored via `#previewRequest`; disposed scene stops applying loaded themes.
- dependencies_and_callers: Used by setup wizard; depends on TUI select list and theme manager.
- edge_cases_or_failure_modes: Theme loading failure, rapid selection race, all-theme back navigation, narrow preview width.
- validation_or_tests: Covered by setup wizard/theme tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3589 `file` `packages/utils/src/vendor/mermaid-ascii/ascii/er-diagram.ts`
- cursor: `[_]`
- core_role: Vendor ASCII renderer for Mermaid ER diagrams.
- algorithmic_behavior: Parses ER diagrams, formats entity attributes, computes connected components, lays out entity boxes, draws crow’s-foot relationship lines, classifies character roles, and renders colored/plain ASCII output.
- inputs_outputs_state: Inputs are Mermaid ER text, ASCII config, color mode, and theme; output is ASCII diagram string.
- gates_or_invariants: Entity/relationship layout must preserve box widths and relationship endpoints; wide text uses display-width helpers.
- dependencies_and_callers: Used by Mermaid ASCII utility renderer; depends on ER parser/types, canvas/draw/text metrics.
- edge_cases_or_failure_modes: Wide Unicode labels, disconnected components, many relationships, and unsupported cardinality.
- validation_or_tests: Covered by mermaid-ascii renderer tests if present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3619 `file` `packages/utils/src/vendor/mermaid-ascii/ascii/shapes/types.ts`
- cursor: `[_]`
- core_role: Vendor type contracts for ASCII shape renderers.
- algorithmic_behavior: Defines shape dimensions, render options, renderer interface, and registry type.
- inputs_outputs_state: Type-level inputs are canvas/shape options; outputs are renderer dimension/drawing contracts.
- gates_or_invariants: Runtime renderers must implement dimension and render functions consistently.
- dependencies_and_callers: Used by mermaid-ascii shape implementations.
- edge_cases_or_failure_modes: Type-only file does not implement drawing behavior.
- validation_or_tests: Shape renderer tests cover implementations.
- skip_candidate: `yes: type/interface contract only`

## Worker Self-Test
- assigned_items_seen: `121 Item Evidence headings; item IDs are intentionally present only in those headings to avoid duplicates`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`