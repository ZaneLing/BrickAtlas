"""Compose review and paper plates from verified Mechanism-1 renders."""
from pathlib import Path
import json
import shutil
import time

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "mechanism-v1"
models = json.loads((OUT / "models.json").read_text())
tasks = json.loads((OUT / "oracle-private.json").read_text())
font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
font = ImageFont.truetype(font_path, 24) if Path(font_path).exists() else ImageFont.load_default()
small = ImageFont.truetype(font_path, 18) if Path(font_path).exists() else ImageFont.load_default()

def grid_plate(entries, columns, cell, output):
    rows = (len(entries) + columns - 1) // columns
    canvas = Image.new("RGB", (cell[0] * columns, cell[1] * rows), "#eef1f2")
    draw = ImageDraw.Draw(canvas)
    for index, (path, title, subtitle) in enumerate(entries):
        col, row = index % columns, index // columns
        left, top = col * cell[0], row * cell[1]
        draw.rounded_rectangle((left + 8, top + 8, left + cell[0] - 8, top + cell[1] - 8),
                               radius=7, fill="white", outline="#d6dee2", width=2)
        image = Image.open(path).convert("RGB")
        image = ImageOps.contain(image, (cell[0] - 24, cell[1] - 78))
        canvas.paste(image, (left + (cell[0] - image.width) // 2, top + 12))
        draw.text((left + 16, top + cell[1] - 58), title, fill="#111820", font=font)
        draw.text((left + 16, top + cell[1] - 30), subtitle, fill="#5b6870", font=small)
    canvas.save(output)
    epoch = time.gmtime(0)
    canvas.save(output.with_suffix(".pdf"), "PDF", resolution=180,
                creationDate=epoch, modDate=epoch)

model_entries = []
for model in models:
    model_entries.append((OUT / f'images/models/{model["id"]}-iso.png',
                          model["nameZh"], f'{len(model["parts"])} visual parts · {len(model["joints"])} joints'))
grid_plate(model_entries, 3, (520, 390), OUT / "ALL_MODELS.png")

labels = {
    "prefix-dynamics": "Prefix dynamics",
    "insertion-access": "Continuous access",
    "fault-recovery": "Fault recovery",
    "inventory-substitution": "Inventory substitution",
    "dynamic-robustness": "Dynamic robustness",
    "functional-kinematics": "Functional kinematics",
    "active-inspection": "Active inspection",
    "multiobjective-design": "Multi-objective design",
}
kind_order = list(labels)
task_entries = []
for index, kind in enumerate(kind_order):
    model = models[index % len(models)]
    task_entries.append((OUT / f'images/tasks/{model["id"]}-{kind}.png',
                         labels[kind], model["name"]))
grid_plate(task_entries, 4, (430, 330), OUT / "TASK_MATRIX.png")
PAPER_FIGURES = ROOT / "paper" / "figures"
PAPER_FIGURES.mkdir(parents=True, exist_ok=True)
for name, target in [("ALL_MODELS", "mechanism-models"), ("TASK_MATRIX", "mechanism-tasks")]:
    shutil.copyfile(OUT / f"{name}.png", PAPER_FIGURES / f"{target}.png")
    shutil.copyfile(OUT / f"{name}.pdf", PAPER_FIGURES / f"{target}.pdf")
print(json.dumps({"models": len(model_entries), "taskFamilies": len(task_entries)}))
