# agent_25 do-not-wish-coding 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 6
- source_commit: `ac6cd9c180bcb9b84f6083fba1e458b4aab9ae14`

## Item Evidence

### DO_NOT_WISH_CODING-HZ-025 `file` `agents/bitlesson-selector.md`
- cursor: `[_]`
- core_role: Prompt/policy spec for selecting which `bitlesson.md` lessons apply to a task before execution. Frontmatter declares agent name, description, `haiku` model, and `Read, Grep` tools at `agents/bitlesson-selector.md:1-5`.
- algorithmic_behavior: Receives a task, related paths, and BitLesson content, then applies precision-first matching rules: select only directly relevant lessons, prefer precision over recall, and return `NONE` when no lesson is relevant at `agents/bitlesson-selector.md:12-30`.
- inputs_outputs_state: Inputs are current sub-task description, related file paths, and project `bitlesson.md` content at `agents/bitlesson-selector.md:12-18`. Output is exactly two stable lines: `LESSON_IDS:` and `RATIONALE:` at `agents/bitlesson-selector.md:32-41`. No persistent state is written by this prompt file.
- gates_or_invariants: Determinism and format stability are explicit cross-agent invariants so later Codex/Claude review can validate the selection quickly at `agents/bitlesson-selector.md:19-24`.
- dependencies_and_callers: The file documents runtime execution through `scripts/bitlesson-select.sh`, which routes to Codex for `gpt-*` models and Claude for `haiku`, `sonnet`, or `opus` at `agents/bitlesson-selector.md:21-23`. Related workflow prompts require running `bitlesson-selector`, including `prompt-template/claude/agent-teams-core.md:23` and `commands/start-rlcr-loop.md:167`.
- edge_cases_or_failure_modes: The prompt itself cannot validate malformed model output; enforcement is in `scripts/bitlesson-select.sh`, which extracts the first matching `LESSON_IDS` and `RATIONALE` lines and errors if either is missing at `scripts/bitlesson-select.sh:197-219`.
- validation_or_tests: Output contract is enforced by `scripts/bitlesson-select.sh:221-222`. Routing and mocked selector output are covered by `tests/test-bitlesson-select-routing.sh` according to repository references.
- skip_candidate: `no`

### DO_NOT_WISH_CODING-HZ-055 `file` `scripts/fetch-pr-comments.sh`
- cursor: `[_]`
- core_role: Runtime PR-loop ingestion script that fetches GitHub PR comments from all relevant PR surfaces and emits a normalized markdown review input file. The script states it covers issue comments, inline review comments, and PR reviews at `scripts/fetch-pr-comments.sh:3-13`.
- algorithmic_behavior: Parses `<pr_number> <output_file>` plus `--after` and `--bots`; resolves the correct base repo for fork PRs; fetches three GitHub API endpoints with retries; converts each JSON payload to a shared object shape; deduplicates, optionally filters by timestamp, sorts humans before bots/newest first, and writes markdown sections at `scripts/fetch-pr-comments.sh:27-90`, `130-220`, `260-343`, and `345-443`.
- inputs_outputs_state: Inputs are PR number, output path, optional ISO timestamp, optional active bot list, GitHub CLI repo context, and API responses. Output is a markdown file headed with PR number, fetch time, repository, human comments, bot comments, end marker, and optional warning at `scripts/fetch-pr-comments.sh:245-254` and `440-450`. Temporary JSON state lives under `mktemp -d` and is removed by trap at `scripts/fetch-pr-comments.sh:168-174`.
- gates_or_invariants: Requires non-empty numeric PR number, non-empty output path, `gh`, `jq`, resolvable current or parent repo, and parseable owner/name at `scripts/fetch-pr-comments.sh:92-120` and `130-162`. API endpoint failure is nonfatal after three retries but increments `API_FAILURES` and produces warning state at `scripts/fetch-pr-comments.sh:176-208` and `445-450`.
- dependencies_and_callers: Depends on `gh api --paginate`, `gh repo view`, `gh pr view`, `jq`, `mktemp`, `date`, `sed`, and shell utilities. `scripts/setup-pr-loop.sh` calls it to create `round-0-pr-comment.md` and pass active bot grouping at `scripts/setup-pr-loop.sh:425-431`; later startup logic treats the exact `*No comments found.*` sentinel as zero-comment state at `scripts/setup-pr-loop.sh:723-729`.
- edge_cases_or_failure_modes: Fork PRs are handled by checking current repo then parent repo at `scripts/fetch-pr-comments.sh:136-149`. Empty review bodies become `[Review state: STATE]` so approval-only reviews are not lost at `scripts/fetch-pr-comments.sh:300-320`. Entries with null `created_at` are dropped before sorting at `scripts/fetch-pr-comments.sh:334-343`. `--after` uses string comparison without validating timestamp format at `scripts/fetch-pr-comments.sh:326-332`. Active bot mapping special-cases `codex` to `chatgpt-codex-connector[bot]`; other names become `<bot>[bot]` at `scripts/fetch-pr-comments.sh:381-401`.
- validation_or_tests: Help and missing-argument behavior are covered by `tests/test-pr-loop-scripts.sh:256-290`. Fixture tests assert all comment types and approval-only placeholder output at `tests/test-pr-loop-hooks.sh:1242-1283`, and `--after` filtering at `tests/test-pr-loop-hooks.sh:1287-1318`. Robustness tests cover empty arrays, rate-limit warnings, and network errors at `tests/robustness/test-pr-loop-api-robustness.sh:362-430`.
- skip_candidate: `no`

### DO_NOT_WISH_CODING-HZ-085 `file` `tests/test-monitor-e2e-deletion.sh`
- cursor: `[_]`
- core_role: Executable split test runner for monitor deletion behavior, specifically “parallel split 1/3” of monitor E2E deletion coverage at `tests/test-monitor-e2e-deletion.sh:1-5`.
- algorithmic_behavior: Sources the real monitor E2E test implementation, prints a suite banner, runs bash deletion, zsh deletion, and PR-loop deletion test functions, then exits according to the shared failure counter at `tests/test-monitor-e2e-deletion.sh:4-22`.
- inputs_outputs_state: Inputs are the sourced `tests/test-monitor-e2e-real.sh` functions and global counters. Outputs are stdout banners, pass/fail counts, and process exit status. The wrapper itself mutates only sourced shell variables `TESTS_PASSED` and `TESTS_FAILED` through called functions.
- gates_or_invariants: Uses `set -euo pipefail`, so missing source file, undefined functions, or unexpected command failures stop the runner at `tests/test-monitor-e2e-deletion.sh:3-14`. Final invariant is zero failures for exit 0 at `tests/test-monitor-e2e-deletion.sh:20-22`.
- dependencies_and_callers: Depends on `tests/test-monitor-e2e-real.sh`, where the called functions are defined: `monitor_test_bash_deletion` at `tests/test-monitor-e2e-real.sh:56`, `monitor_test_zsh_deletion` at `tests/test-monitor-e2e-real.sh:233`, and `monitor_test_pr_deletion` at `tests/test-monitor-e2e-real.sh:691`. Included in the aggregate runner at `tests/run-all-tests.sh:79`.
- edge_cases_or_failure_modes: If `zsh` is absent, the underlying zsh test prints `SKIP: zsh not available` instead of incrementing a failure counter at `tests/test-monitor-e2e-real.sh:238-240`. If deletion handling regresses, the sourced tests check for graceful exit, no shell glob errors, and restored terminal behavior as described in `tests/test-monitor-e2e-real.sh:8-12`.
- validation_or_tests: This file is itself validation. It exercises real monitor functions rather than stubs, per `tests/test-monitor-e2e-real.sh:3-6`.
- skip_candidate: `no`

### DO_NOT_WISH_CODING-HZ-115 `file` `prompt-template/block/bitlesson-delta-invalid.md`
- cursor: `[_]`
- core_role: Block-message template for the BitLesson Delta validation gate when a summary has an invalid or ambiguous `Action` field.
- algorithmic_behavior: Emits a concise markdown stop reason saying the `## BitLesson Delta` section exists but must include exactly one action from `none`, `add`, or `update` at `prompt-template/block/bitlesson-delta-invalid.md:1-7`.
- inputs_outputs_state: Has no template variables and no state. Input is only selection by the validator; output is static markdown text.
- gates_or_invariants: The corresponding validator requires exactly one parsed action and restricts it to `none`, `add`, or `update` at `scripts/bitlesson-validate-delta.sh:118-123`.
- dependencies_and_callers: Loaded through `load_and_render_safe` by `scripts/bitlesson-validate-delta.sh` when action count or value fails validation at `scripts/bitlesson-validate-delta.sh:122-133`.
- edge_cases_or_failure_modes: Because the template is static, it does not echo the invalid value or duplicate count. The JSON block response still includes contextual round information in `systemMessage` from the caller at `scripts/bitlesson-validate-delta.sh:132-133`.
- validation_or_tests: Covered indirectly by the delta validator path. The assigned template’s exact allowed-action list must stay aligned with the shell condition at `scripts/bitlesson-validate-delta.sh:122`.
- skip_candidate: `no`

### DO_NOT_WISH_CODING-HZ-145 `file` `prompt-template/block/wrong-directory-path.md`
- cursor: `[_]`
- core_role: Block-message template for hook validation when an agent tries to read or write a loop file outside the current active loop directory/path.
- algorithmic_behavior: Renders the attempted action and file path, shows the correct path, and gives a follow-up command hint at `prompt-template/block/wrong-directory-path.md:1-6`.
- inputs_outputs_state: Inputs are `ACTION`, `FILE_PATH`, and `CORRECT_PATH`. Output is markdown. No persistent state is changed by the template itself.
- gates_or_invariants: The read hook computes `CORRECT_PATH="$ACTIVE_LOOP_DIR/$CLAUDE_FILENAME"` and blocks unless the requested path matches exactly at `hooks/loop-read-validator.sh:153-167`. The write hook applies the same exact-path invariant at `hooks/loop-write-validator.sh:250-264`.
- dependencies_and_callers: Rendered through `load_and_render_safe` by `hooks/loop-read-validator.sh:163` with `ACTION=read` and by `hooks/loop-write-validator.sh:260` with `ACTION=write to`.
- edge_cases_or_failure_modes: The final hint says `cat {{FILE_PATH}}` rather than `cat {{CORRECT_PATH}}` at `prompt-template/block/wrong-directory-path.md:6`, which can be misleading after a wrong-path rejection. For write failures, the `cat` hint is read-oriented even though `ACTION` may be `write to`.
- validation_or_tests: Validated indirectly through read/write hook behavior; the hooks exit with code 2 after rendering this block at `hooks/loop-read-validator.sh:163-167` and `hooks/loop-write-validator.sh:260-264`.
- skip_candidate: `no`

### DO_NOT_WISH_CODING-HZ-175 `file` `scripts/lib/model-router.sh`
- cursor: `[_]`
- core_role: Shared shell library for routing configured model names to agent providers, checking provider binaries, and normalizing reasoning effort values.
- algorithmic_behavior: Uses a source guard, then defines `detect_provider`, `check_provider_dependency`, and `map_effort` at `scripts/lib/model-router.sh:6-91`. `detect_provider` routes `gpt-*` and `o[0-9]*` to `codex`, Claude-prefixed or family-name models to `claude`, and rejects unknown or empty names at `scripts/lib/model-router.sh:10-30`.
- inputs_outputs_state: Inputs are model name, provider name, and effort string. Outputs are provider strings, mapped effort strings, or stderr errors with nonzero return. State is limited to `_MODEL_ROUTER_LOADED=1` to prevent double-sourcing at `scripts/lib/model-router.sh:6-8`.
- gates_or_invariants: `check_provider_dependency` accepts only `codex` or `claude`, maps to required binary names, uses `command -v`, and emits install guidance on failure at `scripts/lib/model-router.sh:32-60`. `map_effort` accepts only provider `codex|claude` and effort `xhigh|high|medium|low`; `xhigh` maps to `high` only for Claude at `scripts/lib/model-router.sh:62-90`.
- dependencies_and_callers: Used by `scripts/bitlesson-select.sh`, which sources this library at `scripts/bitlesson-select.sh:9-12`, detects the BitLesson provider at `scripts/bitlesson-select.sh:85-90`, checks provider dependencies with fallback to Codex at `scripts/bitlesson-select.sh:91-100`, then invokes either Codex or Claude at `scripts/bitlesson-select.sh:167-181`.
- edge_cases_or_failure_modes: `claude` alone does not match unless it is `claude-*` or contains `haiku`, `sonnet`, or `opus`. The Claude regex can also match any non-Claude string containing those family words. Future `o` models route broadly because any `o` followed by a digit matches. Missing binaries are hard failures unless the caller implements fallback, as `bitlesson-select.sh` does.
- validation_or_tests: `tests/test-model-router.sh` loads the library at `tests/test-model-router.sh:5-8`, verifies `gpt-*` and `o*` Codex routing at `tests/test-model-router.sh:37-108`, and verifies effort mapping/error behavior at `tests/test-model-router.sh:311-420`.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 6/6 Item Evidence sections present, one per assigned row
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`