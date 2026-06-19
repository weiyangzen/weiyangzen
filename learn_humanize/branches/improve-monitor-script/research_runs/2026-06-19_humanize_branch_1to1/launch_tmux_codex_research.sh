#!/usr/bin/env bash
set -euo pipefail
RUN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SESSION="${SESSION:-humanize_improve-monitor-script_1to1_20260619}"
AGENT_COUNT="${AGENT_COUNT:-30}"
ACTIVE_WORKER_TARGET="${ACTIVE_WORKER_TARGET:-25}"
CHECK_INTERVAL_SECONDS="${CHECK_INTERVAL_SECONDS:-120}"
if ! command -v tmux >/dev/null 2>&1; then echo "tmux is required" >&2; exit 1; fi
if ! command -v codex >/dev/null 2>&1; then echo "codex is required" >&2; exit 1; fi
if tmux has-session -t "$SESSION" 2>/dev/null; then
  echo "tmux session already exists: $SESSION" >&2
  exit 1
fi
rm -f "$RUN_DIR/status"/*.status
rm -rf "$RUN_DIR/started"
mkdir -p "$RUN_DIR/status" "$RUN_DIR/started"
tmux new-session -d -s "$SESSION" -n "controller" "AGENT_COUNT='$AGENT_COUNT' ACTIVE_WORKER_TARGET='$ACTIVE_WORKER_TARGET' CHECK_INTERVAL_SECONDS='$CHECK_INTERVAL_SECONDS' bash '$RUN_DIR/replenish_tmux_codex_workers.sh'"
echo "launched replenishing codex research controller in tmux session: $SESSION"
echo "agent slots: $AGENT_COUNT"
echo "active worker refill target: $ACTIVE_WORKER_TARGET"
echo "check interval seconds: $CHECK_INTERVAL_SECONDS"
echo "status dir: $RUN_DIR/status"
echo "controller log: $RUN_DIR/worker_replenish.log"
