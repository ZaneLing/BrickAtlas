"""Dynamic-first questions with one representative static repair per source."""
from collections import Counter
from copy import deepcopy
import argparse,hashlib,fcntl
from scaling_release import OUT
from expansion_v7.build import read,write,states_for,run_witness,signature_key,HUMAN,FAMILIES
from expansion_v7.runtime import runtime,execute,Episode,public_action
from expansion_v7.variants import augment,pad
from bench_design.source_expansion import visibility
from community_modules.core import render_certificate
from dynamic_v5.vision import DynamicVisionRenderer


def build(number):
 folder=OUT/'private'/number;meta=read(folder/'metadata.json');cert=pad(augment(read(folder/'base-certificate.private.json.gz')))
 rt=runtime(cert);normal=read(folder/'base-manual.private.json.gz')['actions'];states=states_for(rt,normal);n=len(normal)
 renderer=DynamicVisionRenderer(render_certificate(cert),rt);cases=[];rejected=[];seen=set()
 def make(family,mode='dynamic',cp=0):
  return dict(id=f'SC:{number}:{mode}:{family}',module=cert['id'],sourceSetId=number,mode=mode,family=family,initial=deepcopy(states[0] if mode=='dynamic' else states[cp]),goal=deepcopy(states[-1] if mode=='dynamic' else states[cp]),events=[],completedInstructionStep=0 if mode=='dynamic' else cp,humanErrorIds=HUMAN.get(family,[]),protocol='brick-atlas-scaling/1',track='whole-object' if cert.get('environmentMode')=='white-baseplate' else 'finishing-stage')
 def add(c):
  key=signature_key(rt,c)
  if key in seen:return False
  seen.add(key);c['physicalTaskSha256']=key;c['humanValidated']=False;c['modelEvaluated']=False;cases.append(c);return True
 control=make('control');control.update(run_witness(cert,control,normal,rt.q));add(control)
 # Rotate family priority between sources, while retaining missing as a common anchor.
 sequence=['wrong-color','offset','wrong-part','rotated','extra-layer','early-cover','buried-repair','left-right-swap','repeat-omission','repeated-step']
 shift=int(hashlib.sha256(number.encode()).hexdigest()[:4],16)%len(sequence)
 order=['missing']+sequence[shift:]+sequence[:shift]
 if n>16:order=[f for f in order if f not in ('buried-repair','early-cover')]+['buried-repair','early-cover']
 cps=list(dict.fromkeys([max(2,n//3),max(2,2*n//3),n-1,n]))
 cps=[cp for cp in cps if 1<cp<=n]
 paired=[]
 for family in order:
  found=None;tried=0
  for cp in cps:
   for variant in range(min(cp,2)):
    try:incident=rt.incident(family,states[cp],latest=normal[cp-1]['actor'],placement_order={a['actor']:i for i,a in enumerate(normal[:cp])},variant=variant)
    except ValueError as exc:
     rejected.append(dict(family=family,reason=str(exc)[:200]));continue
    if not incident:continue
    d=make(family);d['events']=[dict(family=family,minimumInstalled=cp,minimumActionsSincePrevious=1,humanErrorIds=HUMAN[family],variant=variant)]
    try:d.update(run_witness(cert,d,normal,rt.q))
    except AssertionError:continue
    e=d['referenceEvents'][0];v=visibility(renderer,e['before'],e['after']);tried+=1
    if not v['visible']:continue
    d['visibilityCheck']=v;found=d;break
   if found:break
  if found:
   if add(found):paired.append(found)
  else:rejected.append(dict(family=family,reason='No visible legal triggered and recovered event in configured search',renderedTrials=tried))
  if len(paired)>=5:break
 if not paired:
  write(folder/'case-failure.json',dict(reason='No qualified dynamic repair family',rejected=rejected));raise ValueError('No qualified repair family')
 # Multiple incidents are an additional condition only when both actually fire.
 if n>=8:
  names=[d['family'] for d in paired]
  for first,last in ([(names[0],names[1]),(names[1],names[-1])] if len(names)>1 else [(names[0],names[0])]):
   d=make('multiple-'+first+'-then-'+last);d['humanErrorIds']=sorted(set(HUMAN[first]+HUMAN[last]+['H13']))
   d['events']=[dict(family=f,minimumInstalled=cp,minimumActionsSincePrevious=1 if i==0 else 3,humanErrorIds=HUMAN[f],variant=0) for i,(f,cp) in enumerate(zip([first,last],[max(2,n//3),max(4,2*n//3)]))]
   try:
    d.update(run_witness(cert,d,normal,rt.q));vs=[visibility(renderer,e['before'],e['after']) for e in d['referenceEvents']]
    if not all(v['visible'] for v in vs):continue
    d['visibilityCheck']=vs
    if add(d):break
   except AssertionError:continue
 # Exactly one static counterpart; prefer meaningful non-missing recovery.
 choices=sorted(paired,key=lambda d:(d['family']=='missing',-len(d['referenceEvents'][0]['recovery'])))
 d=choices[0];e=d['referenceEvents'][0];cp=d['events'][0]['minimumInstalled'];s=make(d['family'],'static',cp)
 s.update(initial=deepcopy(e['after']),goal=deepcopy(e['before']),referenceActions=deepcopy(e['recovery']),referenceIncident=e,visibilityCheck=d['visibilityCheck'],legalWitnessOnly=True,pairedDynamicId=d['id'])
 if int(hashlib.sha256(number.encode()).hexdigest()[:8],16)%5==0:
  s.update(id=f'SC:{number}:static:control',family='control',initial=deepcopy(s['goal']),referenceActions=[],referenceIncident=None,visibilityCheck=None,humanErrorIds=[],pairedDynamicId=control['id'])
 ep=Episode(cert,s)
 for a in s['referenceActions']:
  ep.step(public_action(ep,a));assert ep.feedback['code']=='OK'
 ep.step(dict(type='finish'));assert ep.score()['success'];s['referenceScore']=ep.score();add(s)
 meta.update(caseCount=len(cases),dynamicCases=sum(c['mode']=='dynamic' for c in cases),staticCases=1,families=sorted({c['family'] for c in cases}),humanValidated=False,apiModelEvaluated=False,questionStatus='machine-checked-human-review-pending',failedFamilies=rejected)
 write(folder/'certificate.private.json.gz',cert);write(folder/'manual.private.json.gz',dict(actions=normal,states=states));write(folder/'cases.private.json.gz',cases);write(folder/'metadata.json',meta)
 (folder/'status.json').unlink(missing_ok=True)
 # A normalized public design describes what is seen, never the hidden event schedule.
 design=dict(setNumber=number,title=meta['title'],scope=meta['scope'],activeParts=n,initialState='white-stud-baseplate' if cert.get('environmentMode')=='white-baseplate' else 'complete-source-context-minus-selected-parts',target='all selected original source parts restored to their original goal geometry',observation='on-demand current / target / inventory; matched canvas; 0/90/180/-90 degree views and top view',instruction='one-part sequence available through inspect(manualStep); not a uniquely required order',actions=['observe','inspect','attach','detach','recall','finish'],gtPolicy='legal witnesses, equivalent physical final states accepted; no intermediate GT matching',cases=[dict(id=c['id'],mode=c['mode'],family=c['family'],events=len(c['events']),referenceMoves=len(c['referenceActions'])) for c in cases])
 write(OUT/'designs'/f'{number}.json',design);return meta


def main():
 p=argparse.ArgumentParser();p.add_argument('--set',required=True);a=p.parse_args()
 folder=OUT/'private'/a.set;folder.mkdir(parents=True,exist_ok=True)
 lock=(folder/'work.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX)
 if (folder/'cases.private.json.gz').exists():print('BUILT CACHED',a.set,flush=True);return
 try:m=build(a.set);print('BUILT',a.set,m['dynamicCases'],m['staticCases'],flush=True)
 except Exception as e:
  from scaling_release.prepare import cause
  write(OUT/'private'/a.set/'status.json',dict(status='withheld',phase='cases',reason=cause(e)));print('CASE WITHHELD',a.set,cause(e),flush=True)
if __name__=='__main__':main()
