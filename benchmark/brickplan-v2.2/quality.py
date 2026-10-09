"""Private discrimination, public-rule controls, and independent scoring units.

These annotations never enter a policy observation. Missing assignments retain
their weight; repeated appearances/IDs cannot multiply an independent problem.
"""
from collections import Counter, defaultdict

from mission import AssemblyDomain, canonical_hash
from metrics import fraction


def inverse_last(history, candidates):
    """Use only executed public history and offered public actions."""
    if not history or history[-1]["type"] not in ("attach", "detach"):
        return None
    last = history[-1]
    inverse_type = "detach" if last["type"] == "attach" else "attach"
    identity_key = "site" if "site" in last else "partId"
    return next((i for i, a in enumerate(candidates)
                 if a["type"] == inverse_type and a[identity_key] == last[identity_key]), None)


def annotate(bank, data):
    geometries = {}
    for p in bank["profiles"]:
        d = AssemblyDomain.load(data / p["id"])
        geometries[p["id"]] = canonical_hash({
            "parts": [(x["sourceIndex"], x["partNumber"], x["rawMatrix"]) for x in d.parts],
            "mutableSourceIndices": [d.parts[i]["sourceIndex"] for i in d.mutable],
            "directions": [d.parts[i]["direction"] for i in d.mutable],
            "sourceGroup": p["sourceGroup"],
        })
    tasks = {t["id"]: t for t in bank["episodes"]}
    for t in tasks.values():
        t["canonicalProblem"] = canonical_hash({
            "geometry": geometries[t["profile"]], "start": t["start"],
            "goal": t["goal"], "jobs": t["jobs"], "capacity": t["capacity"]})
    for p in bank["probes"]:
        t = tasks[p["taskId"]]
        choice = "choices" in p
        p["scoringRole"] = ("calibration" if choice and
                            len(p["optimalChoices"]) == len(p["choices"]) else "discriminative")
        p["canonicalProblem"] = canonical_hash({
            "geometry": geometries[t["profile"]], "state": p["state"], "goal": t["goal"],
            "jobs": t["jobs"], "capacity": t["capacity"],
            "question": "repair" if p["kind"] == "delayed-repair" else "choice" if choice else "continuation",
            **{k: p[k] for k in ("choices", "plan", "checkpoint", "history") if k in p}})
        if p["kind"] == "delayed-repair":
            index = inverse_last(p["history"], p["choices"])
            p["inverseLastControl"] = {
                "choice": index, "available": index is not None,
                "correct": index in p["optimalChoices"],
                "extraCost": p["labels"][index]["conditionalExtraCost"] if index is not None else None}
            p["recoveryCohort"] = ("inverse-solvable" if index in p["optimalChoices"] else
                                   "inverse-suboptimal" if index is not None else "inverse-unavailable")
    probes = bank["probes"]
    repair = [p for p in probes if p["kind"] == "delayed-repair"]
    next_action = [p for p in probes if p["kind"] == "next-action"]
    h1 = [p["horizonEvidence"]["1"] for p in next_action]
    duplicate = defaultdict(list)
    for p in probes:
        duplicate[p["canonicalProblem"]].append(p["id"])
    return {
        "schema": "brickplan-quality/2.2",
        "episodes": len(tasks), "independentEpisodes": len({t["canonicalProblem"] for t in tasks.values()}),
        "probes": len(probes), "independentProblems": len(duplicate),
        "sourceGroups": len({t["sourceGroup"] for t in tasks.values()}),
        "calibration": [p["id"] for p in probes if p["scoringRole"] == "calibration"],
        "discriminative": sum(p["scoringRole"] == "discriminative" for p in probes),
        "duplicateGroups": [ids for ids in duplicate.values() if len(ids) > 1],
        "duplicateExcess": sum(len(ids) - 1 for ids in duplicate.values()),
        "inverseLast": {
            "scope": "Public executed history and candidate list only; missing inverse scores zero.",
            "accuracy": fraction(sum(p["inverseLastControl"]["correct"] for p in repair), len(repair)),
            "available": sum(p["inverseLastControl"]["available"] for p in repair),
            "cohorts": dict(Counter(p["recoveryCohort"] for p in repair)),
            "byLag": {str(lag): fraction(sum(p["inverseLastControl"]["correct"] for p in repair
                                           if p["lagAfterError"] == lag),
                                       sum(p["lagAfterError"] == lag for p in repair))
                      for lag in (1, 3, 5)}},
        "depthOne": {
            "scope": "Privileged exact structural relations and current legal moves; not image-model performance.",
            "questions": len(h1), "containsOptimal": sum(x["anyOptimal"] for x in h1),
            "allTiesOptimal": sum(x["allOptimal"] for x in h1),
            "uniformTieExpectedAccuracy": fraction(sum(x["optimalFractionUnderUniformTies"] for x in h1), len(h1)),
            "tieSizes": dict(Counter(x["tiedChoices"] for x in h1)),
            "uniformAllCandidates": fraction(sum(len(p["optimalChoices"]) / len(p["choices"])
                                                 for p in next_action), len(next_action))},
        "denominatorRule": "Discriminative scores exclude calibration. Average all assigned variants in each canonical problem, then problems within a source, then sources. Missing responses score zero."}


def clustered_scores(assigned, scores, definitions, tasks, role=None):
    groups = defaultdict(list)
    for key in assigned:
        p = definitions[key]
        if role and p.get("scoringRole") != role:
            continue
        source = tasks[p["taskId"]]["sourceGroup"] if "taskId" in p else p["sourceGroup"]
        groups[(source, p["canonicalProblem"])].append(float(scores.get(key, False)))
    sources = defaultdict(list)
    for (source, _), values in groups.items():
        sources[source].append(sum(values) / len(values))
    means = {s: sum(v) / len(v) for s, v in sources.items()}
    return {
        "assignedRows": sum(len(x) for x in groups.values()),
        "independentProblems": len(groups), "independentSources": len(sources),
        "problemMacro": fraction(sum(sum(x) / len(x) for x in groups.values()), len(groups)),
        "sourceMacro": fraction(sum(means.values()), len(means)),
        "bySource": {s: {"problems": len(sources[s]), "accuracy": means[s]} for s in sorted(sources)}}
