"""Verify pinned reading assets and the real-source protocol example offline."""
import json
from pathlib import Path

from common import DATA, ROOT, VERSION, read_frozen, save, sha


def main():
    folder = DATA / "literature"
    verified = []
    for row in json.loads((folder / "download-manifest.json").read_text()):
        path = folder / (row["id"] + ".pdf")
        assert sha(path) == row["sha256"], path
        verified.append({"path": str(path.relative_to(ROOT)), "sha256": sha(path)})
    for row in json.loads((folder / "official/download-manifest.json").read_text()):
        path = folder / "official" / row["repo"].split("/")[-1] / row["path"]
        assert sha(path) == row["sha256"], path
        assert f"/{row['commit']}/" in row["url"]
        verified.append({"path": str(path.relative_to(ROOT)), "sha256": sha(path)})
    for row in json.loads((folder / "format-download-manifest.json").read_text()):
        path = folder / row["path"]
        assert sha(path) == row["sha256"], path
        verified.append({"path": str(path.relative_to(ROOT)), "sha256": sha(path)})

    source = read_frozen("public/benchmark/ldraw-v2/models/omr-42004.json")
    tid = "ld2-omr-42004-shape-match-1"
    task = next(t for t in source["tasks"] if t["id"] == tid)
    parts = {p["label"]: p for p in source["parts"]}
    assert parts["B0035"]["partNumber"] == parts["B0036"]["partNumber"] == "32250"
    assert parts["B0196"]["partNumber"] == "2780"
    assert task["answer"] == {"choiceId": "C"}
    options = {x["id"]: x["label"] for x in task["options"]}
    assert options["C"] == "B0036" and options["A"] == "B0196"
    renders = read_frozen("benchmark/ldraw-v2/paired-renders.json")
    images = {i["mode"]: i for i in renders["images"] if i["taskId"] == tid}
    assert images["wrong"]["mismatch"] == {
        "swappedLabels": ["B0036", "B0196"], "alternateChoiceId": "A"}
    for i in images.values():
        path = ROOT / "public" / i["file"]
        assert sha(path) == i["sha256"], path
    assert images["full"]["camera"] == images["mask"]["camera"]
    assert images["full"]["projections"] == images["mask"]["projections"]
    edges = [e for e in source["audit"]["edges"]
             if "brick_000035" in (e["a"], e["b"])]
    neighbors = sorted({e["a"] if e["b"] == "brick_000035" else e["b"] for e in edges})
    assert neighbors == [f"brick_{n:06d}" for n in [34, 37, 38, 51]]
    restore = next(t for t in source["tasks"]
                   if t["id"] == "ld2-omr-42004-restore-instance-1")
    assert restore["answer"] == {"actionIds": ["restore-B0035"]}
    request = DATA / "request-audits/gpt41-wrong-image/requests" / (tid + ".json")
    assert sha(request) == "16bbda47009ab11e28c7fe37d18bcf464a6f606ab6b9fe6c3d765f45318c30fc"
    save(folder / "worked-example.json", {
        "analysis_version": VERSION, "task_id": tid, "source_id": source["entry"]["id"],
        "source_hash": source["entry"]["sourceHash"], "source_parts": len(parts),
        "target": parts["B0035"], "match": parts["B0036"], "other": parts["B0196"],
        "options": options, "gold_A": "C", "gold_B": "A",
        "images": images, "recognized_edges": edges,
        "restore_task_id": restore["id"], "restore_action": "restore-B0035",
        "request_B_sha256": sha(request), "model_predictions": None,
        "human_answerability": "pending",
        "interpretation": "Image-conditioned label binding; unchanged source CAD truth."})
    save(folder / "verification.json", {
        "analysis_version": VERSION, "status": "passed",
        "pinned_assets": verified, "paper_pages_read": [10, 11, 40],
        "worked_example": {"status": "passed", "task_id": tid,
                           "path": "literature/worked-example.json",
                           "sha256": sha(folder / "worked-example.json")},
        "external_model_runs": 0, "human_certifications": 0})
    print(f"PASS: {len(verified)} pinned assets and source-bound example")


if __name__ == "__main__":
    main()
