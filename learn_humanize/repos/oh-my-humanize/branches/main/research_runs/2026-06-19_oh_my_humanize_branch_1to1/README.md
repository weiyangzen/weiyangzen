# 2026-06-19_oh_my_humanize_branch_1to1 - `main`

This run uses `30` Codex worker slots with model `gpt-5.5` and reasoning effort `xhigh`.
The tmux controller checks every `120` seconds and refills active worker windows up to `25`.

```text
codex -a never exec -m gpt-5.5 -c model_reasoning_effort=xhigh -C /Users/wangweiyang/GitHub/oh_my_humanize_branch_worktrees/main -s read-only --ephemeral -o <agent>/output.md -
```
