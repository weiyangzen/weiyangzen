# agent_007 use-realpath4everything 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`

## Item Evidence

### USE_REALPATH4EVERYTHING-HZ-007 `directory` `prompt-template`
- cursor: `[_]`
- core_role:
  - `prompt-template/` is the repository’s runtime prompt/message contract bundle. It is not executable control flow by itself, but it is core algorithm data for the RLCR loop because hooks, validators, setup scripts, and planning commands load these Markdown templates to decide what operators and agents see when gates block, reviews run, prompts advance, or plan artifacts are generated.
  - The directory has four required child groups: `block/`, `claude/`, `codex/`, and `plan/`. The loader contract validates those subdirectories explicitly in `hooks/lib/template-loader.sh:213` through `hooks/lib/template-loader.sh:237`, and `hooks/lib/loop-common.sh:240` through `hooks/lib/loop-common.sh:248` wires the resolved `TEMPLATE_DIR` into loop runtime with graceful fallback behavior.
  - Recursive inventory found 61 Markdown files under `prompt-template/`, totaling 60,538 bytes:
    - `prompt-template/block/`: blocking/error messages rendered by read/write/edit/bash/stop/BitLesson/goal-tracker/plan/git/finalize/methodology gates.
    - `prompt-template/claude/`: next-round, drift-recovery, review-remediation, finalize, methodology-analysis, open-question, goal-tracker-update, push, and agent-team instruction templates for Claude-facing loop prompts.
    - `prompt-template/codex/`: Codex-facing review prompts, audit prompts, goal-tracker update instructions, and commit-history context blocks.
    - `prompt-template/plan/`: plan-generation and refine-plan QA scaffolds used by `/humanize:gen-plan` and `/humanize:refine-plan`.

- algorithmic_behavior:
  - Runtime loading is centralized in `hooks/lib/template-loader.sh`. `get_template_dir` computes `<plugin-root>/prompt-template` from `hooks/lib` (`hooks/lib/template-loader.sh:24` through `hooks/lib/template-loader.sh:31`). `load_template` reads a template by relative name and warns if missing (`hooks/lib/template-loader.sh:33` through `hooks/lib/template-loader.sh:46`).
  - Rendering is single-pass placeholder substitution using `{{VARIABLE_NAME}}`, with variables supplied as `VAR=value` pairs and exposed to `awk` as `TMPL_VAR_*` environment variables (`hooks/lib/template-loader.sh:56` through `hooks/lib/template-loader.sh:135`). The contract states uppercase/numeric/underscore placeholders, missing variables remain literal, and substituted values are not rescanned (`hooks/lib/template-loader.sh:7` through `hooks/lib/template-loader.sh:13`, `hooks/lib/template-loader.sh:52` through `hooks/lib/template-loader.sh:55`). This prevents prompt/body content such as review results from accidentally triggering second-pass substitution.
  - Missing or empty templates are intentionally non-fatal in most hook paths. `load_and_render_safe` loads a template, falls back when missing/empty, renders the fallback with the same variables, and emits the rendered result (`hooks/lib/template-loader.sh:185` through `hooks/lib/template-loader.sh:211`). This makes `prompt-template/` a preferred runtime surface, while inline fallbacks preserve gate behavior if installation is incomplete.
  - `block/` templates are used to produce JSON block decisions and human-readable recovery instructions. Examples:
    - Plan-integrity block renders `block/plan-file-modified.md` when the active plan changed after loop start (`hooks/loop-codex-stop-hook.sh:380` through `hooks/loop-codex-stop-hook.sh:396`).
    - Incomplete task block renders `block/incomplete-todos.md` before expensive review (`hooks/loop-codex-stop-hook.sh:401` through `hooks/loop-codex-stop-hook.sh:455`).
    - Git status, large-file, dirty-tree, unpushed-commit, summary-missing, contract-missing, goal-tracker-init, and BitLesson gates render the matching `block/*.md` templates (`hooks/loop-codex-stop-hook.sh:500` through `hooks/loop-codex-stop-hook.sh:735`, `hooks/loop-codex-stop-hook.sh:755` through `hooks/loop-codex-stop-hook.sh:910`).
    - Shared guard messages for todos access, prompt writes, state writes, finalize-state writes, contract access, summary bash writes, goal-tracker bash writes, methodology-analysis state writes, `.humanize` git protection, direct hook execution, and goal-tracker modification are routed through `hooks/lib/loop-common.sh:839` through `hooks/lib/loop-common.sh:912`, `hooks/lib/loop-common.sh:1012` through `hooks/lib/loop-common.sh:1019`, and `hooks/lib/loop-common.sh:1442` through `hooks/lib/loop-common.sh:1529`.
  - `claude/` templates drive state transitions between implementation rounds:
    - `claude/next-round-prompt.md` and `claude/drift-replan-prompt.md` are selected based on drift-replan state and rendered into the next `round-N-prompt.md` (`hooks/loop-codex-stop-hook.sh:1986` through `hooks/loop-codex-stop-hook.sh:2037`).
    - `claude/review-phase-prompt.md` is rendered when Codex/code review findings require a remediation round (`hooks/loop-codex-stop-hook.sh:1505` through `hooks/loop-codex-stop-hook.sh:1520`).
    - `claude/finalize-phase-prompt.md` and `claude/finalize-phase-skipped-prompt.md` become blocking prompts that move the loop into finalize behavior after review success or skipped review (`hooks/loop-codex-stop-hook.sh:1310` through `hooks/loop-codex-stop-hook.sh:1365`).
    - `claude/methodology-analysis-prompt.md` is rendered after loop exit is reached, after state is renamed to `methodology-analysis-state.md` and a completion marker is created (`hooks/lib/methodology-analysis.sh:64` through `hooks/lib/methodology-analysis.sh:95`).
    - `claude/open-question-notice.md`, `claude/post-alignment-action-items.md`, `claude/next-round-footer.md`, `claude/push-every-round-note.md`, `claude/goal-tracker-update-request.md`, `claude/agent-teams-continue.md`, and `claude/agent-teams-core.md` are appended conditionally while building the next prompt (`hooks/loop-codex-stop-hook.sh:2078` through `hooks/loop-codex-stop-hook.sh:2155`).
    - `claude/agent-teams-instructions.md` and `claude/agent-teams-core.md` are also injected into the initial round prompt when agent-teams mode is enabled (`scripts/setup-rlcr-loop.sh:1370` through `scripts/setup-rlcr-loop.sh:1390`).
  - `codex/` templates drive review prompt construction:
    - `codex/goal-tracker-update-section.md` is rendered as a reusable section for regular and full-alignment reviews (`hooks/loop-codex-stop-hook.sh:971` through `hooks/loop-codex-stop-hook.sh:975`).
    - `codex/commit-history-section.md` receives commit history and recent round references after the stop hook derives those values from git and loop state (`hooks/loop-codex-stop-hook.sh:997` through `hooks/loop-codex-stop-hook.sh:1026`).
    - `codex/full-alignment-review.md` is selected every configured full-review interval; otherwise `codex/regular-review.md` is used (`hooks/loop-codex-stop-hook.sh:977` through `hooks/loop-codex-stop-hook.sh:1080`). Both templates require the mainline verdict line; the missing-verdict block uses `block/mainline-verdict-missing.md` (`hooks/loop-codex-stop-hook.sh:1421` through `hooks/loop-codex-stop-hook.sh:1450`).
    - `codex/code-review-phase.md` is rendered as an audit prompt for `codex review --base ...` invocations (`hooks/loop-codex-stop-hook.sh:1190` through `hooks/loop-codex-stop-hook.sh:1208`).
  - `plan/` templates support planning commands:
    - `prompt-template/plan/gen-plan-template.md` defines the canonical generated plan schema. `scripts/validate-gen-plan-io.sh` resolves absolute input/output paths with `realpath -m`, validates the output target, locates the template under `CLAUDE_PLUGIN_ROOT` or script-relative fallback, and prints `TEMPLATE_FILE:` for the command to copy (`scripts/validate-gen-plan-io.sh:98` through `scripts/validate-gen-plan-io.sh:100`, `scripts/validate-gen-plan-io.sh:162` through `scripts/validate-gen-plan-io.sh:177`). `commands/gen-plan.md:141` and `commands/gen-plan.md:176` through `commands/gen-plan.md:180` then instruct copying that template and appending the original draft.
    - `.claude/CLAUDE.md:8` through `.claude/CLAUDE.md:9` declares an invariant that `commands/gen-plan.md`’s Plan Structure section and `prompt-template/plan/gen-plan-template.md` stay synchronized.
    - `prompt-template/plan/refine-plan-qa-template.md` is the required QA output scaffold for refine-plan. `commands/refine-plan.md:459` requires reading and populating it completely; `tests/test-refine-plan.sh:804` through `tests/test-refine-plan.sh:817` assert its expected title, sections, ledger columns, paths, and convergence status fields.

- inputs_outputs_state:
  - Inputs:
    - Template directory root: `TEMPLATE_DIR`, defaulted from plugin root (`hooks/lib/loop-common.sh:242` through `hooks/lib/loop-common.sh:248`).
    - Template relative names such as `block/git-not-clean.md`, `claude/next-round-prompt.md`, `codex/regular-review.md`, and `plan/gen-plan-template.md`.
    - Placeholder variables supplied by callers, for example `PLAN_FILE`, `GOAL_TRACKER_FILE`, `ROUND_CONTRACT_FILE`, `REVIEW_CONTENT`, `SUMMARY_CONTENT`, `COMMIT_HISTORY`, `CURRENT_ROUND`, `NEXT_SUMMARY_FILE`, `BASE_BRANCH`, `START_BRANCH`, `STALL_COUNT`, `GIT_ISSUES`, `SPECIAL_NOTES`, `BITLESSON_FILE`, and `REVIEW_RESULT_FILE`.
    - Plan command input/output paths. For gen-plan, the validator turns CLI paths into absolute paths with `realpath -m` where available (`scripts/validate-gen-plan-io.sh:98` through `scripts/validate-gen-plan-io.sh:100`) and returns the plan template path to the command (`scripts/validate-gen-plan-io.sh:177`).
  - Outputs:
    - Rendered Markdown block reasons embedded in hook JSON as `"decision": "block"` and `"reason": ...`, for example the plan-modified, incomplete-task, git-clean, summary-missing, and goal-tracker blocks.
    - Generated or appended loop prompt files: `round-N-review-prompt.md`, `round-N-prompt.md`, finalize prompt content, review-phase prompts, drift-recovery prompts, and methodology-analysis prompts.
    - Generated planning artifacts: initial plan scaffold from `plan/gen-plan-template.md`, and QA ledger scaffold from `plan/refine-plan-qa-template.md`.
    - Installation/runtime bundle contents: `install-skill.sh` requires `prompt-template/` in the runtime source (`scripts/install-skill.sh:75` through `scripts/install-skill.sh:84`) and copies it into the installed runtime bundle (`scripts/install-skill.sh:156` through `scripts/install-skill.sh:164`). Installation docs also list `prompt-template/` as an installed runtime dependency (`docs/install-for-codex.md:48` through `docs/install-for-codex.md:64`, `docs/install-for-kimi.md:56` through `docs/install-for-kimi.md:63`).
  - State transitions coordinated by templates:
    - Active loop continues or blocks based on stop-hook gates; templates define the remediation instruction text while shell logic emits the JSON decision.
    - Review prompt generation branches into regular review or full-alignment review using `FULL_ALIGNMENT_CHECK` (`hooks/loop-codex-stop-hook.sh:977` through `hooks/loop-codex-stop-hook.sh:987`).
    - Missing or malformed mainline verdict blocks transition until Codex reruns review; repeated `STALLED`/`REGRESSED` verdicts can trigger the drift circuit breaker prompt and stop state (`hooks/loop-codex-stop-hook.sh:1395` through `hooks/loop-codex-stop-hook.sh:1419`).
    - Next-round prompt generation branches into normal next round or drift recovery (`hooks/loop-codex-stop-hook.sh:2017` through `hooks/loop-codex-stop-hook.sh:2037`), then conditionally appends BitLesson, open-question, full-alignment, footer, push, goal-tracker, and agent-team sections (`hooks/loop-codex-stop-hook.sh:2039` through `hooks/loop-codex-stop-hook.sh:2155`).
    - Finalize and methodology-analysis phases are entered by rendering corresponding Claude prompts; methodology analysis also renames `state.md` and creates `methodology-analysis-done.md` before prompting (`hooks/lib/methodology-analysis.sh:64` through `hooks/lib/methodology-analysis.sh:83`).

- gates_or_invariants:
  - Directory invariant: `prompt-template/` is valid only if the root exists and contains `block`, `codex`, `claude`, and `plan` subdirectories (`hooks/lib/template-loader.sh:213` through `hooks/lib/template-loader.sh:237`). `loop-common.sh` warns but does not fail if validation fails, relying on inline fallbacks (`hooks/lib/loop-common.sh:245` through `hooks/lib/loop-common.sh:248`).
  - Placeholder invariant: variables use `{{UPPER_CASE}}` style; missing variables remain visible instead of silently disappearing, and variable values are not recursively rendered (`hooks/lib/template-loader.sh:7` through `hooks/lib/template-loader.sh:13`, `hooks/lib/template-loader.sh:52` through `hooks/lib/template-loader.sh:55`).
  - Safety invariant: critical validators should use `load_and_render_safe`, not raw rendering, so missing templates still produce useful block reasons. `tests/test-template-references.sh:170` through `tests/test-template-references.sh:200` checks this for read/write/edit validators.
  - Reference invariant: shell call sites that reference templates should point to existing files. `tests/test-template-references.sh:51` through `tests/test-template-references.sh:115` scans loader calls and fails missing references.
  - Syntax/load invariant: `tests/test-templates-comprehensive.sh:61` through `tests/test-templates-comprehensive.sh:107` loads all Markdown templates, `tests/test-templates-comprehensive.sh:113` through `tests/test-templates-comprehensive.sh:194` checks placeholder syntax, and `tests/test-templates-comprehensive.sh:563` through `tests/test-templates-comprehensive.sh:607` tries rendering every template with dummy placeholder values.
  - Fallback invariant: `load_and_render_safe` must use fallback for missing templates and real content for existing templates; this is tested around `tests/test-templates-comprehensive.sh:446` through `tests/test-templates-comprehensive.sh:490`.
  - Plan-template synchronization invariant: `.claude/CLAUDE.md:8` through `.claude/CLAUDE.md:9` requires the command Plan Structure block and `prompt-template/plan/gen-plan-template.md` to remain in sync; `tests/test-gen-plan.sh:708` through `tests/test-gen-plan.sh:714` verifies that equivalence.
  - Agent-team template invariants: `tests/test-agent-teams.sh:331` through `tests/test-agent-teams.sh:388` verifies existence/content of agent-team templates, and `tests/test-agent-teams.sh:718` through `tests/test-agent-teams.sh:724` guards that review-phase prompts do not accidentally include agent-team continuation text.

- dependencies_and_callers:
  - Primary loader dependency: `hooks/lib/template-loader.sh`, sourced by `hooks/lib/loop-common.sh` (`hooks/lib/loop-common.sh:240`). The hooks and scripts call loader functions directly or via loop-common.
  - Major runtime callers:
    - `hooks/loop-codex-stop-hook.sh`: largest caller; renders block messages, Codex review prompts, finalize prompts, drift prompts, next-round prompts, and conditional appended sections.
    - `hooks/lib/loop-common.sh`: shared block-message helper functions for read/write/edit/bash validators and state protections.
    - `hooks/lib/methodology-analysis.sh`: renders `claude/methodology-analysis-prompt.md`.
    - `scripts/bitlesson-validate-delta.sh`: renders BitLesson block templates for missing/invalid/inconsistent delta states (`scripts/bitlesson-validate-delta.sh:188` through `scripts/bitlesson-validate-delta.sh:310`).
    - `scripts/setup-rlcr-loop.sh`: reads `claude/agent-teams-instructions.md` and `claude/agent-teams-core.md` directly for initial round prompt injection (`scripts/setup-rlcr-loop.sh:1370` through `scripts/setup-rlcr-loop.sh:1379`).
    - `hooks/loop-read-validator.sh`, `hooks/loop-write-validator.sh`, `hooks/loop-edit-validator.sh`, and `hooks/loop-bash-validator.sh`: render path/location/protected-write/git-push templates, as shown by repository reference search.
  - Planning callers:
    - `commands/gen-plan.md` consumes the `TEMPLATE_FILE` returned by `scripts/validate-gen-plan-io.sh`, which points to `prompt-template/plan/gen-plan-template.md`.
    - `commands/refine-plan.md` consumes `prompt-template/plan/refine-plan-qa-template.md`.
    - `skills/humanize-refine-plan/SKILL.md` references the QA template path for installed runtime use.
  - Packaging callers:
    - `scripts/install-skill.sh` validates and copies `prompt-template/` as part of runtime installation (`scripts/install-skill.sh:75` through `scripts/install-skill.sh:84`, `scripts/install-skill.sh:162` through `scripts/install-skill.sh:164`).
    - Codex/Kimi install docs require copying or installing `prompt-template/` as a runtime dependency (`docs/install-for-codex.md:48` through `docs/install-for-codex.md:64`, `docs/install-for-kimi.md:56` through `docs/install-for-kimi.md:63`).
  - Test callers:
    - `tests/test-template-references.sh`
    - `tests/test-templates-comprehensive.sh`
    - `tests/test-template-loader.sh`
    - `tests/test-error-scenarios.sh`
    - `tests/test-commit-history-section.sh`
    - `tests/test-gen-plan.sh`
    - `tests/test-refine-plan.sh`
    - `tests/test-agent-teams.sh`
    - `tests/test-bitlesson-validate-delta.sh`
    - plus feature-specific tests that assert prompts or block messages contain expected template-derived content.

- edge_cases_or_failure_modes:
  - Missing template file: `load_template` warns and returns empty (`hooks/lib/template-loader.sh:41` through `hooks/lib/template-loader.sh:45`). Safe callers use fallback (`hooks/lib/template-loader.sh:197` through `hooks/lib/template-loader.sh:210`); unsafe direct `load_template` append paths may silently skip optional sections, e.g. open-question or post-alignment text has explicit fallback only in some cases (`hooks/loop-codex-stop-hook.sh:2091` through `hooks/loop-codex-stop-hook.sh:2094`, `hooks/loop-codex-stop-hook.sh:2115` through `hooks/loop-codex-stop-hook.sh:2119`).
  - Empty template: treated like missing by `load_and_render_safe` (`hooks/lib/template-loader.sh:197` through `hooks/lib/template-loader.sh:199`), so accidental blank files degrade to fallback.
  - Missing variable: placeholder remains in output, which is safer than erasing content but can leak unresolved `{{VAR}}` into prompts/block messages (`hooks/lib/template-loader.sh:118` through `hooks/lib/template-loader.sh:121`).
  - Placeholder injection: single-pass rendering prevents values containing `{{OTHER_VAR}}` from mutating output recursively (`hooks/lib/template-loader.sh:52` through `hooks/lib/template-loader.sh:55`). This matters for large untrusted text inputs like `REVIEW_CONTENT` and `SUMMARY_CONTENT`.
  - Multiline/special character values: values are passed via environment to `awk`. Tests include special characters, long values, and multiline handling in `tests/test-templates-comprehensive.sh`.
  - Template directory incomplete: loop startup warns and continues with inline fallbacks (`hooks/lib/loop-common.sh:245` through `hooks/lib/loop-common.sh:248`), but missing optional templates can reduce instruction richness.
  - Relative/absolute path sensitivity: gen-plan validation resolves input/output paths with `realpath -m` when available, then locates the plan template via `CLAUDE_PLUGIN_ROOT` or script-relative fallback (`scripts/validate-gen-plan-io.sh:98` through `scripts/validate-gen-plan-io.sh:100`, `scripts/validate-gen-plan-io.sh:162` through `scripts/validate-gen-plan-io.sh:168`). Since prompt templates often embed path variables directly, upstream callers must provide already-canonical or intended-display paths where path stability matters.
  - Documentation/runtime drift: `gen-plan-template.md` has a synchronization requirement with `commands/gen-plan.md`; if one changes without the other, generated plans and command instructions diverge. This is explicitly called out in `.claude/CLAUDE.md:8` through `.claude/CLAUDE.md:9` and tested.
  - Installed bundle omission: `install-skill.sh` treats missing `prompt-template/` as fatal for runtime source validation (`scripts/install-skill.sh:75` through `scripts/install-skill.sh:84`), because hooks and skills depend on it after installation.

- validation_or_tests:
  - Inspected but did not execute tests because this worker was instructed to work in a read-only branch export and produce research notes only.
  - Relevant validation coverage includes:
    - `tests/test-template-references.sh`: scans shell scripts for `load_template`, `load_and_render`, and `load_and_render_safe` references and fails missing template files (`tests/test-template-references.sh:51` through `tests/test-template-references.sh:115`); also checks key common templates and safe rendering use (`tests/test-template-references.sh:149` through `tests/test-template-references.sh:200`).
    - `tests/test-templates-comprehensive.sh`: validates directory structure, loads every template, checks placeholder syntax, tests malformed placeholder detection, verifies fallback behavior, and renders all templates with dummy values (`tests/test-templates-comprehensive.sh:61` through `tests/test-templates-comprehensive.sh:107`, `tests/test-templates-comprehensive.sh:113` through `tests/test-templates-comprehensive.sh:230`, `tests/test-templates-comprehensive.sh:446` through `tests/test-templates-comprehensive.sh:490`, `tests/test-templates-comprehensive.sh:563` through `tests/test-templates-comprehensive.sh:607`).
    - `tests/test-refine-plan.sh`: checks refine-plan QA template existence and required sections (`tests/test-refine-plan.sh:648` through `tests/test-refine-plan.sh:650`, `tests/test-refine-plan.sh:804` through `tests/test-refine-plan.sh:817`).
    - `tests/test-gen-plan.sh`: checks `prompt-template/plan/gen-plan-template.md` stays in sync with the command Plan Structure block (`tests/test-gen-plan.sh:708` through `tests/test-gen-plan.sh:714`).
    - `tests/test-agent-teams.sh`: checks agent-team template existence/content and that review-phase prompts do not include agent-team continuation instructions (`tests/test-agent-teams.sh:331` through `tests/test-agent-teams.sh:388`, `tests/test-agent-teams.sh:718` through `tests/test-agent-teams.sh:724`).
    - `tests/test-bitlesson-validate-delta.sh`: exercises BitLesson delta validation paths that render `block/bitlesson-delta-*.md`.
    - `tests/test-commit-history-section.sh`: exercises `codex/commit-history-section.md` rendering and fallback behavior.
  - Read-only environment note: `git status --short` failed because this branch export is not a git repository and the sandbox could not create macOS/Xcode temp cache files. This did not block directory inspection, but it prevented git-based verification of working tree state.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `USE_REALPATH4EVERYTHING-HZ-007`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`