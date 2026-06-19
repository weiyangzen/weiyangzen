#!/usr/bin/env python3
from pathlib import Path
import csv, re, sys, json
root = Path(__file__).resolve().parents[2]
run = Path(__file__).resolve().parent
items = []
with (root / "research_list.tsv").open() as f:
    items = list(csv.DictReader(f, delimiter="\t"))
problems = []
for item in items:
    agent = item["assigned_agent"]
    out = run / "agents" / agent / "output.md"
    status = run / "status" / f"{agent}.status"
    if not status.exists() or status.read_text().strip() != "complete":
        problems.append({"item_id": item["item_id"], "problem": "status_not_complete", "agent": agent})
    if not out.exists():
        problems.append({"item_id": item["item_id"], "problem": "missing_output", "agent": agent})
        continue
    text = out.read_text(errors="replace")
    if not re.search(r"(?<![A-Z0-9-])" + re.escape(item["item_id"]) + r"(?![A-Z0-9-])", text):
        problems.append({"item_id": item["item_id"], "problem": "item_id_missing_from_output", "agent": agent, "path": item["path"]})
summary = {
    "research_items": len(items),
    "status_files": len(list((run / "status").glob("*.status"))),
    "complete_status_files": sum(1 for p in (run / "status").glob("*.status") if p.read_text().strip() == "complete"),
    "output_files": len(list((run / "agents").glob("agent_*/output.md"))),
    "problems": len(problems),
}
print(json.dumps(summary, indent=2))
if problems:
    print(json.dumps(problems[:200], indent=2))
    sys.exit(1)
