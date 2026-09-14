"""Compose reviewer and paper figures for the advanced challenge layer."""
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image, ImageOps, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent / "challenge-cases"
PAPER = HERE.parent.parent / "paper" / "figures"
manifest = json.loads((ROOT / "manifest.json").read_text())
models = {model["id"]: model for model in manifest["models"]}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "pdf.fonttype": 42})


def show(ax, path, title, subtitle=""):
    ax.imshow(Image.open(ROOT / path))
    ax.axis("off")
    ax.set_title(title, fontsize=12, fontweight="bold", pad=2)
    if subtitle:
        ax.text(.5, -.02, subtitle, transform=ax.transAxes, ha="center", va="top",
                fontsize=8.5, color="#4c5a5e")


fig, axes = plt.subplots(2, 3, figsize=(13, 7.3))
for ax, model in zip(axes.flat, manifest["models"]):
    show(ax, f"models/{model['tier']}/{model['id']}/views/iso.png", model["name"],
         f"{model['tier']} · {model['domain']} · {model['parts']} parts")
fig.subplots_adjust(wspace=.03, hspace=.24)
fig.savefig(ROOT / "CONTACT_SHEET.png", dpi=180, bbox_inches="tight")
fig.savefig(ROOT / "CONTACT_SHEET.pdf", bbox_inches="tight", metadata={"CreationDate": None, "ModDate": None})
fig.savefig(PAPER / "challenge-scale.pdf", bbox_inches="tight", metadata={"CreationDate": None, "ModDate": None})
fig.savefig(PAPER / "challenge-scale.png", dpi=180, bbox_inches="tight")
plt.close(fig)


def paired_image(kind):
    left = Image.open(ROOT / f"tasks/{kind}/input/context.png").convert("RGB")
    right_name = {
        "active-inspection": "minimal-inspection.png",
        "support-counterfactual": "after-collapse.png",
    }.get(kind, "iso.png")
    right = Image.open(ROOT / f"tasks/{kind}/ground-truth/{right_name}").convert("RGB")
    left = ImageOps.contain(left, (500, 375))
    right = ImageOps.contain(right, (500, 375))
    canvas = Image.new("RGB", (1020, 375), "white")
    canvas.paste(left, (0, (375 - left.height) // 2))
    canvas.paste(right, (520, (375 - right.height) // 2))
    draw = ImageDraw.Draw(canvas)
    draw.line((510, 20, 510, 355), fill="#aab7ba", width=2)
    draw.polygon([(517, 187), (503, 180), (503, 194)], fill="#637478")
    return canvas


fig, axes = plt.subplots(3, 4, figsize=(14, 6.5))
for ax, task in zip(axes.flat, manifest["tasks"]):
    ax.imshow(paired_image(task["kind"]))
    ax.axis("off")
    ax.set_title(task["kind"].replace("-", " "), fontsize=11, fontweight="bold", pad=2)
    model = models[task["sourceId"]]
    ax.text(.5, -.02, f"{model['name']} · {model['parts']} parts",
            transform=ax.transAxes, ha="center", va="top", fontsize=8.5, color="#4c5a5e")
fig.subplots_adjust(wspace=.03, hspace=.34)
fig.savefig(ROOT / "TASK_MATRIX.png", dpi=180, bbox_inches="tight")
fig.savefig(ROOT / "TASK_MATRIX.pdf", bbox_inches="tight", metadata={"CreationDate": None, "ModDate": None})
fig.savefig(PAPER / "challenge-tasks.pdf", bbox_inches="tight", metadata={"CreationDate": None, "ModDate": None})
fig.savefig(PAPER / "challenge-tasks.png", dpi=180, bbox_inches="tight")
plt.close(fig)

outputs = ["CONTACT_SHEET.png", "CONTACT_SHEET.pdf", "TASK_MATRIX.png", "TASK_MATRIX.pdf"]
paper_outputs = ["challenge-scale.pdf", "challenge-scale.png", "challenge-tasks.pdf", "challenge-tasks.png"]
(ROOT / "figure-evidence.json").write_text(json.dumps({
    "version": "brickatlas-challenge-figures-1",
    "manifestSha256": hashlib.sha256((ROOT / "manifest.json").read_bytes()).hexdigest(),
    "generatorSha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "outputs": {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in outputs},
    "paperOutputs": {path: hashlib.sha256((PAPER / path).read_bytes()).hexdigest() for path in paper_outputs},
}, indent=2) + "\n")
print(json.dumps({"models": len(models), "tasks": len(manifest["tasks"]), "outputs": outputs}))
