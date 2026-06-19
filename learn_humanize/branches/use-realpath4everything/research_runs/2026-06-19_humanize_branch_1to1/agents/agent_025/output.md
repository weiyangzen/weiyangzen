# agent_025 use-realpath4everything 1:1 Core Algorithm Research

## Worker Summary
- status: `[_]`
- assigned_item_count: 1
- source_commit: `cf17140050c4e063f27924c2d56cc2279d81f4cd`

## Item Evidence

### USE_REALPATH4EVERYTHING-HZ-025 `directory` `tests/robustness`
- cursor: `[_]`
- core_role:
  - `tests/robustness` is a flat recursive shell-test suite, not runtime implementation code. It is core algorithm evidence because it stress-tests the repository’s RLCR loop algorithms around path canonicalization, state-machine safety, hook validation, setup validation, git status parsing, goal-tracker parsing, template rendering, timeout portability, and monitor resilience.
  - The directory contains 16 shell scripts and no subdirectories. It coordinates through `tests/test-helpers.sh`, temporary git repositories, mock `codex`/`jq`/timeout binaries, and direct calls into production scripts under `hooks/` and `scripts/`.
  - The most branch-relevant responsibility is validating canonical path behavior: plan paths reject symlinks/traversal patterns, hook validators compare canonicalized path prefixes, and cancel authorization canonicalizes loop paths without dereferencing protected leaf files.

- algorithmic_behavior:
  - `test-path-validation-robustness.sh` runs `scripts/setup-rlcr-loop.sh` against synthetic plan paths. It accepts normal relative paths, nested paths, dash/underscore/dot names, long filenames, and deep paths, while rejecting absolute paths, spaces, shell metacharacters, symlink plan files, parent-directory symlinks, symlink chains, empty/comment-only/short files, missing files, and directories. See `tests/robustness/test-path-validation-robustness.sh:78`, `:122`, `:179`, `:342`, `:352`, `:367`, `:425`.
  - `test-cancel-security-robustness.sh` exercises `is_cancel_authorized` for the only allowed cancellation state transition: `mv state.md|finalize-state.md cancel-state.md` with `.cancel-requested`. It accepts quoted and unquoted canonical cancel forms, rejects command substitution, backticks, shell chaining, wrong source/destination, extra args, variable/IFS expansion, mixed quote styles, trailing-space ambiguity, non-standard source filenames, and leaf symlinks. See `tests/robustness/test-cancel-security-robustness.sh:39`, `:100`, `:109`, `:135`, `:174`, `:317`, `:332`, `:369`.
  - `test-hook-input-robustness.sh` and `test-hook-system-robustness.sh` pipe JSON into the actual hook validators. They verify malformed/deep/non-UTF8 JSON rejection or graceful handling, tool-field validation, state-file and goal-tracker protection, old-session goal-tracker read blocking, mutable-vs-immutable goal-tracker enforcement after round 0, concurrent hook calls, and stop-hook behavior for missing/corrupt/incomplete/active state. See `tests/robustness/test-hook-input-robustness.sh:35`, `:177`, `:201`, `:381`, `:444`; `tests/robustness/test-hook-system-robustness.sh:39`, `:123`, `:316`, `:418`, `:464`, `:538`, `:644`, `:726`.
  - `test-state-file-robustness.sh`, `test-state-transition-robustness.sh`, `test-concurrent-state-robustness.sh`, and `test-session-robustness.sh` validate the RLCR state discovery/parsing algorithms: tolerant defaults, strict schema rejection, active/finalize/cancel/complete state handling, zombie-loop protection, newest-session selection, concurrent reads, atomic-write reads, malformed/CRLF/unicode/binary inputs, drift fields, and full-review-round defaults. Production anchors are `hooks/lib/loop-common.sh:332`, `:430`, `:494`, `:533`.
  - `test-goal-tracker-robustness.sh` checks `humanize_parse_goal_tracker` and issue counting across list/table AC formats, active/completed/deferred tasks, blocking/queued/legacy issues, long goal summaries, malformed/truncated/binary inputs, and large AC counts. Production anchors are `scripts/humanize.sh:38`, `:71`.
  - `test-git-operations-robustness.sh` checks `humanize_parse_git_status` and `humanize_detect_git_state` for clean/dirty/staged/deleted/untracked/renamed/binary/space-name files, empty repos, detached HEAD, rebase, merge, shallow clone, non-git directories, and permission-like failures. Production anchors are `scripts/humanize.sh:158`, `:208`.
  - `test-base-branch-detection.sh` isolates setup base-branch selection: remote default branch, local `main`, local `master`, and hard failure with no eligible branch. The setup script’s matching behavior is at `scripts/setup-rlcr-loop.sh:749`, `:771`, `:779`, `:783`, `:786`.
  - `test-plan-file-robustness.sh` and `test-setup-scripts-robustness.sh` validate setup argument gates, dependency checks, git cleanliness, tracked-plan policy, plan content thresholds, YAML-safe names, timeout failure handling, `--full-review-round`, and `--skip-impl` scaffold creation. Setup validation anchors include `scripts/setup-rlcr-loop.sh:220`, `:256`, `:272`, `:399`, `:408`, `:457`, `:469`, `:483`, `:509`, `:519`, `:598`, `:615`, `:667`, `:920`.
  - `test-template-error-robustness.sh` and `test-template-stress-robustness.sh` validate template loading/rendering under missing files, malformed placeholders, invalid variable names, BOM/permission/symlink cases, concurrency, large values/templates, special replacement characters, and placeholder injection prevention. Production anchors are `hooks/lib/template-loader.sh:56`, `:140`, `:188`.
  - `test-timeout-robustness.sh` validates portable timeout detection and execution semantics: implementation fallback chain, exit `124` on timeout, command argument preservation, exit-code preservation, pipelines, rapid cycles, nonexistent commands, zero timeout behavior, special characters, signal handling, subshells, and exported `TIMEOUT_IMPL`. Production anchors are `scripts/portable-timeout.sh:10`, `:33`.

- inputs_outputs_state:
  - Inputs are shell arguments, JSON hook payloads, markdown plan/goal/state files, git repositories, fake session directories, command strings, template files, terminal/cache/log conditions, and mock binaries on `PATH`.
  - Outputs are pass/fail assertions through `tests/test-helpers.sh`, production script exit codes, hook JSON block/allow decisions, parsed pipe-delimited summaries, generated temporary loop/session files, and git/status state classifications.
  - State transitions tested include `state.md -> finalize-state.md`, `state.md|finalize-state.md -> cancel-state.md`, active loop discovery from latest session directory, ignored terminal `complete-state.md`/`cancel-state.md`, strict parser rejection of malformed or incomplete state, and setup-created `--skip-impl` review scaffolds.
  - Key production state logic: `find_active_loop` only checks the newest unfiltered directory for active state to avoid stale-loop revival (`hooks/lib/loop-common.sh:342`), while strict parsing requires frontmatter and schema-critical fields (`hooks/lib/loop-common.sh:541`, `:553`).

- gates_or_invariants:
  - Plan file gate: relative path only, no spaces or shell metacharacters, no leaf symlink, no parent symlink traversal, must exist/read as a file, must resolve inside project, must obey tracked/gitignored policy, and must have enough meaningful content. See `scripts/setup-rlcr-loop.sh:457`, `:463`, `:469`, `:483`, `:509`, `:539`, `:598`, `:618`, `:667`.
  - Cancel gate: `.cancel-requested` must exist; command must be a single `mv`; source must be exactly `state.md`, `finalize-state.md`, or `methodology-analysis-state.md`; destination must be exactly `cancel-state.md`; shell expansion/chaining is rejected; source symlink is rejected. See `hooks/lib/loop-common.sh:1055`, `:1062`, `:1072`, `:1101`, `:1106`, `:1191`, `:1217`, `:1232`.
  - Realpath/canonicalization invariant: comparisons resolve ancestor prefixes but do not dereference protected leaf files. `is_cancel_authorized` uses `canonicalize_path_prefix` for source/destination, with comments explaining that full realpath would incorrectly permit a planted symlink leaf (`hooks/lib/loop-common.sh:1191`). Read/write validators apply the same prefix-canonical comparison for wrong-directory checks (`hooks/loop-read-validator.sh:307`, `hooks/loop-write-validator.sh:334`).
  - Hook invariant: direct edits/writes to loop state files are blocked; goal-tracker mutable sections may be updated after round 0, but immutable sections must remain stable; old-session goal trackers are blocked.
  - State invariant: tolerant parsing defaults missing non-critical values, but strict parsing rejects missing frontmatter, missing `current_round`, missing `max_iterations`, missing `review_started`, missing `base_branch`, and non-numeric numeric fields (`hooks/lib/loop-common.sh:533`).
  - Template invariant: substitution is single-pass, preserving `{{VAR}}` text inside substituted values to prevent placeholder injection (`hooks/lib/template-loader.sh:52`, `:69`, `:115`).
  - Timeout invariant: `gtimeout > timeout > python3 > python > none`, with GNU-compatible timeout exit `124` for Python fallback (`scripts/portable-timeout.sh:10`, `:56`).

- dependencies_and_callers:
  - Test helpers: all robustness scripts rely on `tests/test-helpers.sh` for temp directories and assertions.
  - Production libraries/scripts: `hooks/lib/loop-common.sh`, `hooks/lib/template-loader.sh`, `scripts/portable-timeout.sh`, `scripts/humanize.sh`, and `scripts/setup-rlcr-loop.sh`.
  - Hook entrypoints: `hooks/loop-read-validator.sh`, `hooks/loop-write-validator.sh`, `hooks/loop-edit-validator.sh`, `hooks/loop-bash-validator.sh`, `hooks/loop-plan-file-validator.sh`, and `hooks/loop-codex-stop-hook.sh`.
  - External command dependencies under test: `git`, `jq`, `codex`, `timeout`/`gtimeout`, `python`, `awk`, `sed`, `grep`, `find`, `wc`, and shell builtins. Several scripts mock these to isolate validation behavior.
  - Parent/sibling coordination: this directory complements non-robustness tests under `tests/` by focusing on adversarial inputs and boundary conditions rather than nominal workflow coverage. It validates behavior implemented in `hooks/` and `scripts/`, not behavior local to `tests/robustness` itself.

- edge_cases_or_failure_modes:
  - Path and symlink attacks: absolute paths, parent symlink traversal, leaf symlink substitution, symlink chains, `/./` normalization, `/var` vs `/private/var`-style canonical prefix differences, and path names containing words like `finalize`.
  - Command injection: `$(...)`, backticks, `;`, `&&`, `||`, pipes, newlines, `${HOME}`, `${IFS}`, extra arguments, mixed quotes, and trailing-space ambiguity.
  - Parser hazards: malformed YAML, missing frontmatter, CRLF, binary bytes, null bytes, non-UTF8 JSON, deeply nested JSON, giant JSON/templates/plan files, unicode text, long lines, and missing/unreadable files.
  - Race and concurrency hazards: simultaneous state reads, atomic write replacement, concurrent hook invocations, rapid session creation, session deletion while monitoring, and log churn.
  - Git/setup hazards: non-git repos, empty repos, dirty working trees, untracked `.humanizeconfig`, tracked plan policy, missing dependencies, timed-out git checks, detached/rebase/merge/shallow states, and no detectable base branch.

- validation_or_tests:
  - I inspected the directory recursively with `find`/`rg`; it contains only `tests/robustness` plus these 16 files: `test-base-branch-detection.sh`, `test-cancel-security-robustness.sh`, `test-concurrent-state-robustness.sh`, `test-git-operations-robustness.sh`, `test-goal-tracker-robustness.sh`, `test-hook-input-robustness.sh`, `test-hook-system-robustness.sh`, `test-path-validation-robustness.sh`, `test-plan-file-robustness.sh`, `test-session-robustness.sh`, `test-setup-scripts-robustness.sh`, `test-state-file-robustness.sh`, `test-state-transition-robustness.sh`, `test-template-error-robustness.sh`, `test-template-stress-robustness.sh`, and `test-timeout-robustness.sh`.
  - I did not execute the suite because the branch export is read-only and these scripts intentionally create/delete temp repos, write test files, and invoke setup paths. This research pass is evidence-only.
  - `git status --short` could not be used as validation because this branch export has no `.git` directory and the sandbox denied Xcode temp-cache writes; this does not affect the file inspection evidence.

- skip_candidate: `no`

## Worker Self-Test
- assigned_items_seen: `1 item evidence section present`
- missing_items: `none`
- duplicate_items: `none`
- final_worker_status: `complete`