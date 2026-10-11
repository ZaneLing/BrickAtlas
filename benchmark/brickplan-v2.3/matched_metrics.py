"""Exact paired metrics for v2.3; pure functions, no bank or oracle I/O.

Call after authoritative transcript replay. A partially assigned pair enters the
denominator with zero joint credit; an entirely unassigned pair is census-only.
Starts, interventions, and sources are nested units, not independent repeats.
"""
from collections import Counter, defaultdict
from collections.abc import Mapping
import hashlib
import json
import math
import random


PRIMARY = "primary-matched"
HISTORICAL = "historical-unmatched-regression"
SPLITS = ("development", "heldout-source")
MATCH_FLAGS = (
    "equalPartCount", "sameRemovedPartTypes",
    "sameRemovedPartTypeColorInventory", "sameRetainedPartTypeColorInventory",
)


def fingerprint(value):
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def fraction(numerator, denominator):
    return {"numerator": numerator, "denominator": denominator,
            "value": numerator / denominator if denominator else None}


def _index(rows, name):
    result = {}
    for row in rows:
        key = row.get("id")
        if not isinstance(key, str) or not key or key in result:
            raise ValueError(f"Invalid or duplicate {name} ID: {key!r}")
        result[key] = row
    return result


def valid_answer(answer, plan_length):
    return (isinstance(answer, dict) and set(answer) == {"firstConflict"}
            and (answer["firstConflict"] is None
                 or type(answer["firstConflict"]) is int
                 and 1 <= answer["firstConflict"] <= plan_length))


def visual_pair_definitions(bank):
    """Validate and normalize visual pairs, including explicit legacy fallback.

    Prefer construction's interventionId. Otherwise the unordered pair of
    context profiles plus removed original instances identifies an intervention.
    A start key uses actual task inputs, not a row ID or an answer.
    """
    probes = _index(bank["probes"], "probe")
    tasks = _index(bank["episodes"], "episode")
    pairs = _index(bank["pairs"], "pair")
    result, used_members, source_splits, intervention_contexts = [], set(), {}, {}
    context_interventions = {}
    for pair in pairs.values():
        if pair["kind"] != "visual-geometry":
            continue
        members = pair["members"]
        if (not isinstance(members, list) or len(members) != 2
                or any(not isinstance(p, str) or p not in probes for p in members)
                or len(set(members)) != 2 or used_members.intersection(members)):
            raise ValueError(f"Invalid or reused visual pair members: {pair['id']}")
        used_members.update(members)
        ps = [probes[p] for p in members]
        ts = [tasks[p["taskId"]] for p in ps]
        for p in ps:
            if ("choices" in p or p.get("kind") != "geometry-continuation"
                    or "firstConflict" not in p
                    or not valid_answer({"firstConflict": p["firstConflict"]}, len(p["plan"]))):
                raise ValueError(f"Visual member needs an exact firstConflict label: {p['id']}")
        if ps[0]["firstConflict"] == ps[1]["firstConflict"]:
            raise ValueError(f"Visual pair is not answer-changing: {pair['id']}")
        source, split = ts[0]["sourceGroup"], ts[0]["split"]
        if not isinstance(source, str) or not source or split not in SPLITS:
            raise ValueError(f"Invalid source/split: {pair['id']}")
        for item in [*ts, pair]:
            if (item.get("sourceGroup", source) != source
                    or item.get("split", split) != split):
                raise ValueError(f"Pair crosses sources or splits: {pair['id']}")
        if source in source_splits and source_splits[source] != split:
            raise ValueError(f"Source appears in development and heldout: {source}")
        source_splits[source] = split
        cohort = pair.get("evaluationCohort")
        inferred = cohort is None
        if inferred:
            if pair.get("introducedVersion") == "2.3":
                raise ValueError(f"v2.3 pair needs an explicit evaluationCohort: {pair['id']}")
            cohort = HISTORICAL
        if cohort not in (PRIMARY, HISTORICAL):
            raise ValueError(f"Unknown visual evaluationCohort: {cohort}")
        context = pair.get("fixedContext", {})
        if cohort == PRIMARY:
            if (pair.get("introducedVersion") != "2.3"
                    or any(context.get(flag) is not True for flag in MATCH_FLAGS)):
                raise ValueError(f"Primary pair lacks v2.3 matching contract: {pair['id']}")
            if (ps[0]["plan"] != ps[1]["plan"] or ps[0]["state"] != ps[1]["state"]
                    or any(ts[0][key] != ts[1][key] for key in ("goal", "capacity", "jobs"))):
                raise ValueError(f"Primary pair changes non-context task inputs: {pair['id']}")
        removed = context.get("removedSourceIndices")
        if (not isinstance(removed, list) or len(removed) != 2
                or any(not isinstance(r, list) or any(type(i) is not int for i in r)
                       or len(set(r)) != len(r) for r in removed)):
            raise ValueError(f"Missing or invalid removedSourceIndices: {pair['id']}")
        # Member presentation can be shuffled independently of manifest order.
        context_key = fingerprint({
            "profiles": sorted(t["profile"] for t in ts),
            "removedSourceIndices": sorted(sorted(r) for r in removed),
        })
        intervention = pair.get("interventionId", context_key)
        if not isinstance(intervention, str) or not intervention:
            raise ValueError("interventionId must be a nonempty string")
        group = (cohort, source, intervention)
        if group in intervention_contexts and intervention_contexts[group] != context_key:
            raise ValueError(f"interventionId aliases different contexts: {intervention}")
        intervention_contexts[group] = context_key
        context_group = (cohort, source, context_key)
        if (context_group in context_interventions
                and context_interventions[context_group] != intervention):
            raise ValueError("Same context pair has multiple intervention IDs")
        context_interventions[context_group] = intervention
        starts = [{"profile": t["profile"], "state": p["state"], "plan": p["plan"],
                   "goal": t["goal"], "capacity": t["capacity"], "jobs": t["jobs"]}
                  for p, t in zip(ps, ts)]
        result.append({
            "pairId": pair["id"], "members": list(members), "sourceGroup": source,
            "split": split, "evaluationCohort": cohort, "cohortInferred": inferred,
            "interventionId": intervention, "startId": fingerprint(sorted(starts, key=fingerprint)),
        })
    return sorted(result, key=lambda row: row["pairId"])


def hierarchical_pair_weights(rows):
    """Weights sum to one: source -> intervention -> distinct start -> repeat."""
    sources = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for row in rows:
        sources[row["sourceGroup"]][row["interventionId"]][row["startId"]].append(row["pairId"])
    weights = {}
    for interventions in sources.values():
        for starts in interventions.values():
            for pair_ids in starts.values():
                for pair_id in pair_ids:
                    if pair_id in weights:
                        raise ValueError(f"Duplicate pair row: {pair_id}")
                    weights[pair_id] = 1 / (len(sources) * len(interventions)
                                           * len(starts) * len(pair_ids))
    return weights


def _quantile(ordered, probability):
    position = (len(ordered) - 1) * probability
    lower, upper = math.floor(position), math.ceil(position)
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)


def source_cluster_bootstrap(source_means, *, seed=0, samples=2000, confidence=0.95):
    """Percentile bootstrap of equally weighted whole-source clusters.

    No row/seed resampling. With fewer than two independent sources the point
    estimate is retained but the interval is null, not a degenerate fake CI.
    """
    if type(seed) is not int or not 0 <= seed < 2**32:
        raise ValueError("seed must be an unsigned 32-bit integer")
    if type(samples) is not int or samples < 0:
        raise ValueError("samples must be a nonnegative integer")
    if (isinstance(confidence, bool) or not isinstance(confidence, (int, float))
            or not math.isfinite(confidence) or not 0 < confidence < 1):
        raise ValueError("confidence must be finite and between zero and one")
    if (not isinstance(source_means, Mapping)
            or any(not isinstance(key, str) or not key for key in source_means)):
        raise ValueError("source_means must map nonempty source IDs to probabilities")
    values = [source_means[key] for key in sorted(source_means)]
    if any(not isinstance(v, (int, float)) or not math.isfinite(v) or not 0 <= v <= 1
           for v in values):
        raise ValueError("Source means must be finite probabilities")
    n = len(values)
    result = {
        "method": "source-cluster-percentile", "seed": seed, "requestedSamples": samples,
        "resamples": 0, "confidence": confidence, "independentSources": n,
        "estimate": sum(values) / n if n else None, "lower": None, "upper": None,
        "status": ("no-assigned-sources" if not n else "fewer-than-two-sources" if n < 2
                   else "disabled" if not samples else "ok"),
        "scope": "Conditional on retained sources/interventions and assignments; not a population guarantee.",
    }
    if n >= 2 and samples:
        rng = random.Random(seed)
        draws = sorted(sum(rng.choice(values) for _ in range(n)) / n for _ in range(samples))
        alpha = (1 - confidence) / 2
        result.update(lower=_quantile(draws, alpha), upper=_quantile(draws, 1 - alpha),
                      resamples=samples)
    return result


def _summary(rows, seed, samples, confidence):
    active = [r for r in rows if r["assignedMembers"]]
    groups = defaultdict(list)
    for row in active:
        groups[(row["sourceGroup"], row["interventionId"], row["startId"])].append(
            float(row["jointCorrect"]))
    interventions = defaultdict(list)
    for (source, intervention, _), values in groups.items():
        interventions[(source, intervention)].append(sum(values) / len(values))
    sources = defaultdict(list)
    for (source, _), values in interventions.items():
        sources[source].append(sum(values) / len(values))
    means = {s: sum(v) / len(v) for s, v in sources.items()}
    counts = Counter(r["assignmentStatus"] for r in rows)
    incomplete = [r for r in active if r["assignedMembers"] < 2 or r["validAnswers"] < 2]
    return {
        "census": {
            "bankPairs": len(rows), "eligiblePairs": len(active),
            "fullyAssignedPairs": counts["both"], "oneSidedPairs": counts["one-sided"],
            "unassignedPairs": counts["neither"],
            "bankSources": len({r["sourceGroup"] for r in rows}),
            "bankInterventions": len({(r["sourceGroup"], r["interventionId"]) for r in rows}),
            "bankDistinctStarts": len({(r["sourceGroup"], r["interventionId"], r["startId"])
                                       for r in rows}),
            "assignedMembers": sum(r["assignedMembers"] for r in rows),
            "missingAssignedResponses": sum(len(r["missingResponseMembers"]) for r in rows),
            "invalidResponses": sum(len(r["invalidResponseMembers"]) for r in rows),
            "observedBoth": sum(r["observedMembers"] == 2 for r in rows),
            "validBoth": sum(r["validAnswers"] == 2 for r in rows),
            "incompletePairIds": [r["pairId"] for r in incomplete],
            "oneSidedPairIds": [r["pairId"] for r in rows if r["assignmentStatus"] == "one-sided"],
            "unassignedPairIds": [r["pairId"] for r in rows if not r["assignedMembers"]],
        },
        "pairMicro": fraction(sum(r["jointCorrect"] for r in active), len(active)),
        "independentStarts": len(groups), "independentInterventions": len(interventions),
        "independentSources": len(sources),
        "interventionMacro": fraction(sum(sum(v) / len(v) for v in interventions.values()),
                                      len(interventions)),
        "sourceMacro": fraction(sum(means.values()), len(means)),
        "bySource": {s: {"interventions": len(sources[s]), "accuracy": means[s]}
                     for s in sorted(sources)},
        "uncertainty": source_cluster_bootstrap(means, seed=seed, samples=samples,
                                                 confidence=confidence),
        "leaveOneSourceOut": {
            s: (sum(v for key, v in means.items() if key != s) / (len(means) - 1)
                if len(means) > 1 else None) for s in sorted(means)},
    }


def matched_pair_scores(bank, assigned, answers, *, seed=0, samples=2000, confidence=0.95):
    """Score raw normalized answers, not correctness booleans or answer flips.

    `assigned` is the complete run's probe-ID list. `answers` maps observed probe
    IDs to raw answer dictionaries after replay. Missing/malformed answers are
    zero, including a missing unassigned partner of a one-sided assignment.
    Nonvisual probes may be present and do not enter these metrics.
    """
    definitions = visual_pair_definitions(bank)
    probes = _index(bank["probes"], "probe")
    if (not isinstance(assigned, (list, tuple))
            or any(not isinstance(p, str) for p in assigned)
            or len(set(assigned)) != len(assigned) or not set(assigned) <= probes.keys()):
        raise ValueError("Invalid or duplicate probe assignments")
    assigned = set(assigned)
    if not isinstance(answers, Mapping) or not answers.keys() <= assigned:
        raise ValueError("Unassigned probe response")
    rows = []
    for definition in definitions:
        members = definition["members"]
        assigned_members = [p for p in members if p in assigned]
        observed = [p for p in members if p in answers]
        valid = [p for p in observed if valid_answer(answers[p], len(probes[p]["plan"]))]
        correct = [p for p in valid if answers[p]["firstConflict"] == probes[p]["firstConflict"]]
        rows.append({
            **definition, "assignedMembers": len(assigned_members),
            "assignmentStatus": "both" if len(assigned_members) == 2 else
                                "one-sided" if assigned_members else "neither",
            "observedMembers": len(observed), "validAnswers": len(valid),
            "correctMembers": len(correct), "jointCorrect": len(correct) == 2,
            "unassignedMembers": [p for p in members if p not in assigned],
            "missingResponseMembers": [p for p in assigned_members if p not in answers],
            "invalidResponseMembers": [p for p in observed if p not in valid],
        })
    cohorts = {}
    for cohort in (PRIMARY, HISTORICAL):
        selected = [r for r in rows if r["evaluationCohort"] == cohort]
        cohorts[cohort] = {
            "all": _summary(selected, seed, samples, confidence),
            "bySplit": {split: _summary([r for r in selected if r["split"] == split],
                                        seed, samples, confidence) for split in SPLITS},
        }
    return {
        "schema": "brickplan-matched-metrics/2.3", "metric": "joint-exact-firstConflict",
        "cohorts": cohorts, "pairs": rows,
        "denominatorRule": (
            "Any assigned member makes a pair eligible. Both exact labels must be correct; "
            "unassigned partners, missing responses and invalid answers score zero. "
            "Wholly unassigned pairs are census-only. Average repeated rows within distinct "
            "starts, starts within interventions, interventions within sources, then sources. "
            "Never pool primary and historical cohorts or treat run/ID seeds as sources."),
    }
