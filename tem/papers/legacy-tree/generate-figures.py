"""Data-grounded paper figures. No model calls or synthetic result values."""
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent
STUDY = ROOT.parent / "suite/artifacts/study"
OUT = ROOT / "figures"
SOURCES = {}
OUTPUTS = []
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "axes.titlesize": 10,
    "axes.labelsize": 9, "axes.spines.top": False, "axes.spines.right": False,
    "pdf.fonttype": 42, "savefig.facecolor": "white",
})
BLUE, GREEN, RED, GRAY = "#2776ad", "#25806a", "#bf514b", "#647078"
COLORS = [BLUE, GREEN, RED, "#d6a435"]


def read(path):
    raw = path.read_bytes()
    SOURCES[str(path.relative_to(ROOT.parent))] = hashlib.sha256(raw).hexdigest()
    return json.loads(raw)


def image(path):
    raw = path.read_bytes()
    SOURCES[str(path.relative_to(ROOT.parent))] = hashlib.sha256(raw).hexdigest()
    return Image.open(path)


def save(fig, name):
    fig.savefig(OUT / (name + ".pdf"), bbox_inches="tight",
                metadata={"CreationDate": None, "ModDate": None})
    fig.savefig(OUT / (name + ".png"), dpi=180, bbox_inches="tight")
    OUTPUTS.append(name)
    plt.close(fig)


audit = read(STUDY / "paper-audit/audit.json")
order = read(STUDY / "order-study/analysis.json")
witness = read(STUDY / "observability-witness.json")
probe = read(STUDY / "pose-probes/protocol.json")
failures = read(STUDY / "failure-diagnostics.json")
catalog = {p["partId"]: p for p in audit["coverage"]["partTypes"]}

# A real probe makes information privileges visible without suggesting all tasks use RGB.
row = next(r for r in probe["rows"] if r["arm"] == "full-rgb")
fig = plt.figure(figsize=(12, 4.5))
for i, (label, path) in enumerate(zip(["Isometric", "Top (+Y)", "Front (+Z)", "Side (+X)"], row["images"])):
    ax = fig.add_axes([.02 + i * .155, .47, .15, .40])
    ax.imshow(image(STUDY / "pose-probes" / path))
    ax.axis("off")
    ax.set_title(label, fontsize=10)
ax = fig.add_axes([0, 0, 1, 1])
ax.axis("off")
ax.text(.02, .97, "A. Declared observations", fontweight="bold", fontsize=12)
ax.text(.66, .97, "B. Shared source, distinct tasks", fontweight="bold", fontsize=12)
for i, label in enumerate(["Recognize parts", "Query relations", "Reconstruct", "Generate",
                           "Complete", "Edit", "Assemble / disassemble", "Detect / repair"]):
    ax.text(.66 + (i % 2) * .17, .85 - (i // 2) * .085, label, fontsize=10)
ax.text(.02, .435, "RGB + BOM", color=BLUE, fontweight="bold", fontsize=10)
ax.text(.22, .435, "Layer views: additional geometry", color=GREEN, fontsize=10)
ax.text(.22, .377, "Symbolic reference: privileged geometry", color=RED, fontsize=10)
ax.text(.66, .435, "Other tasks use their declared symbolic inputs.", fontsize=9)
ax.text(.02, .285, "C. Evaluation contract", fontweight="bold", fontsize=12)
boxes = [
    (.02, "Source group", "split + provenance"),
    (.27, "Public input", "fixed images + prompt"),
    (.52, "Submitted answer", "no hidden correction"),
    (.77, "Typed evaluation", "format / geometry / task"),
]
for x, title, subtitle in boxes:
    ax.add_patch(Rectangle((x, .055), .21, .16, facecolor="#f2f5f6", edgecolor="#b8c6ca"))
    ax.text(x + .105, .153, title, ha="center", fontweight="bold", fontsize=11)
    ax.text(x + .105, .097, subtitle, ha="center", fontsize=9)
    if x < .7:
        ax.annotate("", (x + .247, .135), (x + .215, .135),
                    arrowprops={"arrowstyle": "->", "color": GRAY})
save(fig, "benchmark-overview")

rows = audit["coverage"]["rows"]
policies = list(dict.fromkeys(r["policy"] for r in rows))
fig, axes = plt.subplots(1, 3, figsize=(12, 3.15), gridspec_kw={"width_ratios": [1, 1.25, 1.1]})
for split, color, label in zip(["train", "validation", "test_id", "test_ood"], COLORS,
                              ["Train", "Validation", "ID test", "Policy holdout"]):
    values = [r["pieces"] for r in rows if r["split"] == split]
    axes[0].hist(values, bins=np.arange(8, 50, 3), histtype="step", linewidth=1.7, color=color, label=label)
axes[0].set(xlabel="Parts per source object", ylabel="Objects", title="A. Size by split")
axes[0].legend(frameon=False, fontsize=7.5)
counts = np.array([[sum(r["policy"] == p and r["difficulty"] == d for r in rows)
                    for d in ["small", "medium", "large"]] for p in policies])
axes[1].imshow(counts, cmap="Blues", vmin=0, vmax=640, aspect="auto")
axes[1].set_xticks(range(3), ["9-16", "17-28", "29-47"])
axes[1].set_yticks(range(8), [p.replace("-", " ") for p in policies], fontsize=8)
axes[1].set(title="B. Policy x size (object counts)", xlabel="Parts per source object")
for y in range(8):
    for x in range(3):
        axes[1].text(x, y, str(counts[y, x]), ha="center", va="center",
                     color="white" if counts[y, x] > 370 else "#18272d", fontsize=8)
types = audit["coverage"]["partTypes"]
axes[2].bar(range(len(types)), [p["instances"] for p in types],
            color=[BLUE if p["instances"] else RED for p in types])
axes[2].set_xticks(range(len(types)), [p["partId"] for p in types], rotation=90, fontsize=6.5)
axes[2].set(ylabel="Placed part instances", title="C. Actual catalog coverage")
axes[2].text(.97, .94, f'{audit["coverage"]["assembledTypes"]}/25 assembled types',
             transform=axes[2].transAxes, ha="right", fontsize=9)
fig.tight_layout(w_pad=1.5)
save(fig, "dataset-distribution")

# The hidden-layer diagram is a disclosed cross-section, never an ordinary input image.
fig, axes = plt.subplots(1, 3, figsize=(10.8, 2.7), gridspec_kw={"width_ratios": [1, 1, 1.3]})
for ax, name, label in zip(axes[:2], ["target", "alternative"], ["A. Reference tiling", "B. Alternative tiling"]):
    parts = witness[name]["parts"]
    for p in parts:
        if p["y"] != 1:
            continue
        cat = catalog[p["partId"]]
        w, d = (cat["d"], cat["w"]) if p["turn"] % 2 else (cat["w"], cat["d"])
        ax.add_patch(Rectangle((p["x"], p["z"]), w, d,
                              facecolor=RED if p["color"] == "red" else "#ced5d9",
                              edgecolor="white", linewidth=2))
        if p["color"] == "red":
            ax.text(p["x"] + w / 2, p["z"] + d / 2, p["id"].replace("inside", "I"),
                    ha="center", va="center", color="white", fontsize=11)
    for p in [p for p in parts if p["color"] == "blue"]:
        ax.plot(p["x"] + .5, p["z"] + .5, "o", color=BLUE, markersize=11, markeredgecolor="white")
    ax.set(xlim=(-.1, 4.1), ylim=(-.1, 4.1), aspect="equal", title=label, xlabel="X (studs)", ylabel="Z (studs)")
    ax.set_xticks(range(5)); ax.set_yticks(range(5))
    ax.invert_yaxis()
ax = axes[2]
ax.axis("off")
ax.text(0, .94, "C. Same volume, different supports", fontweight="bold")
items = [
    "BOM / colored occupancy: identical",
    "Positive-axis surface F1: 1.00",
    "Part F1: {:.3f}; edge F1: {:.3f}".format(
        witness["scores"]["ordinary"]["metrics"]["partF1"],
        witness["scores"]["ordinary"]["metrics"]["edgeF1"]),
    "Ordinary criterion: accepts both",
    "Full reference criterion: distinguishes",
    "Blue pair shares a lower support:",
    "A: yes                 B: no",
]
for i, text in enumerate(items):
    ax.text(0, .78 - i * .105, text, fontsize=9, color=BLUE if i == 6 else "#26353b")
fig.tight_layout(w_pad=1)
save(fig, "hidden-structure")

fig, axes = plt.subplots(1, 2, figsize=(10.8, 2.8), gridspec_kw={"width_ratios": [1.15, 1]})
models = ["GPT-4.1 mini", "GPT-4.1", "Gemini Flash", "Qwen3-VL-32B"]
yy = np.arange(4)
axes[0].barh(yy - .16, [r["repeatMismatch"] / r["pairedGroups"] for r in order["byModel"]],
             height=.3, color=GRAY, label="Same-order repeat")
axes[0].barh(yy + .16, [r["permutationMismatch"] / r["pairedGroups"] for r in order["byModel"]],
             height=.3, color=RED, label="Candidate permutation")
axes[0].set_yticks(yy, models)
axes[0].invert_yaxis()
axes[0].set(xlim=(0, 1), xlabel="Actual-pose mismatch rate", title="A. Reordering versus repetition")
axes[0].legend(loc="upper center", bbox_to_anchor=(.5, -.32), ncol=2, frameon=False, fontsize=8)
for i, r in enumerate(order["byModel"]):
    ci = r["excessMismatchInterval"]
    axes[1].errorbar(ci["mean"], i, xerr=[[ci["mean"] - ci["low"]], [ci["high"] - ci["mean"]]],
                     fmt="o", capsize=4, color=BLUE, markersize=6)
axes[1].set_yticks(yy, models)
axes[1].invert_yaxis()
axes[1].axvline(0, color=GRAY, linestyle="--", linewidth=1)
axes[1].set(xlim=(-.05, 1.05), xlabel="Excess mismatch D (95% source-bootstrap interval)",
            title="B. Paired effect, 12 sources per model")
fig.tight_layout(w_pad=2)
save(fig, "order-sensitivity")

fig, axes = plt.subplots(1, 2, figsize=(10.8, 3.1))
copy = audit["copyControls"]["summary"]
yy = np.arange(len(copy))
axes[0].barh(yy, [r["metrics"]["partF1"]["mean"] * 100 for r in copy], height=.6, color=BLUE, label="Global part F1")
axes[0].plot([r["metrics"]["success"]["mean"] * 100 for r in copy], yy, "D", color=RED, label="Task success")
axes[0].set_yticks(yy, [r["key"] for r in copy], fontsize=8)
axes[0].invert_yaxis()
axes[0].set(xlim=(-2, 106), xlabel="Score (%)", title="A. Copy-current control: 5,120 objects per row")
axes[0].legend(frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(.5, -.32), ncol=2)
selected = failures["byModel"][:3]
groups = [
    ("JSON / schema / domain", ["json", "response-schema", "structure-domain"], RED),
    ("Geometry", ["geometry"], "#d6a435"),
    ("Task / execution / preservation", ["plan-execution", "answer-mismatch", "preservation", "localization", "target-or-constraints"], BLUE),
    ("Success", ["success"], GREEN),
]
bottom = np.zeros(3)
for label, stages, color in groups:
    values = np.array([sum(r["stages"][s] for s in stages) / r["n"] * 100 for r in selected])
    axes[1].bar(range(3), values, bottom=bottom, label=label, color=color, width=.6)
    bottom += values
assert np.allclose(bottom, 100)
axes[1].set_xticks(range(3), ["GPT mini", "Gemini Flash", "SmolVLM base"], fontsize=8)
axes[1].set(ylim=(0, 105), ylabel="Responses (%)", title="B. Earliest rejection stage (337 cases each)")
axes[1].legend(frameon=False, fontsize=7.3, loc="upper center", bbox_to_anchor=(.5, -.16))
fig.tight_layout(w_pad=2)
save(fig, "metric-diagnostics")

(ROOT / "figure-evidence.json").write_text(json.dumps({
    "version": "paper-figures-1", "apiRequests": 0,
    "generatorSha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "sourcesSha256": SOURCES, "figures": OUTPUTS,
    "overviewSourceGroup": row["group"],
    "scope": "Real archived renders, full-casebank descriptive statistics, a disclosed geometric witness and adaptive development results.",
    "outputSha256": {name + ".pdf": hashlib.sha256((OUT / (name + ".pdf")).read_bytes()).hexdigest() for name in OUTPUTS},
}, indent=2) + "\n")
print(json.dumps({"figures": OUTPUTS, "sourceFiles": len(SOURCES)}))
