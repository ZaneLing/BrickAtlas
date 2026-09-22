#!/usr/bin/env python3
"""Check all certificates, interventions, split boundaries and native PNG edits."""
import argparse
import itertools
from collections import defaultdict

import numpy as np
from PIL import Image

from common import HERE, ROOT, VERSION, digest, filehash, read, reference, write
from evaluate import evaluate, solve


def optimal_sets(answer):
    return {frozenset(s["restored"]) for s in answer["solutions"]}


def verify(images=True):
    public, gold = read(HERE / "public.json"), read(HERE / "gold.json")
    truth = {t["id"]: t["answer"] for t in gold["tasks"]}
    ledger = read(HERE / "sampling-ledger.json")
    groups = defaultdict(list)
    for task in public["tasks"]:
        answer = truth[task["id"]]
        independent = solve(task["input"], answer["bound_terminal"])
        assert optimal_sets(independent) == optimal_sets(answer), task["id"]
        result = evaluate(task["input"], answer["bound_terminal"], answer)
        assert result["repair_exact"], (task["id"], result)
        assert len(task["input"]["missing"]) <= 8
        assert independent["minimum_cost"] >= 2
        assert set(task["input"]["missing"]).isdisjoint(task["input"]["candidate_ids"])
        assert set(task["input"]["missing"]).isdisjoint(task["input"]["fixed_terminals"])
        groups[task["construction_id"]].append(task)
    audit = []
    for cid, tasks in groups.items():
        cells = {(t["replicate"], t["structural_arm"], t["visual_arm"]): t for t in tasks}
        assert len(tasks) == len(cells) == 12
        assert len({t["split"] for t in tasks}) == 1
        for rep, fault in itertools.product(range(2), ("fault_0", "fault_1")):
            a, c, p = [cells[rep, fault, arm] for arm in ("anchor", "changing", "preserving")]
            assert a["input"] == c["input"] == p["input"], "Visual pair changed public text"
            assert optimal_sets(truth[a["id"]]).isdisjoint(optimal_sets(truth[c["id"]]))
            assert truth[a["id"]] == truth[p["id"]]
        for rep, arm in itertools.product(range(2), ("anchor", "changing", "preserving")):
            a, b = [cells[rep, f, arm] for f in ("fault_0", "fault_1")]
            assert a["image"] == b["image"]
            assert truth[a["id"]]["bound_terminal"] == truth[b["id"]]["bound_terminal"]
            assert optimal_sets(truth[a["id"]]).isdisjoint(optimal_sets(truth[b["id"]]))
            assert len(set(a["input"]["missing"]) ^ set(b["input"]["missing"])) == 2
            assert {k: v for k, v in a["input"].items() if k != "missing"} == \
                {k: v for k, v in b["input"].items() if k != "missing"}
            assert sum(x != y for x, y in zip(a["input"]["missing"], b["input"]["missing"])) == 1
        record = next(r for r in ledger["records"] if r.get("construction_id") == cid)
        for fault, arm in itertools.product(("fault_0", "fault_1"), ("anchor", "changing", "preserving")):
            mapped = []
            for rep in range(2):
                task = cells[rep, fault, arm]
                inverse = {v: k for k, v in record["private_id_maps"][rep].items()}
                answer = truth[task["id"]]
                mapped.append(({frozenset(inverse[v] for v in s["restored"]) for s in answer["solutions"]},
                               inverse[answer["bound_terminal"]]))
            assert mapped[0] == mapped[1], "ID randomization changed semantics"
        audit.append({"construction_id": cid, "split": tasks[0]["split"],
                      "visual_changing_disjoint_complete_sets": True,
                      "visual_preserving_identical_complete_answers": True,
                      "structural_disjoint_complete_sets": True,
                      "id_equivariance": True,
                      "minimum_costs": sorted({truth[t["id"]]["minimum_cost"] for t in tasks}),
                      "optimum_counts": sorted({len(truth[t["id"]]["solutions"]) for t in tasks}),
                      "nodes": record["parts"], "edges": record["recognized_edges"],
                      "cycle_rank": record["recognized_edges"] - record["parts"] + 1,
                      "template_group": record["template_group"]})
    selected = [r for r in ledger["records"] if r.get("construction_id")]
    for record in selected:
        manifest = read(ROOT / f"public/models/{record['source_id']}/manifest.json")
        bundle = read(ROOT / f"public/benchmark/ldraw-v2/models/{record['source_id']}.json")
        descendants = {record["submodel_id"]}
        while True:
            more = {s["id"] for s in manifest["submodels"] if s["parentId"] in descendants}
            if more <= descendants:
                break
            descendants |= more
        ids = {p["instanceId"] for p in manifest["instances"] if p["parentSubmodelId"] in descendants}
        assert ids == set(record["nodes"])
        edges = {frozenset((e["a"], e["b"])) for e in bundle["audit"]["edges"] if {e["a"], e["b"]} <= ids}
        assert edges == {frozenset(e) for e in record["edges"]}
        assert not any(set(pair) <= ids for pair in bundle["audit"]["nonMatingCollisionPairs"])
        assert ids.isdisjoint(p["instanceId"] for p in bundle["audit"]["unsupported"])
    for key in ("source_id", "dependence_group", "design_group", "template_group"):
        dev = {r[key] for r in selected if r["split"] == "dev"}
        heldout = {r[key] for r in selected if r["split"] == "heldout"}
        assert not dev & heldout, (key, dev & heldout)
    contributors = {s["source_id"]: set(s["contributors"]) for s in ledger["sources"]}
    assert not set.union(*(contributors[r["source_id"]] for r in selected if r["split"] == "dev")) & \
        set.union(*(contributors[r["source_id"]] for r in selected if r["split"] == "heldout"))
    for a, b in itertools.combinations(selected, 2):
        if a["source_id"] == b["source_id"]:
            assert set(a["nodes"]).isdisjoint(b["nodes"]), "Nested or overlapping selection"
    mesh_files = []
    for source in ledger["sources"]:
        for key in ("manifest", "graph"):
            assert filehash(ROOT / source[key]["path"]) == source[key]["sha256"]
        manifest_path = ROOT / source["manifest"]["path"]
        for chunk in read(manifest_path)["chunks"]:
            path = manifest_path.parent / chunk["url"]
            assert filehash(path) == chunk["sha256"], path
            mesh_files.append(reference(path))
    image_rows = []
    card_occupancy = []
    if images:
        captures = read(HERE / "captures.json")
        assert captures["renderer_sha256"] == filehash(HERE / "render.ts")
        assert captures["specs_sha256"] == filehash(HERE / "render-specs.json")
        frames = {f["file"]: f for f in captures["frames"]}
        for cid, tasks in groups.items():
            for rep in range(2):
                cells = {t["visual_arm"]: t for t in tasks if t["replicate"] == rep and t["structural_arm"] == "fault_0"}
                arrays = {}
                for arm, task in cells.items():
                    frame = frames[task["image"]]
                    assert filehash(ROOT / task["image"]) == frame["sha256"]
                    assert frame["source_poses_preserved"] and not frame["geometry_modified"]
                    arr = np.asarray(Image.open(ROOT / task["image"]).convert("RGB"))
                    assert arr.shape == (900, 1600, 3)
                    arrays[arm] = arr
                    for box in [frame["reference_box"], *(c["shape_box"] for c in frame["cards"])]:
                        x, y, w, h = box
                        mask = np.any(arr[y:y+h, x:x+w] < 245, axis=2)
                        nonwhite = mask.sum()
                        assert nonwhite >= 40, (task["image"], box, "blank/tiny card")
                        assert not (mask[:2].any() or mask[-2:].any() or mask[:, :2].any() or mask[:, -2:].any()), \
                            (task["image"], box, "clipped card")
                        card_occupancy.append(int(nonwhite))
                    source_manifest = read(ROOT / f"public/models/{frame['source_id']}/manifest.json")
                    source_ids = {p["instanceId"] for p in source_manifest["instances"]}
                    assert frame["reference_id"] in source_ids
                    assert len({c["source_id"] for c in frame["cards"]}) == 4
                    assert frame["reference_id"] in {c["source_id"] for c in frame["cards"]}
                    assert set(c["label"] for c in frame["cards"]) == set(task["input"]["candidate_ids"])
                    reference_label = next(c["label"] for c in frame["cards"] if c["source_id"] == frame["reference_id"])
                    assert reference_label == truth[task["id"]]["bound_terminal"]
                allowed = np.zeros((900, 1600), dtype=bool)
                frame = frames[cells["anchor"]["image"]]
                changed_boxes = {}
                for card in frame["cards"]:
                    x, y, w, h = card["label_box"]
                    allowed[y:y+h, x:x+w] = True
                for arm in ("changing", "preserving"):
                    diff = np.any(arrays["anchor"] != arrays[arm], axis=2)
                    assert diff.any() and not diff[~allowed].any(), "Unmatched visual intervention"
                    count = 0
                    for card in frame["cards"]:
                        x, y, w, h = card["label_box"]
                        count += bool(diff[y:y+h, x:x+w].any())
                    assert count == 2
                    changed_boxes[arm] = int(diff.sum())
                image_rows.append({"construction_id": cid, "replicate": rep,
                                   "only_two_label_boxes_changed": True, "changed_pixels": changed_boxes})
    result = {"version": VERSION, "status": "passed", "observations": len(public["tasks"]),
              "constructions": len(groups), "independent_semantic_answers": len(truth),
              "image_pairs_checked": len(image_rows) * 2,
              "native_cards_checked": len(card_occupancy),
              "minimum_card_foreground_pixels": min(card_occupancy) if card_occupancy else None,
              "mesh_files_checked": len(mesh_files),
              "mesh_files": mesh_files,
              "inputs": [reference(HERE / "public.json"), reference(HERE / "gold.json"),
                         reference(HERE / "sampling-ledger.json")],
              "split_disjoint_keys": ["source", "contributor", "design_signature", "topology_template"],
              "rows": audit, "pixel_checks": image_rows,
              "human_qualification": "pending; machine checks do not establish human answerability"}
    write(HERE / "dependency-audit.json", result)
    print({k: v for k, v in result.items() if k not in ("rows", "pixel_checks", "inputs", "mesh_files")})
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-images", action="store_true")
    args = parser.parse_args()
    verify(not args.no_images)
