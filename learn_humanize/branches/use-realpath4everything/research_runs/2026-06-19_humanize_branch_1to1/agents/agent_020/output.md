# agent_020 use-realpath4everything 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`

## Item Evidence

### USE_REALPATH4EVERYTHING-HZ-020 `directory` `skills/ask-gemini`
- cursor: `[_]`
- core_role:
  - `skills/ask-gemini` is a Claude/Humanize skill definition directory with one recursive child file: `skills/ask-gemini/SKILL.md`.
  - Its role is an invocation contract and safety wrapper for the real Gemini execution path, not a standalone algorithm implementation. The manifest declares the skill name, description, argument hint, and allowed tool boundary in `skills/ask-gemini/SKILL.md:1-5`.
  - The runtime implementation is delegated to `scripts/ask-gemini.sh`, constrained by `allowed-tools: "Bash(${CLAUDE_PLUGIN_ROOT}/scripts/ask-gemini.sh:*)"` at `skills/ask-gemini/SKILL.md:5`.
  - In the `use-realpath4everything` branch context, this directory participates indirectly in canonical project-root behavior because the delegated script sources `hooks/lib/project-root.sh` at `scripts/ask-gemini.sh:32-33`, then calls `resolve_project_root` at `scripts/ask-gemini.sh:174`.

- algorithmic_behavior:
  - The skill instructs the agent to send a user question/task to Gemini for web-backed research, always with a Google Search instruction. The skill-level behavior is described at `skills/ask-gemini/SKILL.md:10-13`.
  - The key local algorithmic rule in the skill manifest is shell argument preservation:
    - If the user supplied only a free-form question, invoke `"${CLAUDE_PLUGIN_ROOT}/scripts/ask-gemini.sh" "$ARGUMENTS"` as shown at `skills/ask-gemini/SKILL.md:19-23`.
    - If flags are present, reconstruct them as separate argv entries and pass the remaining free-form question as one quoted final argument, per `skills/ask-gemini/SKILL.md:25-31`.
    - The manifest explicitly forbids the unsafe unquoted form at `skills/ask-gemini/SKILL.md:33-39`, because shell re-parsing could split spaces or interpret metacharacters before `ask-gemini.sh` starts.
  - The delegated script implements the runtime flow:
    - Parses `--gemini-model`, `--gemini-timeout`, `--help`, and `--` option terminator at `scripts/ask-gemini.sh:91-136`.
    - Joins remaining question parts into one `QUESTION` string at `scripts/ask-gemini.sh:138-139`.
    - Validates Gemini CLI availability, non-empty question, and model-name character safety at `scripts/ask-gemini.sh:145-168`.
    - Resolves the project root using shared realpath-aware logic at `scripts/ask-gemini.sh:174`.
    - Creates project-local and cache storage directories at `scripts/ask-gemini.sh:184-199`.
    - Saves input metadata at `scripts/ask-gemini.sh:205-218`.
    - Builds Gemini args with model, approval mode, and text output at `scripts/ask-gemini.sh:224-234`.
    - Prepends an instruction requiring Google Search to the prompt at `scripts/ask-gemini.sh:236-241`.
    - Saves a debug command and prompt copy at `scripts/ask-gemini.sh:247-261`.
    - Runs `gemini` through a portable timeout wrapper at `scripts/ask-gemini.sh:279-283`.
    - Converts results into metadata, local output files, stderr diagnostics, and final stdout at `scripts/ask-gemini.sh:294-388`.

- inputs_outputs_state:
  - Inputs:
    - Skill arguments from `/humanize:ask-gemini`, optionally including `--gemini-model MODEL` and `--gemini-timeout SECONDS`, documented at `skills/ask-gemini/SKILL.md:4` and `skills/ask-gemini/SKILL.md:25-31`.
    - Free-form question/task text, which may contain spaces and shell metacharacters; the skill warns about `(`, `)`, `;`, `#`, `*`, and `[` at `skills/ask-gemini/SKILL.md:17`.
    - Environment variables used by the delegated script include `CLAUDE_PLUGIN_ROOT` for locating the script, `CLAUDE_PROJECT_DIR` through the shared project-root resolver, `XDG_CACHE_HOME`/`HOME` for cache placement, and `HUMANIZE_GEMINI_YOLO` for approval mode.
  - Outputs:
    - Gemini response on stdout, specified by `skills/ask-gemini/SKILL.md:43` and produced by `cat "$GEMINI_STDOUT_FILE"` at `scripts/ask-gemini.sh:388`.
    - Status/debug information on stderr, specified by `skills/ask-gemini/SKILL.md:43` and emitted around `scripts/ask-gemini.sh:267-269`, `scripts/ask-gemini.sh:288`, and error branches.
    - Project-local invocation state under `.humanize/skill/<unique-id>/`, including `input.md`, `output.md`, and `metadata.md`, described at `scripts/ask-gemini.sh:16-18` and created/written at `scripts/ask-gemini.sh:188-218`, `scripts/ask-gemini.sh:368-380`.
    - Cache/debug files under `~/.cache/humanize/<sanitized-path>/skill-<unique-id>/gemini-run.{cmd,out,log}`, with fallback to `.humanize/skill/<unique-id>/cache` if home cache is not writable, at `scripts/ask-gemini.sh:191-199` and `scripts/ask-gemini.sh:247-249`.
  - State transitions:
    - New invocation starts by creating a timestamp/pid/random `UNIQUE_ID` at `scripts/ask-gemini.sh:184-185`.
    - Before Gemini runs, `input.md` and `gemini-run.cmd` are written, making the invocation monitorable as running.
    - On timeout, `metadata.md` is written with `status: timeout` and the script exits `124` at `scripts/ask-gemini.sh:294-313`.
    - On Gemini nonzero exit, `metadata.md` is written with `status: error` and the same exit code is returned at `scripts/ask-gemini.sh:316-337`.
    - On empty stdout, `metadata.md` is written with `status: empty_response` and the script exits `1` at `scripts/ask-gemini.sh:340-361`.
    - On success, stdout is copied to `output.md`, `metadata.md` records `status: success`, and the response is printed at `scripts/ask-gemini.sh:368-388`.

- gates_or_invariants:
  - Invocation safety invariant: free-form user text must be shell-quoted and never passed through unquoted `$ARGUMENTS`; this is the main gate encoded directly in the skill manifest at `skills/ask-gemini/SKILL.md:17-39`.
  - Tool boundary invariant: the skill is only allowed to run `${CLAUDE_PLUGIN_ROOT}/scripts/ask-gemini.sh`, declared at `skills/ask-gemini/SKILL.md:5`.
  - Output contract invariant: stdout is model response; stderr is status/debug; nonzero exit must be reported to the user, per `skills/ask-gemini/SKILL.md:41-47`.
  - Exit-code invariant: `0` success, `1` validation error, `124` timeout, other codes are Gemini process errors, documented at `skills/ask-gemini/SKILL.md:48-55`.
  - Runtime validation gates in the delegated script:
    - `gemini` command must be installed, `scripts/ask-gemini.sh:145-151`.
    - Question must not be empty, `scripts/ask-gemini.sh:153-160`.
    - Model name must match `^[a-zA-Z0-9._-]+$`, `scripts/ask-gemini.sh:162-168`.
    - Project root must resolve through `resolve_project_root`, `scripts/ask-gemini.sh:174-178`.
    - Timeout argument must be numeric, though the error says positive integer while the regex accepts `0`, at `scripts/ask-gemini.sh:113-123`.
  - Realpath-related invariant inherited from `hooks/lib/project-root.sh`:
    - `resolve_project_root` prefers `CLAUDE_PROJECT_DIR`, then `git rev-parse --show-toplevel`, and intentionally does not use `pwd` fallback, documented at `hooks/lib/project-root.sh:5-12`.
    - The resolved root is canonicalized with `realpath` via `canonicalize_path`, preventing symlink-prefix divergence, documented at `hooks/lib/project-root.sh:14-20` and implemented at `hooks/lib/project-root.sh:41-53`.
    - This matters for `ask-gemini.sh` because `.humanize/skill` state and cache path sanitization derive from the canonical `PROJECT_ROOT` at `scripts/ask-gemini.sh:188-194`.

- dependencies_and_callers:
  - Direct child file:
    - `skills/ask-gemini/SKILL.md` is the only file under `skills/ask-gemini`.
  - Delegated execution dependency:
    - `scripts/ask-gemini.sh` is the actual runtime script named by the skill manifest at `skills/ask-gemini/SKILL.md:5`.
  - Shared script dependencies:
    - `scripts/ask-gemini.sh` sources `scripts/portable-timeout.sh` at `scripts/ask-gemini.sh:29-30`; that wrapper chooses `gtimeout`, GNU `timeout`, Python, or no-timeout fallback at `scripts/portable-timeout.sh:9-27`, and executes commands through `run_with_timeout` at `scripts/portable-timeout.sh:33-71`.
    - `scripts/ask-gemini.sh` sources `hooks/lib/project-root.sh` at `scripts/ask-gemini.sh:32-33`, then uses `resolve_project_root` at `scripts/ask-gemini.sh:174`.
  - CLI/user-facing references:
    - `README.md:59-62` documents `/humanize:ask-gemini` as the way to consult Gemini for deep web research.
    - `README.md:64-70` documents `humanize monitor gemini`, which monitors these invocations.
  - Monitor coordination:
    - `scripts/humanize.sh:1196-1210` routes `humanize monitor gemini` to `_humanize_monitor_skill --tool-filter gemini`.
    - `scripts/lib/monitor-skill.sh:50-64` identifies invocation tool type from `metadata.md` first, then `input.md`.
    - `scripts/lib/monitor-skill.sh:165-217` selects the best monitored file, including `gemini-run.log`, `gemini-run.out`, and `output.md`.
    - `scripts/lib/monitor-skill.sh:301-307` displays Gemini model without a Codex-style effort suffix.
  - Sibling coordination:
    - `skills/ask-codex/SKILL.md` is a sibling skill; `scripts/lib/monitor-skill.sh:5-17` treats ask-codex and ask-gemini as the two skill invocation families under `.humanize/skill`.

- edge_cases_or_failure_modes:
  - Unquoted free-form arguments can fail before the script starts or can be shell-interpreted incorrectly; the manifest explicitly calls this out at `skills/ask-gemini/SKILL.md:33-39`.
  - Unknown option causes validation exit `1` in the delegated script at `scripts/ask-gemini.sh:125-128`.
  - Missing flag values for `--gemini-model` or `--gemini-timeout` exit `1` at `scripts/ask-gemini.sh:105-123`.
  - Timeout validation accepts only digits but does not reject `0`; this is a minor mismatch with the “positive integer” message at `scripts/ask-gemini.sh:113-123`.
  - Missing Gemini CLI exits `1` with install guidance at `scripts/ask-gemini.sh:145-151`.
  - Empty question exits `1` with usage guidance at `scripts/ask-gemini.sh:153-160`.
  - Model names containing characters outside alphanumeric, dot, underscore, and hyphen exit `1` at `scripts/ask-gemini.sh:162-168`.
  - Project root resolution failure exits `1`; this can happen when neither `CLAUDE_PROJECT_DIR` nor a git toplevel is available, at `scripts/ask-gemini.sh:174-178`.
  - Home cache creation failure falls back to project-local `.humanize/skill/<id>/cache` and emits a warning at `scripts/ask-gemini.sh:195-199`.
  - Gemini timeout maps to exit `124`, writes timeout metadata, and suggests increasing `--gemini-timeout`, at `scripts/ask-gemini.sh:294-313`.
  - Gemini nonzero exit preserves the exit code, prints the last 20 stderr lines if present, and writes error metadata at `scripts/ask-gemini.sh:316-337`.
  - Empty Gemini stdout after exit `0` is treated as failure with `status: empty_response` and exit `1` at `scripts/ask-gemini.sh:340-361`.
  - If no timeout implementation is available, `portable-timeout.sh` runs without timeout and warns at `scripts/portable-timeout.sh:64-68`, so the documented timeout contract becomes best-effort on minimal systems.

- validation_or_tests:
  - Recursive directory inspection found only:
    - `skills/ask-gemini`
    - `skills/ask-gemini/SKILL.md`
  - Read-only inspection commands used:
    - `rg --files skills/ask-gemini`
    - `find skills/ask-gemini -print`
    - `nl -ba skills/ask-gemini/SKILL.md`
    - `rg -n "ask-gemini|Gemini|gemini" . --glob '!node_modules/**' --glob '!target/**' --glob '!.git/**'`
    - `nl -ba scripts/ask-gemini.sh`
    - `nl -ba scripts/lib/monitor-skill.sh`
    - `nl -ba scripts/humanize.sh`
    - `nl -ba hooks/lib/project-root.sh`
    - `nl -ba scripts/portable-timeout.sh`
  - I did not execute `scripts/ask-gemini.sh` because the branch export is read-only, the script writes `.humanize/skill/...` state and cache files, and the assignment requested research notes only.
  - A `git status --short` attempt was not usable in this sandbox because Xcode/git tried to create an `/tmp/xcrun_db-*` cache and hit `Operation not permitted`; no repository files were modified.

- skip_candidate: `yes: this directory is a skill manifest/adapter, not a core algorithm implementation by itself. Its only child, SKILL.md, defines invocation safety and output semantics while delegating all runtime behavior to scripts/ask-gemini.sh and shared helpers. It is still relevant to the branch because the delegated script uses the realpath-aware project-root resolver.`

## Worker Self-Test
- assigned_items_seen: `USE_REALPATH4EVERYTHING-HZ-020`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`