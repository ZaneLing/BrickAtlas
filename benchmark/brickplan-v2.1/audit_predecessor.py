"""Read-only exhaustive static-formula audit of the frozen 1.2 cost labels."""
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "brickplan-v1.2"))
from build import load_bank
from cases import CASES


def closure(domain, state, goal):
    remove = state & ~goal
    missing = goal & ~state
    while missing:
        bit = missing & -missing
        missing ^= bit
        remove |= state & domain.blockers[bit.bit_length() - 1]
    frontier = remove
    while frontier:
        bit = frontier & -frontier
        frontier ^= bit
        extra = state & domain.blockers[bit.bit_length() - 1] & ~remove
        remove |= extra
        frontier |= extra
    return remove


def main():
    rows = []
    for case in CASES:
        domain, _, tables, _ = load_bank(case["id"])
        checked = equal = 0
        exceptions = []
        for target, costs in tables.items():
            goal = int(target)
            for state, cost in enumerate(costs):
                if cost < 0:
                    continue
                predicted = (state ^ goal).bit_count() + 2 * (closure(domain, state, goal) & goal).bit_count()
                checked += 1
                equal += predicted == cost
                if predicted != cost:
                    exceptions.append({"start": state, "goal": goal, "cost": cost, "staticLower": predicted})
        rows.append({"case": case["id"], "goals": len(tables), "checked": checked,
                     "exactStaticFormula": equal, "exceptions": exceptions[:10]})
    expected = json.loads((HERE / "data/predecessor-static-audit.json").read_text())
    if rows != expected or any(r["checked"] != r["exactStaticFormula"] for r in rows):
        raise AssertionError("Predecessor audit disagrees with archived evidence")
    print(json.dumps({"passed": True, "rows": rows, "labels": sum(r["checked"] for r in rows)}, indent=2))


if __name__ == "__main__":
    main()
