"""Generate the OMR whole-model paper figure and source table."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

PAPER = Path(__file__).resolve().parent
ROOT = PAPER.parent.parent
RELEASE = ROOT / "benchmark" / "omr-cases-v1"
registry = json.loads((RELEASE / "manifest.json").read_text())
assert registry["version"] == "brickatlas-omr-cases-1"
assert registry["summary"]["wholeModels"] == 15
assert registry["summary"]["semanticSubassemblies"] == 39

selected = [
    "5867", "31009", "10128", "10159",
    "10001", "10213", "10220", "10214",
]
whole = {case["sourceModelId"]: case for case in registry["wholeModels"]}
font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
font = ImageFont.truetype(font_path, 24) if Path(font_path).exists() else ImageFont.load_default()
small = ImageFont.truetype(font_path, 18) if Path(font_path).exists() else ImageFont.load_default()
cell_w, cell_h = 480, 360
canvas = Image.new("RGB", (cell_w * 4, cell_h * 2), "white")
draw = ImageDraw.Draw(canvas)

for index, model_id in enumerate(selected):
    case = whole[model_id]
    preview = Image.open(ROOT / case["preview"]).convert("RGB")
    preview = ImageOps.contain(preview, (440, 285))
    col, row = index % 4, index // 4
    left, top = col * cell_w, row * cell_h
    draw.rounded_rectangle((left + 8, top + 8, left + cell_w - 8, top + cell_h - 8),
                           radius=8, fill="#f4f6f7", outline="#d8dee1", width=2)
    canvas.paste(preview, (left + (cell_w - preview.width) // 2, top + 18))
    title = case["title"]
    count = f'{case["instances"]:,} parts'
    box = draw.textbbox((0, 0), title, font=font)
    draw.text((left + (cell_w - box[2]) / 2, top + 302), title, font=font, fill="#111820")
    count_box = draw.textbbox((0, 0), count, font=small)
    draw.text((left + (cell_w - count_box[2]) / 2, top + 332), count, font=small, fill="#56616a")

figures = PAPER / "figures"
figures.mkdir(exist_ok=True)
png = figures / "omr-whole-models.png"
pdf = figures / "omr-whole-models.pdf"
canvas.save(png)
canvas.save(pdf, "PDF", resolution=180.0)

all_cell_w, all_cell_h = 420, 350
all_canvas = Image.new("RGB", (all_cell_w * 3, all_cell_h * 5), "#eef1f2")
all_draw = ImageDraw.Draw(all_canvas)
for index, case in enumerate(registry["wholeModels"]):
    preview = Image.open(ROOT / case["preview"]).convert("RGB")
    preview = ImageOps.contain(preview, (390, 255))
    col, row = index % 3, index // 3
    left, top = col * all_cell_w, row * all_cell_h
    all_draw.rounded_rectangle((left + 8, top + 8, left + all_cell_w - 8, top + all_cell_h - 8),
                               radius=8, fill="white", outline="#d8dee1", width=2)
    all_canvas.paste(preview, (left + (all_cell_w - preview.width) // 2, top + 15))
    title = f'{case["setNumber"]} {case["title"]}'
    count = f'{case["instances"]:,} parts'
    all_draw.text((left + 18, top + 292), title, font=small, fill="#111820")
    all_draw.text((left + 18, top + 322), count, font=small, fill="#56616a")
all_models = RELEASE / "ALL_MODELS.png"
all_canvas.save(all_models)

rows = []
category_en = {
    "车辆": "vehicle", "铁路": "rail", "建筑": "building",
    "场景": "scene", "航天": "space", "地标建筑": "landmark",
    "飞行器": "aircraft", "船舶": "marine",
}
for case in registry["wholeModels"]:
    provenance = "source" if case["instructionProvenance"] == "source" else "editorial"
    title = case["title"].replace("&", r"\&")
    rows.append(
        f'{case["setNumber"]} {title} & {category_en[case["category"]]} & '
        f'{case["instances"]:,} & {case["uniqueParts"]} & '
        f'{case["instructionSteps"]} & {provenance} \\\\'
    )
(PAPER / "tables" / "omr-models.tex").write_text("\n".join(rows) + "\n")

sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
evidence = {
    "version": registry["version"],
    "summary": registry["summary"],
    "selectedFigureModels": selected,
    "registrySha256": sha(RELEASE / "manifest.json"),
    "generatorSha256": sha(Path(__file__)),
    "outputs": {
        "figures/omr-whole-models.png": sha(png),
        "figures/omr-whole-models.pdf": sha(pdf),
        "tables/omr-models.tex": sha(PAPER / "tables" / "omr-models.tex"),
        "../omr-cases-v1/ALL_MODELS.png": sha(all_models),
    },
}
(PAPER / "omr-evidence.json").write_text(json.dumps(evidence, indent=2) + "\n")
print(json.dumps({"models": 15, "semanticSubassemblies": 39, "figureModels": 8}))
