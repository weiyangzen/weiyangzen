# agent_067 use-realpath4everything 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`

## Item Evidence

### USE_REALPATH4EVERYTHING-HZ-067 `file` `tests/test-ask-codex.sh`
- cursor: `[_]`
- core_role: `tests/test-ask-codex.sh` is an executable black-box specification for `scripts/ask-codex.sh`, the one-shot Codex consultation command. It verifies that the command safely parses user-supplied flags and question text, resolves the active project root through the shared project-root machinery, invokes a `codex exec`-compatible binary through a portable timeout wrapper, writes project-local and cache artifacts, and maps Codex success/failure outcomes into stable exit codes plus metadata. The test is core-adjacent rather than production code, but it is algorithmically important because it codifies the required command behavior with mock Codex I/O instead of relying on live Codex calls.

- algorithmic_behavior: The test starts with strict shell settings and sources shared test helpers from `tests/test-helpers.sh` (`tests/test-ask-codex.sh:12-18`). It creates a temporary mock git repository as `MOCK_PROJECT` (`tests/test-ask-codex.sh:29-34`) and a mock `codex` binary placed ahead of the real PATH (`tests/test-ask-codex.sh:35-53`). The mock writes environment-controlled stdout/stderr, drains stdin, and exits with an environment-controlled code (`tests/test-ask-codex.sh:39-52`). `run_ask_codex` then executes the real script from inside the mock repo with `CLAUDE_PROJECT_DIR="$MOCK_PROJECT"` and `XDG_CACHE_HOME="$TEST_DIR/cache"` (`tests/test-ask-codex.sh:67-75`), which exercises the same project-root resolution path the production script uses.

  The test cases cover these algorithmic sections:
  - validation gate behavior: empty input, help, unknown flags, missing option arguments, nonnumeric timeout, and unsafe model/effort characters (`tests/test-ask-codex.sh:81-154`);
  - successful execution behavior: stdout passthrough, creation of `.humanize/skill/<unique>/output.md`, `metadata.md` with `status: success`, `input.md` with the question, and exit code `0` (`tests/test-ask-codex.sh:164-210`);
  - failure mapping: nonzero Codex exit propagation, `status: error`, empty response as exit `1` plus `status: empty_response`, timeout exit `124` plus a timeout diagnostic and `status: timeout` (`tests/test-ask-codex.sh:221-276`);
  - uniqueness under concurrent calls: two background invocations must create distinct project-local skill directories and distinct cache directories (`tests/test-ask-codex.sh:286-320`);
  - argument parsing semantics: `--codex-model MODEL:EFFORT`, model-only default effort, `--` end-of-options handling, and timeout recording (`tests/test-ask-codex.sh:330-372`);
  - cache artifact creation: `codex-run.cmd`, `codex-run.out`, and prompt recording under the stderr-reported cache path (`tests/test-ask-codex.sh:382-405`);
  - skill documentation safety: the skill must warn against bare `$ARGUMENTS`, document quoted invocation, and require free-form text as one quoted final argument (`tests/test-ask-codex.sh:415-434`).

- inputs_outputs_state: Primary inputs are command-line arguments passed to `run_ask_codex`, exported mock controls `MOCK_CODEX_EXIT_CODE`, `MOCK_CODEX_STDOUT`, and `MOCK_CODEX_STDERR` (`tests/test-ask-codex.sh:55-65`), the mock git repo root, and the mock `codex` executable injected into PATH (`tests/test-ask-codex.sh:67-74`). The tested script itself consumes those inputs by parsing flags into `CODEX_MODEL`, `CODEX_EFFORT`, `CODEX_TIMEOUT`, and `QUESTION` (`scripts/ask-codex.sh:86-147`), resolving `PROJECT_ROOT` through `resolve_project_root` (`scripts/ask-codex.sh:192-196`), and creating a unique run id from timestamp, PID, and random bytes (`scripts/ask-codex.sh:202-213`).

  Observable outputs asserted by the test include:
  - process stdout containing the Codex answer on success (`tests/test-ask-codex.sh:164-172`; implementation at `scripts/ask-codex.sh:414-415`);
  - process stderr status lines including `ask-codex: cache=...`, which the cache tests parse (`tests/test-ask-codex.sh:386-389`; implementation at `scripts/ask-codex.sh:282-284`);
  - project-local run state under `.humanize/skill/<unique-id>/`, specifically `input.md`, `output.md`, and `metadata.md` (`tests/test-ask-codex.sh:174-199`, `187-199`; implementation at `scripts/ask-codex.sh:205-238`, `391-406`);
  - cache state under `$XDG_CACHE_HOME/humanize/<sanitized-project-path>/skill-<unique-id>/`, specifically `codex-run.cmd`, `codex-run.out`, and `codex-run.log` (`tests/test-ask-codex.sh:382-405`; implementation at `scripts/ask-codex.sh:211-218`, `262-276`);
  - exit codes `0`, `1`, `42`, and `124` depending on validation, mock Codex status, empty output, and timeout/error conditions (`tests/test-ask-codex.sh:84-154`, `201-210`, `221-276`).

  State transitions specified by the test are run-local and file-backed. A successful run transitions from no run directory to a unique `.humanize/skill/<id>` directory with saved input, output, and `status: success`; a nonzero Codex exit transitions to a run directory with `status: error` and preserves the external exit code; a timeout transitions to `status: timeout` and exit `124`; an empty stdout transitions to `status: empty_response` and exit `1`.

- gates_or_invariants: The validation gates are explicit and fail-fast. Empty question must exit `1` with “No question or task provided” (`tests/test-ask-codex.sh:84-91`; implementation `scripts/ask-codex.sh:162-170`). `--help` must exit `0` and print usage (`tests/test-ask-codex.sh:93-100`; implementation `scripts/ask-codex.sh:49-80`, `97-99`). Unknown options must exit `1` (`tests/test-ask-codex.sh:102-109`; implementation `scripts/ask-codex.sh:132-135`). `--codex-model` and `--codex-timeout` require arguments (`tests/test-ask-codex.sh:111-127`; implementation `scripts/ask-codex.sh:105-130`). Timeout must match digits only (`tests/test-ask-codex.sh:129-136`; implementation `scripts/ask-codex.sh:125-128`). Model and effort reject shell-metacharacter inputs through strict regexes (`tests/test-ask-codex.sh:138-154`; implementation `scripts/ask-codex.sh:172-186`).

  Storage invariants include one unique project-local directory per invocation and one unique cache directory per invocation, even for rapid concurrent calls (`tests/test-ask-codex.sh:286-320`). The uniqueness algorithm is timestamp + shell PID + random suffix in the implementation (`scripts/ask-codex.sh:202-203`), and the test specifically checks that two background invocations produce at least two new directories.

  The branch-relevant realpath invariant is indirect but important: the test pins `CLAUDE_PROJECT_DIR` to the mock project (`tests/test-ask-codex.sh:71`), and `ask-codex.sh` relies on `resolve_project_root` from `hooks/lib/project-root.sh` through `loop-common.sh` (`scripts/ask-codex.sh:31-33`, `192-196`). That resolver prioritizes `CLAUDE_PROJECT_DIR`, falls back to `git rev-parse --show-toplevel`, never uses drifting `pwd`, and canonicalizes via `realpath` or a Python fallback (`hooks/lib/project-root.sh:5-16`, `41-52`, `113-143`). The test does not create a symlinked project root, but it verifies the command path that consumes the canonical project root for `.humanize/skill` storage and `codex exec -C "$PROJECT_ROOT"`.

- dependencies_and_callers: Direct dependencies are `tests/test-helpers.sh` for `setup_test_dir`, `init_test_git_repo`, `pass`, `fail`, and `print_test_summary` (`tests/test-ask-codex.sh:14-15`; helper definitions at `tests/test-helpers.sh:30-78`, `86-104`); `scripts/ask-codex.sh` as the executable under test (`tests/test-ask-codex.sh:17`); and `skills/ask-codex/SKILL.md` for documentation-safety assertions (`tests/test-ask-codex.sh:18`, `415-434`). The script under test depends on `scripts/portable-timeout.sh` for `run_with_timeout` (`scripts/ask-codex.sh:28-30`; timeout behavior at `scripts/portable-timeout.sh:9-71`) and `hooks/lib/loop-common.sh` for default Codex config and project-root resolution (`scripts/ask-codex.sh:31-33`; defaults at `hooks/lib/loop-common.sh:208-230`). `loop-common.sh` sources `hooks/lib/project-root.sh` before callers need `PROJECT_ROOT` (`hooks/lib/loop-common.sh:176-179`), making the realpath-canonical resolver part of the tested dependency chain.

  Callers are human or skill-invoked `/humanize:ask-codex` flows documented in `skills/ask-codex/SKILL.md`. That skill constrains shell invocation by requiring the free-form question to be quoted and forbidding bare `$ARGUMENTS` expansion (`skills/ask-codex/SKILL.md:14-36`), and this test treats that guidance as part of the behavioral contract.

- edge_cases_or_failure_modes: Covered edge cases include missing question, help path, unknown flags, missing flag values, nonnumeric timeout, model/effort shell metacharacters, Codex nonzero exit, empty stdout despite exit `0`, timeout code `124`, concurrent invocations, end-of-options separator with a question beginning like a flag, model-only default effort, and cache directory extraction from stderr. Failure modes not directly exercised include missing `codex` binary, inability to resolve a project root, unwritable home cache fallback to project-local cache, malformed project config warnings inherited through `loop-common.sh`, lack of a timeout provider causing the command to run without enforced timeout, and symlinked `CLAUDE_PROJECT_DIR` canonicalization. The realpath branch relevance is therefore partially covered through the normal resolver path but not stress-tested with symlink aliases or non-existing project paths in this file.

- validation_or_tests: This file is itself the validation asset. It implements a mock-driven integration test that avoids live Codex calls while still executing `scripts/ask-codex.sh` end to end. It finishes by calling `print_test_summary "Ask Codex Test Summary"` (`tests/test-ask-codex.sh:436-440`), whose helper returns nonzero if any `fail` was recorded (`tests/test-helpers.sh:58-78`). I did not execute the test during this research pass because the scheduler instruction was read-only research notes only; the evidence above is from direct static inspection of the assigned file and its necessary dependencies.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `1/1; the sole assigned item id appears in exactly one Item Evidence heading above`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`