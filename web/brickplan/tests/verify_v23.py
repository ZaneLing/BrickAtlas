"""Isolated frontend/API acceptance; no model inference or manuscript writes."""
import functools
import hashlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "benchmark/brickplan-v2.3"))

from bank import HERE, task_bank, write_json
from catalogue import catalogue, preview
from mission import canonical_hash
import package_release
from package_release import check_export, prepare_site
from server import Arena, handler_for, run_config

OUT = Path(os.environ.get("BRICKPLAN_TEST_OUTPUT", "/tmp/brickplan-v23-work/frontend")).resolve()


def main():
    if OUT.is_relative_to(ROOT):
        raise ValueError("Intermediate frontend evidence must be outside the workspace")
    OUT.mkdir(parents=True, exist_ok=True)
    bank = task_bank()
    evidence = {"bankHash": canonical_hash(bank), "checks": []}
    reports = ("workbench-validation.json", "workbench-integration.json")
    for name in reports:
        write_json(OUT / name, {"status": "running", "bankHash": evidence["bankHash"], "errors": []})
    for name in ("local-vlm.json", "local-vlm.authoritative.json", "task.v2.1.json", "provenance.json"):
        assert (HERE / "cases" / name).read_bytes() == (HERE.parent / "brickplan-v2.2/cases" / name).read_bytes()
    evidence["checks"].append("Historical model case and task bytes match frozen 2.2")
    servers = []
    with tempfile.TemporaryDirectory(prefix="brickplan-v23-ui-") as temporary:
        folder = Path(temporary)
        practice = Arena(folder / "practice", run_config(), render_images=False)
        cat = catalogue(practice)
        exported = [json.loads(line) for line in (HERE / "release/questions.jsonl").read_text().splitlines()]
        assert [(r["id"], r["stableId"]) for r in exported] == [(r["id"], r["stableId"]) for r in cat["questions"]]
        assert len(exported) == len(bank["episodes"]) + len(bank["probes"])
        evidence["questions"] = len(exported)
        evidence["checks"].append("All exported public IDs match the current bank mapping")
        pairs = [p for p in bank["pairs"] if p["kind"] == "visual-geometry"]
        membership = {member: p["evaluationCohort"] for p in pairs for member in p["members"]}
        forbidden = {"evaluationCohort", "provenance", "sourceGroup", "stableId", "scoringRole",
                     "canonicalProblem", "recoveryCohort", "optimalCost", "optimalChoices"}

        def policy_input(value):
            if isinstance(value, dict):
                assert not forbidden & value.keys(), forbidden & value.keys()
                for child in value.values():
                    policy_input(child)
            elif isinstance(value, list):
                for child in value:
                    policy_input(child)

        for row in exported:
            assert row["evaluationCohort"] == membership.get(row["stableId"], "")
            public = json.loads(row["publicInputJSON"])
            policy_input(public)
            for field, namespace in (("observation", "initialView"), ("checkpointObservation", "checkpointInitialView")):
                observation = public.get(field, public.get("repairContext", {}).get(field, {}))
                for view in observation.get("inspectionHistory", []):
                    assert view["atRevision"] == 0
                    assert view["frameId"] == canonical_hash({namespace: view["view"], "seed": row["identitySeed"]})[:24]
        for cohort in cat["cohorts"]:
            selected = [r for r in exported if r["evaluationCohort"] == cohort["id"]]
            assert cohort["probes"] == len(selected) > 0
            assert cohort["pairs"] * 2 == len(selected)
            assert cohort["sources"] == len({r["source"] for r in selected})
        evidence["cohorts"] = cat["cohorts"]
        evidence["checks"].append("Every export has exact bank cohort membership; policy inputs omit practice metadata and state-derived frame IDs")
        check_export()
        with patch.object(package_release, "task_bank", return_value={}):
            try:
                check_export()
                raise RuntimeError("Stale-bank exports accepted")
            except AssertionError:
                pass
        evidence["checks"].append("Export file inventory/runtime hashes verified; stale-bank export rejected")
        key = next(k for k in practice.probe_ids if len(k) > 4)
        assert practice.get(f"/api/preview/{key}")["id"] == key
        assert practice.get(f"/api/scene/preview/{key}")["frames"]
        public = practice.get(f"/api/probes/{key}")
        assert public["observation"]["actions"] == {}
        assert all(v["atRevision"] == 0 for v in public["observation"]["inspectionHistory"])
        assert not {"scoringRole", "canonicalProblem", "recoveryCohort"} & public.keys()
        assert "scoringRole" not in json.dumps(preview(practice, key))
        try:
            practice.post(f"/api/probes/{key}/actions", {
                "requestId": "reject-acquisition", "revision": 0,
                "action": {"type": "inspect", "view": "left"}})
            raise AssertionError("Static probe accepted inspect")
        except ValueError as error:
            assert "Static multiview" in str(error)
        assert practice.probe(key).revision == 0
        answer = {"choice": 0} if "candidates" in public else {"firstConflict": None}
        practice.post(f"/api/probes/{key}/actions", {
            "requestId": "answer", "revision": 0, "action": {"type": "answer", "answer": answer}})
        assert practice.get(f"/api/probes/{key}/review")
        evidence["checks"].append("Four-digit preview/scene/action/review routes and static acquisition rejection")
        write_json(OUT / "api-validation.json", {**evidence, "status": "passed"})

        # Start clean practice stores so API fixtures cannot pre-answer UI tests.
        practice = Arena(folder / "browser-practice", run_config())
        probe_id = next(k for k, value in practice.probe_ids.items()
                        if len(k) > 4 and next(p for p in bank["probes"] if p["id"] == value)["kind"] == "delayed-repair")
        probe_internal = practice.probe_ids[probe_id]
        assigned = {"episodes": [bank["episodes"][0]["id"]], "probes": [probe_internal]}
        active = Arena(folder / "active", run_config(track="image-id-active"))
        study = Arena(folder / "study", run_config(study=True, assignments=assigned))
        urls = {}
        for name, arena, port in (("practice", practice, int(os.environ.get("BRICKPLAN_TEST_PORT", "8793"))),
                                  ("active", active, 0), ("study", study, 0)):
            server = ThreadingHTTPServer(("127.0.0.1", port), handler_for(arena))
            servers.append(server)
            urls[name] = f"http://127.0.0.1:{server.server_port}"
        prepare_site(folder / "static-site")
        assert (folder / "static-site/cases/local-vlm.json").read_bytes() == (HERE / "cases/local-vlm.json").read_bytes()
        static = ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(
            SimpleHTTPRequestHandler, directory=str(folder)))
        servers.append(static)
        urls["static"] = f"http://127.0.0.1:{static.server_port}/static-site/"
        write_json(OUT / "services.json", {**urls, "probe": probe_id, "bankHash": evidence["bankHash"]})
        for server in servers:
            threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            node = os.environ.get("BRICKPLAN_NODE", str(ROOT / ".tools/node-v22.23.2-darwin-arm64/bin/node"))
            environment = {**os.environ, "BRICKPLAN_TEST_OUTPUT": str(OUT), "BRICKPLAN_TEST_URL": urls["practice"],
                           "PYTHONNOUSERSITE": "1"}
            environment.pop("PYTHONPATH", None)
            for script in (HERE / "test_workbench.mjs", HERE / "test_workbench_integration.mjs"):
                result = subprocess.run([node, str(script)], cwd=ROOT, env=environment)
                if result.returncode:
                    raise SystemExit(result.returncode)
            current_bank = json.loads((HERE / "data/tasks.private.json").read_text())
            assert canonical_hash(current_bank) == evidence["bankHash"], "Bank changed during frontend acceptance"
            for name in reports:
                report = json.loads((OUT / name).read_text())
                assert report["status"] == "passed" and not report["errors"]
                assert report["bankHash"] == evidence["bankHash"]
                for file, digest in report["frontendFiles"].items():
                    assert hashlib.sha256((ROOT / file).read_bytes()).hexdigest() == digest, file
            for name in reports:
                target = HERE / "data" / name
                temporary_report = target.with_suffix(".tmp")
                shutil.copyfile(OUT / name, temporary_report)
                temporary_report.replace(target)
            print("Installed current-bank workbench-validation.json and workbench-integration.json in data/", flush=True)
        finally:
            for server in servers:
                server.shutdown()
                server.server_close()


if __name__ == "__main__":
    main()
