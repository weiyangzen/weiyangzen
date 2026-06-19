You are incremental worker agent_delta_03 for the unified oh-my-humanize/main learn research.

Repository root: /Users/wangweiyang/GitHub/oh_my_humanize_branch_worktrees/main
Work only inside this read-only export: /Users/wangweiyang/GitHub/oh_my_humanize_branch_worktrees/main
Do not edit source files. Produce research notes only.

This is a targeted refresh because oh-my-humanize/main advanced from 6b3819fad50a89fffae899b240ad1ce065c51d23 to bf4509d4f5a669375b3c88510ba0449e9770884c.
Model requested by scheduler: gpt-5.5
Reasoning effort requested by scheduler: xhigh
Protocol: learn_mode=understand, algorithm-subset 1:1 item refresh.

Assigned item:
- item_id: OH_MY_HUMANIZE_MAIN-HZ-2763
- path: packages/coding-agent/test/workflow/runner.test.ts
- original assigned agent: agent_03
- old bytes/sha16: 25570 / 6385cd7e373daad6
- inclusion reason: oh-my-humanize package/crate/runtime source defining core behavior

Diff from old researched commit to latest head:
```diff
diff --git a/packages/coding-agent/test/workflow/runner.test.ts b/packages/coding-agent/test/workflow/runner.test.ts
index 39bffb58c..c8002deb2 100644
--- a/packages/coding-agent/test/workflow/runner.test.ts
+++ b/packages/coding-agent/test/workflow/runner.test.ts
@@ -464,200 +464,262 @@ edges:
 	it("passes a dedicated node abort signal separately from the scheduler stop signal", async () => {
 		const host = createHost();
 		const definition = parseWorkflowDefinition(source, { sourcePath: "workflow.yml" });
 		const stopController = new AbortController();
 		const nodeAbortController = new AbortController();
 		const calls: string[] = [];
 		let receivedSignal: AbortSignal | undefined;
 		const runtimeHost: WorkflowNodeRuntimeHost = {
 			runAgentNode: async input => {
 				calls.push("build");
 				receivedSignal = input.signal;
 				stopController.abort("workflow stop requested");
 				return { summary: "build completed" };
 			},
 			runReviewNode: async () => {
 				calls.push("review");
 				return { summary: "review should not run", verdict: "finish" };
 			},
 		};
 
 		await runWorkflow({
 			host,
 			definition,
 			runId: "run-node-abort-signal",
 			startNodeId: "build",
 			runtimeHost,
 			signal: stopController.signal,
 			nodeAbortSignal: nodeAbortController.signal,
 			lifecycle: {
 				familyId: "family-node-abort-signal",
 				attemptId: "attempt-node-abort-signal-1",
 				freeze: createFreeze("flowfreeze:node-abort-signal", definition),
 				runtimeBindingSnapshot: binding("binding-node-abort-signal"),
 			},
 		});
 
 		expect(calls).toEqual(["build"]);
 		expect(receivedSignal).toBe(nodeAbortController.signal);
 		const families = reconstructWorkflowFamilies(host.getBranch());
 		expect(families[0]?.attempts[0]?.status).toBe("stopped");
 		expect(families[0]?.checkpoints[0]?.frontierNodeIds).toEqual(["review"]);
 	});
 
 	it("checkpoints deadline-aborted lifecycle activations instead of failing the attempt", async () => {
 		const host = createHost();
 		const definition = parseWorkflowDefinition(source, { sourcePath: "workflow.yml" });
 		const stopController = new AbortController();
 		const nodeAbortController = new AbortController();
 		const runtimeHost: WorkflowNodeRuntimeHost = {
 			runAgentNode: async input => {
 				stopController.abort("workflow stop requested");
 				await Promise.resolve();
 				nodeAbortController.abort("stop deadline elapsed");
 				throw new Error(input.signal?.reason ?? "stop deadline elapsed");
 			},
 			runReviewNode: async () => ({ summary: "review should not run", verdict: "finish" }),
 		};
 
 		const result = await runWorkflow({
 			host,
 			definition,
 			runId: "run-node-abort",
 			startNodeId: "build",
 			runtimeHost,
 			signal: stopController.signal,
 			nodeAbortSignal: nodeAbortController.signal,
 			lifecycle: {
 				familyId: "family-node-abort",
 				attemptId: "attempt-node-abort-1",
 				freeze: createFreeze("flowfreeze:node-abort", definition),
 				runtimeBindingSnapshot: binding("binding-node-abort"),
 			},
 		});
 
 		expect(result.scheduler.activations.map(activation => [activation.nodeId, activation.status])).toEqual([
 			["build", "aborted"],
 		]);
 		expect(reconstructWorkflowRuns(host.getBranch())[0]?.activations.map(activation => activation.status)).toEqual([
 			"aborted",
 		]);
 		const families = reconstructWorkflowFamilies(host.getBranch());
 		expect(families[0]?.attempts.map(attempt => [attempt.id, attempt.status, attempt.error])).toEqual([
 			["attempt-node-abort-1", "stopped", undefined],
 		]);
 		expect(families[0]?.attempts[0]?.activations.map(activation => [activation.nodeId, activation.status])).toEqual([
 			["build", "aborted"],
 		]);
 		expect(families[0]?.checkpoints).toMatchObject([
 			{
 				id: "attempt-node-abort-1:checkpoint-1",
 				attemptId: "attempt-node-abort-1",
 				completedActivationIds: [],
 				abortedActivationIds: ["activation-1"],
 				frontierNodeIds: ["build"],
 				state: {},
 				sourceMapping: { build: "build" },
 			},
 		]);
 	});
 
+	it("checkpoints deadline-aborted lifecycle activations even when the runtime ignores abort", async () => {
+		const host = createHost();
+		const definition = parseWorkflowDefinition(source, { sourcePath: "workflow.yml" });
+		const stopController = new AbortController();
+		const nodeAbortController = new AbortController();
+		const started = Promise.withResolvers<void>();
+		const never = Promise.withResolvers<never>();
+		const runtimeHost: WorkflowNodeRuntimeHost = {
+			runAgentNode: async () => {
+				started.resolve();
+				return await never.promise;
+			},
+			runReviewNode: async () => ({ summary: "review should not run", verdict: "finish" }),
+		};
+
+		const resultPromise = runWorkflow({
+			host,
+			definition,
+			runId: "run-node-abort-ignored",
+			startNodeId: "build",
+			runtimeHost,
+			signal: stopController.signal,
+			nodeAbortSignal: nodeAbortController.signal,
+			lifecycle: {
+				familyId: "family-node-abort-ignored",
+				attemptId: "attempt-node-abort-ignored-1",
+				freeze: createFreeze("flowfreeze:node-abort-ignored", definition),
+				runtimeBindingSnapshot: binding("binding-node-abort-ignored"),
+			},
+		});
+		await started.promise;
+
+		stopController.abort("workflow stop requested");
+		nodeAbortController.abort("stop deadline elapsed");
+		const result = await Promise.race([resultPromise, Bun.sleep(100).then(() => "timeout" as const)]);
+		if (result === "timeout") {
+			throw new Error("workflow stop did not checkpoint when the node runtime ignored abort");
+		}
+
+		expect(result.scheduler.activations.map(activation => [activation.nodeId, activation.status])).toEqual([
+			["build", "aborted"],
+		]);
+		const families = reconstructWorkflowFamilies(host.getBranch());
+		expect(families[0]?.attempts.map(attempt => [attempt.id, attempt.status, attempt.error])).toEqual([
+			["attempt-node-abort-ignored-1", "stopped", undefined],
+		]);
+		expect(families[0]?.attempts[0]?.activations.map(activation => [activation.nodeId, activation.status])).toEqual([
+			["build", "aborted"],
+		]);
+		expect(families[0]?.checkpoints).toMatchObject([
+			{
+				id: "attempt-node-abort-ignored-1:checkpoint-1",
+				attemptId: "attempt-node-abort-ignored-1",
+				completedActivationIds: [],
+				abortedActivationIds: ["activation-1"],
+				frontierNodeIds: ["build"],
+				state: {},
+				sourceMapping: { build: "build" },
+			},
+		]);
+	});
+
 	it("checkpoints lifecycle attempts when max runtime elapses", async () => {
 		const host = createHost();
 		const definition = parseWorkflowDefinition(source, { sourcePath: "workflow.yml" });
 		const runtimeElapsed = Promise.withResolvers<void>();
 		const runtimeHost: WorkflowNodeRuntimeHost = {
 			runAgentNode: async input => {
 				input.signal?.addEventListener("abort", () => runtimeElapsed.resolve(), { once: true });
 				await runtimeElapsed.promise;
 				throw new Error(input.signal?.reason ?? "workflow max runtime elapsed");
 			},
 			runReviewNode: async () => ({ summary: "review should not run", verdict: "finish" }),
 		};
 
 		const result = await runWorkflow({
 			host,
 			definition,
 			runId: "run-max-runtime",
 			startNodeId: "build",
 			runtimeHost,
 			maxRuntimeMs: 1,
 			lifecycle: {
 				familyId: "family-max-runtime",
 				attemptId: "attempt-max-runtime-1",
 				freeze: createFreeze("flowfreeze:max-runtime", definition),
 				runtimeBindingSnapshot: binding("binding-max-runtime"),
 			},
 		});
 
 		expect(result.scheduler.activations.map(activation => [activation.nodeId, activation.status])).toEqual([
 			["build", "aborted"],
 		]);
 		const families = reconstructWorkflowFamilies(host.getBranch());
 		expect(families[0]?.attempts.map(attempt => [attempt.id, attempt.status, attempt.error])).toEqual([
 			["attempt-max-runtime-1", "stopped", undefined],
 		]);
 		expect(families[0]?.attempts[0]?.activations[0]).toMatchObject({
 			nodeId: "build",
 			status: "aborted",
 			reason: "workflow max runtime elapsed after 1ms",
 		});
 		expect(families[0]?.checkpoints).toMatchObject([
 			{
 				id: "attempt-max-runtime-1:checkpoint-1",
 				attemptId: "attempt-max-runtime-1",
 				completedActivationIds: [],
 				abortedActivationIds: ["activation-1"],
 				frontierNodeIds: ["build"],
 				state: {},
 				sourceMapping: { build: "build" },
 			},
 		]);
 	});
 
 	it("uses approved change request mappings when checkpointing activation-limited attempts", async () => {
 		const host = createHost();
 		const definition = parseWorkflowDefinition(source, { sourcePath: "workflow.yml" });
 		startWorkflowFamily(host, { familyId: "family-mapped-limit" });
 		proposeWorkflowChangeRequest(host, {
 			changeRequestId: "change-review",
 			familyId: "family-mapped-limit",
 			attemptId: "attempt-mapped-limit-1",
 			actor: "human:operator",
 			origin: "human",
 			reason: "upgrade review node before restart",
 			operations: [],
 			frontierMapping: { review: "strongReview" },
 		});
 		approveWorkflowChangeRequest(host, {
 			changeRequestId: "change-review",
 			actor: "human:sihao",
 		});
 		const runtimeHost: WorkflowNodeRuntimeHost = {
 			runAgentNode: async () => ({ summary: "build completed" }),
 		};
 
 		await runWorkflow({
 			host,
 			definition,
 			runId: "run-mapped-limit",
 			startNodeId: "build",
 			runtimeHost,
 			maxActivations: 1,
 			lifecycle: {
 				familyId: "family-mapped-limit",
 				attemptId: "attempt-mapped-limit-1",
 				freeze: createFreeze("flowfreeze:mapped-limit", definition),
 				runtimeBindingSnapshot: binding("binding-mapped-limit"),
 			},
 		});
 
 		const families = reconstructWorkflowFamilies(host.getBranch());
 		expect(families[0]?.checkpoints[0]?.sourceMapping).toEqual({ review: "strongReview" });
 	});
 
 	it("resolves parent output prompts from checkpointed activations during restart", async () => {
 		const host = createHost();
 		const definition = parseWorkflowDefinition(
 			`
 name: checkpoint-prompt-restart
 version: 1

```

Research requirements:
1. Inspect the current file at `packages/coding-agent/test/workflow/runner.test.ts` directly in the read-only export.
2. Focus on the algorithmic delta introduced by commits after 6b3819fad50a89fffae899b240ad1ce065c51d23: cwd handling for headless JS workflow scripts, node abort/deadline behavior, and related tests where applicable.
3. Preserve the exact item_id `OH_MY_HUMANIZE_MAIN-HZ-2763` in the heading and evidence. This addendum will be appended to the existing worker output for that item.
4. Include concrete current behavior, inputs/outputs/state, gates/invariants, dependencies/callers, edge cases, and validation/tests.
5. Mark worker cursor as `[_]` only; master will promote to `[x]` after verify.

Required format:
# agent_delta_03 oh-my-humanize main incremental research

## Worker Summary
- status: `[_]`
- source_commit_old: `6b3819fad50a89fffae899b240ad1ce065c51d23`
- source_commit_new: `bf4509d4f5a669375b3c88510ba0449e9770884c`
- assigned_item_count: 1

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-2763 `file` `packages/coding-agent/test/workflow/runner.test.ts`
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
- assigned_items_seen: `OH_MY_HUMANIZE_MAIN-HZ-2763`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`
