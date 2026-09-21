"""Source-balanced paired estimates; explicit empty and boundary behavior."""
from collections import defaultdict
import math

import numpy as np

SEED = 20260920
RESAMPLES = 10000


def mean(values):
    return sum(values) / len(values) if values else None


def wilson(hits, n):
    if not n:
        return None
    z = 1.959963984540054
    p, z2 = hits / n, z * z
    center = (p + z2 / (2 * n)) / (1 + z2 / n)
    half = z * math.sqrt(p * (1 - p) / n + z2 / (4 * n * n)) / (1 + z2 / n)
    return [0. if hits == 0 else max(0., center - half),
            1. if hits == n else min(1., center + half)]


def source_values(rows, key):
    groups = defaultdict(list)
    for row in rows:
        # None means undefined conditional denominator, never missing model output.
        if row[key] is not None:
            groups[row["source_id"]].append(float(row[key]))
    return {s: mean(v) for s, v in sorted(groups.items())}


def estimate(rows, key, resamples=RESAMPLES):
    values = [float(r[key]) for r in rows if r[key] is not None]
    sources = source_values(rows, key)
    array = np.array(list(sources.values()), dtype=float)
    ci = None
    if len(array) >= 2:
        rng = np.random.default_rng(SEED)
        draws = array[rng.integers(0, len(array), (resamples, len(array)))].mean(axis=1)
        ci = np.quantile(draws, [.025, .975]).tolist()
    return {"n": len(values), "sources": len(sources), "micro": mean(values),
            "source_macro": mean(list(sources.values())), "source_macro_ci95": ci,
            "source_values": sources, "resamples": resamples,
            "interval_method": "percentile bootstrap of whole source means; equal source weight",
            "interval_limit": "descriptive at fixed sources; boundary samples may give degenerate intervals"}


def selection_shift(full, subset, key, resamples=RESAMPLES):
    """QA-minus-full macro difference using shared source-resampling weights.

    Each replicate draws from full sources, then recomputes both estimands.
    Subset means use only selected sources in that draw. Empty draws are
    excluded explicitly. This retains the source-coverage change, not just
    within-source selection, and never treats the overlapping samples as iid.
    """
    a, b = source_values(full, key), source_values(subset, key)
    assert set(b) <= set(a)
    if not a or not b:
        return {"difference": None, "ci95": None, "full_sources": len(a),
                "subset_sources": len(b), "undefined_reason": "empty full or QA subset"}
    ids = sorted(a)
    av = np.array([a[s] for s in ids])
    bv = np.array([b.get(s, 0.) for s in ids])
    present = np.array([int(s in b) for s in ids])
    rng = np.random.default_rng(SEED)
    idx = rng.integers(0, len(ids), (resamples, len(ids)))
    denominator = present[idx].sum(axis=1)
    valid = denominator > 0
    delta = bv[idx][valid].sum(axis=1) / denominator[valid] - av[idx][valid].mean(axis=1)
    return {"difference": mean(list(b.values())) - mean(list(a.values())),
            "ci95": np.quantile(delta, [.025, .975]).tolist() if len(ids) >= 2 and len(delta) else None,
            "full_sources": len(a), "subset_sources": len(b),
            "undefined_bootstrap_draws": int((~valid).sum()),
            "method": "shared whole-source resampling; recompute full and selected source macro"}


def ranks(values):
    """Descending midranks; exact ties stay ties."""
    return {name: 1 + sum(v > value for v in values.values())
            + (sum(v == value for v in values.values()) - 1) / 2
            for name, value in values.items()}


def sign(value):
    return None if value is None else 1 if value > 0 else -1 if value < 0 else 0
