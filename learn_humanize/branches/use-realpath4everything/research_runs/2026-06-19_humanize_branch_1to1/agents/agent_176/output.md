# agent_176 use-realpath4everything 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`

## Item Evidence

### USE_REALPATH4EVERYTHING-HZ-176 `file` `skills/ask-codex/SKILL.md`
- cursor: `[_]`
- core_role:
  - `skills/ask-codex/SKILL.md` is the Agent Skill instruction wrapper for the repository’s one-shot Codex consultation workflow.
  - Its algorithmic role is not to run Codex directly, but to constrain how an agent invokes `scripts/ask-codex.sh`, especially how user-provided free-form text is passed through the shell.
  - The file is part of the skill-command surface: frontmatter declares `name: ask-codex`, describes delegation to `codex exec`, provides the argument hint, and restricts the allowed tool invocation to `${CLAUDE_PLUGIN_ROOT}/scripts/ask-codex.sh` at `skills/ask-codex/SKILL.md:1-5`.

- algorithmic_behavior:
  - The skill defines a two-path invocation algorithm:
    - If the user supplies only a question/task, invoke `"${CLAUDE_PLUGIN_ROOT}/scripts/ask-codex.sh" "$ARGUMENTS"` as a single quoted argument, preserving the free-form text as one shell argument. See `skills/ask-codex/SKILL.md:16-20`.
    - If the user supplies recognized flags such as `--codex-model` or `--codex-timeout`, reconstruct the command so flags remain separate shell arguments and the remaining free-form question is one quoted final argument. See `skills/ask-codex/SKILL.md:22-28`.
  - The main behavioral guard is explicit shell-safety guidance: never expand bare `$ARGUMENTS`, because shell reparsing can treat user text containing spaces or metacharacters as syntax or separate commands. This is documented at `skills/ask-codex/SKILL.md:14` and `skills/ask-codex/SKILL.md:30-36`.
  - The actual delegated implementation in `scripts/ask-codex.sh` parses flags, validates inputs, resolves the project root, stores input/cache artifacts, builds a `codex exec` command, runs it with timeout, writes metadata, and prints Codex stdout. Key delegated implementation points:
    - argument parse loop and option handling: `scripts/ask-codex.sh:86-144`
    - joining question parts into one string: `scripts/ask-codex.sh:146-147`
    - prerequisite/input validation: `scripts/ask-codex.sh:153-186`
    - project root resolution: `scripts/ask-codex.sh:192-196`
    - skill/cache directory creation: `scripts/ask-codex.sh:202-218`
    - command construction: `scripts/ask-codex.sh:244-257`
    - timeout-wrapped `codex exec`: `scripts/ask-codex.sh:294-298`
    - result handling and stdout return: `scripts/ask-codex.sh:309-415`

- inputs_outputs_state:
  - Inputs:
    - The skill accepts `[--codex-model MODEL:EFFORT] [--codex-timeout SECONDS] [question or task]`, declared at `skills/ask-codex/SKILL.md:4`.
    - Free-form user task text may contain shell-sensitive characters; the skill treats this as an input hazard and requires quoting at `skills/ask-codex/SKILL.md:14`.
    - Runtime implementation also consumes environment/config defaults from `hooks/lib/loop-common.sh` for `DEFAULT_CODEX_MODEL` and `DEFAULT_CODEX_EFFORT`, sourced by `scripts/ask-codex.sh:31-43`.
  - Outputs:
    - On success, the script’s stdout is Codex’s response; the skill instructs the caller to read it and incorporate it into the user answer at `skills/ask-codex/SKILL.md:38-42`.
    - Status/debug information is sent to stderr, documented at `skills/ask-codex/SKILL.md:40`.
    - Response persistence is documented in the skill at `skills/ask-codex/SKILL.md:55`; implementation copies Codex stdout to `.humanize/skill/<unique-id>/output.md` at `scripts/ask-codex.sh:391-392`.
  - State transitions:
    - The delegated script creates a unique skill invocation directory using timestamp, pid, and random bytes: `scripts/ask-codex.sh:202-207`.
    - It writes `input.md` before execution with question/config state: `scripts/ask-codex.sh:224-238`.
    - It writes metadata on timeout, runtime error, empty response, or success:
      - timeout metadata: `scripts/ask-codex.sh:318-331`
      - error metadata: `scripts/ask-codex.sh:345-358`
      - empty-response metadata: `scripts/ask-codex.sh:372-384`
      - success metadata: `scripts/ask-codex.sh:394-406`
    - It also writes cache/debug files under `~/.cache/humanize/...` or a project-local fallback cache, including `codex-run.cmd`, `codex-run.out`, and `codex-run.log`: `scripts/ask-codex.sh:209-218` and `scripts/ask-codex.sh:262-276`.

- gates_or_invariants:
  - Invocation quoting invariant:
    - Free-form user text must never be passed as unquoted `$ARGUMENTS`. The unsafe form is explicitly banned at `skills/ask-codex/SKILL.md:30-36`.
    - When flags are present, flags must remain independent shell arguments while the question remains one quoted final argument: `skills/ask-codex/SKILL.md:22`.
  - Allowed tool gate:
    - The skill permits only Bash calls matching `${CLAUDE_PLUGIN_ROOT}/scripts/ask-codex.sh:*`, declared at `skills/ask-codex/SKILL.md:5`.
  - Delegated validation gates in `scripts/ask-codex.sh`:
    - `codex` must be installed and on `PATH`: `scripts/ask-codex.sh:153-160`.
    - The question must be non-empty: `scripts/ask-codex.sh:162-170`.
    - Unknown options fail immediately: `scripts/ask-codex.sh:132-135`.
    - `--codex-model` requires an argument and supports `MODEL:EFFORT`: `scripts/ask-codex.sh:105-118`.
    - `--codex-timeout` requires a numeric argument: `scripts/ask-codex.sh:120-130`.
    - Model and effort are restricted to safe character classes: `scripts/ask-codex.sh:172-186`.
    - Project root must resolve, otherwise the script exits with an error: `scripts/ask-codex.sh:192-196`.
    - Empty Codex stdout is treated as failure even if `codex exec` exits zero: `scripts/ask-codex.sh:361-385`.

- dependencies_and_callers:
  - Direct dependency:
    - `skills/ask-codex/SKILL.md` delegates to `${CLAUDE_PLUGIN_ROOT}/scripts/ask-codex.sh`; all runtime behavior beyond invocation safety is in that script.
  - Script dependencies:
    - `scripts/ask-codex.sh` sources `scripts/portable-timeout.sh` at `scripts/ask-codex.sh:28-29`.
    - It sources `hooks/lib/loop-common.sh` for Codex defaults and project-root helpers at `scripts/ask-codex.sh:31-33`.
    - It requires the external `codex` CLI at runtime: `scripts/ask-codex.sh:153-160`.
  - Repository callers/references:
    - `commands/gen-plan.md` allows and invokes `scripts/ask-codex.sh` for structured prompts and fallback behavior.
    - `commands/start-rlcr-loop.md`, `prompt-template/plan/gen-plan-template.md`, and `hooks/loop-codex-stop-hook.sh` reference `/humanize:ask-codex` as the route for `analyze` tasks.
    - `skills/humanize/SKILL.md` documents `ask-codex.sh` as part of the broader Humanize skill surface.
    - `docs/usage.md` documents the `/ask-codex` and `/humanize:ask-codex` user-facing command.

- edge_cases_or_failure_modes:
  - Shell metacharacter hazard:
    - The assigned skill specifically exists to prevent a failure mode where text containing `(`, `)`, `;`, `#`, `*`, or `[` is reparsed by the shell before the script starts. This is called out at `skills/ask-codex/SKILL.md:14` and `skills/ask-codex/SKILL.md:30-36`.
  - Flag reconstruction hazard:
    - If a caller passes the entire argument string as one quoted argument when flags are present, `scripts/ask-codex.sh` cannot parse `--codex-model` or `--codex-timeout` as separate options. The skill avoids this by requiring flags to remain separate and only the residual question to be one quoted final argument at `skills/ask-codex/SKILL.md:22`.
  - Delegated runtime failures:
    - Missing `codex` binary exits `1`: `scripts/ask-codex.sh:153-160`.
    - Empty question exits `1`: `scripts/ask-codex.sh:162-170`.
    - Invalid option, invalid timeout, or unsafe model/effort characters exit `1`: `scripts/ask-codex.sh:120-135` and `scripts/ask-codex.sh:172-186`.
    - Timeout exits `124` and suggests increasing `--codex-timeout`: `scripts/ask-codex.sh:309-331`.
    - Non-zero Codex process exit propagates the exit code and reports stderr tail: `scripts/ask-codex.sh:334-358`.
    - Empty successful stdout becomes `status: empty_response` and exits `1`: `scripts/ask-codex.sh:361-385`.
  - State/storage edge cases:
    - If the home cache cannot be created, the script falls back to project-local `.humanize/skill/<id>/cache`: `scripts/ask-codex.sh:214-218`.
    - Concurrent invocations are intended to avoid directory collisions by incorporating pid and random bytes into `UNIQUE_ID`: `scripts/ask-codex.sh:202-207`.

- validation_or_tests:
  - Focused tests are in `tests/test-ask-codex.sh`.
  - The tests use a mock `codex` binary and a mock git project, avoiding real Codex calls: `tests/test-ask-codex.sh:3-5` and `tests/test-ask-codex.sh:31-53`.
  - Covered validation behavior includes empty question, help, unknown option, missing option values, non-numeric timeout, invalid model characters, and invalid effort characters: `tests/test-ask-codex.sh:84-154`.
  - Covered success behavior includes stdout response passthrough, `output.md`, `metadata.md`, `input.md`, and zero exit: `tests/test-ask-codex.sh:164-210`.
  - Covered error behavior includes non-zero Codex exit propagation, empty response, timeout status, and metadata creation: `tests/test-ask-codex.sh:220-276`.
  - Covered state uniqueness behavior includes concurrent calls creating distinct skill and cache directories: `tests/test-ask-codex.sh:286-320`.
  - Covered argument parsing includes `MODEL:EFFORT`, model without effort, `--` separator handling, and timeout recording: `tests/test-ask-codex.sh:330-372`.
  - Tests directly verify the assigned skill guidance warns against bare `$ARGUMENTS`, documents safe quoted invocation, and requires one quoted final argument for free-form text: `tests/test-ask-codex.sh:415-434`.
  - I did not execute tests in this worker pass because the instructions specify a read-only branch export and research notes only.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `1 evidence section for 1 assigned item`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`