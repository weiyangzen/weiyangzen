# agent_18 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 7
- source_commit: `0ec921a36b4365df503511c5567bbd3e02db0df5`

## Item Evidence

### HZ-018 `directory` `prompt-template/plan`
- cursor: `[_]`
- core_role: Plan-generation and plan-refinement contract directory. It contains the authoritative output schemas that turn a draft or commented plan into structured RLCR work: [gen-plan-template.md](/Users/wangweiyang/GitHub/humanize/prompt-template/plan/gen-plan-template.md:1) and [refine-plan-qa-template.md](/Users/wangweiyang/GitHub/humanize/prompt-template/plan/refine-plan-qa-template.md:1).
- algorithmic_behavior: `gen-plan-template.md` requires goal description, acceptance criteria with positive and negative tests, path boundaries, milestones, task dependencies, routing tags, Claude/Codex deliberation, pending decisions, and implementation constraints; key sections are AC/test structure at lines 6-23, scope bounds at lines 25-44, dependency sequence at lines 57-68, and task routing at lines 69-79. `refine-plan-qa-template.md` requires a comment ledger, answers, research findings, applied changes, remaining decisions, and refinement metadata; the ledger shape is defined at lines 7-17 and detailed QA sections at lines 19-119.
- inputs_outputs_state: Inputs are draft requirements, comments, inferred language, merged config such as `alternative_plan_language`, and output path choices. Outputs are the primary plan, optional translated plan variant, and a mandatory QA document. The translated-plan output convention is specified in `gen-plan-template.md` lines 106-120; the QA command requires reading/populating the refinement template in [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:457).
- gates_or_invariants: Each task must have exactly one `coding` or `analyze` tag in `gen-plan-template.md` lines 71-79. Generated implementation code must not inherit workflow labels such as `AC-`, `Milestone`, `Step`, or `Phase` per lines 99-104. Refinement validation must ensure required sections remain, no comments remain, AC references exist, dependencies resolve, task rows have one valid routing tag, and convergence/decision status is coherent per [commands/refine-plan.md](/Users/wangweiyang/GitHub/humanize/commands/refine-plan.md:442).
- dependencies_and_callers: `scripts/validate-gen-plan-io.sh` locates `prompt-template/plan/gen-plan-template.md` and fails with plugin configuration error if missing at [validate-gen-plan-io.sh](/Users/wangweiyang/GitHub/humanize/scripts/validate-gen-plan-io.sh:162). `commands/refine-plan.md` makes the QA document non-optional and lists all required template sections at lines 457-471.
- edge_cases_or_failure_modes: Unsupported, empty, absent, or English `alternative_plan_language` suppresses translated output; identifiers and paths remain untranslated. Refinement must stop rather than invent requirements when plan inconsistencies cannot be reconciled.
- validation_or_tests: `tests/test-gen-plan.sh` cross-checks the command’s plan structure against `gen-plan-template.md`; `tests/test-refine-plan.sh` references the refinement QA template. `scripts/validate-gen-plan-io.sh` provides an operational existence gate for the generation template.
- skip_candidate: `no`

### HZ-048 `file` `hooks/loop-write-validator.sh`
- cursor: `[_]`
- core_role: PreToolUse `Write` hook enforcing RLCR write boundaries. It is registered for the `Write` matcher in [hooks/hooks.json](/Users/wangweiyang/GitHub/humanize/hooks/hooks.json:14).
- algorithmic_behavior: Reads hook JSON from stdin, validates JSON and nesting, ignores non-Write tools, requires `tool_input.file_path`, extracts `session_id`, blocks prompt and most todos writes, applies methodology-analysis restrictions, locates the active loop, strict-parses state, then validates state files, finalize summaries, contracts, plan backups, goal trackers, round numbers, and loop-directory paths. The main flow starts at [loop-write-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-write-validator.sh:24), prompt/todos checks are lines 57-69, methodology-analysis gating is lines 79-143, state parsing is lines 173-195, and final path canonicalization is lines 342-361.
- inputs_outputs_state: Input is hook JSON with `tool_name`, `tool_input.file_path`, optional `tool_input.content`, and optional `session_id`. Output is exit `0` to allow, exit `1` for invalid input or malformed state, or exit `2` with a rendered block message for policy violations. It does not mutate loop state; it protects state-machine surfaces from unauthorized writes.
- gates_or_invariants: Prompt files are always blocked at lines 67-69. State, finalize-state, and methodology-analysis-state writes are blocked at lines 202-214. During finalize, only the active `finalize-summary.md` is allowed and round contracts are blocked at lines 223-233. Goal tracker writes must target the active tracker and, after round 0, preserve the immutable section at lines 253-275.
- dependencies_and_callers: Sources `hooks/lib/loop-common.sh` at line 18 and uses `validate_hook_input`, `is_deeply_nested`, `find_active_loop`, `resolve_active_state_file`, `parse_state_file_strict`, block-message renderers, path predicates, and canonical path helpers. It depends on `jq`, `realpath` when available, template loading, and project-root resolution.
- edge_cases_or_failure_modes: If no project root or no active loop is found, it allows normal writes. It fails closed on deeply nested JSON, malformed state, unresolved traversal paths during methodology analysis, and unresolved symlink leaves. Session filtering intentionally avoids restricting unrelated sessions; spawned agents with different session ids are called out as prompt-sanitized rather than hook-restricted at lines 82-85.
- validation_or_tests: Covered by allowlist, finalize, plan-file, hook-input, and hook-system tests, with direct invocations found in `tests/test-allowlist-validators.sh`, `tests/test-finalize-phase.sh`, `tests/test-plan-file-hooks.sh`, and robustness tests.
- skip_candidate: `no`

### HZ-078 `file` `tests/test-config-error-handling.sh`
- cursor: `[_]`
- core_role: Executable specification for configuration merge failure behavior used by RLCR defaults and hook setup.
- algorithmic_behavior: Sources [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:1), then constructs temporary plugin/project/user config layouts and asserts whether `load_merged_config` succeeds, warns, or falls back. The test intent is listed in [test-config-error-handling.sh](/Users/wangweiyang/GitHub/humanize/tests/test-config-error-handling.sh:3).
- inputs_outputs_state: Inputs are fake plugin roots, project dirs, `.humanize/config.json`, `XDG_CONFIG_HOME`, malformed JSON, empty JSON objects, and missing files. Outputs are test pass/fail records through `test-helpers.sh` and the final summary at line 174. It does not modify repository state; only temporary test directories.
- gates_or_invariants: Missing required `default_config.json` must be fatal at lines 40-53. Malformed project config must warn and fall back to default `bitlesson_model=haiku` at lines 59-80. Malformed user config has the same warning/default behavior at lines 87-109. Empty project config and missing optional user/project config must be non-fatal at lines 116-171.
- dependencies_and_callers: Depends on `scripts/lib/config-loader.sh`, `tests/test-helpers.sh`, and `jq` through the loader. The loader’s required-vs-optional layer behavior is implemented in [config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:24), with merge order at lines 113-132.
- edge_cases_or_failure_modes: Missing `config-loader.sh` is a fatal test setup error at lines 27-30. Optional malformed JSON is degraded to `{}` with a warning, while malformed or missing required default config exits nonzero. Nonexistent `XDG_CONFIG_HOME` is explicitly treated as optional.
- validation_or_tests: This file is itself the validation artifact for config error handling and verifies the loader API used by `loop-common.sh` to derive defaults such as `DEFAULT_BITLESSON_MODEL`, `DEFAULT_CODEX_MODEL`, and `DEFAULT_CODEX_EFFORT`.
- skip_candidate: `no`

### HZ-108 `file` `hooks/lib/loop-common.sh`
- cursor: `[_]`
- core_role: Shared RLCR hook/state-machine library used by read/write/edit/bash validators, the Codex stop hook, setup, and cancel scripts. The consumer list is stated at [loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:3).
- algorithmic_behavior: Defines state-field constants, verdict/drift enums, JSON validation, config-backed defaults, active-loop discovery, state parsing, review issue detection, block-message rendering, goal-tracker immutable checks, cancel authorization, git protection, command mutation detection, and loop termination. Constants are lines 24-76; hook JSON validation is lines 91-165; config/template setup is lines 171-248.
- inputs_outputs_state: Inputs include hook JSON, loop directories, YAML frontmatter state files, Codex review logs, goal tracker content, shell commands, config JSON, and git index state. Outputs include global `STATE_*` variables, normalized verdicts, block messages, review issue text, authorization status codes, updated state frontmatter via `upsert_state_fields`, and terminal state files via `end_loop`.
- gates_or_invariants: `resolve_active_state_file` prioritizes methodology-analysis, finalize, then normal state at lines 268-280. `find_active_loop` enforces newest-loop and session/zombie-loop rules at lines 332-425. `parse_state_file_strict` requires frontmatter, `current_round`, `max_iterations`, `review_started`, `base_branch`, numeric round/max values, and boolean `review_started` at lines 533-600. `detect_review_issues` scans only the last 50 log lines for `[P0-9]` markers near line start at lines 740-788.
- dependencies_and_callers: Sources `project-root.sh`, `scripts/lib/config-loader.sh`, `template-loader.sh`, and finally `loop-bg-tasks.sh`; requires common Unix tools plus `jq`, optional `iconv`, `perl`, and `git` for specific helpers. Cross-references show callers in `loop-write-validator.sh`, `loop-read-validator.sh`, `loop-edit-validator.sh`, `loop-bash-validator.sh`, `loop-plan-file-validator.sh`, `loop-codex-stop-hook.sh`, setup/cancel scripts, and multiple tests.
- edge_cases_or_failure_modes: Config loading is best-effort if project root exists and warnings remain visible at lines 189-200. `find_active_loop` without a session only checks the single newest dir, preventing stale older loops from reviving. With session filtering, a terminal newest dir for that session returns empty. Cancel authorization rejects command substitution, shell operators, hidden variables, mixed quotes, extra args, wrong source/destination, and source symlinks at lines 1051-1249. `git_adds_humanize` blocks direct or broad `.humanize` staging at lines 1280-1375.
- validation_or_tests: Covered broadly by `tests/robustness/test-state-transition-robustness.sh`, `tests/test-session-id.sh`, `tests/test-cancel-signal-file.sh`, `tests/test-codex-review-merge.sh`, `tests/test-humanize-escape.sh`, and hook robustness tests. Template message references are validated by `tests/test-template-references.sh`.
- skip_candidate: `no`

### HZ-138 `file` `prompt-template/block/prompt-file-write.md`
- cursor: `[_]`
- core_role: Block-message template for attempts to write `round-*-prompt.md`, protecting the prompt/instruction surface from self-modification.
- algorithmic_behavior: States that prompt files contain instructions from Codex to Claude and directs the actor to read the prompt, execute tasks, and write results to the summary file instead. The core policy is in [prompt-file-write.md](/Users/wangweiyang/GitHub/humanize/prompt-template/block/prompt-file-write.md:1).
- inputs_outputs_state: Input is a prompt-file write violation detected by a hook. Output is the rendered denial text emitted to stderr. No state transition occurs; it preserves the existing instruction state.
- gates_or_invariants: `round-*-prompt.md` files are read-only operational inputs. If the prompt is wrong, the only allowed response is documenting that in the summary file, not editing the prompt; see lines 7-12.
- dependencies_and_callers: Loaded by `prompt_write_blocked_message` in [loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:850), called by [loop-write-validator.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-write-validator.sh:67). `tests/test-template-references.sh` includes `block/prompt-file-write.md` in the common template existence checks at lines 152-155.
- edge_cases_or_failure_modes: The template is a simple static message. If missing, `load_and_render_safe` falls back to inline text in `loop-common.sh`, so blocking behavior can continue with degraded messaging.
- validation_or_tests: Template existence and safe-render usage are covered by `tests/test-template-references.sh`; functional blocking is covered through write-validator tests.
- skip_candidate: `no`

### HZ-168 `file` `prompt-template/codex/code-review-phase.md`
- cursor: `[_]`
- core_role: Audit template for the Codex review phase, documenting a review invocation and the review-to-finalize/remediation transition contract.
- algorithmic_behavior: Records base branch, review round, timestamp, review command semantics, severity-marker scanning, and generated artifacts. The phase behavior is stated in [code-review-phase.md](/Users/wangweiyang/GitHub/humanize/prompt-template/codex/code-review-phase.md:12), and generated files are listed at lines 30-36.
- inputs_outputs_state: Inputs are `REVIEW_ROUND`, `BASE_BRANCH`, and `TIMESTAMP` placeholders. Output is `round-N-review-prompt.md`, an audit file saved in the loop directory, not a prompt passed to `codex review`.
- gates_or_invariants: The review gate runs `codex review --base`, scans output for `[P0-9]` severity markers, sends issues back for remediation, and proceeds to finalize only if no issues are found at lines 14-17. Expected issue output shape is lines 19-28.
- dependencies_and_callers: Rendered by [loop-codex-stop-hook.sh](/Users/wangweiyang/GitHub/humanize/hooks/loop-codex-stop-hook.sh:1223) via `load_and_render_safe` at lines 1240-1246. The same stop hook then runs Codex review and delegates marker detection to `detect_review_issues` at lines 1288-1316.
- edge_cases_or_failure_modes: The template explicitly notes that `codex review` does not accept prompt input at lines 3-4, so this file is audit evidence rather than execution input. Review command failure blocks finalize; missing or empty review log is handled as a hard error by `detect_review_issues`.
- validation_or_tests: Review marker extraction is tested by `tests/test-codex-review-merge.sh`. Template references are included in repository-wide template reference tests and stop-hook review flow tests.
- skip_candidate: `no`

### HZ-198 `file` `tests/robustness/test-state-transition-robustness.sh`
- cursor: `[_]`
- core_role: Executable robustness spec for RLCR state parsing, active-loop discovery, finalize/cancel handling, and state edge cases.
- algorithmic_behavior: Creates synthetic loop directories and state files, then exercises `parse_state_file_strict`, `get_current_round`, and `find_active_loop`. Helpers create normal, finalize, and cancel states at [test-state-transition-robustness.sh](/Users/wangweiyang/GitHub/humanize/tests/robustness/test-state-transition-robustness.sh:30).
- inputs_outputs_state: Inputs are temporary `.humanize/rlcr/<timestamp>` trees and generated `state.md`, `finalize-state.md`, and `cancel-state.md` files. Outputs are pass/fail records and a final test summary at lines 419-424. It mutates only temporary test state.
- gates_or_invariants: Valid rounds 0, 5, and max round parse successfully at lines 98-138. Finalize state is active and can coexist with normal state at lines 148-171. Cancel state is terminal/non-active, and a newer regular state after cancel is discoverable at lines 182-207. Non-numeric rounds and missing required fields are rejected at lines 259-361.
- dependencies_and_callers: Sources [loop-common.sh](/Users/wangweiyang/GitHub/humanize/hooks/lib/loop-common.sh:1) and `tests/test-helpers.sh` at lines 14-17. It directly validates behavior implemented by `resolve_active_state_file`, `find_active_loop`, `get_current_round`, and `parse_state_file_strict`.
- edge_cases_or_failure_modes: Negative rounds are parsed but flagged as possibly erroneous at lines 217-236. Rounds exceeding `max_iterations` are parsed, with enforcement declared elsewhere at lines 238-257. Discovery uses lexicographic ordering rather than timestamp validation at lines 385-402. Nested state files in the wrong location are ignored at lines 404-417.
- validation_or_tests: This file is itself the validation artifact for state transition robustness and complements broader state/session/concurrency tests elsewhere under `tests/robustness`.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 7/7 item headings present, each assigned item_id appears exactly once as a heading
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`