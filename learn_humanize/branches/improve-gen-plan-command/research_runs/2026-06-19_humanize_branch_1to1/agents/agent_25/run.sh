#!/usr/bin/env bash
set -euo pipefail
RUN_DIR='/Users/wangweiyang/GitHub/weiyangzen/learn_humanize/branches/improve-gen-plan-command/research_runs/2026-06-19_humanize_branch_1to1'
BRANCH='improve-gen-plan-command'
AGENT='agent_25'
AGENT_DIR="$RUN_DIR/agents/$AGENT"
PROMPT="$RUN_DIR/prompts/$AGENT.md"
OUTPUT="$AGENT_DIR/output.md"
STATUS="$RUN_DIR/status/$AGENT.status"
META="$AGENT_DIR/metadata.env"
STARTED="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
printf 'branch=%s\nagent=%s\nsource_commit=%s\nsource_tree=%s\nmodel=%s\nreasoning_effort=%s\nitem_count=%s\nstatus=running\nstarted_utc=%s\n' "$BRANCH" "$AGENT" '934cf543d66046b72071d121b15583d5e3d6799e' 'a22ad6bef2ad440595842fd080d8abf4ffc5c7b9' 'gpt-5.5' 'xhigh' 4 "$STARTED" > "$META"
set +e
"$AGENT_DIR/timeout_run.py" 7200 codex -a never exec -m gpt-5.5 -c model_reasoning_effort=xhigh -C '/Users/wangweiyang/GitHub/humanize_branch_worktrees/improve-gen-plan-command' --skip-git-repo-check -s read-only --ephemeral -o "$OUTPUT" - < "$PROMPT"
rc=$?
set -e
ENDED="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
if [ "$rc" -eq 0 ]; then
  echo complete > "$STATUS"
  final_status=complete
else
  echo failed:$rc > "$STATUS"
  final_status=failed
fi
printf 'branch=%s\nagent=%s\nsource_commit=%s\nsource_tree=%s\nmodel=%s\nreasoning_effort=%s\nitem_count=%s\nstatus=%s\nstarted_utc=%s\nended_utc=%s\nexit_code=%s\n' "$BRANCH" "$AGENT" '934cf543d66046b72071d121b15583d5e3d6799e' 'a22ad6bef2ad440595842fd080d8abf4ffc5c7b9' 'gpt-5.5' 'xhigh' 4 "$final_status" "$STARTED" "$ENDED" "$rc" > "$META"
exit "$rc"
