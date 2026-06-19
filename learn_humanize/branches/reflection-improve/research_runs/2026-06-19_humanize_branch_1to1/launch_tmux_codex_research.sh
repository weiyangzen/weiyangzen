#!/usr/bin/env bash
set -euo pipefail
RUN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SESSION="${SESSION:-humanize_reflection-improve_1to1_20260619}"
AGENT_COUNT="${AGENT_COUNT:-30}"
if ! command -v tmux >/dev/null 2>&1; then echo "tmux is required" >&2; exit 1; fi
if ! command -v codex >/dev/null 2>&1; then echo "codex is required" >&2; exit 1; fi
if tmux has-session -t "$SESSION" 2>/dev/null; then
  echo "tmux session already exists: $SESSION" >&2
  exit 1
fi
rm -f "$RUN_DIR/status"/*.status
first="$RUN_DIR/agents/agent_01/run.sh"
tmux new-session -d -s "$SESSION" -n "agent01" "bash '$first'"
for n in $(seq 2 "$AGENT_COUNT"); do
  id=$(printf '%02d' "$n")
  runner="$RUN_DIR/agents/agent_${id}/run.sh"
  tmux new-window -t "$SESSION:" -n "agent${id}" "bash '$runner'"
done
echo "launched $AGENT_COUNT codex research agents in tmux session: $SESSION"
echo "status dir: $RUN_DIR/status"
