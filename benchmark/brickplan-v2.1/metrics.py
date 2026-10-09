"""Evaluator-only conditional costs, recovery corridors and assignment census."""
from collections import Counter, deque
from array import array
from dataclasses import asdict

from mission import State


def fraction(numerator, denominator):
    return {"numerator": numerator, "denominator": denominator,
            "value": numerator / denominator if denominator else None}


def optimal_corridor(oracle, checkpoint):
    """All states lying on any optimal completion from the pre-error checkpoint.

    Equivalent to d_forward(checkpoint,x)+d_goal(x)=d_goal(checkpoint).
    Traversing only Bellman-equality edges avoids exploring irrelevant states.
    """
    root = oracle.encode(checkpoint)
    seen, queue = {root}, deque([root])
    while queue:
        node = queue.popleft()
        for _, after in oracle.next(node):
            if after not in seen and oracle.costs[after] == oracle.costs[node] - 1:
                seen.add(after)
                queue.append(after)
    return seen


def repair_distances(oracle, corridor):
    """Exact directed distances to a pre-error corridor, excluding the goal."""
    result = array("i", [-1]) * oracle.size
    queue = deque()
    for node in corridor:
        if node != oracle.target:
            result[node] = 0
            queue.append(node)
    while queue:
        node = queue.popleft()
        p, flags = divmod(node, oracle.width)
        assembly = oracle.graph.states[p]
        predecessors = [neighbor * oracle.width + flags
                        for _, _, neighbor in oracle.graph.edges[p]]
        for j, site in enumerate(oracle.mission.jobs):
            if flags & (1 << j) and not assembly & (1 << site):
                predecessors.append(p * oracle.width + (flags ^ (1 << j)))
        for previous in predecessors:
            if previous != oracle.target and result[previous] < 0:
                result[previous] = result[node] + 1
                queue.append(previous)
    return result


def trajectory_metrics(oracle, session):
    m, task = oracle.mission, session.task
    start = State(**task["start"])
    initial = oracle.distance(start)
    if initial < 0:
        raise ValueError("Unsolvable assigned episode")
    decisions, events, diagnoses = [], [], []
    active, corridor_cache, repair_cache = [], {}, {}
    interval_error, previous_diagnosis_attempt = False, 0
    counts = Counter()
    for event in session.events:
        before, after = State(**event["before"]), State(**event["after"])
        if event["code"] == "DIAGNOSIS_RECORDED":
            prediction = event["request"]["action"]["avoidableError"]
            diagnoses.append({
                "attempt": event["attempt"], "prediction": prediction, "truth": interval_error,
                "sinceAttempt": previous_diagnosis_attempt, "remainingOptimal": oracle.distance(before)})
            for error in events:
                if error["diagnosis"] is None:
                    error["diagnosis"] = prediction
                    error["diagnosisLag"] = event["attempt"] - error["entryAttempt"]
            interval_error = False
            previous_diagnosis_attempt = event["attempt"]
            continue
        if not event["cost"]:
            continue
        legal = event["code"] == "OK"
        cost_before, cost_after = oracle.distance(before), oracle.distance(after)
        if min(cost_before, cost_after) < 0:
            raise ValueError("Retained mission left its certified solvable component")
        excess = event["cost"] + cost_after - cost_before
        if excess < 0:
            raise AssertionError("Negative Bellman excess")
        options = [(action, oracle.distance(target)) for action, target in m.moves(before)]
        q_values = [1 + value - cost_before for _, value in options if value >= 0]
        remaining_before = task["maxActions"] - (event["attempt"] - event["cost"])
        budget_options = [value >= 0 and value <= remaining_before - 1 for _, value in options]
        row = {
            "attempt": event["attempt"], "legal": legal, "code": event["code"],
            "conditionalExtraCost": excess, "remainingOptimal": cost_after,
            "avoidableChoiceEligible": legal and 0 in q_values and any(q > 0 for q in q_values),
            "avoidableCost": legal and excess > 0,
            "budgetChoiceEligible": (legal and cost_before <= remaining_before
                                     and any(budget_options) and not all(budget_options)),
            "budgetViabilityLost": (cost_before <= remaining_before
                                    and cost_after > remaining_before - event["cost"]),
            "genuinelyUnreachable": False,
        }
        decisions.append(row)
        if legal:
            counts[event["internalAction"]["type"]] += 1
        else:
            counts["invalid"] += event["cost"]
        # Every open event is tracked, including overlapping later mistakes.
        for error in active[:]:
            if oracle.encode(after) in corridor_cache[error["checkpointKey"]]:
                error["outcome"] = "restored"
                error["restoreAttempt"] = event["attempt"]
                error["operationsToRestore"] = event["attempt"] - error["entryAttempt"]
                error["recoveryEfficiency"] = error["minimumRecoveryOperations"] / error["operationsToRestore"]
                for delayed in error["delayedCheckpoints"]:
                    delayed["restored"] = True
                    delayed["operationsToRestore"] = event["attempt"] - delayed["attempt"]
                    delayed["efficiency"] = delayed["minimumRepairOperations"] / delayed["operationsToRestore"]
                active.remove(error)
            else:
                lag = event["attempt"] - error["entryAttempt"]
                if lag in (1, 3, 5) and after != m.terminal:
                    key = error["checkpointKey"]
                    if key not in repair_cache:
                        repair_cache[key] = repair_distances(oracle, corridor_cache[key])
                    distance = repair_cache[key][oracle.encode(after)]
                    error["delayedCheckpoints"].append({
                        "lagAfterError": lag, "attempt": event["attempt"],
                        "state": asdict(after), "minimumRepairOperations": distance if distance >= 0 else None,
                        "repairReachable": distance >= 0, "restored": False,
                        "operationsToRestore": None, "efficiency": None})
        if legal and excess > 0:
            interval_error = True
            key = (before.assembly, before.done)
            if key not in corridor_cache:
                corridor_cache[key] = optimal_corridor(oracle, before) - {oracle.target}
            # A structural error is reversibly one step from its checkpoint.
            # Audit edges cannot be costly mistakes: earlier eligible auditing
            # commutes with subsequent physical moves in this mission contract.
            assert any(target == before for _, target in m.moves(after))
            error = {
                "entryAttempt": event["attempt"], "entryRevision": event["revision"],
                "checkpointKey": key, "checkpoint": asdict(before), "stateAfterError": asdict(after),
                "costAdded": excess, "checkpointRemainingOptimal": cost_before,
                "mandatoryReworkBeforeError": cost_before > (
                    (before.assembly ^ m.goal).bit_count() + len(m.pending(before))),
                "minimumRecoveryOperations": 1, "diagnosis": None, "diagnosisLag": None,
                "delayedCheckpoints": [],
                "outcome": "terminated-unrestored" if session.terminated else "censored",
                "restoreAttempt": None, "operationsToRestore": None, "recoveryEfficiency": None}
            events.append(error)
            active.append(error)
    for event in events:
        del event["checkpointKey"]
    success = session.terminated and session.termination == "finish" and session.state == m.terminal
    spent, remaining = session.attempts, oracle.distance(session.state)
    excess = sum(x["conditionalExtraCost"] for x in decisions)
    assert excess == spent + remaining - initial
    decomposition = None
    if success:
        pending = len(m.pending(start))
        balance = m.goal.bit_count() - start.assembly.bit_count()
        value = initial - pending - balance
        assert value >= 0 and value % 2 == 0 and counts["audit"] == pending
        optimal_detaches = value // 2
        decomposition = {
            "necessaryAudits": pending, "actualAudits": counts["audit"],
            "optimalDetaches": optimal_detaches, "actualDetaches": counts["detach"],
            "twiceExcessDetaches": 2 * (counts["detach"] - optimal_detaches),
            "invalidAttempts": counts["invalid"]}
        assert decomposition["twiceExcessDetaches"] + counts["invalid"] == spent - initial
    replans = [
        {"diagnosisAttempt": d["attempt"], "remainingOptimalAtDiagnosis": d["remainingOptimal"],
         "operationsAfterDiagnosis": spent - d["attempt"],
         "residualRegret": spent - d["attempt"] - d["remainingOptimal"] if success else None,
         "completed": success}
        for d in diagnoses if d["prediction"] and d["truth"]]
    return {
        "success": success, "terminated": session.terminated, "operations": spent,
        "optimal": initial, "remainingOptimal": remaining,
        "regret": spent - initial if success else None, "regretDecomposition": decomposition,
        "conditionalExcessTotal": excess, "decisions": decisions, "errorEvents": events,
        "diagnoses": diagnoses, "replanning": replans,
        "firstCostLoss": next((x["attempt"] for x in decisions if x["conditionalExtraCost"]), None),
        "firstIllegal": next((x["attempt"] for x in decisions if not x["legal"]), None),
        "initialMandatoryRework": initial > (
            (start.assembly ^ m.goal).bit_count() + len(m.pending(start))),
    }


def aggregate_trajectories(rows, assigned):
    """Missing and censored assignments remain visible in all denominators."""
    decisions = [d for row in rows for d in row["decisions"]]
    errors = [e for row in rows for e in row["errorEvents"]]
    reports = [d for row in rows for d in row["diagnoses"]]
    restored = [e for e in errors if e["outcome"] == "restored"]
    censored = [e for e in errors if e["outcome"] == "censored"]
    completed = [row for row in rows if row["success"]]
    return {
        "census": {"assigned": assigned, "observed": len(rows), "missing": assigned - len(rows),
                   "terminated": sum(r["terminated"] for r in rows),
                   "censored": sum(not r["terminated"] for r in rows)},
        "success": fraction(len(completed), assigned),
        "avoidableCostChoiceRate": fraction(
            sum(d["avoidableChoiceEligible"] and d["avoidableCost"] for d in decisions),
            sum(d["avoidableChoiceEligible"] for d in decisions)),
        "budgetLossChoiceRate": fraction(
            sum(d["budgetChoiceEligible"] and d["budgetViabilityLost"] for d in decisions),
            sum(d["budgetChoiceEligible"] for d in decisions)),
        "genuineUnreachableChoiceRate": fraction(0, 0),
        "unreachabilityScope": "All legal actions preserve solvability in retained components. This release has no genuine irreversible dead-end choices.",
        "successfulMeanRegret": sum(r["regret"] for r in completed) / len(completed) if completed else None,
        "recovery": {
            "events": len(errors), "restored": len(restored), "censored": len(censored),
            "rateLower": fraction(len(restored), len(errors)),
            "rateUpper": fraction(len(restored) + len(censored), len(errors)),
            "meanEfficiencyWhenRestored": (sum(e["recoveryEfficiency"] for e in restored) / len(restored)
                                            if restored else None),
            "diagnosed": fraction(sum(e["diagnosis"] is True for e in errors), len(errors)),
            "definition": "Return to a NONTERMINAL pre-error optimal corridor state. Goal is excluded. Immediate inverse-operation efficiency is secondary.",
            "delayedCohorts": {
                str(lag): {
                    "eligible": len(cohort := [d for e in errors for d in e["delayedCheckpoints"]
                                             if d["lagAfterError"] == lag]),
                    "restored": sum(d["restored"] for d in cohort),
                    "unreachable": sum(not d["repairReachable"] for d in cohort),
                    "meanMinimumRepair": (sum(values) / len(values) if
                        (values := [d["minimumRepairOperations"] for d in cohort if d["repairReachable"]]) else None),
                    "meanEfficiencyWhenRestored": (sum(values) / len(values) if
                        (values := [d["efficiency"] for d in cohort if d["restored"]]) else None)}
                for lag in (1, 3, 5)}},
        "diagnosisAccuracy": fraction(sum(d["prediction"] == d["truth"] for d in reports), len(reports)),
        "conditionalExcessAllObserved": sum(r["conditionalExcessTotal"] for r in rows),
    }


def score_probe(probe, answer):
    if not isinstance(answer, dict):
        return {"answered": False, "correct": False}
    if "choices" in probe:
        choice = answer.get("choice")
        valid = type(choice) is int and 0 <= choice < len(probe["choices"])
        return {"answered": valid, "correct": valid and choice in probe["optimalChoices"],
                "extraCost": probe["labels"][choice]["conditionalExtraCost"] if valid else None}
    value = answer.get("firstConflict")
    valid = (set(answer) == {"firstConflict"}
             and (value is None or type(value) is int and 1 <= value <= len(probe["plan"])))
    return {"answered": valid, "correct": valid and value == probe["firstConflict"]}
