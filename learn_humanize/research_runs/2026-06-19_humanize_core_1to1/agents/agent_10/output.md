# agent_10 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 7
- source_commit: `0ec921a36b4365df503511c5567bbd3e02db0df5`

## Item Evidence

### HZ-010 `directory` `templates`
- cursor: `[_]`
- core_role: Seed template directory for reusable project knowledge. Recursive inspection found one file: `templates/bitlesson.md` at 687 bytes.
- algorithmic_behavior: `templates/bitlesson.md:1-23` defines the BitLesson knowledge base format. Its strict entry schema is algorithmically relevant because RLCR prompts require agents to read the BitLesson file, select lessons before tasks, and write a BitLesson Delta in round summaries. The schema fields at `templates/bitlesson.md:10-18` establish the durable lesson state: ID, scope, failure mode, root cause, solution, constraints, validation evidence, and source rounds.
- inputs_outputs_state: Input is human or agent-authored lesson entries appended below `templates/bitlesson.md:21-23`. Output is a project-specific knowledge base consumed by BitLesson selection and delta validation. State accumulates across rounds as entries are added or updated; the file starts empty except for the schema and insertion marker.
- gates_or_invariants: The invariant is the “exact field order” required by `templates/bitlesson.md:5-8`. Every entry must include validation evidence and source rounds, making lessons auditable rather than free-form notes.
- dependencies_and_callers: `scripts/setup-rlcr-loop.sh:1354-1367` injects BitLesson selection requirements into the round-0 prompt and references the BitLesson file. `hooks/loop-codex-stop-hook.sh:861-875` invokes `scripts/bitlesson-validate-delta.sh` before allowing non-finalize stop processing to continue.
- edge_cases_or_failure_modes: Empty `## Entries` is valid as an initial state but means selection can only return no applicable lessons. A malformed or reordered entry can weaken downstream selection/validation because the template is documentation-enforced rather than executable code in this directory.
- validation_or_tests: The directory itself has no executable validator. Related validation is performed by BitLesson delta checks in the stop hook and by BitLesson-specific tests outside this assigned directory.
- skip_candidate: `no`

### HZ-040 `file` `hooks/check-todos-from-transcript.py`
- cursor: `[_]`
- core_role: Fast stop-gate validator that blocks RLCR loop exit when Claude still has active work in either legacy TodoWrite transcript state or the newer file-backed Task system.
- algorithmic_behavior: It reads hook JSON from stdin, checks file-backed tasks first, then legacy transcript todos, and emits `INCOMPLETE_TODOS` plus details when blockers exist. `LANE_PREFIX_PATTERN` at `hooks/check-todos-from-transcript.py:24` recognizes only leading `[mainline]`, `[blocking]`, or `[queued]` tags. `classify_lane` at `hooks/check-todos-from-transcript.py:27-35` defaults untagged work to blocking for safety. `extract_tool_calls_from_entry` at `hooks/check-todos-from-transcript.py:38-70` supports assistant/message content blocks and direct tool-use entries.
- inputs_outputs_state: Inputs are `session_id`, optional `tasks_base_dir`, and optional `transcript_path` from hook JSON, parsed at `hooks/check-todos-from-transcript.py:173-199`. Outputs are exit code 0 for no blockers, exit code 1 with stdout task details for incomplete blockers, and exit code 2 with `PARSE_ERROR` on invalid hook JSON. It does not mutate state; it reads `~/.claude/tasks/<session_id>/*.json` or a test override at `hooks/check-todos-from-transcript.py:136-139`.
- gates_or_invariants: Legacy TodoWrite state uses only the most recent TodoWrite call, assigned at `hooks/check-todos-from-transcript.py:99-103`. Todo status must be exactly `completed` to pass; file-backed task status must be `completed` or `deleted` to pass at `hooks/check-todos-from-transcript.py:149-151`. Leading `[queued]` items are non-blocking and skipped at `hooks/check-todos-from-transcript.py:111-112` and `hooks/check-todos-from-transcript.py:157-158`; inline tags are intentionally ignored by the anchored regex.
- dependencies_and_callers: `hooks/loop-codex-stop-hook.sh:408-456` calls this script before expensive Codex review, converts exit code 2 into a parse-error block, and converts exit code 1 into an incomplete-task block using `prompt-template/block/incomplete-todos.md`. The hook is registered as the Stop hook through `hooks/hooks.json:63-70`.
- edge_cases_or_failure_modes: Empty stdin allows exit at `hooks/check-todos-from-transcript.py:177-179`. Missing transcript or task directory returns no blockers at `hooks/check-todos-from-transcript.py:79-80` and `hooks/check-todos-from-transcript.py:140-141`. Invalid JSONL transcript lines are ignored at `hooks/check-todos-from-transcript.py:91-95`. Malformed or unreadable task files are skipped at `hooks/check-todos-from-transcript.py:166-168`, which favors availability but can hide a blocker if a task file is corrupted.
- validation_or_tests: `tests/test-todo-checker.sh` covers invalid input, empty/missing inputs, completed vs pending/in-progress todos, queued lane bypass, inline tag non-bypass, file-backed tasks, deleted tasks, mixed sources, and missing session directories. Representative assertions are at `tests/test-todo-checker.sh:52-98`, `tests/test-todo-checker.sh:122-188`, and `tests/test-todo-checker.sh:340-536`.
- skip_candidate: `no`

### HZ-070 `file` `tests/test-ask-codex.sh`
- cursor: `[_]`
- core_role: Executable specification for `scripts/ask-codex.sh`, the one-shot Codex consultation path used by analyze-routed work.
- algorithmic_behavior: The test creates a mock Codex binary at `tests/test-ask-codex.sh:35-53`, runs the real script in a temp git project through `run_ask_codex` at `tests/test-ask-codex.sh:67-75`, and asserts CLI validation, artifact creation, error handling, concurrency behavior, cache logging, and skill guidance.
- inputs_outputs_state: Inputs are CLI args such as `--codex-model`, `--codex-timeout`, `--`, and question text, plus mock env vars declared at `tests/test-ask-codex.sh:6-9` and reset at `tests/test-ask-codex.sh:60-65`. Expected outputs are clean stdout response, stderr status/cache info, `.humanize/skill/<unique>/input.md`, `output.md`, `metadata.md`, and cache files under `$XDG_CACHE_HOME`.
- gates_or_invariants: Validation tests assert empty question, help, unknown flags, missing option values, nonnumeric timeout, and unsafe model/effort characters at `tests/test-ask-codex.sh:84-154`. The production script enforces those gates in `scripts/ask-codex.sh:89-186`. Successful runs must save `status: success` metadata and echo Codex stdout, asserted at `tests/test-ask-codex.sh:164-210`.
- dependencies_and_callers: Depends on `tests/test-helpers.sh` for temp repo and assertions, `scripts/ask-codex.sh`, `scripts/portable-timeout.sh`, `hooks/lib/loop-common.sh` for model defaults, and `skills/ask-codex/SKILL.md`. The ask-codex skill guidance is checked at `tests/test-ask-codex.sh:415-434` against `skills/ask-codex/SKILL.md:14-34`.
- edge_cases_or_failure_modes: Nonzero Codex exit must propagate and write `status: error` at `tests/test-ask-codex.sh:220-238`. Empty stdout exits 1 with `status: empty_response` at `tests/test-ask-codex.sh:241-257`. Timeout exit 124 emits timeout guidance and writes `status: timeout` at `tests/test-ask-codex.sh:259-276`. Concurrent calls must generate distinct project and cache directories at `tests/test-ask-codex.sh:286-320`, matching the unique ID logic in `scripts/ask-codex.sh:202-218`.
- validation_or_tests: This file is itself the validation asset. It also verifies implementation details in `scripts/ask-codex.sh:224-238` for input recording, `scripts/ask-codex.sh:262-276` for debug command capture, `scripts/ask-codex.sh:296-331` for timeout handling, and `scripts/ask-codex.sh:391-415` for output/metadata persistence.
- skip_candidate: `no`

### HZ-100 `file` `tests/test-task-tag-routing.sh`
- cursor: `[_]`
- core_role: Executable specification for RLCR task routing between Claude-owned coding tasks and Codex-owned analyze tasks.
- algorithmic_behavior: The test builds temporary RLCR projects, injects a plan table with `coding` and `analyze` task tags, and validates two transitions: setup-time round-0 prompt generation and stop-hook follow-up prompt generation. The first fixture is built at `tests/test-task-tag-routing.sh:75-95`; the stop-hook fixture is built at `tests/test-task-tag-routing.sh:121-224`.
- inputs_outputs_state: Inputs are plan markdown containing `Tag (coding/analyze)` and `Depends On` columns at `tests/test-task-tag-routing.sh:85-90` and `tests/test-task-tag-routing.sh:135-140`, plus mocked Codex review output at `tests/test-task-tag-routing.sh:214-220`. Outputs are `round-0-prompt.md`, `goal-tracker.md`, and then `round-1-prompt.md`.
- gates_or_invariants: Round-0 prompt must include `## Task Tag Routing (MUST FOLLOW)` and `/humanize:ask-codex`, asserted at `tests/test-task-tag-routing.sh:99-109`. Goal Tracker Active Tasks must include `Tag` and `Owner` columns, asserted at `tests/test-task-tag-routing.sh:111-115`. Follow-up prompts must preserve a routing reminder and ask-codex instruction, asserted at `tests/test-task-tag-routing.sh:227-237`.
- dependencies_and_callers: Production setup behavior is in `scripts/setup-rlcr-loop.sh:151-153`, which states `coding` tasks are direct and `analyze` tasks delegate via ask-codex. The normal Goal Tracker scaffold includes `Tag` and `Owner` columns at `scripts/setup-rlcr-loop.sh:1128-1132`. The round-0 prompt routing rules are generated at `scripts/setup-rlcr-loop.sh:1335-1342`. The stop hook appends follow-up reminders through `append_task_tag_routing_note` at `hooks/loop-codex-stop-hook.sh:1405-1418`.
- edge_cases_or_failure_modes: A task without an explicit tag defaults to coding per `scripts/setup-rlcr-loop.sh:1342`. The test’s mocked stop-hook review returns `CONTINUE`, so it exercises continuation prompt generation rather than completion/finalize behavior. It does not test malformed plan tag values or dependency-order enforcement.
- validation_or_tests: This file is the validation asset and exits via `print_test_summary` at `tests/test-task-tag-routing.sh:239`. It relies on `tests/test-helpers.sh:86-105` for temp repo setup.
- skip_candidate: `no`

### HZ-130 `file` `prompt-template/block/goal-tracker-not-initialized.md`
- cursor: `[_]`
- core_role: Stop-hook block template for the Round 0 Goal Tracker initialization gate.
- algorithmic_behavior: The template tells the agent it is in Round 0, names missing Goal Tracker sections through `{{MISSING_ITEMS}}`, and requires reading and updating `{{GOAL_TRACKER_FILE}}`. Required actions at `prompt-template/block/goal-tracker-not-initialized.md:8-14` force three initialization steps: define or extract the ultimate goal, define 3-7 testable acceptance criteria, and populate Active Tasks mapped to acceptance criteria.
- inputs_outputs_state: Inputs are rendered placeholders `GOAL_TRACKER_FILE` and `MISSING_ITEMS` at `prompt-template/block/goal-tracker-not-initialized.md:5-6`. Output is a JSON block reason emitted by the stop hook. The state transition is from an initialized-but-placeholder Goal Tracker to a usable Round 0 tracker whose immutable section is set.
- gates_or_invariants: The critical invariant is `prompt-template/block/goal-tracker-not-initialized.md:16`: the immutable section can only be set in Round 0 and becomes read-only afterward. The stop hook checks placeholders only when not finalize, not review-started, current round is 0, and the tracker exists at `hooks/loop-codex-stop-hook.sh:884-887`.
- dependencies_and_callers: `hooks/loop-codex-stop-hook.sh:893-935` extracts Ultimate Goal, Acceptance Criteria, and Active Tasks sections and builds missing-item bullets when placeholder text remains. It renders this template with `load_and_render_safe` at `hooks/loop-codex-stop-hook.sh:940-942`, then returns a block decision at `hooks/loop-codex-stop-hook.sh:944-952`.
- edge_cases_or_failure_modes: Placeholder detection looks for a generic `[To be ...]` pattern inside extracted sections, so non-placeholder missing content without that pattern may not trigger this exact template. The template assumes Round 0; later rounds rely on other goal-tracker immutability validators.
- validation_or_tests: Covered indirectly by stop-hook tests that exercise Round 0 initialization behavior and by the production stop-hook gate. No dedicated template-only test was inspected for this specific file.
- skip_candidate: `no`

### HZ-160 `file` `prompt-template/claude/goal-tracker-update-request.md`
- cursor: `[_]`
- core_role: Claude prompt snippet that provides a fallback protocol for requesting Goal Tracker reconciliation when direct mutable-section update is unsafe.
- algorithmic_behavior: The snippet defines an optional summary section headed `Goal Tracker Update Request` at `prompt-template/claude/goal-tracker-update-request.md:2-15`. It constrains the request to concrete requested changes and a justification tying the changes back to the Ultimate Goal. Example request classes include marking task evidence, adding blocking or queued side issues, plan evolution, and deferrals at `prompt-template/claude/goal-tracker-update-request.md:6-11`.
- inputs_outputs_state: Input is the agent’s final round summary when it cannot safely edit the mutable Goal Tracker directly. Output is structured reconciliation data for Codex to review. The intended state transition is not automatic; it queues a requested mutation to `goal-tracker.md` for Codex-mediated reconciliation.
- gates_or_invariants: The snippet explicitly limits itself to the mutable section at `prompt-template/claude/goal-tracker-update-request.md:2`, preserving the immutable-section gate. `prompt-template/claude/goal-tracker-update-request.md:17` states Codex will review and reconcile only if justified, so the request is advisory evidence rather than direct state mutation.
- dependencies_and_callers: `hooks/loop-codex-stop-hook.sh:2176-2181` loads and appends this template to the next prompt, with a fallback message if the template is missing. Related prompt guidance in `prompt-template/claude/next-round-prompt.md` tells Claude to keep the mutable tracker updated and include this request only if needed.
- edge_cases_or_failure_modes: Because the section is optional, missing it produces no reconciliation request. Vague requests without evidence may be ignored or rejected by Codex. It is not a validator and does not itself prevent unsafe edits; that is handled by write/edit/bash validators and stop-hook review.
- validation_or_tests: Indirectly validated by prompt-generation paths that append next-round instructions. No dedicated test was inspected that asserts this exact template body.
- skip_candidate: `no`

### HZ-190 `file` `tests/robustness/test-goal-tracker-robustness.sh`
- cursor: `[_]`
- core_role: Robustness specification for Goal Tracker parsing, which feeds monitoring and RLCR state summaries.
- algorithmic_behavior: The test sources `scripts/humanize.sh` at `tests/robustness/test-goal-tracker-robustness.sh:21-22`, then exercises `humanize_parse_goal_tracker` and `humanize_parse_goal_tracker_issue_counts`. It expects the main parser to return `total_acs|completed_acs|active_tasks|completed_tasks|deferred_tasks|open_issues|goal_summary`, documented at `tests/robustness/test-goal-tracker-robustness.sh:35-37`.
- inputs_outputs_state: Inputs are synthetic `goal-tracker.md` variants written under a temp directory. Outputs are pipe-delimited parser summaries split by helpers at `tests/robustness/test-goal-tracker-robustness.sh:39-61`, plus pass/fail assertions. No production state is modified.
- gates_or_invariants: Acceptance criteria are counted by unique AC identifiers inside the Acceptance Criteria section, matching `scripts/humanize.sh:87-93`. Active tasks are table rows minus completed and deferred statuses, matching `scripts/humanize.sh:95-123`. Completed task rows and unique completed ACs come from `scripts/humanize.sh:125-135`. Deferred tasks and issues come from `scripts/humanize.sh:137-144`.
- dependencies_and_callers: Depends on `tests/test-helpers.sh` and `scripts/humanize.sh`. The issue-count helper in `scripts/humanize.sh:38-67` separates Blocking Side Issues and Queued Side Issues, then falls back from legacy Open Issues to blocking for safety at `scripts/humanize.sh:60-64`.
- edge_cases_or_failure_modes: The test covers non-existent files, empty files, large AC counts, special characters, malformed headers, truncated markdown, binary bytes, open/deferred issues, only headers, mixed AC formats, and long goals across `tests/robustness/test-goal-tracker-robustness.sh:247-583`. One notable looseness: the mixed-format test comment says decimal ACs are not counted at `tests/robustness/test-goal-tracker-robustness.sh:553`, but production regex supports decimals at `scripts/humanize.sh:92`; the assertion only requires at least two, so the test tolerates either behavior.
- validation_or_tests: This file is itself the validation asset. Positive cases include list/table ACs, active task filtering, completed rows, unique completed ACs, and goal extraction at `tests/robustness/test-goal-tracker-robustness.sh:70-237`. Negative and robustness cases run through `tests/robustness/test-goal-tracker-robustness.sh:247-589`.
- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: 7 unique Item Evidence sections, one per assigned row
- missing_items: none
- duplicate_items: none
- final_worker_status: `complete`