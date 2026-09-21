#!/usr/bin/env python3
"""Build code-derived paper assets and a separate searchable historical dossier."""
from collections import Counter, defaultdict
from pathlib import Path
import shutil

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from common import ROOT, DATA, PUBLIC, VERSION, DATASET, load, save, sha, frozen, original_tasks
from priors import gate
from roster import checked as verify_roster

PAPER = ROOT / "benchmark/paper/evidence-v3"
HERE = Path(__file__).parent
NAMES = {
    "node-count-lookup": "Node-count lookup",
    "edge-count-lookup": "Edge-count lookup",
    "degree-histogram-lookup": "Degree-histogram lookup",
    "anonymous-1wl-lookup": "Anonymous 1-WL lookup",
    "isolates-plus-one": "Isolates + one",
    "bfs": "BFS",
    "union-find": "Union-find",
}


def tex(value):
    return str(value).replace("_", r"\_").replace("&", r"\&").replace("%", r"\%")


def table(path, columns, headings, rows):
    body = [r"\begin{tabular}{" + columns + "}", r"\toprule",
            " & ".join(headings) + r"\\", r"\midrule"]
    body += [" & ".join(map(str, row)) + r"\\" for row in rows]
    body += [r"\bottomrule", r"\end{tabular}"]
    (PAPER / "generated" / path).write_text("\n".join(body) + "\n")


def figures(manifest, renders):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "pdf.fonttype": 42, "axes.titleweight": "bold"})
    obs = manifest["observations"]
    receipts = {r["observation_id"]: r for r in renders["images"]}
    provenance = []
    fig, axes = plt.subplots(2, 2, figsize=(9, 6.4))
    for row, (family, parent, crop) in enumerate([
        ("Color", "ld2-omr-42004-color-1", (350, 120, 960, 720)),
        ("Part-type", "ld2-omr-42004-shape-match-1", (580, 365, 925, 670)),
    ]):
        for col, arm in enumerate(["A", "B"]):
            o = next(o for o in obs if o["parent_task_id"] == parent and o["arm"] == arm)
            r = receipts[o["observation_id"]]
            im = Image.open(ROOT / r["file"])
            assert sha(ROOT / r["file"]) == r["sha256"]
            axes[row, col].imshow(im.crop(crop))
            axes[row, col].set_title(f"{family} {arm}  |  gold: {o['gold_semantics']}", fontsize=11)
            axes[row, col].axis("off")
            provenance.append({"figure": "paired-observations", "observation_id": o["observation_id"],
                               "file": r["file"], "sha256": r["sha256"], "paper_crop": crop,
                               "gold": o["gold"], "gold_semantics": o["gold_semantics"],
                               "paper_only_crop": True, "model_response": None})
    fig.subplots_adjust(left=.01, right=.99, top=.95, bottom=.01, wspace=.04, hspace=.17)
    fig.savefig(PAPER / "figures/paired-observations.pdf")
    fig.savefig(PAPER / "figures/paired-observations.png", dpi=220)
    plt.close(fig)
    # This control is shown with its complete native image, not a re-render.
    o = next(o for o in obs if o["parent_task_id"] == "ld2-omr-42004-shape-match-1"
             and o["role"] == "position-reference-control")
    r = receipts[o["observation_id"]]
    shutil.copyfile(ROOT / r["file"], PAPER / "figures/position-control.png")
    provenance.append({"figure": "position-control", "observation_id": o["observation_id"],
                       "file": r["file"], "sha256": r["sha256"], "paper_crop": None})
    # Reuse a source-preserving 3D replay with explicit publication provenance.
    replay = ROOT / "benchmark/paper/evidence-v1/figures/given-order-replay.pdf"
    shutil.copyfile(replay, PAPER / "figures/given-order-replay.pdf")
    provenance.append({"figure": "given-order-replay", "file": str(replay.relative_to(ROOT)),
                       "sha256": sha(replay), "role": "historical execution-control illustration"})
    save(PAPER / "figure-provenance.json", provenance)


def main():
    (PAPER / "generated").mkdir(parents=True, exist_ok=True)
    (PAPER / "figures").mkdir(exist_ok=True)
    PUBLIC.mkdir(parents=True, exist_ok=True)
    catalog = frozen("benchmark/ldraw-v2/catalog.json")
    tasks = original_tasks()
    registry = load(DATA / "family-registry.json")["families"]
    visual = load(DATA / "visual-manifest.json")
    graph = frozen("benchmark/ldraw-evidence-v2/graph-audit.json")
    renders = load(DATA / "renders.json")
    report = load(DATA / "reports/protocol-ready.json")
    priors = load(DATA / "answer-prior-audit.json")
    checked = gate()
    assert all(checked["families"][f]["transition_matrix"] == v["transition_matrix"]
               for f, v in priors["families"].items())
    roster = verify_roster()
    dependence = load(DATA / "source-dependence.json")
    counts = Counter(t["family"] for t in tasks.values())
    assert len(tasks) == 617 and len(visual["pairs"]) == 140
    assert not report["models"], "Use an explicit reviewed publication update for empirical results."
    roles = {"color": "Core visual", "shape-match": "Core visual",
             "neighbors": "Structural evidence", "graph-removal": "Structural evidence",
             "evidence-limit": "Constant control", "source-sequence": "Constant control"}
    table("families.tex", "@{}llr@{}", ["Family", "Historical role", "Items"],
          [(v["display_name"], roles.get(k, "Nonconstant control"), counts[k])
           for k, v in registry.items()])
    table("scale.tex", "@{}lrrr@{}", ["Source band", "Sources", "Parts", "Items"],
          [(band, sum(m["difficulty"] == band for m in catalog),
            f"{sum(m['parts'] for m in catalog if m['difficulty'] == band):,}",
            sum(m["tasks"] for m in catalog if m["difficulty"] == band))
           for band in ["D1", "D2", "D3", "D4"]])
    table("visual-inventory.tex", "@{}lrrr@{}", ["Family", "Pairs", "Sources", "QA final"],
          [(registry[k]["display_name"], v["pairs"], v["sources"], f"0/{2*v['pairs']}")
           for k, v in report["planned"].items()])
    table("marginals.tex", "@{}llrrrr@{}", ["Family", "Arm", "A", "B", "C", "D"],
          [(registry[f]["display_name"], arm.upper(),
            *[v["gold_marginals"][arm][c] for c in "ABCD"])
           for f, v in priors["families"].items() for arm in ["a", "b"]])
    for family, short in [("color", "color"), ("shape-match", "type")]:
        f = priors["families"][family]
        table(f"transitions-{short}.tex", "@{}lrrrr@{}", [r"$A\backslash B$", "A", "B", "C", "D"],
              [(a, *[f["transition_matrix"][a][b] for b in "ABCD"]) for a in "ABCD"])
    selected = ["fixed-A", "fixed-B", "fixed-C", "fixed-D",
                "oracle-A/first-alternative", "oracle-A/last-alternative",
                "oracle-A/cyclic-next", "oracle-A/cyclic-previous", "oracle-A/cyclic-two"]
    rule_names = {"first-alternative": "First alternative", "last-alternative": "Last alternative",
                  "cyclic-next": "Cyclic next", "cyclic-previous": "Cyclic previous",
                  "cyclic-two": "Cyclic two", "smallest-alternate-label": "Smallest alternate label",
                  "largest-alternate-label": "Largest alternate label",
                  "nearest-alternate-label-number": "Nearest label number",
                  "farthest-alternate-label-number": "Farthest label number",
                  "nearest-alternate-center": "Nearest source center",
                  "farthest-alternate-center": "Farthest source center",
                  "nearest-alternate-projection": "Nearest projected anchor",
                  "farthest-alternate-projection": "Farthest projected anchor"}
    pct = lambda x: f"{100*x:.2f}"
    table("priors-main.tex", "@{}lrrrr@{}",
          ["B predictor", r"\multicolumn{2}{c}{Color}", r"\multicolumn{2}{c}{Part-type}"],
          [("", "Micro", "Source", "Micro", "Source")] + [
              (k.replace("fixed-", "Fixed ") if k.startswith("fixed-")
               else rule_names[k.split("/")[1]] + r"$^\dagger$",
               *[pct(priors["families"][f]["baselines"][k]["metrics"]["NewAcc"][m])
                 for f in ["color", "shape-match"] for m in ["micro", "source_macro"]])
              for k in selected])
    table("shortcuts-type.tex", "@{}lrrl@{}", ["Oracle-A rule", "Micro", "Source", "Source 95\\% CI"],
          [(rule_names[k.split("/")[1]], pct(b["metrics"]["NewAcc"]["micro"]),
            pct(b["metrics"]["NewAcc"]["source_macro"]),
            "[" + ", ".join(pct(x) for x in b["metrics"]["NewAcc"]["source_macro_ci95"]) + "]")
           for k,b in priors["families"]["shape-match"]["baselines"].items()
           if k.startswith("oracle-A/")])
    table("roster.tex", "@{}lll@{}", ["Model", "Pinned revision", "Runs"],
          [(e["display_name"], r"\texttt{" + e["expected_served_model_revision"] + "}", "0/3")
           for e in roster["entries"]])
    groups = defaultdict(list)
    for row in dependence["rows"]:
        groups[row["primary_author"]].append(row["source_id"])
    table("authors.tex", "@{}ll@{}", ["Repeated primary author", "Source IDs"],
          [(tex(a), ", ".join(s.replace("omr-", "") for s in sorted(v)))
           for a,v in sorted(groups.items()) if len(v) > 1])
    table("overlap.tex", "@{}llrr@{}", ["Source A", "Source B", "Count J.", "Set J."],
          [(r["source_a"].replace("omr-", ""), r["source_b"].replace("omr-", ""),
            f"{r['part_multiset_weighted_jaccard']:.3f}", f"{r['part_type_set_jaccard']:.3f}")
           for r in dependence["inventory_pairs"][:5]])
    summary = graph["summary"]
    table("graph-main.tex", "@{}lrrrr@{}",
          ["Algorithm", r"\shortstack{Natural\\correct / 73}",
           r"\shortstack{Strong change\\Both / 12}",
           r"\shortstack{Degree-visible\\Both / 61}",
           r"\shortstack{Strong invariance\\Both / 12}"],
          [(name, round(graph["natural"]["metrics"][k]["correct"]["micro"] * 73),
            *[round(summary[role]["baselines"][k]["both"]["micro"] * summary[role]["pairs"])
              for role in ["strong-change", "degree-visible-control", "strong-invariance"]])
           for k, name in NAMES.items()])
    table("graph-natural.tex", "@{}lrr@{}", ["Algorithm", "Source macro", "95\\% interval"],
          [(name, f"{100*graph['natural']['metrics'][k]['correct']['source_macro']:.2f}",
            "[" + ", ".join(f"{100*v:.2f}" for v in
                            graph["natural"]["metrics"][k]["correct"]["source_macro_ci95"]) + "]")
           for k, name in NAMES.items()])
    strong = [p for p in graph["pairs"] if p["role"] == "strong-change"]
    table("strong-pairs.tex", "@{}lrrr@{}", ["Parent task", r"$y_A$", r"$y_B$", "Isolates+1 Both"],
          [(tex(p["parent_task_id"]), p["a_gold"], p["b_gold"],
            p["baselines"]["isolates-plus-one"]["both"]) for p in sorted(strong, key=lambda p:p["parent_task_id"])])
    table("graph-invariance.tex", "@{}lrr@{}", ["Algorithm", "Strong / 12", "Degree-visible / 61"],
          [(name, *[round(summary[role]["baselines"][k]["both"]["micro"] * summary[role]["pairs"])
                    for role in ["strong-invariance", "degree-visible-invariance"]])
           for k, name in NAMES.items()])
    hist = summary["strong-change"]["answer_histograms"]
    table("answer-balance.tex", "@{}lrrrr@{}", ["Stored arm", "Gold 1", "Gold 2", "Gold 3", "Gold 4"],
          [(arm.upper(), *[hist[arm].get(str(i), 0) for i in range(1, 5)]) for arm in ["a", "b"]])
    table("sources.tex", "@{}llrrrr@{}", ["Source", "Name", "Band", "Parts", "Color", "Part-type"],
          [(tex(m["id"]), tex(m["name"]), m["difficulty"], m["parts"],
            sum(p["source_id"] == m["id"] and p["family"] == "color" for p in visual["pairs"]),
            sum(p["source_id"] == m["id"] and p["family"] == "shape-match" for p in visual["pairs"]))
           for m in catalog])
    numbers = {"Sources": len(catalog), "Parts": f"{sum(m['parts'] for m in catalog):,}",
               "Tasks": len(tasks), "Color": counts["color"], "Type": counts["shape-match"]}
    (PAPER / "generated/numbers.tex").write_text("\n".join(
        "\\newcommand{\\Ev" + k + "}{" + str(v) + "}" for k, v in numbers.items()) + "\n")
    for filename in ["cvpr.sty", "ieeenat_fullname.bst"]:
        shutil.copyfile(ROOT / "benchmark/paper" / filename, PAPER / filename)
    (PAPER / "references.bib").write_text(
        (ROOT / "benchmark/paper/evidence-v1/references.bib").read_text()
        + "\n" + (PAPER / "additions.bib").read_text())
    figures(visual, renders)
    by_parent = defaultdict(list)
    obs = {o["observation_id"]: o for o in visual["observations"]}
    index = {o["observation_id"]: o for o in load(DATA / "observation-index.json")["observations"]}
    paired = []
    for p in visual["pairs"]:
        by_parent[p["parent_task_id"]].append(p["pair_id"])
        row = {**p, "display_name": registry[p["family"]]["display_name"], "observations": []}
        for o in [obs[p["a"]], obs[p["b"]]] + [
                o for o in obs.values() if o["parent_task_id"] == p["parent_task_id"]
                and o["role"] == "position-reference-control"]:
            row["observations"].append({
                **{k:o[k] for k in ["observation_id", "arm", "role", "payload", "gold", "gold_semantics"]},
                "image": "/" + str((ROOT / receipts_path(renders, o["observation_id"])).relative_to(ROOT / "public")),
                "wire_observation_sha256": index[o["observation_id"]]["wire_observation_sha256"],
                "qa_final": "pending", "model_response": None})
        paired.append(row)
    # Preserve the complete old dossier byte-for-byte; update links in a separate overlay.
    historical = ROOT / "public/benchmark/evidence-v2/dossiers.json"
    dossiers = frozen(str(historical.relative_to(ROOT)))["items"]
    shutil.copyfile(historical, PUBLIC / "dossiers.json")
    save(PUBLIC / "parent-mapping.json", {
        "analysis_version": VERSION, "historical_dossier_sha256": sha(historical),
        "historical_record_policy": "Original records and their old links remain frozen; use this overlay for current pairs.",
        "pairs_by_parent": dict(by_parent)})
    save(PUBLIC / "paired-observations.json", {
        "artifact_role": "evaluator-inspection-not-blind-review", "dataset": DATASET,
        "system_prompt": visual["system_prompt"], "pairs": paired})
    save(PUBLIC / "release-summary.json", {
        "analysis_version": VERSION, "dataset": DATASET, "historical_items": len(dossiers),
        "primary_pairs": len(paired), "sources": len(catalog), "native_observations": len(obs),
        "human_primary_final": report["qa"]["primary_final"], "human_primary_total": 280,
        "real_model_runs": len(report["models"]), "qa_comparable_pairs": 0,
        "roster_completeness": report["roster_completeness"],
        "roster": [{"display_name": e["display_name"], "revision": e["expected_served_model_revision"],
                    "provider": e["provider"], "planned_runs": len(e["planned_runs"]), "completed_runs": 0}
                   for e in roster["entries"]],
        "answer_priors": {f: {"gold_marginals": v["gold_marginals"],
                             "transition_matrix": v["transition_matrix"],
                             "rules": {k: {m: b["metrics"]["NewAcc"][m] for m in ["micro", "source_macro"]}
                                       for k,b in v["baselines"].items()}}
                          for f,v in priors["families"].items()},
        "author_groups": dependence["primary_author_groups"],
        "contributor_groups": dependence["contributor_connected_groups"],
        "graph": {k: {"pairs": v["pairs"], "sources": v["sources"],
                      "baselines": {b: m["both"]["micro"] for b,m in v["baselines"].items()}}
                  for k,v in summary.items()}})
    for filename in ["family-registry.json", "REVISION-CONTRACT.md", "QA-AND-RUN.md",
                     "stimulus-validation.json", "answer-prior-audit.json", "historical-prior-audit.json",
                     "assignment-contract.json", "part-type-assignment.json", "source-dependence.json",
                     "model-roster.json", "roster-lock.json", "model-run-index.json",
                     "wire-audit-validation.json", "retained-components.json"]:
        shutil.copyfile(DATA / filename, PUBLIC / filename)
    for filename in ["graph-audit.json", "graph-partitions.json"]:
        shutil.copyfile(ROOT / "benchmark/ldraw-evidence-v2" / filename, PUBLIC / filename)
    shutil.copytree(DATA / "adapters", PUBLIC / "adapters", dirs_exist_ok=True)
    shutil.copyfile(DATA / "reports/protocol-ready.json", PUBLIC / "protocol-ready.json")
    (PUBLIC / "review-packages").mkdir(exist_ok=True)
    for n in range(1, 7):
        shutil.copyfile(DATA / f"qa/initial/reviewer-{n}.zip", PUBLIC / f"review-packages/reviewer-{n}.zip")
    if (HERE / "delivery.html").exists():
        # The inherited visual template uses version tokens only for local delivery links.
        html = (HERE / "delivery.html").read_text().replace("evidence-v2", "evidence-v3").replace("display-v2", "display-v3")
        (ROOT / "evidence-v3.html").write_text(html)
        (PUBLIC / "index.html").write_text(html)
    save(PAPER / "publication-provenance.json", {
        "analysis_version": VERSION, "evidence_kind": "algorithmic-and-stimulus-audits-only",
        "inputs": {str(p.relative_to(ROOT)): sha(p) for p in [
            ROOT / "benchmark/ldraw-evidence-v2/graph-audit.json", DATA / "visual-manifest.json", DATA / "renders.json",
            DATA / "reports/protocol-ready.json", DATA / "family-registry.json",
            DATA / "answer-prior-audit.json", DATA / "part-type-assignment.json",
            DATA / "source-dependence.json", DATA / "model-roster.json",
            ROOT / "benchmark/ldraw-v2/catalog.json"]},
        "counts": numbers, "dossiers": len(dossiers), "real_model_results": 0,
        "figures": "figure-provenance.json"})
    print({"status": "generated", "dossiers": len(dossiers), "pairs": len(paired),
           "figures": 3, "model_results": 0})


def receipts_path(renders, observation_id):
    return next(r["file"] for r in renders["images"] if r["observation_id"] == observation_id)


if __name__ == "__main__":
    main()
