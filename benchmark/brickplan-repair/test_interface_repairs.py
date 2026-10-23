"""Offline regression for target ambiguity, matched canvases, manuals and attribution."""
from pathlib import Path
from copy import deepcopy
import importlib.util
import json
import sys
import tempfile
import subprocess
import numpy as np
from PIL import Image

HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE/'community_modules'),str(HERE),str(HERE/'eval')]
from community_modules.core import Episode, OUT as MODULES, ROOT, dump
from community_modules.run_episode import ModulePacket
from dynamic_v6.episode import DynamicEpisode, load_case
from dynamic_v6.interface import packet, renderer_for
from evaluation_outcomes import assess_run, pair_assessment, service_error

OUT=ROOT/'deliverables/brickplan-interface-repair-2026-10-23'


def same_scene_panels(record):
    with Image.open(record['file']) as im:
        assert im.size==(1600,636)
        a,b=record['panels']
        left=np.asarray(im.crop(a['rectanglePixels']))
        right=np.asarray(im.crop(b['rectanglePixels']))
        assert left.shape==right.shape==(600,800,3)
        assert np.array_equal(left,right)
        # Identical rectangles stay identical under the same resize operation.
        for size in ((400,300),(200,150)):
            x=im.crop(a['rectanglePixels']).resize(size,Image.Resampling.LANCZOS)
            y=im.crop(b['rectanglePixels']).resize(size,Image.Resampling.LANCZOS)
            assert np.array_equal(np.asarray(x),np.asarray(y))


def accounting():
    for error,expected in [({'httpStatus':403},'request_rejected'),({'httpStatus':429},'rate_limited'),
            ({'message':'The operation was aborted due to timeout'},'timeout'),
            ('HTTP Error 503: unavailable','provider_unavailable'),
            ({'httpStatus':200,'errorCode':429},'rate_limited')]:
        assert service_error(error)['category']==expected
        r=assess_run(dict(track='D',status='api_error',errors=[error],episode={'score':{'success':False}}))
        assert r['success'] is None and r['repairSuccess'] is None and r['detectionMiss'] is None
        assert r['serviceErrors']=={expected:1}
    t=dict(track='D',status='untriggered',episode={'score':{'success':False,'eventTriggered':False}})
    r=assess_run(t);assert r['outcome']=='untriggered' and r['repairSuccess'] is None and r['success'] is None
    t=dict(track='D',caseId='example--control',status='complete',eventScheduled=False,episode={'score':{'success':True,'eventTriggered':False}})
    r=assess_run(t);assert r['outcome']=='completed' and r['success'] is True and r['repairSuccess'] is None
    t=dict(track='M-D',status='complete',moduleScore=dict(success=False,eventApplied=False))
    r=assess_run(t);assert r['outcome']=='untriggered' and r['completionSuccess'] is False and r['repairSuccess'] is None
    t['moduleScore'].update(success=True,eventApplied=True)
    r=assess_run(t);assert r['outcome']=='unpaired_observation' and r['observedCompletionAfterEvent'] is True and r['repairSuccess'] is None
    control=dict(success=True,preEventFalseAlarms=0);event=dict(success=False,eventTriggered=True,reportedAtEvent=False)
    a=pair_assessment(control,event,'complete','complete',visibility_gate=True)
    assert a['recoveryPairEligible'] and a['repairSuccess'] is False and a['detectionMiss'] is True
    for c,e,cs,es,reason in [(dict(success=False),event,'complete','complete','control_failed'),
            (control,event,'complete','api_error','run_interrupted'),
            (control,dict(eventTriggered=False),'complete','complete','untriggered')]:
        a=pair_assessment(c,e,cs,es,visibility_gate=True)
        assert not a['recoveryPairEligible'] and a['repairSuccess'] is None and a['detectionMiss'] is None and a['repairEligibilityReason']==reason
    t=dict(track='S',status='decision_cap',replayScore={'success':False},steps=[dict(action={'type':'invalid'},feedback={'code':'INVALID_ACTION'})])
    r=assess_run(t)
    assert r['formatErrorResponses']==1 and r['visualFailure'] is None and r['placementFailure'] is None
    print('PASS error categories, untriggered, control gate, unpaired M and format separation',flush=True)


def main():
    OUT.mkdir(parents=True,exist_ok=True);accounting()
    modules=json.loads((MODULES/'gallery-data.js.json').read_text());rows=[];pixel_checks=0
    for m in modules:
        base=MODULES/m['id'];cert=json.loads((base/'certificate.private.json').read_text())
        cases=json.loads((base/'cases.private.json').read_text())
        with tempfile.TemporaryDirectory() as temp:
            control=next(c for c in cases if c['mode']=='static' and c['family']=='control')
            ep=Episode(cert,control,41);builder=ModulePacket(ep,m,temp);first=builder.observation()
            assert first['manual']['defaultImages']==0
            assert not any(x['role'] in ('target','full-completion-reference','acceptance-target','instruction-reference','future-instruction-reference','scene-overview-final') for x in first['images'])
            assert len([x for x in first['images'] if x['role']=='current-target'])==3
            assert len([x for x in first['images'] if x['role']=='inventory'])==(len(ep.actors)+11)//12
            for x in first['images']:
                if x['role']=='current-target':same_scene_panels(x);pixel_checks+=1
            # Recheck fault visibility at the new default panel resolution.
            visibility={}
            goals={v:np.asarray(builder.render(control['goal'],v,size=(800,600))).astype(np.int16) for v in ('isometric','rear','top')}
            for faulty in (c for c in cases if c['mode']=='static' and c['family']!='control'):
                changed={}
                for v,g in goals.items():
                    actual=np.asarray(builder.render(faulty['initial'],v,size=(800,600))).astype(np.int16)
                    changed[v]=int(np.count_nonzero(np.max(np.abs(actual-g),axis=2)>=24))
                assert max(changed.values())>=128,(m['id'],faulty['family'],changed)
                visibility[faulty['family']]=changed
            # An instruction is one contact sheet, not a new task target.
            ep.step(dict(type='inspect',manualStep=control['completedInstructionStep']))
            shown=builder.observation()
            refs=[x for x in shown['images'] if x['role']=='instruction-reference']
            assert len(refs)==1 and refs[0]['isTarget'] is False
            assert ep.previous==ep.state
            stage=first['manual']['targetStage'];total=first['manual']['totalSteps']
            if stage<total:
                try:ep.step(dict(type='inspect',manualStep=stage+1))
                except ValueError:pass
                else:raise AssertionError('Future instruction shown without explicit request')
                ep.step(dict(type='inspect',manualStep=stage+1,futureReference=True))
                future=builder.observation()
                assert len([x for x in future['images'] if x['role']=='future-instruction-reference'])==1
                assert [x['sha256'] for x in first['images'] if x['role']=='current-target']==[x['sha256'] for x in future['images'] if x['role']=='current-target']
            dyn=next(c for c in cases if c['mode']=='dynamic' and c['family']=='control')
            de=Episode(cert,dyn,41);db=ModulePacket(de,m,temp);di=db.observation()
            de.step(dict(type='inspect',view='isometric'));later=db.observation()
            assert de.previous==de.state and len(later['images'])==len(di['images'])+4  # 3 temporal + requested inspection
            for x in later['images']:
                if x['role']=='temporal-pair':same_scene_panels(x);pixel_checks+=1
            rows.append(dict(module=m['id'],steps=total,targetStage=stage,
                oldFirstImages=6*total+15,oldLaterImages=6*total+18,
                newFirstImages=len(di['images']),newLaterImages=len(later['images'])-1,
                requestedManualAdds=1,soleTarget=True,futureStepsExplicitOnly=True,defaultResolutionFaultVisibility=visibility))
            if m['id']=='repair-truck-cab':
                example=OUT/'example';example.mkdir(exist_ok=True)
                # Copy exactly the public default packet, then one separately requested manual page.
                exported=deepcopy(first)
                for im in exported['images']:
                    p=Path(im['file']);(example/p.name).write_bytes(p.read_bytes());im['file']='example/'+p.name
                ref=refs[0];p=Path(ref['file']);(example/p.name).write_bytes(p.read_bytes())
                dump(OUT/'example-input.json',exported)
                dump(OUT/'requested-manual.json',{**ref,'file':'example/'+p.name})
                fault=next(c for c in cases if c['mode']=='static' and c['family']=='wrong-color')
                faulty=ModulePacket(Episode(cert,fault,41),m,temp).observation()
                for im in faulty['images']:
                    p=Path(im['file']);(example/p.name).write_bytes(p.read_bytes());im['file']='example/'+p.name
                dump(OUT/'example-fault-input.json',faulty)
        print('PASS module',m['id'],rows[-1]['newFirstImages'],rows[-1]['newLaterImages'],flush=True)
    cert,case=load_case('obj-city-car--t3--control')
    ep=DynamicEpisode(cert,case);ep.state=dict(ep.runtime.goal);ep.previous_state=dict(ep.state)
    with tempfile.TemporaryDirectory() as temp:
        obs,ims=packet(ep,renderer_for(ep),temp)
        for im in ims:
            if im['role'] in ('current-target','temporal-pair'):
                same_scene_panels({**im,'file':str(Path(temp)/im['file'])});pixel_checks+=1
        assert obs['inspectionCoordinates']['sceneRectangleInCurrentTargetPixels']==[0,36,800,636]
    # Invalid JSON must return fresh, complete input, not an error-only object.
    proc=subprocess.run([sys.executable,str(HERE/'community_modules/run_episode.py'),
        '--module','repair-truck-cab','--condition','static-control'],
        input='not-json\n'+json.dumps(dict(type='inspect',manualStep=1))+'\n'+json.dumps(dict(type='finish'))+'\n',
        capture_output=True,text=True,timeout=90)
    assert proc.returncode==0,proc.stderr
    obs=[json.loads(x) for x in proc.stdout.splitlines()]
    assert len(obs)==4 and obs[1]['feedback']['code']=='INVALID_REQUEST' and obs[1]['images']
    assert len([x for x in obs[2]['images'] if x['role']=='instruction-reference'])==1
    assert obs[-1]['done']
    dump(OUT/'module-image-counts.json',rows)
    report=dict(status='PASS',realPaidRequests=0,modules=len(rows),equalScenePixelChecks=pixel_checks,
        manualOnDemand=True,soleTarget=True,futureInstructionsExplicitOnly=True,
        providerErrorsSeparate=True,formatErrorsSeparate=True,untriggeredScoresNull=True,
        successfulControlRequired=True,unpairedModuleExcluded=True,
        invalidRequestReturnsFreshImages=True,
        visibleStaticFaults=3*len(rows),minimumChangedPixels=128,rgbDifferenceThreshold=24,
        providerPreprocessingVerified=False,
        limitation='Offline exact-pixel and same-resize regression only; no live provider A/B or model rerun.')
    dump(OUT/'checks.json',report);print(json.dumps(report,indent=2))


if __name__=='__main__':main()
