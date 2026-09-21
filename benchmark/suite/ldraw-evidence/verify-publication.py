#!/usr/bin/env python3
"""Verify numerical/provenance and every PDF page; export visual inspection sheets."""
import argparse
import re
from pathlib import Path

from common import DATA, ROOT, VERSION, internal_tasks, load, save, sha

PAPER = ROOT / "benchmark/paper/evidence-v1"


def main():
    import fitz
    from PIL import Image, ImageDraw
    parser = argparse.ArgumentParser()
    parser.add_argument("--render", action="store_true")
    args = parser.parse_args()
    provenance = load(PAPER / "asset-provenance.json")
    for name, expected in provenance["inputs"].items():
        assert sha(ROOT / name) == expected, f"Stale input: {name}"
    for name, expected in provenance["outputs"].items():
        assert sha(PAPER / name) == expected, f"Stale output: {name}"
    nums = load(PAPER / "generated/numbers.json")
    audit = load(DATA / "node-prior-audit.json")
    assert nums["NodeHits"] == sum(r["hit"] for r in audit["rows"])
    assert nums["NodeMicro"] == f"{100*nums['NodeHits']/len(audit['rows']):.2f}"
    assert nums["Tasks"] == sum(nums[k] for k in ["Visual", "Structural", "Controls", "Constant"])
    assert (PAPER / "generated/cases.tex").read_bytes() == (ROOT / "benchmark/paper/tables-v2/cases.tex").read_bytes()
    assert (PAPER / "cvpr.sty").read_bytes() == (DATA / "literature/author-kit/cvpr.sty").read_bytes()
    tex = (PAPER / "main.tex").read_text()
    assert len(re.findall(r"\\begin\{figure\*?\}", tex)) == 4
    assert "\\plateid" not in tex and "[review]{cvpr}" in tex
    issues, docs = [], {}
    target = PAPER / "inspection"
    target.mkdir(exist_ok=True)
    for name in ["main", "supplement"]:
        log = (PAPER / f"{name}.log").read_text()
        for line in log.splitlines():
            if re.search(r"Overfull|undefined|Missing character|LaTeX Error", line):
                issues.append({"document": name, "log": line})
        doc = fitz.open(PAPER / f"{name}.pdf")
        pages, alltext, font_ids, thumbs = [], [], set(), []
        for i, page in enumerate(doc):
            text = page.get_text()
            alltext.append(text)
            assert len(text.strip()) > 10, f"Empty page {name} {i+1}"
            assert not re.search(r"[\u3400-\u9fff]|\ufffd|/Users/|to verify|Public abstract checked|\?\?", text), (name, i+1)
            assert abs(page.rect.width-612) < 1 and abs(page.rect.height-792) < 1
            spans = [s for b in page.get_text("dict")["blocks"] if "lines" in b for l in b["lines"] for s in l["spans"]]
            for span in spans:
                x0, y0, x1, y1 = span["bbox"]
                if x0 < 0 or x1 > 612 or y0 < 0 or y1 > 792:
                    issues.append({"document": name, "page": i+1, "outside_page": span["text"]})
            for font in page.get_fonts(full=True):
                font_ids.add(font[0])
            pages.append({"page": i+1, "characters": len(text), "images": len(page.get_images()),
                          "min_font_pt": round(min(s["size"] for s in spans if s["text"].strip()), 2)})
            if args.render:
                pix = page.get_pixmap(matrix=fitz.Matrix(1.3, 1.3), alpha=False)
                pix.save(target / f"{name}-{i+1:03d}.png")
                thumb = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                thumb.thumbnail((396, 513))
                thumbs.append(thumb)
        fonts = []
        for fid in sorted(font_ids):
            fontname, ext, kind, content = doc.extract_font(fid)
            assert content and kind != "Type3", (name, fontname, kind)
            fonts.append({"name": fontname, "type": kind, "embedded_bytes": len(content)})
        body = "\n".join(alltext)
        if name == "main":
            refs = [i+1 for i, text in enumerate(alltext) if "\nReferences\n" in text]
            assert refs and refs[0] <= 9 and len(doc) <= 9, "Main text exceeds eight pages"
            for n in range(1, 5):
                assert f"Figure {n}." in body
            assert nums["NodeMicro"] in body and nums["NodeMacro"] in body
        else:
            # Each original task appears once as a dossier heading.
            dossiers = re.findall(r"\d+\.\s+(ld2-[a-z0-9-]+)\.", body)
            expected = set(internal_tasks())
            assert len(dossiers) == len(expected) and set(dossiers) == expected, (
                len(dossiers), len(expected), sorted(expected-set(dossiers))[:5])
        if args.render:
            for offset in range(0, len(thumbs), 12):
                sheet = Image.new("RGB", (1600, 1620), "#c6ccd2")
                draw = ImageDraw.Draw(sheet)
                for j, thumb in enumerate(thumbs[offset:offset+12]):
                    x, y = (j % 4)*400, (j // 4)*540
                    sheet.paste(thumb, (x, y+23))
                    draw.text((x+8, y+5), f"{name} / page {offset+j+1}", fill="black")
                sheet.save(target / f"{name}-sheet-{offset//12+1:02d}.jpg", quality=92)
        docs[name] = {"sha256": sha(PAPER / f"{name}.pdf"), "pages": pages, "fonts": fonts}
        (target / f"{name}.txt").write_text(body)
    save(PAPER / "pdf-verification.json", {
        "analysis_version": VERSION, "status": "passed" if not issues else "needs-correction",
        "numeric_provenance": "passed", "original_question_coverage": nums["Tasks"],
        "documents": docs, "issues": issues,
        "visual_review": "Separate manual inspection required; renders alone are not approval."})
    print({"status": "passed" if not issues else "needs-correction",
           "pages": {n: len(d["pages"]) for n, d in docs.items()}, "issues": issues})
    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
