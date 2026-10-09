"""Seven exact diagnostics, with explicit missing/invalid/censoring denominators."""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from build import load_bank, write_json
from cases import CASES
from engine import minimum_detaches, no_undo
from session import replay_export
from online import trajectory_metrics, aggregate


def fraction(numerator, denominator):
    return {"numerator": numerator, "denominator": denominator,
            "value": numerator / denominator if denominator else None}


def episode_score(domain, task, costs, record):
    table, goal = costs[str(task["goal"])], task["goal"]
    session = replay_export(domain, task, record) if record is not None else None
    events = session.events if session else []
    structural = [e for e in events if e["structural"]]
    success = bool(session and session.terminated and session.state == goal)
    detaches = [e for e in structural if e["code"] == "OK"
                and e["request"]["action"]["type"] == "detach"]
    failed = sum(e["code"] != "OK" for e in structural)
    first_plus = first_budget = repair_action = None
    for e in structural:
        if (first_plus is None and no_undo(task["start"], goal, table)
                and no_undo(e["after"], goal, table) is False):
            first_plus = e["attempt"]
        if first_budget is None and table[e["after"]] > task["budget"] - e["attempt"]:
            first_budget = e["attempt"]
        if (repair_action is None and e["code"] == "OK"
                and e["request"]["action"]["type"] == "detach"
                and minimum_detaches(e["after"], goal, table) < minimum_detaches(e["before"], goal, table)):
            repair_action = e["attempt"]
    # Freeze the first diagnosis while the injected checkpoint is unchanged.
    diagnosis = None
    failed_before_diagnosis = False
    for e in events:
        if e["code"] == "DIAGNOSIS_RECORDED":
            diagnosis = e["request"]["action"]["needsRework"]
            break
        if e["structural"] and e["code"] == "OK":
            break
        failed_before_diagnosis |= e["structural"] and e["code"] != "OK"
    regret_steps = len(structural) - task["optimalActions"] if success else None
    regret_detach = len(detaches) - task["minimumDetaches"] if success else None
    if success and regret_steps != 2 * regret_detach + failed:
        raise ValueError("Trajectory violates unit-action regret conservation")
    return {
        "taskId": task["id"], "case": task["case"], "mode": task["mode"],
        "status": "missing" if session is None else "success" if success else
                  "failure" if session.terminated else "unfinished",
        "success": success, "attempts": len(structural), "budget": task["budget"],
        "optimalActions": task["optimalActions"], "minimumDetaches": task["minimumDetaches"],
        "detachOperations": len(detaches),
        "distinctRemovedParts": len({e["removedPartId"] for e in detaches}),
        "failedAttempts": failed, "actionRegret": regret_steps, "detachRegret": regret_detach,
        "initialNoUndo": no_undo(task["start"], goal, table),
        "initialBudgetFeasible": table[task["start"]] <= task["budget"],
        "firstNoUndoLoss": first_plus, "firstBudgetLoss": first_budget,
        "checkpointDiagnosis": diagnosis,
        "diagnosisAfterFailedAttempt": failed_before_diagnosis if diagnosis is not None else None,
        "firstAppropriateRepairAttempt": repair_action,
        "online": trajectory_metrics(domain, task, table, session),
        "track": record.get("track", "known-pose-structured") if record else None,
    }


def survival(rows, label):
    initial_key, loss_key = (("initialNoRework", "firstNoReworkLoss") if label == "noRework" else
                             ("initialNoUndo", "firstNoUndoLoss") if label == "noUndo"
                             else ("initialBudgetFeasible", "firstBudgetLoss"))
    groups = defaultdict(list)
    for row in rows:
        if row[initial_key]:
            # Do not pool lengths or injected repair/healthy/full protocols.
            groups[(row["case"], row["mode"], row["optimalActions"], row["budget"])].append(row)
    out = []
    for key, members in groups.items():
        curve = []
        for t in range(key[3] + 1):
            failed = sum(r[loss_key] is not None and r[loss_key] <= t for r in members)
            surviving = sum(r["status"] != "missing" and (r[loss_key] is None or r[loss_key] > t)
                            and (r["attempts"] >= t or r["success"]) for r in members)
            censored = len(members) - failed - surviving
            curve.append({"t": t, "survivors": surviving, "firstLoss": failed, "censored": censored,
                          "lower": surviving / len(members),
                          "upper": (surviving + censored) / len(members)})
        out.append({"case": key[0], "mode": key[1], "optimalActions": key[2],
                    "budget": key[3], "n": len(members), "curve": curve})
    return out


def score_choices(probes, answers):
    valid = invalid = missing = plus_loss = budget_loss = 0
    rows = []
    for p in probes:
        answer = answers.get(p["id"])
        status = "missing" if p["id"] not in answers else "invalid"
        if (isinstance(answer, dict) and set(answer) == {"choice"} and type(answer["choice"]) is int
                and 0 <= answer["choice"] < len(p["candidates"])):
            status = "valid"
            label = p["labels"][answer["choice"]]
            plus_loss += label["noUndoLoss"]
            budget_loss += label["budgetLoss"]
            valid += 1
        elif status == "missing":
            missing += 1
        else:
            invalid += 1
        rows.append({"id": p["id"], "status": status})
    n = len(probes)
    return {"noUndoDeadEndRate": fraction(plus_loss, valid),
            "budgetDeadEndRate": fraction(budget_loss, valid),
            "decisionCoverage": fraction(valid, n), "invalidRate": fraction(invalid, n),
            "missing": missing, "unknownLabels": 0,
            "certifiedNoUndoAvoidanceAllAssigned": fraction(valid - plus_loss, n),
            "certifiedBudgetAvoidanceAllAssigned": fraction(valid - budget_loss, n), "rows": rows}


def lookahead_bins(probes, answers, group_key):
    bins = {}
    for horizon in sorted({group_key(p) for p in probes}):
        members = [p for p in probes if group_key(p) == horizon]
        correct = valid = missing = conflict_hit = conflict_valid = false_alarm = control_valid = 0
        positives = sum(p["firstConflict"] is not None for p in members)
        for p in members:
            if p["id"] not in answers:
                missing += 1
                continue
            a = answers[p["id"]]
            if not isinstance(a, dict) or set(a) != {"firstConflict"}:
                continue
            predicted = a["firstConflict"]
            if predicted is not None and not (type(predicted) is int and 1 <= predicted <= len(p["plan"])):
                continue
            valid += 1
            correct += predicted == p["firstConflict"]
            if p["firstConflict"] is not None:
                conflict_valid += 1
                conflict_hit += predicted is not None
            else:
                control_valid += 1
                false_alarm += predicted is not None
        bins[str(horizon)] = {
            "exactFirstConflictAccuracy": fraction(correct, len(members)),
            "responseCoverage": fraction(valid, len(members)), "missing": missing,
            "invalid": len(members) - missing - valid,
            "conflictRecallAllAssigned": fraction(conflict_hit, positives),
            "falseAlarmRateValidControls": fraction(false_alarm, control_valid),
            "controlCoverage": fraction(control_valid, len(members) - positives),
            "conflictCoverage": fraction(conflict_valid, positives),
        }
    return bins


def score_lookahead(probes, answers):
    positions = {p["matchedPair"]: p["firstConflict"] for p in probes if p["firstConflict"] is not None}
    return {"planLengthCurve": lookahead_bins(probes, answers, lambda p: p["horizon"]),
            "distanceCurve": lookahead_bins(probes, answers, lambda p: positions[p["matchedPair"]]),
            "supportedInternalSearchDepth": None,
            "causalDepthOfConflictProbes": None,
            "interpretation": "Distance to conflict on supplied plans; no independent depth claim."}


def score_counterfactual(probes, answers):
    totals = {"switch": [0, 0, 0], "invariance": [0, 0, 0]}
    position_counts = defaultdict(int)
    missing = invalid = valid_members = 0
    rows = []
    for p in probes:
        choices, correct = {}, {}
        for m in p["members"]:
            key = f"{p['id']}/{m['id']}"
            if key not in answers:
                missing += 1
                continue
            a = answers[key]
            if (not isinstance(a, dict) or set(a) != {"choice"} or type(a["choice"]) is not int
                    or not 0 <= a["choice"] < len(p["candidates"])):
                invalid += 1
                continue
            valid_members += 1
            choices[m["id"]] = a["choice"]
            correct[m["id"]] = a["choice"] in m["optimalChoices"]
            position_counts[str(a["choice"])] += 1
        for label, ids in (("switch", p["switchPair"]), ("invariance", p["invariancePair"])):
            complete = all(i in choices for i in ids)
            joint = complete and all(correct[i] for i in ids)
            changed = complete and choices[ids[0]] != choices[ids[1]]
            totals[label][0] += joint
            totals[label][1] += complete
            totals[label][2] += changed
            rows.append({"id": p["id"], "pair": label, "complete": complete,
                         "jointCorrect": joint, "changed": changed if complete else None})
    return {
        "jointCorrectSwitch": fraction(totals["switch"][0], len(probes)),
        "switchRateCompletePairs": fraction(totals["switch"][2], totals["switch"][1]),
        "correctInvariance": fraction(totals["invariance"][0], len(probes)),
        "invarianceRateCompletePairs": fraction(totals["invariance"][1] - totals["invariance"][2],
                                               totals["invariance"][1]),
        "memberCoverage": fraction(valid_members, sum(len(p["members"]) for p in probes)),
        "missing": missing, "invalid": invalid, "canonicalChoiceCounts": dict(position_counts),
        "rows": rows,
    }


def evaluate(submission):
    if not isinstance(submission, dict) or set(submission) - {"schema", "episodes", "choices", "lookahead", "counterfactual", "metadata"}:
        raise ValueError("Invalid submission fields")
    if submission.get("schema") != "brickplan-submission/1.2":
        raise ValueError("Wrong submission schema")
    for section in ("episodes", "choices", "lookahead", "counterfactual"):
        if not isinstance(submission.get(section, {}), dict):
            raise ValueError(f"{section} must be an ID-keyed object")
    if not isinstance(submission.get("metadata", {}), dict):
        raise ValueError("metadata must be an object")
    rows, choices, lookahead, cf, expected_episodes, certificates = [], [], [], [], set(), []
    for config in CASES:
        domain, tasks, costs, cert = load_bank(config["id"])
        certificates.append(cert)
        for task in tasks["episodes"]:
            expected_episodes.add(task["id"])
            rows.append(episode_score(domain, task, costs, submission.get("episodes", {}).get(task["id"])))
            rows[-1].update({k: rows[-1]["online"][k]
                             for k in ("initialNoRework", "firstNoReworkLoss")})
        choices += tasks["choices"]
        lookahead += tasks["lookahead"]
        cf += tasks["counterfactual"]
    expected = {"episodes": expected_episodes, "choices": {p["id"] for p in choices},
                "lookahead": {p["id"] for p in lookahead},
                "counterfactual": {f"{p['id']}/{m['id']}" for p in cf for m in p["members"]}}
    for section, known in expected.items():
        if set(submission.get(section, {})) - known:
            raise ValueError(f"Unknown {section} IDs")
    repairs, healthy = [r for r in rows if r["mode"] == "repair"], [r for r in rows if r["mode"] == "healthy"]
    tp = sum(r["checkpointDiagnosis"] is True for r in repairs)
    fp = sum(r["checkpointDiagnosis"] is True for r in healthy)
    healthy_answered = sum(r["checkpointDiagnosis"] is not None for r in healthy)
    tracks = {r["track"] for r in rows if r["track"] is not None}
    declared = submission.get("metadata", {}).get("track")
    if declared:
        tracks.add(declared)
    if len(tracks) > 1:
        raise ValueError("Do not pool observation tracks; collect and evaluate separate runs")
    return {
        "schema": "brickplan-evaluation/1.2", "metadata": submission.get("metadata", {}),
        "benchmarkRelease": "1.2", "track": next(iter(tracks), None),
        "structures": len(certificates),
        "independentProvenanceGroups": len({c["provenanceGroup"] for c in certificates}),
        "caseCertificates": {c["case"]: c["transitionHash"] for c in certificates},
        "successRate": fraction(sum(r["success"] for r in rows), len(rows)),
        "successByMode": {mode: fraction(sum(r["success"] for r in rows if r["mode"] == mode),
                                         sum(r["mode"] == mode for r in rows))
                          for mode in sorted({r["mode"] for r in rows})},
        "missingEpisodes": sum(r["status"] == "missing" for r in rows),
        "deadEndChoices": score_choices(choices, submission.get("choices", {})),
        "lookahead": score_lookahead(lookahead, submission.get("lookahead", {})),
        "planSurvival": {label: survival(rows, label) for label in ("noUndo", "noRework", "budget")},
        "online": aggregate(rows, fraction),
        "regretDependence": "Action regret = 2 * detach regret + failed attempts; not independent evidence.",
        "regretAndEfficiency": rows,
        "recovery": {
            "detectionRecall": fraction(tp, len(repairs)), "detectionPrecision": fraction(tp, tp + fp),
            "healthyFalseAlarmRate": fraction(fp, healthy_answered),
            "healthyDiagnosisCoverage": fraction(healthy_answered, len(healthy)),
            "repairDiagnosisCoverage": fraction(sum(r["checkpointDiagnosis"] is not None for r in repairs), len(repairs)),
            "completionRate": fraction(sum(r["success"] for r in repairs), len(repairs)),
            "jointDetectionAndCompletion": fraction(sum(r["success"] and r["checkpointDiagnosis"] is True
                                                        for r in repairs), len(repairs)),
            "successfulRepairEfficiency": [r for r in repairs if r["success"]],
        },
        "counterfactual": score_counterfactual(cf, submission.get("counterfactual", {})),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("submission", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    write_json(args.output, evaluate(json.loads(args.submission.read_text())))


if __name__ == "__main__":
    main()
