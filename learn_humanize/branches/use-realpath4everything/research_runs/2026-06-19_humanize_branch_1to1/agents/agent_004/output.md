# agent_004 use-realpath4everything 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`

## Item Evidence

### USE_REALPATH4EVERYTHING-HZ-004 `directory` `config`
- cursor: `[_]`
- core_role:
  - `config` is a runtime configuration directory, not executable algorithm code. It supplies default knobs and hook-install templates used by the Humanize RLCR/Codex runtime.
  - Recursive contents are exactly two JSON files: `config/codex-hooks.json` and `config/default_config.json`; byte total matches assignment metadata at 562 bytes.
  - `config/default_config.json` is the lowest-priority config layer for merged runtime settings. It defines `codex_model`, `codex_effort`, `bitlesson_model`, `agent_teams`, `alternative_plan_language`, and `gen_plan_mode` at `config/default_config.json:2` through `config/default_config.json:7`.
  - `config/codex-hooks.json` is the native Codex Stop-hook template. It declares a `Stop` hook whose command placeholder points to `{{HUMANIZE_RUNTIME_ROOT}}/hooks/loop-codex-stop-hook.sh` at `config/codex-hooks.json:3` through `config/codex-hooks.json:16`.

- algorithmic_behavior:
  - The directory’s behavior is declarative. Runtime algorithms consume it through loaders/installers rather than executing it directly.
  - `default_config.json` participates in a four-layer merge performed by `scripts/lib/config-loader.sh`: default config, user config, project config, and later CLI flags where supported. The default file is resolved as `$plugin_root/config/default_config.json` at `scripts/lib/config-loader.sh:77`, then merged with user and project layers at `scripts/lib/config-loader.sh:113` through `scripts/lib/config-loader.sh:132`.
  - Merge semantics are object-only JSON validation plus null-stripping. `_config_loader_prepare_layer` rejects missing required default config, ignores malformed optional user/project config, and requires JSON objects at `scripts/lib/config-loader.sh:40` through `scripts/lib/config-loader.sh:60`. The merge strips null values recursively before applying layers at `scripts/lib/config-loader.sh:119` through `scripts/lib/config-loader.sh:131`.
  - `hooks/lib/loop-common.sh` consumes merged config to derive runtime defaults. `bitlesson_model` becomes `DEFAULT_BITLESSON_MODEL` at `hooks/lib/loop-common.sh:204` through `hooks/lib/loop-common.sh:206`. `codex_model` and `codex_effort` are validated and fall back to `gpt-5.4`/`high` at `hooks/lib/loop-common.sh:208` through `hooks/lib/loop-common.sh:230`. `agent_teams` becomes `DEFAULT_AGENT_TEAMS` at `hooks/lib/loop-common.sh:232` through `hooks/lib/loop-common.sh:235`.
  - `codex-hooks.json` is transformed by `scripts/install-codex-hooks.sh`. The installer reads the template, replaces `{{HUMANIZE_RUNTIME_ROOT}}`, JSON-escapes the runtime root, parses the resulting JSON, shell-quotes hook commands, removes old managed Humanize stop hooks, preserves unrelated hooks, appends the managed Stop group, and writes `${CODEX_HOME}/hooks.json` at `scripts/install-codex-hooks.sh:94` through `scripts/install-codex-hooks.sh:171`.

- inputs_outputs_state:
  - Inputs:
    - Installed/default runtime files under `config/`.
    - Optional user config at `$XDG_CONFIG_HOME/humanize/config.json` or `$HOME/.config/humanize/config.json`, selected at `scripts/lib/config-loader.sh:78` through `scripts/lib/config-loader.sh:82`.
    - Optional project config at `.humanize/config.json`, or `HUMANIZE_CONFIG` override, selected at `scripts/lib/config-loader.sh:84` through `scripts/lib/config-loader.sh:88`.
    - Codex install parameters `--codex-config-dir` and `--runtime-root`, parsed at `scripts/install-codex-hooks.sh:41` through `scripts/install-codex-hooks.sh:69`.
  - Outputs:
    - `load_merged_config` prints merged JSON to stdout at `scripts/lib/config-loader.sh:135`.
    - `get_config_value` extracts scalar/stringified config values at `scripts/lib/config-loader.sh:139` through `scripts/lib/config-loader.sh:158`.
    - Codex install writes `${CODEX_HOME}/hooks.json` with managed Stop hook entries at `scripts/install-codex-hooks.sh:170` through `scripts/install-codex-hooks.sh:171`.
    - Codex skill install also seeds `${XDG_CONFIG_HOME:-~/.config}/humanize/config.json` with a Codex/OpenAI `bitlesson_model` and `provider_mode: "codex-only"` when unset, using defaults loaded from installed `runtime_root/config/default_config.json` at `scripts/install-skill.sh:269` through `scripts/install-skill.sh:319`.
  - State transitions:
    - Config merge state is purely read-time: defaults are overlaid by user/project config, with higher layers overriding lower layers unless values are null.
    - Hook install state transitions `${CODEX_HOME}/hooks.json` from existing hooks to existing-minus-stale-managed-Humanize-hooks plus the current managed Humanize Stop hook. Idempotency is achieved by filtering managed commands before appending the template at `scripts/install-codex-hooks.sh:138` through `scripts/install-codex-hooks.sh:165`.

- gates_or_invariants:
  - `default_config.json` is required. Missing or malformed required default config is fatal in `_config_loader_prepare_layer` at `scripts/lib/config-loader.sh:40` through `scripts/lib/config-loader.sh:55`.
  - User/project config files are optional. Missing optional files become `{}` at `scripts/lib/config-loader.sh:48` through `scripts/lib/config-loader.sh:49`; malformed optional files warn and become `{}` at `scripts/lib/config-loader.sh:57` through `scripts/lib/config-loader.sh:59`.
  - Merged config must be a JSON object at every layer; arrays/scalars are rejected by the `jq` object check at `scripts/lib/config-loader.sh:52`.
  - Codex model names from config must match shell-safe characters and start with a Codex model prefix (`gpt-` or `o[0-9]`), otherwise they warn and fall back at `hooks/lib/loop-common.sh:211` through `hooks/lib/loop-common.sh:222`.
  - Codex effort must be one of `xhigh`, `high`, `medium`, or `low`, otherwise it warns and falls back at `hooks/lib/loop-common.sh:223` through `hooks/lib/loop-common.sh:230`.
  - Codex hook installation requires `config/codex-hooks.json` to exist at `scripts/install-codex-hooks.sh:71`, requires `python3` for JSON merging at `scripts/install-codex-hooks.sh:90` through `scripts/install-codex-hooks.sh:92`, and requires Codex CLI to expose the `codex_hooks` feature at `scripts/install-codex-hooks.sh:75` through `scripts/install-codex-hooks.sh:82`.
  - Native hook install is skipped only by installer flags, not by the config template itself. Feature enabling can be disabled via `--skip-enable-feature` at `scripts/install-codex-hooks.sh:53` through `scripts/install-codex-hooks.sh:55`.

- dependencies_and_callers:
  - `scripts/lib/config-loader.sh` is the main consumer of `config/default_config.json`.
  - `hooks/lib/loop-common.sh` sources `config-loader.sh` and exposes config-backed defaults to hook validators, `loop-codex-stop-hook.sh`, setup scripts, cancel scripts, and related runtime code; its consumer list is documented at `hooks/lib/loop-common.sh:5` through `hooks/lib/loop-common.sh:13`.
  - `scripts/setup-rlcr-loop.sh` receives `DEFAULT_CODEX_MODEL`, `DEFAULT_CODEX_EFFORT`, and `DEFAULT_AGENT_TEAMS` from `loop-common.sh`, then initializes loop state defaults at `scripts/setup-rlcr-loop.sh:29` through `scripts/setup-rlcr-loop.sh:54`.
  - `scripts/bitlesson-select.sh` directly loads merged config, reads `bitlesson_model`, `codex_model`, and `provider_mode`, then selects Codex or Claude provider behavior at `scripts/bitlesson-select.sh:20` through `scripts/bitlesson-select.sh:26` and `scripts/bitlesson-select.sh:115` through `scripts/bitlesson-select.sh:130`.
  - `scripts/install-skill.sh` treats `config` as a required runtime-bundle component at `scripts/install-skill.sh:75` through `scripts/install-skill.sh:84`, copies it into installed runtimes at `scripts/install-skill.sh:155` through `scripts/install-skill.sh:164`, seeds Codex user config from installed defaults at `scripts/install-skill.sh:269` through `scripts/install-skill.sh:319`, and invokes `scripts/install-codex-hooks.sh` at `scripts/install-skill.sh:253` through `scripts/install-skill.sh:267`.
  - `scripts/install-codex-hooks.sh` is the main consumer of `config/codex-hooks.json`, binding the template to `${CODEX_HOME}/hooks.json`.

- edge_cases_or_failure_modes:
  - Missing `config/default_config.json` blocks merged config loading; tested as fatal.
  - Malformed user/project config does not block operation but warns and falls back to lower layers/defaults.
  - A higher-priority `null` does not erase a lower-priority default due to recursive `strip_nulls`.
  - `HUMANIZE_CONFIG` can redirect project config to a custom file path; if malformed, it is treated as malformed optional project config.
  - Invalid `codex_model` such as shell-unsafe strings or non-Codex provider names falls back to `gpt-5.4`. Invalid `codex_effort` falls back to `high`.
  - Existing `${CODEX_HOME}/hooks.json` must be a JSON object and must have a valid object-valued `hooks` field and list-valued `hooks.Stop`; invalid shapes fail in `scripts/install-codex-hooks.sh:120` through `scripts/install-codex-hooks.sh:136`.
  - Runtime roots with shell-sensitive characters are JSON-escaped before template parsing and command paths are shell-quoted after parsing at `scripts/install-codex-hooks.sh:105` through `scripts/install-codex-hooks.sh:118`.
  - Old managed Humanize Stop hooks are removed by regex, while unrelated Stop hooks and other lifecycle hook groups are preserved at `scripts/install-codex-hooks.sh:138` through `scripts/install-codex-hooks.sh:165`.
  - Codex builds without `codex_hooks` support cause install failure, not silent degradation, at `scripts/install-codex-hooks.sh:75` through `scripts/install-codex-hooks.sh:82`.

- validation_or_tests:
  - I validated both assigned JSON files with `jq empty config/codex-hooks.json config/default_config.json`; command exited successfully with no output.
  - `tests/test-config-merge.sh` covers default-only reads from `config/default_config.json`, project/user override priority, additive merge, null stripping, and `HUMANIZE_CONFIG` custom path at `tests/test-config-merge.sh:36` through `tests/test-config-merge.sh:200`.
  - `tests/test-config-error-handling.sh` covers missing default config as fatal, malformed optional user/project config warnings, empty project config, missing project config, and missing user config at `tests/test-config-error-handling.sh:36` through `tests/test-config-error-handling.sh:174`.
  - `tests/test-unified-codex-config.sh` asserts `default_config.json` contains `codex_model: gpt-5.4` and `codex_effort: high`, and that legacy reviewer keys are absent at `tests/test-unified-codex-config.sh:58` through `tests/test-unified-codex-config.sh:80`. It also tests invalid model/effort fallback warnings at `tests/test-unified-codex-config.sh:200` through `tests/test-unified-codex-config.sh:245`.
  - `tests/test-codex-hook-install.sh` covers Codex install writing hooks, enabling `codex_hooks`, seeding user config, preserving unrelated hooks, removing stale managed hooks, writing exactly one managed Humanize Stop hook, idempotency, and rejection of unsupported Codex builds at `tests/test-codex-hook-install.sh:110` through `tests/test-codex-hook-install.sh:334`.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `1`
- missing_items: `0`
- duplicate_items: `0`
- final_worker_status: `complete`