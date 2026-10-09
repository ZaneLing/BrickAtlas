"""Small, explicit source selections. Nothing here asserts they pass qualification."""

CASES = [
    {
        "id": "roadster-body",
        "model": "31027",
        "title": "Roadster body panels",
        "included": [i for i in range(47) if i not in (1, 13) and i not in range(19, 27)],
        "mutable": [9, 10, 28, 29, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46],
        "counterfactual": {
            "closureSources": [28, 29],
            "interiorSources": [9, 10],
            "checkpoint": "empty",
        },
    },
    {
        "id": "kart-deck",
        "model": "31027-kart",
        "title": "Kart deck and rear grille",
        "included": [0] + list(range(3, 27)),
        "mutable": [8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26],
        "reversePaths": [12, 13],
        "counterfactual": {
            "closureSources": [19, 22],
            "interiorSources": [18, 21],
            "checkpoint": "all-except-pair",
        },
    },
]
