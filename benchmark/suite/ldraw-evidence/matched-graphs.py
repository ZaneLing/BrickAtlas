#!/usr/bin/env python3
"""Freeze a bounded hypothetical graph challenge; preserve all natural v2 data."""
import argparse
from collections import Counter
from itertools import permutations
from common import DATA, VERSION, public_tasks, load, save, sha, digest, target_label
from graph_oracles import graph_stats


def undirected(edges):
    return sorted({tuple(sorted(e)) for e in edges})


def build():
    rule_path = DATA / "graph-challenge-rules.json"
    rules = load(rule_path)
    parents = [t for t in public_tasks().values() if t["family"] == "graph-removal"]
    parents.sort(key=lambda t: digest([rules["seed"], t["id"]]))
    observations, pair_records, gaps = [], [], []
    for index, parent in enumerate(parents):
        nodes = parent["input"]["nodes"]
        target = target_label({"question": parent["promptEn"]})
        rest = sorted((n for n in nodes if n != target), key=lambda n: digest([rules["seed"], parent["id"], n]))
        star = [[target, n] for n in rest]
        if len(rest) >= 6:
            a, b, c, d, e, f = rest[:6]
            low = [[a,b],[b,c],[c,d],[d,e],[e,f],[f,a]]
            high = [[a,b],[b,c],[c,a],[d,e],[e,f],[f,d]]
            match = "same-nodes-edges-target-and-surviving-degrees"
        else:
            a, b, c, d = rest[:4]
            low = [[a,b],[b,c],[c,d]]
            high = [[a,b],[b,c],[c,a]]
            match = "same-nodes-edges-and-target-degree"
            gaps.append({"parent_task_id": parent["id"], "constraint": "surviving-degree-sequence",
                         "status": "not-matched", "reason": "Four/five surviving nodes; path/triangle template has different degrees."})
        anchor, partner = (low, high) if index % 2 == 0 else (high, low)
        anchor_all = undirected(star + anchor)
        # Find an isomorphic but edge-distinct relabeling; source labels are fixed.
        nuisance = None
        for permutation in permutations(rest):
            mapping = dict(zip(rest, permutation))
            candidate = [[mapping.get(a, a), mapping.get(b, b)] for a, b in star + anchor]
            if undirected(candidate) != anchor_all:
                nuisance = candidate
                break
        assert nuisance
        this = []
        for serial, edges in enumerate([star + anchor, star + partner, nuisance]):
            opaque_id = "mg-" + digest([rules["seed"], parent["id"], serial])[:20]
            stats = graph_stats(nodes, edges, target)
            payload = {"question": parent["promptEn"], "format": "integer",
                       "input": {"nodes": nodes, "edges": [list(e) for e in undirected(edges)],
                                 "graphMeaning": "Supplied hypothetical undirected graph; do not infer physical source connectivity."}}
            row = {"id": opaque_id, "parent_task_id": parent["id"], "source_id": parent["modelId"],
                   "source_hash": parent["source_hash"], "generation_seed": rules["seed"],
                   "transform": ["anchor", "component-change", "isomorphic-relabel"][serial],
                   "evidence_kind": "hypothetical-evidence", "input": payload,
                   "request_hash": digest(payload), "gold": {"value": stats["component_count"]},
                   "stats": stats, "independent_oracles_agree": True}
            observations.append(row)
            this.append(row)
        for j in [1, 2]:
            x, y = this[0], this[j]
            for field in ["n_before", "m_before", "target_degree"]:
                assert x["stats"][field] == y["stats"][field]
            if match.endswith("surviving-degrees") or j == 2:
                assert x["stats"]["surviving_degree_sequence"] == y["stats"]["surviving_degree_sequence"]
            delta = y["gold"]["value"] - x["gold"]["value"]
            assert (delta != 0) if j == 1 else (delta == 0)
            pair_records.append({"pair_id": "pair-" + digest([x["id"], y["id"]])[:20],
                                 "parent_task_id": parent["id"], "source_id": parent["modelId"],
                                 "a": x["id"], "b": y["id"], "gold_delta": delta,
                                 "direction": "increase" if delta > 0 else "decrease" if delta < 0 else "unchanged",
                                 "matching": match if j == 1 else "isomorphic-all-degrees"})
    assert max(Counter(o["parent_task_id"] for o in observations).values()) <= rules["max_observations_per_parent"]
    assert max(Counter(o["source_id"] for o in observations).values()) <= rules["max_observations_per_source"]
    observations.sort(key=lambda r: digest([rules["seed"], "trial-order", r["id"]]))
    directory = DATA / "matched-graphs-v1"
    existing = directory / "manifest.json"
    result = {"extension_version": rules["extension_version"], "analysis_version": VERSION,
              "rules_sha256": sha(rule_path), "status": "frozen-not-run", "parent_count": len(parents),
              "source_count": len({o["source_id"] for o in observations}), "observation_count": len(observations),
              "pair_count": len(pair_records), "directions": dict(Counter(p["direction"] for p in pair_records)),
              "matching_counts": dict(Counter(p["matching"] for p in pair_records)),
              "feasibility_gaps": gaps, "pairs": pair_records, "observations": observations,
              "trial_order": [o["id"] for o in observations], "model_results": None,
              "interpretation": "Hypothetical challenge only; source graph topology and natural edge counts are not preserved."}
    if existing.exists() and load(existing) != result:
        raise ValueError("Frozen extension would change; create a new extension version")
    save(existing, result)
    public = {"extension_version": rules["extension_version"], "role": "model-input",
              "observations": [{"id": o["id"], "payload": o["input"], "request_hash": o["request_hash"]} for o in observations]}
    save(directory / "inputs.json", public)
    save(directory / "verification.json", {"status": "passed", "observations": len(observations),
         "pairs": len(pair_records), "bfs_union_find_agreement": len(observations),
         "directions": result["directions"], "manifest_sha256": sha(existing),
         "model_results": None})
    print({k: result[k] for k in ["parent_count", "source_count", "observation_count", "directions", "matching_counts"]})


if __name__ == "__main__":
    argparse.ArgumentParser(description=__doc__).parse_args()
    build()
