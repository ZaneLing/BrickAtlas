"""Authoritative evaluator: run identity, complete assignment census, seven metrics."""
import argparse
import json
from pathlib import Path

from bank import load_oracle, make_mission, task_bank, task_by_id, write_json
from metrics import aggregate_trajectories, fraction, score_probe, trajectory_metrics
from mission import State, canonical_hash
from probes import Probe
from quality import clustered_scores
from session import TRACKS, replay_export


def validate_assignments(assignments):
    bank = task_bank()
    tasks = {x["id"] for x in bank["episodes"]}
    probes = {x["id"] for x in bank["probes"]}
    if (not isinstance(assignments, dict) or set(assignments) != {"episodes", "probes"}
            or any(not isinstance(assignments[k], list) or len(set(assignments[k])) != len(assignments[k])
                   for k in assignments)
            or not set(assignments["episodes"]) <= tasks or not set(assignments["probes"]) <= probes):
        raise ValueError("Invalid or duplicate assignments")
    return assignments


def evaluate(submission):
    if submission.get("schema") != "brickplan-submission/2.0":
        raise ValueError("Unknown submission schema")
    bank = task_bank()
    identity = submission["identity"]
    if (not isinstance(identity, dict) or set(identity) != {"runId", "participantId", "condition"}
            or any(not isinstance(identity.get(k), str) or not identity[k] for k in identity)):
        raise ValueError("Missing run identity")
    if type(submission.get("seed")) is not int or not 0 <= submission["seed"] < 2**32:
        raise ValueError("Invalid run seed")
    if identity["condition"] not in TRACKS:
        raise ValueError("Unknown condition")
    if submission.get("bankHash") != canonical_hash(bank):
        raise ValueError("Submission bank hash mismatch")
    assigned = validate_assignments(submission["assignments"])
    episode_records, probe_records = submission.get("episodes", {}), submission.get("probes", {})
    if not set(episode_records) <= set(assigned["episodes"]) or not set(probe_records) <= set(assigned["probes"]):
        raise ValueError("Unassigned result")
    rows, by_id = [], {}
    session_ids = set()
    for task_id, record in episode_records.items():
        task = task_by_id(task_id)
        if record["seed"] != submission["seed"]:
            raise ValueError("Assignment seed mismatch")
        session_id = record["identity"]["sessionId"]
        if (not isinstance(session_id, str) or not session_id
                or record["identity"] != {**identity, "sessionId": session_id}):
            raise ValueError("Participant/run/condition mixing")
        if session_id in session_ids:
            raise ValueError("Reused episode session ID")
        session_ids.add(session_id)
        session = replay_export(make_mission(task), task, record)
        row = trajectory_metrics(load_oracle(task_id), session)
        row.update(taskId=task_id, tier=task["tier"], sourceGroup=task["sourceGroup"])
        rows.append(row)
        by_id[task_id] = row
    probes = {p["id"]: p for p in bank["probes"]}
    probe_scores, view_counts = {}, {}
    for probe_id, record in probe_records.items():
        if (record.get("probeId") != probe_id or record.get("seed") != submission["seed"]
                or record.get("probeHash") != canonical_hash(probes[probe_id])
                or record.get("identity") != identity):
            raise ValueError("Probe identity/certificate mismatch")
        replay = Probe(probes[probe_id], probe_id, submission["seed"], identity)
        for request in record["requests"]:
            revision = replay.revision
            replay.submit(request)
            if replay.revision != revision + 1:
                raise ValueError("Duplicate request in probe transcript")
        if record != replay.export():
            raise ValueError("Probe answer/view transcript mismatch")
        probe_scores[probe_id] = score_probe(probes[probe_id], record.get("answer"))
        view_counts[probe_id] = replay.session.views
    pair_rows = []
    tasks = {t["id"]: t for t in bank["episodes"]}
    for pair in bank["pairs"]:
        members = pair["members"]
        probe_pair = pair["kind"] in ("interior-order", "visual-geometry", "appearance-invariant")
        collection = assigned["probes"] if probe_pair else assigned["episodes"]
        if not set(members) <= set(collection):
            continue
        if probe_pair:
            correct = [probe_scores.get(x, {}).get("correct", False) for x in members]
            observed = [x in probe_scores for x in members]
        else:
            correct, observed = [], []
            for task_id in members:
                record = episode_records.get(task_id)
                observed.append(record is not None)
                first = next((e for e in record["events"] if e["cost"]), None) if record else None
                correct.append(bool(first and first["code"] == "OK"
                                    and first["internalAction"] in tasks[task_id]["initialOptimalActions"]))
        pair_rows.append({"pairId": pair["id"], "kind": pair["kind"], "observedBoth": all(observed),
                          "jointCorrect": all(correct)})
    survival = []
    max_budget = max((tasks[t]["maxActions"] for t in assigned["episodes"]), default=0)
    for step in range(1, max_budget + 1):
        eligible = [t for t in assigned["episodes"] if tasks[t]["maxActions"] >= step]
        lower, unknown, observed_risk = 0, 0, 0
        for task_id in eligible:
            row = by_id.get(task_id)
            if row is None:
                unknown += 1
                continue
            if row["firstCostLoss"] is not None and row["firstCostLoss"] <= step:
                observed_risk += 1
            elif row["success"] or row["operations"] >= step:
                lower += 1
                observed_risk += 1
            elif row["terminated"]:
                observed_risk += 1
            else:
                unknown += 1
        survival.append({"step": step, "assignedAtRisk": len(eligible), "observedAtRisk": observed_risk,
                         "lower": fraction(lower, len(eligible)),
                         "upper": fraction(lower + unknown, len(eligible)), "censoredOrMissing": unknown})
    replans = [p for row in rows for p in row["replanning"]]
    discriminative = [p for p in assigned["probes"] if probes[p]["scoringRole"] == "discriminative"]
    correct = {p: s["correct"] for p, s in probe_scores.items()}
    report = {
        "schema": "brickplan-report/2.0", "identity": identity,
        "assignmentHash": canonical_hash(assigned), "bankHash": canonical_hash(bank),
        "trajectory": aggregate_trajectories(rows, len(assigned["episodes"])),
        "byTier": {tier: aggregate_trajectories([r for r in rows if r["tier"] == tier],
                   sum(tasks[t]["tier"] == tier for t in assigned["episodes"])) for tier in ("D1", "D2", "D3", "D4")},
        "bySourceGroup": {group: aggregate_trajectories([r for r in rows if r["sourceGroup"] == group],
                   sum(tasks[t]["sourceGroup"] == group for t in assigned["episodes"]))
                         for group in sorted({t["sourceGroup"] for t in bank["episodes"]})},
        "probes": {
            "assigned": len(assigned["probes"]), "observed": len(probe_records),
            "correct": fraction(sum(correct.get(p, False) for p in discriminative), len(discriminative)),
            "allRowsDescriptive": fraction(sum(correct.values()), len(assigned["probes"])),
            "discriminative": clustered_scores(assigned["probes"], correct, probes, tasks, "discriminative"),
            "calibration": clustered_scores(assigned["probes"], correct, probes, tasks, "calibration"),
            "recoveryCohorts": {cohort: clustered_scores(
                [p for p in discriminative if probes[p].get("recoveryCohort") == cohort],
                correct, probes, tasks) for cohort in
                ("inverse-solvable", "inverse-suboptimal", "inverse-unavailable")},
            "observation": {
                "condition": identity["condition"], "answered": len(probe_scores),
                "acquiredViews": sum(view_counts.values()),
                "meanAcquiredViewsAmongAnswered": fraction(sum(view_counts.values()), len(view_counts)),
                "correctWithoutAcquisition": fraction(sum(correct[p] and view_counts[p] == 0 for p in correct),
                                                       len(assigned["probes"])),
                "byAcquiredViews": {str(n): fraction(sum(correct[p] for p in correct if view_counts[p] == n),
                                                     sum(v == n for v in view_counts.values()))
                                    for n in sorted(set(view_counts.values()))}},
            "byKind": {kind: fraction(
                sum(correct.get(p, False) for p in discriminative if probes[p]["kind"] == kind),
                sum(probes[p]["kind"] == kind for p in discriminative))
                for kind in sorted({p["kind"] for p in probes.values()})}},
        "independentEpisodeSuccess": clustered_scores(
            assigned["episodes"], {t: r["success"] for t, r in by_id.items()}, tasks, tasks),
        "pairedConsistency": {kind: {
            "joint": fraction(sum(p["jointCorrect"] for p in pair_rows if p["kind"] == kind),
                              sum(p["kind"] == kind for p in pair_rows)),
            "observedBoth": sum(p["observedBoth"] for p in pair_rows if p["kind"] == kind)}
            for kind in sorted({p["kind"] for p in bank["pairs"]})},
        "planSurvival": survival, "replanning": {"events": replans,
            "completed": fraction(sum(p["completed"] for p in replans), len(replans))},
        "episodes": rows,
        "interpretation": "D1–D4 are optimal-operation-length bins, not reasoning depth. Report mechanisms, source groups and sampling strata separately; ID seeds are repeated observations."}
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("submission", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    write_json(args.output, evaluate(json.loads(args.submission.read_text())))


if __name__ == "__main__":
    main()
