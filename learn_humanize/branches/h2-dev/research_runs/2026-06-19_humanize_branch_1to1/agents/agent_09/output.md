# agent_09 h2-dev 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 9
- source_commit: `2da7defbd5e955dbc329a27f1745fa74a0bee3f7`

## Item Evidence

### H2_DEV-HZ-009 `directory` `skills`
- cursor: `[_]`
- core_role: The `skills` directory is the user-facing orchestration layer for Humanize workflows. It does not implement the shell algorithms directly, but it defines the allowed workflow entrypoints, command routing, hook-gated transitions, required artifacts, validation gates, and failure handling that drive the core Humanize loop.
- algorithmic_behavior: Recursively inspected children are:
  - `skills/humanize/SKILL.md`: umbrella workflow spec. It defines RLCR as implementation then review, where a normal implementation round writes a summary and a native Codex Stop hook performs review gating. It also defines plan-generation structure, goal tracker responsibilities, `.humanize/` state layout, monitor command, and exit-code meanings for related scripts at lines 30-48, 61-88, 112-174, 181-230.
  - `skills/humanize-gen-plan/SKILL.md`: structured plan generation flow. Its mermaid graph gates input/output validation first, stops on validation failure or repository-irrelevant drafts, loops on draft ambiguity via user questions, emits a plan with goal, ACs, boundaries, feasibility, dependencies, and notes, then reviews/fixes inconsistencies before reporting success at lines 19-47 and 49-107.
  - `skills/humanize-refine-plan/SKILL.md`: refine-plan flow. It routes annotated plans through config load, `scripts/validate-refine-plan-io.sh`, stateful CMT extraction, classification, ambiguity handling, schema preservation, QA ledger generation, optional language variants, and atomic writes at lines 18-47. Required arguments and mutually exclusive `--discussion` / `--direct` mode rules are at lines 50-65. Required schema preservation and QA output guarantees are at lines 67-107.
  - `skills/humanize-rlcr/SKILL.md`: Codex-native RLCR entrypoint. It requires `setup-rlcr-loop.sh`, round prompt reading, implementation, commit, summary writing, normal exit, and native Stop-hook continuation on block at lines 24-48. It enumerates enforced gates including state/schema validation, branch consistency, plan integrity, incomplete task blocking, git-clean, summary presence, max iterations, `COMPLETE` / `STOP` markers, review-phase transition, and code-review severity gating at lines 50-67.
  - `skills/humanize-rlcr/SKILL-kimi.md`: hook-equivalent variant for environments without native hooks. It requires calling `scripts/rlcr-stop-gate.sh`, which delegates to `hooks/loop-codex-stop-hook.sh`, then interprets gate exit `0`, `10`, and `20` at lines 7-16 and 50-63. It shares the same enforced RLCR gate list at lines 65-82.
  - `skills/ask-codex/SKILL.md`: one-shot Codex consultation wrapper. It constrains shell invocation so free-form text is one quoted argument, preserves explicit `--codex-model` / `--codex-timeout` flags, reports stdout/stderr roles, and maps exit codes `0`, `1`, `124`, and other failures at lines 12-56.
  - `skills/ask-gemini/SKILL.md`: one-shot Gemini research wrapper. It mirrors the safe argument reconstruction rules, adds an expectation that Gemini performs Google Search, and maps stdout/stderr plus exit handling at lines 10-60.
- inputs_outputs_state: Inputs are slash/flow invocations and arguments such as plan path, draft path, skip/review flags, model/timeout flags, execution mode, QA directory, and optional alternate language. Outputs are `.humanize/rlcr/<timestamp>/` state, prompt, summary, review, finalize, complete-state, goal-tracker files, `.humanize/skill/<timestamp>/input.md` / `output.md` / `metadata.md`, refined plans, generated plans, and QA ledgers. Runtime root is injected through `{{HUMANIZE_RUNTIME_ROOT}}` in all Humanize skills, for example `skills/humanize/SKILL.md` lines 12-20 and `skills/humanize-refine-plan/SKILL.md` lines 12-16.
- gates_or_invariants: Major invariants are: do not manually edit RLCR state files; do not bypass blocked hooks; do not run ad-hoc Codex review in place of hook-managed transitions; always use generated round prompt/review files as source of truth; preserve gen-plan schema; remove resolved CMT blocks; keep task routing tags to `coding` or `analyze`; write refined artifacts atomically. These are explicit in `skills/humanize-rlcr/SKILL.md` lines 69-75 and `skills/humanize-refine-plan/SKILL.md` lines 62-86.
- dependencies_and_callers: The directory coordinates with `scripts/setup-rlcr-loop.sh`, `scripts/cancel-rlcr-loop.sh`, `scripts/validate-gen-plan-io.sh`, `scripts/validate-refine-plan-io.sh`, `scripts/ask-codex.sh`, `scripts/ask-gemini.sh`, `scripts/rlcr-stop-gate.sh`, `hooks/loop-codex-stop-hook.sh`, `hooks/lib/template-loader.sh`, and prompt templates under `prompt-template/`. `scripts/install-skill.sh` includes `humanize-refine-plan` in its skill list, as seen in the related reference search output around `scripts/install-skill.sh:42`.
- edge_cases_or_failure_modes: Covered failure modes include missing or malformed validator inputs, irrelevant drafts, unresolved ambiguity, inconsistent generated plans, unsupported or no-op alternate language, non-zero setup exits, hook blocks, infrastructure gate errors, unsafe shell argument splitting, model process timeout, and external command failures. The skill docs also distinguish Codex native hooks from Kimi hook-equivalent mode, preventing drift between environments.
- validation_or_tests: The assigned tests validate underlying config and template behavior. Related non-assigned coverage in `tests/test-refine-plan.sh` checks refine-plan command wiring, skill frontmatter, validator exit codes, comment extraction reference behavior, language mapping, and install docs; relevant validator script tests are at `tests/test-refine-plan.sh` lines 1055-1354.
- skip_candidate: `no`

### H2_DEV-HZ-039 `file` `config/default_config.json`
- cursor: `[_]`
- core_role: Default runtime configuration layer for Humanize commands and skills. It supplies baseline model, effort, mode, team, and language settings before user/project overrides are merged.
- algorithmic_behavior: The file is a JSON object with default keys: `codex_model` set to `gpt-5.5`, `codex_effort` set to `high`, `bitlesson_model` set to `haiku`, `agent_teams` false, empty `alternative_plan_language`, and `gen_plan_mode` set to `discussion` at lines 1-8.
- inputs_outputs_state: Input is static JSON read by `scripts/lib/config-loader.sh`. Output is a default layer participating in the merged config JSON returned by `load_merged_config`. The config loader reads this exact file via `default_config_path="$plugin_root/config/default_config.json"` at `scripts/lib/config-loader.sh` line 77.
- gates_or_invariants: Must be valid JSON object because `_config_loader_prepare_layer` treats the default layer as required and exits on missing or malformed required config at `scripts/lib/config-loader.sh` lines 40-60 and 109. Null stripping later prevents higher-layer null values from deleting defaults at `scripts/lib/config-loader.sh` lines 119-131.
- dependencies_and_callers: Used by `load_merged_config` in `scripts/lib/config-loader.sh` lines 63-137. Exercised by `tests/test-config-merge.sh`, which asserts `bitlesson_model=haiku`, `agent_teams=false`, and non-empty `gen_plan_mode` under default-only conditions at lines 43-64.
- edge_cases_or_failure_modes: If this file is missing, malformed, or not a JSON object, config loading fails because the default layer is required. If keys are removed, tests depending on default values fail. Higher layers can override non-null values, but nulls in project/user config are stripped and do not override defaults.
- validation_or_tests: `tests/test-config-merge.sh` validates defaults at lines 36-64, project override at lines 66-89, priority at lines 91-109, null stripping at lines 134-150, custom project path via `HUMANIZE_CONFIG` at lines 152-173, and additive all-layer merge at lines 175-198.
- skip_candidate: `no`

### H2_DEV-HZ-069 `file` `scripts/validate-refine-plan-io.sh`
- cursor: `[_]`
- core_role: Shell validator for the refine-plan workflow. It is the preflight gate that decides whether an annotated plan can enter comment extraction/refinement and whether output and QA destinations are writable.
- algorithmic_behavior: The script implements two stateful AWK scanners plus CLI/path gates:
  - `scan_cmt_blocks` counts valid, non-empty comment blocks and rejects malformed comment syntax. It supports `CMT:` / `ENDCMT`, `<cmt>` / `</cmt>`, and `<comment>` / `</comment>` markers at lines 62-113 and records scanner state for code fences, HTML comments, comment blocks, nearest heading, opening line/column, and comment format at lines 115-130.
  - It ignores fenced code blocks and HTML comments while outside CMT blocks at lines 135-158 and 165-180. Inside a CMT block, it marks non-whitespace text, counts the block only when the correct matching end marker appears, rejects nested starts, rejects wrong or stray end markers, and reports missing end marker at EOF with context at lines 182-315.
  - `scan_sections` produces visible markdown headings while skipping code fences, HTML comments, and CMT blocks, so required schema headings inside ignored regions do not satisfy the gen-plan schema gate at lines 318-478.
  - CLI parsing accepts `--input`, optional `--output`, optional `--qa-dir`, and mutually exclusive `--discussion` / `--direct`; unknown flags, missing values, help, and conflicting modes exit `7` at lines 480-548.
  - Runtime checks validate input existence, non-empty input, at least one non-empty comment block, required gen-plan sections, output directory or in-place input directory writability, and QA directory creation/writability at lines 573-678. Success reports line count, comment count, output mode, QA directory, and exits `0` at lines 680-692.
- inputs_outputs_state: Inputs are CLI args and an annotated markdown plan. Defaults are `OUTPUT_FILE=INPUT_FILE` for in-place mode at lines 556-559 and `QA_DIR=.humanize/plan_qa` at line 495. Outputs are diagnostic stdout/stderr and exit code; the script creates missing QA directories at lines 662-670 but does not write refined plan content itself.
- gates_or_invariants: Exit-code contract is documented at lines 4-12: `0` success, `1` missing input, `2` empty input, `3` no valid comments or malformed comment syntax, `4` missing required gen-plan sections, `5` output/input directory write failure, `6` QA directory failure, `7` invalid arguments. Required sections are enumerated at lines 609-619. Comment markers inside HTML comments or fenced code are ignored, empty CMT blocks do not count, and mismatched/nested/unterminated blocks are hard failures mapped to validation error `INVALID_COMMENT_BLOCKS` at lines 589-596.
- dependencies_and_callers: Called by `skills/humanize-refine-plan/SKILL.md` line 22. Related command tests in `tests/test-refine-plan.sh` assert command allowlisting and validator semantics; direct validator coverage is at lines 1055-1354. It depends on POSIX-ish shell utilities `awk`, `grep`, `wc`, `realpath`, `dirname`, `mkdir`, `tr`.
- edge_cases_or_failure_modes: Handles missing `--input` value, missing `--output` value, missing `--qa-dir` value, unexpected `--alt-language`, mutually exclusive modes, help as usage exit, missing/empty inputs, markers only in ignored regions, empty CMT blocks, unterminated blocks, nested blocks, sections only inside ignored regions, missing output dir, non-writable output dir, non-writable in-place input dir, QA path that is a file, and mixed valid/ignored/empty comment blocks. One subtle schema mismatch: this script requires `## Feasibility Hints` at lines 609-614, while `skills/humanize-refine-plan/SKILL.md` says `## Feasibility Hints and Suggestions` at line 77; `scan_sections` uses fixed-string grep, so plans with only the longer heading still match because the shorter required string is a substring of the longer heading.
- validation_or_tests: Non-assigned but directly relevant `tests/test-refine-plan.sh` validates invalid args and usage at lines 1062-1110, exit codes 1-6 at lines 1112-1294, valid in-place and new-file success at lines 1296-1354, ignored HTML/fence markers at lines 1139-1155, empty comments at lines 1157-1164, unterminated/nested parse errors at lines 1166-1199, and success count for mixed valid/ignored/empty blocks at lines 1318-1331.
- skip_candidate: `no`

### H2_DEV-HZ-099 `file` `tests/test-config-merge.sh`
- cursor: `[_]`
- core_role: Executable specification for Humanize configuration precedence and merge semantics. It verifies that config loading is deterministic across default, user, project, and environment-selected project config layers.
- algorithmic_behavior: The test sources `tests/test-helpers.sh` and `scripts/lib/config-loader.sh` at lines 16-33, then creates isolated temporary project/user config trees for each scenario. It calls `load_merged_config "$PROJECT_ROOT" "$PROJECT_DIR"` with per-test `XDG_CONFIG_HOME` and sometimes `HUMANIZE_CONFIG`, extracts keys with `get_config_value`, and records pass/fail through the shared helper counters.
- inputs_outputs_state: Inputs are temporary JSON files written under `$TEST_DIR`, the repository default config, `XDG_CONFIG_HOME`, and `HUMANIZE_CONFIG`. Outputs are test pass/fail lines and the final summary from `print_test_summary "Config Merge Tests"` at line 200. State is isolated with `setup_test_dir`, which creates a temp directory and registers cleanup at `tests/test-helpers.sh` lines 84-89.
- gates_or_invariants: The asserted merge order is empty base then default then user then project. Project values override user/default when non-null; user values remain additive when project does not specify the key; nulls in higher layers are stripped and therefore do not override lower-layer values; `HUMANIZE_CONFIG` replaces the default `$PROJECT_DIR/.humanize/config.json` path. These invariants are tested at lines 36-198.
- dependencies_and_callers: Depends on `scripts/lib/config-loader.sh`. The implementation requires `jq` at `scripts/lib/config-loader.sh` lines 17-22, validates each layer as a JSON object at lines 24-61, chooses default/user/project paths at lines 77-88, strips nulls and multiplies objects in order at lines 113-132, and extracts scalar/stringified values at lines 139-159.
- edge_cases_or_failure_modes: If `jq` is unavailable, malformed required default config exists, layer order changes, null stripping is removed, `HUMANIZE_CONFIG` is ignored, booleans stringify differently, or defaults change unexpectedly, this test fails. It does not cover malformed optional user/project config directly, though the loader warns and treats those as empty objects at `scripts/lib/config-loader.sh` lines 52-60.
- validation_or_tests: Test cases are default-only lines 36-64, project-overrides-default lines 66-89, project-wins-over-user lines 91-109, additive user preservation lines 111-132, null stripping lines 134-150, `HUMANIZE_CONFIG` override lines 152-173, and all-layers contribution lines 175-198.
- skip_candidate: `no`

### H2_DEV-HZ-129 `file` `tests/test-template-loader.sh`
- cursor: `[_]`
- core_role: Executable specification for prompt template discovery, loading, rendering, fallback behavior, shell-metacharacter safety, single-pass placeholder substitution, and Unicode/variable edge cases.
- algorithmic_behavior: The test sources `hooks/lib/template-loader.sh` at line 12 and then checks:
  - `get_template_dir` maps `hooks/lib` to `prompt-template` at lines 41-52.
  - `load_template` loads existing templates and returns empty for missing templates at lines 54-78.
  - `render_template` substitutes one or multiple variables, preserves multiline structure, handles special characters, ignores unused variables, and leaves missing variables as `{{ID}}` at lines 80-194.
  - `load_and_render` integrates real templates with substitutions at lines 146-164.
  - `load_and_render_safe` falls back on missing templates and uses real templates when present at lines 196-222.
  - `validate_template_dir` accepts valid and rejects invalid template roots at lines 224-244.
  - Shell metacharacter tests verify literal rendering for `&`, backslash, dollar, backticks, pipe, semicolon, globs, parentheses, redirection, quotes, hash, tilde, combined shell syntax, multiple ampersands, Windows paths, regex-like strings, JSON, and multiline values at lines 246-486.
  - Placeholder-injection tests ensure values containing `{{VAR}}` are not recursively expanded at lines 488-543.
  - Additional edge cases cover empty values, non-ASCII text in templates/values, underscore-prefixed variables, and numbered variables at lines 545-659.
- inputs_outputs_state: Inputs are inline template strings, real templates under `prompt-template`, and variable assignments passed as `VAR=value`. Outputs are pass/fail counters and final process exit `0` if no failures or `1` otherwise at lines 641-659.
- gates_or_invariants: The underlying implementation documents single-pass `{{VARIABLE_NAME}}` replacement and missing-variable preservation at `hooks/lib/template-loader.sh` lines 7-14 and 48-55. It builds environment variables with `TMPL_VAR_` prefix at lines 60-67, then AWK scans each line character by character and appends replacement values without re-scanning at lines 69-128. Safe loading emits fallback when content or rendered result is empty at lines 185-211. Template directory validation requires `block`, `codex`, `claude`, and `plan` subdirectories at lines 213-237.
- dependencies_and_callers: Depends on `hooks/lib/template-loader.sh`, real templates such as `prompt-template/block/git-push.md` and `prompt-template/block/wrong-round-number.md`, Bash, AWK, grep, and standard shell. This library is used by hooks and Humanize prompt rendering paths.
- edge_cases_or_failure_modes: Catches regressions where `sed`/`gsub`-style replacement would interpret ampersands or backslashes, shell metacharacters would be expanded, multiline values would be flattened, placeholder values would recursively expand and corrupt prompts, missing templates would crash instead of fallback, invalid template root would pass, or non-ASCII bytes would be mangled.
- validation_or_tests: This file is itself the validation. It exits with failure if any assertion increments `TESTS_FAILED` at lines 651-659.
- skip_candidate: `no`

### H2_DEV-HZ-159 `file` `prompt-template/block/bitlesson-delta-inconsistent.md`
- cursor: `[_]`
- core_role: Stop/gate message template for BitLesson delta consistency. It defines the remediation contract when a declared `## BitLesson Delta` action does not match expected lesson state.
- algorithmic_behavior: The template tells the user that the BitLesson Delta declaration is inconsistent at lines 1-3, then gives two state rules: `Action: none` must map to `Lesson ID(s): NONE` or no IDs, and `Action: add|update` must provide concrete Lesson IDs that exist in `.humanize/bitlesson.md` at lines 5-7.
- inputs_outputs_state: Input is a hook/gate condition identifying inconsistent BitLesson metadata. Output is a fixed markdown block shown to the agent/user. It does not mutate state; it directs the next transition to update the plan/summary BitLesson metadata or backing `.humanize/bitlesson.md`.
- gates_or_invariants: Enforces consistency between action and IDs: no lesson IDs for no-op deltas, concrete existing IDs for add/update deltas. This prevents the loop from accepting ambiguous or unverifiable lesson-history changes.
- dependencies_and_callers: Likely consumed by hook/template rendering through `hooks/lib/template-loader.sh` safe loader. The template depends conceptually on `.humanize/bitlesson.md` as the authoritative lesson ledger.
- edge_cases_or_failure_modes: Misdeclaring `Action: none` with IDs, declaring `add`/`update` with `NONE`, omitting IDs, or referencing IDs not present in `.humanize/bitlesson.md` should trigger this block. Because it has no placeholders, template rendering cannot fail due to missing variables.
- validation_or_tests: Covered indirectly by template loading tests that exercise `block` templates and directory validity. No assigned direct BitLesson-specific executable test was inspected.
- skip_candidate: `no`

### H2_DEV-HZ-189 `file` `prompt-template/block/stop-hook-direct-execution.md`
- cursor: `[_]`
- core_role: Guardrail message for active Humanize loops. It blocks manual Bash execution of hook scripts and routes the agent back to normal Stop-hook lifecycle handling.
- algorithmic_behavior: The template states that directly executing a hook script via Bash during an active loop is not allowed at lines 1-3, explains hooks are managed automatically and must not be run manually at line 5, and instructs the agent to complete work and end the response so the hook system handles the rest at line 7.
- inputs_outputs_state: Input is detection of attempted direct hook execution. Output is a fixed markdown block. No state changes are performed by the template; it preserves loop state by preventing manual hook invocation.
- gates_or_invariants: Enforces the invariant also present in `skills/humanize-rlcr/SKILL.md` lines 69-75: hook-managed phase transitions are the source of truth, and blocked hook results must not be bypassed by manual commands.
- dependencies_and_callers: Likely loaded by Stop-hook or Bash-command guard paths through `hooks/lib/template-loader.sh`. It coordinates with `hooks/loop-codex-stop-hook.sh`, `scripts/rlcr-stop-gate.sh`, and RLCR skill docs that define native/hook-equivalent behavior.
- edge_cases_or_failure_modes: Prevents accidental or intentional direct execution of hook scripts, which could corrupt current round state, bypass summary/git/plan checks, or trigger a gate out of order. Since the template has no variables, it is robust to missing render data.
- validation_or_tests: Indirectly covered by template loader directory and block-template loading tests. No assigned direct test for this exact block was inspected.
- skip_candidate: `no`

### H2_DEV-HZ-219 `file` `prompt-template/explore/final-idea-template.md`
- cursor: `[_]`
- core_role: Structured output schema for an exploration run’s selected final idea. It bridges exploratory research into productization by producing a final recommendation document that can be fed into plan generation and RLCR.
- algorithmic_behavior: The template defines mandatory sections for run metadata and decision evidence: title line, Run Context with run ID, directions JSON, report path, and final idea path at lines 1-8; Final Recommendation, Rationale, Approach Summary, Objective Evidence, Explore Outcomes, Constraints, Known Risks, and Cross-Direction Learnings at lines 10-40; and a Suggested Productization Flow that invokes `/humanize:gen-plan` then `/humanize:start-rlcr-loop` at lines 42-47.
- inputs_outputs_state: Inputs are placeholder values such as `<TITLE>`, `<RUN_ID>`, `<DIRECTIONS_JSON_FILE>`, `<REPORT_PATH>`, `<FINAL_IDEA_PATH>`, recommendation/rationale/evidence/outcome/risk text. Output is a markdown final idea artifact. It does not change runtime state directly, but it defines the handoff artifact consumed by downstream planning.
- gates_or_invariants: Requires objective evidence, constraints, risks, and cross-direction learnings to be captured before productization. This acts as a decision-quality gate so exploration output is not just a recommendation without traceable evidence.
- dependencies_and_callers: Coordinates with explore/report generation and downstream Humanize commands. The suggested flow explicitly depends on the gen-plan command and RLCR loop invocation at lines 44-46.
- edge_cases_or_failure_modes: If placeholders remain unresolved, the final idea artifact is incomplete. If evidence/constraints/risks are omitted, downstream plan generation may lack enough context. The template uses angle-bracket placeholders rather than `{{VAR}}`, so it is not rendered by the same placeholder mechanism unless another renderer handles those tokens.
- validation_or_tests: No assigned direct executable test for this exact explore template was inspected. Its structure is simple markdown and likely validated by higher-level explore workflow tests if present.
- skip_candidate: `no`

### H2_DEV-HZ-249 `file` `tests/robustness/test-template-error-robustness.sh`
- cursor: `[_]`
- core_role: Robustness executable specification for template system error handling under missing files, malformed placeholders, unusual variable names/values, filesystem anomalies, concurrent access, subdirectories, and symlinks.
- algorithmic_behavior: The script sources `hooks/lib/template-loader.sh` and shared test helpers at lines 15-18, creates a temp test directory at line 20, then validates:
  - Missing templates and missing directories return fallback through `load_and_render_safe` at lines 27-51.
  - Empty template handling allows empty output or fallback at lines 53-63.
  - Malformed templates with unclosed, nested, opening-only, or empty placeholders do not crash and return non-empty output at lines 65-115.
  - Variable names with spaces, special chars, numbers only, and very long names do not crash at lines 117-198.
  - Values containing template syntax are not recursively expanded, and newline-containing values preserve content at lines 157-186.
  - BOM, whitespace-only templates, filenames with spaces, permission-denied files, concurrent loading, subdirectory templates, and symlinked templates are handled at lines 200-340.
- inputs_outputs_state: Inputs are synthetic templates and variables created under `$TEST_DIR`, plus filesystem permissions and symlink support. Outputs are pass/fail/skip counters via `tests/test-helpers.sh`, final summary, and the script exit code from `print_test_summary` at lines 336-341.
- gates_or_invariants: Template loading must degrade safely: missing content falls back, malformed syntax does not abort the process, variable values are literal and single-pass, filesystem oddities do not corrupt files, and concurrent readers do not remove or modify the template. These invariants map to `hooks/lib/template-loader.sh` functions: missing template warning at lines 36-46, single-pass AWK rendering at lines 56-136, safe fallback at lines 185-211.
- dependencies_and_callers: Depends on Bash, `hooks/lib/template-loader.sh`, `tests/test-helpers.sh`, `mktemp`, `chmod`, `id`, `seq`, `wait`, `ln`, and filesystem support for permissions/symlinks. It complements `tests/test-template-loader.sh` by focusing on failure and robustness instead of nominal rendering.
- edge_cases_or_failure_modes: Captures missing directory, unreadable template, empty/whitespace content, malformed braces, placeholder-like values, newlines in environment-provided values, BOM prefix, special filenames, permission differences when running as root, parallel background jobs, nested subdirectory loading, and symlink support variance. Some assertions intentionally accept multiple safe outcomes, for example empty-template and permission handling, to avoid platform-specific false failures.
- validation_or_tests: This file is itself validation. It exits with the shared helper’s summary status at line 341, failing when any hard assertion increments `TESTS_FAILED`.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 9 item sections present, matching the 9 assigned rows in order.
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`