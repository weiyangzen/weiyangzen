#!/usr/bin/env bash
set -euo pipefail
RUN_DIR='/Users/wangweiyang/GitHub/weiyangzen/learn_humanize/branches/vcs-cli-on-plan-file/research_runs/2026-06-19_humanize_branch_1to1'
BRANCH='vcs-cli-on-plan-file'
AGENT='agent_26'
AGENT_DIR="$RUN_DIR/agents/$AGENT"
PROMPT="$RUN_DIR/prompts/$AGENT.md"
OUTPUT="$AGENT_DIR/output.md"
ERRLOG="$AGENT_DIR/stderr.log"
STATUS="$RUN_DIR/status/$AGENT.status"
META="$AGENT_DIR/metadata.env"
STARTED="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
printf 'branch=%s\nagent=%s\nsource_commit=%s\nsource_tree=%s\nmodel=%s\nreasoning_effort=%s\nitem_count=%s\nstatus=running\nstarted_utc=%s\n' "$BRANCH" "$AGENT" '4dd1ca2fece39d3c6d7f84965cd71bda02489397' '2eceab4140baa5aa2a6130625bfe3e91590ceb99' 'gpt-5.5' 'xhigh' 1 "$STARTED" > "$META"
set +e
rm -f "$ERRLOG"
"$AGENT_DIR/timeout_run.py" 7200 codex -a never exec -m gpt-5.5 -c model_reasoning_effort=xhigh -C '/Users/wangweiyang/GitHub/humanize_branch_worktrees/vcs-cli-on-plan-file' --skip-git-repo-check -s read-only --ephemeral -o "$OUTPUT" - < "$PROMPT" 2> "$ERRLOG"
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
printf 'branch=%s\nagent=%s\nsource_commit=%s\nsource_tree=%s\nmodel=%s\nreasoning_effort=%s\nitem_count=%s\nstatus=%s\nstarted_utc=%s\nended_utc=%s\nexit_code=%s\n' "$BRANCH" "$AGENT" '4dd1ca2fece39d3c6d7f84965cd71bda02489397' '2eceab4140baa5aa2a6130625bfe3e91590ceb99' 'gpt-5.5' 'xhigh' 1 "$final_status" "$STARTED" "$ENDED" "$rc" > "$META"
exit "$rc"
