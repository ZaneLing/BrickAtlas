"""Evaluator-only trajectory diagnostics; never imported by the policy renderer."""
from engine import minimum_detaches, no_undo


def no_rework(state, goal, table):
    """Reach target with each mismatched site changed once."""
    return table[state] >= 0 and table[state] == (state ^ goal).bit_count()


def trajectory_metrics(domain, task, table, session):
    goal = task["goal"]
    decisions, losses, events, diagnoses = [], [], [], []
    active = None
    seen_diagnosis_states = set()
    for e in session.events if session else []:
        before, after = e["before"], e["after"]
        if e["code"] == "DIAGNOSIS_RECORDED":
            if before not in seen_diagnosis_states:
                diagnoses.append({
                    "revision": e["revision"], "prediction": e["request"]["action"]["needsRework"],
                    "truth": not no_rework(before, goal, table),
                })
                seen_diagnosis_states.add(before)
            if active is not None and active["diagnosis"] is None:
                active["diagnosis"] = e["request"]["action"]["needsRework"]
                active["detectionLagAttempts"] = e["attempt"] - active["entryAttempt"]
            continue
        if not e["structural"]:
            continue
        legal = e["code"] == "OK"
        old_budget = table[before] <= task["budget"] - (e["attempt"] - 1)
        new_budget = table[after] <= task["budget"] - e["attempt"]
        old_mono, new_mono = no_rework(before, goal, table), no_rework(after, goal, table)
        row = {"attempt": e["attempt"], "legal": legal, "eligible": {},
               "loss": {}, "code": e["code"]}
        moves = list(domain.moves(before))
        for label, was, now, safe in (
            ("noUndo", no_undo(before, goal, table), no_undo(after, goal, table),
             lambda s: no_undo(s, goal, table)),
            ("noRework", old_mono, new_mono, lambda s: no_rework(s, goal, table)),
            ("budget", old_budget, new_budget,
             lambda s: table[s] <= task["budget"] - e["attempt"]),
        ):
            # Require a legal safe alternative and a legal unsafe alternative.
            options = [bool(safe(s)) for _, _, s in moves]
            row["eligible"][label] = legal and bool(was) and any(options) and not all(options)
            row["loss"][label] = bool(was) and not bool(now)
            if row["loss"][label]:
                losses.append({"attempt": e["attempt"], "kind": label, "legal": legal})
        row["bellmanExcess"] = 1 + table[after] - table[before]
        decisions.append(row)
        if active is not None:
            active["attemptsToRestore"] += 1
            active["detachesToRestore"] += legal and e["request"]["action"]["type"] == "detach"
            if new_mono:
                active.update(outcome="restored", restoreAttempt=e["attempt"],
                              prefixActionExcess=active["attemptsToRestore"] + table[after]
                                                - active["distanceAtEntry"])
                active = None
        if old_mono and not new_mono and legal:
            active = {
                "entryAttempt": e["attempt"], "entryRevision": e["revision"],
                "distanceAtEntry": table[after],
                "minimumDetachesAtEntry": minimum_detaches(after, goal, table),
                "diagnosis": None, "detectionLagAttempts": None,
                "attemptsToRestore": 0, "detachesToRestore": 0,
                "outcome": "terminated_unrestored" if session.terminated else "censored",
                "restoreAttempt": None, "prefixActionExcess": None,
            }
            events.append(active)
    return {"decisions": decisions, "lossEvents": losses, "selfInducedEvents": events,
            "stateDiagnoses": diagnoses,
            "initialNoRework": no_rework(task["start"], goal, table),
            "firstNoReworkLoss": next((e["attempt"] for e in losses if e["kind"] == "noRework"), None)}


def aggregate(rows, fraction):
    decisions = [d for r in rows for d in r["online"]["decisions"]]
    events = [e for r in rows for e in r["online"]["selfInducedEvents"]]
    diagnoses = [e for r in rows for e in r["online"]["stateDiagnoses"]]
    restored = sum(e["outcome"] == "restored" for e in events)
    censored = sum(e["outcome"] == "censored" for e in events)
    return {
        "legalDecisionCount": sum(d["legal"] for d in decisions),
        "eligibleDeadEndChoiceRates": {
            label: fraction(sum(d["eligible"][label] and d["loss"][label] for d in decisions),
                            sum(d["eligible"][label] for d in decisions))
            for label in ("noUndo", "noRework", "budget")},
        "legalActionBellmanExcess": sum(d["bellmanExcess"] for d in decisions if d["legal"]),
        "selfInducedRecovery": {
            "events": len(events), "restored": restored, "censored": censored,
            "restorationRateAllEvents": fraction(restored, len(events)),
            "restorationUpperBound": fraction(restored + censored, len(events)),
            "detectionRecallAllEvents": fraction(sum(e["diagnosis"] is True for e in events), len(events)),
            "diagnosisCoverage": fraction(sum(e["diagnosis"] is not None for e in events), len(events)),
            "jointDetectionAndRestoration": fraction(
                sum(e["diagnosis"] is True and e["outcome"] == "restored" for e in events), len(events)),
        },
        "onlineDiagnosisAccuracy": fraction(sum(e["truth"] == e["prediction"] for e in diagnoses), len(diagnoses)),
        "definition": "Legal choices with both safe and unsafe legal alternatives. Self-induced events begin at no-rework loss; restoration means no-rework feasibility returns. Budget loss is separately irreversible.",
    }
