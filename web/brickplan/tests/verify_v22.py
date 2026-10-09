"""Isolated frontend/API acceptance; no model inference or manuscript writes."""
import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "benchmark/brickplan-v2.2"))

from bank import HERE, task_bank, write_json
from catalogue import catalogue, preview
from mission import canonical_hash
import package_release
from package_release import check_export, prepare_site
from release import historical_case_check, predecessor_check
from server import Arena, handler_for, run_config

OUT = ROOT / "tem/research/20261009-brickplan-v22-revision/frontend"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    bank = task_bank()
    evidence = {"bankHash": canonical_hash(bank), "checks": []}
    evidence["predecessors"] = predecessor_check()
    evidence["historicalCase"] = historical_case_check()
    servers = []
    with tempfile.TemporaryDirectory(prefix="brickplan-v22-ui-") as temporary:
        folder = Path(temporary)
        practice = Arena(folder / "practice", run_config(), render_images=False)
        cat = catalogue(practice)
        exported = [json.loads(line) for line in (HERE / "release/questions.jsonl").read_text().splitlines()]
        assert [(r["id"], r["stableId"]) for r in exported] == [(r["id"], r["stableId"]) for r in cat["questions"]]
        assert len(exported) == len(bank["episodes"]) + len(bank["probes"])
        evidence["questions"] = len(exported)
        evidence["checks"].append("All exported public IDs match the current bank mapping")
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
        for name, arena, port in (("practice", practice, 8792), ("active", active, 0), ("study", study, 0)):
            server = ThreadingHTTPServer(("127.0.0.1", port), handler_for(arena))
            servers.append(server)
            urls[name] = f"http://127.0.0.1:{server.server_port}"
        prepare_site(folder / "static-site")
        assert (folder / "static-site/cases/local-vlm.json").read_bytes() == (HERE / "cases/local-vlm.json").read_bytes()
        static = ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(
            SimpleHTTPRequestHandler, directory=str(folder)))
        servers.append(static)
        urls["static"] = f"http://127.0.0.1:{static.server_port}/static-site/"
        write_json(OUT / "services.json", {**urls, "probe": probe_id})
        for server in servers:
            threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            node = ROOT / ".tools/node-v22.23.2-darwin-arm64/bin/node"
            result = subprocess.run([str(node), str(Path(__file__).with_suffix(".mjs"))], cwd=ROOT)
            if result.returncode:
                raise SystemExit(result.returncode)
        finally:
            for server in servers:
                server.shutdown()
                server.server_close()


if __name__ == "__main__":
    main()
