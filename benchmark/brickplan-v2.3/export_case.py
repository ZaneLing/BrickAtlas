"""Archive an actual completed model trace and its exact public image bytes."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

from bank import HERE, write_json
from server import Arena


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--store", type=Path, required=True)
    parser.add_argument("--run", required=True)
    args = parser.parse_args()
    arena = Arena(args.store, json.loads((args.store / "run-config.json").read_text()), False)
    run = arena.model_manager().get(args.run)
    if run["status"] != "ended" or not run["steps"] or any(s["status"] != "executed" for s in run["steps"]):
        raise ValueError("Only complete, executed real traces can be archived")
    target = HERE / "cases"
    (target / "media").mkdir(parents=True, exist_ok=True)
    files = {}
    def images(value):
        if isinstance(value, dict):
            if value.get("mime") == "image/png" and "url" in value:
                path = arena.media_file(value["url"])
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                assert path.stem == digest
                shutil.copyfile(path, target / "media" / path.name)
                files[path.name] = digest
            else:
                for item in value.values():
                    images(item)
        elif isinstance(value, list):
            for item in value:
                images(item)
    images(run)
    run["recorded"] = True
    write_json(target / "local-vlm.json", run)
    write_json(target / "local-vlm.authoritative.json", arena.sessions[run["sessionId"]].export())
    write_json(target / "provenance.json", {
        "schema": "brickplan-case-provenance/2.3", "bankHash": run["bankHash"],
        "modelWeightsSHA256": run["modelWeightsSHA256"],
        "traceSha256": hashlib.sha256((target / "local-vlm.json").read_bytes()).hexdigest(),
        "images": files, "calls": len(run["steps"]), "realInference": True,
        "selection": "First local visual-model run on the default kart-deck-08 demonstration; all calls retained."})
    print(f"Archived {len(run['steps'])} real calls and {len(files)} image files.")


if __name__ == "__main__":
    main()
