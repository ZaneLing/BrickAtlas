"""Source-to-question and strict matched-inventory audit of the entire 2.3 bank."""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import sys

import numpy as np

from bank import DATA, ROOT, task_bank, write_json
from mission import Action, AssemblyDomain, Mission, State, canonical_hash
from oracle import PhysicalGraph
from source_inputs import registry_path, intake_path, frozen_plan_path
from source_fidelity import fidelity

sys.path.insert(0, str(DATA.parent.parent / "brickplan-v1"))
from geometry import load_source


def inventory(d):
    return Counter((p["partNumber"], str(p["colorCode"])) for p in d.parts)


def main():
    bank = task_bank()
    plan = json.loads((DATA.parent / "source-plan.json").read_text())
    frozen = frozen_plan_path()
    assert plan == json.loads(frozen.read_text())
    registry = {r["id"]: r for r in json.loads(registry_path(plan).read_text())["candidates"]}
    admission = json.loads((DATA / "source-admission.json").read_text())
    additions = [r for r in admission["sources"] if r["model"] in registry]
    assert len(additions) == len(registry) == len(plan["newCandidates"])
    assert len({r["model"] for r in additions}) == len(additions)
    assert all(r["planHash"] == canonical_hash(plan) for r in additions)
    for row in additions:
        assert row["sourceFidelity"] == fidelity(row["model"], plan)
        assert not row["qualified"] or row["sourceFidelity"]["passed"]
    profiles = {p["id"]: p for p in bank["profiles"]}
    tasks = {t["id"]: t for t in bank["episodes"]}
    probes = {p["id"]: p for p in bank["probes"]}
    assert len(profiles) == len(bank["profiles"])
    assert len(tasks) == len(bank["episodes"]) and len(probes) == len(bank["probes"])
    domains, rows, model_provenances, leaf_proofs = {}, [], {}, {}
    for profile_id in sorted({t["profile"] for t in tasks.values()}):
        profile = profiles[profile_id]
        d = AssemblyDomain.load(DATA / profile_id)
        domains[profile_id] = d
        provenance = d.source["provenance"]
        model_id = provenance["modelId"]
        manifest_path = ROOT / "web/public/models" / model_id / "manifest.json"
        manifest = json.loads(manifest_path.read_text())
        assert hashlib.sha256(manifest_path.read_bytes()).hexdigest() == provenance["manifestSha256"]
        assert provenance["sourceHash"] == manifest["sourceHash"]
        assert provenance["sourceGeometryModified"] is False
        indices = [p["sourceIndex"] for p in d.parts]
        assert indices == provenance["includedSourceIndices"]
        assert len(indices) == len(set(indices))
        original, fresh_edges, fresh_provenance = load_source(model_id, indices)
        assert fresh_provenance["manifestSha256"] == provenance["manifestSha256"]
        for part, fresh in zip(d.parts, original):
            for key in ("sourceIndex", "sourceInstanceId", "partNumber", "canonical",
                        "colorCode", "colorHex", "meshSha256", "sourcePartSha256"):
                assert part[key] == fresh[key], (profile_id, part["sourceIndex"], key)
            for key in ("originalMatrix", "rawMatrix", "matrix"):
                assert np.allclose(part[key], fresh[key], atol=1e-10, rtol=0), (profile_id, key)
            # Only the explicitly declared extraction direction may be reversed.
            direction_dot = np.dot(part["direction"], fresh["direction"])
            assert abs(abs(direction_dot) - 1) < 1e-5
        assert Counter(canonical_hash(e) for e in d.source["edges"]) == Counter(
            canonical_hash(e) for e in fresh_edges if e["family"] == "stud")
        assert Counter(canonical_hash(e) for e in d.source.get("ignoredNonStudEdges", [])) == Counter(
            canonical_hash(e) for e in fresh_edges if e["family"] != "stud")
        assert d.supported(d.full)
        if model_id in registry:
            assert fidelity(model_id, plan)["passed"], model_id
            intake = json.loads(intake_path(plan, model_id).read_text())
            assert intake["status"] == "manifest-ready"
            if model_id not in model_provenances:
                proof_path = DATA / "source-intake/leaf-proofs" / f"{model_id}.json.gz"
                proof_bytes = gzip.decompress(proof_path.read_bytes())
                proof = json.loads(proof_bytes)
                assert proof["id"] == model_id
                assert proof["candidateRegistrySha256"] == plan["candidateRegistrySha256"]
                assert proof["ordinaryLeafStatus"] == proof["packedHierarchyStatus"] == proof["fullHierarchyStatus"] == "pass"
                assert proof["originalSha256"] == provenance["sourceHash"]
                assert proof["manifestSha256"] == provenance["manifestSha256"]
                assert hashlib.sha256((ROOT / proof["packedHierarchyFile"]).read_bytes()).hexdigest() == proof["packedHierarchySha256"]
                leaf_proofs[model_id] = (hashlib.sha256(proof_bytes).hexdigest(),
                                         {leaf["index"]: leaf for leaf in proof["leaves"]})
                assert len(leaf_proofs[model_id][1]) == proof["instancesCompared"]
                source_provenance = json.loads(
                    (manifest_path.parent / "provenance.json").read_text())
                assert hashlib.sha256((manifest_path.parent / "provenance.json").read_bytes()).hexdigest() == proof["provenanceSha256"]
                source_record = source_provenance["source"]
                assert hashlib.sha256((ROOT / source_record["path"]).read_bytes()).hexdigest() == source_record["sha256"]
                assert source_record["sha256"] == manifest["sourceHash"]
                assert source_provenance["model"]["setNumber"] == registry[model_id]["setNumber"]
                assert source_provenance["candidateRegistrySha256"] == plan["candidateRegistrySha256"]
                for dependency in source_provenance["dependencyFiles"]:
                    assert hashlib.sha256((ROOT / dependency["path"]).read_bytes()).hexdigest() == dependency["sha256"]
                model_provenances[model_id] = source_provenance
            for part in d.parts:
                leaf = leaf_proofs[model_id][1][part["sourceIndex"]]
                assert leaf["instanceId"] == part["sourceInstanceId"]
                for key in ("partNumber", "colorCode", "colorHex", "sourcePartSha256"):
                    assert leaf[key] == part[key], (model_id, part["sourceIndex"], key)
                assert np.allclose(part["originalMatrix"], leaf["originalMatrix"], atol=1e-8, rtol=0)
                assert np.allclose(part["rawMatrix"], np.array(leaf["sourceWorldMatrixLdu"]).reshape(
                    (4, 4), order="F"), atol=1e-8, rtol=0)
            conflicting = {r["partNumber"] for r in
                           model_provenances[model_id].get("embeddedPartLockedPathConflicts", [])}
            assert not conflicting.intersection(p["partNumber"] for p in d.parts)
            assert profile["sourceGroup"] == registry[model_id]["kit"]
            assert profile["split"] == ("heldout-source" if model_id in plan["heldoutCandidates"]
                                         else "development")
            if profile["sampling"] != "geometry-contrast":
                graph = PhysicalGraph(d, profile["capacity"], d.full)
                movable = sum(any(not state & (1 << site) for state in graph.states)
                              for site in range(d.n))
                assert d.n >= 8 and movable == profile["reachableMovableSites"] >= 8
        rows.append({
            "profile": profile_id, "sourceGroup": profile["sourceGroup"],
            "modelId": model_id, "manifestSha256": provenance["manifestSha256"],
            "sourceHash": provenance["sourceHash"], "includedSourceIndices": indices,
            "registeredSourceIndices": [d.parts[i]["sourceIndex"] for i in d.mutable],
            "geometryHash": canonical_hash(d.geometry), "sourceGraphRecomputed": True,
            "originalPosesVerified": True, "passed": True,
            "independentLeafMappingsVerified": model_id in leaf_proofs,
            "independentLeafProofSha256": leaf_proofs[model_id][0] if model_id in leaf_proofs else None,
        })
        print("SOURCE_QUESTION_AUDIT", profile_id, len(d.parts), flush=True)
    question_rows = []
    for task in tasks.values():
        profile = profiles[task["profile"]]
        assert all(task[key] == profile[key] for key in ("sourceGroup", "split", "sampling"))
        mission = Mission(domains[task["profile"]], task["capacity"], task["goal"], task["jobs"])
        assert mission.valid(State(**task["start"]))
        question_rows.append({"id": task["id"], "form": "episode", "profile": task["profile"],
                              "sourceGroup": task["sourceGroup"], "oracleFile": task["oracleFile"]})
    for probe in probes.values():
        task = tasks[probe["taskId"]]
        mission = Mission(domains[task["profile"]], task["capacity"], task["goal"], task["jobs"])
        assert mission.valid(State(**probe["state"]))
        question_rows.append({"id": probe["id"], "form": "probe", "taskId": task["id"],
                              "profile": task["profile"], "sourceGroup": task["sourceGroup"],
                              "oracleFile": task["oracleFile"]})
    specs = {p["id"]: p for p in bank["geometryCensus"]["pairs"]}
    matched = []
    for pair in bank["pairs"]:
        if pair.get("evaluationCohort") != "primary-matched":
            continue
        assert pair["introducedVersion"] == "2.3"
        a, b = [probes[i] for i in pair["members"]]
        ta, tb = [tasks[p["taskId"]] for p in (a, b)]
        da, db = [domains[t["profile"]] for t in (ta, tb)]
        spec = specs[pair["interventionId"]]
        assert set(spec["profiles"]) == {ta["profile"], tb["profile"]}
        assert inventory(da) == inventory(db)
        assert len(da.parts) == len(db.parts) and len(da.fixed) == len(db.fixed)
        assert [[(d.parts[i]["sourceIndex"], d.parts[i]["rawMatrix"]) for i in d.mutable]
                for d in (da, db)][0] == [
                    (db.parts[i]["sourceIndex"], db.parts[i]["rawMatrix"]) for i in db.mutable]
        assert all(ta[k] == tb[k] for k in ("start", "goal", "capacity", "jobs", "sourceGroup", "split"))
        assert a["state"] == b["state"] and a["plan"] == b["plan"]
        assert a["firstConflict"] != b["firstConflict"]
        base_id = spec["profiles"][0].split("-matched-")[0]
        base = AssemblyDomain.load(DATA / base_id)
        included = {p["sourceIndex"] for p in base.parts}
        actual_removed = {frozenset(included - {p["sourceIndex"] for p in d.parts}) for d in (da, db)}
        assert actual_removed == {frozenset(r) for r in pair["fixedContext"]["removedSourceIndices"]}
        assert all(included >= {p["sourceIndex"] for p in d.parts} for d in (da, db))
        valid_count = 0
        for probe, task, domain in ((a, ta, da), (b, tb, db)):
            m = Mission(domain, task["capacity"], task["goal"], task["jobs"])
            replay = m.replay(State(**probe["state"]), [Action(**a) for a in probe["plan"]])
            assert replay["firstConflict"] == probe["firstConflict"]
            if probe["firstConflict"] is None:
                valid_count += 1
                assert replay["state"] == m.terminal
                assert len(probe["plan"]) == task["optimalCost"]
                assert len(replay["states"]) == len(set(replay["states"]))
            else:
                assert probe["firstConflict"] == pair["sharedLegalPrefix"] + 1 >= 3
        assert valid_count == 1
        matched.append({"id": pair["id"], "interventionId": pair["interventionId"],
                        "sourceGroup": ta["sourceGroup"], "split": ta["split"],
                        "answers": [a["firstConflict"], b["firstConflict"]],
                        "partCount": len(da.parts), "inventoryHash": canonical_hash(sorted(inventory(da).items())),
                        "passed": True})
    split_groups = {split: {t["sourceGroup"] for t in tasks.values() if t["split"] == split}
                    for split in ("development", "heldout-source")}
    assert not split_groups["development"] & split_groups["heldout-source"]
    assert matched and len({t["sourceGroup"] for t in tasks.values()}) > 16
    output = {
        "schema": "brickplan-source-question-audit/2.3", "bankHash": canonical_hash(bank),
        "passed": True, "candidateCount": len(additions),
        "newAdmittedSources": sum(r["qualified"] for r in additions),
        "independentSourceGroups": len({t["sourceGroup"] for t in tasks.values()}),
        "profilesChecked": len(rows), "questionsChecked": len(question_rows),
        "sources": rows, "questions": question_rows, "matchedPairs": matched,
        "matchedSourceGroups": sorted({r["sourceGroup"] for r in matched}),
        "matchedHeldoutSources": sorted({r["sourceGroup"] for r in matched if r["split"] == "heldout-source"}),
        "scope": "All active source poses, locked dependency identities, parsed stud graphs, source/question links and primary matched inventories. Exact all-state costs and answers are separately recomputed by the archived independent rules. No force or human-answerability certificate.",
    }
    write_json(DATA / "source-question-audit.json", output)
    write_json(DATA / "geometry-probe-audit.json", {
        "schema": "brickplan-geometry-probe-audit/2.3", "bankHash": canonical_hash(bank),
        "census": bank["geometryCensus"],
        "episodes": sum(t["kind"] == "visual-geometry-context" for t in bank["episodes"]),
        "pairs": [p for p in bank["pairs"] if p["kind"] == "visual-geometry"],
        "probes": [p for p in bank["probes"] if p["kind"] == "geometry-continuation"]})
    print("COMPLETE", len(rows), "profiles", len(question_rows), "questions", len(matched), "matched pairs")


if __name__ == "__main__":
    main()
