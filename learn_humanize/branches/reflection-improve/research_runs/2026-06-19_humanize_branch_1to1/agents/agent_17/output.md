# agent_17 reflection-improve 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 7
- source_commit: `13a47fb2260667a272b448e8d3c1a521f2382590`

## Item Evidence

### REFLECTION_IMPROVE-HZ-017 `directory` `prompt-template/plan`
- cursor: `[_]`
- core_role: Plan-generation template directory. Recursively contains one included child, `prompt-template/plan/gen-plan-template.md`, which defines the canonical generated plan structure used by `/humanize:gen-plan`.
- algorithmic_behavior: The child template lays out deterministic planning sections: goal, TDD-style acceptance criteria, path boundaries, feasibility hints, dependencies, task breakdown, Claude-Codex deliberation, pending user decisions, implementation notes, and output/translation conventions. It encodes task routing with exactly one tag per task: `coding` for Claude and `analyze` for Codex via `/humanize:ask-codex` at `prompt-template/plan/gen-plan-template.md:71-79`.
- inputs_outputs_state: Input is the user design draft plus generated planning analysis; output is the main plan file such as `plan.md`. The template also defines optional translated output variants when `alternative_plan_language` is configured; filename insertion rules are specified at `prompt-template/plan/gen-plan-template.md:106-120`.
- gates_or_invariants: Plan criteria must include positive and negative tests per acceptance criterion at `prompt-template/plan/gen-plan-template.md:6-23`. Code must not contain plan-specific workflow markers such as `AC-`, `Milestone`, `Step`, or `Phase` per `prompt-template/plan/gen-plan-template.md:99-104`. Task rows must include one routing tag at `prompt-template/plan/gen-plan-template.md:69-79`.
- dependencies_and_callers: `/commands/gen-plan.md` copies the template to the output file after relevance validation and appends the original design draft at `commands/gen-plan.md:164-168`. `scripts/validate-gen-plan-io.sh` locates this template using `CLAUDE_PLUGIN_ROOT` or a script-relative fallback and fails as a plugin configuration error if missing at `scripts/validate-gen-plan-io.sh:162-175`. The template itself references `/humanize:ask-codex`, tying `analyze` tasks to `scripts/ask-codex.sh`.
- edge_cases_or_failure_modes: Missing template blocks generation with exit code 7 from `validate-gen-plan-io.sh`. Unsupported or empty `alternative_plan_language` produces no translated variant. Highly deterministic designs are allowed to collapse upper/lower path bounds into a fixed choice per `prompt-template/plan/gen-plan-template.md:44`.
- validation_or_tests: `tests/test-gen-plan.sh` checks that the command’s embedded plan structure matches this template, and `tests/test-templates-comprehensive.sh` recursively loads and syntax-validates all prompt templates. `tests/test-templates-comprehensive.sh:90-107` loads every template; `tests/test-templates-comprehensive.sh:118-194` validates placeholder syntax.
- skip_candidate: `no`

### REFLECTION_IMPROVE-HZ-047 `file` `scripts/ask-codex.sh`
- cursor: `[_]`
- core_role: Runtime workflow script for one-shot Codex consultation. It implements the active `/humanize:ask-codex` delegation path used by plan `analyze` tasks and RLCR follow-up prompts.
- algorithmic_behavior: Parses options until first positional argument or `--`, supports `--codex-model MODEL:EFFORT` and `--codex-timeout SECONDS`, validates prerequisites, persists input/debug artifacts, runs `codex exec` with model/effort and sandbox mode, then writes output and metadata. Option parsing is at `scripts/ask-codex.sh:89-144`; Codex invocation is at `scripts/ask-codex.sh:243-297`.
- inputs_outputs_state: Inputs are CLI args, environment (`HUMANIZE_CODEX_BYPASS_SANDBOX`, `XDG_CACHE_HOME`, `CLAUDE_PROJECT_DIR`), config-backed defaults from `hooks/lib/loop-common.sh`, and stdin-like prompt via `printf`. Outputs are stdout Codex response, stderr status/debug lines, `.humanize/skill/<unique-id>/input.md`, `output.md`, `metadata.md`, and cache files `codex-run.cmd/out/log` under `~/.cache/humanize/...` or project-local fallback at `scripts/ask-codex.sh:202-218`.
- gates_or_invariants: Requires `codex` in `PATH` and non-empty question at `scripts/ask-codex.sh:153-170`. Model allows only alnum, dot, underscore, hyphen; effort allows alnum, underscore, hyphen at `scripts/ask-codex.sh:172-186`. Timeout must be numeric at `scripts/ask-codex.sh:120-129`. Default mode uses `--full-auto`; explicit bypass env switches to the dangerous sandbox bypass flag at `scripts/ask-codex.sh:249-255`.
- dependencies_and_callers: Sources `scripts/portable-timeout.sh` and `hooks/lib/loop-common.sh` at `scripts/ask-codex.sh:26-33`. `loop-common.sh` loads merged config-backed Codex defaults at `hooks/lib/loop-common.sh:184-190`. `/commands/gen-plan.md` calls this script for first-pass Codex analysis at `commands/gen-plan.md:172-193`, and `prompt-template/plan/gen-plan-template.md:71-79` routes `analyze` tasks to it.
- edge_cases_or_failure_modes: Missing Codex exits 1 with install guidance. Timeout exits 124 and writes timeout metadata at `scripts/ask-codex.sh:308-330`. Nonzero Codex exits propagate after tailing stderr at `scripts/ask-codex.sh:332-356`. Empty stdout is treated as failure with `empty_response` metadata at `scripts/ask-codex.sh:358-381`. Non-writable home cache falls back to project-local cache at `scripts/ask-codex.sh:214-218`.
- validation_or_tests: `tests/test-ask-codex.sh` and `tests/test-unified-codex-config.sh` are direct behavioral/config tests. Assigned related specs include `tests/test-templates-comprehensive.sh` for `/humanize:ask-codex` routing in plan templates and `tests/test-config-error-handling.sh` for the config loader that feeds defaults.
- skip_candidate: `no`

### REFLECTION_IMPROVE-HZ-077 `file` `tests/test-config-error-handling.sh`
- cursor: `[_]`
- core_role: Executable spec for config merge error handling used by runtime scripts, including `ask-codex.sh` through `loop-common.sh`.
- algorithmic_behavior: Creates isolated temp project/user config layouts, sources `scripts/lib/config-loader.sh`, calls `load_merged_config`, and asserts fatal versus fallback behavior. Test cases cover missing default config, malformed project config, malformed user config, empty project config, missing project config, and missing user config directory at `tests/test-config-error-handling.sh:36-172`.
- inputs_outputs_state: Inputs are temp `default_config.json`, `.humanize/config.json`, and `XDG_CONFIG_HOME/humanize/config.json` layers. Outputs are pass/fail counters from `tests/test-helpers.sh`, stderr warning captures, and merged JSON checked via `get_config_value`. Default expected `bitlesson_model` is `haiku`, matching `config/default_config.json:1-8`.
- gates_or_invariants: Required default config must be present and valid; optional user/project configs may be absent or malformed without aborting. Malformed optional layers must emit warning text and fall back to defaults at `tests/test-config-error-handling.sh:64-80` and `tests/test-config-error-handling.sh:93-109`.
- dependencies_and_callers: Depends on `scripts/lib/config-loader.sh` and `tests/test-helpers.sh`. The loader requires `jq`, validates each layer as a JSON object, strips nulls, and merges empty/default/user/project layers at `scripts/lib/config-loader.sh:63-136`.
- edge_cases_or_failure_modes: Missing required default config is fatal, tested at `tests/test-config-error-handling.sh:40-53`. Malformed optional configs are ignored with warnings. Empty `{}` project config is valid. A missing `.humanize` project config or missing `XDG_CONFIG_HOME` tree is nonfatal.
- validation_or_tests: The file is itself the validation spec and ends with `print_test_summary "Config Error Handling Tests"` at `tests/test-config-error-handling.sh:174`. It indirectly validates `load_merged_config` and `get_config_value` behavior from `scripts/lib/config-loader.sh:63-159`.
- skip_candidate: `no`

### REFLECTION_IMPROVE-HZ-107 `file` `tests/test-templates-comprehensive.sh`
- cursor: `[_]`
- core_role: Comprehensive executable spec for prompt-template loading, syntax, rendering, fallback behavior, and stress behavior across the template tree.
- algorithmic_behavior: Resolves `TEMPLATE_DIR` via `get_template_dir`, verifies required subdirectories, loads every `.md` template, scans placeholder syntax, runs malformed-placeholder detector checks, renders edge-case inputs, verifies fallback handling, renders selected real templates, then stress-renders all templates with dummy variables.
- inputs_outputs_state: Inputs are all markdown templates under `prompt-template/`, plus `hooks/lib/template-loader.sh`. Outputs are colored pass/fail/warn counters and process exit 0 only if `TESTS_FAILED` is zero at `tests/test-templates-comprehensive.sh:608-625`.
- gates_or_invariants: Requires `block`, `codex`, and `claude` subdirectories at `tests/test-templates-comprehensive.sh:74-80`. Valid placeholders are uppercase `{{VAR_NAME}}`; extra braces, wrong brackets, spaces, and lowercase placeholders are failures at `tests/test-templates-comprehensive.sh:118-194`. Missing template fallback must render fallback content at `tests/test-templates-comprehensive.sh:445-453`.
- dependencies_and_callers: Depends on `hooks/lib/template-loader.sh`, especially single-pass `render_template` at `hooks/lib/template-loader.sh:50-132`, `load_and_render_safe` fallback behavior at `hooks/lib/template-loader.sh:167-203`, and `validate_template_dir` at `hooks/lib/template-loader.sh:205-222`.
- edge_cases_or_failure_modes: Tests empty content, empty-line preservation, regex chars, backslashes, quotes, CJK-like values, markdown formatting, long values, multiline values, adjacent variables, repeated variables, and rapid successive calls at `tests/test-templates-comprehensive.sh:266-439` and `tests/test-templates-comprehensive.sh:547-560`. Warnings are allowed for unreplaced placeholders during all-template dummy rendering at `tests/test-templates-comprehensive.sh:590-597`.
- validation_or_tests: Real-template integration checks include `block/wrong-round-number.md`, `block/unpushed-commits.md`, and assigned `codex/goal-tracker-update-section.md` at `tests/test-templates-comprehensive.sh:497-540`. All templates are load-and-render stress tested at `tests/test-templates-comprehensive.sh:562-606`.
- skip_candidate: `no`

### REFLECTION_IMPROVE-HZ-137 `file` `prompt-template/block/pr-loop-prompt-write.md`
- cursor: `[_]`
- core_role: Block-message template enforcing PR-loop generated file immutability for `round-*-pr-comment.md` and `round-*-prompt.md` files.
- algorithmic_behavior: Provides a static denial reason: these files are generated by the PR loop system and are read-only. It names the protected patterns and describes their roles at `prompt-template/block/pr-loop-prompt-write.md:1-9`.
- inputs_outputs_state: No placeholders or runtime state. Input is a blocked write/edit decision from PR-loop validators; output is the rendered markdown block message.
- gates_or_invariants: Invariant is that `.humanize/pr-loop/round-*-pr-comment.md` and `.humanize/pr-loop/round-*-prompt.md` are system-managed and not user/agent-writable.
- dependencies_and_callers: Called through `pr_loop_prompt_blocked_message()` in `hooks/lib/loop-common.sh`, which uses `load_and_render_safe "$TEMPLATE_DIR" "block/pr-loop-prompt-write.md"` with an inline fallback at `hooks/lib/loop-common.sh:1091-1099`.
- edge_cases_or_failure_modes: If the template is missing or empty, `load_and_render_safe` emits the fallback string from `hooks/lib/loop-common.sh:1093-1096`. Because the template has no placeholders, rendering failure surface is minimal.
- validation_or_tests: Covered by `tests/test-templates-comprehensive.sh` all-template load/syntax/render passes at `tests/test-templates-comprehensive.sh:90-107`, `tests/test-templates-comprehensive.sh:118-194`, and `tests/test-templates-comprehensive.sh:562-606`.
- skip_candidate: `no`

### REFLECTION_IMPROVE-HZ-167 `file` `prompt-template/codex/goal-tracker-update-section.md`
- cursor: `[_]`
- core_role: Codex review prompt section assigning Codex responsibility for evaluating and applying Claude-requested goal tracker updates after Round 0.
- algorithmic_behavior: Instructs Codex to evaluate whether a requested goal-tracker change is justified, update `@{{GOAL_TRACKER_FILE}}` if approved, reject with rationale if not, and never modify the immutable Ultimate Goal/Acceptance Criteria section. Required actions are at `prompt-template/codex/goal-tracker-update-section.md:1-17`.
- inputs_outputs_state: Input placeholder is `{{GOAL_TRACKER_FILE}}`. Output is a rendered markdown section embedded into Codex review prompts, with the concrete goal tracker path substituted.
- gates_or_invariants: Codex must preserve the immutable section, only allow deferrals with strong justification, and log plan changes with round number and assessment. These constraints are explicit at `prompt-template/codex/goal-tracker-update-section.md:5-17`.
- dependencies_and_callers: `hooks/loop-codex-stop-hook.sh` renders this section with `GOAL_TRACKER_FILE=$GOAL_TRACKER_FILE` and a fallback at `hooks/loop-codex-stop-hook.sh:897-901`, then includes it in regular/full alignment review prompt construction. Rendering depends on `load_and_render_safe` from `hooks/lib/template-loader.sh`.
- edge_cases_or_failure_modes: Missing template falls back to a shorter “Goal Tracker Updates” instruction at `hooks/loop-codex-stop-hook.sh:897-900`. If `GOAL_TRACKER_FILE` is missing from caller state, the placeholder substitution would be empty or unresolved depending on caller variable handling.
- validation_or_tests: Directly rendered in `tests/test-templates-comprehensive.sh:531-540`, which asserts the heading and substituted `.humanize/rlcr/.../goal-tracker.md` path appear. Also covered by all-template syntax and stress rendering.
- skip_candidate: `no`

### REFLECTION_IMPROVE-HZ-197 `file` `tests/robustness/test-session-robustness.sh`
- cursor: `[_]`
- core_role: Robustness executable spec for active RLCR session detection under concurrent, stale, malformed, and edge-case directory layouts.
- algorithmic_behavior: Creates temp `.humanize/rlcr`-style session trees, calls `find_active_loop`, and verifies newest-active-session semantics. Positive cases cover newest active session, finalize phase, many sessions, zombie-loop protection, and both `state.md` plus `finalize-state.md` at `tests/robustness/test-session-robustness.sh:33-119`.
- inputs_outputs_state: Inputs are session directory names and state marker files (`state.md`, `finalize-state.md`, `complete-state.md`, `cancel-state.md`). Output is the path returned by `find_active_loop` or empty string, plus pass/fail summary.
- gates_or_invariants: Without session filter, only the single newest immediate child directory may be considered; older `state.md` files must not revive stale loops. That invariant is documented in `hooks/lib/loop-common.sh:257-274` and tested at `tests/robustness/test-session-robustness.sh:89-103` and `tests/robustness/test-session-robustness.sh:287-302`.
- dependencies_and_callers: Sources `hooks/lib/loop-common.sh` and `tests/test-helpers.sh` at `tests/robustness/test-session-robustness.sh:14-18`. `find_active_loop` uses `resolve_active_state_file`, which checks methodology-analysis, finalize, then state files at `hooks/lib/loop-common.sh:213-229`, and newest-directory logic at `hooks/lib/loop-common.sh:275-333`.
- edge_cases_or_failure_modes: Tests empty/nonexistent bases, files with no subdirectories, no state files, nonstandard names, symlinks, spaces, deep paths ignored beyond one level, rapid creation, finished/cancelled marker-only sessions ignored, and mixed finished/newer versus stale/older active sessions at `tests/robustness/test-session-robustness.sh:128-317`.
- validation_or_tests: The script is the validation. It exits with the helper summary status at `tests/robustness/test-session-robustness.sh:318-323`. It also includes a performance invariant for 15 sessions under 1000 ms at `tests/robustness/test-session-robustness.sh:63-87`.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: REFLECTION_IMPROVE-HZ-017, REFLECTION_IMPROVE-HZ-047, REFLECTION_IMPROVE-HZ-077, REFLECTION_IMPROVE-HZ-107, REFLECTION_IMPROVE-HZ-137, REFLECTION_IMPROVE-HZ-167, REFLECTION_IMPROVE-HZ-197
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`