#!/usr/bin/env python3
"""Build three uncollected compositional examples from real LDraw records."""
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def read(path):
    return json.loads(path.read_text())


def write(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2) + "\n")


def source(path):
    return {"file": str(path.relative_to(ROOT)), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def label(instance):
    return "B" + instance[-4:]


def components(nodes, edges, absent=()):
    remaining = set(nodes) - set(absent)
    adj = {n: set() for n in remaining}
    for a, b in edges:
        if a in adj and b in adj:
            adj[a].add(b)
            adj[b].add(a)
    result = []
    while remaining:
        todo, visited = [min(remaining)], set()
        while todo:
            node = todo.pop()
            if node not in visited:
                visited.add(node)
                todo.extend(adj[node] - visited)
        remaining -= visited
        result.append(sorted(visited))
    return sorted(result, key=lambda g: (-len(g), g))


def connected(groups, terminals):
    return any(set(terminals) <= set(group) for group in groups)


def best_policy(worlds, outcomes, used=()):
    if len(worlds) == 1:
        return 0, {"world": worlds[0]}
    options = []
    for q in outcomes:
        if q in used:
            continue
        yes = [w for w in worlds if outcomes[q][w]]
        no = [w for w in worlds if not outcomes[q][w]]
        if not yes or not no:
            continue
        cy, py = best_policy(yes, outcomes, used + (q,))
        cn, pn = best_policy(no, outcomes, used + (q,))
        options.append((1 + max(cy, cn), q, {"query": q, "yes": py, "no": pn}))
    return (min(options)[0], min(options)[2]) if options else (999, None)


def build():
    model = ROOT / "public/models/omr-42004/manifest.json"
    bundle = ROOT / "public/benchmark/ldraw-v2/models/omr-42004.json"
    m, b = read(model), read(bundle)
    sid = "s-629fc43f2db48f6b"
    selected = [p for p in m["instances"] if p["parentSubmodelId"] == sid]
    nodes = sorted(label(p["instanceId"]) for p in selected)
    edges = sorted({tuple(sorted([label(e["a"]), label(e["b"])])) for e in b["audit"]["edges"]
                    if label(e["a"]) in nodes and label(e["b"]) in nodes})
    assert len(nodes) == 36 and len(edges) == 44 and len(components(nodes, edges)) == 1
    graph = {"nodes": nodes, "edges": edges,
             "meaning": "Exact induced undirected recognized-connector graph; 36 source instances, 44 unique pairs.",
             "boundary": "Only paths inside this supplied subassembly graph count. No external assembly path is available."}
    missing = ["B0150", "B0160", "B0164", "B0165", "B0167", "B0173", "B0175", "B0177"]
    terminals = ["B0158", "B0171", "B0179", "B0180"]
    cases, gold = [], []
    cases.append({
        "id": "CX1", "family": "minimum-terminal-repair", "source_id": "omr-42004",
        "question": "Eight vertices are unavailable. Restore the fewest listed vertices so that B0158, B0171, "
                    "B0179 and B0180 lie in one connected component. A restore action reinstates that vertex "
                    "and every original edge to a currently present neighbor. Return every minimum repair set, "
                    "its cost, and the final component sizes. Decide whether budget 2 is sufficient.",
        "input": {"graph": graph, "missing": missing, "terminals": terminals, "cost_per_vertex": 1,
                  "budget": 2, "restore_candidates": missing},
        "answer_format": {"minimum_sets": "list[list[ID]]", "cost": "integer",
                          "final_component_sizes": "list[integer]", "budget_sufficient": "boolean"},
    })
    enumeration = []
    for k in range(len(missing) + 1):
        for repair in itertools.combinations(missing, k):
            gs = components(nodes, edges, set(missing) - set(repair))
            enumeration.append({"restored": list(repair), "cost": k,
                                "success": connected(gs, terminals), "component_sizes": [len(g) for g in gs]})
    minimum = min(r["cost"] for r in enumeration if r["success"])
    opt = [r for r in enumeration if r["success"] and r["cost"] == minimum]
    assert minimum == 3 and len(opt) == 1 and opt[0]["restored"] == ["B0160", "B0175", "B0177"]
    gold.append({"id": "CX1", "answer": {"minimum_sets": [r["restored"] for r in opt], "cost": minimum,
                 "final_component_sizes": opt[0]["component_sizes"], "budget_sufficient": False},
                 "initial_components": components(nodes, edges, missing), "exhaustive_subsets": enumeration,
                 "feasible_counts_by_cost": [sum(r["success"] and r["cost"] == k for r in enumeration) for k in range(9)]})

    # Select a four-world diagnosis task whose unique optimal first query
    # needs a different second query on each branch.
    pool = []
    tests = list(itertools.combinations(terminals, 2))
    for failed in itertools.combinations(missing, 3):
        gs = components(nodes, edges, failed)
        pool.append((failed, tuple(connected(gs, pair) for pair in tests)))
    signatures = {}
    for failed, sig in pool:
        signatures.setdefault(sig, failed)
    chosen = None
    for q_indices in itertools.combinations(range(len(tests)), 3):
        for sigs in itertools.combinations(sorted(signatures), 4):
            outcomes = {f"Q{i + 1}": {f"W{j + 1}": sig[index] for j, sig in enumerate(sigs)}
                        for i, index in enumerate(q_indices)}
            worlds = ["W1", "W2", "W3", "W4"]
            depth, policy = best_policy(worlds, outcomes)
            if depth != 2 or "query" not in policy.get("yes", {}) or "query" not in policy.get("no", {}):
                continue
            if policy["yes"]["query"] == policy["no"]["query"]:
                continue
            roots = []
            for q in outcomes:
                yes = [w for w in worlds if outcomes[q][w]]
                no = [w for w in worlds if not outcomes[q][w]]
                if yes and no:
                    cost = 1 + max(best_policy(yes, outcomes, (q,))[0], best_policy(no, outcomes, (q,))[0])
                    if cost == 2:
                        roots.append(q)
            if len(roots) == 1:
                chosen = q_indices, sigs, outcomes, policy
                break
        if chosen:
            break
    assert chosen
    q_indices, sigs, outcomes, policy = chosen
    worlds = [{"id": f"W{i + 1}", "absent": list(signatures[sig])} for i, sig in enumerate(sigs)]
    queries = [{"id": f"Q{i + 1}", "pair": list(tests[index]), "cost": 1} for i, index in enumerate(q_indices)]
    cases.append({
        "id": "CX2", "family": "adaptive-fault-diagnosis", "source_id": "omr-42004",
        "question": "Exactly one listed three-vertex fault world holds. A query returns whether its two IDs "
                    "are connected in the remaining graph. Design a decision tree that identifies the exact "
                    "world in the minimum worst-case query cost. Specify the first query and both conditional "
                    "continuations. Prove whether a budget of 1 can succeed.",
        "input": {"graph": graph, "worlds": worlds, "queries": queries, "prior": "uniform",
                  "query_semantics": "Exact noiseless reachability; graph is static during inspection.",
                  "budget_to_test": 1},
        "answer_format": {"worst_case_cost": "integer", "policy": "recursive query/yes/no or world leaf",
                          "budget_one_sufficient": "boolean"},
    })
    gold.append({"id": "CX2", "answer": {"worst_case_cost": 2, "policy": policy, "budget_one_sufficient": False},
                 "outcomes": outcomes, "one_query_lower_bound": "A binary answer has two outcomes but four distinct worlds."})

    axle_path = ROOT / "public/models/omr-42061/manifest.json"
    axle = read(axle_path)
    parts = {label(p["instanceId"]): p for p in axle["instances"]}
    a_ids, b_ids = ["B0024", "B0025", "B0026", "B0035"], ["B0036", "B0037", "B0038", "B0047"]
    def anchor(name):
        p = parts[name]
        return {"id": name, "part_type": p["partNumber"], "origin_mm": [round(v, 6) for v in p["originalMatrix"][12:15]]}
    target = "B0030"
    target_data = anchor(target)
    target_matrix = np.array(parts[target]["originalMatrix"]).reshape(4, 4).T
    target_data["local_x_axis_world"] = np.round(target_matrix[:3, 0] / np.linalg.norm(target_matrix[:3, 0]), 8).tolist()
    cases.append({
        "id": "CX3", "family": "typed-rigid-registration", "source_id": "omr-42061",
        "question": "Two 12-part axle subassemblies repeat the same CAD design. The four listed anchors have "
                    "unknown correspondences; IDs provide no matching rule. Match only equal part types. "
                    "Determine the unique admissible correspondence and its least-squares proper rigid transform "
                    "q = R p + t, with det(R)=+1. A correspondence is admissible only if some proper rigid "
                    "transform gives maximum anchor error <= 0.05 mm. Return the correspondences, R, t, and "
                    "the mapped origin and local x-axis of B0030. Reflecting the geometry is forbidden.",
        "input": {"anchor_A": [anchor(n) for n in a_ids], "anchor_B": [anchor(n) for n in reversed(b_ids)],
                  "probe": target_data, "coordinate_frame": "Viewer world millimeters; part local origins, not mesh centers.",
                  "tolerance_mm": .05},
        "answer_format": {"correspondence": "map[ID,ID]", "R": "3x3 matrix", "t_mm": "3-vector",
                          "mapped_probe_origin_mm": "3-vector", "mapped_probe_axis": "unit 3-vector"},
    })
    candidates = []
    x = np.array([anchor(n)["origin_mm"] for n in a_ids])
    for permutation in itertools.permutations(b_ids):
        if any(parts[a]["partNumber"] != parts[b]["partNumber"] for a, b in zip(a_ids, permutation)):
            continue
        y = np.array([anchor(n)["origin_mm"] for n in permutation])
        u, _, vt = np.linalg.svd((x - x.mean(0)).T @ (y - y.mean(0)))
        raw = vt.T @ u.T
        correction = np.eye(3)
        correction[2, 2] = np.linalg.det(raw)
        r = vt.T @ correction @ u.T
        t = y.mean(0) - r @ x.mean(0)
        error = np.max(np.linalg.norm((r @ x.T).T + t - y, axis=1))
        candidates.append({"match": dict(zip(a_ids, permutation)), "proper_fit_max_error_mm": float(error),
                           "unconstrained_fit_determinant": float(np.linalg.det(raw)),
                           "max_pair_distance_gap_mm": float(np.max(abs(
                               np.linalg.norm(x[:, None] - x[None, :], axis=2)
                               - np.linalg.norm(y[:, None] - y[None, :], axis=2))))})
    accepted = [c for c in candidates if c["proper_fit_max_error_mm"] <= .05]
    assert len(accepted) == 1
    # A distance discrepancy > 2 * tolerance rules out every rigid transform,
    # including ones with a smaller max residual than the least-squares fit.
    assert all(c["max_pair_distance_gap_mm"] > .1 for c in candidates if c not in accepted)
    r = np.diag([-1., 1., -1.])
    t = np.array([16., 0., 120.])
    full_correspondence = {}
    aa = [p for p in axle["instances"] if p["parentSubmodelId"] == "s-d6e83c4998bc01bd"]
    bb = [p for p in axle["instances"] if p["parentSubmodelId"] == "s-25bcf51cad146fc2"]
    for p in aa:
        q = next(q for q in bb if q["sourceLine"] == p["sourceLine"])
        pa, pb = np.array(p["originalMatrix"]).reshape(4, 4).T, np.array(q["originalMatrix"]).reshape(4, 4).T
        assert np.max(abs(r @ pa[:3, :3] - pb[:3, :3])) < 1e-8
        assert np.max(abs(r @ pa[:3, 3] + t - pb[:3, 3])) < 1e-8
        full_correspondence[label(p["instanceId"])] = label(q["instanceId"])
    gold.append({"id": "CX3", "answer": {"correspondence": accepted[0]["match"], "R": r.tolist(), "t_mm": t.tolist(),
                 "mapped_probe_origin_mm": np.round(r @ np.array(target_data["origin_mm"]) + t, 6).tolist(),
                 "mapped_probe_axis": np.round(r @ np.array(target_data["local_x_axis_world"]), 8).tolist()},
                 "candidate_fits": candidates, "full_source_correspondence": full_correspondence,
                 "anchor_tetrahedron_six_volume_mm3": abs(float(np.linalg.det(x[1:] - x[0]))),
                 "source_validation": "All 12 complete part transforms agree; corresponding probe is B0042."})

    common = {"version": "complex-examples-v1", "status": "three-designed-examples-uncollected-not-primary",
              "scope": "Compositional examples built from real source records; no model responses or human qualification.",
              "physical_scope": "No pose or geometry edits. Graph faults are abstract vertex unavailability, not physical removal trajectories.",
              "sources": [source(model), source(bundle), source(axle_path)]}
    write("public.json", {**common, "cases": cases})
    write("gold.json", {**common, "cases": gold})
    write("render-cases.json", {
        "backhoe-context": {"model": "omr-42004", "ids": None, "labels": [], "direction": [-1, .65, 1]},
        "backhoe-detail": {"model": "omr-42004", "ids": nodes,
                           "labels": ["B0148", "B0158", "B0160", "B0169", "B0175", "B0177", "B0179", "B0180"],
                           "direction": [-1, .65, 1]},
        "axle-context": {"model": "omr-42061", "ids": None, "labels": [], "direction": [-1, .65, 1]},
        "axle-A": {"model": "omr-42061", "ids": sorted(full_correspondence), "labels": a_ids + [target],
                   "direction": [-1, .8, 1]},
        "axle-B": {"model": "omr-42061", "ids": sorted(full_correspondence.values()), "labels": b_ids,
                   "direction": [-1, .8, 1]},
    })
    print(json.dumps({"minimum_repair": gold[0]["answer"], "diagnostic_worlds": worlds,
                      "queries": queries, "policy": policy, "registration": gold[2]["answer"]}, indent=2))


if __name__ == "__main__":
    build()
