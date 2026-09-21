#!/usr/bin/env python3
"""Replicate the node-only prior using frozen requests, then score independently."""
import argparse
from collections import defaultdict
from common import ROOT, DATA, VERSION, read_frozen, save, sha, digest, text_payload, target_label, public_tasks, internal_tasks
from graph_oracles import graph_stats, component_sets, matched_cycle_fixture
from estimators import estimate


def predict_without_edges(nodes):
    """The predictor receives only a list of public node labels."""
    if not isinstance(nodes, list) or not nodes or any(not isinstance(n, str) for n in nodes):
        raise ValueError("Expected node labels")
    return {"value": len(set(nodes)) - 1}


def original_intervention(payload):
    # Independent transcription of the frozen intervention's public semantics.
    nodes = payload["input"]["nodes"]
    edges = [list(e) for e in payload["input"]["edges"]]
    target = target_label(payload)
    survivors = [n for n in nodes if n != target]
    components = component_sets(nodes, edges, target)
    first = next(set(c) for c in components if survivors[0] in c)
    other = next(n for n in survivors if n not in first)
    return edges + [[survivors[0], other]]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", default=str(DATA / "node-prior-audit.json"))
    args = p.parse_args()
    public = public_tasks()
    snapshots = read_frozen("benchmark/ldraw-v2/request-snapshots/manifest.json")["requests"]
    refs = {r["taskId"]: r for r in snapshots}
    predictions, payloads = {}, {}
    # Prediction stage never loads answers or passes edges to the predictor.
    for task in public.values():
        if task["family"] != "graph-removal":
            continue
        row = refs[task["id"]]
        path = ROOT / row["file"]
        if sha(path) != row["sha256"]:
            raise ValueError("Request hash mismatch")
        payload = text_payload(read_frozen(row["file"]))
        predictions[task["id"]] = predict_without_edges(payload["input"]["nodes"])
        payloads[task["id"]] = payload
    prediction_file = DATA / "node-only-predictions.json"
    save(prediction_file, {"analysis_version": VERSION,
                          "predictor_input": "nodes only, no edges or answers",
                          "predictions": predictions})
    # Scoring starts only after the prediction artifact has been materialized.
    golds = internal_tasks()
    rows = []
    for task_id, prediction in predictions.items():
        payload = payloads[task_id]
        target = target_label(payload)
        stats = graph_stats(payload["input"]["nodes"], payload["input"]["edges"], target)
        gold = golds[task_id]["answer"]["value"]
        if stats["component_count"] != gold:
            raise ValueError(f"Stored/BFS/union-find gold disagreement: {task_id}")
        altered_edges = original_intervention(payload)
        changed = graph_stats(payload["input"]["nodes"], altered_edges, target)
        assert changed["component_count"] == gold - 1
        both = int(prediction["value"] == gold and prediction["value"] == changed["component_count"])
        rows.append({"task_id": task_id, "parent_task_id": task_id,
                     "source_id": public[task_id]["modelId"],
                     "source_hash": public[task_id]["source_hash"],
                     "request_hash": refs[task_id]["sha256"], "prediction": prediction,
                     "gold": gold, "hit": int(prediction["value"] == gold), **stats,
                     "stratum": "deficit=0" if stats["deficit"] == 0 else "deficit>0",
                     "intervention": {"edges": altered_edges, "input_hash": digest({**payload["input"], "edges": altered_edges}),
                                      "gold": changed["component_count"], "both_oracles_agree": True},
                     "node_both_correct": both,
                     "fixed4_hit": int(gold == 4),
                     "fixed4_both_correct": int(gold == 4 and changed["component_count"] == 4),
                     "graph_algorithm_hit": 1, "graph_algorithm_both_correct": 1})
    by_source = defaultdict(list)
    for r in rows:
        by_source[r["source_id"]].append(r)
    summary = estimate(rows, "hit")
    assert len(rows) == 73 and sum(r["hit"] for r in rows) == 63, "Guide prior not reproduced"
    assert abs(summary["source_macro"] - .8375) < 1e-12
    strata = {key: {"items": sum(r["stratum"] == key for r in rows),
                    "sources": len({r["source_id"] for r in rows if r["stratum"] == key})}
              for key in ["deficit=0", "deficit>0"]}
    baselines = {name: {"natural": estimate(rows, hit), "paired_both_correct": estimate(rows, both)}
                 for name, hit, both in [
                     ("node-count-only", "hit", "node_both_correct"),
                     ("fixed-answer-4", "fixed4_hit", "fixed4_both_correct"),
                     ("graph-algorithm", "graph_algorithm_hit", "graph_algorithm_both_correct")]}
    result = {"analysis_version": VERSION, "status": "passed", "study_role": "post-hoc corpus audit; no model inference",
              "prediction_file_sha256": sha(prediction_file), "dataset_release": "brickatlas-ldraw-2",
              "summary": summary, "hits": sum(r["hit"] for r in rows), "strata": strata,
              "baselines": baselines, "by_source": {s: {"n": len(rr), "hits": sum(r["hit"] for r in rr)}
                                                   for s, rr in sorted(by_source.items())},
              "failure_task_ids": [r["task_id"] for r in rows if not r["hit"]],
              "rows": rows, "independent_fixture": matched_cycle_fixture(),
              "model_results": None, "exclusions": [],
              "interpretation": "High natural deletion accuracy can follow the node-count prior. Both-correct separates this baseline from graph computation; this is not a model finding."}
    save(args.out, result)
    print({"n": len(rows), "hits": result["hits"], "micro": summary["micro"], "source_macro": summary["source_macro"],
           "strata": strata, "node_both_correct": baselines["node-count-only"]["paired_both_correct"]["micro"]})


if __name__ == "__main__":
    main()
