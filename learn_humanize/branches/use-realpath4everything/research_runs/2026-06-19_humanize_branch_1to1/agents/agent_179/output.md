# agent_179 use-realpath4everything 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`

## Item Evidence

### USE_REALPATH4EVERYTHING-HZ-179 `file` `skills/humanize-refine-plan/SKILL.md`
- cursor: `[_]`
- core_role:
  - `skills/humanize-refine-plan/SKILL.md` is a flow-skill instruction file for refining an annotated `gen-plan` implementation plan into two outputs: a comment-free refined plan and a QA ledger.
  - The skill is not user-invocable directly in frontmatter (`user-invocable: false`, lines 1-6); it is installed as part of the Humanize skill suite and is surfaced through `/flow:humanize-refine-plan` or `/skill:humanize-refine-plan` usage examples (lines 144-161).
  - Algorithmically, it defines the high-level workflow contract rather than containing executable implementation code. The concrete command prompt and validator live in related files: `commands/refine-plan.md`, `scripts/validate-refine-plan-io.sh`, and `prompt-template/plan/refine-plan-qa-template.md`.

- algorithmic_behavior:
  - The declared pipeline is sequential and stateful. The Mermaid graph in lines 18-48 specifies these stages:
    - parse arguments and derive paths;
    - load merged Humanize config;
    - validate IO via `{{HUMANIZE_RUNTIME_ROOT}}/scripts/validate-refine-plan-io.sh`;
    - extract valid `CMT:` / `ENDCMT` blocks with a stateful scanner;
    - classify comments as `question`, `change_request`, or `research_request`;
    - ask the user only for ambiguous comments in discussion mode;
    - process comments in order by answering, editing the plan, or doing targeted repository research;
    - generate a refined plan while preserving required `gen-plan` sections;
    - validate the refined plan has no comment markers and has consistent references/routing tags;
    - populate a QA document from `prompt-template/plan/refine-plan-qa-template.md`;
    - optionally generate alternate-language variants;
    - write all outputs atomically.
  - The skill requires preserving the `gen-plan` schema, not inventing new top-level sections (lines 67-87). Required sections are listed at lines 73-82, including `## Goal Description`, `## Acceptance Criteria`, `## Task Breakdown`, `## Pending User Decisions`, and `## Implementation Notes`.
  - Comment classification is constrained to exactly one dominant class per raw comment block: `question`, `change_request`, or `research_request` (lines 88-95). Related command instructions expand this with deterministic sub-items for multi-intent comments and dominance precedence of research over change over question (`commands/refine-plan.md` lines 276-329).
  - Output behavior is explicit: produce a refined plan with comment blocks removed and approved refinements applied, plus a QA ledger recording one row per raw `CMT-N`, classification, disposition, answers, research, applied changes, remaining decisions, metadata, and convergence status (lines 96-107).
  - Alternate-language behavior is normalized by a fixed table of supported names/codes/suffixes (lines 108-130). English is a no-op, identifiers remain unchanged, and matching main/alternate languages skip variant generation.

- inputs_outputs_state:
  - Required input:
    - `--input <path/to/annotated-plan.md>`: an annotated plan already following the `gen-plan` schema and containing at least one `CMT:` / `ENDCMT` block (lines 50-54).
  - Optional inputs:
    - `--output`: output path, defaulting to in-place mode when omitted (lines 55-56, 62-65).
    - `--qa-dir`: QA ledger directory, default `.humanize/plan_qa` (line 57).
    - `--alt-language`: optional translated variant language (line 58).
    - `--discussion` / `--direct`: mutually exclusive ambiguity-handling modes (lines 59-64).
  - Outputs:
    - refined plan at `--output` or the input path in in-place mode;
    - QA ledger in `--qa-dir`;
    - optional translated refined-plan and QA variants with stable suffixes such as `_zh`, `_ko`, `_ja`, etc. (lines 108-130).
  - State transitions:
    - raw annotated plan -> validated plan input;
    - valid comment blocks -> ordered `CMT-N` records;
    - `CMT-N` records -> classified/processed dispositions;
    - comment-bearing plan -> comment-free refined plan;
    - processed comments -> QA ledger rows and metadata;
    - unresolved material decisions -> `partially_converged`; fully resolved comments with no pending decisions -> `converged`, as specified more fully in `commands/refine-plan.md` lines 378-392 and metadata rules lines 500-505.
  - The branch’s realpath-related behavior appears in the referenced validator: `scripts/validate-refine-plan-io.sh` canonicalizes `INPUT_FILE` and `OUTPUT_FILE` using `realpath -m` before directory and existence checks (lines 561-565). `QA_DIR` is printed and validated separately without the same visible realpath normalization in the inspected range (lines 567-572, 662-678).

- gates_or_invariants:
  - Argument invariants:
    - `--input` is required.
    - `--discussion` and `--direct` are mutually exclusive.
    - `--alt-language` must not be passed to `validate-refine-plan-io.sh` because the validator does not accept it (lines 62-65).
  - Schema invariants:
    - The final plan must preserve required `gen-plan` sections (lines 71-82).
    - Optional sections and original design draft appendices must be preserved when present (line 83).
    - Task routing tags are restricted to `coding` or `analyze` (line 84).
    - All resolved `CMT:` / `ENDCMT` blocks must be removed from the final plan (line 72).
  - Validation gate:
    - The skill’s graph routes through IO validation before parsing (lines 20-27).
    - The validator checks input existence, non-empty input, at least one valid non-empty comment block, required sections, output/input directory writability, and QA directory writability or creation (`scripts/validate-refine-plan-io.sh` lines 573-692).
    - Required section scanning ignores headings inside code fences, HTML comments, and comment blocks (`scripts/validate-refine-plan-io.sh` lines 318-478), preventing hidden schema headings from satisfying the gate.
  - Parse/scanner invariants:
    - The command-level scanner requirements support classic `CMT:` / `ENDCMT`, `<cmt>` / `</cmt>`, and `<comment>` / `</comment>` formats, both inline and multiline (`commands/refine-plan.md` lines 197-223).
    - Markers inside fenced code blocks and HTML comments are ignored (`commands/refine-plan.md` lines 223-225).
    - Empty comment blocks are removed but do not consume IDs (`commands/refine-plan.md` lines 227-229).
    - Fatal parse errors include nested markers, stray/wrong end markers, and EOF before close, with line/column/heading/context (`commands/refine-plan.md` lines 244-264).
  - Atomicity invariant:
    - The skill requires atomic writes for refined plan, QA, and variants (line 86).
    - The command-level transaction expands this: prepare all final content first, write temp files in destination directories, delete temps on failure, replace auxiliary outputs before the main in-place plan, and report partial-finalization risk if needed (`commands/refine-plan.md` lines 508-572).

- dependencies_and_callers:
  - Direct dependencies named by the skill:
    - `{{HUMANIZE_RUNTIME_ROOT}}/scripts/validate-refine-plan-io.sh` for IO validation (line 22).
    - `{{HUMANIZE_RUNTIME_ROOT}}/prompt-template/plan/refine-plan-qa-template.md` for QA generation (line 41).
  - Related command prompt:
    - `commands/refine-plan.md` is the detailed executable instruction surface for the flow. It declares the planning-only constraint, allowed tools, phase ordering, config loading, extraction/classification/processing rules, QA generation, and atomic write behavior (notably lines 19-43 and 46-607).
  - Validator:
    - `scripts/validate-refine-plan-io.sh` implements argument parsing, realpath normalization of input/output paths, comment-block scanning, section scanning, exit-code behavior, and directory writability checks.
  - QA template:
    - `prompt-template/plan/refine-plan-qa-template.md` supplies the required ledger shape with sections for Summary, Comment Ledger, Answers, Research Findings, Plan Changes Applied, Remaining Decisions, and Refinement Metadata (lines 1-119).
  - Installation and documentation callers:
    - `scripts/install-skill.sh` includes `"humanize-refine-plan"` in `SKILL_NAMES` (lines 39-44) and validates the skill exists in source/installed layouts (lines 75-87, 104-114).
    - `README.md` documents `/humanize:refine-plan --input docs/plan.md` as the second quick-start step after generating a plan and before running the RLCR loop (lines 44-56).
    - `docs/install-for-codex.md` and `docs/install-for-kimi.md` mention/install the `humanize-refine-plan` skill according to the repository-wide search results.
  - Test caller:
    - `tests/test-refine-plan.sh` validates the command structure, validator exit codes/mode handling, comment extraction/classification requirements, language variant/atomic write rules, QA template coverage, and installation/documentation wiring (lines 1-12).

- edge_cases_or_failure_modes:
  - Invalid argument and mode cases:
    - Missing `--input`, missing option values, unknown options, or both `--discussion` and `--direct` return validator exit code 7 (`scripts/validate-refine-plan-io.sh` lines 480-554).
    - `--alt-language` is accepted by the skill/command but must be excluded from validator invocation (skill lines 62-65; command lines 72-77, 157-163).
  - Input failure cases:
    - Missing input exits 1 (validator lines 573-579).
    - Empty input exits 2 (validator lines 581-587).
    - No valid non-empty comment block exits 3 (validator lines 589-606).
    - Missing required `gen-plan` sections exits 4 (validator lines 608-637).
  - Path/write failure cases:
    - Output directory missing or not writable, or input directory not writable in in-place mode, exits 5 (validator lines 639-660).
    - QA directory creation failure or non-writable QA directory exits 6 (validator lines 662-678).
  - Parse edge cases:
    - Nested comment starts and stray/wrong end markers are parse errors detected by the scanner (`scripts/validate-refine-plan-io.sh` lines 227-235, 294-297).
    - EOF while still in a comment block reports the opening line/column/heading/context and fails the scan (`scripts/validate-refine-plan-io.sh` lines 303-315).
    - Comment markers inside fenced code blocks and HTML comments are ignored in both comment and section scanning (`scripts/validate-refine-plan-io.sh` lines 139-158, 165-180, 318-478).
    - Empty comment blocks do not count toward the required non-empty comment-block gate (`commands/refine-plan.md` lines 227-229; validator count logic lines 212-214 and 599-606).
  - Refinement failure cases:
    - Ambiguous comments in discussion mode require a minimum user question; in direct mode, the flow must choose the smallest safe assumption and record it in QA (skill lines 30-34, 59-64; command lines 306-312, 387-390).
    - If consistency validation after refinement is fixable, repair and loop; if blocking, report and stop (skill lines 36-40).
    - Unsupported CLI alternate language is blocking; unsupported config alternate language should warn and disable variants (`commands/refine-plan.md` lines 140-147).
  - Potential spec mismatch:
    - The skill’s validation exit-code table says exit code 3 means no `CMT:` blocks and does not explicitly mention malformed comment syntax (lines 131-143). The validator script comments and behavior use exit code 3 for no valid comment blocks or malformed comment syntax (`scripts/validate-refine-plan-io.sh` lines 4-12, 589-597). This is not necessarily a defect, but final documentation consumers should understand exit code 3 covers both “none” and “invalid/malformed” cases in the executable validator.

- validation_or_tests:
  - `tests/test-refine-plan.sh` is the primary validation surface for this skill area.
  - It defines test scope as command structure, validator behavior, QA template coverage, and installation wiring (lines 1-12).
  - It checks core files exist, including `commands/refine-plan.md`, `prompt-template/plan/refine-plan-qa-template.md`, executable `scripts/validate-refine-plan-io.sh`, and `skills/humanize-refine-plan/SKILL.md` (lines 640-657).
  - It validates command frontmatter, argument hint, validator allowlist, `AskUserQuestion`, hidden slash-command status, and ultrathink instruction (lines 660-674).
  - It validates the planning-only constraint and phase order, including extraction before classification and QA before atomic write (lines 676-701).
  - It validates exit-code documentation and that `--alt-language` is excluded from validator invocation (lines 703-713).
  - It validates extraction requirements, including inline/multiline blocks, fenced-code/HTML exclusions, surrounding-text preservation, metadata, fatal parse errors, and empty-only rejection (lines 715-730).
  - It validates classification requirements, heuristics, sub-item splitting, ambiguity modes, and disposition values (lines 732-748).
  - It validates structure/mode rules, alternate-language rules, and atomic write requirements (lines 750-801).
  - It validates QA template sections and metadata fields (lines 803-817).
  - It validates the skill frontmatter `user-invocable: false` and installer/docs wiring for `humanize-refine-plan` (lines 820-855).
  - I did not run the tests because this assignment requested research notes only and the workspace is read-only; all evidence above is from direct file inspection.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `USE_REALPATH4EVERYTHING-HZ-179`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`