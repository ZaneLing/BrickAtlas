"""Construct, exposure, inclusion and failure-denominator regression tests."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import shutil
import unittest
from unittest.mock import patch

from common import DATA, ROOT, load, save, sha, digest
import qa
import roster
import run
from transport import parse_receipt
from priors import enforce
from assignment import shortcut_predictions
from authors import sensitivity, comparison_sensitivity
from estimates import estimate, selection_shift
from analyze import pair_rows, build


class AssignmentTests(unittest.TestCase):
    def test_preregistered_bounds_and_independent_rules(self):
        audit=load(DATA/"answer-prior-audit.json")
        self.assertTrue(enforce(audit))
        rows=load(DATA/"part-type-assignment.json")["rows"]
        inventory={r["parent_task_id"]:r for r in load(DATA/"candidate-inventory.json")["rows"]}
        for r in rows:
            a,p=shortcut_predictions(inventory[r["parent_task_id"]],r["option_labels"])
            self.assertEqual(a,r["a_gold"]); self.assertEqual(p,r["oracle_A_predictions"])

    def test_reject_collapsed_marginal(self):
        audit=deepcopy(load(DATA/"answer-prior-audit.json"))
        audit["families"]["shape-match"]["gold_marginals"]["b"]={"A":57,"B":10,"C":0,"D":0}
        with self.assertRaises(AssertionError): enforce(audit)

    def test_reject_deterministic_transition(self):
        audit=deepcopy(load(DATA/"answer-prior-audit.json"))
        audit["families"]["shape-match"]["transition_matrix"]["C"]["A"]=17
        with self.assertRaises(AssertionError): enforce(audit)

    def test_reject_source_weighted_shortcut(self):
        audit=deepcopy(load(DATA/"answer-prior-audit.json"))
        rows=audit["families"]["shape-match"]["baselines"]["oracle-A/first-alternative"]["per_pair"]
        for r in rows: r["NewAcc"]=1
        with self.assertRaises(AssertionError): enforce(audit)

    def test_part_type_renewed_both_arms_color_preserved(self):
        old=load(DATA.parent/"ldraw-evidence-v2/visual-manifest.json")
        new=load(DATA/"visual-manifest.json")
        oldids={o["observation_id"] for o in old["observations"] if o["family"]=="shape-match" and o["role"]=="primary"}
        newids={o["observation_id"] for o in new["observations"] if o["family"]=="shape-match" and o["role"]=="primary"}
        self.assertEqual(len(newids),134); self.assertFalse(oldids&newids)
        for o in new["observations"]:
            if o["family"]=="color": self.assertIn(o,old["observations"])


class HumanReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        m,obs,wires=qa.assets()
        parents=sorted({o["parent_task_id"] for o in obs.values() if o["role"]=="position-reference-control"})[:3]
        cls.obs={k:v for k,v in obs.items() if v["parent_task_id"] in parents}
        cls.wires={k:v for k,v in wires.items() if k in cls.obs}
        cls.m={**m,"pairs":[p for p in m["pairs"] if p["parent_task_id"] in parents],
               "observations":list(cls.obs.values())}

    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.folder=Path(self.tmp.name)
        self.patcher=patch.object(qa,"assets",return_value=(self.m,self.obs,self.wires))
        self.patcher.start()
        qa.export(self.folder/"queues")
        self.mapping=load(self.folder/"queues/private-mapping.json")

    def tearDown(self):
        self.patcher.stop();self.tmp.cleanup()

    def feedback(self):
        paths=[]
        for slot,spec in self.mapping["slots"].items():
            reviews=[]
            for token,item in spec["items"].items():
                o=self.obs[item["observation_id"]]
                reviews.append({"review_id":token,"wire_observation_sha256":item["wire_observation_sha256"],
                    "reviewer":slot,"author_kind":"synthetic-fixture","timestamp":"2026-09-19T00:00:00Z",
                    "decision":"decidable","visual_choice":o["gold"]["choiceId"],
                    "checks":{k:True for k in qa.CHECKS},"reason_code":"none","reason":"Temporary software fixture",
                    "native_size_attestation":True,"independence_attestation":True})
            p=self.folder/(slot+".json");save(p,{"slot":slot,"queue_sha256":spec["queue_sha256"],
                "evidence_kind":"synthetic-fixture","reviewer":slot,"reviews":reviews})
            paths.append(p)
        return paths

    def test_assignment_disjoint_across_all_parent_views(self):
        a=qa.validate_assignment(self.mapping,self.obs,self.folder/"queues")
        self.assertEqual(a["reviews"],18);self.assertEqual(a["cross_arm_or_auxiliary_exposures"],0)
        for slot in self.mapping["slots"]:
            q=load(self.folder/"queues"/slot/"queue.json")
            self.assertTrue(all("gold" not in x and "arm" not in x and "parent_task_id" not in x for x in q["queue"]))

    def test_complete_dual_review(self):
        result=qa.combine(self.folder/"queues",self.feedback(),fixture=True)
        self.assertTrue(result["all_ready_for_inference"]);self.assertEqual(result["raw_review_count"],18)

    def test_b_only_remains_pending(self):
        paths=self.feedback()
        for p in paths:
            f=load(p)
            f["reviews"]=[r for r in f["reviews"] if self.obs[self.mapping["slots"][f["slot"]]["items"][r["review_id"]]["observation_id"]]["arm"]=="B"]
            save(p,f)
        result=qa.combine(self.folder/"queues",paths,fixture=True)
        self.assertFalse(result["primary_ready_for_inference"]);self.assertEqual(result["qa_comparable_pairs"],0)

    def test_same_identity_two_slots_rejected(self):
        paths=self.feedback(); f=load(paths[1]);f["reviewer"]="reviewer-1"
        for r in f["reviews"]:r["reviewer"]="reviewer-1"
        save(paths[1],f)
        with self.assertRaises(AssertionError):qa.combine(self.folder/"queues",paths,fixture=True)

    def test_stale_wire_rejected(self):
        paths=self.feedback();f=load(paths[0]);f["reviews"][0]["wire_observation_sha256"]="bad";save(paths[0],f)
        with self.assertRaises(AssertionError):qa.combine(self.folder/"queues",paths,fixture=True)

    def test_synthetic_not_human(self):
        with self.assertRaises(AssertionError):qa.combine(self.folder/"queues",self.feedback())

    def test_gold_conflict_blocks_final(self):
        paths=self.feedback()
        oid=next(iter(self.obs)); gold=self.obs[oid]["gold"]["choiceId"]
        for p in paths:
            f=load(p)
            for r in f["reviews"]:
                if self.mapping["slots"][f["slot"]]["items"][r["review_id"]]["observation_id"]==oid:
                    r["visual_choice"]=next(c for c in "ABCD" if c!=gold)
            save(p,f)
        result=qa.combine(self.folder/"queues",paths,fixture=True)
        row=next(r for r in result["rows"] if r["observation_id"]==oid)
        self.assertEqual(row["final_decision"],"pending")
        self.assertIn("oracle-conflict",row["final_reason"])

    def test_counterpart_adjudicator_rejected(self):
        paths=self.feedback()
        parent=next(iter(self.obs.values()))["parent_task_id"]
        ids=[o["observation_id"] for o in self.obs.values() if o["parent_task_id"]==parent][:2]
        for oid in ids:
            slot=sorted(qa.assigned_slots(self.obs)[oid])[0]
            p=next(p for p in paths if p.stem==slot);f=load(p)
            for r in f["reviews"]:
                if self.mapping["slots"][slot]["items"][r["review_id"]]["observation_id"]==oid:
                    r.update(decision="ambiguous",reason_code="other")
            save(p,f)
        pending=qa.combine(self.folder/"queues",paths,fixture=True)
        adjudications=[]
        for row in pending["rows"]:
            if row["observation_id"] in ids:
                r=deepcopy(row["reviews"][0]);r["reviewer"]="new-adjudicator"
                r["observation_id"]=row["observation_id"];r["review_hashes"]=[digest(x) for x in row["reviews"]]
                adjudications.append(r)
        p=self.folder/"adjudications.json";save(p,{"evidence_kind":"synthetic-fixture","adjudications":adjudications})
        with self.assertRaises(AssertionError):qa.combine(self.folder/"queues",paths,p,fixture=True)


class InclusionTests(unittest.TestCase):
    def test_roster_has_exact_nine(self):
        self.assertEqual(len(roster.planned()),9)
        self.assertEqual({p["planned_observations"] for p in roster.planned().values()},{219,347})

    def test_missing_extra_runs_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            with self.assertRaises(AssertionError):roster.exact_run_set(root)
            for rid in roster.planned():
                save(root/rid/"manifest.json",{})
            self.assertEqual(len(roster.exact_run_set(root)),9)
            (root/"unplanned").mkdir()
            with self.assertRaises(AssertionError):roster.exact_run_set(root)

    def test_free_model_not_accepted(self):
        with self.assertRaises(AssertionError):roster.specification("unplanned","visual")

    def test_no_image_removes_only_pixels(self):
        visual,obs,_=run.inputs("visual");noimage,_,_=run.inputs("no-image")
        self.assertEqual(len(visual),347)
        for oid in visual:
            expected=deepcopy(visual[oid])
            expected["messages"][1]["content"]=[expected["messages"][1]["content"][0]]
            self.assertEqual(noimage[oid],expected)

    def test_graph_dry_run_and_tamper(self):
        with tempfile.TemporaryDirectory() as tmp:
            m=run.run("gpt41","graph",root=tmp)
            dest=Path(tmp)/m["run_id"]
            v=run.verify(dest);self.assertEqual(v["status"],"not-run");self.assertEqual(len(v["rows"]),219)
            p=dest/m["requests"][0]["file"];p.write_text("{}")
            with self.assertRaises(AssertionError):run.verify(dest)

    def test_analyzer_missing_roster_cannot_publish(self):
        with tempfile.TemporaryDirectory() as tmp:
            output=Path(tmp)/"report.json"
            with self.assertRaises(AssertionError):build(Path(tmp)/"runs",output)
            self.assertFalse(output.exists())

    def test_live_qa_gate_precedes_directory_and_network(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(run,"verify_final",side_effect=AssertionError("pending")),patch.object(run,"call") as call:
            with self.assertRaises(AssertionError):run.run("gpt41","visual",qa_path="pending",live=True,root=tmp)
            self.assertFalse(list(Path(tmp).iterdir()));call.assert_not_called()

    def test_interrupted_run_closes_without_retry_and_preserves_all_failures(self):
        with tempfile.TemporaryDirectory() as tmp:
            temporary=Path(tmp)
            shutil.copyfile(DATA/"model-roster.json",temporary/"model-roster.json")
            response={"http_status":None,"raw_response":None,"transport_error":"timeout"}
            with patch.object(run,"DATA",temporary),patch.object(run,"prior_gate"),patch.dict("os.environ",{"BRICKATLAS_API_KEY":"synthetic-test-not-a-real-key"}),patch.object(run,"call",side_effect=[response,KeyboardInterrupt]) as call:
                with self.assertRaises(KeyboardInterrupt):run.run("gpt41","graph",live=True)
                dest=temporary/"model-runs/gpt41-graph-r1"
                run.close_interrupted(dest,"Synthetic interrupted transport test")
                verified=run.verify(dest)
                self.assertEqual(call.call_count,2)
                self.assertEqual(len(verified["rows"]),219)
                self.assertEqual(sum(r["success"] for r in verified["rows"]),0)
                failures=[r["failure_reason"] for r in verified["rows"]]
                self.assertEqual(failures.count("timeout"),1)
                self.assertEqual(failures.count("interrupted-no-receipt"),1)
                self.assertEqual(failures.count("unattempted-closed"),217)
                self.assertEqual(verified["status"],"closed-interrupted")


class ParsingStatisticsTests(unittest.TestCase):
    def setUp(self):
        self.adapter=load(DATA/"adapters/gpt41.json")

    def receipt(self,text,model=None):
        return {"http_status":200,"raw_response":json.dumps({"model":model or self.adapter["response_model"],
               "choices":[{"message":{"content":text}}]})}

    def test_strict_json_and_revision(self):
        for text in ['{"choiceId":"A","choiceId":"B"}','{"choiceId":"A"} prose','{"choiceId":NaN}','{"choiceId":true}']:
            self.assertFalse(parse_receipt(self.receipt(text),list("ABCD"),self.adapter)["valid_format"])
        with self.assertRaises(AssertionError):parse_receipt(self.receipt('{"choiceId":"A"}',"other"),list("ABCD"),self.adapter)

    def test_graph_integer_not_bool(self):
        self.assertFalse(parse_receipt(self.receipt('{"value":true}'),[],self.adapter,4)["valid_format"])
        self.assertTrue(parse_receipt(self.receipt('{"value":2}'),[],self.adapter,4)["valid_format"])

    def test_failure_denominator(self):
        rows=[{"source_id":"10001","correct":1},{"source_id":"10001","correct":0},{"source_id":"10014","correct":0}]
        r=estimate(rows,"correct")
        self.assertEqual(r["n"],3);self.assertEqual(r["micro"],1/3);self.assertEqual(r["source_macro"],.25)

    def test_author_weighting_and_leave_one_out(self):
        rows=[{"source_id":"10001","score":1},{"source_id":"10014","score":0},
              {"source_id":"10036","score":0},{"source_id":"31028","score":1}]
        r=sensitivity(rows,"score",resamples=100)
        self.assertEqual(r["eligible_sources"],4)
        self.assertEqual(len(r["leave_one_group_out"]),r["eligible_groups"])
        self.assertIsNotNone(r["group_macro_ci95"])

    def test_author_difference_uses_same_pairs(self):
        a=[{"pair_id":"a","source_id":"10001","x":1},{"pair_id":"b","source_id":"31028","x":0}]
        b=[{"pair_id":"a","source_id":"10001","x":0},{"pair_id":"b","source_id":"31028","x":1}]
        r=comparison_sensitivity(a,b,"x")
        self.assertEqual(r["primary_author_id"]["source_macro"],0)
        self.assertTrue(r["primary_author_id"]["leave_one_group_direction_changes"])

    def test_empty_subset_remains_null(self):
        self.assertIsNone(sensitivity([],"score")["group_macro"])
        self.assertIsNone(selection_shift([{"source_id":"10001","x":1}],[],"x")["difference"])


if __name__=="__main__":
    unittest.main()
