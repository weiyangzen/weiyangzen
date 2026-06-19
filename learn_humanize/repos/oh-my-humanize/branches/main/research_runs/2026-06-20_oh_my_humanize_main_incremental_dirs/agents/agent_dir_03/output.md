# agent_dir_03 oh-my-humanize main directory incremental research

## Worker Summary
- status: `[_]`
- source_commit_old: `6b3819fad50a89fffae899b240ad1ce065c51d23`
- source_commit_new: `bf4509d4f5a669375b3c88510ba0449e9770884c`
- assigned_item_count: 1

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-028 `directory` `packages/coding-agent`
- cursor: `[_]`
- current_directory_core_role:
  `packages/coding-agent` is the primary CLI/runtime package for the coding-agent product. For workflow execution specifically, it owns CLI command dispatch (`src/commands/workflow.ts`, `src/cli/workflow-cli.ts`), workflow artifact loading/freezing, runtime host adaptation for agent/script/human/review nodes, scheduler execution, lifecycle attempt/checkpoint records, run-store reconstruction, and package-local workflow tests. The workflow subsystem now treats headless `omp workflow start` as a frozen-artifact executor that can run file-backed JS/sh nodes, materialize frozen resources, emit run/family/checkpoint JSON, and stop/checkpoint predictably on limits or process signals.

- directory_level_delta_since_old_commit:
  The new commit tightens headless workflow start semantics in three visible ways. First, JavaScript workflow scripts launched through `omp workflow start --cwd <dir>` now execute with `process.cwd()` temporarily set to the requested workflow cwd, then restore the previous cwd and `console.log` hook in `finally`; this makes relative file access inside JS workflow scripts resolve against the user-requested run workspace rather than the CLI process launch directory. Second, headless starts now install a SIGINT/SIGTERM-backed abort controller and pass that signal as both the scheduler stop signal and node execution abort signal into `runWorkflow`, so an interrupted headless run can become a stopped lifecycle attempt with a checkpoint instead of remaining effectively alive. Third, `runWorkflow` now combines caller abort signals with `maxRuntimeMs` timeout signals, wraps node execution so ignored aborts are converted into prompt rejection, and uses abort/limit state to request stop plus create lifecycle checkpoints.

- affected_descendant_algorithms:
  `src/cli/workflow-cli.ts` now resolves `cwd`, constructs a session workflow runtime host with that cwd, requires headless starts to load frozen `.omhflow` artifacts, creates/disposes process signal listeners, passes `signal`, `nodeAbortSignal`, and `maxRuntimeMs` into `runWorkflow`, and reports checkpoint frontier data in JSON output. Its JS eval adapter changes cwd before `AsyncFunction` execution, captures console output and returned values, and restores globals afterward. Shell and agent headless adapters continue to pass the cwd into `Bun.spawn`, with shell scripts also receiving workflow script environment including resource-directory variables.

  `src/workflow/runner.ts` now owns more cancellation policy. `workflowRuntimeSignal()` creates a max-runtime timeout abort signal and combines it with the scheduler signal, node abort signal, and per-activation node abort signal. `executeAndPersistActivation()` forwards the selected execution signal to `executeWorkflowNode()` and races node execution through `awaitWorkflowNodeExecution()`, which rejects on abort even if the node runtime never settles. `finishLifecycleAttempt()` now derives a checkpoint reason from activation limits or an aborted scheduler signal, requests an attempt stop if the lifecycle attempt is still running, and creates checkpoints with completed/aborted activation ids, frontier nodes, state, and source mapping.

  `src/workflow/scheduler.ts` remains the lower-level execution engine that distinguishes the scheduler stop signal from node abort signals. It stops queue scheduling when the scheduler signal aborts, records stopped frontier nodes, marks node-aborted activations as `aborted`, and includes the current node in the restart frontier when an in-flight activation aborts. `src/workflow/lifecycle.ts` enforces that checkpoints are only created for stopped/stop-requested/failed attempts and refuses checkpoint creation while lifecycle activations are still running.

- current_inputs_outputs_state:
  Inputs include `omp workflow start <flow-or-path>` flags (`--cwd`, `--json`, `--run-id`, `--family-id`, `--start`, activation limits, node activation limits, and `--max-runtime-ms`), frozen `.omhflow` artifacts plus same-name resource directories, file-backed script nodes, workflow state/schema, process SIGINT/SIGTERM events, and runner-level `signal` / `nodeAbortSignal` / `nodeAbortSignalForActivation` / lifecycle options. Headless starts use an in-memory workflow store host, then reconstruct run and family snapshots for stdout JSON/text output.

  Outputs include workflow run activation records, state patches, lifecycle family/freeze/attempt/checkpoint records, structured script output parsed from JSON or top-level JS returns, shell stdout/stderr-derived script results, materialized frozen resource directories supplied to script runtimes, and cleanup of those temp resource directories after execution. For JSON headless starts, output now includes run status, activation counts, frontier node ids, max runtime, family attempts, checkpoints, change requests, and run state keys.

- new_or_changed_gates_or_invariants:
  Headless `workflow start` requires a frozen `.omhflow` artifact; raw authoring YAML/package starts are rejected with a package error. The run cwd is resolved once and used for flow lookup, session runtime host construction, JS eval cwd, shell cwd, and agent subprocess cwd. JS eval must restore both `console.log` and the previous process cwd even on script failure. SIGINT/SIGTERM listeners must be removed after start completion or failure. Max runtime is a workflow-level wall-clock gate and is applied to both scheduler progress and node execution. Lifecycle checkpointing now treats activation limits, scheduler aborts, and max-runtime aborts as stopped/checkpointed conditions rather than ordinary failures. Node runtimes that ignore abort cannot block stop/checkpoint indefinitely because the runner rejects the awaited node execution on abort. Aborted activations are checkpoint inputs, not failed-attempt evidence, when the stop/deadline path is active.

- dependencies_and_callers:
  `src/commands/workflow.ts` is the direct CLI command caller for `runWorkflowCommand()`. Interactive and background workflow slash-command flows in `src/slash-commands/helpers/workflow.ts` also call `runWorkflow()` and share the max-runtime/node-abort semantics, including per-activation node abort controllers. `workflow-cli.ts` depends on artifact registry/package loader/freeze/lifecycle/run-store/runtime-binding/session-runtime/script-runtime-env/runtime-timeout modules. `runner.ts` depends on scheduler, lifecycle, run-store, node-runtime, prompt-source, model-resolution, liveness diagnosis, frozen resource materialization, and runtime timeout reason formatting. Script execution output is normalized by `session-runtime.ts`, where top-level-return JS scripts are wrapped to log a JSON result, and structured output is parsed back into workflow activation output.

- edge_cases_or_failure_modes:
  JS headless eval mutates process-wide cwd and `console.log` while a script runs; the implementation restores both in `finally`, but concurrent JS evals in the same process would still be sensitive to that global mutation. A missing or unreadable `--cwd` will surface through the JS eval adapter as script failure when `process.chdir(cwd)` fails. Python eval scripts remain unsupported in the headless CLI. For lifecycle checkpointing, callers must abort the scheduler stop signal when they intend a stopped attempt; node abort signals are the execution/deadline cutoff, while the scheduler signal is what lets `finishLifecycleAttempt()` derive a checkpoint reason unless the activation limit is reached. If a workflow has no lifecycle options, the run can still return aborted/stopped scheduler state, but no family checkpoint is recorded. Frozen resource paths and package script paths remain guarded against escaping their roots.

- validation_or_tests:
  `src/cli/__tests__/workflow-cli.test.ts` now pins headless JS cwd behavior with a file-backed JS script that reads `marker.txt` from the requested `--cwd` and emits a `/marker` state patch. The same test file pins SIGINT behavior with a fake signal target: a sleeping shell node is interrupted, JSON output reports `run.status === "stopped"`, frontier `["hold"]`, family attempt status `stopped`, checkpoint frontier `["hold"]`, and signal listener cleanup for both SIGINT and SIGTERM. It also covers frozen-resource shell access and rejection of non-artifact starts.

  `test/workflow/runner.test.ts` pins runner-level stop/deadline contracts: cancellation after a completed activation checkpoints downstream frontier, dedicated node abort signals are passed separately from scheduler stop signals, deadline-aborted activations become `aborted` and produce stopped attempts plus checkpoints, runtimes that ignore abort are force-unblocked by the runner, and `maxRuntimeMs` produces the reason `workflow max runtime elapsed after <n>ms` with an aborted activation checkpoint. `packages/coding-agent/CHANGELOG.md` records the two user-visible fixes: JS headless `--cwd` handling with structured top-level-return output, and stop/checkpoint handling when node runtimes ignore abort.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `OH_MY_HUMANIZE_MAIN-HZ-028`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`