# agent_26 make-working-folder-to-humanize-only 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 2
- source_commit: `823cb32d01ae021ec8a0eb3dc1f18af901d2ba65`

## Item Evidence

### MAKE_WORKING_FOLDER_TO_HUMANIZE_ONLY-HZ-026 `file` `tests/test-plan-file-hooks.sh`
- cursor: `[_]`
- core_role:
  - This is an executable specification for RLCR plan-file immutability and hook boundary behavior. It verifies that an active loop treats the original plan and loop-local `plan.md` backup as protected inputs, and that hook validators enforce schema, branch, git-tracking, directory, and shell-bypass constraints.
  - The test targets the hook suite listed in its header: `loop-plan-file-validator.sh`, `loop-write-validator.sh`, `loop-edit-validator.sh`, and `loop-bash-validator.sh` at `tests/test-plan-file-hooks.sh:5`-`9`. Later sections also exercise `loop-codex-stop-hook.sh` for stop-time plan integrity at `tests/test-plan-file-hooks.sh:388`-`428` and `tests/test-plan-file-hooks.sh:469`-`730`.

- algorithmic_behavior:
  - Test setup constructs a temporary git repository, captures the default branch, creates `.humanize/rlcr/2024-01-01_12-00-00`, creates a gitignored source plan at `plans/test-plan.md`, copies it to the loop backup `plan.md`, and writes frontmatter state with `current_round`, `max_iterations`, `plan_file`, `plan_tracked`, and `start_branch` at `tests/test-plan-file-hooks.sh:37`-`85`.
  - The UserPromptSubmit tests assert the pre-prompt validator allows a valid state with no output, parses YAML-quoted `plan_file`, blocks old-schema states missing `plan_tracked`, blocks states missing `start_branch`, and blocks when the current branch differs from `start_branch` at `tests/test-plan-file-hooks.sh:91`-`185`.
  - The Write/Edit tests assert direct tool writes or edits to the loop-local `plan.md` backup are rejected with exit code `2` and a plan-related message at `tests/test-plan-file-hooks.sh:194`-`222`.
  - The Bash tests assert shell-level mutation attempts against `.humanize/rlcr/.../plan.md` are rejected, including `echo >`, `rm`, direct `.humanize/rlcr/plan.md`, command substitution, glob expansion, brace expansion, piped `tee`, and backtick substitution at `tests/test-plan-file-hooks.sh:228`-`335`.
  - YAML quote-parsing tests assert `start_branch: "$DEFAULT_BRANCH"` is accepted, quoted branch mismatch is blocked, the stop hook parses quoted `plan_file` and `start_branch` without YAML/schema parse failures, and hyphenated plan paths such as `my-plans/test-plan.md` are accepted at `tests/test-plan-file-hooks.sh:341`-`459`.
  - Stop-hook integrity tests assert exit attempts are blocked if the project plan differs from backup, if the project plan is deleted, if the loop backup is missing, if a tracked plan has uncommitted edits, if state schema is outdated, or if a tracked plan was modified and committed so `git status` is clean but content differs from backup at `tests/test-plan-file-hooks.sh:469`-`730`.
  - Legacy negative tests assert old `.humanize-loop.local` paths are no longer protected by these validators: Bash, Write, and Edit access to that legacy path must exit `0` at `tests/test-plan-file-hooks.sh:733`-`775`.

- inputs_outputs_state:
  - Inputs:
    - Hook stdin JSON, usually `{}` for prompt/stop hooks or Claude-style PreToolUse JSON with `tool_name` and `tool_input.file_path` / `tool_input.command` for Write/Edit/Bash validators at `tests/test-plan-file-hooks.sh:97`, `tests/test-plan-file-hooks.sh:196`, `tests/test-plan-file-hooks.sh:213`, and `tests/test-plan-file-hooks.sh:230`.
    - Environment variable `CLAUDE_PROJECT_DIR`, set to the temporary repo or nested tracked-test repo so hooks resolve the project root deterministically at `tests/test-plan-file-hooks.sh:93`, `tests/test-plan-file-hooks.sh:619`, and `tests/test-plan-file-hooks.sh:720`.
    - RLCR state frontmatter under `.humanize/rlcr/<timestamp>/state.md`, especially `plan_file`, `plan_tracked`, and `start_branch` at `tests/test-plan-file-hooks.sh:77`-`84`.
    - The source plan and loop backup pair: `plans/test-plan.md` and `.humanize/rlcr/<timestamp>/plan.md` at `tests/test-plan-file-hooks.sh:59`-`73`.
  - Outputs:
    - Test result counters and colored `PASS`/`FAIL`/`SKIP` lines via helper functions at `tests/test-plan-file-hooks.sh:17`-`28`.
    - Process exit status equals `TESTS_FAILED`, so any failed assertion produces a nonzero test-file exit at `tests/test-plan-file-hooks.sh:777`-`786`.
    - Expected hook outputs differ by hook type: allow cases return exit `0` with no output for pre-prompt validation; block cases may return exit `0` with JSON `"decision": "block"` for prompt/stop hooks or exit `2` with stderr for PreToolUse Write/Edit/Bash validators.
  - State transitions:
    - `setup_test_loop` initializes git only once per temp repo, then may be called repeatedly to recreate the loop directory, source plan, backup, and state at `tests/test-plan-file-hooks.sh:37`-`85`.
    - Branch state changes to `feature-branch` and back to the captured default branch to test branch invariants at `tests/test-plan-file-hooks.sh:164`-`185`.
    - Plan state is mutated by append, delete, backup delete, uncommitted tracked edit, and committed tracked edit to verify independent stop-hook detection paths at `tests/test-plan-file-hooks.sh:472`-`473`, `tests/test-plan-file-hooks.sh:511`-`513`, `tests/test-plan-file-hooks.sh:543`-`547`, `tests/test-plan-file-hooks.sh:617`-`628`, and `tests/test-plan-file-hooks.sh:711`-`730`.

- gates_or_invariants:
  - Active RLCR state must use the v1.1.2+ schema with `plan_tracked` and `start_branch`; missing fields are considered block-worthy outdated schema conditions at `tests/test-plan-file-hooks.sh:121`-`159` and `tests/test-plan-file-hooks.sh:631`-`653`.
  - `start_branch` is immutable for the duration of a loop; a current branch mismatch must block at `tests/test-plan-file-hooks.sh:164`-`185`.
  - The source plan’s tracking mode is part of loop state: gitignored plans must remain untracked, and tracked plans must remain tracked and clean. The test covers tracked uncommitted and committed-content changes at `tests/test-plan-file-hooks.sh:562`-`730`.
  - The loop-local `plan.md` backup is read-only to Write, Edit, and Bash mutation channels at `tests/test-plan-file-hooks.sh:194`-`266`.
  - Shell bypass attempts are treated as equivalent to direct file mutation, including dynamic path constructs that could expand to a protected plan backup at `tests/test-plan-file-hooks.sh:272`-`335`.
  - `.humanize/rlcr` is the active protected loop path. Legacy `.humanize-loop.local` must not be treated as the active loop directory at `tests/test-plan-file-hooks.sh:733`-`775`.
  - Stop-time completion is gated on source-plan and backup integrity before review proceeds: modified source plan, deleted source plan, or missing backup all block at `tests/test-plan-file-hooks.sh:469`-`560`.

- dependencies_and_callers:
  - Direct dependencies are shell, `mktemp`, `git`, `jq` through the hooks, and the hook scripts under `hooks/`.
  - `loop-plan-file-validator.sh` implements the prompt-time schema, branch, and plan tracking checks. It parses frontmatter, strips legacy YAML quotes from `plan_file` and `start_branch`, checks required fields, compares `git rev-parse --abbrev-ref HEAD` with `start_branch`, and validates tracking/dirty state at `hooks/loop-plan-file-validator.sh:36`-`138`.
  - `loop-write-validator.sh` and `loop-edit-validator.sh` implement direct tool protection. They parse PreToolUse JSON via `jq`, resolve the active loop, block `state.md`, protect `plan.md`, gate `goal-tracker.md` after round 0, and for summary files validate round and directory correctness at `hooks/loop-write-validator.sh:23`-`182` and `hooks/loop-edit-validator.sh:22`-`133`.
  - `loop-bash-validator.sh` implements shell mutation protection. It blocks `git push` unless configured, blocks state and plan backup modification, blocks goal-tracker mutation, and rejects shell writes to prompt, summary, and todos files at `hooks/loop-bash-validator.sh:22`-`137`.
  - Shared behavior is in `hooks/lib/loop-common.sh`: `find_active_loop`, `get_current_round`, `is_round_file_type`, `extract_round_number`, path classifiers, and `command_modifies_file` patterns at `hooks/lib/loop-common.sh:23`-`183`.
  - `loop-codex-stop-hook.sh` supplies stop-time plan integrity logic. It parses state, enforces schema and branch consistency, requires the backup plan, requires the original plan to exist, checks tracked-plan dirty status, and always diffs source plan vs backup at `hooks/loop-codex-stop-hook.sh:69`-`216`.

- edge_cases_or_failure_modes:
  - YAML quote compatibility is explicitly tested because older or hand-written state may quote `plan_file` and `start_branch`; failures here would falsely report missing files or branch mismatch at `tests/test-plan-file-hooks.sh:106`-`119` and `tests/test-plan-file-hooks.sh:341`-`386`.
  - Hyphenated plan paths are tested to avoid over-restrictive parsing of valid relative paths at `tests/test-plan-file-hooks.sh:431`-`459`.
  - Bash command detection is regex-based through `command_modifies_file`; tests cover several bypass forms, but behavior depends on recognizing the command text before shell expansion at `tests/test-plan-file-hooks.sh:272`-`335` and `hooks/lib/loop-common.sh:155`-`183`.
  - Committed changes to a tracked plan are a critical race/integrity case: `git status` is clean, so the stop hook must still compare content against the loop backup. This is tested at `tests/test-plan-file-hooks.sh:655`-`730` and implemented by the unconditional `diff -q` at `hooks/loop-codex-stop-hook.sh:196`-`216`.
  - The file starts with `set -uo pipefail`, not `set -e`, but individual tests toggle `set +e` / `set -e` around hook invocations. After the first guarded invocation, `set -e` remains active for setup and fixture operations, causing unexpected setup failures to abort instead of being counted as assertion failures.
  - The temp cleanup trap removes the whole temporary repository on exit at `tests/test-plan-file-hooks.sh:30`-`32`; this keeps test state isolated but means post-failure inspection needs rerunning with trap changes.
  - The branch name is captured dynamically because `git init` may default to `main` or `master` depending on local git configuration at `tests/test-plan-file-hooks.sh:48`-`53`.

- validation_or_tests:
  - This assigned file is itself the validation asset. It performs 17 numbered tests plus subtests `1.5` and `8.1`-`8.9`, then exits with the number of failed assertions at `tests/test-plan-file-hooks.sh:777`-`786`.
  - It validates both positive allow cases and negative block cases:
    - Allow: valid state, YAML-quoted fields, hyphenated plan path, and legacy `.humanize-loop.local`.
    - Block: missing schema fields, branch mismatch, plan backup writes/edits/shell mutations, bash bypass attempts, modified/deleted plan, missing backup, tracked dirty plan, outdated schema, and committed tracked plan changes.
  - I did not run the full test file because the workspace is read-only and the test creates temporary git repositories and writes under `/tmp`; a `git status --short` probe also failed due sandbox restrictions around cache/temp creation and because this branch export does not expose a normal `.git` directory.

- skip_candidate: `no`

### MAKE_WORKING_FOLDER_TO_HUMANIZE_ONLY-HZ-056 `file` `prompt-template/block/wrong-round-number.md`
- cursor: `[_]`
- core_role:
  - This is a block-message template used by RLCR hooks when an agent tries to write or edit a round-scoped file with a filename round number that does not match the loop’s current round.
  - It is algorithmic because it defines the user-facing correction contract for a hook gate: identify the attempted wrong artifact, state the authoritative current round, give the correct path, and forbid manual round increments.

- algorithmic_behavior:
  - The template renders a Markdown block headed `Wrong Round Number` at `prompt-template/block/wrong-round-number.md:1`.
  - It interpolates five variables:
    - `{{ACTION}}`: the attempted operation, such as `write to` or `edit`.
    - `{{CLAUDE_ROUND}}`: the round number parsed from the requested filename.
    - `{{FILE_TYPE}}`: the artifact type, currently used for `summary`.
    - `{{CURRENT_ROUND}}`: the authoritative round from active loop state.
    - `{{CORRECT_PATH}}`: the canonical path in the active loop directory.
  - Its core transition message is: attempted path `round-{{CLAUDE_ROUND}}-{{FILE_TYPE}}.md` is invalid because the current round is `{{CURRENT_ROUND}}`; use `{{CORRECT_PATH}}` instead at `prompt-template/block/wrong-round-number.md:3`-`5`.
  - The final instruction, `Do NOT increment the round number yourself`, at `prompt-template/block/wrong-round-number.md:7`, prevents the agent from treating the next round as self-service state.

- inputs_outputs_state:
  - Inputs are template variables supplied by callers through `load_and_render_safe`.
  - Write validator caller:
    - Extracts the requested round with `extract_round_number`, compares it to `CURRENT_ROUND`, sets `CORRECT_PATH="$ACTIVE_LOOP_DIR/round-${CURRENT_ROUND}-summary.md"`, and renders this template with `ACTION=write to` and `FILE_TYPE=summary` at `hooks/loop-write-validator.sh:145`-`160`.
  - Edit validator caller:
    - Performs the same comparison for edits and renders this template with `ACTION=edit` at `hooks/loop-edit-validator.sh:105`-`128`.
  - Outputs are Markdown text emitted to stderr by the PreToolUse validators before exiting `2`, causing the tool use to be blocked. The template itself does not mutate state.
  - The authoritative state input is `current_round` parsed from `.humanize/rlcr/<active>/state.md` by `get_current_round` in `hooks/lib/loop-common.sh:46`-`58`.

- gates_or_invariants:
  - Round-number invariant: generated round files are tied to `current_round`; agents may not create or modify `round-N-summary.md` for any `N` other than the active round.
  - Path invariant: even when the filename pattern is otherwise valid, the correct file must be inside the newest active `.humanize/rlcr/<timestamp>` loop directory, which is resolved by `find_active_loop` at `hooks/lib/loop-common.sh:23`-`44`.
  - State-authority invariant: the agent is instructed not to increment round numbers manually; round advancement belongs to loop state/hook machinery, not to Write/Edit behavior.
  - The template is only used after a caller has already determined that a summary filename contains a parseable round number and that it differs from `CURRENT_ROUND`.

- dependencies_and_callers:
  - Direct callers found in this branch:
    - `hooks/loop-write-validator.sh:155` renders `block/wrong-round-number.md` for wrong-round summary writes.
    - `hooks/loop-edit-validator.sh:122` renders it for wrong-round summary edits.
  - Shared parsing dependency:
    - `extract_round_number` parses `round-<digits>-(summary|prompt|todos).md` at `hooks/lib/loop-common.sh:74`-`84`.
    - `is_round_file_type` recognizes file type suffixes at `hooks/lib/loop-common.sh:65`-`72`.
  - Template rendering is validated in:
    - `tests/test-template-loader.sh:151`-`164`, which renders the real template and checks replacement of wrong round `3`, current round `5`, and the output phrase.
    - `tests/test-templates-comprehensive.sh:498`-`510`, which checks all variables render including `/tmp/round-5-summary.md`.
  - The broader reference search shows only this template path under `prompt-template/block/wrong-round-number.md`, plus the two hook callers and template tests, so the template’s active behavioral surface is limited and specific.

- edge_cases_or_failure_modes:
  - Missing or malformed variables would produce unresolved `{{...}}` placeholders because the template is simple substitution; correctness depends on callers supplying all five variables.
  - The template does not itself validate whether `CORRECT_PATH` is safe or inside the active loop directory. That invariant is caller-owned through `ACTIVE_LOOP_DIR`.
  - It currently names the attempted file as `round-{{CLAUDE_ROUND}}-{{FILE_TYPE}}.md`, not the full attempted path. This is enough for round mismatch remediation but not for diagnosing directory mismatch; `loop-write-validator.sh` separately uses `block/wrong-directory-path.md` for that case at `hooks/loop-write-validator.sh:169`-`180`.
  - Bash writes to summary files do not use this wrong-round template. Bash summary modification is blocked categorically and points to `summary-bash-write.md` via `summary_bash_blocked_message` at `hooks/loop-bash-validator.sh:122`-`125` and `hooks/lib/loop-common.sh:115`-`124`.
  - The assigned test file `tests/test-plan-file-hooks.sh` does not directly test wrong-round summary filename behavior; coverage for this template is in template-loader tests, not the plan-file hook test.

- validation_or_tests:
  - `tests/test-template-loader.sh` integration-renders the template with `ACTION=edit`, `CLAUDE_ROUND=3`, `FILE_TYPE=summary`, `CURRENT_ROUND=5`, and `CORRECT_PATH=/tmp/round-5-summary.md`, then checks for the heading, attempted filename, and current-round text at `tests/test-template-loader.sh:151`-`164`.
  - `tests/test-templates-comprehensive.sh` repeats the real-template rendering and additionally checks the correct path appears at `tests/test-templates-comprehensive.sh:498`-`510`.
  - Runtime validation is provided by Write/Edit hook branches that compare `CLAUDE_ROUND` to `CURRENT_ROUND` before rendering this template and exiting `2` at `hooks/loop-write-validator.sh:145`-`162` and `hooks/loop-edit-validator.sh:105`-`129`.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen:
  - `MAKE_WORKING_FOLDER_TO_HUMANIZE_ONLY-HZ-026`: appears exactly once as an Item Evidence heading.
  - `MAKE_WORKING_FOLDER_TO_HUMANIZE_ONLY-HZ-056`: appears exactly once as an Item Evidence heading.
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`