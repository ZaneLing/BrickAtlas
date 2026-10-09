"""Qualify fixed-context contrasts from induced original-source subassemblies."""
import copy
from itertools import combinations
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "brickplan-v1"))
from geometry import qualify
from engine import AssemblyDomain, canonical_hash


def induced(domain, removed):
    keep = sorted(set(range(len(domain.parts))) - set(removed))
    index = {old: new for new, old in enumerate(keep)}
    geo = copy.deepcopy(domain.geometry)
    geo["parts"] = [geo["parts"][i] for i in keep]
    geo["mutable"] = [index[i] for i in domain.mutable]
    geo["endpoints"] = [{**r, "a": index[r["a"]], "b": index[r["b"]]}
                        for r in geo["endpoints"] if r["a"] in index and r["b"] in index]
    geo["paths"] = [{**r, "moving": index[r["moving"]],
                     "pairs": [{**p, "obstacle": index[p["obstacle"]]} for p in r["pairs"]
                               if p["obstacle"] in index]} for r in geo["paths"]]
    source = copy.deepcopy(domain.source)
    for field in ("edges", "ignoredNonStudEdges"):
        source[field] = [{**e, "a": index[e["a"]], "b": index[e["b"]]}
                         for e in source.get(field, []) if e["a"] in index and e["b"] in index]
    source["provenance"]["includedSourceIndices"] = [p["sourceIndex"] for p in geo["parts"]]
    source["provenance"]["derivation"] = "Induced source subassembly with a fixed-context subset; original poses unchanged."
    result = AssemblyDomain(geo, source)
    if not result.supported(result.full):
        raise ValueError("Full assembly unsupported")
    return result


def main():
    from collections import Counter
    # Import the local registry rather than the legacy executor's sibling modules.
    sys.path.insert(0, str(HERE))
    from bank import PROFILES
    profiles, pairs, census = [], [], []
    for base in [p for p in PROFILES if p["sampling"] != "geometry-contrast"]:
        name, capacity = base["id"], base["capacity"]
        domain = AssemblyDomain.load(HERE / "data" / name)
        variants, reasons = {}, Counter()
        fixed_supports = {i: set() for i in domain.mutable}
        for e in domain.source["edges"]:
            for a, b in ((e["a"], e["b"]), (e["b"], e["a"])):
                if a in fixed_supports and b in domain.fixed:
                    fixed_supports[a].add(b)
        for count in (1, 2):
            for removed in combinations(sorted(domain.fixed), count):
                if not any(s and s <= set(removed) for s in fixed_supports.values()):
                    reasons["unchanged-fixed-support"] += 1
                    continue
                try:
                    candidate = induced(domain, removed)
                except ValueError as exc:
                    reasons[str(exc)] += 1
                    continue
                if candidate.fixed_neighbors != domain.fixed_neighbors:
                    reasons["qualified-changed-support"] += 1
                    variants.setdefault(candidate.fixed_neighbors, (removed, candidate))
        options = list(variants.values()) + [((), domain)]
        def priority(pair):
            (ra, _), (rb, _) = pair
            ta = sorted(domain.parts[i]["partNumber"] for i in ra)
            tb = sorted(domain.parts[i]["partNumber"] for i in rb)
            return (ta != tb, len(ra) != len(rb), ra, rb)
        selected = sorted(combinations(options, 2), key=priority)[:3]
        for contrast_index, specs in enumerate(selected):
            prefix = name if contrast_index == 0 else f"{name}-intervention-{contrast_index}"
            ids = []
            for j, (removed, candidate) in enumerate(specs):
                profile_id = f"{prefix}-context-{j}"
                folder = HERE / "data" / profile_id
                mutable_sources = [candidate.parts[i]["sourceIndex"] for i in candidate.mutable]
                from geometry import load_source
                original, _, _ = load_source(candidate.source["provenance"]["modelId"],
                                             [p["sourceIndex"] for p in candidate.parts])
                inverse = [p["sourceIndex"] for p, q in zip(candidate.parts, original)
                           if sum(x * y for x, y in zip(p["direction"], q["direction"])) < 0]
                qualified = qualify(original, mutable_sources, folder / "geometry.json", inverse)
                rebuilt = AssemblyDomain(qualified, candidate.source)
                assert rebuilt.fixed_neighbors == candidate.fixed_neighbors
                assert rebuilt.blockers == candidate.blockers
                (folder / "source.json").write_text(json.dumps(candidate.source, indent=2) + "\n")
                profiles.append({
                    "id": profile_id, "title": f"{prefix.replace('-', ' ').title()} · support context {j + 1}",
                    "sourceGroup": base["sourceGroup"], "capacity": capacity,
                    "split": base["split"], "sampling": "geometry-contrast"})
                ids.append(profile_id)
            pairs.append({
                "id": prefix + "/geometry", "profiles": ids,
                "fixedContext": {"equalPartCount": len(specs[0][0]) == len(specs[1][0]),
                                 "removedSourceIndices": [[domain.parts[i]["sourceIndex"] for i in r]
                                                          for r, _ in specs],
                                 "sameRemovedPartTypes": (sorted(domain.parts[i]["partNumber"] for i in specs[0][0])
                                                          == sorted(domain.parts[i]["partNumber"] for i in specs[1][0]))},
                "qualification": {"sourcePosesUnchanged": True, "meshesAndPathsRecomputed": True,
                                  "sourceManifestHash": domain.source["provenance"]["manifestSha256"]}})
            print("CONTRAST", name, pairs[-1], flush=True)
        census.append({"profile": name, "qualifiedContrast": bool(selected),
                       "candidateSubsets": sum(reasons.values()), "reasons": dict(reasons),
                       "distinctChangedSupportMasks": len(variants), "retainedPairs": len(selected)})
    (HERE / "data/geometry-contrasts.json").write_text(json.dumps(
        {"schema": "brickplan-geometry-contrasts/2.2", "profiles": profiles, "pairs": pairs,
         "census": census}, indent=2) + "\n")
    from preserve_contrasts import main as preserve
    preserve()


if __name__ == "__main__":
    main()
