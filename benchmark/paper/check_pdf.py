"""Verify the compiled manuscript and render pages for visual inspection."""
import hashlib
import json
from pathlib import Path
import re

import fitz
from PIL import Image, ImageOps, ImageDraw

ROOT = Path(__file__).resolve().parent
document = fitz.open(ROOT / "main.pdf")
log = (ROOT / "main.log").read_text(errors="replace")
assert not re.search(r"Overfull \\[hv]box|Citation .* undefined|Reference .* undefined|^!", log, re.M)
assert len(document) > 0
output = ROOT.parent / ".runtime/paper-inspection"
output.mkdir(parents=True, exist_ok=True)
pages = []
out_of_bounds = []
text = ""
for index, page in enumerate(document):
    assert abs(page.rect.width - 612) < 1 and abs(page.rect.height - 792) < 1
    page_text = page.get_text()
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
assert "117,910" in text and "5,120" in text
assert "References" in text
assert not re.search(r"\[\?\]", text)
contact = Image.new("RGB", (420*3, 570*((len(pages)+2)//3)), "#dddddd")
for i, image in enumerate(pages):
    contact.paste(image, ((i % 3)*420, (i//3)*570))
contact.save(output / "contact-sheet.png")
result = {
    "pages": len(document), "paperSize": "US Letter", "textOnEveryPage": True,
    "unresolvedCitationsOrReferences": False, "overfullBoxes": False,
    "textOutsidePage": out_of_bounds,
    "pdfSha256": hashlib.sha256((ROOT / "main.pdf").read_bytes()).hexdigest(),
    "scope": "Compile, page-boundary and textual checks; visual page inspection performed separately.",
}
(ROOT / "pdf-verification.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
