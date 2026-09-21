#!/usr/bin/env python3
"""Independently recompute source golds and A-only shortcut predictions."""
from collections import Counter
from fractions import Fraction

from common import DATA, VERSION, frozen, load, save, sha
from assignment import CHOICES, HEURISTICS, candidate_inventory, shortcut_predictions
from estimates import estimate
from authors import sensitivity


def score(rows):
    return {"pairs": len(rows), "sources": len({r["source_id"] for r in rows}),
            "metrics": {k:estimate(rows,k) for k in ["A_acc","NewAcc","Both"]},
            "per_pair": rows, "B_error_pairs": [r["pair_id"] for r in rows if not r["NewAcc"]]}


def analyze(manifest):
    observations = {o["observation_id"]:o for o in manifest["observations"]}
    inventory = {r["parent_task_id"]:r for r in candidate_inventory()}
    bundles = {s:frozen(f"public/benchmark/ldraw-v2/models/{s}.json")
               for s in {p["source_id"] for p in manifest["pairs"]}}
    groups = {}
    for family in ["color","shape-match"]:
        pairs = [p for p in manifest["pairs"] if p["family"] == family]
        marginals = {arm:{c:0 for c in CHOICES} for arm in ["a","b"]}
        matrix = {a:{b:0 for b in CHOICES} for a in CHOICES}
        baselines = {}
        for p in pairs:
            a,b = observations[p["a"]],observations[p["b"]]
            assert a["payload"] == b["payload"]
            golds = []
            for o in [a,b]:
                if family == "color":
                    semantic = o["render_spec"]["body_color"]["name"]
                else:
                    parts = {r["id"]:r for r in bundles[p["source_id"]]["parts"]}
                    typ = parts[o["render_spec"]["target_id"]]["partNumber"]
                    candidates = [x for x in o["payload"]["options"] if any(
                        label == x["label"] and parts[cid]["partNumber"] == typ
                        for cid,label in o["render_spec"]["labels"].items())]
                    assert len(candidates) == 1, (p["pair_id"],"No unique independent source gold")
                    semantic = candidates[0]["label"]
                choice = next(c["id"] for c in o["payload"]["options"] if c["label"] == semantic)
                assert o["gold"] == {"choiceId":choice}
                golds.append(choice)
            ga,gb = golds
            assert ga != gb
            marginals["a"][ga] += 1; marginals["b"][gb] += 1; matrix[ga][gb] += 1
            predictions = {"fixed-"+c:(c,c,"no-image") for c in CHOICES}
            options = a["payload"]["options"]
            for name,reverse in [("smallest-option-label",False),("largest-option-label",True)]:
                c = sorted(options,key=lambda x:x["label"],reverse=reverse)[0]["id"]
                predictions[name] = (c,c,"text-only")
            simple = {"first-alternative":next(c for c in CHOICES if c!=ga),
                "last-alternative":next(c for c in reversed(CHOICES) if c!=ga),
                "cyclic-next":CHOICES[(CHOICES.index(ga)+1)%4],
                "cyclic-previous":CHOICES[(CHOICES.index(ga)-1)%4],
                "cyclic-two":CHOICES[(CHOICES.index(ga)+2)%4]}
            if family == "shape-match":
                verified_a, simple = shortcut_predictions(inventory[p["parent_task_id"]],
                                                          [o["label"] for o in options])
                assert verified_a == ga
            predictions.update({"oracle-A/"+name:(ga,c,"oracle-A-no-B-image") for name,c in simple.items()})
            for name,(pa,pb,access) in predictions.items():
                baselines.setdefault(name,[]).append({
                    "pair_id":p["pair_id"],"parent_task_id":p["parent_task_id"],"source_id":p["source_id"],
                    "a_prediction":pa,"b_prediction":pb,"a_gold":ga,"b_gold":gb,
                    "A_acc":int(pa==ga),"NewAcc":int(pb==gb),"Both":int(pa==ga and pb==gb),
                    "access":access})
        groups[family] = {"pairs":len(pairs),"sources":len({p["source_id"] for p in pairs}),
            "gold_marginals":marginals,"transition_matrix":matrix,
            "global_A_choice_only_ceiling":sum(max(row.values()) for row in matrix.values())/len(pairs),
            "baselines":{name:score(rows) for name,rows in baselines.items()}}
    return {"analysis_version":VERSION,"evidence_kind":"deterministic-shortcut-audit",
            "families":groups,"model_outputs_used":False,
            "interpretation":"Oracle-A attacks receive the correct A choice; spatial attacks additionally use A-side source geometry. No attack reads B pixels. Bounds cover only the declared rules."}


def enforce(report):
    p = report["families"]["shape-match"]
    contract = load(DATA / "assignment-contract.json")
    assert sha(DATA / "assignment-contract.json") == load(DATA / "part-type-assignment.json")["contract_sha256"]
    assert p["pairs"] == contract["pairs"] == 67
    assert all(16 <= n <= 17 for arm in p["gold_marginals"].values() for n in arm.values())
    assert all(n == 0 if a == b else 5 <= n <= 6
               for a,row in p["transition_matrix"].items() for b,n in row.items())
    for name,b in p["baselines"].items():
        if name.startswith("fixed-"):
            assert all(b["metrics"][k]["source_macro"] <= .30+1e-12 for k in ["A_acc","NewAcc"])
        if name.startswith("oracle-A/"):
            rows = b["per_pair"]
            bysource = Counter(r["source_id"] for r in rows)
            micro = Fraction(sum(r["NewAcc"] for r in rows),len(rows))
            macro = sum(Fraction(r["NewAcc"],bysource[r["source_id"]]) for r in rows)/len(bysource)
            assert micro <= Fraction(2,5) and macro <= Fraction(2,5), name
    assert {"oracle-A/"+h for h in HEURISTICS} <= set(p["baselines"])
    return True


def gate():
    manifest = load(DATA / "visual-manifest.json")
    assert manifest["assignment_sha256"] == sha(DATA / "part-type-assignment.json")
    report = analyze(manifest)
    enforce(report)
    return report


def main():
    prior = analyze(frozen("benchmark/ldraw-evidence-v2/visual-manifest.json"))
    prior["analysis_role"] = "historical rejected mechanism; never a current release gate"
    save(DATA / "historical-prior-audit.json",prior,immutable=True)
    report = gate()
    for f in report["families"].values():
        for b in f["baselines"].values():
            b["author_sensitivity"] = sensitivity(b["per_pair"],"NewAcc")
    report["status"] = "passed-preregistered-part-type-bounds"
    report["manifest_sha256"] = sha(DATA / "visual-manifest.json")
    report["assignment_contract_sha256"] = sha(DATA / "assignment-contract.json")
    save(DATA / "answer-prior-audit.json",report,immutable=True)
    print({"status":report["status"],
           "old_first_alternative_hits":sum(r["Both"] for r in prior["families"]["shape-match"]["baselines"]["oracle-A/first-alternative"]["per_pair"]),
           "new_first_alternative":report["families"]["shape-match"]["baselines"]["oracle-A/first-alternative"]["metrics"]["Both"],
           "new_marginals":report["families"]["shape-match"]["gold_marginals"]})


if __name__ == "__main__":
    main()
