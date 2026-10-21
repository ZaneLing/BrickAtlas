"""Export reproducible, response-free states from two archived v5 model traces.

Raw API messages are local provenance only; no new API requests are made.
Every archived state hash and feedback code is checked before export.
"""
from pathlib import Path
import hashlib,json,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'benchmark/brickplan-repair/community_modules'))
import core
from dynamic_v5.episode import DynamicEpisode,load_case
from static_v4.certify import digest

def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,indent=2)+'\n')

def snapshot(ep,index,action,code):
 actual,target=ep.runtime.signature(ep.state),ep.runtime.signature(ep.runtime.goal)
 return dict(index=index,action=action,state=dict(ep.state),feedback=code,stateSha256=digest(ep.state),
             outOfGoalPieces=sum((actual-target).values()),missingTargetPieces=sum((target-actual).values()),
             terminalCorrect=ep.runtime.complete(ep.state),eventOccurred=bool(ep.records[-1]['eventOccurred']))

base=ROOT/'deliverables/brickplan-dynamic-v5/pilot/latest-runs/google--gemini-4-argon'
traces=[];certificate=None;fault_case=None
for condition in ['extra_layer','control']:
 path=base/f'obj-city-car--t3--{condition}--visual-v9/trace.json';raw=read(path)
 cert,case=load_case(raw['caseId']);ep=DynamicEpisode(cert,case,seed=raw['seed'])
 assert cert['contentSha256']==raw['episode']['sourceCertificateSha256']
 if condition=='extra_layer':certificate=cert;fault_case=case
 frames=[]
 for step,record in zip(raw['steps'],raw['episode']['records']):
  code=ep.step(step['action'])['code'];observed=ep.records[-1]
  assert observed['beforeSha256']==record['beforeSha256']
  assert observed['afterSha256']==record['afterSha256']
  assert code==record['feedback']['code']
  frames.append(snapshot(ep,step['index'],ep.internal_action(step['action']),code))
 assert len(frames)==len(raw['steps'])==len(raw['episode']['records']) and ep.success==raw['score']['success']
 traces.append(dict(condition=condition,model=raw['model'],seed=raw['seed'],imageInterface=raw['imageInterface'],
                    source=str(path.relative_to(ROOT)),sourceSha256=sha(path),sourceCertificateSha256=cert['contentSha256'],
                    frames=frames,success=ep.success,decisions=len(frames),legalMoves=raw['score']['legalMoves'],
                    selectedIndices=[1,3,5,6,8,10,12,13] if condition=='extra_layer' else [2,4,7,8,10,12,14,17]))
# One reference completion; it is not the uniquely required target trajectory.
evpath=ROOT/'deliverables/brickplan-dynamic-v5/models/obj-city-car/evidence.json';reference=read(evpath)['buildWitness'];ep=DynamicEpisode(certificate,fault_case,seed=41);gt=[]
def apply(a):
 public={'type':a['type']}
 if 'partId' in a:public['partId']=ep.alias[a['partId']]
 if 'candidate' in a:public['candidate']=ep.pose(a['candidate'])
 code=ep.step(public)['code'];assert code in ['OK','SUCCESS']
 gt.append(snapshot(ep,len(gt),a,code))
for a in reference:
 apply(a)
 if ep.records[-1]['eventOccurred']:apply({'type':'detach','partId':'X001'})
apply({'type':'finish'})
assert ep.success and len(gt)==8
wrong=traces[1]['frames'][4];fixed=traces[1]['frames'][8]
assert wrong['feedback']=='OK' and wrong['outOfGoalPieces']>0 and fixed['outOfGoalPieces']==0
result=dict(schema='brickplan-qualitative-repair/1',status='REPLAY_VERIFIED',
            scope='Archived v5 development example; no current-v6/community agent score. API response text is excluded.',
            rawMessagesBundled=False,apiCallsThisExport=0,certificate=certificate,referenceSource=str(evpath.relative_to(ROOT)),
            referenceSourceSha256=sha(evpath),gt=gt,traces=traces,
            semantics={'GT':'One feasible witness; alternative legal order is accepted.',
                       'valid':'Physically legal action and no out-of-goal installed piece; incompleteness is allowed.',
                       'wrongPose':'An installed piece does not match any target placement, although its action may be legal.',
                       'externalFault':'Injected environment change, not a model error.',
                       'finish':'Success requires correct final geometry, not matching GT at intermediate steps.'})
dump(HERE/'evidence/repair-comparison.json',result)
print('Verified archived decisions:',sum(t['decisions'] for t in traces),'GT steps:',len(gt))
