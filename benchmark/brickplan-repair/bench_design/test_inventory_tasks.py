"""Behavior checks: genuine alternative builds, finite inventory and replanning."""
from pathlib import Path
from copy import deepcopy
import hashlib
import numpy as np
from PIL import Image
from bench_design.inventory_tasks import OUT,index,placement,InventoryEpisode,InventoryPacket,EquivalentAssembly
from bench_design.session import Session,internal_action,assess_pair
from bench_design.independent_geometry import check
from bench_design.selection import retired
from expansion_v7.build import read,write

TMP=Path('/tmp/brick-inventory-validation')


def opened(cid,name='reference',control=False):
    s=Session.open(cid,TMP/name/cid.replace(':','-'),actor='scripted:inventory-validation',control=control);s.autosave=False
    return s


def perform(s,actions,observe=False):
    for a in actions:
        if observe:s.observe()
        feedback=s.submit(internal_action(s.ep,a))
        assert feedback['code']=='OK',(s.row['key'],a,feedback)


def finish(s):
    s.submit(dict(type='finish'));return s.result()


def main():
    results=[];geometry=[];behaviors=[]
    for r in index()['cases']:
        s=opened(r['id']);before=dict(s.ep.state)
        if r['variant']=='repair':
            big=s.row['case']['referenceActions'][-1]
            _,blocked=s.ep.runtime.check(s.ep.state,big['actor'],'attach',candidate=big['candidate'])
            assert blocked['code']=='ENDPOINT_COLLISION'
        for a in s.row['case']['referenceActions']:
            if r['variant'] in ('repair','small-required'):
                rt=s.ep.runtime;_,v=rt.check(s.ep.state,a['actor'],a['type'],candidate=a.get('candidate'))
                g=check(rt,s.ep.state,a,v);assert g['status']=='agrees-on-accepted-geometry',(r['id'],g)
                geometry.append(dict(caseId=r['id'],action=a,evidence=g))
            perform(s,[a])
        out=finish(s);assert out['success'] and len(s.events)==len(s.row['case']['events'])
        assert all(e['effectiveIncidentVerified'] for e in s.events)
        results.append(dict(caseId=r['id'],moves=out['executionMetrics']['acceptedMoves'],success=True,
            eventCount=len(s.events),targetContract=out['targetContract']))
        print('PASS',r['id'],flush=True)
        # Every initially installed small brick in the repair must be removed.
        if r['variant']=='repair':
            for keep in [a for a,k in before.items() if k]:
                trial=opened(r['id'],'keep-'+keep)
                for a in trial.row['case']['referenceActions']:
                    if a['type']=='detach' and a['actor']==keep:continue
                    fb=trial.submit(internal_action(trial.ep,a))
                assert not finish(trial)['success']
            behaviors.append(dict(axis=r['axis'],check='each-initial-small-brick-requires-removal',passed=True))
    for axis in ('horizontal','vertical'):
        # Same fixed target illustration accepts a genuinely different part set.
        s=opened(f'QI:{axis}::either','alternative')
        small=opened(f'QI:{axis}::small-required').row['case']['referenceActions']
        perform(s,small);assert finish(s)['success']
        assert sum(bool(k) for k in s.ep.state.values())>sum(bool(k) for k in s.goal.values())
        # A different legal order also succeeds (vertical requires bottom-up).
        if axis=='horizontal':
            s=opened('QI:horizontal::small-required','reverse');perform(s,list(reversed(small)));assert finish(s)['success']
        # Insufficient stock is never replenished, and one handle is never reusable.
        s=opened(f'QI:{axis}::large-required','stock');cert=s.ep.cert
        first=small[0];perform(s,[first]);original=dict(s.ep.state)
        assert s.submit(internal_action(s.ep,first))['code']=='ALREADY_INSTALLED'
        assert s.ep.state==original
        remaining=[a for a in small[1:] if a['actor'] in s.ep.actor_alias]
        perform(s,remaining);assert not finish(s)['success']
        # A legal overhanging large brick still fails the exact target volume.
        s=opened(f'QI:{axis}::large-required','overhang')
        k=next(k for k,v in s.ep.cert['candidates'].items() if v['actor']=='large1' and np.asarray(v['part']['rawMatrix'])[0,3]==20)
        perform(s,[dict(type='attach',actor='large1',candidate=k)]);assert not finish(s)['success']
        # The changed inventory, not an unchanged image, establishes exposure.
        cid=f'QI:{axis}::dynamic-shortage';left=opened(cid,'paired-control',True);right=opened(cid,'paired-incident')
        normal=left.row['case']['normalReferenceActions'];prefix=normal[:-2]
        for a in prefix:
            for session in (left,right):perform(session,[a],True)
        for session in (left,right):perform(session,[normal[-2]],True)
        assert len(right.events)==1 and not left.events
        event=right.events[0];assert event['before']==event['after'] and event['resourceChangeVerified']
        removed=event['native']['withdrawnActors'][0];key=next(k for k,v in right.ep.cert['candidates'].items() if v['actor']==removed)
        original=dict(right.ep.state)
        assert right.submit(internal_action(right.ep,dict(type='attach',actor=removed,candidate=key)))['code']=='OUT_OF_STOCK'
        assert right.ep.state==original
        observation=right.observe()
        assert next(v for v in observation['inventoryAvailability'] if v['partId']==right.ep.actor_alias[removed])['status']=='unavailable'
        perform(left,[normal[-1]]);finish(left)
        recovery=right.row['case']['referenceActions'][len(normal)-1:]
        perform(right,recovery);finish(right)
        paired=assess_pair(left,right,len(prefix));assert paired['metrics']['conditionalRecoverySuccess'] is True,paired
        write(OUT/f'{axis}-paired-check.json',paired)
        # Using the large brick first avoids the accident. It is untriggered,
        # and must not be reported as a failed repair.
        s=opened(cid,'avoided');perform(s,[s.row['case']['referenceActions'][-1]]);out=finish(s)
        assert out['success'] and out['incidentExposure']=='untriggered' and not s.events
        if axis=='horizontal':
            s=opened(cid,'different-dynamic-order');prefix=list(reversed(s.row['case']['normalReferenceActions']))[:-1]
            perform(s,prefix);assert len(s.events)==1
            assert s.events[0]['native']['withdrawnActors']==['small1']
            perform(s,[dict(type='detach',actor=a['actor']) for a in reversed(prefix)]+[s.row['case']['referenceActions'][-1]])
            assert finish(s)['success']
        behaviors.append(dict(axis=axis,check='alternative-build-stock-shortage-matched-pair-and-untriggered',passed=True))
    # Seam evidence uses only actual visible actor boundaries; never all mesh
    # triangles and never a target-derived error annotation.
    for axis in ('horizontal','vertical'):
        s=opened(f'QI:{axis}::small-required','seams');perform(s,s.row['case']['referenceActions'])
        renderer=s.packet.renderer;view='top' if axis=='horizontal' else 'front'
        image,mask=renderer.rgb(s.ep.state,view,frame_keys=['_module_frame'],size=(1200,900),supersample=1)
        ids={renderer.ids[a] for a,k in s.ep.state.items() if k}
        edge=(mask[:,1:]!=mask[:,:-1])&np.isin(mask[:,1:],list(ids))&np.isin(mask[:,:-1],list(ids))
        edge2=(mask[1:]!=mask[:-1])&np.isin(mask[1:],list(ids))&np.isin(mask[:-1],list(ids))
        assert int(edge.sum()+edge2.sum())>50
        seam=np.zeros(mask.shape,bool);seam[:,1:]|=edge;seam[1:]|=edge2
        assert np.all(np.asarray(image)[seam]==[45,48,51])
        folder=OUT/'examples';folder.mkdir(exist_ok=True);image.save(folder/(axis+'-seams.png'))
        # Same apparent volume built as a SINGLE brick has no small-small seams.
        one=opened(f'QI:{axis}::either','single-seam');perform(one,one.row['case']['referenceActions'])
        onepacket=one.observe();assert len([i for i in onepacket['images'] if i['role']=='current-target'])==3
        image,_=one.packet.renderer.rgb(one.ep.state,view,frame_keys=['_module_frame'],size=(1200,900),supersample=1)
        image.save(folder/(axis+'-single.png'))
        # Real provider payload construction, without sending any request.
        from dynamic_v5.run_api import request
        payload=request('dry-run-only',observation,observation['images'],TMP,'Follow targetContract.',[])
        blocks=[c for m in payload['messages'] if isinstance(m.get('content'),list) for c in m['content'] if c.get('type')=='image_url']
        assert len(blocks)==len(observation['images']) and all(b['image_url']['url'].startswith('data:image/png;base64,') for b in blocks)
        behaviors.append(dict(axis=axis,check='visible-seams-and-multimodal-image-payload',passed=True,imagesSent=len(blocks),apiCalls=0))
    for cid in ['E7:v7::rockefeller-crown::static::missing::t3','QX:quality::museum-roof-long::buried-overlap']:
        assert retired(cid)
        try:opened(cid,'retired');raise AssertionError('Withdrawn task was accepted')
        except ValueError as e:assert 'withdrawn' in str(e)
    write(OUT/'validation.json',dict(status='PASS',runs=results,behaviorChecks=behaviors,independentGeometry=geometry,
        allReferencesPassed=True,realHumanVotesWritten=0,apiCalls=0,paidUSD=0,
        scope='Finite rectangular brick/plate equivalence; no force, stiffness, load-bearing or arbitrary-part equivalence claim.'))


if __name__=='__main__':main()
