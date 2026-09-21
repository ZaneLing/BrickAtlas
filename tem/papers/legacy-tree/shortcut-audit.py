#!/usr/bin/env python3
"""Read-only public-input shortcut audit for BrickAtlas LDraw-1.

Run from any directory:
  python3 benchmark/paper/shortcut-audit.py
  python3 benchmark/paper/shortcut-audit.py --output /absolute/path/result.json

Predictions use ONLY public option labels or public reference ordering.
Answer-bearing review bundles are loaded only AFTER all predictions are made.
No source, manifest, task, image, model run or experiment process is modified.
An output path must not already exist. This audit does NOT establish that a
particular model runner exposes these fields or that a model uses these rules.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path

FAMILIES = {
    "graph-removal": "second-smallest numeric option label",
    "source-step": "second-smallest numeric option label",
    "shape-match": "option matching public references[1]",
    "neighbors": "options matching public references[1:-2]",
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def public_prediction(task):
    family = task["family"]
    if family in ("graph-removal", "source-step"):
        options = sorted(task["options"], key=lambda option: float(option["label"]))
        assert len(options) >= 2, "Insufficient numeric choices"
        return {"choiceId": options[1]["id"]}
    if family == "shape-match":
        candidate = task["references"][1]["id"]
        matches = [option["id"] for option in task["options"] if option["value"] == candidate]
        assert len(matches) == 1, "Public reference is not a unique option"
        return {"choiceId": matches[0]}
    if family == "neighbors":
        candidates = {ref["id"] for ref in task["references"][1:-2]}
        return {"choiceIds": sorted(option["id"] for option in task["options"]
                                     if option["value"] in candidates)}
    raise ValueError(f"Unsupported family: {family}")


def audit(root):
    catalog_path = root / "catalog.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    model_ids = [entry["id"] for entry in catalog]
    assert model_ids and len(model_ids) == len(set(model_ids)), "Catalog must be nonempty and unique"
    predictions = []
    seen = set()
    input_receipts = []
    public_count = 0
    # Phase 1: all predictions are made without opening any private answers.
    for model_id in model_ids:
        path = root / "inputs" / f"{model_id}.json"
        bundle = json.loads(path.read_text(encoding="utf-8"))
        assert bundle["modelId"] == model_id
        input_receipts.append({"path": str(path), "sha256": digest(path)})
        for task in bundle["tasks"]:
            assert task["id"] not in seen, "Duplicate public task"
            assert "answer" not in task, "Public task unexpectedly contains an answer"
            seen.add(task["id"])
            public_count += 1
            if task["family"] in FAMILIES:
                predictions.append({"model_id": model_id, "task_id": task["id"],
                                    "family": task["family"], "prediction": public_prediction(task)})
    # Phase 2: load review answers, solely for independent scoring.
    gold = {}
    answer_receipts = []
    for model_id in model_ids:
        path = root / "models" / f"{model_id}.json"
        bundle = json.loads(path.read_text(encoding="utf-8"))
        answer_receipts.append({"path": str(path), "sha256": digest(path)})
        for task in bundle["tasks"]:
            assert task["id"] not in gold, "Duplicate reference task"
            answer = task["answer"].copy()
            if "choiceIds" in answer:
                answer["choiceIds"] = sorted(answer["choiceIds"])
            gold[task["id"]] = answer
    assert seen == set(gold), "Public/reference task coverage mismatch"
    summary = {family: {"rule": rule, "tested": 0, "correct": 0} for family, rule in FAMILIES.items()}
    for row in predictions:
        row["reference"] = gold[row["task_id"]]
        row["correct"] = row["prediction"] == row["reference"]
        summary[row["family"]]["tested"] += 1
        summary[row["family"]]["correct"] += int(row["correct"])
    for item in summary.values():
        item["accuracy"] = item["correct"] / item["tested"] if item["tested"] else None
    return {
        "scope": "Frozen public JSON only; model request serialization and image-layout shortcuts not audited",
        "interpretation": "Shortcut availability, not evidence of actual model exploitation; not a learned baseline",
        "root": str(root), "catalog_sha256": digest(catalog_path),
        "sources": len(model_ids), "public_tasks": public_count,
        "tested_tasks": len(predictions), "correct_tasks": sum(row["correct"] for row in predictions),
        "summary": summary, "public_inputs": input_receipts,
        "reference_bundles_scoring_only": answer_receipts, "item_results": predictions,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path,
                        default=Path(__file__).resolve().parents[2] / "public/benchmark/ldraw")
    parser.add_argument("--output", type=Path, help="Optional NEW JSON output file; existing files are not overwritten")
    args = parser.parse_args()
    report = audit(args.root.resolve())
    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        with args.output.open("x", encoding="utf-8") as stream:
            stream.write(payload)
        print(json.dumps({"output": str(args.output.resolve()), "sources": report["sources"],
                          "public_tasks": report["public_tasks"], "tested_tasks": report["tested_tasks"],
                          "correct_tasks": report["correct_tasks"], "summary": report["summary"]},
                         ensure_ascii=False, indent=2))
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
