# agent_035 use-realpath4everything 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`

## Item Evidence

### USE_REALPATH4EVERYTHING-HZ-035 `file` `config/default_config.json`
- cursor: `[_]`
- core_role:
  - `config/default_config.json` is the required base/default configuration layer for Humanize runtime behavior. It is not executable algorithm code, but it participates in gates and routing by seeding the merged config object consumed by RLCR setup/hooks, BitLesson provider selection, plan-generation command behavior, and installer seeding.
  - The file defines six default keys: `codex_model`, `codex_effort`, `bitlesson_model`, `agent_teams`, `alternative_plan_language`, and `gen_plan_mode` at `config/default_config.json:2` through `config/default_config.json:7`.
  - It is a skip candidate only if "core algorithm" is interpreted as executable logic, but under the scheduler inclusion reason it is correctly in scope because it is a runtime configuration seed used by routing/gates.

- algorithmic_behavior:
  - The file itself has no functions or control flow. Its behavior is realized by `scripts/lib/config-loader.sh`, which requires it at `$plugin_root/config/default_config.json` during `load_merged_config` (`scripts/lib/config-loader.sh:77`, `scripts/lib/config-loader.sh:109`).
  - Merge semantics are four-layer and deterministic: empty `{}`, required defaults, optional user config, optional project config. Later layers override earlier layers after recursive null stripping (`scripts/lib/config-loader.sh:113` to `scripts/lib/config-loader.sh:132`).
  - `codex_model` and `codex_effort` become unified Codex defaults. `hooks/lib/loop-common.sh` reads them from the merged config, validates model shape/provider prefix and effort enum, then exports fallback-backed `DEFAULT_CODEX_MODEL` and `DEFAULT_CODEX_EFFORT` (`hooks/lib/loop-common.sh:211` to `hooks/lib/loop-common.sh:230`). `scripts/setup-rlcr-loop.sh` initializes `CODEX_MODEL` and `CODEX_EFFORT` from those runtime defaults (`scripts/setup-rlcr-loop.sh:43` to `scripts/setup-rlcr-loop.sh:44`).
  - `bitlesson_model` selects the BitLesson selector provider. `scripts/bitlesson-select.sh` reads merged `bitlesson_model`, falls back to `haiku`, reads `codex_model` as a Codex fallback model, and reads optional `provider_mode` (`scripts/bitlesson-select.sh:20` to `scripts/bitlesson-select.sh:26`). It then detects the provider from `BITLESSON_MODEL`, forces Codex when `provider_mode` is `codex-only`, and falls back to Codex if the configured provider binary is missing (`scripts/bitlesson-select.sh:115` to `scripts/bitlesson-select.sh:130`).
  - `agent_teams` is an RLCR setup default. `hooks/lib/loop-common.sh` reads the merged `agent_teams` key into `DEFAULT_AGENT_TEAMS` (`hooks/lib/loop-common.sh:232` to `hooks/lib/loop-common.sh:235`), and `scripts/setup-rlcr-loop.sh` initializes the state value from it (`scripts/setup-rlcr-loop.sh:53`).
  - `alternative_plan_language` and `gen_plan_mode` drive command-level planning behavior. `commands/gen-plan.md` requires the command to load config through `config-loader.sh` and extract both keys (`commands/gen-plan.md:62` to `commands/gen-plan.md:82`). It maps supported language names/codes to translated output variants and resolves `gen_plan_mode` with CLI flags taking precedence over config (`commands/gen-plan.md:89` to `commands/gen-plan.md:128`).
  - Installer behavior also depends on this file: Codex install seeding reads `codex_model` from the copied runtime default config to choose a Codex/OpenAI BitLesson default when user config lacks `bitlesson_model` (`scripts/install-skill.sh:269` to `scripts/install-skill.sh:320`).

- inputs_outputs_state:
  - Inputs:
    - Static JSON object from `config/default_config.json`.
    - Optional user config at `${XDG_CONFIG_HOME:-$HOME/.config}/humanize/config.json` (`scripts/lib/config-loader.sh:78` to `scripts/lib/config-loader.sh:82`).
    - Optional project config at `${HUMANIZE_CONFIG:-$project_root/.humanize/config.json}` (`scripts/lib/config-loader.sh:84` to `scripts/lib/config-loader.sh:88`).
    - Call-site overrides such as pre-set `DEFAULT_CODEX_MODEL`, `DEFAULT_CODEX_EFFORT`, `DEFAULT_AGENT_TEAMS`, or CLI flags like `--codex-model`, `--discussion`, and `--direct`.
  - Outputs:
    - `load_merged_config` prints merged JSON to stdout (`scripts/lib/config-loader.sh:135`).
    - `get_config_value` returns scalar values as strings, stringifies non-string values, and returns empty for absent or null keys (`scripts/lib/config-loader.sh:139` to `scripts/lib/config-loader.sh:158`).
    - Runtime defaults include `DEFAULT_CODEX_MODEL`, `DEFAULT_CODEX_EFFORT`, `DEFAULT_BITLESSON_MODEL`, and `DEFAULT_AGENT_TEAMS` in `hooks/lib/loop-common.sh` (`hooks/lib/loop-common.sh:204` to `hooks/lib/loop-common.sh:236`).
    - RLCR setup writes effective values into loop state; the state template includes `agent_teams: $AGENT_TEAMS` at `scripts/setup-rlcr-loop.sh:897` per search evidence, and related fields include `codex_model`/`codex_effort` in the same state-writing section.
  - State transitions:
    - The default JSON has no mutable state.
    - Runtime state transition is layered resolution: absent optional config means defaults survive; higher-layer non-null values override; higher-layer null values are stripped and therefore do not clear lower-layer defaults (`scripts/lib/config-loader.sh:119` to `scripts/lib/config-loader.sh:131`).
    - Invalid Codex config values transition to "ignored" at `loop-common.sh` level, restoring caller preset or hardcoded fallback instead of aborting (`hooks/lib/loop-common.sh:212` to `hooks/lib/loop-common.sh:230`).

- gates_or_invariants:
  - `config/default_config.json` is required. Missing required default config is fatal in `_config_loader_prepare_layer` (`scripts/lib/config-loader.sh:40` to `scripts/lib/config-loader.sh:47`), and malformed required config is fatal if it is not a JSON object (`scripts/lib/config-loader.sh:52` to `scripts/lib/config-loader.sh:55`).
  - `jq` is a hard dependency for config loading; absence causes a fatal error (`scripts/lib/config-loader.sh:17` to `scripts/lib/config-loader.sh:21`).
  - The required default config must be a JSON object, not an array/scalar (`scripts/lib/config-loader.sh:52`).
  - Optional malformed user/project config is ignored with warning and replaced by `{}` (`scripts/lib/config-loader.sh:52` to `scripts/lib/config-loader.sh:60`).
  - `codex_model` downstream invariant: shell-safe characters only, and model must start with `gpt-` or `o[0-9]`; otherwise it is ignored with warning (`hooks/lib/loop-common.sh:211` to `hooks/lib/loop-common.sh:222`).
  - `codex_effort` downstream invariant: one of `xhigh`, `high`, `medium`, `low`; otherwise ignored with warning (`hooks/lib/loop-common.sh:223` to `hooks/lib/loop-common.sh:230`).
  - `gen_plan_mode` downstream invariant in command spec: only `discussion` or `direct`, case-insensitive; invalid values fall back with warning (`commands/gen-plan.md:119` to `commands/gen-plan.md:125`).
  - `alternative_plan_language` downstream invariant in command spec: empty/absent/English disables variant; supported names or ISO codes enable a variant; unsupported values disable variant with warning (`commands/gen-plan.md:99` to `commands/gen-plan.md:128`).
  - `bitlesson_model` routing invariant is provider detection plus provider binary availability. Codex-only installs force the Codex path before provider resolution according to `docs/bitlesson.md:21` to `docs/bitlesson.md:23` and implementation at `scripts/bitlesson-select.sh:117` to `scripts/bitlesson-select.sh:120`.

- dependencies_and_callers:
  - Loader dependency: `scripts/lib/config-loader.sh` consumes this file as the required `default_config_path` (`scripts/lib/config-loader.sh:77`).
  - Shared hook dependency: `hooks/lib/loop-common.sh` sources `config-loader.sh`, resolves a real project root, then loads merged config best-effort when a project root exists (`hooks/lib/loop-common.sh:171` to `hooks/lib/loop-common.sh:202`).
  - RLCR setup caller: `scripts/setup-rlcr-loop.sh` sources `loop-common.sh`, then uses the config-backed defaults for Codex model/effort and agent teams (`scripts/setup-rlcr-loop.sh:29` to `scripts/setup-rlcr-loop.sh:33`, `scripts/setup-rlcr-loop.sh:43` to `scripts/setup-rlcr-loop.sh:53`).
  - BitLesson caller: `scripts/bitlesson-select.sh` calls `load_merged_config`, reads `bitlesson_model`, `codex_model`, and `provider_mode`, then routes to Codex or Claude (`scripts/bitlesson-select.sh:20` to `scripts/bitlesson-select.sh:33`, `scripts/bitlesson-select.sh:188` to `scripts/bitlesson-select.sh:217`).
  - Plan-generation command specs: `commands/gen-plan.md` and `commands/refine-plan.md` instruct command execution to load merged config for `alternative_plan_language` and `gen_plan_mode` rather than reading project config directly. Evidence for `gen-plan` is at `commands/gen-plan.md:62` to `commands/gen-plan.md:128`; `refine-plan` references were found in search at `commands/refine-plan.md:35`, `commands/refine-plan.md:104` to `commands/refine-plan.md:116`, and `commands/refine-plan.md:123` to `commands/refine-plan.md:153`.
  - Installer caller: `scripts/install-skill.sh` requires copied runtime `config/default_config.json` and uses its `codex_model` to seed Codex-friendly user config (`scripts/install-skill.sh:269` to `scripts/install-skill.sh:320`).
  - Documentation dependency: `docs/bitlesson.md` documents the config hierarchy with `config/default_config.json` as the first layer (`docs/bitlesson.md:5` to `docs/bitlesson.md:19`).

- edge_cases_or_failure_modes:
  - Missing default config fails `load_merged_config`; tests explicitly cover this as a non-zero exit (`tests/test-config-error-handling.sh:36` to `tests/test-config-error-handling.sh:53`).
  - Malformed optional project/user config warns and falls back to defaults, preserving `bitlesson_model=haiku` in tests (`tests/test-config-error-handling.sh:55` to `tests/test-config-error-handling.sh:110`).
  - Empty project config `{}` is valid and keeps all defaults (`tests/test-config-error-handling.sh:112` to `tests/test-config-error-handling.sh:128`).
  - Missing project config and missing optional user config are not fatal and use defaults (`tests/test-config-error-handling.sh:130` to `tests/test-config-error-handling.sh:172`).
  - Higher-layer null values do not clear defaults because `strip_nulls` removes them before merge; tested for `bitlesson_model: null` falling back to `haiku` (`scripts/lib/config-loader.sh:119` to `scripts/lib/config-loader.sh:131`, `tests/test-config-merge.sh:134` to `tests/test-config-merge.sh:150`).
  - Invalid but syntactically shell-safe `codex_model` values can exist in merged config, but `loop-common.sh` rejects non-Codex prefixes and falls back (`hooks/lib/loop-common.sh:216` to `hooks/lib/loop-common.sh:222`).
  - `bitlesson_model` defaults to `haiku`, which routes to Claude; on Codex-only installs, `provider_mode: "codex-only"` is written into user config to avoid that route and force Codex (`scripts/install-skill.sh:313` to `scripts/install-skill.sh:317`, `scripts/bitlesson-select.sh:117` to `scripts/bitlesson-select.sh:120`).
  - If `alternative_plan_language` remains the default empty string, translated plan generation is disabled; unsupported values also disable variant after warning (`commands/gen-plan.md:115` to `commands/gen-plan.md:128`).
  - Because `get_config_value` stringifies booleans, defaults like `agent_teams: false` are consumed downstream as the string `false`; tests assert this behavior in config merge defaults (`tests/test-config-merge.sh:52` to `tests/test-config-merge.sh:57`).

- validation_or_tests:
  - I inspected tests but did not run them, because the assignment requested read-only research notes only and these shell tests create temporary fixtures.
  - `tests/test-config-merge.sh` validates default-only values, project override, user/project priority, additive merging, null stripping, `HUMANIZE_CONFIG`, and all-layer behavior (`tests/test-config-merge.sh:35` to `tests/test-config-merge.sh:200`).
  - `tests/test-config-error-handling.sh` validates fatal missing default config and non-fatal optional config failures (`tests/test-config-error-handling.sh:36` to `tests/test-config-error-handling.sh:174`).
  - `tests/test-unified-codex-config.sh` asserts `default_config.json` contains `codex_model=gpt-5.4` and `codex_effort=high`, and asserts obsolete `loop_reviewer_*` keys are absent (`tests/test-unified-codex-config.sh:57` to `tests/test-unified-codex-config.sh:80`). It also validates default and project override merge behavior for Codex keys (`tests/test-unified-codex-config.sh:84` to `tests/test-unified-codex-config.sh:122`).
  - `tests/test-agent-teams.sh` includes coverage showing `agent_teams` defaults to false, can be enabled by project config, and affects generated continuation prompts; key references were found at `tests/test-agent-teams.sh:124` to `tests/test-agent-teams.sh:185` and `tests/test-agent-teams.sh:593` to `tests/test-agent-teams.sh:700`.
  - `tests/test-refine-plan.sh` includes assertions that `refine-plan.md` reads `alternative_plan_language` from config and ignores deprecated `chinese_plan`; search evidence shows this at `tests/test-refine-plan.sh:769` to `tests/test-refine-plan.sh:772`.
  - `tests/test-bitlesson-select-routing.sh` covers provider routing and fallback behavior for `bitlesson_model`, including `gpt-*`, `haiku`, Claude aliases, unknown model failure, missing binary fallback, and Codex-only provider mode; representative search hits show config writes around `tests/test-bitlesson-select-routing.sh:147`, `tests/test-bitlesson-select-routing.sh:203`, `tests/test-bitlesson-select-routing.sh:296`, `tests/test-bitlesson-select-routing.sh:349`, and `tests/test-bitlesson-select-routing.sh:396`.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `USE_REALPATH4EVERYTHING-HZ-035`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`