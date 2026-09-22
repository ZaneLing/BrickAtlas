#!/usr/bin/env python3
"""Independently verify complex-example GT without importing its builder."""
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def partition(graph, absent):
    # Union-find is independent of the builder's graph search.
    parent = {n: n for n in graph["nodes"] if n not in absent}
    def find(n):
        while parent[n] != n:
            n = parent[n]
        return n
    for a, b in graph["edges"]:
        if a in parent and b in parent:
            parent[find(a)] = find(b)
    groups = {}
    for n in parent:
        groups.setdefault(find(n), []).append(n)
    return sorted([sorted(g) for g in groups.values()], key=lambda g: (-len(g), g))


def verify():
    public, golden = read(HERE / "public.json"), read(HERE / "gold.json")
    for spec in [public, golden]:
        assert spec["status"] == "three-designed-examples-uncollected-not-primary"
        for record in spec["sources"]:
            assert sha(ROOT / record["file"]) == record["sha256"]
    cases, gt = ({c["id"]: c for c in document["cases"]} for document in [public, golden])
    assert set(cases) == set(gt) == {"CX1", "CX2", "CX3"}
    assert all("answer" not in case for case in cases.values())
    bundle = read(ROOT / "public/benchmark/ldraw-v2/models/omr-42004.json")
    model = read(ROOT / "public/models/omr-42004/manifest.json")
    to_label = lambda p: "B" + p[-4:]
    source_nodes = {to_label(p["instanceId"]) for p in model["instances"]
                    if p["parentSubmodelId"] == "s-629fc43f2db48f6b"}
    source_edges = {tuple(sorted([to_label(e["a"]), to_label(e["b"])]))
                    for e in bundle["audit"]["edges"]
                    if to_label(e["a"]) in source_nodes and to_label(e["b"]) in source_nodes}
    graph = cases["CX1"]["input"]["graph"]
    assert graph == cases["CX2"]["input"]["graph"]
    assert set(graph["nodes"]) == source_nodes and set(map(tuple, graph["edges"])) == source_edges
    assert len(source_nodes) == 36 and len(source_edges) == 44

    inp, cert = cases["CX1"]["input"], gt["CX1"]
    missing, feasible = inp["missing"], []
    lookup = {frozenset(r["restored"]): r for r in cert["exhaustive_subsets"]}
    assert len(lookup) == 256
    for bits in itertools.product([False, True], repeat=len(missing)):
        repair = {n for n, bit in zip(missing, bits) if bit}
        groups = partition(graph, set(missing) - repair)
        success = any(set(inp["terminals"]) <= set(g) for g in groups)
        assert lookup[frozenset(repair)] == {
            "restored": sorted(repair), "cost": len(repair), "success": success,
            "component_sizes": [len(g) for g in groups]}
        if success:
            feasible.append(sorted(repair))
    min_cost = min(map(len, feasible))
    minimum = sorted(r for r in feasible if len(r) == min_cost)
    assert cert["answer"]["minimum_sets"] == minimum == [["B0160", "B0175", "B0177"]]
    assert cert["answer"]["cost"] == min_cost == 3
    assert cert["answer"]["budget_sufficient"] is (min_cost <= inp["budget"])
    assert cert["answer"]["final_component_sizes"] == [31]
    assert partition(graph, missing) == cert["initial_components"]

    inp, cert = cases["CX2"]["input"], gt["CX2"]
    outcomes = {}
    for query in inp["queries"]:
        outcomes[query["id"]] = {}
        for world in inp["worlds"]:
            groups = partition(graph, world["absent"])
            outcomes[query["id"]][world["id"]] = any(set(query["pair"]) <= set(g) for g in groups)
    assert outcomes == cert["outcomes"]
    worlds, queries = sorted(outcomes["Q1"]), sorted(outcomes)
    # Enumerate all depth-two binary decision-tree query choices (3^3).
    valid_trees = []
    for first, no_second, yes_second in itertools.product(queries, repeat=3):
        signatures = [(outcomes[first][w], outcomes[yes_second if outcomes[first][w] else no_second][w])
                      for w in worlds]
        if len(set(signatures)) == len(worlds):
            valid_trees.append((first, no_second, yes_second))
    assert valid_trees == [("Q3", "Q1", "Q2")]
    assert not any(len({outcomes[q][w] for w in worlds}) == len(worlds) for q in queries)
    depths = []
    for world in worlds:
        tree, depth = cert["answer"]["policy"], 0
        while "query" in tree:
            tree = tree["yes" if outcomes[tree["query"]][world] else "no"]
            depth += 1
        assert tree["world"] == world
        depths.append(depth)
    assert max(depths) == cert["answer"]["worst_case_cost"] == 2
    assert cert["answer"]["budget_one_sufficient"] is False

    inp, cert = cases["CX3"]["input"], gt["CX3"]
    axle = read(ROOT / "public/models/omr-42061/manifest.json")
    parts = {to_label(p["instanceId"]): p for p in axle["instances"]}
    for anchor in inp["anchor_A"] + inp["anchor_B"] + [inp["probe"]]:
        part = parts[anchor["id"]]
        assert part["partNumber"] == anchor["part_type"]
        assert np.allclose(part["originalMatrix"][12:15], anchor["origin_mm"], atol=1e-6, rtol=0)
    x = np.array([a["origin_mm"] for a in inp["anchor_A"]])
    matches, distance_rejections = [], []
    for order in itertools.permutations(inp["anchor_B"]):
        if any(a["part_type"] != b["part_type"] for a, b in zip(inp["anchor_A"], order)):
            continue
        y = np.array([b["origin_mm"] for b in order])
        gap = np.max(abs(np.linalg.norm(x[:, None] - x[None, :], axis=2)
                         - np.linalg.norm(y[:, None] - y[None, :], axis=2)))
        if gap > 2 * inp["tolerance_mm"]:
            distance_rejections.append(float(gap))
            continue
        # Solve directly from three coordinate differences; no SVD/Kabsch.
        r = (y[1:] - y[0]).T @ np.linalg.inv((x[1:] - x[0]).T)
        t = y[0] - r @ x[0]
        assert np.allclose(r.T @ r, np.eye(3), atol=1e-10)
        assert abs(np.linalg.det(r) - 1) < 1e-10
        match = {a["id"]: b["id"] for a, b in zip(inp["anchor_A"], order)}
        matches.append(match)
    answer = cert["answer"]
    assert matches == [answer["correspondence"]] and len(distance_rejections) == 3
    assert np.allclose(r, answer["R"], atol=1e-10) and np.allclose(t, answer["t_mm"], atol=1e-10)
    assert abs(np.linalg.det((x[1:] - x[0]))) > 2000
    probe_matrix = np.array(parts["B0030"]["originalMatrix"]).reshape(4, 4).T
    probe_axis = probe_matrix[:3, 0] / np.linalg.norm(probe_matrix[:3, 0])
    assert np.allclose(probe_axis, inp["probe"]["local_x_axis_world"], atol=1e-8)
    assert np.allclose(r @ probe_matrix[:3, 3] + t, answer["mapped_probe_origin_mm"], atol=1e-6)
    assert np.allclose(r @ probe_axis, answer["mapped_probe_axis"], atol=1e-8)
    assert len(cert["full_source_correspondence"]) == 12
    for a, b in cert["full_source_correspondence"].items():
        pa, pb = (np.array(parts[n]["originalMatrix"]).reshape(4, 4).T for n in [a, b])
        assert np.allclose(r @ pa[:3, :3], pb[:3, :3], atol=1e-10, rtol=0)
        assert np.allclose(r @ pa[:3, 3] + t, pb[:3, 3], atol=1e-10, rtol=0)

    captures = read(ROOT / "paper/figures/complex-raw/captures.json")
    render_cases = read(HERE / "render-cases.json")
    assert captures["renderer_sha256"] == sha(ROOT / "paper/complex-render.ts")
    for frame in captures["frames"]:
        assert sha(ROOT / frame["file"]) == frame["sha256"] and frame["sourcePosesPreserved"]
        source_manifest = read(ROOT / f"public/models/{frame['model']}/manifest.json")
        assert frame["sourceHash"] == source_manifest["sourceHash"]
        expected = render_cases[frame["id"]]["ids"]
        visible = {to_label(i) for i in frame["visibleIds"]}
        assert visible == (set(expected) if expected else {to_label(p["instanceId"]) for p in source_manifest["instances"]})
        assert len(visible) == frame["visibleCount"]
    report = {"status": "passed", "complex_cases": 3, "model_or_human_results": 0,
              "CX1": {"checked_subsets": 256, "minimum_cost": min_cost, "unique_minimum": minimum},
              "CX2": {"checked_depth_two_trees": 27, "optimal_trees": valid_trees, "worlds_checked": 4},
              "CX3": {"assignments_checked": 4, "independent_solver": "coordinate-basis inverse",
                      "rejected_pair_distance_gaps_mm": distance_rejections, "full_source_transforms_checked": 12},
              "captures_verified": len(captures["frames"]),
              "input_sha256": sha(HERE / "public.json"), "gold_sha256": sha(HERE / "gold.json")}
    (HERE / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
