#!/usr/bin/env python3
"""Deterministic Phase 2 contract, descriptive and review-queue exports."""
import argparse
import csv
import hashlib
import io
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "benchmark/ldraw-v2"
OUT = DATA / "descriptive-analysis"
PAPER = ROOT / "benchmark/paper"
MOD = {"visual": "V", "source-data": "S", "connector-graph": "G", "scene-edit": "E"}
LAYER = {"atomic": "A", "metacognitive": "M", "procedural": "P", "graph-internal": "GI"}
# category, operation, validity boundary, legacy paper lines, marker
SPEC = {
    "color": ("Perception", "Bind the target B-number in the image; identify its source color name.",
              "Source color equality is an oracle, not proof of perceptual distinguishability.", "244--246", ""),
    "shape-match": ("Perception", "Bind target and candidates in the image; match the source part type while ignoring color and pose.",
                    "Near-identical source types require human adjudication; no unseen geometry is inferred.", "244--246,531--532", ""),
    "distance": ("Evidence reading / arithmetic", "Read supplied bounding-box centers, compute Euclidean distance, select the unique minimum.",
                 "Coordinates are explicit, not visually estimated. Candidates are hash sampled, not nearest spatial neighbors.", "245--247", "control"),
    "interface": ("Evidence reading", "Read connectorRecord.family and select the identical label.",
                  "An explicit record-reading control, not contact perception or load-capacity reasoning.", "247--249", "control"),
    "neighbors": ("Graph operation", "Collect candidate labels joined to the target by any supplied undirected edge; deduplicate.",
                  "One-hop set extraction within the recognized graph, not physical connectivity discovery.", "251--257", ""),
    "graph-removal": ("Graph operation", "Delete the named vertex and incident edges; count connected components including remaining isolated vertices.",
                      "An operation within a supplied local graph; no extraction trajectory or cross-contract chain.", "252--256", ""),
    "coverage": ("Evidence reading", "Select the sole row whose supplied supported flag is false.",
                 "A definition-coverage control; unsupported does not imply floating or disconnected.", "256--257", "control"),
    "evidence-limit": ("Evidence scope control", "Select Not established by this evidence for the stated gravitational-stability claim.",
                       "The semantic answer is constant; accuracy alone is not reasoning evidence.", "258--259,388--390", "constant"),
    "source-step": ("Evidence reading / lookup", "Find the target label in the supplied author-step table; select the smallest matching expanded index.",
                    "Table lookup; source order is not evidence of collision-free assembly.", "270--277", "control"),
    "source-sequence": ("Execution contract", "Follow the public predecessor facts and reveal the supplied author window in order.",
                        "A small explicit fact chain, not mechanical planning; the current six-step response template is constant.", "270--274", "template"),
    "restore-instance": ("Execution contract", "Choose the restore action whose missing fact holds; execute it within budget and satisfy all goals.",
                         "One visibility edit at an original source pose, not insertion-feasibility planning.", "301--308,529--530", ""),
}
NAMES = {"color": "Color", "shape-match": "Part type", "distance": "Distance", "interface": "Interface",
         "neighbors": "Neighbors", "graph-removal": "Graph deletion", "coverage": "Coverage",
         "evidence-limit": "Evidence limit", "source-step": "Step lookup", "source-sequence": "Step sequence",
         "restore-instance": "Restoration"}


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")


def correlation(xs, ys):
    ax, ay = sum(xs) / len(xs), sum(ys) / len(ys)
    denom = math.sqrt(sum((x-ax)**2 for x in xs) * sum((y-ay)**2 for y in ys))
    return sum((x-ax)*(y-ay) for x, y in zip(xs, ys)) / denom if denom else None


def ranks(xs):
    ordered = sorted(xs)
    return [(ordered.index(x) + len(ordered) - ordered[::-1].index(x) + 1) / 2 for x in xs]


def response_semantics(t):
    """Source-scope instance labels; do not equate B0001 across different sets."""
    a = t["answer"]
    options = {o["id"]: o["label"] for o in t.get("options", [])}
    if "choiceId" in a:
        value = options[a["choiceId"]]
    elif "choiceIds" in a:
        value = sorted(options[k] for k in a["choiceIds"])
    elif "value" in a:
        value = a["value"]
    else:
        value = a["actionIds"]
    if re.search(r"B\d{4,}", json.dumps(value)):
        value = {"source": t["modelId"], "response": value}
    return json.dumps(value, sort_keys=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true", help="Compare all generated outputs with existing bytes.")
    args = parser.parse_args()
    catalog = read(DATA / "catalog.json")
    bundles = [read(ROOT / f"public/benchmark/ldraw-v2/models/{e['id']}.json") for e in catalog]
    tasks = [t for b in bundles for t in b["tasks"]]
    audits = read(DATA / "task-audit.json")["tasks"]
    assert len(tasks) == len(audits) == 617 and len(bundles) == 24
    assert {t["family"] for t in tasks} == set(SPEC)
    paths = [OUT / n for n in ["analysis.json", "band-modality.csv", "answer-concentration.csv"]]
    paths += [DATA / "TASK_CONTRACTS.md", DATA / "task-contracts.json", DATA / "human-review-queue.json",
              PAPER / "ldraw-v2-operators.tex", PAPER / "ldraw-v2-band-modality.tex"]
    old = {p: p.read_bytes() for p in paths} if args.verify else {}
    cross = {band: {m: 0 for m in MOD.values()} for band in ["D1", "D2", "D3", "D4"]}
    families = defaultdict(list)
    for t in tasks:
        cross[t["difficulty"]][MOD[t["modality"]]] += 1
        families[t["family"]].append(t)
    # Independent aggregation from per-source membership.
    independent = Counter((e["difficulty"], MOD[t["modality"]]) for e, b in zip(catalog, bundles) for t in b["tasks"])
    assert all(cross[b][m] == independent[b, m] for b in cross for m in MOD.values())
    concentration = {}
    contracts = []
    cards = [
        "# LDraw-2 task contracts", "",
        "No family currently requires chaining two observation contracts within a single item; "
        "the benchmark measures modular competencies separately.",
        "",
        "Counts below are computed from all 617 frozen items. Model requests contain only the "
        "fixed system prompt, English question, format, necessary input, anonymous options, and "
        "image bytes for V. Internal source oracles do not certify human perceptual validity.",
        "",
        "Known deterministic shortcuts S1--S4 were repaired (see PHASE-1-REPORT.md). "
        "Answer priors and the constant six-step program remain explicit limitations. "
        "No claim of universal shortcut absence is made. Instance answers are source-scoped "
        "when calculating semantic concentration; equal B-numbers in different sets are not equated.",
        "",
    ]
    tex = [r"\begin{tabularx}{\textwidth}{lrrllXXX}", r"\toprule",
           r"Family & $N$ & Layer & Input & Measurement & Direct operation & Required evidence & Shortcut control\\\midrule"]
    for family in SPEC:
        ts = families[family]
        category, operation, boundary, lines, marker = SPEC[family]
        counts = Counter(response_semantics(t) for t in ts)
        majority, maximum = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[0]
        constant = maximum == len(ts)
        concentration[family] = {"n": len(ts), "majority": json.loads(majority), "majorityCount": maximum,
                                 "majorityShare": maximum / len(ts), "constantResponse": constant,
                                 "distribution": dict(sorted(counts.items())),
                                 "interpretation": "Descriptive in-corpus prior, not a held-out model result."}
        inputs = [read(ROOT / f"public/benchmark/ldraw-v2/inputs/{e['id']}.json") for e in catalog]
        publics = [t for b in inputs for t in b["tasks"] if t["family"] == family]
        fields = sorted({k for t in publics for k in t["input"]})
        assert all(sorted(t["input"]) == fields for t in publics)
        if family == "interface":
            detailed = "connectorRecord.{family,aConnector,bConnector}; scope"
        elif family == "coverage":
            detailed = "coverage[].{label,supported}"
        elif family == "source-step":
            detailed = "steps[].{index,numbers}; provenance"
        elif ts[0]["format"] == "actions":
            detailed = "initialFacts; goalFacts; absentFacts; budget; actions[].{id,label,requires,forbids?,adds,deletes,cost}; editMode"
        else:
            detailed = ", ".join(fields) or "{}"
        if ts[0]["modality"] == "visual":
            detailed += "; visualInput.numberedView supplies a frozen operand-isolation PNG; isolationAllowed=true"
        rule = {"single-choice": "Exact anonymous choiceId of the semantic answer.",
                "multiple-choice": "Exact set of choiceIds; order ignored; duplicate IDs invalid.",
                "integer": "A safe JSON integer value exactly equal to the independent component count.",
                "actions": "String actionIds; legal full replay under prerequisites, forbids and budget; all goal facts and no prohibited facts."}[ts[0]["format"]]
        residual = "No known deterministic S1--S4 request shortcut; semantic priors reported separately."
        if constant:
            residual += " Constant semantic answer." if family == "evidence-limit" else " Identical six-step action program in this release."
        contract = dict(family=family, name=NAMES[family], n=len(ts), modality=ts[0]["modality"],
                        layer=ts[0]["layer"], format=ts[0]["format"], inputFields=fields,
                        publicInput=detailed, operation=operation, scoring=rule, classification=category,
                        constantAnswer=constant, marker=marker, knownShortcuts=residual,
                        constructValidity=boundary, legacyPaperLocation=f"main.tex:{lines}",
                        v2PaperLocation="main-v2.tex:sec:contracts")
        assert all(t["layer"] == contract["layer"] and t["modality"] == contract["modality"] for t in ts)
        contracts.append(contract)
        cards += [f"## {NAMES[family]} ({family})", ""]
        for k, label in [("n", "Count"), ("modality", "Observation contract"), ("layer", "Layer"),
                         ("publicInput", "Exact public input"), ("operation", "Required operation"),
                         ("scoring", "Scoring"), ("classification", "Measurement category"),
                         ("constantAnswer", "Constant response"), ("knownShortcuts", "Known shortcuts / priors"),
                         ("constructValidity", "Construct validity"), ("legacyPaperLocation", "Legacy paper location"),
                         ("v2PaperLocation", "V2 paper location")]:
            cards.append(f"- **{label}:** {contract[k]}")
        cards += [""]
        symbol = {"constant": r"$^\dagger$", "control": r"$^\ddagger$", "template": r"$^\ast$"}.get(marker, "")
        short_op = {"color": "Identify color", "shape-match": "Match type", "distance": "Euclidean minimum",
                    "interface": "Read family", "neighbors": "One-hop set", "graph-removal": "Delete; count components",
                    "coverage": "Read support flag", "evidence-limit": "Fixed scope answer", "source-step": "First index lookup",
                    "source-sequence": "Follow predecessor chain", "restore-instance": "Restore visibility"}[family]
        evidence = {"V": "Numbered operand image", "S": "Supplied source fields", "G": "Record / local edges",
                    "E": "Facts and actions"}[MOD[ts[0]["modality"]]]
        control = {"graph-removal": "Integer response", "source-step": "Legal balanced ranks",
                   "shape-match": "No reference order", "neighbors": "No reference order",
                   "interface": "Five fixed options", "evidence-limit": "Report fixed prior",
                   "source-sequence": "Report fixed program"}.get(family, "Request whitelist")
        tex.append(f"{NAMES[family]}{symbol} & {len(ts)} & {LAYER[ts[0]['layer']]} & {MOD[ts[0]['modality']]} & "
                   f"{category} & {short_op} & {evidence} & {control}" + r"\\")
    tex += [r"\bottomrule", r"\end{tabularx}"]
    assert concentration["evidence-limit"]["majorityShare"] == 1
    # Reuse: exact operand sets and shared focal targets are different measurements.
    reuse = []
    focal_families = {"color", "shape-match", "distance", "restore-instance"}
    for e, b in zip(catalog, bundles):
        ts = b["tasks"]
        sets = Counter(tuple(sorted(r["id"] for r in t["references"])) for t in ts if t["references"])
        target_families = defaultdict(set)
        focal = [t for t in ts if t["family"] in focal_families]
        for t in focal:
            target_families[t["targetModule"]].add(t["family"])
        repeated = sum(n for n in sets.values() if n > 1)
        pairs = sum(n*(n-1)//2 for n in sets.values())
        reuse.append({"source": e["id"], "tasks": len(ts), "parts": e["parts"],
                      "nonemptyOperandTasks": sum(sets.values()), "tasksSharingExactOperandSet": repeated,
                      "exactOperandPairMatches": pairs, "allTaskPairs": len(ts)*(len(ts)-1)//2,
                      "focalFamilyTasks": len(focal), "distinctFocalTargets": len(target_families),
                      "focalTasksWithTargetUsedByOtherFamily": sum(len(target_families[t["targetModule"]]) > 1 for t in focal),
                      "targetFamilyCounts": {k: len(v) for k, v in sorted(target_families.items())}})
    graph = families["graph-removal"]
    graph_sizes = {"nodes": dict(sorted(Counter(len(t["input"]["nodes"]) for t in graph).items())),
                   "simpleEdges": dict(sorted(Counter(len({tuple(sorted(e)) for e in t["input"]["edges"]}) for t in graph).items()))}
    analysis = {
        "version": "brickatlas-ldraw-2", "tasks": len(tasks), "sources": len(catalog),
        "bandModality": cross, "answerConcentration": concentration, "redundancyBySource": reuse,
        "redundancyTotals": {k: sum(r[k] for r in reuse) for k in [
            "nonemptyOperandTasks", "tasksSharingExactOperandSet", "exactOperandPairMatches", "allTaskPairs",
            "focalFamilyTasks", "distinctFocalTargets", "focalTasksWithTargetUsedByOtherFamily"]},
        "sourceSizeTaskCorrelation": {
            "pearson": correlation([r["parts"] for r in reuse], [r["tasks"] for r in reuse]),
            "spearman": correlation(ranks([r["parts"] for r in reuse]), ranks([r["tasks"] for r in reuse])),
            "interpretation": "Size-dependent sampling and evidence availability generate this association; no cognitive difficulty inference."},
        "graphDeletionLocalSize": graph_sizes,
        "singleChoicePriors": {
            "n": sum(t["format"] == "single-choice" for t in tasks),
            "alwaysACorrect": sum(t["answer"].get("choiceId") == "A" for t in tasks),
            "uniformExpected": sum(1/len(t["options"]) for t in tasks if t["format"] == "single-choice") / sum(t["format"] == "single-choice" for t in tasks)},
        "limits": ["D bands index source size, not measured item difficulty.",
                   "Majority proportions use this release, not a training split.",
                   "No model inference or human certification is reported."]}
    write(OUT / "analysis.json", analysis)
    write(DATA / "task-contracts.json", {"contracts": contracts})
    (DATA / "TASK_CONTRACTS.md").write_text("\n".join(cards))
    (PAPER / "ldraw-v2-operators.tex").write_text("\n".join(tex) + "\n")
    bandtex = [r"\begin{tabular}{lrrrrr}", r"\toprule", r"Band & V & S & G & E & Total\\\midrule"]
    for band, row in cross.items():
        bandtex.append(f"{band} & " + " & ".join(str(n) for n in row.values()) + f" & {sum(row.values())}" + r"\\")
    bandtex += [r"\bottomrule", r"\end{tabular}"]
    (PAPER / "ldraw-v2-band-modality.tex").write_text("\n".join(bandtex) + "\n")
    for name, rows in [
        ("band-modality.csv", [["band", *MOD.values(), "total"]] + [[b, *r.values(), sum(r.values())] for b, r in cross.items()]),
        ("answer-concentration.csv", [["family", "n", "majority", "count", "share"]] +
         [[f, r["n"], json.dumps(r["majority"]), r["majorityCount"], r["majorityShare"]] for f, r in concentration.items()])]:
        buf = io.StringIO(newline="")
        csv.writer(buf).writerows(rows)
        (OUT / name).write_text(buf.getvalue())
    queue = []
    for t in audits:
        amb = t["ambiguity"]
        reasons = []
        if t["modality"] == "visual":
            reasons += ["label-readability", "color-discriminability" if t["family"] == "color" else "near-identical-shape"]
        if amb["unsupportedOperands"]:
            reasons.append("unsupported-operand")
        if amb["incidentIntersectionCandidates"]:
            reasons.append("incident-intersection-candidate")
        if reasons:
            queue.append({"taskId": t["id"], "sourceId": t["sourceId"], "reasons": reasons,
                          "status": "pending", "reviewer": None, "decision": None, "rationale": None,
                          "views": {"standard": t["publicInput"].get("visualInput", {}).get("numberedView")}})
    write(DATA / "human-review-queue.json", {
        "version": "brickatlas-ldraw-2", "status": "pending", "humanReviewsCompleted": 0, "items": queue,
        "physicalPairQueue": "source-audit.json plus per-source internal audit intersections; 573 candidates, no physical certification"})
    if args.verify:
        assert all(p.read_bytes() == old[p] for p in paths), "Non-reproducible descriptive output"
    print(json.dumps({"status": "passed", "contracts": len(contracts), "bandModality": cross,
                      "graphDeletion": concentration["graph-removal"], "reuse": analysis["redundancyTotals"],
                      "correlations": analysis["sourceSizeTaskCorrelation"], "humanQueue": len(queue),
                      "constantResponses": [f for f, v in concentration.items() if v["constantResponse"]],
                      "reproduced": args.verify}, indent=2))


if __name__ == "__main__":
    main()
