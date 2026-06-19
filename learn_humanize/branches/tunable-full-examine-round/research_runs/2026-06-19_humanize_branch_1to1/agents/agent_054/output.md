# agent_054 tunable-full-examine-round 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `67aa7bab09f0d0e36ac403264eed6989b09aada5`

## Item Evidence

### TUNABLE_FULL_EXAMINE_ROUND-HZ-054 `file` `tests/test-gen-plan.sh`
- cursor: `[_]`
- core_role: Executable specification for the `/humanize:gen-plan` command contract. It validates that the plugin exposes the expected command metadata, the draft relevance agent metadata, version-synchronization surfaces, frontmatter/name/model/content constraints, and the IO validation script’s public exit-code behavior. It is not the implementation of plan generation itself; it is a shell-based contract test for the command and its supporting artifacts.
- algorithmic_behavior:
  - Initializes strict shell behavior with `set -euo pipefail`, derives `SCRIPT_DIR`, `PROJECT_ROOT`, `COMMANDS_DIR`, and `AGENTS_DIR` from the test file location, then accumulates result state in `TESTS_PASSED` and `TESTS_FAILED` through `pass()` and `fail()` helpers at `tests/test-gen-plan.sh:9-40`.
  - Positive test block PT-1 through PT-9 verifies stable repo surfaces:
    - `commands/gen-plan.md` exists at `tests/test-gen-plan.sh:54-64`.
    - `commands/gen-plan.md` has a non-empty YAML `description:` extracted by `sed` from the first frontmatter block at `tests/test-gen-plan.sh:66-78`.
    - `allowed-tools:` and `argument-hint:` are present in the command file at `tests/test-gen-plan.sh:80-104`.
    - `agents/draft-relevance-checker.md` exists and has exact `name: draft-relevance-checker`, exact `model: haiku`, and a `tools:` field at `tests/test-gen-plan.sh:106-157`.
    - `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, and `README.md` all expose the same version string, parsed with simple `grep`/`tr` pipelines at `tests/test-gen-plan.sh:159-180`.
  - Negative/validation block creates temporary invalid fixtures under `mktemp -d` and removes them via `trap` at `tests/test-gen-plan.sh:191-193`. It defines local validators rather than invoking a shared validator for command metadata:
    - `validate_name()` accepts only lowercase names matching `^[a-z][a-z0-9-]*$` at `tests/test-gen-plan.sh:195-199`.
    - `check_yaml_frontmatter()` requires first line `---` and a `description:` key at `tests/test-gen-plan.sh:201-206`.
    - `check_agent_yaml_frontmatter()` requires first line `---`, `name:`, and `description:` at `tests/test-gen-plan.sh:208-214`.
    - `check_yaml_syntax()` extracts frontmatter with `awk` and then accepts blank/comment lines, key-value lines, list entries, or quoted continuation-style lines at `tests/test-gen-plan.sh:304-319`.
    - `validate_model_name()` accepts exact short aliases `opus`, `sonnet`, `haiku`, or model IDs starting with `claude-`, `gpt-`, `o<digit>`, or `gemini-` at `tests/test-gen-plan.sh:350-358`.
  - Negative cases confirm the local validators reject uppercase names, names with spaces, missing frontmatter, missing `description:`, malformed YAML, invalid/empty/partial model aliases, and non-English/emoji/CJK content in the two command surfaces at `tests/test-gen-plan.sh:216-423`.
  - Script Tests section treats `scripts/validate-gen-plan-io.sh` as an executable dependency and asserts the command-line parser and path checks produce exact exit codes:
    - missing `--input` value, missing `--output` value, flag-as-value, unknown option, and `--help` must exit `6` at `tests/test-gen-plan.sh:438-539`.
    - nonexistent input exits `1`, empty input exits `2`, missing output directory exits `3`, existing output file exits `4`, output path as directory exits `4`, and valid paths exit `0` at `tests/test-gen-plan.sh:474-530`.
  - Final transition prints a summary and exits `0` only when `TESTS_FAILED` is zero; otherwise it exits `1` at `tests/test-gen-plan.sh:544-562`.
- inputs_outputs_state:
  - Inputs:
    - Repository-root files resolved relative to the test script: `commands/gen-plan.md`, `agents/draft-relevance-checker.md`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `README.md`, and `scripts/validate-gen-plan-io.sh` at `tests/test-gen-plan.sh:11-14`, `tests/test-gen-plan.sh:59`, `tests/test-gen-plan.sh:111`, `tests/test-gen-plan.sh:164-166`, and `tests/test-gen-plan.sh:431`.
    - Temporary fixture files created in a `mktemp -d` directory for invalid metadata and IO path cases at `tests/test-gen-plan.sh:191-193`, `tests/test-gen-plan.sh:253-272`, `tests/test-gen-plan.sh:321-327`, and `tests/test-gen-plan.sh:483-525`.
  - Outputs:
    - Human-readable PASS/FAIL lines emitted by `pass()`/`fail()` at `tests/test-gen-plan.sh:25-40`.
    - Aggregate summary lines for passed and failed counts at `tests/test-gen-plan.sh:544-552`.
    - Process exit `0` on full success and `1` on any failed assertion at `tests/test-gen-plan.sh:554-562`.
    - On the valid IO path case, the called validator creates `new-output.md` inside the temporary script-test directory because `scripts/validate-gen-plan-io.sh` copies the plan template and appends draft content on success at `scripts/validate-gen-plan-io.sh:126-160`.
  - State transitions:
    - `TESTS_PASSED` increments by one for every satisfied assertion and `TESTS_FAILED` increments by one for every failed assertion at `tests/test-gen-plan.sh:26-40`.
    - `EXIT_CODE` is reset to `0` before each validator invocation, then captures nonzero command exits through `|| EXIT_CODE=$?` at `tests/test-gen-plan.sh:438-539`.
    - Temporary directories are scheduled for cleanup with `trap`, but the script installs two separate `trap "rm -rf ..."` handlers: the second one for `SCRIPT_TEST_DIR` at `tests/test-gen-plan.sh:435-436` replaces the earlier `TEST_FIXTURES_DIR` trap from `tests/test-gen-plan.sh:191-193`, which means the first temp directory may not be cleaned when the validator script is executable.
- gates_or_invariants:
  - Command metadata invariant: `commands/gen-plan.md` must exist, include `description:`, `allowed-tools:`, and `argument-hint:` in/near frontmatter at `tests/test-gen-plan.sh:54-104`. The referenced command file declares `description`, `argument-hint`, and `allowed-tools` at `commands/gen-plan.md:1-12`.
  - Agent metadata invariant: `agents/draft-relevance-checker.md` must exist with exact `name: draft-relevance-checker`, exact `model: haiku`, and a `tools:` line at `tests/test-gen-plan.sh:106-157`. The agent file currently has those fields at `agents/draft-relevance-checker.md:1-6`.
  - Version invariant: plugin metadata, marketplace metadata, and README version must match at `tests/test-gen-plan.sh:168-177`; current surfaces show `1.6.0` in `.claude-plugin/plugin.json:4`, `.claude-plugin/marketplace.json:11`, and `README.md:3`.
  - Naming invariant: command/agent IDs must be lowercase kebab-case beginning with a letter at `tests/test-gen-plan.sh:195-199`, then checked against `gen-plan` and `draft-relevance-checker` at `tests/test-gen-plan.sh:234-245`.
  - Frontmatter invariant: command files must start with `---` and contain `description:`; agent files must start with `---` and contain `name:` plus `description:` at `tests/test-gen-plan.sh:201-214`.
  - Model invariant: short model aliases require exact matches, while full IDs are accepted by prefix; partial aliases like `opus-v2`, `haiku123`, and `sonnet-fast` must fail at `tests/test-gen-plan.sh:350-389`.
  - Content invariant: `commands/gen-plan.md` and `agents/draft-relevance-checker.md` should not contain CJK or emoji code ranges according to `grep -P` at `tests/test-gen-plan.sh:403-423`.
  - IO validator invariant: `scripts/validate-gen-plan-io.sh` must be executable before its behavioral tests run at `tests/test-gen-plan.sh:431-542`. The file mode is executable in the export.
- dependencies_and_callers:
  - Direct dependencies of the test:
    - Shell utilities: `bash`, `sed`, `grep`, `awk`, `head`, `tr`, `mktemp`, `touch`, `mkdir`, `rm`, and the executable validator script.
    - Repo command surface: `commands/gen-plan.md`.
    - Repo agent surface: `agents/draft-relevance-checker.md`.
    - Version surfaces: `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, and `README.md`.
    - IO validator: `scripts/validate-gen-plan-io.sh`.
  - Related implementation contract:
    - `commands/gen-plan.md` allows only the validator Bash call plus `Read`, `Glob`, `Grep`, `Task`, `Write`, and `AskUserQuestion` at `commands/gen-plan.md:4-12`.
    - The command instructs Phase 1 to execute `"${CLAUDE_PLUGIN_ROOT}/scripts/validate-gen-plan-io.sh" $ARGUMENTS` and maps exit codes `0-7` to user-facing stop/continue behavior at `commands/gen-plan.md:30-47`.
    - The command invokes the `humanize:draft-relevance-checker` agent using haiku for relevance checking at `commands/gen-plan.md:50-72`.
    - The validator resolves the plan template from `CLAUDE_PLUGIN_ROOT` or script-relative fallback at `scripts/validate-gen-plan-io.sh:133-140`, checks template existence at `scripts/validate-gen-plan-io.sh:142-146`, then copies `prompt-template/plan/gen-plan-template.md` and appends the draft at `scripts/validate-gen-plan-io.sh:148-160`.
  - Callers:
    - `tests/run-all-tests.sh` includes `test-gen-plan.sh` in its test list, so this file participates in the broader repository test suite.
    - README documents the user-facing `/humanize:gen-plan --input ... --output ...` command at `README.md:76-79` and `README.md:122-139`.
- edge_cases_or_failure_modes:
  - Trap replacement: the second cleanup trap at `tests/test-gen-plan.sh:436` overrides the first trap at `tests/test-gen-plan.sh:193`. When the validator script is executable, `TEST_FIXTURES_DIR` may be left behind after the test exits. This is a test hygiene issue, not a product behavior failure.
  - `set -e` plus command substitutions: parsing commands such as the version `grep` pipelines at `tests/test-gen-plan.sh:169-171` can terminate the script early if an expected pattern disappears, instead of recording a normal `fail()` result. That weakens graceful failure reporting for malformed version surfaces.
  - The YAML syntax checker is intentionally shallow. It accepts lines matching simple key/list/quoted patterns and does not validate YAML semantics, indentation correctness, quoted scalar completion, arrays, or nested structures at `tests/test-gen-plan.sh:304-319`.
  - Frontmatter checks do not require a closing `---`; they only verify the first line and required keys at `tests/test-gen-plan.sh:201-214`.
  - Content validation uses `grep -P`; the script redirects grep errors to `/dev/null`, but if the local grep lacks PCRE support the condition falls through as “content is English only,” potentially masking unsupported tooling at `tests/test-gen-plan.sh:409-423`.
  - The test’s valid IO case depends on `prompt-template/plan/gen-plan-template.md` existing because `scripts/validate-gen-plan-io.sh` checks and copies it after path validation at `scripts/validate-gen-plan-io.sh:133-160`. A missing template makes the “valid paths exits 0” assertion fail with exit `7`, even though the test section labels it as IO path validation.
  - The validator’s write-permission check `[[ ! -w "$OUTPUT_DIR" ]]` at `scripts/validate-gen-plan-io.sh:118-124` can behave differently under elevated users or unusual filesystems; the assigned test does not cover exit `5`.
  - The validator normalizes paths with `realpath -m` but falls back to raw paths if unavailable at `scripts/validate-gen-plan-io.sh:69-72`; this makes path display and dirname behavior platform-sensitive, though exit-code tests should mostly remain stable.
- validation_or_tests:
  - This file is itself the validation artifact. It defines 9 positive test groups, 6-numbered negative/model groups with subcases, content checks, and 10 IO-validator command cases.
  - The test verifies metadata structure for `commands/gen-plan.md` and `agents/draft-relevance-checker.md`, consistency of version strings across plugin/marketplace/README, name and model validation logic, absence of CJK/emoji content, and validator exit codes.
  - I did not run the script because the assignment explicitly says not to modify files and the branch export is read-only; the script writes temporary fixtures and the validator writes an output plan file during the success-path assertion.
  - Static inspection confirms `commands/gen-plan.md`, `agents/draft-relevance-checker.md`, `scripts/validate-gen-plan-io.sh`, and `prompt-template/plan/gen-plan-template.md` are present, and the validator script plus test script are executable in the branch export.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `1`
- missing_items: `0`
- duplicate_items: `0`
- final_worker_status: `complete`