# agent_30 main 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 120
- source_commit: `6b3819fad50a89fffae899b240ad1ce065c51d23`
- inspection_scope: read-only inspection of assigned paths under `/Users/wangweiyang/GitHub/oh_my_humanize_branch_worktrees/main`
- files_modified: none
- validation_commands_run: none; evidence is from direct source/test/document inspection

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-030 `directory` `packages/hashline`
- cursor: `[_]`
- core_role: Implements the hash-anchored structured edit protocol used by coding-agent read/edit flows.
- algorithmic_behavior: `src/input.ts` parses model-authored edits into `[PATH#HASH]` sections, recovers noisy `apply_patch` wrappers, merges same-path sections, and rejects unified diff contamination. `src/parser.ts` tokenizes edit grammar into typed edit ops with streaming support. `src/apply.ts` applies edits against hashed snapshots with anchor checks, boundary repair, delimiter balancing, and landing correction. `src/patcher.ts` performs preflight/commit orchestration over filesystem snapshots. `src/recovery.ts` attempts snapshot/session-chain recovery when the target file has drifted.
- inputs_outputs_state: Inputs are hashline edit text, filesystem file contents, snapshot hashes, and block/range references. Outputs are edit results, warnings, rewritten file contents, mismatch diagnostics, snapshot updates, and compact previews. State lives primarily in `SnapshotStore`, patcher per-file preparation records, parser pending tokens, and recovery chain metadata.
- gates_or_invariants: Path/hash headers must match known file state; overlapping deletes are rejected; invalid grammar produces structured parser errors; patcher applies all-or-nothing per batch; recovery only commits when guards confirm safe replay. Snapshot limits constrain paths, versions, and byte volume.
- dependencies_and_callers: Used by `packages/coding-agent/src/tools/read.ts` for hashline read headers and by `packages/coding-agent/src/edit/index.ts` for edit application. Depends on filesystem abstractions, hashing/normalization helpers, block resolver, tokenizer/parser, and diff-preview code.
- edge_cases_or_failure_modes: Handles BOM/line-ending normalization, missing trailing newline deletes, shifted replacement boundaries, apply-patch wrapper leakage, path normalization, stale hashes, block edits that resolve to a single line, and session-chain recovery failure.
- validation_or_tests: Covered by `packages/hashline/test/*`: core contracts, patcher, recovery session chain, leniency, boundary repair, landing shift, block edits, diff preview, format v2, and snapshots.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-060 `file` `docs/natives-build-release-debugging.md`
- cursor: `[_]`
- core_role: Architecture/runbook documentation for native build, packaging, runtime loading, and release failure diagnosis.
- algorithmic_behavior: Describes the build pipeline from Rust source through `build-native`, target/variant selection, native package embedding, compiled binary cache extraction, runtime loader paths, and release validation. It defines behavior operators must preserve even though it is prose rather than executable code.
- inputs_outputs_state: Inputs are platform target, CPU variant, build flags, package layout, binary embedding state, and cache directories. Outputs are native artifacts, embedded package assets, extracted runtime files, smoke-test evidence, and debug signals.
- gates_or_invariants: Native package names and target triples must stay consistent; compiled binaries must extract/load embedded native assets; smoke tests validate native loading and tiny inference; robomp cache behavior is content-addressed.
- dependencies_and_callers: Documents relationships among `crates/pi-natives`, native build scripts, package exports, compiled `omp`, installer tests, and release jobs.
- edge_cases_or_failure_modes: Covers missing architecture variants, cache extraction failures, wrong module lookup path, silently broken compiled binary workers, stale native assets, and CI/release mismatch.
- validation_or_tests: References smoke-test and install-test workflows rather than containing tests itself.
- skip_candidate: `yes: documentation, but it defines runtime/build invariants for native algorithms`

### OH_MY_HUMANIZE_MAIN-HZ-090 `file` `scripts/ci-release-notes.ts`
- cursor: `[_]`
- core_role: CI release-note aggregation script for changelog sections across package releases.
- algorithmic_behavior: Compares semver tags, enumerates changelog version spans, merges package sections over `(floor,target]`, buckets bullets by canonical changelog categories, deduplicates exact trimmed bullet text, resolves the previous published release through `gh release list`, and writes a release notes file.
- inputs_outputs_state: Inputs are `packages/*/CHANGELOG.md`, package names, target version argv, `OMP_RELEASE_NOTES_FLOOR`, `OMP_REPO` or `GITHUB_REPOSITORY`, and GitHub release metadata. Output is merged markdown release notes. State is local maps of categories, seen bullets, and package sections.
- gates_or_invariants: Non-semver headings are ignored but still bound spans; `gh` failure is fatal unless an explicit floor override is supplied; category order follows `Breaking Changes`, `Added`, `Changed`, `Fixed`, `Removed`; duplicate bullets are removed by exact normalized line.
- dependencies_and_callers: Uses Bun `Glob`, Bun shell, `Bun.file`, and `Bun.write`; intended for the `release_github` CI job.
- edge_cases_or_failure_modes: Handles silent tags without GitHub releases, missing package names, unknown categories, empty floor override for legacy single-version mode, missing `GH_TOKEN`, and no previous release.
- validation_or_tests: No direct test file inspected; exported helpers are structured for unit testing.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-120 `directory` `crates/pi-natives/src`
- cursor: `[_]`
- core_role: Rust native algorithm crate exposed through N-API for search, text rendering, shell/process, syntax, AST, workspace, image, and compression helpers.
- algorithmic_behavior: `grep.rs` implements ripgrep-backed filesystem/in-memory search with parallel walking, filters, cancellation, limits, and aggregation. `ast.rs` performs ast-grep search/match/edit with language inference, candidate collection, dry-run/write modes, and parse gates. `text.rs` implements ANSI-aware width, wrapping, truncation, slicing, and OSC66 sizing. `highlight.rs` maps syntactic scopes to semantic color slots. Other modules provide PTY/process control, glob/fd scanning, workspace indexing, sixel rendering, HTML, tokens, snapcompact, native caches, and platform integrations.
- inputs_outputs_state: Inputs include file trees, glob/type filters, regexes, AST patterns, terminal strings, syntax language names, process commands, and image/text buffers. Outputs include match records, edit results, wrapped/styled strings, ANSI-highlighted text, process events, glob results, and native-rendered assets. State includes fs scan caches, thread-local text/highlight buffers, task cancellation flags, and native module initialization.
- gates_or_invariants: Search enforces max file and match limits; text routines must preserve escape-state correctness; AST edits validate parse/language and can fail on parse errors; native exports must match JS package bindings; platform-specific modules are gated.
- dependencies_and_callers: Called by `packages/natives` and downstream coding-agent/TUI utilities. Depends on Rust crates such as ripgrep internals, syntect, ast-grep, napi, unicode segmentation/width, and OS APIs.
- edge_cases_or_failure_modes: Handles oversized files, invalid UTF-8, regex fallback/sanitization, cancellation during walkers, parse errors, ANSI escape carryover, OSC hyperlinks/text sizing, Windows/process quirks, and missing platform capabilities.
- validation_or_tests: Indirectly covered by `packages/natives/test/*`, TUI render tests, coding-agent search/read/edit tests, and native build smoke tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-150 `directory` `packages/stats/scripts`
- cursor: `[_]`
- core_role: Build-time script support for embedding the stats web client into the stats server package.
- algorithmic_behavior: `generate-client-bundle.ts` handles `--generate` by building the client output, collecting files in deterministic sorted order, producing a gzip tar payload, and writing base64 content to `src/embedded-client.generated.txt`; `--reset` clears the generated embed.
- inputs_outputs_state: Inputs are CLI mode flags and the stats client build directory. Outputs are a generated embedded-client text asset or an empty reset file. State is temporary archive paths and the generated artifact content.
- gates_or_invariants: File traversal is sorted for stable output; temporary archive cleanup is expected; generation must include the built client tree rather than arbitrary paths.
- dependencies_and_callers: Used by package build/release flow and consumed by `packages/stats/src/server.ts` when serving embedded assets.
- edge_cases_or_failure_modes: Missing build output, tar/gzip failure, stale generated asset, or reset mode accidentally used in release packaging.
- validation_or_tests: No direct test inspected; behavior is exercised by stats server embedded-client path.
- skip_candidate: `yes: build helper, not runtime core, but it feeds the runtime embedded asset algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-180 `file` `docs/tools/ask.md`
- cursor: `[_]`
- core_role: User/tool documentation defining the Ask tool’s interaction contract.
- algorithmic_behavior: Describes how the ask tool presents one to three concise questions, option lists, optional free-form input, blocking versus auto-resolution behavior, and how tool calls are rendered/answered in the coding-agent workflow.
- inputs_outputs_state: Inputs are tool-call question definitions, options, optional timeout, and user answers. Outputs are structured responses back to the agent session. State is pending question UI state and timeout/answer resolution state.
- gates_or_invariants: Questions must be short and bounded; options should be mutually exclusive; auto-resolution is only for non-blocking clarification; explicit user input is required when the task cannot proceed safely.
- dependencies_and_callers: Aligns with `packages/coding-agent/test/tools/ask.test.ts` and the Ask tool implementation/rendering paths.
- edge_cases_or_failure_modes: Malformed arguments, too many questions, no answer before timeout, cancellation, or ambiguous blocking semantics.
- validation_or_tests: `packages/coding-agent/test/tools/ask.test.ts` covers tool behavior, rendering, cancellation, option handling, custom input, and malformed args.
- skip_candidate: `yes: documentation, but it defines an externally visible tool protocol`

### OH_MY_HUMANIZE_MAIN-HZ-210 `file` `scripts/install-tests/binary.dockerfile`
- cursor: `[_]`
- core_role: Binary install smoke-test container definition.
- algorithmic_behavior: Starts from Debian slim, installs runtime/build prerequisites, installs Bun/Rust, copies the repository, runs package installation/build commands, builds native/coding-agent artifacts, copies the resulting `omp` binary, and verifies it with `omp --version`.
- inputs_outputs_state: Inputs are repository source, Docker build context, network/package availability, and build scripts. Output is a container image with a verified binary. State is Docker layer filesystem state.
- gates_or_invariants: Binary must be built from the copied repo and executable inside the image; build dependency installation must precede Bun/Rust/package build steps; final smoke command must succeed.
- dependencies_and_callers: Used by install-test CI or local release smoke workflows; depends on Bun, Rust, Debian packages, native build scripts, and coding-agent build scripts.
- edge_cases_or_failure_modes: Package install failure, missing native build dependency, Bun/Rust installer failure, native build failure, or binary missing shared runtime assets.
- validation_or_tests: The Docker build itself is the validation surface.
- skip_candidate: `yes: CI smoke harness rather than application algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-240 `directory` `packages/catalog/src/discovery`
- cursor: `[_]`
- core_role: Provider model discovery implementations for dynamic catalog population.
- algorithmic_behavior: `openai-compatible.ts` fetches `/models`, accepts multiple envelope shapes, recursively extracts model arrays, and maps records to catalog specs. `gemini.ts` paginates Google model discovery and infers generation-method/reasoning/modality traits. `codex.ts` queries Codex/OpenAI endpoints with client/auth headers and normalizes context, token limits, reasoning levels, and modalities. `antigravity.ts` fetches Google Antigravity/Gemini CLI discovery with validation and denylist/collapse behavior. `cursor.ts` performs HTTP/2 Connect/protobuf `GetUsableModels` discovery and merges custom/reference models. `cursor-gen/agent_pb.ts` supplies generated protobuf schema glue.
- inputs_outputs_state: Inputs are provider descriptors, base URLs, auth tokens/keys, fetch implementation, bundled reference models, and discovery options. Outputs are `ModelSpec`-like catalog entries and discovery metadata. State is request pagination cursors, response validation results, and reference-model maps.
- gates_or_invariants: Discovery validates response shapes before mapping; provider URL normalization must be stable; Cursor protobuf decoding must match generated schema; Gemini/Codex pagination is bounded; generated protobuf code should not be hand-edited.
- dependencies_and_callers: Called by provider model manager/generation flows, including catalog generator and runtime refresh paths. Depends on fetch, arktype-like validators, Connect/protobuf support, and provider descriptors.
- edge_cases_or_failure_modes: Nonstandard `/models` payloads, nested provider envelopes, pagination loops, missing auth, stale generated protobuf schema, model denylist misses, and provider-specific context metadata drift.
- validation_or_tests: Catalog resolver/provider tests and issue repro tests indirectly protect discovery normalization; generated Cursor schema itself is support code.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-270 `directory` `packages/coding-agent/src/markit`
- cursor: `[_]`
- core_role: Document-to-markdown conversion subsystem used by the read tool for PDFs and office/document formats.
- algorithmic_behavior: `registry.ts` selects converters by extension/MIME and delegates buffered file content. PDF conversion extracts text boxes, content-stream segments, image regions, table grids, headers/footers, columns, and renders markdown tables/paragraphs/images. DOCX/PPTX/XLSX/EPUB converters use format libraries/parsers to emit markdown-like text.
- inputs_outputs_state: Inputs are file paths, binary document buffers, MIME/extension hints, and conversion options. Outputs are markdown text plus extracted image/member metadata where applicable. State is converter registry, PDF page structures, detected grids, header/footer candidates, and image placeholders.
- gates_or_invariants: Converter choice must be deterministic; PDF table rendering guards against diagrams and sparse shifted columns; repeated page headers/footers are stripped by thresholds; PDF image placeholders must remain resolvable by read paths.
- dependencies_and_callers: Called from `packages/coding-agent/src/tools/read.ts`. Depends on MuPDF WASM/native extraction, `mammoth`, spreadsheet/presentation parsing utilities, and markdown render conventions.
- edge_cases_or_failure_modes: Multi-column PDFs, scanned/image-only PDFs, repeated headers/footers, sparse tables, diagrams mistaken for tables, embedded images, malformed office files, and unsupported extensions.
- validation_or_tests: `packages/coding-agent/test/tools/read-pdf-line-range.test.ts` and read-tool tests cover converted PDF line access; converters are also exercised through read workflows.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-300 `directory` `packages/coding-agent/test/export`
- cursor: `[_]`
- core_role: Test coverage for coding-agent export behavior, especially workflow HTML export.
- algorithmic_behavior: The contained `html-workflow-export.test.ts` builds sessions/workflows, runs export routines, decodes embedded data from generated HTML, and asserts workflow metadata, lifecycle, inspection, and frozen data are preserved.
- inputs_outputs_state: Inputs are temporary sessions/workflow definitions and export options. Outputs are HTML export artifacts and decoded session/export payloads. State is temp directory/session storage state.
- gates_or_invariants: Exported HTML must include enough embedded state to inspect workflows offline; frozen workflow definitions and lifecycle records must survive serialization.
- dependencies_and_callers: Validates coding-agent export modules and session/workflow serialization.
- edge_cases_or_failure_modes: Missing embedded data, incomplete workflow lifecycle export, path/temp isolation failures, or regression in HTML payload decoding.
- validation_or_tests: This directory is itself validation coverage.
- skip_candidate: `yes: test directory, not runtime implementation`

### OH_MY_HUMANIZE_MAIN-HZ-330 `directory` `packages/tui/src/components`
- cursor: `[_]`
- core_role: Reusable TUI rendering/input component library for coding-agent and related packages.
- algorithmic_behavior: `markdown.ts` renders markdown with extensions for math, strict strikethrough, code blocks, tables, headings, hyperlinks, swatches, and inline formatting. `text.ts` handles wrapping/padding/tab treatment. `input.ts` implements editor-like input with keybindings, paste, kill-ring, and cursor movement. `select-list.ts`, `settings-list.ts`, and `scroll-view.ts` provide fuzzy filtering, selection, scrolling, and truncation. `image.ts` renders terminal images/kitty graphics, while loader/tab/box/spacer/editor helpers compose UI surfaces.
- inputs_outputs_state: Inputs are render props, terminal dimensions, style/theme data, key events, markdown strings, image data, and selection lists. Outputs are TUI render nodes/cells and input state transitions. State includes component-local cursor, scroll, filter, cache, and animation state.
- gates_or_invariants: Text must be width-safe; markdown renderer must sanitize/control ANSI and terminal escapes; scrolling/selection must clamp indexes; image rendering must respect terminal budgets.
- dependencies_and_callers: Used by coding-agent TUI modes, stats/collab CLI UI, tool renderers, and tests. Depends on pi-tui core renderer, native width/highlight helpers, markdown parsing, and terminal capability detection.
- edge_cases_or_failure_modes: Wide Unicode, ANSI carryover, malformed markdown, huge code blocks, resize races, empty lists, out-of-range selection, terminal image unsupported, and long unbreakable text.
- validation_or_tests: Covered by TUI render tests including `packages/tui/test/issue-2088-repro.test.ts` and stress reducer tooling.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-360 `file` `crates/pi-natives/src/highlight.rs`
- cursor: `[_]`
- core_role: Native syntax highlighter that maps source text and language hints to ANSI-colored output.
- algorithmic_behavior: Uses syntect syntax/theme sets, maps syntax scopes to a compact semantic color index, caches scope-to-color decisions thread-locally, supports language aliases, special-cases diff inserted/deleted lines, and falls back to plain input if parsing or language lookup fails.
- inputs_outputs_state: Inputs are source code, optional language name, and a caller-provided color palette. Output is ANSI-highlighted code text or uncolored text. State includes lazily initialized syntax/theme sets and thread-local color cache.
- gates_or_invariants: Language aliases must resolve to known syntect syntax names; palette indexes must align with semantic mapping; highlighter must preserve text content and not panic on unknown syntax.
- dependencies_and_callers: Exported from `pi-natives` to JS native bindings; used by TUI/markdown/code rendering.
- edge_cases_or_failure_modes: Unknown language, empty palette, unsupported scope names, diff lines requiring override, large files, and parse failures.
- validation_or_tests: Exercised indirectly by markdown/render tests and native smoke tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-390 `file` `packages/agent/src/index.ts`
- cursor: `[_]`
- core_role: Package barrel for the agent runtime.
- algorithmic_behavior: Re-exports public modules such as agent loop, append-only context, compaction, proxy, run collector, telemetry, thinking, tokenizer, types, and yield utilities.
- inputs_outputs_state: Input is import resolution from downstream packages. Output is a stable package API surface. It holds no runtime state.
- gates_or_invariants: Barrel exports must avoid ambiguity and preserve public module availability.
- dependencies_and_callers: Imported by coding-agent and other packages needing agent runtime APIs.
- edge_cases_or_failure_modes: Broken export path or ambiguous duplicate export can break consumers at compile/import time.
- validation_or_tests: Covered indirectly by package typecheck and downstream imports.
- skip_candidate: `yes: export surface only, no algorithmic logic in this file`

### OH_MY_HUMANIZE_MAIN-HZ-420 `file` `packages/ai/src/auth-retry.ts`
- cursor: `[_]`
- core_role: Central authentication retry wrapper for AI provider API calls.
- algorithmic_behavior: Distinguishes static API keys from resolver-backed keys, resolves an initial key, classifies retryable auth errors, and runs retry steps that first refresh the same account and then allow account rotation/switching. `withOAuthAccess` wraps token acquisition and invalidation around retryable provider calls.
- inputs_outputs_state: Inputs are API key resolvers, OAuth access sources, abort signals, provider call closures, and thrown errors. Outputs are successful provider call results or final errors. State is passed through resolver context including refresh/switch flags and previous key/token.
- gates_or_invariants: Static keys do not retry; retry only on auth-like failures such as 401/usage-limit messages; resolver failures during retry are swallowed only when another path may proceed; abort signals propagate.
- dependencies_and_callers: Used by AI provider implementations and search/auth integrations, including Exa provider and OAuth-backed registries.
- edge_cases_or_failure_modes: Resolver returns same bad key, token invalidation failure, non-auth provider error, exhausted retry steps, aborted request, and stale OAuth access.
- validation_or_tests: Covered by AI auth storage, OAuth, provider, and issue repro tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-450 `file` `packages/ai/test/anthropic-thinking-only-length-truncated.test.ts`
- cursor: `[_]`
- core_role: Regression tests for Anthropic message history transformation when thinking-only assistant turns are present.
- algorithmic_behavior: Constructs histories with thinking blocks and truncation scenarios, runs Anthropic formatting/streaming paths, and asserts thinking-only turns are dropped or transformed so Anthropic does not receive invalid message sequences.
- inputs_outputs_state: Inputs are synthetic message histories, model/provider settings, and captured request payloads. Outputs are assertions on serialized Anthropic messages. Test state is local mocks/captures.
- gates_or_invariants: Anthropic payloads must not contain invalid thinking-only assistant turns after history truncation; meaningful content/tool continuity must be preserved.
- dependencies_and_callers: Validates `packages/ai` Anthropic dialect/provider history code.
- edge_cases_or_failure_modes: Length truncation removing surrounding text, thinking-only assistant content, and provider payload validation errors.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-480 `file` `packages/ai/test/auth-storage-email-dedupe.test.ts`
- cursor: `[_]`
- core_role: Validation coverage for auth storage account/session deduplication and migration behavior.
- algorithmic_behavior: Builds auth storage scenarios with duplicated emails/accounts, session stickiness, provider credentials, migrations, and account selection; asserts dedupe/merge behavior and stable identity mapping.
- inputs_outputs_state: Inputs are temporary auth storage files/records and provider account metadata. Outputs are normalized storage state and selected credentials. State is temp filesystem-backed auth database/config.
- gates_or_invariants: Duplicate accounts sharing email should be merged deterministically; active session/provider identity must not silently switch incorrectly; migrations should preserve usable credentials.
- dependencies_and_callers: Validates `packages/ai` auth storage and OAuth registry consumers.
- edge_cases_or_failure_modes: Email case differences, missing email metadata, multiple providers, stale sessions, duplicate refresh tokens, and migration from older shapes.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-510 `file` `packages/ai/test/github-copilot-long-context-wire.test.ts`
- cursor: `[_]`
- core_role: Regression tests for GitHub Copilot long-context model request wiring.
- algorithmic_behavior: Captures outgoing provider payloads for Copilot model variants and asserts correct wire IDs, long-context selection, and response image detail handling.
- inputs_outputs_state: Inputs are mock Copilot model selections and request messages. Outputs are captured request payload assertions. State is test-local request capture.
- gates_or_invariants: Long-context variants must map to correct wire model IDs; image detail settings must be clamped/serialized as expected.
- dependencies_and_callers: Validates AI GitHub Copilot provider/registry code.
- edge_cases_or_failure_modes: Wrong model alias, missing long-context flag, unsupported image detail, or payload drift.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-540 `file` `packages/ai/test/issue-2123-repro.test.ts`
- cursor: `[_]`
- core_role: Issue regression test for OAuth Anthropic/Opus request shaping with forced tool choice.
- algorithmic_behavior: Constructs the failing request condition, captures the provider payload, and asserts incompatible fields such as context management are stripped when thinking/tool-choice constraints require it.
- inputs_outputs_state: Inputs are model/auth options, thinking config, forced tool choice, and mock request payload capture. Output is assertion on serialized provider request. State is test-local mocks.
- gates_or_invariants: Provider request must satisfy Anthropic compatibility constraints for thinking plus tool-choice combinations.
- dependencies_and_callers: Validates AI provider request-building logic.
- edge_cases_or_failure_modes: Tool-choice forcing with thinking enabled, OAuth model path differences, and provider rejection from unsupported field combinations.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-570 `file` `packages/ai/test/oauth.ts`
- cursor: `[_]`
- core_role: Shared OAuth/auth test helper module.
- algorithmic_behavior: Provides utilities for constructing OAuth test storage, credentials, tokens, or mock flows used by AI provider tests.
- inputs_outputs_state: Inputs are test parameters and temp paths. Outputs are helper-created auth records or mocked OAuth results. State is test-local storage/mocks.
- gates_or_invariants: Helpers must produce valid auth shapes matching runtime storage expectations.
- dependencies_and_callers: Imported by AI OAuth-related tests.
- edge_cases_or_failure_modes: Helper drift from runtime schema, expired token defaults, or storage cleanup mistakes.
- validation_or_tests: It supports validation rather than defining a standalone runtime test.
- skip_candidate: `yes: test helper, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-600 `file` `packages/ai/test/openai-responses-stream-terminal.test.ts`
- cursor: `[_]`
- core_role: Regression coverage for OpenAI Responses stream terminal handling.
- algorithmic_behavior: Simulates terminal SSE event sequences, including lost or reordered `output_item.added` style cases, and asserts the stream adapter reconstructs terminal output/tool events correctly.
- inputs_outputs_state: Inputs are synthetic SSE events and request options. Outputs are normalized stream deltas/events and assertions. State is mock stream buffers.
- gates_or_invariants: Terminal output must not be dropped if stream event ordering is incomplete; stream finalization must preserve tool/result state.
- dependencies_and_callers: Validates OpenAI Responses provider stream adapter in `packages/ai`.
- edge_cases_or_failure_modes: Missing item-added event, terminal output chunks before metadata, final event without complete state, and stream truncation.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-630 `file` `packages/ai/test/sse-debug.test.ts`
- cursor: `[_]`
- core_role: Unit tests for SSE debug observer normalization.
- algorithmic_behavior: Feeds raw SSE-like events through debug helpers and asserts observers receive normalized event details.
- inputs_outputs_state: Inputs are raw SSE text/event chunks. Outputs are observer calls. State is mock observer call history.
- gates_or_invariants: Debug observation must not mutate stream semantics and should normalize consistently.
- dependencies_and_callers: Validates `packages/ai/src/utils/sse-debug.ts`.
- edge_cases_or_failure_modes: Empty events, malformed data, and event-name/default handling.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-660 `file` `packages/catalog/src/hosts.ts`
- cursor: `[_]`
- core_role: Host/provider classification helpers for catalog/provider routing.
- algorithmic_behavior: Defines known host specs with provider prefixes and URL markers, matches models/base URLs against host classes, performs ASCII case-insensitive substring matching, and recognizes special endpoint shapes for Vertex Express OpenAI, raw Vertex predict, Azure deployments, and Dashscope compatible mode.
- inputs_outputs_state: Inputs are model provider/baseUrl values and endpoint URLs. Outputs are booleans or known-host classifications. State is static host metadata.
- gates_or_invariants: Matching must be stable across case differences without locale surprises; provider-prefix and URL marker rules must not overmatch unrelated hosts.
- dependencies_and_callers: Used by catalog/provider model resolution and host-specific policy decisions.
- edge_cases_or_failure_modes: Custom OpenAI-compatible URLs, Azure deployment path variants, Vertex raw versus OpenAI-compatible endpoints, and Dashscope base URL differences.
- validation_or_tests: Indirectly covered by catalog provider tests and issue repros.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-690 `file` `packages/catalog/test/issue-2558-repro.test.ts`
- cursor: `[_]`
- core_role: Regression test for GitHub Copilot Anthropic model capability metadata.
- algorithmic_behavior: Builds Anthropic client options for Copilot-hosted Anthropic models and asserts eager tool streaming and beta header behavior are disabled when required.
- inputs_outputs_state: Inputs are catalog model/provider settings and client option builder inputs. Outputs are assertions on option flags/headers. State is test-local.
- gates_or_invariants: Copilot-hosted Anthropic models must not inherit incompatible Anthropic-native beta/tool streaming behavior.
- dependencies_and_callers: Validates catalog/AI provider compatibility behavior.
- edge_cases_or_failure_modes: Host misclassification, beta header leakage, and tool streaming incompatibility.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-720 `file` `packages/coding-agent/scripts/embed-mupdf-wasm.ts`
- cursor: `[_]`
- core_role: Build helper for embedding MuPDF WASM used by document/PDF conversion.
- algorithmic_behavior: Reads MuPDF WASM/package assets from dependencies or build output, encodes or writes them into coding-agent distributable resources, and ensures the markit PDF converter can load MuPDF in packaged environments.
- inputs_outputs_state: Inputs are local MuPDF WASM files and script options/environment. Outputs are embedded WASM asset files or generated source/resource content. State is build filesystem state.
- gates_or_invariants: Embedded asset must match loader expectations and be present in packaged builds; missing source WASM should fail loudly.
- dependencies_and_callers: Supports `packages/coding-agent/src/markit/converters/pdf/extract.ts` and release/build scripts.
- edge_cases_or_failure_modes: Missing dependency asset, stale generated WASM, path resolution differences in source versus packaged binary, and incompatible MuPDF version.
- validation_or_tests: Indirectly covered by PDF read/markit tests and build smoke tests.
- skip_candidate: `yes: build helper, but it enables a runtime PDF algorithm dependency`

### OH_MY_HUMANIZE_MAIN-HZ-750 `file` `packages/coding-agent/test/agent-hub-ordering.test.ts`
- cursor: `[_]`
- core_role: Test coverage for agent hub ordering behavior.
- algorithmic_behavior: Constructs agent hub/session overlay states and asserts row ordering or display ordering remains stable under active/completed/queued agent state changes.
- inputs_outputs_state: Inputs are mock agent/session records. Outputs are ordered arrays/render assertions. State is test-local hub data.
- gates_or_invariants: Agent hub UI/order must be deterministic and preserve expected priority semantics.
- dependencies_and_callers: Validates coding-agent agent hub UI/model logic.
- edge_cases_or_failure_modes: Same timestamp ties, active versus inactive ordering, and overlay state changes.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-780 `file` `packages/coding-agent/test/agent-session-retry-fallback.test.ts`
- cursor: `[_]`
- core_role: Extensive regression coverage for agent session retry and fallback model behavior.
- algorithmic_behavior: Simulates provider failures, retryable/non-retryable outcomes, fallback model selection, session event emission, and assistant message finalization. It asserts fallback requests and transcript state match expected recovery semantics.
- inputs_outputs_state: Inputs are mocked model/provider responses, session options, and failure sequences. Outputs are emitted events, final assistant messages, and captured model requests. State is test session/transcript state.
- gates_or_invariants: Retry fallback should activate only for eligible failures; fallback model requests must carry correct role/thinking/tool state; final transcript must not duplicate or lose assistant output.
- dependencies_and_callers: Validates coding-agent session manager/agent loop integration with `packages/ai`.
- edge_cases_or_failure_modes: Multiple retry attempts, fallback exhaustion, partial stream failure, tool-call interactions, and preserved session metadata.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-810 `file` `packages/coding-agent/test/bash-acp-terminal.test.ts`
- cursor: `[_]`
- core_role: Tests Bash tool routing through ACP terminal bridge behavior.
- algorithmic_behavior: Constructs Bash tool invocations under ACP terminal conditions and asserts commands route through the terminal bridge or normal execution path as configured.
- inputs_outputs_state: Inputs are command arguments, session/tool options, and mock terminal bridge availability. Outputs are captured bridge calls/tool results. State is test mocks.
- gates_or_invariants: Terminal-backed bash execution must preserve command args and not bypass the bridge when ACP terminal mode is active.
- dependencies_and_callers: Validates coding-agent Bash tool and ACP/terminal integration.
- edge_cases_or_failure_modes: Missing bridge, command args with terminal-sensitive content, fallback execution, and result propagation.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-840 `file` `packages/coding-agent/test/countdown-timer.test.ts`
- cursor: `[_]`
- core_role: Unit tests for countdown timer state behavior.
- algorithmic_behavior: Advances timer state under controlled time/mocks and asserts displayed remaining time or completion transitions.
- inputs_outputs_state: Inputs are duration/time advances. Outputs are timer state/render assertions. State is test-local timer instance.
- gates_or_invariants: Countdown must clamp at zero/complete and update consistently.
- dependencies_and_callers: Validates coding-agent timer utility/component.
- edge_cases_or_failure_modes: Boundary at zero, repeated ticks, and cancellation/disposal.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-870 `file` `packages/coding-agent/test/hindsight-bank.test.ts`
- cursor: `[_]`
- core_role: Tests for hindsight bank storage/scope behavior.
- algorithmic_behavior: Creates bank scopes, IDs, git-backed or filesystem-backed data, and asserts ensure/load/update behavior across scope boundaries.
- inputs_outputs_state: Inputs are temp repos/paths, bank entries, and IDs. Outputs are stored/retrieved hindsight records. State is temp filesystem/git state.
- gates_or_invariants: Bank IDs and scopes must isolate records; ensure operations must be idempotent; git integration should not corrupt unrelated state.
- dependencies_and_callers: Validates coding-agent hindsight bank feature.
- edge_cases_or_failure_modes: Missing git repo, duplicate IDs, path scope collisions, and repeated initialization.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-900 `file` `packages/coding-agent/test/interactive-mode-lsp-startup.test.ts`
- cursor: `[_]`
- core_role: Regression tests for interactive mode LSP startup behavior.
- algorithmic_behavior: Runs or simulates interactive startup and asserts language server startup/welcome-banner behavior occurs in the correct order and conditions.
- inputs_outputs_state: Inputs are interactive mode options and mocked LSP/session environment. Outputs are rendered events or startup calls. State is test-local mocks.
- gates_or_invariants: Interactive startup should initialize LSP where appropriate without blocking or corrupting welcome rendering.
- dependencies_and_callers: Validates coding-agent interactive mode and LSP integration.
- edge_cases_or_failure_modes: Disabled LSP, unavailable workspace, race with banner render, and repeated startup.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-930 `file` `packages/coding-agent/test/issue-953-repro.test.ts`
- cursor: `[_]`
- core_role: Issue regression coverage for status/cache indicator behavior.
- algorithmic_behavior: Recreates the issue condition and asserts status line/cache icon output is stable and correct.
- inputs_outputs_state: Inputs are mocked cache/session/model state. Outputs are rendered status line assertions. State is test-local.
- gates_or_invariants: Status indicators must accurately reflect cache/model state without stale icons.
- dependencies_and_callers: Validates coding-agent status line rendering.
- edge_cases_or_failure_modes: Missing cache data, model switch, stale session state, and render refresh timing.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-960 `file` `packages/coding-agent/test/mcp-json-rpc.test.ts`
- cursor: `[_]`
- core_role: Tests MCP JSON-RPC utility behavior.
- algorithmic_behavior: Asserts URL redaction and SSE/JSON-RPC parsing behavior for MCP-related inputs.
- inputs_outputs_state: Inputs are URLs, JSON-RPC/SSE snippets, and parser calls. Outputs are redacted strings and parsed events. State is test-local.
- gates_or_invariants: Sensitive URL components must be redacted; parser must preserve valid JSON-RPC frame semantics.
- dependencies_and_callers: Validates coding-agent MCP utilities/transports.
- edge_cases_or_failure_modes: Tokens in URLs, malformed frames, and SSE framing boundaries.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-990 `file` `packages/coding-agent/test/non-interactive-env.test.ts`
- cursor: `[_]`
- core_role: Tests environment construction for non-interactive execution.
- algorithmic_behavior: Builds non-interactive command/session environments and asserts expected variables are set, omitted, or preserved.
- inputs_outputs_state: Inputs are process/env options and session settings. Outputs are environment maps. State is test-local environment mocks.
- gates_or_invariants: Non-interactive mode must set deterministic env defaults without leaking interactive-only state.
- dependencies_and_callers: Validates coding-agent non-interactive runner.
- edge_cases_or_failure_modes: Existing env collisions, missing terminal vars, CI env, and override behavior.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-1020 `file` `packages/coding-agent/test/role-thinking-helper-propagation.test.ts`
- cursor: `[_]`
- core_role: Tests propagation of role-specific thinking helper settings.
- algorithmic_behavior: Creates model role/session scenarios and asserts thinking helper configuration reaches downstream model calls.
- inputs_outputs_state: Inputs are role config, model config, and mocked calls. Outputs are captured thinking settings. State is test-local.
- gates_or_invariants: Role-specific thinking settings must not be dropped or overwritten during session/model resolution.
- dependencies_and_callers: Validates coding-agent model-role handling and AI request construction.
- edge_cases_or_failure_modes: Default role fallback, missing helper, and conflicting model config.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-1050 `file` `packages/coding-agent/test/session-manager-cwd-adoption.test.ts`
- cursor: `[_]`
- core_role: Tests session manager current-working-directory adoption on resume.
- algorithmic_behavior: Builds/resumes sessions under different cwd contexts and asserts stored/adopted cwd behavior follows expected policy.
- inputs_outputs_state: Inputs are temp workspaces, session records, and resume options. Outputs are session cwd fields and assertions. State is temp session storage.
- gates_or_invariants: Resume must not unexpectedly switch workspace unless adoption rules allow it; stored cwd must remain coherent.
- dependencies_and_callers: Validates coding-agent session manager.
- edge_cases_or_failure_modes: Deleted cwd, moved workspace, relative paths, and resume from different shell cwd.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-1080 `file` `packages/coding-agent/test/status-line-token-rate.test.ts`
- cursor: `[_]`
- core_role: Tests status line token-rate calculation.
- algorithmic_behavior: Feeds usage/timing samples into status line logic and asserts token-per-second display or computation.
- inputs_outputs_state: Inputs are token counts and timestamps. Outputs are rendered rate strings or numeric rates. State is test-local timing data.
- gates_or_invariants: Rate should avoid divide-by-zero, stale values, and incorrect unit display.
- dependencies_and_callers: Validates coding-agent status line.
- edge_cases_or_failure_modes: Zero elapsed time, missing usage, very small/large rates, and update ordering.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-1110 `file` `packages/coding-agent/test/tool-execution-args.test.ts`
- cursor: `[_]`
- core_role: Tests tool execution argument update behavior.
- algorithmic_behavior: Exercises `updateArgs` or equivalent tool-call state mutation and asserts reference-equality fast paths or replacement semantics.
- inputs_outputs_state: Inputs are tool argument objects/updates. Outputs are updated execution state and assertions. State is test-local tool execution object.
- gates_or_invariants: Identical args should avoid unnecessary churn; changed args must propagate accurately.
- dependencies_and_callers: Validates coding-agent tool execution UI/state controller.
- edge_cases_or_failure_modes: Partial streamed args, same reference versus equal value, and stale render state.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-1140 `file` `packages/collab-web/test/local-relay.test.ts`
- cursor: `[_]`
- core_role: Tests local relay behavior for collaboration web integration.
- algorithmic_behavior: Starts or mocks relay endpoints, sends local messages/requests, and asserts routing, connection handling, and response behavior.
- inputs_outputs_state: Inputs are test HTTP/WebSocket or relay messages. Outputs are relay responses/events. State is local server/test connection state.
- gates_or_invariants: Relay should route only valid local traffic, preserve message payloads, and clean up connections.
- dependencies_and_callers: Validates collab-web local relay code.
- edge_cases_or_failure_modes: Connection close, invalid payload, multiple clients, and cleanup after test.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-1170 `file` `packages/hashline/test/snapshots.test.ts`
- cursor: `[_]`
- core_role: Validation coverage for hashline snapshot storage.
- algorithmic_behavior: Creates snapshot store entries, promotes heads, merges seen-line metadata, invalidates paths, and forces LRU eviction conditions.
- inputs_outputs_state: Inputs are path/content/hash/seen-line records. Outputs are retrieved snapshots and store state assertions. State is in-memory snapshot store.
- gates_or_invariants: Hash format and head tracking must be stable; dedupe must avoid duplicate versions; seen-line unions must preserve observed lines; max path/version/byte limits must evict deterministically.
- dependencies_and_callers: Validates `packages/hashline/src/snapshots.ts`, which read/edit flows rely on.
- edge_cases_or_failure_modes: Duplicate content, invalidation, version promotion, and LRU pressure.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-1200 `file` `packages/mnemopi/test/e5a-vector-voice-dense-rewire.test.ts`
- cursor: `[_]`
- core_role: Regression coverage for mnemopi vector voice dense rewiring.
- algorithmic_behavior: Sets up vector/voice dense data path scenarios and asserts rewired dense-vector behavior still returns expected memory/search results.
- inputs_outputs_state: Inputs are synthetic memory/vector records and model/voice config. Outputs are recall/search assertions. State is temp mnemopi storage.
- gates_or_invariants: Dense vector routing must preserve recall semantics across rewiring.
- dependencies_and_callers: Validates `packages/mnemopi` vector storage/recall implementation.
- edge_cases_or_failure_modes: Missing dense vectors, dimension mismatch, and changed provider embedding shape.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-1230 `file` `packages/mnemopi/test/recall-diagnostics.test.ts`
- cursor: `[_]`
- core_role: Tests diagnostic reporting for mnemopi recall.
- algorithmic_behavior: Executes recall/search scenarios and asserts diagnostic counters/details are emitted for recall stages.
- inputs_outputs_state: Inputs are stored memories, query vectors/text, and diagnostic options. Outputs are recall results plus diagnostics. State is test storage/index state.
- gates_or_invariants: Diagnostics must reflect actual candidate/filter/ranking stages without changing recall results.
- dependencies_and_callers: Validates mnemopi recall pipeline.
- edge_cases_or_failure_modes: Empty memory set, filtered-out candidates, vector mismatch, and missing diagnostic fields.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-1260 `file` `packages/natives/test/windows-staging.test.ts`
- cursor: `[_]`
- core_role: Tests native package staging behavior on Windows-like packaging paths.
- algorithmic_behavior: Simulates native loader/staging scenarios, version sentinels, and path expectations to ensure native artifacts are copied/resolved correctly.
- inputs_outputs_state: Inputs are temp native package layouts and platform/path mocks. Outputs are staged files and loader assertions. State is temp filesystem state.
- gates_or_invariants: Native staging must honor version sentinel and avoid stale binary reuse; Windows path conventions must work.
- dependencies_and_callers: Validates `packages/natives` loader/staging code.
- edge_cases_or_failure_modes: Stale sentinel, missing binary, path separators, and repeated staging.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-1290 `file` `packages/snapcompact/research/exp18_bestkimi.py`
- cursor: `[_]`
- core_role: Experimental research script for snapcompact model/layout evaluation.
- algorithmic_behavior: Runs cached model calls, formats text/page layouts, renders images or visual records through PIL-style drawing, evaluates units, and aggregates experiment records.
- inputs_outputs_state: Inputs are experiment datasets, cached model responses, render parameters, and output directories. Outputs are evaluation records, rendered artifacts, and summary metrics. State includes cache files and experiment outputs.
- gates_or_invariants: Caching should avoid repeated expensive calls; layout/rendering must be deterministic for comparable experiment results.
- dependencies_and_callers: Research-only path under `packages/snapcompact/research`; depends on Python imaging/model/eval utilities.
- edge_cases_or_failure_modes: Missing cache/model key, font/render differences, dataset format drift, and nondeterministic model output.
- validation_or_tests: No runtime tests inspected; script is an experiment artifact.
- skip_candidate: `yes: research script, not production runtime core`

### OH_MY_HUMANIZE_MAIN-HZ-1320 `file` `packages/snapcompact/research/snapcompact_r2_chord.py`
- cursor: `[_]`
- core_role: Research visualization script for snapcompact results.
- algorithmic_behavior: Computes chord/ribbon geometry, allocates arcs, builds Bezier-like ribbons, and renders relationship diagrams from experiment result data.
- inputs_outputs_state: Inputs are result/category data and render dimensions/styles. Outputs are visualization images or files. State is local geometry/render structures.
- gates_or_invariants: Arc allocation and ribbon paths must be deterministic and non-overlapping enough to read.
- dependencies_and_callers: Research-only visualization support for snapcompact experiments.
- edge_cases_or_failure_modes: Empty categories, extreme weights, overlapping labels, and render backend/font differences.
- validation_or_tests: No direct tests inspected.
- skip_candidate: `yes: research visualization, not production runtime core`

### OH_MY_HUMANIZE_MAIN-HZ-1350 `file` `packages/stats/src/server.ts`
- cursor: `[_]`
- core_role: Bun HTTP server for the local stats dashboard.
- algorithmic_behavior: Resolves embedded client assets from base64 tar/gzip, safely extracts them to a cache directory, builds client assets from source when needed, serves static files, and exposes JSON API routes for stats overview, model dashboard, costs, behavior, recent sessions, details, errors, sync/message counts, and server lifecycle.
- inputs_outputs_state: Inputs are stats database/service options, embedded client asset, source client tree, HTTP requests, and server config. Outputs are static responses, JSON API responses, and listening server. State includes extracted asset cache, build freshness, and Bun server handle.
- gates_or_invariants: Archive extraction must prevent path traversal; compiled/prebuilt mode should prefer embedded assets; source build should run when stale; API route matching must return stable JSON shapes.
- dependencies_and_callers: Used by `omp stats` or stats package entrypoints. Depends on Bun server APIs, generated client bundle, stats data modules, filesystem/tar/gzip.
- edge_cases_or_failure_modes: Missing embedded client, stale build, malicious archive paths, port binding failure, missing stats DB, and API route errors.
- validation_or_tests: Covered indirectly by stats package tests/build smoke; no direct test inspected here.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1380 `file` `packages/tui/src/loop-watchdog.ts`
- cursor: `[_]`
- core_role: Event-loop lag watchdog for TUI responsiveness diagnostics.
- algorithmic_behavior: Schedules periodic timers, compares actual versus expected wake time, records loop phase history, and logs warnings/details when lag exceeds configured thresholds.
- inputs_outputs_state: Inputs are watchdog options, timer ticks, phase markers, and logger. Outputs are diagnostic log entries. State includes running timer, last tick time, threshold config, and recent phase ring/history.
- gates_or_invariants: Watchdog must avoid excessive logging, stop cleanly, and measure lag relative to monotonic performance time.
- dependencies_and_callers: Used by TUI/runtime loops to diagnose stalls; depends on logger/performance timers.
- edge_cases_or_failure_modes: Timer drift under heavy load, duplicate start/stop, missing phase metadata, and false positives during process suspension.
- validation_or_tests: Indirectly covered by TUI runtime tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1410 `file` `packages/tui/test/issue-2088-repro.test.ts`
- cursor: `[_]`
- core_role: Regression tests for terminal resize/render race behavior.
- algorithmic_behavior: Simulates virtual terminal or tmux resize conditions, ED3/clear behavior, debounce timing, and multiplexer detection to reproduce issue 2088.
- inputs_outputs_state: Inputs are terminal size changes, render operations, and environment/multiplexer flags. Outputs are terminal buffer/render assertions. State is virtual terminal/test renderer state.
- gates_or_invariants: Resize should not corrupt render output; ED3/clear behavior must be gated correctly under multiplexers.
- dependencies_and_callers: Validates TUI renderer and terminal capability code.
- edge_cases_or_failure_modes: Rapid resize, tmux/screen detection, delayed clears, and stale dimensions.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-1440 `file` `packages/tui/test/render-stress-reducer.ts`
- cursor: `[_]`
- core_role: Debug/reduction utility for TUI render stress failures.
- algorithmic_behavior: Takes failing render replay operations, delta-reduces operation sequences, and attempts to preserve the failure while minimizing reproduction input.
- inputs_outputs_state: Inputs are recorded render operations and failure predicate/replay harness. Outputs are reduced operation sequences. State is reducer iteration state and temporary replay artifacts.
- gates_or_invariants: Reduction must only discard chunks when the failure still reproduces.
- dependencies_and_callers: Developer test/debug tooling for TUI rendering.
- edge_cases_or_failure_modes: Nondeterministic failures, expensive replay loops, and false reductions from flaky predicates.
- validation_or_tests: It is itself a validation helper.
- skip_candidate: `yes: test utility, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-1470 `file` `packages/typescript-edit-benchmark/src/generate.ts`
- cursor: `[_]`
- core_role: Benchmark fixture generator for TypeScript edit tasks.
- algorithmic_behavior: Clones or reads source repositories, selects TypeScript/JavaScript files, applies controlled mutations, formats or diffs results, and packages generated benchmark cases into archives/datasets.
- inputs_outputs_state: Inputs are source repo URL/path, selection parameters, mutation config, formatter/tooling availability, and output path. Outputs are benchmark fixture files, diffs, metadata, and archive. State includes temp clone/work directories and generated case metadata.
- gates_or_invariants: Generated tasks should be reproducible; mutations must produce meaningful edit diffs; source selection should avoid unsuitable files; packaging should include enough metadata for benchmark replay.
- dependencies_and_callers: Used by benchmark tooling, not main coding-agent runtime. Depends on Bun shell/filesystem, git, formatter/compiler tools, and TypeScript file parsing heuristics.
- edge_cases_or_failure_modes: Clone failure, huge files, formatter errors, no eligible files, mutation producing no diff, and nondeterministic source state.
- validation_or_tests: No direct tests inspected.
- skip_candidate: `yes: benchmark generator, not application runtime core`

### OH_MY_HUMANIZE_MAIN-HZ-1500 `file` `packages/utils/src/peek-file.ts`
- cursor: `[_]`
- core_role: Efficient file header/tail peeking utility with pooled buffers.
- algorithmic_behavior: Provides sync and async `peekFile` variants that read only the first N bytes, tail bytes, or both file ends. Async path uses a fixed pool of 512-byte buffers with a bounded waiter queue before allocating; sync path uses growable reusable buffers. File handles are closed in `finally`.
- inputs_outputs_state: Inputs are file paths, max byte counts, and callback operations over `Uint8Array` slices. Outputs are callback return values. State includes async buffer pool indexes, waiter queue, and sync buffer cache.
- gates_or_invariants: Must not leak file descriptors; callback only sees valid bytes read; pool indexes must be returned; tail reads must clamp to file size.
- dependencies_and_callers: Shared utility for content sniffing and lightweight file classification.
- edge_cases_or_failure_modes: Empty files, small files shorter than requested bytes, concurrent async pressure, read errors, stat/open race, and callback exceptions.
- validation_or_tests: Indirectly covered by consumers; no direct test inspected.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1530 `file` `packages/utils/test/profiles.test.ts`
- cursor: `[_]`
- core_role: Tests profile path/name/environment handling in shared utils.
- algorithmic_behavior: Creates profile scenarios and asserts profile directory resolution, import behavior, env handling, and invalid-name rejection.
- inputs_outputs_state: Inputs are profile names, env vars, temp directories, and config files. Outputs are resolved profile paths/configs and thrown errors. State is temp filesystem/env mocks.
- gates_or_invariants: Profile names must be safe; environment overrides must be deterministic; imports must not escape expected profile roots.
- dependencies_and_callers: Validates `packages/utils` profile helpers used by CLI/runtime packages.
- edge_cases_or_failure_modes: Invalid characters, missing profile, env collisions, and import path traversal.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-1560 `file` `python/robomp/src/logging_config.py`
- cursor: `[_]`
- core_role: Logging configuration for the Python robomp service/tools.
- algorithmic_behavior: Configures idempotent logging with pretty ANSI console output, JSON rotating file handlers, log-level controls, and filtering of noisy dashboard polling/uvicorn access logs.
- inputs_outputs_state: Inputs are config/environment options, log records, output paths, and reset/test flags. Outputs are console log lines and JSON log files. State is Python logging handler/filter configuration.
- gates_or_invariants: Configuration should be idempotent, avoid duplicate handlers, maintain structured JSON for files, and filter only known-noisy records.
- dependencies_and_callers: Used by robomp Python runtime and tests.
- edge_cases_or_failure_modes: Reconfiguration during tests, missing log dir, handler duplication, malformed records, and over-filtering useful access logs.
- validation_or_tests: Covered indirectly by robomp tests and any logging-specific assertions.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1590 `file` `python/robomp/tests/test_sandbox.py`
- cursor: `[_]`
- core_role: Large integration/regression test suite for robomp sandbox/workspace management.
- algorithmic_behavior: Exercises workspace key creation, branch rename, permission/chown behavior, slot process cleanup, temp/runtime env handling, git safe.directory, metadata sharing, idempotent workspace ensure, PR head handling, partial clone blob backfill, native cache sharing, removal, redaction, push semantics, and hung child termination.
- inputs_outputs_state: Inputs are temp repos, sandbox configs, git remotes/branches, process fixtures, and filesystem permissions. Outputs are workspace state, process state, git refs, and assertions. State is extensive temp sandbox filesystem/process state.
- gates_or_invariants: Sandboxes must isolate workspaces, safely manage ownership/permissions, clean child processes, preserve metadata, and avoid unsafe git operations.
- dependencies_and_callers: Validates Python robomp sandbox implementation.
- edge_cases_or_failure_modes: Partial clone missing blobs, stale pid files, branch rename, permission errors, unsafe git config, hung processes, and redaction leaks.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-1620 `directory` `packages/coding-agent/src/eval/py`
- cursor: `[_]`
- core_role: Python execution and kernel bridge for coding-agent eval/tool workflows.
- algorithmic_behavior: Spawns a Python runner/kernel, injects prelude helpers, streams execution status/display/result events, converts Python display outputs into markdown/text structures, exposes a tool bridge callable from Python, and manages runtime lifecycle/cancellation/cleanup.
- inputs_outputs_state: Inputs are Python source/code cells, runtime options, spawn environment, tool-call requests, and stdin/stdout event streams. Outputs are execution results, display events, tool-call results, diagnostics, and cleanup status. State includes running process/kernel session, pending request IDs, bridge callbacks, and runtime resources.
- gates_or_invariants: Runner protocol messages must stay framed/typed; cancellation must terminate the right process; tool bridge must serialize arguments/results safely; prelude must be loaded before user code.
- dependencies_and_callers: Used by coding-agent eval features. Depends on Bun process APIs, Python runner scripts, prelude files, and session tool execution bridge.
- edge_cases_or_failure_modes: Python missing, runner crash, malformed JSON event, long-running code, display payload too large, tool error propagation, and cleanup after cancellation.
- validation_or_tests: `packages/coding-agent/src/eval/py/__tests__/prelude.test.ts` covers prelude contracts; broader behavior is covered by eval/session tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1650 `directory` `packages/collab-web/src/components/agents`
- cursor: `[_]`
- core_role: Collaboration web UI components for displaying and controlling agent sessions.
- algorithmic_behavior: `AgentsPanel.tsx` computes visible agent rows, activity/status text, and ordering from active tool/session state. `AgentDrawer.tsx` polls transcript data, parses JSONL, renders messages/tool activity, and provides cancel/retry/send controls. CSS defines layout and status presentation.
- inputs_outputs_state: Inputs are agent/session records, transcript endpoints, user actions, and polling responses. Outputs are React UI, API calls for control actions, and parsed transcript render state. State is component local selection, polling, loading, transcript, and action states.
- gates_or_invariants: Agent rows must remain stable and readable; transcript polling should handle malformed/partial data; control actions must target the correct agent/session.
- dependencies_and_callers: Used by collab-web app pages; consumes server APIs and tool-render components.
- edge_cases_or_failure_modes: Missing transcript, failed poll, active tool timestamp absent, canceled/retried race, and malformed JSONL.
- validation_or_tests: Covered indirectly by collab-web tests and UI behavior.
- skip_candidate: `yes: UI components with light state logic, not core algorithmic backend`

### OH_MY_HUMANIZE_MAIN-HZ-1680 `file` `packages/agent/src/compaction/pruning.ts`
- cursor: `[_]`
- core_role: Agent context compaction pruning algorithm.
- algorithmic_behavior: Selects/prunes conversation/context items to fit budgets while preserving required anchors such as system/developer instructions, recent turns, tool-call/result consistency, and compaction summary requirements.
- inputs_outputs_state: Inputs are agent context entries, token budgets, pruning options, and message/tool metadata. Outputs are pruned context plus accounting/diagnostics. State is local scoring/selection sets during pruning.
- gates_or_invariants: Must not break tool call/result pairing; protected instructions and required recent context must survive; budget enforcement should be deterministic.
- dependencies_and_callers: Used by `packages/agent` compaction pipeline and coding-agent sessions when context needs pruning.
- edge_cases_or_failure_modes: Oversized protected messages, orphaned tool results, empty removable set, inaccurate token estimates, and ordering preservation.
- validation_or_tests: Covered by agent compaction/session tests where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1710 `file` `packages/ai/src/dialect/history.ts`
- cursor: `[_]`
- core_role: Dialect-neutral history encoder for tool calls and tool results.
- algorithmic_behavior: Converts internal conversation/tool events into provider-compatible message sequences, including assistant tool-call messages and tool result messages, while preserving IDs and content ordering.
- inputs_outputs_state: Inputs are internal message/history objects and dialect capabilities. Outputs are provider-facing history entries. State is local conversion context.
- gates_or_invariants: Tool call IDs must match tool result IDs; assistant/tool role ordering must remain provider-valid; empty or unsupported content must be handled consistently.
- dependencies_and_callers: Used by AI provider adapters before request serialization.
- edge_cases_or_failure_modes: Missing tool result, multiple tool calls in one assistant message, empty content, and provider dialect mismatch.
- validation_or_tests: Covered indirectly by provider wire tests and issue repros.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1740 `file` `packages/ai/src/providers/google-vertex.ts`
- cursor: `[_]`
- core_role: Google Vertex AI provider stream adapter.
- algorithmic_behavior: Builds Vertex endpoint URLs from project/location/model, resolves access token or API key from options/environment, maps request options into shared Google stream handling, and streams model responses back through the common AI event interface.
- inputs_outputs_state: Inputs are model ID, project/location/base options, credentials, messages, and stream options. Outputs are AI stream events/results. State is resolved auth/project/location config for the call.
- gates_or_invariants: Project and location must be resolvable for Vertex calls; credentials must be present in an accepted form; endpoint path must match Vertex API expectations.
- dependencies_and_callers: Used by AI registry/provider selection for Google Vertex models; delegates to shared Google provider code.
- edge_cases_or_failure_modes: Missing project/location, expired token, wrong regional endpoint, model ID needing escaping, and stream/network errors.
- validation_or_tests: Covered indirectly by provider tests and catalog host tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1770 `file` `packages/ai/src/registry/azure.ts`
- cursor: `[_]`
- core_role: Azure provider registry descriptor.
- algorithmic_behavior: Exports or defines Azure registry metadata used to configure an OpenAI-compatible/Azure provider entry.
- inputs_outputs_state: Inputs are registry import/lookup. Outputs are provider descriptor metadata. No meaningful runtime state in the file.
- gates_or_invariants: Descriptor fields must align with provider registry expectations.
- dependencies_and_callers: Used by AI registry construction.
- edge_cases_or_failure_modes: Incorrect descriptor export breaks Azure model configuration/import.
- validation_or_tests: Covered indirectly by registry/import/type checks.
- skip_candidate: `yes: thin descriptor/export file`

### OH_MY_HUMANIZE_MAIN-HZ-1800 `file` `packages/ai/src/registry/ollama.ts`
- cursor: `[_]`
- core_role: Ollama provider login/registry integration.
- algorithmic_behavior: Provides `loginOllama` style flow that prompts or resolves API base/key information and returns configured provider auth/base settings; exports provider descriptor metadata.
- inputs_outputs_state: Inputs are existing config, prompt answers, base URL, and optional API key. Outputs are registry/login result for Ollama. State is provider config chosen by the user.
- gates_or_invariants: Base URL must be captured consistently; API key may be optional for local Ollama; descriptor must match registry schema.
- dependencies_and_callers: Used by AI provider registry and login commands.
- edge_cases_or_failure_modes: Empty base URL, unavailable local server, user cancellation, and malformed config.
- validation_or_tests: Covered indirectly by registry/login tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1830 `file` `packages/ai/src/registry/zhipu-coding-plan.ts`
- cursor: `[_]`
- core_role: Zhipu coding-plan provider registry/login integration.
- algorithmic_behavior: Opens browser/manual API-key flow, validates credentials with a target model such as `glm-5.1`, and returns provider configuration/descriptor.
- inputs_outputs_state: Inputs are user API key, login prompt/browser state, and validation request result. Outputs are stored provider credential/config. State is login attempt state.
- gates_or_invariants: API key validation must succeed before accepting login; provider descriptor must identify supported model/API.
- dependencies_and_callers: Used by AI registry login flow.
- edge_cases_or_failure_modes: Browser unavailable, user cancellation, invalid API key, validation network failure, and model endpoint drift.
- validation_or_tests: Covered indirectly by registry/login tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1860 `file` `packages/ai/src/utils/sse-debug.ts`
- cursor: `[_]`
- core_role: SSE debug observation helper.
- algorithmic_behavior: Normalizes raw SSE frame/event information and forwards it to an optional observer for logging/debugging without changing stream processing.
- inputs_outputs_state: Inputs are raw event names/data/chunks and observer callbacks. Outputs are observer notifications. No persistent state except call-local normalized event objects.
- gates_or_invariants: Debug hooks must be side-effect-light and tolerate absent observers.
- dependencies_and_callers: Used by AI provider SSE stream implementations and tested by `packages/ai/test/sse-debug.test.ts`.
- edge_cases_or_failure_modes: Malformed data, empty event name, observer throwing, and high-volume debug traffic.
- validation_or_tests: `packages/ai/test/sse-debug.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1890 `file` `packages/catalog/src/provider-models/google.ts`
- cursor: `[_]`
- core_role: Google-family provider model manager configuration.
- algorithmic_behavior: Creates model manager options for Google, Vertex, Antigravity, and Gemini CLI providers; bridges provider-specific fetch/auth settings; enables dynamic model discovery when credentials exist; maps Gemini CLI/Antigravity discovered models into provider/base URL metadata.
- inputs_outputs_state: Inputs are provider descriptors, API tokens/keys, fetch implementation, and discovery options. Outputs are model manager configuration and discovered model specs. State is discovery/cache managed by the model manager.
- gates_or_invariants: Discovery should only run when required credentials/config exist; provider/baseUrl mapping must distinguish Google API, Vertex, Antigravity, and Gemini CLI shapes.
- dependencies_and_callers: Used by catalog provider-model infrastructure and generator/runtime refresh.
- edge_cases_or_failure_modes: Missing credentials, wrong host mapping, discovery fetch failure, and stale Antigravity/Gemini CLI metadata.
- validation_or_tests: Covered by catalog provider tests and discovery tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1920 `file` `packages/coding-agent/src/capability/instruction.ts`
- cursor: `[_]`
- core_role: Capability descriptor for externally supplied instructions.
- algorithmic_behavior: Defines an `Instruction` shape and registers it with the capability system so instruction content can be contributed/consumed through a typed capability channel.
- inputs_outputs_state: Inputs are instruction records/content. Outputs are capability registration metadata and typed values. No complex runtime state.
- gates_or_invariants: Instruction records must conform to the capability schema and stable identifier.
- dependencies_and_callers: Used by coding-agent capability framework and instruction loading.
- edge_cases_or_failure_modes: Missing instruction fields, duplicate capability names, and downstream consumers assuming absent metadata.
- validation_or_tests: Covered indirectly by capability/instruction loading tests.
- skip_candidate: `yes: small descriptor, minimal algorithmic behavior`

### OH_MY_HUMANIZE_MAIN-HZ-1950 `file` `packages/coding-agent/src/cli/models-cli.ts`
- cursor: `[_]`
- core_role: CLI implementation for listing, finding, refreshing, and canonicalizing models.
- algorithmic_behavior: Parses model CLI actions, formats provider/model tables or JSON, groups/sorts models by provider and ID, renders canonical model mappings, invokes registry refresh where requested, and handles action aliases.
- inputs_outputs_state: Inputs are CLI args, model registry/catalog data, refresh options, and output mode. Outputs are stdout table/JSON lines and refresh effects. State is model registry/cache state loaded by dependencies.
- gates_or_invariants: Unknown actions must be rejected; table widths/limits must be stable; JSON output must serialize model metadata consistently; refresh should not run for pure listing unless requested.
- dependencies_and_callers: Called by coding-agent CLI command registry. Depends on `@oh-my-pi/pi-catalog` model registry/identity helpers and Bun/console output.
- edge_cases_or_failure_modes: Unknown provider, empty model list, pattern no-match, refresh failure, and wide names/limits.
- validation_or_tests: Covered indirectly by CLI/model tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-1980 `file` `packages/coding-agent/src/commands/complete.ts`
- cursor: `[_]`
- core_role: Shell completion command implementation.
- algorithmic_behavior: Parses completion context, resolves possible completions such as models/sessions/commands, cleans/escapes output lines, and writes completion candidates for shell integration.
- inputs_outputs_state: Inputs are shell completion argv/env and available command/model/session data. Outputs are newline-delimited completion strings. State is transient completion context.
- gates_or_invariants: Completion output must be shell-safe, not include UI noise, and respect the current word/action context.
- dependencies_and_callers: Used by CLI completion integration; depends on model/session command registries.
- edge_cases_or_failure_modes: Partial words with spaces, missing session store, unknown shell/action, and stale model registry.
- validation_or_tests: Covered indirectly by CLI tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2010 `file` `packages/coding-agent/src/commit/pipeline.ts`
- cursor: `[_]`
- core_role: Commit command pipeline coordinating legacy and agentic commit generation.
- algorithmic_behavior: Delegates to agentic commit mode unless legacy mode is requested; legacy mode stages files when needed, optionally proposes changelog changes, gathers git diff/stat/numstat/recent commits/context files, chooses map-reduce for large diffs, validates analysis, and retries summary generation.
- inputs_outputs_state: Inputs are git repo state, commit options, staged/unstaged diff, changelog settings, model/session config, and prompt context. Outputs are generated commit message/changelog changes and potentially staged commit artifacts. State includes gathered diff context and retry attempts.
- gates_or_invariants: Should not commit without meaningful changes; large diffs use map-reduce; summary validation must pass before finalizing; staged state is respected.
- dependencies_and_callers: Used by coding-agent `/commit` or CLI commit command. Depends on git shell operations, prompt/model helpers, changelog tool, and map-reduce pipeline.
- edge_cases_or_failure_modes: No changes, huge diffs, binary files, git command failure, invalid generated summary, changelog conflicts, and model failure.
- validation_or_tests: Covered by commit pipeline/map-reduce/tool tests where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2040 `file` `packages/coding-agent/src/debug/raw-sse.ts`
- cursor: `[_]`
- core_role: TUI/debug view for raw SSE stream frames.
- algorithmic_behavior: Receives raw SSE/debug events, sanitizes and truncates lines, optionally pretty-prints smaller JSON data payloads, and renders framed stream diagnostics for developers.
- inputs_outputs_state: Inputs are SSE event records/data chunks and render dimensions. Outputs are TUI render nodes/text. State is accumulated/debug event list if held by caller/component.
- gates_or_invariants: Must sanitize raw remote text for terminal display; should avoid rendering huge payloads verbatim; JSON pretty printing must fall back safely.
- dependencies_and_callers: Used by coding-agent debug modes; depends on TUI components and SSE debug hooks.
- edge_cases_or_failure_modes: Very large events, invalid JSON, binary-ish payloads, ANSI/control characters, and narrow terminal widths.
- validation_or_tests: Indirectly covered by debug/render tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2070 `file` `packages/coding-agent/src/edit/index.ts`
- cursor: `[_]`
- core_role: Main edit tool dispatcher and result aggregator.
- algorithmic_behavior: Selects edit mode (`hashline`, `apply_patch`, `patch`, `replace`) from config/env/input, resolves fuzzy behavior, applies single or multi-file edits, wires LSP write-through formatting/diagnostics, aggregates per-file results with partial UI updates, expands `apply_patch` multi-file payloads, and stops same-path sequential entries after first failure.
- inputs_outputs_state: Inputs are edit tool calls, patch/hashline text, filesystem/session, LSP config, approval context, and mode options. Outputs are tool results, file writes, diagnostics, and renderer details. State includes per-entry result aggregation, write-through metadata, and edited path sets.
- gates_or_invariants: Approval path extraction must include all affected files; same-path edit failures block subsequent edits for that path; formatting/diagnostics are deduped; edit mode selection must be deterministic.
- dependencies_and_callers: Used by coding-agent tool execution. Depends on hashline package, patch/apply helpers, LSP service, filesystem invalidation, and tool renderer infrastructure.
- edge_cases_or_failure_modes: Multi-file patch partial failure, fuzzy path mismatch, LSP unavailable, formatting failure, stale hashline snapshot, and unsupported edit mode.
- validation_or_tests: Covered by edit/hashline/apply_patch tests and tool execution tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2100 `file` `packages/coding-agent/src/extensibility/tool-proxy.ts`
- cursor: `[_]`
- core_role: Tool proxy descriptor overlay helper for extension/extensibility tooling.
- algorithmic_behavior: Applies proxy metadata/wrappers to an existing tool object so extension-facing descriptors can override or augment the visible tool contract while preserving execution behavior.
- inputs_outputs_state: Inputs are base tool and proxy descriptor/config. Outputs are proxied tool object/descriptor. State is wrapper-local references.
- gates_or_invariants: Proxy must preserve required tool methods/schema while changing only intended descriptor fields.
- dependencies_and_callers: Used by coding-agent extensibility layer for tool wrapping.
- edge_cases_or_failure_modes: Missing base descriptor, incompatible schema override, accidental mutation of shared tool, and lost renderer/details.
- validation_or_tests: Covered indirectly by extensibility/typebox/tool tests.
- skip_candidate: `yes: small adapter, not a standalone core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-2130 `file` `packages/coding-agent/src/internal-urls/rule-protocol.ts`
- cursor: `[_]`
- core_role: Internal URL protocol support for rule resources.
- algorithmic_behavior: Parses or resolves `rule://` internal URLs into rule content/resources so read/navigation paths can access generated or configured rules.
- inputs_outputs_state: Inputs are internal URL strings and rule registry/session context. Outputs are resolved rule content or errors. State is caller-provided rule source data.
- gates_or_invariants: URL scheme/path must be validated; unresolved rules should fail clearly; protocol should not escape into arbitrary filesystem paths.
- dependencies_and_callers: Used by coding-agent internal URL handling and read tool.
- edge_cases_or_failure_modes: Malformed URL, missing rule, percent-encoding, and stale rule registry.
- validation_or_tests: Covered indirectly by rule/internal URL tests such as modes controller rule tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2160 `file` `packages/coding-agent/src/mcp/render.ts`
- cursor: `[_]`
- core_role: Renderer for MCP tool calls/results in the coding-agent TUI.
- algorithmic_behavior: Formats MCP server/tool names, arguments, result content, errors, and output blocks into sanitized TUI display with truncation and path/text cleanup.
- inputs_outputs_state: Inputs are MCP call/result objects and render context. Outputs are TUI nodes/text. State is render-local formatting decisions.
- gates_or_invariants: Raw tool output and errors must be sanitized; long content must be truncated; render paths should handle both pending and completed calls.
- dependencies_and_callers: Used by coding-agent MCP integration and tool execution UI.
- edge_cases_or_failure_modes: Malformed JSON args, huge result content, binary/control text, missing server/tool metadata, and error objects with embedded file content.
- validation_or_tests: Covered indirectly by MCP tests and TUI render tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2190 `file` `packages/coding-agent/src/modes/oauth-manual-input.ts`
- cursor: `[_]`
- core_role: In-memory coordination for manual OAuth input requests.
- algorithmic_behavior: Tracks pending OAuth manual-input prompts, lets callers claim/resolve them, and manages request lifecycle so UI and auth flows can rendezvous.
- inputs_outputs_state: Inputs are pending OAuth request descriptors and submitted manual values. Outputs are claimed request records or resolved inputs. State is module-level pending/claimed request map or queue.
- gates_or_invariants: A pending request should be claimed/resolved once; stale or missing request IDs must be handled predictably.
- dependencies_and_callers: Used by coding-agent OAuth login modes and provider registry flows requiring manual code/token input.
- edge_cases_or_failure_modes: Multiple simultaneous OAuth prompts, user cancellation, stale claims, and duplicate submission.
- validation_or_tests: Covered indirectly by OAuth/login tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2220 `file` `packages/coding-agent/src/session/indexed-session-storage.ts`
- cursor: `[_]`
- core_role: Indexed asynchronous session storage with sync-looking index operations and serialized backend writes.
- algorithmic_behavior: Maintains an in-memory index of session metadata while queuing filesystem/backend mutations per path. Sync APIs update index immediately and enqueue writes; async APIs await path tails; failed backend writes roll back or surface errors. Supports slicing, rename, unlink, deleting artifacts, writer handles, and draining pending work.
- inputs_outputs_state: Inputs are session records, storage paths, write/delete/rename operations, and backend filesystem calls. Outputs are persisted session files, updated indexes, and returned records. State is index map, path write queues, pending promises, and error state.
- gates_or_invariants: Per-path operations must serialize; index and filesystem must converge or roll back on failure; drain must surface write errors; rename/unlink must update index atomically from caller perspective.
- dependencies_and_callers: Used by coding-agent session manager/storage.
- edge_cases_or_failure_modes: Concurrent writes to same session, backend failure after index update, rename collision, delete during pending write, and process exit with pending queue.
- validation_or_tests: Covered by session-manager tests, usage statistics tests, and cwd adoption tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2250 `file` `packages/coding-agent/src/ssh/sshfs-mount.ts`
- cursor: `[_]`
- core_role: SSHFS mount management helper for remote workspaces.
- algorithmic_behavior: Resolves sshfs availability, constructs mount/control paths and arguments, checks mounted state, mounts/unmounts remote paths, and tracks all mounted paths for cleanup.
- inputs_outputs_state: Inputs are remote SSH target/path, local mount root, sshfs options, and process state. Outputs are mounted directories, unmount actions, and status booleans. State is mounted-path registry.
- gates_or_invariants: Should not mount twice unnecessarily; unmount must target known mount paths; command args must preserve remote path semantics.
- dependencies_and_callers: Used by coding-agent remote workspace features. Depends on `sshfs`, mount utilities, filesystem, and process execution.
- edge_cases_or_failure_modes: Missing sshfs binary, mount already exists, remote unavailable, unmount failure, path spaces, and stale mount registry.
- validation_or_tests: Covered indirectly by remote/ssh feature tests if present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2280 `file` `packages/coding-agent/src/tiny/models.ts`
- cursor: `[_]`
- core_role: Tiny/local model metadata and selection helpers.
- algorithmic_behavior: Defines tiny model identifiers/configuration, resolves available local tiny inference models, maps model names to runtime asset/config requirements, and supports selection for smoke tests or lightweight local inference.
- inputs_outputs_state: Inputs are requested tiny model name/config and environment/runtime availability. Outputs are model descriptors or selection errors. State is static model table plus any resolved availability/cache.
- gates_or_invariants: Unknown model names should fail clearly; model asset paths/config must match tiny inference worker expectations.
- dependencies_and_callers: Used by coding-agent tiny inference worker/smoke test paths.
- edge_cases_or_failure_modes: Missing model asset, unsupported architecture, stale descriptor, and fallback selection mismatch.
- validation_or_tests: Covered by smoke tests that spawn tiny-model subprocesses.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2310 `file` `packages/coding-agent/src/tools/fs-cache-invalidation.ts`
- cursor: `[_]`
- core_role: Filesystem scan cache invalidation hook for tool writes/deletes/renames.
- algorithmic_behavior: Provides helpers to notify native/filesystem caches when paths change so subsequent reads/searches see fresh state.
- inputs_outputs_state: Inputs are changed path(s) and operation type. Outputs are cache invalidation calls. State is native/global fs cache outside this helper.
- gates_or_invariants: Invalidation should run after write-like operations and include affected old/new paths for renames.
- dependencies_and_callers: Used by edit/write/delete/rename tools; depends on native fs cache APIs.
- edge_cases_or_failure_modes: Missing native module, relative versus absolute path mismatch, and forgotten invalidation leading to stale search/read results.
- validation_or_tests: Covered indirectly by tool tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2340 `file` `packages/coding-agent/src/tools/read.ts`
- cursor: `[_]`
- core_role: Main read tool for files, directories, URLs, internal URLs, archives, notebooks, databases, documents, images, and converted formats.
- algorithmic_behavior: Parses selectors/ranges/raw modes, resolves suffix paths and PDF image members, streams file chunks with line/byte limits, formats with line numbers or hashline headers, records hashline full/seen-line context, converts PDF/DOCX/PPTX/XLSX/EPUB through markit, reads directory trees, supports archive/sqlite/notebook/internal URL paths, summarizes code via native helper with per-session LRU cache, and renders sanitized results.
- inputs_outputs_state: Inputs are read path, selector, session/workspace, filesystem, URL/internal URL sources, and render context. Outputs are tool results with content/details, image payloads, warnings, and TUI render nodes. State includes per-session summary cache, suffix match cache, hashline snapshot context, and range expansion state.
- gates_or_invariants: Limits apply to bytes/lines/images; internal agent query extraction cannot combine with line selectors; remote mounts skip suffix fuzzy matching; path resolution must not escape allowed semantics; raw/error/render paths sanitize tabs, paths, and long lines.
- dependencies_and_callers: Used by coding-agent tool execution. Depends on hashline, markit converters, native summarizer, archive/sqlite/notebook readers, web/internal URL handlers, TUI render utilities, and filesystem cache.
- edge_cases_or_failure_modes: Huge files, binary/invalid UTF-8, PDF image placeholder reads, multi-range selectors, remote mount latency, glob timeout, conflicting line/range selectors, URL raw mode, directory truncation, and conversion failures.
- validation_or_tests: Covered by read/fetch/PDF/web/internal URL tests including `read-pdf-line-range.test.ts`, `fetch-raw-mode.test.ts`, and workflow tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2370 `file` `packages/coding-agent/src/tui/hyperlink.ts`
- cursor: `[_]`
- core_role: OSC 8 hyperlink generation and gating for TUI output.
- algorithmic_behavior: Detects hyperlink support from environment/terminal settings, filters unsafe URIs, builds OSC 8 sequences for external/internal/file links, and formats file URIs with optional line/column targets.
- inputs_outputs_state: Inputs are display text, URI/path, line/column, environment, and capability flags. Outputs are hyperlink-wrapped strings or plain fallback text. State is capability detection/cache if present.
- gates_or_invariants: Unsafe URI schemes must be rejected; disabled terminals should not receive OSC 8; file links must encode paths safely.
- dependencies_and_callers: Used by read/tool renderers and TUI components.
- edge_cases_or_failure_modes: Unsupported terminal, nested ANSI/OSC sequences, spaces/special chars in file paths, Windows paths, and malicious URI text.
- validation_or_tests: Covered indirectly by renderer tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2400 `file` `packages/coding-agent/src/utils/sixel.ts`
- cursor: `[_]`
- core_role: Sixel detection/sanitization utility for terminal-safe display.
- algorithmic_behavior: Detects sixel escape sequences, optionally allows passthrough, strips or masks sixel content for safe text rendering, and handles line-level placeholders for image-heavy output.
- inputs_outputs_state: Inputs are terminal output strings and passthrough/sanitize options. Outputs are sanitized strings or sixel-preserving text. State is scan-local escape parser state.
- gates_or_invariants: Raw sixel must not corrupt normal TUI rendering unless explicitly allowed; escape parsing must consume complete image sequences.
- dependencies_and_callers: Used by terminal/tool output renderers.
- edge_cases_or_failure_modes: Incomplete sixel sequence, huge image payload, mixed ANSI and sixel, and terminals without sixel support.
- validation_or_tests: Covered indirectly by terminal/render tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2430 `file` `packages/coding-agent/src/workflow/prompt-source.ts`
- cursor: `[_]`
- core_role: Workflow prompt-source resolver.
- algorithmic_behavior: Resolves node prompt content from inline text, files, state values, human input, templates, or previous outputs; enforces max byte limits, package-root escape prevention, frozen resource rules, parent/latest output selection, JSON serialization for bindings, and content hash snapshotting.
- inputs_outputs_state: Inputs are workflow node definitions, run state, filesystem root/package root, frozen resources, parent outputs, and template bindings. Outputs are resolved prompt text plus metadata/hash or structured errors. State is workflow execution state and frozen resource map.
- gates_or_invariants: File sources must stay inside allowed roots; frozen workflows must use frozen resources; oversized prompts fail; template binding serialization must be deterministic.
- dependencies_and_callers: Used by coding-agent workflow executor. Depends on filesystem, templating, workflow state/output models, and error classes.
- edge_cases_or_failure_modes: Missing file/state/output, path traversal, stale frozen resource hash, huge prompt file, invalid template binding, and ambiguous parent output.
- validation_or_tests: `packages/coding-agent/test/workflow/prompt-source.test.ts` provides detailed coverage.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2460 `file` `packages/coding-agent/test/core/js-tool-bridge.test.ts`
- cursor: `[_]`
- core_role: Tests JavaScript eval tool bridge normalization.
- algorithmic_behavior: Calls bridge helpers with mocked tool results/errors/content and asserts JS-facing return values, error shapes, content extraction, and details handling.
- inputs_outputs_state: Inputs are fake session tools and bridge call arguments. Outputs are normalized JS values or thrown bridge errors. State is test mock session/tool registry.
- gates_or_invariants: Tool bridge must preserve result semantics while producing ergonomic JS values; errors must surface consistently.
- dependencies_and_callers: Validates `packages/coding-agent/src/eval/js/tool-bridge.ts`.
- edge_cases_or_failure_modes: Missing tool, malformed args, tool error result, multi-content result, and details-only result.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-2490 `file` `packages/coding-agent/test/discovery/at-imports.test.ts`
- cursor: `[_]`
- core_role: Tests discovery/import expansion for `@` references.
- algorithmic_behavior: Supplies prompt/content with `@` imports or file references and asserts expansion/resolution behavior, including boundaries and rendered output.
- inputs_outputs_state: Inputs are temp files/workspace and prompt strings. Outputs are expanded prompt content or errors. State is temp discovery context.
- gates_or_invariants: Imports should resolve allowed paths, preserve content semantics, and reject invalid/unsafe references.
- dependencies_and_callers: Validates coding-agent discovery/import expansion code.
- edge_cases_or_failure_modes: Missing file, ambiguous reference, path traversal, nested imports, and binary/large files.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-2520 `file` `packages/coding-agent/test/extensibility/typebox-shim.test.ts`
- cursor: `[_]`
- core_role: Tests TypeBox compatibility shim for extensions.
- algorithmic_behavior: Constructs schemas through the shim and asserts safe parsing/validation behavior matches expected extension API contracts.
- inputs_outputs_state: Inputs are schema definitions and test values. Outputs are parse success/failure objects. State is test-local.
- gates_or_invariants: Extension schema validation must be stable across supported TypeBox-like inputs.
- dependencies_and_callers: Validates coding-agent extensibility type/schema shim.
- edge_cases_or_failure_modes: Optional fields, invalid values, nested schemas, and error reporting shape.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-2550 `file` `packages/coding-agent/test/marketplace/source-resolver.test.ts`
- cursor: `[_]`
- core_role: Tests marketplace/plugin source resolution.
- algorithmic_behavior: Feeds source strings/URLs/package identifiers into resolver and asserts canonical source type/path/ref results.
- inputs_outputs_state: Inputs are marketplace source descriptors. Outputs are resolved source metadata or errors. State is test-local.
- gates_or_invariants: Resolver must distinguish local, git, registry, and URL-like sources without unsafe ambiguity.
- dependencies_and_callers: Validates coding-agent marketplace/plugin resolver.
- edge_cases_or_failure_modes: Ambiguous shorthand, missing ref, invalid URL, path traversal, and unsupported protocol.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-2580 `file` `packages/coding-agent/test/session-manager/usage-statistics.test.ts`
- cursor: `[_]`
- core_role: Tests session usage statistics aggregation.
- algorithmic_behavior: Creates session usage records and asserts aggregate token/cost/model statistics computed by the session manager.
- inputs_outputs_state: Inputs are usage events/session records. Outputs are aggregate statistics. State is temp session storage.
- gates_or_invariants: Aggregation must handle missing usage, multiple models, and session boundaries correctly.
- dependencies_and_callers: Validates coding-agent session manager/statistics integration.
- edge_cases_or_failure_modes: Empty sessions, partial usage, model switch, and duplicate events.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-2610 `file` `packages/coding-agent/test/task/autoload-skills.test.ts`
- cursor: `[_]`
- core_role: Tests automatic skill loading into task sessions.
- algorithmic_behavior: Builds task prompts/config with skill references or matching conditions and asserts required skill files are loaded into session context.
- inputs_outputs_state: Inputs are temp skill directories, task definitions, and session config. Outputs are session instruction/context content. State is temp filesystem/session state.
- gates_or_invariants: Named skills must load exactly when applicable; missing skills should surface controlled errors/fallback; duplicate loading should be avoided.
- dependencies_and_callers: Validates coding-agent task executor skill autoloading.
- edge_cases_or_failure_modes: Missing skill file, duplicate skill names, relative references, and unreadable skill content.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-2640 `file` `packages/coding-agent/test/tools/ask.test.ts`
- cursor: `[_]`
- core_role: Comprehensive Ask tool behavior tests.
- algorithmic_behavior: Exercises blocking/non-blocking questions, option choices, free-form input, cancellation, malformed args, multi-question handling, render output, and auto-resolution timing.
- inputs_outputs_state: Inputs are Ask tool call args and simulated user responses/timeouts. Outputs are tool results, errors, and rendered UI states. State is pending question/session state.
- gates_or_invariants: One to three short questions; valid option structures; blocking calls wait for answer; auto-resolution only when configured; cancellation must settle pending state.
- dependencies_and_callers: Validates Ask tool implementation and docs contract in `docs/tools/ask.md`.
- edge_cases_or_failure_modes: No user response, invalid args, too many questions, canceled pending prompt, and mixed option/free-form responses.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-2670 `file` `packages/coding-agent/test/tools/fetch-raw-mode.test.ts`
- cursor: `[_]`
- core_role: Tests read/fetch raw URL selector behavior.
- algorithmic_behavior: Serves or mocks JSON/feed/URL responses and asserts raw-mode selectors and multi-range URL parsing preserve expected content and ranges.
- inputs_outputs_state: Inputs are URL paths/selectors and mock HTTP responses. Outputs are read tool results. State is test server/mock state.
- gates_or_invariants: Raw selector must avoid converted/summarized output; multi-range URL selectors must parse distinctly from URL punctuation.
- dependencies_and_callers: Validates `packages/coding-agent/src/tools/read.ts` URL/fetch handling.
- edge_cases_or_failure_modes: JSON/feed MIME types, URL fragments/selectors, range parsing ambiguity, and failed fetch.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-2700 `file` `packages/coding-agent/test/tools/read-pdf-line-range.test.ts`
- cursor: `[_]`
- core_role: Regression tests for PDF converted markdown line ranges.
- algorithmic_behavior: Reads a PDF through markit conversion, applies line-range selectors to converted markdown, and asserts selected lines/context match expected behavior.
- inputs_outputs_state: Inputs are PDF fixture/read path and line selectors. Outputs are read tool markdown snippets. State is temp/session read state.
- gates_or_invariants: Converted PDF content must be line-addressable like text; selectors must apply after conversion, not raw binary bytes.
- dependencies_and_callers: Validates read tool plus markit PDF converter.
- edge_cases_or_failure_modes: Page breaks, image placeholders, conversion line numbering drift, and out-of-range selectors.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-2730 `file` `packages/coding-agent/test/tools/web-search-tavily.test.ts`
- cursor: `[_]`
- core_role: Tests Tavily web search provider behavior.
- algorithmic_behavior: Mocks Tavily responses/errors and asserts search provider request/response normalization and error mapping.
- inputs_outputs_state: Inputs are search queries/options and mocked HTTP responses. Outputs are normalized search results or provider errors. State is test-local fetch mocks.
- gates_or_invariants: Provider errors should map to stable tool-facing errors; response fields should normalize consistently.
- dependencies_and_callers: Validates coding-agent web search provider integration.
- edge_cases_or_failure_modes: Missing API key, HTTP error, malformed response, empty results, and timeout.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-2760 `file` `packages/coding-agent/test/workflow/prompt-source.test.ts`
- cursor: `[_]`
- core_role: Detailed tests for workflow prompt-source resolution.
- algorithmic_behavior: Exercises inline/file/state/template/output/human prompt sources, root escape prevention, frozen resources, byte limits, output selection, JSON serialization, and error mapping.
- inputs_outputs_state: Inputs are workflow definitions, temp files, state/output maps, and frozen resource data. Outputs are resolved prompt content or `WorkflowPromptSourceError`. State is temp workflow execution context.
- gates_or_invariants: Prompt sources must be deterministic, bounded, root-safe, and frozen-resource-consistent.
- dependencies_and_callers: Validates `packages/coding-agent/src/workflow/prompt-source.ts`.
- edge_cases_or_failure_modes: Missing source, traversal, oversized file, stale frozen resource, ambiguous parent output, and invalid template data.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-2790 `file` `packages/mnemopi/src/core/binary-vectors.ts`
- cursor: `[_]`
- core_role: Binary/int8 vector quantization, storage, and search helpers for mnemopi memory recall.
- algorithmic_behavior: Determines vector type, quantizes floats to int8, binarizes sign bits, computes Hamming distance with popcount/dimension masks, scores vectors, validates SQL identifiers, stores vectors in SQLite, and searches sorted by score then memory ID.
- inputs_outputs_state: Inputs are float vectors, dimensions, memory IDs, SQLite database/table names, and search options. Outputs are binary/int8 encoded vectors, scores, search results, stats, and persisted rows. State is SQLite table/index contents and in-memory buffers.
- gates_or_invariants: Dimension/type must match stored vector data; SQL identifiers must be validated; search ordering must be deterministic; zero/invalid vectors should not corrupt scoring.
- dependencies_and_callers: Used by `packages/mnemopi` recall/indexing pipeline. Depends on SQLite and vector math helpers.
- edge_cases_or_failure_modes: Dimension mismatch, empty vectors, invalid table name, corrupt stored blob, tie scores, and batch search memory pressure.
- validation_or_tests: Covered by mnemopi vector/recall tests including dense rewire and diagnostics.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2820 `file` `packages/mnemopi/src/core/vector-math.ts`
- cursor: `[_]`
- core_role: Small vector math utility module.
- algorithmic_behavior: Computes cosine similarity by dot product and vector norms, returning a safe fallback for invalid zero-norm or mismatched-length cases.
- inputs_outputs_state: Inputs are numeric arrays/vectors. Output is similarity score. No persistent state.
- gates_or_invariants: Lengths must match and norms must be nonzero for meaningful cosine; invalid cases should not throw unexpectedly.
- dependencies_and_callers: Used by mnemopi ranking/recall algorithms.
- edge_cases_or_failure_modes: Empty vectors, zero vectors, unequal lengths, NaN values, and large arrays.
- validation_or_tests: Covered indirectly by mnemopi recall/vector tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2850 `file` `packages/tui/src/components/markdown.ts`
- cursor: `[_]`
- core_role: Markdown renderer for terminal UI.
- algorithmic_behavior: Extends marked parsing for strict strikethrough, inline/block math, bare math environments, render caching, OSC66 text-sized headings, hyperlinks, color swatches, tables, lists, code blocks, blockquotes, and inline markdown formatting. Converts markdown AST/tokens into width-aware TUI nodes.
- inputs_outputs_state: Inputs are markdown text, render width/theme/options, link/image handlers, and cache keys. Outputs are TUI render nodes/text cells. State includes render cache and token/render-local layout state.
- gates_or_invariants: Rendered text must fit terminal width, sanitize/control ANSI safely, preserve code block content, and avoid malformed markdown crashes.
- dependencies_and_callers: Used throughout coding-agent/TUI renderers for messages, tool results, docs, and web content.
- edge_cases_or_failure_modes: Huge markdown, deeply nested lists, wide Unicode, malformed tables, math delimiters, unsafe links, raw ANSI, and long code lines.
- validation_or_tests: Covered by TUI markdown/render tests and downstream tool rendering tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2880 `directory` `packages/ai/src/registry/oauth/__tests__`
- cursor: `[_]`
- core_role: OAuth registry test coverage, currently for XAI OAuth behavior.
- algorithmic_behavior: Tests token expiry parsing, endpoint validation, refresh flow, and auth-code/token exchange logic for OAuth registry implementations.
- inputs_outputs_state: Inputs are mocked OAuth endpoints, token payloads, expiry fields, and refresh/exchange responses. Outputs are validated auth results or errors. State is test-local fetch/auth mocks.
- gates_or_invariants: Expiry handling should refresh before unsafe token use; endpoint validation must reject bad responses; exchange/refresh payloads must match provider contract.
- dependencies_and_callers: Validates `packages/ai/src/registry/oauth/*` provider auth modules.
- edge_cases_or_failure_modes: Missing expiry, expired token, invalid endpoint response, refresh failure, and malformed token payload.
- validation_or_tests: Directory is validation coverage.
- skip_candidate: `yes: test directory, not runtime implementation`

### OH_MY_HUMANIZE_MAIN-HZ-2910 `file` `crates/pi-shell/src/minimizer/filters/go.rs`
- cursor: `[_]`
- core_role: Go command output minimizer for shell/result compaction.
- algorithmic_behavior: Detects supported Go-related commands, dispatches by subcommand, parses `go test` text/JSON output, aggregates success/failure diagnostics, compacts build/vet/lint noise, and summarizes `golangci-lint` JSON while preserving actionable diagnostics.
- inputs_outputs_state: Inputs are command name/args and stdout/stderr lines. Outputs are minimized shell output and summaries. State is local parsed package/test/diagnostic accumulators.
- gates_or_invariants: Must preserve failures and diagnostics; successful noisy output can be summarized; JSON parsing failures should fall back without hiding raw errors.
- dependencies_and_callers: Used by `pi-shell` command output minimizer.
- edge_cases_or_failure_modes: Mixed stdout/stderr, malformed go test JSON, panic output, package build failures, no tests, and linter JSON schema drift.
- validation_or_tests: Covered by pi-shell minimizer tests if present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2940 `file` `packages/ai/src/registry/oauth/perplexity.ts`
- cursor: `[_]`
- core_role: Perplexity OAuth/login provider integration.
- algorithmic_behavior: First attempts to borrow a macOS app auth token via `defaults read` unless disabled, otherwise performs email OTP login with CSRF/signin/OTP steps. Computes JWT expiry with safety margin and returns provider auth credentials.
- inputs_outputs_state: Inputs are environment flags, macOS defaults token, user email/OTP, HTTP responses, and JWT payload. Outputs are Perplexity auth token/config and expiry metadata. State is login flow cookies/CSRF/token state.
- gates_or_invariants: Borrowed token path must respect opt-out; OTP flow must include CSRF and validated responses; expiry should subtract safety margin or use conservative fallback.
- dependencies_and_callers: Used by AI registry login/auth storage. Depends on platform command access, fetch, JWT parsing, and user prompting.
- edge_cases_or_failure_modes: Non-macOS defaults unavailable, disabled borrow, invalid/expired JWT, OTP failure, CSRF mismatch, network error, and missing email.
- validation_or_tests: Covered indirectly by OAuth registry tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-2970 `file` `packages/coding-agent/src/cli/commands/init-xdg.ts`
- cursor: `[_]`
- core_role: CLI command to initialize XDG directory structure for coding-agent.
- algorithmic_behavior: Resolves config/data/state/cache directories and creates them so later CLI operations have expected storage roots.
- inputs_outputs_state: Inputs are XDG environment/config paths. Outputs are created directories and command status. State is filesystem directory existence.
- gates_or_invariants: Directory creation should be idempotent and respect XDG path resolution.
- dependencies_and_callers: Used by CLI command registry/setup flows.
- edge_cases_or_failure_modes: Permission denied, invalid env path, concurrent creation, and partial directory creation.
- validation_or_tests: Covered indirectly by CLI/profile/storage tests.
- skip_candidate: `yes: setup command with minimal algorithmic logic`

### OH_MY_HUMANIZE_MAIN-HZ-3000 `file` `packages/coding-agent/src/commit/map-reduce/index.ts`
- cursor: `[_]`
- core_role: Entry/export surface for commit map-reduce summarization.
- algorithmic_behavior: Re-exports or wires map-reduce commit analysis modules so large diffs can be summarized in chunks and reduced into final commit guidance.
- inputs_outputs_state: Inputs are imports from commit pipeline. Outputs are exported map-reduce functions/types. Runtime state is held by underlying modules.
- gates_or_invariants: Export surface must expose the expected map-reduce API without ambiguity.
- dependencies_and_callers: Called by `packages/coding-agent/src/commit/pipeline.ts` for large diffs.
- edge_cases_or_failure_modes: Broken export path or missing reducer function breaks large-diff commits.
- validation_or_tests: Covered indirectly by commit pipeline tests.
- skip_candidate: `yes: index/entry file, algorithm lives in child modules`

### OH_MY_HUMANIZE_MAIN-HZ-3030 `file` `packages/coding-agent/src/eval/js/tool-bridge.ts`
- cursor: `[_]`
- core_role: JavaScript eval bridge for invoking coding-agent session tools.
- algorithmic_behavior: Exposes `callSessionTool`-style functionality that looks up active session tools, normalizes arguments, executes the tool, converts `AgentToolResult` content/details into JS-friendly values, and wraps errors consistently.
- inputs_outputs_state: Inputs are tool name, args, active session/tool registry, and execution context. Outputs are JS values or thrown bridge errors. State is active session/tool references and per-call result normalization.
- gates_or_invariants: Only registered tools should be callable; result content/details must map predictably; tool errors should not leak raw internals in unusable shapes.
- dependencies_and_callers: Used by coding-agent JS eval runtime and tested by `core/js-tool-bridge.test.ts`.
- edge_cases_or_failure_modes: Missing tool, invalid args, tool cancellation/error, multi-part content, empty result, and unserializable details.
- validation_or_tests: `packages/coding-agent/test/core/js-tool-bridge.test.ts`.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3060 `file` `packages/coding-agent/src/extensibility/extensions/types.ts`
- cursor: `[_]`
- core_role: Extension API type and event contract surface.
- algorithmic_behavior: Defines extension-facing types, event shapes, tool-call event discriminants, and type guards such as `isToolCallEventType` to classify extension events safely.
- inputs_outputs_state: Inputs are extension event objects and imported type consumers. Outputs are type-level contracts and runtime guard booleans. Minimal runtime state.
- gates_or_invariants: Event discriminants must remain stable for extension compatibility; guards must not overmatch unrelated events.
- dependencies_and_callers: Used by coding-agent extensibility runtime, plugins, and tests.
- edge_cases_or_failure_modes: Extension API drift, missing event variants, and type guard mismatch with runtime events.
- validation_or_tests: Covered by extensibility/typebox/extension tests.
- skip_candidate: `yes: mostly type contract, limited runtime algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3090 `file` `packages/coding-agent/src/mcp/transports/stdio.ts`
- cursor: `[_]`
- core_role: MCP JSON-RPC stdio subprocess transport.
- algorithmic_behavior: Spawns MCP server commands, resolves Windows executables/PATHEXT/cmd shims, reads newline-delimited JSON-RPC frames from stdout, writes frames to stdin while tolerating EPIPE, tracks pending requests with timeouts, dispatches notifications/responses, and manages lifecycle/close.
- inputs_outputs_state: Inputs are command/args/env/cwd, JSON-RPC requests, timeout config, and process output. Outputs are JSON-RPC responses/events, process errors, and close notifications. State includes child process, pending request map, frame reader loop, and closed/error flags.
- gates_or_invariants: Request IDs must match pending promises; frames must be valid JSON-RPC; write after close/EPIPE should not crash; process cleanup must settle pending requests.
- dependencies_and_callers: Used by coding-agent MCP client/server integration. Depends on Bun subprocess APIs, JSONL reading, Windows command resolution helpers, and logger.
- edge_cases_or_failure_modes: Server exits early, malformed JSON, stderr noise, Windows `.cmd` wrappers, timeout, EPIPE, partial line, and close while requests pending.
- validation_or_tests: Covered by MCP JSON-RPC tests and integration tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3120 `file` `packages/coding-agent/src/modes/components/history-search.ts`
- cursor: `[_]`
- core_role: TUI component/controller for searching session history.
- algorithmic_behavior: Tokenizes search queries, scores/highlights matching history entries, formats relative timestamps/status, and renders a selectable list of matching sessions/messages.
- inputs_outputs_state: Inputs are query text, history/session records, current selection, and render dimensions. Outputs are filtered/highlighted TUI rows and selection events. State is query, selected index, and scroll/filter state.
- gates_or_invariants: Selection must clamp to filtered results; highlighting must not corrupt text width; empty query/results should render cleanly.
- dependencies_and_callers: Used by coding-agent interactive modes.
- edge_cases_or_failure_modes: No matches, wide/ANSI text, very large history, timestamp missing, and rapid query updates.
- validation_or_tests: Covered indirectly by modes/component tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3150 `file` `packages/coding-agent/src/modes/components/theme-selector.ts`
- cursor: `[_]`
- core_role: TUI selector for theme choice.
- algorithmic_behavior: Displays available themes, tracks selected theme, and returns the user’s chosen theme through component callbacks.
- inputs_outputs_state: Inputs are theme list/current selection and key events. Outputs are selected theme action/rendered selector. State is selected index/filter if present.
- gates_or_invariants: Selection must stay within theme list and reflect current theme.
- dependencies_and_callers: Used by coding-agent interactive settings/theme mode.
- edge_cases_or_failure_modes: Empty theme list, missing current theme, and narrow terminal.
- validation_or_tests: Covered indirectly by component tests.
- skip_candidate: `yes: UI component with minimal algorithmic behavior`

### OH_MY_HUMANIZE_MAIN-HZ-3180 `file` `packages/coding-agent/src/modes/controllers/tool-args-reveal.ts`
- cursor: `[_]`
- core_role: Controller for revealing streamed tool arguments in the UI.
- algorithmic_behavior: Tracks partial JSON/tool argument text, computes safe reveal boundaries, clamps slices to avoid invalid/cut content, and builds display args from raw/parsed input as streaming progresses.
- inputs_outputs_state: Inputs are streamed partial argument text, parsed args, reveal settings, and tool call state. Outputs are displayable argument previews. State is reveal progress/slice position.
- gates_or_invariants: Preview should never expose incoherent partials past a safe boundary; final parsed args should replace partial preview consistently.
- dependencies_and_callers: Used by coding-agent modes/tool execution rendering, especially streaming tool-call previews.
- edge_cases_or_failure_modes: Unterminated JSON strings, rapidly changing partials, parsed args lagging raw input, large args, and final/error states.
- validation_or_tests: Covered by tool execution args/streaming preview tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3210 `file` `packages/coding-agent/src/slash-commands/helpers/todo.ts`
- cursor: `[_]`
- core_role: Slash-command helper for todo/task manipulation.
- algorithmic_behavior: Parses todo command arguments, fuzzily matches phases/tasks, supports copy/export/import/append/start/done/drop/remove mutations, and commits changes back into runtime todo phase/task state.
- inputs_outputs_state: Inputs are slash-command text, current todo phases/tasks, clipboard/import content, and user selection. Outputs are updated todo state, messages, and exported/copied content. State is todo phase/task structure.
- gates_or_invariants: Task and phase matching must avoid ambiguous destructive changes; mutations must preserve todo schema; import/export formats must round-trip.
- dependencies_and_callers: Used by coding-agent slash command system.
- edge_cases_or_failure_modes: Ambiguous fuzzy match, missing phase/task, malformed import, duplicate task IDs/names, and destructive command typo.
- validation_or_tests: Covered indirectly by slash-command/todo tests if present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3240 `file` `packages/coding-agent/src/web/scrapers/dockerhub.ts`
- cursor: `[_]`
- core_role: Specialized web scraper/formatter for Docker Hub pages.
- algorithmic_behavior: Parses Docker Hub repository/tag URLs, fetches Docker Hub API data, normalizes repository/tag metadata, and formats it into markdown for web/read/search results.
- inputs_outputs_state: Inputs are Docker Hub URLs and HTTP responses. Outputs are structured scrape result or markdown summary. State is request-local parsed URL/API data.
- gates_or_invariants: Only supported Docker Hub URL shapes should route here; API errors must map to controlled fetch errors.
- dependencies_and_callers: Used by coding-agent web fetch/scraper routing.
- edge_cases_or_failure_modes: Private/missing repo, rate limiting, changed Docker Hub API shape, tag pagination, and invalid URL.
- validation_or_tests: Covered indirectly by web scraper tests where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3270 `file` `packages/coding-agent/src/web/scrapers/orcid.ts`
- cursor: `[_]`
- core_role: Specialized scraper/formatter for ORCID profile records.
- algorithmic_behavior: Parses ORCID IDs/URLs, fetches ORCID JSON record data, extracts person name, affiliations, works, and identifiers, then formats a readable markdown profile summary.
- inputs_outputs_state: Inputs are ORCID URLs/IDs and API JSON. Outputs are markdown/profile scrape result. State is request-local parsed record.
- gates_or_invariants: ORCID ID format must be validated; missing profile sections should degrade gracefully.
- dependencies_and_callers: Used by coding-agent web scraper routing.
- edge_cases_or_failure_modes: Private ORCID sections, missing name, API schema changes, invalid checksum/ID, and network failure.
- validation_or_tests: Covered indirectly by web scraper tests where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3300 `file` `packages/coding-agent/src/web/scrapers/youtube.ts`
- cursor: `[_]`
- core_role: Specialized scraper for YouTube video metadata/transcripts.
- algorithmic_behavior: Parses YouTube URL variants, fetches page/API/transcript data, cleans VTT captions, extracts video metadata, and formats transcript/summary markdown.
- inputs_outputs_state: Inputs are YouTube URLs and fetched page/transcript responses. Outputs are structured video scrape result or markdown. State is request-local parsed video ID/caption tracks.
- gates_or_invariants: Video ID parsing must avoid false positives; transcript cleanup must remove VTT timing/noise while preserving text order.
- dependencies_and_callers: Used by coding-agent web fetch/scraper routing.
- edge_cases_or_failure_modes: No captions, age/region restrictions, Shorts/embed URL variants, changed page JSON, and transcript fetch failure.
- validation_or_tests: Covered indirectly by web scraper/search tests where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3330 `file` `packages/coding-agent/test/modes/components/session-selector-status.test.ts`
- cursor: `[_]`
- core_role: Tests session selector status label/render behavior.
- algorithmic_behavior: Builds session records with different statuses and asserts selector labels/status markers are rendered as expected.
- inputs_outputs_state: Inputs are mock session metadata/statuses. Outputs are rendered labels/assertions. State is test-local.
- gates_or_invariants: Status labels must reflect session state without ambiguity.
- dependencies_and_callers: Validates coding-agent session selector component.
- edge_cases_or_failure_modes: Missing status, active/stale state, and ordering/display conflicts.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-3360 `file` `packages/coding-agent/test/modes/controllers/omfg-rule.test.ts`
- cursor: `[_]`
- core_role: Tests generated rule parsing/history matching controller behavior.
- algorithmic_behavior: Feeds generated rule/history inputs into the controller and asserts rule extraction, matching, and command behavior.
- inputs_outputs_state: Inputs are rule text/history records. Outputs are parsed/matched rule results. State is test-local.
- gates_or_invariants: Rule parsing must recognize intended generated rules and avoid false positives in history.
- dependencies_and_callers: Validates coding-agent modes controller/internal rule behavior.
- edge_cases_or_failure_modes: Malformed rule text, multiple candidate rules, stale history, and ambiguous matches.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-3390 `file` `packages/coding-agent/test/web/search/codex-broker.test.ts`
- cursor: `[_]`
- core_role: Tests Codex broker web search/auth SSE behavior.
- algorithmic_behavior: Mocks broker/auth/SSE responses and asserts search provider request handling, authentication, stream parsing, and result normalization.
- inputs_outputs_state: Inputs are search queries and mocked broker streams. Outputs are normalized search results/errors. State is test-local fetch/SSE mocks.
- gates_or_invariants: Broker auth and SSE parsing must preserve result semantics and map errors consistently.
- dependencies_and_callers: Validates coding-agent web search broker provider.
- edge_cases_or_failure_modes: Auth failure, malformed SSE, broker error frame, empty result, and timeout.
- validation_or_tests: This file is validation coverage.
- skip_candidate: `yes: test file, not runtime source`

### OH_MY_HUMANIZE_MAIN-HZ-3420 `file` `packages/collab-web/src/tool-render/tools/job.tsx`
- cursor: `[_]`
- core_role: Collab-web renderer for job-related tool calls/results.
- algorithmic_behavior: Extracts job IDs/status from poll/cancel/result payloads, maps status to visual tone/order, computes duration display, strips task result envelopes, and renders summary/body/outcome rows.
- inputs_outputs_state: Inputs are tool call/result props and job payload data. Outputs are React elements representing job status/results. State is render-local derived status/duration.
- gates_or_invariants: Job IDs and statuses must be parsed from multiple payload shapes; rendering should not expose raw envelopes unnecessarily.
- dependencies_and_callers: Used by collab-web tool-render registry.
- edge_cases_or_failure_modes: Unknown status, missing ID, malformed result envelope, very long task output, and canceled/error states.
- validation_or_tests: Covered indirectly by collab-web render tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3450 `file` `packages/stats/src/client/app/NavRail.tsx`
- cursor: `[_]`
- core_role: Stats client navigation rail component.
- algorithmic_behavior: Renders navigation items and selected state for stats dashboard routes.
- inputs_outputs_state: Inputs are active route/item definitions and click/navigation callbacks. Outputs are React navigation UI. State is minimal component props/local active state.
- gates_or_invariants: Active item should match route; navigation callbacks should target correct view.
- dependencies_and_callers: Used by stats dashboard client app.
- edge_cases_or_failure_modes: Unknown route, empty nav list, and responsive layout constraints.
- validation_or_tests: Covered indirectly by client UI tests/build.
- skip_candidate: `yes: UI component, not core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3480 `file` `packages/stats/src/client/ui/SegmentedControl.tsx`
- cursor: `[_]`
- core_role: Generic segmented-control UI component for stats client.
- algorithmic_behavior: Renders option buttons, selected state, and change callbacks for compact mode/filter selection.
- inputs_outputs_state: Inputs are option list, selected value, disabled state, and change handler. Outputs are React UI/events. State is controlled by props.
- gates_or_invariants: Only valid options should be selectable; selected visual state must match value.
- dependencies_and_callers: Used by stats dashboard UI.
- edge_cases_or_failure_modes: Empty options, invalid selected value, disabled clicks, and narrow layout.
- validation_or_tests: Covered indirectly by client UI/build.
- skip_candidate: `yes: generic UI component, not core algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3510 `file` `packages/coding-agent/src/commit/agentic/tools/propose-changelog.ts`
- cursor: `[_]`
- core_role: Agentic commit tool for proposing changelog entries.
- algorithmic_behavior: Defines tool schema for package/category/changelog entries, validates category/package data, and writes proposed changelog entries into commit-agent state for later application/review.
- inputs_outputs_state: Inputs are tool args from commit agent, package metadata, and commit-agent mutable state. Outputs are accepted changelog proposal result or validation error. State is commit-agent changelog proposal collection.
- gates_or_invariants: Category must be one of changelog sections; entry text/package must be valid; tool should not directly edit released changelog sections.
- dependencies_and_callers: Used by agentic commit workflow.
- edge_cases_or_failure_modes: Unknown package, invalid category, duplicate entry, empty entry text, and state unavailable.
- validation_or_tests: Covered by commit agent/tool tests where present.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3540 `file` `packages/coding-agent/src/modes/components/extensions/extension-list.ts`
- cursor: `[_]`
- core_role: TUI extension list component.
- algorithmic_behavior: Displays installed/available extensions, filters/searches entries, tracks selection, and emits action callbacks for extension management.
- inputs_outputs_state: Inputs are extension records, filter query, selected index, and key/action events. Outputs are rendered list rows and action events. State is selection/filter/scroll state.
- gates_or_invariants: Selection must clamp to filtered extension list; actions must target selected extension; render text must be truncated/sanitized.
- dependencies_and_callers: Used by coding-agent extension management modes.
- edge_cases_or_failure_modes: Empty list, missing extension metadata, long names/descriptions, disabled actions, and rapid filter changes.
- validation_or_tests: Covered indirectly by mode/component tests.
- skip_candidate: `yes: UI component with list/filter logic, not core backend algorithm`

### OH_MY_HUMANIZE_MAIN-HZ-3570 `file` `packages/coding-agent/src/web/search/providers/exa.ts`
- cursor: `[_]`
- core_role: Exa web search provider with direct API and MCP fallback support.
- algorithmic_behavior: Resolves auth from env/storage via `withAuth`, builds Exa request bodies with query/search mode/summary options, maps `keyword` to Exa-compatible mode, executes with timeout, normalizes direct API or MCP structured/text payloads, synthesizes answers from result summaries, and maps HTTP/provider failures to `SearchProviderError`.
- inputs_outputs_state: Inputs are search query/options, API key/source, fetch/MCP client responses, and timeout signal. Outputs are normalized search results, synthesized answer text, or provider errors. State is call-local auth retry/timeout state.
- gates_or_invariants: Missing auth must fail clearly; timeouts must abort; MCP fallback parsing must accept structured and text-block payloads; errors must map to stable provider error classes.
- dependencies_and_callers: Used by coding-agent web search tool/provider registry. Depends on AI auth retry helpers, fetch, MCP client shape, and search provider types.
- edge_cases_or_failure_modes: Missing/expired API key, HTTP non-OK, malformed MCP payload, empty result summaries, timeout, and unsupported search mode.
- validation_or_tests: Covered indirectly by web search provider tests.
- skip_candidate: `no`

### OH_MY_HUMANIZE_MAIN-HZ-3600 `file` `packages/utils/src/vendor/mermaid-ascii/er/parser.ts`
- cursor: `[_]`
- core_role: Vendor Mermaid ER diagram parser for ASCII rendering/utilities.
- algorithmic_behavior: Parses Mermaid ER syntax, creates entity records, parses attributes, relationship lines, cardinality markers, labels, and builds an internal ER graph representation for downstream ASCII rendering.
- inputs_outputs_state: Inputs are Mermaid ER diagram source lines. Outputs are parsed entity/relationship structures. State is parser-local maps of entities and relationships.
- gates_or_invariants: Entity names, attributes, and relationship cardinalities must parse according to Mermaid ER conventions; malformed lines should produce controlled errors or skips.
- dependencies_and_callers: Used by vendored mermaid-ascii utilities in `packages/utils`.
- edge_cases_or_failure_modes: Comments/blank lines, quoted labels, unknown cardinality, duplicate entities, malformed attributes, and relationship syntax drift.
- validation_or_tests: Covered indirectly by mermaid-ascii/vendor consumers if tests exist.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 120 item evidence sections present as headings; item IDs intentionally not repeated here to preserve single-occurrence evidence headings
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`