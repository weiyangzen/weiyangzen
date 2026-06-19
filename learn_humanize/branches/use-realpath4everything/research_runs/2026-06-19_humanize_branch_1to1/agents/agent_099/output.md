# agent_099 use-realpath4everything 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`

## Item Evidence

### USE_REALPATH4EVERYTHING-HZ-099 `file` `tests/test-template-references.sh`
- cursor: `[_]`
- core_role:
  - `tests/test-template-references.sh` is an executable shell specification for the hook/template contract. Its purpose is to ensure hook validators and stop-hook logic never reference missing prompt templates and that critical validators use the fallback-safe render path.
  - The behavior it protects is algorithmically relevant because hook blocking decisions depend on producing non-empty, user-actionable messages. The file header states the failure class directly: missing templates can cause Claude to receive empty error messages when a validator blocks an action (`tests/test-template-references.sh:5-9`).
  - It is a test/validation artifact, not the template renderer implementation itself. The implementation contract lives in `hooks/lib/template-loader.sh`, where `load_template` emits content or warns on missing files (`hooks/lib/template-loader.sh:36-46`), `load_and_render` renders only non-empty loaded content (`hooks/lib/template-loader.sh:140-151`), and `load_and_render_safe` falls back when load or render output is empty (`hooks/lib/template-loader.sh:188-211`).

- algorithmic_behavior:
  - Initializes project paths from the test script location: `SCRIPT_DIR`, `PROJECT_ROOT`, and `TEMPLATE_DIR="$PROJECT_ROOT/prompt-template"` (`tests/test-template-references.sh:14-16`).
  - Maintains three counters as state: `TESTS_PASSED`, `TESTS_FAILED`, and `WARNINGS` (`tests/test-template-references.sh:25-27`). Helper functions `pass`, `fail`, and `warn` print colored status lines and increment those counters (`tests/test-template-references.sh:29-42`).
  - Section 1 scans a fixed set of hook scripts: `hooks/loop-codex-stop-hook.sh`, `hooks/loop-read-validator.sh`, `hooks/loop-write-validator.sh`, `hooks/loop-edit-validator.sh`, `hooks/loop-bash-validator.sh`, and `hooks/lib/loop-common.sh` (`tests/test-template-references.sh:56-64`).
  - For each existing script, it reads line by line, skips full-line comments, detects calls matching `load_template`, `load_and_render`, or `load_and_render_safe` with literal `"$TEMPLATE_DIR"` as the first argument, extracts the second quoted argument with `sed`, and verifies `"$TEMPLATE_DIR/$template_path"` exists (`tests/test-template-references.sh:74-110`).
  - Each discovered reference increments `FOUND_REFERENCES`; each existing template is a pass, while each missing template is a failure and is appended to `MISSING_TEMPLATES` (`tests/test-template-references.sh:98-107`).
  - Section 2 inventories every `*.md` file under `prompt-template` using null-delimited `find`, strips the template-dir prefix, and then greps `hooks/` for direct quoted references to each relative path (`tests/test-template-references.sh:121-141`). This section treats unreferenced templates as warnings, not failures.
  - Section 3 hard-codes common `loop-common.sh` message templates and verifies each file exists (`tests/test-template-references.sh:149-167`). This cross-check supplements the regex scan for central block-message helpers.
  - Section 4 enforces safer rendering in critical validators. It checks only `loop-read-validator.sh`, `loop-write-validator.sh`, and `loop-edit-validator.sh`; it counts `load_and_render "$TEMPLATE_DIR"` lines that are not `load_and_render_safe` and fails if any exist (`tests/test-template-references.sh:172-201`).
  - The summary prints pass/fail/warning counts, lists missing templates when any were collected, exits `0` if `TESTS_FAILED == 0`, and exits `1` otherwise (`tests/test-template-references.sh:206-229`).

- inputs_outputs_state:
  - Inputs:
    - Fixed script list from `SCRIPTS_TO_CHECK` (`tests/test-template-references.sh:57-64`).
    - Template root `prompt-template/` resolved under the repository root (`tests/test-template-references.sh:14-16`).
    - All markdown templates discovered with `find "$TEMPLATE_DIR" -name "*.md" -type f -print0` (`tests/test-template-references.sh:123-126`).
    - Hook/template reference source text, especially literal calls shaped like `load_and_render_safe "$TEMPLATE_DIR" "block/wrong-directory-path.md"` (`tests/test-template-references.sh:93-97`).
  - Outputs:
    - Human-readable colored status sections and per-reference pass/fail/warn lines (`tests/test-template-references.sh:29-49`, `tests/test-template-references.sh:206-211`).
    - Process exit code `0` when there are no failures; `1` when missing templates or unsafe critical-validator render calls produced failures (`tests/test-template-references.sh:221-229`).
    - A critical missing-template list if `MISSING_TEMPLATES` is non-empty (`tests/test-template-references.sh:213-219`).
  - State transitions:
    - Missing script path: `warn`, increments `WARNINGS`, then continues scanning later scripts (`tests/test-template-references.sh:74-78`).
    - Existing referenced template: `pass`, increments `TESTS_PASSED` (`tests/test-template-references.sh:102-103`).
    - Missing referenced template: `fail`, increments `TESTS_FAILED`, records template in `MISSING_TEMPLATES` (`tests/test-template-references.sh:104-107`).
    - Unreferenced discovered template: `warn`, increments `WARNINGS`, records in `UNREFERENCED` (`tests/test-template-references.sh:138-140`).
    - Unsafe `load_and_render` in a critical validator: increments `unsafe_count`, then fails that script if count is greater than zero (`tests/test-template-references.sh:187-199`).

- gates_or_invariants:
  - Hard gate: every literal template reference found in the selected hook files must resolve to an existing markdown file under `prompt-template/` (`tests/test-template-references.sh:93-107`).
  - Hard gate: common block-message templates expected by `loop-common.sh` must exist: `block/todos-file-access.md`, `block/prompt-file-write.md`, `block/state-file-modification.md`, `block/summary-bash-write.md`, `block/goal-tracker-bash-write.md`, and `block/goal-tracker-modification.md` (`tests/test-template-references.sh:152-159`).
  - Hard gate: critical read/write/edit validators must render via `load_and_render_safe`, not raw `load_and_render`, when using `"$TEMPLATE_DIR"` (`tests/test-template-references.sh:176-201`).
  - Soft gate: templates discovered in `prompt-template/` but not directly quoted in `hooks/` are warnings because dynamic usage may be valid (`tests/test-template-references.sh:130-140`).
  - Invariant: warnings do not affect exit status; only `TESTS_FAILED` controls final success/failure (`tests/test-template-references.sh:221-229`).
  - Invariant/limitation: the Section 1 parser only recognizes calls where the first argument is literally quoted as `"$TEMPLATE_DIR"` and the template path is the next quoted string (`tests/test-template-references.sh:83-97`). Calls through other variables, unquoted args, computed names, or multi-line argument formatting may be invisible to this validator.

- dependencies_and_callers:
  - Depends on Bash with process substitution and arrays, plus standard tools: `find`, `grep`, `sed`, `basename`, and shell test operators.
  - Depends on repository layout:
    - Hook scripts under `hooks/`.
    - Template markdown files under `prompt-template/`.
  - Related implementation:
    - `hooks/lib/template-loader.sh` defines `get_template_dir`, `load_template`, `render_template`, `load_and_render`, `load_and_render_safe`, and `validate_template_dir` (`hooks/lib/template-loader.sh:24-46`, `hooks/lib/template-loader.sh:56-151`, `hooks/lib/template-loader.sh:188-238`).
    - `hooks/lib/loop-common.sh` sources `template-loader.sh`, initializes `TEMPLATE_DIR`, warns rather than fails when template-dir validation fails, and exposes block-message helpers using `load_and_render_safe` (`hooks/lib/loop-common.sh:240-248`, `hooks/lib/loop-common.sh:839-912`, `hooks/lib/loop-common.sh:1442-1479`, `hooks/lib/loop-common.sh:1528-1530`).
    - `hooks/loop-read-validator.sh` uses safe template rendering for wrong file location, wrong round file, and wrong directory path blocks (`hooks/loop-read-validator.sh:232-241`, `hooks/loop-read-validator.sh:270-279`, `hooks/loop-read-validator.sh:286-298`, `hooks/loop-read-validator.sh:305-321`).
    - `hooks/loop-write-validator.sh` uses safe template rendering for protected plan backup, wrong contract/summary location, wrong round number, and wrong directory path (`hooks/loop-write-validator.sh:230-235`, `hooks/loop-write-validator.sh:272-288`, `hooks/loop-write-validator.sh:311-324`, `hooks/loop-write-validator.sh:332-351`).
    - `hooks/loop-edit-validator.sh` is one of the critical scripts checked for safe rendering (`tests/test-template-references.sh:176-180`, `tests/test-template-references.sh:182-201`).
    - `hooks/loop-bash-validator.sh` and `hooks/loop-codex-stop-hook.sh` are scanned for missing referenced templates but are not part of the Section 4 critical safe-render enforcement list (`tests/test-template-references.sh:57-64`, `tests/test-template-references.sh:176-180`).
  - Likely callers:
    - Manual or CI-style shell validation, e.g. `bash tests/test-template-references.sh`.
    - Broader test runners may include it alongside `tests/test-template-loader.sh` and `tests/test-templates-comprehensive.sh`, but this assigned file itself has no internal caller dispatch.

- edge_cases_or_failure_modes:
  - Missing hook script is only a warning, not a failure (`tests/test-template-references.sh:74-78`). This can hide accidental script removal unless another test catches it.
  - Missing `prompt-template/` directory is not explicitly checked before `find`; because the script does not use `set -e`, `find "$TEMPLATE_DIR"` failure can still leave Section 2 with zero templates and may rely on Section 1/3 failures to catch missing concrete files (`tests/test-template-references.sh:12`, `tests/test-template-references.sh:121-128`).
  - The parser skips only lines whose first non-space character is `#`; inline comments after live code are still parsed if they match the regex (`tests/test-template-references.sh:87-94`).
  - Multi-line function invocations, single quotes, unquoted `$TEMPLATE_DIR`, template names held in variables, or calls via wrapper functions are not detected by Section 1 because extraction uses a single-line `grep` plus `sed` pattern (`tests/test-template-references.sh:93-97`).
  - Section 2 uses `grep -rq "\"$template\"" "$PROJECT_ROOT/hooks/"`, so it detects direct quoted string occurrences, not necessarily executable references (`tests/test-template-references.sh:134-140`).
  - Duplicate references are counted and passed separately. In the validation run, `block/wrong-file-location.md` appeared more than once and each occurrence generated a pass, which matches the line-oriented scanner model.
  - Critical safe-render enforcement is limited to read/write/edit validators. `loop-codex-stop-hook.sh`, `loop-bash-validator.sh`, `loop-common.sh`, and other hook libraries can still use `load_template` or `load_and_render_safe` without Section 4 applying the same “no unsafe `load_and_render`” rule (`tests/test-template-references.sh:176-180`).
  - The test intentionally allows direct `load_template` usage, including optional template appends/notes in the stop hook, as long as the referenced template file exists (`tests/test-template-references.sh:93-107`).

- validation_or_tests:
  - I ran the assigned executable spec read-only:
    - Command: `bash tests/test-template-references.sh`
    - Result: exit code `0`.
    - Summary: `Passed: 120`, `Failed: 0`, `Warnings: 9`.
    - The run found `Total template references found: 57` and `Total template files: 63`.
  - Warnings were informational unreferenced-template warnings, not failures. The warned templates were dynamic or non-direct references such as `plan/gen-plan-template.md`, `plan/refine-plan-qa-template.md`, `claude/agent-teams-instructions.md`, `block/bitlesson-delta-*`, and `block/claude-eyes-timeout.md`.
  - Current observed validation outcome supports the file’s intended invariant: all directly scanned hook template references exist, common `loop-common.sh` block templates exist, and read/write/edit validators use `load_and_render_safe`.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 1 item represented in Item Evidence exactly once
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`