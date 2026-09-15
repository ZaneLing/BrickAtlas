"""Verify the compiled manuscript and render pages for visual inspection."""
import hashlib
import json
import argparse
from pathlib import Path
import re

import fitz
from PIL import Image, ImageOps, ImageDraw

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--paper", choices=["main", "supplement"], default="main")
args = parser.parse_args()
document = fitz.open(ROOT / (args.paper + ".pdf"))
log = (ROOT / (args.paper + ".log")).read_text(errors="replace")
assert not re.search(r"Overfull \\[hv]box|Citation .* undefined|Reference .* undefined|^!", log, re.M)
assert len(document) > 0
output = ROOT.parent / ".runtime/paper-inspection"
if args.paper == "supplement":
    output = output / "supplement"
output.mkdir(parents=True, exist_ok=True)
pages = []
out_of_bounds = []
text = ""
references_start = None
main_content_last_page = None
for index, page in enumerate(document):
    assert abs(page.rect.width - 612) < 1 and abs(page.rect.height - 792) < 1
    page_text = page.get_text()
    if references_start is None and re.search(r"(?m)^References$", page_text):
        references_start = index + 1
        before_references = page_text.split("References", 1)[0].strip()
        main_content_last_page = index + 1 if before_references else index
    assert len(page_text.strip()) > 100
    text += page_text
    for word in page.get_text("words"):
        x0, y0, x1, y1 = word[:4]
        if x0 < 0 or y0 < 0 or x1 > page.rect.width or y1 > page.rect.height:
            out_of_bounds.append({"page": index + 1, "text": word[4]})
    pix = page.get_pixmap(matrix=fitz.Matrix(1.3, 1.3))
    path = output / f"page-{index+1}.png"
    pix.save(str(path))
    image = Image.open(path).convert("RGB")
    thumb = ImageOps.contain(image, (400, 540))
    frame = Image.new("RGB", (420, 570), "white")
    frame.paste(thumb, ((420-thumb.width)//2, 12))
    ImageDraw.Draw(frame).text((12, 550), f"Page {index+1}", fill="black")
    pages.append(frame)
assert not out_of_bounds, out_of_bounds
if args.paper == "main":
    assert "9,935" in text and "OMR/LDraw" in text
    assert "117,910" in text and "retired" in text
    assert references_start is not None
    assert main_content_last_page <= 8, f"Main content exceeds 8 pages: {main_content_last_page}"
    assert len(set(re.findall(r"Figure (\d+)\.", text))) >= 5, "Missing information figures"
assert not re.search(r"\[\?\]", text)
contact = Image.new("RGB", (420*3, 570*((len(pages)+2)//3)), "#dddddd")
for i, image in enumerate(pages):
    contact.paste(image, ((i % 3)*420, (i//3)*570))
contact.save(output / "contact-sheet.png")
result = {
    "pages": len(document), "paperSize": "US Letter", "textOnEveryPage": True,
    "unresolvedCitationsOrReferences": False, "overfullBoxes": False,
    "textOutsidePage": out_of_bounds,
    "pdfSha256": hashlib.sha256((ROOT / (args.paper + ".pdf")).read_bytes()).hexdigest(),
    "referencesStartPage": references_start,
    "mainContentPageUpperBound": main_content_last_page if main_content_last_page is not None else len(document),
    "scope": "Compile, page-boundary and textual checks; visual page inspection performed separately.",
}
(ROOT / ("pdf-verification.json" if args.paper == "main" else "supplement-verification.json")).write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
