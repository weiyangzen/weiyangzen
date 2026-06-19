# agent_024 use-realpath4everything 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`

## Item Evidence

### USE_REALPATH4EVERYTHING-HZ-024 `directory` `skills/humanize-rlcr`
- cursor: `[_]`
- core_role:
  - `skills/humanize-rlcr` is a Codex skill/flow entrypoint for the Humanize RLCR loop. The directory contains one recursively inspected file: `skills/humanize-rlcr/SKILL.md`.
  - The file is not executable implementation code. Its algorithmic role is orchestration and operator contract: it tells Codex how to start RLCR, what per-round files are authoritative, which state files must not be edited, and which native Stop-hook gates own phase transitions.
  - Metadata marks it as `name: humanize-rlcr`, `type: flow`, `user-invocable: false`, and `disable-model-invocation: true`, so it is an installed flow entrypoint rather than an autonomous model prompt generator (`skills/humanize-rlcr/SKILL.md:1-7`).
  - It depends on installer-time hydration of `{{HUMANIZE_RUNTIME_ROOT}}`, then delegates real setup and cancel behavior to runtime scripts under that root (`skills/humanize-rlcr/SKILL.md:14-22`, `skills/humanize-rlcr/SKILL.md:30-31`, `skills/humanize-rlcr/SKILL.md:111-112`).

- algorithmic_behavior:
  - Required setup path: run `"{{HUMANIZE_RUNTIME_ROOT}}/scripts/setup-rlcr-loop.sh" $ARGUMENTS`; if setup exits nonzero, stop and report the error (`skills/humanize-rlcr/SKILL.md:24-35`).
  - Per-round behavior is a fixed loop:
    - read `.humanize/rlcr/<timestamp>/round-<N>-prompt.md`, or finalize prompt files during finalize phase;
    - implement required changes;
    - commit changes;
    - write either `round-<N>-summary.md` or `finalize-summary.md`;
    - stop/exit normally so the native Humanize Stop hook runs;
    - if the hook blocks, follow its returned instructions and continue (`skills/humanize-rlcr/SKILL.md:36-49`).
  - The skill itself does not parse state, run Codex, or validate diffs. It explicitly delegates those decisions to the native Stop-hook path, listing enforced checks such as schema validation, branch consistency, plan integrity, incomplete Task/Todo blocking, clean git state, unpushed commits when requested, summary presence, max-iteration handling, alignment rounds, marker handling, review-phase transition guard, code-review gating, failed/empty Codex review blocking, and Codex open-question handling (`skills/humanize-rlcr/SKILL.md:50-68`).
  - The delegated setup script implements the concrete initialization algorithm:
    - parses options including `--max`, `--codex-model`, `--codex-timeout`, `--push-every-round`, `--plan-file`, `--track-plan-file`, `--base-branch`, `--full-review-round`, `--skip-impl`, `--claude-answer-codex`, `--agent-teams`, `--yolo`, `--skip-quiz`, BitLesson flags, and `--privacy` (`scripts/setup-rlcr-loop.sh:188-320`);
    - validates required tools `codex`, `jq`, and `git` (`scripts/setup-rlcr-loop.sh:340-363`);
    - rejects a second active loop before creating a new one (`scripts/setup-rlcr-loop.sh:369-379`);
    - validates plan path and content, git state, branch/model YAML safety, and base branch selection (`scripts/setup-rlcr-loop.sh:455-607`, `scripts/setup-rlcr-loop.sh:618-741`, `scripts/setup-rlcr-loop.sh:748-815`);
    - creates `.humanize/rlcr/<timestamp>/state.md`, `goal-tracker.md`, `round-0-summary.md`, `round-0-contract.md`, and `round-0-prompt.md` (`scripts/setup-rlcr-loop.sh:821-923`, `scripts/setup-rlcr-loop.sh:929-1189`, `scripts/setup-rlcr-loop.sh:1191-1441`);
    - prints the initial prompt and completion requirements (`scripts/setup-rlcr-loop.sh:1451-1540`).
  - The delegated Stop hook implements the phase machine:
    - reads hook JSON input and session id;
    - finds the active loop;
    - applies background-task short-circuit guards;
    - resolves `state.md`, `finalize-state.md`, or methodology-analysis state;
    - parses and validates state fields before running review logic (`hooks/loop-codex-stop-hook.sh:25-99`, `hooks/loop-codex-stop-hook.sh:103-180`).
  - Stop-hook review behavior:
    - implementation completion is signaled by final `COMPLETE`;
    - on first completion, the hook sets `review_started=true`, writes `.review-phase-started`, and runs `codex review`;
    - review issues are recognized by priority markers, causing another prompt/summary round;
    - no review issues transitions to finalize by renaming `state.md` to `finalize-state.md` and returning a blocking finalize prompt (`hooks/loop-codex-stop-hook.sh:1817-1872`, `hooks/loop-codex-stop-hook.sh:1884-1907`, `hooks/loop-codex-stop-hook.sh:1281-1365`, `hooks/loop-codex-stop-hook.sh:1456-1510`).
  - Shared helper behavior confirms the concrete review-issue detector scans the last 50 log lines for priority markers near line starts, writes extracted issues to `round-<N>-review-result.md`, and returns distinct outcomes for issues, no issues, and missing/empty log (`hooks/lib/loop-common.sh:720-788`).

- inputs_outputs_state:
  - Inputs:
    - `$ARGUMENTS` passed through from the flow to `setup-rlcr-loop.sh` (`skills/humanize-rlcr/SKILL.md:30-31`, `skills/humanize-rlcr/SKILL.md:78-95`).
    - Optional plan file path unless `--skip-impl` is used (`skills/humanize-rlcr/SKILL.md:80-83`, `skills/humanize-rlcr/SKILL.md:90`).
    - Runtime-root placeholder hydrated by installer (`skills/humanize-rlcr/SKILL.md:14-22`).
    - Per-round loop prompt files generated under `.humanize/rlcr/<timestamp>/` (`skills/humanize-rlcr/SKILL.md:40`).
  - Outputs:
    - Normal phase summary: `.humanize/rlcr/<timestamp>/round-<N>-summary.md` (`skills/humanize-rlcr/SKILL.md:43-45`).
    - Finalize phase summary: `.humanize/rlcr/<timestamp>/finalize-summary.md` (`skills/humanize-rlcr/SKILL.md:45`).
    - Commits are required after implementation/fixes before summary handoff (`skills/humanize-rlcr/SKILL.md:41-46`).
    - Setup outputs initial loop state and prompt files; Stop hook outputs JSON block/allow decisions and generated next-round/finalize prompts (`scripts/setup-rlcr-loop.sh:880-918`, `scripts/setup-rlcr-loop.sh:1195-1201`, `scripts/setup-rlcr-loop.sh:1225-1290`, `hooks/loop-codex-stop-hook.sh:1356-1365`, `hooks/loop-codex-stop-hook.sh:1952-2037`).
  - State transitions:
    - setup creates `state.md` with `current_round: 0`, max/config fields, plan/branch/base metadata, `review_started`, session id placeholder, BitLesson fields, drift fields, and timestamp (`scripts/setup-rlcr-loop.sh:880-907`).
    - setup writes `.humanize/.pending-session-id` so PostToolUse can patch session id safely (`scripts/setup-rlcr-loop.sh:909-918`).
    - skip-implementation mode starts with `review_started` true and `.review-phase-started` already present (`scripts/setup-rlcr-loop.sh:872-878`, `scripts/setup-rlcr-loop.sh:920-923`).
    - review phase is guarded by `.review-phase-started`; missing marker while state says review started blocks as inconsistent (`hooks/loop-codex-stop-hook.sh:1884-1900`).
    - finalize transition renames active state to `finalize-state.md` and blocks with finalize instructions rather than silently exiting (`hooks/loop-codex-stop-hook.sh:1281-1365`).
    - cancel path is separate: `cancel-rlcr-loop.sh` finds active state, writes `.cancel-requested`, removes pending session signal, and renames active state to `cancel-state.md`; finalize cancellation requires `--force` (`scripts/cancel-rlcr-loop.sh:80-91`, `scripts/cancel-rlcr-loop.sh:103-149`, `scripts/cancel-rlcr-loop.sh:156-167`).

- gates_or_invariants:
  - The skill’s critical invariants are operator rules:
    - never manually edit `state.md` or `finalize-state.md`;
    - never bypass a blocked hook result by declaring completion manually;
    - never run ad-hoc `codex exec` or `codex review` in place of hook-managed transitions;
    - always use generated `round-*-prompt.md` and `round-*-review-result.md` as source of truth (`skills/humanize-rlcr/SKILL.md:69-75`).
  - Setup gates:
    - exactly one active loop at a time for setup without session filtering (`scripts/setup-rlcr-loop.sh:369-379`);
    - plan path must be relative, space-free, metacharacter-free, not a symlink, within project, not in submodule, and have acceptable tracked/gitignored status according to `--track-plan-file` (`scripts/setup-rlcr-loop.sh:455-607`);
    - plan content must have at least five lines and at least three non-comment content lines, except skip-impl without plan (`scripts/setup-rlcr-loop.sh:615-676`);
    - git working tree must be clean except untracked `.humanize` runtime paths (`scripts/setup-rlcr-loop.sh:719-741`);
    - branch names and Codex model/effort values must satisfy safety patterns (`scripts/setup-rlcr-loop.sh:692-716`, `scripts/setup-rlcr-loop.sh:799-805`);
    - base branch must be local or auto-detected from remote default, local main, or local master (`scripts/setup-rlcr-loop.sh:743-815`).
  - Hook gates delegated by the skill:
    - state/schema fields are validated before use (`hooks/loop-codex-stop-hook.sh:107-180`);
    - review failure and empty review output are hard blocks, not success/finalize paths (`hooks/loop-codex-stop-hook.sh:1256-1271`);
    - code review issues keep the loop active, and no issues enter finalize (`hooks/loop-codex-stop-hook.sh:1262-1278`);
    - max iterations can terminate before finalize (`hooks/loop-codex-stop-hook.sh:1833-1841`);
    - direct state-file modification is blocked by validator helpers for normal and finalize state (`hooks/lib/loop-common.sh:859-875`, `hooks/lib/loop-common.sh:994-1004`).
  - File-access invariants:
    - prompt files are instructions from the loop to the agent and must not be written (`hooks/lib/loop-common.sh:850-857`);
    - finalize phase uses `finalize-summary.md` for notes and blocks historical round contract access (`hooks/lib/loop-common.sh:877-890`);
    - `.humanize` runtime state must not be tracked/staged/committed (`hooks/lib/loop-common.sh:1442-1465`).

- dependencies_and_callers:
  - Direct children:
    - `skills/humanize-rlcr/SKILL.md` is the only child file and owns the flow documentation/contract.
  - Runtime dependencies referenced by the skill:
    - `scripts/setup-rlcr-loop.sh` for activation and state/prompt scaffolding (`skills/humanize-rlcr/SKILL.md:30-31`);
    - `scripts/cancel-rlcr-loop.sh` for cancellation (`skills/humanize-rlcr/SKILL.md:109-112`);
    - native Humanize Stop hook for gate enforcement (`skills/humanize-rlcr/SKILL.md:46-68`).
  - Setup and cancel both depend on `hooks/lib/loop-common.sh` for project-root resolution, active-loop lookup, state parsing/constants, path predicates, marker constants, and shared validation messages (`hooks/lib/loop-common.sh:3-14`, `hooks/lib/loop-common.sh:24-76`, `hooks/lib/loop-common.sh:264-330`).
  - Stop-hook implementation depends on:
    - `hooks/lib/loop-common.sh`;
    - `scripts/portable-timeout.sh`;
    - `hooks/lib/methodology-analysis.sh`;
    - `hooks/lib/loop-bg-tasks.sh` indirectly sourced through loop common (`hooks/loop-codex-stop-hook.sh:42-55`, `hooks/lib/loop-common.sh:258-262`).
  - Sibling/parent coordination:
    - `skills/humanize/SKILL.md` is the broader Humanize skill and references the same setup/cancel scripts for user-facing workflows.
    - `commands/start-rlcr-loop.md` is the Claude slash-command counterpart with plan compliance pre-check, plan understanding quiz, and setup execution (`commands/start-rlcr-loop.md:1-15`, `commands/start-rlcr-loop.md:60-115`).
    - `commands/cancel-rlcr-loop.md` is the Claude slash-command counterpart for cancel, including finalize confirmation handling (`commands/cancel-rlcr-loop.md:1-37`).
    - `scripts/install-skill.sh` includes `humanize-rlcr` in the installed skills bundle; installation tests assert Codex installs preserve this entrypoint (`tests/test-codex-hook-install.sh:118-128`).
  - External tools:
    - setup requires `codex`, `jq`, and `git` (`scripts/setup-rlcr-loop.sh:340-363`);
    - review phase runs `codex review --base <review_base>` with timeout and model effort arguments (`hooks/loop-codex-stop-hook.sh:1171-1229`).

- edge_cases_or_failure_modes:
  - Setup exits nonzero and the skill instructs the caller to stop/report immediately (`skills/humanize-rlcr/SKILL.md:34`).
  - Plan file edge cases include absolute path, missing parent, spaces, shell metacharacters, symlink file, symlink parent path, nonexistent/unreadable file, outside-project real path, submodule path, tracked-vs-gitignored mismatch, too-short plans, and comment-only plans (`scripts/setup-rlcr-loop.sh:455-676`).
  - Git edge cases include non-repository, no commits, dirty working tree, git command timeout, YAML-unsafe branch, absent local base branch, and remote-only base branch (`scripts/setup-rlcr-loop.sh:433-443`, `scripts/setup-rlcr-loop.sh:686-741`, `scripts/setup-rlcr-loop.sh:748-815`).
  - Codex config edge cases include unsafe model strings and effort outside `xhigh|high|medium|low`; the Stop hook revalidates state values in case `state.md` was manually edited (`scripts/setup-rlcr-loop.sh:702-716`, `hooks/loop-codex-stop-hook.sh:172-180`).
  - Review edge cases include `codex review` command failure, no stdout/empty log, issue markers found in review output, and missing review-phase marker despite `review_started=true` (`hooks/loop-codex-stop-hook.sh:1256-1278`, `hooks/loop-codex-stop-hook.sh:1884-1900`).
  - Finalize edge cases include state-protected files: `finalize-state.md` cannot be modified, `finalize-summary.md` is the allowed finalize output, and round contracts are blocked during finalize (`hooks/lib/loop-common.sh:868-890`, `hooks/lib/loop-common.sh:1000-1024`).
  - Cancellation edge case: finalize cancellation is intentionally two-step; plain cancel returns `FINALIZE_NEEDS_CONFIRM`, and `--force` is required to rename `finalize-state.md` to `cancel-state.md` (`scripts/cancel-rlcr-loop.sh:139-149`).
  - Misclassification assessment: this directory is core-adjacent rather than algorithm implementation by itself. It is still core for the branch because it defines the Codex RLCR entrypoint and delegates to the core state machine/gates.

- validation_or_tests:
  - Installation coverage: `tests/test-codex-hook-install.sh` asserts Codex install syncs the Humanize bundle and keeps `skills/humanize-rlcr/SKILL.md` present (`tests/test-codex-hook-install.sh:118-128`).
  - Plan validation coverage: `tests/test-plan-file-validation.sh` covers absolute path rejection, nonexistent file/directory rejection, spaces, shell metacharacters, symlink rejection, valid content acceptance, single-line HTML comment handling, `--plan-file` parsing, duplicate plan-file rejection, and Codex model/effort validation (`tests/test-plan-file-validation.sh:92-199`, `tests/test-plan-file-validation.sh:626-736`).
  - Finalize coverage: `tests/test-finalize-phase.sh` covers allowing `finalize-summary.md`, blocking `finalize-state.md`, blocking round contracts during finalize, `COMPLETE` transition to `finalize-state.md`, and max-iteration behavior that skips finalize (`tests/test-finalize-phase.sh:386-431`, `tests/test-finalize-phase.sh:597-626`).
  - Command documentation coverage: `commands/start-rlcr-loop.md` documents the same two-phase semantics and Stop hook flow; `commands/cancel-rlcr-loop.md` documents cancel output handling and finalize confirmation (`commands/start-rlcr-loop.md:117-128`, `commands/start-rlcr-loop.md:182-209`, `commands/cancel-rlcr-loop.md:17-37`).
  - I did not execute the full test suite because this research assignment is read-only and asks for notes only; validation evidence above is from direct inspection of existing test files.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 1 item section, matching the assigned table
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`