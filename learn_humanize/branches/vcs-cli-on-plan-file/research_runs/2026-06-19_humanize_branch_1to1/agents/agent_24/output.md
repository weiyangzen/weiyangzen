# agent_24 vcs-cli-on-plan-file 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `4dd1ca2fece39d3c6d7f84965cd71bda02489397`

## Item Evidence

### VCS_CLI_ON_PLAN_FILE-HZ-024 `file` `scripts/setup-rlcr-loop.sh`
- cursor: `[_]`
- core_role: Bootstrap script for `/humanize:start-rlcr-loop`. It turns a user-supplied markdown plan file into an active RLCR loop session by validating prerequisites, creating `.humanize-loop.local/<timestamp>/`, writing loop state, backing up the plan, generating `goal-tracker.md`, and emitting the Round 0 prompt consumed by the current Claude session. The actual stop/review loop is downstream in `hooks/loop-codex-stop-hook.sh`; this file creates the state contract that hook relies on.
- algorithmic_behavior: 
  - Initializes strict shell mode and imports `hooks/lib/loop-common.sh` for portable path handling via `get_relative_path` (`scripts/setup-rlcr-loop.sh:11-15`, `hooks/lib/loop-common.sh:143-232`).
  - Defines defaults for Codex model, effort, timeout, and max iterations (`scripts/setup-rlcr-loop.sh:21-25`).
  - Parses one positional plan file plus options: `--max`, `--codex-model MODEL:EFFORT`, `--codex-timeout`, `--push-every-round`, and `--commit-plan-file`; duplicate plan files and unknown options are hard errors (`scripts/setup-rlcr-loop.sh:31-170`).
  - Normalizes a relative plan path against `CLAUDE_PROJECT_DIR` or `pwd`, verifies the file exists, requires a git repository with `HEAD`, computes project-relative and git-root-relative paths, and rejects paths containing spaces or regex metacharacters (`scripts/setup-rlcr-loop.sh:176-249`).
  - Enforces minimum plan substance by requiring at least five lines and refuses to start unless `codex` is on `PATH` (`scripts/setup-rlcr-loop.sh:225-241`).
  - Applies stricter rules when `--commit-plan-file` is set: the plan must be inside the git repo, not ignored, tracked, and clean (`scripts/setup-rlcr-loop.sh:251-303`).
  - Creates timestamped loop state under `.humanize-loop.local`, copies the immutable starting plan to `plan-backup.md`, records `START_COMMIT`, and writes YAML-like frontmatter with current round, max iterations, Codex config, push policy, plan path, tracked status, and start time (`scripts/setup-rlcr-loop.sh:309-340`).
  - Builds `goal-tracker.md` with an immutable goal/acceptance section and mutable task/evolution tables. It heuristically extracts goal text from `## Goal`, `## Objective`, or `## Purpose`, and acceptance criteria from `## Acceptance`, `## Criteria`, or `## Requirements`; otherwise it leaves placeholders for Round 0 initialization (`scripts/setup-rlcr-loop.sh:346-434`).
  - Generates `round-0-prompt.md` by embedding the plan file, requiring goal-tracker initialization, instructing todo creation for all discovered work, forbidding loop-state tampering, and requiring commit plus `round-0-summary.md`; it appends a push instruction only when `--push-every-round` is true (`scripts/setup-rlcr-loop.sh:440-501`).
  - Prints an activation summary and then prints the generated Round 0 prompt plus completion requirements to stdout (`scripts/setup-rlcr-loop.sh:507-561`).
- inputs_outputs_state:
  - Inputs: CLI args, `CLAUDE_PROJECT_DIR` or current directory, the markdown plan file content, current git repository/HEAD/tracking metadata, presence of `codex`, and the shared loop library.
  - Outputs: `.humanize-loop.local/<timestamp>/state.md`, `plan-backup.md`, `goal-tracker.md`, `round-0-prompt.md`, and the expected future summary path `round-0-summary.md` (`scripts/setup-rlcr-loop.sh:309-340`, `346-493`).
  - State transition: no active setup artifacts become an active loop when `state.md` exists with `current_round: 0`. Downstream hooks treat that file as the active cursor; `find_active_loop` selects the newest loop directory with `state.md` (`hooks/lib/loop-common.sh:63-84`).
  - Downstream state evolution: the stop hook reads `current_round`, `max_iterations`, Codex config, `plan_file`, `commit_plan_file`, and `start_commit`; it advances `current_round`, creates later prompts, or renames `state.md` to `completed-state.md`, `stopped-state.md`, or `unexpected-state.md` (`hooks/loop-codex-stop-hook.sh:185-213`, `380-416`, `865-900`; `hooks/lib/loop-common.sh:23-38`).
- gates_or_invariants:
  - Exactly one plan file argument is allowed (`scripts/setup-rlcr-loop.sh:159-166`).
  - The loop may start only in a git repo with at least one commit (`scripts/setup-rlcr-loop.sh:199-210`).
  - Plan file paths must be simple enough for later git-status filtering: no whitespace and no listed regex metacharacters (`scripts/setup-rlcr-loop.sh:215-223`).
  - Plan file must have at least five lines and `codex` must be installed (`scripts/setup-rlcr-loop.sh:225-241`).
  - `--commit-plan-file` means plan file is intentional commit surface: it must be in repo, not ignored, tracked, and clean (`scripts/setup-rlcr-loop.sh:251-303`).
  - Without `--commit-plan-file`, the plan can remain uncommitted, but the backup becomes the content invariant. `loop-plan-validator.sh` blocks later prompts if the plan changes or disappears relative to `plan-backup.md` (`hooks/loop-plan-validator.sh:253-317`).
  - `commit_plan_file: false` is enforced after setup by bash and stop hooks: staged plan-file commits are blocked before commit, and accidental plan-file commits since `start_commit` are blocked after commit (`hooks/loop-bash-validator.sh:99-148`, `hooks/loop-codex-stop-hook.sh:296-340`).
  - Round 0 must initialize goal tracker placeholders before exit; the stop hook blocks if the generated placeholders remain (`hooks/loop-codex-stop-hook.sh:444-503`).
- dependencies_and_callers:
  - Direct caller: slash command `commands/start-rlcr-loop.md` allows only the setup script and executes it with user arguments (`commands/start-rlcr-loop.md:1-14`).
  - Shared library dependency: `hooks/lib/loop-common.sh`, which itself sources `template-loader.sh`; setup only visibly uses `get_relative_path`, but sourcing can also validate template directory availability (`hooks/lib/loop-common.sh:11-21`, `143-232`).
  - Runtime consumers of setup output: `hooks/loop-codex-stop-hook.sh` consumes `state.md`, `goal-tracker.md`, round prompt/summary/review files, Codex config, push policy, plan file path, and `start_commit` (`hooks/loop-codex-stop-hook.sh:8-12`, `185-188`, `390-403`, `421-448`, `530-699`).
  - Prompt-time validator: `hooks/loop-plan-validator.sh` uses `state.md` and `plan-backup.md` to prevent stale or changed plans from being used mid-loop (`hooks/loop-plan-validator.sh:44-87`, `253-317`).
  - Bash validator: `hooks/loop-bash-validator.sh` uses setup state to block branch-history violations, unintended `git push`, plan-file commits, state edits, and goal-tracker edits through shell commands (`hooks/loop-bash-validator.sh:45-96`, `99-175`).
  - User-facing docs and monitoring mention the generated `.humanize-loop.local/<timestamp>/` artifacts and state files (`README.md` references surfaced around `.humanize-loop.local`, `state.md`, `goal-tracker.md`, and `round-N-review-result.md` in repository search).
- edge_cases_or_failure_modes:
  - `--max 0` and `--codex-timeout 0` pass the regex check even though error text says “positive integer”; `--max 0` causes the first stop hook pass to exceed max immediately after Round 0 summary (`scripts/setup-rlcr-loop.sh:112-116`, `139-143`; `hooks/loop-codex-stop-hook.sh:510-516`).
  - Starting multiple loops in the same project is not blocked. Because `find_active_loop` uses only the newest timestamped directory, an older `state.md` can become ignored or “zombie” state (`hooks/lib/loop-common.sh:63-84`).
  - Timestamp precision is seconds. Two starts in the same second reuse the same loop directory via `mkdir -p`, potentially overwriting `state.md`, `plan-backup.md`, and Round 0 prompt (`scripts/setup-rlcr-loop.sh:311-318`, `326-340`, `442-493`).
  - Goal and acceptance extraction is heuristic. The `sed` range includes the terminating heading before later `head` trimming, so short sections can accidentally include the next heading in extracted text; missing headings leave placeholders that must be fixed in Round 0 (`scripts/setup-rlcr-loop.sh:369-397`).
  - The generated state file writes absolute paths and option values unquoted in frontmatter. The script rejects many problematic project-relative path characters, but it does not fully YAML-escape values (`scripts/setup-rlcr-loop.sh:326-340`).
  - `PLAN_CONTENT=$(cat "$PLAN_FILE")` is assigned but unused; this is harmless for normal text plans but indicates redundant memory/load work for large plan files (`scripts/setup-rlcr-loop.sh:346-347`).
  - Setup requires `codex` even though Codex is not invoked until stop-hook review; environments that want to initialize state before installing Codex cannot (`scripts/setup-rlcr-loop.sh:235-241`).
- validation_or_tests:
  - Static test coverage exists in `tests/test-plan-file-handling.sh`: it checks help text for `--commit-plan-file`, state fields, plan backup creation, project-root ordering, tracked/clean checks, ignored-file checks, simple path validation, git repo/commit requirements, and outside-repo rejection (`tests/test-plan-file-handling.sh:55-148`, `149-218`, `600-659`).
  - The same test file verifies downstream hook expectations from setup state: stop hook reads `commit_plan_file` and `start_commit`, filters plan-file status, performs post-commit validation, and documents prompt-time validation (`tests/test-plan-file-handling.sh:219-291`, `661-680`).
  - Bash-validator tests verify the pre-commit staged-plan-file block that relies on setup’s `commit_plan_file` and `plan_file` state fields (`tests/test-plan-file-handling.sh:295-334`).
  - Template error tests cover safe fallback behavior for missing templates in the shared loader that `loop-common.sh` sources before setup validation (`tests/test-error-scenarios.sh:21-120`).
  - No runtime execution was performed for this research pass because the branch export is read-only and this script’s normal behavior creates `.humanize-loop.local` state files.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `1 unique assigned item section present`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`