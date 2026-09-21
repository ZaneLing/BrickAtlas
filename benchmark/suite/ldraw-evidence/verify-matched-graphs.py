#!/usr/bin/env python3
"""Independently read every saved challenge observation and pairing."""
from collections import Counter
from common import DATA, load, digest, save, sha, public_tasks, target_label
from graph_oracles import graph_stats, component_sets, component_count_union_find

directory = DATA / "matched-graphs-v1"
manifest = load(directory / "manifest.json")
inputs = load(directory / "inputs.json")
observations = {r["id"]: r for r in manifest["observations"]}
parents = public_tasks()
assert len(observations) == manifest["observation_count"]
assert len(set(manifest["trial_order"])) == len(observations)
assert set(manifest["trial_order"]) == set(observations)
for public in inputs["observations"]:
    r = observations[public["id"]]
    assert public["payload"] == r["input"] and digest(public["payload"]) == public["request_hash"]
    assert set(public) == {"id", "payload", "request_hash"}
    assert set(public["payload"]) == {"question", "format", "input"}
    parent = parents[r["parent_task_id"]]
    nodes, edges = r["input"]["input"]["nodes"], r["input"]["input"]["edges"]
    target = target_label(r["input"])
    assert nodes == parent["input"]["nodes"]
    assert r["source_id"] == parent["modelId"] and r["source_hash"] == parent["source_hash"]
    assert r["gold"]["value"] == len(component_sets(nodes, edges, target))
    assert r["gold"]["value"] == component_count_union_find(nodes, edges, target)
    assert r["stats"] == graph_stats(nodes, edges, target)
    assert r["evidence_kind"] == "hypothetical-evidence"
directions = Counter()
for pair in manifest["pairs"]:
    a, b = [observations[pair[k]] for k in ["a", "b"]]
    assert a["parent_task_id"] == b["parent_task_id"] == pair["parent_task_id"]
    assert a["input"]["input"]["nodes"] == b["input"]["input"]["nodes"]
    for field in ["n_before", "m_before", "target_degree"]:
        assert a["stats"][field] == b["stats"][field]
    if pair["matching"] != "same-nodes-edges-and-target-degree":
        assert a["stats"]["surviving_degree_sequence"] == b["stats"]["surviving_degree_sequence"]
    delta = b["gold"]["value"] - a["gold"]["value"]
    assert delta == pair["gold_delta"]
    assert pair["direction"] == ("increase" if delta > 0 else "decrease" if delta < 0 else "unchanged")
    directions[pair["direction"]] += 1
assert dict(directions) == manifest["directions"]
rules = load(DATA / "graph-challenge-rules.json")
assert sha(DATA / "graph-challenge-rules.json") == manifest["rules_sha256"]
assert max(Counter(r["parent_task_id"] for r in observations.values()).values()) <= rules["max_observations_per_parent"]
assert max(Counter(r["source_id"] for r in observations.values()).values()) <= rules["max_observations_per_source"]
report = {"status": "passed", "observations": len(observations), "pairs": len(manifest["pairs"]),
          "directions": dict(directions), "independent_oracles": ["BFS", "union-find"],
          "natural_sources_added": 0, "model_inference": "not-run",
          "manifest_sha256": sha(directory / "manifest.json")}
save(directory / "independent-verification.json", report)
print(report)
