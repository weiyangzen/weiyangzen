# agent_190 use-realpath4everything 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`

## Item Evidence

### USE_REALPATH4EVERYTHING-HZ-190 `file` `tests/robustness/test-plan-file-robustness.sh`
- cursor: `[_]`
- core_role:
  This shell script is an executable robustness specification for plan-file validation in `scripts/setup-rlcr-loop.sh`. Its main core role is to prove that RLCR loop setup accepts sufficiently detailed markdown plans and rejects missing, empty, comment-only, unreadable, symlinked, or otherwise unsafe plan inputs before creating loop state. The file explicitly states that it covers empty files, very large files, mixed line endings, disappearance, and content-line counting at `tests/robustness/test-plan-file-robustness.sh:3-10`.

- algorithmic_behavior:
  The script runs under `set -euo pipefail` at `tests/robustness/test-plan-file-robustness.sh:13`, creates an isolated temporary environment, and installs a mock `codex` executable so production setup does not call the real Codex binary at `tests/robustness/test-plan-file-robustness.sh:18-40`.
  Its central harness is `test_plan_validation()` at `tests/robustness/test-plan-file-robustness.sh:48-106`. That function deletes any existing `$TEST_DIR/.humanize/rlcr`, invokes `scripts/setup-rlcr-loop.sh` with `CLAUDE_PROJECT_DIR="$TEST_DIR"` and a relative plan path, captures stdout/stderr into a temporary file, and classifies the production result as accepted or rejected by matching known validation messages and loop-state side effects.
  The production algorithm it exercises is in `scripts/setup-rlcr-loop.sh`: project-root resolution at `scripts/setup-rlcr-loop.sh:326-330`, dependency checks at `scripts/setup-rlcr-loop.sh:340-363`, plan path validation at `scripts/setup-rlcr-loop.sh:445-609`, and content validation at `scripts/setup-rlcr-loop.sh:611-676`.
  The test’s local `count_content_lines()` helper at `tests/robustness/test-plan-file-robustness.sh:129-169` mirrors the production content-counting rule: skip blank lines, single-line HTML comments, multi-line HTML comment bodies, and lines beginning with `#`; count every other line as meaningful content.
  The positive production cases are valid markdown, exactly three content lines after comments, a standard-size plan, rich markdown, a 1MB-plus plan, and mixed CRLF/LF line endings at `tests/robustness/test-plan-file-robustness.sh:178-366`.
  The negative or edge cases cover empty files, comment-only files, binary/null content readability, long lines, special characters, whitespace-only files, complex comments, missing files, unreadable files, symlink files, directory paths, and disappeared files at `tests/robustness/test-plan-file-robustness.sh:300-551`.

- inputs_outputs_state:
  Inputs are repo-relative plan paths passed to `test_plan_validation()` and resolved by production setup under the temporary repository root via `CLAUDE_PROJECT_DIR="$TEST_DIR"` at `tests/robustness/test-plan-file-robustness.sh:61`. The root resolver honors `CLAUDE_PROJECT_DIR` first and canonicalizes it with `realpath`/fallback behavior through `hooks/lib/project-root.sh:41-52`.
  The test constructs an isolated git repository at `tests/robustness/test-plan-file-robustness.sh:112-122`, with `.gitignore` ignoring generated plan files so production’s default “plan file must be gitignored” policy does not block normal content-validation cases.
  Observable outputs are pass/fail counters from `tests/test-helpers.sh:30-44`, final summary and exit status from `tests/test-helpers.sh:58-77`, captured production output files, and possible production loop state under `$TEST_DIR/.humanize/rlcr`.
  Production accepted-state indicators are: dependency/setup progress messages, the message `start-rlcr-loop activated`, or creation of a loop directory with `state.md`, checked at `tests/robustness/test-plan-file-robustness.sh:70-95`.
  Production rejected-state indicators are specific plan validation errors: too simple, insufficient content, not found, not readable, or symbolic link, matched at `tests/robustness/test-plan-file-robustness.sh:64-68`.

- gates_or_invariants:
  The production plan path must be relative, contain no spaces, avoid shell metacharacters, not be a symlink itself, have no symlink parent segment, exist, be readable, resolve within the project directory, and not live inside a git submodule; those gates are implemented at `scripts/setup-rlcr-loop.sh:455-556`.
  Tracking policy is a separate gate: without `--track-plan-file`, the plan must not be tracked in git; with `--track-plan-file`, it must be tracked and clean. This is enforced at `scripts/setup-rlcr-loop.sh:562-607`.
  Content gates require at least five physical lines and at least three meaningful content lines at `scripts/setup-rlcr-loop.sh:618-671`. Headings beginning with `#` are intentionally treated as comments, not content, per `scripts/setup-rlcr-loop.sh:628-631` and the mirrored helper at `tests/robustness/test-plan-file-robustness.sh:160-163`.
  The large-file gate is behavioral rather than a hard size limit: Test 7 generates more than 1MB and expects production validation to finish successfully, explicitly guarding a prior `sed | head` SIGPIPE-style issue at `tests/robustness/test-plan-file-robustness.sh:325-350`.
  The test assumes the setup script is run from inside the temporary git repo because production still uses bare `git rev-parse` for initial repository checks at `scripts/setup-rlcr-loop.sh:433-442`, even though later git operations use `-C "$PROJECT_ROOT"`.

- dependencies_and_callers:
  Direct dependencies are `scripts/setup-rlcr-loop.sh`, `tests/test-helpers.sh`, `scripts/portable-timeout.sh`, `hooks/lib/loop-common.sh`, and `hooks/lib/project-root.sh`. The setup script sources timeout and loop-common helpers at `scripts/setup-rlcr-loop.sh:25-33`.
  External command dependencies include `bash`, `git`, `jq`, `wc`, `grep`, `sed`, `head`, `tail`, `date`, `mktemp`, `chmod`, `ln`, and `codex`. The test mocks only `codex` at `tests/robustness/test-plan-file-robustness.sh:26-40`; `jq` and `git` remain real production dependencies checked at `scripts/setup-rlcr-loop.sh:340-352`.
  The broader test suite calls this script from `tests/run-all-tests.sh:102-109`, where it is listed among other robustness tests.
  Production setup consumes the plan further after validation by copying it into the loop directory at `scripts/setup-rlcr-loop.sh:829-850`, creating state and prompt artifacts based on the validated plan.

- edge_cases_or_failure_modes:
  Several later edge cases are local predicate/helper checks rather than production-validation calls. Binary content, long lines, special characters, whitespace-only counting, nested comments, unreadable-file detection, symlink detection, directory detection, and null-byte line counting are checked locally at `tests/robustness/test-plan-file-robustness.sh:368-525`; they do not all invoke `test_plan_validation()`.
  The harness treats `must be gitignored` as an accepted validation outcome at `tests/robustness/test-plan-file-robustness.sh:76-80`, but production emits that before content validation at `scripts/setup-rlcr-loop.sh:597-607`. In the current test repo setup, generated plan files are ignored, so this should not mask the intended content cases; if the gitignore setup regressed, it could create false positives for some plans.
  The script creates an initial `TEST_DIR`, cache directory, and mock codex, then sources `tests/test-helpers.sh` and calls `setup_test_dir`, which reassigns `TEST_DIR` and replaces the exit trap at `tests/robustness/test-plan-file-robustness.sh:18-40` and `tests/robustness/test-plan-file-robustness.sh:108-110`. That leaves `PATH` pointing to the first temp directory’s mock codex and `XDG_CACHE_HOME` pointing to the first temp directory, while the git repo lives in the second temp directory. This is functional during one process but is a cleanup/isolation sharp edge.
  A plan with three meaningful content lines but fewer than five physical lines would still be rejected because physical line count is checked first at `scripts/setup-rlcr-loop.sh:618-626`.
  Null bytes are only tested for `wc` readability at `tests/robustness/test-plan-file-robustness.sh:514-525`; the production Bash `read` loop is not directly exercised with null bytes by this case.

- validation_or_tests:
  The file defines 19 named tests and exits through `print_test_summary "Plan File Robustness Test Summary"` at `tests/robustness/test-plan-file-robustness.sh:553-558`.
  Production-invoking assertions include valid plan acceptance, minimum content acceptance, standard and rich markdown acceptance, empty/comment-only rejection, 1MB-plus plan acceptance, mixed line-ending acceptance, and missing/disappeared plan rejection.
  Local robustness assertions cover content-line helper behavior and filesystem predicates for unreadable files, symlinks, directories, null bytes, long lines, and special characters.
  I inspected the file and related implementation only; I did not execute the test suite in this read-only research pass.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 1 unique assigned item section above
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`