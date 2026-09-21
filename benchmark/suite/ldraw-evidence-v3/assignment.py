#!/usr/bin/env python3
"""Jointly balance Part-type option positions and candidate-reference swaps."""
from collections import Counter
from fractions import Fraction
from itertools import permutations
import math
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import Bounds, LinearConstraint, milp

from common import DATA, VERSION, digest, frozen, load, original_tasks, save, sha

CHOICES = "ABCD"
HEURISTICS = [
    "first-alternative", "last-alternative", "cyclic-next", "cyclic-previous", "cyclic-two",
    "smallest-alternate-label", "largest-alternate-label",
    "nearest-alternate-label-number", "farthest-alternate-label-number",
    "nearest-alternate-center", "farthest-alternate-center",
    "nearest-alternate-projection", "farthest-alternate-projection",
]


def distance(a, b):
    return sum((x-y)**2 for x, y in zip(a, b))


def candidate_inventory():
    """Reconstruct candidate eligibility and features directly from frozen sources."""
    tasks = original_tasks()
    old = frozen("benchmark/ldraw-evidence-v2/visual-manifest.json")
    anchors = {o["parent_task_id"]: o for o in old["observations"]
               if o["family"] == "shape-match" and o["arm"] == "A"}
    bundles = {s: frozen(f"public/benchmark/ldraw-v2/models/{s}.json")
               for s in {o["source_id"] for o in anchors.values()}}
    scenes = {s: frozen(f"public/models/{s}/manifest.json") for s in bundles}
    rows = []
    for parent, a in sorted(anchors.items()):
        t = tasks[parent]
        parts = {p["id"]: p for p in bundles[a["source_id"]]["parts"]}
        placed = {p["instanceId"]: p for p in scenes[a["source_id"]]["instances"]}
        target = a["render_spec"]["target_id"]
        target_label = a["render_spec"]["labels"][target]
        projections = {p["id"]: p["anchor"] for p in a["render_spec"]["projections"]}
        center = lambda p: [(lo+hi)/2 for lo, hi in zip(placed[p]["bounds"]["min"], placed[p]["bounds"]["max"])]
        candidates = []
        for option in t["options"]:
            cid = next(r["id"] for r in t["references"] if r["label"] == option["label"])
            candidates.append({"instance_id": cid, "label": option["label"],
                "part_number": parts[cid]["partNumber"], "center": center(cid), "anchor": projections[cid]})
        matching = [c for c in candidates if c["part_number"] == parts[target]["partNumber"]]
        assert len(matching) == 1 and len(candidates) == 4
        eligible = [c["instance_id"] for c in candidates
                    if c["part_number"] != parts[target]["partNumber"] and
                    0 <= c["anchor"][0] <= 1280 and 0 <= c["anchor"][1] <= 800]
        assert len(eligible) == 3, (parent, "Not all distractors eligible; revise the preregistered universe")
        rows.append({"parent_task_id": parent, "source_id": a["source_id"],
            "target_id": target, "target_label": target_label, "target_center": center(target),
            "target_anchor": projections[target], "matching_id": matching[0]["instance_id"],
            "candidates": sorted(candidates, key=lambda c:c["label"]),
            "eligible_swap_ids": sorted(eligible), "source_anchor_observation": a["observation_id"]})
    assert len(rows) == 67
    return rows


def shortcut_predictions(row, option_labels):
    """Privileged A-only attacks; no access to the chosen swap or B pixels."""
    options = dict(zip(option_labels, CHOICES))
    a_label = next(c["label"] for c in row["candidates"] if c["instance_id"] == row["matching_id"])
    a = options[a_label]
    alternative = [c for c in row["candidates"] if c["instance_id"] != row["matching_id"]]
    label_number = lambda c: int(c["label"][1:])
    target_number = int(row["target_label"][1:])
    predicates = {
        "smallest-alternate-label": (label_number, False),
        "largest-alternate-label": (label_number, True),
        "nearest-alternate-label-number": (lambda c: abs(label_number(c)-target_number), False),
        "farthest-alternate-label-number": (lambda c: abs(label_number(c)-target_number), True),
        "nearest-alternate-center": (lambda c: distance(c["center"], row["target_center"]), False),
        "farthest-alternate-center": (lambda c: distance(c["center"], row["target_center"]), True),
        "nearest-alternate-projection": (lambda c: distance(c["anchor"], row["target_anchor"]), False),
        "farthest-alternate-projection": (lambda c: distance(c["anchor"], row["target_anchor"]), True),
    }
    result = {"first-alternative": next(c for c in CHOICES if c != a),
              "last-alternative": next(c for c in reversed(CHOICES) if c != a),
              "cyclic-next": CHOICES[(CHOICES.index(a)+1) % 4],
              "cyclic-previous": CHOICES[(CHOICES.index(a)-1) % 4],
              "cyclic-two": CHOICES[(CHOICES.index(a)+2) % 4]}
    for name, (key, reverse) in predicates.items():
        c = min(alternative, key=lambda c: (-key(c) if reverse else key(c), c["label"]))
        result[name] = options[c["label"]]
    assert set(result) == set(HEURISTICS)
    return a, result


def configurations(inventory):
    all_configs, representatives = [], []
    for row in inventory:
        equivalent = {}
        for labels in permutations(c["label"] for c in row["candidates"]):
            a, predictions = shortcut_predictions(row, labels)
            for cid in row["eligible_swap_ids"]:
                b_label = next(c["label"] for c in row["candidates"] if c["instance_id"] == cid)
                b = CHOICES[labels.index(b_label)]
                assert a != b
                hits = tuple(int(predictions[h] == b) for h in HEURISTICS)
                cost = 1 + int(digest([VERSION, row["parent_task_id"], labels, cid])[:12], 16) % 1000003
                c = {"parent_task_id": row["parent_task_id"], "source_id": row["source_id"],
                     "option_labels": list(labels), "swap_instance_id": cid,
                     "a_gold": a, "b_gold": b, "cost": cost,
                     "oracle_A_predictions": predictions, "heuristic_hits": hits}
                all_configs.append(c)
                # All constraints depend only on this signature. Keeping the
                # minimum-cost representative preserves the full problem's optimum.
                signature = (a, b, hits)
                old = equivalent.get(signature)
                if old is None or (cost, labels, cid) < (old["cost"], tuple(old["option_labels"]), old["swap_instance_id"]):
                    equivalent[signature] = c
        representatives.extend(sorted(equivalent.values(), key=lambda c: (
            c["parent_task_id"], c["option_labels"], c["swap_instance_id"])))
    return all_configs, representatives


def bounds_audit(rows):
    counts = Counter(r["source_id"] for r in rows)
    macro = lambda hits: sum(Fraction(h, counts[r["source_id"]]) for r, h in zip(rows, hits)) / len(counts)
    marginal = {arm: {c: sum(r[arm+"_gold"] == c for r in rows) for c in CHOICES} for arm in ["a", "b"]}
    matrix = {a: {b: sum(r["a_gold"] == a and r["b_gold"] == b for r in rows)
                  for b in CHOICES} for a in CHOICES}
    assert len(rows) == 67 and all(r["a_gold"] != r["b_gold"] for r in rows)
    assert all(v in [16, 17] for m in marginal.values() for v in m.values())
    assert all(matrix[a][b] == 0 if a == b else matrix[a][b] in [5, 6] for a in CHOICES for b in CHOICES)
    fixed_macro = {arm: {c: float(macro([int(r[arm+"_gold"] == c) for r in rows]))
                         for c in CHOICES} for arm in ["a", "b"]}
    assert all(v <= .30 + 1e-12 for arm in fixed_macro.values() for v in arm.values())
    heuristics = {}
    for name in HEURISTICS:
        hits = [int(r["oracle_A_predictions"][name] == r["b_gold"]) for r in rows]
        micro, source = Fraction(sum(hits), len(rows)), macro(hits)
        assert micro <= Fraction(2, 5) and source <= Fraction(2, 5), (name, micro, source)
        heuristics[name] = {"correct": sum(hits), "micro": float(micro), "source_macro": float(source)}
    return {"marginals": marginal, "transition_matrix": matrix, "fixed_choice_source_macro": fixed_macro,
            "oracle_A_heuristics": heuristics,
            "A_choice_only_empirical_ceiling": sum(max(v.values()) for v in matrix.values()) / 67}


def main():
    assert not (DATA / "part-type-assignment.json").exists(), "Assignment is immutable"
    contract = {"version": VERSION, "contract_sha256": sha(DATA / "REVISION-CONTRACT.md"),
        "pairs": 67, "arm_marginal_bounds": [16, 17], "off_diagonal_bounds": [5, 6],
        "fixed_choice_source_macro_max": .30, "oracle_A_rule_micro_and_source_macro_max": .40,
        "heuristics": HEURISTICS, "heuristic_ties": "ascending original numeric display label",
        "objective": "minimum sum of SHA-derived positive integer configuration costs",
        "equivalence_reduction": "keep least-cost configuration for each identical constraint coefficient signature"}
    save(DATA / "assignment-contract.json", contract, immutable=True)
    inventory = candidate_inventory()
    all_configs, configs = configurations(inventory)
    save(DATA / "candidate-inventory.json", {"rows": inventory, "total_configurations": len(all_configs)}, immutable=True)
    n = len(configs)
    source_count = Counter(r["source_id"] for r in inventory)
    lcm = math.lcm(*source_count.values())
    weights = np.array([lcm // source_count[c["source_id"]] for c in configs])
    denominator = lcm * len(source_count)
    design, lower, upper = [], [], []
    def constraint(values, lo, hi):
        design.append(np.asarray(values, dtype=float))
        lower.append(lo); upper.append(hi)
    for r in inventory:
        constraint([int(c["parent_task_id"] == r["parent_task_id"]) for c in configs], 1, 1)
    for arm in ["a", "b"]:
        for choice in CHOICES:
            indicator = np.array([int(c[arm+"_gold"] == choice) for c in configs])
            constraint(indicator, 16, 17)
            constraint(indicator * weights, 0, math.floor(Fraction(3, 10) * denominator))
    for a in CHOICES:
        for b in CHOICES:
            if a != b:
                constraint([int(c["a_gold"] == a and c["b_gold"] == b) for c in configs], 5, 6)
    for name in HEURISTICS:
        hits = np.array([int(c["oracle_A_predictions"][name] == c["b_gold"]) for c in configs])
        constraint(hits, 0, math.floor(Fraction(2, 5)*67))
        constraint(hits * weights, 0, math.floor(Fraction(2, 5)*denominator))
    options = {"time_limit": 300, "mip_rel_gap": 0, "presolve": True, "threads": 1}
    print({"stage": "optimize", "enumerated": len(all_configs), "reduced_variables": n,
           "constraints": len(design), "scipy": scipy.__version__}, flush=True)
    result = milp(c=np.array([c["cost"] for c in configs], dtype=float),
        integrality=np.ones(n), bounds=Bounds(np.zeros(n), np.ones(n)),
        constraints=LinearConstraint(np.array(design), lower, upper), options=options)
    assert result.success and result.status == 0, ("No proven optimum; do not weaken bounds", result.message)
    selected = [c for i,c in enumerate(configs) if result.x[i] > .5]
    selected.sort(key=lambda c:c["parent_task_id"])
    audit = bounds_audit(selected)
    save(DATA / "part-type-assignment.json", {
        "analysis_version": VERSION, "contract_sha256": sha(DATA / "assignment-contract.json"),
        "inventory_sha256": sha(DATA / "candidate-inventory.json"),
        "code_sha256": sha(Path(__file__)), "solver": {"scipy": scipy.__version__, "backend": "HiGHS",
            "status": int(result.status), "message": result.message, "options": options,
            "objective": int(round(result.fun)), "mip_gap": float(result.mip_gap)},
        "enumerated_configurations": len(all_configs), "reduced_variables": n, "rows": selected,
        "audit": audit, "empirical_model_evidence_used": False}, immutable=True)
    print({"status": "passed", "pairs": len(selected), "marginals": audit["marginals"],
           "transition_matrix": audit["transition_matrix"], "objective": result.fun}, flush=True)


if __name__ == "__main__":
    main()
