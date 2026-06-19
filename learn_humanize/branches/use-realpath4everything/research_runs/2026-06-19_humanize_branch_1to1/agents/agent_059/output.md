# agent_059 use-realpath4everything 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`

## Item Evidence

### USE_REALPATH4EVERYTHING-HZ-059 `file` `scripts/validate-refine-plan-io.sh`
- cursor: `[_]`
- core_role:
  - `scripts/validate-refine-plan-io.sh` is the preflight IO and schema validator for the `refine-plan` workflow. It is invoked before comment extraction or plan mutation, and its exit code controls whether `/humanize:refine-plan` can proceed.
  - It enforces that the input is an annotated `gen-plan`-style document with at least one valid non-empty reviewer comment block, required plan sections, writable output target, and writable or creatable QA directory.
  - The command integration is explicit in `commands/refine-plan.md`: the refine workflow’s Phase 1 runs `"${CLAUDE_PLUGIN_ROOT}/scripts/validate-refine-plan-io.sh" <validated-arguments>` and maps exit codes `0..7` to stop/continue behavior. See `commands/refine-plan.md:157`.
  - The hydrated flow skill also routes through this validator before extraction. See `skills/humanize-refine-plan/SKILL.md:20` and `skills/humanize-refine-plan/SKILL.md:131`.

- algorithmic_behavior:
  - The script starts with `set -e`, then defines two stateful `awk` scanners before parsing CLI flags. See `scripts/validate-refine-plan-io.sh:14`.
  - `scan_cmt_blocks()` counts valid, non-empty annotation blocks while rejecting malformed comment syntax. It tracks:
    - fenced markdown blocks via `in_fence` and `fence_marker`, ignoring markers inside both triple-backtick and tilde fences. See `scripts/validate-refine-plan-io.sh:139`.
    - HTML comments via `in_html`, ignoring annotation markers inside `<!-- ... -->`. See `scripts/validate-refine-plan-io.sh:165`.
    - active refine annotations via `in_cmt`, `cmt_format`, opening line/column/heading/context, and `cmt_has_text`. See `scripts/validate-refine-plan-io.sh:115`.
    - nearest visible markdown heading for error context, defaulting to `Preamble`. See `scripts/validate-refine-plan-io.sh:30` and `scripts/validate-refine-plan-io.sh:135`.
  - Supported annotation formats are:
    - classic `CMT:` ... `ENDCMT`
    - short tag `<cmt>` ... `</cmt>`
    - long tag `<comment>` ... `</comment>`
    - Marker dispatch is centralized in `find_comment_markers()`, `get_end_marker_for_format()`, and `get_marker_length()`. See `scripts/validate-refine-plan-io.sh:62`, `scripts/validate-refine-plan-io.sh:96`, and `scripts/validate-refine-plan-io.sh:103`.
  - The scanner treats inline and multiline blocks with the same state machine. A block increments the count only if it contains non-whitespace content before the matching end marker. See `scripts/validate-refine-plan-io.sh:182` and `scripts/validate-refine-plan-io.sh:209`.
  - Malformed comment syntax is fatal inside the scanner:
    - nested annotation start marker while already inside an annotation block emits a nested parse error. See `scripts/validate-refine-plan-io.sh:227`.
    - wrong or stray annotation end marker emits a stray-end parse error. See `scripts/validate-refine-plan-io.sh:232` and `scripts/validate-refine-plan-io.sh:294`.
    - EOF while still inside an annotation block emits a missing-end-marker parse error with opening line, column, heading, and excerpt. See `scripts/validate-refine-plan-io.sh:303`.
  - `scan_sections()` builds the visible markdown section stream while also ignoring fenced code, HTML comments, and custom annotation blocks. It appends only non-comment visible text and prints markdown headings matching `^#[#]*[[:space:]]+`. See `scripts/validate-refine-plan-io.sh:318` and `scripts/validate-refine-plan-io.sh:472`.
  - CLI parsing accepts only `--input`, `--output`, `--qa-dir`, `--discussion`, `--direct`, and help flags. Unknown options, missing option values, and help all route to `usage()` with exit code `7`. See `scripts/validate-refine-plan-io.sh:480` and `scripts/validate-refine-plan-io.sh:500`.
  - `--discussion` and `--direct` are parsed only as mutually exclusive mode signals for downstream workflow compatibility; the validator does not otherwise branch on them. See `scripts/validate-refine-plan-io.sh:526` and `scripts/validate-refine-plan-io.sh:544`.
  - The script normalizes input and output paths with `realpath -m` where available, falling back to the original string if resolution fails. This is branch-relevant because the validator surfaces canonicalized input/output paths in diagnostics and success output. See `scripts/validate-refine-plan-io.sh:561`.
  - The validation pipeline is ordered:
    - required `--input`
    - default output to input for in-place mode
    - canonicalize paths and derive input/output directories
    - check input exists
    - check input non-empty
    - scan annotation blocks
    - verify required visible gen-plan sections
    - check output or input directory writability depending on mode
    - create/check QA directory
    - print success metadata and exit `0`
  - Required visible sections are hard-coded as:
    - `## Goal Description`
    - `## Acceptance Criteria`
    - `## Path Boundaries`
    - `## Feasibility Hints`
    - `## Dependencies and Sequence`
    - `## Task Breakdown`
    - `## Claude-Codex Deliberation`
    - `## Pending User Decisions`
    - `## Implementation Notes`
    - See `scripts/validate-refine-plan-io.sh:608`.
  - Missing section detection compares the visible scanned headings with `grep -qF`, so exact required strings are accepted even when a heading has additional suffix text containing that exact substring; for example, `## Feasibility Hints and Suggestions` satisfies `## Feasibility Hints`. See `scripts/validate-refine-plan-io.sh:621`.

- inputs_outputs_state:
  - Inputs:
    - `--input <path>` is required and must point to an existing non-empty annotated plan file. See `scripts/validate-refine-plan-io.sh:550` and `scripts/validate-refine-plan-io.sh:573`.
    - `--output <path>` is optional. If omitted, the script uses in-place mode by setting `OUTPUT_FILE="$INPUT_FILE"`. See `scripts/validate-refine-plan-io.sh:556`.
    - `--qa-dir <path>` is optional and defaults to `.humanize/plan_qa`. See `scripts/validate-refine-plan-io.sh:493`.
    - `--discussion` and `--direct` are optional mode flags, but are mutually exclusive. See `scripts/validate-refine-plan-io.sh:544`.
  - Outputs:
    - On success, stdout includes `VALIDATION_SUCCESS`, canonical input/output paths, line count, valid comment block count, mode, QA directory, and `IO validation passed.` See `scripts/validate-refine-plan-io.sh:680`.
    - On failure, stdout includes a `VALIDATION_ERROR: ...` tag for most validation gates, plus human-readable repair guidance. Parse errors from the inner `awk` scanner are captured and wrapped under `VALIDATION_ERROR: INVALID_COMMENT_BLOCKS`. See `scripts/validate-refine-plan-io.sh:591`.
    - The script may create `QA_DIR` with `mkdir -p` if it is missing. This is intentional setup and is documented in `commands/refine-plan.md:176`.
  - State transitions:
    - This script has no durable scheduler state, no lock state, and no ledger state.
    - Its main mutable side effect is creating the QA directory if absent. See `scripts/validate-refine-plan-io.sh:662`.
    - Internal scanner states transition among outside-text, fenced-code, HTML-comment, and annotation-comment modes. These states determine whether comment markers and headings are visible or ignored.

- gates_or_invariants:
  - Exit code contract is declared in the file header and enforced by the script:
    - `0`: success
    - `1`: input file missing
    - `2`: input empty
    - `3`: no valid comment blocks or malformed comment syntax
    - `4`: missing required gen-plan sections
    - `5`: output directory not usable, or input directory not writable for in-place mode
    - `6`: QA directory not writable/creatable
    - `7`: invalid arguments
    - See `scripts/validate-refine-plan-io.sh:4`.
  - The validator must reject malformed annotation syntax before downstream comment extraction. It rejects nested starts, stray/wrong ends, and unclosed blocks. See `scripts/validate-refine-plan-io.sh:227`, `scripts/validate-refine-plan-io.sh:232`, and `scripts/validate-refine-plan-io.sh:308`.
  - Annotation markers inside fenced code or HTML comments are ignored for block counting, and required sections inside those ignored regions are not valid section evidence. See `scripts/validate-refine-plan-io.sh:139`, `scripts/validate-refine-plan-io.sh:165`, `scripts/validate-refine-plan-io.sh:339`, and `scripts/validate-refine-plan-io.sh:365`.
  - Empty annotation blocks do not count as valid input because `cmt_has_text` must be true before `count++`. See `scripts/validate-refine-plan-io.sh:212`.
  - In new-file mode, output directory must already exist and be writable; the validator does not create it. See `scripts/validate-refine-plan-io.sh:639`.
  - In in-place mode, the input directory must be writable to support the later atomic temp-file replacement. See `scripts/validate-refine-plan-io.sh:653`.
  - QA directory may be auto-created but must ultimately be writable. See `scripts/validate-refine-plan-io.sh:662`.
  - The validator intentionally rejects `--alt-language`; the command spec says to keep that flag out of the validator invocation. See `commands/refine-plan.md:72` and `tests/test-refine-plan.sh:1074`.

- dependencies_and_callers:
  - Runtime dependencies:
    - `bash`
    - POSIX-ish shell utilities: `awk`, `grep`, `dirname`, `realpath`, `wc`, `tr`, `mkdir`
    - Filesystem permissions for checking input/output/QA paths
  - Primary caller:
    - `commands/refine-plan.md` exposes the validator in the allowed tools frontmatter and mandates it in Phase 1. See `commands/refine-plan.md:4` and `commands/refine-plan.md:157`.
  - Flow wrapper:
    - `skills/humanize-refine-plan/SKILL.md` documents the validator as the `VALIDATE` step before extraction/classification/processing. See `skills/humanize-refine-plan/SKILL.md:18`.
  - Tests:
    - `tests/test-refine-plan.sh` assigns `VALIDATE_SCRIPT="$SCRIPTS_DIR/validate-refine-plan-io.sh"` and includes a dedicated script test block. See `tests/test-refine-plan.sh:25` and `tests/test-refine-plan.sh:1044`.
  - Install/docs references:
    - `docs/usage.md` documents `refine-plan` usage and options.
    - `docs/install-for-codex.md`, `docs/install-for-claude.md`, and `docs/install-for-kimi.md` cover installing the related command/skill.
    - `scripts/install-skill.sh` includes `humanize-refine-plan` in skill sync wiring.

- edge_cases_or_failure_modes:
  - `realpath -m` is GNU-style. On systems where `realpath` lacks `-m`, the command falls back to the uncanonicalized path string. This avoids immediate failure but can make equality checks/path diagnostics depend on platform behavior. See `scripts/validate-refine-plan-io.sh:561`.
  - The script checks writability with `[[ -w ... ]]`; when run as a privileged user or in unusual ACL/sandbox contexts, this may not exactly match later write behavior.
  - `mkdir -p "$QA_DIR"` is the one real filesystem mutation. In a read-only workspace, a valid plan with a missing QA dir would fail with exit code `6` at that gate even if all content validation passes.
  - `scan_sections()` does not validate matching custom annotation start/end formats as strictly as `scan_cmt_blocks()`; however, the stricter comment scan runs first and blocks malformed inputs before section validation. See `scripts/validate-refine-plan-io.sh:589` before `scripts/validate-refine-plan-io.sh:608`.
  - Nested HTML comments are not a general HTML parser; the scanner tracks only `<!--` and the next `-->`. That is appropriate for markdown comment exclusion but can behave simply on malformed/nested HTML comment text.
  - The required section check is fixed to the v1 `gen-plan` schema. Plans using renamed headings or localized headings will fail exit `4` even if structurally equivalent.
  - The script reports `NO_COMMENT_BLOCKS` when all markers are inside ignored regions or blocks are empty. This can surprise users who visually see `CMT:` text inside examples or comments, but it matches the documented scanner rules.
  - Because `usage()` exits `7`, `--help` is treated as invalid-argument exit rather than a conventional success exit. Tests explicitly require this behavior. See `tests/test-refine-plan.sh:1088`.

- validation_or_tests:
  - I inspected the file directly with line numbers and ran `bash -n scripts/validate-refine-plan-io.sh`; syntax validation passed with exit code `0`.
  - I did not run the full `tests/test-refine-plan.sh` suite because the branch export is read-only and those tests create fixture files/directories and change permissions.
  - Existing test coverage in `tests/test-refine-plan.sh` covers:
    - invalid flags and missing values, including forbidden `--alt-language`, mutually exclusive modes, and help behavior. See `tests/test-refine-plan.sh:1051`.
    - exit codes `1..6` for missing input, empty input, no comments, missing sections, bad output directory, bad QA path. See `tests/test-refine-plan.sh:1101`.
    - ignored markers inside HTML comments and fenced code. See `tests/test-refine-plan.sh:1128` and `tests/test-refine-plan.sh:1137`.
    - empty comment blocks, unterminated blocks, nested blocks, and parse error messages with context. See `tests/test-refine-plan.sh:1146`, `tests/test-refine-plan.sh:1155`, and `tests/test-refine-plan.sh:1176`.
    - required section filtering so headings in code fences or HTML comments do not satisfy schema checks. See `tests/test-refine-plan.sh:1200` and `tests/test-refine-plan.sh:1209`.
    - successful in-place and new-file modes, QA auto-create behavior, mode reporting, and valid comment count reporting. See `tests/test-refine-plan.sh:1285`.
  - A `git status` probe was attempted read-only but macOS tooling tried to create a cache under `/tmp` and hung under sandbox restrictions; I interrupted it without escalation or file modification.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 1/1 evidence section present
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`