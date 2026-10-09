"""Certified 1.2 bank loader and deterministic serialization."""
from functools import lru_cache
import gzip
import json
from pathlib import Path
from engine import AssemblyDomain, canonical_hash

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def write_gzip(path, value):
    path.write_bytes(gzip.compress(json.dumps(value, sort_keys=True, separators=(",", ":")).encode(), mtime=0))


def budget(cost):
    return cost + max(4, (cost + 1) // 2)


@lru_cache(maxsize=None)
def load_bank(case_id):
    if case_id not in ("roadster-body", "kart-deck", "airframe"):
        raise ValueError("Unknown certified case")
    folder = DATA / case_id
    domain = AssemblyDomain.load(folder)
    tasks = json.loads((folder / "tasks.private.json").read_text())
    costs = json.loads(gzip.decompress((folder / "costs.private.json.gz").read_bytes()))
    cert = json.loads((folder / "certificate.json").read_text())
    if (cert["schema"] != "brickplan-certificate/1.2"
            or cert["transitionHash"] != domain.transition_hash
            or cert["tasksHash"] != canonical_hash(tasks)
            or cert["costsHash"] != canonical_hash(costs)
            or cert["sourceHash"] != canonical_hash(domain.source)
            or cert["geometryHash"] != canonical_hash(domain.geometry)):
        raise ValueError("Release certificate mismatch; rebuild or restore the frozen release")
    return domain, tasks, costs, cert


if __name__ == "__main__":
    from revise import main
    main()
