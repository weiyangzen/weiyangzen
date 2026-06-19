**Topic and conclusion**

Topic: BitLesson delta validation algorithm（`scripts/bitlesson-validate-delta.sh`）

结论：该算法是一个严格的 stop-gate 校验器。它从 round summary 中抽取一个“裸露”的 `## BitLesson Delta` 二级标题块，忽略代码围栏和 HTML 注释内的伪块，然后按 `Action` 将流程路由到 `none` 或 `add/update` 两条路径。通过条件是：结构存在、Action 唯一且合法、Action 与 Lesson ID 语义一致、`add/update` 有非占位 Notes、引用的 BitLesson 文件存在、ID 格式合法且已在知识库中登记。业务校验失败时输出 `{"decision":"block", ...}` 并以 `exit 0` 返回；参数/summary 文件前置错误则直接 `exit 1`。

**Algorithm subset covered**

覆盖范围只包括这三处与 delta validation 直接相关的内容：

- `scripts/bitlesson-validate-delta.sh`: 实际算法、状态变量、解析逻辑、门禁、阻断输出。
- `docs/bitlesson.md`: summary contract 与公开验证规则。
- `tests/test-bitlesson-validate-delta.sh`: 对 Notes、代码围栏、HTML 注释、正常通过路径的回归断言。

未覆盖安装、配置合并、模型选择、营销说明、截图、通用使用文本；`docs/bitlesson.md` 中 provider routing 不是 delta 校验算法的一部分，仅文档上下文。

**Pseudocode or transition table**

```text
inputs:
  SUMMARY_FILE
  BITLESSON_FILE
  BITLESSON_FILE_REL
  BITLESSON_ALLOW_EMPTY_NONE
  TEMPLATE_DIR
  CURRENT_ROUND

preflight:
  if unknown arg or missing required arg: print usage, exit 1
  if SUMMARY_FILE does not exist: error, exit 1
  source template-loader

block(reason, msg):
  output JSON:
    decision = "block"
    reason = rendered template/fallback
    systemMessage = msg
  exit 0

extract_delta(mode):
  state:
    in_delta = 0
    found_delta = 0
    in_fence = 0
    fence_delim = ""
    in_html_comment = 0

  for each summary line:
    if outside fence/comment and line matches case-insensitive exact:
       /^##[[:space:]]*bitlesson delta[[:space:]]*$/
       found_delta = 1
       in_delta = 1
       continue

    if in_delta and outside fence/comment and line matches /^##[[:space:]]+/:
       in_delta = 0

    if mode == extract and in_delta:
       print line

    update fence state for leading ``` or ~~~
    update HTML comment state for <!-- ... -->

  if mode == detect and not found_delta:
     exit 1

main:
  if detect_delta fails:
     block("missing BitLesson Delta section")

  delta = extract_delta()

  action_candidates =
    all lines in delta matching optional spaces/dash + "Action:" + alphabetic token
    lowercased

  if count(action_candidates) != 1 or action not in {none, add, update}:
     block("invalid action")

  ids_raw =
    first "Lesson ID(s): ..." value
    else first "Lesson IDs: ..." value
    trimmed

  ids_upper = uppercase(ids_raw)

  concrete_kb_count = 0
  if BITLESSON_FILE exists:
     count Lesson ID lines where id is:
       non-empty
       not "<BL-YYYYMMDD-short-name>"
       not "BL-YYYYMMDD-short-name"
       not any angle-bracket placeholder /^<.*>$/

  if action == none:
     if ids_raw is non-empty and ids_upper != "NONE":
        block("Action none inconsistent with IDs")

     if concrete_kb_count == 0 and BITLESSON_ALLOW_EMPTY_NONE != true:
        block("empty knowledge base cannot report none")

     pass

  else action in {add, update}:
     if ids_raw is empty or ids_upper == "NONE":
        block("add/update requires concrete IDs")

     notes =
       first "Notes: ..." value in delta, trimmed

     if notes empty or notes matches /^(\[.*\]|<.*>)$/:
        block("add/update requires non-placeholder Notes")

     if BITLESSON_FILE does not exist:
        block("BitLesson file missing")

     split ids_raw by comma

     for each trimmed lesson_id:
       skip empty tokens
       HAS_ANY_ID = true

       if lesson_id not match /^BL-[0-9]{8}-[A-Za-z0-9._-]+$/:
          add to INVALID_IDS
          continue

       if no exact "Lesson ID: lesson_id" entry in BITLESSON_FILE:
          add to MISSING_IDS

     if HAS_ANY_ID != true:
        block("no concrete lesson IDs")

     if INVALID_IDS non-empty:
        block("invalid Lesson ID format")

     if MISSING_IDS non-empty:
        block("IDs not found in knowledge base")

     pass

exit 0
```

Transition/routing summary:

| State/Gate | Condition | Next / output |
|---|---|---|
| Argument parse | unknown arg | usage + `exit 1` |
| Required args | any required input empty | usage + `exit 1` |
| Summary file | missing `SUMMARY_FILE` | error + `exit 1` |
| Delta detect | no valid naked `## BitLesson Delta` | block JSON |
| Action parse | not exactly one valid `none/add/update` | block JSON |
| `none` route | IDs present and not `NONE` | block JSON |
| `none` route | KB has 0 concrete entries and `allow-empty-none != true` | block JSON |
| `add/update` route | IDs empty or `NONE` | block JSON |
| `add/update` route | Notes empty or placeholder | block JSON |
| `add/update` route | BitLesson file missing | block JSON |
| `add/update` route | all ID tokens empty | block JSON |
| `add/update` route | invalid ID format | block JSON |
| `add/update` route | valid ID not found in KB | block JSON |
| Any valid route | all gates pass | no output, `exit 0` |

Scoring/routing rules: there is no numeric scoring. Routing is deterministic by `Action`: `none` takes the “no lesson change” validation path; `add` and `update` share the “concrete lesson evidence” path.

**Source evidence**

- Inputs and required arguments are explicit CLI flags: `--summary-file`, `--bitlesson-file`, `--bitlesson-relpath`, `--allow-empty-none`, `--template-dir`, `--current-round` in `scripts/bitlesson-validate-delta.sh:4-14`; variables are initialized at `scripts/bitlesson-validate-delta.sh:17-22`; argument parsing occurs at `scripts/bitlesson-validate-delta.sh:24-60`.
- Missing required arguments block execution with usage and `exit 1`: `scripts/bitlesson-validate-delta.sh:62-67`. Missing summary file is also a hard error with `exit 1`: `scripts/bitlesson-validate-delta.sh:69-72`.
- Business-rule failures use `block_exit`, which emits JSON with `"decision": "block"`, `"reason"`, and `"systemMessage"`, then exits 0: `scripts/bitlesson-validate-delta.sh:78-90`.
- Delta extraction uses AWK state variables `in_delta`, `found_delta`, `in_fence`, `fence_delim`, and `in_html_comment`: `scripts/bitlesson-validate-delta.sh:92-102`.
- Code fences are tracked only for lines starting with triple backticks or tildes, with matching delimiter close logic: `scripts/bitlesson-validate-delta.sh:104-131`.
- HTML comment state is ignored while inside a fence, starts on `<!--`, ends on `-->`, and supports multi-line comments: `scripts/bitlesson-validate-delta.sh:133-151`.
- A valid delta block heading must be outside fence/comment and match case-insensitive standalone `## BitLesson Delta`; extraction stops at the next outside-comment/fence level-2 heading: `scripts/bitlesson-validate-delta.sh:153-171`.
- Missing delta section is detected via `extract_bitlesson_delta_block detect`; failure emits a fallback explaining the required minimal format: `scripts/bitlesson-validate-delta.sh:181-198`.
- Action parsing collects matching `Action:` lines, lowercases them, counts non-empty candidates, and selects the first candidate: `scripts/bitlesson-validate-delta.sh:202-204`. The gate requires exactly one action and membership in `none/add/update`: `scripts/bitlesson-validate-delta.sh:206-218`.
- Lesson IDs are parsed from first `Lesson ID(s):` line, falling back to `Lesson IDs:`; value is trimmed and uppercased for `NONE` comparison: `scripts/bitlesson-validate-delta.sh:220-225`.
- Concrete KB entries are counted from `Lesson ID:` lines while excluding empty values and template placeholders: `scripts/bitlesson-validate-delta.sh:227-240`.
- `Action: none` requires empty ID field or `NONE`: `scripts/bitlesson-validate-delta.sh:242-252`. It can also be blocked when KB has no concrete lessons and `--allow-empty-none` is not `true`: `scripts/bitlesson-validate-delta.sh:254-267`.
- `Action: add/update` requires concrete IDs, not empty or `NONE`: `scripts/bitlesson-validate-delta.sh:268-279`.
- `add/update` requires `Notes:` to be present, trimmed non-empty, and not a whole-field placeholder like `[what changed and why]` or `<what changed and why>`: `scripts/bitlesson-validate-delta.sh:281-297`.
- `add/update` requires the BitLesson file to exist: `scripts/bitlesson-validate-delta.sh:299-310`.
- ID list is comma-split; each non-empty token must match `^BL-[0-9]{8}-[A-Za-z0-9._-]+$`: `scripts/bitlesson-validate-delta.sh:312-326`.
- Each valid ID must appear exactly as a trimmed `Lesson ID:` value in the BitLesson file: `scripts/bitlesson-validate-delta.sh:328-339`.
- Empty comma lists, invalid IDs, and missing KB entries each have separate block gates: `scripts/bitlesson-validate-delta.sh:342-384`.
- Successful validation reaches `exit 0` with no block output: `scripts/bitlesson-validate-delta.sh:385-387`.
- Public contract in documentation requires the block shape `## BitLesson Delta`, `Action`, `Lesson ID(s)`, and `Notes`: `docs/bitlesson.md:36-45`.
- Documentation states the strict rules: `none` must use `NONE` or empty IDs; `add/update` must reference concrete IDs in `.humanize/bitlesson.md`; `--require-bitlesson-entry-for-none` blocks repeated `none` on empty KBs: `docs/bitlesson.md:47-51`.
- Tests construct a valid BitLesson entry with `Lesson ID: BL-20260313-notes-validation`: `tests/test-bitlesson-validate-delta.sh:21-34`.
- Tests assert whitespace-only Notes blocks for `add`: `tests/test-bitlesson-validate-delta.sh:101-104`.
- Tests assert bracket and angle-bracket placeholder Notes block for `update`: `tests/test-bitlesson-validate-delta.sh:106-114`.
- Tests assert a delta section inside a fenced code block fails detection: `tests/test-bitlesson-validate-delta.sh:116-128`.
- Tests assert a delta section inside an HTML comment fails detection: `tests/test-bitlesson-validate-delta.sh:130-142`.
- Tests assert valid `add` and normal text `update` pass with no output: `tests/test-bitlesson-validate-delta.sh:144-152`.

**Edge cases and risks**

- Business-rule blocks exit with status 0. Callers must inspect stdout JSON, especially `.decision == "block"`, rather than treating non-zero exit as the only failure signal. Evidence: `block_exit` exits 0 after JSON output at `scripts/bitlesson-validate-delta.sh:78-90`.
- The delta heading must be a level-2 Markdown heading. `### BitLesson Delta`, headings with extra text, or headings inside quote/list contexts are not accepted by the AWK regex at `scripts/bitlesson-validate-delta.sh:153-158`.
- The heading is case-insensitive, but the label must otherwise be exact: `tolower($0) ~ /^##[[:space:]]*bitlesson delta[[:space:]]*$/` at `scripts/bitlesson-validate-delta.sh:153-155`.
- Fenced block detection only recognizes fence open/close at beginning of line via `^``` ` or `^~~~` patterns without leading indentation. Indented fences may not be treated as fences. Evidence: `scripts/bitlesson-validate-delta.sh:109-130`.
- HTML comment tracking is simple string-index state. It handles multi-line comments but does not parse nested or multiple comment segments per line as a full Markdown/HTML parser would. Evidence: `scripts/bitlesson-validate-delta.sh:133-151`.
- Multiple valid `Action:` lines inside the extracted block cause failure because `BITLESSON_ACTION_COUNT` must be exactly 1: `scripts/bitlesson-validate-delta.sh:202-218`.
- `Action:` extraction only accepts alphabetic action values due to `([A-Za-z]+)`. Values with punctuation or inline comments do not match and will likely cause invalid-action failure: `scripts/bitlesson-validate-delta.sh:202-206`.
- Only the first `Lesson ID(s):` or `Lesson IDs:` line is used because parsing pipes to `head -n1`: `scripts/bitlesson-validate-delta.sh:220-223`.
- ID list splitting is comma-only. Space-separated or semicolon-separated multiple IDs are treated as one invalid token or one missing ID: `scripts/bitlesson-validate-delta.sh:315-326`.
- Empty ID tokens in comma lists are skipped; a string like `, ,` eventually fails `HAS_ANY_ID`, while `valid-id, ,` can pass if the valid ID exists. Evidence: `scripts/bitlesson-validate-delta.sh:317-320` and `scripts/bitlesson-validate-delta.sh:342-352`.
- `Notes:` is required only for `add/update`, not for `none`. Evidence: Notes gate is inside the `else` branch for non-`none` actions at `scripts/bitlesson-validate-delta.sh:268-297`.
- Placeholder Notes detection is broad: any entire value wrapped in `[...]` or `<...>` is blocked, not only the documented placeholder string. Evidence: `NOTES_PLACEHOLDER_REGEX='^(\[.*\]|<.*>)$'` at `scripts/bitlesson-validate-delta.sh:283-285`.
- The algorithm validates that an ID exists in the BitLesson file, but does not prove that the file was changed in the current round. It trusts summary action semantics once the referenced ID exists. Evidence: existence check searches current `Lesson ID:` lines only at `scripts/bitlesson-validate-delta.sh:328-339`.

**What is explicitly out of scope**

- BitLesson selection/model routing is out of scope for this delta validator. `docs/bitlesson.md:5-24` describes configuration and provider routing, but the validator script does not use those rules.
- Initialization from `templates/bitlesson.md` and task/sub-task selection via `scripts/bitlesson-select.sh` are workflow context, not part of delta validation. Evidence: `docs/bitlesson.md:25-35`.
- The validator does not inspect git diffs, commit history, or whether a lesson was newly added versus merely pre-existing.
- The validator does not score lesson quality, semantic relevance, or whether Notes truly explain “what changed and why”; it only checks presence and placeholder shape.
- The validator does not parse full Markdown AST semantics. It uses line-oriented AWK/sed/regex gates for heading, fence, comment, action, IDs, and Notes.
- Installation, screenshots, marketing copy, generic CLI usage outside the required validator flags, and provider binary fallback behavior are outside this algorithm subset.