"""Versioned source profiles and private task-bank loading."""
from functools import lru_cache
import gzip
import json
from pathlib import Path

from mission import AssemblyDomain, Mission, State, canonical_hash
from oracle import Oracle, PhysicalGraph

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DATA = HERE / "data"
PROFILES = [
    {"id": "roadster-body", "title": "Roadster body", "sourceGroup": "31027",
     "source": "../brickplan-v1.2/data/roadster-body", "capacity": 9, "split": "development"},
    {"id": "kart-deck", "title": "Kart deck", "sourceGroup": "31027",
     "source": "../brickplan-v1.2/data/kart-deck", "capacity": 5, "split": "development"},
    {"id": "airframe", "title": "Airframe", "sourceGroup": "31028",
     "source": "../brickplan-v1.2/data/airframe", "capacity": 8, "split": "development"},
    {"id": "truck-cab", "title": "Truck cab and roof", "sourceGroup": "10156",
     "source": "../../tem/research/20261008-brickplan-overhaul/qualified/10156", "capacity": 12, "split": "development"},
    {"id": "house-roof", "title": "House roof assembly", "sourceGroup": "31009",
     "source": "../../tem/research/20261008-brickplan-overhaul/qualified/31009", "capacity": 5, "split": "development"},
    {"id": "sports-body", "title": "Sports car upper body", "sourceGroup": "5867",
     "source": "../../tem/research/20261008-brickplan-overhaul/qualified/5867", "capacity": 8, "split": "development"},
]
for profile in PROFILES:
    profile["sampling"] = "legacy-mechanism-conditioned"
for filename in ("source-admission.json", "geometry-contrasts.json"):
    if (DATA / filename).exists():
        PROFILES.extend(json.loads((DATA / filename).read_text())["profiles"])


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


@lru_cache(maxsize=32)
def domain(profile_id):
    if profile_id not in {p["id"] for p in PROFILES}:
        raise ValueError("Unknown source profile")
    result = AssemblyDomain.load(DATA / profile_id)
    certificate = DATA / "certificate.json"
    if certificate.exists():
        hashes = json.loads(certificate.read_text())["sources"][profile_id]
        if (canonical_hash(result.geometry) != hashes["geometryHash"]
                or canonical_hash(result.source) != hashes["sourceHash"]
                or result.transition_hash != hashes["transitionHash"]):
            raise ValueError("Source qualification certificate mismatch")
    return result


@lru_cache(maxsize=16)
def graph(profile_id, capacity, goal):
    return PhysicalGraph(domain(profile_id), capacity, goal)


@lru_cache(maxsize=1)
def task_bank():
    value = json.loads((DATA / "tasks.private.json").read_text())
    cert = json.loads((DATA / "certificate.json").read_text())
    if value["schema"] != "brickplan-bank/2.1" or canonical_hash(value) != cert["tasksHash"]:
        raise ValueError("Task bank certificate mismatch")
    return value


def task_by_id(task_id):
    return next(t for t in task_bank()["episodes"] if t["id"] == task_id)


def make_mission(task):
    return Mission(domain(task["profile"]), task["capacity"], task["goal"], task["jobs"])


@lru_cache(maxsize=24)
def load_oracle(task_id):
    task = task_by_id(task_id)
    mission = make_mission(task)
    cert = json.loads((DATA / "certificate.json").read_text())["oracles"][task["oracleFile"]]
    oracle = Oracle.load(mission, graph(task["profile"], task["capacity"], task["goal"]),
                         DATA / task["oracleFile"], cert["contentHash"])
    if oracle.distance(State(**task["start"])) != task["optimalCost"]:
        raise ValueError("Task/oracle cost mismatch")
    return oracle
