"""Build manuscript tables and scientific figures from certified release data."""
from collections import Counter
from dataclasses import asdict
import gzip
import hashlib
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw

from bank import DATA, HERE, ROOT, domain, load_oracle, make_mission, task_bank, write_json
from mission import Action, State, canonical_hash
from session import Session
from visual import core, render

FIGURES = HERE / "figures"
RESEARCH = ROOT / "tem/research/20261008-brickplan-overhaul"
ORDER = ["oracle", "relaxed-greedy", "capacity-dispatch", "astar-100",
         "astar-1000", "astar-500000", "astar-hamming", "legal-random",
         "assembly-only", "unlimited-rack"]
NAMES = ["Exact oracle", "Closure greedy", "Capacity dispatch", "Closure A* (100)",
         "Closure A* (1,000)", "Closure A* (full)", "Hamming A* (full)",
         "Legal random", "Drop inspections", "Ignore rack limit"]


def table(name, columns, header, rows):
    text = [rf"\begin{{tabular}}{{{columns}}}\toprule", header + r"\\\midrule"]
    text += [" & ".join(map(str, row)) + r"\\" for row in rows]
    text += [r"\bottomrule\end{tabular}"]
    (HERE / name).write_text("\n".join(text) + "\n")


def persist_evidence():
    # Archive exact earlier results, never regenerate or invent policy records.
    audit = DATA / "predecessor-static-audit.json"
    if not audit.exists():
        audit.write_bytes((RESEARCH / "static-audit.json").read_bytes())
    records = DATA / "software-control-records.json.gz"
    raw_records = ROOT / "tem/brickplan-v2.2/validation/controls.records.json"
    if raw_records.exists():
        records.write_bytes(gzip.compress(raw_records.read_bytes(), mtime=0))
    elif not records.exists():
        raise FileNotFoundError("Run controls.py before generating the release documents")


def tables(bank, controls):
    episodes, probes = bank["episodes"], bank["probes"]
    cert = json.loads((DATA / "certificate.json").read_text())
    quality = json.loads((DATA / "quality.json").read_text())
    counts = Counter(t["tier"] for t in episodes)
    stats = {
        "EpisodeCount": len(episodes), "ProbeCount": len(probes), "PairCount": len(bank["pairs"]),
        "SourceCount": len({p["sourceGroup"] for p in bank["profiles"]}),
        "ProfileCount": len(bank["profiles"]), "OracleCount": len(cert["oracles"]),
        "ProductCount": sum(c["productStates"] for c in cert["oracles"].values()),
        "EdgeCount": sum(c["directedTransitions"] for c in cert["oracles"].values()),
        "MaxGap": max(t["relaxationGap"] for t in episodes),
        "OldLabels": sum(x["checked"] for x in json.loads((DATA / "predecessor-static-audit.json").read_text())),
        "CalibrationCount": len(quality["calibration"]),
        "DiscriminativeCount": quality["discriminative"],
        "ProblemCount": quality["independentProblems"],
        "PolicyRuns": len(episodes) * 3,
        "RawPolicyRuns": sum(v["all"]["assigned"] for v in controls["policies"].values()),
    }
    (HERE / "generated.tex").write_text("\n".join(
        rf"\newcommand{{\{k}}}{{{v:,}}}" for k, v in stats.items()) + "\n")
    table("sources.tex", "llrrrr", "Base assembly & Kit & Parts & Registered & Movable & Episodes", [
        [p["title"], p["sourceGroup"], p["sourceParts"], p["registeredSites"],
         p.get("reachableMovableSites", "---"),
         sum(t["profile"] == p["id"] for t in episodes)]
        for p in bank["profiles"] if p["sampling"] != "geometry-contrast"])
    table("source-controls.tex", "lrrrr", "Partition & Sources & Episodes & Greedy & Full A*", [
        [split.replace("heldout-source", "Held-out source").replace("development", "Development"),
         len({t["sourceGroup"] for t in episodes if t["split"] == split}),
         sum(t["split"] == split for t in episodes),
         f'{100*controls["policies"]["relaxed-greedy"]["bySplit"][split]["successRate"]:.1f}\\%',
         f'{100*controls["policies"]["astar-500000"]["bySplit"][split]["successRate"]:.1f}\\%']
        for split in ("development", "heldout-source")])
    table("controls-table.tex", "lrrrrr",
          "Control & Runs & Success & Optimal & Regret & Max exp.", [
              [label, (r := controls["policies"][key]["all"])["assigned"], r["completed"],
               r["optimalCompletions"], f'{r["meanSuccessfulRegret"]:.2f}',
               f'{r["maximumExpansions"]:,}' if "astar" in key else "---"]
              for key, label in zip(ORDER, NAMES)])
    table("tiers.tex", "lrrrr", r"Tier & Episodes & $C^*$ range & Gap range & A* max", [
        [tier, counts[tier],
         f'{min(t["optimalCost"] for t in episodes if t["tier"] == tier)}--{max(t["optimalCost"] for t in episodes if t["tier"] == tier)}',
         f'{min(t["relaxationGap"] for t in episodes if t["tier"] == tier)}--{max(t["relaxationGap"] for t in episodes if t["tier"] == tier)}',
         max(t["astarClosureExpansionsSeed0"] for t in episodes if t["tier"] == tier)]
        for tier in ("D1", "D2", "D3", "D4")])
    choices = [p for p in probes if p["kind"] == "next-action"]
    horizon = [{
        "depth": d, "decisions": len(choices),
        "pessimistic": sum(p["horizonEvidence"][str(d)]["allOptimal"] for p in choices),
        "optimistic": sum(p["horizonEvidence"][str(d)]["anyOptimal"] for p in choices),
        "uniformTieMean": sum(p["horizonEvidence"][str(d)]["optimalFractionUnderUniformTies"]
                              for p in choices) / len(choices)}
        for d in (1, 2, 4, 8)]
    table("horizon.tex", "rrrrr", "Depth & Choices & All optimal & Any optimal & Uniform tie", [
        [r["depth"], r["decisions"], r["pessimistic"], r["optimistic"], f'{100*r["uniformTieMean"]:.1f}\\%']
        for r in horizon])
    table("tier-controls.tex", "lrrrr", "Control & D1 & D2 & D3 & D4", [
        [label] + [f'{(r := controls["policies"][key]["byTier"][tier])["completed"]}/{r["assigned"]}'
                   for tier in ("D1", "D2", "D3", "D4")]
        for key, label in zip(ORDER[1:7], NAMES[1:7])])
    audit = json.loads((DATA / "upgrade-audit.json").read_text())
    table("prefix-controls.tex", "rrr", "Prefix length & Correct / assigned & Accuracy", [
        [k, f'{r["correct"]}/{r["total"]}', f'{100*r["accuracy"]:.1f}\\%']
        for k, r in sorted(audit["prefixReplayControl"].items(), key=lambda item: int(item[0]))])
    census = [r"\begin{longtable}{llrrrrrr}", r"\toprule Episode & Tier & Rack & Jobs & Done & $C^*$ & $h$ & A* exp.\\\midrule\endhead"]
    for t in episodes:
        census.append(" & ".join(map(str, [t["id"], t["tier"], t["capacity"], len(t["jobs"]),
                      t["start"]["done"].bit_count(), t["optimalCost"],
                      t["relaxedLowerBound"], t["astarClosureExpansionsSeed0"]])) + r"\\")
    census.append(r"\bottomrule\end{longtable}")
    (HERE / "census.tex").write_text("\n".join(census) + "\n")
    write_json(DATA / "publication-statistics.json", {
        "schema": "brickplan-publication-statistics/2.2", "bankHash": canonical_hash(bank),
        "counts": stats, "byTier": counts, "horizonSelectedProbes": horizon,
        "probeKinds": Counter(p["kind"] for p in probes),
        "pairKinds": Counter(p["kind"] for p in bank["pairs"])})
    write_json(DATA / "geometry-probe-audit.json", {
        "schema": "brickplan-geometry-probe-audit/2.2", "bankHash": canonical_hash(bank),
        "census": bank["geometryCensus"],
        "episodes": sum(t["kind"] == "visual-geometry-context" for t in episodes),
        "pairs": [p for p in bank["pairs"] if p["kind"] == "visual-geometry"],
        "probes": [p for p in probes if p["kind"] == "geometry-continuation"]})


def panel(pixels, title, footer):
    width, height = pixels.size
    result = Image.new("RGB", (width, height + 210), "#f2f5f6")
    result.paste(pixels, (0, 76))
    draw = ImageDraw.Draw(result)
    draw.text((24, 17), title, font=core.font(38), fill="#183040")
    for line, value in enumerate(footer):
        draw.text((24, height + 90 + line * 40), value, font=core.font(30), fill="#142c23")
    return result


def collage(panels, columns):
    w, h = panels[0].size
    output = Image.new("RGB", (columns * w + 16 * (columns - 1),
                              ((len(panels) + columns - 1) // columns) * (h + 16) - 16), "white")
    for i, p in enumerate(panels):
        output.paste(p, ((i % columns) * (w + 16), (i // columns) * (h + 16)))
    return output


def sparse_callouts(pixels, domain, selected, labels):
    """Two publication-only ID callouts; executable geometry stays unchanged."""
    groups = core.geometry(domain)
    bounds = np.concatenate([g[0].reshape(-1, 3) for g in groups])
    center = (bounds.min(0) + bounds.max(0)) / 2
    direction = np.array(core.VECTORS["isometric"], dtype=float)
    direction /= np.linalg.norm(direction)
    right = np.cross([0, 1, 0], direction)
    right /= np.linalg.norm(right)
    rotation = np.stack([right, -np.cross(direction, right), direction], axis=1)
    projected = (bounds - center) @ rotation
    w, h = pixels.size
    unit = w / 760
    scale = min((w - 150 * unit) / max(np.ptp(projected[:, 0]), 1),
                (h - 100 * unit) / max(np.ptp(projected[:, 1]), 1))
    draw = ImageDraw.Draw(pixels)
    for index, (local, label) in enumerate(labels.items()):
        if local not in selected:
            continue
        point = (groups[local][0].reshape(-1, 3).mean(0) - center) @ rotation
        x, y = point[0] * scale + w / 2, point[1] * scale + h / 2
        lx, ly = (w - 176, 84) if index == 0 else (24, 84)
        draw.line((x, y, lx + 68, ly + 28), fill="#264d68", width=4)
        draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill="#264d68")
        draw.rounded_rectangle((lx, ly, lx + 145, ly + 57), radius=8,
                               fill="#ffffff", outline="#264d68", width=3)
        draw.text((lx + 12, ly + 7), label, fill="#183040", font=core.font(38))
    return pixels


def figures(bank, controls):
    FIGURES.mkdir(exist_ok=True)
    provenance = []
    panels = []
    base_profiles = [p for p in bank["profiles"] if p["sampling"] != "geometry-contrast"]
    for p in base_profiles:
        d = domain(p["id"])
        pixels = render(d, range(len(d.parts)), {}, "isometric", size=(1140, 870))
        panels.append(panel(pixels, f'Kit {p["sourceGroup"]}', [
            f'{p["sourceParts"]} source parts; {p["registeredSites"]} registered',
            f'{p["reachableMovableSites"]} movable in the full-assembly component']))
    for page, offset in enumerate(range(0, len(panels), 6), 1):
        filename = f"source-gallery-{page}.png"
        collage(panels[offset:offset + 6], 2).save(FIGURES / filename)
        provenance.append({"file": filename, "profiles": [p["id"] for p in base_profiles[offset:offset + 6]],
                           "state": "Full admitted source subassembly; no pose changes."})

    task = max(bank["episodes"], key=lambda t: t["relaxationGap"])
    mission, oracle = make_mission(task), load_oracle(task["id"])
    session = Session(mission, task, seed=31)
    states = mission.replay(State(**task["start"]), [Action(**a) for a in task["witness"]])["states"]
    frames, panels = [], []
    for step in (0, len(states) // 3, 2 * len(states) // 3, len(states) - 1):
        state = states[step]
        d = mission.domain
        selected = sorted(d.fixed) + [d.mutable[i] for i in range(d.n) if state.assembly & (1 << i)]
        pixels = render(d, selected, {}, "isometric", size=(1140, 870))
        panels.append(panel(pixels, f'Operation {step:02d}', [
            f'Rack {d.n - state.assembly.bit_count()}/{mission.capacity}; remaining cost {oracle.distance(state)}',
            f'{state.assembly.bit_count()} registered pieces installed']))
        frames.append({"step": step, "state": asdict(state), "remainingCost": oracle.distance(state)})
    collage(panels, 2).save(FIGURES / "resource-replay.png")
    provenance.append({"file": "resource-replay.png", "taskId": task["id"], "seed": 31, "frames": frames})

    pair = next(p for p in bank["pairs"] if p["kind"] == "history" and p["id"].startswith("truck"))
    panels, examples = [], []
    for member in pair["members"]:
        t = next(t for t in bank["episodes"] if t["id"] == member)
        m, o = make_mission(t), load_oracle(member)
        s = State(**t["start"])
        session = Session(m, t, seed=31)
        d = m.domain
        selected = sorted(d.fixed) + [d.mutable[i] for i in range(d.n) if s.assembly & (1 << i)]
        relevant = {a.site for a in o.optimal_actions(s)} | set(m.jobs)
        labels = {d.mutable[i]: f'{session.part_ids[i]} {session.site_ids[i]}' for i in relevant
                  if s.assembly & (1 << i)}
        pixels = render(d, selected, labels, "isometric", size=(1140, 870))
        work = "; ".join(f'{session.part_ids[i]}: {"done" if s.done & bit else "pending"}'
                         for i, bit in m.job_bit.items())
        actions = [session.public_action(a) for a in o.optimal_actions(s)]
        choice = ", ".join(f'{a["type"]} {a["partId"]}' for a in actions)
        panels.append(panel(pixels, f'Same assembly | {member}', [work, f'Optimal next: {choice}']))
        examples.append({"taskId": member, "state": asdict(s), "optimalActions": actions})
    collage(panels, 2).save(FIGURES / "ledger-contrast.png")
    provenance.append({"file": "ledger-contrast.png", "pair": pair["id"], "seed": 31, "members": examples})

    # Show the initially supplied revealing view, not a future state.
    pair = next(p for p in bank["pairs"] if p["kind"] == "visual-geometry")
    panels, examples = [], []
    for step in (0,):
        for context, member in enumerate(pair["members"], 1):
            probe = next(p for p in bank["probes"] if p["id"] == member)
            task = next(t for t in bank["episodes"] if t["id"] == probe["taskId"])
            m = make_mission(task)
            d = m.domain
            states = m.replay(State(**probe["state"]), [Action(**a) for a in probe["plan"]])["states"]
            state = states[step]
            selected = sorted(d.fixed) + [d.mutable[i] for i in range(d.n) if state.assembly & (1 << i)]
            pixels = render(d, selected, {}, "left" if step == 0 else "isometric", size=(1000, 650))
            answer = "Whole plan legal" if probe["firstConflict"] is None else f'First conflict at operation {probe["firstConflict"]}'
            panels.append(panel(pixels, f'Context {context} | ' + ("initial left view" if step == 0 else f"after step {step}"), [
                f'{len(d.fixed)} fixed pieces; original source poses',
                answer]))
            examples.append({"probe": member, "step": step, "state": asdict(state), "answer": probe["firstConflict"]})
    collage(panels, 2).save(FIGURES / "geometry-contrast.png")
    provenance.append({"file": "geometry-contrast.png", "pair": pair["id"], "seed": 0, "members": examples})

    from metrics import optimal_corridor, repair_distances
    probe = max((p for p in bank["probes"] if p["kind"] == "delayed-repair"
                 and p["recoveryCohort"] == "inverse-suboptimal" and p["lagAfterError"] == 5),
                key=lambda p: (p["minimumRepairCost"], p["id"]))
    oracle = load_oracle(probe["taskId"])
    mission, d = oracle.mission, oracle.mission.domain
    checkpoint, current = State(**probe["checkpoint"]), State(**probe["state"])
    corridor = optimal_corridor(oracle, checkpoint) - {oracle.target}
    distances = repair_distances(oracle, corridor)
    state, repair = current, []
    while oracle.encode(state) not in corridor:
        action, state = next((a, s) for a, s in mission.moves(state)
                             if s != mission.terminal and distances[oracle.encode(s)] >= 0
                             and distances[oracle.encode(s)] == distances[oracle.encode(state)] - 1)
        repair.append(action)
    session = Session(mission, next(t for t in bank["episodes"] if t["id"] == probe["taskId"]), seed=0)
    first = session.public_action(repair[0])
    last = session.public_action(Action(**probe["history"][-1]))
    panels = []
    for title, s, footer in [
            ("A  Before the error", checkpoint, [f'Optimal remainder: {oracle.distance(checkpoint)} operations', "Reference for the repair corridor"]),
            ("B  Delayed checkpoint", current, [f'Error + {probe["lagAfterError"]} more operations', f'Shortest repair: {len(repair)} operations']),
            ("C  Corridor restored", state, [f'First repair: {first["type"]} {first["partId"]}', "Nonterminal optimal corridor reached"])]:
        selected = sorted(d.fixed) + [d.mutable[i] for i in range(d.n) if s.assembly & (1 << i)]
        pixels = render(d, selected, {}, "isometric", size=(1000, 750))
        pixels = sparse_callouts(pixels, d, selected, {
            d.mutable[session.pieces[first["partId"]]]: first["partId"],
            d.mutable[session.pieces[last["partId"]]]: last["partId"]})
        panels.append(panel(pixels, title, footer))
    images = collage(panels, 3)
    result = Image.new("RGB", (images.width, images.height + 176), "#f2f5f6")
    result.paste(images)
    draw = ImageDraw.Draw(result)
    trace = "Shortest repair: " + "  >  ".join(
        f'{a["type"]} {a["partId"]}' for a in [session.public_action(a) for a in repair])
    font_size = 39
    while draw.textbbox((0, 0), trace, font=core.font(font_size))[2] > images.width - 48:
        font_size -= 1
    draw.text((24, images.height + 20), trace, fill="#183040", font=core.font(font_size))
    draw.text((24, images.height + 88),
              f'{len(repair)} operations via {first["partId"]}  |  '
              f'{len(repair) + probe["inverseLastControl"]["extraCost"]} operations if the first step undoes {last["partId"]}',
              fill="#183040", font=core.font(39))
    result.save(FIGURES / "repair-case.png")
    provenance.append({"file": "repair-case.png", "probe": probe["id"], "seed": 0,
                       "states": [asdict(s) for s in (checkpoint, current, state)],
                       "lastHistoryAction": last, "firstRepairAction": first,
                       "repairActions": [session.public_action(a) for a in repair],
                       "inverseLast": probe["inverseLastControl"]})
    write_json(DATA / "paper-case.json", provenance[-1])

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 3.3), layout="constrained")
    colors = {"D1": "#849995", "D2": "#327c9f", "D3": "#437f5a", "D4": "#b15d36"}
    for tier, color in colors.items():
        tasks = [t for t in bank["episodes"] if t["tier"] == tier]
        axes[0].scatter([t["relaxedLowerBound"] for t in tasks], [t["optimalCost"] for t in tasks],
                        c=color, label=f'{tier} (n={len(tasks)})', s=30, alpha=.8)
    upper = max(t["optimalCost"] for t in bank["episodes"]) + 2
    axes[0].plot([0, upper], [0, upper], "--", color="#777777", lw=1)
    axes[0].set(xlabel="Static closure lower bound (operations)", ylabel="Exact mission cost (operations)")
    axes[0].legend(frameon=False, fontsize=8)
    keys, labels = ORDER[1:6], ["Greedy", "Dispatch", "A* 100", "A* 1,000", "Full A*"]
    for j, (key, label) in enumerate(zip(keys, labels)):
        row = controls["policies"][key]["all"]
        axes[1].bar(j, row["successRate"] * 100, color="#bdd0c7", width=.7)
        axes[1].bar(j, row["optimalCompletions"] / row["assigned"] * 100, color="#276649", width=.7)
    axes[1].set(xticks=range(len(keys)), xticklabels=labels, ylim=(0, 110),
                ylabel="Task-runs (%)", title=f'{len(bank["episodes"]) * 3} runs per control; {len(bank["episodes"])} tasks')
    axes[1].bar([], [], color="#bdd0c7", label="Completed")
    axes[1].bar([], [], color="#276649", label="Optimal completion")
    axes[1].legend(frameon=False, fontsize=8, loc="upper left")
    fig.savefig(FIGURES / "mechanism-evidence.pdf")
    fig.savefig(FIGURES / "mechanism-evidence.png", dpi=220)
    plt.close(fig)
    provenance.append({"file": "mechanism-evidence.pdf", "inputs": [
        "data/tasks.private.json", "data/software-controls.json"], "scope": "Software controls only"})
    for row in provenance:
        row["sha256"] = hashlib.sha256((FIGURES / row["file"]).read_bytes()).hexdigest()
    write_json(FIGURES / "provenance.json", {
        "schema": "brickplan-figures/2.2", "bankHash": canonical_hash(bank),
        "meshSha256": hashlib.sha256((HERE / "arena/meshes.json").read_bytes()).hexdigest(),
        "renderer": "../brickplan-v1.2/visual.py + raster.c; original LDraw triangles",
        "license": "../ASSET-LICENSES.json", "figures": provenance})


def main():
    persist_evidence()
    bank = task_bank()
    controls = json.loads((DATA / "software-controls.json").read_text())
    assert controls["visualModelResults"] is None and controls["humanResults"] is None
    tables(bank, controls)
    figures(bank, controls)
    print("Generated evidence-bound tables, census and original-geometry figures.")


if __name__ == "__main__":
    main()
