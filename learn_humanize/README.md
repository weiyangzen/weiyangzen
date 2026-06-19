# learn_humanize

This directory contains a focused research artifact for the open-source
`PolyArch/humanize` repository.

## Scope

- Source repository: `https://github.com/PolyArch/humanize.git`
- Local source checkout: `/Users/wangweiyang/GitHub/humanize`
- Source commit studied: `0ec921a36b4365df503511c5567bbd3e02db0df5`
- Research run: `research_runs/2026-06-19_humanize_core_algorithms`
- Method: 30 parallel `tmux` windows running `codex exec`
- Model: `gpt-5.5`
- Reasoning effort: `xhigh`
- Sandbox: read-only against the Humanize source checkout

## Main Deliverables

- `core_algorithm_subset_report.md`: consolidated Chinese report on the algorithmic subset of Humanize.
- `research_runs/2026-06-19_humanize_core_algorithms/topics.tsv`: the 30-topic research split.
- `research_runs/2026-06-19_humanize_core_algorithms/launch_tmux_codex_research.sh`: reproducible launcher used for the 30-agent tmux run.
- `research_runs/2026-06-19_humanize_core_algorithms/run_manifest.env`: run metadata.
- `research_runs/2026-06-19_humanize_core_algorithms/status/*.status`: completion status for each agent.
- `research_runs/2026-06-19_humanize_core_algorithms/agents/agent_*/output.md`: raw agent research notes.

## Headline Conclusion

Humanize's core is not a conventional numeric algorithm. The algorithmic center is a workflow state machine:

1. Generate or refine a plan with Claude/Codex convergence.
2. Initialize an RLCR loop with strict setup gates.
3. Run implementation rounds through a Claude `Stop` hook.
4. Use Codex summary review to decide whether implementation is complete.
5. Transition to `codex review --base` and gate on `[P0-9]` findings.
6. Enter finalize only after code review passes.
7. Enforce supporting invariants through protected files, validators, git gates, BitLesson memory gates, background-task parking, and drift detection.

Business, installation, screenshot, and generic usage content was intentionally skipped unless it defined behavior used by the state machine.

## Verification Notes

The run completed with all 30 agents reporting `complete`. The launcher records the exact model, effort, source commit, and tmux session name in `run_manifest.env`.
