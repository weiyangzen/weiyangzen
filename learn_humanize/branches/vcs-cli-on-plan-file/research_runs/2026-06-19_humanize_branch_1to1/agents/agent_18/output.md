# agent_18 vcs-cli-on-plan-file 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `4dd1ca2fece39d3c6d7f84965cd71bda02489397`

## Item Evidence

### VCS_CLI_ON_PLAN_FILE-HZ-018 `file` `hooks/loop-edit-validator.sh`
- cursor: `[_]`
- core_role:
  - `hooks/loop-edit-validator.sh` is the RLCR loop `PreToolUse` gate for Claude `Edit` tool calls. It protects generated/control files under `.humanize-loop.local` and enforces round-local edit routing before the edit reaches the filesystem.
  - It is registered as the `Edit` matcher in `hooks/hooks.json:24-30`, alongside sibling `Write`, `Read`, `Bash`, `UserPromptSubmit`, and `Stop` hooks. This makes it part of the hook/validator layer rather than the loop executor itself.
  - The file is core algorithm support for the RLCR state machine because it preserves ownership boundaries: Claude can edit allowed working files, but cannot mutate todos, prompts, hook-managed state, or post-round-0 goal tracking directly.

- algorithmic_behavior:
  - Initialization is strict shell mode via `set -euo pipefail` at `hooks/loop-edit-validator.sh:12`.
  - It resolves its own directory and sources shared RLCR helper functions from `hooks/lib/loop-common.sh` at `hooks/loop-edit-validator.sh:14-16`.
  - It reads the complete hook JSON payload from stdin into `HOOK_INPUT`, extracts `.tool_name` with `jq`, and exits successfully unless the event is exactly `Edit` at `hooks/loop-edit-validator.sh:22-27`.
  - For `Edit`, it extracts `.tool_input.file_path`, lowercases it, and applies path classifiers at `hooks/loop-edit-validator.sh:29-30`.
  - It first blocks any path ending in `round-<n>-todos.md` with a todos-specific message and exit code `2` at `hooks/loop-edit-validator.sh:36-39`. This is deliberately global, before the `.humanize-loop.local` containment check, so round-todos edits are blocked wherever the filename pattern appears.
  - It similarly blocks `round-<n>-prompt.md` edits at `hooks/loop-edit-validator.sh:41-44`, treating prompts as generated Codex-to-Claude input.
  - It then allows edits outside `.humanize-loop.local` at `hooks/loop-edit-validator.sh:50-52`. From that point on, the validator only governs loop-private files.
  - For loop-private paths, it finds the current project root from `CLAUDE_PROJECT_DIR` or `pwd`, derives `.humanize-loop.local`, and selects the newest active loop directory with `find_active_loop` at `hooks/loop-edit-validator.sh:58-60`.
  - If there is no active loop, edits are allowed at `hooks/loop-edit-validator.sh:62-64`; the hook avoids blocking stale/local files when the RLCR state machine is inactive.
  - It reads `current_round` from active `state.md` using `get_current_round` at `hooks/loop-edit-validator.sh:66`.
  - It blocks `state.md` edits at `hooks/loop-edit-validator.sh:72-75`, preserving hook-managed state transitions.
  - It blocks `goal-tracker.md` edits only after round 0 at `hooks/loop-edit-validator.sh:81-85`, redirecting the agent to write a goal tracker update request into the current round summary.
  - For `round-<n>-summary.md`, it extracts the loop-local filename, parses the embedded round number, and blocks edits when the requested summary round does not match the current active round at `hooks/loop-edit-validator.sh:91-115`.
  - The only successful terminal path is `exit 0` at `hooks/loop-edit-validator.sh:119`. Blocking terminal paths emit a rendered/fallback message to stderr and return exit code `2`, matching Claude Code hook blocking semantics.

- inputs_outputs_state:
  - Input: stdin JSON from Claude hook runtime. Required fields are `.tool_name` and `.tool_input.file_path`, read at `hooks/loop-edit-validator.sh:22-30`.
  - Input: environment variable `CLAUDE_PROJECT_DIR`, falling back to `pwd`, used to locate `.humanize-loop.local` at `hooks/loop-edit-validator.sh:58-59`.
  - Input: filesystem state under `.humanize-loop.local`, specifically the newest active loop directory and its `state.md`.
  - Input: shared template directory resolved by `hooks/lib/loop-common.sh:11-21`, used indirectly for block messages.
  - Output on allow: no stdout/stderr requirement and exit code `0`.
  - Output on block: human-readable error/remediation text to stderr and exit code `2`, for example todos/prompt/state/goal-tracker/wrong-round blocks at `hooks/loop-edit-validator.sh:36-44`, `72-85`, and `101-115`.
  - State read: current round is parsed from YAML-like frontmatter in `state.md` by `get_current_round` in `hooks/lib/loop-common.sh:86-98`.
  - State transition protected: the script itself does not mutate loop state. Its state-machine role is negative control: prevent Claude from bypassing the intended transitions by editing `state.md`, generated prompts/todos, previous/future summaries, or the locked goal tracker.

- gates_or_invariants:
  - Tool invariant: only exact `tool_name == "Edit"` is processed; all other tool names pass at `hooks/loop-edit-validator.sh:25-27`.
  - Round todos invariant: files matching `round-[0-9]+-todos.md` are not to be edited; `is_round_file_type` implements the regex at `hooks/lib/loop-common.sh:234-241`.
  - Prompt invariant: files matching `round-[0-9]+-prompt.md` are read-only generated prompt artifacts, blocked at `hooks/loop-edit-validator.sh:41-44`.
  - Loop-private containment invariant: most RLCR-specific restrictions apply only when the target path contains `.humanize-loop.local/`, checked by `is_in_humanize_loop_dir` at `hooks/lib/loop-common.sh:318-322`.
  - Active-loop invariant: only the newest timestamped loop directory with `state.md` is active. Older loop directories are ignored by `find_active_loop` at `hooks/lib/loop-common.sh:63-84`.
  - State ownership invariant: `state.md` is hook-managed and cannot be edited through Claude `Edit`, enforced at `hooks/loop-edit-validator.sh:72-75`.
  - Goal tracker ownership invariant: `goal-tracker.md` is editable in round 0 but blocked after current round becomes greater than 0, enforced at `hooks/loop-edit-validator.sh:81-85`.
  - Current-summary invariant: Claude may edit only the summary for the current round. Attempting to edit `round-N-summary.md` for a different round is blocked with a correction path at `hooks/loop-edit-validator.sh:91-115`.
  - Message safety invariant: common block messages use `load_and_render_safe` fallbacks in `hooks/lib/loop-common.sh:255-281` and `349-360`; the edit validator’s wrong-round branch also uses `load_and_render_safe` at `hooks/loop-edit-validator.sh:108-113`.

- dependencies_and_callers:
  - Caller/registration: `hooks/hooks.json:24-30` wires this script as a Claude `PreToolUse` command hook for `Edit`.
  - Shared shell library: `hooks/lib/loop-common.sh` supplies `to_lower`, `is_round_file_type`, `is_in_humanize_loop_dir`, `find_active_loop`, `get_current_round`, `is_state_file_path`, `is_goal_tracker_path`, `extract_round_number`, and block message functions.
  - Template loader dependency: `hooks/lib/loop-common.sh:11-16` sources `hooks/lib/template-loader.sh` and resolves `TEMPLATE_DIR`, enabling template-backed error messages with inline fallback behavior.
  - Template dependencies reached through shared functions include `prompt-template/block/todos-file-access.md`, `prompt-template/block/prompt-file-write.md`, `prompt-template/block/state-file-modification.md`, and `prompt-template/block/goal-tracker-modification.md`; these are enumerated as common templates in `tests/test-template-references.sh:153-160`.
  - Direct template dependency: `prompt-template/block/wrong-round-number.md` is rendered from the wrong-summary-round gate at `hooks/loop-edit-validator.sh:108`.
  - Sibling validators coordinate the broader hook surface: README lists `loop-write-validator.sh`, `loop-edit-validator.sh`, `loop-read-validator.sh`, and `loop-bash-validator.sh` as lifecycle hooks at `README.md:265-274`.
  - The plan-file branch context is related but separate: README states plan content changes are handled before prompt processing by `UserPromptSubmit`, not this edit validator, at `README.md:211-235`.

- edge_cases_or_failure_modes:
  - Missing or invalid `jq` is a hard runtime dependency. Because of `set -e`, failed `jq` parsing exits nonzero without a custom block message.
  - Empty or missing `.tool_input.file_path` becomes an empty path. It does not match the blocked patterns or `.humanize-loop.local`, so the edit is allowed.
  - The script only handles exact `Edit`; if a runtime emits a different edit-capable tool name such as `MultiEdit`, this script exits `0` at `hooks/loop-edit-validator.sh:25-27`. No `MultiEdit` matcher appears in `hooks/hooks.json`.
  - Todos/prompt filename blocking is broad because it runs before the `.humanize-loop.local` check. Any path ending with the round file pattern is blocked, even outside the loop directory.
  - `.humanize-loop.local` matching is substring-based and slash-sensitive (`grep '\.humanize-loop\.local/'`), so unusual path forms without the trailing slash segment may not be treated as loop-private.
  - `find_active_loop` only considers the newest timestamp-named subdirectory. If an older directory has active `state.md` but a newer directory lacks it, this validator treats the loop as inactive and allows loop-private edits, per `hooks/lib/loop-common.sh:63-84`.
  - `CURRENT_ROUND` is assumed numeric for `[[ "$CURRENT_ROUND" -gt 0 ]]` at `hooks/loop-edit-validator.sh:81`; malformed `current_round` in `state.md` can produce a shell integer-expression failure under strict mode.
  - Summary filename extraction assumes paths containing `.humanize-loop.local/<loop>/...` or `.humanize-loop.local/...` at `hooks/loop-edit-validator.sh:93-96`. If extraction fails, wrong-round validation is skipped and the edit is allowed.
  - Lowercasing makes pattern matching case-insensitive for filenames, but the correction path preserves the active loop directory’s original path casing.

- validation_or_tests:
  - Hook registration is directly inspectable in `hooks/hooks.json:24-30`.
  - `tests/test-template-references.sh:57-65` includes `hooks/loop-edit-validator.sh` in the scripts scanned for template references.
  - `tests/test-template-references.sh:153-160` checks the common block templates used by this validator through `loop-common.sh`.
  - `tests/test-template-references.sh:177-201` treats `loop-edit-validator.sh` as a critical validator and verifies it does not use unsafe non-fallback `load_and_render` calls.
  - I did not find a dedicated behavioral test that feeds hook JSON into `loop-edit-validator.sh` and asserts allow/block exit codes for todos, prompts, state files, goal tracker, or wrong-round summaries. Existing coverage appears structural/template-oriented for this file.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 1 item evidence section present
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`