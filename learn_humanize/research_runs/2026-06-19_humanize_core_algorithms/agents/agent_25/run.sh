#!/usr/bin/env bash
set -euo pipefail
AGENT_DIR="/Users/wangweiyang/GitHub/weiyangzen/learn_humanize/research_runs/2026-06-19_humanize_core_algorithms/agents/agent_25"
PROMPT_FILE="/Users/wangweiyang/GitHub/weiyangzen/learn_humanize/research_runs/2026-06-19_humanize_core_algorithms/prompts/agent_25.md"
OUT_FILE="$AGENT_DIR/output.md"
STDOUT_FILE="$AGENT_DIR/stdout.log"
STDERR_FILE="$AGENT_DIR/stderr.log"
STATUS_FILE="/Users/wangweiyang/GitHub/weiyangzen/learn_humanize/research_runs/2026-06-19_humanize_core_algorithms/status/agent_25.status"
echo running > "$STATUS_FILE"
echo "started_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$AGENT_DIR/metadata.env"
echo "topic=Skill monitor and telemetry parsing" >> "$AGENT_DIR/metadata.env"
echo "codex_bin=/Users/wangweiyang/.nvm/versions/node/v22.14.0/bin/codex" >> "$AGENT_DIR/metadata.env"
set +e
"/usr/bin/python3" "/Users/wangweiyang/GitHub/weiyangzen/learn_humanize/research_runs/2026-06-19_humanize_core_algorithms/agents/agent_25/timeout_run.py" "7200" "$PROMPT_FILE" "$STDOUT_FILE" "$STDERR_FILE" "/Users/wangweiyang/.nvm/versions/node/v22.14.0/bin/codex" -a never exec -m "gpt-5.5" -c model_reasoning_effort="xhigh" -C "/Users/wangweiyang/GitHub/humanize" -s read-only --ephemeral -o "$OUT_FILE" -
code=$?
set -e
echo "finished_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$AGENT_DIR/metadata.env"
echo "exit_code=$code" >> "$AGENT_DIR/metadata.env"
if [[ $code -eq 0 && -s "$OUT_FILE" ]]; then echo complete > "$STATUS_FILE"; else echo failed:$code > "$STATUS_FILE"; fi
exit $code
