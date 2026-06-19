You are incremental worker agent_delta_02 for the unified oh-my-humanize/main learn research.

Repository root: /Users/wangweiyang/GitHub/oh_my_humanize_branch_worktrees/main
Work only inside this read-only export: /Users/wangweiyang/GitHub/oh_my_humanize_branch_worktrees/main
Do not edit source files. Produce research notes only.

This is a targeted refresh because oh-my-humanize/main advanced from 6b3819fad50a89fffae899b240ad1ce065c51d23 to bf4509d4f5a669375b3c88510ba0449e9770884c.
Model requested by scheduler: gpt-5.5
Reasoning effort requested by scheduler: xhigh
Protocol: learn_mode=understand, algorithm-subset 1:1 item refresh.

Assigned item:
- item_id: OH_MY_HUMANIZE_MAIN-HZ-2432
- path: packages/coding-agent/src/workflow/runner.ts
- original assigned agent: agent_02
- old bytes/sha16: 23403 / 4450d5d8f1b9327f
- inclusion reason: oh-my-humanize package/crate/runtime source defining core behavior

Diff from old researched commit to latest head:
```diff
diff --git a/packages/coding-agent/src/workflow/runner.ts b/packages/coding-agent/src/workflow/runner.ts
index 7d2f671a5..86d6a1fd3 100644
--- a/packages/coding-agent/src/workflow/runner.ts
+++ b/packages/coding-agent/src/workflow/runner.ts
@@ -274,255 +274,289 @@ function finishLifecycleAttempt(
 function requestWorkflowAttemptStopIfRunning(options: WorkflowRunnerOptions, reason: string): void {
 	const lifecycle = options.lifecycle;
 	if (!lifecycle) return;
 	const family = reconstructWorkflowFamilies(options.host.getBranch()).find(
 		candidate => candidate.id === lifecycle.familyId,
 	);
 	const attempt = family?.attempts.find(candidate => candidate.id === lifecycle.attemptId);
 	if (attempt?.status !== "running") return;
 	requestWorkflowAttemptStop(options.host, {
 		attemptId: lifecycle.attemptId,
 		deadlineMs: lifecycle.stopDeadlineMs ?? 0,
 		reason,
 	});
 }
 
 function workflowCheckpointReason(
 	scheduler: WorkflowSchedulerResult,
 	signal: AbortSignal | undefined,
 ): string | undefined {
 	if (scheduler.limitReached) return "activation limit reached";
 	if (scheduler.frontierNodeIds.length === 0 || !signal?.aborted) return undefined;
 	const reason: unknown = signal.reason;
 	if (reason instanceof Error) return reason.message;
 	if (typeof reason === "string" && reason.length > 0) return reason;
 	if (reason !== undefined && reason !== null) return String(reason);
 	return "workflow stopped";
 }
 
 function failedWorkflowFrontierNodeIds(scheduler: WorkflowSchedulerResult): string[] {
 	const seen = new Set<string>();
 	const nodeIds: string[] = [];
 	for (const activation of scheduler.activations) {
 		if (activation.status !== "failed" || seen.has(activation.nodeId)) continue;
 		seen.add(activation.nodeId);
 		nodeIds.push(activation.nodeId);
 	}
 	return nodeIds;
 }
 
 function lifecycleCheckpointSourceMapping(
 	options: WorkflowRunnerOptions,
 	frontierNodeIds: string[],
 ): Record<string, string> {
 	const lifecycle = options.lifecycle;
 	if (!lifecycle) return identitySourceMapping(frontierNodeIds);
 	const family = reconstructWorkflowFamilies(options.host.getBranch()).find(
 		candidate => candidate.id === lifecycle.familyId,
 	);
 	const approvedMappings =
 		family?.changeRequests
 			.filter(
 				request =>
 					request.status === "approved" &&
 					(request.attemptId === undefined || request.attemptId === lifecycle.attemptId),
 			)
 			.map(request => request.frontierMapping) ?? [];
 	return Object.fromEntries(
 		frontierNodeIds.map(nodeId => [
 			nodeId,
 			approvedMappings.find(mapping => mapping[nodeId] !== undefined)?.[nodeId] ?? nodeId,
 		]),
 	);
 }
 
 function identitySourceMapping(frontierNodeIds: string[]): Record<string, string> {
 	return Object.fromEntries(frontierNodeIds.map(nodeId => [nodeId, nodeId]));
 }
 
 async function executeAndPersistActivation(
 	options: WorkflowRunnerOptions,
 	run: WorkflowRunSnapshot,
 	activation: WorkflowActivation,
 	node: WorkflowNode,
 	context: WorkflowSchedulerExecutionContext,
 	resourceDir: string | undefined,
 ): Promise<WorkflowActivationOutput> {
 	let started = false;
 	try {
 		const livenessDiagnostic = diagnoseWorkflowLiveness(options.definition, node, context.completedActivations);
 		if (livenessDiagnostic !== undefined) {
 			throw new WorkflowRunnerError(livenessDiagnostic.message);
 		}
 		const resolvedPrompt = await resolvePromptForActivation(options, activation, node, context);
 		const input = inputSnapshotFromPrompt(resolvedPrompt);
 		appendWorkflowActivationStarted(options.host, run.id, {
 			activationId: activation.id,
 			nodeId: node.id,
 			graphRevisionId: activation.graphRevisionId,
 			parentActivationIds: activation.parentActivationIds,
 			input,
 		});
 		appendLifecycleActivationStarted(options, activation, node);
 		started = true;
 		const promptedNode = resolvedPrompt ? { ...node, prompt: resolvedPrompt.value } : node;
 		const nodeForExecution = await resolveScriptForExecution(options, promptedNode);
 		const modelAudit = nodeRequiresModel(node) ? resolveModelAudit(options, node) : undefined;
 		if (modelAudit?.error && nodeRequiresModel(node)) {
 			throw new WorkflowRunnerError(modelAudit.error);
 		}
 		const executionSignal = context.nodeAbortSignal ?? context.signal;
-		const rawOutput = await executeWorkflowNode(nodeForExecution, activation, options.runtimeHost, {
-			modelOverride: modelOverrideFromAudit(modelAudit),
-			signal: executionSignal,
-			context: {
-				state: context.state,
-				completedActivations: context.completedActivations,
-			},
-			resourceDir,
-		});
+		const rawOutput = await awaitWorkflowNodeExecution(
+			executeWorkflowNode(nodeForExecution, activation, options.runtimeHost, {
+				modelOverride: modelOverrideFromAudit(modelAudit),
+				signal: executionSignal,
+				context: {
+					state: context.state,
+					completedActivations: context.completedActivations,
+				},
+				resourceDir,
+			}),
+			executionSignal,
+		);
 		const output = validateWorkflowActivationOutput(materializeSingleWriteData(node, rawOutput), {
 			allowedWritePaths: node.writes,
 			stateSchema: options.definition.stateSchema,
 		});
 		if (output.statePatch) {
 			appendWorkflowStatePatch(options.host, run.id, {
 				patch: output.statePatch,
 				reason: `activation ${activation.id}`,
 			});
 		}
 		appendWorkflowActivationCompleted(options.host, run.id, {
 			activationId: activation.id,
 			output,
 			modelAudit,
 		});
 		appendLifecycleActivationCompleted(options, activation, output);
 		return output;
 	} catch (error) {
 		if (!started) {
 			appendWorkflowActivationStarted(options.host, run.id, {
 				activationId: activation.id,
 				nodeId: node.id,
 				graphRevisionId: activation.graphRevisionId,
 				parentActivationIds: activation.parentActivationIds,
 			});
 			appendLifecycleActivationStarted(options, activation, node);
 		}
 		const message = error instanceof Error ? error.message : String(error);
 		const abortReason = workflowNodeAbortReason(context.nodeAbortSignal ?? context.signal);
 		if (abortReason !== undefined) {
 			appendWorkflowActivationAborted(options.host, run.id, {
 				activationId: activation.id,
 				reason: abortReason,
 			});
 			appendLifecycleActivationAborted(options, activation, node, abortReason);
 			throw error;
 		}
 		appendWorkflowActivationFailed(options.host, run.id, {
 			activationId: activation.id,
 			error: message,
 		});
 		appendLifecycleActivationFailed(options, activation, message);
 		throw error;
 	}
 }
 
+function awaitWorkflowNodeExecution<T>(operation: Promise<T>, signal: AbortSignal | undefined): Promise<T> {
+	if (signal === undefined) return operation;
+	const { promise, resolve, reject } = Promise.withResolvers<T>();
+	let settled = false;
+	let abortTimer: NodeJS.Timeout | undefined;
+	const settle = (fn: () => void): void => {
+		if (settled) return;
+		settled = true;
+		if (abortTimer !== undefined) {
+			clearTimeout(abortTimer);
+			abortTimer = undefined;
+		}
+		signal.removeEventListener("abort", onAbort);
+		fn();
+	};
+	const onAbort = (): void => {
+		if (abortTimer !== undefined) return;
+		abortTimer = setTimeout(() => {
+			const reason = workflowNodeAbortReason(signal) ?? "workflow activation aborted";
+			settle(() => reject(new Error(reason)));
+		}, 0);
+	};
+	signal.addEventListener("abort", onAbort, { once: true });
+	operation.then(
+		output => settle(() => resolve(output)),
+		error => settle(() => reject(error)),
+	);
+	if (signal.aborted) onAbort();
+	return promise;
+}
+
 function materializeSingleWriteData(node: WorkflowNode, output: WorkflowActivationOutput): WorkflowActivationOutput {
 	if (output.statePatch !== undefined) return output;
 	const writePath = node.writes?.length === 1 ? node.writes[0] : undefined;
 	if (writePath === undefined || !hasStructuredWorkflowData(output.data)) return output;
 	return {
 		...output,
 		statePatch: [{ op: "set", path: writePath, value: output.data }],
 	};
 }
 
 function hasStructuredWorkflowData(data: Record<string, unknown> | undefined): data is Record<string, unknown> {
 	if (data === undefined) return false;
 	return Object.keys(data).some(key => key !== "exitCode" && key !== "summaryTruncated" && key !== "summaryBytes");
 }
 
 function appendLifecycleActivationStarted(
 	options: WorkflowRunnerOptions,
 	activation: WorkflowActivation,
 	node: WorkflowNode,
 ): void {
 	const lifecycle = options.lifecycle;
 	if (!lifecycle) return;
 	appendWorkflowAttemptActivationStarted(options.host, {
 		attemptId: lifecycle.attemptId,
 		activationId: activation.id,
 		nodeId: node.id,
 		parentActivationIds: activation.parentActivationIds,
 	});
 }
 
 function appendLifecycleActivationCompleted(
 	options: WorkflowRunnerOptions,
 	activation: WorkflowActivation,
 	output: WorkflowActivationOutput,
 ): void {
 	const lifecycle = options.lifecycle;
 	if (!lifecycle) return;
 	appendWorkflowAttemptActivationCompleted(options.host, {
 		attemptId: lifecycle.attemptId,
 		activationId: activation.id,
 		output,
 	});
 }
 
 function appendLifecycleActivationAborted(
 	options: WorkflowRunnerOptions,
 	activation: WorkflowActivation,
 	node: WorkflowNode,
 	reason: string | undefined,
 ): void {
 	const lifecycle = options.lifecycle;
 	if (!lifecycle) return;
 	appendWorkflowAttemptActivationAborted(options.host, {
 		attemptId: lifecycle.attemptId,
 		activationId: activation.id,
 		nodeId: node.id,
 		reason: reason ?? "workflow activation aborted",
 	});
 }
 
 function appendLifecycleActivationFailed(
 	options: WorkflowRunnerOptions,
 	activation: WorkflowActivation,
 	error: string,
 ): void {
 	const lifecycle = options.lifecycle;
 	if (!lifecycle) return;
 	appendWorkflowAttemptActivationFailed(options.host, {
 		attemptId: lifecycle.attemptId,
 		activationId: activation.id,
 		error,
 	});
 }
 
 function modelOverrideFromAudit(modelAudit: WorkflowModelResolutionAudit | undefined): string | undefined {
 	if (!modelAudit?.resolvedModel) return undefined;
 	if (modelAudit.explicitThinkingLevel && modelAudit.thinkingLevel) {
 		return `${modelAudit.resolvedModel}:${modelAudit.thinkingLevel}`;
 	}
 	return modelAudit.resolvedModel;
 }
 
 function workflowNodeAbortReason(signal: AbortSignal | undefined): string | undefined {
 	if (!signal?.aborted) return undefined;
 	const reason: unknown = signal.reason;
 	if (reason instanceof Error) return reason.message;
 	if (typeof reason === "string" && reason.length > 0) return reason;
 	if (reason !== undefined && reason !== null) return String(reason);
 	return "workflow activation aborted";
 }
 
 async function resolvePromptForActivation(
 	options: WorkflowRunnerOptions,
 	activation: WorkflowActivation,
 	node: WorkflowNode,
 	context: WorkflowSchedulerExecutionContext,
 ): Promise<WorkflowResolvedPrompt | undefined> {
 	if (!nodeConsumesPrompt(node)) return undefined;
 	return resolveWorkflowPrompt(node, {
 		state: context.state,

```

Research requirements:
1. Inspect the current file at `packages/coding-agent/src/workflow/runner.ts` directly in the read-only export.
2. Focus on the algorithmic delta introduced by commits after 6b3819fad50a89fffae899b240ad1ce065c51d23: cwd handling for headless JS workflow scripts, node abort/deadline behavior, and related tests where applicable.
3. Preserve the exact item_id `OH_MY_HUMANIZE_MAIN-HZ-2432` in the heading and evidence. This addendum will be appended to the existing worker output for that item.
4. Include concrete current behavior, inputs/outputs/state, gates/invariants, dependencies/callers, edge cases, and validation/tests.
5. Mark worker cursor as `[_]` only; master will promote to `[x]` after verify.

Required format:
# agent_delta_02 oh-my-humanize main incremental research

## Worker Summary
- status: `[_]`
- source_commit_old: `6b3819fad50a89fffae899b240ad1ce065c51d23`
- source_commit_new: `bf4509d4f5a669375b3c88510ba0449e9770884c`
- assigned_item_count: 1

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-2432 `file` `packages/coding-agent/src/workflow/runner.ts`
- cursor: `[_]`
- current_core_role:
- algorithmic_delta_since_old_commit:
- current_inputs_outputs_state:
- new_or_changed_gates_or_invariants:
- dependencies_and_callers:
- edge_cases_or_failure_modes:
- validation_or_tests:
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `OH_MY_HUMANIZE_MAIN-HZ-2432`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`
