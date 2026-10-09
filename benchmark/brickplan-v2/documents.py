"""Build manuscript tables and scientific figures from certified release data."""
from collections import Counter
from dataclasses import asdict
import gzip
import hashlib
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
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
    raw_records = ROOT / "tem/brickplan-v2/validation/controls.records.json"
    if raw_records.exists():
        records.write_bytes(gzip.compress(raw_records.read_bytes(), mtime=0))
    elif not records.exists():
        raise FileNotFoundError("Run controls.py before generating the release documents")


def tables(bank, controls):
    episodes, probes = bank["episodes"], bank["probes"]
    cert = json.loads((DATA / "certificate.json").read_text())
    counts = Counter(t["tier"] for t in episodes)
    stats = {
        "EpisodeCount": len(episodes), "ProbeCount": len(probes), "PairCount": len(bank["pairs"]),
        "SourceCount": len({p["sourceGroup"] for p in bank["profiles"]}),
        "ProfileCount": len(bank["profiles"]), "OracleCount": len(cert["oracles"]),
        "ProductCount": sum(c["productStates"] for c in cert["oracles"].values()),
        "EdgeCount": sum(c["directedTransitions"] for c in cert["oracles"].values()),
        "MaxGap": max(t["relaxationGap"] for t in episodes),
        "OldLabels": sum(x["checked"] for x in json.loads((DATA / "predecessor-static-audit.json").read_text())),
    }
    (HERE / "generated.tex").write_text("\n".join(
        rf"\newcommand{{\{k}}}{{{v:,}}}" for k, v in stats.items()) + "\n")
    table("sources.tex", "llrrrrrr", "Profile & Kit & Parts & Reg. & Move & Rack & Episodes & Max gap", [
        [p["title"], p["sourceGroup"], p["sourceParts"], p["registeredSites"],
         p["reachableMovableSites"], p["capacity"],
         sum(t["profile"] == p["id"] for t in episodes),
         max(t["relaxationGap"] for t in episodes if t["profile"] == p["id"])]
        for p in bank["profiles"]])
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
    census = [r"\begin{longtable}{llrrrrrr}", r"\toprule Episode & Tier & Rack & Jobs & Done & $C^*$ & $h$ & A* exp.\\\midrule\endhead"]
    for t in episodes:
        census.append(" & ".join(map(str, [t["id"], t["tier"], t["capacity"], len(t["jobs"]),
                      t["start"]["done"].bit_count(), t["optimalCost"],
                      t["relaxedLowerBound"], t["astarClosureExpansionsSeed0"]])) + r"\\")
    census.append(r"\bottomrule\end{longtable}")
    (HERE / "census.tex").write_text("\n".join(census) + "\n")
    write_json(DATA / "publication-statistics.json", {
        "schema": "brickplan-publication-statistics/2.0", "bankHash": canonical_hash(bank),
        "counts": stats, "byTier": counts, "horizonSelectedProbes": horizon,
        "probeKinds": Counter(p["kind"] for p in probes),
        "pairKinds": Counter(p["kind"] for p in bank["pairs"])})


def panel(pixels, title, footer):
    width, height = pixels.size
    result = Image.new("RGB", (width, height + 160), "#edf1ed")
    result.paste(pixels, (0, 66))
    draw = ImageDraw.Draw(result)
    draw.text((24, 17), title, font=core.font(26), fill="#142c23")
    for line, value in enumerate(footer):
        draw.text((24, height + 75 + line * 29), value, font=core.font(21), fill="#142c23")
    return result


def collage(panels, columns):
    w, h = panels[0].size
    output = Image.new("RGB", (columns * w + 16 * (columns - 1),
                              ((len(panels) + columns - 1) // columns) * (h + 16) - 16), "white")
    for i, p in enumerate(panels):
        output.paste(p, ((i % columns) * (w + 16), (i // columns) * (h + 16)))
    return output


def figures(bank, controls):
    FIGURES.mkdir(exist_ok=True)
    provenance = []
    panels = []
    for p in bank["profiles"]:
        d = domain(p["id"])
        pixels = render(d, range(len(d.parts)), {}, "isometric", size=(1140, 870))
        panels.append(panel(pixels, f'{p["title"]} | kit {p["sourceGroup"]}', [
            f'{p["sourceParts"]} source parts; {p["registeredSites"]} registered',
            f'{p["reachableMovableSites"]} movable in the full-assembly component']))
    collage(panels, 3).save(FIGURES / "source-gallery.png")
    provenance.append({"file": "source-gallery.png", "profiles": [p["id"] for p in bank["profiles"]],
                       "state": "Full original assembly; no pose changes."})

    task = max(bank["episodes"], key=lambda t: t["relaxationGap"])
    mission, oracle = make_mission(task), load_oracle(task["id"])
    session = Session(mission, task, seed=31)
    states = mission.replay(State(**task["start"]), [Action(**a) for a in task["witness"]])["states"]
    frames, panels = [], []
    for step in (0, 12, 28, len(states) - 1):
        state = states[step]
        d = mission.domain
        selected = sorted(d.fixed) + [d.mutable[i] for i in range(d.n) if state.assembly & (1 << i)]
        labels = {d.mutable[i]: session.site_ids[i] for i in range(d.n) if state.assembly & (1 << i)}
        pixels = render(d, selected, labels, "isometric", size=(1140, 870))
        panels.append(panel(pixels, f'Operation {step:02d} | {task["id"]}', [
            f'Rack {d.n - state.assembly.bit_count()}/{mission.capacity}; remaining cost {oracle.distance(state)}',
            f'Source poses preserved; {state.assembly.bit_count()} registered pieces installed']))
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

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 3.3), layout="constrained")
    colors = {"D1": "#849995", "D2": "#327c9f", "D3": "#437f5a", "D4": "#b15d36"}
    for tier, color in colors.items():
        tasks = [t for t in bank["episodes"] if t["tier"] == tier]
        axes[0].scatter([t["relaxedLowerBound"] for t in tasks], [t["optimalCost"] for t in tasks],
                        c=color, label=f'{tier} (n={len(tasks)})', s=30, alpha=.8)
    axes[0].plot([0, 45], [0, 45], "--", color="#777777", lw=1)
    axes[0].set(xlabel="Static closure lower bound (operations)", ylabel="Exact mission cost (operations)")
    axes[0].legend(frameon=False, fontsize=8)
    keys, labels = ORDER[1:6], ["Greedy", "Dispatch", "A* 100", "A* 1,000", "Full A*"]
    for j, (key, label) in enumerate(zip(keys, labels)):
        row = controls["policies"][key]["all"]
        axes[1].bar(j, row["successRate"] * 100, color="#bdd0c7", width=.7)
        axes[1].bar(j, row["optimalCompletions"] / row["assigned"] * 100, color="#276649", width=.7)
    axes[1].set(xticks=range(len(keys)), xticklabels=labels, ylim=(0, 110),
                ylabel="Task-runs (%)", title="207 runs per control; 69 tasks")
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
        "schema": "brickplan-figures/2.0", "bankHash": canonical_hash(bank),
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
