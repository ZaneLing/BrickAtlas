#!/usr/bin/env python3
"""Author dependence and complete part-inventory overlap sensitivity."""
from collections import Counter, defaultdict
from itertools import combinations
import re

import numpy as np

from common import DATA, VERSION, digest, frozen, load, save
from estimates import SEED, RESAMPLES, estimate, mean, source_values


def credit_name(raw):
    return re.sub(r"\s*\[[^\]]*\]", "", raw).strip()


def freeze():
    catalog = frozen("benchmark/ldraw-v2/catalog.json")
    rows, inventory = [], {}
    for m in catalog:
        credits = m["author"].split(", OMR by ")
        primary = credit_name(credits[0])
        people = [credit_name(c) for c in credits]
        rows.append({"source_id": m["id"], "raw_credit": m["author"],
            "primary_author": primary, "primary_author_id": "author-" + digest(primary)[:16],
            "contributors": people, "source_sha256": m["sourceHash"], "url": m["sourceUrl"]})
        bundle = frozen(f"public/benchmark/ldraw-v2/models/{m['id']}.json")
        inventory[m["id"]] = Counter(p["partNumber"] for p in bundle["parts"])
    # Sources connected through any credited author/editor share one sensitivity cluster.
    parent = {r["source_id"]: r["source_id"] for r in rows}
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    for a,b in combinations(rows, 2):
        if set(a["contributors"]) & set(b["contributors"]):
            parent[find(a["source_id"])] = find(b["source_id"])
    clusters = defaultdict(list)
    for r in rows:
        clusters[find(r["source_id"])].append(r["source_id"])
    for r in rows:
        members = sorted(clusters[find(r["source_id"])])
        r["contributor_cluster"] = "credit-" + digest(members)[:16]
    pairs = []
    for a,b in combinations(sorted(inventory), 2):
        ca,cb = inventory[a], inventory[b]
        union = set(ca)|set(cb)
        pairs.append({"source_a": a, "source_b": b,
            "part_multiset_weighted_jaccard": sum(min(ca[k],cb[k]) for k in union) / sum(max(ca[k],cb[k]) for k in union),
            "part_type_set_jaccard": len(set(ca)&set(cb)) / len(union),
            "shared_part_types": len(set(ca)&set(cb)),
            "placed_parts_a": sum(ca.values()), "placed_parts_b": sum(cb.values())})
    save(DATA / "source-dependence.json", {
        "analysis_version": VERSION, "sources": len(rows),
        "primary_author_groups": len({r["primary_author_id"] for r in rows}),
        "contributor_connected_groups": len(clusters), "rows": rows,
        "primary_rule": "First credited model author; bracketed handles removed; OMR editor retained separately.",
        "secondary_rule": "Connected source groups sharing any credited model author or OMR editor.",
        "source_interval_policy": "Equal-source remains primary; author weighting and contributor clusters are sensitivity analyses.",
        "overlap_definition": "Part-number set and count-multiset overlap only; not aligned spatial geometry or a difficulty estimate.",
        "inventory_pairs": sorted(pairs, key=lambda p:(-p["part_multiset_weighted_jaccard"],p["source_a"],p["source_b"]))
    }, immutable=True)
    print({"status": "frozen", "sources": len(rows),
           "primary_author_groups": len({r["primary_author_id"] for r in rows}),
           "contributor_clusters": len(clusters), "inventory_pairs": len(pairs)})


def sensitivity(rows, key, grouping="primary_author_id", resamples=RESAMPLES):
    source = source_values(rows, key)
    mapping = {r["source_id"]: r[grouping] for r in load(DATA / "source-dependence.json")["rows"]}
    assert set(source) <= set(mapping)
    groups = defaultdict(list)
    for sid,value in source.items():
        groups[mapping[sid]].append(value)
    means = {a:mean(v) for a,v in sorted(groups.items())}
    if not means:
        return {"grouping": grouping, "eligible_sources": 0, "eligible_groups": 0,
                "source_macro": None, "group_macro": None, "group_macro_ci95": None,
                "group_minus_source": None, "leave_one_group_out": []}
    ids = sorted(groups)
    gm = np.array([means[g] for g in ids])
    totals = np.array([sum(groups[g]) for g in ids])
    counts = np.array([len(groups[g]) for g in ids])
    rng = np.random.default_rng(SEED)
    draws = rng.integers(0, len(ids), (resamples, len(ids)))
    author_boot = gm[draws].mean(axis=1)
    source_boot = totals[draws].sum(axis=1)/counts[draws].sum(axis=1)
    interval = lambda values: np.quantile(values,[.025,.975]).tolist() if len(ids)>=2 else None
    loao = []
    for removed in ids:
        retained = {s:v for s,v in source.items() if mapping[s]!=removed}
        loao.append({"omitted_group": removed, "sources": len(retained),
            "source_macro": mean(list(retained.values())),
            "group_macro": mean([v for a,v in means.items() if a!=removed])})
    return {"grouping": grouping, "eligible_sources": len(source), "eligible_groups": len(groups),
        "source_macro": mean(list(source.values())), "group_macro": mean(list(means.values())),
        "group_macro_ci95": interval(author_boot),
        "source_macro_group_cluster_ci95": interval(source_boot),
        "group_minus_source": mean(list(means.values()))-mean(list(source.values())),
        "group_minus_source_ci95": interval(author_boot-source_boot),
        "group_values": means, "leave_one_group_out": loao,
        "resamples": resamples, "seed": SEED,
        "interpretation": "Resamples author/contributor groups; no inference about cross-call service variability."}


def comparison_sensitivity(a, b, key):
    other = {r["pair_id"]: r for r in b}
    assert {r["pair_id"] for r in a} == set(other)
    differences = [{"source_id": r["source_id"], key: r[key]-other[r["pair_id"]][key]}
                   for r in a if r[key] is not None and other[r["pair_id"]][key] is not None]
    result = {}
    for grouping in ["primary_author_id", "contributor_cluster"]:
        report = sensitivity(differences, key, grouping)
        point = report["source_macro"]
        sign = lambda x: 0 if x==0 else 1 if x>0 else -1
        report["leave_one_group_direction_changes"] = [
            r["omitted_group"] for r in report["leave_one_group_out"]
            if point is not None and r["source_macro"] is not None and
            sign(r["source_macro"]) != sign(point)]
        result[grouping] = report
    return result


if __name__ == "__main__":
    freeze()
