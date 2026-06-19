# agent_052 use-realpath4everything 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`

## Item Evidence

### USE_REALPATH4EVERYTHING-HZ-052 `file` `scripts/cancel-rlcr-loop.sh`
- cursor: `[_]`
- core_role:
  - `scripts/cancel-rlcr-loop.sh` is the authoritative runtime cancellation entrypoint for an active RLCR loop. It is invoked by the slash command wrapper in `commands/cancel-rlcr-loop.md:11-33` and skill docs in `skills/humanize/SKILL.md:89-95` and `skills/humanize-rlcr/SKILL.md:109-113`.
  - Its core state transition is active loop state -> cancelled loop state: it creates `.cancel-requested`, removes setup/analysis transient markers, and renames the active state file to `cancel-state.md` (`scripts/cancel-rlcr-loop.sh:156-166`).
  - It is a core workflow script, not a skip candidate, because it changes the lifecycle state that hooks and validators use to determine whether an RLCR loop is active.

- algorithmic_behavior:
  - Argument parsing is intentionally narrow. It accepts `--force`, `-h`, and `--help`; any unknown option writes an error and exits `3` (`scripts/cancel-rlcr-loop.sh:24-63`).
  - The script discovers its plugin-relative dependency path with `SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"`, then sources `../hooks/lib/loop-common.sh` (`scripts/cancel-rlcr-loop.sh:69-71`).
  - Project root resolution is delegated to `resolve_project_root`, then the script targets `$PROJECT_ROOT/.humanize/rlcr` as the loop base (`scripts/cancel-rlcr-loop.sh:73-79`). The shared resolver prefers `CLAUDE_PROJECT_DIR`, falls back to `git rev-parse --show-toplevel`, and canonicalizes through `realpath`/fallback logic (`hooks/lib/project-root.sh:41-53`).
  - Cancellation is global by design. The script explicitly avoids `session_id` filtering because the standalone slash-command path does not receive hook JSON session metadata (`scripts/cancel-rlcr-loop.sh:80-91`).
  - Active loop discovery calls `find_active_loop "$LOOP_BASE_DIR"` with no filter (`scripts/cancel-rlcr-loop.sh:90-91`). In the unfiltered case, `find_active_loop` checks only the newest loop directory and returns it only if it has an active state file, preventing older stale loops from being revived (`hooks/lib/loop-common.sh:308-356`).
  - Active state selection in this script checks, in order, `state.md`, `methodology-analysis-state.md`, then `finalize-state.md` (`scripts/cancel-rlcr-loop.sh:103-121`). The shared resolver’s active-state order is methodology-analysis, finalize, then state (`hooks/lib/loop-common.sh:264-280`), but valid loop directories should normally contain a single active state file.
  - It extracts `current_round` and `max_iterations` with anchored `grep` plus `sed`, strips spaces, and defaults missing values to `?` (`scripts/cancel-rlcr-loop.sh:127-133`).
  - Finalize phase has an explicit confirmation gate. Without `--force`, a loop with `finalize-state.md` returns `FINALIZE_NEEDS_CONFIRM`, emits loop/round metadata, and exits `2` (`scripts/cancel-rlcr-loop.sh:139-149`). The command wrapper maps that marker to an `AskUserQuestion` flow before rerunning with `--force` (`commands/cancel-rlcr-loop.md:17-33`).
  - On permitted cancellation, the script creates `.cancel-requested`, removes `.humanize/.pending-session-id`, removes `.methodology-exit-reason`, moves the active state file to `cancel-state.md`, and prints a state-specific marker: `CANCELLED`, `CANCELLED_METHODOLOGY_ANALYSIS`, or `CANCELLED_FINALIZE` (`scripts/cancel-rlcr-loop.sh:156-184`).

- inputs_outputs_state:
  - Inputs:
    - CLI args: no args for normal cancellation, `--force` to cancel during Finalize Phase, `-h/--help` for usage (`scripts/cancel-rlcr-loop.sh:26-56`).
    - Environment/runtime root: `CLAUDE_PROJECT_DIR` or current git toplevel via `resolve_project_root`; lack of both is a hard script error (`scripts/cancel-rlcr-loop.sh:73-77`, `hooks/lib/project-root.sh:41-53`).
    - Filesystem state under `.humanize/rlcr/<timestamp>/`: one of `state.md`, `methodology-analysis-state.md`, or `finalize-state.md` (`scripts/cancel-rlcr-loop.sh:103-121`).
    - Optional metadata fields inside the active state file: `current_round:` and `max_iterations:` (`scripts/cancel-rlcr-loop.sh:127-133`).
  - Outputs:
    - Exit `0` on successful cancellation (`scripts/cancel-rlcr-loop.sh:186`).
    - Exit `1` with `NO_LOOP` if no active loop directory is found (`scripts/cancel-rlcr-loop.sh:93-97`).
    - Exit `1` with `NO_ACTIVE_LOOP` if a loop directory exists but none of the recognized active state files exists (`scripts/cancel-rlcr-loop.sh:117-120`).
    - Exit `2` with `FINALIZE_NEEDS_CONFIRM` when Finalize Phase is active and `--force` was not provided (`scripts/cancel-rlcr-loop.sh:139-149`).
    - Exit `3` for root-resolution or argument errors (`scripts/cancel-rlcr-loop.sh:57-61`, `scripts/cancel-rlcr-loop.sh:73-77`).
  - State transitions:
    - Creates `$LOOP_DIR/.cancel-requested` before moving the state file (`scripts/cancel-rlcr-loop.sh:156-157`).
    - Deletes `$PROJECT_ROOT/.humanize/.pending-session-id`, which can remain if setup had not completed (`scripts/cancel-rlcr-loop.sh:159-160`).
    - Deletes `$LOOP_DIR/.methodology-exit-reason`, preventing a stale methodology-analysis exit marker from driving terminal-state logic later (`scripts/cancel-rlcr-loop.sh:162-163`; related methodology marker handling appears in `hooks/lib/methodology-analysis.sh:69-171`).
    - Renames the active state file to `$LOOP_DIR/cancel-state.md` (`scripts/cancel-rlcr-loop.sh:165-166`). Tests confirm `cancel-state.md` is terminal, not active (`tests/test-state-exit-naming.sh:97-112`).

- gates_or_invariants:
  - Active-loop invariant: cancellation only acts on the newest active loop directory returned by unfiltered `find_active_loop`; if the newest directory is terminal, older active-looking directories are intentionally ignored for zombie-loop protection (`hooks/lib/loop-common.sh:342-356`, tested in `tests/test-session-id.sh:386-429`).
  - Session invariant: cancel is deliberately not session-scoped. `scripts/cancel-rlcr-loop.sh:80-91` records the product decision, and `tests/test-session-id.sh:348-383` verifies cancellation succeeds despite a stored `session_id`.
  - Finalize safety gate: `finalize-state.md` cannot be cancelled by the normal command without a separate `--force` invocation (`scripts/cancel-rlcr-loop.sh:139-149`, `commands/cancel-rlcr-loop.md:24-35`).
  - Hook protection handshake: `.cancel-requested` is the authorization signal that lets the Bash validator allow the otherwise-protected state-file `mv` (`scripts/cancel-rlcr-loop.sh:156-166`; validator exception in `hooks/loop-bash-validator.sh:253-279`).
  - Cancel `mv` authorization is strict in shared logic. `is_cancel_authorized` requires the signal file, rejects command substitution, backticks, newlines, shell chaining, leftover `$` variables, mixed quote styles, extra args, non-expected source/dest paths, and symlinked source files (`hooks/lib/loop-common.sh:1033-1249`).
  - Realpath/canonicalization is part of the invariant in this branch. Project roots are canonicalized (`hooks/lib/project-root.sh:14-20`, `hooks/lib/project-root.sh:41-53`), and cancel authorization canonicalizes the loop dir plus user-supplied source/destination prefixes to avoid false mismatches through symlinked prefixes while still rejecting symlink leaf attacks (`hooks/lib/loop-common.sh:1082-1096`, `hooks/lib/loop-common.sh:1191-1229`).

- dependencies_and_callers:
  - Direct dependency: `hooks/lib/loop-common.sh`, sourced at `scripts/cancel-rlcr-loop.sh:69-71`.
  - Transitive dependency: `hooks/lib/project-root.sh`, sourced by `loop-common.sh` (`hooks/lib/loop-common.sh:171-178`) and providing `resolve_project_root` plus canonicalization helpers (`hooks/lib/project-root.sh:41-90`).
  - Active loop dependency: `find_active_loop` and `resolve_active_state_file` in `hooks/lib/loop-common.sh` (`hooks/lib/loop-common.sh:264-280`, `hooks/lib/loop-common.sh:308-356`).
  - Validator dependency: `hooks/loop-bash-validator.sh` allows `cancel-rlcr-loop.sh` as a leading command during methodology analysis (`hooks/loop-bash-validator.sh:81-87`) and allows protected state-file moves only through `is_cancel_authorized` (`hooks/loop-bash-validator.sh:253-279`).
  - User-facing caller: `commands/cancel-rlcr-loop.md` runs the script, interprets first-line markers, and prompts for Finalize Phase confirmation (`commands/cancel-rlcr-loop.md:11-37`).
  - Documentation/skill callers: `skills/humanize/SKILL.md:89-95`, `skills/humanize-rlcr/SKILL.md:109-113`, and `docs/usage.md:63` expose the cancellation command.

- edge_cases_or_failure_modes:
  - No project root: if neither `CLAUDE_PROJECT_DIR` nor a git root exists, the script prints an error and exits `3` (`scripts/cancel-rlcr-loop.sh:73-77`).
  - No `.humanize/rlcr` or no active newest loop: emits `NO_LOOP` and exits `1` (`scripts/cancel-rlcr-loop.sh:90-97`).
  - Loop directory exists but recognized active state file is absent: emits `NO_ACTIVE_LOOP` and exits `1` (`scripts/cancel-rlcr-loop.sh:108-121`).
  - Missing round fields: output still succeeds but reports `?` for missing `current_round` or `max_iterations` (`scripts/cancel-rlcr-loop.sh:127-133`).
  - Finalize without `--force`: non-destructive exit `2`; wrapper must prompt before force-cancelling (`scripts/cancel-rlcr-loop.sh:139-149`, `commands/cancel-rlcr-loop.md:24-35`).
  - Multiple active state files in one loop directory: this script chooses `state.md` before methodology/finalize (`scripts/cancel-rlcr-loop.sh:108-116`), while `resolve_active_state_file` prefers methodology/finalize before normal state (`hooks/lib/loop-common.sh:268-280`). That mismatch is only relevant in corrupted state with multiple active files.
  - Existing `cancel-state.md`: `mv "$ACTIVE_STATE_FILE" "$LOOP_DIR/cancel-state.md"` will overwrite the destination on typical Unix `mv` behavior without a prompt in non-interactive mode (`scripts/cancel-rlcr-loop.sh:165-166`); the script does not add a destination-exists guard.
  - Symlink/security attacks are primarily covered in the Bash validator authorization path, not inside `cancel-rlcr-loop.sh` itself. If the script is executed outside the hook validator, it relies on normal shell quoting and direct variable construction, but does not perform the same leaf-symlink rejection before `mv`.

- validation_or_tests:
  - `tests/test-session-id.sh:348-383` verifies the cancel script ignores stored `session_id` and renames `state.md` to `cancel-state.md`.
  - `tests/test-session-id.sh:386-429` verifies zombie-loop protection: when the newest loop directory is completed, cancel reports `NO_LOOP` instead of reviving an older active-looking loop.
  - `tests/test-session-id.sh:748-785` verifies a newest `cancel-state.md` prevents stale revival in session-filtered active-loop lookup.
  - `tests/test-state-exit-naming.sh:97-112` verifies `cancel-state.md` is not detected as an active loop.
  - `tests/test-cancel-signal-file.sh:1-10` defines the cancel-signal test purpose; `tests/test-cancel-signal-file.sh:80-115` covers authorized `mv` with `.cancel-requested`, and `tests/test-cancel-signal-file.sh:117-130` begins the negative case for missing signal.
  - `tests/robustness/test-cancel-security-robustness.sh` is a broader security/robustness suite around cancel authorization patterns, including quoted paths, command substitution, shell chaining, extra args, symlink cases, and finalize/methodology state variants.
  - No tests were run in this research pass; evidence is from direct source/test inspection in the read-only branch export.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `1`
- missing_items: `0`
- duplicate_items: `0`
- final_worker_status: `complete`