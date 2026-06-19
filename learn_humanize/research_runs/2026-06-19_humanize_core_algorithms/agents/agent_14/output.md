**Topic and conclusion**

Topic: Config merge algorithm

结论：该实现是一个固定 4 层、右侧优先的 JSON object 合并器：`empty -> default -> user -> project`。默认配置是必需层；用户配置和项目配置是可选层。每层在参与合并前必须是 JSON object，并会递归移除 `null`；因此 `null` 不能用来清空或覆盖低优先级值。项目层优先级最高，用户层次之，默认层最低。没有评分、动态路由或 schema 校验，只有固定路径解析、JSON object gate、null stripping 和 jq object merge。

**Algorithm subset covered**

覆盖范围仅限这 4 个文件：

- [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:24): layer 准备、路径解析、合并、取值。
- [config/default_config.json](/Users/wangweiyang/GitHub/humanize/config/default_config.json:1): 默认层内容。
- [tests/test-config-merge.sh](/Users/wangweiyang/GitHub/humanize/tests/test-config-merge.sh:3): 合并优先级、加法合并、`null` 行为、`HUMANIZE_CONFIG` 行为。
- [tests/test-config-error-handling.sh](/Users/wangweiyang/GitHub/humanize/tests/test-config-error-handling.sh:3): 缺失/格式错误配置的失败与降级行为。

核心输入：

- `plugin_root`: 用于定位默认配置，路径为 `$plugin_root/config/default_config.json`，见 [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:77)。
- `project_root`: 用于定位默认项目配置，路径为 `$project_root/.humanize/config.json`，见 [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:87)。
- 环境变量 `XDG_CONFIG_HOME`: 若存在，用户配置为 `$XDG_CONFIG_HOME/humanize/config.json`，见 [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:78)。
- 环境变量 `HOME`: 若无 `XDG_CONFIG_HOME`，用户配置为 `${HOME:-}/.config/humanize/config.json`，见 [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:81)。
- 环境变量 `HUMANIZE_CONFIG`: 若存在，覆盖项目配置路径，见 [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:84)。

核心状态变量：

- `default_config_path`, `user_config_path`, `project_config_path`: 三个实际 layer 路径，见 [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:66)。
- `empty_layer_file`, `default_layer_file`, `user_layer_file`, `project_layer_file`: 临时规范化 layer 文件，见 [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:103)。
- `merged_json`: jq 合并后的最终 JSON，见 [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:98)。

**Pseudocode**

```text
load_merged_config(plugin_root, project_root):
  if plugin_root or project_root missing:
    fatal usage error

  require jq

  default_path = plugin_root + "/config/default_config.json"

  if XDG_CONFIG_HOME is set:
    user_path = XDG_CONFIG_HOME + "/humanize/config.json"
  else:
    user_path = HOME + "/.config/humanize/config.json"

  if HUMANIZE_CONFIG is set:
    project_path = HUMANIZE_CONFIG
  else:
    project_path = project_root + "/.humanize/config.json"

  create tmp_dir
  layer0 = {}
  layer1 = prepare_layer(default_path, required=true)
  layer2 = prepare_layer(user_path, required=false)
  layer3 = prepare_layer(project_path, required=false)

  for each layer:
    strip_nulls recursively:
      object: remove keys whose value is null; recurse into remaining values
      array: remove null elements; recurse into remaining elements
      scalar: keep as-is

  return strip(layer0) * strip(layer1) * strip(layer2) * strip(layer3)
```

```text
prepare_layer(path, label, output, required):
  if output path missing:
    fatal internal error

  if path is empty:
    output {}

  if file does not exist:
    if required:
      fatal missing required layer
    else:
      output {}

  if file is not valid JSON object:
    if required:
      fatal malformed required layer
    else:
      warn and output {}

  output normalized JSON object
```

合并顺序是核心优先级规则：`layer0 * layer1 * layer2 * layer3`，见 [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:128), [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:129), [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:130), [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:131)。按 jq object merge 的语义，右侧 layer 覆盖左侧冲突 key；因此项目配置覆盖用户配置，用户配置覆盖默认配置。

**Source evidence**

- `load_merged_config` 要求两个参数；缺失时报 usage fatal，见 [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:70) 和 [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:71)。
- jq 是硬依赖；缺失时 `_config_loader_require_jq` 返回 fatal，见 [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:17), [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:18), [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:19)。
- 默认层路径固定为 `$plugin_root/config/default_config.json`，见 [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:77)；默认值包括 `bitlesson_model: "haiku"`、`agent_teams: false`、`gen_plan_mode: "discussion"`，见 [config/default_config.json](/Users/wangweiyang/GitHub/humanize/config/default_config.json:4), [config/default_config.json](/Users/wangweiyang/GitHub/humanize/config/default_config.json:5), [config/default_config.json](/Users/wangweiyang/GitHub/humanize/config/default_config.json:7)。
- 用户配置路径优先使用 `XDG_CONFIG_HOME`，否则使用 `HOME/.config`，见 [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:78) 和 [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:81)。
- 项目配置路径可被 `HUMANIZE_CONFIG` 覆盖，见 [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:84)；测试证明自定义路径会覆盖 `.humanize/config.json`，见 [tests/test-config-merge.sh](/Users/wangweiyang/GitHub/humanize/tests/test-config-merge.sh:159), [tests/test-config-merge.sh](/Users/wangweiyang/GitHub/humanize/tests/test-config-merge.sh:164), [tests/test-config-merge.sh](/Users/wangweiyang/GitHub/humanize/tests/test-config-merge.sh:168)。
- layer 文件不存在时，required layer fatal，optional layer 写入 `{}`，见 [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:40), [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:42), [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:46), [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:48)。
- 每个配置文件必须是 JSON object；非 object 或 malformed JSON 通过 jq gate 拒绝，见 [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:52)。required malformed fatal，optional malformed warning 后写 `{}`，见 [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:54), [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:57), [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:58)。
- 默认层 required，用户层 optional，项目层 optional，见 [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:109), [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:110), [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:111)。
- `strip_nulls` 会删除 object 中值为 `null` 的 entry，并递归处理剩余值，见 [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:119), [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:121)。数组中的 `null` 元素也会被删除，见 [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:122), [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:123)。
- 测试确认 project 覆盖 default：项目写入 `{"bitlesson_model": "opus"}` 后最终值为 `opus`，见 [tests/test-config-merge.sh](/Users/wangweiyang/GitHub/humanize/tests/test-config-merge.sh:73), [tests/test-config-merge.sh](/Users/wangweiyang/GitHub/humanize/tests/test-config-merge.sh:78)。
- 测试确认 project 覆盖 user：用户为 `user-model`、项目为 `project-model`，最终值为 `project-model`，见 [tests/test-config-merge.sh](/Users/wangweiyang/GitHub/humanize/tests/test-config-merge.sh:99), [tests/test-config-merge.sh](/Users/wangweiyang/GitHub/humanize/tests/test-config-merge.sh:100), [tests/test-config-merge.sh](/Users/wangweiyang/GitHub/humanize/tests/test-config-merge.sh:105)。
- 测试确认加法合并：用户提供 `bitlesson_model`、项目提供 `gen_plan_mode`，两者都保留，见 [tests/test-config-merge.sh](/Users/wangweiyang/GitHub/humanize/tests/test-config-merge.sh:119), [tests/test-config-merge.sh](/Users/wangweiyang/GitHub/humanize/tests/test-config-merge.sh:120), [tests/test-config-merge.sh](/Users/wangweiyang/GitHub/humanize/tests/test-config-merge.sh:126)。
- 测试确认 `null` 不覆盖低层值：项目写入 `{"bitlesson_model": null}` 后最终仍为默认 `haiku`，见 [tests/test-config-merge.sh](/Users/wangweiyang/GitHub/humanize/tests/test-config-merge.sh:141), [tests/test-config-merge.sh](/Users/wangweiyang/GitHub/humanize/tests/test-config-merge.sh:146)。
- `get_config_value` 只按顶层 key 读取：`has($key)` 后访问 `.[$key]`，见 [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:148), [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:149), [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:150)。string 原样输出，非 string 非 null 转成字符串，缺失 key 输出空，见 [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:151), [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:153), [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:156)。

**Edge cases and risks**

- `null` 不是“显式清空”语义，而是“从该 layer 删除”。这避免 accidental override，但也意味着用户无法把某个配置值设为 JSON null；代码证据见 [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:121)，测试证据见 [tests/test-config-merge.sh](/Users/wangweiyang/GitHub/humanize/tests/test-config-merge.sh:146)。
- 数组中的 `null` 元素也会被删除；测试只覆盖 object key 为 `null` 的情况，没有覆盖数组 null stripping，代码证据见 [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:123)。
- 可选配置 malformed 时不会阻断执行，只 warning 并降级为 `{}`；项目 malformed 的测试见 [tests/test-config-error-handling.sh](/Users/wangweiyang/GitHub/humanize/tests/test-config-error-handling.sh:62), [tests/test-config-error-handling.sh](/Users/wangweiyang/GitHub/humanize/tests/test-config-error-handling.sh:67), [tests/test-config-error-handling.sh](/Users/wangweiyang/GitHub/humanize/tests/test-config-error-handling.sh:77)。用户 malformed 的测试见 [tests/test-config-error-handling.sh](/Users/wangweiyang/GitHub/humanize/tests/test-config-error-handling.sh:91), [tests/test-config-error-handling.sh](/Users/wangweiyang/GitHub/humanize/tests/test-config-error-handling.sh:96), [tests/test-config-error-handling.sh](/Users/wangweiyang/GitHub/humanize/tests/test-config-error-handling.sh:106)。
- 默认配置缺失或 malformed 是 fatal，因为默认层是 required；缺失默认配置测试见 [tests/test-config-error-handling.sh](/Users/wangweiyang/GitHub/humanize/tests/test-config-error-handling.sh:43), [tests/test-config-error-handling.sh](/Users/wangweiyang/GitHub/humanize/tests/test-config-error-handling.sh:48)。
- 空 object `{}` 是合法配置；不会覆盖任何默认值。测试证据见 [tests/test-config-error-handling.sh](/Users/wangweiyang/GitHub/humanize/tests/test-config-error-handling.sh:119), [tests/test-config-error-handling.sh](/Users/wangweiyang/GitHub/humanize/tests/test-config-error-handling.sh:124)。
- 缺失项目配置和缺失用户配置都不是 fatal，会回退默认值；项目缺失测试见 [tests/test-config-error-handling.sh](/Users/wangweiyang/GitHub/humanize/tests/test-config-error-handling.sh:139), [tests/test-config-error-handling.sh](/Users/wangweiyang/GitHub/humanize/tests/test-config-error-handling.sh:142)。用户目录缺失测试见 [tests/test-config-error-handling.sh](/Users/wangweiyang/GitHub/humanize/tests/test-config-error-handling.sh:161), [tests/test-config-error-handling.sh](/Users/wangweiyang/GitHub/humanize/tests/test-config-error-handling.sh:164)。
- `get_config_value` 不支持 dotted path 或 nested lookup；它把传入 key 当作顶层字段名处理，见 [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:149)。
- 没有 schema/type validation：只验证根节点是 object。比如 `agent_teams` 是否 boolean、`codex_effort` 是否枚举，不在该算法中检查；唯一 gate 是 JSON object，见 [scripts/lib/config-loader.sh](/Users/wangweiyang/GitHub/humanize/scripts/lib/config-loader.sh:52)。

**What is explicitly out of scope**

- 不覆盖安装说明、README 营销/用法说明、截图、插件市场元数据。
- 不覆盖配置值被下游脚本如何消费；这里只分析加载、合并和顶层取值。
- 不覆盖模型选择策略、agent routing、计划生成行为等业务语义；这些文件只定义配置层合并。
- 不覆盖完整测试执行结果；本次按要求只做只读静态检查，没有编辑文件、没有提交、没有网络搜索。