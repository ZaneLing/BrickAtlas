"""Generate manuscript numbers and original-geometry replay figures from evidence."""
import hashlib
import json
from collections import defaultdict

from build import HERE, load_bank, write_json
from cases import CASES
from session import Session
from visual import render

OUT = HERE.parents[1] / "tem/brickplan-v1.2/validation"


def main():
    banks = [load_bank(c["id"]) for c in CASES]
    release = json.loads((HERE / "data/release.json").read_text())
    (HERE / "generated.tex").write_text("\n".join(
        f"\\newcommand{{\\{key}}}{{{value:,}}}" for key,value in {
            "StructureCount":release["structures"], "EpisodeCount":release["episodes"],
            "ProbeCount":release["probeResponses"],
            "StateCount":sum(b[3]["reachableStates"] for b in banks),
            "EdgeCount":sum(b[3]["directedTransitions"] for b in banks),
        }.items()) + "\n")
    rows = []
    for d,tasks,costs,c in banks:
        t = tasks["episodes"][-1]
        rows.append(f"{c['case']} & {c['provenanceGroup']} & {d.n} & {c['reachableStates']:,} & "
                    f"{t['optimalActions']} & {t['minimumDetaches']} & {t['hammingLowerBound']} \\\\")
    (HERE / "case-table.tex").write_text(
        "\\begin{tabular}{llrrrrr}\\toprule\nCase & Source group & Sites & States & $C^*$ & $D^*$ & Hamming \\\\\\midrule\n"
        + "\n".join(rows) + "\n\\bottomrule\\end{tabular}\n")
    controls = json.loads((OUT / "controls.json").read_text())
    grouped = defaultdict(list)
    for row in controls["rows"]:
        grouped[row["policy"]].append(row)
    rows = []
    for name, members in grouped.items():
        n = sum(m["success"]["numerator"] for m in members)
        total = sum(m["success"]["denominator"] for m in members)
        rows.append(f"{name} & {len(members)} & {n}/{total} \\\\")
    (HERE / "control-table.tex").write_text(
        "\\begin{tabular}{lrr}\\toprule\nSoftware control & Runs & Success \\\\\\midrule\n"
        + "\n".join(rows) + "\n\\bottomrule\\end{tabular}\n")
    figures = HERE / "figures"
    figures.mkdir(exist_ok=True)
    d,tasks,costs,cert = banks[2]
    task = tasks["episodes"][-1]
    s = Session(d, task, 31)
    selected = {0, 10, 20, task["optimalActions"]}
    frames = []
    for step in range(task["optimalActions"] + 1):
        if step in selected:
            locals_ = sorted(d.fixed) + [d.mutable[i] for i in s.installed]
            labels = {d.mutable[i]: f"{s.installed[i]} {s.site_ids[i]}" for i in s.installed}
            image = render(d, locals_, labels, "isometric", size=(1520, 1160))
            file = figures / f"reconfigure-{step}.png"
            image.save(file)
            frames.append({"step": step, "state": s.state, "file": file.name,
                           "sha256": hashlib.sha256(file.read_bytes()).hexdigest()})
        if step < task["optimalActions"]:
            action = s.public_action(task["completionWitness"][step])
            s.submit({"requestId": str(step), "revision": step, "action": action})
    write_json(figures / "provenance.json", {
        "source": "Authoritative airframe partial-target reconfiguration; original locked LDraw triangles.",
        "taskId":task["id"], "seed":31, "taskHash":cert["tasksHash"],
        "geometryHash":cert["geometryHash"], "sourceHash":cert["sourceHash"],
        "optimalActions":task["optimalActions"], "minimumDetaches":task["minimumDetaches"],
        "frames":frames, "softwareValidationOnly":True, "sourcePosesModified":False,
    })
    print("Generated tables and four source-pose replay figures.")


if __name__ == "__main__":
    main()
