# agent_082 tunable-full-examine-round 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `67aa7bab09f0d0e36ac403264eed6989b09aada5`

## Item Evidence

### TUNABLE_FULL_EXAMINE_ROUND-HZ-082 `file` `prompt-template/block/git-not-clean.md`
- cursor: `[_]`
- core_role: This is the Markdown reason template for the RLCR/Codex stop-hook dirty-worktree gate. It does not execute git logic itself; it defines the agent-facing remediation contract emitted when the hook detects a non-clean repository before allowing the loop to stop or continue to later review gates. The title is declared at `prompt-template/block/git-not-clean.md:1`, and the primary diagnostic sentence is parameterized at `prompt-template/block/git-not-clean.md:3`.

- algorithmic_behavior: The template is rendered when `hooks/loop-codex-stop-hook.sh` finds cached git porcelain output during its “Quick Check: Git Clean and Pushed?” phase. The hook initializes `GIT_ISSUES` and `SPECIAL_NOTES` at `hooks/loop-codex-stop-hook.sh:518-519`; any non-empty cached status sets `GIT_ISSUES` to `uncommitted changes` at `hooks/loop-codex-stop-hook.sh:522-524`. The rendered block then tells the agent to handle optional code simplification, review untracked files, update `.gitignore` for artifacts, stage real changes, and commit with a descriptive project-conventional message at `prompt-template/block/git-not-clean.md:5-9`. The hook emits this rendered Markdown as the JSON `reason` in a `decision: block` response at `hooks/loop-codex-stop-hook.sh:561-568`, then exits without entering subsequent gates.

- inputs_outputs_state: Inputs are the `{{GIT_ISSUES}}` placeholder at `prompt-template/block/git-not-clean.md:3` and the `{{SPECIAL_NOTES}}` placeholder at `prompt-template/block/git-not-clean.md:4`. Runtime values come from git status classification in `hooks/loop-codex-stop-hook.sh:521-545`: generic dirty status becomes `uncommitted changes`; untracked `.humanize*` files append the humanize-local note; other untracked files append the untracked-artifacts note. Output is a rendered Markdown block passed through `load_and_render_safe` at `hooks/loop-codex-stop-hook.sh:557-559`, then serialized into hook JSON. State transition is external and policy-driven: an attempted stop changes to a blocked stop until the repository transitions from dirty to clean through staging and committing. The template itself makes no filesystem changes.

- gates_or_invariants: The gate invariant is that RLCR should not proceed past this point while git status has staged, unstaged, or untracked entries. This check runs before expensive Codex review, as described in the hook comments at `hooks/loop-codex-stop-hook.sh:510-514`. The template also defines commit hygiene invariants: commit messages must follow project conventions, AI tools must not be credited as authors, and `Co-Authored-By` AI attribution is forbidden at `prompt-template/block/git-not-clean.md:11-14`. It also distinguishes real changes from build artifacts by requiring untracked-file review and `.gitignore` handling at `prompt-template/block/git-not-clean.md:7-8`.

- dependencies_and_callers: The direct caller is `hooks/loop-codex-stop-hook.sh`, which uses `load_and_render_safe` with this template and a fallback message at `hooks/loop-codex-stop-hook.sh:551-559`. Rendering is implemented by `hooks/lib/template-loader.sh`: placeholder syntax is documented at `hooks/lib/template-loader.sh:7-13`, single-pass substitution is implemented at `hooks/lib/template-loader.sh:71-129`, and safe fallback behavior is implemented at `hooks/lib/template-loader.sh:170-203`. Related optional note templates are `prompt-template/block/git-not-clean-humanize-local.md`, loaded at `hooks/loop-codex-stop-hook.sh:530`, and `prompt-template/block/git-not-clean-untracked.md`, loaded at `hooks/loop-codex-stop-hook.sh:540`. `hooks/pr-loop-stop-hook.sh` has a separate inline dirty-worktree block at `hooks/pr-loop-stop-hook.sh:299-310`; it does not call this template.

- edge_cases_or_failure_modes: If this template is missing or renders empty, `load_and_render_safe` falls back to an embedded minimal Git Not Clean message from `hooks/loop-codex-stop-hook.sh:551-556`. If a caller omits a variable, the loader leaves unresolved placeholders intact by design, documented at `hooks/lib/template-loader.sh:12-13`. The rendered message is intentionally generic: it says there are `{{GIT_ISSUES}}` but does not include the actual porcelain status lines, so the agent must inspect git status separately. `SPECIAL_NOTES` is concatenated from note templates; those files begin with blank lines, which prevents immediate text collision, but the main template does not enforce spacing itself. The template tells the agent it may try to exit after committing at `prompt-template/block/git-not-clean.md:16`, but a later unpushed-commits gate can still block when push-every-round policy is enabled.

- validation_or_tests: I did not run tests because this research pass is read-only and the shell test suite may create temporary fixtures. Static coverage exists around the rendering system rather than this block alone: `tests/test-template-loader.sh` covers `load_and_render_safe` fallback and existing-template behavior around its lines reported for tests 11-12; `tests/test-templates-comprehensive.sh` exercises `render_template` and `load_and_render_safe` behavior across empty input, variables, multiline values, and special characters; `tests/test-template-references.sh` scans template references and safe rendering usage, including checks around `load_and_render_safe`. The hook-level dirty gate is inspectable at `hooks/loop-codex-stop-hook.sh:516-570`.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `1/1; the Item Evidence section contains one assigned-item heading, and the assigned id is not repeated elsewhere`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`