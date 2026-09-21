#!/usr/bin/env python3
"""Generate v2-only publication data, real render derivatives and review locks."""
import argparse
import csv
import hashlib
import json
import shutil
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "benchmark/ldraw-v2"
PAPER = ROOT / "benchmark/paper"
SITE = ROOT / "public/benchmark/ldraw-v2"
FIG = PAPER / "figures-v2"
TABLE = PAPER / "tables-v2"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tex(value):
    return "".join({"&": r"\&", "%": r"\%", "_": r"\_", "#": r"\#", "$": r"\$",
                    "{": r"\{", "}": r"\}", "\\": r"\textbackslash{}",
                    "^": r"\textasciicircum{}", "~": r"\textasciitilde{}"}.get(c, c) for c in str(value))


def table(headers, rows, spec=None):
    spec = spec or "X" + "r" * (len(headers) - 1)
    return (r"\begin{tabularx}{\linewidth}{" + spec + "}\n\\toprule\n" +
            " & ".join(headers) + r"\\\midrule" + "\n" +
            "\n".join(" & ".join(map(tex, row)) + r"\\" for row in rows) +
            "\n\\bottomrule\n\\end{tabularx}\n")


def main():
    from PIL import Image
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    FIG.mkdir(exist_ok=True)
    TABLE.mkdir(exist_ok=True)
    inputs = {}

    def read(path):
        inputs[str(path.relative_to(ROOT))] = sha(path)
        return json.loads(path.read_text())

    catalog = read(DATA / "catalog.json")
    bundles = {m["id"]: read(SITE / f"models/{m['id']}.json") for m in catalog}
    publics = {m["id"]: read(SITE / f"inputs/{m['id']}.json") for m in catalog}
    tasks = [t for b in bundles.values() for t in b["tasks"]]
    analysis = read(DATA / "descriptive-analysis/analysis.json")
    contracts = read(DATA / "task-contracts.json")["contracts"]
    audit = {t["id"]: t for t in read(DATA / "task-audit.json")["tasks"]}
    sources = read(DATA / "source-audit.json")["sources"]
    plan = read(PAPER / "ldraw-v2-experiments.json")
    queue = read(SITE / "human-review-queue.json")
    pairs = read(SITE / "physical-review-queue.json")["pairs"]
    queue_ids = {t["taskId"] for t in queue["items"]}
    names = {c["family"]: c["name"] for c in contracts}
    formats = Counter(t["format"] for t in tasks)
    summary = {"version": "brickatlas-ldraw-2", "sources": len(catalog),
               "parts": sum(m["parts"] for m in catalog), "tasks": len(tasks),
               "formats": dict(formats), "families": dict(Counter(t["family"] for t in tasks)),
               "modalities": dict(Counter(t["modality"] for t in tasks)),
               "layers": dict(Counter(t["layer"] for t in tasks)),
               "conditions": {c["id"]: c["n"] for c in plan["conditions"]},
               "humanQueue": len(queue_ids), "physicalQueue": len(pairs),
               "modelResults": None, "humanResults": None}
    choices = [t for t in tasks if t["format"] == "single-choice"]
    summary["alwaysA"] = sum(t["answer"]["choiceId"] == "A" for t in choices) / len(choices)
    summary["uniformExpected"] = sum(1 / len(t["options"]) for t in choices) / len(choices)
    (TABLE / "constants.tex").write_text(
        "\n".join(r"\newcommand{\%s}{%s}" % (k, v) for k, v in {
            "VTwoSources": len(catalog), "VTwoParts": f"{summary['parts']:,}",
            "VTwoTasks": len(tasks), "VTwoPairs": len(pairs),
            "VTwoAlwaysA": f"{100*summary['alwaysA']:.2f}",
            "VTwoUniform": f"{100*summary['uniformExpected']:.2f}"}.items()) + "\n")
    (TABLE / "bands.tex").write_text(table(["Band", "Sources", "V", "S", "G", "E", "Total"],
        [[b, sum(m["difficulty"] == b for m in catalog), *v.values(), sum(v.values())]
         for b, v in analysis["bandModality"].items()]))
    operation = {
        "color": ("Identify color", "Numbered image", "Request whitelist"),
        "shape-match": ("Match source type", "Numbered image", "No reference order"),
        "distance": ("Euclidean minimum", "Centers (mm)", "No source path"),
        "interface": ("Read family", "Connector record", "Fixed five options"),
        "neighbors": ("One-hop exact set", "Local edges", "No reference order"),
        "graph-removal": ("Delete; count components", "Nodes and local edges", "Integer output"),
        "coverage": ("Read support flag", "Coverage rows", "Minimal row fields"),
        "evidence-limit": ("Fixed scope response", "Available evidence", "Report fixed prior"),
        "source-step": ("First index lookup", "Author-step rows", "Legal balanced ranks"),
        "source-sequence": ("Follow fixed program", "Facts and actions", "Report fixed prior"),
        "restore-instance": ("Restore visibility", "Facts and actions", "Remove redundancy")}
    rows = []
    mod = {"visual": "V", "source-data": "S", "connector-graph": "G", "scene-edit": "E"}
    layer = {"atomic": "A", "metacognitive": "M", "procedural": "P", "graph-internal": "GI"}
    for c in contracts:
        marker = r"$^\dagger$" if c["constantAnswer"] else r"$^\ddagger$" if c["marker"] == "control" else ""
        rows.append(" & ".join([tex(c["name"]) + marker, str(c["n"]), layer[c["layer"]], mod[c["modality"]],
                               tex(c["classification"]), *map(tex, operation[c["family"]])]) + r"\\")
    (TABLE / "operators.tex").write_text(
        r"\begin{tabularx}{\linewidth}{lrrlXXXX}" + "\n\\toprule\n" +
        r"Family & $N$ & Layer & Input & Measurement & Direct operation & Necessary input & Shortcut control\\\midrule" +
        "\n" + "\n".join(rows) + "\n\\bottomrule\n\\end{tabularx}\n")
    # Every result field is read from the plan and rendered blank, never as zero.
    null_count = 0
    for t in plan["tables"]:
        rows = []
        for r in t["rows"]:
            assert all(v is None for v in r["results"].values())
            null_count += len(r["results"])
            rows.append([*r["condition"], *["" for _ in t["metrics"]]])
        specs = "X" * len(t["descriptors"]) + "r" * len(t["metrics"])
        (TABLE / f"plan-{t['id']}.tex").write_text(table(
            [tex(h) for h in t["descriptors"] + t["metrics"]], rows, specs))
    (TABLE / "conditions.tex").write_text(table(["Condition", "$N$", "Exact success"],
        [[c["id"], c["n"], ""] for c in plan["conditions"]], "Xrr"))
    (TABLE / "paired.tex").write_text(table(["A", "B", "$N$", r"$\Delta$ macro", r"$\Delta$ micro"],
        [[c["a"], c["b"], len(c["taskIds"]), "", ""] for c in plan["pairedComparisons"]], "XXrrr"))
    adapters = []
    for p in sorted((ROOT / "benchmark/suite/ldraw-v2/model-adapters").glob("*.json")):
        a = read(p)
        adapters.append(a)
    (TABLE / "adapters.tex").write_text(table(["Config", "Exact model ID", "Revision"],
        [[a.get("id", a.get("family", "")), a["modelId"], a.get("revision") or a.get("apiRevision") or "Freeze before live use"]
         for a in adapters], "XXX"))

    # New copies/derivatives only. These are actual LDraw captures, not generated art.
    renders = []
    def copy_render(source, name):
        target = FIG / name
        shutil.copyfile(source, target)
        renders.append({"source": str(source.relative_to(ROOT)), "sourceSha256": sha(source),
                        "file": str(target.relative_to(PAPER)), "sha256": sha(target)})
    oldfig = PAPER / "figures/ldraw"
    copy_render(oldfig / "teaser.png", "sources.png")
    for m in catalog:
        copy_render(oldfig / f"print/{m['id']}-iso.jpg", f"{m['id']}-iso.jpg")
    for s in [*[f"sequence-{i}" for i in range(1, 7)], "restore-before", "restore-after", "restore-invalid"]:
        copy_render(oldfig / f"print/clean-{s}.jpg", f"{s}.jpg")
    # A full/mask/crop plate preserves pixels and camera relationships.
    example = "ld2-omr-42004-shape-match-1"
    for mode in ["full", "mask", "crop"]:
        copy_render(SITE / f"inputs/views-{mode}/{example}.png", f"paired-{mode}.png")

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "pdf.fonttype": 42, "svg.fonttype": "none"})
    priors = analysis["answerConcentration"]
    source_scoped = {"shape-match", "distance", "neighbors", "coverage", "restore-instance"}
    fig, ax = plt.subplots(figsize=(9, 3.7), layout="constrained")
    family_ids = [c["family"] for c in contracts]
    bars = ax.barh(range(len(family_ids)), [priors[f]["majorityShare"] * 100 for f in family_ids],
                   color=["#c78245" if f in source_scoped else "#236887" for f in family_ids])
    ax.set_yticks(range(len(family_ids)), [names[f] for f in family_ids])
    ax.invert_yaxis()
    ax.set(xlim=(0, 113), xlabel="In-corpus semantic majority share (%)")
    ax.spines[["top", "right"]].set_visible(False)
    ax.bar_label(bars, labels=[f"{priors[f]['majorityShare']*100:.1f}" for f in family_ids], padding=4, fontsize=9)
    fig.savefig(FIG / "answer-concentration.pdf", metadata={"CreationDate": None})
    fig.savefig(FIG / "answer-concentration.png", dpi=220)
    plt.close(fig)
    with (TABLE / "answer-concentration.csv").open("w") as f:
        w = csv.writer(f); w.writerow(["family", "n", "majority_count", "majority_share", "source_scoped"])
        for k in family_ids:
            r = priors[k]; w.writerow([k, r["n"], r["majorityCount"], r["majorityShare"], k in source_scoped])
    # Detailed contracts in the supplement use the same generated JSON as Phase 2.
    details = []
    for c in contracts:
        details += [r"\subsection{" + tex(c["name"]) + "}",
                    tex(f"{c['n']} items; {c['modality']}; {c['layer']}; {c['format']}."),
                    r"\paragraph{Public input.}" + tex(c["publicInput"]),
                    r"\paragraph{Operation and scoring.}" + tex(c["operation"] + " " + c["scoring"]),
                    r"\paragraph{Interpretation.}" + tex(c["constructValidity"]),
                    r"\paragraph{Control.}" + tex(c["knownShortcuts"])]
    (TABLE / "contracts.tex").write_text("\n".join(details) + "\n")
    # Complete source/question index with exact options and answers; long raw
    # inputs remain available in the hash-bound public files.
    dossiers = []
    for m in catalog:
        b = bundles[m["id"]]
        s = next(s for s in sources if s["id"] == m["id"])
        dossiers += [r"\clearpage\section{" + tex(f"{m['setNumber']}: {m['name']}") + "}",
            tex(f"{m['parts']} source instances; {m['tasks']} tasks; {m['difficulty']} size band. "
                f"{s['partTypes']} type strings; {s['colors']} color codes; "
                f"{s['unsupportedInstances']} unsupported instances; {m['intersectionCandidates']} intersection candidates. "
                f"{m['sourceSteps']} expanded author steps. Independent reparse: passed."),
            r"\begin{center}\includegraphics[width=.65\linewidth]{figures-v2/" + m["id"] + r"-iso.jpg}\end{center}",
            r"\paragraph{Attribution.}" + tex(m["author"] + ". " + m["license"] + ".") +
            r"\par\url{" + m["sourceUrl"] + "}",
            r"\paragraph{Source SHA256.}\path{" + m["sourceHash"] + "}",
            r"\paragraph{Connector records.}" + tex("; ".join(f"{k}: {v}" for k, v in s["connectorRecordsByFamily"].items())),
            r"\paragraph{Public input lock.}\path{" + sha(SITE / f"inputs/{m['id']}.json") + "}",
            r"\paragraph{Status.}Source preservation does not certify stability. "
            "Reference outputs below are internal review material. Full model inputs are the versioned public JSON and numbered PNGs.",
            r"\begin{enumerate}"]
        for t in b["tasks"]:
            a = audit[t["id"]]
            opts = "; ".join(f"{o['id']}: {o['label']}" for o in t.get("options", []))
            inp = publics[m["id"]]["tasks"][next(i for i, p in enumerate(publics[m["id"]]["tasks"]) if p["id"] == t["id"])]["input"]
            if t["modality"] == "visual":
                evidence = "Numbered PNG: " + t["visualInput"]["numberedView"] + "; structured input = {}."
            elif t["family"] in {"neighbors", "graph-removal"}:
                evidence = f"{len({tuple(sorted(e)) for e in inp['edges']})} unique undirected pairs"
                if "nodes" in inp:
                    evidence += f"; {len(inp['nodes'])} nodes"
            elif t["family"] == "source-step":
                evidence = f"{len(inp['steps'])} supplied author-step records; exact table in public JSON"
            elif t["format"] == "actions":
                evidence = f"{len(inp['actions'])} public actions; budget {inp['budget']}; " + json.dumps({k: inp[k] for k in ["initialFacts", "goalFacts", "absentFacts"]})
            else:
                evidence = json.dumps(inp, ensure_ascii=True)
            dossiers += [r"\item \textbf{" + tex(t["id"]) + "}. " + tex(t["promptEn"]),
                r"\par{\small " + tex(f"{t['family']}; {t['modality']}; {t['layer']}; {t['format']}.") +
                r"\par\textit{Operands:} " + tex(", ".join(p["label"] + " = " + p["id"] for p in a["operands"]) or "none") +
                r"\par\textit{Public evidence summary:} " + tex(evidence) +
                (r"\par\textit{Options:} " + tex(opts) if opts else "") +
                r"\par\textit{Reference output:} " + tex(json.dumps(t["answer"], ensure_ascii=True)) +
                r"\par\textit{Derivation:} " + tex(a["derivation"]) +
                r"\par\textit{Equivalence:} " + tex(a["equivalence"]) +
                r"\par\textit{Review:} " + ("pending required human review" if t["id"] in queue_ids else "machine checks passed; no human certification") + ".}"]
        dossiers.append(r"\end{enumerate}")
    (TABLE / "cases.tex").write_text("\n".join(dossiers) + "\n")

    # The feedback lock includes question content, source and review pixels.
    units = []
    for t in tasks:
        a = audit[t["id"]]
        image_hashes = {}
        if t.get("visualInput"):
            for mode in ["views", "views-full", "views-mask", "views-crop", "views-camera"]:
                p = SITE / f"inputs/{mode}/{t['id']}.png"
                image_hashes[mode] = sha(p)
        body = {"task": t, "images": image_hashes}
        content_hash = hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=True).encode()).hexdigest()
        units.append({"id": t["id"], "kind": "task", "sourceId": t["modelId"],
                      "sourceHash": a["sourceSha256"], "contentHash": content_hash,
                      "operands": a["operands"], "required": t["id"] in queue_ids,
                      "title": t["title"], "family": t["family"], "modality": t["modality"],
                      "reasons": next((r["reasons"] for r in queue["items"] if r["taskId"] == t["id"]), [])})
    for p in pairs:
        units.append({"id": p["id"], "kind": "pair", "sourceId": p["sourceId"],
                      "sourceHash": p["sourceSha256"], "operands": p["operands"], "required": True,
                      "contentHash": hashlib.sha256(json.dumps(p, sort_keys=True).encode()).hexdigest(),
                      "title": " / ".join(o["label"] for o in p["operands"]),
                      "reasons": ["unadjudicated-intersection"]})
    lock = hashlib.sha256(json.dumps(units, sort_keys=True).encode()).hexdigest()
    (SITE / "review-index.json").write_text(json.dumps({"version": "brickatlas-ldraw-2",
        "releaseHash": lock, "summary": summary, "units": units}, indent=2) + "\n")
    (SITE / "publication-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    outputs = {str(p.relative_to(ROOT)): sha(p) for d in [FIG, TABLE] for p in sorted(d.glob("*")) if p.is_file()}
    (DATA / "publication-manifest.json").write_text(json.dumps({
        "summary": summary, "inputs": inputs, "outputs": outputs, "renders": renders,
        "nullResultCells": null_count, "appendixTaskIds": [t["id"] for t in tasks],
        "reviewReleaseHash": lock, "generatorSha256": sha(Path(__file__))}, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    main()
