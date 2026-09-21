#!/usr/bin/env python3
"""Full Phase-2 derived ledgers and structural feasibility over sealed inputs.

Evaluator-only reconstruction is deliberately separate from the subprocess
Color predictor, which receives exactly one wire over stdin and no paths.
"""
import argparse
import base64
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import io
from itertools import combinations
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image

from baseline import ROOT, BASE, WORK, VERSION, checked, load, save, sha
from analyze import NO_IMAGE_INTERPRETATION, prompt_bytes
from common import digest, frozen
from estimates import estimate
from graphs import component
from graph_audit import predictions as graph_predictions
from single_image_baselines import CONTRACT

HERE = Path(__file__).resolve().parent
COLOR_NAME = CONTRACT["name"]
COLOR_LOCK = WORK / "work/single-image-baseline-lock.json"


def bytes_sha(value):
    return hashlib.sha256(value).hexdigest()


def write_lines(name, rows):
    path = WORK / name
    path.write_text("".join(json.dumps(r, sort_keys=True, ensure_ascii=True,
                                       allow_nan=False) + "\n" for r in rows))


def freeze_color():
    if COLOR_LOCK.exists():
        verify_color_lock()
        return
    run = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", str(HERE),
                          "-p", "test_single_image_baselines.py", "-v"],
                         capture_output=True, text=True)
    log = WORK / "work/single-image-synthetic-tests.txt"
    log.write_text(run.stdout + run.stderr)
    assert run.returncode == 0, log.read_text()
    save(COLOR_LOCK, {
        "frozen_at": datetime.now(timezone.utc).isoformat(), "contract": CONTRACT,
        "predictor_sha256": sha(HERE / "single_image_baselines.py"),
        "synthetic_tests_sha256": sha(HERE / "test_single_image_baselines.py"),
        "test_log_sha256": sha(log), "tests_returncode": run.returncode,
        "freeze_kind": "local pre-corpus commitment, not an external registration",
        "model_results_seen": False, "dataset_predictions_exist_at_freeze":
            (WORK / "single-image-color-baseline.json").exists(),
    })
    assert not load(COLOR_LOCK)["dataset_predictions_exist_at_freeze"]


def verify_color_lock():
    locked = load(COLOR_LOCK)
    assert locked["contract"] == CONTRACT
    assert locked["predictor_sha256"] == sha(HERE / "single_image_baselines.py")
    assert locked["synthetic_tests_sha256"] == sha(HERE / "test_single_image_baselines.py")
    assert locked["test_log_sha256"] == sha(WORK / "work/single-image-synthetic-tests.txt")


def recompute_gold(observation, bundle):
    """Private evaluator gold reconstruction; never called by the predictor."""
    spec, options = observation["render_spec"], observation["payload"]["options"]
    if observation["family"] == "color":
        matches = [o["id"] for o in options if o["label"] == spec["body_color"]["name"]]
    else:
        parts = {p["id"]: p for p in bundle["parts"]}
        target_type = parts[spec["target_id"]]["partNumber"]
        candidates = spec.get("candidate_ids")
        if candidates is None:
            candidates = []
            for option in options:
                ids = [key for key, label in spec["labels"].items() if label == option["label"]]
                if len(ids) != 1:
                    raise ValueError("candidate display reference is not structurally unique")
                candidates.append(ids[0])
        matches = [option["id"] for option, cid in zip(options, candidates)
                   if parts[cid]["partNumber"] == target_type]
    if len(matches) != 1:
        raise ValueError("source-derived gold is not unique")
    return matches[0]


def projection_check(reference, label, width, height):
    if reference is None:
        return {"anchor_in_canvas": False, "text_origin_in_canvas": False,
                "conservative_label_box_in_canvas": False, "reference": None}
    def inside(point):
        return len(point) == 2 and all(math.isfinite(v) for v in point) and (
            0 <= point[0] < width and 0 <= point[1] < height)
    x, y = reference["text"]
    # A conservative 16px advance per character for the recorded 16px monospace
    # renderer; not a pixel measurement or an occlusion/legibility certification.
    box = [x-5, y-13, x+16*len(label)+5, y+13]
    return {"anchor_in_canvas": inside(reference["anchor"]),
            "text_origin_in_canvas": inside(reference["text"]),
            "conservative_label_box_in_canvas": inside(box[:2]) and inside(box[2:]),
            "conservative_label_box": box, "reference": reference,
            "visibility": "pending-human"}


def enumerate_swaps(anchor, bundle, width, height):
    """Enumerate ALL unordered pairs of incorrect candidates, including failures."""
    spec = anchor["render_spec"]
    parts = {p["id"]: p for p in bundle["parts"]}
    target_type = parts[spec["target_id"]]["partNumber"]
    options = anchor["payload"]["options"]
    candidates = [cid for cid, label in spec["labels"].items()
                  if label in {o["label"] for o in options}]
    wrong = sorted(cid for cid in candidates if parts[cid]["partNumber"] != target_type)
    references = {r["id"]: r for r in spec["reference_positions"]}
    original_gold = recompute_gold(anchor, bundle)
    swaps = []
    for left, right in combinations(wrong, 2):
        changed = deepcopy(anchor)
        labels = changed["render_spec"]["labels"]
        labels[left], labels[right] = labels[right], labels[left]
        try:
            gold = recompute_gold(changed, bundle)
            unique = True
        except ValueError:
            gold, unique = None, False
        projections = {cid: projection_check(references.get(cid), labels[cid], width, height)
                       for cid in [left, right]}
        checks = {
            "both_in_current_operands": all(cid in spec["render_operands"] for cid in [left, right]),
            "distinct_display_labels": labels[left] != labels[right],
            "unique_gold_preserved": unique and gold == original_gold,
            "projected_anchors_in_canvas": all(r["anchor_in_canvas"] for r in projections.values()),
            "projected_text_origins_in_canvas": all(r["text_origin_in_canvas"] for r in projections.values()),
            "conservative_label_boxes_in_canvas": all(r["conservative_label_box_in_canvas"] for r in projections.values()),
        }
        swaps.append({
            "instance_ids": [left, right], "before_labels": [spec["labels"][left], spec["labels"][right]],
            "after_labels": [labels[left], labels[right]],
            "part_numbers": [parts[left]["partNumber"], parts[right]["partNumber"]],
            "different_source_part_types": parts[left]["partNumber"] != parts[right]["partNumber"],
            "gold_before": original_gold, "gold_after": gold, "checks": checks,
            "projections": projections, "machine_eligible": all(checks.values()),
            "missing_reasons": [k for k, passed in checks.items() if not passed],
            "visually_distinguishable": "pending-human",
        })
    return swaps


def attribution(source, authors):
    row = authors[source]
    return {"source_id": source, "source_cluster": source,
            "author_id": row["primary_author_id"], "author_cluster": row["contributor_cluster"]}


def coverage(rows):
    return {"parents": len(rows), "sources": len({r["source_id"] for r in rows}),
            "authors": len({r["author_id"] for r in rows}),
            "contributor_clusters": len({r["author_cluster"] for r in rows})}


def feasibility(manifest, bundles, index, authors):
    observations = {o["observation_id"]: o for o in manifest["observations"]}
    rows = []
    for pair in sorted(manifest["pairs"], key=lambda p: p["parent_task_id"]):
        if pair["family"] != "shape-match":
            continue
        anchor = observations[pair["a"]]
        dims = index[pair["a"]]
        swaps = enumerate_swaps(anchor, bundles[pair["source_id"]], dims["width"], dims["height"])
        rows.append({"parent_task_id": pair["parent_task_id"], "pair_id": pair["pair_id"],
                     "anchor_observation_id": pair["a"], **attribution(pair["source_id"], authors),
                     "candidate_swap_count": len(swaps),
                     "machine_eligible_swap_count": sum(s["machine_eligible"] for s in swaps),
                     "candidate_swaps": swaps, "selected_swap": None,
                     "visual_feasibility": "pending-human",
                     "zero_eligible_reasons": sorted({reason for s in swaps for reason in s["missing_reasons"]})
                         if swaps else ["fewer-than-two-incorrect-candidates"]})
    assert len(rows) == 67 and len({r["parent_task_id"] for r in rows}) == 67
    eligible = [r for r in rows if r["machine_eligible_swap_count"]]
    report = {
        "analysis_version": VERSION, "evidence_kind": "structural-feasibility-not-visual-qualification",
        "anchor_policy": "One proposed invariance partner per existing Part-type A; no stimuli selected or rendered.",
        "eligibility_rule": "Both incorrect candidates already rendered; unique unchanged source gold; "
                            "distinct labels; recorded anchors, text origins and conservative boxes in canvas.",
        "projection_limit": "Recorded projections and conservative text bounds only; "
                            "occlusion, label legibility and visible geometric distinction require blind review.",
        "coverage": {"all": coverage(rows), "machine_eligible": coverage(eligible)},
        "swap_count_distribution": dict(Counter(r["machine_eligible_swap_count"] for r in rows)),
        "enumerated_swaps": sum(len(r["candidate_swaps"]) for r in rows),
        "eligible_swaps": sum(r["machine_eligible_swap_count"] for r in rows),
        "zero_eligible_parent_ids": [r["parent_task_id"] for r in rows if not r["machine_eligible_swap_count"]],
        "missing_patterns": dict(Counter(reason for r in rows for s in r["candidate_swaps"]
                                        for reason in s["missing_reasons"])),
        "coverage_by_source": {s: {"all_parents": sum(r["source_id"] == s for r in rows),
                                   "eligible_parents": sum(r["source_id"] == s for r in eligible)}
                               for s in sorted({r["source_id"] for r in rows})},
        "coverage_by_author": {a: {"all_parents": sum(r["author_id"] == a for r in rows),
                                   "eligible_parents": sum(r["author_id"] == a for r in eligible)}
                               for a in sorted({r["author_id"] for r in rows})},
        "route_selected": None, "human_qualified_parents": None, "rows": rows,
    }
    save(WORK / "part-type-invariance-feasibility.json", report)
    return report


def run_color(manifest, wires, golds):
    verify_color_lock()
    outputs = {}
    observations = sorted((o for o in manifest["observations"] if o["family"] == "color"),
                          key=lambda o: o["observation_id"])
    assert len(observations) == 146
    # Fresh process for each observation, isolated Python imports and empty cwd.
    # Only the wire is passed on stdin. Evaluator golds are used below, after prediction.
    with tempfile.TemporaryDirectory(prefix="brickatlas-color-") as directory:
        for i, o in enumerate(observations, 1):
            oid = o["observation_id"]
            run = subprocess.run([sys.executable, "-I", str(HERE / "single_image_baselines.py")],
                                 cwd=directory, input=json.dumps(wires[oid]), capture_output=True,
                                 text=True, timeout=60,
                                 env={**os.environ, "OPENBLAS_NUM_THREADS": "1", "OMP_NUM_THREADS": "1"})
            assert run.returncode == 0, run.stderr
            prediction = json.loads(run.stdout)
            outputs[oid] = {"observation_id": oid, "input_messages_sha256": digest(wires[oid]["messages"]),
                            "prediction": prediction, "gold_choice_id": golds[oid],
                            "correct": int(prediction["choiceId"] == golds[oid])}
            if i % 25 == 0 or i == len(observations):
                print(f"Color single-wire predictions: {i}/146", flush=True)
    pairs = []
    for p in manifest["pairs"]:
        if p["family"] != "color":
            continue
        a, b = (outputs[p[arm]] for arm in ["a", "b"])
        pairs.append({"pair_id": p["pair_id"], "parent_task_id": p["parent_task_id"], "source_id": p["source_id"],
                      "a_prediction": a["prediction"]["choiceId"], "b_prediction": b["prediction"]["choiceId"],
                      "a_gold": a["gold_choice_id"], "b_gold": b["gold_choice_id"],
                      "A_acc": a["correct"], "NewAcc": b["correct"], "Both": a["correct"] * b["correct"]})
    report = {
        "analysis_version": VERSION, "evidence_kind": "deterministic-legal-single-image-baseline",
        "name": COLOR_NAME, "contract_lock_sha256": sha(COLOR_LOCK),
        "scope": CONTRACT["scope"], "inputs": "one frozen model-visible wire per isolated subprocess",
        "evaluator_only_fields": "IDs and independently recomputed gold are joined only AFTER prediction.",
        "observations": list(outputs.values()), "per_pair": pairs, "pairs": len(pairs),
        "metrics": {key: estimate(pairs, key) for key in ["A_acc", "NewAcc", "Both"]},
        "endpoint_correct": sum(o["correct"] for o in outputs.values()),
        "abstentions": sum(o["prediction"]["choiceId"] is None for o in outputs.values()),
        "failures": [o["observation_id"] for o in outputs.values() if not o["correct"]],
        "model_results_used": False, "human_qualification": "pending",
    }
    save(WORK / "single-image-color-baseline.json", report)
    return outputs, report


def graph_ledger(authors):
    wires, inspected, audit = component()  # Recomputes gold with BFS AND union-find.
    partitions = frozen("benchmark/ldraw-evidence-v2/graph-partitions.json")["roles"]
    training_ids = {p[k] for p in audit["pairs"] if p["gold_delta"] for k in ["a", "b"]}
    computed = graph_predictions(list(inspected.values()), [inspected[k] for k in sorted(training_ids)])
    assert computed == audit["predictions"]
    rows = []
    for oid, record in sorted(inspected.items()):
        payload = json.loads(wires[oid]["messages"][1]["content"][0]["text"])
        memberships = [{"pair_id": p["pair_id"], "role": p["role"],
                        "arm": "A" if p["a"] == oid else "B", "counterpart": p["b"] if p["a"] == oid else p["a"]}
                       for p in audit["pairs"] if oid in [p["a"], p["b"]]]
        assert memberships and all(m["pair_id"] in partitions[m["role"]] for m in memberships)
        nodes, edges = payload["input"]["nodes"], payload["input"]["edges"]
        target = next(n for n in nodes if n not in record["surviving_nodes"])
        rows.append({
            "observation_id": oid, "parent_task_id": record["parent_task_id"],
            **attribution(record["source_id"], authors), "family": "graph-removal",
            "pair_memberships": memberships, "partitions": sorted({m["role"] for m in memberships}),
            "wire_sha256": digest(wires[oid]),
            "wire_hash_definition": "SHA256 of canonical JSON wire; graph has no separate frozen wire file",
            "runner_binding_sha256": digest(wires[oid]["messages"]),
            "prompt_text_sha256": bytes_sha(prompt_bytes(wires[oid])),
            "nodes": nodes, "edges": edges, "node_count": len(nodes),
            "unique_edge_count": len({tuple(sorted(e)) for e in edges}),
            "deleted_node": target, "surviving_node_count": len(record["surviving_nodes"]),
            "surviving_edge_count": record["surviving_edges"],
            "gold_value": record["gold"], "gold_independently_recomputed": True,
            "gold_checks": {"bfs": record["bfs"], "union_find": record["union-find"]},
            "anonymous_features": record["features"], "baseline_predictions": computed[oid],
            "model_results_join_key": oid,
        })
    assert len(rows) == len(wires) == 219
    return rows


def build():
    verify_color_lock()
    manifest = checked(BASE / "visual-manifest.json")
    indices = checked(BASE / "observation-index.json")
    renders = checked(BASE / "renders.json")
    author_data = checked(BASE / "source-dependence.json")
    qa = checked(BASE / "qa/initial/pending-summary.json")
    assert qa["raw_review_count"] == 0 and all(r["final_decision"] == "pending" for r in qa["rows"])
    authors = {r["source_id"]: r for r in author_data["rows"]}
    index = {r["observation_id"]: r for r in indices["observations"]}
    rendered = {r["observation_id"]: r for r in renders["images"]}
    obs = {o["observation_id"]: o for o in manifest["observations"]}
    assert len(obs) == len(index) == len(rendered) == 347 and set(obs) == set(index) == set(rendered)
    bundles = {s: frozen(f"public/benchmark/ldraw-v2/models/{s}.json") for s in authors}
    wires, golds, pixel_hashes = {}, {}, {}
    for oid, o in obs.items():
        idx = index[oid]
        assert sha(ROOT / idx["file"]) == idx["wire_observation_sha256"]
        wire = load(ROOT / idx["file"])
        assert digest(wire["messages"]) == idx["messages_hash"]
        assert json.loads(wire["messages"][1]["content"][0]["text"]) == o["payload"]
        png = base64.b64decode(wire["messages"][1]["content"][1]["image_url"]["url"].split(",", 1)[1])
        assert bytes_sha(png) == idx["image_sha256"] == sha(ROOT / rendered[oid]["file"])
        with Image.open(io.BytesIO(png)) as image:
            assert list(image.size) == [idx["width"], idx["height"]]
            pixel_hashes[oid] = bytes_sha(np.asarray(image.convert("RGBA")).tobytes())
        golds[oid] = recompute_gold(o, bundles[o["source_id"]])
        assert golds[oid] == o["gold"]["choiceId"]
        wires[oid] = wire
    color, color_report = run_color(manifest, wires, golds)
    pairs_by_oid = {p[arm]: p for p in manifest["pairs"] for arm in ["a", "b"]}
    parent_anchor = {p["parent_task_id"]: p["a"] for p in manifest["pairs"]}
    visual = []
    for oid, o in sorted(obs.items()):
        pair = pairs_by_oid.get(oid)
        counterpart = pair["b" if pair["a"] == oid else "a"] if pair else parent_anchor[o["parent_task_id"]]
        baseline = {COLOR_NAME: {**color[oid]["prediction"], "correct": color[oid]["correct"],
                                "access": CONTRACT["access"]}} if oid in color else {}
        spec = o["render_spec"]
        visual.append({
            "observation_id": oid, "pair_id": pair["pair_id"] if pair else None,
            "parent_task_id": o["parent_task_id"], **attribution(o["source_id"], authors),
            "family": o["family"], "arm": o["arm"], "role": o["role"],
            "wire_sha256": index[oid]["wire_observation_sha256"], "image_sha256": index[oid]["image_sha256"],
            "counterpart_observation_id": counterpart,
            "counterpart_relation": "primary-pair" if pair else "same-parent-primary-A-descriptive-comparison",
            "image_pixels_unchanged_vs_counterpart": pixel_hashes[oid] == pixel_hashes[counterpart],
            "prompt_text_sha256": bytes_sha(prompt_bytes(wires[oid])),
            "options": o["payload"]["options"], "gold_choice_id": golds[oid],
            "gold_semantics": next(x["label"] for x in o["payload"]["options"] if x["id"] == golds[oid]),
            "gold_independently_recomputed": True,
            "gold_reconstruction_basis": "rendered-body-color" if o["family"] == "color" else "source-part-type",
            "reference_is_unique_in_image": "pending-human", "visibility_sufficient": "pending-human",
            "qa_final_decision": "pending", "human_qa": {
                "review_count": 0, "final_decision": "pending", "final_visual_choice": None, "exclusion_reasons": []},
            "legal_baseline_predictions": baseline, "model_results_join_key": oid,
            "exclusion_reason": None, "render_operand_count": len(spec["render_operands"]),
            "display_label_count": len(spec["labels"]),
        })
    noimage_rows = []
    for pair in manifest["pairs"]:
        a, b = pair["a"], pair["b"]
        same = prompt_bytes(wires[a]) == prompt_bytes(wires[b])
        assert same and golds[a] != golds[b]
        noimage_rows.append({"pair_id": pair["pair_id"], "family": pair["family"],
                             "a": a, "b": b, "requests_text_byte_identical": same,
                             "a_text_sha256": bytes_sha(prompt_bytes(wires[a])),
                             "b_text_sha256": bytes_sha(prompt_bytes(wires[b])),
                             "golds_differ": True})
    graph = graph_ledger(authors)
    possible = feasibility(manifest, bundles, index, authors)
    write_lines("visual-observation-audit-ledger.jsonl", visual)
    write_lines("graph-observation-audit-ledger.jsonl", graph)
    save(WORK / "no-image-request-audit.json", {
        "analysis_version": VERSION, "pairs": len(noimage_rows), "identical_text_pairs": len(noimage_rows),
        "interpretation": NO_IMAGE_INTERPRETATION, "rows": noimage_rows, "model_predictions": None,
    })
    assert len({r["observation_id"] for r in visual + graph}) == 566
    assert all(r["render_operand_count"] == r["display_label_count"] == 1
               for r in visual if r["family"] == "color")
    inputs = [BASE / name for name in ["visual-manifest.json", "observation-index.json", "renders.json",
              "source-dependence.json", "qa/initial/pending-summary.json", "model-roster.json"]]
    inputs += [ROOT / p for p in ["benchmark/ldraw-evidence-v2/graph-partitions.json",
                                  "benchmark/ldraw-evidence-v2/graph-audit.json",
                                  "benchmark/ldraw-evidence-v1/matched-graphs-v1/inputs.json"]]
    report = {
        "analysis_version": VERSION, "machine_status": "passed", "phase_status": "awaiting-route-decision",
        "counts": {"visual": len(visual), "graph": len(graph), "unique_total": 566,
                   "color_endpoints": len(color), "no_image_pairs": len(noimage_rows),
                   "feasibility_parents": len(possible["rows"])},
        "inputs": {str(p.relative_to(ROOT)): sha(p) for p in inputs},
        "outputs": {name: sha(WORK / name) for name in [
            "visual-observation-audit-ledger.jsonl", "graph-observation-audit-ledger.jsonl",
            "single-image-color-baseline.json", "part-type-invariance-feasibility.json", "no-image-request-audit.json"]},
        "code_hashes": {p.name: sha(p) for p in [HERE / name for name in [
            "measurement_audit.py", "single_image_baselines.py", "analyze.py"]]},
        "color_endpoint_correct": color_report["endpoint_correct"],
        "color_abstentions": color_report["abstentions"],
        "human_reviews": 0, "model_results": 0, "route_selected": None,
        "graph_hash_policy": "Canonical wire hash plus exact v3 runner messages binding; no invented graph image/index.",
        "source_cluster_policy": "source_cluster=source_id; author_id=primary_author_id; author_cluster=contributor_cluster.",
    }
    save(WORK / "work/phase-2-machine-validation.json", report)
    print(json.dumps({k: report[k] for k in ["machine_status", "counts", "color_endpoint_correct", "color_abstentions"]}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["freeze-color", "build"])
    args = parser.parse_args()
    freeze_color() if args.command == "freeze-color" else build()
