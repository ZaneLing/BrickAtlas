"""Keep every 2.1 geometry regression while adding newly qualified interventions."""
import json
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent


def main():
    path = HERE / "data/geometry-contrasts.json"
    current = json.loads(path.read_text())
    if current.get("predecessorPreserved"):
        return
    old = json.loads((HERE.parent / "brickplan-v2.1/data/geometry-contrasts.json").read_text())
    old_ids = {p["id"] for p in old["profiles"]}
    rename = {}
    for p in current["profiles"]:
        if p["id"] in old_ids:
            before = p["id"]
            after = before.replace("-context-", "-revision-context-")
            rename[before] = after
            shutil.copytree(HERE / "data" / before, HERE / "data" / after, dirs_exist_ok=True)
            p["id"] = after
    old_pairs = {p["id"] for p in old["pairs"]}
    for p in current["pairs"]:
        p["profiles"] = [rename.get(i, i) for i in p["profiles"]]
        if p["id"] in old_pairs:
            p["id"] = p["id"].replace("/geometry", "-revision/geometry")
        p["introducedVersion"] = "2.2"
    for p in old["profiles"]:
        shutil.copytree(HERE.parent / "brickplan-v2.1/data" / p["id"],
                        HERE / "data" / p["id"], dirs_exist_ok=True)
    for p in old["pairs"]:
        p["introducedVersion"] = "2.1"
    current["profiles"] = old["profiles"] + current["profiles"]
    current["pairs"] = old["pairs"] + current["pairs"]
    current["predecessorPreserved"] = True
    path.write_text(json.dumps(current, indent=2) + "\n")


if __name__ == "__main__":
    main()
