#!/usr/bin/env python3
"""Publication statistics reconstructed from new-version provider receipts only."""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations
from pathlib import Path

from common import DATA, DATASET, VERSION, digest, load, save, sha
from estimates import estimate, ranks, selection_shift, sign, wilson
from qa import assets, verify_final
from run import verify
from roster import checked, exact_run_set
from priors import gate as prior_gate
from authors import sensitivity, comparison_sensitivity
from graphs import component

FAMILIES = {"color": "Color", "shape-match": "Part-type"}
METRICS = ["A_acc", "NewAcc", "Both", "old_gold_retention", "other_wrong", "invalid_B",
           "valid_A", "valid_B", "valid_both", "conditional_adaptation", "conditional_old_retention"]


def pair_rows(manifest, validated, qa):
    observations = {r["observation_id"]: r for r in validated["rows"]}
    qa_pairs = {p["pair_id"]: p for p in qa["pairs"]}
    result = []
    for pair in manifest["pairs"]:
        a, b = observations[pair["a"]], observations[pair["b"]]
        assert a["gold"] != b["gold"]
        assert a["family"] == b["family"] == pair["family"]
        assert a["source_id"] == b["source_id"] == pair["source_id"]
        ca, cb = a["answer"] == a["gold"], b["answer"] == b["gold"]
        va, vb = a["valid_format"] is True, b["valid_format"] is True
        old = vb and b["answer"] == a["gold"]
        other = vb and not cb and not old
        assert sum([cb, old, other, not vb]) == 1
        q = qa_pairs[pair["pair_id"]]
        qa_decidable = q["both_decidable"]
        transition = ("correct" if ca else "wrong" if va else "invalid") + "->" + (
            "new-gold" if cb else "old-gold" if old else "other-wrong" if vb else "invalid")
        result.append({**pair, "display_name": FAMILIES[pair["family"]],
            "qa_both_decidable": qa_decidable, "qa_exclusion_reasons": q["exclusion_reasons"],
            "A_acc": int(ca), "NewAcc": int(cb), "Both": int(ca and cb),
            "old_gold_retention": int(old), "other_wrong": int(other), "invalid_B": int(not vb),
            "valid_A": int(va), "valid_B": int(vb), "valid_both": int(va and vb),
            "conditional_adaptation": int(cb) if ca else None,
            "conditional_old_retention": int(old) if ca else None,
            "A_outcome": "correct" if ca else "wrong" if va else "invalid",
            "B_outcome": "new-gold" if cb else "old-gold" if old else "other-wrong" if vb else "invalid",
            "transition": transition,
            "same_valid_wrong_answer": bool(va and vb and not ca and not cb and a["answer"] == b["answer"]),
            "failure_A": a["failure_reason"], "failure_B": b["failure_reason"],
            "a_answer": a["answer"], "b_answer": b["answer"], "a_gold": a["gold"], "b_gold": b["gold"],
            "a_receipt_file": a["receipt_file"], "b_receipt_file": b["receipt_file"]})
    return result


def summarize(rows):
    return {"pairs": len(rows), "sources": len({r["source_id"] for r in rows}),
            "metrics": {key: estimate(rows, key) for key in METRICS},
            "author_sensitivity": {key: {group:sensitivity(rows,key,group) for group in
                ["primary_author_id","contributor_cluster"]} for key in
                ["A_acc","NewAcc","Both","old_gold_retention","invalid_B"]},
            "transitions": dict(Counter(r["transition"] for r in rows)),
            "failure_reasons": {arm: dict(Counter(r["failure_" + arm] for r in rows if r["failure_" + arm]))
                                for arm in ["A", "B"]}}


def family_report(rows):
    selected = [r for r in rows if r["qa_both_decidable"]]
    reasons = sorted({reason for r in rows for reason in r["qa_exclusion_reasons"]})
    return {"full": summarize(rows), "both_decidable": summarize(selected),
        "exclusions": {reason: {"pairs": sum(reason in r["qa_exclusion_reasons"] for r in rows),
                               "sources": len({r["source_id"] for r in rows if reason in r["qa_exclusion_reasons"]})}
                       for reason in reasons},
        "qa_minus_full": {key: selection_shift(rows, selected, key) for key in
                          ["A_acc", "NewAcc", "Both", "old_gold_retention", "invalid_B", "valid_both"]},
        "interpretation": "Selection is descriptive; exclusions may change source composition. Reasons can overlap."}


def exact_macro(rows, key):
    """Rational point estimates prevent floating-order artifacts from breaking ties."""
    groups = defaultdict(list)
    for row in rows:
        if row[key] is not None:
            groups[row["source_id"]].append(row[key])
    means = [Fraction(sum(v), len(v)) for v in groups.values()]
    return sum(means, Fraction()) / len(means) if means else None


def comparisons(models, family, subset):
    groups = {m["run_id"]: [r for r in m["pair_rows"] if r["family"] == family
                           and (subset == "full" or r["qa_both_decidable"])] for m in models}
    groups = {k: v for k, v in groups.items() if v}
    names = sorted(groups)
    points = {key: {name: exact_macro(groups[name], key) for name in names}
              for key in ["A_acc", "NewAcc", "Both"]}
    ranked = {key: ranks(values) for key, values in points.items()}
    differences = []
    for x, y in combinations(names, 2):
        yr = {r["pair_id"]: r for r in groups[y]}
        assert {r["pair_id"] for r in groups[x]} == set(yr), "Different model comparison denominators"
        paired = [{"source_id": r["source_id"], **{key: r[key] - yr[r["pair_id"]][key] for key in METRICS
                   if key not in ["conditional_adaptation", "conditional_old_retention"]}}
                  for r in groups[x]]
        interval = {key: estimate(paired, key) for key in
                    ["A_acc", "NewAcc", "Both", "valid_A", "valid_B", "valid_both", "invalid_B"]}
        d_a, d_b = points["A_acc"][x] - points["A_acc"][y], points["Both"][x] - points["Both"][y]
        differences.append({"model_x": x, "model_y": y, "direction": "x-minus-y",
            "A_order": sign(d_a), "Both_order": sign(d_b), "strict_rank_reversal": d_a * d_b < 0,
            "tie_in_either_ranking": d_a == 0 or d_b == 0, "paired_differences": interval,
            "author_sensitivity": {k:comparison_sensitivity(groups[x],groups[y],k)
                                    for k in ["A_acc","NewAcc","Both"]},
            "direction_supported_by_source_interval": {k: bool(
                interval[k]["source_macro_ci95"] and
                (interval[k]["source_macro_ci95"][0]>0 or interval[k]["source_macro_ci95"][1]<0))
                for k in ["A_acc","NewAcc","Both"]},
            "inference": "One frozen invocation set. A point rank reversal is descriptive; intervals crossing zero support no directional ranking. No cross-call stability claim."})
    return {"family": family, "display_name": FAMILIES[family], "subset": subset,
            "ranking_basis": "source macro; exact rational comparisons; descending midrank for ties",
            "models": [{"run_id": name, **{key: {"value": float(points[key][name]), "rank": ranked[key][name]}
                                          for key in points}} for name in names],
            "pairwise": differences,
            "status": "available" if len(names) >= 2 else "requires-at-least-two-completed-model-runs"}


def ranking_consistency(full, subset):
    other = {(p["model_x"], p["model_y"]): p for p in subset["pairwise"]}
    rows = []
    for pair in full["pairwise"]:
        q = other.get((pair["model_x"], pair["model_y"]))
        rows.append({"model_x": pair["model_x"], "model_y": pair["model_y"],
                     "A_direction_agrees": pair["A_order"] == q["A_order"] if q else None,
                     "Both_direction_agrees": pair["Both_order"] == q["Both_order"] if q else None,
                     "reversal_agrees": pair["strict_rank_reversal"] == q["strict_rank_reversal"] if q else None})
    return rows


def raw_cases(model, observations):
    output = []
    rules = {"correct-to-new": lambda r: r["transition"] == "correct->new-gold",
             "correct-to-old": lambda r: r["transition"] == "correct->old-gold",
             "same-valid-wrong": lambda r: r["same_valid_wrong_answer"]}
    for family in FAMILIES:
        for kind, predicate in rules.items():
            eligible = [r for r in model["pair_rows"] if r["family"] == family and r["qa_both_decidable"] and predicate(r)]
            if not eligible:
                output.append({"family": family, "case_type": kind, "status": "no-qualifying-real-case"})
                continue
            row = min(eligible, key=lambda r: digest([model["run_id"], kind, r["pair_id"]]))
            raw = {}
            for arm in ["a", "b"]:
                o = observations[row[arm]]
                assert o["receipt_file"], "Cases require genuine saved responses on both sides"
                receipt = load(o["receipt_file"])
                assert receipt["evidence_kind"] == "provider-http-receipt"
                assert sha(o["receipt_file"]) == o["receipt_sha256"]
                raw[arm] = {"observation_id": o["observation_id"], "wire_observation_sha256": o["wire_observation_sha256"],
                    "request_sha256": o["request_sha256"], "receipt_file": o["receipt_file"],
                    "receipt_sha256": o["receipt_sha256"], "http_status": receipt["http_status"],
                    "raw_response": receipt["raw_response"], "verbatim_output": o["output"], "gold": o["gold"]}
            output.append({"run_id": model["run_id"], "family": family, "case_type": kind, "status": "real-receipt",
                           "pair_id": row["pair_id"], "source_id": row["source_id"], "arms": raw})
    return output


def auxiliary(validated, qa, pairs):
    """Separate interface control; no combined Color/Part-type measure."""
    byparent = {r["parent_task_id"]: r for r in pairs if r["family"] == "shape-match"}
    qarows = {r["observation_id"]: r for r in qa["rows"]}
    rows = []
    for r in validated["rows"]:
        if r["role"] != "position-reference-control":
            continue
        p = byparent[r["parent_task_id"]]
        rows.append({"observation_id": r["observation_id"], "parent_task_id": r["parent_task_id"],
            "source_id": r["source_id"], "position_acc": int(r["success"]), "valid_format": int(r["valid_format"]),
            "position_minus_label_A": int(r["success"]) - p["A_acc"],
            "qa_all_decidable": p["qa_both_decidable"] and qarows[r["observation_id"]]["final_decision"] == "decidable"})
    return {"role": "position-reference-control", "family": "shape-match", "display_name": "Part-type",
        "status": "available" if rows else "not-run",
        "full": {k: estimate(rows, k) for k in ["position_acc", "valid_format", "position_minus_label_A"]},
        "qa_decidable": {k: estimate([r for r in rows if r["qa_all_decidable"]], k)
                         for k in ["position_acc", "valid_format", "position_minus_label_A"]},
        "rows": rows, "interpretation": "Layout, isolation/access and reference interface all change; not an OCR causal effect."}


def graph_report(validated):
    _,_,audit=component()
    predictions={r["observation_id"]:r for r in validated["rows"]}
    rows=[]
    for p in audit["pairs"]:
        a,b=predictions[p["a"]],predictions[p["b"]]
        rows.append({**p,"accuracy":(a["success"]+b["success"])/2,
                     "both":a["success"]*b["success"],
                     "valid_both":int(a["valid_format"] and b["valid_format"])})
    return {"pair_rows":rows,"partitions":{role:{
        "metrics":{k:estimate([p for p in rows if p["role"]==role],k) for k in ["accuracy","both","valid_both"]},
        "author_sensitivity":sensitivity([p for p in rows if p["role"]==role],"both"),
        "both_pair_wilson_ci95":wilson(sum(p["both"] for p in rows if p["role"]==role),
                                     sum(p["role"]==role for p in rows))}
        for role in audit["summary"]},"interpretation":"Separate text-graph audit; never pooled with visual results."}


def build(run_root, destination, protocol_only=False):
    manifest, _, _ = assets()
    roster=checked()
    prior_gate()
    models = []
    qa_hashes = set()
    validated_runs={}
    if not protocol_only:
        directories=exact_run_set(run_root)
        for run_id,directory in directories.items():
            validated=verify(directory)
            assert validated["mode"]=="live-inference" and validated["status"] in ["complete","closed-interrupted"], (
                "Every roster run must be terminal genuine inference, including failures; dry runs are ineligible")
            validated_runs[run_id]=validated
    index=[]
    for entry in roster["entries"] if not protocol_only else []:
        expected={p["condition"]:p["run_id"] for p in entry["planned_runs"]}
        validated=validated_runs[expected["visual"]]
        assert validated["mode"] == "live-inference" and validated["status"] in ["complete","closed-interrupted"], (
            "Only completed real-inference manifests can register; dry runs and fixtures are not model results")
        qa = verify_final(validated["qa"]["file"], "all")
        qa_hashes.add(validated["qa"]["sha256"])
        pairs = pair_rows(manifest, validated, qa)
        run_id = entry["model_id"]
        model = {"run_id": run_id, "provenance": {k: validated[k] for k in [
            "model_revision", "provider", "adapter_hash", "index_sha256", "manifest_file", "manifest_sha256", "qa","started","finished"]},
            "families": {f: family_report([r for r in pairs if r["family"] == f]) for f in FAMILIES},
            "pair_rows": pairs, "auxiliary": auxiliary(validated, qa, pairs)}
        model["cases"] = raw_cases(model, {r["observation_id"]: r for r in validated["rows"]})
        noimage=validated_runs[expected["no-image"]]
        assert noimage["qa"]["sha256"]==validated["qa"]["sha256"]
        npairs=pair_rows(manifest,noimage,qa)
        model["no_image"]={"families":{f:family_report([r for r in npairs if r["family"]==f]) for f in FAMILIES},
                          "pair_rows":npairs,"interpretation":roster["no_image_policy"]}
        model["image_minus_no_image"]={}
        for family in FAMILIES:
            original=[r for r in pairs if r["family"]==family]
            baseline=[r for r in npairs if r["family"]==family]
            mapped={r["pair_id"]:r for r in baseline}
            differences=[{"source_id":r["source_id"],**{k:r[k]-mapped[r["pair_id"]][k] for k in
                         ["A_acc","NewAcc","Both","valid_both"]}} for r in original]
            model["image_minus_no_image"][family]={
                "source":{k:estimate(differences,k) for k in ["A_acc","NewAcc","Both","valid_both"]},
                "author":comparison_sensitivity(original,baseline,"Both")}
        model["graphs"]=graph_report(validated_runs[expected["graph"]])
        for condition,rid in expected.items():
            v=validated_runs[rid]
            index.append({"run_id":rid,"model_id":run_id,"condition":condition,
                "roster_entry_hash":digest(entry),"paper_row":run_id+"/"+condition,
                **{k:v[k] for k in ["manifest_file","manifest_sha256","request_index_sha256",
                                   "receipt_set_sha256","attempt_set_sha256","status","started","finished"]},
                "qa_snapshot_sha256":v["qa"]["sha256"] if v["qa"] else None})
        models.append(model)
    assert len(qa_hashes) <= 1, "Freeze one QA snapshot for all model comparisons"
    if not protocol_only:
        assert len(models)==len(roster["entries"]) and len(index)==roster["expected_run_count"]
    pending = load(DATA / "qa/initial/pending-summary.json")
    comparison = {}
    for f in FAMILIES:
        full, subset = comparisons(models, f, "full"), comparisons(models, f, "both_decidable")
        comparison[f] = {"full": full, "both_decidable": subset,
                         "full_subset_direction_agreement": ranking_consistency(full, subset)}
    report = {"analysis_version": VERSION, "dataset": DATASET,
        "status": "real-results" if models else "awaiting-human-QA-and-real-inference",
        "evidence_kind": "receipt-recomputed-analysis" if models else "protocol-only-no-model-results",
        "code_hashes": {name: sha(Path(__file__).with_name(name)) for name in ["analyze.py", "estimates.py","authors.py","roster.py"]},
        "model_roster_sha256":sha(DATA/"model-roster.json"),
        "roster_completeness":{"expected":roster["expected_run_count"],"included":len(index),
                               "complete":len(index)==roster["expected_run_count"]},
        "model_run_index":index,
        "answer_position_baselines":load(DATA/"answer-prior-audit.json")["families"],
        "index_sha256": sha(DATA / "observation-index.json"), "families": FAMILIES,
        "planned": {f: {"pairs": sum(p["family"] == f for p in manifest["pairs"]),
            "sources": len({p["source_id"] for p in manifest["pairs"] if p["family"] == f})} for f in FAMILIES},
        "qa": {"sha256": next(iter(qa_hashes)), "status": "verified"} if models else {
            "status": "pending", "primary_total": pending["primary_total"], "primary_final": pending["primary_final"],
            "raw_review_count": pending["raw_review_count"], "qa_comparable_pairs": pending["qa_comparable_pairs"],
            "snapshot": str(DATA / "qa/initial/pending-summary.json"),
            "sha256": sha(DATA / "qa/initial/pending-summary.json")},
        "models": models, "comparisons": comparison,
        "claims": {"pooled_visual_score": "prohibited", "real_rank_reversal": None if not models else "see family comparisons",
            "real_case_examples": None if not models else "see receipt-bound family cases",
            "diagnostic_value": "An empirical hypothesis; no model difference, stability or significance assumed."},
        "statistics": {"seed": 20260920, "resamples": 10000, "unit": "whole source",
            "primary": "equal-source mean of within-source pair outcomes",
            "conditional": "only A-correct pairs; sources without eligible pairs excluded and counted",
            "failure_denominator": "all planned observations, including missing/API/refusal/invalid output",
            "multiple_comparisons": "descriptive unadjusted intervals; exploratory pairwise comparisons",
            "case_selection": "first hash-ordered QA-decidable case per family/model/type; never synthesize missing cases"}}
    dest = Path(destination)
    assert not dest.exists(), "Write a new analysis snapshot"
    save(dest, report, immutable=True)
    if not protocol_only:
        save(dest.with_name(dest.stem+"-model-run-index.json"),{
            "model_roster_sha256":sha(DATA/"model-roster.json"),
            "analysis_sha256":sha(dest),"complete":True,"rows":index},immutable=True)
    print({"status": report["status"], "real_model_runs": len(models), "output": str(dest)})
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    parser.add_argument("--run-root",default=str(DATA/"model-runs"))
    parser.add_argument("--protocol-only",action="store_true")
    args = parser.parse_args()
    build(args.run_root, args.output, args.protocol_only)


if __name__ == "__main__":
    main()
