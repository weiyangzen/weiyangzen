**Topic and conclusion**

主题：Model router 与 task-tag routing。

结论：该子集里有两层路由机制：

1. `model-router.sh` 是确定性字符串规则路由：输入模型名，输出 provider `codex` 或 `claude`；输入 provider，再校验对应 CLI 依赖；输入 effort/provider，再做 provider 兼容性映射。没有评分、权重、历史状态或动态 fallback。
2. `commands/gen-plan.md` 定义的是计划文档中的任务标签协议：每个任务必须标成 `coding` 或 `analyze`；`coding` 归 Claude 实现，`analyze` 通过 Codex `/humanize:ask-codex` 执行。测试只验证生成/跟进 prompt 中持续保留该路由提示，以及 goal tracker 有 `Tag`/`Owner` 列。

**Algorithm subset covered**

覆盖范围仅限以下路径中与算法行为直接相关的内容：

- [scripts/lib/model-router.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/model-router.sh:10)：`detect_provider`、`check_provider_dependency`、`map_effort`
- [tests/test-model-router.sh](/Users/wangweiyang/GitHub/humanize/tests/test-model-router.sh:37)：模型名路由、依赖检查、effort 映射的行为断言
- [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:447)：计划生成阶段的 `Task Breakdown` 标签协议
- [tests/test-task-tag-routing.sh](/Users/wangweiyang/GitHub/humanize/tests/test-task-tag-routing.sh:99)：round-0 prompt、goal tracker、stop hook follow-up prompt 对 task-tag routing 的保留性断言

未覆盖安装说明、营销文本、截图、通用使用说明，也未进入非 focus path 的实现细节。

**Pseudocode**

```text
state:
  _MODEL_ROUTER_LOADED: source guard
  model_name: string
  provider: enum {codex, claude}
  binary: string
  effort: enum {xhigh, high, medium, low}
  target_provider: enum {codex, claude}

detect_provider(model_name):
  if model_name is empty:
    stderr "Model name must be non-empty"
    return error

  if model_name matches shell pattern "gpt-*" or "o[0-9]*":
    stdout "codex"
    return ok

  if model_name matches case-insensitive regex "(^claude-)|(haiku|sonnet|opus)":
    stdout "claude"
    return ok

  stderr "Unknown model name ..."
  return error


check_provider_dependency(provider):
  if provider == "codex":
    binary = "codex"
  else if provider == "claude":
    binary = "claude"
  else:
    stderr "Unknown provider ..."
    return error

  if command -v binary succeeds:
    return ok

  stderr "Required binary ... not found"
  stderr install hint based on provider
  return error


map_effort(effort, target_provider):
  if target_provider not in {codex, claude}:
    stderr "Unknown target provider ..."
    return error

  if effort not in {xhigh, high, medium, low}:
    stderr "Unknown effort ..."
    return error

  if target_provider == "claude" and effort == "xhigh":
    stderr info "Mapping effort xhigh to high"
    stdout "high"
    return ok

  stdout effort
  return ok
```

**Task-tag transition table**

| 输入/状态 | Gate | 转换/输出 | 证据 |
|---|---|---|---|
| plan generation reaches final plan structure | `## Task Breakdown` required | 每个 task 必须有且仅有 `coding` 或 `analyze` 标签 | [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:447), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:529) |
| task tag = `coding` | tag value valid | owner semantics: Claude implements | [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:449) |
| task tag = `analyze` | tag value valid | owner semantics: Codex via `/humanize:ask-codex` | [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:450) |
| round-0 RLCR prompt generated from plan | prompt must include routing section | prompt contains `## Task Tag Routing (MUST FOLLOW)` | [tests/test-task-tag-routing.sh](/Users/wangweiyang/GitHub/humanize/tests/test-task-tag-routing.sh:99) |
| round-0 RLCR prompt generated from plan | analyze routing must be visible | prompt contains `/humanize:ask-codex` | [tests/test-task-tag-routing.sh](/Users/wangweiyang/GitHub/humanize/tests/test-task-tag-routing.sh:105) |
| goal tracker generated | active tasks table schema gate | table has `Tag` and `Owner` columns | [tests/test-task-tag-routing.sh](/Users/wangweiyang/GitHub/humanize/tests/test-task-tag-routing.sh:111) |
| stop hook creates follow-up prompt | routing must persist across rounds | `round-1-prompt.md` contains `## Task Tag Routing Reminder` | [tests/test-task-tag-routing.sh](/Users/wangweiyang/GitHub/humanize/tests/test-task-tag-routing.sh:227) |
| stop hook creates follow-up prompt | analyze routing must persist | follow-up prompt contains `/humanize:ask-codex` | [tests/test-task-tag-routing.sh](/Users/wangweiyang/GitHub/humanize/tests/test-task-tag-routing.sh:233) |

**Source evidence**

- Source guard prevents double sourcing through `_MODEL_ROUTER_LOADED`; if already loaded, the file returns immediately. Evidence: [scripts/lib/model-router.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/model-router.sh:6), [scripts/lib/model-router.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/model-router.sh:7).
- `detect_provider` rejects empty model names before applying routing rules. Evidence: [scripts/lib/model-router.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/model-router.sh:10), [scripts/lib/model-router.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/model-router.sh:13).
- Codex routing rule is shell-pattern based: `gpt-*` or `o[0-9]*` routes to `codex`. Evidence: [scripts/lib/model-router.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/model-router.sh:18), [scripts/lib/model-router.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/model-router.sh:19).
- Claude routing rule is case-insensitive regex: model starts with `claude-` or contains `haiku`, `sonnet`, or `opus`. Evidence: [scripts/lib/model-router.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/model-router.sh:23), [scripts/lib/model-router.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/model-router.sh:24).
- Unknown model names are hard failures, not fallback to a default provider. Evidence: [scripts/lib/model-router.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/model-router.sh:28), [scripts/lib/model-router.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/model-router.sh:29); tested by [tests/test-model-router.sh](/Users/wangweiyang/GitHub/humanize/tests/test-model-router.sh:207), [tests/test-model-router.sh](/Users/wangweiyang/GitHub/humanize/tests/test-model-router.sh:209).
- Tests assert representative Codex model routes: `gpt-5.3-codex`, `gpt-4o`, `o3-mini`, `o1-pro`, `o4-mini`. Evidence: [tests/test-model-router.sh](/Users/wangweiyang/GitHub/humanize/tests/test-model-router.sh:37), [tests/test-model-router.sh](/Users/wangweiyang/GitHub/humanize/tests/test-model-router.sh:54), [tests/test-model-router.sh](/Users/wangweiyang/GitHub/humanize/tests/test-model-router.sh:71), [tests/test-model-router.sh](/Users/wangweiyang/GitHub/humanize/tests/test-model-router.sh:88), [tests/test-model-router.sh](/Users/wangweiyang/GitHub/humanize/tests/test-model-router.sh:105).
- Tests assert representative Claude model routes: `haiku`, `sonnet`, `opus`, `claude-sonnet-4-6`, uppercase `OPUS` inside a Claude model. Evidence: [tests/test-model-router.sh](/Users/wangweiyang/GitHub/humanize/tests/test-model-router.sh:122), [tests/test-model-router.sh](/Users/wangweiyang/GitHub/humanize/tests/test-model-router.sh:139), [tests/test-model-router.sh](/Users/wangweiyang/GitHub/humanize/tests/test-model-router.sh:156), [tests/test-model-router.sh](/Users/wangweiyang/GitHub/humanize/tests/test-model-router.sh:173), [tests/test-model-router.sh](/Users/wangweiyang/GitHub/humanize/tests/test-model-router.sh:190).
- `check_provider_dependency` maps provider to binary by exact provider name, then uses `command -v`. Evidence: [scripts/lib/model-router.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/model-router.sh:32), [scripts/lib/model-router.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/model-router.sh:36), [scripts/lib/model-router.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/model-router.sh:49).
- Missing binary is a hard failure with provider-specific install hint. Evidence: [scripts/lib/model-router.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/model-router.sh:53), [scripts/lib/model-router.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/model-router.sh:54), [scripts/lib/model-router.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/model-router.sh:56).
- Dependency tests cover success/failure for both `codex` and `claude`. Evidence: [tests/test-model-router.sh](/Users/wangweiyang/GitHub/humanize/tests/test-model-router.sh:243), [tests/test-model-router.sh](/Users/wangweiyang/GitHub/humanize/tests/test-model-router.sh:258), [tests/test-model-router.sh](/Users/wangweiyang/GitHub/humanize/tests/test-model-router.sh:277), [tests/test-model-router.sh](/Users/wangweiyang/GitHub/humanize/tests/test-model-router.sh:292).
- `map_effort` validates provider before effort values. Evidence: [scripts/lib/model-router.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/model-router.sh:66), [scripts/lib/model-router.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/model-router.sh:75).
- Only special effort mapping is `xhigh -> high` for `claude`; all other valid combinations pass through unchanged. Evidence: [scripts/lib/model-router.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/model-router.sh:84), [scripts/lib/model-router.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/model-router.sh:90).
- Tests confirm `xhigh` maps to `high` for Claude with info log, while `xhigh` passes through for Codex and `medium`/`low` pass through for Claude. Evidence: [tests/test-model-router.sh](/Users/wangweiyang/GitHub/humanize/tests/test-model-router.sh:311), [tests/test-model-router.sh](/Users/wangweiyang/GitHub/humanize/tests/test-model-router.sh:314), [tests/test-model-router.sh](/Users/wangweiyang/GitHub/humanize/tests/test-model-router.sh:346), [tests/test-model-router.sh](/Users/wangweiyang/GitHub/humanize/tests/test-model-router.sh:363), [tests/test-model-router.sh](/Users/wangweiyang/GitHub/humanize/tests/test-model-router.sh:380).
- Invalid effort is a hard failure for both providers. Evidence: [tests/test-model-router.sh](/Users/wangweiyang/GitHub/humanize/tests/test-model-router.sh:397), [tests/test-model-router.sh](/Users/wangweiyang/GitHub/humanize/tests/test-model-router.sh:414).
- `gen-plan` explicitly uses Codex first-pass analysis through `ask-codex.sh`, then feeds that into Claude planning. Evidence: [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:184), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:190), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:205).
- `gen-plan` direct mode skips the Claude/Codex convergence loop and sets `PLAN_CONVERGENCE_STATUS=partially_converged`, blocking auto-start convergence semantics. Evidence: [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:255), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:257).
- In discussion mode, second Codex review repeats until no required changes/high-impact disagreement remain, no material changes for two rounds, or max 3 rounds. Evidence: [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:286), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:288), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:291).
- Auto-start gate requires converged status, discussion mode, explicit flag, and no pending decisions. Evidence: [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:596), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:600).

**Gates, invariants, and failure modes**

- Gate: model name must be non-empty. Empty input returns non-zero and stderr error.
- Gate: provider must be exactly `codex` or `claude` for dependency and effort mapping.
- Gate: effort must be exactly one of `xhigh`, `high`, `medium`, `low`.
- Gate: provider binary must exist in `PATH`; otherwise routing cannot proceed for that provider.
- Invariant: provider detection is deterministic and order-dependent; Codex patterns are checked before Claude regex.
- Invariant: no unknown-model fallback exists; ambiguity or unsupported naming fails closed.
- Invariant: Claude does not receive `xhigh`; it is downgraded to `high` with an info message.
- Invariant: Codex may receive `xhigh` unchanged.
- Invariant: generated plans must include `## Task Breakdown`; each task must be tagged `coding` or `analyze`.
- Invariant: task-tag routing is expected to survive from initial RLCR prompt into stop-hook follow-up prompts.
- Failure mode: a model name like `my-sonnet-wrapper` routes to Claude because the Claude regex matches any occurrence of `sonnet`, not only provider prefixes.
- Failure mode: a model name that starts with uppercase `GPT-` or `O3-` does not route to Codex because Codex matching uses case-sensitive shell patterns; Claude matching is case-insensitive.
- Failure mode: an unknown provider fails before binary lookup; no attempt is made to infer provider from binary availability.
- Failure mode: `ask-codex.sh` failure during `gen-plan` is handled by asking the user whether to retry or continue Claude-only, with reduced cross-review confidence noted. Evidence: [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:208), [commands/gen-plan.md](/Users/wangweiyang/GitHub/humanize/commands/gen-plan.md:210).

**What is explicitly out of scope**

- CLI installation and environment setup beyond dependency presence checks.
- Marketing, screenshots, README-style usage, and non-behavioral prose.
- Actual implementation of `setup-rlcr-loop.sh`, stop hook internals, `ask-codex.sh`, and config loader internals; tests reference their externally observable routing behavior, but those files were not part of the requested focus subset.
- Model quality selection, scoring, load balancing, retry policy, latency/cost optimization, or provider fallback; no such scoring/routing algorithm appears in the inspected subset.
- Running tests: I only used read-only inspection commands and did not execute the test suites.