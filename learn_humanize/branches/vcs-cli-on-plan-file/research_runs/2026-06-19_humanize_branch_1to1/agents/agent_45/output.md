# agent_45 vcs-cli-on-plan-file 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `4dd1ca2fece39d3c6d7f84965cd71bda02489397`

## Item Evidence

### VCS_CLI_ON_PLAN_FILE-HZ-045 `file` `prompt-template/block/plan-file-committed.md`
- cursor: `[_]`
- core_role:
  - This file is a prompt/block template for the RLCR plan-file protection gate. It is rendered when a plan file has been committed even though the loop was started without `--commit-plan-file`.
  - It is not executable by itself, but it is part of the core transition contract for the stop-hook validation path: when the invariant is violated, the hook blocks completion and gives deterministic recovery instructions.
  - The template headline and first sentence define the failure class at [prompt-template/block/plan-file-committed.md](/Users/wangweiyang/GitHub/humanize_branch_worktrees/vcs-cli-on-plan-file/prompt-template/block/plan-file-committed.md:1) and [prompt-template/block/plan-file-committed.md](/Users/wangweiyang/GitHub/humanize_branch_worktrees/vcs-cli-on-plan-file/prompt-template/block/plan-file-committed.md:3).

- algorithmic_behavior:
  - The runtime caller is the Codex stop hook. It reads `commit_plan_file`, `plan_file`, and `start_commit` from `.humanize-loop.local/<timestamp>/state.md` at [hooks/loop-codex-stop-hook.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/vcs-cli-on-plan-file/hooks/loop-codex-stop-hook.sh:185).
  - If `commit_plan_file` is not `true` and a plan file exists in state, the hook computes the git-root-relative plan path, then runs `git log --oneline --follow "${START_COMMIT}..HEAD" -- "$PLAN_FILE_REL_POST"` to detect commits containing the plan file at [hooks/loop-codex-stop-hook.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/vcs-cli-on-plan-file/hooks/loop-codex-stop-hook.sh:301).
  - If that git-log result is non-empty, the hook renders this template via `load_and_render_safe "$TEMPLATE_DIR" "block/plan-file-committed.md"` with `PLAN_FILE` and `PLAN_FILE_COMMITS` variables at [hooks/loop-codex-stop-hook.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/vcs-cli-on-plan-file/hooks/loop-codex-stop-hook.sh:328).
  - The rendered template is returned inside a JSON stop-hook response with `"decision": "block"` and system message `Loop: Blocked - plan file was accidentally committed` at [hooks/loop-codex-stop-hook.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/vcs-cli-on-plan-file/hooks/loop-codex-stop-hook.sh:332).
  - The template’s own behavior is a two-option remediation protocol:
    - Option 1 removes the plan file from the offending commits by soft-resetting `HEAD~N`, unstaging the plan file, and recommitting without it at [prompt-template/block/plan-file-committed.md](/Users/wangweiyang/GitHub/humanize_branch_worktrees/vcs-cli-on-plan-file/prompt-template/block/plan-file-committed.md:18).
    - Option 2 changes the policy by cancelling the loop and restarting with `--commit-plan-file` at [prompt-template/block/plan-file-committed.md](/Users/wangweiyang/GitHub/humanize_branch_worktrees/vcs-cli-on-plan-file/prompt-template/block/plan-file-committed.md:25).

- inputs_outputs_state:
  - Inputs:
    - `{{PLAN_FILE}}`: rendered as the repository-relative plan-file path at [prompt-template/block/plan-file-committed.md](/Users/wangweiyang/GitHub/humanize_branch_worktrees/vcs-cli-on-plan-file/prompt-template/block/plan-file-committed.md:5). The caller supplies `PLAN_FILE=$PLAN_FILE_REL_POST` at [hooks/loop-codex-stop-hook.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/vcs-cli-on-plan-file/hooks/loop-codex-stop-hook.sh:329).
    - `{{PLAN_FILE_COMMITS}}`: rendered as the newline-preserving `git log --oneline --follow` output for the plan file at [prompt-template/block/plan-file-committed.md](/Users/wangweiyang/GitHub/humanize_branch_worktrees/vcs-cli-on-plan-file/prompt-template/block/plan-file-committed.md:7). The caller supplies `PLAN_FILE_COMMITS=$PLAN_FILE_COMMITS` at [hooks/loop-codex-stop-hook.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/vcs-cli-on-plan-file/hooks/loop-codex-stop-hook.sh:330).
  - Upstream state:
    - `scripts/setup-rlcr-loop.sh` creates the loop state file with `commit_plan_file`, `plan_file`, `plan_file_tracked`, and `start_commit` fields at [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/vcs-cli-on-plan-file/scripts/setup-rlcr-loop.sh:326).
    - The plan backup is always written before state creation, and `START_COMMIT` is captured from `git rev-parse HEAD` at [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/vcs-cli-on-plan-file/scripts/setup-rlcr-loop.sh:317).
  - Outputs:
    - The template renders markdown guidance that becomes the stop-hook `reason`.
    - The hook emits a JSON block response and exits successfully from the hook process, leaving the RLCR loop blocked for the user/agent to repair rather than silently accepting the invalid commit history.
  - State transition:
    - Normal state: `commit_plan_file != true`, plan file may be dirty/untracked, and git history since `START_COMMIT` must not include the plan file.
    - Violation state: `PLAN_FILE_COMMITS` non-empty.
    - Transition output: hook decision becomes `block`; no files are modified by the template or hook path.
    - Recovery transition A: rewrite local commits so the plan file is no longer in `${START_COMMIT}..HEAD`.
    - Recovery transition B: cancel current loop and start a new loop with `--commit-plan-file`.

- gates_or_invariants:
  - Primary invariant: when `--commit-plan-file` is absent, the plan file is a working document and should not be tracked in loop-generated commits. The template states this rationale at [prompt-template/block/plan-file-committed.md](/Users/wangweiyang/GitHub/humanize_branch_worktrees/vcs-cli-on-plan-file/prompt-template/block/plan-file-committed.md:10).
  - The stop hook only evaluates this post-commit gate when `COMMIT_PLAN_FILE != true` and `PLAN_FILE_FROM_STATE` is non-empty at [hooks/loop-codex-stop-hook.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/vcs-cli-on-plan-file/hooks/loop-codex-stop-hook.sh:301).
  - The hook first handles legacy pre-1.1.2 state files that lack `start_commit`, terminating with an upgrade message before this gate can run with an invalid range at [hooks/loop-codex-stop-hook.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/vcs-cli-on-plan-file/hooks/loop-codex-stop-hook.sh:196).
  - There is a complementary pre-commit gate in `hooks/loop-bash-validator.sh`: when `commit_plan_file` is false and the command is `git commit`, it checks `git diff --cached --name-only` and blocks if the exact plan path is staged at [hooks/loop-bash-validator.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/vcs-cli-on-plan-file/hooks/loop-bash-validator.sh:99). This template covers the post-commit escape path if that earlier gate was bypassed.
  - The README documents the same user-facing contract: inside-repo plan files without `--commit-plan-file` may be tracked/untracked or dirty/clean, but accidental commits are blocked and a backup is saved at [README.md](/Users/wangweiyang/GitHub/humanize_branch_worktrees/vcs-cli-on-plan-file/README.md:225).

- dependencies_and_callers:
  - Direct caller:
    - `hooks/loop-codex-stop-hook.sh`, post-commit section `Plan File Accidentally Committed?`, renders this template at [hooks/loop-codex-stop-hook.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/vcs-cli-on-plan-file/hooks/loop-codex-stop-hook.sh:296).
  - Template rendering dependency:
    - `hooks/lib/template-loader.sh` defines `{{VARIABLE_NAME}}` syntax at [hooks/lib/template-loader.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/vcs-cli-on-plan-file/hooks/lib/template-loader.sh:5).
    - `render_template` performs single-pass awk substitution and intentionally does not rescan variable values for nested placeholders, limiting placeholder injection risk at [hooks/lib/template-loader.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/vcs-cli-on-plan-file/hooks/lib/template-loader.sh:35).
    - `load_and_render_safe` falls back to an inline fallback message if the template is missing or renders empty at [hooks/lib/template-loader.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/vcs-cli-on-plan-file/hooks/lib/template-loader.sh:152).
  - Upstream producer:
    - `scripts/setup-rlcr-loop.sh` records `commit_plan_file`, `plan_file`, and `start_commit` in state at [scripts/setup-rlcr-loop.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/vcs-cli-on-plan-file/scripts/setup-rlcr-loop.sh:326).
  - Sibling guard/template:
    - `prompt-template/block/plan-file-staged.md` is the pre-commit version used by `hooks/loop-bash-validator.sh` when the plan file is staged before commit.
  - Tests:
    - `tests/test-plan-file-handling.sh` asserts that the stop hook has this post-commit check and uses `git log` over `START_COMMIT..HEAD` at [tests/test-plan-file-handling.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/vcs-cli-on-plan-file/tests/test-plan-file-handling.sh:246).
    - The same test asserts this template exists and contains both required placeholders at [tests/test-plan-file-handling.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/vcs-cli-on-plan-file/tests/test-plan-file-handling.sh:336).

- edge_cases_or_failure_modes:
  - Empty or missing `start_commit`: pre-1.1.2 state files are terminated before this gate runs, because the git range would not safely identify loop-era plan-file commits.
  - Missing template file: `load_and_render_safe` uses an embedded fallback, so the stop-hook block still works even if `prompt-template/block/plan-file-committed.md` is absent.
  - Multiline commit list: `PLAN_FILE_COMMITS` can contain multiple `git log --oneline` rows; the template places the placeholder on its own line to preserve readability at [prompt-template/block/plan-file-committed.md](/Users/wangweiyang/GitHub/humanize_branch_worktrees/vcs-cli-on-plan-file/prompt-template/block/plan-file-committed.md:7).
  - Path matching: the stop hook converts the plan file to a git-root-relative path before `git log`; the pre-stop dirty status filtering also escapes regex-sensitive characters and anchors the path to end-of-line at [hooks/loop-codex-stop-hook.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/vcs-cli-on-plan-file/hooks/loop-codex-stop-hook.sh:240). This avoids treating similarly named files as the plan file.
  - Fresh repo behavior: if the loop starts before a usable `HEAD`, `START_COMMIT` may be empty. The test suite separately covers fresh repo detection and git-log behavior after the first commit at [tests/test-plan-file-handling.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/vcs-cli-on-plan-file/tests/test-plan-file-handling.sh:525).
  - History rewrite risk: the recommended recovery uses `git reset --soft HEAD~N`; the template assumes the offending commits are local/rewriteable and requires the user to choose `N` based on the displayed commit list. It does not itself calculate `N`, perform the reset, or check whether commits were pushed.
  - Mode mismatch: if the user intended the plan to be versioned, the only supported recovery is cancelling and restarting with `--commit-plan-file`; the current loop cannot be converted in place by this template.

- validation_or_tests:
  - Static template contract tests:
    - Existence check for `prompt-template/block/plan-file-committed.md` at [tests/test-plan-file-handling.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/vcs-cli-on-plan-file/tests/test-plan-file-handling.sh:338).
    - Placeholder checks for `{{PLAN_FILE}}` and `{{PLAN_FILE_COMMITS}}` at [tests/test-plan-file-handling.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/vcs-cli-on-plan-file/tests/test-plan-file-handling.sh:402).
  - Stop-hook behavior tests:
    - Checks that the stop hook reads `commit_plan_file` and `start_commit`, filters plan-file status, contains the post-commit check, and uses `git log` over the loop range at [tests/test-plan-file-handling.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/vcs-cli-on-plan-file/tests/test-plan-file-handling.sh:223).
  - Git detection unit scenario:
    - The test creates an initial commit, records `START_COMMIT`, commits `docs/plan.md`, then verifies `git log --oneline --follow "${START_COMMIT}..HEAD" -- "docs/plan.md"` returns data and a nonexistent path returns empty at [tests/test-plan-file-handling.sh](/Users/wangweiyang/GitHub/humanize_branch_worktrees/vcs-cli-on-plan-file/tests/test-plan-file-handling.sh:482).
  - Template loader tests elsewhere cover safe rendering, fallbacks, special characters, and multiline values through `render_template` / `load_and_render_safe`; this matters because `PLAN_FILE_COMMITS` is multiline and may contain shell-sensitive characters.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 1
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`