"""Re-execute every paid trace against the current geometry engine."""
from pathlib import Path
import hashlib
import io
import json
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from dynamic_v5.episode import BANK, DynamicEpisode, load_case
from dynamic_v5.vision import DynamicVisionRenderer
from vision import temporal_pair, temporal_target

def image_hash(image):
    stream=io.BytesIO();image.save(stream,format='PNG')
    return hashlib.sha256(stream.getvalue()).hexdigest()

def main():
    rows=[]
    for path in sorted((BANK/'pilot/runs').glob('*/trace.json')):
        run=json.loads(path.read_text())
        cert,case=load_case(run['caseId']);ep=DynamicEpisode(cert,case,seed=run.get('seed',41))
        executed=[step for step in run['steps'] if step.get('status')=='executed']
        temporal=run.get('track') in ('visual-v8','monitor-v1','monitor-v2','visual-v9','visual-v10','monitor-v3','monitor-v4','monitor-v5')
        paired=run.get('track') in ('visual-v9','visual-v10','monitor-v3','monitor-v4','monitor-v5')
        renderer=DynamicVisionRenderer(ep.cert,ep.runtime) if temporal else None
        previous_state=None
        for step in executed:
            if temporal:
                assert 'privateEvent' not in json.dumps(step['observation']),path
                assert step['observation']['visualTiming']['pairAvailable']==(previous_state is not None)
                for view in ('isometric','top'):
                    if paired:
                        image_rows=[r for r in step['images'] if r.get('view')==view and r['role'] in
                              ('temporal-pair','target')]
                        assert [r['role'] for r in image_rows]==['temporal-pair','target'],(path,step['index'],view)
                        comparison=ep.expected_after_last_action if run.get('track')=='monitor-v5' else previous_state
                        expected=[('temporal-pair',temporal_pair(renderer,comparison,ep.assignments(),view,
                                  left_label='EXPECTED AFTER YOUR ACTION' if comparison is not None and run.get('track')=='monitor-v5' else None)),
                                  ('target',temporal_target(renderer,ep.runtime.goal,view))]
                    else:
                        image_rows=[r for r in step['images'] if r.get('view')==view and r['role'] in
                              ('before-last-action','current','target')]
                        assert [r['role'] for r in image_rows]==(
                            ['before-last-action','current','target'] if previous_state is not None else
                            ['current','target']),(path,step['index'],view)
                        states=[('current',ep.assignments()),('target',ep.runtime.goal)]
                        if previous_state is not None:states.insert(0,('before-last-action',previous_state))
                        expected=[(role,renderer.rgb(state,view)[0]) for role,state in states]
                    for role,image in expected:
                        row=next(r for r in image_rows if r['role']==role)
                        assert row['sha256']==image_hash(image),(path,step['index'],role,view)
                assert not any(r['role']=='target-inspection' for r in step['images']),path
            previous_state=ep.assignments() if temporal else None
            feedback=ep.step(step['action'])
            assert feedback==step['feedback'],(path,step['index'],feedback,step['feedback'])
        score=ep.score()
        for field in ('success','finalEquivalent','eventTriggered','legalMoves','invalidMoves','finalResidual'):
            assert score[field]==run['score'][field],(path,field,score[field],run['score'][field])
        recorded=run.get('episode',{}).get('event')
        assert bool(recorded)==bool(ep.event)
        if recorded:assert (recorded['kind'],recorded['afterSha256'])==(ep.event['kind'],ep.event['afterSha256'])
        rows.append(dict(trace=str(path.relative_to(BANK)),caseId=run['caseId'],steps=len(executed),
                         status=run['status'],paidCalls=sum('response' in s for s in run['steps']),
                         eventTriggered=bool(ep.event),success=score['success'],chainSha256=ep.chain))
    report=dict(schema='brickplan-dynamic-pilot-replay/1',total=len(rows),passed=len(rows),rows=rows)
    (BANK/'pilot/replay-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(total=len(rows),passed=len(rows))))

if __name__=='__main__':main()
