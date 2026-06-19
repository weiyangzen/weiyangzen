# 2026-06-19 Humanize Core Algorithm Research Run

This run used 30 parallel tmux windows, each launching one read-only Codex research agent against the same Humanize source checkout.

## Command Shape

The launcher generated per-agent prompts and ran:

```text
codex -a never exec -m gpt-5.5 -c model_reasoning_effort=xhigh -C /Users/wangweiyang/GitHub/humanize -s read-only --ephemeral -o <agent>/output.md -
```

The macOS host did not provide GNU `timeout`, so the launcher uses a small Python standard-library timeout wrapper per agent.

## Run Metadata

See `run_manifest.env` for authoritative run metadata.

```text
source_commit=0ec921a36b4365df503511c5567bbd3e02db0df5
tmux_session=humanize_core_20260619
model=gpt-5.5
reasoning_effort=xhigh
timeout_seconds=7200
```

## Outputs

- `topics.tsv`: 30 topic split.
- `prompts/agent_*.md`: generated per-agent prompts.
- `agents/agent_*/output.md`: raw research output.
- `agents/agent_*/metadata.env`: start/end/exit metadata.
- `status/agent_*.status`: final completion markers.
- `logs/`: reserved for run logs.

All 30 agents completed with `exit_code=0`.
