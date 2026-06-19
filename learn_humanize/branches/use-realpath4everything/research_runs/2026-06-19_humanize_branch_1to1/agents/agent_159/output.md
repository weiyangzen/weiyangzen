# agent_159 use-realpath4everything 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`

## Item Evidence

### USE_REALPATH4EVERYTHING-HZ-159 `file` `prompt-template/claude/next-round-footer.md`
- cursor: `[_]`
- core_role: This file is a Claude next-round prompt footer. It acts as the final exit contract appended to generated round prompts after the stop hook decides that review found issues and the loop must continue. Its role is not to choose tasks or perform validation directly; it constrains the worker’s next transition by requiring honest loop continuation, commit creation, and summary writing. The core contract is in `prompt-template/claude/next-round-footer.md:4` and `prompt-template/claude/next-round-footer.md:6-9`.

- algorithmic_behavior: The template emits a short separator and completion checklist. The first behavioral rule blocks bypassing the loop by “lying, editing loop state files, or executing `cancel-rlcr-loop`” at `prompt-template/claude/next-round-footer.md:4`. The second section tells the next Claude worker what must happen after completing work: optionally invoke `code-simplifier` if installed, commit changes, and write the work summary to the rendered `@{{NEXT_SUMMARY_FILE}}` target at `prompt-template/claude/next-round-footer.md:6-9`. In the algorithmic flow, `hooks/loop-codex-stop-hook.sh` builds the next prompt body first, then appends this footer with `load_and_render_safe` at `hooks/loop-codex-stop-hook.sh:2122-2126`.

- inputs_outputs_state: Input is the template variable `NEXT_SUMMARY_FILE`, supplied by `hooks/loop-codex-stop-hook.sh:1961` as `$LOOP_DIR/round-${NEXT_ROUND}-summary.md` and passed into the renderer at `hooks/loop-codex-stop-hook.sh:2125-2126`. Output is rendered Markdown appended to `$NEXT_PROMPT_FILE`, defined at `hooks/loop-codex-stop-hook.sh:1960`. The footer itself has no executable state mutation; surrounding hook logic already updates loop state fields for `CURRENT_ROUND`, mainline stall count, last verdict, and drift status at `hooks/loop-codex-stop-hook.sh:1952-1957`, creates a placeholder next summary if missing at `hooks/loop-codex-stop-hook.sh:1961-1983`, and then appends this footer late in prompt assembly at `hooks/loop-codex-stop-hook.sh:2122-2127`.

- gates_or_invariants: The footer encodes process invariants for the next implementation round: do not falsify completion, do not edit loop state files to escape, do not run `cancel-rlcr-loop`, commit before exit, and write the summary to the exact loop-managed summary path. The template loader enforces single-pass placeholder rendering, keeping missing placeholders unchanged, as documented in `hooks/lib/template-loader.sh:7-13`; this matters because an unresolved `{{NEXT_SUMMARY_FILE}}` would remain visible rather than being silently deleted. `load_and_render_safe` falls back only if the template is missing, empty, or renders empty, as implemented at `hooks/lib/template-loader.sh:188-211`.

- dependencies_and_callers: The direct caller found is `hooks/loop-codex-stop-hook.sh:2125`, which renders `claude/next-round-footer.md` and appends it to the next prompt. Rendering depends on `hooks/lib/template-loader.sh`, especially `load_template` at `hooks/lib/template-loader.sh:36-46`, `render_template` at `hooks/lib/template-loader.sh:56-135`, and `load_and_render_safe` at `hooks/lib/template-loader.sh:188-211`. The footer complements adjacent prompt-generation templates: `claude/next-round-prompt.md` or `claude/drift-replan-prompt.md` are selected earlier at `hooks/loop-codex-stop-hook.sh:2017-2037`, optional notices may be inserted at `hooks/loop-codex-stop-hook.sh:2039-2120`, and push/goal-tracker continuation notes are appended after the footer at `hooks/loop-codex-stop-hook.sh:2129-2143`. The initial round uses similar but hardcoded footer semantics in `scripts/setup-rlcr-loop.sh:1423-1430`, indicating this template is the reusable later-round counterpart.

- edge_cases_or_failure_modes: If `prompt-template/claude/next-round-footer.md` is missing or empty, the hook falls back to `FOOTER_FALLBACK`, defined as a minimal “Before Exiting” instruction at `hooks/loop-codex-stop-hook.sh:2122-2124`; that fallback omits the anti-bypass warning and `code-simplifier` instruction, so behavior degrades but prompt generation continues. If `NEXT_SUMMARY_FILE` is not supplied, the placeholder remains as `{{NEXT_SUMMARY_FILE}}` due the loader’s missing-variable behavior in `hooks/lib/template-loader.sh:119-121`, causing a visible but less actionable path. If the rendered output becomes empty because of loader/render failure, `load_and_render_safe` emits the fallback at `hooks/lib/template-loader.sh:202-207`. Since this is prompt text, enforcement depends on downstream agents and validators rather than code execution in the template itself.

- validation_or_tests: I found no test that asserts the exact content of `prompt-template/claude/next-round-footer.md`. General template rendering behavior is covered by `tests/test-template-loader.sh:197-222`, which verifies `load_and_render_safe` uses fallback for missing templates and prefers real templates when available. Template reference coverage is checked by `tests/test-template-references.sh:83-107`, which scans `load_template`, `load_and_render`, and `load_and_render_safe` calls against `$TEMPLATE_DIR` and fails missing referenced templates. The relevant call path references this exact template at `hooks/loop-codex-stop-hook.sh:2125`.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `USE_REALPATH4EVERYTHING-HZ-159`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`