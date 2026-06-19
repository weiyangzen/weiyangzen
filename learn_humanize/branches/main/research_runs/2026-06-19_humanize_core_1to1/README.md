# 2026-06-19_humanize_core_1to1

Corrected Humanize core algorithm 1:1 research run.

## Command Shape

```text
codex -a never exec -m gpt-5.5 -c model_reasoning_effort=xhigh -C /Users/wangweiyang/GitHub/humanize -s read-only --ephemeral -o <agent>/output.md -
```

## Protocol

- One included core algorithm file or directory equals one checklist item.
- Workers receive bounded batches but must report every assigned item separately.
- Workers may only produce `[_]` research evidence.
- The main session promotes items to `[x]` only after status/output/coverage verification.
- Non-core files and directories are listed in `skipped_paths.tsv` and not assigned.

## Metadata

- source_commit: `0ec921a36b4365df503511c5567bbd3e02db0df5`
- tmux_session: `humanize_core_1to1_20260619`
- model: `gpt-5.5`
- reasoning_effort: `xhigh`
- worker_count: `30`
- included_items: `201`
