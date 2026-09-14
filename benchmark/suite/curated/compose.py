"""Compose the curated-case review sheets from generated case images."""
import hashlib
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent / "curated-cases"
PAPER = HERE.parent.parent / "paper" / "figures"
manifest = json.loads((ROOT / "manifest.json").read_text())
models = {m["id"]: m for m in manifest["models"]}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "pdf.fonttype": 42})


def show(ax, path, title, subtitle=""):
    ax.imshow(Image.open(ROOT / path))
    ax.axis("off")
    ax.set_title(title, fontsize=12, fontweight="bold", pad=2)
    if subtitle:
        ax.text(.5, -.02, subtitle, transform=ax.transAxes, ha="center", va="top", fontsize=9, color="#4c5a5e")

def text_panel(ax, title, lines, subtitle=""):
    ax.axis("off")
    ax.set_title(title, fontsize=12, fontweight="bold", pad=2)
    ax.add_patch(plt.Rectangle((.08, .13), .84, .72, transform=ax.transAxes,
                              facecolor="#f4f7f7", edgecolor="#aebdc1", linewidth=1.2))
    ax.text(.5, .5, "\n".join(lines), transform=ax.transAxes, ha="center", va="center",
            fontsize=10, linespacing=1.45, family="monospace")
    if subtitle:
        ax.text(.5, -.02, subtitle, transform=ax.transAxes, ha="center", va="top", fontsize=9, color="#4c5a5e")


fig, axes = plt.subplots(3, 4, figsize=(14, 9))
for row, difficulty in enumerate(["easy", "medium", "hard"]):
    selected = [m for m in manifest["models"] if m["difficulty"] == difficulty]
    for col, model in enumerate(selected):
        show(axes[row, col], f"models/{difficulty}/{model['id']}/views/iso.png",
             model["name"], f"{difficulty} · {model['style']}\n{model['parts']} parts · {model['colors']} colors")
        if col == 0:
            axes[row, col].text(-.08, .5, difficulty.upper(), transform=axes[row, col].transAxes,
                                rotation=90, va="center", ha="center", fontsize=13, fontweight="bold")
fig.subplots_adjust(wspace=.06, hspace=.30)
fig.savefig(ROOT / "CONTACT_SHEET.png", dpi=180, bbox_inches="tight")
fig.savefig(ROOT / "CONTACT_SHEET.pdf", bbox_inches="tight", metadata={"CreationDate": None, "ModDate": None})
fig.savefig(PAPER / "curated-contact-sheet.pdf", bbox_inches="tight", metadata={"CreationDate": None, "ModDate": None})
plt.close(fig)

task_order = ["parts", "relations", "reconstruct", "generate", "complete", "edit", "plan", "repair"]
input_image = {
    "parts": "input/isolated-iso.png",
    "relations": "input/symbolic-structure-illustration.png",
    "reconstruct": "input/reference-iso.png",
    "generate": "ground-truth/iso.png",
    "complete": "input/current.png",
    "edit": "input/current.png",
    "plan": "ground-truth/iso.png",
    "repair": "input/current.png",
}
fig, axes = plt.subplots(4, 4, figsize=(14, 13))
for row, kind in enumerate(task_order):
    task = next(t for t in manifest["tasks"] if t["kind"] == kind)
    info = json.loads((ROOT / f"tasks/{kind}/task.json").read_text())
    model = models[task["sourceId"]]
    left, right = axes.flat[row * 2], axes.flat[row * 2 + 1]
    if kind == "generate":
        req = info["public"]["input"]["requirements"]
        text_panel(left, f"{kind}: INPUT", [
            f"extent = {req['extent']['x']}×{req['extent']['z']}×{req['extent']['y']}",
            "anchor = (0,0,0)", f"pieces ≤ {req['maxPieces']}",
            f"colors ≥ {req['minColors']}", f"components = {req['components']}",
            f"max degree ≥ {req['minMaximumDegree']}",
        ], "constraints only; no unique target image")
    else:
        show(left, f"tasks/{kind}/{input_image[kind]}", f"{kind}: INPUT", info["display"]["inputLabel"])
    if kind == "parts":
        gt = info["groundTruth"]
        text_panel(right, "GROUND TRUTH", [f"type = {gt['partId']}", f"color = {gt['color']}", f"studs = {gt['studs']}"],
                   info["display"]["groundTruthLabel"])
    elif kind == "relations":
        gt = info["groundTruth"]
        text_panel(right, "GROUND TRUTH", [f"connected = {str(gt['connected']).lower()}",
                   f"above = {str(gt['above']).lower()}", f"studs = {gt['contactStuds']}",
                   f"distance = {gt['shortestPath']}"], info["display"]["groundTruthLabel"])
    else:
        gt_image = "ground-truth/steps/14-of-28.png" if kind == "plan" else \
            "ground-truth/exploded.png" if kind == "reconstruct" else "ground-truth/iso.png"
        show(right, f"tasks/{kind}/{gt_image}", "GROUND TRUTH", info["display"]["groundTruthLabel"])
    left.text(-.02, .98, f"{model['name']} · {model['difficulty']}", transform=left.transAxes,
              va="top", ha="left", fontsize=9, bbox={"facecolor": "white", "edgecolor": "#bcc6c8", "pad": 3})
fig.subplots_adjust(wspace=.02, hspace=.24)
fig.savefig(ROOT / "TASK_GROUND_TRUTH.png", dpi=180, bbox_inches="tight")
fig.savefig(ROOT / "TASK_GROUND_TRUTH.pdf", bbox_inches="tight", metadata={"CreationDate": None, "ModDate": None})
fig.savefig(PAPER / "curated-task-ground-truth.pdf", bbox_inches="tight", metadata={"CreationDate": None, "ModDate": None})
plt.close(fig)

outputs = ["CONTACT_SHEET.png", "CONTACT_SHEET.pdf", "TASK_GROUND_TRUTH.png", "TASK_GROUND_TRUTH.pdf"]

teaser_ids = ["easy-garden-bench", "easy-staircase", "easy-garden-gate", "medium-canal-bridge",
              "medium-pavilion", "medium-townhouse", "hard-lighthouse", "hard-two-tier-pagoda"]
fig, axes = plt.subplots(2, 4, figsize=(12, 4.4))
for ax, model_id in zip(axes.flat, teaser_ids):
    model = models[model_id]
    show(ax, f"models/{model['difficulty']}/{model_id}/views/iso.png", model["name"])
fig.subplots_adjust(wspace=.02, hspace=.14)
fig.savefig(PAPER / "brick-teaser.pdf", bbox_inches="tight", metadata={"CreationDate": None, "ModDate": None})
fig.savefig(PAPER / "brick-teaser.png", dpi=180, bbox_inches="tight")
plt.close(fig)

paper_panels = [
    ("tasks/reconstruct/input/reference-iso.png", "(a) Reconstruction: RGB"),
    ("tasks/reconstruct/ground-truth/exploded.png", "GT: typed poses"),
    ("tasks/complete/input/current.png", "(b) Completion: rails missing"),
    ("tasks/complete/ground-truth/iso.png", "GT: rails restored"),
    ("tasks/edit/input/current.png", "(c) Edit: blue canopy"),
    ("tasks/edit/ground-truth/iso.png", "GT: red canopy"),
    ("tasks/repair/input/current.png", "(d) Repair: shifted roof"),
    ("tasks/repair/ground-truth/iso.png", "GT: roof restored"),
    ("tasks/parts/input/isolated-iso.png", "(e) Part / color / studs"),
    ("tasks/relations/input/symbolic-structure-illustration.png", "(f) Contact + graph query"),
    ("tasks/generate/ground-truth/iso.png", "(g) Constraint witness"),
    ("tasks/plan/ground-truth/steps/14-of-28.png", "(h) Verified plan prefix"),
]
fig, axes = plt.subplots(3, 4, figsize=(12, 7.3))
for ax, (path, title) in zip(axes.flat, paper_panels):
    show(ax, path, title)
fig.subplots_adjust(wspace=.02, hspace=.16)
fig.savefig(PAPER / "brick-tasks.pdf", bbox_inches="tight", metadata={"CreationDate": None, "ModDate": None})
fig.savefig(PAPER / "brick-tasks.png", dpi=180, bbox_inches="tight")
plt.close(fig)

plan_steps = ["07-of-28.png", "14-of-28.png", "21-of-28.png", "28-of-28.png"]
fig, axes = plt.subplots(2, 3, figsize=(12, 5.2))
for ax, file in zip(axes.flat[:4], plan_steps):
    count = int(file.split("-")[0])
    show(ax, f"tasks/plan/ground-truth/steps/{file}", f"Legal prefix: {count}/28 parts")
show(axes.flat[4], "tasks/plan/ground-truth/dead-end.png", "Invalid strategy: decks too early")
show(axes.flat[5], "tasks/plan/ground-truth/dead-end-target.png", "Blocked inner pier outlined")
fig.subplots_adjust(wspace=.02, hspace=.14)
fig.savefig(PAPER / "brick-execution.pdf", bbox_inches="tight", metadata={"CreationDate": None, "ModDate": None})
fig.savefig(PAPER / "brick-execution.png", dpi=180, bbox_inches="tight")
plt.close(fig)

paper_outputs = ["brick-teaser.pdf", "brick-teaser.png", "brick-tasks.pdf", "brick-tasks.png",
                 "brick-execution.pdf", "brick-execution.png",
                 "curated-contact-sheet.pdf", "curated-task-ground-truth.pdf"]
(ROOT / "contact-sheet-evidence.json").write_text(json.dumps({
    "version": "curated-contact-sheets-1",
    "manifestSha256": hashlib.sha256((ROOT / "manifest.json").read_bytes()).hexdigest(),
    "generatorSha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "outputs": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in outputs},
    "paperOutputs": {p: hashlib.sha256((PAPER / p).read_bytes()).hexdigest() for p in paper_outputs},
}, indent=2) + "\n")
print(json.dumps({"models": len(models), "tasks": len(task_order), "outputs": outputs}))
