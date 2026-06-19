**Topic and Conclusion**

Topic: `Gen-idea` 多候选创意生成算法。

结论：该机制是一个“先定向发散、再并行证据探索、最后按证据密度合成”的 draft-only 管线。核心不是直接产出实现方案，而是把一个松散 idea 转换成一个 repo-grounded idea draft：先生成 `N` 个正交方向，再为每个方向并行启动只读 `Explore` 子代理，收集结构化 proposal，丢弃降级项，最后按证据密度、既有模式契合度、实现面大小、置信度选择 primary，并将剩余方向作为 alternatives 写入模板。

**Algorithm Subset Covered**

覆盖文件：

- `commands/gen-idea.md`
- `prompt-template/idea/gen-idea-template.md`
- `scripts/validate-gen-idea-io.sh`

覆盖算法面：

- 输入解析与 IO validation。
- `N` 个正交方向生成与降级规则。
- 并行 `Explore` 子代理调度、证据收集、proposal 结构校验。
- primary 选择规则与 alternatives 编号。
- 模板填充、单次写入、失败不产出 partial output。
- validation 脚本中的路径判定、slug/output/template/N 约束。

未覆盖安装、营销、截图、普通用法说明，除非它们定义行为。

**Pseudocode**

```text
INPUT: $ARGUMENTS = <idea-text-or-path> [--n int] [--output path]

Phase 0:
  parse first positional as IDEA_INPUT
  parse --n as N, default 6
  parse --output as OUTPUT_FILE, optional
  do not rewrite idea text

Phase 1:
  result = validate-gen-idea-io.sh($ARGUMENTS)
  if exit != 0:
    map exit code to user-facing error
    stop without output

  extract INPUT_MODE, OUTPUT_FILE, SLUG, TEMPLATE_FILE, N
  if INPUT_MODE == file:
    read IDEA_BODY from IDEA_BODY_FILE
  else:
    read IDEA_BODY from stdout sentinel block
  preserve IDEA_BODY byte-identically

Phase 2:
  read grounding context: README.md, optional CLAUDE files, top-level dirs
  generate exactly N DIRECTIONS = [{name, rationale}]
  enforce orthogonality:
    replace duplicates
    replace vague "do X better" entries
    reject restatements of original idea

  if count < N:
    retry once with explicit N requirement
  if second count < N and count >= 2:
    warn and continue with reduced count
  if count < 2:
    stop without output

Phase 3:
  dispatch one Explore subagent per direction in a single Task-tool message
  each subagent receives:
    IDEA_BODY verbatim
    assigned direction
    read-only evidence-gathering instructions

  for each response:
    require APPROACH_SUMMARY
    require OBJECTIVE_EVIDENCE
    require KNOWN_RISKS
    require CONFIDENCE in {high, medium, low}
    if missing field: drop proposal as degraded

  if surviving proposals < 2:
    stop without output
  preserve direction association for survivors

Phase 4:
  choose PRIMARY by ordered criteria:
    1. evidence density
    2. fit with existing repo patterns
    3. smaller implementation surface
    4. CONFIDENCE high > medium > low as tiebreaker

  alternatives = surviving non-primary proposals
  number alternatives Alt-1..Alt-K in original direction order without gaps

  infer 4-10 word Title Case title from primary direction
  read TEMPLATE_FILE
  replace placeholders, preserving ORIGINAL_IDEA byte-identically
  write finalized draft to OUTPUT_FILE once
  report path, primary name, requested N, actual count, gen-plan hint
```

**State Variables**

- `IDEA_INPUT`: first positional argument, either inline text or candidate `.md` path.
- `N`: requested direction count; default `6`; validation range `2..10`.
- `OUTPUT_FILE`: user path or default `.humanize/ideas/<slug>-<timestamp>.md`.
- `INPUT_MODE`: `inline` or `file`.
- `IDEA_BODY_FILE`: only present for file mode.
- `IDEA_BODY`: authoritative idea content; must be preserved byte-identically after Phase 1.
- `SLUG`: derived from file basename or inline text; informational after validation.
- `TEMPLATE_FILE`: resolved template path.
- `DIRECTIONS`: ordered direction list, index `0..len-1`.
- `PROPOSALS`: subagent results associated with origin direction.
- `SURVIVORS`: proposals that contain all required fields.
- `PRIMARY`: selected strongest surviving proposal.
- `ALT-1..ALT-K`: non-primary survivors, renumbered without gaps.
- `WARNINGS`: validation short-idea warnings and direction-count degradation warnings.

**Transition Table**

| Phase | Gate | Pass Transition | Fail Transition |
|---|---|---|---|
| 0 Parse | first positional exists syntactically | pass raw `$ARGUMENTS` to validator | validator handles missing input |
| 1 Validate | script exit code `0` | extract keys and load `IDEA_BODY` | map exit `1..7` to stop message |
| 2 Directions | exactly `N` orthogonal entries | store `DIRECTIONS` | retry once if `< N`; stop if final `< 2` |
| 3 Explore | one valid structured response per direction preferred | drop degraded responses, continue if survivors `>= 2` | stop if survivors `< 2` |
| 4 Select | proposals survive | pick primary by scoring/routing rules | no write if earlier phase failed |
| 4 Write | template populated in memory | single write to `OUTPUT_FILE` | no progressive or partial writes |

**Scoring And Routing Rules**

- Direction generation route: produce exactly `N` entries, each with `name` and `rationale`; `name` is 2-5 words and `rationale` is one sentence.
- Orthogonality gate: near-duplicates, vague “just do X better” directions, and restatements of the input must be replaced.
- Exploration route: one `Explore` subagent per direction, all launched in a single Task-tool message.
- Proposal validity gate: response must parse four fields: `APPROACH_SUMMARY`, `OBJECTIVE_EVIDENCE`, `KNOWN_RISKS`, `CONFIDENCE`; missing field means drop.
- Primary scoring order:
  1. More concrete repo evidence wins.
  2. Extending existing repo patterns beats unfamiliar paradigms.
  3. Smaller implementation surface wins when quality is comparable.
  4. `CONFIDENCE`: `high > medium > low` only as tiebreaker.
- Alternative routing: non-primary survivors are numbered `Alt-1..Alt-K` sequentially in original direction order, with dropped proposal gaps removed.

**Source Evidence**

- Draft-only invariant and write boundary: `commands/gen-idea.md:17-21` says the command must not implement features, modify source, or commit; permitted writes are limited to the single output draft file, and subagents are read-only.
- Sequential phase invariant: `commands/gen-idea.md:23-31` defines strict phase order: Parse Input, IO Validation, Direction Generation, Parallel Exploration, Synthesis and Write.
- Input parse contract: `commands/gen-idea.md:35-42` defines first positional input, `--n`, `--output`, and says not to interpret or rewrite idea text in Phase 0.
- Validation output contract and stop conditions: `commands/gen-idea.md:46-63` maps validator exit codes `0..7`, extracts `INPUT_MODE`, `OUTPUT_FILE`, `SLUG`, `TEMPLATE_FILE`, `N`, and treats `WARNING:` as informational.
- Idea body authority: `commands/gen-idea.md:65-69` defines inline sentinel extraction vs file read and requires byte-identical preservation.
- Context grounding: `commands/gen-idea.md:77-85` requires reading `README.md`, optional `CLAUDE.md`, optional `.claude/CLAUDE.md`, and top-level directory listing before direction generation.
- Direction shape and orthogonality: `commands/gen-idea.md:87-97` requires exactly `N` direction entries with `name` and `rationale`, plus duplicate/restatement replacement.
- Direction degradation: `commands/gen-idea.md:98-104` defines retry-once, reduced-count warning when `>=2`, and hard stop when `<2`.
- Parallel swarm dispatch: `commands/gen-idea.md:108-114` requires all directions dispatched in a single Task-tool message, one `Explore` subagent per direction.
- Subagent prompt contract: `commands/gen-idea.md:116-133` requires verbatim `IDEA_BODY`, assigned direction, objective evidence, read-only behavior, no fabrication, sentinel for no precedent, and exact fields.
- Proposal collection gate: `commands/gen-idea.md:135-143` says missing fields mark a proposal degraded and dropped; fewer than two survivors stops; survivors retain origin direction and alternatives are renumbered without gaps.
- Primary scoring: `commands/gen-idea.md:148-156` defines selection by evidence density, repo pattern fit, implementation surface, and confidence tiebreaker.
- Template population rules: `commands/gen-idea.md:158-187` defines title inference, placeholder replacement, byte-identical original idea preservation, evidence rendering, alternatives format, and synthesis notes.
- Single write/report: `commands/gen-idea.md:189-199` requires one write to `OUTPUT_FILE` and reports path, primary, requested/actual `N`, and next-step command.
- Global error invariant: `commands/gen-idea.md:203-209` says validation/degradation errors stop, references must not be fabricated, sentinel preserved, and partial output must not be written.
- Template placeholders: `prompt-template/idea/gen-idea-template.md:1-31` defines the final draft skeleton: title, original idea, primary direction, rationale, approach, evidence, risks, alternatives, synthesis notes.
- Validator exit codes: `scripts/validate-gen-idea-io.sh:4-12` defines failure classes for missing input, path/file issues, output dir, existing output, permission, invalid args, and missing template.
- CLI arguments and `N` range: `scripts/validate-gen-idea-io.sh:16-24` documents default `N=6`, range `2-10`, and default output shape.
- Argument parser: `scripts/validate-gen-idea-io.sh:31-66` accepts only one positional input plus `--n` and `--output`; unknown or extra args exit as invalid.
- Missing input and `N` validation: `scripts/validate-gen-idea-io.sh:68-83` rejects empty input, non-numeric `N`, and `N` outside `2..10`.
- Path-vs-inline heuristic: `scripts/validate-gen-idea-io.sh:89-101` treats whitespace-free strings ending `.md` or containing `/` as path-like if no file exists; whitespace disqualifies path mode.
- File-mode gates: `scripts/validate-gen-idea-io.sh:103-122` requires existing `.md`, readable, non-empty file; sets `INPUT_MODE=file`, `IDEA_BODY_FILE`, and slug from basename.
- Inline-mode behavior: `scripts/validate-gen-idea-io.sh:123-140` emits input-not-found for path-like missing input, otherwise uses inline mode, warns if under 10 chars, and derives slug from normalized first 40 bytes.
- Output path gates: `scripts/validate-gen-idea-io.sh:142-174` resolves project root, creates default output dir only for default output, rejects missing user output dir, existing file, and non-writable dir.
- Template resolution and success payload: `scripts/validate-gen-idea-io.sh:176-202` resolves `TEMPLATE_FILE`, rejects missing template, prints success keys, and emits inline body between sentinel markers.

**Edge Cases And Risks**

- Missing or empty idea input stops before generation; empty file input exits as missing/empty idea, not as path error.
- Inline idea shorter than 10 characters only warns; it still proceeds.
- A non-existing path with whitespace is treated as inline by design, so `"my idea.md"` can silently become idea text rather than `INPUT_NOT_FOUND`.
- A string like `rename README.md` contains whitespace, so it is intentionally inline, not path mode.
- Only `.md` file inputs are accepted; readable non-`.md` files are rejected.
- `--n` is constrained to `2..10`; Phase 2 can degrade below requested `N` but never below 2.
- If direction generation returns one usable direction after retry, the command stops; no draft is written.
- If subagents omit any required proposal field, those proposals are dropped; if fewer than two remain, the command stops.
- Evidence fabrication is explicitly forbidden; when no concrete precedent exists, the algorithm must use the literal sentinel `exploratory, no concrete precedent`.
- Primary selection is deterministic only by stated criteria; “evidence density” and “fit” require lead judgment and are not numerically scored.
- Alternatives can be fewer than `N-1` after degradation or dropped proposals; numbering must be compact and gapless.
- User-supplied output directories are not auto-created; only default `.humanize/ideas/` may be created by validation.
- Existing output files are never overwritten.
- If any phase fails, partial output must not be written.

**What Is Explicitly Out Of Scope**

- Implementing the idea, modifying source files, or creating commits.
- Any write other than the single final draft file, plus default output directory creation by the validator.
- Subagent writes; all exploration is read-only.
- Generic brainstorming not grounded in repo context.
- Fabricated repo references, prior art, or objective evidence.
- Installation flow, marketing copy, screenshots, and broad usage documentation.
- Producing a `/humanize:gen-plan` plan directly; the draft is only suitable input for a later gen-plan step.