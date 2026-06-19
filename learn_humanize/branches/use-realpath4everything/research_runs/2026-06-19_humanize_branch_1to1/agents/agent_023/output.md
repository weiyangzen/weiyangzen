# agent_023 use-realpath4everything 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`

## Item Evidence

### USE_REALPATH4EVERYTHING-HZ-023 `directory` `skills/humanize-refine-plan`
- cursor: `[_]`
- core_role:
  - `skills/humanize-refine-plan` is a flow-skill definition directory for refining an already generated, annotated implementation plan into two durable artifacts: a comment-free refined plan and a QA ledger.
  - Recursive inspection found one descendant file, `skills/humanize-refine-plan/SKILL.md`, 6293 bytes. No nested subdirectories or additional scripts/templates live under this assigned directory.
  - The skill is not user-invocable directly: frontmatter declares `name: humanize-refine-plan`, describes the refine behavior, sets `type: flow`, and sets `user-invocable: false` at `skills/humanize-refine-plan/SKILL.md:1-5`.
  - Its algorithmic responsibility is orchestration/specification, not implementation code. The concrete runtime algorithm is split across the command contract in `commands/refine-plan.md`, IO validator `scripts/validate-refine-plan-io.sh`, shared config loader `scripts/lib/config-loader.sh`, and QA template `prompt-template/plan/refine-plan-qa-template.md`.

- algorithmic_behavior:
  - The directory’s skill body defines a deterministic refine pipeline: parse arguments, load merged config, validate IO, extract comments with a stateful scanner, classify comments, process them in order, generate a refined plan, validate the plan, populate QA, optionally translate variants, write atomically, and report success. The full flow is shown in the Mermaid graph at `skills/humanize-refine-plan/SKILL.md:18-48`.
  - Required input is `--input <path/to/annotated-plan.md>`, which must already follow the `gen-plan` schema and contain at least one `CMT:` / `ENDCMT` block according to `skills/humanize-refine-plan/SKILL.md:50-54`.
  - Optional controls are `--output`, `--qa-dir`, `--alt-language`, `--discussion`, and `--direct` at `skills/humanize-refine-plan/SKILL.md:55-60`.
  - The skill requires preserving the existing `gen-plan` structure and removing resolved comment blocks from the final plan at `skills/humanize-refine-plan/SKILL.md:67-86`.
  - The required retained top-level plan sections are enumerated in `skills/humanize-refine-plan/SKILL.md:73-82`: `Goal Description`, `Acceptance Criteria`, `Path Boundaries`, `Feasibility Hints and Suggestions`, `Dependencies and Sequence`, `Task Breakdown`, `Claude-Codex Deliberation`, `Pending User Decisions`, and `Implementation Notes`.
  - The downstream command expands the algorithm in more detail. `commands/refine-plan.md:30-42` requires strict sequential phases from execution-mode setup through atomic write; `commands/refine-plan.md:32` explicitly forbids phase parallelization.
  - Comment extraction must use a stateful scanner, not a naive regex pass, and must track code fences, HTML comments, comment-block state, and nearest heading per `commands/refine-plan.md:184-196`.
  - Supported comment forms include classic `CMT:` / `ENDCMT`, short XML-like `<cmt>...</cmt>`, and long `<comment>...</comment>`, each supporting inline and multiline forms at `commands/refine-plan.md:197-222`.
  - The processing algorithm assigns ordered raw IDs `CMT-1`, `CMT-2`, etc. only for non-empty extracted blocks, while empty blocks are removed without consuming IDs according to `commands/refine-plan.md:226-228`.
  - Each comment receives a dominant classification: `question`, `change_request`, or `research_request`, listed in `skills/humanize-refine-plan/SKILL.md:88-95` and expanded in `commands/refine-plan.md:276-305`.
  - Multi-intent comments are split into deterministic sub-items `CMT-N.1`, `CMT-N.2`, etc., while retaining the raw ledger ID, per `commands/refine-plan.md:296-305`.
  - Processing is document-order and classification-specific: questions are answered with minimal clarifying plan edits; change requests update the plan and propagate cross-section consistency; research requests use targeted repository research with `Read`, `Glob`, and `Grep` only, then integrate or defer findings. See `commands/refine-plan.md:332-377`.
  - Plan generation starts from `PLAN_WITH_COMMENTS_REMOVED`, applies accepted refinements, preserves schema and IDs unless explicitly changed, and enforces routing tags `coding` or `analyze` at `commands/refine-plan.md:395-428`.
  - Before QA generation, the refined plan must still have required sections, no comment markers, valid AC references, valid task dependencies, valid task routing tags, and convergence-state consistency per `commands/refine-plan.md:442-453`.
  - QA generation uses `prompt-template/plan/refine-plan-qa-template.md`, and must populate summary, ledger, answers, research findings, applied changes, remaining decisions, and metadata per `commands/refine-plan.md:457-505`.
  - Atomic write behavior is specified at `commands/refine-plan.md:508-572`: prepare content in memory, write temp files in the destination directories, clean up on failures, replace auxiliary outputs before the main in-place plan, and leave no stale temp files.

- inputs_outputs_state:
  - Inputs:
    - Primary file: annotated plan path from `--input`.
    - Optional output path from `--output`; if omitted, output is in-place at the input path. This is specified in `skills/humanize-refine-plan/SKILL.md:55-66` and `commands/refine-plan.md:57-77`.
    - Optional QA directory from `--qa-dir`, defaulting to `.humanize/plan_qa`, at `skills/humanize-refine-plan/SKILL.md:57` and `commands/refine-plan.md:61`.
    - Optional alternate language from `--alt-language`, handled by the flow but deliberately not passed to the validator, per `skills/humanize-refine-plan/SKILL.md:58-65`.
    - Execution mode: `--discussion` asks minimal user questions for ambiguity; `--direct` uses the smallest safe assumption and records it in QA. The flags are mutually exclusive at `skills/humanize-refine-plan/SKILL.md:59-64`.
    - Shared config: the command reuses `scripts/lib/config-loader.sh` semantics, with default, user, and project layers at `commands/refine-plan.md:86-116`. The actual loader merges default config, optional user config, and optional project config with later layers overriding earlier layers at `scripts/lib/config-loader.sh:63-136`.
  - Outputs:
    - Main refined plan at `OUTPUT_FILE`, described in `skills/humanize-refine-plan/SKILL.md:96-99` and `commands/refine-plan.md:514-518`.
    - Main QA ledger at `QA_FILE`, derived from the input basename rather than output basename, per `commands/refine-plan.md:65-72`.
    - Optional language variants for plan and QA, with suffix insertion before the extension, per `commands/refine-plan.md:519-544`.
    - Final success report including output paths, counts, mode, and convergence status, per `skills/humanize-refine-plan/SKILL.md:45-47` and `commands/refine-plan.md:574-586`.
  - State transitions:
    - The state machine moves from validated input to extracted comments, then classified records, then dispositions, then refined plan text, then QA text, then final filesystem writes.
    - Comment-level state moves from raw `CMT-N` to dominant classification and optional sub-items, then to a final disposition: `answered`, `applied`, `researched`, `deferred`, or `resolved`, per `commands/refine-plan.md:378-391`.
    - Convergence state becomes `converged` if all comments are fully resolved and no pending decisions remain; otherwise it becomes `partially_converged`, per `commands/refine-plan.md:390-391`.
    - Alternate-language state normalizes supported language names or ISO codes into suffixes. The skill’s supported table is at `skills/humanize-refine-plan/SKILL.md:108-129`; the command’s equivalent table and no-op English behavior are at `commands/refine-plan.md:118-153`.

- gates_or_invariants:
  - Planning-only invariant: the command must refine plan artifacts only, must not implement repository code, must not modify unrelated source files, must not start RLCR automatically, and must not create a new plan schema. This hard boundary is in `commands/refine-plan.md:19-28`.
  - Validator invocation invariant: `--alt-language` is part of refine flow setup but must not be passed to `validate-refine-plan-io.sh`, because the validator does not accept it. This appears in `skills/humanize-refine-plan/SKILL.md:62-65` and `commands/refine-plan.md:72-77`.
  - Mode invariant: `--discussion` and `--direct` are mutually exclusive at `skills/humanize-refine-plan/SKILL.md:62-64`, `commands/refine-plan.md:57-64`, and enforced by the validator at `scripts/validate-refine-plan-io.sh:544-548`.
  - Schema invariant: required `gen-plan` sections must remain intact. The skill lists them at `skills/humanize-refine-plan/SKILL.md:71-82`; the command rechecks them at `commands/refine-plan.md:399-418`; the validator checks input sections with `scan_sections` and `REQUIRED_SECTIONS` at `scripts/validate-refine-plan-io.sh:318-478` and `scripts/validate-refine-plan-io.sh:608-637`.
  - Marker invariant: final plan must contain no unresolved comment markers; this is stated in `skills/humanize-refine-plan/SKILL.md:71-72` and required before QA in `commands/refine-plan.md:442-448`.
  - Routing invariant: task routing tags must be restricted to `coding` or `analyze`, in `skills/humanize-refine-plan/SKILL.md:84` and `commands/refine-plan.md:426-427`.
  - QA invariant: QA is mandatory and must be generated from the shipped template. The skill states this at `skills/humanize-refine-plan/SKILL.md:85`; the command requires reading and fully populating the template at `commands/refine-plan.md:457-505`.
  - Atomicity invariant: all final content is prepared before writes; temp files are written in destination directories; failures delete temp files and preserve final outputs when possible; main in-place plan replacement happens last. See `commands/refine-plan.md:508-572`.
  - Validator gates:
    - input exists: `scripts/validate-refine-plan-io.sh:573-579`
    - input not empty: `scripts/validate-refine-plan-io.sh:581-587`
    - at least one valid non-empty comment block: `scripts/validate-refine-plan-io.sh:589-606`
    - required sections outside ignored regions: `scripts/validate-refine-plan-io.sh:608-637`
    - writable output/input directory depending on in-place vs new-file mode: `scripts/validate-refine-plan-io.sh:639-660`
    - writable or creatable QA directory: `scripts/validate-refine-plan-io.sh:662-678`
  - Exit-code contract is part of the skill API: codes 0-7 are documented at `skills/humanize-refine-plan/SKILL.md:131-143` and matched by command handling at `commands/refine-plan.md:157-175`.

- dependencies_and_callers:
  - Direct child role:
    - `skills/humanize-refine-plan/SKILL.md` is the only file in the assigned directory. It is the Codex/Kimi skill metadata and high-level flow contract.
  - Runtime dependencies:
    - `scripts/validate-refine-plan-io.sh` is the concrete IO and input-shape validator referenced in the skill flow at `skills/humanize-refine-plan/SKILL.md:21-23` and implemented at `scripts/validate-refine-plan-io.sh:1-692`.
    - `prompt-template/plan/refine-plan-qa-template.md` is the QA ledger skeleton referenced by the skill at `skills/humanize-refine-plan/SKILL.md:41` and containing required sections and ledger columns at `prompt-template/plan/refine-plan-qa-template.md:1-119`.
    - `commands/refine-plan.md` is the slash-command execution contract. Its frontmatter exposes the same CLI surface and allowlists the validator, `Read`, `Glob`, `Grep`, `Write`, `Edit`, and `AskUserQuestion` at `commands/refine-plan.md:1-12`.
    - `scripts/lib/config-loader.sh` supplies the shared config precedence model the command is required to reuse. It requires `jq`, validates JSON object layers, ignores malformed optional layers with warnings, and merges default/user/project layers at `scripts/lib/config-loader.sh:17-61` and `scripts/lib/config-loader.sh:63-136`.
    - `config/default_config.json` supplies default `alternative_plan_language` and `gen_plan_mode` values at `config/default_config.json:1-8`.
  - Installation and coordination:
    - `scripts/install-skill.sh` includes `humanize-refine-plan` in `SKILL_NAMES` at `scripts/install-skill.sh:39-44`.
    - The installer validates that every skill has `SKILL.md` and that runtime dependency directories exist at `scripts/install-skill.sh:75-88`.
    - The Codex install documentation lists `humanize-refine-plan` as an installed skill and lists expected runtime dependency directories at `docs/install-for-codex.md:25-32` and `docs/install-for-codex.md:42-68`.
  - Sibling/parent coordination:
    - The directory is one of the Humanize skill set siblings: `skills/humanize`, `skills/humanize-gen-plan`, `skills/humanize-refine-plan`, and `skills/humanize-rlcr`. The refine-plan skill sits between plan generation and RLCR execution: it refines a `gen-plan` artifact but explicitly does not start or perform implementation.

- edge_cases_or_failure_modes:
  - Misclassified as implementation core? No. It is core algorithm documentation/orchestration for plan refinement, not source-code implementation. Its behavior is central because it defines the flow contract and runtime dependencies for comment extraction, classification, schema preservation, QA generation, variant output, and atomic writing.
  - Empty or marker-only comments: empty blocks are removed but do not create ledger IDs or satisfy input validity. See `commands/refine-plan.md:226-228` and validator count behavior at `scripts/validate-refine-plan-io.sh:211-214`.
  - Markers inside fenced code or HTML comments must be ignored. Command requirements are at `commands/refine-plan.md:223-224`; validator fence/HTML tracking appears at `scripts/validate-refine-plan-io.sh:115-180` and `scripts/validate-refine-plan-io.sh:139-158`.
  - Nested comment starts inside an open comment block are fatal parse errors. Required at `commands/refine-plan.md:244-258`; implemented in `scripts/validate-refine-plan-io.sh:227-235`.
  - Stray or wrong end markers are fatal parse errors, implemented in `scripts/validate-refine-plan-io.sh:232-235` and `scripts/validate-refine-plan-io.sh:294-297`.
  - Missing end marker at EOF is fatal and reports opening line, column, nearest heading, and context at `scripts/validate-refine-plan-io.sh:303-311`.
  - Missing required sections produce validator exit code 4 and list missing sections at `scripts/validate-refine-plan-io.sh:621-637`.
  - Output directory not found or not writable produces exit code 5 for new-file mode; in-place mode instead checks the input directory writability. See `scripts/validate-refine-plan-io.sh:639-660`.
  - QA directory may be auto-created, but failure to create or write to it produces exit code 6 at `scripts/validate-refine-plan-io.sh:662-678`.
  - Unsupported CLI alternate language is a hard stop, while unsupported config alternate language only logs a warning and disables variant generation; see `commands/refine-plan.md:140-147`.
  - Same-language or English alternate language is a no-op and should not create variants, per `skills/humanize-refine-plan/SKILL.md:124-129` and `commands/refine-plan.md:140-147`.
  - If ambiguity remains, `discussion` mode asks the minimum user question; `direct` mode records the smallest safe assumption in QA. See `skills/humanize-refine-plan/SKILL.md:31-34` and `commands/refine-plan.md:306-312`.
  - If any decision materially affects implementation direction and is deferred, convergence must be `partially_converged`, per `commands/refine-plan.md:603-607`.
  - In this read-only branch export, `git status` could not be used because the export has no `.git` metadata and the sandbox blocked temporary cache creation; this did not block recursive filesystem inspection or line-numbered reads.

- validation_or_tests:
  - Static validation coverage exists in `tests/test-refine-plan.sh`, which declares it validates the command frontmatter/workflow, validator exit codes 0-7, comment extraction/classification requirements, language variants, atomic write requirements, and installation wiring at `tests/test-refine-plan.sh:1-12`.
  - Positive tests assert core files exist and the validator is executable at `tests/test-refine-plan.sh:639-657`.
  - Command metadata tests assert the argument hint, validator allowlist, `AskUserQuestion`, hidden command flag, and ultrathink instruction at `tests/test-refine-plan.sh:660-674`.
  - Planning-only and sequential workflow constraints are asserted at `tests/test-refine-plan.sh:676-701`.
  - IO validation exit-code documentation is checked at `tests/test-refine-plan.sh:703-713`.
  - Comment extraction requirements, ignored regions, parse-error categories, metadata capture, and empty-comment rejection are checked at `tests/test-refine-plan.sh:715-730`.
  - Classification, multi-intent splitting, ambiguity handling, and dispositions are checked at `tests/test-refine-plan.sh:732-748`.
  - Plan schema preservation, in-place/default output rules, QA path derivation, and v1 CLI constraints are checked at `tests/test-refine-plan.sh:750-764`.
  - Alternate-language mappings and variant filename rules are checked at `tests/test-refine-plan.sh:766-788`.
  - Atomic write requirements and QA template coverage are checked at `tests/test-refine-plan.sh:790-817`.
  - Skill/install wiring coverage asserts `user-invocable: false`, `install-skill.sh` registration, and documentation mentions at `tests/test-refine-plan.sh:819-855`.
  - Validator behavior tests cover invalid args, unexpected `--alt-language`, mutually exclusive modes, missing input, empty input, no comments, HTML-only markers, fence-only markers, empty comments, unterminated comments, nested comments, missing sections, sections only in ignored regions, output permissions, QA path failures, successful in-place mode, mixed valid/ignored/empty markers, and successful new-file mode at `tests/test-refine-plan.sh:1044-1343`.
  - I did not run the tests because the assignment requires research notes only and this branch export is read-only; several tests create fixtures, directories, and chmod state.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 1 item evidence section present
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`