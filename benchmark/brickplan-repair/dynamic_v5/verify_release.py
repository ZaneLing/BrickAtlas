"""Cross-check the generated bank and its independent audit artifacts."""
from collections import Counter
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from dynamic_v5.episode import BANK


def read(name):
    return json.loads((BANK/name).read_text())


def main():
    index, private = read('index.json'), read('cases.private.json')
    public_cases, private_cases = index['cases'], private['cases']
    ids = [c['id'] for c in public_cases]
    assert len(ids) == len(set(ids)) == len(private_cases)
    assert [c['id'] for c in private_cases] == ids
    assert all({k:v for k,v in c.items() if k != 'privateEvent'} == p
               for p,c in zip(public_cases, private_cases))
    assert dict(Counter(c['kind'] for c in public_cases)) == index['counts']
    models = {c['modelId'] for c in public_cases}
    families = {c['sourceFamily'] for c in public_cases}
    assert len(models) == len(index['modelAudits'])
    assert {a['modelId'] for a in index['modelAudits']} == models
    assert all((BANK/'models'/m/'qualification.json').exists() and
               (BANK/'models'/m/'evidence.json').exists() for m in models)
    geometry, visual, baseline = read('audit.json'), read('visual-audit.json'), read('baselines.json')
    assert geometry['total'] == geometry['passed'] == len(ids)
    assert visual['total'] == visual['passed'] == len(ids)
    assert {r['caseId'] for r in geometry['results']} == set(ids)
    assert {r['caseId'] for r in visual['rows']} == set(ids)
    assert all(r['passesPixelGate'] for r in visual['rows'])
    temporal = read('temporal-interface-audit.json')
    assert temporal['total'] == len(ids)
    assert {r['caseId'] for r in temporal['rows']} == set(ids)
    assert sum(temporal['counts'].values()) == len(ids)
    assert all(r['eventChangedPixels'] == next(v['changedPixels']['isometric'] for v in visual['rows']
               if v['caseId'] == r['caseId']) for r in temporal['rows'])
    assert all(r['primaryCandidate'] == (r['category'] == 'candidate-for-human-validation')
               for r in temporal['rows'])
    for policy in ('blind-manual','privileged-reset'):
        rows = [r for r in baseline['rows'] if r['policy'] == policy]
        assert len(rows) == len(ids)
        assert {r['caseId'] for r in rows} == set(ids)
        assert baseline['summary'][policy]['total'] == len(ids)
    source = read('source-extension.json')
    assert source['admittedModels'] == sum(bool(d['admittedCases']) for d in source['decisions'])
    assert source['admittedCases'] == sum(d['admittedCases'] for d in source['decisions'])
    objects, object_track = read('object-extension.json'), read('object-track.json')
    object_cases = [c for c in public_cases if c['modelId'].startswith('obj-')]
    assert objects['models'] == len(object_track['modelIds']) == 4
    assert objects['cases'] == len(object_cases) == len(object_track['cases'])
    assert object_cases == object_track['cases']
    assert dict(Counter(c['kind'] for c in object_cases)) == objects['kinds'] == object_track['counts']
    assert all(c.get('objectCategory') in ('furniture','vehicle','machine') and c.get('objectNameZh')
               for c in object_cases)
    assert all(c['sourceFamily'] in {'complete-chair','complete-table','complete-city-car','complete-crane'}
               for c in object_cases)
    review = read('human-review-answer-key.private.json')
    assert review['cases'] == len(review['rows'])
    assert set(object_track['modelIds']) <= {r['modelId'] for r in review['rows']}
    for reviewer in ('reviewer-A','reviewer-B','reviewer-C'):
        html = (BANK/'human-review'/f'{reviewer}.html').read_text()
        assert 'object_guess' in html and 'privateEvent' not in html and 'caseId' not in html
    temporal_review = read('human-temporal-answer-key.private.json')
    assert temporal_review['cases'] == len(temporal_review['rows']) == 12
    for reviewer in ('reviewer-A','reviewer-B','reviewer-C'):
        html = (BANK/'human-temporal-review'/f'{reviewer}.html').read_text()
        assert 'privateEvent' not in html and 'caseId' not in html
        assert all(r['code'] in html for r in temporal_review['rows'])
    pilot, pilot_replay = read('pilot/summary.json'), read('pilot/replay-audit.json')
    attribution = read('pilot/attribution-audit.json')
    assert len(pilot['traces']) == pilot_replay['total'] == pilot_replay['passed']
    assert sum(t['calls'] for t in pilot['traces']) == pilot['requests']
    assert abs(sum(t['costUSD'] for t in pilot['traces'])-pilot['settledCostUSD']) < 1e-7
    assert all(r['caseId'] in ids and r['controlId'] in ids and not r['humanUsabilityValidated']
               for r in attribution['rows'])
    assert all(not r['provisionalDetectionMiss'] or
               (r['technicalAttributionEligible'] and r['detectionAtEvent'] is False)
               for r in attribution['rows'])
    report = dict(schema='brickplan-dynamic-release-check/1', cases=len(ids),
                  structures=len(models), sourceFamilies=len(families),
                  controls=index['counts']['none'], interventions=len(ids)-index['counts']['none'],
                  interventionKinds=len(index['counts'])-1,
                  geometryPassed=geometry['passed'], visualPassed=visual['passed'],
                  temporalCandidateCases=temporal['counts']['candidate-for-human-validation'],
                  lastActionCancelledCases=temporal['counts']['last-action-cancelled'],
                  lowContrastCases=temporal['counts']['low-event-contrast'],
                  temporalHumanReviewCases=temporal_review['cases'],
                  minimumEventChangedPixels=min(r['maxChangedPixels'] for r in visual['rows'] if r['kind']!='none'),
                  sourceModelsAdmitted=source['admittedModels'],
                  completeObjectModels=objects['models'],completeObjectCases=objects['cases'],
                  blindedReviewCases=review['cases'],
                  baselineBlindSuccess=baseline['summary']['blind-manual']['success'],
                  baselinePrivilegedResetSuccess=baseline['summary']['privileged-reset']['success'],
                  pilotTracesReplayed=pilot_replay['passed'],pilotPaidRequests=pilot['requests'],
                  pilotCostUSD=pilot['settledCostUSD'],
                  attributionPairs=len(attribution['rows']),
                  technicallyEligibleAttributionPairs=sum(r['technicalAttributionEligible'] for r in attribution['rows']),
                  humanValidatedAttributionPairs=0)
    (BANK/'release-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False))


if __name__ == '__main__':
    main()
