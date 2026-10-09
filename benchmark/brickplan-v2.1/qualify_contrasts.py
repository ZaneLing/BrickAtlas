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
    profiles, pairs, census = [], [], []
    for name, capacity in (("roadster-body", 9), ("kart-deck", 5), ("airframe", 8),
                           ("truck-cab", 12), ("sports-body", 8)):
        domain = AssemblyDomain.load(HERE / "data" / name)
        variants = []
        for count in (1, 2):
            for removed in combinations(sorted(domain.fixed), count):
                try:
                    candidate = induced(domain, removed)
                except ValueError:
                    continue
                if candidate.fixed_neighbors != domain.fixed_neighbors:
                    variants.append((removed, candidate))
            if variants:
                break
        # Prefer equal-count variants with identical part-type multisets.
        matched = []
        for (ra, a), (rb, b) in combinations(variants, 2):
            if a.fixed_neighbors == b.fixed_neighbors:
                continue
            ta = sorted(domain.parts[i]["partNumber"] for i in ra)
            tb = sorted(domain.parts[i]["partNumber"] for i in rb)
            matched.append((ta != tb, ra, rb, a, b))
        if matched:
            _, ra, rb, a, b = min(matched, key=lambda x: x[:3])
            specs = [(ra, a), (rb, b)]
            count_matched = True
        elif variants:
            specs = [((), domain), variants[0]]
            count_matched = False
        else:
            census.append({"profile": name, "qualifiedContrast": False})
            continue
        ids = []
        for j, (removed, candidate) in enumerate(specs):
            profile_id = f"{name}-context-{j}"
            folder = HERE / "data" / profile_id
            mutable_sources = [candidate.parts[i]["sourceIndex"] for i in candidate.mutable]
            # Recompute meshes and paths instead of only editing relation labels.
            # For the unchanged underside extraction contract preserve directions.
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
                "id": profile_id, "title": f"{name.replace('-', ' ').title()} · support context {j + 1}",
                "sourceGroup": domain.source["provenance"]["modelId"].split("-")[0],
                "capacity": capacity, "split": "development", "sampling": "geometry-contrast"})
            ids.append(profile_id)
        pairs.append({
            "id": name + "/geometry", "profiles": ids,
            "fixedContext": {"equalPartCount": count_matched,
                             "removedSourceIndices": [[domain.parts[i]["sourceIndex"] for i in r]
                                                      for r, _ in specs],
                             "sameRemovedPartTypes": (sorted(domain.parts[i]["partNumber"] for i in specs[0][0])
                                                      == sorted(domain.parts[i]["partNumber"] for i in specs[1][0]))},
            "qualification": {"sourcePosesUnchanged": True, "meshesAndPathsRecomputed": True,
                              "sourceManifestHash": domain.source["provenance"]["manifestSha256"]}})
        census.append({"profile": name, "qualifiedContrast": True, "candidateSubsets": len(variants)})
        print("CONTRAST", name, pairs[-1], flush=True)
    (HERE / "data/geometry-contrasts.json").write_text(json.dumps(
        {"schema": "brickplan-geometry-contrasts/2.1", "profiles": profiles, "pairs": pairs,
         "census": census}, indent=2) + "\n")


if __name__ == "__main__":
    main()
