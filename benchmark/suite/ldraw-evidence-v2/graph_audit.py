#!/usr/bin/env python3
"""Audit preserved graph evidence against explicit shallow, anonymous features."""
from collections import Counter, defaultdict, deque
from pathlib import Path
import re

from common import DATA, VERSION, digest, frozen, original_tasks, save, sha
from estimates import estimate, wilson

PRIOR = "benchmark/ldraw-evidence-v1/matched-graphs-v1/manifest.json"
FEATURES = ["node-count", "edge-count", "degree-histogram", "anonymous-1wl"]
ROLES = ["strong-change", "degree-visible-control", "strong-invariance", "degree-visible-invariance"]


def adjacency(nodes, edges, target):
    assert len(nodes) == len(set(nodes)) and target in nodes
    assert all(len(e) == 2 and e[0] != e[1] and set(e) <= set(nodes) for e in edges)
    result = {n: set() for n in nodes if n != target}
    for a, b in edges:
        if target not in (a, b):
            result[a].add(b)
            result[b].add(a)
    return result


def bfs(adj):
    unseen, components = set(adj), []
    while unseen:
        start = min(unseen)
        unseen.remove(start)
        q, reached = deque([start]), [start]
        while q:
            for n in sorted(adj[q.popleft()]):
                if n in unseen:
                    unseen.remove(n)
                    reached.append(n)
                    q.append(n)
        components.append(sorted(reached))
    return sorted(components)


def union_find(nodes, edges, target):
    parent = {n: n for n in nodes if n != target}

    def root(n):
        while parent[n] != n:
            n = parent[n]
        return n

    for a, b in edges:
        if target not in (a, b):
            parent[root(a)] = root(b)
    return len({root(n) for n in parent})


def wl_signature(adj, rounds=16):
    # Uniform initial labels; globally canonical hashes, no node names or source IDs.
    # Keep round histograms. Local color renumbering would erase degree differences.
    colors = {n: "uniform" for n in adj}
    histories = []
    for _ in range(rounds):
        colors = {n: digest([colors[n], sorted(colors[m] for m in adj[n])]) for n in adj}
        histories.append(sorted(Counter(colors.values()).items()))
    return digest(histories)


def inspect(oid, source, parent, payload, gold):
    graph = payload["input"]
    targets = re.findall(r"\bB\d{4,}\b", payload["question"])
    assert len(targets) == 1
    target = targets[0]
    adj = adjacency(graph["nodes"], graph["edges"], target)
    degrees = sorted(len(v) for v in adj.values())
    components = bfs(adj)
    assert len(components) == union_find(graph["nodes"], graph["edges"], target) == gold
    histogram = sorted(Counter(degrees).items())
    n, m = len(adj), sum(degrees) // 2
    isolates = degrees.count(0)
    return {"id": oid, "source_id": source, "parent_task_id": parent, "gold": gold,
            "surviving_nodes": sorted(adj), "surviving_edges": m,
            "target_degree": len({x for e in graph["edges"] if target in e for x in e} - {target}),
            "degree_sequence": degrees, "degree_histogram": histogram, "isolates": isolates,
            "features": {"node-count": digest(n), "edge-count": digest(m),
                         "degree-histogram": digest(histogram), "anonymous-1wl": wl_signature(adj)},
            "isolates-plus-one": isolates + int(any(degrees)), "bfs": len(components),
            "union-find": len(components), "components": components}


def lookup(row, training, feature):
    train = [r for r in training if r["source_id"] != row["source_id"]]
    assert all(r["source_id"] != row["source_id"] for r in train)
    matched = [r for r in train if r["features"][feature] == row["features"][feature]]
    counts = Counter(r["gold"] for r in matched)
    # Frozen no-support policy: abstain, counted incorrect. Ties choose smaller integer.
    prediction = sorted(counts, key=lambda k: (-counts[k], k))[0] if counts else None
    return {"prediction": prediction, "support_items": len(matched),
            "support_sources": sorted({r["source_id"] for r in matched}),
            "training_sources": sorted({r["source_id"] for r in train}),
            "held_out_source": row["source_id"], "label_counts": dict(sorted(counts.items()))}


def predictions(rows, training):
    result = {}
    for row in rows:
        pred = {f + "-lookup": lookup(row, training, f) for f in FEATURES}
        pred.update({k: {"prediction": row[k]} for k in ["isolates-plus-one", "bfs", "union-find"]})
        result[row["id"]] = pred
    return result


def collisions(rows, feature):
    groups = defaultdict(list)
    for r in rows:
        groups[r["features"][feature]].append(r)
    conflicts = []
    ceiling = 0
    for key, group in groups.items():
        counts = Counter(r["gold"] for r in group)
        ceiling += max(counts.values())
        if len(counts) > 1:
            conflicts.append({"feature_hash": key, "gold_counts": dict(counts),
                              "observation_ids": [r["id"] for r in group],
                              "source_ids": sorted({r["source_id"] for r in group})})
    return {"conflicting_feature_classes": len(conflicts), "classes": conflicts,
            "best_empirical_deterministic_feature_accuracy": ceiling / len(rows) if rows else None,
            "interpretation": "in-sample feature collision ceiling, not a fitted/test-set result"}


def build():
    prior = frozen(PRIOR)
    rows = [inspect(o["id"], o["source_id"], o["parent_task_id"], o["input"], o["gold"]["value"])
            for o in prior["observations"]]
    byid = {r["id"]: r for r in rows}
    assert max(len(r["surviving_nodes"]) for r in rows) <= 16
    changed = {p["parent_task_id"]: p for p in prior["pairs"] if p["gold_delta"]}
    primary_ids = {p[k] for p in changed.values() for k in ["a", "b"]}
    training = [r for r in rows if r["id"] in primary_ids]
    pred = predictions(rows, training)
    pair_records = []
    for pair in prior["pairs"]:
        a, b = byid[pair["a"]], byid[pair["b"]]
        strong = changed[pair["parent_task_id"]]["matching"].endswith("surviving-degrees")
        role = ("strong-change" if strong else "degree-visible-control") if pair["gold_delta"] else (
            "strong-invariance" if strong else "degree-visible-invariance")
        checks = {field: a[field] == b[field] for field in [
            "surviving_nodes", "surviving_edges", "target_degree", "degree_sequence", "isolates"]}
        assert all(checks.values()) if strong or not pair["gold_delta"] else all(
            checks[k] for k in ["surviving_nodes", "surviving_edges", "target_degree"])
        if strong:
            assert a["features"]["anonymous-1wl"] == b["features"]["anonymous-1wl"]
        baselines = {}
        for method in pred[a["id"]]:
            x, y = pred[a["id"]][method]["prediction"], pred[b["id"]][method]["prediction"]
            ca, cb = x == a["gold"], y == b["gold"]
            baselines[method] = {"a": x, "b": y, "a_correct": int(ca), "b_correct": int(cb),
                                 "both": int(ca and cb), "accuracy": (ca + cb) / 2,
                                 "covered": (int(x is not None) + int(y is not None)) / 2}
        pair_records.append({**pair, "role": role, "constraints": checks,
            "wl_indistinguishable": a["features"]["anonymous-1wl"] == b["features"]["anonymous-1wl"],
            "a_gold": a["gold"], "b_gold": b["gold"], "baselines": baselines})
    assert Counter(p["role"] for p in pair_records) == {
        "strong-change": 12, "degree-visible-control": 61, "strong-invariance": 12, "degree-visible-invariance": 61}
    reports = {}
    for role in ROLES:
        pairs = [p for p in pair_records if p["role"] == role]
        observations = [byid[k] for k in sorted({p[k] for p in pairs for k in ["a", "b"]})]
        endpoints = Counter(p[k + "_gold"] for p in pairs for k in ["a", "b"])
        reports[role] = {"pairs": len(pairs), "sources": len({p["source_id"] for p in pairs}),
            "answer_histograms": {arm: dict(Counter(p[arm + "_gold"] for p in pairs)) for arm in ["a", "b"]},
            "symmetric_endpoint_weights": {arm: {gold: count / 2 for gold, count in endpoints.items()}
                                          for arm in ["a", "b"]},
            "answer_balance": "Stored A/B label frequencies need not match. Primary metrics are unordered Both and "
                              "symmetric endpoint accuracy; endpoint symmetrization gives equal arm weights without "
                              "creating new observations or inflating the pair/source denominator.",
            "directions": dict(Counter(p["direction"] for p in pairs)),
            "collisions": {f: collisions(observations, f) for f in FEATURES}, "baselines": {}}
        for method in pred[rows[0]["id"]]:
            scores = [{"source_id": p["source_id"], **p["baselines"][method]} for p in pairs]
            reports[role]["baselines"][method] = {
                **{k: estimate(scores, k) for k in ["a_correct", "b_correct", "both", "accuracy", "covered"]},
                "pair_both_wilson_ci95": wilson(sum(r["both"] for r in scores), len(scores)),
                "pair_interval_caveat": "Wilson treats pairs as independent; source reuse violates that approximation"}
    natural = []
    for t in original_tasks().values():
        if t["family"] != "graph-removal":
            continue
        natural.append(inspect(t["id"], t["modelId"], t["id"],
                               {"input": t["input"], "question": t["promptEn"]}, t["answer"]["value"]))
    natural_pred = predictions(natural, natural)
    natural_metrics = {}
    for method in pred[rows[0]["id"]]:
        scores = [{"source_id": r["source_id"],
                   "correct": int(natural_pred[r["id"]][method]["prediction"] == r["gold"]),
                   "covered": int(natural_pred[r["id"]][method]["prediction"] is not None)} for r in natural]
        natural_metrics[method] = {k: estimate(scores, k) for k in ["correct", "covered"]}
    result = {"analysis_version": VERSION, "evidence_kind": "deterministic-graph-audit",
        "status": "computed", "prior_manifest_sha256": sha(DATA.parent / "ldraw-evidence-v1/matched-graphs-v1/manifest.json"),
        "code_hashes": {f: sha(Path(__file__).with_name(f)) for f in ["graph_audit.py", "estimates.py", "common.py"]},
        "protocol": {"training": "held-source-out; all changed observations only; no invariance duplication",
            "natural_training": "held-source-out within 73 natural items; separate from challenge",
            "unseen_feature": "abstain, counted incorrect", "tie_rule": "smallest component count",
            "wl": "16 rounds, uniform initial colors, graph histogram per round, no IDs/positional features",
            "scope": "12 strong pairs are a template-limited proof of concept; no broad graph-intelligence claim",
            "gnn_limit": "Anonymous 1-WL-equivalent message passing cannot distinguish the strong pairs",
            "intervals": "source bootstrap descriptive; pair Wilson approximate; neither validates population generalization"},
        "summary": reports, "pairs": pair_records, "observations": rows, "predictions": pred,
        "natural": {"items": len(natural), "sources": len({r["source_id"] for r in natural}),
                    "metrics": natural_metrics, "observations": natural, "predictions": natural_pred,
                    "collisions": {f: collisions(natural, f) for f in FEATURES}},
        "learned_model_results": None}
    save(DATA / "graph-audit.json", result)
    save(DATA / "graph-partitions.json", {"analysis_version": VERSION,
         "prior_manifest_sha256": result["prior_manifest_sha256"],
         "roles": {role: [p["pair_id"] for p in pair_records if p["role"] == role] for role in ROLES}})
    for role, report in reports.items():
        print(role, report["pairs"], report["sources"],
              {k: v["both"]["micro"] for k, v in report["baselines"].items()})


if __name__ == "__main__":
    build()
