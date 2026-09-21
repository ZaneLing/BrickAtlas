#!/usr/bin/env python3
"""Family-first source-cluster paired analysis of two completed score files."""
import argparse
import json
import random
from collections import defaultdict
from pathlib import Path

p = argparse.ArgumentParser(description=__doc__)
p.add_argument("--a", required=True, type=Path, help="Condition A scores.json")
p.add_argument("--b", required=True, type=Path, help="Condition B scores.json")
p.add_argument("--out", required=True, type=Path)
p.add_argument("--comparison", help="Preregistered comparison ID in ldraw-v2-experiments.json")
p.add_argument("--seed", default=20260918, type=int)
p.add_argument("--resamples", default=10000, type=int)
args = p.parse_args()
a, b = [json.loads(path.read_text()) for path in (args.a, args.b)]
assert a["version"] == b["version"] == "brickatlas-ldraw-2"
assert a["missing"] == b["missing"] == 0, "Expected runs must be complete; explicit null outputs count as failures."
ra, rb = [{r["id"]: r for r in result["rows"]} for result in (a, b)]
assert len(ra) == len(a["rows"]) and len(rb) == len(b["rows"])
ids = sorted(ra.keys() & rb.keys())
assert ids, "No paired items"
if args.comparison:
    root = Path(__file__).resolve().parents[3]
    plan = json.loads((root / "benchmark/paper/ldraw-v2-experiments.json").read_text())
    comparison = next(c for c in plan["pairedComparisons"] if c["id"] == args.comparison)
    ids = comparison["taskIds"]
    assert all(i in ra and i in rb for i in ids), "Preregistered pair is incomplete"
assert args.resamples >= 100


def estimate(selected):
    groups = defaultdict(list)
    cw = wc = 0
    for task in selected:
        x, y = ra[task], rb[task]
        assert x["modelId"] == y["modelId"] and x["family"] == y["family"]
        av, bv = x["verdict"]["success"], y["verdict"]["success"]
        assert av in [0, 1] and bv in [0, 1]
        groups[x["modelId"]].append(av-bv)
        cw += av == 1 and bv == 0
        wc += av == 0 and bv == 1
    blocks = list(groups.values())
    macro = sum(sum(v)/len(v) for v in blocks)/len(blocks)
    micro = sum(sum(v) for v in blocks)/sum(len(v) for v in blocks)
    rng = random.Random(args.seed)
    macros, micros = [], []
    for _ in range(args.resamples):
        draw = [blocks[rng.randrange(len(blocks))] for _ in blocks]
        macros.append(sum(sum(v)/len(v) for v in draw)/len(draw))
        micros.append(sum(sum(v) for v in draw)/sum(len(v) for v in draw))
    def interval(samples):
        samples.sort()
        def quantile(q):
            k = q*(len(samples)-1); low = int(k); frac = k-low
            return samples[low]*(1-frac)+samples[min(low+1, len(samples)-1)]*frac
        return [quantile(.025), quantile(.975)]
    ci = interval(macros)
    return {"items": len(selected), "sources": len(groups), "deltaMacro": macro, "deltaMicro": micro,
            "macroCI95": ci, "microCI95": interval(micros), "correctToWrong": cw, "wrongToCorrect": wc,
            "interpretation": "No stable gain detected; equivalence not established" if ci[0] <= 0 <= ci[1]
            else "Paired difference detected under this observation contract"}


result = {
    "version": "brickatlas-ldraw-2", "seed": args.seed, "resamples": args.resamples,
    "preregisteredComparison": args.comparison,
    "direction": "A minus B", "pairedIds": ids, "unpairedA": sorted(ra.keys()-rb.keys()),
    "unpairedB": sorted(rb.keys()-ra.keys()),
    "byFamily": {f: estimate([i for i in ids if ra[i]["family"] == f]) for f in sorted({ra[i]["family"] for i in ids})},
    "allEligibleDescriptive": estimate(ids), "equivalenceMargin": None,
}
args.out.write_text(json.dumps(result, indent=2)+"\n")
print(f"Wrote {len(ids)} paired items; family-first source-cluster estimates.")
