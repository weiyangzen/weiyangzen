# agent_01 h2-dev 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 9
- source_commit: `2da7defbd5e955dbc329a27f1745fa74a0bee3f7`
- note: read-only research only; no files modified. The branch export did not expose a usable `.git` checkout to this sandbox, so commit metadata is taken from the run assignment.

## Item Evidence

### H2_DEV-HZ-001 `directory` `.`
- cursor: `[_]`
- core_role: Repository root for a dual Humanize system: legacy RLCR Claude/Codex loop plus the Humanize2 TypeScript MCP/workflow hub. README identifies the branch as transitional, shipping both Humanize 1.0 and 2.0 side by side (`README.md:7-9`, `README.md:109-159`).
- algorithmic_behavior: Root coordination is split across `commands/` command contracts, `scripts/` setup/runtime helpers, `hooks/` loop gates, `prompt-template/` generated prompts/block reasons, `agents/` task-agent policies, `src/` MCP/workflow runtime, `flow/` HTML workflow cartridges, `viz/` monitors, and `tests/` executable specs. `package.json:12-22` exposes build, hub, smoke, test, and typecheck entrypoints.
- inputs_outputs_state: Inputs include Claude command arguments, hook JSON, merged config, plan files, BitLesson knowledge, workflow HTML, JSON-RPC/MCP calls, and agent artifacts. Outputs include `.humanize/rlcr` loop state, `.humanize/skill` invocations, cache logs, prompt/summary/contract files, workflow artifacts/events/boards, and monitor dashboards.
- gates_or_invariants: Major invariants are path safety, current-round scoping, state-file ownership, BitLesson delta discipline, provider routing, schema validation, workflow expectation satisfaction, and terminal monitor non-crash behavior. Hook JSON validation is centralized in `hooks/lib/loop-common.sh:91-165`; workflow artifact validation is in `src/workflows/coordinator.ts:1422-1460`.
- dependencies_and_callers: Runtime depends on Node >=22, TypeScript/tsx, `parse5`, `zod`, MCP SDK, shell, `jq`, `git`, Codex CLI, Claude CLI, optional Gemini, and Python for the viz server. Root callers are plugin commands, shell users sourcing `scripts/humanize.sh`, MCP clients, test scripts, and workflow cartridges under `flow/`.
- edge_cases_or_failure_modes: Covered failure modes include missing binaries, unknown model names, malformed config, malformed hook JSON, deep JSON, invalid UTF-8, no active loop, no git repo, terminal width/log issues, schema mismatch, undeclared artifacts, and stale/wrong loop files.
- validation_or_tests: Recursive inventory found 108 test files plus 16 robustness specs. Assigned tests cover BitLesson routing, skill monitor behavior, workflow schemas, and hook/monitor robustness; `README.md:161-167` lists `npm test`, `npm run typecheck`, and `npm run build` as development checks.
- skip_candidate: `no`

### H2_DEV-HZ-031 `file` `agents/plan-understanding-quiz.md`
- cursor: `[_]`
- core_role: Agent policy for the pre-RLCR Plan Understanding Quiz; it verifies user comprehension of the implementation mechanics before loop setup (`agents/plan-understanding-quiz.md:1-6`).
- algorithmic_behavior: The agent reads supplied plan content, explores repository context, then emits exactly two technical multiple-choice questions and a short technical summary (`agents/plan-understanding-quiz.md:14-31`, `agents/plan-understanding-quiz.md:53-75`).
- inputs_outputs_state: Inputs are the plan file content plus repo context via Read/Glob/Grep. Output is a strict 13-field text contract: question fields, four options per question, one answer per question, and `PLAN_SUMMARY` (`agents/plan-understanding-quiz.md:57-75`). The command layer presents answers to the user and may stop setup if the user chooses to review first (`commands/start-rlcr-loop.md:60-105`).
- gates_or_invariants: Exactly two questions, exactly four options each, exactly one correct answer, answer letter A-D, same language as plan, implementation-focused rather than title-level, and all fields required (`agents/plan-understanding-quiz.md:31-42`, `agents/plan-understanding-quiz.md:77-85`).
- dependencies_and_callers: Called by `commands/start-rlcr-loop.md` through the Task tool with opus model (`commands/start-rlcr-loop.md:75-83`). Humanize2 also models a quiz generator and human confirmation in `flow/rlcr/workflow.html:56-60`.
- edge_cases_or_failure_modes: If plan detail is sparse, derive questions from available hints (`agents/plan-understanding-quiz.md:84`). If command parsing sees malformed agent output, setup continues with a warning rather than hard-blocking (`commands/start-rlcr-loop.md:86`).
- validation_or_tests: Contract is validated indirectly by command and first-party workflow tests; the assigned file itself is policy, not executable code.
- skip_candidate: `no`

### H2_DEV-HZ-061 `file` `scripts/real-btc-smoke.ts`
- cursor: `[_]`
- core_role: Real-agent smoke script that exercises the Humanize2 `agent_run` path through Codex and/or Claude, including external network retrieval and file creation (`scripts/real-btc-smoke.ts:16-33`).
- algorithmic_behavior: Accepts `codex`, `claude`, or `all`; builds a prompt requesting a concise BTC spot-price Markdown file; calls `callHumanizeTool` against `src/index.ts`; parses the text JSON payload; then verifies the target file exists and is non-empty (`scripts/real-btc-smoke.ts:35-78`).
- inputs_outputs_state: Inputs are CLI arg, environment, installed `tsx`, agent backends, network market-data source, and project root. Outputs are `temp/btc-price-today-codex.md` and/or `temp/btc-price-today-claude.md`, plus console status (`scripts/real-btc-smoke.ts:7-14`, `scripts/real-btc-smoke.ts:72-77`).
- gates_or_invariants: Usage errors exit 2; RPC timeout is 900s; per-agent timeout is 840s; payload must have `success`; target must be a non-empty regular file; Codex gets workspace-write sandbox and skip-git check while Claude gets bypass permissions (`scripts/real-btc-smoke.ts:19-22`, `scripts/real-btc-smoke.ts:45-60`, `scripts/real-btc-smoke.ts:68-75`).
- dependencies_and_callers: `package.json:18` wires this as `npm run smoke:btc`. It depends on `src/dev-client.js`, `src/index.ts`, `node_modules/tsx/dist/cli.mjs`, external agent CLIs, and network market endpoints.
- edge_cases_or_failure_modes: Invalid agent argument, missing build/runtime deps, agent timeout/failure, non-JSON tool response, network failure, empty output file, or read-only execution environment. I did not run it because this assignment forbids modifications and the script writes `temp/`.
- validation_or_tests: The script is itself a smoke validation path for real backends rather than a mocked unit test.
- skip_candidate: `no`

### H2_DEV-HZ-091 `file` `tests/test-bitlesson-select-routing.sh`
- cursor: `[_]`
- core_role: Executable routing specification for `scripts/bitlesson-select.sh`, covering model-to-provider decisions, fallback behavior, and safe Codex selector invocation.
- algorithmic_behavior: Creates temporary BitLesson files, project configs, and mock `codex`/`claude` binaries; runs `bitlesson-select.sh`; asserts output and captured arguments (`tests/test-bitlesson-select-routing.sh:19-135`, `tests/test-bitlesson-select-routing.sh:137-506`).
- inputs_outputs_state: Inputs are `--task`, `--paths`, `--bitlesson-file`, `.humanize/config.json`, `PATH`, and mock BitLesson content. Outputs are `LESSON_IDS`/`RATIONALE`, captured mock stdin/args, and pass/fail summary.
- gates_or_invariants: `gpt-*` routes to Codex; `haiku`/`sonnet`/`opus` routes to Claude case-insensitively; unknown model exits non-zero; missing Codex for Codex route fails; missing Claude falls back to Codex; `provider_mode: codex-only` forces Codex; placeholder BitLesson files short-circuit to `NONE`; Codex helper must use trailing stdin `-`, disable hooks when supported, use read-only/ephemeral/skip-git flags, and avoid `--full-auto` (`tests/test-bitlesson-select-routing.sh:137-504`).
- dependencies_and_callers: Directly targets `scripts/bitlesson-select.sh`, which loads `config-loader`, `model-router`, `project-root`, `portable-timeout`, and `loop-common` (`scripts/bitlesson-select.sh:9-21`). Routing implementation is in `scripts/lib/model-router.sh:10-30`.
- edge_cases_or_failure_modes: Strict `PATH` isolation avoids accidental real binaries (`tests/test-bitlesson-select-routing.sh:9-12`); help-output probing avoids an `echo | grep -q` pipefail/SIGPIPE hazard (`tests/test-bitlesson-select-routing.sh:497-504`, implemented at `scripts/bitlesson-select.sh:191-208`).
- validation_or_tests: Self-contained shell test ending in `print_test_summary` (`tests/test-bitlesson-select-routing.sh:506`); included in `tests/run-all-tests.sh` per search evidence.
- skip_candidate: `no`

### H2_DEV-HZ-121 `file` `tests/test-skill-monitor.sh`
- cursor: `[_]`
- core_role: Executable spec for `_humanize_monitor_skill`, the terminal/once-mode monitor for `.humanize/skill` ask-codex and ask-gemini invocations (`tests/test-skill-monitor.sh:1-7`).
- algorithmic_behavior: Builds mock git repos and `.humanize/skill/<timestamp>` directories, sources `scripts/humanize.sh`, invokes `_humanize_monitor_skill --once`, and checks aggregate counts, focused invocation selection, question extraction, output display, and directory filtering (`tests/test-skill-monitor.sh:41-104`, `tests/test-skill-monitor.sh:106-404`).
- inputs_outputs_state: Inputs are skill invocation directories containing `input.md`, optional `metadata.md`, optional `output.md`, and status values. Outputs are once-mode status text with total/success/error/timeout/empty/running counts, focused invocation details, watched output, and recent list (`scripts/lib/monitor-skill.sh:339-425`).
- gates_or_invariants: Missing `.humanize/skill` and empty invocation set return non-zero; valid invocation names must begin with timestamp format; missing metadata means running; newest invocation with content is preferred; only first question line is displayed; non-timestamp dirs are ignored (`scripts/lib/monitor-skill.sh:43-48`, `scripts/lib/monitor-skill.sh:77-143`, `scripts/lib/monitor-skill.sh:145-152`).
- dependencies_and_callers: `humanize monitor skill`, `humanize monitor codex`, and `humanize monitor gemini` dispatch to this function (`scripts/humanize.sh:1355-1371`). It depends on monitor common helpers, git root detection, cache layout, shell terminal functions, and `humanize_split_to_array`.
- edge_cases_or_failure_modes: Running invocation without metadata, empty response status, no output file, absent cache, legacy unknown tool treated as Codex for filtering, and unrelated directories ignored (`scripts/lib/monitor-skill.sh:50-75`, `scripts/lib/monitor-skill.sh:165-217`).
- validation_or_tests: This file is the focused test suite for the monitor; broader monitor crash behavior is covered by the robustness item below.
- skip_candidate: `no`

### H2_DEV-HZ-151 `file` `tests/workflow-schema.test.ts`
- cursor: `[_]`
- core_role: Vitest contract for Humanize2 artifact schema validation and workflow expectation enforcement.
- algorithmic_behavior: Tests default registry validation, custom Zod validator registration, artifact delivery with accepted content, artifact delivery with schema mismatch, continuation retry messaging, and unregistered schema handling (`tests/workflow-schema.test.ts:10-136`).
- inputs_outputs_state: Inputs are workflow HTML, schema names, delivered artifact content, fake agent backends, and deterministic IDs/clocks. Outputs are `ArtifactRecord.validationStatus`, workflow run status, and events such as `artifact.schema_mismatch`, `agent.expectation_satisfied`, and `agent.expectation_retry` (`tests/workflow-schema.test.ts:44-103`).
- gates_or_invariants: Registered schema pass yields `accepted`; registered schema failure yields `schema-mismatch`; invalid artifact cannot satisfy an agent expectation; retry message must mention the missing schema; unregistered schema delivered under a declared manifest becomes `manifest-undeclared` (`src/workflows/coordinator.ts:1422-1460`, `src/workflows/coordinator.ts:1497-1523`).
- dependencies_and_callers: Uses `createSchemaRegistry`, `createDefaultSchemaRegistry`, `WorkflowCoordinator`, `AgentRunCoordinator`, `HumanizeService`, fake backends, and `zod` (`tests/workflow-schema.test.ts:1-9`). Default validators live in `src/workflows/schema-registry.ts:84-175`.
- edge_cases_or_failure_modes: Malformed artifact content, unregistered schema names, retry exhaustion, schema names declared in manifest but not registry, and producer/iteration mismatch preventing expectation satisfaction.
- validation_or_tests: This file is the validation suite; it directly exercises `src/workflows/schema-registry.ts` and `src/workflows/coordinator.ts`.
- skip_candidate: `no`

### H2_DEV-HZ-181 `file` `prompt-template/block/methodology-analysis-state-file-modification.md`
- cursor: `[_]`
- core_role: Block-message template enforcing that `methodology-analysis-state.md` is loop-managed during Methodology Analysis Phase (`prompt-template/block/methodology-analysis-state-file-modification.md:1-9`).
- algorithmic_behavior: When a user/agent attempts to modify the methodology-analysis state file, loop helpers render this template and instruct the agent to focus on analysis, sanitized report review, optional GitHub issue filing, and writing `methodology-analysis-done.md`.
- inputs_outputs_state: Input is the template load request from `methodology_analysis_state_file_blocked_message`; output is a Markdown block emitted by Write/Edit/Bash validators. State transition protected: active loop state must remain managed by the loop system, not by tool calls (`hooks/lib/loop-common.sh:1017-1024`).
- gates_or_invariants: Direct Write/Edit/Bash modification of `methodology-analysis-state.md` is blocked; more specific methodology-state checks run before generic `state.md` checks to avoid misclassification (`hooks/loop-write-validator.sh:198-205`, `hooks/loop-edit-validator.sh:161-168`, `hooks/loop-bash-validator.sh:271-278`).
- dependencies_and_callers: Depends on `hooks/lib/template-loader.sh` through `load_and_render_safe`; called from `loop-common`, then from `loop-write-validator.sh`, `loop-edit-validator.sh`, and `loop-bash-validator.sh`.
- edge_cases_or_failure_modes: Missing template falls back to a shorter built-in message (`hooks/lib/loop-common.sh:1017-1024`); Bash bypass attempts through redirection, `mv`, `cp`, shell wrappers, or source/destination state-file patterns are separately detected (`hooks/loop-bash-validator.sh:299-330`, `hooks/loop-bash-validator.sh:428-468`).
- validation_or_tests: Covered by hook robustness patterns and state-file protection tests; assigned robustness test exercises the common JSON and Bash modification detection surface used by these validators.
- skip_candidate: `no`

### H2_DEV-HZ-211 `file` `prompt-template/claude/post-alignment-action-items.md`
- cursor: `[_]`
- core_role: Prompt fragment appended after a Full Goal Alignment Check to steer the next implementation round toward alignment findings (`prompt-template/claude/post-alignment-action-items.md:2-8`).
- algorithmic_behavior: Adds a short checklist to the next-round prompt emphasizing forgotten tasks, unmet acceptance criteria, unjustified deferrals, and queued issues that have become blockers.
- inputs_outputs_state: Input is `FULL_ALIGNMENT_CHECK=true` during stop-hook prompt construction. Output is appended Markdown in `NEXT_PROMPT_FILE`; it changes next-round agent priorities without directly mutating loop state (`hooks/loop-codex-stop-hook.sh:2164-2169`).
- gates_or_invariants: Only appended when the alignment flag is true and the template loads non-empty. It preserves the invariant that queued non-blocking work stays queued unless it now blocks mainline progress (`prompt-template/claude/post-alignment-action-items.md:4-8`).
- dependencies_and_callers: Loaded by `load_template` in `hooks/loop-codex-stop-hook.sh`; coordinated with the next-round footer and task-tag routing notes appended immediately after it (`hooks/loop-codex-stop-hook.sh:2172-2177`).
- edge_cases_or_failure_modes: If the template is missing or empty, no post-alignment section is appended. If alignment findings are stale or too broad, the fragment still narrows behavior to forgotten items, AC status, deferrals, and blocker escalation.
- validation_or_tests: Template presence and hook template loading are covered by the repository’s template-related tests; direct integration point is the stop-hook append block cited above.
- skip_candidate: `no`

### H2_DEV-HZ-241 `file` `tests/robustness/test-hook-input-robustness.sh`
- cursor: `[_]`
- core_role: Robustness executable spec for hook input parsing, shell command modification detection, and monitor helper non-crash behavior (`tests/robustness/test-hook-input-robustness.sh:1-10`).
- algorithmic_behavior: Pipes crafted JSON into production hook validators, checks exit codes and messages, creates log/terminal edge cases, calls production parser helpers, and launches real monitor functions in controlled wrappers (`tests/robustness/test-hook-input-robustness.sh:35-235`, `tests/robustness/test-hook-input-robustness.sh:245-670`).
- inputs_outputs_state: Inputs are JSON hook payloads for Read/Write/Bash, long commands, special chars, Unicode, deep JSON, binary bytes, null bytes, temporary logs, fake `.humanize/rlcr` sessions, and fake cache dirs. Outputs are pass/fail assertions and monitor exit-code captures.
- gates_or_invariants: Valid JSON for known tools passes; malformed JSON, missing `tool_name`, missing required `tool_input` fields, excessive nesting, and invalid UTF-8 reject without signal crash; unknown tool passes through; sed/redirect modifications must be detected by `command_modifies_file`; production parsers must return pipe-delimited summaries (`tests/robustness/test-hook-input-robustness.sh:35-217`, `tests/robustness/test-hook-input-robustness.sh:351-422`).
- dependencies_and_callers: Sources `hooks/lib/loop-common.sh` and `tests/test-helpers.sh`; invokes `hooks/loop-read-validator.sh`, `hooks/loop-write-validator.sh`, `hooks/loop-bash-validator.sh`, and functions from `scripts/humanize.sh` (`tests/robustness/test-hook-input-robustness.sh:14-17`, `tests/robustness/test-hook-input-robustness.sh:381-428`).
- edge_cases_or_failure_modes: Long 10KB command, shell metacharacters, Unicode paths, 50-level JSON, non-UTF8 binary content, Bash-stripped null bytes, ANSI logs, binary logs, rapid log growth, narrow/wide terminals, missing session dirs, and deleted live session dirs.
- validation_or_tests: This file is itself a broad validation gate for the hook/monitor algorithm. The production JSON guards it verifies are in `hooks/lib/loop-common.sh:91-165`; monitor functions are in `scripts/humanize.sh:71-251` and `scripts/humanize.sh:261-760`.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 9 unique assigned item evidence headings present; manual count matches `assigned_item_count`
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`