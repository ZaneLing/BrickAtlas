#!/usr/bin/env python3
"""Check paper pages, table provenance, all dossiers and scientific asset links."""
import argparse
import re
from pathlib import Path

import fitz
from PIL import Image, ImageDraw

from common import ROOT, DATA, PUBLIC, load, save, sha, original_tasks

PAPER = ROOT / "benchmark/paper/evidence-v2"


def main(render=False):
    tasks = original_tasks()
    dossiers = load(PUBLIC / "dossiers.json")["items"]
    assert len(dossiers) == len(tasks) == 617
    assert {d["parent_task_id"] for d in dossiers} == set(tasks)
    for d in dossiers:
        t = tasks[d["parent_task_id"]]
        assert d["original_record"] == t and d["answer"] == t["answer"]
        assert d["prompt_en"] == t["promptEn"] and d["input"] == t["input"]
    registry = load(DATA / "family-registry.json")["families"]
    assert all(d["display_name"] == registry[d["family_id"]]["display_name"] for d in dossiers)
    manifest = load(DATA / "visual-manifest.json")
    obs = {o["observation_id"]: o for o in manifest["observations"]}
    pairs = load(PUBLIC / "paired-observations.json")["pairs"]
    assert len(pairs) == 140 and sum(len(p["observations"]) for p in pairs) == 347
    for p in pairs:
        for o in p["observations"]:
            assert o["payload"] == obs[o["observation_id"]]["payload"]
            assert o["gold"] == obs[o["observation_id"]]["gold"]
            assert (ROOT / "public" / o["image"].lstrip("/")).exists()
    for f in load(PAPER / "figure-provenance.json"):
        assert sha(ROOT / f["file"]) == f["sha256"]
    prov = load(PAPER / "publication-provenance.json")
    for file, digest in prov["inputs"].items():
        assert sha(ROOT / file) == digest, file
    assert len(re.findall(r"\\bibitem", (PAPER / "main.bbl").read_text())) == 13
    pages = []
    inspection = PAPER / "inspection"
    inspection.mkdir(exist_ok=True)
    for name in ["main", "supplement"]:
        pdf = fitz.open(PAPER / f"{name}.pdf")
        assert len(pdf) == 8 if name == "main" else len(pdf) <= 8
        if render:
            for file in inspection.glob(f"{name}-*"):
                page_match = re.fullmatch(rf"{name}-(\d+)\.png", file.name)
                sheet_match = re.fullmatch(rf"{name}-sheet-(\d+)\.jpg", file.name)
                if (page_match and int(page_match[1]) > len(pdf)) or (
                        sheet_match and int(sheet_match[1]) > (len(pdf) + 1) // 2):
                    file.unlink()  # Remove only our superseded generated page previews.
        text = "\n".join(p.get_text() for p in pdf)
        assert "\ufffd" not in text and not re.search(r"[\u4e00-\u9fff]", text)
        assert "??" not in text
        log = (PAPER / f"{name}.log").read_text()
        assert "Overfull" not in log and "undefined references" not in log
        images = []
        for i, p in enumerate(pdf):
            outside = []
            for block in p.get_text("dict")["blocks"]:
                for line in block.get("lines", []):
                    for span in line["spans"]:
                        box = fitz.Rect(span["bbox"])
                        if box.x0 < -1 or box.y0 < -1 or box.x1 > p.rect.width + 1 or box.y1 > p.rect.height + 1:
                            outside.append(span["text"])
            assert not outside, (name, i+1, outside)
            assert len(p.get_text().split()) > 80, (name, i+1, "empty or sparse page")
            pages.append({"document": name, "page": i+1, "words": len(p.get_text().split()),
                          "text_within_page": True, "fonts": sorted({f[3] for f in p.get_fonts()})})
            if render:
                image = inspection / f"{name}-{i+1:02}.png"
                p.get_pixmap(matrix=fitz.Matrix(1.6, 1.6), alpha=False).save(image)
                images.append(image)
        if render:
            for start in range(0, len(images), 2):
                sheet = Image.new("RGB", (1640, 1100), "#d7dcd9")
                draw = ImageDraw.Draw(sheet)
                for j, file in enumerate(images[start:start+2]):
                    image = Image.open(file)
                    image.thumbnail((806, 1050))
                    sheet.paste(image, (j*820+7, 34))
                    draw.text((j*820+18, 12), f"{name} - page {start+j+1}", fill="#132521")
                sheet.save(inspection / f"{name}-sheet-{start//2+1}.jpg", quality=94)
    # The generation step cannot supply empirical rankings or model case figures.
    report = load(DATA / "reports/protocol-ready.json")
    assert report["models"] == [] and report["qa"]["primary_final"] == 0
    save(PAPER / "verification.json", {
        "status": "passed", "dossiers": 617, "visual_pairs": 140, "observations": 347,
        "references": 13, "pages": pages, "pdf_sha256": {
            name: sha(PAPER / f"{name}.pdf") for name in ["main", "supplement"]},
        "actual_human_reviews": 0, "real_model_results": 0,
        "inspection_role": "publication layout checks, not benchmark human QA",
        "visual_inspection_required": True})
    print({"status": "passed", "main_pages": sum(p["document"] == "main" for p in pages),
           "supplement_pages": sum(p["document"] == "supplement" for p in pages),
           "dossiers": len(dossiers), "references": 13})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--render", action="store_true")
    args = parser.parse_args()
    main(args.render)
