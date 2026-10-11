"""Reduced-input certificates and offline controls, never model/human evidence.

Certificates inspect labels to compute finite-bank deterministic ceilings. They
are NOT fitted heldout predictors. Source-majority fitting receives development
labels only. Inventory rules receive no labels, poses, edges, or transition API.
"""
import argparse
from collections import Counter, defaultdict
import copy
import itertools
import json
import math
from pathlib import Path

from matched_metrics import (
    HISTORICAL, PRIMARY, SPLITS, fingerprint, fraction, hierarchical_pair_weights,
    matched_pair_scores, visual_pair_definitions,
)


def _label_order(label):
    return -1 if label is None else label


def _mode(counts):
    return min(counts, key=lambda label: (-counts[label], _label_order(label)))


def _different_paths(a, b, path="$"):
    if type(a) is not type(b):
        return [path]
    if isinstance(a, dict):
        return [item for key in sorted(a.keys() | b.keys())
                for item in ([f"{path}.{key}"] if key not in a or key not in b else
                             _different_paths(a[key], b[key], f"{path}.{key}"))]
    if isinstance(a, list) and len(a) == len(b):
        return [item for i, (x, y) in enumerate(zip(a, b))
                for item in _different_paths(x, y, f"{path}[{i}]")]
    return [] if a == b else [path]


def _joint_bound(pair_rows, keys, labels, weights, maximum_assignments):
    """Solve small equivalence-class components exactly; bound larger ones.

    A feasible pair contributes a conjunction of one or two class-label
    assignments. Conflicting pairs with the same representation are impossible.
    Component enumeration avoids claiming that incompatible pairwise optima are
    simultaneously achievable by a single deterministic classifier.
    """
    factors, adjacency, options = [], defaultdict(set), defaultdict(set)
    for row in pair_rows:
        a, b = row["members"]
        if keys[a] == keys[b] and labels[a] != labels[b]:
            continue
        required = {keys[a]: labels[a], keys[b]: labels[b]}
        factors.append((required, weights[row["pairId"]]))
        for key, label in required.items():
            adjacency[key].update(required)
            options[key].add(label)
    components, unseen = [], set(adjacency)
    while unseen:
        stack, component = [min(unseen)], set()
        while stack:
            key = stack.pop()
            if key not in component:
                component.add(key)
                stack.extend(adjacency[key] - component)
        unseen -= component
        components.append(sorted(component))
    lowers, uppers, evaluated, witness = [], [], 0, {}
    for component in components:
        local = [(required, weight) for required, weight in factors
                 if next(iter(required)) in component]

        def score(assignment):
            return math.fsum(weight for required, weight in local
                             if all(assignment[key] == label for key, label in required.items()))

        choices = [sorted(options[key], key=_label_order) for key in component]
        space = math.prod(map(len, choices))
        best = dict(zip(component, (values[0] for values in choices)))
        best_score = score(best)
        exact = space <= maximum_assignments - evaluated
        if exact:
            for values in itertools.product(*choices):
                candidate = dict(zip(component, values))
                value = score(candidate)
                if value > best_score:
                    best, best_score = candidate, value
            evaluated += space
        else:
            # A concrete feasible classifier remains a lower bound, never a CI.
            for required, _ in local:
                candidate = {**best, **required}
                value = score(candidate)
                if value > best_score:
                    best, best_score = candidate, value
        witness.update(best)
        lowers.append(best_score)
        uppers.append(best_score if exact else math.fsum(weight for _, weight in local))
    for key in sorted(set(keys.values()) - witness.keys()):
        witness[key] = min((labels[p] for p in keys if keys[p] == key), key=_label_order)
    lower, upper, total = math.fsum(lowers), math.fsum(uppers), math.fsum(weights.values())
    tight = math.isclose(lower, upper, rel_tol=0, abs_tol=1e-12)
    return {
        "upperBound": fraction(upper, total), "achievable": fraction(lower, total),
        "tight": tight, "status": "exact" if tight else "enumeration-budget",
        "enumeratedAssignments": evaluated, "maximumAssignments": maximum_assignments,
        "witnessClassLabels": witness,
    }


def equivalence_certificate(pair_rows, representations, labels, *, maximum_assignments=100000):
    """Certify the explicitly supplied representation, including joint conflicts.

    Member modal ceilings are always tight/achievable on this finite label set.
    The joint ceiling uses the primary metric's hierarchical source weights.
    If exact enumeration is too large, its upper bound is explicitly not called
    achievable; a separate concrete witness supplies an achievable lower bound.
    """
    if type(maximum_assignments) is not int or maximum_assignments < 0:
        raise ValueError("maximum_assignments must be a nonnegative integer")
    members = [p for row in pair_rows for p in row["members"]]
    if len(set(members)) != len(members):
        raise ValueError("Certificate needs unique pair members")
    if any(p not in representations or p not in labels for p in members):
        raise ValueError("Missing representation or label")
    if any(labels[p] is not None and (type(labels[p]) is not int or labels[p] < 1)
           for p in members):
        raise ValueError("Labels must be null or positive integer conflict indices")
    keys = {p: fingerprint(representations[p]) for p in members}
    weights = hierarchical_pair_weights(pair_rows)
    member_weights = {p: weights[row["pairId"]] / 2
                      for row in pair_rows for p in row["members"]}
    classes = defaultdict(list)
    for p in members:
        classes[keys[p]].append(p)
    records, micro_max, weighted_maxima = [], 0, []
    for key, ids in sorted(classes.items()):
        counts = Counter(labels[p] for p in ids)
        weighted = {label: math.fsum(member_weights[p] for p in ids if labels[p] == label)
                    for label in counts}
        modal, weighted_modal = _mode(counts), _mode(weighted)
        micro_max += counts[modal]
        weighted_maxima.append(weighted[weighted_modal])
        records.append({
            "representationHash": key, "members": sorted(ids),
            "labelCounts": [{"firstConflict": label, "count": counts[label],
                             "sourceWeight": weighted[label]}
                            for label in sorted(counts, key=_label_order)],
            "microModalLabel": modal, "sourceWeightedModalLabel": weighted_modal,
        })
    witnesses = []
    for row in pair_rows:
        a, b = row["members"]
        same, differ = keys[a] == keys[b], labels[a] != labels[b]
        witnesses.append({
            "pairId": row["pairId"], "representationHashes": [keys[a], keys[b]],
            "identicalRepresentation": same, "labelsDiffer": differ,
            "firstConflictLabels": [labels[a], labels[b]],
            "jointDeterministicallyImpossible": same and differ,
            "differingPaths": _different_paths(representations[a], representations[b]),
        })
    return {
        "pairs": len(pair_rows), "members": len(members),
        "equivalenceClasses": records, "pairCertificates": witnesses,
        "identicalRepresentationPairs": sum(w["identicalRepresentation"] for w in witnesses),
        "impossibleJointPairs": sum(w["jointDeterministicallyImpossible"] for w in witnesses),
        "memberMicroUpperBound": fraction(micro_max, len(members)),
        "memberSourceMacroUpperBound": fraction(math.fsum(weighted_maxima),
                                                math.fsum(member_weights.values())),
        "jointSourceMacro": _joint_bound(pair_rows, keys, labels, weights, maximum_assignments),
        "interpretation": (
            "Label-aware finite-bank information ceiling, not heldout fitted accuracy. "
            "A deterministic single-member function gives the same prediction on equal "
            "representations; unequal exact labels therefore preclude joint correctness. "
            "This does not constrain a richer representation, stochastic policy, or "
            "classifier using pair position/assignment identity as an extra input."),
    }


def _inventory(parts, presence=False):
    counts = Counter((str(p["partNumber"]), str(p["colorCode"])) for p in parts)
    return [{"partNumber": part, "colorCode": color, "count": 1 if presence else count}
            for (part, color), count in sorted(counts.items())]


def reduced_representations(public, geometry, state, goal):
    """Project exact global inventories, sequence, and initial image-track text.

    Geometry is used only to enumerate inventory and named occupancy. No matrix,
    direction, connectivity, support edge, or removed-instance ID is included.
    Exact inventory availability is a privileged perception abstraction.
    """
    observation = public["observation"]
    if observation["track"] not in ("image-id", "image-id-active"):
        raise ValueError("Metadata certificates require an image-track public payload")
    if any(key in observation for key in ("sites", "fixed", "images")):
        raise ValueError("Pass Probe.public(False), without structured geometry or images")
    parts, mutable = geometry["parts"], geometry["mutable"]
    mutable_set = set(mutable)
    if (len(mutable_set) != len(mutable)
            or any(type(i) is not int or not 0 <= i < len(parts) for i in mutable)):
        raise ValueError("Invalid registered inventory")
    installed = [parts[local] for site, local in enumerate(mutable)
                 if state["assembly"] & (1 << site)]
    rack = [parts[local] for site, local in enumerate(mutable)
            if not state["assembly"] & (1 << site)]
    populations = {
        "fixed": [p for i, p in enumerate(parts) if i not in mutable_set],
        "registered": [parts[i] for i in mutable], "installed": installed, "rack": rack,
        "target": [parts[local] for site, local in enumerate(mutable) if goal & (1 << site)],
    }
    metadata = copy.deepcopy(public)
    # Addresses are independently randomized routing handles, not scene content.
    metadata.pop("id", None)
    metadata["observation"].pop("taskId", None)
    metadata["observation"].pop("sessionId", None)
    counts = {name: len(values) for name, values in populations.items()}
    counts.update(totalAssembly=len(populations["fixed"]) + len(installed),
                  rackCapacity=observation["rack"]["capacity"],
                  planLength=len(public["proposedPlan"]))
    inventories = {name: _inventory(values) for name, values in populations.items()}
    return {
        "count-only": counts,
        "part-type-color-presence": {name: _inventory(values, True)
                                     for name, values in populations.items()},
        "part-type-color-count": inventories,
        "sequence-only": public["proposedPlan"],
        "public-metadata": metadata,
        "public-metadata-and-inventory": {"metadata": metadata, "inventory": inventories},
        "public-metadata-with-addresses": copy.deepcopy(public),
    }


def inventory_state_continuation(public):
    """Optimistically execute public occupancy/rack/work-order rules only.

    Named initial occupancy is optional. Without it, count-only text can infer
    all-in/all-out states and later touched pieces, but not general site presence.
    A null prediction means no non-geometric violation found, not proven legality.
    """
    observation, plan = public["observation"], public["proposedPlan"]
    ids = observation["partIds"]
    registration = {r["partId"]: r["siteId"] for r in observation["registration"]}
    occupied = observation["rack"]["occupiedHolders"]
    capacity = observation["rack"]["capacity"]
    installed = {part: True if occupied == 0 else False if occupied == len(ids) else None
                 for part in ids}
    for site in observation.get("sites", []):
        installed[site["registeredPartId"]] = site["installed"]
    jobs = {job["partId"]: job["completed"] for job in observation["workOrders"]}

    def propagate():
        unknown = [part for part, present in installed.items() if present is None]
        detached_unknown = occupied - sum(value is False for value in installed.values())
        if not 0 <= detached_unknown <= len(unknown):
            return False
        if detached_unknown == 0 or detached_unknown == len(unknown):
            for part in unknown:
                installed[part] = detached_unknown == 0
        return True

    if not propagate():
        raise ValueError("Inconsistent public rack count and named occupancy")
    for step, action in enumerate(plan, 1):
        part, kind = action.get("partId"), action.get("type")
        illegal = part not in installed
        if not illegal:
            if kind == "audit":
                illegal = part not in jobs or jobs.get(part) or installed[part] is True
                if not illegal:
                    jobs[part], installed[part] = True, False
            elif kind == "attach":
                illegal = (registration.get(part) != action.get("siteId")
                           or installed[part] is True or occupied <= 0)
                if not illegal:
                    installed[part], occupied = True, occupied - 1
            elif kind == "detach":
                illegal = installed[part] is False or occupied >= capacity
                if not illegal:
                    installed[part], occupied = False, occupied + 1
            else:
                illegal = True
        if illegal or not propagate():
            return {"firstConflict": step}
    return {"firstConflict": None}


def fit_source_majority(development_pairs, development_labels):
    """Development labels only; equal source/intervention/start weights."""
    if any(row["split"] != "development" or row["evaluationCohort"] != PRIMARY
           for row in development_pairs):
        raise ValueError("Source-majority fits primary development only, never heldout labels")
    members = {p for row in development_pairs for p in row["members"]}
    if set(development_labels) != members:
        raise ValueError("Fit labels must contain exactly the development members")
    if any(label is not None and (type(label) is not int or label < 1)
           for label in development_labels.values()):
        raise ValueError("Invalid development firstConflict label")
    if not members:
        return {"available": False, "reason": "no-development-training",
                "sourceLabels": {}, "fallbackLabel": None}
    weights = hierarchical_pair_weights(development_pairs)
    counts, pooled = defaultdict(Counter), Counter()
    for row in development_pairs:
        for p in row["members"]:
            label = development_labels[p]
            weight = weights[row["pairId"]] / 2
            counts[row["sourceGroup"]][label] += weight
            pooled[label] += weight
    return {
        "available": True, "sourceLabels": {s: _mode(v) for s, v in sorted(counts.items())},
        "fallbackLabel": _mode(pooled), "trainingPairs": len(development_pairs),
        "trainingSources": sorted(counts), "trainingMembers": sorted(members),
        "tieBreak": "null before increasing conflict index",
        "fitScope": "Primary development only, hierarchical source-balanced labels.",
        "heldoutRule": "Unseen source uses frozen development pooled majority; no heldout fitting.",
    }


def predict_source_majority(model, pair_rows):
    if not model["available"]:
        return {}
    return {
        p: {"firstConflict": model["sourceLabels"].get(row["sourceGroup"], model["fallbackLabel"])}
        for row in pair_rows for p in row["members"]
    }


REPRESENTATION_SCOPE = {
    "count-only": "Exact counts for fixed/registered/installed/rack/target, capacity and plan length.",
    "part-type-color-presence": "Unordered global type/color sets in each inventory compartment.",
    "part-type-color-count": "Unordered exact global type/color multisets in each compartment.",
    "sequence-only": "Ordered public proposed actions including P/S IDs, no scene or state.",
    "public-metadata": (
        "Complete initial Probe.public(False) image-track text except id, observation.taskId "
        "and observation.sessionId. Includes budgets, frame IDs, work orders and sequence."),
    "public-metadata-and-inventory": "Address-normalized public text plus exact global inventories.",
    "public-metadata-with-addresses": "Complete initial non-rendered payload, including routing IDs.",
}


def generate_controls(bank, public_inputs, geometries, *, seed=0, samples=2000,
                      maximum_assignments=100000, instance_inputs=None):
    """Generate certificates and deterministic software scores on supplied bank.

    public_inputs[probeId] is an initial image-track Probe.public(False).
    geometries[profileId] is qualified geometry JSON. Optional instance_inputs
    expose named registered occupancy but no geometry to a separate control.
    """
    definitions = visual_pair_definitions(bank)
    tasks = {t["id"]: t for t in bank["episodes"]}
    probes = {p["id"]: p for p in bank["probes"]}
    ids = [p for row in definitions for p in row["members"]]
    labels = {p: probes[p]["firstConflict"] for p in ids}
    if any(p not in public_inputs for p in ids):
        raise ValueError("Missing public control input")
    tracks = sorted({public_inputs[p]["observation"]["track"] for p in ids})
    if len(tracks) > 1:
        raise ValueError("Do not mix observation conditions in one controls report")
    features = {}
    for p in ids:
        task = tasks[probes[p]["taskId"]]
        features[p] = reduced_representations(
            public_inputs[p], geometries[task["profile"]], probes[p]["state"], task["goal"])
    certificates = {}
    for name, scope in REPRESENTATION_SCOPE.items():
        representations = {p: features[p][name] for p in ids}
        cohorts = {}
        for cohort in (PRIMARY, HISTORICAL):
            rows = [r for r in definitions if r["evaluationCohort"] == cohort]
            cohorts[cohort] = {
                "all": equivalence_certificate(rows, representations, labels,
                                               maximum_assignments=maximum_assignments),
                "bySplit": {
                    split: equivalence_certificate([r for r in rows if r["split"] == split],
                                                   representations, labels,
                                                   maximum_assignments=maximum_assignments)
                    for split in SPLITS},
            }
        certificates[name] = {"inputScope": scope, "cohorts": cohorts}
    development = [r for r in definitions if r["evaluationCohort"] == PRIMARY
                   and r["split"] == "development"]
    development_ids = {p for r in development for p in r["members"]}
    model = fit_source_majority(development, {p: labels[p] for p in development_ids})
    heldout = [r for r in definitions if r["split"] == "heldout-source"]
    heldout_ids = [p for r in heldout for p in r["members"]]
    majority_answers = predict_source_majority(model, heldout)
    majority = {
        "model": model, "predictions": majority_answers,
        "heldoutScores": matched_pair_scores(bank, heldout_ids, majority_answers,
                                            seed=seed, samples=samples) if model["available"] else None,
        "developmentScores": None,
        "scope": "Source identity is privileged metadata; unseen heldout sources use development fallback.",
    }
    rules = {}
    inputs = {"public-text-inventory-rule": public_inputs}
    if instance_inputs is not None:
        if any(p not in instance_inputs for p in ids):
            raise ValueError("Missing named-occupancy rule input")
        inputs["named-occupancy-inventory-rule"] = instance_inputs
    for name, payloads in inputs.items():
        predictions = {p: inventory_state_continuation(payloads[p]) for p in ids}
        rules[name] = {
            "predictions": predictions,
            "scores": matched_pair_scores(bank, ids, predictions, seed=seed, samples=samples),
            "scope": ("Label-free optimistic rack/identity/work-order execution; no support, "
                      "path, pose, mesh, edge, oracle or cost queries. "
                      + ("Named registered occupancy supplied as privileged input."
                         if name.startswith("named") else "Initial image-track public text only.")),
        }
    return {
        "schema": "brickplan-matched-controls/2.3", "softwareValidationOnly": True,
        "bankHash": fingerprint(bank), "seed": seed, "observationConditions": tracks,
        "certificates": certificates,
        "matchingContractAudit": {
            name: {"checkedPairs": sum(r["evaluationCohort"] == PRIMARY for r in definitions),
                   "unequalPairIds": [
                       row["pairId"] for row in definitions if row["evaluationCohort"] == PRIMARY
                       and features[row["members"][0]][name] != features[row["members"][1]][name]]}
            for name in ("count-only", "part-type-color-presence", "part-type-color-count",
                         "sequence-only")},
        "sourceMajority": majority, "labelFreeRules": rules,
        "visualModelResults": None, "humanResults": None,
        "primaryPairs": sum(r["evaluationCohort"] == PRIMARY for r in definitions),
        "status": "generated" if any(r["evaluationCohort"] == PRIMARY for r in definitions)
                  else "no-primary-matched-pairs",
        "limitations": [
            "Global inventory equality is not object/instance-sensitive spatial presence equality.",
            "Exact inventory features assume perfect counts/types/colors, not measured visual extraction.",
            "Routing IDs are excluded only in explicitly address-normalized representations.",
            "Metadata certificates cover supplied initial payloads/seed, not all adaptive view histories.",
            "Equivalence bounds use evaluation labels analytically, never as fitted heldout predictions.",
            "Source bootstrap is conditional on retained sources; no model/human outcomes are inferred.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--track", choices=("image-id", "image-id-active"), default="image-id")
    parser.add_argument("--samples", type=int, default=2000)
    parser.add_argument("--maximum-assignments", type=int, default=100000)
    args = parser.parse_args()
    # Lazy imports keep unit fixtures independent of source assets and physics.
    from bank import task_bank
    from probes import Probe, public_mapping

    try:
        bank = task_bank()
    except FileNotFoundError:
        parser.error("Build and certify the real v2.3 task bank before generating controls.")
    definitions = visual_pair_definitions(bank)
    if not any(row["evaluationCohort"] == PRIMARY for row in definitions):
        parser.error("No primary matched pairs. Build and certify the real v2.3 bank first.")
    probes = {p["id"]: p for p in bank["probes"]}
    mapping = public_mapping(probes, args.seed, "Q")
    public_ids = {private: public for public, private in mapping.items()}
    identity = {"runId": "matched-controls", "participantId": "software", "condition": args.track}
    public, geometries, instance = {}, {}, {}
    for row in definitions:
        for key in row["members"]:
            probe = Probe(probes[key], public_ids[key], args.seed, identity)
            payload = probe.public(False)
            public[key] = payload
            geometries[probe.session.task["profile"]] = probe.session.domain.geometry
            richer = copy.deepcopy(payload)
            richer["observation"]["sites"] = [
                {"registeredPartId": probe.session.part_ids[i],
                 "installed": bool(probes[key]["state"]["assembly"] & (1 << i))}
                for i in range(probe.session.domain.n)]
            instance[key] = richer
    result = generate_controls(
        bank, public, geometries, seed=args.seed, samples=args.samples,
        maximum_assignments=args.maximum_assignments, instance_inputs=instance)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n")
    print(json.dumps({"output": str(args.output), "primaryPairs": result["primaryPairs"],
                      "status": result["status"]}))


if __name__ == "__main__":
    main()
