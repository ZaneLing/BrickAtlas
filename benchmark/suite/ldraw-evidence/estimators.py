"""Parent-balanced, source-cluster paired estimates with explicit denominators."""
from collections import defaultdict
import random


def quantile(values, q):
    values = sorted(values)
    k = q * (len(values) - 1)
    low = int(k)
    return values[low] * (1 - k + low) + values[min(low + 1, len(values) - 1)] * (k - low)


def estimate(rows, field, resamples=10000, seed=20260919):
    if not rows:
        return {"pairs": 0, "parents": 0, "sources": 0, "micro": None,
                "parent_macro": None, "source_macro": None, "source_macro_ci95": None}
    groups = defaultdict(lambda: defaultdict(list))
    for r in rows:
        v = r[field]
        if not isinstance(v, (bool, int, float)) or not -1 <= v <= 1:
            raise ValueError(f"Invalid bounded metric: {field}")
        groups[r["source_id"]][r["parent_task_id"]].append(float(v))
    blocks = [[sum(v) / len(v) for v in parents.values()] for _, parents in sorted(groups.items())]
    means = [sum(b) / len(b) for b in blocks]
    rng = random.Random(seed)
    draws = [sum(means[rng.randrange(len(means))] for _ in means) / len(means) for _ in range(resamples)]
    return {"pairs": len(rows), "parents": sum(len(b) for b in blocks), "sources": len(blocks),
            "micro": sum(r[field] for r in rows) / len(rows),
            "parent_macro": sum(sum(b) for b in blocks) / sum(len(b) for b in blocks),
            "source_macro": sum(means) / len(means),
            "source_macro_ci95": [quantile(draws, .025), quantile(draws, .975)],
            "bootstrap": {"resamples": resamples, "seed": seed, "unit": "source",
                          "weighting": "variants within parent, parents within source, sources equally"}}


def paired_difference(rows, a, b, resamples=10000, seed=20260919):
    return estimate([{**r, "delta": r[a] - r[b]} for r in rows], "delta", resamples, seed)
