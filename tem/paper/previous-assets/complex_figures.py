"""Scientific figures for CX1--CX3, with actual geometry and algorithmic GT."""
import json
from pathlib import Path
import textwrap

import numpy as np
from PIL import Image
from matplotlib.patches import FancyArrowPatch


def build(api):
    root, here = api.ROOT, api.HERE
    data_path = root / "benchmark/complex-examples-v1/public.json"
    gold_path = root / "benchmark/complex-examples-v1/gold.json"
    data, gold = api.load(data_path), api.load(gold_path)
    cases = {r["id"]: r for r in data["cases"]}
    answers = {r["id"]: r for r in gold["cases"]}
    captures_path = here / "figures/complex-raw/captures.json"
    captures = api.load(captures_path)
    capture = {r["id"]: r for r in captures["frames"]}
    records = [api.record(data_path), api.record(gold_path), api.record(captures_path),
               api.record(Path(__file__))]

    def pixels(name):
        row = capture[name]
        path = root / row["file"]
        assert api.sha(path) == row["sha256"] and row["sourcePosesPreserved"]
        im = Image.open(path).convert("RGB")
        box = api.content_box([im])
        return im.crop(box), api.record(path, capture_id=name, metadata=row, crop_xyxy=box)

    def write_tex(name, lines):
        (here / "generated" / name).write_text("\n".join(lines) + "\n")

    # CX1 contracts each surviving component, retaining every edge to each
    # missing candidate. The contraction is an exact graph simplification.
    cx1, gt1 = cases["CX1"], answers["CX1"]
    graph = cx1["input"]["graph"]
    groups = gt1["initial_components"]
    labels = [f"C{i+1}" for i in range(len(groups))]
    component = {n: label for label, group in zip(labels, groups) for n in group}
    missing = cx1["input"]["missing"]
    contracted = sorted({tuple(sorted([component.get(a, a), component.get(b, b)]))
                         for a, b in graph["edges"] if component.get(a, a) != component.get(b, b)})
    positions = {"C1": (.12, .60), "C2": (.57, .86), "C3": (.53, .18), "C4": (.88, .41), "C5": (.28, .92),
                 "B0150": (.02, .20), "B0160": (.37, .71), "B0164": (.22, .83),
                 "B0165": (.02, .95), "B0167": (.48, .97), "B0173": (.38, .40),
                 "B0175": (.68, .53), "B0177": (.88, .68)}
    fig = api.canvas(7, 4.5)
    api.text(fig, .015, .985, "CX1  |  Multi-fault minimum repair  |  OMR 42004", 9, weight="bold", color=api.BLUE)
    api.text(fig, .015, .91, "Restore the fewest of 8 missing vertices to reconnect B0158, B0171, B0179 and B0180.\n"
             "Every restore reinstates the original incident edges. Is a budget of 2 sufficient?", 8)
    im, rec = pixels("backhoe-detail")
    api.image(fig, [.005, .22, .42, .535], im)
    api.text(fig, .02, .78, "Actual 36-part source subassembly", 7.3, color=api.MUTED)
    ax = fig.add_axes([.45, .23, .535, .56])
    ax.set_xlim(-.08, 1.0); ax.set_ylim(.03, 1.07); ax.axis("off")
    for a, b in contracted:
        ax.plot([positions[a][0], positions[b][0]], [positions[a][1], positions[b][1]],
                color="#acbbc8", linewidth=1.4, zorder=1)
    for node, (x, y) in positions.items():
        is_component = node in labels
        members = groups[labels.index(node)] if is_component else []
        terminal = next((n for n in members if n in cx1["input"]["terminals"]), None)
        body = (f"{node}: {len(members)} " + ("part" if len(members) == 1 else "parts")
                + (f"\n{terminal}" if terminal else "")) if is_component else node
        ax.text(x, y, body, ha="center", va="center", fontsize=7,
                bbox={"boxstyle": "round,pad=.32", "fc": "#e8f0f7" if is_component else "white",
                      "ec": api.BLUE if is_component else "#a25c38", "lw": 1.0}, zorder=2)
    api.text(fig, .45, .78, "Exact component contraction after faults", 7.3, color=api.MUTED)
    api.text(fig, .02, .205, "Missing: " + ", ".join(missing), 7.6)
    api.text(fig, .02, .145, "GT: {B0160, B0175, B0177}; minimum cost = 3; budget 2 is infeasible.", 8.5,
             color=api.GREEN, weight="bold")
    api.text(fig, .02, .087, "Initial component sizes: 18, 5, 2, 2, 1. After the minimum repair: one 31-vertex component.\n"
             "All 256 subsets are enumerated; none of the 37 subsets of size 0, 1 or 2 succeeds.", 7.5, color=api.MUTED)
    api.save(fig, "complex-repair", records + [rec], complex_case="CX1",
             meaning="Native source pose at left. Graph contraction at right models unavailable vertices, not physical extraction.",
             contracted_edges=contracted, component_membership=dict(zip(labels, groups)))

    # CX2: complete hypotheses and tests, followed by a derived adaptive tree.
    cx2, gt2 = cases["CX2"], answers["CX2"]
    fig = api.canvas(7, 2.65)
    api.text(fig, .015, .985, "CX2  |  Adaptive diagnosis under a query budget", 9, weight="bold", color=api.BLUE)
    api.text(fig, .015, .87, "Which three-vertex fault world holds? Query path connectivity; minimize the worst-case number of tests.", 7.8)
    api.text(fig, .015, .75, "Possible unavailable sets", 8, weight="bold")
    for i, row in enumerate(cx2["input"]["worlds"]):
        api.text(fig, .015, .65 - i * .09, f"{row['id']}: " + ", ".join(row["absent"]), 7.7)
    api.text(fig, .015, .26, "Each test costs 1. All tests start at B0158.", 7.5)
    api.text(fig, .015, .17, "Q1: reach B0171   Q2: reach B0179\nQ3: reach B0180", 7.5)
    ax = fig.add_axes([.51, .17, .47, .61])
    ax.set_xlim(-.05, 1.05); ax.set_ylim(-.1, 1.12); ax.axis("off")
    pos = {"Q3": (.5, 1), "Q1": (.2, .55), "Q2": (.8, .55),
           "W1": (.06, .05), "W2": (.36, .05), "W3": (.65, .05), "W4": (.96, .05)}
    for a, b, outcome in [("Q3", "Q1", "no"), ("Q3", "Q2", "yes"),
                           ("Q1", "W1", "no"), ("Q1", "W2", "yes"),
                           ("Q2", "W3", "no"), ("Q2", "W4", "yes")]:
        ax.add_patch(FancyArrowPatch(pos[a], pos[b], arrowstyle="-|>", mutation_scale=10, color="#90a4b5"))
        x, y = (np.array(pos[a]) + pos[b]) / 2
        ax.text(x, y, outcome, fontsize=7, ha="center", bbox={"fc":"white","ec":"none","pad":1})
    for n, xy in pos.items():
        ax.text(*xy, n, ha="center", va="center", fontsize=8.5, weight="bold",
                bbox={"boxstyle":"round,pad=.35","fc":"#e8f0f7" if n.startswith("Q") else "#e5f3ec","ec":"#6b879a"})
    api.text(fig, .51, .075, "GT: Q3 first; worst-case cost = 2. Budget 1 fails.", 7.7, color=api.GREEN, weight="bold")
    api.save(fig, "complex-diagnosis", records, complex_case="CX2",
             meaning="Policy computed from reachability in the actual 36-node source graph.",
             policy=gt2["answer"]["policy"], outcomes=gt2["outcomes"])

    # CX3 shows the actual two complete axle assemblies, followed by exact
    # origin/type constraints and the recovered proper rigid transform.
    cx3, gt3 = cases["CX3"], answers["CX3"]
    fig = api.canvas(7, 4.4)
    api.text(fig, .015, .985, "CX3  |  Typed correspondence + rigid pose recovery  |  OMR 42061", 9,
             weight="bold", color=api.BLUE)
    api.text(fig, .015, .91, "Match the four anchors by part type and geometry; recover q = R p + t with det(R) = +1.\n"
             "Maximum error: 0.05 mm. Predict the transformed origin and local x-axis of B0030.", 8)
    recs = []
    for col, name in enumerate(["axle-A", "axle-B"]):
        im, row = pixels(name); recs.append(row)
        x = .01 + col * .50
        api.text(fig, x + .02, .80, f"Subassembly {'A' if col == 0 else 'B'}: 12 parts, original pose", 7.7, weight="bold")
        api.image(fig, [x, .44, .48, .32], im)
        anchors = cx3["input"]["anchor_A" if col == 0 else "anchor_B"]
        api.text(fig, x + .02, .425, "ID       Type       Origin (x, y, z), mm", 7.5, weight="bold", family="monospace")
        for i, a in enumerate(anchors):
            xyz = ", ".join(f"{v:g}" for v in a["origin_mm"])
            api.text(fig, x + .02, .375 - i * .039, f"{a['id']}    {a['part_type']}    ({xyz})", 7.1, family="monospace")
    api.text(fig, .02, .212, "Probe B0030: origin (43.9924, 24.8, 120.4212) mm; x-axis (-0.99938684, 0, -0.03501355).", 7.1)
    api.text(fig, .02, .17, "GT: R = diag(-1, 1, -1),  t = (16, 0, 120) mm. Exactly 1 of 4 types-only assignments passes.", 8,
             color=api.GREEN, weight="bold")
    api.text(fig, .02, .11, "B0024→B0036; B0025→B0037; B0026→B0038; B0035→B0047.\n"
             "B0030 maps to (-27.9924, 24.8, -0.4212) mm; x-axis = (0.99938684, 0, 0.03501355).", 7.7,
             color=api.GREEN)
    api.save(fig, "complex-registration", records + recs, complex_case="CX3",
             meaning="Actual source meshes and poses; anchors are part origins in the supplied coordinates.",
             gt=gt3["answer"])

    # Supplement: every original adjacency is given explicitly, so graph
    # drawings and inspection views are not needed to infer hidden edges.
    lines = [r"\begin{tabular}{@{}llll@{}}", r"\toprule", r"ID & Neighbors & ID & Neighbors\\", r"\midrule"]
    nodes = graph["nodes"]
    for a, b in zip(nodes[:18], nodes[18:]):
        def neighbors(n):
            return ", ".join(sorted(v if u == n else u for u, v in graph["edges"] if n in (u, v)))
        lines.append(" & ".join([a, neighbors(a), b, neighbors(b)]) + r"\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    write_tex("complex-adjacency.tex", lines)
    lines = [r"\begin{tabular}{@{}ll@{}}", r"\toprule", r"Component & Remaining source IDs\\", r"\midrule"]
    for key, group in zip(labels, groups):
        lines.append(key + r" & \shortstack[l]{" + r"\\ ".join(", ".join(group[i:i+9]) for i in range(0,len(group),9)) + r"}\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    write_tex("complex-components.tex", lines)
    lines = [r"\begin{tabular}{@{}lrrrr@{}}", r"\toprule", r"Query & W1 & W2 & W3 & W4\\", r"\midrule"]
    for q, outcomes in gt2["outcomes"].items():
        lines.append(" & ".join([q] + ["yes" if outcomes[w] else "no" for w in ["W1","W2","W3","W4"]]) + r"\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    write_tex("complex-diagnosis-outcomes.tex", lines)
    lines = [r"\begin{tabular}{@{}lr@{}}", r"\toprule",
             r"B-side assignment for (B0024,B0025,B0026,B0035) & Max error (mm)\\", r"\midrule"]
    for candidate in gt3["candidate_fits"]:
        lines.append(", ".join(candidate["match"].values()) + f" & {candidate['proper_fit_max_error_mm']:.4f}" + r"\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    write_tex("complex-registration-candidates.tex", lines)
    for cid, case in cases.items():
        write_tex(f"{cid}-question.tex", [case["question"]])
