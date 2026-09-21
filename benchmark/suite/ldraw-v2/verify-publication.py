#!/usr/bin/env python3
"""Verify v2 paper/data parity, English PDFs, page bounds and figure provenance."""
import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "benchmark/ldraw-v2"
PAPER = ROOT / "benchmark/paper"
SITE = ROOT / "public/benchmark/ldraw-v2"
CJK = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    import fitz
    from PIL import Image, ImageDraw, ImageOps
    from publication import tex
    manifest = json.loads((DATA / "publication-manifest.json").read_text())
    for role in ["inputs", "outputs"]:
        for p, digest in manifest[role].items():
            assert sha(ROOT / p) == digest, (role, p, "changed")
    assert manifest["generatorSha256"] == sha(Path(__file__).with_name("publication.py"))
    summary = manifest["summary"]
    catalog = json.loads((SITE / "catalog.json").read_text())
    tasks = [t for m in catalog for t in json.loads((SITE / f"models/{m['id']}.json").read_text())["tasks"]]
    publics = [t for m in catalog for t in json.loads((SITE / f"inputs/{m['id']}.json").read_text())["tasks"]]
    assert summary["tasks"] == len(tasks) == 617
    assert summary["parts"] == sum(m["parts"] for m in catalog) == 15334
    assert summary["families"] == dict(Counter(t["family"] for t in tasks))
    assert summary["formats"] == dict(Counter(t["format"] for t in tasks))
    assert summary["layers"] == dict(Counter(t["layer"] for t in tasks))
    assert {t["id"] for t in tasks} == {t["id"] for t in publics}
    assert manifest["appendixTaskIds"] == [t["id"] for t in tasks]
    contracts = json.loads((DATA / "task-contracts.json").read_text())["contracts"]
    for c in contracts:
        group = [t for t in tasks if t["family"] == c["family"]]
        assert len(group) == c["n"]
        assert all(t["modality"] == c["modality"] and t["layer"] == c["layer"] and t["format"] == c["format"] for t in group)
    cases = (PAPER / "tables-v2/cases.tex").read_text()
    assert cases.count(r"\item \textbf{ld2-") == 617
    for t in tasks:
        assert tex(t["promptEn"]) in cases
        assert tex(json.dumps(t["answer"], ensure_ascii=True)) in cases
        for o in t.get("options", []):
            assert tex(f"{o['id']}: {o['label']}") in cases
    plan = json.loads((PAPER / "ldraw-v2-experiments.json").read_text())
    assert summary["conditions"] == {c["id"]: c["n"] for c in plan["conditions"]}
    assert len(plan["conditions"]) == 14 and sum(c["n"] for c in plan["conditions"]) == 3147
    nulls = 0
    for t in plan["tables"]:
        for r in t["rows"]:
            assert all(v is None for v in r["results"].values())
            nulls += len(r["results"])
    assert nulls == manifest["nullResultCells"]
    refs = json.loads((DATA / "reference-verification.json").read_text())
    assert refs["allContentVerified"], refs
    index = json.loads((SITE / "review-index.json").read_text())
    assert index["summary"] == summary
    assert len([u for u in index["units"] if u["kind"] == "task" and u["required"]]) == 251
    assert len([u for u in index["units"] if u["kind"] == "pair"]) == 573
    assert all(u["sourceHash"] == next(m["sourceHash"] for m in catalog if m["id"] == u["sourceId"]) for u in index["units"])
    assert json.loads((SITE / "publication-summary.json").read_text()) == summary
    # Shared scorer is imported by both UI and CLI; no second integer oracle.
    for filename in ["benchmark/suite/ldraw-v2/score.ts", "src/benchmark-v2/App.tsx"]:
        assert re.search(r"import \{ score \} from '[^']*scoring'", (ROOT / filename).read_text())
    for p in [PAPER / "main-v2.tex", PAPER / "supplement-v2.tex", PAPER / "references-v2.bib",
              *sorted((PAPER / "tables-v2").glob("*.tex"))]:
        assert not CJK.search(p.read_text()), p
    images = list((PAPER / "figures-v2").glob("*.jpg")) + list((PAPER / "figures-v2").glob("*.png"))
    encoded = {sha(p) for p in images}
    decoded = {hashlib.sha256(Image.open(p).convert("RGB").tobytes()).hexdigest() for p in images}
    for row in manifest["renders"]:
        assert sha(ROOT / row["source"]) == row["sourceSha256"]
        assert sha(PAPER / row["file"]) == row["sha256"]
    out = DATA / "paper-inspection"
    out.mkdir(exist_ok=True)
    results = {}
    for name in ["main-v2", "supplement-v2"]:
        document = fitz.open(PAPER / f"{name}.pdf")
        log = (PAPER / f"{name}.log").read_text()
        assert not re.search(r"Overfull \\[hv]box|Citation .* undefined|Reference .* undefined|^!", log, re.M)
        main_last = len(document)
        total_images = 0
        thumbnails = []
        for n, page in enumerate(document, 1):
            text = page.get_text()
            assert not CJK.search(text), (name, n)
            assert "??" not in text and "[?]" not in text
            assert len(text.strip()) > 80, (name, n, "nearly empty page")
            assert abs(page.rect.width - 612) < 1 and abs(page.rect.height - 792) < 1
            if name == "main-v2" and re.search(r"(?m)^References$", text):
                main_last = n if text.split("References")[0].strip() else n - 1
            for word in page.get_text("words"):
                assert word[0] >= 0 and word[1] >= 0 and word[2] <= 612 and word[3] <= 792, (name, n, word)
            for entry in page.get_images():
                total_images += 1
                pix = fitz.Pixmap(document, entry[0])
                if pix.n != 3:
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                digest = hashlib.sha256(pix.samples).hexdigest()
                original = hashlib.sha256(document.extract_image(entry[0])["image"]).hexdigest()
                assert digest in decoded or original in encoded, (name, n, "untracked raster")
            # Main: all pages. Supplement: first page, contract/replay and source samples.
            if name == "main-v2" or n in {1, 3, 5, 8, 12, 15, 40, 80, len(document)}:
                path = out / f"{name}-{n}.png"
                page.get_pixmap(matrix=fitz.Matrix(1.4, 1.4)).save(path)
                thumb = ImageOps.contain(Image.open(path).convert("RGB"), (306, 396))
                cell = Image.new("RGB", (320, 420), "white")
                cell.paste(thumb, (7, 0)); ImageDraw.Draw(cell).text((10, 400), f"{name}: {n}", fill="black")
                thumbnails.append(cell)
        if name == "main-v2":
            assert main_last <= 8
            assert total_images >= 10
        sheet = Image.new("RGB", (320 * 3, 420 * ((len(thumbnails) + 2) // 3)), "#dedede")
        for i, image in enumerate(thumbnails):
            sheet.paste(image, ((i % 3) * 320, (i // 3) * 420))
        sheet.save(out / f"{name}-contact.png")
        results[name] = {"pages": len(document), "mainContentPageUpperBound": main_last,
                         "images": total_images, "pdfSha256": sha(PAPER / f"{name}.pdf"),
                         "englishOnly": True, "trackedRasterImages": True,
                         "unresolvedReferences": False, "overfullBoxes": False, "outOfPageText": False}
    report = {"status": "passed", "pdfs": results, "sourceDataPaperParity": True,
              "appendixItems": 617, "nullResultCells": nulls,
              "referencesContentVerified": True, "sharedScorer": True,
              "reviewUnits": len(index["units"]), "humanCertification": "pending"}
    (DATA / "publication-verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    main()
