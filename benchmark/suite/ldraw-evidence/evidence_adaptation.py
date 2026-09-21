"""Evidence-aware, immutable reanalysis; never infer predictions from success bits."""
import argparse
from collections import Counter
import json
from pathlib import Path
import subprocess
import tempfile

from common import ROOT, DATA, VERSION, digest, load, save, read_frozen, target_label
from estimators import estimate, paired_difference
from graph_oracles import component_sets, component_count_union_find

TRUTH = {
    "visual-mismatch": "fact-change",
    "edge-causal-control": "fact-change",
    "visual-information": "information-withdrawal",
    "edge-information": "information-withdrawal",
    "large-scene-versus-text": "information-withdrawal",
    "background-only": "observation-access",
    "crop-access": "observation-access",
    "view-access": "observation-access",
}
WRONG_CATEGORIES = ["new-evidence-answer", "old-answer", "other-legal-answer", "invalid-or-missing"]
TRANSITIONS = ["both-correct", "A-correct-B-wrong", "A-wrong-B-correct",
               "both-wrong-same-legal-semantics", "both-wrong-different-or-invalid"]


def comparisons():
    plan = read_frozen("benchmark/paper/ldraw-v2-experiments.json")
    return [{**p, "truth_policy": TRUTH.get(p["id"], "semantic-invariance"),
             "qa_required": p["id"] in {
                 "visual-mismatch", "background-only", "crop-access", "view-access",
                 "camera", "color-nuisance", "label-binding", "visual-information",
                 "large-scene-versus-text"}}
            for p in plan["pairedComparisons"]]


def unique_by(rows, key):
    result = {}
    for row in rows:
        if row[key] in result:
            raise ValueError(f"Duplicate {key}: {row[key]}")
        result[row[key]] = row
    return result


def normalize(answer, payload, execution=None):
    """Choice IDs map to canonical option meanings; invalid repeats remain invalid."""
    if not isinstance(answer, dict):
        return None
    options = {o["id"]: o["label"] for o in payload.get("options", [])}
    form = payload["format"]
    if form == "single-choice":
        c = answer.get("choiceId")
        return {"choice": options[c]} if isinstance(c, str) and c in options else None
    if form == "multiple-choice":
        values = answer.get("choiceIds")
        if (not isinstance(values, list) or any(not isinstance(v, str) or v not in options for v in values)
                or len(set(values)) != len(values)):
            return None
        return {"set": sorted(options[v] for v in values)}
    if form == "integer":
        v = answer.get("value")
        if isinstance(v, bool) or not isinstance(v, (int, float)) or not (-2**53 < v < 2**53) or int(v) != v:
            return None
        return {"value": int(v)}
    if form == "actions":
        ids = answer.get("actionIds")
        if not isinstance(ids, list) or any(not isinstance(v, str) for v in ids) or execution is None:
            return None
        # Actions are judged by the frozen execution contract, not set comparison.
        return {"final_facts": execution["final_facts"], "execution_issue": execution["issue"]}
    raise ValueError(f"Unsupported response format: {form}")


def normalized_gold(row):
    if row["format"] == "actions":
        return {"goal_facts": sorted(row["payload"]["input"]["goalFacts"]),
                "absent_facts": sorted(row["payload"]["input"].get("absentFacts", [])),
                "contract": "frozen executable action preconditions and budget"}
    return normalize(row["gold"], row["payload"])


def graph_gold(row):
    payload = row["payload"]
    edges, target = payload["input"]["edges"], target_label(payload)
    if row["family"] == "graph-removal":
        nodes = payload["input"]["nodes"]
        bfs = len(component_sets(nodes, edges, target))
        if bfs != component_count_union_find(nodes, edges, target):
            raise ValueError("Independent graph oracle mismatch")
        return {"value": bfs}
    neighbors = {n for edge in edges if target in edge for n in edge if n != target}
    return {"choiceIds": [o["id"] for o in payload["options"] if o["label"] in neighbors]}


def pair_rows(a, b, spec):
    for field in ["analysis_version", "model_revision", "adapter_hash", "prompt_hash", "dataset_hash", "code_hashes",
                  "evidence_kind"]:
        if a[field] != b[field]:
            raise ValueError(f"Pair provenance mismatch: {field}")
    if a["analysis_version"] != VERSION or a["condition"] != spec["a"] or b["condition"] != spec["b"]:
        raise ValueError("Pair condition/version mismatch")
    if a["status"] != "complete" or b["status"] != "complete":
        raise ValueError("Only completed runs support paired model metrics")
    left, right = unique_by(a["rows"], "task_id"), unique_by(b["rows"], "task_id")
    expected = spec["taskIds"]
    if len(set(expected)) != len(expected):
        raise ValueError("Duplicate expected pair")
    if not set(expected) <= left.keys() or not set(expected) <= right.keys():
        raise ValueError("Run does not cover declared pair universe; never take an intersection")
    rows = []
    for task_id in expected:
        x, y = left[task_id], right[task_id]
        if x["source_id"] != y["source_id"] or x["parent_task_id"] != y["parent_task_id"]:
            raise ValueError("Pair source/parent mismatch")
        if x["family"] != y["family"]:
            raise ValueError("Pair family mismatch")
        p, q = [normalize(r["answer"], r["payload"], r.get("execution")) for r in [x, y]]
        ga, gb = [normalized_gold(r) for r in [x, y]]
        ca, cb = bool(x["success"]), bool(y["success"])
        if spec["truth_policy"] == "fact-change":
            if ga is None or gb is None or ga == gb:
                raise ValueError("Fact change requires distinct legal golds")
            if x["family"] in ["neighbors", "graph-removal"]:
                for r in [x, y]:
                    if normalize(graph_gold(r), r["payload"]) != normalize(r["gold"], r["payload"]):
                        raise ValueError("Wire graph gold mismatch")
            category = ("invalid-or-missing" if q is None else "new-evidence-answer" if q == gb
                        else "old-answer" if q == ga else "other-legal-answer")
        else:
            if x["format"] != "actions" and ga != gb:
                raise ValueError("Unchanged-task gold mismatch")
            category = None
        transition = ("both-correct" if ca and cb else "A-correct-B-wrong" if ca else "A-wrong-B-correct" if cb
                      else "both-wrong-same-legal-semantics" if p is not None and p == q
                      else "both-wrong-different-or-invalid")
        row = {"pair_id": f'{spec["id"]}:{task_id}', "parent_task_id": x["parent_task_id"],
               "source_id": x["source_id"], "family": x["family"], "analysis_version": VERSION,
               **{k: a[k] for k in ["model_revision", "adapter_hash", "prompt_hash", "dataset_hash"]},
               "condition_A": a["condition"], "condition_B": b["condition"],
               "request_hash_A": x["request_sha256"], "request_hash_B": y["request_sha256"],
               "receipt_hash_A": x["receipt_sha256"], "receipt_hash_B": y["receipt_sha256"],
               "prediction_A": p, "prediction_B": q, "gold_A": ga, "gold_B": gb,
               "gold_source_A": x["gold_source"], "gold_source_B": y["gold_source"],
               "gold_hash_A": digest({"gold": ga, "source": x["gold_source"]}),
               "gold_hash_B": digest({"gold": gb, "source": y["gold_source"]}),
               "truth_policy": spec["truth_policy"], "failure_A": x["failure_reason"],
               "failure_B": y["failure_reason"], "A_correct": int(ca), "B_correct": int(cb),
               "both_correct": int(ca and cb), "B_original_gold_correct": y["original_gold_success"],
               "both_valid": int(p is not None and q is not None),
               "legal_output_changed": int(p is not None and q is not None and p != q),
               "same_legal_output": int(p is not None and p == q),
               "wrong_image_category": category, "transition": transition,
               "qa_status": "unreviewed-at-wire-bytes" if x["images"] or y["images"] else "not-visual",
               "image_hashes_A": [i["wire_sha256"] for i in x["images"]],
               "image_hashes_B": [i["wire_sha256"] for i in y["images"]]}
        if x["family"] == "graph-removal" and spec["id"] == "edge-causal-control":
            n = len(set(x["payload"]["input"]["nodes"])) - 1
            for name, va, vb in [("node-only", n, n), ("fixed-four", 4, 4),
                                 ("BFS", graph_gold(x)["value"], graph_gold(y)["value"])]:
                row[f"{name}_both_correct"] = int(va == ga["value"] and vb == gb["value"])
                row[f"{name}_A_correct"] = int(va == ga["value"])
            row["deficit"] = n - ga["value"]
        rows.append(row)
    unique_by(rows, "pair_id")
    return rows


def summarize(rows, truth_policy, resamples=10000):
    n = len(rows)
    ac = sum(r["A_correct"] for r in rows)
    bc = sum(r["both_correct"] for r in rows)
    categories = Counter(r["wrong_image_category"] for r in rows)
    transitions = Counter(r["transition"] for r in rows)
    metrics = {k: estimate(rows, k, resamples) for k in
               ["A_correct", "B_correct", "both_correct", "B_original_gold_correct",
                "same_legal_output", "legal_output_changed", "both_valid"]}
    metrics["delta_A_minus_B"] = paired_difference(rows, "A_correct", "B_correct", resamples)
    result = {"denominator": n, "metrics": metrics,
              "adaptation_given_A_correct": {"numerator": bc, "denominator": ac,
                                            "value": bc / ac if ac else None},
              "transition_counts": {k: transitions[k] for k in TRANSITIONS},
              "failure_counts_A": dict(Counter(r["failure_A"] or "correct" for r in rows)),
              "failure_counts_B": dict(Counter(r["failure_B"] or "correct" for r in rows))}
    assert sum(result["transition_counts"].values()) == n
    if truth_policy == "fact-change":
        result["new_evidence_accuracy"] = metrics["B_correct"]
        result["paired_both_correct"] = metrics["both_correct"]
        result["B_categories"] = {k: categories[k] for k in WRONG_CATEGORIES}
        assert sum(result["B_categories"].values()) == n
    graph_rows = [r for r in rows if "node-only_both_correct" in r]
    if graph_rows:
        result["graph_removal"] = {
            "model_minus_baseline_natural_accuracy": {
                k: paired_difference(graph_rows, "A_correct", f"{k}_A_correct", resamples)
                for k in ["node-only", "fixed-four", "BFS"]},
            "model_minus_baseline_both_correct": {
                k: paired_difference(graph_rows, "both_correct", f"{k}_both_correct", resamples)
                for k in ["node-only", "fixed-four", "BFS"]},
            "deficit_strata": {label: estimate([r for r in graph_rows if (r["deficit"] == 0) == easy],
                                              "both_correct", resamples)
                               for label, easy in [("zero", True), ("positive", False)]}}
    return result


def analyze(a, b, spec, resamples=10000):
    rows = pair_rows(a, b, spec)
    return {"analysis_version": VERSION, "status": "complete", "comparison": spec["id"],
            "evidence_kind": a["evidence_kind"], "model_revision": a["model_revision"],
            "manifest_A": {"file": a["manifest"], "sha256": a["manifest_sha256"]},
            "manifest_B": {"file": b["manifest"], "sha256": b["manifest_sha256"]},
            "truth_policy": spec["truth_policy"], "expected_task_ids": spec["taskIds"],
            "interpretation": ("provisional-descriptive; exact-wire visual decidability unverified"
                               if any(r["qa_status"] != "not-visual" for r in rows)
                               else "given-graph computation; no physical inference"),
            "summary": summarize(rows, spec["truth_policy"], resamples),
            "by_family": {f: summarize([r for r in rows if r["family"] == f], spec["truth_policy"], resamples)
                          for f in sorted({r["family"] for r in rows})},
            "rows": rows}


def validate_run(path, allow_synthetic=False):
    node = ROOT / ".tools/node-v22.23.2-darwin-arm64/bin/node"
    tsx = ROOT / "node_modules/tsx/dist/cli.mjs"
    with tempfile.TemporaryDirectory(prefix="brickatlas-verify-") as tmp:
        output = Path(tmp) / "run.json"
        subprocess.run([str(node), str(tsx), str(ROOT / "benchmark/suite/ldraw-evidence/validate-run.ts"),
                        str(path), str(output)] + (["--synthetic-fixture"] if allow_synthetic else []),
                       check=True, cwd=ROOT, capture_output=True, text=True)
        return load(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-a")
    parser.add_argument("--run-b")
    parser.add_argument("--comparison", choices=[p["id"] for p in comparisons()])
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        parser.error("Select a new analysis output; never overwrite a result")
    if not any([args.run_a, args.run_b, args.comparison]):
        inventory = load(DATA / "run-inventory.json")
        if inventory["v2_live_runs"]:
            parser.error("Live runs found; select explicit runs/comparison")
        save(args.out, {"analysis_version": VERSION, "status": "not-run", "model_results": None,
                        "inventory_sha256": digest(inventory),
                        "comparisons": [{**p, "result": None} for p in comparisons()],
                        "reason": "No authentic v2 model responses are available. Fixtures excluded."})
    elif not all([args.run_a, args.run_b, args.comparison]):
        parser.error("Supply both runs and a comparison")
    else:
        spec = next(p for p in comparisons() if p["id"] == args.comparison)
        save(args.out, analyze(validate_run(args.run_a), validate_run(args.run_b), spec))
    print(json.dumps({"output": str(args.out), "status": load(args.out)["status"]}))


if __name__ == "__main__":
    main()
