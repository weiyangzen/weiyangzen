#!/usr/bin/env bash
set -euo pipefail

RUN_DIR='/Users/wangweiyang/GitHub/weiyangzen/learn_humanize/branches/add-a-final-code-simplifier-after-codex-complete/research_runs/2026-06-19_humanize_branch_1to1'
SESSION='humanize_add-a-final-code-simplif_1to1_20260619'
AGENT_COUNT="${AGENT_COUNT:-30}"
ACTIVE_WORKER_TARGET="${ACTIVE_WORKER_TARGET:-25}"
CHECK_INTERVAL_SECONDS="${CHECK_INTERVAL_SECONDS:-120}"
STARTED_DIR="$RUN_DIR/started"
STATUS_DIR="$RUN_DIR/status"
LOG="$RUN_DIR/worker_replenish.log"

mkdir -p "$STARTED_DIR" "$STATUS_DIR"
touch "$LOG"

log() {
  printf '%s %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*" >> "$LOG"
}

active_workers() {
  local names
  names="$(tmux list-windows -t "$SESSION" -F '#W' 2>/dev/null || true)"
  printf '%s\n' "$names" | awk '/^agent[0-9][0-9]$/ { count++ } END { print count + 0 }'
}

status_count() {
  find "$STATUS_DIR" -maxdepth 1 -type f -name 'agent_*.status' | wc -l | tr -d ' '
}

next_unstarted_agent() {
  local n id agent
  for n in $(seq 1 "$AGENT_COUNT"); do
    id="$(printf '%02d' "$n")"
    agent="agent_$id"
    if [[ ! -f "$STARTED_DIR/$agent.started" && ! -f "$STATUS_DIR/$agent.status" ]]; then
      printf '%s\n' "$id"
      return 0
    fi
  done
  return 1
}

start_agent() {
  local id="$1"
  local agent="agent_$id"
  local runner="$RUN_DIR/agents/$agent/run.sh"
  if [[ ! -x "$runner" ]]; then
    log "missing runner for $agent: $runner"
    return 1
  fi
  tmux new-window -t "$SESSION:" -n "agent$id" "bash '$runner'"
  touch "$STARTED_DIR/$agent.started"
  log "started $agent"
}

replenish() {
  local active next_id
  active="$(active_workers)"
  while [[ "$active" -lt "$ACTIVE_WORKER_TARGET" ]]; do
    if ! next_id="$(next_unstarted_agent)"; then
      break
    fi
    start_agent "$next_id"
    active="$(active_workers)"
  done
}

log "controller started session=$SESSION agent_count=$AGENT_COUNT active_target=$ACTIVE_WORKER_TARGET interval=$CHECK_INTERVAL_SECONDS"
while true; do
  replenish
  active="$(active_workers)"
  statuses="$(status_count)"
  log "tick active_workers=$active status_files=$statuses"
  if [[ "$statuses" -ge "$AGENT_COUNT" && "$active" -eq 0 ]]; then
    log "all agents finished"
    break
  fi
  sleep "$CHECK_INTERVAL_SECONDS"
done
