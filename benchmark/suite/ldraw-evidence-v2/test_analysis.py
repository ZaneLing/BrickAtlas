"""Statistical/graph fixtures exercise errors; they never register as results."""
import copy
import json
from fractions import Fraction
from pathlib import Path
import tempfile
import unittest

import analyze
import graph_run
from common import DATA, load
from estimates import estimate, ranks, selection_shift, wilson
from graph_audit import adjacency, bfs, lookup, union_find, wl_signature


def fixture(outcomes, qa_flags=None):
    # Each item is (a response, b response), with old gold A and new gold B.
    pairs, rows, qa = [], [], []
    for i, (a, b) in enumerate(outcomes):
        p = {"pair_id": f"pair-{i}", "parent_task_id": f"task-{i}", "source_id": f"source-{i//2}",
             "family": "color", "a": f"a-{i}", "b": f"b-{i}"}
        pairs.append(p)
        qa.append({"pair_id": p["pair_id"], "both_decidable": qa_flags[i] if qa_flags else True,
                   "exclusion_reasons": [] if not qa_flags or qa_flags[i] else ["resolution"]})
        for arm, response, gold in [("a", a, "A"), ("b", b, "B")]:
            rows.append({"observation_id": p[arm], "family": "color", "source_id": p["source_id"],
                         "answer": {"choiceId": response} if response else None, "gold": {"choiceId": gold},
                         "valid_format": response is not None,
                         "failure_reason": "invalid-json" if response is None else None, "receipt_file": None})
    return analyze.pair_rows({"pairs": pairs}, {"rows": rows}, {"pairs": qa})


class AnalysisTests(unittest.TestCase):
    def test_partition_and_all_denominator(self):
        rows = fixture([("A", "B"), ("A", "A"), ("C", "C"), (None, None)])
        summary = analyze.summarize(rows)
        self.assertEqual(summary["pairs"], 4)
        self.assertEqual(summary["metrics"]["Both"]["micro"], .25)
        self.assertEqual(summary["metrics"]["conditional_adaptation"]["n"], 2)
        self.assertEqual(summary["metrics"]["conditional_adaptation"]["micro"], .5)
        self.assertEqual(sum(summary["metrics"][k]["micro"] for k in
                             ["NewAcc", "old_gold_retention", "other_wrong", "invalid_B"]), 1)
        self.assertTrue(rows[2]["same_valid_wrong_answer"])
        self.assertFalse(rows[3]["same_valid_wrong_answer"])

    def test_empty_conditional_and_source_macro(self):
        rows = [{"source_id": "s1", "x": 1}, {"source_id": "s2", "x": 0}, {"source_id": "s2", "x": 0}]
        e = estimate(rows, "x", 100)
        self.assertEqual(e["micro"], 1/3)
        self.assertEqual(e["source_macro"], .5)
        no_anchor = analyze.summarize(fixture([("C", "B"), (None, None)]))
        self.assertIsNone(no_anchor["metrics"]["conditional_adaptation"]["source_macro"])
        self.assertEqual(no_anchor["metrics"]["conditional_adaptation"]["n"], 0)

    def test_qa_subset_retains_full_results(self):
        rows = fixture([("A", "B"), ("A", "A"), ("C", "B"), (None, None)], [True, False, True, False])
        report = analyze.family_report(rows)
        self.assertEqual(report["full"]["pairs"], 4)
        self.assertEqual(report["both_decidable"]["pairs"], 2)
        self.assertEqual(report["exclusions"]["resolution"], {"pairs": 2, "sources": 2})
        self.assertEqual(report["qa_minus_full"]["NewAcc"]["difference"], .5)
        same = selection_shift(rows, rows, "Both", 100)
        self.assertEqual(same["difference"], 0)
        self.assertEqual(same["ci95"], [0, 0])
        self.assertIsNone(selection_shift(rows, [], "Both")["difference"])

    def test_reversal_and_ties_are_distinct(self):
        a = fixture([("A", "B"), ("A", "A"), ("A", "A"), ("A", "A")])
        b = fixture([("A", "B"), ("A", "B"), ("C", "C"), ("C", "C")])
        c = copy.deepcopy(a)
        report = analyze.comparisons([{"run_id": n, "pair_rows": r} for n, r in [("x", a), ("y", b), ("z", c)]],
                                     "color", "full")
        xy = next(r for r in report["pairwise"] if r["model_x"] == "x" and r["model_y"] == "y")
        xz = next(r for r in report["pairwise"] if r["model_x"] == "x" and r["model_y"] == "z")
        self.assertTrue(xy["strict_rank_reversal"])
        self.assertFalse(xz["strict_rank_reversal"])
        self.assertTrue(xz["tie_in_either_ranking"])
        self.assertEqual(ranks({"x": Fraction(1, 3), "y": Fraction(2, 6), "z": Fraction(1, 4)}),
                         {"x": 1.5, "y": 1.5, "z": 3})

    def test_boundary_pair_interval_is_not_zero_width(self):
        self.assertGreater(wilson(0, 12)[1], .24)
        self.assertLess(wilson(12, 12)[0], .76)
        self.assertIsNone(wilson(0, 0))

    def test_dry_run_cannot_be_published(self):
        with tempfile.TemporaryDirectory() as d:
            dest = Path(d) / "must-not-exist.json"
            with self.assertRaises(AssertionError):
                analyze.build([DATA / "runs/wire-audit-final"], dest)
            self.assertFalse(dest.exists())

    def test_real_cases_require_real_receipts(self):
        rows = fixture([("A", "B")])
        with self.assertRaises((KeyError, AssertionError)):
            analyze.raw_cases({"run_id": "fixture-only", "pair_rows": rows}, {})

    def test_wl_blindspot_is_real_and_permutation_invariant(self):
        nodes = ["t", *"abcdef", "isolated"]
        ring = [list(e) for e in ["ab", "bc", "cd", "de", "ef", "fa"]]
        triangles = [list(e) for e in ["ab", "bc", "ca", "de", "ef", "fd"]]
        a, b = adjacency(nodes, ring, "t"), adjacency(nodes, triangles, "t")
        self.assertEqual(wl_signature(a), wl_signature(b))
        self.assertEqual(len(bfs(a)), 2)
        self.assertEqual(len(bfs(b)), 3)
        self.assertEqual(union_find(nodes, triangles, "t"), 3)
        mapping = {n: str(i) for i, n in enumerate(reversed(nodes))}
        c = adjacency([mapping[n] for n in nodes], [[mapping[x] for x in e] for e in ring], mapping["t"])
        self.assertEqual(wl_signature(a), wl_signature(c))

    def test_lookup_never_uses_target_source_labels(self):
        target = {"source_id": "held", "features": {"degree-histogram": "key"}, "gold": 10}
        train = [target, {"source_id": "other", "features": {"degree-histogram": "key"}, "gold": 2}]
        prediction = lookup(target, train, "degree-histogram")
        self.assertEqual(prediction["prediction"], 2)
        self.assertEqual(prediction["training_sources"], ["other"])
        self.assertIsNone(lookup(target, [target], "degree-histogram")["prediction"])

    def test_released_roles_and_baselines(self):
        report = load(DATA / "graph-audit.json")
        strong = report["summary"]["strong-change"]
        weak = report["summary"]["degree-visible-control"]
        self.assertEqual((strong["pairs"], strong["sources"]), (12, 8))
        self.assertEqual(weak["pairs"], 61)
        for method in ["degree-histogram-lookup", "anonymous-1wl-lookup", "isolates-plus-one"]:
            self.assertEqual(strong["baselines"][method]["both"]["micro"], 0)
            self.assertEqual(weak["baselines"][method]["both"]["micro"], 1)
        self.assertEqual(strong["baselines"]["bfs"]["both"]["micro"], 1)
        for row in report["pairs"]:
            if row["role"] == "strong-change":
                self.assertTrue(all(row["constraints"].values()))
                self.assertTrue(row["wl_indistinguishable"])

    def test_graph_integer_contract_rejects_extra_keys_boolean_and_duplicate(self):
        adapter = load(DATA / "adapter.example.json")
        for text, valid in [('{"value":2}', True), ('{"value":true}', False),
                            ('{"value":2,"extra":0}', False), ('{"value":2,"value":1}', False),
                            ('{"value":10}', False), ('{"value":2.0}', False)]:
            receipt = {"http_status": 200, "raw_response": json.dumps({"model": adapter["response_model"],
                       "choices": [{"message": {"content": text}}]})}
            self.assertEqual(graph_run.parse_graph(receipt, 6, adapter)["valid_format"], valid)

    def test_graph_dry_snapshot_tamper_and_registration_gate(self):
        with tempfile.TemporaryDirectory() as d:
            dest = Path(d) / "graph-fixture"
            graph_run.run(dest, load(DATA / "adapter.example.json"))
            result = graph_run.verify(dest)
            self.assertEqual(len(result["rows"]), 219)
            self.assertTrue(all(r["success"] is None for r in result["rows"]))
            with self.assertRaises(AssertionError):
                graph_run.analyze(dest)
            request = next((dest / "requests").glob("*.json"))
            request.write_text(request.read_text() + " ")
            with self.assertRaises(AssertionError):
                graph_run.verify(dest)


if __name__ == "__main__":
    unittest.main(verbosity=2)
