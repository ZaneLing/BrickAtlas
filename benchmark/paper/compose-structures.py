"""Compose actual version-bound 3D renders into explanatory paper figures."""
import hashlib
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

ROOT = Path(__file__).resolve().parent
manifest = json.loads((ROOT / "structure-evidence.json").read_text())
images = {r["name"]: r for r in manifest["images"]}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12, "pdf.fonttype": 42})


def panel(ax, name, title):
    row = images[name]
    path = ROOT / row["file"]
    assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"]
    ax.imshow(Image.open(path))
    ax.axis("off")
    ax.set_title(title, fontsize=12, pad=2)


outputs = []


def save(fig, name):
    fig.savefig(ROOT / "figures" / (name + ".pdf"), bbox_inches="tight",
                metadata={"CreationDate": None, "ModDate": None})
    fig.savefig(ROOT / "figures" / (name + ".png"), bbox_inches="tight", dpi=180)
    outputs.append(name)
    plt.close(fig)


policies = ["tip-walk", "low-fan", "shallow-terrace", "plate-network",
            "column-field", "alternating-beams", "two-support-bridge", "enclosed-shell"]
fig, axes = plt.subplots(2, 4, figsize=(12, 4.4))
for ax, policy in zip(axes.flat, policies):
    panel(ax, "gallery-" + policy, policy.replace("-", " ").title())
fig.subplots_adjust(wspace=.02, hspace=.14)
save(fig, "brick-teaser")

fig, axes = plt.subplots(3, 4, figsize=(12, 7.4))
panels = [
    ("reconstruct-input", "(a) Reconstruction: RGB"),
    ("reconstruct-gt", "GT: all part poses"),
    ("complete-input", "(b) Completion: prefix"),
    ("complete-gt", "GT: additions outlined"),
    ("edit-input", "(c) Edit: current"),
    ("edit-gt", "GT: quarter-turn"),
    ("repair-input", "(d) Repair: shifted part"),
    ("repair-gt", "GT: restore + identify"),
    ("recognition", "(e) Part / color / studs"),
    ("relation", "(f) Contact + graph query"),
    ("generation", "(g) Constraint witness"),
    ("recolor-gt", "(h) Recolor target"),
]
for ax, (name, title) in zip(axes.flat, panels):
    panel(ax, name, title)
fig.subplots_adjust(wspace=.02, hspace=.17)
save(fig, "brick-tasks")

fig, axes = plt.subplots(2, 3, figsize=(12, 5.2))
for i in range(4):
    row = images[f"step-{i + 1}"]
    panel(axes.flat[i], row["name"], f'Legal prefix: {row["metadata"]["count"]}/{row["metadata"]["total"]} parts')
blocked = images["step-blocked"]["metadata"]
panel(axes.flat[4], "step-blocked", f'Greedy dead end: {len(blocked["order"])} parts')
panel(axes.flat[5], "step-target", "Target: missing piece outlined")
fig.subplots_adjust(wspace=.02, hspace=.15)
save(fig, "brick-execution")

fig, axes = plt.subplots(1, 4, figsize=(12, 3.5))
for ax, name, title in zip(axes, ["hidden-exterior-0", "hidden-exterior-1", "hidden-exploded-0", "hidden-exploded-1"],
                            ["Exterior A", "Exterior B", "GT A: horizontal tiling", "GT B: vertical tiling"]):
    panel(ax, name, title)
fig.subplots_adjust(wspace=.02)
save(fig, "brick-ambiguity")

(ROOT / "structure-figure-evidence.json").write_text(json.dumps({
    "generatorSha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "renderManifestSha256": hashlib.sha256((ROOT / "structure-evidence.json").read_bytes()).hexdigest(),
    "figures": outputs, "images": len(images), "apiRequests": 0,
    "outputSha256": {name + ".pdf": hashlib.sha256((ROOT / "figures" / (name + ".pdf")).read_bytes()).hexdigest()
                     for name in outputs},
}, indent=2) + "\n")
print(json.dumps({"figures": outputs, "actual3DRenders": len(images)}))
