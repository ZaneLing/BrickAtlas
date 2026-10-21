"""Reconcile API pilot traces with the settled experiment ledger."""
from collections import Counter
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
BANK=ROOT/'deliverables/brickplan-dynamic-v5'

def main():
    traces=[]
    for path in sorted((BANK/'pilot/runs').glob('*/trace.json')):
        run=json.loads(path.read_text());score=run.get('score',{})
        traces.append(dict(caseId=run['caseId'],track=run.get('track','visual'),seed=run.get('seed',41),status=run['status'],
                           calls=sum('response' in s for s in run['steps']),
                           attemptedCalls=len(run['steps']),costUSD=run['costUSD'],
                           eventTriggered=score.get('eventTriggered'),success=score.get('success'),
                           detectionAtEvent=run.get('detectionReport',{}).get('declaredAtEvent'),
                           preEventFalseAlarms=run.get('detectionReport',{}).get('preEventFalseAlarms'),
                           finalEquivalent=score.get('finalEquivalent'),
                           invalidMoves=score.get('invalidMoves'),finalResidual=score.get('finalResidual'),
                           traceFile=str(path.relative_to(BANK))))
    ledger=json.loads((ROOT/'benchmark/.runtime/dynamic-v5-ledger.json').read_text())
    charges=ledger['charges']
    if any(c['status']!='settled' for c in charges):raise RuntimeError('Unsettled API charge')
    trace_sum=sum(t['costUSD'] for t in traces)
    ledger_sum=sum(c['actual'] for c in charges)
    if abs(trace_sum-ledger_sum)>1e-7:raise AssertionError(('Trace/ledger costs differ',trace_sum,ledger_sum))
    def paired(track):
        selected=[t for t in traces if t['track']==track]
        by_kind={t['caseId'].rsplit('--',1)[-1]:t for t in selected}
        assert {'control','removed_piece','extra_layer'}<=by_kind.keys()
        runs=[json.loads((BANK/t['traceFile']).read_text()) for t in selected]
        prefixes=[[s['action'] for s in run['steps'][:3]] for run in runs]
        text_at_next=[run['steps'][3]['observation'] for run in runs]
        return dict(cases=3,sameFirstThreeActions=all(p==prefixes[0] for p in prefixes),
                    sameNextTextObservation=all(v==text_at_next[0] for v in text_at_next),
                    controlSuccess=by_kind['control']['success'],
                    eventsTriggered=sum(by_kind[k]['eventTriggered'] for k in ('removed_piece','extra_layer')),
                    eventSuccesses=sum(by_kind[k]['success'] for k in ('removed_piece','extra_layer')))
    source_names=('control','removed_piece','wrong_color')
    source_runs=[json.loads((BANK/'pilot/runs'/f'v23-30023--t3--{kind}--manual-v5'/'trace.json').read_text())
                 for kind in source_names]
    source_pair=dict(cases=3,modelId='v23-30023',
                     sameFirstThreeActions=all([s['action'] for s in run['steps'][:3]]==
                                               [s['action'] for s in source_runs[0]['steps'][:3]] for run in source_runs),
                     sameNextTextObservation=all(run['steps'][3]['observation']==
                                                 source_runs[0]['steps'][3]['observation'] for run in source_runs),
                     sameFullActionSequence=all([s['action'] for s in run['steps']]==
                                                [s['action'] for s in source_runs[0]['steps']] for run in source_runs),
                     controlSuccess=source_runs[0]['score']['success'],
                     eventsTriggered=sum(run['score']['eventTriggered'] for run in source_runs[1:]),
                     eventSuccesses=sum(run['score']['success'] for run in source_runs[1:]))
    track_summary={}
    for track in sorted({t['track'] for t in traces}):
        group=[t for t in traces if t['track']==track]
        track_summary[track]=dict(traces=len(group),paidCalls=sum(t['calls'] for t in group),
            controls=sum(t['caseId'].endswith('--control') for t in group),
            controlSuccesses=sum(t['success'] is True for t in group if t['caseId'].endswith('--control')),
            interventionsTriggered=sum(t['eventTriggered'] is True for t in group if not t['caseId'].endswith('--control')),
            interventionSuccesses=sum(t['success'] is True for t in group if not t['caseId'].endswith('--control')),
            eventDetectionTrue=sum(t['detectionAtEvent'] is True for t in group),
            eventDetectionFalse=sum(t['detectionAtEvent'] is False for t in group),
            preEventFalseAlarms=sum(t['preEventFalseAlarms'] or 0 for t in group))
    summary=dict(schema='brickplan-dynamic-pilot-summary/1',model='google/gemini-2.5-flash',
                 exploratory=True,promptVersions=sorted(set(t['track'] for t in traces)),
                 requests=len(charges),settledCostUSD=ledger_sum,traceCostUSD=trace_sum,
                 registeredCapUSD=ledger['cap'],traces=traces,trackSummary=track_summary,
                 pairedManualV3=paired('manual-v3'),pairedContinuousManualV4=paired('manual-v4'),
                 pairedSourceManualV5=source_pair,
                 note='Prompt revised after seeing pilot failures; these runs are interface/behavior diagnostics, not a held-out model estimate.')
    path=BANK/'pilot/summary.json';path.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:summary[k] for k in ('requests','settledCostUSD','pairedContinuousManualV4')},ensure_ascii=False))

if __name__=='__main__':main()
