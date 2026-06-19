# agent_21 vcs-cli-on-plan-file 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `4dd1ca2fece39d3c6d7f84965cd71bda02489397`

## Item Evidence

### VCS_CLI_ON_PLAN_FILE-HZ-021 `file` `hooks/loop-write-validator.sh`
- cursor: `[_]`
- core_role:
  - `hooks/loop-write-validator.sh` is the Claude Code `PreToolUse` gate for the `Write` tool in the RLCR loop. It protects loop-managed control files from direct or misdirected writes while still allowing normal repository writes.
  - It is registered in `hooks/hooks.json:14-23` under `PreToolUse` with matcher `Write`, pointing to `${CLAUDE_PLUGIN_ROOT}/hooks/loop-write-validator.sh`.
  - Within the RLCR state machine, this validator enforces that Claude writes only the current round summary at the active loop path, initializes `goal-tracker.md` only in Round 0, never writes prompts/todos/state, and does not spoof or advance round files manually.

- algorithmic_behavior:
  - Reads the hook payload from stdin into `HOOK_INPUT` and extracts `.tool_name` and `.tool_input.file_path` with `jq` (`hooks/loop-write-validator.sh:23-31`).
  - If the incoming tool is not `Write`, exits successfully with no checks (`hooks/loop-write-validator.sh:26-28`).
  - Lowercases the requested file path for pattern classification, then blocks writes to any `round-N-todos.md` and `round-N-prompt.md` path by emitting shared block messages and exiting `2` (`hooks/loop-write-validator.sh:37-45`).
  - Determines whether the target is a `round-N-summary.md` file and whether the path contains `.humanize-loop.local/` (`hooks/loop-write-validator.sh:51-52`).
  - Allows ordinary writes immediately when the path is neither a summary file nor inside `.humanize-loop.local/` (`hooks/loop-write-validator.sh:54-57`).
  - Allows miscellaneous files under `.humanize-loop.local/` when they are not summaries, not `state.md`, and not `goal-tracker.md` (`hooks/loop-write-validator.sh:59-65`).
  - Locates the active loop via `CLAUDE_PROJECT_DIR` or `pwd`, then `.humanize-loop.local`, then `find_active_loop` (`hooks/loop-write-validator.sh:71-79`). `find_active_loop` selects only the newest timestamped loop directory and requires its `state.md` to exist (`hooks/lib/loop-common.sh:63-84`).
  - If no active loop exists, exits `0`; this keeps the hook non-invasive outside a running RLCR session (`hooks/loop-write-validator.sh:75-77`).
  - Reads `current_round` from YAML frontmatter in the active loop `state.md`, defaulting to `0` if missing (`hooks/loop-write-validator.sh:79`, `hooks/lib/loop-common.sh:86-98`).
  - Blocks direct `state.md` writes after active-loop discovery (`hooks/loop-write-validator.sh:85-88`).
  - Blocks `goal-tracker.md` writes when `CURRENT_ROUND > 0`; the user-facing remediation tells Claude to request changes through the current round summary (`hooks/loop-write-validator.sh:94-98`, `hooks/lib/loop-common.sh:349-361`).
  - Blocks summary writes outside `.humanize-loop.local/` and renders the correct active path (`hooks/loop-write-validator.sh:104-112`).
  - Extracts the target filename relative to `.humanize-loop.local/<timestamp>/` or `.humanize-loop.local/` using `sed` (`hooks/loop-write-validator.sh:118-124`).
  - For summary files, extracts the requested round number and blocks if it differs from `CURRENT_ROUND`, rendering the correct current summary path (`hooks/loop-write-validator.sh:130-148`).
  - Validates that even a correctly named file is in the active loop directory by comparing the raw requested `FILE_PATH` to `$ACTIVE_LOOP_DIR/$CLAUDE_FILENAME`; mismatch exits `2` with a wrong-directory message (`hooks/loop-write-validator.sh:154-165`).
  - Successful validation exits `0` (`hooks/loop-write-validator.sh:167`).

- inputs_outputs_state:
  - Input: Claude Code hook JSON on stdin, specifically `tool_name` and `tool_input.file_path` (`hooks/loop-write-validator.sh:23-31`).
  - Input state: active loop directory under `${CLAUDE_PROJECT_DIR:-$(pwd)}/.humanize-loop.local` (`hooks/loop-write-validator.sh:71-73`).
  - Input state: active loop `state.md` frontmatter with `current_round`; setup initializes this to `0` when creating a loop (`scripts/setup-rlcr-loop.sh:326-340`).
  - Input state: loop artifacts created by setup include `goal-tracker.md`, `round-0-prompt.md`, and expected `round-0-summary.md` (`scripts/setup-rlcr-loop.sh:346-493`).
  - Output on allow: no stdout/stderr contract beyond exit status `0`.
  - Output on block: explanatory markdown goes to stderr and the hook exits `2`, which is the blocking signal used consistently by sibling validators.
  - State transitions: this file does not mutate repository or loop state. Its only transition is permit/block at hook time. It preserves the RLCR state machine by preventing unauthorized state mutations and forcing summary writes to the current round file.

- gates_or_invariants:
  - Tool gate: only validates `Write`; all other tool payloads exit `0` (`hooks/loop-write-validator.sh:26-28`).
  - Todo invariant: `round-*-todos.md` must not be created or written through file tools; users should use the native TodoWrite path instead (`hooks/loop-write-validator.sh:37-40`, `prompt-template/block/todos-file-access.md`).
  - Prompt invariant: `round-*-prompt.md` is read-only because it contains generated instructions for Claude (`hooks/loop-write-validator.sh:42-45`, `prompt-template/block/prompt-file-write.md`).
  - State invariant: `state.md` is managed by the loop system and direct writes are blocked once an active loop is found (`hooks/loop-write-validator.sh:85-88`, `prompt-template/block/state-file-modification.md`).
  - Goal tracker invariant: `goal-tracker.md` is directly writable only during Round 0; after that, changes must be requested in `round-CURRENT-summary.md` (`hooks/loop-write-validator.sh:94-98`, `prompt-template/block/goal-tracker-modification.md`).
  - Summary location invariant: summaries must be under the active `.humanize-loop.local/<timestamp>/` directory, not arbitrary project paths (`hooks/loop-write-validator.sh:104-112`, `prompt-template/block/wrong-summary-location.md:1-5`).
  - Summary round invariant: a summary write may only target the current round number; Claude must not increment or backdate round files (`hooks/loop-write-validator.sh:130-148`, `prompt-template/block/wrong-round-number.md:1-7`).
  - Active-loop invariant: even under `.humanize-loop.local`, the file must resolve to the newest active loop directory selected by `find_active_loop`, preventing writes to stale loop directories (`hooks/loop-write-validator.sh:154-165`, `hooks/lib/loop-common.sh:63-84`).
  - Template safety invariant: blocking messages use `load_and_render_safe` where the validator needs per-case templates, falling back to inline text if the template is missing (`hooks/loop-write-validator.sh:109-110`, `140-145`, `160-163`; `hooks/lib/template-loader.sh:152-180`).

- dependencies_and_callers:
  - Called by Claude Code through `hooks/hooks.json` as the `Write` `PreToolUse` hook (`hooks/hooks.json:14-23`).
  - Depends on Bash with `set -euo pipefail` (`hooks/loop-write-validator.sh:13`).
  - Depends on `jq` for parsing the hook JSON (`hooks/loop-write-validator.sh:24`, `30`).
  - Sources `hooks/lib/loop-common.sh` (`hooks/loop-write-validator.sh:15-17`), which in turn sources `hooks/lib/template-loader.sh` and initializes `TEMPLATE_DIR` (`hooks/lib/loop-common.sh:11-20`).
  - Uses shared classifiers/renderers from `loop-common.sh`: `to_lower`, `is_round_file_type`, `is_in_humanize_loop_dir`, `find_active_loop`, `get_current_round`, `is_state_file_path`, `is_goal_tracker_path`, `extract_round_number`, and shared block message functions (`hooks/lib/loop-common.sh:100-103`, `234-253`, `255-282`, `306-321`, `349-361`).
  - Coordinates with `hooks/loop-edit-validator.sh`, which applies similar protections for `Edit`, including prompt/todos/state/goal tracker and summary round checks (`hooks/loop-edit-validator.sh:22-119`).
  - Coordinates with `hooks/loop-read-validator.sh`, which prevents stale or wrong-location reads of prompt/summary files and blocks todos reads (`hooks/loop-read-validator.sh:22-135`).
  - Coordinates with `hooks/loop-bash-validator.sh`, which blocks shell-based modifications to state, goal tracker, prompt, summary, and todos files (`hooks/loop-bash-validator.sh:155-205`).
  - Relies on templates under `prompt-template/block/`, including `wrong-summary-location.md`, `wrong-round-number.md`, `wrong-directory-path.md`, and shared message templates for todos, prompt, state, and goal tracker blocks.

- edge_cases_or_failure_modes:
  - If `jq` is unavailable or the hook input is invalid JSON, `set -euo pipefail` makes the hook fail before graceful block/allow logic; there is no fallback parser.
  - If there is no active loop directory or the newest loop directory lacks `state.md`, the validator exits `0` for most loop-file cases after active-loop lookup (`hooks/loop-write-validator.sh:75-77`), intentionally avoiding false positives but allowing writes when loop state is absent or corrupted.
  - `get_current_round` defaults to `0` when the `current_round` field is missing or unreadable (`hooks/lib/loop-common.sh:91-98`), which may cause post-Round-0 state corruption to be treated as Round 0.
  - `[[ "$CURRENT_ROUND" -gt 0 ]]` assumes a numeric value (`hooks/loop-write-validator.sh:94`). A malformed `current_round` could cause a shell integer comparison error under `set -e`.
  - Path containment is regex/string based. `is_in_humanize_loop_dir` only checks for the substring `.humanize-loop.local/` (`hooks/lib/loop-common.sh:318-322`) and does not canonicalize symlinks or normalize `..`.
  - Final directory validation compares raw `FILE_PATH` to `CORRECT_PATH` (`hooks/loop-write-validator.sh:154-165`). Equivalent paths with relative segments, symlinks, or different absolute/relative spelling may be blocked even if they resolve to the same file.
  - The script lowercases only for type detection, then compares original paths for location. This permits case-insensitive filename detection but may behave differently on case-sensitive versus case-insensitive filesystems.
  - The filename extraction regex captures all remaining path under `.humanize-loop.local/<timestamp>/`; nested paths beneath a loop directory can be transformed into `$ACTIVE_LOOP_DIR/<nested>`, then blocked if not exactly in the active loop (`hooks/loop-write-validator.sh:118-124`, `154-165`).
  - `state.md` outside `.humanize-loop.local` is allowed unless it also falls into a guarded loop path, because ordinary non-loop non-summary writes exit early (`hooks/loop-write-validator.sh:54-57`).
  - `goal-tracker.md` writes inside `.humanize-loop.local` are allowed in Round 0, matching setup instructions that require Claude to initialize it in Round 0 (`scripts/setup-rlcr-loop.sh:445-455`, `488-493`).
  - Template loading failures are mitigated by inline fallback messages for this validator’s direct `load_and_render_safe` calls, and shared message functions also use safe rendering (`hooks/lib/loop-common.sh:257-282`, `349-361`).

- validation_or_tests:
  - `tests/test-template-references.sh` includes `hooks/loop-write-validator.sh` in the scripts scanned for template references (`tests/test-template-references.sh:56-64`) and checks critical validators use `load_and_render_safe` rather than unsafe template rendering (`tests/test-template-references.sh:173-201`).
  - `tests/test-template-references.sh` verifies common templates used by shared block-message functions exist, including todos, prompt-write, state-file, and goal-tracker templates (`tests/test-template-references.sh:150-168`).
  - `tests/test-templates-comprehensive.sh` has an integration rendering check for `block/wrong-round-number.md`, verifying the title, attempted round, current round, and correct path interpolate correctly (`tests/test-templates-comprehensive.sh:498-514`).
  - `tests/test-error-scenarios.sh` documents template-loader failure behavior and highlights that missing templates can otherwise produce empty feedback; this risk is reduced here by `load_and_render_safe` fallbacks (`tests/test-error-scenarios.sh:21-58`, `89-121`).
  - I found no dedicated executable behavioral test that feeds JSON into `hooks/loop-write-validator.sh` and asserts exit codes for allowed writes, todos/prompt blocks, wrong-round summary blocks, wrong-directory blocks, or post-Round-0 goal tracker blocks. Coverage appears mostly template existence/rendering plus sibling hook consistency.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 1 Item Evidence section present for the single assigned item
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`