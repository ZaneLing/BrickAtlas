"""Explicit source selection, admitted only after complete certification."""

INCLUDED = [i for i in range(35) if i not in (*range(11, 15), *range(21, 28))]
FIXED = [1, 2, 5]
EXTRA_CASES = [{
    "id": "airframe",
    "model": "31028",
    "title": "Airframe fuselage, tail and upper plates",
    "provenanceGroup": "LEGO-31028",
    "included": INCLUDED,
    "mutable": [i for i in INCLUDED if i not in FIXED],
    "counterfactual": {
        "closureSources": [15, 17],
        "interiorSources": [9, 0],
        # 10 supports 15 without 9; 3/4 support 17 without 0.
        # Both omitted branches still have to be installed before their covers.
        "checkpointOccupiedSources": [3, 4, 10],
    },
}]
