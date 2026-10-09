"""Build evaluator input from a local run store; duplicate task runs require selection."""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path

from build import load_bank, write_json
from cases import CASES
from probes import ProbeSet


def collect(store, selection=None, metadata=None):
    grouped = defaultdict(list)
    for path in Path(store).glob("session-*.json"):
        record = json.loads(path.read_text())
        grouped[record["taskId"]].append((path.stem.removeprefix("session-"), record))
    episodes = {}
    for task_id, records in grouped.items():
        if selection is not None and task_id not in selection:
            continue
        if selection is None:
            if len(records) > 1:
                raise ValueError(f"Multiple runs for {task_id}; supply an explicit --selection manifest")
            episodes[task_id] = records[0][1]
        else:
            selected = [r for key, r in records if key == selection[task_id]]
            if len(selected) != 1:
                raise ValueError(f"Unknown selected session for {task_id}")
            episodes[task_id] = selected[0]
    if selection is not None and set(selection) != set(episodes):
        raise ValueError("Selection contains an unavailable task")
    submission = {"schema": "brickplan-submission/1.0", "episodes": episodes,
                  "metadata": metadata or {}}
    answers = Path(store) / "probe-answers.json"
    if answers.exists():
        data = json.loads(answers.read_text())
        probes = ProbeSet([load_bank(c["id"]) for c in CASES], data["seed"])
        normalized, positions = probes.normalize(data["answers"])
        submission.update(normalized)
        submission["metadata"]["presentedCandidatePositionCounts"] = positions
        submission["metadata"]["probeSeed"] = data["seed"]
    return submission


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--store", type=Path, required=True)
    parser.add_argument("--selection", type=Path, help="JSON object: private task ID -> session ID")
    parser.add_argument("--metadata", type=Path, help="Model/version, budgets, cost, seed and preregistration metadata")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    write_json(args.output, collect(args.store,
               json.loads(args.selection.read_text()) if args.selection else None,
               json.loads(args.metadata.read_text()) if args.metadata else None))


if __name__ == "__main__":
    main()
