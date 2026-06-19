# agent_dir_05 oh-my-humanize main directory incremental research

## Worker Summary
- status: `[_]`
- source_commit_old: `6b3819fad50a89fffae899b240ad1ce065c51d23`
- source_commit_new: `bf4509d4f5a669375b3c88510ba0449e9770884c`
- assigned_item_count: 1

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-250 `directory` `packages/coding-agent/src/cli`
- cursor: `[_]`
- current_directory_core_role:
  The `packages/coding-agent/src/cli` directory is the coding-agent command adapter layer. For workflows, `workflow-cli.ts` owns the non-TUI `omp workflow` execution surface: it normalizes command args, dispatches `list` / `freeze` / `start` / `install` / `uninstall`, resolves flow names or artifact paths relative to `--cwd` or `getProjectDir()`, loads and freezes `.omhflow` artifacts, constructs a headless workflow runtime host, maps lifecycle/run output into text or JSON, and converts known package/registry failures into concise stderr messages without stack traces. The command class in `src/commands/workflow.ts` lazy-loads this directory module and defines the public flags that become `WorkflowCommandArgs`.
- directory_level_delta_since_old_commit:
  The changed CLI responsibility is concentrated in headless `workflow start`. Start now treats the requested cwd as the execution cwd for JS workflow scripts, not only as a path-resolution base. `runHeadlessEvalScript(cwd, code, language)` temporarily calls `process.chdir(cwd)` around JS eval execution, captures `console.log`, formats returned values, and restores both `console.log` and the previous process cwd in `finally`. This aligns JS eval script behavior with shell and agent nodes, which already spawn with `cwd`.
  The CLI also now owns interrupt-to-abort wiring for headless starts. `handleStart` creates a `WorkflowStartSignalController` from `process` or an injected test signal target, passes the same signal as both `signal` and `nodeAbortSignal` into `runWorkflow`, and disposes listeners after the run completes. This makes SIGINT/SIGTERM stop both downstream scheduling and the currently running node, allowing lifecycle checkpointing rather than leaving a live or hanging headless attempt.
  Although `packages/coding-agent/src/workflow/runner.ts` is outside this assigned directory, the CLI delta depends on its new behavior: runner combines `maxRuntimeMs` deadlines with scheduler and node abort signals, treats aborted node execution as `aborted` rather than `failed`, creates stopped-attempt checkpoints for aborted/frontier state, and wraps node execution so ignored aborts still unblock after an abort checkpoint path.
- affected_descendant_algorithms:
  `resolveWorkflowCommandArgs` continues to map public CLI flags into typed workflow command flags, including `--cwd`, `--max-runtime-ms`, activation caps, run/family IDs, `--start`, `--json`, and `--force`.
  `handleStart` is the main affected algorithm: resolve cwd; resolve/load/freeze artifact; compute default root start nodes; create in-memory run store; build headless runtime host; create runtime binding snapshot; reject unavailable human/headless bindings unless `maxActivations === 0`; attach start signal; run `runWorkflow` with package root, frozen resources, activation limits, lifecycle metadata, max runtime, scheduler abort signal, and node abort signal; reconstruct run/family evidence; derive user-facing status; emit JSON or text.
  `createWorkflowStartSignalController` is a new/changed support algorithm for converting process `SIGINT`/`SIGTERM` events into a single abort reason string like `workflow interrupted by SIGINT`, while guaranteeing listener removal through `dispose`.
  `runHeadlessEvalScript` is now cwd-sensitive. It rejects Python eval scripts, runs JS code through `AsyncFunction`, captures console output and return values, and restores global process state even on script failure.
  The headless shell and agent task adapters remain part of the same start algorithm: shell uses `Bun.spawn(["sh", "-c", code], { cwd, signal, env: workflowScriptEnvironment(...) })`; agent task builds a nested CLI launch command with `--cwd`.
- current_inputs_outputs_state:
  Inputs are workflow action, target args, and flags from `omp workflow` / `omp flow`; `OMHFLOW_DIR` may affect named flow lookup; cwd defaults to `getProjectDir()` but may be overridden with `--cwd`.
  `list` outputs discovered flow specs as text or `{ flows }` JSON.
  `freeze` outputs freeze ID, graph/resource counts, and flow info as text or JSON.
  `install` / `uninstall` output installed/uninstalled flow metadata and use cwd for source resolution where relevant.
  `start` accepts only frozen distributable `.omhflow` artifacts for headless starts. It outputs run summary and frontier as text, or JSON with `flow`, `run`, `families`, and `runs`. The JSON run object includes status, activation counts, frontier node IDs, and effective `maxRuntimeMs`. Family JSON includes freezes, attempts, checkpoints, and change request summaries. Run JSON includes run IDs, activation counts, and sorted state keys.
  Runtime outputs from scripts/tasks are converted into workflow activation outputs through `createSessionWorkflowRuntimeHost`; state patches and single-write structured data then flow through the runner/state validation layer.
- new_or_changed_gates_or_invariants:
  Headless `workflow start` must use a `.omhflow` artifact path; raw workflow directories or `workflow.yml` packages are rejected with `Workflow start requires a frozen .omhflow artifact...`.
  Headless JS script relative file access is now invariantly relative to the requested run cwd during script execution. The process cwd must be restored afterward, and `console.log` capture must also be restored.
  SIGINT/SIGTERM listeners must be one-shot, must abort only once, and must be removed after `runWorkflow` settles.
  Headless start must pass an abort signal to both workflow scheduling and node execution so a signal can stop scheduling and abort in-flight shell/agent/script work.
  Default max runtime remains applied at the CLI boundary: `command.flags.maxRuntimeMs ?? DEFAULT_WORKFLOW_MAX_RUNTIME_MS`.
  Known `WorkflowArtifactRegistryError` and `WorkflowPackageError` failures remain user-facing stderr messages with `process.exitCode = 1`, not stack traces.
  A binding availability gate still prevents headless starts for human-node flows, except the explicit `maxActivations === 0` path can bypass execution-time binding failure.
- dependencies_and_callers:
  Public caller: `packages/coding-agent/src/commands/workflow.ts` defines the `workflow` command and `flow` alias, parses flags through the command framework, then calls `resolveWorkflowCommandArgs(...)` and `runWorkflowCommand(...)`.
  Workflow CLI depends on `artifact-registry` for list/resolve/install/uninstall, `package-loader` and `freeze` for artifact loading/freezing, `runtime-binding` for headless capability checks, `session-runtime` for adapting workflow nodes to CLI shell/eval/task runners, `runner` for scheduler/lifecycle execution, and `run-store`/`lifecycle` reconstruction for output evidence.
  The new signal behavior depends on `runWorkflow` honoring `signal`, `nodeAbortSignal`, and `maxRuntimeMs`. Runner now combines CLI interrupt signals with deadline signals and reports aborted activations/checkpoints in lifecycle state.
  Headless shell execution depends on Bun process spawning and `workflowScriptEnvironment`; headless JS eval depends on process-wide cwd and console overrides, so it is intentionally serialized within one eval call and restored in `finally`.
- edge_cases_or_failure_modes:
  A JS workflow script that reads relative paths with `Bun.file("...")` previously risked reading from the parent process cwd; it now reads from `--cwd`. Failure mode remains that `process.chdir(cwd)` will fail if the cwd does not exist or is inaccessible, returning an eval error result.
  Because JS eval changes process cwd and `console.log` globally during execution, concurrent in-process headless JS evals would contend for process-global state. The current CLI start path runs within one headless workflow invocation, but this remains a relevant concurrency caution for future parallel eval execution.
  If a workflow node runtime ignores abort, runner-side abort wrapping is required so CLI SIGINT/deadline can still checkpoint instead of hanging forever.
  If SIGINT/SIGTERM arrives after listeners are disposed, the workflow run is unaffected by this controller. If both arrive, only the first abort reason is preserved.
  For shell nodes, abort depends on Bun spawn signal behavior; nonzero exit maps stderr or `exit code N` into workflow node failure unless the runner observes the abort signal and records an aborted activation.
  Human-node flows are still unavailable in headless CLI and surface as binding errors rather than attempting interaction.
  `WorkflowPackageError` from non-artifact starts is intentionally caught and printed without source stack traces.
- validation_or_tests:
  `packages/coding-agent/src/cli/__tests__/workflow-cli.test.ts` now includes a cwd contract test: a frozen JS workflow script reads `marker.txt` from a separate requested `--cwd` workspace and must complete with state key `marker`.
  The same CLI test file includes a SIGINT checkpoint contract test: a fake signal target emits `SIGINT` while a shell script sleeps; JSON output must show run status `stopped`, frontier `["hold"]`, stopped family attempt, checkpoint frontier `["hold"]`, and zero remaining SIGINT/SIGTERM listeners.
  Existing CLI tests also pin stackless ambiguous flow/package errors, rejection of non-artifact headless starts, and frozen resource availability to headless shell scripts.
  Related runner tests in `packages/coding-agent/test/workflow/runner.test.ts` pin the lower-level contracts the CLI now relies on: cancellation checkpoints downstream scheduling, dedicated node abort signals remain separate from scheduler stop signals, deadline-aborted lifecycle activations are checkpointed instead of failing attempts, runtimes that ignore abort still unblock into an aborted checkpoint, and `maxRuntimeMs` creates stopped attempts with abort reason `workflow max runtime elapsed after 1ms`.
  I did not execute tests in this read-only research pass; evidence is from direct source inspection of the current export.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `OH_MY_HUMANIZE_MAIN-HZ-250`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`