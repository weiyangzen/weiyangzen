# agent_064 use-realpath4everything 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`

## Item Evidence

### USE_REALPATH4EVERYTHING-HZ-064 `file` `tests/test-agent-teams.sh`
- cursor: `[_]`
- core_role:
  - `tests/test-agent-teams.sh` is an executable shell specification for the RLCR `--agent-teams` feature. It validates how agent-team mode is enabled, persisted in loop state, parsed by shared state readers, injected into initial prompts, carried into implementation continuation prompts, and deliberately omitted from review-phase fix prompts.
  - The file is not production algorithm code, but it is core behavioral coverage for an algorithmic workflow spanning setup, state frontmatter, prompt generation, active-loop discovery, and stop-hook phase routing.
  - The test header states the intended coverage directly at `tests/test-agent-teams.sh:3-12`: CLI option validation, `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`, `agent_teams` state field, `parse_state_file`, initial prompt team-leader instructions, next-round implementation prompt inclusion, and review-phase exclusion.

- algorithmic_behavior:
  - The script runs as a Bash test suite with strict mode enabled at `tests/test-agent-teams.sh:15`. It sources shared test helpers and loop-common functions at `tests/test-agent-teams.sh:17-22`, giving it `pass`, `fail`, `skip`, `setup_test_dir`, `init_test_git_repo`, `parse_state_file`, and `find_active_loop`.
  - The first behavior block creates a temporary Git repo, a valid ignored plan file, and invokes `scripts/setup-rlcr-loop.sh --agent-teams` without the required feature env var. It expects nonzero exit and an error mentioning `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` at `tests/test-agent-teams.sh:35-69`.
  - It then iterates invalid env values `"0"`, `"false"`, `"yes"`, and `"true"`, expecting rejection for every value except exact `"1"` at `tests/test-agent-teams.sh:71-79`. This models a strict feature-gate invariant, not a truthy-string parser.
  - The success path creates another temp repo and runs setup with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, then asserts that a `.humanize/rlcr/**/state.md` exists at `tests/test-agent-teams.sh:85-111`.
  - Persistence is checked by grepping the generated state for `agent_teams: true` after `--agent-teams` at `tests/test-agent-teams.sh:113-121`, and for `agent_teams: false` when the flag is absent at `tests/test-agent-teams.sh:123-153`.
  - Config-driven enablement is covered by writing `.humanize/config.json` containing `{"agent_teams": true}`, invoking setup without the CLI flag but with the experimental env var, and expecting `agent_teams: true` in state at `tests/test-agent-teams.sh:156-186`.
  - Parser behavior is tested by writing minimal synthetic frontmatter and calling `parse_state_file`: when `agent_teams: true` is present, `STATE_AGENT_TEAMS` must become `true`; when missing, it must default to `false` at `tests/test-agent-teams.sh:188-242`.
  - Initial prompt behavior is tested by running setup with agent teams enabled, locating `round-0-prompt.md`, and requiring at least two team-related keyword families: `team leader`, `agent.team`, and `coordinate|coordination` at `tests/test-agent-teams.sh:244-291`.
  - Negative initial prompt behavior is checked by running setup without agent teams and asserting no `team leader` text appears in `round-0-prompt.md` at `tests/test-agent-teams.sh:293-328`.
  - Template presence and minimum-content tests assert that `prompt-template/claude/agent-teams-instructions.md`, `agent-teams-core.md`, and `agent-teams-continue.md` exist and contain expected marker sections at `tests/test-agent-teams.sh:330-388`.
  - Active-loop discovery is tested by creating a synthetic loop directory with `state.md` containing `session_id: team-session-123` and `agent_teams: true`, then requiring `find_active_loop "$TEST_DIR/loop" "team-session-123"` to return a non-empty result at `tests/test-agent-teams.sh:390-414`.
  - Stop-hook continuation behavior is tested through a dedicated fixture builder, `setup_stophook_test`, at `tests/test-agent-teams.sh:430-540`. It creates a temp Git repo, plan, ignored loop artifacts, state frontmatter, plan backup, goal tracker, summary, round contract, and optionally `.review-phase-started`.
  - Mock Codex executables are injected into `PATH` for implementation and review phases at `tests/test-agent-teams.sh:542-590`. The mocks distinguish `codex exec` from `codex review`, allowing the real stop hook to run while avoiding a real Codex dependency.
  - Implementation phase with `agent_teams=true` is expected to generate `round-4-prompt.md` containing `Agent Teams` and `team leader` after Codex returns review feedback plus `CONTINUE` at `tests/test-agent-teams.sh:592-629`.
  - Drift recovery is modeled by mutating state from `mainline_stall_count: 0` to `1` and `last_mainline_verdict: unknown` to `stalled`, then feeding a `STALLED` verdict. The next prompt must contain both `Drift Recovery Mode` and `Agent Teams` at `tests/test-agent-teams.sh:631-669`.
  - Implementation phase with `agent_teams=false` must still produce `round-4-prompt.md`, but the prompt must not contain `Agent Teams` at `tests/test-agent-teams.sh:671-701`.
  - Review phase with `agent_teams=true` and `review_started=true` must generate `round-6-prompt.md` from review-phase logic, must not contain `Agent Teams`, and must include the mocked `P1` issue at `tests/test-agent-teams.sh:703-734`.
  - The suite ends through `print_test_summary "Agent Teams Feature Tests"` at `tests/test-agent-teams.sh:736-740`, returning success only if no `fail` calls were recorded by `tests/test-helpers.sh:58-77`.

- inputs_outputs_state:
  - Inputs:
    - CLI inputs to `scripts/setup-rlcr-loop.sh`: `--agent-teams`, positional `temp/plan.md`, and default/no-flag variants at `tests/test-agent-teams.sh:56`, `tests/test-agent-teams.sh:104`, `tests/test-agent-teams.sh:146`, `tests/test-agent-teams.sh:179`, `tests/test-agent-teams.sh:267`, and `tests/test-agent-teams.sh:316`.
    - Environment inputs: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`, `CLAUDE_PROJECT_DIR`, `PATH`, and `XDG_CACHE_HOME`. The feature gate is varied at `tests/test-agent-teams.sh:56`, `tests/test-agent-teams.sh:72-79`, `tests/test-agent-teams.sh:104`, and `tests/test-agent-teams.sh:179`.
    - Project config input: `.humanize/config.json` with `agent_teams` set to `true` at `tests/test-agent-teams.sh:162-179`.
    - Synthetic state frontmatter for parser and stop-hook tests at `tests/test-agent-teams.sh:194-205`, `tests/test-agent-teams.sh:223-232`, `tests/test-agent-teams.sh:396-407`, and `tests/test-agent-teams.sh:473-495`.
    - Stop-hook JSON input: `{"stop_hook_active": false, "transcript": [], "session_id": ""}` at `tests/test-agent-teams.sh:608`, `tests/test-agent-teams.sh:649`, `tests/test-agent-teams.sh:687`, and `tests/test-agent-teams.sh:712`.
    - Mock Codex stdout content containing `Mainline Progress Verdict`, issues, `CONTINUE`, or review-phase `[P1]` output at `tests/test-agent-teams.sh:596-606`, `tests/test-agent-teams.sh:638-647`, `tests/test-agent-teams.sh:675-685`, and `tests/test-agent-teams.sh:707-710`.
  - Outputs:
    - Test console output via `pass`, `fail`, `skip`, and final summary counters from `tests/test-helpers.sh:30-77`.
    - Generated RLCR state files under `.humanize/rlcr/**/state.md`, located via `find` at `tests/test-agent-teams.sh:106`, `tests/test-agent-teams.sh:148`, and `tests/test-agent-teams.sh:181`.
    - Generated initial prompts `round-0-prompt.md`, located and grepped at `tests/test-agent-teams.sh:269-291` and `tests/test-agent-teams.sh:318-328`.
    - Generated continuation prompts `round-4-prompt.md` and review prompts `round-6-prompt.md` asserted at `tests/test-agent-teams.sh:615-629`, `tests/test-agent-teams.sh:655-669`, `tests/test-agent-teams.sh:692-701`, and `tests/test-agent-teams.sh:719-734`.
    - In-memory parser outputs `STATE_AGENT_TEAMS=true|false` after `parse_state_file` at `tests/test-agent-teams.sh:207-215` and `tests/test-agent-teams.sh:234-242`.
  - State transitions:
    - Setup initializes `AGENT_TEAMS` from `DEFAULT_AGENT_TEAMS`, then `--agent-teams` flips it to `true`; production code shows this at `scripts/setup-rlcr-loop.sh:53` and `scripts/setup-rlcr-loop.sh:280-282`.
    - Setup blocks before state creation when `AGENT_TEAMS=true` but `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` is not exactly `1`; production code shows the gate at `scripts/setup-rlcr-loop.sh:385-396`.
    - Setup writes `agent_teams: $AGENT_TEAMS` into state frontmatter at `scripts/setup-rlcr-loop.sh:880-907`, specifically `scripts/setup-rlcr-loop.sh:897`.
    - Shared config can set `DEFAULT_AGENT_TEAMS` from merged config; production code loads it at `hooks/lib/loop-common.sh:232-235`, and config merge order is default, user, then project at `scripts/lib/config-loader.sh:113-132`.
    - `parse_state_file` reads `agent_teams` from frontmatter into `STATE_AGENT_TEAMS` at `hooks/lib/loop-common.sh:464`, then defaults it to `false` if absent at `hooks/lib/loop-common.sh:513`.
    - Stop hook maps parsed state into local `AGENT_TEAMS` at `hooks/loop-codex-stop-hook.sh:119-143`.
    - Implementation continuation prompt generation appends agent-team continuation only when `AGENT_TEAMS=true` and `REVIEW_STARTED!=true` at `hooks/loop-codex-stop-hook.sh:2145-2165`.
    - Review phase takes a separate path: if `REVIEW_STARTED=true`, summary review is skipped at `hooks/loop-codex-stop-hook.sh:1628-1631`, and review issues continue through `continue_review_loop_with_issues`, which renders `claude/review-phase-prompt.md` at `hooks/loop-codex-stop-hook.sh:1456-1520` without appending agent-team continuation.

- gates_or_invariants:
  - Exact env gate: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` must equal `"1"` when agent teams is enabled. Empty, `0`, `false`, `yes`, and `true` are invalid by test at `tests/test-agent-teams.sh:54-79` and by implementation at `scripts/setup-rlcr-loop.sh:385-396`.
  - State persistence invariant: generated `state.md` must always include `agent_teams: true|false`, verified at `tests/test-agent-teams.sh:117-120` and `tests/test-agent-teams.sh:149-152`; production writes it at `scripts/setup-rlcr-loop.sh:897`.
  - Parser compatibility invariant: old state files missing `agent_teams` must parse successfully and default to `false`, verified at `tests/test-agent-teams.sh:218-242` and implemented at `hooks/lib/loop-common.sh:513` and `hooks/lib/loop-common.sh:593`.
  - Config precedence invariant: a project-level `.humanize/config.json` can enable agent teams without the CLI flag, but still requires the experimental env var, verified at `tests/test-agent-teams.sh:156-186`; production default loading is at `hooks/lib/loop-common.sh:232-235`.
  - Prompt injection invariant: initial prompts include agent-team leader instructions only when enabled, tested at `tests/test-agent-teams.sh:244-328`; production appends header/core templates or fallback at `scripts/setup-rlcr-loop.sh:1370-1391`.
  - Template integrity invariant: agent-team template files must exist with enough content and key sections, tested at `tests/test-agent-teams.sh:330-388`. The core template includes `Your Role`, `Guidelines`, and `Important` sections at `prompt-template/claude/agent-teams-core.md:1-31`.
  - Phase routing invariant: implementation continuation prompts include agent teams only when `agent_teams=true`, while review-phase prompts omit agent teams even when state has `agent_teams: true`; tests cover the positive, negative, and review-phase paths at `tests/test-agent-teams.sh:592-734`.
  - Drift recovery invariant: stalled mainline prompts still preserve agent-team continuation, covered at `tests/test-agent-teams.sh:631-669`.
  - Active-loop discovery invariant: adding an optional `agent_teams` field to state frontmatter must not break `find_active_loop` session matching, covered at `tests/test-agent-teams.sh:390-414`.
  - Test-harness invariant: `print_test_summary` fails the script if any assertion used `fail`, defined at `tests/test-helpers.sh:58-77`.

- dependencies_and_callers:
  - Directly sourced dependencies:
    - `tests/test-helpers.sh` for test lifecycle, temp dirs, Git repo setup, and pass/fail accounting at `tests/test-agent-teams.sh:17-18`; helper definitions are at `tests/test-helpers.sh:30-104`.
    - `hooks/lib/loop-common.sh` for state parsing and loop discovery at `tests/test-agent-teams.sh:20-22`.
  - Production scripts under test:
    - `scripts/setup-rlcr-loop.sh`, assigned to `SETUP_SCRIPT` at `tests/test-agent-teams.sh:29`.
    - `hooks/loop-codex-stop-hook.sh`, assigned to `STOP_HOOK` at `tests/test-agent-teams.sh:427-428`.
  - Production setup dependencies:
    - `scripts/setup-rlcr-loop.sh` sources `portable-timeout.sh` and `hooks/lib/loop-common.sh` at `scripts/setup-rlcr-loop.sh:25-33`.
    - `loop-common.sh` sources `hooks/lib/project-root.sh`, `scripts/lib/config-loader.sh`, and `template-loader.sh` at `hooks/lib/loop-common.sh:171-240`.
    - `project-root.sh` resolves `CLAUDE_PROJECT_DIR` first, then Git toplevel, and canonicalizes via `realpath` at `hooks/lib/project-root.sh:41-53`. This is relevant to the branch theme `use-realpath4everything`: the tests set `CLAUDE_PROJECT_DIR` consistently so setup and hook state lookup operate on the same project root.
  - Runtime command dependencies:
    - `git` is used for temp repo initialization and commits throughout the test, especially in `init_test_git_repo` at `tests/test-helpers.sh:93-104` and `setup_stophook_test` at `tests/test-agent-teams.sh:437-464`.
    - `find`, `grep`, `sed`, `awk`, `perl`, `mktemp`, `chmod`, and `wc` are used by the shell assertions and fixture setup.
    - `jq` is required by the stop hook and config loader; setup checks it as a required dependency at `scripts/setup-rlcr-loop.sh:346-348`.
    - `codex` is required by setup’s dependency check at `scripts/setup-rlcr-loop.sh:342-344`, but stop-hook tests replace runtime `codex` with a local mock at `tests/test-agent-teams.sh:542-590`.
  - Template dependencies:
    - Initial setup appends `prompt-template/claude/agent-teams-instructions.md` and `prompt-template/claude/agent-teams-core.md` when enabled at `scripts/setup-rlcr-loop.sh:1370-1379`.
    - Stop-hook continuation appends `prompt-template/claude/agent-teams-continue.md` and `agent-teams-core.md` when enabled and still in implementation phase at `hooks/loop-codex-stop-hook.sh:2145-2155`.
    - Review-phase fixes render `prompt-template/claude/review-phase-prompt.md` through `continue_review_loop_with_issues` at `hooks/loop-codex-stop-hook.sh:1513-1520`.
  - Test suite caller:
    - `tests/run-all-tests.sh` includes `test-agent-teams.sh` in its test list at `tests/run-all-tests.sh:92`.

- edge_cases_or_failure_modes:
  - `SETUP_EXIT` is not reset before each setup invocation in the early env-gate blocks. The first failing setup assigns a nonzero `SETUP_EXIT`; subsequent invalid-value checks at `tests/test-agent-teams.sh:72-79` use `${SETUP_EXIT:-0}` but do not clear it before each iteration. If a later invalid env value unexpectedly exited `0`, the stale nonzero value could make that subtest pass incorrectly.
  - Several setup invocations use `|| true`, for example `tests/test-agent-teams.sh:104`, `tests/test-agent-teams.sh:146`, `tests/test-agent-teams.sh:179`, `tests/test-agent-teams.sh:267`, and `tests/test-agent-teams.sh:316`. This prevents the suite from aborting under `set -e`, but it also means failures are inferred only from generated artifacts. That is acceptable for artifact-oriented assertions, but it can hide the immediate setup exit reason.
  - The config-driven enablement case writes `.humanize/config.json` but only commits `.gitignore` at `tests/test-agent-teams.sh:172-176`. This intentionally tests local project config loading rather than tracked config behavior, but it means Git cleanliness assumptions depend on setup’s handling of untracked `.humanize/config.json`.
  - Prompt assertions use case-insensitive keyword greps rather than exact rendered sections at `tests/test-agent-teams.sh:271-288`, so they verify semantic presence but could pass if unrelated text contains the same keywords.
  - Negative prompt assertions only check absence of `team leader` or `Agent Teams`, not absence of all possible delegation wording. This is pragmatic but not exhaustive.
  - Template existence checks can `skip` rather than `fail` if template files are absent at `tests/test-agent-teams.sh:342-344`, `tests/test-agent-teams.sh:364-366`, and `tests/test-agent-teams.sh:386-388`. Because the production code has inline fallbacks, missing templates are not always fatal, but the suite’s “template exists” coverage is softer than the rest.
  - `setup_test_dir` installs a new `trap "rm -rf $TEST_DIR" EXIT` each time at `tests/test-helpers.sh:86-89`, replacing the previous cleanup trap. Multiple temp dirs created during one script may not all be removed by the final trap.
  - Stop-hook fixture state uses `base_branch: main` while temp Git default branch may be `master` depending on Git config at `tests/test-agent-teams.sh:473-495`. The stop-hook test path is mostly focused on prompt generation, but branch/base assumptions can matter if the hook reaches review diff logic.
  - The stop-hook fixture sets `base_commit` to `abc123` by default at `tests/test-agent-teams.sh:431-435`, which is not a real commit. Implementation-phase tests relying on `codex exec` feedback can avoid base-commit-sensitive review behavior, but review-phase paths that run `codex review` may be sensitive if production code validates base commits before using the mock.
  - The review-phase assertion expects no `Agent Teams` in `round-6-prompt.md` at `tests/test-agent-teams.sh:720-725`. Production implementation also injects a delegation warning in the generic implementation continuation path when `AGENT_TEAMS=true` at `hooks/loop-codex-stop-hook.sh:2054-2076`, but review-phase issue prompts are generated earlier by `continue_review_loop_with_issues` and exit through that path, so the test guards against accidental leakage between these two prompt-generation routes.
  - Running this exact test suite in a restricted read-only sandbox is not feasible because it creates temp directories, Git repositories, generated loop state, and mock executables. I inspected the file and referenced production paths directly instead of executing it.

- validation_or_tests:
  - This assigned file is itself the validation surface for the agent-teams workflow. It verifies setup error handling, state emission, parser defaults, prompt-template presence, active-loop lookup, implementation continuation prompt inclusion, drift recovery prompt preservation, disabled-mode omission, and review-phase omission.
  - Key production behavior validated by this test maps to:
    - `scripts/setup-rlcr-loop.sh:280-282` for parsing `--agent-teams`.
    - `scripts/setup-rlcr-loop.sh:385-396` for exact experimental env validation.
    - `scripts/setup-rlcr-loop.sh:897` for state persistence.
    - `hooks/lib/loop-common.sh:464` and `hooks/lib/loop-common.sh:513` for state parsing/defaulting.
    - `scripts/setup-rlcr-loop.sh:1370-1391` for initial prompt injection.
    - `hooks/loop-codex-stop-hook.sh:2145-2165` for implementation continuation prompt injection.
    - `hooks/loop-codex-stop-hook.sh:1456-1520` for review-phase prompt generation.
  - The suite is included in the aggregate test runner at `tests/run-all-tests.sh:92`.
  - I did not execute `tests/test-agent-teams.sh` because the current branch export is read-only and the test requires filesystem writes for temp repos, `.humanize/rlcr` state, plan files, and mock `codex` binaries. I also could not verify the Git source commit locally: the export does not expose a usable `.git` checkout under the sandbox, and `git rev-parse` failed with “not a git repository”.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 1 of 1 item sections present
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`