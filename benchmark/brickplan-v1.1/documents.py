"""Generate release counts, tables and validation prose from executed evidence."""
import json
import hashlib
import shutil
import subprocess
from PIL import Image
from runtime import activate, HERE, OUT, ROOT

activate()
from build import load_bank
from cases import CASES


def fraction(row):
    return f"{row['numerator']}/{row['denominator']}"


def main():
    release = json.loads((HERE / "data/release.json").read_text())
    summary = json.loads((OUT / "summary.json").read_text())
    http = json.loads((OUT / "http-summary.json").read_text())
    browser = json.loads((OUT / "arena-summary.json").read_text())
    frames = json.loads((HERE / "figures/provenance.json").read_text())
    assert all(e["passed"] for e in (summary, http, browser))
    crops = []
    for frame in frames["frames"]:
        source = HERE / "figures" / frame["file"]
        target = source.with_stem(source.stem + "-detail")
        with Image.open(source) as image:
            w, h = image.size
            box = (round(w * .25), round(h * .24), round(w * .74), round(h * .84))
            image.crop(box).save(target)
        crops.append({"source": source.name, "output": target.name, "pixelCrop": box,
                      "sourceSha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                      "outputSha256": hashlib.sha256(target.read_bytes()).hexdigest()})
    (HERE / "figures/detail-provenance.json").write_text(json.dumps(
        {"operation": "Crop margins only; no geometry, color or state edits", "frames": crops},
        indent=2) + "\n")
    banks = [load_bank(c["id"]) for c in CASES]
    certs = release["cases"]
    air = next(c for c in certs if c["case"] == "airframe")
    domain = next(d for d, _, _, c in banks if c["case"] == "airframe")
    source_chain = [domain.parts[domain.mutable[s]]["sourceIndex"]
                    for s in air["mandatoryOrder"]["longestMandatoryChainSites"]]
    states = sum(c["reachableStates"] for c in certs)
    edges = sum(c["directedTransitions"] for c in certs)
    macros = {
        "StructureCount": release["structures"], "EpisodeCount": release["episodes"],
        "ProbeCount": release["probeResponses"], "StateCount": f"{states:,}",
        "EdgeCount": f"{edges:,}", "AirframeActions": air["fullOptimalActions"],
        "AirframeChain": air["mandatoryOrder"]["chainLengthParts"],
        "AirframeSourceChain": r" $\rightarrow$ ".join(map(str, source_chain)),
        "SemanticTests": summary["tests"], "RemovedParts": ", ".join(frames["removedIds"]),
        "InsertedPart": frames["inserted"]["partId"], "InsertionSite": frames["inserted"]["siteId"],
        "RepairActions": frames["structuralActions"],
    }
    (HERE / "generated.tex").write_text("".join(
        "\\newcommand{\\" + key + "}{" + str(value) + "}\n" for key, value in macros.items()))
    labels = {"roadster-body": "Roadster", "kart-deck": "Kart", "airframe": "Airframe"}
    table = [r"\begin{tabular}{llrrrrrr}\toprule",
             r"Case & Source group & Fixed/movable & States & Directed edges & Full actions & Chain parts & Repair detaches\\\midrule"]
    for cert in certs:
        table.append(f"{labels[cert['case']]} & {cert['provenanceGroup']} & "
                     f"{cert['fixedParts']}/{cert['movableSites']} & {cert['reachableStates']:,} & "
                     f"{cert['directedTransitions']:,} & {cert['fullOptimalActions']} & "
                     f"{cert['mandatoryOrder']['chainLengthParts']} & {cert['repairMinimumDetaches']}" + r"\\")
    table.append(r"\bottomrule\end{tabular}")
    (HERE / "case-table.tex").write_text("\n".join(table) + "\n")
    controls = [r"\begin{tabular}{lrr}\toprule", r"Controller & Complete & Repair\\\midrule"]
    for key, label in (("oracle", "Optimal oracle"), ("fault-and-recover", "Fault + recovery"),
                       ("attach-only", "Trap + attach only")):
        row = summary["controls"][key]
        controls.append(f"{label} & {fraction(row['successRate'])} & {fraction(row['recovery'])}" + r"\\")
    controls.append(r"\bottomrule\end{tabular}")
    (HERE / "control-table.tex").write_text("\n".join(controls) + "\n")

    rows = [
        "| Case | Fixed / movable | Reachable states | Directed edges | Full optimum | Chain parts / edges |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for c in certs:
        order = c["mandatoryOrder"]
        rows.append(f"| {c['case']} | {c['fixedParts']} / {c['movableSites']} | {c['reachableStates']:,} | "
                    f"{c['directedTransitions']:,} | {c['fullOptimalActions']} | "
                    f"{order['chainLengthParts']} / {order['dependencyDepthEdges']} |")
    case_table = "\n".join(rows)
    ledger = ["| Case | Mode | Installed | Optimal actions | Minimum detaches | Budget |",
              "| --- | --- | ---: | ---: | ---: | ---: |"]
    cf_rows = ["| Case | Goal member | Conditional costs | Optimal offered index |",
               "| --- | --- | --- | ---: |"]
    for _, tasks, _, cert in banks:
        for task in tasks["episodes"]:
            ledger.append(f"| {cert['case']} | {task['mode']} | {task['start'].bit_count()} | "
                          f"{task['optimalActions']} | {task['minimumDetaches']} | {task['budget']} |")
        for probe in tasks["counterfactual"]:
            for member in probe["members"]:
                cf_rows.append(f"| {cert['case']} | {member['id']} | "
                               f"{' / '.join(map(str, member['conditionalCosts']))} | {member['optimalChoices'][0]} |")
    (HERE / "APPENDIX.md").write_text(
        "# BrickPlan 1.1 — Technical appendix\n\n"
        "Generated from certified tasks and executed validation evidence, 2026-10-02.\n\n"
        "## Source bank and exact graph\n\n" + case_table + "\n\n"
        f"Total: {states:,} reachable states and {edges:,} directed transitions, across "
        f"{release['independentProvenanceGroups']} source groups. Roadster and kart share LEGO 31027; "
        "airframe uses LEGO 31028. No independent sample count is inferred from state counts.\n\n"
        f"Airframe mandatory source-index chain: {' → '.join(map(str, source_chain))}. "
        "This is private audit notation. Public part/site IDs are randomized.\n\n"
        "## Geometry contract\n\n"
        "All selected source poses and original render geometry are preserved. The airframe includes "
        "0–34 except 11–14 and 21–27; its fixed connected base is 1, 2, 5. "
        "It excludes the propeller, float/clip assemblies, and main wing plates. The upstream "
        "54383/54384 wing proxies have extensive nonmanifold and boundary edges; they are excluded "
        "without repair. Their dependent top plate 27 is also excluded. Sources 9, 10 and 15 "
        "remain at their original poses but now belong to the mutable task. Each included motion and endpoint pair "
        "is requalified using the frozen 1.0 geometry algorithm, not the old sampled discovery record.\n\n"
        f"Airframe: {air['endpointPairs']} endpoint pairs, {air['motionPairs']} motion pairs, "
        f"{air['blockedMotionPairs']} blocked paths, {air['unknownGeometry']} unknowns, "
        f"{air['connectorEdges']} stud connector edges, {len(air['goals'])} checked goal tables.\n\n"
        "The [1.0 appendix](../brickplan-v1/APPENDIX.md) remains normative for coordinate conversion, "
        "connector support, inset meshes, clearance covers, the source-verified 3022 repair, exact "
        "cost proofs, observation fields, and metric edge cases. Inset is 0.25 LDU per surface; "
        "guard is 0.002 LDU. No force, hand access, free rotation, or gravity claim is added.\n\n"
        "## Episode ledger\n\n" + "\n".join(ledger) + "\n\n"
        "Each start has a reachability witness. Every completion witness is replayed and cost-certified. "
        "Healthy/repair pairs match installed count and action budget.\n\n"
        "## Counterfactual conditional costs\n\n" + "\n".join(cf_rows) + "\n\n"
        "Indices above are canonical private candidate indices. Public positions are independently "
        "permuted. Both candidates are required in paired goals. The optimum is over the two "
        "offered closures, not all available actions.\n\n"
        "## Release binding and reproducibility\n\n"
        "`runtime.activate()` binds one process to the combined bank before importing executor "
        "modules. Original data and frontend code are relative read-only symlink dependencies. "
        "Banks are verified on first load and shared in memory; restart after rebuilding. "
        "The 1.0 files retain their frozen hashes. New data, figures, documents, and meshes are "
        "stored here. The freeze records both extension artifact hashes and the base manifest hash.\n\n"
        "Runtime: Python 3.11+ standard library; geometry/render generation additionally uses the "
        "same NumPy, meshlib, BrickNet, locked LDraw assets, Three.js and Playwright versions as 1.0. "
        "Document generation uses Pillow for margin-only crops of native replay screenshots. "
        "All source licenses are in ASSET-LICENSES.json.\n\n"
        "## Study boundary\n\n"
        "Supplied-plan conflict distances remain 1/2/4/8 with causal depth one. The larger mandatory "
        "assembly chain does not redefine that metric. This is still D1 diagnostic coverage. "
        "Software controls, browser replays and exhaustive states are not measured model or human trials.\n")
    (HERE / "VALIDATION.md").write_text(
        "# BrickPlan 1.1 validation\n\n"
        f"- Semantic: {summary['tests']} tests passed, including all goal tables and exact mandatory order.\n"
        f"- HTTP: {http['httpEpisodes']} episodes and {http['httpProbeResponses']} responses passed; "
        f"{http['restartRecoveredSessions']} sessions recovered after restart.\n"
        f"- Browser: {len(browser['completed'])} full/repair sessions passed through actual buttons; "
        "replay, exports, probe identity, desktop/mobile layout, and no page exceptions checked.\n"
        f"- Browser runtime: {browser['browser']}. Local Chrome launch timed out before navigation; "
        "the installed Firefox completed the suite.\n"
        f"- Geometry/graph: {states:,} states, {edges:,} directed transitions; no UNKNOWN geometry.\n"
        f"- Versioned CLI: oracle evaluation covers all {release['episodes']} episodes; release and transition "
        "certificates are bound to the report and checked during freezing.\n"
        "- Base preservation: every original 1.0 artifact hash checked.\n\n"
        "These are software validation controls. No paid model evaluation or human study was run.\n\n"
        "| Control | Complete success | Repair completion |\n| --- | ---: | ---: |\n"
        + "\n".join(f"| {key} | {fraction(row['successRate'])} | {fraction(row['recovery'])} |"
                    for key, row in summary["controls"].items())
        + "\n\nReports and screenshots: `tem/brickplan-v1.1/validation/`. "
        "The acceptance snapshot is packaged in `release-check.json`. "
        "See the protocol and appendix for physical and statistical limits.\n")
    (HERE / "README.md").write_text(
        "# BrickPlan 1.1\n\n"
        f"Executable assembly-order diagnostics: **{release['structures']} structures, "
        f"{release['independentProvenanceGroups']} source groups, {release['episodes']} episodes, "
        f"{release['probeResponses']} probe responses**. Adds a certified original LEGO 31028 "
        f"airframe with {air['fullOptimalActions']} full-build actions and a "
        f"{air['mandatoryOrder']['chainLengthParts']}-part mandatory chain. Frozen 1.0 remains unchanged.\n\n"
        + case_table + "\n\n"
        "All three repair starts require three removals. Seven dimensions retain the "
        "[metric contract](PROTOCOL.md): dead-end choice, lookahead, survival, regret, recovery, "
        "replanning efficiency and counterfactual consistency. This is a known-pose, straight-path "
        "D1 diagnostic release; no model/human performance is reported.\n\n"
        "[Paper PDF](paper.pdf) · [Paper source](paper.tex) · [Appendix](APPENDIX.md) · "
        "[Validation](VALIDATION.md) · [Release certificate](data/release.json)\n\n"
        "## Run\n\nFrom the repository root, Python 3.11+:\n\n```bash\n"
        "python3 benchmark/brickplan-v1.1/run.py serve --port 8767\n```\n\n"
        "Open **http://127.0.0.1:8767**. Select a task, assemble or detach by stable IDs, diagnose, "
        "then finish for scoring, trajectory export, feedback JSON and stepwise 3D replay. "
        "Only the target reference can be exploded. The installed assembly uses original source poses.\n\n"
        "In this workspace, replace `python3` with "
        "`env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python`.\n\n"
        "The [1.0 Client](../brickplan-v1/client.py) works with `Client('http://127.0.0.1:8767')`; "
        "the [API/action contract](../brickplan-v1/README.md#model-api) is unchanged. "
        "Use the 1.1 launcher for collection/evaluation:\n\n```bash\n"
        "python3 benchmark/brickplan-v1.1/run.py collect --store RUN_DIRECTORY "
        "--metadata METADATA_JSON --output SUBMISSION_JSON\n"
        "python3 benchmark/brickplan-v1.1/run.py evaluate SUBMISSION_JSON --output REPORT_JSON\n```\n\n"
        "Use a fresh store per controller. Repeated runs require explicit `--selection`. "
        "Policies must be isolated from local private certificates and post-trial review tools.\n\n"
        "## Reproduce\n\n```bash\n"
        "python3 benchmark/brickplan-v1.1/prepare.py assets\n"
        "python3 benchmark/brickplan-v1.1/run.py build --geometry\n"
        "python3 benchmark/brickplan-v1.1/run.py render\n"
        "python3 benchmark/brickplan-v1.1/prepare.py assets\n"
        "python3 benchmark/brickplan-v1.1/checks.py\n"
        "python3 benchmark/brickplan-v1.1/run.py evaluate "
        "tem/brickplan-v1.1/validation/oracle.submission.json "
        "--output tem/brickplan-v1.1/validation/oracle.cli-report.json\n"
        "python3 benchmark/brickplan-v1.1/check_http.py\n"
        "# Start a fresh 1.1 server on port 8767, then:\n"
        "python3 benchmark/brickplan-v1.1/prepare.py fixtures\n"
        "BRICKPLAN_BROWSER=firefox node benchmark/brickplan-v1.1/check_browser.mjs\n"
        "python3 benchmark/brickplan-v1.1/documents.py\n"
        "python3 benchmark/brickplan-v1.1/freeze.py\n```\n\n"
        "The shared runtime is imported from `../brickplan-v1`; keep both directories together. "
        "Only new cases are rebuilt. Existing 1.0 data are read-only references. "
        "A running process caches its certified bank; restart it after rebuilding.\n\n"
        "Original LDraw geometry/attributions: [ASSET-LICENSES.json](ASSET-LICENSES.json). "
        "Kinematic proxy certificates do not certify clutch force, gravity, hand access, or "
        "all continuous assembly paths. Free-camera browser practice is not a matched vision-only trial.\n")
    tectonic = shutil.which("tectonic") or str(ROOT / "benchmark/.runtime/tectonic")
    subprocess.run([tectonic, "--keep-logs", "--outdir", str(OUT), "paper.tex"], cwd=HERE, check=True)
    shutil.copyfile(OUT / "paper.pdf", HERE / "paper.pdf")


if __name__ == "__main__":
    main()
