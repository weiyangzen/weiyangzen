You are incremental worker agent_delta_04 for the unified oh-my-humanize/main learn research.

Repository root: /Users/wangweiyang/GitHub/oh_my_humanize_branch_worktrees/main
Work only inside this read-only export: /Users/wangweiyang/GitHub/oh_my_humanize_branch_worktrees/main
Do not edit source files. Produce research notes only.

This is a targeted refresh because oh-my-humanize/main advanced from 6b3819fad50a89fffae899b240ad1ce065c51d23 to bf4509d4f5a669375b3c88510ba0449e9770884c.
Model requested by scheduler: gpt-5.5
Reasoning effort requested by scheduler: xhigh
Protocol: learn_mode=understand, algorithm-subset 1:1 item refresh.

Assigned item:
- item_id: OH_MY_HUMANIZE_MAIN-HZ-2969
- path: packages/coding-agent/src/cli/__tests__/workflow-cli.test.ts
- original assigned agent: agent_29
- old bytes/sha16: 10777 / 8ea6ba29e9b1af1d
- inclusion reason: oh-my-humanize package/crate/runtime source defining core behavior

Diff from old researched commit to latest head:
```diff
diff --git a/packages/coding-agent/src/cli/__tests__/workflow-cli.test.ts b/packages/coding-agent/src/cli/__tests__/workflow-cli.test.ts
index e8bf9969f..7986b54d9 100644
--- a/packages/coding-agent/src/cli/__tests__/workflow-cli.test.ts
+++ b/packages/coding-agent/src/cli/__tests__/workflow-cli.test.ts
@@ -47,298 +47,378 @@ describe("workflow CLI", () => {
 		expect(stdout.join("")).toBe("");
 		expect(errorOutput).toContain('workflow flow "humanize-rlcr" is ambiguous');
 		expect(errorOutput).toContain("Use an explicit .omhflow path to select one artifact.");
 		expect(errorOutput).not.toContain("artifact-registry.ts");
 		expect(errorOutput).not.toContain("WorkflowArtifactRegistryError");
 	});
 
 	it("prints artifact package errors without a source stack trace", async () => {
 		using tempDir = TempDir.createSync("@omp-workflow-cli-package-error-");
 		const root = tempDir.path();
 		await Bun.write(`${root}/not-a-flow/readme.txt`, "not an omhflow artifact");
 		const originalExitCode = process.exitCode;
 		const stderr: string[] = [];
 		vi.spyOn(process.stderr, "write").mockImplementation(chunk => {
 			stderr.push(typeof chunk === "string" ? chunk : new TextDecoder().decode(chunk));
 			return true;
 		});
 		process.exitCode = undefined;
 		try {
 			await runWorkflowCommand({
 				action: "freeze",
 				args: ["not-a-flow"],
 				flags: { cwd: root },
 			});
 		} finally {
 			process.exitCode = originalExitCode ?? 0;
 		}
 
 		const errorOutput = stderr.join("");
 		expect(errorOutput).toContain(".omhflow artifact path must be a file");
 		expect(errorOutput).not.toContain("package-loader.ts");
 		expect(errorOutput).not.toContain("WorkflowPackageError");
 	});
 
 	it("rejects headless starts from non-artifact workflow packages", async () => {
 		using tempDir = TempDir.createSync("@omp-workflow-cli-start-artifact-");
 		const root = tempDir.path();
 		await Bun.write(
 			`${root}/workflow.yml`,
 			["name: raw-start", "version: 1", "nodes:", "  build:", "    type: script", "edges: []", ""].join("\n"),
 		);
 		const originalExitCode = process.exitCode;
 		const stdout: string[] = [];
 		const stderr: string[] = [];
 		vi.spyOn(process.stdout, "write").mockImplementation(chunk => {
 			stdout.push(typeof chunk === "string" ? chunk : new TextDecoder().decode(chunk));
 			return true;
 		});
 		vi.spyOn(process.stderr, "write").mockImplementation(chunk => {
 			stderr.push(typeof chunk === "string" ? chunk : new TextDecoder().decode(chunk));
 			return true;
 		});
 		process.exitCode = undefined;
 		try {
 			await runWorkflowCommand({
 				action: "start",
 				args: [root],
 				flags: { cwd: root, runId: "raw-start" },
 			});
 		} finally {
 			process.exitCode = originalExitCode ?? 0;
 		}
 
 		expect(stdout.join("")).toBe("");
 		const errorOutput = stderr.join("");
 		expect(errorOutput).toContain("Workflow start requires a frozen .omhflow artifact");
 		expect(errorOutput).not.toContain("workflow-cli.ts");
 		expect(errorOutput).not.toContain("WorkflowPackageError");
 	});
 
 	it("passes frozen data resources to headless shell script nodes", async () => {
 		using tempDir = TempDir.createSync("@omp-workflow-cli-resources-");
 		const root = tempDir.path();
 		await Bun.write(`${root}/resource-smoke.omhflow`, workflowResourceSmokeFlow());
 		await Bun.write(`${root}/resource-smoke/scripts/read-resource.sh`, workflowResourceSmokeScript());
 		await Bun.write(`${root}/resource-smoke/data/message.txt`, "resource-ok");
 		const output: string[] = [];
 		vi.spyOn(process.stdout, "write").mockImplementation(chunk => {
 			output.push(typeof chunk === "string" ? chunk : new TextDecoder().decode(chunk));
 			return true;
 		});
 
 		await runWorkflowCommand({
 			action: "start",
 			args: [`${root}/resource-smoke.omhflow`],
 			flags: {
 				cwd: root,
 				json: true,
 				runId: "resource-smoke-run",
 			},
 		});
 
 		const result = JSON.parse(output.join("").trim()) as {
 			run: { status: string; completed: number; failed: number };
 			runs: { stateKeys: string[] }[];
 		};
 		expect(result.run).toMatchObject({ status: "completed", completed: 1, failed: 0 });
 		expect(result.runs[0]?.stateKeys).toEqual(["message"]);
 	});
 
+	it("runs headless js workflow scripts from the requested cwd", async () => {
+		using tempDir = TempDir.createSync("@omp-workflow-cli-js-cwd-");
+		const root = tempDir.path();
+		const runCwd = `${root}/workspace`;
+		await Bun.write(`${root}/cwd-smoke.omhflow`, workflowJsCwdSmokeFlow());
+		await Bun.write(`${root}/cwd-smoke/scripts/read-cwd.js`, workflowJsCwdSmokeScript());
+		await Bun.write(`${runCwd}/marker.txt`, "cwd-ok");
+		const output: string[] = [];
+		vi.spyOn(process.stdout, "write").mockImplementation(chunk => {
+			output.push(typeof chunk === "string" ? chunk : new TextDecoder().decode(chunk));
+			return true;
+		});
+
+		await runWorkflowCommand({
+			action: "start",
+			args: [`${root}/cwd-smoke.omhflow`],
+			flags: {
+				cwd: runCwd,
+				json: true,
+				runId: "js-cwd-smoke-run",
+			},
+		});
+
+		const result = JSON.parse(output.join("").trim()) as {
+			run: { status: string; completed: number; failed: number };
+			runs: { stateKeys: string[] }[];
+		};
+		expect(result.run).toMatchObject({ status: "completed", completed: 1, failed: 0 });
+		expect(result.runs[0]?.stateKeys).toEqual(["marker"]);
+	});
+
 	it("checkpoints headless workflow starts on SIGINT instead of leaving a run alive", async () => {
 		using tempDir = TempDir.createSync("@omp-workflow-cli-sigint-");
 		const root = tempDir.path();
 		await Bun.write(`${root}/sigint-stop.omhflow`, workflowSigintStopFlow());
 		await Bun.write(`${root}/sigint-stop/scripts/hold.sh`, workflowSigintHoldScript());
 		const output: string[] = [];
 		const signalTarget = new FakeWorkflowStartSignalTarget();
 		vi.spyOn(process.stdout, "write").mockImplementation(chunk => {
 			output.push(typeof chunk === "string" ? chunk : new TextDecoder().decode(chunk));
 			return true;
 		});
 
 		const timer = setTimeout(() => {
 			signalTarget.emit("SIGINT");
 		}, 30);
 		timer.unref?.();
 		try {
 			await runWorkflowCommand(
 				{
 					action: "start",
 					args: [`${root}/sigint-stop.omhflow`],
 					flags: {
 						cwd: root,
 						json: true,
 						runId: "sigint-stop-run",
 						familyId: "sigint-stop-family",
 					},
 				},
 				{ signalTarget },
 			);
 		} finally {
 			clearTimeout(timer);
 		}
 
 		const result = JSON.parse(output.join("").trim()) as {
 			run: { status: string; frontier: string[] };
 			families: { attempts: { status: string }[]; checkpoints: { frontier: string[] }[] }[];
 		};
 		expect(result.run.status).toBe("stopped");
 		expect(result.run.frontier).toEqual(["hold"]);
 		expect(result.families[0]?.attempts[0]?.status).toBe("stopped");
 		expect(result.families[0]?.checkpoints[0]?.frontier).toEqual(["hold"]);
 		expect(signalTarget.listenerCount("SIGINT")).toBe(0);
 		expect(signalTarget.listenerCount("SIGTERM")).toBe(0);
 	});
 });
 
 class FakeWorkflowStartSignalTarget implements WorkflowStartSignalTarget {
 	#listeners = new Map<"SIGINT" | "SIGTERM", Set<() => void>>();
 
 	once(event: "SIGINT" | "SIGTERM", listener: () => void): void {
 		this.#listenersFor(event).add(listener);
 	}
 
 	off(event: "SIGINT" | "SIGTERM", listener: () => void): void {
 		this.#listenersFor(event).delete(listener);
 	}
 
 	emit(event: "SIGINT" | "SIGTERM"): void {
 		for (const listener of [...this.#listenersFor(event)]) {
 			this.off(event, listener);
 			listener();
 		}
 	}
 
 	listenerCount(event: "SIGINT" | "SIGTERM"): number {
 		return this.#listenersFor(event).size;
 	}
 
 	#listenersFor(event: "SIGINT" | "SIGTERM"): Set<() => void> {
 		let listeners = this.#listeners.get(event);
 		if (listeners === undefined) {
 			listeners = new Set();
 			this.#listeners.set(event, listeners);
 		}
 		return listeners;
 	}
 }
 
 function workflowAmbiguousHumanizeRlcrFlow(): string {
 	return [
 		"---",
 		"name: humanize-rlcr",
 		"version: 1",
 		"schema: omhflow/v1",
 		"resourceDir: humanize-rlcr",
 		"models:",
 		"  roles: {}",
 		"  defaults: {}",
 		"checkpoint:",
 		"  stopDeadlineMs: 30000",
 		"changePolicy:",
 		"  agentsCanPropose: true",
 		"  humansCanApprove: true",
 		"---",
 		"# Ambiguous humanize-rlcr fixture",
 		"",
 		"```yaml workflow",
 		"resources:",
 		"  - path: scripts/noop.sh",
 		"    kind: script",
 		"sequence:",
 		"  - node:",
 		"      id: noop",
 		"      type: script",
 		"      script:",
 		"        language: sh",
 		"        file: scripts/noop.sh",
 		"```",
 	].join("\n");
 }
 
 function workflowResourceSmokeFlow(): string {
 	return [
 		"---",
 		"name: resource-smoke",
 		"version: 1",
 		"schema: omhflow/v1",
 		"resourceDir: resource-smoke",
 		"models:",
 		"  roles: {}",
 		"  defaults: {}",
 		"checkpoint:",
 		"  stopDeadlineMs: 30000",
 		"changePolicy:",
 		"  agentsCanPropose: true",
 		"  humansCanApprove: true",
 		"---",
 		"# Resource smoke",
 		"",
 		"```yaml workflow",
 		"stateSchema:",
 		"  version: 1",
 		"  shape:",
 		"    message: string",
 		"resources:",
 		"  - path: scripts/read-resource.sh",
 		"    kind: script",
 		"  - path: data/message.txt",
 		"    kind: data",
 		"sequence:",
 		"  - node:",
 		"      id: readResource",
 		"      type: script",
 		"      script:",
 		"        language: sh",
 		"        file: scripts/read-resource.sh",
 		"      writes:",
 		"        - /message",
 		"```",
 	].join("\n");
 }
 
 function workflowResourceSmokeScript(): string {
 	return [
 		"#!/bin/sh",
 		"set -eu",
 		'message=$(cat "$OMP_WORKFLOW_RESOURCE_DIR/data/message.txt")',
 		'printf \'{"summary":"resource observed","statePatch":[{"op":"set","path":"/message","value":"%s"}]}\\n\' "$message"',
 	].join("\n");
 }
 
+function workflowJsCwdSmokeFlow(): string {
+	return [
+		"---",
+		"name: cwd-smoke",
+		"version: 1",
+		"schema: omhflow/v1",
+		"resourceDir: cwd-smoke",
+		"models:",
+		"  roles: {}",
+		"  defaults: {}",
+		"checkpoint:",
+		"  stopDeadlineMs: 30000",
+		"changePolicy:",
+		"  agentsCanPropose: true",
+		"  humansCanApprove: true",
+		"---",
+		"# JS cwd smoke",
+		"",
+		"```yaml workflow",
+		"stateSchema:",
+		"  version: 1",
+		"  shape:",
+		"    marker: string",
+		"resources:",
+		"  - path: scripts/read-cwd.js",
+		"    kind: script",
+		"sequence:",
+		"  - node:",
+		"      id: readCwd",
+		"      type: script",
+		"      script:",
+		"        language: js",
+		"        file: scripts/read-cwd.js",
+		"      writes:",
+		"        - /marker",
+		"```",
+	].join("\n");
+}
+
+function workflowJsCwdSmokeScript(): string {
+	return [
+		'const marker = (await Bun.file("marker.txt").text()).trim();',
+		"return {",
+		'  summary: "cwd marker observed",',
+		'  statePatch: [{ op: "set", path: "/marker", value: marker }],',
+		"};",
+	].join("\n");
+}
+
 function workflowSigintStopFlow(): string {
 	return [
 		"---",
 		"name: sigint-stop",
 		"version: 1",
 		"schema: omhflow/v1",
 		"resourceDir: sigint-stop",
 		"models:",
 		"  roles: {}",
 		"  defaults: {}",
 		"checkpoint:",
 		"  stopDeadlineMs: 30000",
 		"changePolicy:",
 		"  agentsCanPropose: true",
 		"  humansCanApprove: true",
 		"---",
 		"# SIGINT stop",
 		"",
 		"```yaml workflow",
 		"resources:",
 		"  - path: scripts/hold.sh",
 		"    kind: script",
 		"sequence:",
 		"  - node:",
 		"      id: hold",
 		"      type: script",
 		"      script:",
 		"        language: sh",
 		"        file: scripts/hold.sh",
 		"```",
 	].join("\n");
 }
 
 function workflowSigintHoldScript(): string {
 	return ["#!/bin/sh", "set -eu", "sleep 2", 'printf \'{"summary":"unexpected completion"}\\n\''].join("\n");
 }

```

Research requirements:
1. Inspect the current file at `packages/coding-agent/src/cli/__tests__/workflow-cli.test.ts` directly in the read-only export.
2. Focus on the algorithmic delta introduced by commits after 6b3819fad50a89fffae899b240ad1ce065c51d23: cwd handling for headless JS workflow scripts, node abort/deadline behavior, and related tests where applicable.
3. Preserve the exact item_id `OH_MY_HUMANIZE_MAIN-HZ-2969` in the heading and evidence. This addendum will be appended to the existing worker output for that item.
4. Include concrete current behavior, inputs/outputs/state, gates/invariants, dependencies/callers, edge cases, and validation/tests.
5. Mark worker cursor as `[_]` only; master will promote to `[x]` after verify.

Required format:
# agent_delta_04 oh-my-humanize main incremental research

## Worker Summary
- status: `[_]`
- source_commit_old: `6b3819fad50a89fffae899b240ad1ce065c51d23`
- source_commit_new: `bf4509d4f5a669375b3c88510ba0449e9770884c`
- assigned_item_count: 1

## Item Evidence

### OH_MY_HUMANIZE_MAIN-HZ-2969 `file` `packages/coding-agent/src/cli/__tests__/workflow-cli.test.ts`
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
- assigned_items_seen: `OH_MY_HUMANIZE_MAIN-HZ-2969`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`
