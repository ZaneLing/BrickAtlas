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
from matched_metrics import HISTORICAL, PRIMARY, SPLITS, visual_pair_definitions
from mission import Action, State, canonical_hash
from source_inputs import registry_path
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


def tex(value):
    escapes = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
               "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
               "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
               "•": r"\textbullet{}"}
    return "".join(escapes.get(c, c) for c in str(value))


def number(value, places=0):
    return "---" if value is None else f"{value:,.{places}f}"


def percent(value):
    return "---" if value is None else f"{100 * value:.1f}\\%"


def extent(values):
    values = list(values)
    return f"{min(values)}--{max(values)}" if values else "---"


def table(name, columns, header, rows, long=False):
    env = "longtable" if long else "tabular"
    text = [rf"\begin{{{env}}}{{{columns}}}\toprule", header + r"\\\midrule"]
    if long:
        text += [r"\endfirsthead", r"\toprule", header + r"\\\midrule\endhead",
                 r"\midrule\endfoot", r"\bottomrule\endlastfoot"]
    text += [" & ".join(map(str, row)) + r"\\" for row in rows]
    text += [rf"\end{{{env}}}" if long else r"\bottomrule\end{tabular}"]
    (HERE / name).write_text("\n".join(text) + "\n")


def persist_evidence():
    # Archive exact earlier results, never regenerate or invent policy records.
    audit = DATA / "predecessor-static-audit.json"
    if not audit.exists():
        audit.write_bytes((RESEARCH / "static-audit.json").read_bytes())
    records = DATA / "software-control-records.json.gz"
    if not records.exists():
        raise FileNotFoundError("Run controls.py before generating the release documents")


def publication_inputs(bank):
    """Fail closed on stale or partially generated evidence before any writes."""
    paths = {
        "certificate": DATA / "certificate.json", "quality": DATA / "quality.json",
        "controls": DATA / "software-controls.json", "matched": DATA / "matched-controls.json",
        "sourceAudit": DATA / "source-question-audit.json",
        "observations": DATA / "observation-certificate.json",
        "upgrade": DATA / "upgrade-audit.json", "admission": DATA / "source-admission.json",
        "render": DATA / "render-provenance.json", "plan": HERE / "source-plan.json",
        "independent": DATA / "independent-audit/summary.json",
        "semantic": DATA / "semantic-validation.json",
    }
    evidence = {key: json.loads(path.read_text()) for key, path in paths.items()}
    digest = canonical_hash(bank)
    for key in ("controls", "matched", "sourceAudit", "observations", "upgrade", "independent", "semantic"):
        if evidence[key].get("bankHash") != digest:
            raise ValueError(f"{paths[key]} does not identify the final bank")
    if evidence["certificate"]["tasksHash"] != digest:
        raise ValueError("Stale exact certificate")
    audit, obs = evidence["sourceAudit"], evidence["observations"]
    if not audit["passed"] or audit["questionsChecked"] != len(bank["episodes"]) + len(bank["probes"]):
        raise ValueError("The final source/question audit is incomplete")
    independent = evidence["independent"]
    if (not evidence["upgrade"]["passed"] or not evidence["semantic"]["passed"]
            or independent["rows"] != audit["questionsChecked"]
            or independent["passed"] != independent["rows"]
            or independent["failures"] or independent["pairFailures"]
            or independent["tableMismatches"]
            or independent["pairCount"] != len(bank["pairs"])
            or independent["tableCount"] != len(evidence["certificate"]["oracles"])
            or independent["tableStates"] != sum(c["productStates"] for c in evidence["certificate"]["oracles"].values())):
        raise ValueError("The independent all-answer or upgrade audit is incomplete")
    if not obs["complete"] or obs["identitySeed"] != 0 or not all(p["passed"] for p in obs["pairs"]):
        raise ValueError("The final native observation audit is incomplete")
    expected = {p["id"] for p in bank["pairs"] if p["kind"] == "visual-geometry"}
    if {p["pairId"] for p in obs["pairs"]} != expected:
        raise ValueError("Observation audit does not cover every visual pair")
    if any(r["unequalPairIds"] for r in evidence["matched"]["matchingContractAudit"].values()):
        raise ValueError("A primary pair fails the reduced-input matching contract")
    for key in ("controls", "matched"):
        if (evidence[key]["visualModelResults"] is not None
                or evidence[key]["humanResults"] is not None):
            raise ValueError("Population evidence requires a separate publication protocol")
    plan = evidence["plan"]
    if evidence["admission"]["planHash"] != canonical_hash(plan):
        raise ValueError("Stale source admissions")
    registry = registry_path(plan)
    evidence["registry"] = json.loads(registry.read_text())["candidates"]
    paths["registry"] = registry
    if (hashlib.sha256((HERE / "arena/meshes.json").read_bytes()).hexdigest()
            != evidence["render"]["assetSha256"]):
        raise ValueError("Display meshes differ from their provenance")
    quality = evidence["quality"]
    if (quality["episodes"] != len(bank["episodes"]) or quality["probes"] != len(bank["probes"])
            or any(quality[k] != v for k, v in bank["qualitySummary"].items())):
        raise ValueError("Stale quality summary")
    evidence["inputHashes"] = {
        str(path.relative_to(HERE)) if path.is_relative_to(HERE) else str(path.relative_to(ROOT)):
        hashlib.sha256(path.read_bytes()).hexdigest() for path in paths.values()}
    return evidence


def publication_summary(bank, evidence):
    episodes, probes = bank["episodes"], bank["probes"]
    cert, quality, controls = (evidence[k] for k in ("certificate", "quality", "controls"))
    bases = [p for p in bank["profiles"] if p["sampling"] != "geometry-contrast"]
    new_bases = [p for p in bases if p.get("introducedVersion") == "2.3"]
    pair_rows = visual_pair_definitions(bank)
    primary = [p for p in pair_rows if p["evaluationCohort"] == PRIMARY]
    specs = [s for s in bank["geometryCensus"]["pairs"] if s["evaluationCohort"] == PRIMARY]
    registry = {r["id"]: r for r in evidence["registry"]}
    admissions = [s for s in evidence["admission"]["sources"] if s["model"] in registry]
    if len(admissions) != len(registry) or len({s["model"] for s in admissions}) != len(registry):
        raise ValueError("Candidate admission census is incomplete")
    if not new_bases or any(min(p["registeredSites"], p["reachableMovableSites"]) < 8 for p in new_bases):
        raise ValueError("New primary sources must have eight registered and reachable sites")
    repairs = [p for p in probes if p["kind"] == "delayed-repair"]
    choices = [p for p in probes if p["kind"] == "next-action"]
    kinds = Counter(p["kind"] for p in probes)
    pair_kinds = Counter(p["kind"] for p in bank["pairs"])
    sampling = evidence["plan"]["newEpisodeSampling"]
    sampled = [t for t in episodes if t["profile"] in {p["id"] for p in new_bases}]
    expected_per_source = sampling["goalsPerProfile"] * len(sampling["jobCounts"]) * sampling["startsPerMission"]
    if any(sum(t["profile"] == p["id"] for t in sampled) != expected_per_source for p in new_bases):
        raise ValueError("New source sampling is incomplete; publish attrition before proceeding")
    stats = {
        "EpisodeCount": len(episodes), "ProbeCount": len(probes), "PairCount": len(bank["pairs"]),
        "QuestionCount": len(episodes) + len(probes),
        "SourceCount": len({t["sourceGroup"] for t in episodes}),
        "ProfileCount": len(bank["profiles"]), "OracleCount": len(cert["oracles"]),
        "BaseProfileCount": len(bases), "ContextProfileCount": len(bank["profiles"]) - len(bases),
        "ZeroYieldProfileCount": len({p["id"] for p in bank["profiles"]} - {t["profile"] for t in episodes}),
        "NewSourceCount": len({p["sourceGroup"] for p in new_bases}),
        "CandidateCount": len(admissions), "AdmittedCount": sum(s["qualified"] for s in admissions),
        "RejectedCount": sum(not s["qualified"] for s in admissions),
        "NewSampledEpisodeCount": len(sampled), "GoalsPerSource": sampling["goalsPerProfile"],
        "JobSettingsPerSource": len(sampling["jobCounts"]), "StartsPerMission": sampling["startsPerMission"],
        "EpisodesPerNewSource": expected_per_source,
        "PrimaryPairCount": len(primary),
        "PrimarySourceCount": len({p["sourceGroup"] for p in primary}),
        "PrimaryInterventionCount": len({(p["sourceGroup"], p["interventionId"]) for p in primary}),
        "PrimaryStartCount": len({(p["sourceGroup"], p["interventionId"], p["startId"]) for p in primary}),
        "HistoricalPairCount": sum(p["evaluationCohort"] == HISTORICAL for p in pair_rows),
        "QualifiedInterventionCount": len(specs),
        "ZeroYieldInterventionCount": sum(not s["retainedFutureContrasts"] for s in specs),
        "ContextSubsetCount": sum(r.get("candidateSubsets", 0) for r in bank["geometryCensus"]["census"]),
        "MatchedOptionCount": sum(r.get("matchedCandidatePairs", 0) for r in bank["geometryCensus"]["census"]),
        "ProductCount": sum(c["productStates"] for c in cert["oracles"].values()),
        "EdgeCount": sum(c["directedTransitions"] for c in cert["oracles"].values()),
        "MaxGap": max(t["relaxationGap"] for t in episodes),
        "OldLabels": sum(x["checked"] for x in json.loads((DATA / "predecessor-static-audit.json").read_text())),
        "CalibrationCount": len(quality["calibration"]),
        "DiscriminativeCount": quality["discriminative"],
        "ProblemCount": quality["independentProblems"], "RepeatedRowCount": quality["duplicateExcess"],
        "NextActionCount": kinds["next-action"], "ContinuationCount": kinds["continuation"],
        "GeometryQuestionCount": kinds["geometry-continuation"],
        "AppearanceQuestionCount": kinds["appearance-continuation"], "RepairCount": len(repairs),
        "SequencePairCount": pair_kinds["interior-order"],
        "AppearancePairCount": pair_kinds["appearance-invariant"],
        "SequencePairsPerBin": bank["continuationCensus"]["selectedPairsPerBin"],
        "RepairMin": min(p["minimumRepairCost"] for p in repairs),
        "RepairMax": max(p["minimumRepairCost"] for p in repairs),
        "InverseCorrect": sum(p["inverseLastControl"]["correct"] for p in repairs),
        "InverseSuboptimal": sum(p["recoveryCohort"] == "inverse-suboptimal" for p in repairs),
        "InverseUnavailable": sum(p["recoveryCohort"] == "inverse-unavailable" for p in repairs),
        "DepthOneContainsOptimal": quality["depthOne"]["containsOptimal"],
        "MeshCount": evidence["render"]["parts"], "TriangleCount": evidence["render"]["triangles"],
        "PolicyRuns": controls["policies"]["relaxed-greedy"]["all"]["assigned"],
        "RawPolicyRuns": sum(v["all"]["assigned"] for v in controls["policies"].values()),
    }
    for split, prefix in zip(SPLITS, ("Development", "Heldout")):
        tasks = [t for t in episodes if t["split"] == split]
        pairs = [p for p in primary if p["split"] == split]
        stats.update({prefix + "EpisodeCount": len(tasks),
                      prefix + "SourceCount": len({t["sourceGroup"] for t in tasks}),
                      prefix + "PrimaryPairCount": len(pairs),
                      prefix + "PrimarySourceCount": len({p["sourceGroup"] for p in pairs})})
    for key, prefix in (("relaxed-greedy", "Greedy"), ("capacity-dispatch", "Dispatch"),
                        ("astar-100", "BoundedSmall"), ("astar-1000", "BoundedLarge"),
                        ("astar-500000", "FullSearch")):
        row = controls["policies"][key]["all"]
        stats.update({prefix + "Completed": row["completed"], prefix + "Assigned": row["assigned"],
                      prefix + "Optimal": row["optimalCompletions"],
                      prefix + "MaxExpansions": row["maximumExpansions"],
                      prefix + "MedianExpansions": row["medianExpansions"]})
    horizon = [{
        "depth": depth, "decisions": len(choices),
        "pessimistic": sum(p["horizonEvidence"][str(depth)]["allOptimal"] for p in choices),
        "optimistic": sum(p["horizonEvidence"][str(depth)]["anyOptimal"] for p in choices),
        "uniformTieMean": sum(p["horizonEvidence"][str(depth)]["optimalFractionUnderUniformTies"]
                              for p in choices) / len(choices) if choices else None}
        for depth in (1, 2, 4, 8)]
    admission_rows = [
        {"model": r["model"], "qualified": r["qualified"],
         "exclusionStage": r.get("exclusionStage"), "reason": r.get("reason"),
         "qualificationAttempts": len(r.get("attempts", [])),
         "rejectedInstances": len(r.get("rejectedInstances", []))}
        for r in admissions]
    return {"schema": "brickplan-publication-statistics/2.3", "bankHash": canonical_hash(bank),
            "inputHashes": evidence["inputHashes"], "counts": stats,
            "byTier": Counter(t["tier"] for t in episodes), "horizonSelectedProbes": horizon,
            "probeKinds": kinds, "pairKinds": pair_kinds, "visualPairs": pair_rows,
            "admissions": admission_rows, "geometryAttrition": bank["geometryCensus"]["census"],
            "recoveryCohorts": Counter(p["recoveryCohort"] for p in repairs),
            "repairCostHistogram": Counter(p["minimumRepairCost"] for p in repairs),
            "repairLagHistogram": Counter(p["lagAfterError"] for p in repairs),
            "episodeDescriptors": {
                name: Counter(value(t) for t in episodes) for name, value in (
                    ("optimalOperations", lambda t: t["optimalCost"]),
                    ("registeredSites", lambda t: t["descriptors"]["registeredSites"]),
                    ("rackCapacity", lambda t: t["capacity"]),
                    ("jobCount", lambda t: len(t["jobs"])),
                    ("relaxationGap", lambda t: t["relaxationGap"]))},
            "observationCohorts": {
                cohort: {
                    "pairs": len(ids),
                    "pixelDistinct": sum(r["passed"] for r in evidence["observations"]["pairs"]
                                         if r["pairId"] in ids),
                    "isometricAmbiguous": sum(r["activeDefaultAmbiguous"]
                                              for r in evidence["observations"]["pairs"] if r["pairId"] in ids)}
                for cohort in (PRIMARY, HISTORICAL)
                for ids in [{p["pairId"] for p in pair_rows if p["evaluationCohort"] == cohort}]},
            "bySampling": Counter(t["sampling"] for t in episodes)}


def tables(bank, evidence, summary):
    episodes, probes = bank["episodes"], bank["probes"]
    controls, quality = evidence["controls"], evidence["quality"]
    stats, horizon = summary["counts"], summary["horizonSelectedProbes"]
    commands = {k: number(v) for k, v in stats.items()}
    commands.update(
        InverseAccuracy=percent(quality["inverseLast"]["accuracy"]["value"]),
        DepthOneUniform=percent(quality["depthOne"]["uniformTieExpectedAccuracy"]["value"]),
        UniformCandidateAccuracy=percent(quality["depthOne"]["uniformAllCandidates"]["value"]),
        PrefixZeroAccuracy=percent(evidence["upgrade"]["prefixReplayControl"]["0"]["accuracy"]))
    for key, prefix in (("2", "PrefixTwo"), ("5", "PrefixFive")):
        row = evidence["upgrade"]["prefixReplayControl"][key]
        commands[prefix + "Correct"] = number(row["correct"])
        commands[prefix + "Total"] = number(row["total"])
    (HERE / "generated.tex").write_text("\n".join(
        rf"\newcommand{{\{k}}}{{{v}}}" for k, v in commands.items()) + "\n")
    titles = {r["kit"]: r["title"] for r in evidence["registry"]}
    table("sources.tex", "p{.32\\textwidth}llrrrr",
          "Admitted subassembly & Kit & Split & Parts & Sites & Movable & Episodes", [
              [tex(titles.get(p["sourceGroup"], p["title"])), tex(p["sourceGroup"]),
               "Dev." if p["split"] == "development" else "Held out",
               p["sourceParts"], p["registeredSites"], p["reachableMovableSites"],
               sum(t["profile"] == p["id"] for t in episodes)]
              for p in bank["profiles"] if p["sampling"] != "geometry-contrast"], long=True)
    table("source-controls.tex", "lrrrr", "Partition & Sources & Episodes & Greedy & Full A*", [
        [split.replace("heldout-source", "Held-out source").replace("development", "Development"),
         len({t["sourceGroup"] for t in episodes if t["split"] == split}),
         sum(t["split"] == split for t in episodes),
         percent(controls["policies"]["relaxed-greedy"]["bySplit"][split]["successRate"]),
         percent(controls["policies"]["astar-500000"]["bySplit"][split]["successRate"])]
        for split in ("development", "heldout-source")])
    table("controls-table.tex", "lrrrrr",
          "Control & Runs & Success & Optimal & Regret & Max exp.", [
              [label, (r := controls["policies"][key]["all"])["assigned"], r["completed"],
               r["optimalCompletions"], number(r["meanSuccessfulRegret"], 2),
               number(r["maximumExpansions"]) if "astar" in key else "---"]
              for key, label in zip(ORDER, NAMES)])
    table("tiers.tex", "lrrrr", r"Tier & Episodes & $C^*$ range & Gap range & A* max", [
        [tier, summary["byTier"][tier],
         extent(t["optimalCost"] for t in episodes if t["tier"] == tier),
         extent(t["relaxationGap"] for t in episodes if t["tier"] == tier),
         number(max((t["astarClosureExpansionsSeed0"] for t in episodes if t["tier"] == tier), default=None))]
        for tier in ("D1", "D2", "D3", "D4")])
    table("horizon.tex", "rrrrr",
          r"Depth & Choices & \shortstack{All\\optimal} & \shortstack{Any\\optimal} & \shortstack{Uniform\\tie}", [
        [r["depth"], r["decisions"], r["pessimistic"], r["optimistic"], percent(r["uniformTieMean"])]
        for r in horizon])
    table("tier-controls.tex", "lrrrr", "Control & D1 & D2 & D3 & D4", [
        [label] + [f'{(r := controls["policies"][key]["byTier"][tier])["completed"]}/{r["assigned"]}'
                   for tier in ("D1", "D2", "D3", "D4")]
        for key, label in zip(ORDER[1:7], NAMES[1:7])])
    table("prefix-controls.tex", "rrr", "Prefix length & Correct / assigned & Accuracy", [
        [k, f'{r["correct"]}/{r["total"]}', percent(r["accuracy"])]
        for k, r in sorted(evidence["upgrade"]["prefixReplayControl"].items(), key=lambda item: int(item[0]))])
    table("recovery-cohorts.tex", "lrrr", "Inverse cohort & Questions & Sources & Repair cost", [
        [label, len(rows), len({next(t["sourceGroup"] for t in episodes if t["id"] == p["taskId"])
                                for p in rows}), extent(p["minimumRepairCost"] for p in rows)]
        for cohort, label in (("inverse-solvable", "Optimal inverse"),
                              ("inverse-suboptimal", "Suboptimal inverse"),
                              ("inverse-unavailable", "No offered inverse"))
        for rows in [[p for p in probes if p.get("recoveryCohort") == cohort]]])
    table("recovery-lags.tex", "rrrr", "Lag & Questions & Inverse correct & Accuracy", [
        [lag, row["denominator"], row["numerator"], percent(row["value"])]
        for lag, row in quality["inverseLast"]["byLag"].items()])
    table("census.tex", "p{.43\\textwidth}lrrrrrr",
          r"Episode & Tier & Rack & Jobs & Done & $C^*$ & $h$ & A* exp.", [
              [tex(t["id"]), t["tier"], t["capacity"], len(t["jobs"]), t["start"]["done"].bit_count(),
               t["optimalCost"], t["relaxedLowerBound"], number(t["astarClosureExpansionsSeed0"])]
              for t in episodes], long=True)
    matched_tables(bank, evidence, summary)
    write_json(DATA / "publication-statistics.json", summary)


def matched_tables(bank, evidence, summary):
    pairs = summary["visualPairs"]
    rows = []
    for cohort, label in ((PRIMARY, "Primary matched"), (HISTORICAL, "Historical unmatched")):
        for split in SPLITS:
            selected = [p for p in pairs if p["evaluationCohort"] == cohort and p["split"] == split]
            rows.append([label, "Dev." if split == "development" else "Held out", len(selected),
                         len({(p["sourceGroup"], p["interventionId"]) for p in selected}),
                         len({(p["sourceGroup"], p["interventionId"], p["startId"]) for p in selected}),
                         len({p["sourceGroup"] for p in selected})])
    table("matched-cohorts.tex", "llrrrr",
          "Cohort & Split & Pairs & Interventions & Starts & Sources", rows)

    matched = evidence["matched"]
    rows = []
    for key, label in (("count-only", "Counts"), ("part-type-color-presence", "Type/color presence"),
                       ("part-type-color-count", "Type/color counts"), ("sequence-only", "Sequence"),
                       ("public-metadata", "Public text (normalized IDs)"),
                       ("public-metadata-and-inventory", "Public text + inventories")):
        for split in SPLITS:
            cert = matched["certificates"][key]["cohorts"][PRIMARY]["bySplit"][split]
            joint = cert["jointSourceMacro"]
            rows.append([label, "Dev." if split == "development" else "Held out", cert["pairs"],
                         cert["identicalRepresentationPairs"],
                         percent(cert["memberSourceMacroUpperBound"]["value"]),
                         percent(joint["upperBound"]["value"]), "Exact" if joint["tight"] else "Upper bound"])
    table("matched-certificates.tex", "llrrrrl",
          "Representation & Split & Pairs & Equal & Member bound & Joint bound & Status", rows)

    rows = []
    rules = [(name, r["scores"]) for name, r in matched["labelFreeRules"].items()]
    names = {"public-text-inventory-rule": "Public-text inventory",
             "named-occupancy-inventory-rule": "Named-occupancy inventory",
             "source-majority": "Development source majority"}
    rules.append(("source-majority", matched["sourceMajority"]["heldoutScores"]))
    for name, scores in rules:
        for split in (("heldout-source",) if name == "source-majority" else SPLITS):
            if scores is None:
                rows.append([names[name], "Held out", "---", "---", "---", "---", "---"])
                continue
            row = scores["cohorts"][PRIMARY]["bySplit"][split]
            ci = row["uncertainty"]
            interval = ("---" if ci["lower"] is None else
                        f'[{100 * ci["lower"]:.1f}, {100 * ci["upper"]:.1f}]')
            rows.append([names[name], "Dev." if split == "development" else "Held out",
                         row["census"]["eligiblePairs"], row["independentSources"],
                         percent(row["pairMicro"]["value"]), percent(row["sourceMacro"]["value"]), interval])
    table("matched-shortcuts.tex", "llrrrrl",
          r"Software rule & Split & Pairs & Sources & \shortstack{Joint\\micro} & \shortstack{Source\\macro} & \shortstack{95\%\\interval}", rows)

    registry = {r["id"]: r for r in evidence["registry"]}
    strata = []
    for stratum in sorted({r["intakeStratum"] for r in registry.values()}):
        candidates = [r for r in registry.values() if r["intakeStratum"] == stratum]
        ids, groups = {r["id"] for r in candidates}, {r["kit"] for r in candidates}
        admitted = [r for r in summary["admissions"] if r["model"] in ids and r["qualified"]]
        retained = [p for p in pairs if p["evaluationCohort"] == PRIMARY and p["sourceGroup"] in groups]
        strata.append({"stratum": stratum, "candidates": len(ids), "admitted": len(admitted),
                       "rejected": len(ids) - len(admitted),
                       "heldoutAdmitted": sum(r["model"] in evidence["plan"]["heldoutCandidates"] for r in admitted),
                       "matchedPairs": len(retained), "matchedSources": len({p["sourceGroup"] for p in retained})})
    summary["sourceStrata"] = strata
    table("source-strata.tex", "lrrrrrr",
          "Frozen intake stratum & Candidates & Admitted & Rejected & Held out & Pairs & Pair sources", [
              [tex(r["stratum"]), r["candidates"], r["admitted"], r["rejected"],
               r["heldoutAdmitted"], r["matchedPairs"], r["matchedSources"]] for r in strata])
    table("source-admissions.tex", "lllp{.28\\textwidth}l",
          "Model & Kit & Split & Frozen stratum & Admission", [
              [tex(r["model"]), tex(registry[r["model"]]["kit"]),
               "Held out" if r["model"] in evidence["plan"]["heldoutCandidates"] else "Dev.",
               tex(registry[r["model"]]["intakeStratum"]), "Admitted" if r["qualified"] else "Rejected"]
              for r in summary["admissions"]], long=True)
    specs = [s for s in bank["geometryCensus"]["pairs"] if s["evaluationCohort"] == PRIMARY]
    attrition = []
    for row in summary["geometryAttrition"]:
        selected = [s for s in specs if s["profiles"][0].split("-matched-")[0] == row["profile"]]
        attrition.append([
            tex(row["profile"]), row.get("candidateSubsets", "---"), row.get("matchedCandidatePairs", "---"),
            row["selectedContextPairs"], sum(s["retainedFutureContrasts"] > 0 for s in selected),
            sum(s["retainedFutureContrasts"] for s in selected)])
    table("matched-attrition.tex", "p{.38\\textwidth}rrrrr",
          "Base profile & Subsets & Matched options & Qualified & Yielding & Pairs", attrition, long=True)
    table("matched-strata.tex", "lrrrr",
          "Primary stratum & Pairs & Sources & Prefix range & Plan range", [
              [label, len(rows), len({p["sourceGroup"] for p in rows}),
               extent(p["sharedLegalPrefix"] for p in rows),
               extent(len(probes[p["members"][0]]["plan"]) for p in rows)]
              for probes in [{p["id"]: p for p in bank["probes"]}]
              for label, low, high in (("Conflict 2--5", 2, 5), ("Conflict 6--10", 6, 10),
                                        ("Conflict 11+", 11, float("inf")))
              for rows in [[p for p in bank["pairs"] if p.get("evaluationCohort") == PRIMARY
                            and low <= p["sharedLegalPrefix"] + 1 <= high]]])


def publication_text(evidence, summary):
    """Update only the explicitly marked publication block in each document."""
    counts = summary["counts"]
    fields = [
        ("Episodes / diagnostics / canonical diagnostic problems",
         " / ".join(number(counts[k]) for k in ("EpisodeCount", "ProbeCount", "ProblemCount"))),
        ("Active sources / development / held out",
         " / ".join(number(counts[k]) for k in ("SourceCount", "DevelopmentSourceCount", "HeldoutSourceCount"))),
        ("New candidates / admitted / rejected",
         " / ".join(number(counts[k]) for k in ("CandidateCount", "AdmittedCount", "RejectedCount"))),
        ("New seeded source episodes", number(counts["NewSampledEpisodeCount"])),
        ("Primary matched pairs / interventions / sources",
         " / ".join(number(counts[k]) for k in ("PrimaryPairCount", "PrimaryInterventionCount", "PrimarySourceCount"))),
        ("Primary held-out pairs / sources",
         " / ".join(number(counts[k]) for k in ("HeldoutPrimaryPairCount", "HeldoutPrimarySourceCount"))),
        ("Historical unmatched regression pairs", number(counts["HistoricalPairCount"])),
        ("Qualified primary interventions / zero-yield interventions",
         f'{counts["QualifiedInterventionCount"]:,} / {counts["ZeroYieldInterventionCount"]:,}'),
        ("Calibration / discriminative questions",
         f'{counts["CalibrationCount"]:,} / {counts["DiscriminativeCount"]:,}'),
        ("Exact tables / product-state entries / transition entries",
         " / ".join(number(counts[k]) for k in ("OracleCount", "ProductCount", "EdgeCount"))),
        ("Delayed-repair questions / cost range", f'{counts["RepairCount"]:,} / {counts["RepairMin"]}-{counts["RepairMax"]}'),
        ("Inverse-last correct / assigned", f'{counts["InverseCorrect"]:,} / {counts["RepairCount"]:,}'),
        ("Inverse-suboptimal / unavailable", f'{counts["InverseSuboptimal"]:,} / {counts["InverseUnavailable"]:,}'),
        ("D1 / D2 / D3 / D4 episodes", " / ".join(number(summary["byTier"][k]) for k in ("D1", "D2", "D3", "D4"))),
    ]
    body = ["Final-bank evidence generated by `documents.py`; software validation only.", "",
            "| Unit | Count |", "|---|---:|"]
    body += [f"| {label} | {value} |" for label, value in fields]
    body += ["", "| Structural control | Assigned | Completed | Optimal |",
             "|---|---:|---:|---:|"]
    for key, label in zip(ORDER, NAMES):
        row = evidence["controls"]["policies"][key]["all"]
        body.append(f'| {label} | {row["assigned"]:,} | {row["completed"]:,} | {row["optimalCompletions"]:,} |')
    body += ["", f'Bank SHA256: `{summary["bankHash"]}`.',
             "Detailed strata, attrition, cohort denominators, and input hashes: "
             "`data/publication-statistics.json`, `data/matched-controls.json`, and the supplement."]
    for name in ("README.md", "DATASET-CARD.md", "VALIDITY.md",
                 "VALIDATION.md", "REVIEW-RESPONSE.md"):
        path = HERE / name
        text = path.read_text()
        start, end = "<!-- BEGIN PUBLICATION EVIDENCE -->", "<!-- END PUBLICATION EVIDENCE -->"
        if text.count(start) != 1 or text.count(end) != 1:
            raise ValueError(f"Missing or duplicate publication block: {name}")
        before, rest = text.split(start)
        _, after = rest.split(end)
        path.write_text(before + start + "\n" + "\n".join(body) + "\n" + end + after)


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


def source_case(d):
    return {"source": d.source["provenance"], "geometryHash": canonical_hash(d.geometry),
            "parts": [{key: p[key] for key in ("sourceIndex", "sourceInstanceId", "partNumber",
                                              "colorCode", "rawMatrix", "meshSha256")} for p in d.parts],
            "registeredSourceIndices": [d.parts[i]["sourceIndex"] for i in d.mutable]}


def part_inventory(d, indices=None):
    counts = Counter((p["partNumber"], str(p["colorCode"]))
                     for i, p in enumerate(d.parts) if indices is None or i in indices)
    return [{"partNumber": part, "colorCode": color, "count": count}
            for (part, color), count in sorted(counts.items())]


def case_id(value):
    return r"\texttt{" + tex(value).replace("/", r"/\allowbreak{}").replace("-", r"-\allowbreak{}") + "}"


def select_geometry_case(bank, evidence):
    """Lexicographic new-source held-out case with a distinct supplied current view."""
    new_sources = {p["sourceGroup"] for p in bank["profiles"]
                   if p.get("introducedVersion") == "2.3" and p["sampling"] != "geometry-contrast"}
    observations = {r["pairId"]: r for r in evidence["observations"]["pairs"]}
    candidates = sorted((p for p in bank["pairs"] if p.get("evaluationCohort") == PRIMARY
                         and p["introducedVersion"] == "2.3" and p["split"] == "heldout-source"
                         and p["sourceGroup"] in new_sources), key=lambda p: p["id"])
    for pair in candidates:
        row = observations[pair["id"]]
        for view in ("isometric", "left", "rear", "right"):
            if row["differentPixels"][view].get("current"):
                return pair, view, row
    raise ValueError("No new-source held-out primary pair has a certified distinct current view")


def figures(bank, evidence):
    controls = evidence["controls"]
    FIGURES.mkdir(exist_ok=True)
    provenance, captions, gallery = [], {}, []
    base_profiles = [p for p in bank["profiles"] if p["sampling"] != "geometry-contrast"]
    for page, offset in enumerate(range(0, len(base_profiles), 4), 1):
        panels, sources = [], []
        for p in base_profiles[offset:offset + 4]:
            d = domain(p["id"])
            pixels = render(d, range(len(d.parts)), {}, "isometric", size=(1000, 750))
            panels.append(panel(pixels, f'{p["id"]} | {p["split"]}', [
                f'Kit {p["sourceGroup"]}; {p["sourceParts"]} parts; {p["registeredSites"]} registered',
                f'{p["reachableMovableSites"]} reachable movable sites']))
            sources.append({"profile": p["id"], "sourceGroup": p["sourceGroup"], **source_case(d)})
        filename = f"source-gallery-{page}.png"
        collage(panels, 2).save(FIGURES / filename)
        provenance.append({"file": filename, "profiles": [p["id"] for p in base_profiles[offset:offset + 4]],
                           "sources": sources,
                           "state": "Full admitted source subassembly; no pose changes."})
        gallery += [r"\clearpage", rf"\section*{{Original-source gallery: assemblies {offset + 1}--{min(offset + 4, len(base_profiles))}}}",
                    r"\begin{center}",
                    rf"\includegraphics[width=.96\textwidth,height=.85\textheight,keepaspectratio]{{figures/{filename}}}",
                    r"\end{center}"]
    (HERE / "source-gallery.tex").write_text("\n".join(gallery) + "\n")

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
    provenance.append({"file": "resource-replay.png", "taskId": task["id"], "seed": 31, "frames": frames,
                       "sourceGroup": task["sourceGroup"], "profile": task["profile"],
                       "witness": task["witness"], "sourceGeometry": source_case(mission.domain)})
    captions["ResourceCaseCaption"] = (
        f'Exact oracle replay of {case_id(task["id"])} from source {tex(task["sourceGroup"])}. '
        f'The displayed operations are {", ".join(str(f["step"]) for f in frames)}; '
        f'the certified optimum is {task["optimalCost"]} operations. '
        "This is a software witness, not a model trajectory.")

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
        examples.append({"taskId": member, "state": asdict(s), "optimalActions": actions,
                         "sourceGroup": t["sourceGroup"], "profile": t["profile"],
                         "sourceGeometry": source_case(d)})
    collage(panels, 2).save(FIGURES / "ledger-contrast.png")
    provenance.append({"file": "ledger-contrast.png", "pair": pair["id"], "seed": 31, "members": examples})

    pair, view, observation = select_geometry_case(bank, evidence)
    tasks = {t["id"]: t for t in bank["episodes"]}
    probes = {p["id"]: p for p in bank["probes"]}
    panels, examples = [], []
    for context, member in enumerate(pair["members"], 1):
        probe = probes[member]
        task = tasks[probe["taskId"]]
        m = make_mission(task)
        d, state = m.domain, State(**probe["state"])
        session = Session(m, task, seed=0)
        replay = m.replay(state, [Action(**a) for a in probe["plan"]])
        if replay["firstConflict"] != probe["firstConflict"]:
            raise ValueError(f"Figure answer does not replay: {member}")
        selected = sorted(d.fixed) + [d.mutable[i] for i in range(d.n) if state.assembly & (1 << i)]
        pixels = render(d, selected, {}, view, size=(1000, 650))
        answer = "Whole plan legal" if probe["firstConflict"] is None else f'First conflict at operation {probe["firstConflict"]}'
        panels.append(panel(pixels, f'Context {context} | initial {view} view', [
            f'{len(d.fixed)} fixed + {d.n} registered; matched inventory', answer]))
        examples.append({
            "probe": member, "taskId": task["id"], "profile": task["profile"],
            "sourceGroup": task["sourceGroup"], "split": task["split"], "step": 0,
            "state": asdict(state), "goal": task["goal"], "capacity": task["capacity"], "jobs": task["jobs"],
            "answer": probe["firstConflict"], "plan": probe["plan"],
            "publicPlan": [session.public_action(Action(**a)) for a in probe["plan"]],
            "partCount": len(d.parts), "fixedPartCount": len(d.fixed), "registeredCount": d.n,
            "inventory": part_inventory(d), "fixedInventory": part_inventory(d, d.fixed),
            "sourceGeometry": source_case(d)})
    if any(examples[0][key] != examples[1][key] for key in (
            "state", "goal", "capacity", "jobs", "plan", "publicPlan", "inventory", "fixedInventory")):
        raise ValueError("Selected figure fails exact task/inventory matching")
    collage(panels, 2).save(FIGURES / "geometry-contrast.png")
    provenance.append({"file": "geometry-contrast.png", "pair": pair["id"], "seed": 0,
                       "evaluationCohort": PRIMARY, "interventionId": pair["interventionId"],
                       "sourceGroup": pair["sourceGroup"], "view": view,
                       "sharedLegalPrefix": pair["sharedLegalPrefix"], "fixedContext": pair["fixedContext"],
                       "inventoryHash": canonical_hash(examples[0]["inventory"]),
                       "observationCertificate": observation, "members": examples,
                       "selection": "First lexicographic new-source held-out primary pair with distinct current pixels in a supplied view."})
    labels = ["all legal" if e["answer"] is None else f'first conflict at operation {e["answer"]}' for e in examples]
    captions["GeometryCaseCaption"] = (
        f'Primary inventory-matched pair {case_id(pair["id"])} from held-out source '
        f'{tex(pair["sourceGroup"])} in the initial {tex(view)} view. Both contexts use '
        f'{examples[0]["partCount"]} source pieces ({examples[0]["fixedPartCount"]} fixed); '
        "the exact part-number/color multiset, registered poses, start, target, rack, work, and plan match. "
        f'After {pair["sharedLegalPrefix"]} shared legal operations, the exact labels are '
        f'context 1: {labels[0]}; context 2: {labels[1]}. '
        "Only subsets of original fixed instances change. These publication views omit ID overlays; "
        "answers are evaluator annotations. Pixel distinction is not perceptual answerability.")

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
    if len(repair) != probe["minimumRepairCost"]:
        raise ValueError("Selected repair figure does not match its certified distance")
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
    measure = ImageDraw.Draw(images)
    trace_lines, line = [], "Shortest repair: "
    for action in repair:
        public = session.public_action(action)
        phrase = f'{public["type"]} {public["partId"]}'
        candidate = line + ("" if line.endswith(": ") else "  >  ") + phrase
        if measure.textbbox((0, 0), candidate, font=core.font(39))[2] > images.width - 48:
            trace_lines.append(line)
            line = phrase
        else:
            line = candidate
    trace_lines.append(line)
    result = Image.new("RGB", (images.width, images.height + 56 * len(trace_lines) + 120), "#f2f5f6")
    result.paste(images)
    draw = ImageDraw.Draw(result)
    for index, line in enumerate(trace_lines):
        draw.text((24, images.height + 20 + 56 * index), line, fill="#183040", font=core.font(39))
    draw.text((24, images.height + 32 + 56 * len(trace_lines)),
              f'{len(repair)} operations via {first["partId"]}  |  '
              f'{len(repair) + probe["inverseLastControl"]["extraCost"]} operations if the first step undoes {last["partId"]}',
              fill="#183040", font=core.font(39))
    result.save(FIGURES / "repair-case.png")
    provenance.append({"file": "repair-case.png", "probe": probe["id"], "seed": 0,
                       "taskId": probe["taskId"], "sourceGroup": tasks[probe["taskId"]]["sourceGroup"],
                       "profile": tasks[probe["taskId"]]["profile"], "sourceGeometry": source_case(d),
                       "lagAfterError": probe["lagAfterError"], "history": probe["history"],
                       "minimumRepairCost": len(repair), "repair": [asdict(a) for a in repair],
                       "states": [asdict(s) for s in (checkpoint, current, state)],
                       "lastHistoryAction": last, "firstRepairAction": first,
                       "repairActions": [session.public_action(a) for a in repair],
                       "inverseLast": probe["inverseLastControl"]})
    write_json(DATA / "paper-case.json", provenance[-1])
    captions["RepairCaseCaption"] = (
        f'Certified lag-{probe["lagAfterError"]} repair, {case_id(probe["id"])}, '
        f'source {tex(tasks[probe["taskId"]]["sourceGroup"])}. '
        "A: the pre-error checkpoint defines the optimal corridor. "
        f'B: an error and {probe["lagAfterError"]} further operations leave it. '
        f'The last history action is {case_id(last["type"] + " " + last["partId"])}. '
        f'Undoing it first requires {len(repair) + probe["inverseLastControl"]["extraCost"]} '
        f'operations to repair; the optimum takes {len(repair)}, starting with '
        f'{case_id(first["type"] + " " + first["partId"])}. '
        "C: a nonterminal corridor state is restored. These are oracle replay frames, "
        "not model reasoning or a model success; exact source instances and actions are archived.")

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
        axes[1].bar(j, row["successRate"] * 100, color="#bdd0c7", width=.7,
                    label="Completed" if j == 0 else None)
        axes[1].bar(j, row["optimalCompletions"] / row["assigned"] * 100, color="#276649", width=.7,
                    label="Optimal completion" if j == 0 else None)
    axes[1].set(xticks=range(len(keys)), xticklabels=labels, ylim=(0, 110),
                ylabel="Task-runs (%)", title=f'{controls["policies"]["relaxed-greedy"]["all"]["assigned"]} runs per control; {len(bank["episodes"])} tasks')
    axes[1].legend(frameon=False, fontsize=8, loc="upper left", ncol=2)
    fig.savefig(FIGURES / "mechanism-evidence.pdf")
    fig.savefig(FIGURES / "mechanism-evidence.png", dpi=220)
    plt.close(fig)
    provenance.append({"file": "mechanism-evidence.pdf", "inputs": [
        "data/tasks.private.json", "data/software-controls.json"], "scope": "Software controls only"})
    provenance.append({"file": "mechanism-evidence.png", "inputs": [
        "data/tasks.private.json", "data/software-controls.json"], "scope": "Software controls only"})
    for row in provenance:
        row["sha256"] = hashlib.sha256((FIGURES / row["file"]).read_bytes()).hexdigest()
    (HERE / "figure-captions.tex").write_text("\n".join(
        rf"\newcommand{{\{key}}}{{{value}}}" for key, value in captions.items()) + "\n")
    write_json(FIGURES / "provenance.json", {
        "schema": "brickplan-figures/2.3", "bankHash": canonical_hash(bank),
        "meshSha256": hashlib.sha256((HERE / "arena/meshes.json").read_bytes()).hexdigest(),
        "renderer": "../brickplan-v1.2/visual.py + raster.c; original LDraw triangles",
        "license": "../ASSET-LICENSES.json", "captions": captions,
        "captionFileSha256": hashlib.sha256((HERE / "figure-captions.tex").read_bytes()).hexdigest(),
        "figures": provenance})


def main():
    bank = task_bank()
    evidence = publication_inputs(bank)
    persist_evidence()
    summary = publication_summary(bank, evidence)
    tables(bank, evidence, summary)
    figures(bank, evidence)
    publication_text(evidence, summary)
    print("Generated evidence-bound tables, census and original-geometry figures.")


if __name__ == "__main__":
    main()
