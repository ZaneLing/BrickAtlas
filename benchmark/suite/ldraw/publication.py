"""Deterministic publication statistics, vector plots and unrun experiment tables.

Run after paper.py. Never edits source geometry, tasks or historical experiments.
"""
from collections import Counter
from pathlib import Path
import csv
import hashlib
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
DATA, PAPER = ROOT / "benchmark/ldraw-v1", ROOT / "benchmark/paper"
OUT = PAPER / "analysis"
OUT.mkdir(exist_ok=True)
catalog = json.loads((DATA / "catalog.json").read_text())
bundles = {m["id"]: json.loads((ROOT / "public/benchmark/ldraw/models" / (m["id"] + ".json")).read_text()) for m in catalog}
tasks = [t for b in bundles.values() for t in b["tasks"]]
BANDS = ["D1", "D2", "D3", "D4"]
FAMILIES = [
    ("color", "Color", "A", "V", "Bind instance; inspect color; select option."),
    ("shape-match", "Part type", "A", "V", "Bind target and candidates; ignore pose/color; match source type."),
    ("distance", "Distance", "A", "S", "Read bounding-box centers; compute Euclidean distances; select minimum."),
    ("interface", "Interface", "M", "G", "Read supplied connector record; map its family to an option."),
    ("neighbors", "Neighbors", "M", "G", "Bind target; collect one-hop neighbors; return exact candidate set."),
    ("coverage", "Coverage", "M", "S", "Read definition-coverage flags; identify the unsupported instance."),
    ("evidence-limit", "Evidence limit", "M", "S", "Inspect evidence scope; distinguish CAD evidence from stability proof."),
    ("source-step", "Step lookup", "P", "S", "Bind instance; filter author records; return first expanded step."),
    ("source-sequence", "Step sequence", "P", "E", "Read source window; satisfy predecessor facts; reveal steps in order."),
    ("restore-instance", "Restoration", "P", "E", "Bind missing ID; check missing fact; restore original visibility."),
    ("graph-removal", "Graph deletion", "I", "G", "Induce local graph; delete target vertex and edges; count components."),
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tex(value):
    return "".join({"&": r"\&", "%": r"\%", "_": r"\_", "#": r"\#", "$": r"\$",
                    "{": r"\{", "}": r"\}"}.get(c, c) for c in str(value))


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


def csv_file(name, rows):
    with (OUT / (name + ".csv")).open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


sources = []
for m in catalog:
    b = bundles[m["id"]]
    records = Counter(e["family"] for e in b["audit"]["edges"])
    sources.append({
        "id": m["id"], "set": m["setNumber"], "band": m["difficulty"],
        "instances": len(b["parts"]), "types": len({p["partNumber"] for p in b["parts"]}),
        "colors": len({p["colorCode"] for p in b["parts"]}), "tasks": len(b["tasks"]),
        "coverage": m["connectorCoverage"], "intersections": m["intersectionCandidates"],
        **{k: records[k] for k in ["stud", "axle", "hinge", "fixed", "ball"]},
    })
family_scale = [{"family": key, **{d: sum(t["family"] == key and t["difficulty"] == d for t in tasks) for d in BANDS}}
                for key, *_ in FAMILIES]
priors = []
for key, name, *_ in FAMILIES:
    choice = [t for t in tasks if t["family"] == key and t["format"] == "single-choice"]
    if not choice:
        continue
    counts = Counter(t["answer"]["choiceId"] for t in choice)
    semantic = Counter(json.dumps(next(o["value"] for o in t["options"] if o["id"] == t["answer"]["choiceId"]), sort_keys=True) for t in choice)
    priors.append({
        "family": key, "label": name, "n": len(choice), "always_A": counts["A"] / len(choice),
        "uniform": sum(1 / len(t["options"]) for t in choice) / len(choice),
        "semantic_majority": None if key in {"shape-match", "distance", "coverage"} else max(semantic.values()) / len(choice),
        **{letter: counts[letter] for letter in "ABCDE"},
    })
csv_file("sources", sources)
csv_file("family-scale", family_scale)
csv_file("answer-priors", priors)
summary = {
    "sourceCount": len(sources), "taskCount": len(tasks),
    "instances": sum(s["instances"] for s in sources),
    "uniqueSourceTypes": len({p["partNumber"] for b in bundles.values() for p in b["parts"]}),
    "uniqueSourceColors": len({p["colorCode"] for b in bundles.values() for p in b["parts"]}),
    "sourceInstanceRange": [min(s["instances"] for s in sources), max(s["instances"] for s in sources)],
    "sourceInstanceMedian": float(np.median([s["instances"] for s in sources])),
    "modalities": dict(Counter(t["modality"] for t in tasks)),
    "formats": dict(Counter(t["format"] for t in tasks)),
    "connectorRecords": {k: sum(s[k] for s in sources) for k in ["stud", "axle", "hinge", "fixed", "ball"]},
    "scope": "Descriptive source statistics and answer priors only; no learned or physical outcomes.",
}
write_json(OUT / "statistics.json", summary)
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 8, "axes.labelsize": 8,
    "xtick.labelsize": 7, "ytick.labelsize": 7, "axes.spines.top": False,
    "axes.spines.right": False, "axes.edgecolor": "#a3aab6",
    "text.color": "#273343", "axes.labelcolor": "#273343",
    "pdf.fonttype": 42, "ps.fonttype": 42, "savefig.facecolor": "white",
})
palette = ["#2d728f", "#d88841", "#649b8e", "#886ba7", "#cb6374"]
plots = []


def save(fig, name, description, inputs):
    for ext in ["pdf", "png"]:
        fig.savefig(OUT / f"{name}.{ext}", dpi=240, bbox_inches="tight",
                    metadata={"CreationDate": None, "ModDate": None} if ext == "pdf" else {})
    plt.close(fig)
    plots.append({"name": name, "meaning": description, "data": inputs,
                  "files": {ext: sha(OUT / f"{name}.{ext}") for ext in ["pdf", "png"]}})


fig, axes = plt.subplots(1, 2, figsize=(6.9, 2.15), layout="constrained")
for key, label, color in zip(["instances", "types", "colors"], ["Instances", "Part types", "Color codes"], palette):
    xs = np.sort([s[key] for s in sources])
    axes[0].step(xs, np.arange(1, len(xs) + 1) / len(xs), where="post", color=color, label=label, linewidth=1.8)
axes[0].set(xscale="log", xlabel="Count per source (log scale)", ylabel="Fraction of sources", ylim=(0, 1.04))
axes[0].legend(frameon=False, fontsize=7, loc="upper left")
axes[0].grid(axis="y", alpha=.15)
for i, d in enumerate(BANDS):
    ss = [s for s in sources if s["band"] == d]
    axes[1].scatter([s["instances"] for s in ss], [s["types"] for s in ss],
                    s=28, label=d, color=palette[i], edgecolor="white", linewidth=.5, zorder=3)
axes[1].set(xscale="log", yscale="log", xlabel="Source instances (log scale)", ylabel="Source part types (log scale)")
axes[1].legend(frameon=False, ncol=2, fontsize=7)
axes[1].grid(alpha=.15)
save(fig, "source-distribution", "Empirical source distributions and inventory scale, 24 sources.", ["sources.csv"])

fig, ax = plt.subplots(figsize=(3.35, 2.9), layout="constrained")
matrix = np.array([[r[d] for d in BANDS] for r in family_scale])
ax.pcolormesh(np.arange(5) - .5, np.arange(len(FAMILIES) + 1) - .5, matrix,
              cmap="Blues", vmin=0, vmax=matrix.max() * 1.12)
ax.invert_yaxis()
ax.set_xticks(range(4), BANDS)
ax.set_yticks(range(len(FAMILIES)), [f[1] for f in FAMILIES])
ax.tick_params(length=0)
ax.set_xlabel("Source scale band")
for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        ax.text(j, i, str(matrix[i, j]), ha="center", va="center", fontsize=8,
                color="white" if matrix[i, j] > matrix.max() * .6 else "#273343")
save(fig, "family-scale", "Question counts by family and source-size band; zero means absent.", ["family-scale.csv"])

fig, ax = plt.subplots(figsize=(3.35, 2.9), layout="constrained")
bottom = np.zeros(len(sources))
for family, color in zip(["stud", "axle", "hinge", "fixed", "ball"], palette):
    ys = np.array([s[family] / sum(s[k] for k in ["stud", "axle", "hinge", "fixed", "ball"]) for s in sources])
    ax.bar(range(len(sources)), ys, bottom=bottom, color=color, width=.86, label=family.capitalize())
    bottom += ys
ax.set_xticks(range(len(sources)), [s["set"] for s in sources], rotation=90, fontsize=5.8)
ax.set(ylabel="Fraction of connector records", ylim=(0, 1.15), xlabel="Original set (ascending instance count)")
ax.legend(frameon=False, ncol=3, fontsize=6, loc="upper center", columnspacing=.8, handlelength=1)
save(fig, "connector-diversity", "Within-source fractions of raw connector records, including repeated part pairs.", ["sources.csv"])

fig, ax = plt.subplots(figsize=(6.9, 2.15), layout="constrained")
x = np.arange(len(priors))
for i, (key, label) in enumerate([("uniform", "Uniform expectation"), ("always_A", "Always A"), ("semantic_majority", "Semantic majority (shared values)")]):
    ax.bar(x + (i - 1) * .24, [p[key] * 100 if p[key] is not None else np.nan for p in priors], width=.22, label=label, color=palette[i])
ax.set_xticks(x, [p["label"] for p in priors], fontsize=7)
ax.set(ylabel="Single-choice rate (%)", ylim=(0, 121))
ax.set_yticks([0, 25, 50, 75, 100])
ax.legend(frameon=False, ncol=3, fontsize=7, loc="upper center")
ax.grid(axis="y", alpha=.15)
ax.set_axisbelow(True)
save(fig, "answer-priors", "Single-choice controls and semantic concentration, measured on this release, not held-out performance.", ["answer-priors.csv"])

# A publication contract: every prospective result is null; descriptors are not scores.
systems = ["SmolVLM", "Qwen3-VL", "Llama 4", "GPT-4.1", "Gemini", "Claude"]
experiments = {
    "version": "ldraw-1-publication-plan-v1",
    "status": "proposed-not-run",
    "release": "brickatlas-ldraw-1",
    "methodPolicy": "Candidate model families; exact checkpoint/API revision, prompts and decoding must be frozen before execution.",
    "missingPolicy": "null means unrun; render an empty numeric cell, never zero, dash, imputation or a historical pilot score.",
    "tables": [],
}


def planned(name, descriptors, metrics, rows, spec=None):
    entries = [{"condition": row, "results": {metric: None for metric in metrics}} for row in rows]
    experiments["tables"].append({"id": name, "descriptors": descriptors, "metrics": metrics, "rows": entries})
    headers = descriptors + metrics
    body = [" & ".join(tex(c) for c in e["condition"]) + " & " + " & ".join("" for _ in metrics) + r"\\" for e in entries]
    wrapping = name == "ablations"
    begin = r"\begin{tabularx}{\linewidth}{Xlrrr}" if wrapping else "\\begin{tabular}{" + (spec or ("l" * len(descriptors) + "r" * len(metrics))) + "}"
    content = (begin + "\n\\toprule\n"
               + " & ".join(tex(c) for c in headers) + r"\\\midrule" + "\n" + "\n".join(body)
               + "\n\\bottomrule\n\\end{" + ("tabularx" if wrapping else "tabular") + "}\n")
    (PAPER / f"ldraw-plan-{name}.tex").write_text(content)


planned("models", ["Candidate family"], ["V", "S", "G", "E", "Micro", "Macro"], [[s] for s in systems])
planned("families", ["Task family", "N"], ["Smol", "Qwen", "Llama", "GPT", "Gemini", "Claude"],
        [[name, sum(t["family"] == key for t in tasks)] for key, name, *_ in FAMILIES])
planned("scale", ["Candidate family"], ["D1", "D2", "D3", "D4", "95% CI"], [[s] for s in systems])
planned("ablations", ["Condition", "N"], ["Acc.", "Valid", "Calls"],
        [["Static numbered image", "140"], ["+ rotate / zoom", "140"], ["+ ID isolation", "140"],
         ["Text without image", "140"], ["Structured public input", "477"],
         ["Graph edges withheld", "233"], ["Public action solver", "75"]])
planned("robustness", ["Perturbation", "Eligible"], ["Base", "Changed", "Consist."],
        [["ID permutation", "617"], ["Choice-order permutation", "542"], ["Camera perturbation", "V: 140"],
         ["Color nuisance", "Type: 67"], ["Equivalent edge ordering", "G: 233"]])
planned("human", ["Review stratum", "Pool"], ["Reviewed", "Pass", "Agree", "Time"],
        [["Visual grounding", "140"], ["Structured questions", "477"], ["All original sources", "24"],
         ["Intersection candidates", "573"]])
planned("physical", ["Validation procedure"], ["Reviewed", "Pass", "Fail", "Unresolved"],
        [["Connector-aware pair inspection"], ["Unsupported-part adjudication"], ["Insertion / extraction study"],
         ["Gravity / friction simulation"], ["Physical assembly validation"]])
planned("resources", ["Candidate family"], ["Tokens", "Calls", "p50 s", "p95 s", "USD"], [[s] for s in systems])
planned("actions", ["Candidate family"], ["Valid %", "Goal %", "Cost", "Steps"], [[s] for s in systems])
write_json(PAPER / "ldraw-experiments.json", experiments)

rows = []
for key, name, layer, modality, operators in FAMILIES:
    n = sum(t["family"] == key for t in tasks)
    rows.append(f"{tex(name)} & {n} & {layer} & {modality} & {tex(operators)}" + r"\\")
(PAPER / "ldraw-operators.tex").write_text(
    r"\begin{tabularx}{\textwidth}{lrrrX}" + "\n\\toprule\nFamily & $N$ & Layer & Input & Functional decomposition"
    + r"\\\midrule" + "\n" + "\n".join(rows) + "\n\\bottomrule\n\\end{tabularx}\n")

sequence = next(t for t in bundles["omr-42102"]["tasks"] if t["family"] == "source-sequence")
rows = []
cumulative = 0
for i, s in enumerate(sequence["input"]["sourceWindow"], 1):
    labels = s["labels"]
    cumulative += len(labels)
    new_ids = labels[0] if len(labels) == 1 else labels[0] + "--" + labels[-1]
    rows.append(rf"{i} & \texttt{{{'start' if i == 1 else 'done-' + str(i-1)}}} & \texttt{{{new_ids}}} & {cumulative} & \texttt{{done-{i}}}" + r"\\")
(PAPER / "ldraw-step-trace.tex").write_text(
    "\\begin{tabular}{rllrl}\n\\toprule\nStep & Prerequisite & Added IDs & $|V|$ & New fact"
    + r"\\\midrule" + "\n" + "\n".join(rows) + "\n\\bottomrule\n\\end{tabular}\n")

# Main-paper metadata stays compact; every plotted value is available as CSV/JSON.
manifest = {
    "generator": "benchmark/suite/ldraw/publication.py",
    "generatorSha256": sha(Path(__file__)),
    "inputs": {str(p.relative_to(ROOT)): sha(p) for p in [
        DATA / "release.json", DATA / "catalog.json", DATA / "verification.json",
        *[ROOT / "public/benchmark/ldraw/models" / (m["id"] + ".json") for m in catalog]]},
    "plots": plots,
    "analysisFiles": {p.name: sha(p) for p in sorted(OUT.iterdir()) if p.suffix in {".csv", ".json"}},
    "experimentPlanSha256": sha(PAPER / "ldraw-experiments.json"),
    "prospectiveTables": len(experiments["tables"]),
    "prospectiveResultCells": sum(len(row["results"]) for table in experiments["tables"] for row in table["rows"]),
}
write_json(PAPER / "ldraw-publication.json", manifest)
assert summary["instances"] == 15334 and summary["taskCount"] == 617
assert all(v is None for table in experiments["tables"] for row in table["rows"] for v in row["results"].values())
print(json.dumps({"statistics": summary, "plots": len(plots), "unrunResultCells": manifest["prospectiveResultCells"]}, indent=2))
