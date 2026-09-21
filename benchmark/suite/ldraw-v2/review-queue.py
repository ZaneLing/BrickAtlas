#!/usr/bin/env python3
"""Export explicit source-local physical candidate IDs and paired review views."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "benchmark/ldraw-v2"
SITE = ROOT / "public/benchmark/ldraw-v2"
catalog = json.loads((DATA / "catalog.json").read_text())
pairs = []
for entry in catalog:
    bundle = json.loads((SITE / f"models/{entry['id']}.json").read_text())
    labels = {p["id"]: p["label"] for p in bundle["parts"]}
    for i, (a, b) in enumerate(bundle["audit"]["nonMatingCollisionPairs"], 1):
        pairs.append({"id": f"ld2-{entry['id']}-pair-{i:04d}", "sourceId": entry["id"],
                      "sourceSha256": entry["sourceHash"],
                      "operands": [{"id": p, "label": labels[p]} for p in [a, b]],
                      "status": "pending", "reviewer": None, "decision": None, "rationale": None,
                      "meaning": "Inset-mesh intersection without a recognized mating pair; not a certified collision defect."})
assert len(pairs) == 573
physical = {"version": "brickatlas-ldraw-2", "physicalCertification": "not-established", "pairs": pairs}
(DATA / "physical-review-queue.json").write_text(json.dumps(physical, indent=2) + "\n")
queue = json.loads((DATA / "human-review-queue.json").read_text())
for row in queue["items"]:
    if row["views"]["standard"]:
        row["views"].update({mode: f"benchmark/ldraw-v2/inputs/views-{mode}/{row['taskId']}.png"
                             for mode in ["full", "mask", "crop", "camera"]})
queue["physicalPairQueue"] = "physical-review-queue.json"
(DATA / "human-review-queue-with-views.json").write_text(json.dumps(queue, indent=2) + "\n")
for filename, value in [("human-review-queue.json", queue), ("physical-review-queue.json", physical)]:
    (SITE / filename).write_text(json.dumps(value, indent=2) + "\n")
print(f"Review queues: {len(queue['items'])} tasks and {len(pairs)} physical candidates; no decisions supplied.")
