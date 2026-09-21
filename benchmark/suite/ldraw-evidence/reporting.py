"""Versioned report roles and state-driven receipt-to-table publication."""
import argparse
from collections import Counter
from pathlib import Path
import json

from common import ROOT, DATA, VERSION, digest, load, save, sha, public_tasks, read_frozen, dataset_lock
from estimators import estimate, paired_difference
from evidence_adaptation import validate_run, comparisons, analyze

GROUPS = {
    "core-visual": ["color", "shape-match"],
    "structural-evidence": ["neighbors", "graph-removal"],
    "nonconstant-controls": ["distance", "interface", "coverage", "source-step", "restore-instance"],
    "constant-controls": ["evidence-limit", "source-sequence"],
}
NAMES = {"color": "Color", "shape-match": "Part-type", "neighbors": "Neighbors",
         "graph-removal": "Graph deletion", "distance": "Distance", "interface": "Interface",
         "coverage": "Coverage", "source-step": "Step lookup", "restore-instance": "Restoration",
         "evidence-limit": "Evidence limit", "source-sequence": "Step sequence"}


def selection():
    tasks = public_tasks()
    if len({f for fs in GROUPS.values() for f in fs}) != sum(map(len, GROUPS.values())):
        raise ValueError("Overlapping report families")
    if set(NAMES) != {t["family"] for t in tasks.values()}:
        raise ValueError("Unassigned task family")
    plan = read_frozen("benchmark/paper/ldraw-v2-experiments.json")
    families = {f: {"role": next(g for g, fs in GROUPS.items() if f in fs),
                    "task_ids": sorted(t["id"] for t in tasks.values() if t["family"] == f),
                    "sources": sorted({t["modelId"] for t in tasks.values() if t["family"] == f})}
                for f in NAMES}
    return {"analysis_version": VERSION, "dataset_hash": digest(dataset_lock()),
            "frozen_plan_sha256": sha(ROOT / "benchmark/paper/ldraw-v2-experiments.json"),
            "all_task_ids": sorted(tasks), "families": families,
            "groups": {g: sorted(t["id"] for t in tasks.values() if t["family"] in fs) for g, fs in GROUPS.items()},
            "conditions": {c["id"]: c["taskIds"] for c in plan["conditions"]},
            "exclusions": [], "ranking_policy": "Separate visual and structural families; no composite capability ranking",
            "qa_policy": "No silent exclusion. Full denominators and pending/failed QA retained; comparable visual subset requires independent reviews of both exact wire observations."}


def model_revision(adapter):
    return {"model_id": adapter["modelId"], "api_revision": adapter["apiRevision"],
            "checkpoint_sha256": adapter["checkpointSha256"], "provider": adapter["provider"]}


def result_key(revision, condition, dataset_hash, adapter_hash):
    return digest({"model_revision": revision, "condition": condition, "dataset_hash": dataset_hash,
                   "analysis_version": VERSION, "adapter_hash": adapter_hash})


def new_index(sel):
    entries = []
    for path in sorted((ROOT / "benchmark/suite/ldraw-v2/model-adapters").glob("*.json")):
        adapter = read_frozen(str(path.relative_to(ROOT)))
        revision = model_revision(adapter)
        for condition, ids in sel["conditions"].items():
            entries.append({"key": result_key(revision, condition, sel["dataset_hash"], digest(adapter)),
                            "model_revision": revision, "condition": condition,
                            "dataset_hash": sel["dataset_hash"], "adapter_hash": digest(adapter),
                            "analysis_version": VERSION, "expected_task_ids": ids,
                            "status": "not-run", "manifest": None, "analysis": None, "metrics": None})
    return {"analysis_version": VERSION, "selection_hash": digest(sel),
            "evidence_kind": "real-benchmark-only", "entries": entries, "paired_analyses": [],
            "human_results": None, "human_status": "not-run"}


def family_metrics(rows):
    denominator = len(rows)
    scored = [{"source_id": r["source_id"], "parent_task_id": r["parent_task_id"],
               "success": r["success"], "valid": r["valid_format"]} for r in rows]
    return {"items": denominator, "sources": len({r["source_id"] for r in rows}),
            "successes": sum(r["success"] for r in rows),
            "missing_or_failed": sum(r["success"] == 0 for r in rows),
            "failure_reasons": dict(Counter(r["failure_reason"] or "correct" for r in rows)),
            "accuracy": estimate(scored, "success"), "format_validity": estimate(scored, "valid"),
            "conditional_semantic_accuracy": {
                "denominator": sum(r["valid_format"] for r in rows),
                "value": (sum(r["success"] for r in rows) / sum(r["valid_format"] for r in rows))
                if any(r["valid_format"] for r in rows) else None},
            "visual_QA_pending": sum(bool(r["images"]) for r in rows)}


def summarize_run(run, sel, condition=None):
    if run["status"] != "complete":
        raise ValueError("Completed receipts required for numbers")
    condition = condition or run["condition"]
    expected = sel["conditions"][condition]
    if sorted(expected) != sorted(run["task_ids"]) or len(expected) != len(run["rows"]):
        raise ValueError("Run denominator differs from selected condition")
    if run["dataset_hash"] != sel["dataset_hash"]:
        raise ValueError("Selected dataset mismatch")
    by_family = {f: family_metrics([r for r in run["rows"] if r["family"] == f])
                 for f in NAMES if any(r["family"] == f for r in run["rows"])}
    baseline = {r["task_id"]: r for r in load(DATA / "node-prior-audit.json")["rows"]}
    graph_rows = [{**r, "node_only": baseline[r["task_id"]]["hit"],
                   "fixed_four": baseline[r["task_id"]]["fixed4_hit"], "BFS": 1,
                   "deficit": baseline[r["task_id"]]["deficit"]}
                  for r in run["rows"] if r["family"] == "graph-removal" and condition == "standard"]
    graph_comparison = None
    if graph_rows:
        graph_comparison = {
            "paired_model_minus_baseline": {k: paired_difference(graph_rows, "success", k)
                                           for k in ["node_only", "fixed_four", "BFS"]},
            "deficit_strata": {label: family_metrics([r for r in graph_rows if (r["deficit"] == 0) == easy])
                               for label, easy in [("zero", True), ("positive", False)]}}
    return {"by_family": by_family, "natural_graph_baseline_comparison": graph_comparison,
            "by_role": {g: family_metrics([r for r in run["rows"] if r["family"] in fs])
                        for g, fs in GROUPS.items() if any(r["family"] in fs for r in run["rows"])},
            "all_task_descriptive": family_metrics(run["rows"]),
            "interpretation": "Visual scores are provisional until exact-wire QA; no all-task capability ranking."}


def register(index, sel, run_directory, output_dir, allow_synthetic=False):
    run = validate_run(run_directory, allow_synthetic)
    allowed = ["live-inference"]
    if allow_synthetic and index["evidence_kind"] == "synthetic-validation-only":
        allowed = ["synthetic-fixture-not-benchmark"]
    if run["evidence_kind"] not in allowed:
        raise ValueError("Offline/synthetic records cannot enter the real result index")
    metrics = summarize_run(run, sel)
    key = result_key(run["model_revision"], run["condition"], run["dataset_hash"], run["adapter_hash"])
    entry = next((e for e in index["entries"] if e["key"] == key), None)
    if entry is None:
        raise ValueError("Run not in selected model/condition plan; create a separately versioned index")
    if entry["status"] != "not-run":
        raise ValueError("Result already registered; immutable entries cannot be overwritten")
    output = Path(output_dir) / f"{key}.json"
    if output.exists():
        raise ValueError("Analysis receipt already exists")
    save(output, {"run": run, "metrics": metrics})
    entry.update(status="complete", manifest={"file": run["manifest"], "sha256": run["manifest_sha256"]},
                 analysis={"file": str(output.resolve().relative_to(ROOT)), "sha256": sha(output)}, metrics=metrics)


def verify_index(index, sel, recompute=True, allow_synthetic=False):
    if index["analysis_version"] != VERSION or index["selection_hash"] != digest(sel):
        raise ValueError("Index selection/version mismatch")
    keys = set()
    for e in index["entries"]:
        if e["key"] in keys:
            raise ValueError("Duplicate result index key")
        keys.add(e["key"])
        if e["key"] != result_key(e["model_revision"], e["condition"], e["dataset_hash"], e["adapter_hash"]):
            raise ValueError("Incorrect result index key")
        if e["analysis_version"] != VERSION or e["dataset_hash"] != sel["dataset_hash"]:
            raise ValueError("Result dataset/version mismatch")
        if e["expected_task_ids"] != sel["conditions"][e["condition"]]:
            raise ValueError("Result denominator mismatch")
        if e["status"] == "not-run":
            if any(e[k] is not None for k in ["manifest", "analysis", "metrics"]):
                raise ValueError("Unrun result must remain null")
        elif e["status"] == "complete":
            for k in ["manifest", "analysis"]:
                if not e[k] or sha(ROOT / e[k]["file"]) != e[k]["sha256"]:
                    raise ValueError(f"Missing/changed completed {k}")
            stored = load(ROOT / e["analysis"]["file"])
            fresh = validate_run((ROOT / e["manifest"]["file"]).parent, allow_synthetic) if recompute else stored["run"]
            allowed = ["live-inference"]
            if allow_synthetic and index["evidence_kind"] == "synthetic-validation-only":
                allowed = ["synthetic-fixture-not-benchmark"]
            if fresh["evidence_kind"] not in allowed:
                raise ValueError("Fixture or dry run in real result index")
            if any(fresh[k] != e[k] for k in ["model_revision", "condition", "dataset_hash", "adapter_hash"]):
                raise ValueError("Indexed provenance mismatch")
            metrics = summarize_run(fresh, sel)
            if metrics != e["metrics"] or metrics != stored["metrics"]:
                raise ValueError("Published metric differs from receipt recomputation")
            if fresh != stored["run"]:
                raise ValueError("Validated run changed since ingestion")
        else:
            raise ValueError("Unknown result state")
    completed = {e["key"]: e for e in index["entries"] if e["status"] == "complete"}
    expected_pairs = {(s["id"], a["key"], b["key"])
                      for s in comparisons() for a in completed.values() for b in completed.values()
                      if a["condition"] == s["a"] and b["condition"] == s["b"]
                      and all(a[k] == b[k] for k in ["model_revision", "adapter_hash", "dataset_hash"])}
    actual_pairs = [(p["comparison"], p["key_A"], p["key_B"]) for p in index["paired_analyses"]]
    if len(set(actual_pairs)) != len(actual_pairs) or set(actual_pairs) != expected_pairs:
        raise ValueError("Paired result index incomplete/duplicated")
    for pair in index["paired_analyses"]:
        if sha(ROOT / pair["file"]) != pair["sha256"]:
            raise ValueError("Paired result changed")
        runs = [load(ROOT / completed[pair[k]]["analysis"]["file"])["run"] for k in ["key_A", "key_B"]]
        spec = next(s for s in comparisons() if s["id"] == pair["comparison"])
        if analyze(*runs, spec) != load(ROOT / pair["file"]):
            raise ValueError("Paired metric differs from receipt recomputation")
    return {"status": "passed", "records": len(keys),
            "complete": sum(e["status"] == "complete" for e in index["entries"]),
            "not_run": sum(e["status"] == "not-run" for e in index["entries"])}


def compute_pairs(index, sel, directory):
    completed = [e for e in index["entries"] if e["status"] == "complete"]
    pairs = []
    for spec in comparisons():
        for a in [e for e in completed if e["condition"] == spec["a"]]:
            matches = [b for b in completed if b["condition"] == spec["b"] and all(a[k] == b[k] for k in
                       ["model_revision", "adapter_hash", "dataset_hash"])]
            for b in matches:
                av, bv = [load(ROOT / e["analysis"]["file"])["run"] for e in [a, b]]
                result = analyze(av, bv, spec)
                path = Path(directory) / f'{spec["id"]}-{a["key"]}.json'
                if path.exists() and load(path) != result:
                    raise ValueError("Refuse to replace paired analysis")
                if not path.exists():
                    save(path, result)
                pairs.append({"comparison": spec["id"], "key_A": a["key"], "key_B": b["key"],
                              "file": str(path.resolve().relative_to(ROOT)), "sha256": sha(path)})
    index["paired_analyses"] = pairs


def tex_escape(text):
    for a, b in [("\\", r"\textbackslash{}"), ("_", r"\_"), ("%", r"\%"), ("&", r"\&"), ("#", r"\#")]:
        text = text.replace(a, b)
    return text


def table_tex(index, sel, group):
    families = GROUPS[group]
    lines = [r"\begin{tabular}{lrrr}", r"\toprule",
             r"Family / model & $N$ & Sources & Source macro (\%) \\", r"\midrule"]
    completed = [e for e in index["entries"] if e["status"] == "complete" and e["condition"] == "standard"]
    for f in families:
        meta = sel["families"][f]
        if not completed:
            lines.append(f'{NAMES[f]} & {len(meta["task_ids"])} & {len(meta["sources"])} & -- \\\\')
        for e in completed:
            metric = e["metrics"]["by_family"][f]
            acc = metric["accuracy"]
            ci = acc["source_macro_ci95"]
            lines.append(f'{NAMES[f]} / {tex_escape(e["model_revision"]["model_id"])} & {metric["items"]} & '
                         f'{metric["sources"]} & {100*acc["source_macro"]:.2f} [{100*ci[0]:.2f}, {100*ci[1]:.2f}] \\\\')
    lines += [r"\bottomrule", r"\end{tabular}", ""]
    return "\n".join(lines)


def paired_table_tex(index, visual):
    chosen = ["visual-mismatch", "label-binding", "camera", "color-nuisance",
              "background-only", "view-access"] if visual else ["edge-causal-control", "edge-equivalence"]
    lines = [r"\begin{tabular}{lrrr}", r"\toprule",
             r"Comparison & $N$ & $A,B$ correct (\%) & $B$ correct (\%) \\", r"\midrule"]
    for spec in [s for s in comparisons() if s["id"] in chosen]:
        pairs = [p for p in index["paired_analyses"] if p["comparison"] == spec["id"]]
        if not pairs:
            lines.append(f'{tex_escape(spec["id"])} & {len(spec["taskIds"])} & -- & -- \\\\')
        for pair in pairs:
            result = load(ROOT / pair["file"])
            m = result["summary"]["metrics"]
            lines.append(f'{tex_escape(spec["id"] + " / " + result["model_revision"]["model_id"])} & '
                         f'{result["summary"]["denominator"]} & {100*m["both_correct"]["source_macro"]:.2f} & '
                         f'{100*m["B_correct"]["source_macro"]:.2f} \\\\')
    return "\n".join(lines + [r"\bottomrule", r"\end{tabular}", ""])


def baseline_table_tex():
    audit = load(DATA / "node-prior-audit.json")
    lines = [r"\begin{tabular}{lrrr}", r"\toprule",
             r"Algorithmic baseline & Micro (\%) & Source macro (\%) & Both (\%) \\", r"\midrule"]
    names = {"node-count-only": "Node count only", "fixed-answer-4": "Always four", "graph-algorithm": "BFS / union-find"}
    for k, v in audit["baselines"].items():
        natural, both = v["natural"], v["paired_both_correct"]
        lines.append(f'{names[k]} & {100*natural["micro"]:.2f} & {100*natural["source_macro"]:.2f} & '
                     f'{100*both["source_macro"]:.2f} \\\\')
    return "\n".join(lines + [r"\bottomrule", r"\end{tabular}", ""])


def publish(index, sel, out, allow_synthetic=False):
    verify_index(index, sel, allow_synthetic=allow_synthetic)
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    for group in GROUPS:
        (out / f"{group}.tex").write_text(table_tex(index, sel, group))
    for visual, name in [(True, "paired-visual"), (False, "paired-structural")]:
        (out / f"{name}.tex").write_text(paired_table_tex(index, visual))
    (out / "graph-baselines.tex").write_text(baseline_table_tex())
    all_lines = [r"\begin{tabular}{lrrr}", r"\toprule",
                 r"Model & $N$ & Micro (\%) & Source macro (\%) \\", r"\midrule"]
    for entry in [e for e in index["entries"] if e["condition"] == "standard"]:
        name = tex_escape(entry["model_revision"]["model_id"])
        if entry["status"] == "not-run":
            all_lines.append(f'{name} & {len(entry["expected_task_ids"])} & -- & -- \\\\')
        else:
            m = entry["metrics"]["all_task_descriptive"]
            all_lines.append(f'{name} & {m["items"]} & {100*m["accuracy"]["micro"]:.2f} & '
                             f'{100*m["accuracy"]["source_macro"]:.2f} \\\\')
    (out / "all-task-descriptive.tex").write_text("\n".join(all_lines + [r"\bottomrule", r"\end{tabular}", ""]))
    tasks = public_tasks()
    save(out / "source-coverage.json", {
        source: {f: sum(t["family"] == f and t["modelId"] == source for t in tasks.values()) for f in NAMES}
        for source in sorted({t["modelId"] for t in tasks.values()})})
    save(out / "all-results.json", index)
    save(out / "table-provenance.json", {"analysis_version": VERSION, "index_hash": digest(index),
         "selection_hash": digest(sel), "table_hashes": {p.name: sha(p) for p in sorted(out.glob("*.tex"))},
         "source_cluster_CI": "10000 resamples; parent within source; seed 20260919",
         "null_display": "-- means not run, never zero", "model_results_status":
         "complete-or-partial" if any(e["status"] == "complete" for e in index["entries"]) else "not-run"})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["initialize", "register", "verify", "publish"])
    parser.add_argument("--index", type=Path, default=DATA / "results-index.json")
    parser.add_argument("--run", type=Path)
    parser.add_argument("--out-index", type=Path)
    parser.add_argument("--out", type=Path, default=DATA / "generated")
    args = parser.parse_args()
    sel = selection()
    if args.command == "initialize":
        if args.index.exists() or (DATA / "report-selection.json").exists():
            parser.error("Selection/index already exist; never silently overwrite")
        save(DATA / "report-selection.json", sel)
        save(args.index, new_index(sel))
    else:
        if load(DATA / "report-selection.json") != sel:
            parser.error("Selected manifest changed")
        index = load(args.index)
        if args.command == "register":
            if not args.run or not args.out_index or args.out_index.exists():
                parser.error("Supply --run and a NEW --out-index path")
            verify_index(index, sel)
            register(index, sel, args.run, DATA / "results")
            compute_pairs(index, sel, DATA / "paired-results")
            verify_index(index, sel)
            save(args.out_index, index)
        elif args.command == "verify":
            print(json.dumps(verify_index(index, sel), indent=2))
        else:
            publish(index, sel, args.out)


if __name__ == "__main__":
    main()
