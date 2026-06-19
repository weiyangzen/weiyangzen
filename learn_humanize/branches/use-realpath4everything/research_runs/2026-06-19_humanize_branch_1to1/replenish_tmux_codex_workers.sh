#!/usr/bin/env bash
set -euo pipefail

RUN_DIR='/Users/wangweiyang/GitHub/weiyangzen/learn_humanize/branches/use-realpath4everything/research_runs/2026-06-19_humanize_branch_1to1'
SESSION='humanize_use-realpath4everything_1to1_20260619'
WORKER_SLOT_COUNT="${WORKER_SLOT_COUNT:-30}"
AGENT_COUNT="${AGENT_COUNT:-$WORKER_SLOT_COUNT}"
WORKER_JOB_COUNT="${WORKER_JOB_COUNT:-197}"
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
  printf '%s\n' "$names" | awk '/^agent[0-9]+$/ { count++ } END { print count + 0 }'
}

complete_count() {
  local count=0
  local status_file
  shopt -s nullglob
  for status_file in "$STATUS_DIR"/agent_*.status; do
    if [[ "$(cat "$status_file" 2>/dev/null || true)" == "complete" ]]; then
      count=$((count + 1))
    fi
  done
  shopt -u nullglob
  printf '%s' "$count"
}

failed_count() {
  local count=0
  local status_file value
  shopt -s nullglob
  for status_file in "$STATUS_DIR"/agent_*.status; do
    value="$(cat "$status_file" 2>/dev/null || true)"
    if [[ "$value" == failed:* ]]; then
      count=$((count + 1))
    fi
  done
  shopt -u nullglob
  printf '%s' "$count"
}

agent_window_active() {
  local id="$1"
  local name="agent$id"
  tmux list-windows -t "$SESSION" -F '#W' 2>/dev/null | awk -v name="$name" '$0 == name { found=1 } END { exit found ? 0 : 1 }'
}

next_claimable_agent() {
  local runner agent id status_file status
  while IFS= read -r runner; do
    agent="$(basename "$(dirname "$runner")")"
    id="${agent#agent_}"
    status_file="$STATUS_DIR/$agent.status"
    status=""
    if [[ -f "$status_file" ]]; then
      status="$(cat "$status_file" 2>/dev/null || true)"
    fi
    [[ "$status" == "complete" ]] && continue
    agent_window_active "$id" && continue
    printf '%s\n' "$id"
    return 0
  done < <(find "$RUN_DIR/agents" -mindepth 2 -maxdepth 2 -type f -name run.sh | sort -V)
  return 1
}

start_agent() {
  local id="$1"
  local agent="agent_$id"
  local runner="$RUN_DIR/agents/$agent/run.sh"
  local attempt_file="$STARTED_DIR/$agent.attempts"
  local attempt=1
  if [[ ! -x "$runner" ]]; then
    log "missing runner for $agent: $runner"
    return 1
  fi
  if [[ -f "$attempt_file" ]]; then
    attempt="$(cat "$attempt_file" 2>/dev/null || echo 0)"
    attempt=$((attempt + 1))
  fi
  printf '%s\n' "$attempt" > "$attempt_file"
  rm -f "$STATUS_DIR/$agent.status" "$RUN_DIR/agents/$agent/output.md"
  tmux new-window -t "$SESSION:" -n "agent$id" "bash '$runner'; tmux kill-window -t '$SESSION:agent$id' 2>/dev/null || true"
  touch "$STARTED_DIR/$agent.started"
  log "started $agent attempt=$attempt"
}

replenish() {
  local active next_id
  active="$(active_workers)"
  local target="$ACTIVE_WORKER_TARGET"
  if [[ "$target" -gt "$WORKER_SLOT_COUNT" ]]; then
    target="$WORKER_SLOT_COUNT"
  fi
  while [[ "$active" -lt "$target" ]]; do
    if ! next_id="$(next_claimable_agent)"; then
      break
    fi
    start_agent "$next_id"
    active="$(active_workers)"
  done
}

log "controller started session=$SESSION worker_slots=$WORKER_SLOT_COUNT worker_jobs=$WORKER_JOB_COUNT active_target=$ACTIVE_WORKER_TARGET interval=$CHECK_INTERVAL_SECONDS"
while true; do
  replenish
  active="$(active_workers)"
  complete="$(complete_count)"
  failed="$(failed_count)"
  log "tick active_workers=$active complete_statuses=$complete failed_statuses=$failed worker_jobs=$WORKER_JOB_COUNT"
  if [[ "$complete" -ge "$WORKER_JOB_COUNT" && "$active" -eq 0 ]]; then
    log "all worker jobs completed"
    break
  fi
  sleep "$CHECK_INTERVAL_SECONDS"
done
