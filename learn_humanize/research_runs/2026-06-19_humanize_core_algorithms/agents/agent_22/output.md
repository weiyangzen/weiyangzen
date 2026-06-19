**Topic and conclusion**

BitLesson selector routing 的核心算法是一个“配置驱动的两阶段路由器”：先用 `bitlesson_model` 推断 provider，再按 `provider_mode` 与 CLI 可用性做强制改写或 fallback，最后把同一个选择 prompt 交给 Codex CLI 或 Claude CLI 执行。真正的 lesson 选择不是脚本内打分完成，而是由模型按 prompt 规则执行；脚本只负责输入门禁、provider 路由、执行隔离、超时、以及稳定输出格式校验。

结论：路由规则是确定性的；选择规则是模型判定型，但被稳定输入、只读/禁工具 prompt、两行输出契约约束。主要风险在于 `detect_provider` 的模式匹配较宽，以及“任意 provider 缺失均 fallback 到 Codex”会让 Codex 缺失时表现为二次失败。

**Algorithm subset covered**

覆盖范围：

- Selector prompt 与选择规则：[agents/bitlesson-selector.md:10](/Users/wangweiyang/GitHub/humanize/agents/bitlesson-selector.md:10), [agents/bitlesson-selector.md:26](/Users/wangweiyang/GitHub/humanize/agents/bitlesson-selector.md:26)
- Runtime wrapper、输入门禁、prompt 组装、provider 执行、输出校验：[scripts/bitlesson-select.sh:20](/Users/wangweiyang/GitHub/humanize/scripts/bitlesson-select.sh:20), [scripts/bitlesson-select.sh:76](/Users/wangweiyang/GitHub/humanize/scripts/bitlesson-select.sh:76), [scripts/bitlesson-select.sh:115](/Users/wangweiyang/GitHub/humanize/scripts/bitlesson-select.sh:115), [scripts/bitlesson-select.sh:188](/Users/wangweiyang/GitHub/humanize/scripts/bitlesson-select.sh:188), [scripts/bitlesson-select.sh:242](/Users/wangweiyang/GitHub/humanize/scripts/bitlesson-select.sh:242)
- 路由辅助库，因脚本直接 source 且其中定义 `detect_provider` 与 `check_provider_dependency`：[scripts/bitlesson-select.sh:11](/Users/wangweiyang/GitHub/humanize/scripts/bitlesson-select.sh:11), [scripts/lib/model-router.sh:10](/Users/wangweiyang/GitHub/humanize/scripts/lib/model-router.sh:10)
- 行为文档与测试断言：[docs/bitlesson.md:7](/Users/wangweiyang/GitHub/humanize/docs/bitlesson.md:7), [docs/bitlesson.md:14](/Users/wangweiyang/GitHub/humanize/docs/bitlesson.md:14), [tests/test-bitlesson-select-routing.sh:137](/Users/wangweiyang/GitHub/humanize/tests/test-bitlesson-select-routing.sh:137)

**Pseudocode or transition table**

```text
inputs:
  task: non-empty string
  paths: non-empty comma-separated string
  bitlesson_file: existing, non-empty file
  merged_config:
    bitlesson_model default "haiku"
    codex_model default DEFAULT_CODEX_MODEL
    provider_mode default "auto"

state:
  BITLESSON_MODEL
  CODEX_FALLBACK_MODEL
  PROVIDER_MODE
  BITLESSON_PROVIDER
  BITLESSON_CONTENT
  CODEX_PROJECT_ROOT
  PROMPT
  RAW_OUTPUT

algorithm:
  load merged config
  BITLESSON_MODEL = config.bitlesson_model or "haiku"
  CODEX_FALLBACK_MODEL = config.codex_model or DEFAULT_CODEX_MODEL
  PROVIDER_MODE = config.provider_mode or "auto"

  require task, paths, bitlesson_file
  require bitlesson_file exists
  read BITLESSON_CONTENT
  require non-whitespace content

  if BITLESSON_CONTENT has no line matching "^\s*##\s+Lesson:":
      emit "LESSON_IDS: NONE"
      emit "RATIONALE: The BitLesson file has no recorded lessons yet."
      exit 0

  BITLESSON_PROVIDER = detect_provider(BITLESSON_MODEL)
    if model starts "gpt-" or matches shell pattern "o[0-9]*": codex
    else if regex /(^claude-)|(haiku|sonnet|opus)/i: claude
    else error

  if PROVIDER_MODE == "codex-only" and BITLESSON_PROVIDER == "claude":
      BITLESSON_MODEL = CODEX_FALLBACK_MODEL
      BITLESSON_PROVIDER = codex

  if dependency for BITLESSON_PROVIDER missing:
      BITLESSON_MODEL = DEFAULT_CODEX_MODEL
      BITLESSON_PROVIDER = codex
      require codex dependency

  CODEX_PROJECT_ROOT = git top-level of bitlesson_file directory, else bitlesson_file directory

  build prompt from task, paths, full bitlesson content, decision rules

  run selector with timeout 120s:
    if provider == codex:
       optionally add --disable codex_hooks, --skip-git-repo-check, --ephemeral if CLI supports them
       run: codex exec -s read-only -m model -c model_reasoning_effort=low -C CODEX_PROJECT_ROOT -
    if provider == claude:
       run: claude --print --model model -

  if timeout: exit 124
  if nonzero selector exit: propagate failure

  parse first LESSON_IDS line and first RATIONALE line
  require both non-empty
  emit normalized two-line output
```

Transition table:

| Current condition | Gate / match | Next state / output |
|---|---|---|
| Missing `--task` | `TASK == ""` | error, usage, exit 1 |
| Missing `--paths` | `PATHS == ""` | error, usage, exit 1 |
| Missing `--bitlesson-file` | empty path | error, usage, exit 1 |
| File absent | `! -f` | error, exit 1 |
| File whitespace-only | stripped content empty | error, exit 1 |
| No recorded lessons | no `## Lesson:` heading | output `LESSON_IDS: NONE`, exit 0 |
| Model `gpt-*` or `o[0-9]*` | `detect_provider` | provider `codex` |
| Model `claude-*`, `haiku`, `sonnet`, `opus` | case-insensitive regex | provider `claude` |
| Unknown model | no route match | error, exit nonzero |
| `provider_mode=codex-only` and provider is `claude` | override gate | provider `codex`, model `codex_model` fallback |
| Chosen binary missing | dependency gate fails | set provider `codex`, model `DEFAULT_CODEX_MODEL`, then require Codex |
| Selector timeout | exit 124 from wrapper | error, exit 124 |
| Selector output lacks required lines | missing parsed values | error, dump raw output, exit 1 |
| Valid selector output | two lines present | normalize and emit exactly two lines |

**Source evidence**

- Config state is loaded from merged config, then defaults are applied: `bitlesson_model` defaults to `haiku`, `codex_model` to `$DEFAULT_CODEX_MODEL`, and `provider_mode` to `auto` in [scripts/bitlesson-select.sh:20](/Users/wangweiyang/GitHub/humanize/scripts/bitlesson-select.sh:20)-[scripts/bitlesson-select.sh:26](/Users/wangweiyang/GitHub/humanize/scripts/bitlesson-select.sh:26). The documented config hierarchy is default config, user config, project config, then CLI flags where applicable in [docs/bitlesson.md:7](/Users/wangweiyang/GitHub/humanize/docs/bitlesson.md:7)-[docs/bitlesson.md:12](/Users/wangweiyang/GitHub/humanize/docs/bitlesson.md:12).
- CLI inputs are exactly `--task`, `--paths`, `--bitlesson-file`, with output contract `LESSON_IDS` and `RATIONALE` in [scripts/bitlesson-select.sh:35](/Users/wangweiyang/GitHub/humanize/scripts/bitlesson-select.sh:35)-[scripts/bitlesson-select.sh:43](/Users/wangweiyang/GitHub/humanize/scripts/bitlesson-select.sh:43). Required input gates are enforced in [scripts/bitlesson-select.sh:76](/Users/wangweiyang/GitHub/humanize/scripts/bitlesson-select.sh:76)-[scripts/bitlesson-select.sh:96](/Users/wangweiyang/GitHub/humanize/scripts/bitlesson-select.sh:96).
- BitLesson content gates: file is read, whitespace-only content fails, and absence of any `## Lesson:` heading short-circuits to `NONE` without model invocation in [scripts/bitlesson-select.sh:99](/Users/wangweiyang/GitHub/humanize/scripts/bitlesson-select.sh:99)-[scripts/bitlesson-select.sh:108](/Users/wangweiyang/GitHub/humanize/scripts/bitlesson-select.sh:108). Test 9 asserts the placeholder file returns `LESSON_IDS: NONE` with “no recorded lessons” in [tests/test-bitlesson-select-routing.sh:416](/Users/wangweiyang/GitHub/humanize/tests/test-bitlesson-select-routing.sh:416)-[tests/test-bitlesson-select-routing.sh:436](/Users/wangweiyang/GitHub/humanize/tests/test-bitlesson-select-routing.sh:436).
- Provider detection is delegated through `detect_provider` in [scripts/bitlesson-select.sh:115](/Users/wangweiyang/GitHub/humanize/scripts/bitlesson-select.sh:115). The concrete routing rules are `gpt-*` or `o[0-9]*` to `codex`, and case-insensitive `(^claude-)|(haiku|sonnet|opus)` to `claude`, otherwise error, in [scripts/lib/model-router.sh:18](/Users/wangweiyang/GitHub/humanize/scripts/lib/model-router.sh:18)-[scripts/lib/model-router.sh:29](/Users/wangweiyang/GitHub/humanize/scripts/lib/model-router.sh:29). Docs state the same model families in [docs/bitlesson.md:14](/Users/wangweiyang/GitHub/humanize/docs/bitlesson.md:14)-[docs/bitlesson.md:17](/Users/wangweiyang/GitHub/humanize/docs/bitlesson.md:17).
- `provider_mode: "codex-only"` rewrites Claude routing to Codex before dependency checks in [scripts/bitlesson-select.sh:117](/Users/wangweiyang/GitHub/humanize/scripts/bitlesson-select.sh:117)-[scripts/bitlesson-select.sh:120](/Users/wangweiyang/GitHub/humanize/scripts/bitlesson-select.sh:120). Docs describe this Codex-only force route in [docs/bitlesson.md:21](/Users/wangweiyang/GitHub/humanize/docs/bitlesson.md:21)-[docs/bitlesson.md:23](/Users/wangweiyang/GitHub/humanize/docs/bitlesson.md:23), and Test 8 covers `haiku` plus `provider_mode=codex-only` routing to mock Codex in [tests/test-bitlesson-select-routing.sh:390](/Users/wangweiyang/GitHub/humanize/tests/test-bitlesson-select-routing.sh:390)-[tests/test-bitlesson-select-routing.sh:412](/Users/wangweiyang/GitHub/humanize/tests/test-bitlesson-select-routing.sh:412).
- Dependency check maps provider to binary `codex` or `claude`, requires it on `PATH`, and emits provider-specific errors in [scripts/lib/model-router.sh:32](/Users/wangweiyang/GitHub/humanize/scripts/lib/model-router.sh:32)-[scripts/lib/model-router.sh:59](/Users/wangweiyang/GitHub/humanize/scripts/lib/model-router.sh:59). The selector falls back to Codex when the configured provider binary is missing in [scripts/bitlesson-select.sh:126](/Users/wangweiyang/GitHub/humanize/scripts/bitlesson-select.sh:126)-[scripts/bitlesson-select.sh:130](/Users/wangweiyang/GitHub/humanize/scripts/bitlesson-select.sh:130); docs summarize that behavior in [docs/bitlesson.md:19](/Users/wangweiyang/GitHub/humanize/docs/bitlesson.md:19).
- Prompt decision rules are precision-biased: directly relevant lessons only, prefer precision over recall, return `NONE` if nothing relevant, and no external tools/repo inspection in [scripts/bitlesson-select.sh:166](/Users/wangweiyang/GitHub/humanize/scripts/bitlesson-select.sh:166)-[scripts/bitlesson-select.sh:178](/Users/wangweiyang/GitHub/humanize/scripts/bitlesson-select.sh:178). The agent spec mirrors these rules in [agents/bitlesson-selector.md:26](/Users/wangweiyang/GitHub/humanize/agents/bitlesson-selector.md:26)-[agents/bitlesson-selector.md:39](/Users/wangweiyang/GitHub/humanize/agents/bitlesson-selector.md:39).
- Codex execution is deliberately helper-like: optional hook disabling, optional repo-check skip and ephemeral mode, `-s read-only`, low reasoning effort, `-C` project root, and prompt via stdin trailing `-` in [scripts/bitlesson-select.sh:192](/Users/wangweiyang/GitHub/humanize/scripts/bitlesson-select.sh:192)-[scripts/bitlesson-select.sh:212](/Users/wangweiyang/GitHub/humanize/scripts/bitlesson-select.sh:212). Test 10 asserts `--disable codex_hooks`, `--skip-git-repo-check`, `--ephemeral`, `read-only`, and absence of `--full-auto` in [tests/test-bitlesson-select-routing.sh:440](/Users/wangweiyang/GitHub/humanize/tests/test-bitlesson-select-routing.sh:440)-[tests/test-bitlesson-select-routing.sh:493](/Users/wangweiyang/GitHub/humanize/tests/test-bitlesson-select-routing.sh:493).
- Claude execution uses `claude --print --model "$model" -` with prompt from stdin in [scripts/bitlesson-select.sh:215](/Users/wangweiyang/GitHub/humanize/scripts/bitlesson-select.sh:215)-[scripts/bitlesson-select.sh:217](/Users/wangweiyang/GitHub/humanize/scripts/bitlesson-select.sh:217).
- Post-execution gates: timeout exits 124, nonzero selector exits are propagated, and stable output requires parsable first `LESSON_IDS:` and `RATIONALE:` lines in [scripts/bitlesson-select.sh:224](/Users/wangweiyang/GitHub/humanize/scripts/bitlesson-select.sh:224)-[scripts/bitlesson-select.sh:235](/Users/wangweiyang/GitHub/humanize/scripts/bitlesson-select.sh:235), [scripts/bitlesson-select.sh:242](/Users/wangweiyang/GitHub/humanize/scripts/bitlesson-select.sh:242)-[scripts/bitlesson-select.sh:267](/Users/wangweiyang/GitHub/humanize/scripts/bitlesson-select.sh:267).

**Edge cases and risks**

- `o[0-9]*` is a shell glob, not the documented `o[N]-*` exactly. It will route `o3` and `o3foo` to Codex, not just `o3-*`; implementation is broader than docs in [scripts/lib/model-router.sh:18](/Users/wangweiyang/GitHub/humanize/scripts/lib/model-router.sh:18) versus [docs/bitlesson.md:16](/Users/wangweiyang/GitHub/humanize/docs/bitlesson.md:16).
- Claude regex is substring-based for `haiku|sonnet|opus`; a non-Claude model name containing those substrings would route to Claude. Evidence: [scripts/lib/model-router.sh:23](/Users/wangweiyang/GitHub/humanize/scripts/lib/model-router.sh:23).
- Unknown model fails before dependency fallback, because `detect_provider` returns nonzero and the script uses `set -e`; Test 5 expects nonzero plus error text in [tests/test-bitlesson-select-routing.sh:287](/Users/wangweiyang/GitHub/humanize/tests/test-bitlesson-select-routing.sh:287)-[tests/test-bitlesson-select-routing.sh:309](/Users/wangweiyang/GitHub/humanize/tests/test-bitlesson-select-routing.sh:309).
- If Codex is selected and `codex` is missing, fallback sets provider to Codex again and the second dependency check fails. Test 6 expects nonzero with `codex` in stderr in [tests/test-bitlesson-select-routing.sh:313](/Users/wangweiyang/GitHub/humanize/tests/test-bitlesson-select-routing.sh:313)-[tests/test-bitlesson-select-routing.sh:345](/Users/wangweiyang/GitHub/humanize/tests/test-bitlesson-select-routing.sh:345).
- If Claude is selected and `claude` is missing but `codex` exists, fallback succeeds; Test 7 covers this in [tests/test-bitlesson-select-routing.sh:349](/Users/wangweiyang/GitHub/humanize/tests/test-bitlesson-select-routing.sh:349)-[tests/test-bitlesson-select-routing.sh:382](/Users/wangweiyang/GitHub/humanize/tests/test-bitlesson-select-routing.sh:382).
- Lesson selection has no deterministic internal scoring function; “direct relevance”, “failure mode”, and “precision over recall” are model-evaluated criteria. This is intentional in the prompt, but it means routing is deterministic while selection is constrained-natural-language inference, not a pure parser.

**What is explicitly out of scope**

- Installation, marketing, screenshots, generic usage prose, and full RLCR workflow details beyond selector routing.
- BitLesson authoring/update validation except where it affects selector `NONE` behavior.
- Running tests, because the routing test script creates temporary files and mocks; this pass stayed read-only.
- Network lookup or external provider documentation.
- Non-routing helper behavior such as `map_effort`, except noting it exists in the same library but is not called by `bitlesson-select.sh` for this path.