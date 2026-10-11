"""Strict inventory-matched induced source contexts; no unequal-count fallback."""
import argparse
from collections import Counter, defaultdict
import copy
from itertools import combinations
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "brickplan-v1"))
from geometry import load_source, qualify
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
    source["provenance"]["derivation"] = (
        "Inventory-matched induced source subassembly; every retained original pose unchanged.")
    result = AssemblyDomain(geo, source)
    if not result.supported(result.full):
        raise ValueError("Full assembly unsupported")
    return result


def inventory(domain, indices):
    return tuple(sorted((domain.parts[i]["partNumber"], str(domain.parts[i]["colorCode"]))
                        for i in indices))


def enumerate_matched(domain, maximum=4):
    """Use connectivity/support only; retain same-type irrelevant deletions too."""
    fixed_adj = {i: set() for i in domain.fixed}
    supports = {i: set() for i in domain.mutable}
    for e in domain.source["edges"]:
        a, b = e["a"], e["b"]
        if a in fixed_adj and b in fixed_adj:
            fixed_adj[a].add(b)
            fixed_adj[b].add(a)
        for x, y in ((a, b), (b, a)):
            if x in supports and y in fixed_adj:
                supports[x].add(y)
    variants, reasons = defaultdict(dict), Counter()
    for count in (1, 2):
        for removed in combinations(sorted(domain.fixed), count):
            removed_set = set(removed)
            fixed = domain.fixed - removed_set
            if not fixed:
                reasons["no-fixed-context"] += 1
                continue
            reached, stack = set(), [min(fixed)]
            while stack:
                node = stack.pop()
                if node not in reached:
                    reached.add(node)
                    stack.extend(fixed_adj[node] - removed_set - reached)
            if reached != fixed:
                reasons["fixed-disconnected"] += 1
                continue
            mask = sum(1 << site for site, local in enumerate(domain.mutable)
                       if supports[local] - removed_set)
            reached, frontier = mask, mask
            while frontier:
                bit = frontier & -frontier
                frontier ^= bit
                extra = domain.neighbors[bit.bit_length() - 1] & ~reached
                reached |= extra
                frontier |= extra
            if reached != domain.full:
                reasons["full-unsupported"] += 1
                continue
            reasons["admissible-induced-subset"] += 1
            variants[inventory(domain, removed)].setdefault(mask, removed)
    options = []
    for signature, masks in sorted(variants.items()):
        for (ma, ra), (mb, rb) in combinations(sorted(masks.items()), 2):
            options.append((ra, rb, ma, mb, signature))
    # Geometry-only selection, independent of oracle difficulty or answer.
    options.sort(key=lambda row: canonical_hash({"seed": 20261010, "contexts": row[:2]}))
    selected, seen_masks = [], set()
    for row in options:
        key = tuple(sorted(row[2:4]))
        if key not in seen_masks:
            selected.append(row)
            seen_masks.add(key)
        if len(selected) == maximum:
            break
    return selected, {
        "candidateSubsets": sum(reasons.values()), "reasons": dict(reasons),
        "inventorySignatures": len(variants), "matchedCandidatePairs": len(options),
        "distinctMatchedSupportMaskPairs": len({tuple(sorted(r[2:4])) for r in options}),
        "selectedContextPairs": len(selected),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pilot", action="store_true", help="Census only; no geometry output")
    parser.add_argument("--profile", help="Qualify one source in an isolated cache without publishing the registry")
    args = parser.parse_args()
    sys.path.insert(0, str(HERE))
    from bank import PROFILES
    old = json.loads((HERE.parent / "brickplan-v2.2/data/geometry-contrasts.json").read_text())
    profiles, pairs = copy.deepcopy(old["profiles"]), copy.deepcopy(old["pairs"])
    for row in pairs:
        row["evaluationCohort"] = "historical-unmatched-regression"
        row["introducedVersion"] = "2.2-or-earlier"
    census = []
    bases = [p for p in PROFILES if p["sampling"] != "geometry-contrast"]
    if args.profile:
        base = next((p for p in bases if p["id"] == args.profile), None)
        if base is None:
            record = json.loads((HERE / "data/source-admission-records" /
                                 (args.profile.removeprefix("source-") + ".json")).read_text())
            assert record["qualified"]
            base = record["profile"]
        bases = [base]
    for base in bases:
        domain = AssemblyDomain.load(HERE / "data" / base["id"])
        admission_hash = canonical_hash({"profile": base, "geometry": domain.geometry,
                                         "source": domain.source, "code": Path(__file__).read_text()})
        record_path = HERE / "data/contrast-admission-records" / (base["id"] + ".json")
        record = json.loads(record_path.read_text()) if record_path.exists() else None
        if not args.pilot and record and record.get("inputHash") == admission_hash:
            profiles.extend(record["profiles"])
            pairs.extend(record["pairs"])
            census.append(record["census"])
            print("PRESERVED_MATCHED", base["id"], len(record["pairs"]), flush=True)
            continue
        before = len(profiles), len(pairs)
        if domain.n < 8:
            census.append({"profile": base["id"], "selectedContextPairs": 0,
                           "exclusion": "Fewer than eight registered sites"})
            continue
        selected, row = enumerate_matched(domain)
        row.update(profile=base["id"], sourceGroup=base["sourceGroup"], split=base["split"])
        row["selectedRemovedSourceIndices"] = [
            [[domain.parts[i]["sourceIndex"] for i in r] for r in spec[:2]] for spec in selected]
        census.append(row)
        print("MATCHED_CENSUS", json.dumps(row), flush=True)
        if args.pilot:
            continue
        for contrast_index, spec in enumerate(selected):
            prefix = f'{base["id"]}-matched-{contrast_index}'
            ids, kept_inventories = [], []
            for j, removed in enumerate(spec[:2]):
                candidate = induced(domain, removed)
                profile_id = f"{prefix}-context-{j}"
                folder = HERE / "data" / profile_id
                original, edges, provenance = load_source(
                    candidate.source["provenance"]["modelId"],
                    [p["sourceIndex"] for p in candidate.parts])
                reverse = [p["sourceIndex"] for p, q in zip(candidate.parts, original)
                           if sum(x * y for x, y in zip(p["direction"], q["direction"])) < 0]
                mutable_sources = [candidate.parts[i]["sourceIndex"] for i in candidate.mutable]
                input_hash = canonical_hash({"parts": original, "mutable": mutable_sources,
                                             "reverse": reverse, "edges": edges})
                cache = folder / "qualification-input.json"
                cached = json.loads(cache.read_text()) if cache.exists() else {}
                geometry = (json.loads((folder / "geometry.json").read_text())
                            if cached.get("inputHash") == input_hash else None)
                if geometry is None or canonical_hash(geometry) != cached.get("geometryHash"):
                    geometry = qualify(original, mutable_sources, folder / "geometry.json", reverse)
                    cache.write_text(json.dumps({"inputHash": input_hash,
                                                 "geometryHash": canonical_hash(geometry)}, indent=2) + "\n")
                candidate.source["edges"] = [e for e in edges if e["family"] == "stud"]
                candidate.source["ignoredNonStudEdges"] = [e for e in edges if e["family"] != "stud"]
                rebuilt = AssemblyDomain(geometry, candidate.source)
                assert rebuilt.fixed_neighbors == spec[2 + j]
                assert rebuilt.blockers == domain.blockers
                assert rebuilt.supported(rebuilt.full)
                (folder / "source.json").write_text(json.dumps(candidate.source, indent=2) + "\n")
                profiles.append({
                    "id": profile_id, "title": f"{base['title']} · matched support context {j + 1}",
                    "sourceGroup": base["sourceGroup"], "capacity": base["capacity"],
                    "split": base["split"], "sampling": "geometry-contrast",
                    "introducedVersion": "2.3", "evaluationCohort": "primary-matched"})
                ids.append(profile_id)
                kept_inventories.append(inventory(rebuilt, range(len(rebuilt.parts))))
            assert kept_inventories[0] == kept_inventories[1]
            pairs.append({
                "id": prefix + "/geometry", "profiles": ids, "introducedVersion": "2.3",
                "evaluationCohort": "primary-matched", "sourceGroup": base["sourceGroup"],
                "split": base["split"],
                "fixedContext": {
                    "equalPartCount": True, "sameRemovedPartTypes": True,
                    "sameRemovedPartTypeColorInventory": True, "sameRetainedPartTypeColorInventory": True,
                    "removedSourceIndices": [[domain.parts[i]["sourceIndex"] for i in r] for r in spec[:2]],
                    "retainedInventoryHash": canonical_hash(kept_inventories[0])},
                "qualification": {
                    "sourcePosesUnchanged": True, "meshesAndPathsRecomputed": True,
                    "sourceManifestHash": domain.source["provenance"]["manifestSha256"]}})
        record_path.parent.mkdir(exist_ok=True)
        record_path.write_text(json.dumps({
            "inputHash": admission_hash, "profiles": profiles[before[0]:],
            "pairs": pairs[before[1]:], "census": row}, indent=2) + "\n")
        domain.supported.cache_clear()
    if args.profile:
        return
    result = {
        "schema": "brickplan-geometry-contrasts/2.3", "profiles": profiles, "pairs": pairs,
        "census": census, "predecessorPreserved": True,
        "primaryRule": "Exact count/type/color matching; original induced subsets; no unequal fallback.",
    }
    output = (HERE.parents[1] / "tem/research/20261010-brickplan-v23-diversity/matched-pilot.json"
              if args.pilot else HERE / "data/geometry-contrasts.json")
    output.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
