#!/usr/bin/env python3
"""Validate independent review records and the fixed acceptance gate."""
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def audit(require_accept=False):
    rounds = []
    for directory in sorted(HERE.glob("round-*")):
        path = directory / "review.json"
        if not path.exists():
            continue
        review = json.loads(path.read_text())
        snapshot = json.loads((directory / "snapshot.json").read_text())
        assert review["round"] == int(directory.name.split("-")[-1])
        assert review["snapshot_sha256"] == snapshot["sha256"]
        assert 1 <= review["score"] <= 10 and 1 <= review["confidence"] <= 5
        assert isinstance(review["criteria"], (dict, list)) and review["criteria"]
        assert review["assumption"] and review["acceptance_rationale"]
        ids = []
        for issue in review["issues"]:
            for field in ["id", "severity", "status", "summary", "evidence", "why_it_matters", "closure_test"]:
                assert field in issue, (path, field)
            assert issue["severity"] in {"critical", "major", "minor"}
            assert issue["status"] in {"open", "closed"}
            ids.append(issue["id"])
        assert len(ids) == len(set(ids)), path
        blockers = [i["id"] for i in review["issues"] if i["status"] == "open" and i["severity"] in {"critical", "major"}]
        rounds.append({"round": review["round"], "verdict": review["verdict"], "score": review["score"],
                       "open_major_or_critical": blockers, "snapshot_sha256": snapshot["sha256"]})
    if require_accept:
        assert len(rounds) >= 2, "Need multiple independent review interactions"
        final = rounds[-1]
        assert final["score"] >= 7 and final["verdict"] in {"accept", "strong_accept"}
        assert not final["open_major_or_critical"]
        directory = HERE / f"round-{final['round']:02d}"
        validation = json.loads((directory / "validation.json").read_text())
        assert validation["status"] == "passed"
        assert validation["snapshot_sha256"] == final["snapshot_sha256"]
        assert all((directory / name).exists() for name in ["response.md", "changes.json", "report.md"])
    return {"internal_simulation": True, "empirical_completion_is_review_assumption_only": True,
            "rounds": rounds, "acceptance_gate_passed": bool(require_accept)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-accept", action="store_true")
    args = parser.parse_args()
    print(json.dumps(audit(args.require_accept), indent=2))
