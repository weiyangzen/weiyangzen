# agent_060 use-realpath4everything 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`

## Item Evidence

### USE_REALPATH4EVERYTHING-HZ-060 `file` `templates/bitlesson.md`
- cursor: `[_]`
- core_role:
  `templates/bitlesson.md` is the seed template for each project’s BitLesson knowledge base, normally materialized at `.humanize/bitlesson.md`. It defines the canonical memory schema used by the RLCR workflow to store reusable lessons from earlier rounds. The file itself is declarative, but it participates in the core memory workflow because `scripts/setup-rlcr-loop.sh` initializes project state from it before creating loop state, and later selector/stop-gate logic consumes the resulting BitLesson file.
- algorithmic_behavior:
  The template establishes an initially empty knowledge base with a required entry grammar. Lines `templates/bitlesson.md:1-3` identify the file as project-specific reusable memory. Lines `templates/bitlesson.md:5-19` define the strict entry format and field order. Lines `templates/bitlesson.md:21-23` create the insertion area under `## Entries`.
  Initialization behavior is implemented by `scripts/bitlesson-init.sh`: it requires `--project-root` and `--template`, defaults the destination relpath to `.humanize/bitlesson.md`, resolves the project root with `pwd -P`, and copies the template only if the destination file is missing (`scripts/bitlesson-init.sh:18-20`, `scripts/bitlesson-init.sh:48-67`, `scripts/bitlesson-init.sh:75-86`). `scripts/setup-rlcr-loop.sh` wires this exact template path into loop setup (`scripts/setup-rlcr-loop.sh:860-866`).
  Runtime behavior after initialization is split across selection and validation. The round prompt requires agents to read the initialized file, run `bitlesson-selector`, follow selected IDs or `NONE`, and report a `## BitLesson Delta` section (`scripts/setup-rlcr-loop.sh:1354-1365`). The selector reads the BitLesson file and routes lesson selection based on recorded lessons (`scripts/bitlesson-select.sh:99-108`, `scripts/bitlesson-select.sh:148-179`). The stop hook invokes the delta validator for non-finalize rounds when BitLesson is required (`hooks/loop-codex-stop-hook.sh:823-836`).
- inputs_outputs_state:
  Inputs are the template file itself, a project root, and an optional relative destination path passed to `bitlesson-init.sh` (`scripts/bitlesson-init.sh:7-14`). The output of initialization is a project-local BitLesson file path printed on stdout (`scripts/bitlesson-init.sh:88`) and, if absent, a copied `.humanize/bitlesson.md` file with the strict schema from `templates/bitlesson.md`.
  The state transition is: no BitLesson file exists -> `.humanize/bitlesson.md` is created from this template -> future rounds append concrete lessons under `## Entries` -> selector reads concrete lessons for task-specific memory recall -> stop gate validates summary deltas against concrete `Lesson ID:` records. Existing BitLesson files are preserved, not overwritten (`scripts/bitlesson-init.sh:12-13`, `scripts/bitlesson-init.sh:83-86`).
- gates_or_invariants:
  The template’s main invariant is field order for every entry: heading, `Lesson ID`, `Scope`, `Problem Description`, `Root Cause`, `Solution`, `Constraints`, `Validation Evidence`, and `Source Rounds` (`templates/bitlesson.md:7-19`). The expected concrete ID shape is `BL-YYYYMMDD-short-name`, shown as a placeholder in the template (`templates/bitlesson.md:11`) and enforced by the delta validator for add/update summaries (`scripts/bitlesson-validate-delta.sh:322-366`).
  Initialization gates reject missing project root, missing template, non-directory project root, nonexistent template, absolute destination relpaths, and relpaths containing `..` (`scripts/bitlesson-init.sh:48-72`). The destination may not already exist as a non-regular file (`scripts/bitlesson-init.sh:78-80`).
  Stop-gate invariants require exactly one BitLesson Delta action of `none`, `add`, or `update` (`scripts/bitlesson-validate-delta.sh:202-218`). `Action: none` must use no concrete IDs or `NONE`; if the knowledge base has zero concrete lessons and empty-none is disallowed, it blocks (`scripts/bitlesson-validate-delta.sh:242-267`). `Action: add` and `Action: update` require concrete IDs, non-placeholder notes, an existing BitLesson file, valid ID syntax, and matching `Lesson ID:` entries in the BitLesson file (`scripts/bitlesson-validate-delta.sh:268-384`).
- dependencies_and_callers:
  Direct caller: `scripts/setup-rlcr-loop.sh` sets `PLUGIN_BITLESSON_TEMPLATE="$SCRIPT_DIR/../templates/bitlesson.md"` and calls `scripts/bitlesson-init.sh` with destination `.humanize/bitlesson.md` (`scripts/setup-rlcr-loop.sh:860-866`).
  Direct copier/initializer: `scripts/bitlesson-init.sh` copies this template into project-local state without overwriting existing state (`scripts/bitlesson-init.sh:83-86`).
  Downstream consumers of the initialized file include `scripts/bitlesson-select.sh`, which reads the file content into the selector prompt (`scripts/bitlesson-select.sh:99`, `scripts/bitlesson-select.sh:161-164`), and `scripts/bitlesson-validate-delta.sh`, which scans `Lesson ID:` lines to count concrete entries and validate summary-declared IDs (`scripts/bitlesson-validate-delta.sh:227-239`, `scripts/bitlesson-validate-delta.sh:328-336`).
  Documentation confirms the intended workflow: each project keeps `.humanize/bitlesson.md`, it is initialized from `templates/bitlesson.md`, tasks run through `scripts/bitlesson-select.sh`, and the stop gate validates `## BitLesson Delta` (`docs/bitlesson.md:27-35`).
- edge_cases_or_failure_modes:
  If the initialized file remains only the template, the validator treats the placeholder `Lesson ID: <BL-YYYYMMDD-short-name>` as non-concrete and counts zero concrete lessons (`scripts/bitlesson-validate-delta.sh:227-239`). This correctly supports the “empty KB” gate.
  A subtle selector edge case exists: `scripts/bitlesson-select.sh` decides whether a BitLesson file has recorded lessons by grepping for a `## Lesson:` heading anywhere in the file (`scripts/bitlesson-select.sh:105-108`). Because the template includes `## Lesson: <unique-id>` inside a fenced example (`templates/bitlesson.md:9-19`), a file copied directly from this template can look non-empty to the selector even though the validator considers it empty. Existing routing tests cover a different placeholder shape without a `## Lesson:` heading and expect `LESSON_IDS: NONE` without invoking a model (`tests/test-bitlesson-select-routing.sh:18-26`, `tests/test-bitlesson-select-routing.sh:420-436`), so this specific template-vs-selector interaction appears undercovered.
  Other failure modes include missing template file during setup, destination `.humanize/bitlesson.md` being a directory or special file, unsafe destination relpath, whitespace-only BitLesson files causing selector failure, and summary deltas referencing IDs not present in the knowledge base (`scripts/bitlesson-init.sh:65-80`, `scripts/bitlesson-select.sh:100-102`, `scripts/bitlesson-validate-delta.sh:369-384`).
- validation_or_tests:
  Direct initialization behavior is implied by `scripts/bitlesson-init.sh` and documented in `docs/bitlesson.md:29-35`; I did not find a dedicated test named for `bitlesson-init.sh`.
  Selector routing tests cover placeholder/no-recorded-lesson behavior, provider routing, and real lesson fixtures (`tests/test-bitlesson-select-routing.sh:18-45`, `tests/test-bitlesson-select-routing.sh:420-436`). Delta validation tests cover notes requirements, fenced/comment-hidden delta rejection, and passing add/update summaries with concrete IDs (`tests/test-bitlesson-validate-delta.sh:21-33`, `tests/test-bitlesson-validate-delta.sh:101-152`). Template-reference tests verify prompt-template references, but they do not directly validate `templates/bitlesson.md` (`tests/test-template-references.sh:51-111`).
  I did not run the test suite because this worker task is read-only research; file inspection was sufficient for evidence. A `git rev-parse` probe also failed because this branch export does not expose a usable `.git` directory under the restricted read-only environment, so source commit is taken from the scheduler metadata.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `1 evidence section present for the single assigned item`
- missing_items: `0`
- duplicate_items: `0`
- final_worker_status: `complete`