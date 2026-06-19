# agent_dir_01 oh-my-humanize main directory incremental research

## Worker Summary
- status: `[_]`
- source_commit_old: `6b3819fad50a89fffae899b240ad1ce065c51d23`
- source_commit_new: `bf4509d4f5a669375b3c88510ba0449e9770884c`
- assigned_item_count: 1

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-001 `directory` `.`
- cursor: `[_]`
- current_directory_core_role:
  - Repository root remains a multi-package workspace, but the changed core responsibility is concentrated in `packages/coding-agent/`: the coding-agent CLI now owns safer headless workflow start behavior for frozen `.omhflow` artifacts, while `src/workflow/runner.ts` owns converting runtime stops, deadlines, node aborts, and activation limits into resumable workflow lifecycle checkpoints.
  - The root-level algorithmic surface exposed by this directory is therefore: resolve a workflow artifact relative to the requested CLI cwd, freeze/load package resources, run workflow nodes through the session runtime, persist run/lifecycle events into the in-memory workflow store for headless CLI output, and return a completed/stopped/failed summary with run/family/checkpoint state.
  - The directory also continues to provide the workflow subsystem around this path: artifact lookup and install registry, `.omhflow` package loading, freezing/materialized resources, scheduler execution, node runtime dispatch, lifecycle reconstruction, run-store reconstruction, state patch validation, and workflow CLI tests.

- directory_level_delta_since_old_commit:
  - Headless workflow `start` is now explicitly constrained to frozen `.omhflow` artifacts. `loadWorkflowStartPackage()` rejects non-`.omhflow` workflow packages with a user-facing `WorkflowPackageError`, preventing raw `workflow.yml` starts in headless CLI mode and requiring the distributable artifact plus same-name resource directory.
  - The workflow CLI now resolves the requested run cwd once with `path.resolve(command.flags.cwd ?? getProjectDir())` and passes that same cwd into flow resolution, the session runtime host, JS eval scripts, shell scripts, and spawned agent tasks.
  - JS headless workflow scripts now execute from the requested cwd. `runHeadlessEvalScript()` temporarily saves `process.cwd()`, `process.chdir(cwd)`, captures `console.log`, executes the generated async function, formats returned values, then restores both `console.log` and the prior cwd in `finally`. This makes JS scripts behave like shell scripts and agent tasks for relative file access.
  - Headless workflow starts now install SIGINT/SIGTERM listeners through `createWorkflowStartSignalController()`. The controller aborts with reason `workflow interrupted by SIGINT` or `workflow interrupted by SIGTERM`, passes that AbortSignal as both `signal` and `nodeAbortSignal` into `runWorkflow()`, and removes listeners in a `finally` block after the run.
  - `runWorkflow()` now builds a combined runtime signal when `maxRuntimeMs` is supplied. The timeout abort reason is produced by `workflowMaxRuntimeStopReason(maxRuntimeMs)`, currently `workflow max runtime elapsed after ${maxRuntimeMs}ms`.
  - Runner lifecycle finish semantics changed: activation limits, scheduler stop signals, CLI interrupts, and max runtime deadlines now request attempt stop and create checkpoints instead of leaving a lifecycle attempt running or converting expected stops into failed attempts.
  - Node abort/deadline behavior now has two layers: scheduler stop signal controls whether more nodes are scheduled and what frontier is preserved; node abort signal is passed down to node execution and can mark the active activation as `aborted`.
  - Runner execution now wraps each node promise with `awaitWorkflowNodeExecution()`, so if the provided execution signal aborts and the node runtime ignores it, the runner rejects on the next timer tick and persists an aborted activation/checkpoint.
  - Headless CLI JSON output now derives `status` as `failed`, `stopped`, or `completed`, with `stopped` when the lifecycle attempt is stopped or scheduler activation limits are reached; JSON includes family attempts/checkpoints and run state keys for verification/automation.

- affected_descendant_algorithms:
  - `packages/coding-agent/src/cli/workflow-cli.ts`
    - Parses `--cwd`, `--run-id`, `--family-id`, start node, activation limits, and max runtime flags.
    - Resolves target flow against the requested cwd.
    - Loads only `.omhflow` frozen artifacts for headless start.
    - Creates a session workflow runtime host with cwd-bound eval/shell/agent adapters.
    - Installs SIGINT/SIGTERM abort wiring for `workflow start`.
    - Calls `runWorkflow()` with `signal`, `nodeAbortSignal`, lifecycle freeze metadata, materialized frozen resources, and default or explicit max runtime.
    - Formats CLI stdout/stderr and JSON result summaries.
  - `packages/coding-agent/src/workflow/runner.ts`
    - Starts run-store and lifecycle attempt events.
    - Combines external abort signals with max runtime timeout.
    - Materializes frozen resources before execution and removes them afterward.
    - Executes nodes through scheduler callbacks, persists run-store activation events, persists lifecycle activation events, validates state patches/output, and resolves package-local scripts.
    - Converts failure, cancellation, activation limit, signal abort, node abort, ignored node abort, and max runtime deadline outcomes into lifecycle terminal events plus checkpoints.
  - `packages/coding-agent/src/workflow/scheduler.ts`
    - Receives `signal`, `nodeAbortSignal`, and optional per-activation node abort signal from runner.
    - Stops new scheduling when workflow signal is aborted.
    - Computes frontier nodes from queued activations or eligible downstream nodes when cancellation happens after an activation completes.
    - Marks an activation `aborted` if execution throws while node/scheduler signal is aborted, and includes the aborted node in the frontier.
  - `packages/coding-agent/src/workflow/node-runtime.ts`
    - Carries the execution `signal` into agent, script, human, and review node runtime inputs.
  - `packages/coding-agent/src/workflow/session-runtime.ts`
    - Forwards node signal into agent/review task requests and shell script requests.
    - JS eval requests still do not carry a signal directly; the runner wrapper can checkpoint on abort once the event loop can observe the timeout/signal, but cannot preempt synchronous JS execution.
  - `packages/coding-agent/src/workflow/runtime-timeout.ts`
    - Centralizes default max runtime and user-visible deadline stop reason.
  - `packages/coding-agent/test/workflow/runner.test.ts`
    - Adds/extends contract tests for cancellation checkpointing, dedicated node abort signal propagation, deadline-aborted activations, ignored runtime aborts, and max runtime checkpoints.
  - `packages/coding-agent/src/cli/__tests__/workflow-cli.test.ts`
    - Adds/extends CLI tests for `.omhflow` artifact-only starts, frozen resource access, JS cwd semantics, SIGINT checkpointing, and signal listener cleanup.

- current_inputs_outputs_state:
  - Inputs:
    - CLI action `workflow start <flow-or-path>`.
    - Optional flags: `cwd`, `runId`, `familyId`, `startNodeId`, `maxActivations`, `maxNodeActivations`, `maxRuntimeMs`, `json`.
    - Flow target resolved as either explicit path or named built-in/`OMHFLOW_DIR` artifact.
    - Frozen `.omhflow` artifact metadata and same-name resource directory.
    - Runtime signals from process SIGINT/SIGTERM or injected test signal target.
    - Workflow node definitions, script files, frozen resource snapshots, model/runtime binding metadata, and workflow state schemas.
  - Outputs:
    - Human-readable CLI lines or one JSON object.
    - Run-store custom events: run started, activation started/completed/failed/aborted, state patch applied.
    - Lifecycle custom events: family created, freeze recorded, attempt started, runtime binding snapshot, activation lifecycle events, stop requested, checkpoint created, attempt completed/failed.
    - For stopped attempts, a checkpoint with `completedActivationIds`, `abortedActivationIds`, `frontierNodeIds`, current `state`, and `sourceMapping`.
    - For headless JS scripts, output can come from `console.log()` capture and/or returned value; structured JSON activation output is parsed by session runtime.
    - For shell scripts, stdout/stderr are collected from `Bun.spawn(["sh", "-c", request.code], { cwd, signal, env })`, and workflow context/resource env vars are injected when present.

- new_or_changed_gates_or_invariants:
  - Headless `workflow start` gate: target must be a frozen `.omhflow` file. Directory/raw workflow packages are rejected with a package-level error and no source stack trace.
  - Cwd invariant: all headless runtime adapters are expected to honor the requested run cwd; JS eval now does so through temporary `process.chdir(cwd)`.
  - Signal lifecycle invariant: headless CLI SIGINT/SIGTERM listeners must be one-shot abort sources and must be removed after run completion or stop.
  - Deadline invariant: when `maxRuntimeMs` elapses, both scheduler and node execution signals receive the same timeout reason, and lifecycle should stop/checkpoint rather than fail.
  - Separate stop-vs-node-abort invariant: `signal` controls scheduler/frontier progression; `nodeAbortSignal` controls active node cancellation. Passing a dedicated node abort signal must not be confused with the scheduler stop signal.
  - Checkpoint invariant: stopped/limited/aborted lifecycle attempts must have no running activation records before checkpoint creation; checkpoints include completed and aborted activation IDs matching lifecycle activation statuses.
  - Frontier invariant: if cancellation happens before a queued node starts, queued nodes become frontier; if cancellation happens after a node completes, eligible downstream nodes become frontier; if active node aborts, that node is included in frontier.
  - Attempt status invariant: expected operational stops become `stopped`, not `failed`; actual node execution failures still fail the attempt and produce failed-frontier checkpoint data.
  - Max runtime reason invariant: lifecycle activation abort reason and scheduler activation reason preserve the specific timeout string, e.g. `workflow max runtime elapsed after 1ms`.
  - Frozen resource invariant: headless shell and JS script nodes run against frozen script code/resources captured from the artifact; missing frozen script files remain runner errors.

- dependencies_and_callers:
  - CLI entry callers use `runWorkflowCommand()` from `workflow-cli.ts`; tests call it directly and inject a fake signal target.
  - `workflow-cli.ts` depends on:
    - `artifact-registry.ts` for `resolveWorkflowFlowSpec()`, named artifact lookup, and registry errors.
    - `package-loader.ts` for `.omhflow` artifact parsing and package errors.
    - `freeze.ts` for `freezeWorkflowArtifact()` and resource snapshots.
    - `session-runtime.ts` for `createSessionWorkflowRuntimeHost()`.
    - `runner.ts` for actual workflow execution.
    - `runtime-binding.ts` and `lifecycle.ts` for runtime binding unavailability and family reconstruction.
    - `runtime-timeout.ts` for default/max runtime behavior.
  - `runner.ts` depends on:
    - `scheduler.ts` for activation ordering, stop scheduling, frontier, and aborted statuses.
    - `node-runtime.ts` for dispatching agent/script/human/review nodes.
    - `run-store.ts` for run event append/reconstruction.
    - `lifecycle.ts` for family, attempt, activation, stop, checkpoint, complete, and fail events.
    - `prompt-source.ts` and package root/frozen resources for prompt resolution.
    - `state.ts` for activation output and state patch validation.
    - `liveness.ts` for script-only cycle guard before node execution.
  - Session runtime bridges:
    - Shell scripts receive cwd and signal in CLI via `runHeadlessShellScript()`.
    - Agent tasks spawn the current CLI invocation with `launch --cwd <cwd> -p <assignment>`.
    - JS eval scripts execute in-process through `AsyncFunction`.
  - Test dependencies:
    - `TempDir` fixtures create throwaway `.omhflow` packages.
    - `FakeWorkflowStartSignalTarget` simulates process signals without mutating real process signal handling.
    - Runner unit tests use an in-memory `WorkflowRunStoreHost` and synthetic workflow definitions/freeze snapshots.

- edge_cases_or_failure_modes:
  - If the source export is read-only and lacks a `.git` directory, commit-range diff inspection cannot be reproduced locally; current source plus scheduler diff summary must be used for this addendum.
  - JS eval cwd is process-global. The implementation restores cwd and console in `finally`, but concurrent in-process eval execution would share those globals. This is acceptable for current headless sequential workflow tests but remains a concurrency-sensitive area.
  - JS eval requests do not receive an AbortSignal directly from `session-runtime.ts`; deadline/interrupt checkpointing relies on the runner wrapper observing abort. Synchronous infinite JS code can still block the event loop and delay/prevent checkpointing until it yields.
  - Shell scripts and agent tasks receive AbortSignal through spawned process APIs; if a subprocess ignores termination or leaves descendants, the workflow runner may checkpoint while external work still needs process-level cleanup guarantees from the underlying executor/runtime.
  - `awaitWorkflowNodeExecution()` rejects after abort on a zero-delay timer. If an operation resolves before that timer settles, completion can win; this preserves normal fast completion but means abort/completion races are order-sensitive.
  - Checkpoint creation requires lifecycle reconstruction to show no running activations. Missing aborted/completed lifecycle activation events would make checkpoint creation fail; the new tests specifically guard this for abort paths.
  - When cancellation happens with no frontier nodes, `workflowCheckpointReason()` returns undefined unless an activation limit was reached; a fully complete graph with a late abort should still complete rather than produce an empty checkpoint.
  - `createWorkflowStartSignalController()` uses `.once()`/`.off()` on the target; injected targets must implement those methods with process-compatible semantics.
  - Headless start now rejects raw workflow packages, so callers that previously used `workflow start ./workflow-dir` must freeze/install or pass a `.omhflow` artifact.
  - The max runtime default is long (`5 * 24 * 60 * 60 * 1000` ms), so deadline behavior is mostly relevant for explicit `--max-runtime-ms` or long-running CI/headless uses.

- validation_or_tests:
  - `packages/coding-agent/src/cli/__tests__/workflow-cli.test.ts`
    - `rejects headless starts from non-artifact workflow packages`: validates raw directory start is rejected with a user-facing artifact requirement and no stack trace.
    - `passes frozen data resources to headless shell script nodes`: validates frozen resource directory is materialized and exposed to shell scripts through workflow env.
    - `runs headless js workflow scripts from the requested cwd`: validates a JS script using `Bun.file("marker.txt")` reads from `--cwd`, not the artifact resource directory or process startup cwd.
    - `checkpoints headless workflow starts on SIGINT instead of leaving a run alive`: validates SIGINT produces JSON run status `stopped`, frontier `["hold"]`, lifecycle attempt `stopped`, checkpoint frontier `["hold"]`, and SIGINT/SIGTERM listener cleanup.
    - Existing nearby tests also validate workflow registry/package errors print without implementation stack traces.
  - `packages/coding-agent/test/workflow/runner.test.ts`
    - `checkpoints frozen attempts that stop at the activation limit`: validates activation limit creates stopped attempt and checkpoint with completed activation/state/frontier.
    - `checkpoints frozen attempts when cancellation stops downstream scheduling`: validates scheduler signal after completed node stops before downstream review and checkpoints `review`.
    - `passes a dedicated node abort signal separately from the scheduler stop signal`: validates node runtime receives the dedicated node abort signal while scheduler stop signal controls downstream scheduling.
    - `checkpoints deadline-aborted lifecycle activations instead of failing the attempt`: validates an active node that throws after node abort is persisted as aborted and the attempt is stopped/checkpointed.
    - `checkpoints deadline-aborted lifecycle activations even when the runtime ignores abort`: validates runner wrapper can checkpoint even when the runtime promise never resolves.
    - `checkpoints lifecycle attempts when max runtime elapses`: validates max runtime abort reason, aborted activation status, stopped attempt, and checkpoint frontier/state.
  - Ancillary example script change:
    - `packages/coding-agent/examples/workflow-demos/human-interactive-dev/.../scripts/implementation.sh` now writes an `artifacts/implementation.txt` scaffold and returns a structured state patch; this is example/demo support rather than a core algorithm change.
  - Verification note:
    - I did not run the test suite because this task requested read-only research notes, and the environment is a read-only source export. Git diff commands also failed because the export is not a Git checkout; evidence was gathered by reading the current source and tests.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `OH_MY_HUMANIZE_MAIN-HZ-001`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`