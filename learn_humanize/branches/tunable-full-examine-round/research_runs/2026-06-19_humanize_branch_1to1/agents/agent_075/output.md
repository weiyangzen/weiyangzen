# agent_075 tunable-full-examine-round 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `67aa7bab09f0d0e36ac403264eed6989b09aada5`

## Item Evidence

### TUNABLE_FULL_EXAMINE_ROUND-HZ-075 `file` `prompt-template/block/claude-eyes-timeout.md`
- cursor: `[_]`
- core_role:
  - This file is a prompt/block template for a PR-loop blocking condition: Claude is configured for the PR loop, a fresh trigger comment has been confirmed, but Claude did not acknowledge the trigger with an `eyes` reaction.
  - The template provides the human/operator-facing reason text that is rendered into the stop hook’s JSON `reason` field when the Claude handshake gate fails.
  - The direct template content is short: title at `prompt-template/block/claude-eyes-timeout.md:1`, timeout sentence with placeholders at `prompt-template/block/claude-eyes-timeout.md:3`, possible causes at `prompt-template/block/claude-eyes-timeout.md:5`, required actions at `prompt-template/block/claude-eyes-timeout.md:10`, and restart instruction at `prompt-template/block/claude-eyes-timeout.md:18`.

- algorithmic_behavior:
  - The template itself is declarative Markdown, but it participates in an algorithmic gate in `hooks/pr-loop-stop-hook.sh`.
  - The gate is reached only after trigger validation, explicitly to avoid checking a stale trigger comment ID: see `hooks/pr-loop-stop-hook.sh:738` through `hooks/pr-loop-stop-hook.sh:747`.
  - The hook determines whether Claude is among configured bots by scanning `PR_CONFIGURED_BOTS_ARRAY` at `hooks/pr-loop-stop-hook.sh:749` through `hooks/pr-loop-stop-hook.sh:755`.
  - If Claude is configured and trigger validation requires a trigger, the hook uses `PR_TRIGGER_COMMENT_ID` as the confirmed trigger comment to check at `hooks/pr-loop-stop-hook.sh:757` through `hooks/pr-loop-stop-hook.sh:766`.
  - The reaction checker is invoked as `check-bot-reactions.sh claude-eyes ... --retry 3 --delay 5`, so the normal rendered values are `RETRY_COUNT=3` and `TOTAL_WAIT_SECONDS=15`; this is wired at `hooks/pr-loop-stop-hook.sh:764` through `hooks/pr-loop-stop-hook.sh:775`.
  - If no reaction is returned, `load_and_render_safe` renders this template and the hook emits JSON with `{"decision":"block"}` at `hooks/pr-loop-stop-hook.sh:774` through `hooks/pr-loop-stop-hook.sh:779`.
  - If an eyes reaction is found, the algorithm continues past the gate and prints confirmation instead of using this template at `hooks/pr-loop-stop-hook.sh:780` through `hooks/pr-loop-stop-hook.sh:782`.

- inputs_outputs_state:
  - Inputs to the template:
    - `{{RETRY_COUNT}}`, used in the timeout sentence at `prompt-template/block/claude-eyes-timeout.md:3`.
    - `{{TOTAL_WAIT_SECONDS}}`, also used at `prompt-template/block/claude-eyes-timeout.md:3`.
  - Runtime values supplied by caller:
    - `"RETRY_COUNT=3"` and `"TOTAL_WAIT_SECONDS=15"` at `hooks/pr-loop-stop-hook.sh:774` through `hooks/pr-loop-stop-hook.sh:775`.
  - Gate inputs around the caller:
    - Parsed PR-loop state fields include `configured_bots`, `active_bots`, `poll_timeout`, `last_trigger_at`, `trigger_comment_id`, `startup_case`, and latest commit fields; parsing starts at `hooks/pr-loop-stop-hook.sh:87` and includes `PR_TRIGGER_COMMENT_ID` at `hooks/pr-loop-stop-hook.sh:108`.
    - Current user and PR comments are used to detect the most recent bot-mention trigger comment from the current user; the detector returns `timestamp|comment_id` per `hooks/pr-loop-stop-hook.sh:523` through `hooks/pr-loop-stop-hook.sh:590`.
  - Output:
    - Rendered Markdown is assigned to `REASON`, then embedded into JSON as the `reason` field with `decision: block` and system message `PR Loop: Claude bot not responding - check bot configuration` at `hooks/pr-loop-stop-hook.sh:777` through `hooks/pr-loop-stop-hook.sh:778`.
  - State transition:
    - This block does not mutate repository or loop files itself.
    - Algorithmically, it prevents the PR loop from advancing to review/poll completion when the Claude bot does not acknowledge the trigger. The hook exits immediately after returning the block decision at `hooks/pr-loop-stop-hook.sh:779`.
    - It is a fail-closed transition: no eyes reaction means blocked, not skipped or accepted.

- gates_or_invariants:
  - The Claude eyes check is gated behind a confirmed trigger comment, not just stale state, per `hooks/pr-loop-stop-hook.sh:742` through `hooks/pr-loop-stop-hook.sh:747`.
  - The template is selected only when:
    - Claude is in `PR_CONFIGURED_BOTS_ARRAY`, `hooks/pr-loop-stop-hook.sh:749` through `hooks/pr-loop-stop-hook.sh:755`.
    - `REQUIRE_TRIGGER` is true, `hooks/pr-loop-stop-hook.sh:757`.
    - `PR_TRIGGER_COMMENT_ID` is non-empty, `hooks/pr-loop-stop-hook.sh:759` through `hooks/pr-loop-stop-hook.sh:761`.
    - `check-bot-reactions.sh` returns empty/null/failure for the reaction, `hooks/pr-loop-stop-hook.sh:766` through `hooks/pr-loop-stop-hook.sh:768`.
  - The reaction script invariant is specifically `user == "claude[bot]"` and `content == "eyes"` at `scripts/check-bot-reactions.sh:275` through `scripts/check-bot-reactions.sh:279`.
  - Retry behavior waits before each check, sleeps `RETRY_DELAY` seconds, and exhausts `MAX_RETRIES` before returning failure; see `scripts/check-bot-reactions.sh:259` through `scripts/check-bot-reactions.sh:295`.
  - Template rendering is single-pass and preserves unresolved placeholders rather than recursively expanding them; this is documented and implemented in `hooks/lib/template-loader.sh:50` through `hooks/lib/template-loader.sh:132`.
  - `load_and_render_safe` is the resilience gate: if the template is missing or renders empty, it emits the fallback message instead of an empty block reason; see `hooks/lib/template-loader.sh:167` through `hooks/lib/template-loader.sh:203`.

- dependencies_and_callers:
  - Direct caller:
    - `hooks/pr-loop-stop-hook.sh` calls `load_and_render_safe "$TEMPLATE_DIR" "block/claude-eyes-timeout.md"` at `hooks/pr-loop-stop-hook.sh:774`.
  - Template root:
    - `TEMPLATE_DIR` is set to the plugin’s `prompt-template` directory in `hooks/pr-loop-stop-hook.sh:57` per search result evidence.
  - Renderer:
    - `hooks/lib/template-loader.sh` provides `load_template`, `render_template`, and `load_and_render_safe`; the placeholder syntax is `{{VARIABLE_NAME}}` at `hooks/lib/template-loader.sh:7` through `hooks/lib/template-loader.sh:13`.
  - Reaction dependency:
    - `scripts/check-bot-reactions.sh` supports `claude-eyes <comment_id> [--retry <attempts>] [--delay <seconds>]` at `scripts/check-bot-reactions.sh:9` through `scripts/check-bot-reactions.sh:16`.
    - It uses GitHub CLI calls wrapped with `run_with_timeout`, resolves the PR base repository for fork support, and fetches comment reactions from `repos/$PR_BASE_REPO/issues/comments/$COMMENT_ID/reactions` at `scripts/check-bot-reactions.sh:229` through `scripts/check-bot-reactions.sh:270`.
  - External dependencies:
    - `gh` for GitHub API calls.
    - `jq` for filtering comments/reactions.
    - `scripts/portable-timeout.sh` via `run_with_timeout`, sourced by `scripts/check-bot-reactions.sh:31` through `scripts/check-bot-reactions.sh:33`.
  - Related trigger-detection caller context:
    - `detect_trigger_comment` fetches paginated issue comments from the base repo and filters comments by current user, configured bot mention pattern, and optional timestamp, at `hooks/pr-loop-stop-hook.sh:530` through `hooks/pr-loop-stop-hook.sh:590`.

- edge_cases_or_failure_modes:
  - Missing or empty template:
    - `load_and_render_safe` falls back to an inline fallback message defined at `hooks/pr-loop-stop-hook.sh:770` through `hooks/pr-loop-stop-hook.sh:773`; fallback rendering is handled at `hooks/lib/template-loader.sh:179` through `hooks/lib/template-loader.sh:186`.
  - Missing template variables:
    - The template renderer leaves unresolved placeholders intact if no variable is supplied, per `hooks/lib/template-loader.sh:12` through `hooks/lib/template-loader.sh:13` and implementation at `hooks/lib/template-loader.sh:115` through `hooks/lib/template-loader.sh:122`.
  - Stale trigger ID:
    - The eyes check intentionally runs after trigger validation and uses the confirmed `PR_TRIGGER_COMMENT_ID`; comments at `hooks/pr-loop-stop-hook.sh:742` through `hooks/pr-loop-stop-hook.sh:747` identify stale trigger avoidance as an invariant.
  - Trigger timestamp/ID mismatch:
    - If a trigger exists but no comment ID is available, the hook warns and does not render this template; see `hooks/pr-loop-stop-hook.sh:783` through `hooks/pr-loop-stop-hook.sh:786`.
  - Claude configured but no trigger required:
    - The hook skips eyes verification and logs that trigger is not required, at `hooks/pr-loop-stop-hook.sh:787` through `hooks/pr-loop-stop-hook.sh:789`.
  - GitHub API/reaction fetch failures:
    - In `check-bot-reactions.sh`, API failure during an attempt continues to the next retry at `scripts/check-bot-reactions.sh:268` through `scripts/check-bot-reactions.sh:272`; after all attempts, the script exits 1 at `scripts/check-bot-reactions.sh:293` through `scripts/check-bot-reactions.sh:295`, which causes this block template to be rendered by the stop hook.
  - Fork PRs:
    - Both trigger/reaction paths emphasize base-repository API usage for fork PR support: trigger comments at `hooks/pr-loop-stop-hook.sh:539` through `hooks/pr-loop-stop-hook.sh:543`, and comment reactions at `scripts/check-bot-reactions.sh:229` through `scripts/check-bot-reactions.sh:257`.
  - Timing nuance:
    - `check-bot-reactions.sh` sleeps before each attempt, not after the first failed immediate check, at `scripts/check-bot-reactions.sh:259` through `scripts/check-bot-reactions.sh:263`. With `3 x 5s`, total delay before failure is 15 seconds, matching the caller’s template variables.

- validation_or_tests:
  - Targeted behavior test:
    - `tests/test-pr-loop-stophook.sh` includes `test_stophook_claude_eyes_timeout` at `tests/test-pr-loop-stophook.sh:1011`.
    - The test constructs PR-loop state with Claude configured, `trigger_comment_id: 12345`, and `startup_case: 3` at `tests/test-pr-loop-stophook.sh:1016` through `tests/test-pr-loop-stophook.sh:1038`.
    - It mocks `gh` to return the trigger comment but no reactions at `tests/test-pr-loop-stophook.sh:1046` through `tests/test-pr-loop-stophook.sh:1081`.
    - It runs the stop hook under a 20-second wrapper because the eyes check waits 3 times for 5 seconds, at `tests/test-pr-loop-stophook.sh:1131` through `tests/test-pr-loop-stophook.sh:1133`.
    - It asserts the output contains eyes/not-responding/timeout/bot-configured language at `tests/test-pr-loop-stophook.sh:1135` through `tests/test-pr-loop-stophook.sh:1140`.
  - Template-loader tests:
    - `tests/test-template-loader.sh` and `tests/test-error-scenarios.sh` cover `load_and_render_safe` missing-template fallback and substitution behavior per search evidence around `tests/test-template-loader.sh:197` through `tests/test-template-loader.sh:221` and `tests/test-error-scenarios.sh:134` through `tests/test-error-scenarios.sh:157`.
  - Template reference validation gap:
    - `tests/test-template-references.sh` scans a fixed list of scripts at `tests/test-template-references.sh:56` through `tests/test-template-references.sh:64`; that list does not include `hooks/pr-loop-stop-hook.sh`.
    - Therefore this specific template reference is not guaranteed by that reference-validation script, even though the stop-hook behavior test exercises the path.
  - Comprehensive template validation:
    - Search evidence shows `tests/test-templates-comprehensive.sh` scans all Markdown templates under `prompt-template`, but the specific Claude-eyes timeout algorithm is validated primarily by `tests/test-pr-loop-stophook.sh`.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `TUNABLE_FULL_EXAMINE_ROUND-HZ-075`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`