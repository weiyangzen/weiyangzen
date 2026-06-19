# agent_016 use-realpath4everything 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`

## Item Evidence

### USE_REALPATH4EVERYTHING-HZ-016 `directory` `prompt-template/codex`
- cursor: `[_]`
- core_role: This directory is the Codex-side prompt template bundle for the Humanize RLCR review loop. It is not executable by itself, but it is core review-control data: `hooks/loop-codex-stop-hook.sh` renders these templates into round review prompts and Codex review audit files, then downstream hook logic uses the rendered outputs to drive loop state transitions, drift recovery, finalize entry, and retry blocking. The directory contains exactly five markdown templates and no subdirectories: `regular-review.md`, `full-alignment-review.md`, `goal-tracker-update-section.md`, `commit-history-section.md`, and `code-review-phase.md`; the byte total is 12,759, matching the assignment metadata.

- algorithmic_behavior: `regular-review.md` defines the normal implementation-review protocol. It forces Codex to read the original plan first, compare Claude’s claimed work summary against plan and prompt inputs, classify findings into Mainline Gaps, Blocking Side Issues, and Queued Side Issues, include the mandatory `Mainline Progress Verdict: ADVANCED / STALLED / REGRESSED` line, update or request goal tracker corrections, and write issues to the review result file unless every original task is complete with no deferrals. Key lines: `prompt-template/codex/regular-review.md:5-12`, `:22-33`, `:35-47`, `:49-61`, `:65-76`.

  `full-alignment-review.md` is the periodic, stronger audit template selected every configured full-review interval. It requires an acceptance-criteria table, forgotten-item detection, deferred-item audit, mainline drift audit, historical round review, stagnation detection, and `STOP` as the final output when the circuit breaker should trip. Key lines: `prompt-template/codex/full-alignment-review.md:21-50`, `:52-67`, `:77-103`, `:104-114`.

  `goal-tracker-update-section.md` is a reusable subtemplate injected into both regular and full-alignment prompts. It assigns Codex responsibility for correcting the mutable part of `goal-tracker.md` when Claude requests it or Codex detects drift, while explicitly forbidding changes to the immutable Ultimate Goal and Acceptance Criteria. Key lines: `prompt-template/codex/goal-tracker-update-section.md:1-11`, `:13-18`.

  `commit-history-section.md` is another reusable subtemplate. It injects accumulated commit history and recent round summary/review file references so Codex can detect repeated issues, stalled progress, or mainline drift across rounds. Key lines: `prompt-template/codex/commit-history-section.md:1-12`.

  `code-review-phase.md` is the audit prompt for the separate `codex review --base ...` phase. It documents that `codex review` does not consume a prompt, describes expected `[P0-9]` severity markers, and records generated audit/log files. Key lines: `prompt-template/codex/code-review-phase.md:1-17`, `:19-36`.

- inputs_outputs_state: Inputs are template variables supplied by `hooks/loop-codex-stop-hook.sh`: round numbers, plan path, prompt path, summary content, goal tracker path, docs path, review result path, commit history, recent round files, loop timestamp, previous-round indexes, base branch, base commit/review base metadata, and timestamp. The hook builds those values at `hooks/loop-codex-stop-hook.sh:965-1086` for implementation review prompts and at `hooks/loop-codex-stop-hook.sh:1171-1208` for code-review audit prompts.

  Rendering is handled by `hooks/lib/template-loader.sh`. The loader resolves `{{VARIABLE}}` placeholders in one pass, keeps missing placeholders unchanged, and deliberately avoids re-scanning inserted values, which prevents injected placeholder content from being expanded accidentally. Relevant implementation: `hooks/lib/template-loader.sh:7-14`, `:48-56`, `:69-135`. Missing or empty templates fall back through `load_and_render_safe`, so absent Codex templates do not produce empty block/review messages: `hooks/lib/template-loader.sh:185-210`.

  Outputs are files under the active loop directory, primarily `round-N-review-prompt.md` and `round-N-review-result.md`, plus code-review audit/cache files described by `code-review-phase.md`. The state transition itself is not in the templates; it is performed by the stop hook after reading Codex output. The hook extracts the last non-empty review line, accepts only exact `COMPLETE` or `STOP` markers for terminal decisions, parses the mandatory mainline verdict, and updates drift counters or blocks when the verdict is absent. Relevant lines: `hooks/loop-codex-stop-hook.sh:1770-1791`, `:1793-1810`, `:1909-1935`.

- gates_or_invariants: The strongest invariant encoded by these templates is the mandatory mainline verdict. Both normal and full-alignment prompts require `Mainline Progress Verdict: ADVANCED / STALLED / REGRESSED`; the stop hook enforces that with `extract_mainline_progress_verdict` and blocks if implementation review output omits it. Template-side requirement: `prompt-template/codex/regular-review.md:56-61`, `prompt-template/codex/full-alignment-review.md:59-67`. Enforcement: `hooks/lib/loop-common.sh:634-662`, `hooks/loop-codex-stop-hook.sh:1785-1791`, `:1421-1454`.

  Completion is gated by strict final-line semantics. `regular-review.md` allows `COMPLETE` only when all original plan tasks, all acceptance criteria, and all pending/deferral checks are clean: `prompt-template/codex/regular-review.md:71-76`. `full-alignment-review.md` allows `COMPLETE` only when every acceptance criterion is fully met with no deferrals, and it introduces `STOP` for stagnation: `prompt-template/codex/full-alignment-review.md:102-114`. The hook reads and trims the last non-empty line before acting: `hooks/loop-codex-stop-hook.sh:1773-1778`.

  Code review phase has a separate gate: `codex review` output is scanned for severity markers and failures/empty logs block exit. The audit template documents the behavior at `prompt-template/codex/code-review-phase.md:12-17`; runtime execution and blocking are in `hooks/loop-codex-stop-hook.sh:1227-1234`, `:1254-1278`, `:1548-1621`. Issue marker detection scans the review log tail for `[P0-9]` near the start of a line: `hooks/lib/loop-common.sh:719-740`, `:755-770`.

  For the `use-realpath4everything` branch context, this directory does not perform realpath work directly. Its coordination with canonical paths happens through sibling hook libraries: `resolve_project_root` canonicalizes the project root via `realpath` and validators use `canonicalize_path_prefix` for safe comparisons. Relevant path-resolution helper lines: `hooks/lib/project-root.sh:14-20`, `:41-53`, `:55-96`, `:98-143`. The Codex templates receive the already-resolved loop/project-derived paths as rendered variables.

- dependencies_and_callers: Primary caller is `hooks/loop-codex-stop-hook.sh`. It loads `codex/goal-tracker-update-section.md` at `:974-975`, `codex/commit-history-section.md` at `:1024-1026`, chooses `codex/full-alignment-review.md` at `:1055-1069`, chooses `codex/regular-review.md` at `:1071-1086`, and writes the rendered review prompt to `$REVIEW_PROMPT_FILE`. It later loads `codex/code-review-phase.md` at `:1202-1208` to create an audit prompt before running `codex review`.

  Template rendering depends on `hooks/lib/template-loader.sh`, sourced through `hooks/lib/loop-common.sh` and the stop hook. The template directory is expected to contain `block`, `codex`, `claude`, and `plan` subdirectories, so `prompt-template/codex` coordinates with sibling template families through a shared loader and fallback strategy: `hooks/lib/template-loader.sh:213-237`.

  Behavioral siblings include `prompt-template/block/mainline-verdict-missing.md`, used when Codex violates the verdict contract, and `prompt-template/block/codex-review-failed.md`, used when `codex review` cannot produce valid output. The prompt text in this directory therefore defines the contract, while block templates and stop-hook code enforce it.

- edge_cases_or_failure_modes: Missing Codex templates are not fatal at render time because the hook supplies fallback prompt text through `load_and_render_safe`; however, fallback content is simpler and may lose some detailed audit instructions. Fallback mechanics are in `hooks/lib/template-loader.sh:185-210`; stop-hook fallbacks for regular/full-alignment prompts are constructed at `hooks/loop-codex-stop-hook.sh:1028-1053`.

  Missing `Mainline Progress Verdict` is a hard safety block for implementation review output unless Codex explicitly ended with `STOP`. This prevents the loop from updating drift state based on ambiguous feedback: `hooks/loop-codex-stop-hook.sh:1785-1791`.

  Ambiguous verdict lines containing multiple verdict keywords are rejected as unknown by `extract_mainline_progress_verdict`, which avoids accepting the template placeholder form as a real verdict: `hooks/lib/loop-common.sh:648-660`.

  Deferrals and pending tasks are intentionally treated as incomplete by the templates, so a review that follows Claude’s deferral request instead of forcing completion should not emit `COMPLETE`: `prompt-template/codex/regular-review.md:26-33`, `:72-75`; `prompt-template/codex/full-alignment-review.md:38-43`, `:111-114`.

  `code-review-phase.md` documents expected files including stdout/stderr captures, but the current runtime path stores a combined review log under `round-N-codex-review.log`; issue detection analyzes that combined log because `codex review` emits to stderr. This is not necessarily a bug, but the template is an audit narrative while exact file semantics are controlled by the hook: `prompt-template/codex/code-review-phase.md:30-36`, `hooks/lib/loop-common.sh:738-743`.

  Because this directory is prompt text, its failure modes are mostly contract drift: missing placeholders, stale instructions that no longer match hook behavior, or omitted mandates that downstream hooks assume Codex will follow.

- validation_or_tests: Template loading/rendering is covered by `tests/test-template-loader.sh`, including template directory resolution, loading existing/missing templates, variable replacement, multiline content, and special-character values: `tests/test-template-loader.sh:41-164`.

  Codex goal tracker subtemplate rendering is directly checked in `tests/test-templates-comprehensive.sh:531-540`.

  Commit history section behavior is covered by `tests/test-commit-history-section.sh`, including first round/no commits, round history references, corrupted base commit fallback, and missing-template fallback: `tests/test-commit-history-section.sh:1-10`, `:35-61`, `:67-114`, `:117-130`, `:180-222`.

  Template reference coverage is checked by `tests/test-template-references.sh`, which scans hook scripts for `load_template`, `load_and_render`, and `load_and_render_safe` references and verifies referenced templates exist: `tests/test-template-references.sh:1-10`, `:56-111`, `:121-142`.

  Stop/finalize behavior tied to these prompt contracts is covered in `tests/test-finalize-phase.sh`: normal `COMPLETE` handling with a mainline verdict, Codex review failure blocking, empty review output blocking, drift recovery on repeated `STALLED`, missing verdict blocking, and third stalled/regressed circuit breaker behavior. Relevant lines: `tests/test-finalize-phase.sh:575-607`, `:633-688`, `:694-725`, `:893-946`, `:948-994`, `:996-1030`.

  Code-review issue extraction is covered in `tests/test-codex-review-merge.sh`, including creation of `round-N-review-result.md` when `[P?]` issues are detected: `tests/test-codex-review-merge.sh:306-330`.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `1/1; exactly one Item Evidence section header is present for the assigned item`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`