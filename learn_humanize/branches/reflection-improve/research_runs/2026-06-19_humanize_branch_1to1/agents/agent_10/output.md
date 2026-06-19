# agent_10 reflection-improve 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 7
- source_commit: `13a47fb2260667a272b448e8d3c1a521f2382590`

## Item Evidence

### REFLECTION_IMPROVE-HZ-010 `directory` `templates`
- cursor: `[_]`
- core_role: `templates` is a small template surface for BitLesson project memory. Its only recursive child is `templates/bitlesson.md`, a strict Markdown schema used to initialize `.humanize/bitlesson.md`.
- algorithmic_behavior: `templates/bitlesson.md:5-19` defines the required field order for reusable lessons: lesson id, scope, problem, root cause, solution, constraints, validation evidence, and source rounds. `scripts/setup-rlcr-loop.sh` references this template through `PLUGIN_BITLESSON_TEMPLATE` and `scripts/bitlesson-init.sh` copies it into the project BitLesson file when missing.
- inputs_outputs_state: input is the static template file; output is an initialized `.humanize/bitlesson.md` knowledge base used by later RLCR rounds. The template itself has no mutable state, but it seeds state consumed by `bitlesson-selector` and BitLesson delta validation.
- gates_or_invariants: the invariant is schema discipline: entries must preserve the exact field order in `templates/bitlesson.md:7-19`. The initialized file starts with an `## Entries` section at `templates/bitlesson.md:21-23`.
- dependencies_and_callers: callers include `scripts/setup-rlcr-loop.sh` around its BitLesson initialization path, `scripts/bitlesson-init.sh`, `scripts/bitlesson-select.sh`, and the stop hook’s BitLesson delta check at `hooks/loop-codex-stop-hook.sh:749-764`. Documentation in `docs/bitlesson.md` describes initialization from this template.
- edge_cases_or_failure_modes: as a static schema, the directory can only fail by being missing, malformed, or too vague for downstream validators. Empty initialized knowledge bases are explicitly handled by the stop hook’s BitLesson delta policy via `bitlesson_allow_empty_none`.
- validation_or_tests: related validation is indirect: BitLesson routing tests and stop-hook delta validation exercise the initialized file format, while `tests/test-template-references.sh` checks template references generally.
- skip_candidate: `yes: directory is peripheral seed data, not an executable state-machine implementation; it is still algorithm-adjacent because RLCR BitLesson gates depend on the initialized file contract`

### REFLECTION_IMPROVE-HZ-040 `file` `hooks/loop-codex-stop-hook.sh`
- cursor: `[_]`
- core_role: primary RLCR stop hook and state-transition gate. It intercepts Claude exit attempts, validates loop state and work artifacts, runs Codex review, and either blocks with the next prompt or transitions the loop to finalize, methodology-analysis, max-iteration, stop, or terminal complete states.
- algorithmic_behavior: reads hook JSON from stdin at `hooks/loop-codex-stop-hook.sh:28`, resolves the active session-scoped loop at `:61-68`, parses frontmatter at `:93-157`, validates schema and branch/plan integrity at `:172-378`, blocks incomplete tasks at `:387-435`, caches git state and checks large files/git cleanliness at `:471-705`, requires summaries and optional BitLesson deltas at `:707-764`, validates Round 0 goal tracker initialization at `:770-841`, then builds review prompts and invokes Codex at `:891-1455`.
- inputs_outputs_state: inputs include hook JSON, `.humanize/rlcr/<timestamp>/state.md` or phase state files, plan backup, summaries, goal tracker, git status, Codex CLI output, template files, and environment variables such as `CLAUDE_PROJECT_DIR`, `XDG_CACHE_HOME`, and `HUMANIZE_CODEX_BYPASS_SANDBOX`. Outputs are Claude hook JSON blocks, review prompt/result files, cache debug logs, next-round prompt/summary skeletons, and renamed state files such as `finalize-state.md` or `complete-state.md`.
- gates_or_invariants: fails closed on invalid `codex_model` and effort at `:158-170`, missing `current_round` or `max_iterations` at `:172-185`, stale schema at `:204-249`, branch changes at `:285-295`, dirty git at `:614-672`, unpushed commits when required at `:678-704`, missing summaries at `:718-743`, placeholder goal tracker content at `:781-841`, and review phase marker tampering at `:1632-1648`.
- dependencies_and_callers: sources `hooks/lib/loop-common.sh`, `scripts/portable-timeout.sh`, and `hooks/lib/methodology-analysis.sh` at `:45-54`; uses `hooks/check-todos-from-transcript.py`; renders templates from `prompt-template/block`, `prompt-template/codex`, and `prompt-template/claude`; is installed via `hooks/hooks.json` and wrapped by `scripts/rlcr-stop-gate.sh`.
- edge_cases_or_failure_modes: no active loop or session mismatch exits open at `:64-68`; malformed state ends unexpectedly rather than defaulting silently; git timeouts trigger stale `index.lock` cleanup at `:447-462`; Codex failure, missing result, or empty result blocks with debug file references at `:1467-1565`; `COMPLETE` only advances into code review/finalize, while `STOP` terminates or enters methodology analysis at `:1657-1689`.
- validation_or_tests: directly exercised by finalize, plan-file, agent-teams, unified config, and robustness tests; assigned tests cover adjacent contracts for session filtering, input validation, allowlists, and template-driven block prompts.
- skip_candidate: `no`

### REFLECTION_IMPROVE-HZ-070 `file` `tests/test-allowlist-validators.sh`
- cursor: `[_]`
- core_role: executable specification for the narrow allowlist that lets RLCR agents read/write/edit specific historical round files while still blocking general todos, summaries, and wrong-loop paths.
- algorithmic_behavior: sets up a git-backed fake project and active loop at `tests/test-allowlist-validators.sh:33-64`, then tests `is_allowlisted_file` directly at `:72-126`, Write validator behavior at `:135-185`, Edit validator behavior at `:191-228`, Read validator behavior at `:234-284`, and Bash validator path-restricted behavior at `:290-383`.
- inputs_outputs_state: inputs are synthetic hook JSON payloads for `Read`, `Write`, `Edit`, and `Bash`, plus a fake `.humanize/rlcr/<timestamp>/state.md` with `current_round: 5`. Outputs are validator exit codes and stderr messages; the test exits with failure count at `:393`.
- gates_or_invariants: only `round-1-todos.md`, `round-2-todos.md`, `round-0-summary.md`, and `round-1-summary.md` under the active loop dir are allowed, matching `hooks/lib/loop-common.sh:598-616`. Same basename in `/tmp`, an old loop dir, or a different root is blocked.
- dependencies_and_callers: depends on `hooks/lib/loop-common.sh`, `hooks/loop-write-validator.sh`, `hooks/loop-edit-validator.sh`, `hooks/loop-read-validator.sh`, and `hooks/loop-bash-validator.sh`. The implementation paths delegate active-loop discovery through `find_active_loop`.
- edge_cases_or_failure_modes: detects path spoofing by basename, stale loop directories, missing absolute active loop path in Bash commands, and wrong round numbers. It also checks historical summary exceptions without opening the allowlist too broadly.
- validation_or_tests: this file is itself validation. Passing requires exact exit behavior: normal allowlist exits `0`, blocked validator operations exit `2` and mention the relevant reason such as todos or round.
- skip_candidate: `no`

### REFLECTION_IMPROVE-HZ-100 `file` `tests/test-session-id.sh`
- cursor: `[_]`
- core_role: executable specification for RLCR session isolation. It ensures concurrent sessions in one project do not hijack each other’s active loop state, validators, stop hooks, or cancellation behavior.
- algorithmic_behavior: verifies setup writes an empty `session_id` and `.pending-session-id` signal at `tests/test-session-id.sh:31-107`; checks `loop-post-bash-hook.sh` records the hook `session_id` after a real setup command at `:110-165`; tests active-loop matching, finalize-state matching, parser extraction, and cancel behavior at `:203-438`; then exercises filter-first and stale-revival prevention semantics at `:577-784`.
- inputs_outputs_state: inputs are fake state files, `.humanize/.pending-session-id`, PostToolUse JSON containing `session_id`, and fake setup commands. Outputs are mutated `state.md` session fields, removed or preserved signal files, returned active loop paths, and renamed cancel-state files.
- gates_or_invariants: `find_active_loop` must match the newest directory for a session and must not revive older stale loops when the newest matching session directory is terminal. Empty stored session IDs remain backward-compatible. `loop-post-bash-hook.sh` must consume the signal only for boundary-aware setup invocations.
- dependencies_and_callers: depends on `hooks/lib/loop-common.sh` functions `extract_session_id`, `resolve_active_state_file`, `resolve_any_state_file`, `find_active_loop`, and `parse_state_file`; also depends on `hooks/loop-post-bash-hook.sh`, `scripts/setup-rlcr-loop.sh`, and `scripts/cancel-rlcr-loop.sh`.
- edge_cases_or_failure_modes: covers special characters in session IDs, quoted and unquoted setup commands, tab-delimited commands, substring false positives such as `echo setup-rlcr-loop.sh`, quoted-prefix concatenation, cancel-state terminal blocking, and different sessions coexisting without interference.
- validation_or_tests: this file is the validation. It asserts state mutation, signal one-shot semantics, active loop discovery, parser output, and safe command-boundary matching across more than 30 scenarios.
- skip_candidate: `no`

### REFLECTION_IMPROVE-HZ-130 `file` `prompt-template/block/goal-tracker-not-initialized.md`
- cursor: `[_]`
- core_role: block template for the Round 0 goal-tracker initialization gate in the stop hook.
- algorithmic_behavior: rendered when `hooks/loop-codex-stop-hook.sh:775-841` finds placeholder content in the Ultimate Goal, Acceptance Criteria, or Active Tasks sections of `goal-tracker.md`. The template tells the agent to replace placeholders, define 3-7 testable acceptance criteria, populate active tasks, and retry exit.
- inputs_outputs_state: inputs are `GOAL_TRACKER_FILE` and `MISSING_ITEMS` substitutions at `hooks/loop-codex-stop-hook.sh:828-830`. Output is the `reason` string in a Claude hook JSON block with system message `Loop: Goal Tracker not initialized in Round 0`.
- gates_or_invariants: enforces that the immutable section can only be set in Round 0, stated at `prompt-template/block/goal-tracker-not-initialized.md:16`. After Round 0, later templates and validators require goal-tracker updates to go through summary requests rather than direct edits.
- dependencies_and_callers: called through `load_and_render_safe` from the stop hook; coordinated with goal tracker write/edit validators and the next-round prompt’s read-only goal tracker instruction.
- edge_cases_or_failure_modes: fallback text exists in the hook if the template is missing. The detection is section-scoped and placeholder-pattern based, reducing false positives from unrelated placeholder wording elsewhere in the file.
- validation_or_tests: covered indirectly by stop-hook tests around Round 0 goal tracker behavior and template reference checks.
- skip_candidate: `no`

### REFLECTION_IMPROVE-HZ-160 `file` `prompt-template/claude/next-round-prompt.md`
- cursor: `[_]`
- core_role: continuation prompt template emitted when Codex review finds issues and the RLCR loop must proceed to another implementation round.
- algorithmic_behavior: rendered at `hooks/loop-codex-stop-hook.sh:1740-1744` with `PLAN_FILE`, `REVIEW_CONTENT`, `GOAL_TRACKER_FILE`, and `BITLESSON_FILE`. It instructs the agent to reread the original plan, create tasks for all discovered issues, use BitLesson selection before each task, incorporate Codex’s review, and treat the goal tracker as read-only after Round 0.
- inputs_outputs_state: inputs are the original plan path, Codex review result, goal tracker path, and BitLesson file path. Output is `round-${NEXT_ROUND}-prompt.md`, which is then augmented with task-tag routing, optional agent-teams enforcement, optional open-question notice, post-alignment instructions, footer, push note, and goal-tracker update request sections.
- gates_or_invariants: enforces comprehensive issue tracking rather than only fixing highest-priority findings at `prompt-template/claude/next-round-prompt.md:12-13`; enforces BitLesson discipline at `:15-19`; enforces read-only goal tracker behavior at `:27-36`.
- dependencies_and_callers: called by the stop hook after incrementing `current_round` at `hooks/loop-codex-stop-hook.sh:1695-1698`. It coordinates with `prompt-template/claude/next-round-footer.md`, `goal-tracker-update-request.md`, `open-question-notice.md`, and `post-alignment-action-items.md`.
- edge_cases_or_failure_modes: if missing, the stop hook uses an inline fallback at `hooks/loop-codex-stop-hook.sh:1727-1739`. In agent-teams mode, the hook injects delegation enforcement into this prompt at `:1746-1768`.
- validation_or_tests: template existence and reference coverage are handled by template tests; behavior is indirectly exercised by stop-hook tests that verify next-round prompt creation and review-loop continuation.
- skip_candidate: `no`

### REFLECTION_IMPROVE-HZ-190 `file` `tests/robustness/test-hook-input-robustness.sh`
- cursor: `[_]`
- core_role: robustness specification for hook JSON parsing, command modification detection, and monitor edge cases. It validates that production validators and monitor paths reject bad input gracefully instead of crashing or silently accepting unsafe forms.
- algorithmic_behavior: invokes real validators with valid JSON at `tests/robustness/test-hook-input-robustness.sh:35-69`; malformed, missing, deeply nested, non-UTF8, null-byte, long, special-character, Unicode, and unknown-tool inputs at `:71-235`; monitor/log/terminal edge cases at `:245-341`; command modification detection at `:351-370`; production monitor helper integration at `:381-433`; and real `_humanize_monitor_codex` runs under missing, narrow-terminal, and ANSI-log conditions at `:444-664`.
- inputs_outputs_state: inputs are synthetic hook JSON, generated logs with ANSI and binary content, fake goal trackers, fake `.humanize/rlcr` sessions, and shimmed terminal functions. Outputs are validator exit codes, parser return strings, and monitor exit codes.
- gates_or_invariants: validator inputs must pass `validate_hook_input`, reject malformed or unsafe JSON with non-signal exits, reject nesting beyond depth 30, reject invalid UTF-8 when `iconv` is available, require needed `tool_input` fields, and allow unknown tools to pass through.
- dependencies_and_callers: depends on `hooks/lib/loop-common.sh`, `hooks/loop-read-validator.sh`, `hooks/loop-write-validator.sh`, `hooks/loop-bash-validator.sh`, `scripts/humanize.sh`, and monitor helper behavior. The relevant parser implementation is in `hooks/lib/loop-common.sh:80-154`.
- edge_cases_or_failure_modes: explicitly covers 10KB commands, shell metacharacters, Unicode paths, non-UTF8 bytes, null bytes stripped by Bash, deleted logs, binary logs, rapid log growth, narrow/wide terminals, missing session directories, and ANSI-coded logs.
- validation_or_tests: this file is itself validation; passing requires graceful exits below signal range, correct parser output shape, and no monitor crashes under simulated terminal/log failures.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `7/7 item evidence headings present; each assigned heading appears once`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`