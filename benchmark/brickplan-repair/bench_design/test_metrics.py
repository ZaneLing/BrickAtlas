"""Numerical examples and attribution gates that materially affect conclusions."""
from collections import Counter
import unittest
from bench_design.metrics import state_metrics,execution_metrics,event_recovery,pair_metrics,aggregate,aggregate_pairs
from evaluation_outcomes import assess_run,pair_assessment
from bench_design.policy import descriptors


class ToyRuntime:
    def signature(self,state):return Counter(v for v in state.values() if v)


class MetricsTests(unittest.TestCase):
    def test_empty_prefix_still_requires_images_and_equal_budget(self):
        from types import SimpleNamespace
        from copy import deepcopy
        from bench_design.session import assess_pair
        def branch(scheduled):
            return SimpleNamespace(initial={},ep=SimpleNamespace(),cap=40,actor='scripted:proof',
                records=[dict(decision=1,action={'type':'finish'},newEventIndices=[])],
                result=lambda:dict(terminalStatus='completed',success=True,scheduledEvents=scheduled,
                                   appliedEvents=0,effectiveIncidentVerified=False))
        a,b=branch(0),branch(1)
        self.assertFalse(assess_pair(a,b,0)['sharedPrefixProof']['verified'])
        observation=dict(packetSha256='a'*64,imageHashes=[])
        for s in [a,b]:s.records[0]['observation']=deepcopy(observation)
        self.assertFalse(assess_pair(a,b,0)['sharedPrefixProof']['verified'])
        for s in [a,b]:s.records[0]['observation']['imageHashes']=['b'*64]
        self.assertTrue(assess_pair(a,b,0)['sharedPrefixProof']['verified'])
        b.cap=41
        self.assertFalse(assess_pair(a,b,0)['sharedPrefixProof']['verified'])

    def test_unobserved_event_window_is_not_a_repair_failure(self):
        a=('brick','red','p1')
        out=event_recovery(ToyRuntime(),{'a':a},{},{'a':a},[])
        self.assertIsNone(out['observedRecovery'])
        self.assertIsNone(out['retainedAfterRecovery'])

    def test_untriggered_remains_na_with_failed_control(self):
        c=dict(terminalStatus='completed',success=False)
        e=dict(terminalStatus='completed',success=False,scheduledEvents=2,appliedEvents=0,effectiveIncidentVerified=False)
        out=pair_metrics(c,e,shared_prefix_verified=True)
        self.assertEqual(out['repairJudgment'],'not_applicable')
        self.assertIn('untriggered',out['exclusionReasons'])
        self.assertIn('control_failed',out['exclusionReasons'])

    def test_pair_aggregation_preserves_both_denominators(self):
        base=dict(model='scripted',inputVersion='v2',track='whole-object-dynamic',taskType='D1',terminalStatus='completed',scheduledEvents=1,appliedEvents=1,effectiveIncidentVerified=True)
        pairs=[]
        for index,(control,fault) in enumerate([(True,True),(False,True)]):
            pairs.append(dict(control={**base,'success':control},intervention={**base,'success':fault,'conditionId':str(index)},sharedPrefixProof={'verified':True}))
        result=aggregate_pairs(pairs)[0]
        self.assertEqual(result['conditionalRecoveryEligibleN'],1)
        self.assertEqual(result['pairedComparisonN'],2)
        self.assertEqual(result['conditionalRecoveryRate'],1)
        self.assertEqual(result['pairedCompletionDrop'],-.5)
    def test_identical_pieces_and_temporary_dismantling(self):
        r=ToyRuntime();goal={'a':('brick','red','p1'),'b':('brick','red','p2')}
        swapped={'a':goal['b'],'b':goal['a']}
        m=state_metrics(r,goal,swapped,goal,finished=True)
        self.assertTrue(m['success']);self.assertEqual(m['finalDamageRate'],0)
        self.assertIsNone(m['errorReduction'])

    def test_errors_are_not_hidden_by_fixed_scenery(self):
        r=ToyRuntime();g={'x':('brick','red','p1')};i={'w':('brick','blue','p1')}
        m=state_metrics(r,i,{},g,finished=True)
        self.assertEqual(m['initialEditResidual'],2);self.assertEqual(m['finalEditResidual'],1)
        self.assertEqual(m['errorReduction'],.5);self.assertFalse(m['success'])
        self.assertIsNone(m['finalDamageRate']);self.assertEqual(m['fullPlacement']['f1'],0)

    def test_repair_does_not_require_old_prefix(self):
        r=ToyRuntime();a=('brick','red','p1');b=('brick','green','p2');c=('brick','blue','p3')
        m=event_recovery(r,{'a':a},{},{'a':a,'b':b,'c':c},[{'a':a,'b':b},{'a':a,'b':b,'c':c},{'a':a,'b':b,'c':c}])
        self.assertTrue(m['observedRecovery']);self.assertEqual(m['firstRecoveryDecision'],1)
        self.assertTrue(m['retainedAfterRecovery'])

    def test_regression_and_no_harmful_event(self):
        r=ToyRuntime();a=('brick','red','p1')
        m=event_recovery(r,{'a':a},{},{'a':a},[{'a':a},{},{}])
        self.assertFalse(m['observedRecovery']);self.assertFalse(m['retainedAfterRecovery'])
        no=event_recovery(r,{}, {'a':a},{'a':a},[],process_incident=True)
        self.assertIsNone(no['firstRecoveryDecision']);self.assertFalse(no['repairApplicable'])

    def test_pairing_gates_and_budget_failure(self):
        control=dict(terminalStatus='completed',success=True)
        event=dict(terminalStatus='completed',success=True,scheduledEvents=2,appliedEvents=2,effectiveIncidentVerified=True)
        self.assertTrue(pair_metrics(control,event,shared_prefix_verified=True)['conditionalRecoverySuccess'])
        for changed in [dict(appliedEvents=1),dict(terminalStatus='service_error'),dict(effectiveIncidentVerified=False)]:
            self.assertIsNone(pair_metrics(control,{**event,**changed},shared_prefix_verified=True)['conditionalRecoverySuccess'])
        self.assertIsNone(pair_metrics({**control,'success':False},event,shared_prefix_verified=True)['conditionalRecoverySuccess'])
        self.assertEqual(pair_metrics({**control,'success':False},event,shared_prefix_verified=True)['pairedCompletionDrop'],-1)
        self.assertIsNone(pair_metrics(control,event)['conditionalRecoverySuccess'])
        self.assertFalse(pair_metrics(control,{**event,'terminalStatus':'model_budget_exhausted'},shared_prefix_verified=True)['conditionalRecoverySuccess'])

    def test_format_schema_and_physics_are_separate(self):
        records=[dict(action={'type':'invalid'},feedback={'code':'INVALID_REQUEST'}),
          dict(action={'type':'attach'},feedback={'code':'INVALID_REQUEST'}),
          dict(action={'type':'attach'},feedback={'code':'PATH_BLOCKED'}),
          dict(action={'type':'detach'},feedback={'code':'OK'})]
        m=execution_metrics(records,initial_was_correct=True,reference_moves=2)
        self.assertEqual(m['formatErrorResponses'],1);self.assertEqual(m['schemaErrorResponses'],1)
        self.assertEqual(m['manipulationAttempts'],3);self.assertEqual(m['legalActionRate'],.5)
        self.assertTrue(m['falseRepair']);self.assertEqual(m['movesRelativeToWitness'],1.5)

    def test_aggregate_service_and_duplicate_weight(self):
        base=dict(model='test',inputVersion='v1',track='static',taskType='S1',objectId='house',sourceGroup='set:1',terminalStatus='completed')
        rows=[dict(base,conditionId='a',canonicalTaskId='one',success=True),dict(base,conditionId='b',canonicalTaskId='one',success=True),
              dict(base,conditionId='c',canonicalTaskId='two',success=False),dict(base,conditionId='d',canonicalTaskId='three',success=True,terminalStatus='service_error')]
        result=aggregate(rows)[0]
        self.assertEqual(result['validDistinctTasks'],2);self.assertEqual(result['distinctTaskSuccessRate'],.5)
        self.assertEqual(result['validRunCoverage'],.75)
        with self.assertRaises(ValueError):aggregate(rows+[rows[0]])
        with self.assertRaises(ValueError):aggregate([{**rows[0],'success':None}])
        separate=aggregate([rows[0],{**rows[2],'taskType':'S0'}])
        self.assertEqual(len(separate),2)

    def test_legacy_event_applied_alias_and_multiple_gate(self):
        score=dict(success=True,eventApplied=True,scheduledEvents=2,appliedEvents=2)
        self.assertIsNone(pair_assessment({'success':True},{**score,'appliedEvents':1},'complete','complete')['repairSuccess'])
        trace=dict(track='D',status='complete',sharedPrefixVerified=True,branches={
          'control':dict(status='complete',episode={'score':{'success':True}}),
          'intervention':dict(status='complete',episode={'score':score})})
        out=assess_run(trace);self.assertTrue(out['eventTriggered']);self.assertTrue(out['repairSuccess'])
        trace['branches']['intervention']['episode']['score']['appliedEvents']=1
        self.assertIsNone(assess_run(trace)['repairSuccess'])

    def test_recovered_service_error_is_still_counted_without_censoring(self):
        out=assess_run(dict(track='S',status='complete',caseId='static',replayScore={'success':True},
            errors=[dict(message='HTTP 429',recovered=True)]))
        self.assertTrue(out['success']);self.assertEqual(out['serviceErrorCount'],1)
        out=assess_run(dict(track='S',status='complete',replayScore={'success':True},errors=['HTTP 429']))
        self.assertIsNone(out['success'])

    def test_static_grade_uses_stage_not_future_build_size(self):
        stage=descriptors(32,2,0,0,'missing','static',5)
        self.assertEqual(stage['buildLength'],'B1');self.assertEqual(stage['planningLevel'],'G1')
        self.assertEqual(stage['activeParts'],32)
        self.assertEqual(descriptors(32,2,0,1,'missing')['planningLevel'],'G3')


if __name__=='__main__':unittest.main()
