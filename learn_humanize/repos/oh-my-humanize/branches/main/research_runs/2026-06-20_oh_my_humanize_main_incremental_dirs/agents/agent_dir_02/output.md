# agent_dir_02 oh-my-humanize main directory incremental research

## Worker Summary
- status: `[_]`
- source_commit_old: `6b3819fad50a89fffae899b240ad1ce065c51d23`
- source_commit_new: `bf4509d4f5a669375b3c88510ba0449e9770884c`
- assigned_item_count: 1

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-005 `directory` `packages`
- cursor: `[_]`
- current_directory_core_role:
  - `packages/` is the monorepo package root. For this refresh, the effective core responsibility is concentrated in `packages/coding-agent/`, which owns the CLI-facing workflow command surface, workflow package loading/freezing, runtime host adapters, scheduler/runner lifecycle persistence, and workflow test contracts.
  - The relevant workflow stack is layered as: `src/cli/workflow-cli.ts` resolves and starts frozen workflow artifacts; `src/workflow/session-runtime.ts` adapts workflow nodes to eval/shell/agent/human runtimes; `src/workflow/runner.ts` materializes resources, executes nodes, persists run/lifecycle events, and finalizes attempts; `src/workflow/scheduler.ts` schedules activations, propagates stop/frontier state, and classifies activation statuses.
  - The directory still spans many packages (`ai`, `catalog`, `agent`, `tui`, `utils`, etc.), but the changed core descendants only alter `packages/coding-agent` workflow behavior.

- directory_level_delta_since_old_commit:
  - Headless workflow start now resolves a concrete workflow cwd once via `path.resolve(command.flags.cwd ?? getProjectDir())` and threads that cwd into the headless runtime host for eval scripts, shell scripts, and spawned agent tasks (`packages/coding-agent/src/cli/workflow-cli.ts`).
  - Headless JavaScript workflow scripts now execute with `process.chdir(cwd)` around the `AsyncFunction` invocation and restore both `console.log` and the previous process cwd in `finally`. This makes `Bun.file("relative-path")` and other cwd-relative reads use `omp workflow start --cwd`, while preserving structured top-level returns as captured output.
  - Headless `omp workflow start` now installs a start-signal controller for `SIGINT`/`SIGTERM`, passes the same signal as both scheduler stop signal and node abort signal, and always disposes listeners after `runWorkflow` completes.
  - Runner options now include `nodeAbortSignal`, `nodeAbortSignalForActivation`, and `maxRuntimeMs`. The runner derives a combined runtime timeout signal when `maxRuntimeMs` is present, forwards it to the scheduler, and clears the timer in `finally`.
  - Runner node execution is wrapped by `awaitWorkflowNodeExecution(...)`, which races node execution against the node abort signal. If the runtime ignores abort and never settles, the runner rejects on the next abort turn with the signal reason, persists the activation as aborted, and lets lifecycle checkpointing proceed instead of waiting forever.
  - Lifecycle finalization now treats scheduler limit, scheduler stop, signal abort, and deadline/max-runtime aborts as checkpointable stop states rather than failed attempts when there is no failed activation.
  - Changelog documents two user-visible fixes under `[Unreleased]`: ignored abort signals no longer keep workflow stop waiting forever, and headless `omp workflow start --cwd` now works for JavaScript workflow script nodes.
  - The demo script `examples/workflow-demos/human-interactive-dev/.../scripts/implementation.sh` now creates `artifacts/` before writing `artifacts/implementation.txt`, making the demo script compatible with fresh cwd/resource layouts.

- affected_descendant_algorithms:
  - `handleStart` in `workflow-cli.ts`: resolves the run cwd, restricts headless starts to frozen `.omhflow` artifacts, constructs an in-memory run store, creates a session workflow runtime host, binds runtime availability, installs signal handling, calls `runWorkflow`, reconstructs runs/families, and reports `completed`/`stopped`/`failed`.
  - `runHeadlessEvalScript` in `workflow-cli.ts`: executes only JS eval scripts in-process, captures `console.log`, captures top-level return values via formatting, temporarily changes cwd to the requested workflow cwd, restores cwd/logging in `finally`, and reports `{ exitCode, output, error, language }`.
  - `runHeadlessShellScript` in `workflow-cli.ts`: spawns `sh -c` with `cwd`, stdout/stderr pipes, request abort signal, and workflow script environment including resource context.
  - `runHeadlessAgentTask` and `buildHeadlessAgentTaskArgs` in `workflow-cli.ts`: spawn the current CLI invocation with `launch --cwd <cwd>`, optional `--model`, and assignment prompt, so subagent work inherits the workflow cwd.
  - `workflowRuntimeSignal` in `runner.ts`: creates an aborting timeout controller from `maxRuntimeMs`, combines it with scheduler and node abort signals, preserves abort reasons, and disposes timeout state.
  - `executeAndPersistActivation` in `runner.ts`: after prompt/script/model resolution, it chooses `context.nodeAbortSignal ?? context.signal` as the execution signal, passes that into node runtime execution, wraps the promise with abort racing, and records completed/failed/aborted run-store and lifecycle events.
  - `awaitWorkflowNodeExecution` in `runner.ts`: the new ignored-abort guard. It uses `Promise.withResolvers`, subscribes to abort, schedules a zero-delay rejection with the signal reason, settles exactly once, and removes the listener.
  - `finishLifecycleAttempt` / `workflowCheckpointReason` in `runner.ts`: failed activations still fail the attempt, but activation limits and aborted frontier-bearing runs request stop and create checkpoints with completed and aborted activation ids.
  - `runWorkflowScheduler` in `scheduler.ts`: consumes separate scheduler and node abort signals, passes node signals to execution contexts, marks abort-classified results as `aborted`, records the aborted activation’s node as frontier, stops downstream scheduling, and preserves eligible frontier nodes when a stop signal arrives after a completion.

- current_inputs_outputs_state:
  - Inputs:
    - CLI action/flags: `omp workflow start <flow-or-path>`, `--cwd`, `--run-id`, `--family-id`, `--start`, `--max-activations`, `--max-node-activations`, `--max-runtime-ms`, `--json`.
    - Workflow artifacts: frozen `.omhflow` file plus same-name resource directory; raw YAML package starts are rejected for headless start.
    - Runtime signals: process `SIGINT`/`SIGTERM`, optional injected test signal target, user stop signal, node abort signal, per-activation node abort function, and max-runtime timeout.
    - Node inputs: workflow definition, resolved prompt, frozen resources, model resolution audit, current state, completed activations, and resource directory.
  - Outputs:
    - CLI JSON/non-JSON run summary with flow metadata, run status, activation counts, frontier node ids, families, attempts, checkpoints, and run state keys.
    - Run-store custom entries: activation started/completed/failed/aborted, state patch events, run reconstruction state.
    - Lifecycle custom entries: family/freeze/attempt started, activation started/completed/failed/aborted, attempt stopped/completed/failed, checkpoint created.
    - Script outputs: JS eval output from `console.log` and top-level return formatting; shell output from stdout/stderr; structured workflow activation output is validated and may become state patches.
    - Demo shell output now includes an artifact file under `artifacts/implementation.txt` and emits a JSON state patch.

- new_or_changed_gates_or_invariants:
  - Headless workflow start gate: starts require frozen `.omhflow` artifacts; raw workflow authoring packages are rejected with a package error and no stack trace.
  - Cwd invariant: `--cwd` is the execution cwd for headless JS scripts, shell scripts, and spawned agent tasks. JS eval specifically must restore the previous process cwd after execution or failure.
  - Signal cleanup invariant: headless start signal listeners for `SIGINT` and `SIGTERM` are removed after the run completes.
  - Abort classification invariant: when the node abort signal or scheduler signal is aborted, node execution errors become activation status `aborted`, not `failed`.
  - Ignored-abort invariant: if a node runtime never resolves after the node abort signal fires, `awaitWorkflowNodeExecution` forces the activation to settle as aborted so lifecycle checkpointing can complete.
  - Deadline/max-runtime invariant: `maxRuntimeMs` aborts both scheduling and node execution with reason `workflow max runtime elapsed after <N>ms`; frozen lifecycle attempts are stopped and checkpointed rather than failed when no activation failed independently.
  - Frontier invariant: when cancellation happens after a completed activation, eligible downstream nodes are retained as checkpoint frontier; when an activation itself aborts, its own node is retained as frontier for restart.
  - Persistence invariant: checkpoint records include both `completedActivationIds` and `abortedActivationIds`; failed activations still create failed-attempt checkpoints through the failed path.

- dependencies_and_callers:
  - CLI callers enter through `runWorkflowCommand(...)` and `handleStart(...)` in `packages/coding-agent/src/cli/workflow-cli.ts`.
  - Artifact dependencies: `resolveWorkflowFlowSpec`, `loadWorkflowArtifact`, `freezeWorkflowArtifact`, and frozen resource snapshots feed package root/resource materialization.
  - Runtime host dependency: `createSessionWorkflowRuntimeHost(...)` converts workflow node execution into headless eval/shell/agent adapters. It forwards `input.signal` to agent/review requests and shell requests; eval requests do not carry a signal directly, so runner-level abort racing is the guard for async eval execution that does not cooperate.
  - Scheduler dependency: `runWorkflowScheduler(...)` receives `signal`, `nodeAbortSignal`, and `nodeAbortSignalForActivation` from `runWorkflow(...)`, then provides `context.signal` and `context.nodeAbortSignal` to the runner’s `executeNode` callback.
  - Lifecycle/run-store dependencies: `appendWorkflowActivationAborted`, `appendWorkflowAttemptActivationAborted`, `requestWorkflowAttemptStop`, `createWorkflowCheckpoint`, `reconstructWorkflowRuns`, and `reconstructWorkflowFamilies` are the persistence/readback surface for the new stop/checkpoint semantics.
  - Timeout dependency: `DEFAULT_WORKFLOW_MAX_RUNTIME_MS` is used by headless start when no explicit `--max-runtime-ms` is provided; `workflowMaxRuntimeStopReason` supplies the stable abort/checkpoint reason.
  - Tests call `runWorkflowCommand` directly with temporary artifacts and a fake signal target, and call `runWorkflow` directly with controlled runtime hosts and abort controllers.

- edge_cases_or_failure_modes:
  - JS eval cwd is process-global. The implementation restores cwd in `finally`, but concurrent in-process eval work would share process cwd during the execution window. Current headless CLI execution is effectively scoped to a run, but this remains a concurrency-sensitive design point.
  - JS eval cannot be forcibly preempted if it enters a synchronous infinite loop because it runs in the same JS thread; runner abort racing only settles once the event loop can process the abort callback. Async ignored-abort cases are covered.
  - `runHeadlessEvalScript` does not pass a request signal into the eval adapter. Node-level abort is enforced by the runner wrapper around `executeWorkflowNode`, not by cooperative eval code.
  - `combineAbortSignals` installs listeners without explicit removal after one signal wins. The combined signal objects are short-lived and timer disposal is handled, but long-lived external signals could retain one listener until they abort.
  - Headless shell/agent subprocesses receive `request.signal`; if subprocess output streams or child exit handling behave oddly on abort, scheduler classification still depends on the abort signal reason when the execution promise rejects.
  - If a workflow aborts before any frontier exists, checkpoint reason requires `scheduler.frontierNodeIds.length > 0`; empty-frontier aborted runs can complete without a checkpoint reason unless another limit/failure path applies.
  - Failed activations still dominate lifecycle finalization. If one activation fails while another aborts, the attempt is failed and the checkpoint includes aborted ids, but status is not stopped.
  - Headless start reports `failed` only from activation status `failed`; aborted lifecycle attempts report `stopped` through lifecycle attempt status or limit state.
  - The demo script now assumes the shell can create `artifacts/`; this removes missing-directory failure for fresh workspaces.

- validation_or_tests:
  - `packages/coding-agent/src/cli/__tests__/workflow-cli.test.ts` adds/contains a headless resource smoke: frozen shell script resources are passed via `OMP_WORKFLOW_RESOURCE_DIR`, the run completes, and state key `message` appears.
  - The same CLI test file pins JS cwd behavior: a JS workflow script reads `marker.txt` from the requested `--cwd`, returns a structured state patch, and the run completes with state key `marker`.
  - The same CLI test file pins SIGINT checkpoint behavior: a fake signal target emits `SIGINT` during a sleeping shell node, JSON output reports run status `stopped`, frontier `["hold"]`, stopped attempt, checkpoint frontier `["hold"]`, and zero remaining signal listeners.
  - Existing/nearby CLI tests also pin package errors: ambiguous flow/package errors are printed without source stack traces, and headless start rejects non-artifact workflow packages.
  - `packages/coding-agent/test/workflow/runner.test.ts` pins cancellation after completion: aborting the scheduler signal after `build` completes prevents `review`, stops the attempt, and checkpoints frontier `review`.
  - Runner tests pin separated scheduler vs node abort signals: node runtime receives the dedicated node abort signal while scheduler stop prevents downstream scheduling.
  - Runner tests pin deadline-aborted activations: a node abort after scheduler stop is persisted as activation `aborted`, the attempt is `stopped`, and checkpoint `abortedActivationIds` contains `activation-1`.
  - Runner tests pin ignored-abort handling: a runtime that returns a never-settling promise still causes `runWorkflow` to settle within the test race after node abort, with activation `aborted` and a stopped checkpoint.
  - Runner tests pin max runtime: `maxRuntimeMs: 1` aborts the node with reason `workflow max runtime elapsed after 1ms`, marks the activation aborted, stops the attempt, and checkpoints the aborted activation/frontier.
  - I inspected the current read-only source export and test contracts; I did not execute the test suite in this read-only research pass.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `OH_MY_HUMANIZE_MAIN-HZ-005`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`