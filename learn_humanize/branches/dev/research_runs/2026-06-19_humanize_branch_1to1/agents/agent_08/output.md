# agent_08 dev 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 8
- source_commit: `eec73c4dfcc4f9791933e3cbaa616d4f261ed9e2`

## Item Evidence

### DEV-HZ-008 `directory` `scripts`
- cursor: `[_]`
- core_role: `scripts/` is the repo’s executable command layer for Humanize/RLCR. Recursively inspected all 25 shell files under `scripts/` and `scripts/lib/`; they cover RLCR bootstrap/cancel/gate wrappers, one-shot model consultations, BitLesson memory selection and delta validation, command IO validation for idea/plan flows, installer/runtime hydration, terminal/web monitoring, config/model routing, and timeout portability.
- algorithmic_behavior: The primary state-machine entry is `scripts/setup-rlcr-loop.sh`, which validates a plan, asserts clean git state, creates `.humanize/rlcr/<timestamp>/`, writes state frontmatter, initializes BitLesson, goal tracker, summaries, contracts, and the round-0 prompt (`setup-rlcr-loop.sh:404-681`, `826-923`, `1087-1436`). `scripts/rlcr-stop-gate.sh` wraps the Stop hook for non-hook skill workflows and maps hook JSON decisions to allow/block exit codes (`rlcr-stop-gate.sh:99-178`). `scripts/cancel-rlcr-loop.sh` and `scripts/cancel-rlcr-session.sh` transition active `state.md`, `methodology-analysis-state.md`, or `finalize-state.md` to `cancel-state.md` with `.cancel-requested` markers (`cancel-rlcr-loop.sh:103-167`, `cancel-rlcr-session.sh:94-123`). The `ask-*` scripts create `.humanize/skill/<id>/` records, run model CLIs with timeouts, and store output/metadata (`ask-codex.sh:202-238`, `323-444`; `ask-gemini.sh:184-218`, `279-388`).
- inputs_outputs_state: Inputs include plan paths, mode flags, model/timeout options, `.directions.json` files, idea drafts, annotated plans, project config, and hook-like session/transcript fields. Outputs include RLCR loop artifacts under `.humanize/rlcr`, BitLesson KB `.humanize/bitlesson.md`, skill invocation records under `.humanize/skill`, generated run metadata for explore/gen/refine validators, installed runtime bundles, hooks config, and monitor/status display. State transitions are file-name driven: `state.md` active, `methodology-analysis-state.md` analysis, `finalize-state.md` finalization, `cancel-state.md` terminal cancel.
- gates_or_invariants: `setup-rlcr-loop.sh` rejects missing deps, concurrent active loops, invalid Agent Teams env, absolute/spaced/metacharacter plan paths, symlinked plan files or parent dirs, plans outside project, submodule plans, bad tracking status, too-short or comment-only plans, YAML-unsafe branches, invalid model/effort, and dirty git state except untracked `.humanize` runtime paths (`setup-rlcr-loop.sh:331-384`, `390-401`, `460-681`, `691-746`). IO validators enforce schemas/caps/output collisions (`validate-directions-json.sh:40-121`, `validate-explore-idea-io.sh:186-477`, `validate-gen-idea-io.sh:69-218`, `validate-gen-plan-io.sh:82-185`, `validate-refine-plan-io.sh:589-692`). BitLesson delta gates reject missing/invalid/inconsistent summary declarations (`bitlesson-validate-delta.sh:181-387`).
- dependencies_and_callers: `scripts/` coordinates heavily with `hooks/lib/loop-common.sh`, `hooks/loop-codex-stop-hook.sh`, prompt templates, `templates/bitlesson.md`, and `config/default_config.json`. Config loading merges default/user/project JSON (`scripts/lib/config-loader.sh:63-159`); model routing selects Codex vs Claude and maps effort (`scripts/lib/model-router.sh:10-91`); portable timeout abstracts GNU/BSD/Python timeout (`portable-timeout.sh:10-76`). Installers sync runtime pieces into Kimi/Codex skill dirs and install Codex native hooks (`install-skill.sh:75-193`, `281-360`, `527-573`; `install-codex-hooks.sh:84-241`).
- edge_cases_or_failure_modes: The directory handles macOS/Linux timeout differences, missing `codex`/`gemini`/`jq`/`git`, home cache unwritable fallback, unsupported model names, missing/malformed JSON config, invalid hook support, stale or unsafe plan inputs, symlink traversal, dirty checkout, duplicate direction selectors, malformed comment blocks, missing gen-plan sections, and terminal monitor cleanup. Some scripts intentionally create files/directories; in this branch export those are research-only and were not executed.
- validation_or_tests: Covered by tests referenced in the assignment plus broader tests such as `tests/test-bitlesson-select-routing.sh`, `tests/test-bitlesson-validate-delta.sh`, `tests/test-config-merge.sh`, `tests/test-codex-hook-install.sh`, `tests/test-unified-codex-config.sh`, and `tests/run-all-tests.sh`, which includes `test-humanize-escape.sh` and `robustness/test-path-validation-robustness.sh`.
- skip_candidate: `no`

### DEV-HZ-038 `file` `config/codex-hooks.json`
- cursor: `[_]`
- core_role: Codex-native hook installation template for RLCR Stop enforcement. It registers one `Stop` command pointing to the installed Humanize runtime’s `hooks/loop-codex-stop-hook.sh`.
- algorithmic_behavior: The template defines a `Stop` hook group with `type: "command"`, command placeholder `{{HUMANIZE_RUNTIME_ROOT}}/hooks/loop-codex-stop-hook.sh`, timeout `7200`, and status message `humanize RLCR stop hook` (`config/codex-hooks.json:1-17`). It does not itself execute logic; `scripts/install-codex-hooks.sh` hydrates and merges it.
- inputs_outputs_state: Input is the `{{HUMANIZE_RUNTIME_ROOT}}` placeholder. Output is a concrete Codex `hooks.json` entry after installer substitution and shell-quoting. Runtime state affected indirectly is RLCR loop gating on Codex Stop events.
- gates_or_invariants: The command must resolve inside the installed runtime root and must be available long enough for Codex review/loop checks, hence the 7200-second timeout (`config/codex-hooks.json:9-11`). Installer validates native Codex hooks support and rejects legacy `codex_hooks` feature use (`install-codex-hooks.sh:84-117`).
- dependencies_and_callers: Consumed by `scripts/install-codex-hooks.sh` via `HOOKS_TEMPLATE="$REPO_ROOT/config/codex-hooks.json"` (`install-codex-hooks.sh:14`). The installer replaces the runtime placeholder safely, removes old managed stop-hook entries, appends the managed Stop hook, and enables the Codex `hooks` feature (`install-codex-hooks.sh:119-241`).
- edge_cases_or_failure_modes: Misconfigured runtime root would point Codex at a nonexistent hook; installer mitigates spaces/metacharacters by JSON escaping and `shlex.quote` (`install-codex-hooks.sh:139-153`). Unsupported or legacy Codex CLI hook feature blocks installation (`install-codex-hooks.sh:84-117`).
- validation_or_tests: `tests/test-codex-hook-install.sh` exercises Codex install behavior; docs in `docs/install-for-codex.md` reference `./scripts/install-codex-hooks.sh`.
- skip_candidate: `no`

### DEV-HZ-068 `file` `templates/bitlesson.md`
- cursor: `[_]`
- core_role: Seed template for the project-local BitLesson knowledge base, consumed during RLCR setup and by BitLesson selection/delta validation.
- algorithmic_behavior: Defines a strict entry schema and field order: lesson heading, `Lesson ID`, `Scope`, problem/root cause/solution/constraints/validation/source rounds, then an `## Entries` insertion area (`templates/bitlesson.md:1-23`). It standardizes memory records so downstream selectors and validators can find `## Lesson:` and `Lesson ID:` markers.
- inputs_outputs_state: Input to `scripts/bitlesson-init.sh` as `--template`; output is `.humanize/bitlesson.md` if absent. Existing KB files are preserved and not overwritten (`bitlesson-init.sh:83-86`).
- gates_or_invariants: Template demands reusable, precise entries and stable field order (`templates/bitlesson.md:3-18`). Validators later require concrete IDs of the form `BL-YYYYMMDD-short-name` for `add|update` deltas (`bitlesson-validate-delta.sh:322-383`).
- dependencies_and_callers: `setup-rlcr-loop.sh` initializes `.humanize/bitlesson.md` from this template (`setup-rlcr-loop.sh:865-871`). `bitlesson-select.sh` short-circuits to `LESSON_IDS: NONE` when no `## Lesson:` entries exist (`bitlesson-select.sh:87-97`). Stop hook invokes BitLesson delta validation when enabled (`loop-codex-stop-hook.sh:864-883`).
- edge_cases_or_failure_modes: A placeholder-only KB intentionally produces no lessons. A path existing but not a regular file blocks initialization (`bitlesson-init.sh:78-80`). Empty/whitespace-only KB is rejected by selector (`bitlesson-select.sh:87-90`).
- validation_or_tests: `tests/test-bitlesson-select-routing.sh` covers placeholder short-circuiting; `tests/test-bitlesson-validate-delta.sh` covers delta/ID behavior; docs in `docs/bitlesson.md` describe the same workflow.
- skip_candidate: `no`

### DEV-HZ-098 `file` `tests/test-humanize-escape.sh`
- cursor: `[_]`
- core_role: Executable specification for `.humanize` path-staging protection and zsh-safe directory iteration. It tests production helper `git_adds_humanize` from `hooks/lib/loop-common.sh`.
- algorithmic_behavior: Defines `assert_blocks` and `assert_allows`, lowercases commands via `to_lower`, then evaluates `git_adds_humanize` (`tests/test-humanize-escape.sh:44-70`). Test groups cover direct `.humanize` paths, quoted variants, force/all/broad add flags, chained commands, `git -C`/`--git-dir` forms, allowed non-add commands, patch mode, similarly named files, and find-based iteration for empty/dotfile-only/state/session directories (`tests/test-humanize-escape.sh:83-197`, `209-337`).
- inputs_outputs_state: Inputs are synthetic command strings and temporary `/tmp/test-humanize-*` directories. Outputs are PASS/FAIL counters and exit 0 only when no failures remain (`tests/test-humanize-escape.sh:342-357`). No repo state should be modified beyond temp dirs.
- gates_or_invariants: The invariant is that `.humanize/` runtime state must not be added to git, including `git add -f`, `git add -A`, direct/quoted/path variants, and broad forced scopes. Conversely `.humanizeconfig`, `.humanize-backup`, `.humanizerc`, `git status`, `git diff`, `git log`, and patch adds must remain allowed (`tests/test-humanize-escape.sh:180-197`).
- dependencies_and_callers: Sources `hooks/lib/loop-common.sh` (`tests/test-humanize-escape.sh:16-18`). Production implementation splits shell command segments and detects git add subcommands, direct `.humanize` references, force/all flags, broad scopes, and gitignore checks (`loop-common.sh:1263-1381`). Bash validator calls this helper before allowing Bash git commands (`hooks/loop-bash-validator.sh`, found reference at `loop-bash-validator.sh:242-247`).
- edge_cases_or_failure_modes: Protects against quoted paths, `./.humanize`, nested `.humanize/rlcr/...`, chained commands, wildcard/force bypasses of `.gitignore`, zsh glob errors in empty dirs, dotfiles-only dirs, and false positives for similarly named files.
- validation_or_tests: This file is itself the validation asset and is listed in `tests/run-all-tests.sh`. It also validates assumptions explicitly noted by production comments in `loop-common.sh:1427-1429`.
- skip_candidate: `no`

### DEV-HZ-128 `file` `hooks/lib/loop-bg-tasks.sh`
- cursor: `[_]`
- core_role: Background-task guard library for the RLCR Stop hook. It prevents the RLCR state machine from running expensive/terminal gates while Claude async Agent/Bash work is still pending.
- algorithmic_behavior: Provides helpers to expand leading tilde paths, extract `transcript_path`, derive loop start UTC timestamp from local loop-dir names, derive Claude task output dirs, test task liveness with `lsof`, list launched-minus-completed background task IDs, count/boolean-check pending tasks, and run the Stop-hook short-circuit sequence (`loop-bg-tasks.sh:23-46`, `65-95`, `107-153`, `193-297`, `311-435`).
- inputs_outputs_state: Inputs are hook JSON, loop directory, hook session id, Claude transcript JSONL, and task output files under `/tmp/claude-<uid>/<slug>/<sid>/tasks`. Outputs are pending task IDs/counts, JSON system messages, creation/removal of `bg-pending.marker`, or return to normal Stop-hook processing (`loop-bg-tasks.sh:392-404`, `428-433`).
- gates_or_invariants: Guard order is explicit: ambiguous-caller marker guard, cross-session parked-loop guard, pending background early exit, same-session stale-marker cleanup (`loop-bg-tasks.sh:299-310`). Missing transcript, non-file transcript, absent `jq`, or parse failure returns nonzero from `list_pending_background_task_ids`, causing callers not to infer “safe to cleanup” (`loop-bg-tasks.sh:187-192`, `418-425`).
- dependencies_and_callers: Depends on `loop-common.sh` constants and `resolve_active_state_file` (`loop-bg-tasks.sh:15-16`, `307-308`). `loop-common.sh` sources this library at the bottom (`loop-common.sh:1573-1583`), and `hooks/loop-codex-stop-hook.sh` delegates before normal gates (`loop-codex-stop-hook.sh:71-83`).
- edge_cases_or_failure_modes: Handles `~` without `eval`; local timestamp to UTC conversion across GNU/BSD `date`; legacy XML task notifications plus SDK `task_notification`; transcript launches before loop start; absent task output files and missing `lsof` fail-open as alive; foreign session marker leaves artifacts untouched; ambiguous session-id callers exit silently (`loop-bg-tasks.sh:23-35`, `75-93`, `165-185`, `120-141`, `322-367`).
- validation_or_tests: Related tests include stop-hook background/legacy tests found by reference (`tests/test-stop-hook-bg-allow.sh`, `tests/test-stop-hook-legacy-compat.sh`) and transcript/task behavior is indirectly covered by hook-system robustness tests.
- skip_candidate: `no`

### DEV-HZ-158 `file` `prompt-template/block/plan-file-modified.md`
- cursor: `[_]`
- core_role: User-facing block template for the plan-integrity gate when an active RLCR loop detects the source plan changed from its loop backup.
- algorithmic_behavior: Renders the blocked condition, states plan-file modification is forbidden during an active session, gives a cancel/update/restart sequence, and includes backup path (`prompt-template/block/plan-file-modified.md:1-12`).
- inputs_outputs_state: Inputs are `{{PLAN_FILE}}` and `{{BACKUP_PATH}}`. Output is a block reason embedded in Stop-hook JSON, not a state transition by itself.
- gates_or_invariants: Enforces plan immutability for implementation phase. The invariant is that active-loop plan scope remains anchored to the backup copy in `.humanize/rlcr/<timestamp>/plan.md`; changing plan requires cancellation and restart.
- dependencies_and_callers: `hooks/loop-codex-stop-hook.sh` loads this template when `diff -q "$FULL_PLAN_PATH" "$BACKUP_PLAN"` fails and emits `decision: block` with message `Loop: Blocked - plan file modified` (`loop-codex-stop-hook.sh:377-396`). `scripts/setup-rlcr-loop.sh` creates the backup (`setup-rlcr-loop.sh:834-856`).
- edge_cases_or_failure_modes: In review phase, plan integrity is skipped because review no longer needs the plan file (`loop-codex-stop-hook.sh:321-327`). Missing backup and deleted plan have separate block messages before this template (`loop-codex-stop-hook.sh:332-356`).
- validation_or_tests: Covered by plan-file hook/validation tests such as `tests/test-plan-file-hooks.sh`, `tests/test-plan-file-validation.sh`, and robustness plan-file tests by reference.
- skip_candidate: `no`

### DEV-HZ-188 `file` `prompt-template/claude/review-phase-prompt.md`
- cursor: `[_]`
- core_role: Prompt template for RLCR review phase after Codex code review finds blocking issues. It defines how Claude should classify and fix review findings without letting side issues take over the loop.
- algorithmic_behavior: Requires re-reading plan, goal tracker, and round contract before code changes; injects `{{REVIEW_CONTENT}}`; classifies findings as blocking side issues or queued side issues; mandates `[blocking]`/`[queued]` task tags; forbids new `[mainline]` tasks unless review proves previous objective incomplete; requires contract refresh, blocking fixes first, commit, and summary (`review-phase-prompt.md:5-40`).
- inputs_outputs_state: Inputs are `{{PLAN_FILE}}`, `{{GOAL_TRACKER_FILE}}`, `{{ROUND_CONTRACT_FILE}}`, `{{REVIEW_CONTENT}}`, and `{{SUMMARY_FILE}}`. Output is the next round prompt consumed by Claude and returned in Stop-hook block JSON.
- gates_or_invariants: Invariant is a single stable mainline objective during review. `COMPLETE` has no effect in review phase, and the loop continues until no `[P0-9]` issues are found (`review-phase-prompt.md:12`, `20-32`, `53-58`).
- dependencies_and_callers: Loaded by `hooks/loop-codex-stop-hook.sh` when constructing review-phase follow-up prompts (`loop-codex-stop-hook.sh:1560-1582`). The hook appends BitLesson selection instructions if required and task-tag routing notes (`loop-codex-stop-hook.sh:1583-1597`).
- edge_cases_or_failure_modes: Prevents review findings from becoming scope drift by separating blocking vs queued items. It requires summary confirmation that goal tracker was updated if blocking/queued issue lists changed, and allows a Goal Tracker Update Request only if reconciliation still needs Codex help (`review-phase-prompt.md:44-51`).
- validation_or_tests: `tests/test-agent-teams.sh` references this template for review-phase behavior; stop-hook tests exercise review-loop prompt construction.
- skip_candidate: `no`

### DEV-HZ-218 `file` `tests/robustness/test-path-validation-robustness.sh`
- cursor: `[_]`
- core_role: Executable robustness specification for production plan-path and content validation in `scripts/setup-rlcr-loop.sh`.
- algorithmic_behavior: Creates an isolated temp git repo, installs a mock `codex`, writes valid plan fixtures, runs `setup-rlcr-loop.sh` with `CLAUDE_PROJECT_DIR="$TEST_DIR"`, then interprets specific validation messages as accepted/rejected path behavior (`test-path-validation-robustness.sh:16-48`, `76-113`).
- inputs_outputs_state: Inputs are plan path strings and generated plan files/symlinks/dirs. Outputs are pass/fail records via shared test helpers, ending with `print_test_summary` and its exit code (`test-path-validation-robustness.sh:486-487`). Temporary repo state is disposable.
- gates_or_invariants: Positive cases must accept normal relative paths, root filenames, dash/underscore, nested dirs, and dots (`test-path-validation-robustness.sh:122-169`). Negative cases must reject absolute paths, spaces, shell metacharacters, command-injection characters, glob chars, tilde, brackets/braces, symlink files, symlink parent dirs, symlink chains, empty/comment-only/too-short/nonexistent files, and directory paths (`test-path-validation-robustness.sh:179-377`, `425-480`). Long filenames and 10-level nested paths are expected to work if filesystem permits (`test-path-validation-robustness.sh:387-412`).
- dependencies_and_callers: Exercises `scripts/setup-rlcr-loop.sh`; production logic implements the same checks at `setup-rlcr-loop.sh:460-681`. Uses `tests/test-helpers.sh` for temp setup and summary functions. Requires git operations in the temp repo.
- edge_cases_or_failure_modes: The test documents Unicode/CJK/emoji path support as allowed, while shell metacharacters remain rejected (`test-path-validation-robustness.sh:414-415`). It treats later “codex required” or “must be gitignored” errors as evidence path validation passed (`test-path-validation-robustness.sh:97-105`), so it isolates path/content validation from downstream setup gates.
- validation_or_tests: This file is the validation asset and is listed in `tests/run-all-tests.sh`. I did not execute it because the assigned branch export is read-only and the test creates temp repos/files.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 8 evidence sections above; each assigned row is represented once as its own item section
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`