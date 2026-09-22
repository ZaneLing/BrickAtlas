"""Task-aligned, noncausal interface diagnostics and shared-group sensitivity."""
from collections import Counter, defaultdict
from itertools import product
from statistics import mean

import numpy as np

from common import digest

CONDITIONS = ("atomic_binding", "oracle_binding", "multimodal")
CELL_KEYS = ("id", "construction_id", "dependence_group", "split", "replicate",
             "structural_arm", "visual_arm", "repeat")
CONTRACT = {
    "schema": "visual-repair-interface-v1",
    "event_order": "AOM",
    "A": "atomic_binding.binding_correct",
    "O": "oracle_binding.repair_exact",
    "M": "multimodal.repair_exact",
    "joint_failure": "P(M=0 | A=1,O=1), operational, not a causal mechanism",
    "delta_repair": "multimodal.repair_exact - oracle_binding.repair_exact",
    "delta_binding": "multimodal.binding_correct - atomic_binding.binding_correct",
    "join": list(CELL_KEYS),
    "compatibility": "One explicit comparison group in one run lock; identical system, revision, settings, repeats and kind.",
    "primary_weighting": "Equal dependence-group means; J uses only groups with A=O=1 eligibility.",
    "secondary_weighting": "Micro: all planned task slots; conditional J pools eligible task slots.",
    "failures": "Missing planned attempts, invalid outputs, refusals and adapter errors are false; never drop failed slots.",
    "zero_eligible": "Null J for zero-eligible groups; omit them from macro J, retain them in shared resampling and report counts.",
    "bootstrap": {"seed": 20260922, "draws": 2000,
                  "unit": "Shared whole dependence groups, all conditions/cells/ID replicates retained.",
                  "empty_draw": "Omit undefined J draws and report defined count; CI null with fewer than two eligible groups."},
    "qualification": "Full and qualified sets, construction-wide and identical across conditions; pending is not rejected.",
}


def validate_comparisons(manifest):
    """Never infer same-system comparisons from similar display names."""
    configs = {c["id"]: c for c in manifest["configurations"]}
    if len(configs) != len(manifest["configurations"]):
        raise ValueError("Duplicate configuration")
    seen = set()
    for comparison in manifest.get("comparison_groups", []):
        if comparison["id"] in seen:
            raise ValueError("Duplicate comparison group")
        seen.add(comparison["id"])
        members = comparison["config_ids"]
        if set(members) != set(CONDITIONS):
            raise ValueError("Comparison needs atomic, oracle and multimodal conditions")
        selected = []
        for condition, cid in members.items():
            config = configs.get(cid)
            if not config or config["condition"] != condition:
                raise ValueError("Unknown/off-condition comparison configuration")
            selected.append(config)
        for field in ("kind", "revision", "settings", "repeats"):
            if len({digest(c[field]) for c in selected}) != 1:
                raise ValueError(f"Incompatible comparison {field}")
        if not comparison.get("system_id") or any(
                c.get("system_id") != comparison["system_id"] for c in selected):
            raise ValueError("Incompatible comparison system identity")
        if selected[0]["kind"] == "model" and comparison["system_id"] != manifest["model"]["id"]:
            raise ValueError("Comparison model differs from run-locked model")
        if selected[0]["kind"] == "algorithmic":
            a, o, m = [configs[members[c]] for c in CONDITIONS]
            if a["rule"] != m["rule"] or o["rule"] != "oracle":
                raise ValueError("Algorithmic reference requires matched pixel rules and exact oracle")


def aligned_rows(rows, config_ids):
    by_config = defaultdict(dict)
    for row in rows:
        if row["config_id"] not in config_ids.values():
            continue
        key = tuple(row[k] for k in CELL_KEYS)
        bucket = by_config[row["config_id"]]
        if key in bucket:
            raise ValueError("Duplicate aligned task/cell")
        bucket[key] = row
    membership = [set(by_config[cid]) for cid in config_ids.values()]
    if membership and any(keys != membership[0] for keys in membership[1:]):
        raise ValueError("Missing condition or incompatible task/cell membership")
    result = []
    for key in sorted(membership[0]) if membership else []:
        a, o, m = [by_config[config_ids[c]][key] for c in CONDITIONS]
        if any(row["condition"] != condition for row, condition in zip((a, o, m), CONDITIONS)):
            raise ValueError("Off-condition aligned row")

        def correct(row, field):
            return bool(row[field]) and not row["missing"] and not row["invalid"]

        av, ov, mv = correct(a, "binding_correct"), correct(o, "repair_exact"), correct(m, "repair_exact")
        result.append({
            **{k: a[k] for k in CELL_KEYS}, "event": f"{int(av)}{int(ov)}{int(mv)}",
            "eligible": int(av and ov), "failure": int(av and ov and not mv),
            "delta_repair": int(mv) - int(ov),
            "delta_binding": int(correct(m, "binding_correct")) - int(av),
        })
    return result


def interface_metrics(rows, config_ids):
    aligned = aligned_rows(rows, config_ids)
    grouped = defaultdict(list)
    for row in aligned:
        grouped[row["dependence_group"]].append(row)
    group_ids = sorted(grouped)
    events = ["".join(bits) for bits in product("01", repeat=3)]
    contingency = {event: sum(r["event"] == event for r in aligned) for event in events}
    counts = {
        g: {"planned_n": len(grouped[g]),
            "eligible_n": sum(r["eligible"] for r in grouped[g]),
            "failure_n": sum(r["failure"] for r in grouped[g]),
            "contingency": dict.fromkeys(events, 0) | dict(Counter(r["event"] for r in grouped[g]))}
        for g in group_ids
    }
    # The same draws index all numerator/denominator/contrast group vectors.
    rng = np.random.default_rng(CONTRACT["bootstrap"]["seed"])
    draws = rng.integers(0, len(group_ids), size=(CONTRACT["bootstrap"]["draws"], len(group_ids))) if group_ids else None
    planned = np.array([counts[g]["planned_n"] for g in group_ids], dtype=float)
    eligible = np.array([counts[g]["eligible_n"] for g in group_ids], dtype=float)
    failures = np.array([counts[g]["failure_n"] for g in group_ids], dtype=float)

    def summarize(numerators, denominators):
        active = denominators > 0
        values = np.divide(numerators, denominators, out=np.zeros_like(numerators), where=active)
        group_values = {g: float(values[i]) if active[i] else None for i, g in enumerate(group_ids)}
        active_values = [v for v in group_values.values() if v is not None]
        macro_ci = micro_ci = None
        defined_draws = 0
        if draws is not None:
            active_drawn = active[draws].sum(axis=1)
            defined = active_drawn > 0
            defined_draws = int(defined.sum())
            if int(active.sum()) > 1:
                macro = values[draws].sum(axis=1)[defined] / active_drawn[defined]
                micro = numerators[draws].sum(axis=1)[defined] / denominators[draws].sum(axis=1)[defined]
                macro_ci = np.quantile(macro, [.025, .975]).tolist()
                micro_ci = np.quantile(micro, [.025, .975]).tolist()
        return {
            "n": int(denominators.sum()),
            "micro": float(numerators.sum() / denominators.sum()) if denominators.sum() else None,
            "group_macro": mean(active_values) if active_values else None,
            "groups": int(active.sum()), "group_values": group_values,
            "ci95_group_sensitivity": macro_ci, "ci95_micro_group_sensitivity": micro_ci,
            "bootstrap_defined_draws": defined_draws,
            "leave_one_group_out": [
                {"omitted": g, "group_macro": mean(remaining) if remaining else None}
                for g in group_ids
                for remaining in [[v for k, v in group_values.items() if k != g and v is not None]]
            ],
        }

    joint = summarize(failures, eligible)
    joint.update(eligible_n=joint["n"], eligible_groups=joint["groups"],
                 failure_n=int(failures.sum()), zero_eligible_groups=int((eligible == 0).sum()))
    deltas = {}
    for name in ("delta_repair", "delta_binding"):
        numerators = np.array([sum(r[name] for r in grouped[g]) for g in group_ids], dtype=float)
        deltas[name] = summarize(numerators, planned)
    return {
        "planned_count": len(aligned), "groups": len(group_ids),
        "contingency": contingency, "group_counts": counts,
        "joint_failure_given_atomic_oracle": joint, **deltas,
        "bootstrap": {**CONTRACT["bootstrap"], "group_order": group_ids},
    }
