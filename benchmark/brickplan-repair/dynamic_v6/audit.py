"""Independent full-bank geometry, visibility, baselines, leakage and split checks."""
from pathlib import Path
from collections import Counter,defaultdict
import argparse,hashlib,json,sys,time
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE.parent),str(HERE.parent/'eval')]
from dynamic_v6.episode import BANK,model_cert
from dynamic_v5.build import write
from dynamic_v6.build import sig
from dynamic_v5.vision import DynamicVisionRenderer
from baseplate import PlateAssembly
from static_v4.certify import digest

VIEWS=('isometric','top','rear')
def changed(a,b):return int(np.count_nonzero(np.max(np.abs(a.astype(np.int16)-b.astype(np.int16)),axis=2)>=24))
def apply(rt,state,actions):
    for a in actions:
        state,fb=rt.check(state,a['partId'],a['type'],candidate=a.get('candidate'))
        assert fb['code']=='OK',(a,fb)
    return state

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--resume',action='store_true');args=parser.parse_args()
    cases=json.loads((BANK/'cases.private.json').read_text())['cases'];groups=defaultdict(list)
    for c in cases:groups[c['modelId']].append(c)
    results=[];targets={};dupes=[]
    for mid,rows in sorted(groups.items()):
        started=time.time();cert=model_cert(mid);rt=PlateAssembly(cert);renderer=DynamicVisionRenderer(rt.cert,rt)
        evidence=json.loads((BANK/'models'/mid/'evidence.json').read_text());plan=evidence['buildWitness']
        zero={a:'' for a in rt.actors};states=[zero]
        for a in plan:states.append(apply(rt,states[-1], [a]))
        assert rt.complete(states[-1]);targetkey=sig(rt,rt.goal)
        if targetkey in targets:dupes.append([targets[targetkey],mid])
        targets[targetkey]=mid
        renderer.rgb(rt.goal,'isometric',size=(800,600),supersample=1)[0].save(BANK/'models'/mid/'target.png')
        cachefile=BANK/'models'/mid/'audit-v6.json';sourcehash=digest(dict(cert=cert,cases=rows))
        if args.resume and cachefile.exists():
            cached=json.loads(cachefile.read_text())
            if cached['sourceHash']==sourcehash:
                results+=cached['rows'];print(mid,'cached',len(cached['rows']),flush=True);continue
        images={};local=[]
        def rgb(s,v):
            key=(digest(s),v)
            if key not in images:images[key]=np.asarray(renderer.rgb(s,v,size=(800,600),supersample=1)[0])
            return images[key]
        seen={}
        for c in rows:
            at=c['trigger'];prefix=states[at];before=states[at-1];event=c.get('privateEvent')
            after=dict(prefix)
            if event:
                assert digest(prefix)==event['beforeSha256'],c['id']
                after=apply(rt,after,event['transaction']);assert digest(after)==event['afterSha256'],c['id']
                assert rt.signature(after)!=rt.signature(prefix),c['id']
                recovered=apply(rt,after,event['recoveryWitness']);assert rt.complete(recovered),c['id']
            else:assert rt.complete(apply(rt,after,plan[at:])),c['id']
            blind=dict(after);rejections=0
            for a in plan[at:]:
                blind,fb=rt.check(blind,a['partId'],a['type'],candidate=a.get('candidate'));rejections+=fb['code']!='OK'
            reset=dict(after);reset_moves=0
            while any(reset.values()):
                for actor,key in sorted(reset.items()):
                    if not key:continue
                    updated,fb=rt.check(reset,actor,'detach')
                    if fb['code']=='OK':reset=updated;reset_moves+=1;break
                else:raise AssertionError((c['id'],'privileged reset stuck'))
            reset=apply(rt,reset,plan);assert rt.complete(reset)
            delta={v:changed(rgb(prefix,v),rgb(after,v)) for v in VIEWS}
            temporal={v:changed(rgb(before,v),rgb(after,v)) for v in VIEWS}
            cancellation=bool(event and rt.signature(before)==rt.signature(after))
            tier=('control' if not event else 'action-cancellation' if cancellation else 'low-contrast' if max(delta.values())<2000 else 'machine-visible')
            token=(at,sig(rt,after));duplicate=seen.get(token)
            if event:seen.setdefault(token,c['id'])
            local.append(dict(caseId=c['id'],modelId=mid,kind=c['kind'],geometryPassed=True,
                              eventChangedPixels=delta,temporalChangedPixels=temporal,temporalClass=tier,
                              primaryMachineCandidate=tier=='machine-visible' and not duplicate,
                              identicalEventStateTo=duplicate,blindSuccess=rt.complete(blind),blindRejectedMoves=rejections,
                              privilegedResetSuccess=True,privilegedResetMoves=reset_moves+len(plan),
                              humanValidated=False))
        write(cachefile,dict(sourceHash=sourcehash,rows=local));results+=local
        print(mid,len(rows),dict(Counter(r['temporalClass'] for r in local)),'seconds',round(time.time()-started,1),flush=True)
    write(BANK/'audit.json',dict(schema='brickplan-dynamic-full-audit/6',total=len(results),geometryPassed=len(results),
        views=list(VIEWS),resolution=[800,600],pixelThreshold=24,primaryContrastPixels=2000,
        counts=dict(Counter(r['temporalClass'] for r in results)),duplicateTargetModels=dupes,
        duplicateEpisodeStates=sum(bool(r['identicalEventStateTo']) for r in results),rows=results))
    assert not dupes,'Distinct object IDs must not have identical target geometry'
    sets={k:[] for k in ('controls','primary-machine-candidates','action-cancellation','low-contrast','duplicate-event-state')}
    for r in results:
        key=('duplicate-event-state' if r['identicalEventStateTo'] else 'controls' if r['kind']=='none' else 'primary-machine-candidates' if r['primaryMachineCandidate'] else r['temporalClass'])
        sets[key].append(r['caseId'])
    write(BANK/'evaluation-sets.json',dict(schema='brickplan-dynamic-evaluation-sets/6',humanAdmission='pending independent per-case review; no formal detection claims yet',sets=sets))
    families=sorted({c['sourceFamily'] for c in cases},key=lambda f:hashlib.sha256(('brickplan-v6-split:'+f).encode()).hexdigest())
    dev=set(families[:max(1,round(len(families)*.3))]);splits={c['id']:('development' if c['sourceFamily'] in dev else 'evaluation') for c in cases}
    write(BANK/'splits.json',dict(schema='brickplan-source-splits/1',rule='SHA256 ordering of source family, first 30% development; never split variants of one family',sourceFamilies={f:('development' if f in dev else 'evaluation') for f in families},caseAssignments=splits,
                               crossStaticGeneralization='Not claimed: legacy source models also occur in the static bank.'))
    write(BANK/'release-check.json',dict(schema='brickplan-dynamic-release-check/6',cases=len(cases),structures=len(groups),sourceFamilies=len(families),
        completeObjectModels=sum(mid.startswith('obj-') for mid in groups),completeObjectCases=sum(c['track']=='complete-object' for c in cases),
        controls=sum(c['kind']=='none' for c in cases),interventions=sum(c['kind']!='none' for c in cases),interventionKinds=len({c['kind'] for c in cases})-1,
        geometryPassed=len(results),visualGroups={k:len(v) for k,v in sets.items()},
        blindControlSuccess=sum(r['blindSuccess'] for r in results if r['kind']=='none'),blindInterventionSuccess=sum(r['blindSuccess'] for r in results if r['kind']!='none'),privilegedResetSuccess=len(results),
        humanValidatedCases=0,paidModelRuns=0,
        bankSha256=hashlib.sha256((BANK/'cases.private.json').read_bytes()).hexdigest(),status='MACHINE_CHECKED_HUMAN_REVIEW_PENDING'))
    print(json.dumps(json.loads((BANK/'release-check.json').read_text()),ensure_ascii=False),flush=True)
if __name__=='__main__':main()
