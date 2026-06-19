# agent_022 use-realpath4everything 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`

## Item Evidence

### USE_REALPATH4EVERYTHING-HZ-022 `directory` `skills/humanize-gen-plan`
- cursor: `[_]`
- core_role:
  - `skills/humanize-gen-plan` is a single-file skill directory containing only `skills/humanize-gen-plan/SKILL.md`. The file declares a non-user-invocable flow skill named `humanize-gen-plan`, with model invocation disabled, whose role is to turn a draft document into a structured implementation plan with goals, AC-format acceptance criteria, path boundaries, feasibility hints, and dependencies.
  - The directory is core algorithm material because it specifies the high-level state machine for plan generation. The actual executable validation gate is delegated to `scripts/validate-gen-plan-io.sh`, while the richer Claude command surface is `commands/gen-plan.md`, and the generated plan skeleton is `prompt-template/plan/gen-plan-template.md`.

- algorithmic_behavior:
  - The flow in `skills/humanize-gen-plan/SKILL.md:19-47` defines the algorithm as a staged pipeline:
    - begin, validate input/output paths using `{{HUMANIZE_RUNTIME_ROOT}}/scripts/validate-gen-plan-io.sh --input <draft> --output <plan>`;
    - stop on validation failure;
    - read the draft and reject it if unrelated to the repository;
    - analyze for clarity, consistency, completeness, and functionality;
    - loop through user resolution via `AskUserQuestion` when issues remain;
    - confirm quantitative metrics as hard requirements or trend targets;
    - generate the structured plan;
    - write the output while preserving the draft;
    - review and fix inconsistencies;
    - optionally ask for language unification;
    - report success with plan path, AC count, and language status.
  - The concrete validator canonicalizes input and output paths before checking them: `scripts/validate-gen-plan-io.sh:98-101` uses `realpath -m` for `INPUT_FILE` and `OUTPUT_FILE`, falling back to the original string if `realpath` fails. This is directly relevant to the branch’s realpath-focused behavior.
  - The command-level implementation expands the skill into a stricter multi-phase command. `commands/gen-plan.md:32-45` requires sequential phases from execution-mode setup through config load, IO validation, relevance checking, Codex first-pass analysis, Claude plan synthesis, convergence, user-disagreement resolution, final generation, write, optional translation, and optional RLCR auto-start.
  - The command is explicitly planning-only before optional handoff: `commands/gen-plan.md:20-28` permits only the output plan file and optional translated variant before any auto-start, and forbids source changes, commits, or PRs during plan generation.
  - The template defines required output structure: acceptance criteria with positive and negative tests, path boundaries, feasibility hints, dependency milestones, task routing tags, Claude-Codex deliberation, pending user decisions, code-style constraints, and translation conventions in `prompt-template/plan/gen-plan-template.md:1-120`.

- inputs_outputs_state:
  - Required inputs are `--input <path/to/draft.md>` and `--output <path/to/plan.md>`, documented in `skills/humanize-gen-plan/SKILL.md:49-54`.
  - Validator argument state includes `INPUT_FILE`, `OUTPUT_FILE`, `AUTO_START_RLCR_IF_CONVERGED`, `GEN_PLAN_MODE_DISCUSSION`, and `GEN_PLAN_MODE_DIRECT` initialized in `scripts/validate-gen-plan-io.sh:29-33`, then mutated by the argument parser in `scripts/validate-gen-plan-io.sh:35-74`.
  - Output state is a new plan file. The validator is side-effect-free and does not create it, per `commands/gen-plan.md:150`. The command later creates the output by copying the template and appending the original draft after relevance passes, described at `commands/gen-plan.md:176-180`.
  - The skill’s output plan shape includes `Goal Description`, `Acceptance Criteria`, `Path Boundaries`, `Dependencies and Sequence`, and `Implementation Notes` in `skills/humanize-gen-plan/SKILL.md:55-94`.
  - The richer command state includes `PLAN_CONVERGENCE_STATUS`, `HUMAN_REVIEW_REQUIRED`, pending `DEC-N` decisions, optional `ALT_PLAN_LANGUAGE` / `ALT_PLAN_LANG_CODE`, and optional auto-start state. Direct mode sets partial convergence and requires human review in `commands/gen-plan.md:255-258`; manual review gating is defined in `commands/gen-plan.md:305-312`; pending decisions are consolidated in `commands/gen-plan.md:314-329`.
  - Optional translated output variant is constructed by inserting `_<code>` before the final extension or appending it to extensionless filenames, per `commands/gen-plan.md:569-592` and `prompt-template/plan/gen-plan-template.md:110-120`.
  - Optional RLCR handoff occurs only when auto-start is requested, convergence is complete, mode is discussion, and no pending decisions remain, in `commands/gen-plan.md:594-614`.

- gates_or_invariants:
  - Skill-level gates:
    - validation must pass before draft read;
    - relevance must pass before plan generation;
    - analysis issues must be resolved or acknowledged before generation;
    - metrics must be clarified when present;
    - inconsistencies must be fixed before success;
    - multiple-language content may trigger user language unification.
  - Validator gates:
    - `--discussion` and `--direct` are mutually exclusive, enforced in `scripts/validate-gen-plan-io.sh:76-80`;
    - required `--input` and `--output` are enforced in `scripts/validate-gen-plan-io.sh:82-91`;
    - direct mode plus auto-start prints a note that auto-start is skipped, `scripts/validate-gen-plan-io.sh:93-96`;
    - input must exist and be non-empty, `scripts/validate-gen-plan-io.sh:108-122`;
    - output directory must exist, `scripts/validate-gen-plan-io.sh:124-130`;
    - output path must not be a directory or existing file, `scripts/validate-gen-plan-io.sh:132-145`;
    - output directory must be writable, `scripts/validate-gen-plan-io.sh:147-153`;
    - plan template must exist or the validator exits as plugin configuration error, `scripts/validate-gen-plan-io.sh:162-175`.
  - Command-level invariants:
    - phases must execute strictly in order and must not be parallelized across phases, `commands/gen-plan.md:32-35`;
    - config must be loaded through `scripts/lib/config-loader.sh`, not by reading `.humanize/config.json` directly, `commands/gen-plan.md:62-75`;
    - direct mode cannot satisfy auto-start convergence conditions, `commands/gen-plan.md:255-258`;
    - the original draft is treated as authoritative human input and must be preserved, `commands/gen-plan.md:301-304` and `commands/gen-plan.md:521-523`;
    - every task must have exactly one routing tag, `coding` or `analyze`, `commands/gen-plan.md:447-457` and `commands/gen-plan.md:529`;
    - implementation code/comments must not contain plan-specific progress terminology such as `AC-`, `Milestone`, `Step`, or `Phase`, `commands/gen-plan.md:477-482`.

- dependencies_and_callers:
  - Runtime root hydration is explicit. `skills/humanize-gen-plan/SKILL.md:13-17` contains `{{HUMANIZE_RUNTIME_ROOT}}`; `scripts/install-skill.sh:167-191` replaces that placeholder with the installed runtime root for all Humanize skills. Manual Kimi install docs perform the same placeholder replacement in `docs/install-for-kimi.md:65-69`.
  - The installer treats `humanize-gen-plan` as one of the four synced skills in `scripts/install-skill.sh:39-44`, validates each skill has `SKILL.md` in `scripts/install-skill.sh:75-87`, and copies runtime dependencies such as `scripts`, `hooks`, `prompt-template`, `templates`, `config`, and `agents` under the installed `humanize` runtime bundle in `scripts/install-skill.sh:155-164`.
  - The sibling parent skill exposes the same validator path for generating a plan at `skills/humanize/SKILL.md:97-103` and repeats the validator exit-code contract at `skills/humanize/SKILL.md:221-229`.
  - `commands/gen-plan.md` is the principal richer caller/command surface. Its frontmatter allows the validator, `ask-codex.sh`, `setup-rlcr-loop.sh`, `Read`, `Glob`, `Grep`, `Task`, `Write`, and `AskUserQuestion` in `commands/gen-plan.md:1-14`.
  - The relevance subagent is `agents/draft-relevance-checker.md`, declared for gen-plan relevance validation in `agents/draft-relevance-checker.md:1-6`. It explores repository docs and structure, analyzes semantic relevance, and must return `RELEVANT:` or `NOT_RELEVANT:` per `agents/draft-relevance-checker.md:12-30`.
  - The plan template dependency is `prompt-template/plan/gen-plan-template.md`; the validator locates it through `CLAUDE_PLUGIN_ROOT` or script-relative fallback in `scripts/validate-gen-plan-io.sh:162-169`.

- edge_cases_or_failure_modes:
  - Missing `--input`, missing `--output`, flag-as-value, unknown flags, and help all route through usage and exit code 6 in `scripts/validate-gen-plan-io.sh:16-27` and `scripts/validate-gen-plan-io.sh:35-74`.
  - Mutually specifying `--discussion` and `--direct` exits 6 at `scripts/validate-gen-plan-io.sh:76-80`.
  - `realpath -m` is used even for paths that may not yet exist. This is appropriate for output path canonicalization, but the fallback to the raw path means validation can still proceed on systems where `realpath` is unavailable or behaves differently.
  - Existing output files and output directories both fail with exit code 4, while nonexistent output directories fail with exit code 3. The validator does not create directories.
  - `/dev/null` as input is accepted as an existing non-empty file on some systems, which the tests use for flag-recognition checks; that means those tests validate argument recognition rather than semantic draft suitability.
  - Template lookup failure is treated as plugin configuration error and exits 7, so a copied skill without the runtime bundle or template tree cannot proceed.
  - Draft relevance checking is intentionally lenient. The relevance agent says to mark as relevant when in doubt in `agents/draft-relevance-checker.md:31-36`, so unrelated drafts should be rejected only when clearly unrelated.
  - Auto-start is deliberately narrow. Direct mode never qualifies; discussion mode still requires convergence and zero pending decisions, so unresolved `DEC-N` entries block direct RLCR start.
  - The skill itself says to write with an Edit tool to preserve the draft, `skills/humanize-gen-plan/SKILL.md:37`, while the richer command first copies the template and appends the draft, then requires Edit rather than Write for final content updates in `commands/gen-plan.md:533-543`.

- validation_or_tests:
  - `tests/test-gen-plan.sh` verifies the command exists, has description, allowed tools, argument hint, relevance agent, Codex integration, auto-start option, and direct-mode convergence behavior in `tests/test-gen-plan.sh:54-140`.
  - The same test file exercises `validate-gen-plan-io.sh` exit-code behavior for missing values, unknown options, nonexistent input, empty input, missing output directory, existing output file, output directory as output, valid paths, auto-start flag acceptance, discussion/direct flag recognition, mutual exclusion, and help behavior in `tests/test-gen-plan.sh:557-705`.
  - Template consistency is validated by comparing the markdown plan-structure block embedded in `commands/gen-plan.md` to `prompt-template/plan/gen-plan-template.md` in `tests/test-gen-plan.sh:708-715`.
  - `tests/test-template-references.sh` validates that template files referenced by shell template loading exist and scans the `prompt-template` tree for reference completeness; this is broader than gen-plan but protects the same runtime-template dependency class, especially missing-template failures, per `tests/test-template-references.sh:1-10` and `tests/test-template-references.sh:121-142`.
  - I did not run the tests because the task requested research notes only and the branch export is read-only. I also avoided git-based validation after `git` reported no usable repository metadata in this export and macOS tooling attempted restricted cache writes.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 1/1 represented once in the Item Evidence section
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`