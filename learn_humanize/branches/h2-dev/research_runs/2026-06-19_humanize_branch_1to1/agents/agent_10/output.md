# agent_10 h2-dev 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 9
- source_commit: `2da7defbd5e955dbc329a27f1745fa74a0bee3f7`

## Item Evidence

### H2_DEV-HZ-010 `directory` `templates`
- cursor: `[_]`
- core_role: `templates` is the seed-template directory for repository-local reusable artifacts. Recursive inspection found one descendant, `templates/bitlesson.md`, which is the initialization source for each project’s `.humanize/bitlesson.md` knowledge base.
- algorithmic_behavior: The directory participates in BitLesson initialization through `scripts/setup-rlcr-loop.sh`, which sets `PLUGIN_BITLESSON_TEMPLATE="$SCRIPT_DIR/../templates/bitlesson.md"` and invokes `scripts/bitlesson-init.sh` before creating RLCR state, at `scripts/setup-rlcr-loop.sh:865` to `scripts/setup-rlcr-loop.sh:871`. `scripts/bitlesson-init.sh` copies that template only if the target BitLesson file does not exist, at `scripts/bitlesson-init.sh:83` to `scripts/bitlesson-init.sh:86`.
- inputs_outputs_state: Input is the static `templates/bitlesson.md` file. Output is a project-level `.humanize/bitlesson.md` path printed by `bitlesson-init.sh` on success, at `scripts/bitlesson-init.sh:88`. State transition is “missing project knowledge base” to “initialized placeholder knowledge base”; existing files are intentionally preserved.
- gates_or_invariants: The initializer requires an existing project root, an existing template file, and a relative BitLesson path without parent traversal, at `scripts/bitlesson-init.sh:60` to `scripts/bitlesson-init.sh:72`. It rejects a target path that exists but is not a regular file, at `scripts/bitlesson-init.sh:78` to `scripts/bitlesson-init.sh:80`.
- dependencies_and_callers: Parent workflow docs in `docs/bitlesson.md` state that `start-rlcr-loop` initializes from `templates/bitlesson.md` when needed, at `docs/bitlesson.md:29` to `docs/bitlesson.md:34`. The primary caller is `scripts/setup-rlcr-loop.sh`.
- edge_cases_or_failure_modes: Missing template, missing project root, absolute BitLesson relpath, path traversal, or non-file target all hard-fail via `bitlesson-init.sh`. Because the directory currently has only one file, any future template additions would need separate reference validation if used by hooks.
- validation_or_tests: Indirectly covered by setup-script tests that assert `round-0-summary.md` BitLesson scaffolding exists and by BitLesson tests; no assigned test specifically validates the `templates` directory as a directory. Recursive directory content was `templates/bitlesson.md` only.
- skip_candidate: `no`

### H2_DEV-HZ-040 `file` `docs/bitlesson.md`
- cursor: `[_]`
- core_role: Behavior-defining documentation for the BitLesson knowledge capture workflow and stop-gate contract used by RLCR rounds.
- algorithmic_behavior: Defines provider selection, knowledge-base initialization, lesson selection, and summary validation. The selector reads `bitlesson_model` from config layers, at `docs/bitlesson.md:5` to `docs/bitlesson.md:13`, routes model names to Codex or Claude, at `docs/bitlesson.md:14` to `docs/bitlesson.md:19`, and forces Codex/OpenAI when `provider_mode: "codex-only"` is present, at `docs/bitlesson.md:21` to `docs/bitlesson.md:23`.
- inputs_outputs_state: Inputs are merged config, `.humanize/bitlesson.md`, tasks/subtasks, and round summaries. Outputs are selected lesson IDs or `NONE`, plus a mandatory `## BitLesson Delta` summary block. Workflow steps are specified at `docs/bitlesson.md:25` to `docs/bitlesson.md:35`.
- gates_or_invariants: Summary contract requires `Action: none|add|update`, `Lesson ID(s)`, and `Notes`, at `docs/bitlesson.md:36` to `docs/bitlesson.md:45`. Strict rules require `Action: none` to use `NONE` or empty lesson IDs, and `add`/`update` to reference existing concrete `BL-YYYYMMDD-short-name` IDs, at `docs/bitlesson.md:47` to `docs/bitlesson.md:51`.
- dependencies_and_callers: Implemented by `scripts/bitlesson-init.sh`, `scripts/bitlesson-select.sh`, and `scripts/bitlesson-validate-delta.sh`; enforced from `hooks/loop-codex-stop-hook.sh`, which calls `bitlesson-validate-delta.sh` when BitLesson is required, at `hooks/loop-codex-stop-hook.sh:864` to `hooks/loop-codex-stop-hook.sh:883`.
- edge_cases_or_failure_modes: Configured provider binary missing falls back to default Codex per docs, at `docs/bitlesson.md:19`. Empty knowledge bases may still report `none` unless strict mode is requested with `--require-bitlesson-entry-for-none`, at `docs/bitlesson.md:51`.
- validation_or_tests: `tests/test-bitlesson-validate-delta.sh` exercises Notes requirements, fenced-code/comment hiding, and valid normal-text deltas, at `tests/test-bitlesson-validate-delta.sh:101` to `tests/test-bitlesson-validate-delta.sh:152`. Setup tests also assert summary scaffolds include BitLesson Delta defaults.
- skip_candidate: `no`

### H2_DEV-HZ-070 `file` `templates/bitlesson.md`
- cursor: `[_]`
- core_role: Project BitLesson knowledge-base seed consumed by initialization logic for future RLCR rounds.
- algorithmic_behavior: Provides a strict reusable entry schema with fixed field order. Required fields are `Lesson ID`, `Scope`, `Problem Description`, `Root Cause`, `Solution`, `Constraints`, `Validation Evidence`, and `Source Rounds`, at `templates/bitlesson.md:5` to `templates/bitlesson.md:19`. Entries are appended below `## Entries`, at `templates/bitlesson.md:21` to `templates/bitlesson.md:23`.
- inputs_outputs_state: Input is this template file. Output is `.humanize/bitlesson.md` when `scripts/bitlesson-init.sh` copies it into a project. State starts with placeholder-only content and later accumulates concrete `Lesson ID:` records.
- gates_or_invariants: The template itself encodes the expected shape, but validation logic treats placeholder IDs as non-concrete. `scripts/bitlesson-validate-delta.sh` counts only non-empty `Lesson ID:` values that are not placeholders, at `scripts/bitlesson-validate-delta.sh:227` to `scripts/bitlesson-validate-delta.sh:240`.
- dependencies_and_callers: Referenced by `docs/bitlesson.md:31` and copied by `scripts/setup-rlcr-loop.sh:865` to `scripts/setup-rlcr-loop.sh:871` via `scripts/bitlesson-init.sh`.
- edge_cases_or_failure_modes: A freshly initialized file contains no concrete lesson IDs, so strict mode can block `Action: none`; that gate is in `scripts/bitlesson-validate-delta.sh:254` to `scripts/bitlesson-validate-delta.sh:267`. Existing project BitLesson files are not overwritten.
- validation_or_tests: BitLesson selection tests include placeholder-file behavior, and delta validation tests cover concrete lesson lookup. The assigned directory item confirms this is the only file in `templates`.
- skip_candidate: `no`

### H2_DEV-HZ-100 `file` `tests/test-directions-json-schema.sh`
- cursor: `[_]`
- core_role: Executable specification for `scripts/validate-directions-json.sh`, the schema-version-1 validator that gates generated idea directions before explore worker dispatch.
- algorithmic_behavior: Uses `jq` to mutate `tests/fixtures/directions/valid.directions.json` into positive and negative fixtures, then invokes the validator through `run_validate`, at `tests/test-directions-json-schema.sh:29` to `tests/test-directions-json-schema.sh:41`. It skips all assertions when `jq` is unavailable, at `tests/test-directions-json-schema.sh:22` to `tests/test-directions-json-schema.sh:25`.
- inputs_outputs_state: Inputs are the valid fixture and generated temporary `.directions.json` files. Output is pass/fail test reporting through `tests/test-helpers.sh`, ending with `print_test_summary`, at `tests/test-directions-json-schema.sh:302` to `tests/test-directions-json-schema.sh:303`.
- gates_or_invariants: Positive gate requires the valid fixture to exit `0`, at `tests/test-directions-json-schema.sh:46` to `tests/test-directions-json-schema.sh:53`. Negative gates cover missing top-level keys, direction count over 10, exactly-one-primary, duplicate IDs/slugs/source indexes, token-safe IDs, lowercase slug format, sequential `display_order`, array field types, valid confidence enum, metadata count/timestamp/draft fields, derived `direction_id`, and source-index range, at `tests/test-directions-json-schema.sh:59` to `tests/test-directions-json-schema.sh:300`.
- dependencies_and_callers: Directly depends on `scripts/validate-directions-json.sh` and `jq`. The underlying validator encodes the same invariants in one `jq -e` expression, including schema version, type checks, direction count, uniqueness, derivation, and metadata consistency, at `scripts/validate-directions-json.sh:40` to `scripts/validate-directions-json.sh:115`.
- edge_cases_or_failure_modes: Explicitly tests whitespace-only IDs, IDs with spaces, uppercase/slash-unsafe slugs, numeric title, non-string array members, `n_requested` lower than returned, and mixed semantic mismatch between `source_index`, `dir_slug`, and `direction_id`.
- validation_or_tests: This file is itself validation. It is also indirectly covered by explore command tests because `scripts/validate-explore-idea-io.sh` delegates schema checking to `validate-directions-json.sh`, at `scripts/validate-explore-idea-io.sh:266` to `scripts/validate-explore-idea-io.sh:275`.
- skip_candidate: `no`

### H2_DEV-HZ-130 `file` `tests/test-template-references.sh`
- cursor: `[_]`
- core_role: Executable specification preventing hook/block-template drift, especially missing blocker messages that would otherwise produce empty or unclear validator output.
- algorithmic_behavior: Scans selected hook scripts for `load_template`, `load_and_render`, and `load_and_render_safe` calls that use `$TEMPLATE_DIR`, extracts quoted template paths, and verifies each exists, at `tests/test-template-references.sh:51` to `tests/test-template-references.sh:115`.
- inputs_outputs_state: Inputs are hook scripts listed at `tests/test-template-references.sh:57` to `tests/test-template-references.sh:64` and all markdown templates under `prompt-template`, collected at `tests/test-template-references.sh:121` to `tests/test-template-references.sh:127`. Outputs are pass/fail/warn counters and exit `0` only when no failures are recorded, at `tests/test-template-references.sh:206` to `tests/test-template-references.sh:230`.
- gates_or_invariants: Missing referenced templates are critical failures, at `tests/test-template-references.sh:102` to `tests/test-template-references.sh:107`. Common templates including `block/summary-bash-write.md` must exist, at `tests/test-template-references.sh:149` to `tests/test-template-references.sh:167`. Critical read/write/edit validators must use `load_and_render_safe`, at `tests/test-template-references.sh:172` to `tests/test-template-references.sh:201`.
- dependencies_and_callers: Depends on the `prompt-template` directory and hook implementations. It is coupled to `hooks/lib/template-loader.sh`, where missing templates return empty from `load_template`, at `hooks/lib/template-loader.sh:33` to `hooks/lib/template-loader.sh:46`, and safe rendering provides fallback text, at `hooks/lib/template-loader.sh:185` to `hooks/lib/template-loader.sh:211`.
- edge_cases_or_failure_modes: Static regex extraction only sees direct quoted template names after `$TEMPLATE_DIR`; dynamically constructed template names may be reported as unreferenced warnings rather than failures, at `tests/test-template-references.sh:130` to `tests/test-template-references.sh:141`.
- validation_or_tests: This script validates template reference completeness. It specifically protects assigned templates such as `prompt-template/block/summary-bash-write.md`; `bitlesson-delta-invalid.md` is validated when referenced by the BitLesson validator path and by broader template tests.
- skip_candidate: `no`

### H2_DEV-HZ-160 `file` `prompt-template/block/bitlesson-delta-invalid.md`
- cursor: `[_]`
- core_role: Block-message template for the BitLesson stop gate when a summary contains `## BitLesson Delta` but does not contain exactly one valid action.
- algorithmic_behavior: The template tells the agent that the section exists but must include one action from `none`, `add`, or `update`, at `prompt-template/block/bitlesson-delta-invalid.md:1` to `prompt-template/block/bitlesson-delta-invalid.md:7`.
- inputs_outputs_state: Input is the invalid action condition detected from a summary. Output is the human-facing `reason` field inside a JSON block decision. `scripts/bitlesson-validate-delta.sh` loads this template through `load_and_render_safe` when action count is not one or the action enum is invalid, at `scripts/bitlesson-validate-delta.sh:202` to `scripts/bitlesson-validate-delta.sh:218`.
- gates_or_invariants: The invariant is exactly one `Action:` line in the extracted BitLesson Delta block, normalized case-insensitively, and the value must be `none`, `add`, or `update`.
- dependencies_and_callers: Called by `scripts/bitlesson-validate-delta.sh`; that script is called by `hooks/loop-codex-stop-hook.sh` before non-finalize round exit, at `hooks/loop-codex-stop-hook.sh:864` to `hooks/loop-codex-stop-hook.sh:883`.
- edge_cases_or_failure_modes: If the template is missing or empty, fallback text in `scripts/bitlesson-validate-delta.sh` is used, at `scripts/bitlesson-validate-delta.sh:207` to `scripts/bitlesson-validate-delta.sh:217`. Multiple `Action:` lines, missing action, or an unknown action all hit the same invalid-action path.
- validation_or_tests: `tests/test-bitlesson-validate-delta.sh` covers adjacent BitLesson gate behavior, and template existence is covered by template reference/comprehensive tests. Direct action-enum negative cases are implied by the validator branch rather than singled out in the assigned test files.
- skip_candidate: `no`

### H2_DEV-HZ-190 `file` `prompt-template/block/summary-bash-write.md`
- cursor: `[_]`
- core_role: Block-message template for preventing Bash-based mutation of RLCR round summary files, forcing writes through Write/Edit hooks so round/path validation remains active.
- algorithmic_behavior: The template states that Bash commands must not modify summary files and interpolates `{{CORRECT_PATH}}`, at `prompt-template/block/summary-bash-write.md:1` to `prompt-template/block/summary-bash-write.md:8`. The actual interpolation is done by `summary_bash_blocked_message` using `load_and_render_safe`, at `hooks/lib/loop-common.sh:897` to `hooks/lib/loop-common.sh:905`.
- inputs_outputs_state: Input is a Bash tool command that modifies a path matching `round-[0-9]+-summary.md` while an RLCR loop is active. Output is stderr block guidance and validator exit `2` from `hooks/loop-bash-validator.sh`.
- gates_or_invariants: `hooks/loop-bash-validator.sh` blocks summary mutations by Bash at `hooks/loop-bash-validator.sh:529` to `hooks/loop-bash-validator.sh:538`, computing the valid current-round path as `$ACTIVE_LOOP_DIR/round-${CURRENT_ROUND}-summary.md`. This preserves the invariant that summary writes pass through file validators.
- dependencies_and_callers: Depends on `hooks/lib/template-loader.sh` for safe rendering and on `command_modifies_file` in common hook logic for mutation detection. `tests/test-template-references.sh` lists it as a required common template, at `tests/test-template-references.sh:152` to `tests/test-template-references.sh:159`.
- edge_cases_or_failure_modes: If the template is missing, the fallback in `summary_bash_blocked_message` still includes the correct path. Detection depends on shell-command pattern coverage; `tests/test-bash-validator-patterns.sh` includes summary redirection patterns such as `echo x > round-5-summary.md`, at `tests/test-bash-validator-patterns.sh:186` to `tests/test-bash-validator-patterns.sh:194`.
- validation_or_tests: Template existence gate in `tests/test-template-references.sh`; Bash mutation pattern tests in `tests/test-bash-validator-patterns.sh`; template rendering behavior in `tests/test-template-loader.sh`.
- skip_candidate: `no`

### H2_DEV-HZ-220 `file` `prompt-template/explore/report-template.md`
- cursor: `[_]`
- core_role: Canonical report template for `/humanize:explore-idea` artifact synthesis. It structures the final `explore-report.md` produced after parallel prototype workers finish.
- algorithmic_behavior: Defines report metadata, summary, two-tier rankings, worker result summaries, adoption paths, all-worker details, and cleanup reference. Tier 1 ranks product directions, at `prompt-template/explore/report-template.md:18` to `prompt-template/explore/report-template.md:29`; Tier 2 ranks implementation-ready prototypes, at `prompt-template/explore/report-template.md:32` to `prompt-template/explore/report-template.md:42`.
- inputs_outputs_state: Inputs are placeholders such as `<RUN_ID>`, `<BASE_BRANCH>`, `<BASE_COMMIT>`, `<REPORT_PATH>`, `<FINAL_IDEA_PATH>`, ranking rows, rationale text, worker entries, winner branch/worktree/commit, and cleanup commands. The explore command enumerates report substitutions at `commands/explore-idea.md:301` to `commands/explore-idea.md:320`. Output is `<REPORT_PATH>` named `explore-report.md`, described at `commands/explore-idea.md:265` to `commands/explore-idea.md:269`.
- gates_or_invariants: `scripts/validate-explore-idea-io.sh` fails with exit `9` when this template is missing, at `scripts/validate-explore-idea-io.sh:248` to `scripts/validate-explore-idea-io.sh:260`. The command requires canonical artifacts only, no legacy alias, at `commands/explore-idea.md:23` to `commands/explore-idea.md:35`.
- dependencies_and_callers: Used by `commands/explore-idea.md` after validation emits `REPORT_TEMPLATE`, at `commands/explore-idea.md:59` to `commands/explore-idea.md:66`. The validation script emits the resolved template path on success, at `scripts/validate-explore-idea-io.sh:471` to `scripts/validate-explore-idea-io.sh:477`.
- edge_cases_or_failure_modes: Missing template blocks before dispatch, preventing workers from running without a report synthesis surface. The cleanup section includes destructive example placeholders but keeps the run directory removal commented, at `prompt-template/explore/report-template.md:116` to `prompt-template/explore/report-template.md:126`.
- validation_or_tests: `tests/test-validate-explore-idea-io.sh` creates and removes template fixtures to assert exit `9` for missing templates and required key output, at `tests/test-validate-explore-idea-io.sh:46` to `tests/test-validate-explore-idea-io.sh:53` and `tests/test-validate-explore-idea-io.sh:256` to `tests/test-validate-explore-idea-io.sh:283`. `tests/test-explore-command-structure.sh` checks report placeholders and adoption path ordering.
- skip_candidate: `no`

### H2_DEV-HZ-250 `file` `tests/robustness/test-template-stress-robustness.sh`
- cursor: `[_]`
- core_role: Robustness executable spec for the hook template-rendering engine under size and special-character stress.
- algorithmic_behavior: Sources `hooks/lib/template-loader.sh` and exercises `render_template`, `load_and_render`, and `load_and_render_safe`, at `tests/robustness/test-template-stress-robustness.sh:14` to `tests/robustness/test-template-stress-robustness.sh:19`. It verifies standard substitutions and fallback rendering, at `tests/robustness/test-template-stress-robustness.sh:33` to `tests/robustness/test-template-stress-robustness.sh:72`.
- inputs_outputs_state: Inputs are inline template strings, generated temporary template files, and variable assignments. Outputs are rendered strings plus pass/fail test summary via `print_test_summary`, at `tests/robustness/test-template-stress-robustness.sh:285` to `tests/robustness/test-template-stress-robustness.sh:289`.
- gates_or_invariants: Stress gates include 10KB values, 100KB values, 100KB template files, and 50 substitutions, at `tests/robustness/test-template-stress-robustness.sh:82` to `tests/robustness/test-template-stress-robustness.sh:151`. Edge gates include regex characters, ampersands, backslashes, newlines, empty values, placeholder-in-value injection prevention, dollar signs, repeated variables, boundary placeholders, and template-only placeholders, at `tests/robustness/test-template-stress-robustness.sh:161` to `tests/robustness/test-template-stress-robustness.sh:283`.
- dependencies_and_callers: Depends on `hooks/lib/template-loader.sh`, whose renderer intentionally performs single-pass AWK substitution and keeps missing variables unchanged, at `hooks/lib/template-loader.sh:48` to `hooks/lib/template-loader.sh:136`. Also depends on test helper setup.
- edge_cases_or_failure_modes: The most important edge case is placeholder injection: a value containing `{{VAR_B}}` must not trigger a second substitution pass, asserted at `tests/robustness/test-template-stress-robustness.sh:218` to `tests/robustness/test-template-stress-robustness.sh:228`. This protects templates that embed untrusted review or worker content.
- validation_or_tests: This file is itself validation for the template system. It complements `tests/test-template-references.sh`, which verifies existence and safe fallback use rather than rendering under stress.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: H2_DEV-HZ-010, H2_DEV-HZ-040, H2_DEV-HZ-070, H2_DEV-HZ-100, H2_DEV-HZ-130, H2_DEV-HZ-160, H2_DEV-HZ-190, H2_DEV-HZ-220, H2_DEV-HZ-250
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`