# agent_02 ask-codex-skill 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 6
- source_commit: `caf375a20530c8bb81e8e8e103a8598c25c11bb0`

## Item Evidence

### ASK_CODEX_SKILL-HZ-002 `directory` `agents`
- cursor: `[_]`
- core_role: Contains the repository’s delegated agent definition for draft relevance screening. The recursive directory inspection found one child file: `agents/draft-relevance-checker.md`.
- algorithmic_behavior: `agents/draft-relevance-checker.md:1-6` defines frontmatter consumed by the agent/command system: name `draft-relevance-checker`, haiku model, and tools `Read, Glob, Grep`. Its body instructs the agent to inspect repo docs/structure, compare a draft against repo concepts/files/features, and return one of two verdict prefixes, `RELEVANT:` or `NOT_RELEVANT:` at `agents/draft-relevance-checker.md:12-30`.
- inputs_outputs_state: Input is draft document content supplied by the invoking command. The agent may read/glob/grep repository files to build context. Output is a single verdict line plus explanation; it does not persist state or mutate files.
- gates_or_invariants: The relevance check is intentionally lenient: if the draft could reasonably connect to the repository, mark relevant; if unsure, lean relevant (`agents/draft-relevance-checker.md:31-36`). The strict output contract is the verdict prefix at `agents/draft-relevance-checker.md:27-30`.
- dependencies_and_callers: `commands/gen-plan.md:50-65` invokes `humanize:draft-relevance-checker` during Phase 2 after IO validation. `tests/test-gen-plan.sh:105-158` validates the agent file exists and has expected name/model/tools; additional checks cover naming/frontmatter/content at `tests/test-gen-plan.sh:241-421`.
- edge_cases_or_failure_modes: Skip candidate for core RLCR state-machine mechanics because it does not implement loop transitions, hooks, or validators. It is still algorithm-adjacent because gen-plan uses it as a relevance gate before plan generation.
- validation_or_tests: Covered by `tests/test-gen-plan.sh` agent structure checks and by command-level instructions in `commands/gen-plan.md:56-70`.
- skip_candidate: `yes: auxiliary gen-plan relevance agent, not a direct RLCR transition or validator implementation`

### ASK_CODEX_SKILL-HZ-032 `file` `hooks/loop-read-validator.sh`
- cursor: `[_]`
- core_role: PreToolUse Read hook for RLCR read-access safety. It prevents Claude from reading stale/wrong round prompt or summary files, disallows most todos reads, and enforces active-loop/session locality.
- algorithmic_behavior: Reads hook JSON from stdin (`hooks/loop-read-validator.sh:25`), validates JSON and nesting (`hooks/loop-read-validator.sh:27-35`), exits for non-Read tools (`hooks/loop-read-validator.sh:39-41`), requires `tool_input.file_path` (`hooks/loop-read-validator.sh:43-49`), extracts `session_id` (`hooks/loop-read-validator.sh:51-52`), then applies file-type-specific gates.
- inputs_outputs_state: Input is Claude hook JSON with `tool_name`, `tool_input.file_path`, and optional `session_id`. Output is exit `0` allow, exit `1` malformed/unsafe input, or exit `2` user-facing block message on stderr. It reads `.humanize/rlcr/<session>/state.md` or `finalize-state.md` but does not write state.
- gates_or_invariants: Todos access is blocked unless the file is allowlisted for the active loop (`hooks/loop-read-validator.sh:58-66`). Summary/prompt files must be inside `.humanize/rlcr/` (`hooks/loop-read-validator.sh:72-78`, `122-132`), match the current round unless allowlisted (`hooks/loop-read-validator.sh:138-151`), and use the exact active loop path (`hooks/loop-read-validator.sh:157-168`). Malformed state fails closed (`hooks/loop-read-validator.sh:91-99`).
- dependencies_and_callers: Registered as the Read PreToolUse hook in `hooks/hooks.json:33-40`. Depends on `hooks/lib/loop-common.sh` for `validate_hook_input`, `is_deeply_nested`, `find_active_loop`, `resolve_active_state_file`, `parse_state_file_strict`, allowlist logic, and template messages; depends on `hooks/lib/template-loader.sh:170-203` for safe rendering with fallbacks.
- edge_cases_or_failure_modes: No active loop means allow for round files (`hooks/loop-read-validator.sh:87-89`). Files that look like round files but lack extractable round number are allowed (`hooks/loop-read-validator.sh:105-108`). The `is_in_humanize_loop_dir` helper is substring-based (`hooks/lib/loop-common.sh:840-844`), so exact path equality later at `hooks/loop-read-validator.sh:159-168` is the stronger final invariant. Strict state parsing rejects missing frontmatter or required fields (`hooks/lib/loop-common.sh:386-448`).
- validation_or_tests: `tests/test-allowlist-validators.sh:231-283` covers allowed historical todos/summaries and blocked future files. `tests/test-finalize-phase.sh:839-850` covers finalize-state parsing. `tests/robustness/test-hook-input-robustness.sh` and `tests/robustness/test-hook-system-robustness.sh` exercise malformed JSON, null/UTF-8/nesting, and concurrent hook paths.
- skip_candidate: `no`

### ASK_CODEX_SKILL-HZ-062 `file` `tests/test-humanize-escape.sh`
- cursor: `[_]`
- core_role: Executable specification for `.humanize` escape/staging protection and zsh-safe directory iteration patterns used by humanize loop code.
- algorithmic_behavior: Sources `hooks/lib/loop-common.sh` (`tests/test-humanize-escape.sh:16-18`) and defines assertion wrappers around `git_adds_humanize` (`tests/test-humanize-escape.sh:44-70`). It lowercases commands before testing, matching production validator behavior.
- inputs_outputs_state: Input is fixed shell-command strings and temporary filesystem fixtures under `/tmp`. Output is PASS/FAIL counters and process exit `0` if no failures, else `1` (`tests/test-humanize-escape.sh:335-352`). Temporary directories are created and removed during tests (`tests/test-humanize-escape.sh:130-144`, `204-215`, `225-238`, `271-286`, `303-324`).
- gates_or_invariants: Direct `.humanize` path variants, quoted variants, force-add variants, all/broad-scope force adds, chained commands, and `git -C` forms must block (`tests/test-humanize-escape.sh:83-167`). Specific normal paths, `.gitignore`, `git status/diff/log`, patch mode, and similarly named non-`.humanize` files must allow (`tests/test-humanize-escape.sh:175-192`).
- dependencies_and_callers: Exercises `git_adds_humanize` at `hooks/lib/loop-common.sh:1058-1154`, which is called by `hooks/loop-bash-validator.sh:109-118`. The helper blocks direct `.humanize`, force broad-scope, all-scope when `.humanize` exists, and broad `.` or `*` when `.humanize` is not gitignored.
- edge_cases_or_failure_modes: Verifies `git add -A`/`--all` blocks only after `.humanize` exists (`tests/test-humanize-escape.sh:128-145`). Zsh safety cases verify empty directories, dotfile-only directories, no matching `*-state.md`, and timestamped session selection do not rely on unsafe globs (`tests/test-humanize-escape.sh:195-332`).
- validation_or_tests: Included in the aggregate test runner at `tests/run-all-tests.sh:47`. The test itself is validation evidence for the helper’s command parsing and filesystem iteration behavior.
- skip_candidate: `no`

### ASK_CODEX_SKILL-HZ-092 `file` `prompt-template/block/git-not-clean-humanize-local.md`
- cursor: `[_]`
- core_role: User-facing block-note template appended when the stop hook detects untracked `.humanize*` directories during the git-clean exit gate.
- algorithmic_behavior: Provides a special-case explanation that `.humanize/` is local loop state and should not be committed, then prescribes adding `.humanize*` to `.gitignore` and staging only `.gitignore` (`prompt-template/block/git-not-clean-humanize-local.md:2-8`).
- inputs_outputs_state: Input is template loading by the stop hook; there are no variables in this template. Output is markdown text included in the larger git-not-clean block reason. No state changes occur from the template itself.
- gates_or_invariants: Reinforces the invariant that `.humanize/` is generated local RLCR state, not a commit surface. The prescribed remediation avoids staging `.humanize` and stages `.gitignore` only.
- dependencies_and_callers: Loaded by `hooks/loop-codex-stop-hook.sh:552-559` when cached git status contains untracked paths matching `.humanize`; then inserted into the `SPECIAL_NOTES` field rendered into the main git-not-clean block at `hooks/loop-codex-stop-hook.sh:572-589`.
- edge_cases_or_failure_modes: If the template is missing or empty, the stop hook falls back to “Note: .humanize* directories are intentionally untracked.” (`hooks/loop-codex-stop-hook.sh:554-557`). The template intentionally targets `.humanize*`, covering legacy/local variants beyond `.humanize/`.
- validation_or_tests: Indirectly covered by template reference/comprehensive tests and stop-hook git cleanliness tests; production call site is explicit at `hooks/loop-codex-stop-hook.sh:554`.
- skip_candidate: `no`

### ASK_CODEX_SKILL-HZ-122 `file` `prompt-template/claude/finalize-phase-prompt.md`
- cursor: `[_]`
- core_role: Transition prompt for the RLCR Finalize Phase after Codex review passes. It defines the post-review cleanup/refactor contract before final completion.
- algorithmic_behavior: Announces successful review and switches the agent into Finalize Phase (`prompt-template/claude/finalize-phase-prompt.md:1-5`). It requires invoking `code-simplifier:code-simplifier` through Task (`prompt-template/claude/finalize-phase-prompt.md:7-14`), constrains changes to functionality-equivalent simplification (`prompt-template/claude/finalize-phase-prompt.md:16-24`), and directs focus to recent branch changes (`prompt-template/claude/finalize-phase-prompt.md:25-34`).
- inputs_outputs_state: Inputs are template variables `{{BASE_BRANCH}}`, `{{START_BRANCH}}`, `{{PLAN_FILE}}`, `{{GOAL_TRACKER_FILE}}`, and `{{FINALIZE_SUMMARY_FILE}}` (`prompt-template/claude/finalize-phase-prompt.md:29`, `38-45`). Output is a rendered prompt returned by the stop hook as a block decision, causing Claude to continue in finalize mode.
- gates_or_invariants: Must not change behavior, fail existing tests, or introduce bugs; only cleanup/refactoring is allowed (`prompt-template/claude/finalize-phase-prompt.md:18-24`). Before exiting, all tasks must be completed, changes committed, and finalize summary written (`prompt-template/claude/finalize-phase-prompt.md:41-51`).
- dependencies_and_callers: Rendered by `hooks/loop-codex-stop-hook.sh:1112-1137` through `load_and_render_safe` after non-skipped review success; fallback prompt is embedded at `hooks/loop-codex-stop-hook.sh:1112-1130`. Rendering uses `hooks/lib/template-loader.sh:170-203`.
- edge_cases_or_failure_modes: If template load/render fails, stop hook uses its fallback. The prompt asks for commits and tests, so stale git state or missing summary can trigger later stop-hook gates. Variable placeholders remain if caller fails to pass values, because template rendering preserves missing placeholders by design (`hooks/lib/template-loader.sh:12-13`, `116-122`).
- validation_or_tests: `tests/test-finalize-phase.sh` covers finalize-state/read behavior and finalize phase flow; template existence/reference behavior is covered by template tests. Production transition point is `hooks/loop-codex-stop-hook.sh:1132-1145`.
- skip_candidate: `no`

### ASK_CODEX_SKILL-HZ-152 `file` `tests/robustness/test-path-validation-robustness.sh`
- cursor: `[_]`
- core_role: Robustness executable specification for `scripts/setup-rlcr-loop.sh` plan-file path and content validation, including injection resistance and symlink traversal defenses.
- algorithmic_behavior: Creates isolated temp git repo (`tests/robustness/test-path-validation-robustness.sh:16-47`), installs a mock `codex` executable to avoid real Codex calls (`tests/robustness/test-path-validation-robustness.sh:18-35`), creates valid plan fixtures (`tests/robustness/test-path-validation-robustness.sh:49-65`), and runs production setup with `CLAUDE_PROJECT_DIR="$TEST_DIR"` (`tests/robustness/test-path-validation-robustness.sh:76-113`).
- inputs_outputs_state: Inputs are candidate plan paths and fixture files/directories. The helper interprets production stderr patterns for path/content validation failures (`tests/robustness/test-path-validation-robustness.sh:91-105`). Output is PASS/FAIL via `tests/test-helpers.sh` and final exit from `print_test_summary` (`tests/robustness/test-path-validation-robustness.sh:482-487`).
- gates_or_invariants: Valid relative paths, simple filenames, dash/underscore, nested dirs, dotted filenames, long filenames, and deep nesting should pass (`tests/robustness/test-path-validation-robustness.sh:122-169`, `387-412`). Absolute paths, spaces, shell metacharacters, symlink files, parent symlinks, symlink chains, empty/short/comment-only/nonexistent/directory inputs should reject (`tests/robustness/test-path-validation-robustness.sh:179-377`, `425-480`).
- dependencies_and_callers: Tests production validation in `scripts/setup-rlcr-loop.sh:300-585`: single plan source merge, git repo checks, relative-only path gate, no spaces/metacharacters, file and parent symlink rejection, existence/readability, project-bound real path check, submodule check, tracking policy, minimum line count, meaningful content count, and Codex availability. Included in aggregate runner at `tests/run-all-tests.sh:66`.
- edge_cases_or_failure_modes: The test treats “requires codex” and “must be gitignored” as evidence that path validation passed (`tests/robustness/test-path-validation-robustness.sh:97-105`). Unicode/CJK/emoji path characters are explicitly allowed by test comment (`tests/robustness/test-path-validation-robustness.sh:414-416`). Production content logic counts markdown headings beginning with `#` as comments (`scripts/setup-rlcr-loop.sh:529-561`), which is a deliberate but surprising validation rule.
- validation_or_tests: This file is itself a validator test and complements broader `tests/test-plan-file-validation.sh` and `tests/robustness/test-plan-file-robustness.sh` coverage. It directly exercises setup behavior rather than duplicating only helper functions.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `ASK_CODEX_SKILL-HZ-002`, `ASK_CODEX_SKILL-HZ-032`, `ASK_CODEX_SKILL-HZ-062`, `ASK_CODEX_SKILL-HZ-092`, `ASK_CODEX_SKILL-HZ-122`, `ASK_CODEX_SKILL-HZ-152`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`