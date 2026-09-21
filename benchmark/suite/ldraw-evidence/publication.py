#!/usr/bin/env python3
"""Build only the evidence-v1 paper assets from hash-checked frozen inputs."""
import csv
import json
import shutil
from collections import Counter

from common import DATA, ROOT, VERSION, internal_tasks, load, read_frozen, save, sha

PAPER = ROOT / "benchmark/paper/evidence-v1"
FIG = PAPER / "figures"
GEN = PAPER / "generated"
INPUTS = {}
DERIVATIVES = []


def source(path):
    path = ROOT / path
    INPUTS[str(path.relative_to(ROOT))] = sha(path)
    return path


def tex(s):
    return "".join({"&": r"\&", "%": r"\%", "_": r"\_", "#": r"\#",
                    "{": r"\{", "}": r"\}", "$": r"\$"}.get(c, c) for c in str(s))


def frozen(path):
    source(path)
    return read_frozen(path)


def read(path):
    return load(source(path))


def copy(path, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source(path), target)


def savefig(fig, name):
    fig.savefig(FIG / f"{name}.pdf", metadata={"CreationDate": None})
    fig.savefig(FIG / f"{name}.png", dpi=220)


def image(path, box=None):
    from PIL import Image
    im = Image.open(source(path)).convert("RGB")
    if box:
        DERIVATIVES.append({"source": path, "box_xyxy": box, "purpose": "paper-only detail"})
        im = im.crop(box)
    return im


def table(headers, rows, spec):
    return (r"\begin{tabularx}{\linewidth}{" + spec + "}\n\\toprule\n" +
            " & ".join(headers) + r"\\\midrule" + "\n" +
            "\n".join(" & ".join(tex(v) for v in r) + r"\\" for r in rows) +
            "\n\\bottomrule\n\\end{tabularx}\n")


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.patches import Rectangle

    for p in [PAPER, FIG, GEN]:
        p.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9,
                         "pdf.fonttype": 42, "svg.fonttype": "none"})
    cat = frozen("benchmark/ldraw-v2/catalog.json")
    tasks = internal_tasks()
    for m in cat:
        source(f"public/benchmark/ldraw-v2/models/{m['id']}.json")
    sel = read("benchmark/ldraw-evidence-v1/report-selection.json")
    audit = read("benchmark/ldraw-evidence-v1/node-prior-audit.json")
    challenge = read("benchmark/ldraw-evidence-v1/matched-graphs-v1/manifest.json")
    example = read("benchmark/ldraw-evidence-v1/literature/worked-example.json")
    analysis = frozen("benchmark/ldraw-v2/descriptive-analysis/analysis.json")
    contracts = frozen("benchmark/ldraw-v2/task-contracts.json")["contracts"]
    queue = frozen("public/benchmark/ldraw-v2/human-review-queue.json")
    physical = frozen("public/benchmark/ldraw-v2/physical-review-queue.json")
    index = read("benchmark/ldraw-evidence-v1/results-index.json")
    lock = read("benchmark/ldraw-evidence-v1/baseline-lock.json")
    fixed = audit["baselines"]["fixed-answer-4"]["natural"]
    counts = Counter(t["family"] for t in tasks.values())
    macros = {"Sources": len(cat), "Parts": f"{sum(m['parts'] for m in cat):,}",
              "Tasks": len(tasks), "Visual": len(sel["groups"]["core-visual"]),
              "Structural": len(sel["groups"]["structural-evidence"]),
              "Controls": len(sel["groups"]["nonconstant-controls"]),
              "Constant": len(sel["groups"]["constant-controls"]),
              "NodeHits": audit["hits"], "GraphN": audit["summary"]["pairs"],
              "NodeMicro": f"{100*audit['summary']['micro']:.2f}",
              "NodeMacro": f"{100*audit['summary']['source_macro']:.2f}",
              "NodeLo": f"{100*audit['summary']['source_macro_ci95'][0]:.2f}",
              "NodeHi": f"{100*audit['summary']['source_macro_ci95'][1]:.2f}",
              "PositiveDeficit": audit["strata"]["deficit>0"]["items"],
              "PositiveSources": audit["strata"]["deficit>0"]["sources"],
              "ChallengeObs": challenge["observation_count"],
              "ChallengePairs": challenge["pair_count"],
              "ChallengeUp": challenge["directions"]["increase"],
              "ChallengeDown": challenge["directions"]["decrease"],
              "ChallengeSame": challenge["directions"]["unchanged"],
              "DegreeMatched": challenge["matching_counts"]["same-nodes-edges-target-and-surviving-degrees"],
              "DegreeGaps": len(challenge["feasibility_gaps"]),
              "FixedMacro": f"{100*fixed['source_macro']:.2f}",
              "FixedLo": f"{100*fixed['source_macro_ci95'][0]:.2f}",
              "FixedHi": f"{100*fixed['source_macro_ci95'][1]:.2f}",
              "FrozenFiles": f"{len(lock['files']):,}",
              "PlannedRuns": len(index["entries"]),
              "PhysicalPending": len(physical["pairs"]),
              "OtherPending": len(queue["items"]) - len(sel["groups"]["core-visual"])}
    for name, family in [("ColorN", "color"), ("TypeN", "shape-match"), ("StepN", "source-sequence"),
                         ("LimitN", "evidence-limit"), ("RestoreN", "restore-instance")]:
        macros[name] = counts[family]
    (GEN / "numbers.tex").write_text("\n".join(
        r"\newcommand{\Ev%s}{%s}" % (k, v) for k, v in macros.items()) + "\n")
    save(GEN / "numbers.json", macros)
    for p in sorted((DATA / "generated").glob("*.tex")):
        copy(str(p.relative_to(ROOT)), GEN / p.name)
    for name in ["cvpr.sty", "ieeenat_fullname.bst"]:
        copy(f"benchmark/ldraw-evidence-v1/literature/author-kit/{name}", PAPER / name)
    # Complete original dossiers are copied verbatim, without old front matter.
    for name in ["cases.tex", "contracts.tex", "bands.tex", "adapters.tex", "conditions.tex"]:
        copy(f"benchmark/paper/tables-v2/{name}", GEN / name)
    for m in cat:
        copy(f"benchmark/paper/figures-v2/{m['id']}-iso.jpg",
             PAPER / "figures-v2" / f"{m['id']}-iso.jpg")

    names = {c["family"]: c["name"] for c in contracts}
    rows = []
    for c in contracts:
        f = c["family"]
        rows.append([names[f], counts[f], len({t["modelId"] for t in tasks.values() if t["family"] == f}),
                     sel["families"][f]["role"].replace("-", " ")])
    (GEN / "families.tex").write_text(table(["Family", "$N$", "Sources", "Report role"], rows, "XrrX"))
    (GEN / "source-baselines.tex").write_text(table(
        ["Source", "$N$", "Node-only correct"],
        [[s, x["n"], x["hits"]] for s, x in audit["by_source"].items()], "Xrr"))
    (GEN / "graph-failures.tex").write_text(table(
        ["Task", "Nodes after", "Edges after", "Gold"],
        [[r["task_id"], r["n_after"], r["m_after"], r["gold"]] for r in audit["rows"] if not r["hit"]],
        "Xrrr"))

    # Figure 1: one true source identity, four separately inspectable contracts.
    fig, axs = plt.subplots(2, 2, figsize=(7, 3.9))
    fig.subplots_adjust(left=.015, right=.99, top=.93, bottom=.04, wspace=.12, hspace=.38)
    for ax in axs.flat:
        ax.axis("off")
    axs[0, 0].imshow(image("public/" + example["images"]["crop"]["file"], (560, 365, 930, 670)))
    axs[0, 0].set_title("(a) Numbered visual operands", loc="left", fontweight="bold")
    ax = axs[0, 1]
    ax.set_title("(b) Canonical source record", loc="left", fontweight="bold")
    ax.text(.01, .91, "OMR 42004 · Mini Backhoe Loader", va="top", fontweight="bold")
    ax.text(.01, .70, "B0035  =  brick_000035\nPart 32250  ·  Black\nB0036: same type, another instance\nB0196: part 2780 (pin)\nSource poses are preserved.", va="top", linespacing=1.7)
    ax = axs[1, 0]
    ax.set_title("(c) Recognized connector graph", loc="left", fontweight="bold")
    pos = {"B0035": (.48, .5), "B0034": (.13, .85), "B0037": (.84, .85),
           "B0038": (.13, .14), "B0051": (.84, .14)}
    for edge in example["recognized_edges"]:
        label = "B" + edge["b"].split("_")[1][-4:]
        x, y = pos[label]; cx, cy = pos["B0035"]
        ax.plot([cx, x], [cy, y], color="#48778e", lw=1.5)
    for label, (x, y) in pos.items():
        ax.text(x, y, label, ha="center", va="center", bbox=dict(
            boxstyle="round,pad=.35", fc="#deedf5" if label == "B0035" else "white", ec="#48778e"))
    ax.set(xlim=(0, 1), ylim=(-.03, 1))
    ax = axs[1, 1]
    ax.set_title("(d) Independent visibility edit", loc="left", fontweight="bold")
    ax.text(.02, .80, "missing-B0035", bbox=dict(fc="#fff3e6", ec="#a96728", pad=6))
    ax.annotate("", xy=(.77, .49), xytext=(.28, .68), arrowprops=dict(arrowstyle="->", color="#225d78", lw=1.5))
    ax.text(.04, .40, "restore-B0035", fontweight="bold")
    ax.text(.50, .15, "present-B0035", bbox=dict(fc="#e7f1e9", ec="#437b50", pad=6))
    ax.text(.02, -.03, "Same saved pose; no insertion trajectory.", fontsize=8)
    savefig(fig, "instance-alignment"); plt.close(fig)

    # Figure 2: identical paper crop for all six real visibility frames.
    replay_images = [image(f"benchmark/paper/figures/ldraw/clean-sequence-{i}.png") for i in range(1, 7)]
    bounds = []
    for im in replay_images:
        pixels = np.asarray(im).astype(int)
        # Background difference only chooses a paper frame, never an occlusion metric.
        ys, xs = np.where(np.max(abs(pixels - pixels[0, 0]), axis=2) > 20)
        bounds.append((int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())))
    box = (min(b[0] for b in bounds)-70, min(b[1] for b in bounds)-70,
           max(b[2] for b in bounds)+70, max(b[3] for b in bounds)+70)
    fig, axs = plt.subplots(2, 3, figsize=(7, 3.7))
    fig.subplots_adjust(left=.01, right=.99, bottom=.025, top=.95, wspace=.03, hspace=.13)
    for i, ax in enumerate(axs.flat, 1):
        path = f"benchmark/paper/figures/ldraw/clean-sequence-{i}.png"
        ax.imshow(image(path, box))
        ax.axis("off"); ax.set_title(f"({chr(96+i)}) step-{i}", loc="left", fontsize=9, pad=2)
    savefig(fig, "given-order-replay"); plt.close(fig)

    # Figure 3: separate metrics, separate axes; never rank one against the other.
    priors = analysis["answerConcentration"]
    global_f = ["color", "interface", "graph-removal", "source-step", "evidence-limit", "source-sequence"]
    scoped_f = ["shape-match", "distance", "neighbors", "coverage", "restore-instance"]
    fig, axs = plt.subplots(1, 2, figsize=(7, 2.55))
    fig.subplots_adjust(left=.15, right=.965, bottom=.24, top=.84, wspace=.87)
    for ax, fs, color, title in zip(axs, [global_f, scoped_f], ["#246782", "#ad6c32"],
                                  ["(a) Global semantic answers", "(b) Source-scoped exact answers"]):
        values = [priors[f]["majorityShare"] * 100 for f in fs]
        bars = ax.barh(range(len(fs)), values, color=color, height=.6)
        ax.set_yticks(range(len(fs)), [names[f] for f in fs], fontsize=8)
        ax.invert_yaxis(); ax.set_title(title, fontsize=9, fontweight="bold", pad=12)
        ax.set_xlim(0, 115 if fs is global_f else 7)
        ax.set_xlabel("Most frequent answer (%)" if fs is global_f else "Repeated exact key (%)", fontsize=8)
        ax.spines[["top", "right"]].set_visible(False)
        ax.bar_label(bars, labels=[f"{v:.1f}" for v in values], fontsize=8, padding=3)
    savefig(fig, "answer-priors"); plt.close(fig)

    # Figure 4: full image context plus large details. Full/mask crop is pixel-identical.
    fig, axs = plt.subplots(2, 3, figsize=(7, 3.65), gridspec_kw={"height_ratios": [1, 1.55]})
    fig.subplots_adjust(left=.01, right=.99, top=.93, bottom=.045, wspace=.05, hspace=.12)
    boxes = {"full": (615, 390, 795, 570), "mask": (615, 390, 795, 570), "crop": (600, 365, 930, 695)}
    for j, mode in enumerate(["full", "mask", "crop"]):
        path = "public/" + example["images"][mode]["file"]
        axs[0, j].imshow(image(path))
        box = boxes[mode]; x, y, xx, yy = box
        axs[0, j].add_patch(Rectangle((x, y), xx-x, yy-y, fill=False, ec="#bd682e", lw=1.1))
        axs[0, j].set_title(f"({chr(97+j)}) {mode.title()}", loc="left", fontweight="bold", fontsize=10)
        axs[1, j].imshow(image(path, box))
        axs[1, j].set_xlabel("Same pixel window" if j < 2 else "Reframed operands", fontsize=8)
        for ax in axs[:, j]:
            ax.set_xticks([]); ax.set_yticks([])
            for sp in ax.spines.values():
                sp.set_color("#d3dbe0")
    savefig(fig, "full-mask-crop"); plt.close(fig)

    # Supplement: direct A/B image evidence, large enough for the original labels.
    fig, axs = plt.subplots(1, 2, figsize=(7, 3.1))
    fig.subplots_adjust(left=.01, right=.99, bottom=.12, top=.90, wspace=.04)
    for ax, mode, title in zip(axs, ["crop", "wrong"], ["(a) A: operand-only; gold C", "(b) B: wrong-image; gold A"]):
        ax.imshow(image("public/" + example["images"][mode]["file"], (580, 360, 930, 680)))
        ax.axis("off"); ax.set_title(title, fontsize=10, loc="left")
    savefig(fig, "worked-pair"); plt.close(fig)
    # Exact census values stored alongside vector chart for independent reuse.
    with (GEN / "priors.csv").open("w") as f:
        w = csv.writer(f); w.writerow(["family", "n", "majority_count", "share", "metric"])
        for family in global_f + scoped_f:
            p = priors[family]
            w.writerow([family, p["n"], p["majorityCount"], p["majorityShare"],
                        "global-semantic" if family in global_f else "source-scoped-exact-key"])
    save(PAPER / "asset-provenance.json", {
        "analysis_version": VERSION, "inputs": INPUTS, "paper_only_crops": DERIVATIVES,
        "outputs": {str(p.relative_to(PAPER)): sha(p) for d in [GEN, FIG] for p in sorted(d.glob("*"))},
        "figure_policy": "Real frozen LDraw pixels and vector annotations. No modified model inputs."})
    print(json.dumps({"status": "passed", "macros": len(macros), "figures": 5,
                      "question_dossiers": len(tasks), "inputs": len(INPUTS)}))


if __name__ == "__main__":
    main()
