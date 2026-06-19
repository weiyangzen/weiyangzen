# agent_146 use-realpath4everything 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`

## Item Evidence

### USE_REALPATH4EVERYTHING-HZ-146 `file` `prompt-template/block/wrong-directory-path.md`
- cursor: `[_]`
- core_role: This file is a reusable block-message template for the RLCR hook validators when a read or write targets a round/loop file through the wrong directory path. It is not the path-checking algorithm itself; it is the user-facing rejection contract emitted after the validators decide the path is outside the active loop’s expected location. The template title and placeholders are defined at `prompt-template/block/wrong-directory-path.md:1` and `prompt-template/block/wrong-directory-path.md:3-6`.

- algorithmic_behavior: The template renders three dynamic values: `ACTION`, `FILE_PATH`, and `CORRECT_PATH`. Its observable transition is from a validator-detected path mismatch into a blocking diagnostic: “trying to ACTION” for the attempted path, “Correct path” for the required path, and a command hint. The read validator reaches this block after computing `CORRECT_PATH="$ACTIVE_LOOP_DIR/$CLAUDE_FILENAME"` and comparing prefix-canonical forms at `hooks/loop-read-validator.sh:305-313`; on mismatch it renders `block/wrong-directory-path.md` with `ACTION=read` and exits `2` at `hooks/loop-read-validator.sh:314-321`. The write validator performs the same transition with `ACTION=write to` at `hooks/loop-write-validator.sh:332-351`.

- inputs_outputs_state: Inputs are supplied by hook validators, not by the template directly. `FILE_PATH` comes from hook JSON `tool_input.file_path` for Read/Write tools (`hooks/loop-read-validator.sh:41-47`, `hooks/loop-write-validator.sh:42-48`). `CORRECT_PATH` is derived from active loop state plus the target filename (`hooks/loop-read-validator.sh:197-216`, `hooks/loop-read-validator.sh:305`; `hooks/loop-write-validator.sh:167-184`, `hooks/loop-write-validator.sh:332`). Output is rendered text to stderr through `load_and_render_safe ... >&2`, followed by process exit code `2`, which marks the attempted tool use as blocked (`hooks/loop-read-validator.sh:317-321`, `hooks/loop-write-validator.sh:347-351`). The template itself has no persistent state and performs no mutation.

- gates_or_invariants: The governing invariant is that round/loop files must be accessed through the active loop directory path corresponding to the current session and filename. The branch’s realpath-related behavior is visible in the gate: validators compare `canonicalize_path_prefix "$FILE_PATH"` against `canonicalize_path_prefix "$CORRECT_PATH"` rather than raw strings (`hooks/loop-read-validator.sh:307-313`, `hooks/loop-write-validator.sh:334-343`). `canonicalize_path_prefix` resolves symlinks only in the parent directory and reattaches the original basename, explicitly avoiding leaf symlink dereference for authorization checks (`hooks/lib/project-root.sh:55-68`, `hooks/lib/project-root.sh:72-96`). This preserves equivalent parent paths such as macOS `/var` versus `/private/var` while still rejecting leaf symlink escapes.

- dependencies_and_callers: Direct callers are `hooks/loop-read-validator.sh` and `hooks/loop-write-validator.sh`, both via `load_and_render_safe "$TEMPLATE_DIR" "block/wrong-directory-path.md" ...`. `TEMPLATE_DIR` is initialized by `hooks/lib/loop-common.sh` from `get_template_dir` and validated with graceful fallback behavior (`hooks/lib/loop-common.sh:240-248`). Template loading and substitution are implemented in `hooks/lib/template-loader.sh`: placeholders use `{{VARIABLE_NAME}}`, missing variables are preserved, and substitution is single-pass to avoid placeholder injection (`hooks/lib/template-loader.sh:7-14`, `hooks/lib/template-loader.sh:48-56`, `hooks/lib/template-loader.sh:69-135`). If this template is missing or renders empty, `load_and_render_safe` emits the inline fallback supplied by the validator (`hooks/lib/template-loader.sh:185-210`).

- edge_cases_or_failure_modes: If `realpath` cannot canonicalize the parent path, `canonicalize_path_prefix` falls back to the original path, which should fail against the canonical expected path rather than approving an ambiguous path (`hooks/lib/project-root.sh:66-68`, `hooks/lib/project-root.sh:82-95`). Empty path input prints nothing and returns success from the helper (`hooks/lib/project-root.sh:70-76`), but the validators require `tool_input.file_path` before reaching the template (`hooks/loop-read-validator.sh:41-44`, `hooks/loop-write-validator.sh:42-45`). A notable template-level edge case is the command hint at `prompt-template/block/wrong-directory-path.md:6`: it says `cat {{FILE_PATH}}`, even though the rejection says the correct path is `{{CORRECT_PATH}}`. For a wrong-directory block, that hint may point back to the rejected attempted path rather than the allowed path; the fallback messages in both validators avoid this hint and only name the correct path (`hooks/loop-read-validator.sh:314-320`, `hooks/loop-write-validator.sh:344-350`).

- validation_or_tests: I found test coverage for wrong-directory allowlist behavior in `tests/test-allowlist-validators.sh`: an allowlisted filename in `/other/path` is rejected by `is_allowlisted_file` (`tests/test-allowlist-validators.sh:128-134`), and a Bash write to `/tmp/round-1-todos.md` is expected to exit `2` (`tests/test-allowlist-validators.sh:415-425`). The direct read/write validators also contain inline fallback paths, so template absence does not bypass blocking (`hooks/lib/template-loader.sh:197-210`). I did not run the tests because this assignment requested read-only research notes only.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `USE_REALPATH4EVERYTHING-HZ-146`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`