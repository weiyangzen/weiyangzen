#!/usr/bin/env bash
set -euo pipefail
RUN_DIR='/Users/wangweiyang/GitHub/weiyangzen/learn_humanize/research_runs/2026-06-19_humanize_core_1to1'
AGENT='agent_17'
AGENT_DIR="$RUN_DIR/agents/$AGENT"
PROMPT="$RUN_DIR/prompts/$AGENT.md"
OUTPUT="$AGENT_DIR/output.md"
STATUS="$RUN_DIR/status/$AGENT.status"
META="$AGENT_DIR/metadata.env"
STARTED="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
printf 'agent=%s
source_commit=%s
model=%s
reasoning_effort=%s
item_count=%s
status=running
started_utc=%s
' "$AGENT" '0ec921a36b4365df503511c5567bbd3e02db0df5' 'gpt-5.5' 'xhigh' 7 "$STARTED" > "$META"
set +e
"$AGENT_DIR/timeout_run.py" 7200 codex -a never exec -m gpt-5.5 -c model_reasoning_effort=xhigh -C /Users/wangweiyang/GitHub/humanize -s read-only --ephemeral -o "$OUTPUT" - < "$PROMPT"
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
printf 'agent=%s
source_commit=%s
model=%s
reasoning_effort=%s
item_count=%s
status=%s
started_utc=%s
ended_utc=%s
exit_code=%s
' "$AGENT" '0ec921a36b4365df503511c5567bbd3e02db0df5' 'gpt-5.5' 'xhigh' 7 "$final_status" "$STARTED" "$ENDED" "$rc" > "$META"
exit "$rc"
