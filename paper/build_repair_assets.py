#!/usr/bin/env python3
"""Compose the paper from visual-repair-v1 inputs, certificates and reports."""
import collections
import json
from pathlib import Path
import textwrap

from PIL import Image
import build_figures as art
from build_tables import table, tex

HERE, ROOT = art.HERE, art.ROOT
DATA = ROOT / "benchmark/visual-repair-v1"
EXAMPLE = "construction-2abc703c9a7fd78609b7"


def save_tex(name, value):
    (HERE / "generated" / name).write_text(value)


def canonical_answer(answer):
    return {**answer, "solutions": sorted([
        {"restored": sorted(s["restored"]), "component_sizes": sorted(s["component_sizes"], reverse=True)}
        for s in answer["solutions"]], key=lambda s: s["restored"])}


def build():
    summary = art.load(DATA / "summary.json")
    tasks = art.load(DATA / "public.json")["tasks"]
    gold = {row["id"]: canonical_answer(row["answer"]) for row in art.load(DATA / "gold.json")["tasks"]}
    captures = art.load(DATA / "captures.json")
    frames = {row["file"]: row for row in captures["frames"]}
    study = art.load(DATA / "study-manifest.json")
    art.PROVENANCE.clear()
    art.EXAMPLES.clear()
    subset = [t for t in tasks if t["construction_id"] == EXAMPLE and t["replicate"] == 0]
    assert len(subset) == 6 and {t["split"] for t in subset} == {"dev"}
    chosen = {(t["visual_arm"], t["structural_arm"]): t for t in subset}
    task = chosen["anchor", "fault_0"]
    answer = gold[task["id"]]
    data = task["input"]
    refs = [art.record(DATA / name) for name in ["public.json", "gold.json", "summary.json",
                                                "sampling-ledger.json", "dependency-audit.json", "study-manifest.json"]]
    refs += [art.record(Path(__file__)), art.record(DATA / "captures.json")]

    def native(t):
        path = ROOT / t["image"]
        row = frames[t["image"]]
        assert art.sha(path) == row["sha256"] and row["source_poses_preserved"]
        return Image.open(path).convert("RGB"), art.record(path, capture=row, task_id=t["id"])

    # Exact input packet from the study writer (not the metadata-rich index).
    observation = next(o for o in study["observations"]
                       if o["task_id"] == task["id"] and o["condition"] == "multimodal")
    path = ROOT / observation["packet"]["path"]
    assert art.sha(path) == observation["packet"]["sha256"]
    packet = art.load(path)
    refs.append(art.record(path))
    question = packet["question"]
    save_tex("repair-example-question.tex", tex(question) + "\n")

    fig = art.canvas(7, 4.65)
    art.text(fig, .012, .985, "Visual binding + minimum repair  |  actual development construction", 8.7,
             weight="bold", color=art.BLUE)
    art.text(fig, .012, .927,
             "Match the reference, bind its current graph ID, then return every minimum restoration set.", 8)
    im, rec = native(task)
    art.image(fig, [.005, .395, .66, .50], im)
    context = ROOT / f"public/benchmark/visual-repair-v1/provenance/{EXAMPLE}.png"
    context_im = Image.open(context).convert("RGB")
    box = art.content_box([context_im])
    art.image(fig, [.695, .49, .295, .36], context_im.crop(box))
    art.text(fig, .695, .875, "Source context (not input)", 7.3, color=art.MUTED)
    art.text(fig, .695, .45, f"{len(data['graph']['nodes'])} vertices / {len(data['graph']['edges'])} edges\n"
             f"{len(data['missing'])} unavailable vertices\nBudget: {data['budget']}", 7.4)
    art.text(fig, .015, .38, "Structural input", 8, weight="bold", color=art.BLUE)
    art.text(fig, .015, .334, "Fixed terminals: " + ", ".join(data["fixed_terminals"]) + "\n"
             + "Unavailable: " + ", ".join(data["missing"]), 7.1)
    edge_lines = textwrap.wrap("Edges: " + "; ".join(f"{a}–{b}" for a, b in data["graph"]["edges"]), 121)
    art.text(fig, .015, .265, "\n".join(edge_lines), 6.8)
    art.text(fig, .015, .122,
             f"GT: terminal {answer['bound_terminal']}; minimum cost {answer['minimum_cost']}; "
             + f"budget sufficient: {str(answer['budget_sufficient']).lower()}.", 8,
             color=art.GREEN, weight="bold")
    solutions = ["{" + ", ".join(s["restored"]) + "}" for s in answer["solutions"]]
    art.text(fig, .015, .077, "All optimal sets: " + "  OR  ".join(solutions) + "\n"
             + "Component sizes for each optimum: " + str(answer["solutions"][0]["component_sizes"]), 7.3,
             color=art.GREEN)
    art.save(fig, "repair-task", refs + [rec, art.record(context, crop_xyxy=box)],
             version="visual-repair-v1", task=task, gt=answer,
             selection="Development example with multiple optima; selected without model performance.")

    fig = art.canvas(7, 4.0)
    art.text(fig, .012, .985, "Visual change, visual preservation and a separate fault exchange", 8.7,
             weight="bold", color=art.BLUE)
    image_refs = []
    for col, arm in enumerate(["anchor", "changing", "preserving"]):
        t = chosen[arm, "fault_0"]
        im, rec = native(t); image_refs.append(rec)
        x = .012 + col * .333
        art.text(fig, x, .902, ["Anchor", "Relevant label swap", "Distractor label swap"][col], 7.5, weight="bold")
        art.image(fig, [x, .505, .316, .365], im)
        art.text(fig, x, .49, f"Bound ID: {gold[t['id']]['bound_terminal']}", 7.6, color=art.GREEN)
    old, new = chosen["anchor", "fault_0"]["input"], chosen["anchor", "fault_1"]["input"]
    art.text(fig, .012, .404, "Fault exchange: remove " + ", ".join(sorted(set(new["missing"]) - set(old["missing"])))
             + "; reinstate " + ", ".join(sorted(set(old["missing"]) - set(new["missing"])))
             + ".  Original edges stay fixed.", 7.4)
    for row, fault in enumerate(["fault_0", "fault_1"]):
        y = .35 - row * .17
        art.text(fig, .012, y, ["Fault 0", "Fault 1"][row], 7.2, weight="bold")
        for col, arm in enumerate(["anchor", "changing", "preserving"]):
            t = chosen[arm, fault]; a = gold[t["id"]]
            art.text(fig, .117 + col * .298, y,
                     f"cost {a['minimum_cost']}; {len(a['solutions'])} optimum set(s)\n"
                     + ("same as anchor" if arm == "preserving" else
                        "\n".join("{" + ",".join(n[1:] for n in s["restored"]) + "}" for s in a["solutions"])),
                     6.7, color=art.GREEN)
    art.text(fig, .012, .035, "Solution IDs omit the common V prefix only in this compact diagram. Full JSON and both ID replicates are released.",
             6.7, color=art.MUTED)
    art.save(fig, "repair-factorial", refs + image_refs, version="visual-repair-v1",
             tasks=subset, answers={t["id"]: gold[t["id"]] for t in subset},
             selection="Same development construction as main example; no model outputs.")

    art.sources_figure(all_sources=True)
    blank_count = sum(len(row["results"]) for rows in art.load(HERE / "experiments.json")["tables"].values() for row in rows)
    macros = {"VRConstructions": summary["construction_count"], "VRSources": summary["source_count"],
              "VRGroups": summary["dependence_group_count"], "VRObservations": summary["observation_count"],
              "VRBlankCells": blank_count,
              "VRLowCost": sum(gold[t["id"]]["minimum_cost"] in (2, 3) for t in tasks),
              "VRSingleOptimum": sum(len(gold[t["id"]]["solutions"]) == 1 for t in tasks)}
    save_tex("repair-numbers.tex", "\n".join(r"\newcommand{\%s}{%s}" % item for item in macros.items()) + "\n")
    inventory = [
        ["Screened candidates", str(summary["candidate_count"])],
        ["Eligible / deduplicated", f"{summary['eligible_count']} / {summary['deduplicated_count']}"],
        ["Admitted constructions", str(summary["construction_count"])],
        ["Source / dependence groups", f"{summary['source_count']} / {summary['dependence_group_count']}"],
        ["Dev / held-out constructions", f"{summary['dev_constructions']} / {summary['heldout_constructions']}"],
        ["Dev / held-out groups", f"{summary['dev_groups']} / {summary['heldout_groups']}"],
        ["Repair observations", str(summary["observation_count"])],
        ["Vertices / edges (range)", " / ".join("--".join(map(str, summary[k])) for k in ["node_range", "edge_range"])],
        ["Optimal cost / set count", " / ".join("--".join(map(str, summary[k])) for k in ["minimum_cost_range", "optimum_count_range"])],
    ]
    save_tex("repair-inventory.tex", table(["Unit", "Count"], inventory))
    source_rows = []
    for source in sorted({t["source_id"] for t in tasks}):
        rows = [t for t in tasks if t["source_id"] == source]
        source_rows.append([tex(source), rows[0]["split"], rows[0]["dependence_group"].replace("group-", ""),
                            str(len({r["construction_id"] for r in rows})), str(len(rows))])
    save_tex("repair-sources.tex", table(["Source", "Split", "Dependence group", "Constructions", "Observations"],
                                         source_rows, "lllrr"))
    details = [r"\begin{table*}[t]", r"\centering\small",
               r"\caption{Exact complete adjacency of the main-paper development example. Source edges are undirected.}",
               table(["Vertex", "Neighbors"], [[n, ", ".join(sorted(b if a == n else a
                      for a, b in data["graph"]["edges"] if n in (a, b)))] for n in sorted(data["graph"]["nodes"])], "ll"),
               r"\end{table*}", r"\begin{quote}\small\ttfamily",
               *[tex(line).replace("{", r"\{").replace("}", r"\}") + r"\\" for line in json.dumps(answer, indent=2).splitlines()],
               r"\end{quote}"]
    save_tex("repair-example-details.tex", "\n".join(details) + "\n")
    baseline = art.load(DATA / "baseline-report.json")
    refs.append(art.record(DATA / "baseline-report.json"))
    pixel = next(row for row in baseline["configurations"] if row["id"] == "silhouette-repair")["heldout"]["repair_exact"]
    macros.update({"VRPixelMicro": f"{100 * pixel['micro']:.1f}",
                   "VRPixelMacro": f"{100 * pixel['group_macro']:.1f}",
                   "VRHeldoutN": pixel["n"], "VRHeldoutGroups": pixel["groups"]})
    save_tex("repair-numbers.tex", "\n".join(r"\newcommand{\%s}{%s}" % item for item in macros.items()) + "\n")
    baseline_rows = []
    def percent(value):
        return "--" if value is None else f"{100 * value:.1f}"
    for row in baseline["configurations"]:
        stats = row["heldout"]
        baseline_rows.append([tex(row["id"]), tex(row["condition"]),
                              percent(stats["binding_accuracy"]["group_macro"]),
                              percent(stats["repair_exact"]["group_macro"] if stats["repair_exact"] else None),
                              percent(stats["factorial_all_correct"]["group_macro"])])
    save_tex("repair-baselines.tex", table(["Algorithm", "Condition", "Bind", "Exact", "All-six"], baseline_rows, "llrrr"))
    save_tex("repair-baseline-interpretation.tex", tex(baseline["interpretation"]) + "\n")
    provenance = {"version": "visual-repair-v1", "builder": art.record(Path(__file__)),
                  "source_files": refs, "native_packet": packet, "figures": art.PROVENANCE,
                  "example": task["id"], "construction_id": EXAMPLE, "gt": answer,
                  "model_or_human_results": None}
    (HERE / "repair-figure-provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
    print(f"Built exact visual-repair figures and counts: {summary['construction_count']} constructions.")


if __name__ == "__main__":
    build()
