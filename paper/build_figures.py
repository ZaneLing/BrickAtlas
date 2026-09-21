#!/usr/bin/env python3
"""Compose real dataset pixels, exact questions and verified GT for publication."""
import base64
import hashlib
import json
import math
from pathlib import Path
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FIG = HERE / "figures"
MANIFEST = ROOT / "benchmark/ldraw-evidence-v3/visual-manifest.json"
RENDERS = ROOT / "benchmark/ldraw-evidence-v3/renders.json"
INK, MUTED, BLUE, GREEN = "#172b40", "#536579", "#235c86", "#176749"
PROVENANCE, EXAMPLES = [], []
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8,
                     "pdf.fonttype": 42, "ps.fonttype": 42,
                     "text.color": INK, "axes.edgecolor": "#d9e2e9"})


def load(path):
    return json.loads(Path(path).read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def record(path, **fields):
    return {"file": str(Path(path).relative_to(ROOT)), "sha256": sha(path), **fields}


def canvas(w, h):
    return plt.figure(figsize=(w, h), facecolor="white")


def text(fig, x, y, value, size=8, **kw):
    return fig.text(x, y, value, fontsize=size, va="top", **kw)


def image(fig, rect, pixels):
    pixels = pixels.copy()
    pixels.thumbnail((max(1, round(rect[2] * fig.get_figwidth() * 450)),
                      max(1, round(rect[3] * fig.get_figheight() * 450))),
                     Image.Resampling.LANCZOS)
    ax = fig.add_axes(rect)
    ax.imshow(pixels, interpolation="none")
    ax.axis("off")
    return ax


def save(fig, name, sources, **fields):
    FIG.mkdir(exist_ok=True)
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    for artist in list(fig.texts) + [t for ax in fig.axes for t in ax.texts]:
        box = artist.get_window_extent(renderer)
        assert (box.x0 >= 0 and box.y0 >= 0 and box.x1 <= fig.bbox.width
                and box.y1 <= fig.bbox.height), (name, artist.get_text())
    outputs = []
    for suffix in ["pdf", "png"]:
        path = FIG / f"{name}.{suffix}"
        fig.savefig(path, dpi=300, metadata={"Creator": "BrickAtlas dataset figure builder"})
        outputs.append(record(path))
    plt.close(fig)
    PROVENANCE.append({"figure": name, "outputs": outputs, "sources": sources,
                       "model_responses": None,
                       "print_sampling": "Preserve aspect ratio; downsample only above 450 print dpi with LANCZOS.",
                       **fields})


def content_box(images, background=(255, 255, 255), padding=22):
    boxes = []
    for im in images:
        data = np.asarray(im.convert("RGB")).astype(int)
        mask = np.max(abs(data - np.array(background)), axis=2) > 12
        yy, xx = np.where(mask)
        assert len(xx), "Empty source image"
        boxes.append((xx.min(), yy.min(), xx.max() + 1, yy.max() + 1))
    w, h = images[0].size
    return list(map(int, [max(0, min(b[0] for b in boxes) - padding),
            max(0, min(b[1] for b in boxes) - padding),
            min(w, max(b[2] for b in boxes) + padding),
            min(h, max(b[3] for b in boxes) + padding)]))


def visual(oid):
    obs = OBS[oid]
    render = RENDER[oid]
    path = ROOT / render["file"]
    assert sha(path) == render["sha256"]
    wire_path = ROOT / INDEX[oid]["file"]
    wire = load(wire_path)
    user = next(m for m in wire["messages"] if m["role"] == "user")
    payload = json.loads(next(c["text"] for c in user["content"] if c["type"] == "text"))
    assert payload == obs["payload"]
    uri = next(c["image_url"]["url"] for c in user["content"] if c["type"] == "image_url")
    assert base64.b64decode(uri.split(",", 1)[1]) == path.read_bytes()
    gold_label = next(o["label"] for o in payload["options"] if o["id"] == obs["gold"]["choiceId"])
    assert gold_label == obs["gold_semantics"]
    source = record(path, observation_id=oid, wire=record(wire_path),
                    parent_task_id=obs["parent_task_id"], arm=obs["arm"],
                    payload=payload, gold=obs["gold"], gold_semantics=gold_label)
    EXAMPLES.append(source)
    return obs, Image.open(path).convert("RGB"), source


def pair(parent):
    p = next(p for p in M["pairs"] if p["parent_task_id"] == parent)
    a, ia, ra = visual(p["a"])
    b, ib, rb = visual(p["b"])
    assert a["payload"] == b["payload"]
    assert a["gold"] != b["gold"]
    box = content_box([ia, ib])
    for r in [ra, rb]:
        r["crop_xyxy"] = box
        r["crop_policy"] = "Same union bounding box; remove only empty margins; retain all operands and labels."
    return a, b, ia.crop(box), ib.crop(box), [ra, rb]


def option_text(obs):
    return "     ".join(f"{o['id']}: {o['label']}" for o in obs["payload"]["options"])


def question_figure(parent, name):
    a, b, ia, ib, records = pair(parent)
    color = a["family"] == "color"
    fig = canvas(7, 2.65 if color else 4.05)
    text(fig, .015, .98, f"{a['display_name']}  |  {parent}", 8.5, weight="bold", color=BLUE)
    text(fig, .015, .895, "\n".join(textwrap.wrap(a["payload"]["question"], 106)), 8.1)
    text(fig, .015, .795 if color else .79, option_text(a), 8, weight="bold")
    top, bottom = (.69, .20) if color else (.69, .17)
    for col, (o, im) in enumerate([(a, ia), (b, ib)]):
        x = .015 + .5 * col
        text(fig, x, top + .07, f"Observation {o['arm']}", 8.2, color=MUTED)
        image(fig, [x, bottom, .47, top - bottom], im)
        text(fig, x, bottom - .015, 'GT: ' + json.dumps(o["gold"], separators=(",", ":"))
             + f"  =  {o['gold_semantics']}", 8.8, color=GREEN, weight="bold")
    if color:
        note = f"Source record: part {a['source_truth']['part_number']}, {a['source_truth']['color']}.  Scored answer: current rendered color."
    else:
        parts = {p["id"]: p for p in load(ROOT / "public/benchmark/ldraw-v2/models/omr-42004.json")["parts"]}
        matched = a["display_referents"][a["gold_semantics"]]["instance_id"]
        assert matched == b["display_referents"][b["gold_semantics"]]["instance_id"]
        target = a["canonical_target"]["instance_id"]
        assert parts[target]["partNumber"] == parts[matched]["partNumber"] == "32250"
        note = "GT audit: target B0035 and source instance B0036 share part 32250.\nThe matching instance is labeled B0036 in A and B0116 in B; all geometry stays fixed."
    text(fig, .015, .065 if color else .075, note, 7.5, color=MUTED)
    save(fig, name, records, selection="Illustrative source-linked pair; not an answerability or model-performance claim.",
         gt_basis=note, image_edits="Identical empty-margin crop only; annotations outside the image.")


def source_image(source):
    entry = CATALOG[source]
    capture = next(m for m in CAPTURE["models"] if m["id"] == source)
    row = next(i for i in capture["images"] if i["file"] == source + "-iso.png")
    path = ROOT / "tem/papers/legacy-tree/figures/ldraw" / row["file"]
    assert sha(path) == row["sha256"] and capture["sourceHash"] == entry["sourceHash"]
    im = Image.open(path).convert("RGB")
    box = content_box([im], background=(244, 245, 248), padding=28)
    return im.crop(box), record(path, source_id=source, source_hash=entry["sourceHash"],
                                source_band=entry["difficulty"], parts=entry["parts"], crop_xyxy=box,
                                crop_policy="Empty-margin crop of full source assembly; original poses.",
                                capture_manifest="benchmark/ldraw-v1/capture.json")


def sources_figure(all_sources=False):
    ids = list(CATALOG) if all_sources else [
        "31028", "omr-42004", "10159", "omr-10265",
        "omr-42102", "omr-42061", "10001", "omr-42054"]
    rows = 6 if all_sources else 2
    fig = canvas(7, 8.3 if all_sources else 3.25)
    records = []
    for i, source in enumerate(ids):
        entry = CATALOG[source]
        im, rec = source_image(source)
        records.append(rec)
        x, top = .012 + .247 * (i % 4), .95 - (i // 4) * (.94 / rows)
        image(fig, [x, top - .94 / rows + .025, .234,
                    .94 / rows - .025 - .38 / fig.get_figheight()], im)
        text(fig, x + .005, top, f"{entry['difficulty']}  |  {source.replace('omr-', '')}  |  {entry['parts']:,} parts",
             7.6, weight="bold")
        text(fig, x + .005, top - .13 / fig.get_figheight(),
             "\n".join(textwrap.wrap(entry["name"], 28)), 7)
    save(fig, "source-atlas" if all_sources else "source-overview", records,
         role="Complete source assemblies for provenance; not primary model observations.",
         selection="All 24 sources" if all_sources else "Two illustrative sources per scale band D1-D4")


def panel_figure():
    o, im, rec = visual("obs-95b122c4e28060bb3f64fa19")
    fig = canvas(7, 3.05)
    text(fig, .015, .98, "Position-reference control  |  ld2-omr-42004-shape-match-1", 8.5, weight="bold", color=BLUE)
    text(fig, .015, .88, "\n".join(textwrap.wrap(o["payload"]["question"], 106)), 8)
    text(fig, .015, .725, option_text(o), 7.4, weight="bold")
    image(fig, [.10, .105, .8, .58], im)
    text(fig, .015, .078, 'GT: ' + json.dumps(o["gold"], separators=(",", ":")) + "  =  Third from left", 8.4,
         weight="bold", color=GREEN)
    save(fig, "panel-question-gt", [rec], image_edits="None; full native image; question/options/GT outside pixels.")


def components(nodes, edges):
    pending = set(nodes)
    result = []
    while pending:
        group, queue = set(), [min(pending)]
        while queue:
            node = queue.pop()
            if node in group:
                continue
            group.add(node)
            queue.extend(v if u == node else u for u, v in edges if node in (u, v))
        pending -= group
        result.append(sorted(group))
    return result


def graph_figure():
    path = ROOT / "benchmark/ldraw-evidence-v1/matched-graphs-v1/inputs.json"
    audit_path = ROOT / "benchmark/ldraw-evidence-v2/graph-audit.json"
    graph = load(audit_path)
    p = next(p for p in graph["pairs"] if p["role"] == "strong-change"
             and p["parent_task_id"] == "ld2-10014-graph-removal-2")
    inputs = {o["id"]: o for o in load(path)["observations"]}
    fig = canvas(7, 2.75)
    text(fig, .015, .985, "Text-graph task  |  ld2-10014-graph-removal-2", 8.5, weight="bold", color=BLUE)
    text(fig, .015, .88, "\n".join(textwrap.wrap(inputs[p["a"]]["payload"]["question"], 106)), 8)
    records = []
    for col, arm in enumerate(["a", "b"]):
        obs = inputs[p[arm]]
        original = obs["payload"]["input"]
        removed = "B0024"
        nodes = [n for n in original["nodes"] if n != removed]
        edges = [e for e in original["edges"] if removed not in e]
        groups = components(nodes, edges)
        assert len(groups) == p[arm + "_gold"]
        assert len(edges) == 6 and sorted(sum(n in e for e in edges) for n in nodes) == [2] * 6
        ax = fig.add_axes([.01 + col * .50, .22, .47, .49])
        ax.set_xlim(-1.6, 1.6)
        ax.set_ylim(-1.2, 1.2)
        ax.set_aspect("equal")
        ax.axis("off")
        # Fixed coordinates from an actual cycle walk; each edge is read from the input.
        if len(groups) == 1:
            order = [min(nodes)]
            while len(order) < len(nodes):
                order.append(next(v if u == order[-1] else u for u, v in edges
                                  if order[-1] in (u, v) and (v if u == order[-1] else u) not in order))
            positions = {n: (1.0 * math.cos(math.pi / 2 + 2 * math.pi * i / 6),
                             .83 * math.sin(math.pi / 2 + 2 * math.pi * i / 6))
                         for i, n in enumerate(order)}
        else:
            positions = {n: (center + .42 * math.cos(math.pi / 2 + 2 * math.pi * i / 3),
                              .70 * math.sin(math.pi / 2 + 2 * math.pi * i / 3))
                         for group, center in zip(groups, [-.82, .82]) for i, n in enumerate(group)}
        for u, v in edges:
            ax.plot([positions[u][0], positions[v][0]], [positions[u][1], positions[v][1]],
                    color=BLUE, lw=1.5, zorder=1)
        for node, (x, y) in positions.items():
            ax.add_patch(Circle((x, y), .075, facecolor=BLUE, zorder=2))
            ax.text(x, y + (.18 if y >= 0 else -.18), node, ha="center", va="center", fontsize=7.5,
                    bbox={"facecolor": "white", "edgecolor": "none", "pad": .5})
        text(fig, .025 + col * .5, .735, f"Observation {arm.upper()} after deletion", 8, color=MUTED)
        text(fig, .025 + col * .5, .19, f"GT: {len(groups)} connected component" + ("s" if len(groups) > 1 else ""),
             8.8, color=GREEN, weight="bold")
        records.append(record(path, observation_id=obs["id"], payload=obs["payload"], removed=removed,
                              surviving_nodes=nodes, surviving_edges=edges, components=groups,
                              gold=len(groups), audit=record(audit_path)))
    text(fig, .015, .06, "Matched on both sides: 6 surviving nodes, 6 edges, degree multiset [2, 2, 2, 2, 2, 2], no isolates.", 7.5,
         color=MUTED)
    save(fig, "graph-question-gt", records, role="Diagram of supplied hypothetical edge lists after deletion; no physical edge claim.")


def gallery():
    parents = ["ld2-31028-color-1", "ld2-omr-42102-shape-match-1",
               "ld2-10213-color-1", "ld2-omr-42054-shape-match-2"]
    fig = canvas(7, 7.8)
    records = []
    for row, parent in enumerate(parents):
        a, b, ia, ib, rec = pair(parent)
        records += rec
        top = .985 - row * .248
        text(fig, .015, top, f"{a['display_name']}  |  {parent}", 8.5, weight="bold", color=BLUE)
        text(fig, .015, top - .030, "\n".join(textwrap.wrap(a["payload"]["question"], 116)), 7.6)
        text(fig, .015, top - .083, option_text(a), 7.4, weight="bold")
        for col, (o, im) in enumerate([(a, ia), (b, ib)]):
            x = .015 + col * .5
            image(fig, [x, top - .218, .465, .129], im)
            text(fig, x, top - .223, f"{o['arm']} GT: " + json.dumps(o["gold"], separators=(",", ":"))
                 + f" = {o['gold_semantics']}", 7.6, color=GREEN)
    save(fig, "additional-question-gt", records, role="Four further illustrative parents; no model outputs.",
         selection="Two Color and two Part-type pairs from four additional sources.")


def gt_table():
    parent = "ld2-omr-42004-shape-match-1"
    p = next(p for p in M["pairs"] if p["parent_task_id"] == parent)
    a, b = OBS[p["a"]], OBS[p["b"]]
    bundle_path = ROOT / "public/benchmark/ldraw-v2/models/omr-42004.json"
    parts = {x["id"]: x for x in load(bundle_path)["parts"]}
    lines = [r"\begin{tabular}{@{}lllll@{}}", r"\toprule",
             r"Source instance & Part type & Label in A & Label in B & Role\\", r"\midrule"]
    for instance in a["render_spec"]["render_operands"]:
        la = next(k for k, v in a["display_referents"].items() if v["instance_id"] == instance)
        lb = next(k for k, v in b["display_referents"].items() if v["instance_id"] == instance)
        target = instance == a["canonical_target"]["instance_id"]
        role = "Target" if target else "Match" if la == a["gold_semantics"] else "Distractor"
        lines.append(" & ".join([parts[instance]["label"], parts[instance]["partNumber"], la, lb, role]) + r"\\")
    lines += [r"\bottomrule", r"\end{tabular}", ""]
    (HERE / "generated/gt-referents.tex").write_text("\n".join(lines))
    # Export the exact shared contract separately from the compact figure text.
    def escape(value):
        return value.replace("\\", r"\textbackslash{}").replace("_", r"\_").replace("&", r"\&")
    (HERE / "generated/example-contract.tex").write_text(escape(a["payload"]["identity_contract"]) + "\n")
    task = next(t for t in load(ROOT / "public/benchmark/evidence-v3/dossiers.json")["items"]
                if t["parent_task_id"] == "ld2-omr-42102-source-sequence-1")
    lines = [r"\begin{tabular}{@{}lll@{}}", r"\toprule", r"Action & Newly visible IDs & Cumulative parts\\", r"\midrule"]
    count = 0
    for step in task["input"]["sourceWindow"]:
        count += len(step["labels"])
        lines.append(" & ".join([step["actionId"], ", ".join(step["labels"]), str(count)]) + r"\\")
    lines += [r"\bottomrule", r"\end{tabular}", ""]
    (HERE / "generated/replay-gt.tex").write_text("\n".join(lines))
    (HERE / "generated/replay-question.tex").write_text(escape(task["prompt_en"]) + "\n")
    EXAMPLES.append({"kind": "historical-visibility-task", "parent_task_id": task["parent_task_id"],
                     "question": task["prompt_en"], "gold": task["answer"],
                     "source_window": task["input"]["sourceWindow"],
                     "source": record(ROOT / "public/benchmark/evidence-v3/dossiers.json")})


def main():
    sources_figure()
    sources_figure(all_sources=True)
    question_figure("ld2-omr-42004-color-1", "color-question-gt")
    question_figure("ld2-omr-42004-shape-match-1", "type-question-gt")
    panel_figure()
    graph_figure()
    gallery()
    gt_table()
    output = {"schema": 1, "builder": record(Path(__file__)), "manifest": record(MANIFEST),
              "renders": record(RENDERS), "source_catalog": record(ROOT / "benchmark/ldraw-v2/catalog.json"),
              "figures": PROVENANCE,
              "policy": "Real source renders and frozen input pixels only; no generative imagery, responses or human judgments.",
              "examples": EXAMPLES}
    (HERE / "visual-evidence.json").write_text(json.dumps(output, indent=2) + "\n")
    print(f"Built {len(PROVENANCE)} figures and {len(EXAMPLES)} source-bound example records.")


M = load(MANIFEST)
OBS = {o["observation_id"]: o for o in M["observations"]}
RENDER = {o["observation_id"]: o for o in load(RENDERS)["images"]}
INDEX = {o["observation_id"]: o for o in load(ROOT / "benchmark/ldraw-evidence-v3/observation-index.json")["observations"]}
CATALOG = {m["id"]: m for m in load(ROOT / "benchmark/ldraw-v2/catalog.json")}
CAPTURE = load(ROOT / "benchmark/ldraw-v1/capture.json")

if __name__ == "__main__":
    main()
