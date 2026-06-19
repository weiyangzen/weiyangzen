# agent_19 fix-humanize-escape 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 3
- source_commit: `05ff234806d5fe8686b2d9554c00eaa6f3e77dd8`

## Item Evidence

### FIX_HUMANIZE_ESCAPE-HZ-019 `file` `hooks/loop-plan-file-validator.sh`
- cursor: `[_]`
- core_role:
  - UserPromptSubmit gate for active RLCR loops. It validates loop state compatibility, prevents branch switching during a loop, and enforces the plan file tracking mode recorded when the loop started.
  - Registered as the `UserPromptSubmit` hook in `hooks/hooks.json:4-10`, so it runs before user prompts are accepted during an active loop.
  - It is a core state-machine guard, not an implementation worker: normal success is silent `exit 0`; blocked transitions return JSON with `"decision": "block"` and a human-facing `"reason"`.

- algorithmic_behavior:
  - Initializes strict bash mode with `set -euo pipefail` at `hooks/loop-plan-file-validator.sh:11`.
  - Resolves runtime roots from `SCRIPT_DIR` and `CLAUDE_PROJECT_DIR` or `pwd` at `hooks/loop-plan-file-validator.sh:13-14`.
  - Sources shared RLCR helpers from `hooks/lib/loop-common.sh` at `hooks/loop-plan-file-validator.sh:16-17`, which provides `find_active_loop`, state parsing, field constants, and template-loader wiring.
  - Sources `scripts/portable-timeout.sh` at `hooks/loop-plan-file-validator.sh:19-21`, then uses `GIT_TIMEOUT=30` for git calls at `hooks/loop-plan-file-validator.sh:23-24`.
  - Reads hook stdin into `INPUT` at `hooks/loop-plan-file-validator.sh:26-27`, but the current algorithm does not inspect the payload; stdin consumption mainly satisfies hook protocol expectations.
  - Finds the active loop under `$PROJECT_ROOT/.humanize/rlcr` at `hooks/loop-plan-file-validator.sh:29-31`; if no active loop exists, it allows the prompt by exiting cleanly at `hooks/loop-plan-file-validator.sh:33-36`.
  - Selects `finalize-state.md` instead of `state.md` when Finalize Phase is active at `hooks/loop-plan-file-validator.sh:38-42`.
  - Parses frontmatter through `parse_state_file "$STATE_FILE"` at `hooks/loop-plan-file-validator.sh:44-50`; the parser comes from `hooks/lib/loop-common.sh:112-139` and strips legacy quotes from `start_branch` and `plan_file`.
  - Enforces schema compatibility by requiring `plan_tracked` and `start_branch` at `hooks/loop-plan-file-validator.sh:52-86`. Missing required fields emit a schema-outdated block using `prompt-template/block/schema-outdated.md` via `load_and_render_safe`, with an inline fallback at `hooks/loop-plan-file-validator.sh:56-74`.
  - Verifies the current git branch using `git -C "$PROJECT_ROOT" rev-parse --abbrev-ref HEAD` under timeout at `hooks/loop-plan-file-validator.sh:88-103`.
  - Blocks branch drift when current branch differs from `start_branch` at `hooks/loop-plan-file-validator.sh:104-112`.
  - Builds `FULL_PLAN_PATH="$PROJECT_ROOT/$PLAN_FILE"` at `hooks/loop-plan-file-validator.sh:118`, but this variable is not used later; the actual checks operate on git-relative `$PLAN_FILE`.
  - If `plan_tracked == true`, it requires the plan path to remain tracked and clean:
    - `git ls-files --error-unmatch "$PLAN_FILE"` at `hooks/loop-plan-file-validator.sh:120-145`.
    - `git status --porcelain "$PLAN_FILE"` at `hooks/loop-plan-file-validator.sh:147-169`.
    - Blocks when the plan is no longer tracked at `hooks/loop-plan-file-validator.sh:171-179`.
    - Blocks when git reports uncommitted plan modifications at `hooks/loop-plan-file-validator.sh:181-189`.
  - If `plan_tracked != true`, it requires the plan path to remain untracked/gitignored from git’s perspective:
    - `git ls-files --error-unmatch "$PLAN_FILE"` at `hooks/loop-plan-file-validator.sh:190-215`.
    - Blocks if the plan is now tracked at `hooks/loop-plan-file-validator.sh:217-225`.
  - Final allow transition is silent `exit 0` at `hooks/loop-plan-file-validator.sh:228`.

- inputs_outputs_state:
  - Inputs:
    - Hook stdin, consumed with `cat` at `hooks/loop-plan-file-validator.sh:27`.
    - `CLAUDE_PROJECT_DIR`, falling back to the process working directory at `hooks/loop-plan-file-validator.sh:14`.
    - Active loop directory under `.humanize/rlcr`, found by `find_active_loop` at `hooks/lib/loop-common.sh:63-81`.
    - Either `.humanize/rlcr/<timestamp>/state.md` or `.humanize/rlcr/<timestamp>/finalize-state.md` at `hooks/loop-plan-file-validator.sh:38-45`.
    - State frontmatter fields: `plan_tracked`, `plan_file`, `start_branch`; required field names are defined in `hooks/lib/loop-common.sh:16-18`.
    - Git branch and path status from the repository at `$PROJECT_ROOT`.
  - Outputs:
    - No output on allow.
    - JSON block objects on invalid state, branch mismatch, git timeout, git failure, plan tracking drift, or plan dirtiness.
    - JSON strings are mostly emitted through heredocs; schema messages are escaped with `jq -Rs '.'` at `hooks/loop-plan-file-validator.sh:64-67`.
  - State transitions:
    - Does not mutate files or git state.
    - Operationally blocks RLCR prompt submission when the loop state is unsafe or incompatible.
    - Supports both normal loop and Finalize Phase state files by switching to `finalize-state.md`.

- gates_or_invariants:
  - Active loop invariant: only the newest active loop is considered because `find_active_loop` checks the newest timestamp directory and ignores older loop dirs; see `hooks/lib/loop-common.sh:58-81`.
  - Schema invariant: active state must include non-empty `plan_tracked` and `start_branch`; missing either is treated as an outdated schema and blocked.
  - Branch invariant: current git branch must equal the branch captured at loop startup.
  - Plan tracking invariant:
    - For `plan_tracked: true`, the plan file must remain tracked and have no uncommitted changes.
    - For `plan_tracked: false`, the plan file must not become tracked.
  - Fail-closed git invariant: git timeout exit code `124` and unexpected git errors block rather than allow.
  - Hook protocol invariant: all block conditions exit with status 0 after printing JSON; a block is represented by JSON, not process failure.

- dependencies_and_callers:
  - Called by hook registry `hooks/hooks.json:4-10`.
  - Uses `hooks/lib/loop-common.sh` for:
    - field constants at `hooks/lib/loop-common.sh:15-24`;
    - `find_active_loop` at `hooks/lib/loop-common.sh:63-81`;
    - `parse_state_file` at `hooks/lib/loop-common.sh:112-139`;
    - template directory initialization through `hooks/lib/loop-common.sh:46-55`.
  - Uses `hooks/lib/template-loader.sh` indirectly for `load_and_render_safe`; loader behavior is defined at `hooks/lib/template-loader.sh:170-203`.
  - Uses `scripts/portable-timeout.sh`; timeout backend detection prefers `gtimeout`, GNU `timeout`, then Python, then no timeout at `scripts/portable-timeout.sh:9-29`, and `run_with_timeout` maps timeout expiration to `124` when using Python at `scripts/portable-timeout.sh:31-71`.
  - State fields are generated by `scripts/setup-rlcr-loop.sh:485-498`, including `plan_file`, `plan_tracked`, and `start_branch`.
  - Related stop-hook schema and plan checks exist in `hooks/loop-codex-stop-hook.sh`; the stop hook also parses quoted fields and blocks outdated schema before final review, but the assigned file specifically owns prompt-submit plan/branch gating.

- edge_cases_or_failure_modes:
  - No active loop: allowed silently, so normal non-RLCR usage is not disrupted.
  - Finalize Phase: validates `finalize-state.md` when present, preventing bypass after Codex has already returned `COMPLETE`.
  - Missing `plan_tracked` or `start_branch`: blocks with schema-outdated guidance instead of silently allowing older state files.
  - Quoted YAML values: `parse_state_file` strips quotes from `start_branch` and `plan_file`, covering legacy or YAML-quoted states.
  - Git branch lookup failure or timeout: blocks with “Cannot verify branch consistency”.
  - Git status/ls-files timeout: blocks with a timeout-specific message.
  - Git unexpected exit: blocks with exit-code-specific message.
  - `plan_tracked` values other than exact string `true` fall into the untracked-plan branch; there is no explicit boolean validation for malformed values such as `yes`.
  - `FULL_PLAN_PATH` is computed but unused, so this hook does not validate that an untracked/gitignored plan file physically exists; it only validates git tracking mode.
  - For tracked plans, this hook checks uncommitted modifications but does not compare plan content against the loop backup. A separate stop-hook test covers committed tracked-plan divergence around `tests/test-plan-file-hooks.sh:655-720`, implying that deeper content integrity is enforced elsewhere, not here.
  - If no timeout implementation is available, `portable-timeout.sh` runs commands without timeout and warns to stderr at `scripts/portable-timeout.sh:64-68`; that weakens the intended bounded git behavior.

- validation_or_tests:
  - Direct hook tests are in `tests/test-plan-file-hooks.sh`.
  - Valid state passes with no output at `tests/test-plan-file-hooks.sh:91-104`.
  - YAML-quoted `plan_file` parsing is expected to pass at `tests/test-plan-file-hooks.sh:106-119`.
  - Missing `plan_tracked` blocks at `tests/test-plan-file-hooks.sh:121-139`.
  - Missing `start_branch` blocks at `tests/test-plan-file-hooks.sh:141-159`.
  - Branch change blocks at `tests/test-plan-file-hooks.sh:164-185`.
  - Quoted `start_branch` passes when matching at `tests/test-plan-file-hooks.sh:341-363`.
  - Quoted mismatched `start_branch` blocks at `tests/test-plan-file-hooks.sh:365-386`.
  - Stop-hook schema JSON behavior for old state is tested at `tests/test-plan-file-hooks.sh:631-653`.
  - Template reference integrity checks look for missing templates across hook calls in `tests/test-template-references.sh:83-111`.

- skip_candidate: `no`

### FIX_HUMANIZE_ESCAPE-HZ-049 `file` `prompt-template/block/git-not-clean-humanize-local.md`
- cursor: `[_]`
- core_role:
  - Prompt/block fragment used by the RLCR stop hook when git is dirty because untracked `.humanize*` local loop directories are present.
  - It is a supporting transition message for the “git not clean” stop gate, not a standalone validator. It affects operator/agent remediation by instructing that `.humanize/` should not be committed and should be ignored.

- algorithmic_behavior:
  - File content is a short markdown note at `prompt-template/block/git-not-clean-humanize-local.md:2-8`.
  - It declares a special case: `.humanize/` is created by `humanize:start-rlcr-loop` and “should NOT be committed” at `prompt-template/block/git-not-clean-humanize-local.md:2-3`.
  - It prescribes adding `.humanize*` to `.gitignore` and staging `.gitignore` at `prompt-template/block/git-not-clean-humanize-local.md:4-8`.
  - The stop hook injects this note only when git status has untracked paths matching `.humanize`; see `hooks/loop-codex-stop-hook.sh:438-448`.
  - The note is concatenated into `SPECIAL_NOTES`, then rendered into the broader `block/git-not-clean.md` template through `{{SPECIAL_NOTES}}` at `hooks/loop-codex-stop-hook.sh:461-472`.
  - If this template is missing or empty, the stop hook falls back to `Note: .humanize* directories are intentionally untracked.` at `hooks/loop-codex-stop-hook.sh:443-446`.

- inputs_outputs_state:
  - Inputs:
    - Git porcelain status captured earlier by the stop hook.
    - Untracked file subset extracted with `grep '^??'` at `hooks/loop-codex-stop-hook.sh:438-440`.
    - Pattern check for `.humanize` in untracked entries at `hooks/loop-codex-stop-hook.sh:441-442`.
  - Outputs:
    - Markdown remediation note appended to the dirty-git block reason.
    - No direct JSON output from this template; JSON is emitted by the caller in `hooks/loop-codex-stop-hook.sh:474-481`.
  - State transitions:
    - Does not mutate state by itself.
    - Guides the user/agent toward changing `.gitignore` so future stop attempts are not blocked by local `.humanize*` artifacts.
    - Keeps `.humanize*` out of commits, preserving local RLCR runtime state as non-source-control state.

- gates_or_invariants:
  - `.humanize/` and legacy `.humanize-*` runtime directories are considered local loop artifacts and should not be committed.
  - Dirty git remains a hard stop-hook block until changes are committed or ignored; this note modifies the remediation text, not the gate result.
  - The suggested ignore pattern is `.humanize*`, broader than only `.humanize/`, matching the caller’s comment that it includes `.humanize/` and legacy `.humanize-*` dirs at `hooks/loop-codex-stop-hook.sh:441`.

- dependencies_and_callers:
  - Caller: `hooks/loop-codex-stop-hook.sh:443`.
  - Parent block template: `prompt-template/block/git-not-clean.md`, where `{{SPECIAL_NOTES}}` is inserted at line 4 and commit guidance follows at `prompt-template/block/git-not-clean.md:5-16`.
  - Template loading dependency: `load_template` from `hooks/lib/template-loader.sh:36-48`; unlike many block templates, this note is loaded raw, not rendered with variables.
  - Template reference coverage: `tests/test-template-references.sh:83-111` scans hook `load_template` and `load_and_render*` calls and fails on missing referenced templates.

- edge_cases_or_failure_modes:
  - The stop-hook detection uses `grep -q '\.humanize'`, so any untracked path containing `.humanize` triggers the note, not only root `.humanize/`.
  - The note instructs `echo '.humanize*' >> .gitignore`; repeated remediation may append duplicate ignore lines unless the agent checks first.
  - If `.gitignore` itself becomes modified, the broader dirty-git gate still blocks until `.gitignore` is staged and committed.
  - If `.humanize*` is already tracked, this note is insufficient; it handles untracked detection, not tracked artifact removal.
  - The template has no variables, so rendering errors are unlikely; missing file falls back to a shorter note but omits the exact `.gitignore` commands.

- validation_or_tests:
  - Indirectly covered by template reference validation in `tests/test-template-references.sh:83-111`, which confirms referenced templates exist.
  - Stop-hook git cleanliness logic loading this template is in `hooks/loop-codex-stop-hook.sh:430-483`.
  - Several tests create `.gitignore` containing `.humanize*` as expected setup, for example `tests/test-plan-file-hooks.sh:748`, `tests/test-plan-file-hooks.sh:819`, and `tests/test-plan-file-hooks.sh:888`, showing the repository’s intended local-artifact policy.
  - No focused assertion was found that validates the exact rendered text of this specific template; coverage is mainly reference existence and caller behavior.

- skip_candidate: `yes: this file is a small remediation-message fragment rather than core algorithm code, but it is still part of the stop-gate contract for dirty `.humanize*` local state.`

### FIX_HUMANIZE_ESCAPE-HZ-079 `file` `prompt-template/codex/full-alignment-review.md`
- cursor: `[_]`
- core_role:
  - Full Alignment Check prompt template for Codex review rounds in the RLCR loop.
  - Defines the review contract that decides whether the loop continues, enters Finalize Phase via `COMPLETE`, or triggers the stagnation circuit breaker via `STOP`.
  - It is algorithmic as a state-transition prompt: the stop hook creates this prompt every fifth review round and later parses Codex’s last non-empty line for `COMPLETE` or `STOP`.

- algorithmic_behavior:
  - Header parameterizes the round number with `{{CURRENT_ROUND}}` at `prompt-template/codex/full-alignment-review.md:1`.
  - Forces the reviewer to read the original implementation plan via `@{{PLAN_FILE}}` before review at `prompt-template/codex/full-alignment-review.md:5-10`.
  - Embeds Claude’s round summary between stable comment markers at `prompt-template/codex/full-alignment-review.md:13-17`.
  - Part 1 mandates goal tracker audit:
    - read `@{{GOAL_TRACKER_FILE}}` at `prompt-template/codex/full-alignment-review.md:19-22`;
    - evaluate every acceptance criterion using MET / PARTIAL / NOT MET / DEFERRED at `prompt-template/codex/full-alignment-review.md:23-29`;
    - compare original plan against tracked Active / Completed / Deferred work to find forgotten items at `prompt-template/codex/full-alignment-review.md:30-35`;
    - audit deferred items for validity and contradictions at `prompt-template/codex/full-alignment-review.md:36-40`;
    - produce completion counts and blocker summary at `prompt-template/codex/full-alignment-review.md:42-48`.
  - Part 2 requires a critical implementation review and reality check against design docs at `@{{DOCS_PATH}}`; see `prompt-template/codex/full-alignment-review.md:50-55`.
  - Part 3 injects `{{GOAL_TRACKER_UPDATE_SECTION}}` at `prompt-template/codex/full-alignment-review.md:57`, which is rendered separately from `prompt-template/codex/goal-tracker-update-section.md`.
  - Part 4 adds the full-alignment-only stagnation audit:
    - states completed iteration count and current round at `prompt-template/codex/full-alignment-review.md:59-62`;
    - points Codex to historical prompt, summary, review prompt, and review result files under `.humanize/rlcr/{{LOOP_TIMESTAMP}}/` at `prompt-template/codex/full-alignment-review.md:63-73`;
    - requires review of the last five rounds at `prompt-template/codex/full-alignment-review.md:74`;
    - lists stagnation signals at `prompt-template/codex/full-alignment-review.md:76-83`;
    - instructs `STOP` as the final line when stagnation is detected at `prompt-template/codex/full-alignment-review.md:84`.
  - Part 5 defines output conditions:
    - write findings to `@{{REVIEW_RESULT_FILE}}` if issues or unmet ACs exist at `prompt-template/codex/full-alignment-review.md:86-89`;
    - use `STOP` as last line on stagnation at `prompt-template/codex/full-alignment-review.md:90`;
    - use `COMPLETE` only when all original plan tasks and ACs are fully met with no deferrals at `prompt-template/codex/full-alignment-review.md:91-93`.

- inputs_outputs_state:
  - Inputs supplied by the stop hook:
    - `CURRENT_ROUND`, `PLAN_FILE`, `SUMMARY_CONTENT`, `GOAL_TRACKER_FILE`, `DOCS_PATH`, `GOAL_TRACKER_UPDATE_SECTION`, `COMPLETED_ITERATIONS`, `LOOP_TIMESTAMP`, `PREV_ROUND`, `PREV_PREV_ROUND`, and `REVIEW_RESULT_FILE`; see `hooks/loop-codex-stop-hook.sh:720-731`.
  - Trigger state:
    - `FULL_ALIGNMENT_CHECK=true` when `CURRENT_ROUND % 5 == 4`, so rounds 4, 9, 14, etc.; see `hooks/loop-codex-stop-hook.sh:683-687`.
  - Outputs:
    - Rendered prompt written to `$LOOP_DIR/round-${CURRENT_ROUND}-review-prompt.md` at `hooks/loop-codex-stop-hook.sh:671-673` and `hooks/loop-codex-stop-hook.sh:718-731`.
    - Codex is expected to write review output to `$LOOP_DIR/round-${CURRENT_ROUND}-review-result.md`.
    - Last-line markers become state-machine inputs:
      - `COMPLETE` causes Finalize Phase entry unless max iterations blocks it; parsing starts at `hooks/loop-codex-stop-hook.sh:955-963`.
      - `STOP` ends the loop with stop state at `hooks/loop-codex-stop-hook.sh:1023-1049`.
  - State transitions:
    - No direct file mutation by the template itself.
    - Through the rendered prompt, Codex may update goal tracker content per the injected update section.
    - Through final markers, it controls loop continuation, finalization, or circuit-breaker termination.

- gates_or_invariants:
  - Original plan must be read first and remains the source of truth for scope.
  - Every acceptance criterion must be audited explicitly during full alignment.
  - Deferred work is incomplete for `COMPLETE`; this is stricter than a “validly deferred” completion model.
  - `COMPLETE` is valid only if all original plan tasks are done, all ACs are met, and no deferrals remain.
  - `STOP` is the explicit stagnation/circuit-breaker marker for repeated failures or lack of progress.
  - Marker parsing in the caller is strict: the last non-empty line is trimmed and must equal `COMPLETE` or `STOP`; comments in the stop hook note this avoids false positives such as “CANNOT COMPLETE” at `hooks/loop-codex-stop-hook.sh:955-960`.
  - Full alignment cadence is deterministic: every fifth round by zero-based round number modulo 5.

- dependencies_and_callers:
  - Caller: `hooks/loop-codex-stop-hook.sh:718-731`.
  - Full-alignment cadence and variable derivation are in `hooks/loop-codex-stop-hook.sh:683-693`.
  - Uses the shared goal tracker update section rendered at `hooks/loop-codex-stop-hook.sh:677-681`; that section says Codex must evaluate and, if approved, update `@{{GOAL_TRACKER_FILE}}` while never modifying immutable goal/AC sections at `prompt-template/codex/goal-tracker-update-section.md:1-17`.
  - Sibling regular-review template has similar completion strictness but lacks the five-round stagnation audit; compare `prompt-template/codex/regular-review.md:49-57`.
  - Template rendering uses `load_and_render_safe` from `hooks/lib/template-loader.sh:170-203`, with a fallback prompt defined in `hooks/loop-codex-stop-hook.sh:696-705`.
  - The stop hook validates Codex output file existence and non-emptiness before marker parsing at `hooks/loop-codex-stop-hook.sh:897-950`.

- edge_cases_or_failure_modes:
  - If the template is missing or renders empty, the stop hook uses a much shorter fallback at `hooks/loop-codex-stop-hook.sh:696-705`; that fallback lacks the detailed stagnation/history instructions, weakening the full-alignment circuit breaker.
  - The template refers to previous rounds using `PREV_ROUND` and `PREV_PREV_ROUND`; on the first full alignment round, these are positive, but if cadence changed, negative values could appear.
  - The instruction to review “last 5 rounds” depends on historical files existing and being readable under `.humanize/rlcr/{{LOOP_TIMESTAMP}}/`.
  - If Codex writes useful findings but omits a final marker, the stop hook treats it as ordinary review feedback and continues rather than finalizing/stopping.
  - If Codex writes `COMPLETE` despite deferred work, the caller cannot independently validate all ACs; the prompt is the primary contract preventing false completion.
  - If Codex writes `STOP` on a non-alignment round, the stop hook still honors it but logs that it is unusual; see `hooks/loop-codex-stop-hook.sh:1041-1043`.
  - The template states findings should be written when issues exist, but if no issues exist it implies `COMPLETE` final line; malformed output location is handled by the caller copying stdout if possible at `hooks/loop-codex-stop-hook.sh:897-913`.

- validation_or_tests:
  - Template reference existence is covered by `tests/test-template-references.sh:83-111`.
  - Goal tracker update section rendering is directly exercised in `tests/test-templates-comprehensive.sh:531-539`.
  - Finalize behavior driven by `COMPLETE` is covered by `tests/test-finalize-phase.sh`, including comments that `COMPLETE` triggers Finalize entry and related tests around `tests/test-finalize-phase.sh:443-475`.
  - Marker constants are defined centrally as `MARKER_COMPLETE` and `MARKER_STOP` in `hooks/lib/loop-common.sh:26-29`.
  - Stop-hook marker parsing and transition handling are in `hooks/loop-codex-stop-hook.sh:955-1049`.
  - No focused test was found that renders `full-alignment-review.md` and asserts the stagnation instructions or `STOP` wording specifically; coverage is mainly caller selection, marker handling, and template reference integrity.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `3 Item Evidence sections; each assigned item_id appears once as a section header`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`