#!/usr/bin/env python3
"""Verify complete derived Phase-2 artifacts against their sealed authorities."""
from collections import Counter
import json
from pathlib import Path

from baseline import BASE, ROOT, WORK, checked, load, save, sha
from estimates import estimate
from measurement_audit import coverage, verify_color_lock
from graphs import component


def ledger(name, expected):
    lines = (WORK / name).read_text().splitlines()
    assert len(lines) == expected and all(lines)
    rows = [json.loads(line) for line in lines]
    assert len({r["observation_id"] for r in rows}) == expected
    return {r["observation_id"]: r for r in rows}


def verify():
    verify_color_lock()
    report = load(WORK / "work/phase-2-machine-validation.json")
    for relative, expected in report["inputs"].items():
        assert sha(ROOT / relative) == expected, relative
    for relative, expected in report["outputs"].items():
        assert sha(WORK / relative) == expected, relative
    for name, expected in report["code_hashes"].items():
        assert sha(Path(__file__).with_name(name)) == expected, name
    manifest = checked(BASE / "visual-manifest.json")
    indices = checked(BASE / "observation-index.json")
    observations = {o["observation_id"]: o for o in manifest["observations"]}
    pairs = {p["pair_id"]: p for p in manifest["pairs"]}
    index = {r["observation_id"]: r for r in indices["observations"]}
    visual = ledger("visual-observation-audit-ledger.jsonl", 347)
    graph = ledger("graph-observation-audit-ledger.jsonl", 219)
    assert set(visual) == set(observations) == set(index)
    assert not (set(visual) & set(graph))
    wires, inspected, graph_audit = component()
    assert set(graph) == set(wires)
    color = load(WORK / "single-image-color-baseline.json")
    color_rows = {o["observation_id"]: o for o in color["observations"]}
    assert len(color_rows) == len(color["observations"]) == 146
    assert set(color_rows) == {oid for oid, o in observations.items() if o["family"] == "color"}
    for oid, row in visual.items():
        o = observations[oid]
        for field in ["parent_task_id", "source_id", "family", "arm", "role"]:
            assert row[field] == o[field]
        assert row["wire_sha256"] == index[oid]["wire_observation_sha256"]
        assert row["image_sha256"] == index[oid]["image_sha256"]
        assert row["options"] == o["payload"]["options"]
        assert row["gold_choice_id"] == o["gold"]["choiceId"]
        assert row["gold_semantics"] == o["gold_semantics"]
        assert row["gold_independently_recomputed"] is True
        assert row["qa_final_decision"] == row["human_qa"]["final_decision"] == "pending"
        assert row["human_qa"]["review_count"] == 0 and row["human_qa"]["final_visual_choice"] is None
        assert row["reference_is_unique_in_image"] == row["visibility_sufficient"] == "pending-human"
        assert row["exclusion_reason"] is None and "model_results" not in row
        if row["role"] == "primary":
            assert oid in [pairs[row["pair_id"]]["a"], pairs[row["pair_id"]]["b"]]
            assert row["image_pixels_unchanged_vs_counterpart"] is False
        else:
            assert row["pair_id"] is None and row["arm"] is None
        if oid in color_rows:
            assert row["render_operand_count"] == row["display_label_count"] == 1
            result = row["legal_baseline_predictions"][color["name"]]
            assert result["choiceId"] == color_rows[oid]["prediction"]["choiceId"]
            assert result["correct"] == int(result["choiceId"] == row["gold_choice_id"])
        else:
            assert row["legal_baseline_predictions"] == {}
    for oid, row in graph.items():
        assert not ({"image_sha256", "options", "human_qa", "qa_final_decision",
                     "reference_is_unique_in_image", "visibility_sufficient"} & row.keys())
        assert row["gold_value"] == inspected[oid]["gold"]
        assert row["gold_checks"]["bfs"] == row["gold_checks"]["union_find"] == row["gold_value"]
        assert row["baseline_predictions"] == graph_audit["predictions"][oid]
        assert row["pair_memberships"]
    assert len(color["per_pair"]) == 73
    for row in color["per_pair"]:
        pair = pairs[row["pair_id"]]
        a, b = color_rows[pair["a"]], color_rows[pair["b"]]
        assert row["A_acc"] == a["correct"] and row["NewAcc"] == b["correct"]
        assert row["Both"] == a["correct"] * b["correct"]
    for key in ["A_acc", "NewAcc", "Both"]:
        assert color["metrics"][key] == estimate(color["per_pair"], key)
    assert color["endpoint_correct"] == sum(r["correct"] for r in color_rows.values())
    assert color["abstentions"] == sum(r["prediction"]["choiceId"] is None for r in color_rows.values())
    assert set(color["failures"]) == {r["observation_id"] for r in color_rows.values() if not r["correct"]}
    noimage = load(WORK / "no-image-request-audit.json")
    assert len(noimage["rows"]) == noimage["pairs"] == noimage["identical_text_pairs"] == 140
    assert {r["pair_id"] for r in noimage["rows"]} == set(pairs)
    assert all(r["requests_text_byte_identical"] and r["golds_differ"] and
               r["a_text_sha256"] == r["b_text_sha256"] for r in noimage["rows"])
    feasibility = load(WORK / "part-type-invariance-feasibility.json")
    expected = {p["parent_task_id"] for p in pairs.values() if p["family"] == "shape-match"}
    assert len(feasibility["rows"]) == len(expected) == 67
    assert {r["parent_task_id"] for r in feasibility["rows"]} == expected
    assert feasibility["route_selected"] is None
    zero = set()
    for row in feasibility["rows"]:
        swaps = row["candidate_swaps"]
        assert len(swaps) == row["candidate_swap_count"]
        assert row["machine_eligible_swap_count"] == sum(s["machine_eligible"] for s in swaps)
        assert row["different_source_type_swap_count"] == sum(
            s["machine_eligible"] and s["different_source_part_types"] for s in swaps)
        assert row["selected_swap"] is None and row["visual_feasibility"] == "pending-human"
        if not row["machine_eligible_swap_count"]:
            zero.add(row["parent_task_id"])
        for s in swaps:
            assert s["machine_eligible"] == all(s["checks"].values())
            assert s["visually_distinguishable"] == "pending-human"
    assert zero == set(feasibility["zero_eligible_parent_ids"])
    different = [r for r in feasibility["rows"] if r["different_source_type_swap_count"]]
    assert feasibility["coverage"]["different_source_type_proxy"] == coverage(different)
    assert feasibility["different_source_type_proxy"]["eligible_swaps"] == sum(
        r["different_source_type_swap_count"] for r in feasibility["rows"])
    result = {
        "status": "passed", "visual_rows": len(visual), "graph_rows": len(graph),
        "unique_observations": len(visual) + len(graph),
        "color_endpoint_correct": color["endpoint_correct"], "color_abstentions": color["abstentions"],
        "color_both_hits": sum(r["Both"] for r in color["per_pair"]),
        "no_image_identical_pairs": 140, "feasibility_coverage": feasibility["coverage"],
        "graph_pair_roles": dict(Counter(p["role"] for p in graph_audit["pairs"])),
        "human_reviews": 0, "model_results": 0, "route_decision": "pending-user",
    }
    save(WORK / "work/phase-2-verification.json", result)
    print(json.dumps(result))


if __name__ == "__main__":
    verify()
