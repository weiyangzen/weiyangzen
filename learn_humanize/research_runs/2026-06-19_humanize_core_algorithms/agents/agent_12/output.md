**主题与结论**

Topic: Plan-file validator and plan integrity hooks, pinned commit `0ec921a36b4365df503511c5567bbd3e02db0df5`.

结论：核心机制是一个有序的 fail-closed 门禁链，而不是评分系统。启动阶段把计划文件路径、跟踪模式和初始内容固化为 loop state 与 `.humanize/rlcr/<loop>/plan.md` 备份；会话中 `UserPromptSubmit` 钩子持续校验 state schema、Git 分支和计划文件的 Git 跟踪状态；停止阶段在进入 review phase 之前用备份做内容一致性校验；Write/Edit/Bash 类钩子按测试契约阻止改写 loop 目录中的 `plan.md` 备份。路由结果只有允许、JSON block、非零硬阻断、以及 pre-tool validator 的 exit 2 阻断。

**Algorithm Subset Covered**

覆盖的算法子集：

- `hooks/loop-plan-file-validator.sh`: 会话中计划文件状态门禁，包含 active loop 发现、state schema、branch consistency、`plan_tracked` 分流。
- `prompt-template/block/plan-file-modified.md`: 计划文件被修改时的阻断提示模板。
- `tests/test-plan-file-hooks.sh`: 行为合同，包括 quoted YAML 字段、branch 切换、backup 写入阻断、Bash 绕过阻断、stop hook 的 modified/deleted/backup-missing/tracked-change 场景。
- `tests/test-plan-file-validation.sh`: 启动期输入验证合同，包括路径、Git repo、tracking mode、内容有效性和 CLI 互斥规则。
- 最小补充实现证据：`scripts/setup-rlcr-loop.sh` 的启动期计划文件校验与备份创建，以及 `hooks/loop-codex-stop-hook.sh` 的停止期 plan integrity diff；这些只用于解释 focus 测试所断言的行为。

**Pseudocode**

```text
on UserPromptSubmit(input):
  PROJECT_ROOT = resolve_project_root()
  if PROJECT_ROOT missing:
    ALLOW

  HOOK_SESSION_ID = extract_session_id(input)
  LOOP_DIR = find_active_loop(PROJECT_ROOT/.humanize/rlcr, HOOK_SESSION_ID)
  if LOOP_DIR missing:
    ALLOW

  STATE_FILE = resolve_active_state_file(LOOP_DIR)
  if parse_state_file_strict(STATE_FILE) fails:
    HARD_BLOCK(stderr, exit=1)

  PLAN_TRACKED = STATE_PLAN_TRACKED
  PLAN_FILE = STATE_PLAN_FILE
  START_BRANCH = STATE_START_BRANCH

  if PLAN_TRACKED or START_BRANCH is empty:
    JSON_BLOCK(schema-outdated)

  CURRENT_BRANCH = git rev-parse --abbrev-ref HEAD with timeout
  if git fails, times out, or returns empty:
    JSON_BLOCK(cannot verify branch)
  if CURRENT_BRANCH != START_BRANCH:
    JSON_BLOCK(branch changed)

  LS_FILES_EXIT = git ls-files --error-unmatch PLAN_FILE with timeout
  if timeout or unexpected git error:
    JSON_BLOCK(git tracking check failed)

  PLAN_IS_TRACKED = (LS_FILES_EXIT == 0)

  if PLAN_TRACKED == "true":
    PLAN_GIT_STATUS = git status --porcelain PLAN_FILE with timeout
    if status command timeout/error:
      JSON_BLOCK(git status failed)
    if PLAN_IS_TRACKED != true:
      JSON_BLOCK(plan no longer tracked)
    if PLAN_GIT_STATUS non-empty:
      JSON_BLOCK(plan has uncommitted modifications)
  else:
    if PLAN_IS_TRACKED == true:
      JSON_BLOCK(plan now tracked but loop was started untracked)

  ALLOW
```

```text
on start-rlcr-loop(plan_file, --track-plan-file?):
  reject both --plan-file and positional plan file
  require Git repo and at least one commit
  unless skip-impl-no-plan:
    reject absolute path
    reject spaces
    reject shell metacharacters
    reject symlink file or symlink parent segment
    require file exists, readable, inside project, not in submodule
    compute PLAN_IS_TRACKED via git ls-files
    if --track-plan-file:
      require tracked and git status clean
    else:
      require not tracked
    require at least 5 physical lines
    require at least 3 content lines, excluding blanks, # comments, and HTML comments
  copy original plan to LOOP_DIR/plan.md
  write state.md with plan_file, plan_tracked, start_branch
```

```text
on stop hook before review_started:
  BACKUP_PLAN = LOOP_DIR/plan.md
  FULL_PLAN_PATH = PROJECT_ROOT/PLAN_FILE

  if backup missing:
    JSON_BLOCK(plan backup missing)
  if original plan missing:
    JSON_BLOCK(plan deleted)

  if PLAN_TRACKED == true:
    if git status --porcelain PLAN_FILE non-empty:
      JSON_BLOCK(uncommitted plan modification)

  if diff(FULL_PLAN_PATH, BACKUP_PLAN) differs:
    JSON_BLOCK(plan modified, using plan-file-modified template)

  continue stop hook
```

**Transition Table**

| Gate | State/Input | Pass Transition | Block Transition |
|---|---|---|---|
| Active loop discovery | hook stdin `session_id`, `.humanize/rlcr` | no active loop -> allow; active loop -> parse state | none |
| State schema | `state.md` frontmatter | valid -> load `plan_file`, `plan_tracked`, `start_branch` | malformed -> stderr + exit 1; missing required field -> JSON block |
| Branch consistency | `START_BRANCH`, current Git branch | equal -> plan tracking gate | mismatch or Git failure -> JSON block |
| Tracking mode: tracked | `plan_tracked=true`, `git ls-files`, `git status --porcelain` | tracked and clean -> allow | no longer tracked, dirty, timeout, unexpected Git error -> JSON block |
| Tracking mode: untracked | `plan_tracked!=true`, `git ls-files` | not tracked -> allow | now tracked, timeout, unexpected Git error -> JSON block |
| Stop integrity | `review_started`, original plan, backup plan, diff | review phase skips; pre-review equal content -> continue | backup missing, original deleted, uncommitted tracked change, content diff -> JSON block |
| Backup mutator hooks | Write/Edit/Bash tool input targeting `.humanize/rlcr/.../plan.md` | non-loop/legacy paths allowed per tests | active loop backup write/edit/bash mutation -> exit 2 |

**Source Evidence**

- `UserPromptSubmit` hook reads hook input, extracts `session_id`, finds active loop under `.humanize/rlcr`, and silently allows when no active loop exists: `hooks/loop-plan-file-validator.sh:27-40`.
- State parsing is strict; malformed state emits safety error and exits nonzero. The loaded state variables are `PLAN_TRACKED`, `PLAN_FILE`, and `START_BRANCH`: `hooks/loop-plan-file-validator.sh:42-55`.
- Required schema fields are `plan_tracked` and `start_branch`; missing values route to `schema_validation_error` JSON block: `hooks/loop-plan-file-validator.sh:60-90`.
- Branch consistency uses `git rev-parse --abbrev-ref HEAD` with timeout; Git failure or branch mismatch blocks: `hooks/loop-plan-file-validator.sh:96-116`.
- Tracked-plan mode requires `git ls-files --error-unmatch` success and empty `git status --porcelain`; timeout and unexpected Git errors fail closed: `hooks/loop-plan-file-validator.sh:124-193`.
- Untracked/default mode checks only that `git ls-files --error-unmatch` does not report the plan file as tracked; if it becomes tracked, the hook blocks: `hooks/loop-plan-file-validator.sh:194-230`.
- Plan modification block template states that plan files may not be modified during an active session and instructs cancel/update/restart, with backup path included: `prompt-template/block/plan-file-modified.md:3-12`.
- Start command rejects both `--plan-file` and positional plan file, handles skip-impl no-plan, and otherwise requires a plan file: `scripts/setup-rlcr-loop.sh:399-427`.
- Start command requires a Git repository and at least one commit: `scripts/setup-rlcr-loop.sh:429-443`.
- Start command rejects absolute paths, spaces, shell metacharacters, symlinks, missing/unreadable files, paths escaping project root, and submodule-contained plans: `scripts/setup-rlcr-loop.sh:445-556`.
- Start command implements tracking-mode validation: `--track-plan-file` requires tracked and clean; default requires not tracked: `scripts/setup-rlcr-loop.sh:558-607`.
- Start command enforces content threshold: at least 5 lines and at least 3 content lines after excluding blank lines, `#` comment lines, and HTML comments: `scripts/setup-rlcr-loop.sh:611-676`.
- Start command copies the plan to `LOOP_DIR/plan.md` and writes `plan_file`, `plan_tracked`, and `start_branch` to state: `scripts/setup-rlcr-loop.sh:829-890`.
- Stop hook skips plan integrity checks after `review_started=true`; before that it requires backup existence, original existence, tracked-plan clean status, and exact `diff` match against backup: `hooks/loop-codex-stop-hook.sh:322-399`.
- Hook tests establish valid state, YAML-quoted `plan_file`, missing/malformed schema blocking, and branch-change blocking: `tests/test-plan-file-hooks.sh:145-243`.
- Hook tests establish `Write`, `Edit`, and `Bash` validators block active loop `plan.md` backup edits, including direct path, command substitution, glob, brace expansion, pipe, and backtick attempts: `tests/test-plan-file-hooks.sh:252-393`.
- Hook tests establish quoted `start_branch` parsing, branch mismatch with quoted value, and hyphenated plan path handling: `tests/test-plan-file-hooks.sh:399-448`, `tests/test-plan-file-hooks.sh:527-558`.
- Stop-hook tests establish block behavior for modified project plan, deleted project plan, missing backup, tracked uncommitted modification, outdated schema JSON block, and tracked committed content changes detectable only by content diff: `tests/test-plan-file-hooks.sh:567-835`.
- Legacy `.humanize-loop.local/.../plan.md` is explicitly allowed by Bash/Write/Edit validator tests and is not treated as an active loop backup path: `tests/test-plan-file-hooks.sh:1132-1170`.
- Start validation tests assert absolute path rejection, missing file/dir rejection, spaces/metacharacter rejection, symlink rejection, project escape rejection, non-Git repo rejection, and no-commit repo rejection: `tests/test-plan-file-validation.sh:88-322`.
- Start validation tests assert tracking-mode cases: tracked file without `--track-plan-file` is rejected, untracked file with `--track-plan-file` is rejected, and modified tracked file with `--track-plan-file` is rejected: `tests/test-plan-file-validation.sh:328-425`.
- Start validation tests assert YAML-unsafe branch-name rejection and content validation for blank/sparse/comment-only plans versus sufficient real content: `tests/test-plan-file-validation.sh:431-660`.
- CLI tests assert `--plan-file` is accepted as an alternative input and specifying both `--plan-file` plus positional plan is rejected: `tests/test-plan-file-validation.sh:666-691`.

**Edge Cases And Risks**

- `plan_tracked` routing is literal: only `"true"` takes the tracked branch; anything else falls into the untracked branch. If strict parsing does not validate boolean domain, malformed non-empty values could be treated as false. Evidence: `hooks/loop-plan-file-validator.sh:124`, `hooks/loop-plan-file-validator.sh:194`.
- The `UserPromptSubmit` validator’s default path says “must be gitignored,” but the actual gate checks only “not tracked” via `git ls-files`; it does not directly call `git check-ignore`. Evidence: `hooks/loop-plan-file-validator.sh:195-221`.
- Prompt-time validator does not compare original plan content with the backup and does not check untracked plan existence. A gitignored plan can be edited or deleted between prompts and still pass this hook; stop hook catches deletion/diff before review phase. Evidence: prompt hook tracking-only branch `hooks/loop-plan-file-validator.sh:194-230`; stop hook deletion/diff gates `hooks/loop-codex-stop-hook.sh:345-396`.
- Stop hook’s tracked-plan `git status` check uses `|| echo ""`, so a Git status failure there does not fail closed the way `loop-plan-file-validator.sh` does. Content diff may still catch many mutations, but Git-status failure itself is not surfaced at this gate. Evidence: `hooks/loop-codex-stop-hook.sh:361-374` versus fail-closed status handling in `hooks/loop-plan-file-validator.sh:151-172`.
- Stop hook skips all plan integrity checks once `review_started=true`; that is intentional per comment, but it narrows the immutability invariant to pre-review phases. Evidence: `hooks/loop-codex-stop-hook.sh:322-327`.
- There is a stale or contradictory comment in stop hook: it says “Plan changes are now allowed,” but the following `diff` block still blocks changed plans. Evidence: `hooks/loop-codex-stop-hook.sh:377-396`; tests confirm blocking at `tests/test-plan-file-hooks.sh:567-605` and `tests/test-plan-file-hooks.sh:756-835`.
- Content validation treats all lines beginning with `#` as comments, not Markdown headings. This means a plan made only of Markdown headings may count as insufficient content unless it has at least three non-`#` content lines. Evidence: `scripts/setup-rlcr-loop.sh:628-663`; tests assert `#`-only plans are rejected at `tests/test-plan-file-validation.sh:589-607`.
- Write/Edit/Bash backup protection is behaviorally covered by focus tests, including common shell-expansion bypasses, but this analysis did not fully expand the internal regex/parser implementation of those three validators.

**Explicitly Out Of Scope**

- Installation, marketing, screenshots, and generic usage prose.
- Full RLCR loop orchestration unrelated to plan-file integrity, including Codex execution, code review routing, BitLesson enforcement, goal tracker placeholder checks, artifact size gates, and general Git cleanliness gates.
- Codex model/effort parameter validation, except where tests appear adjacent to plan validation.
- Full implementation internals of `loop-write-validator.sh`, `loop-edit-validator.sh`, and `loop-bash-validator.sh`; only their plan-backup behavior asserted by `tests/test-plan-file-hooks.sh` is included.
- Network behavior and external documentation; no network searches were run.
- Any file edits, commits, or test execution.