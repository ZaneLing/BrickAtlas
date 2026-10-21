"""Frozen, balanced static pilot with explicit action schema and shuffled pose order."""
if __name__ == '__main__':
 raise SystemExit('Retired protocol. Use run.py --select --models <vision-model-id> for visual v3. Historical files are retained.')
import os,json,hashlib,random,argparse
from pathlib import Path
os.environ['BRICKPLAN_EVAL_OUT']='deliverables/brickplan-static-audit-2026-10-14'
os.environ['BRICKPLAN_AUDIT']='static-audit-2026-10-14'
import run
MODELS=['openai/gpt-6.1-sol','google/gemini-4-argon','anthropic/claude-sonnet-5.5']
KINDS=['missing','wrong_color','wrong_type','wrong_size','offset','rotation','height_layer','swapped_positions']
def select():
 bank=run.ROOT/'deliverables/brickplan-repair-library';index=json.loads((bank/'index.json').read_text());rows=[]
 for m in index['models']:rows.extend(json.loads((bank/'models'/m['modelId']/'cases.json').read_text()).values())
 chosen=[]
 def add(c,stratum):
  chosen.append({'mode':'static','modelId':c['modelId'],'caseId':c['id'],'kind':c['kind'],'difficulty':c['difficulty'],'restrictedCost':c['expectedOptimum'],'stratum':stratum,'seed':20261014+len(chosen)*97,'protocolVersion':'v2'})
 for kind in KINDS:
  pool=sorted([c for c in rows if c['kind']==kind],key=lambda c:(-c['expectedOptimum'],c['id']))
  add(pool[0],'hard_single')
  other=[c for c in pool if c['modelId']!=pool[0]['modelId']] or pool[1:]
  if other:add(other[len(other)//2],'second_structure')
 for c in sorted([c for c in rows if c.get('challengeVariant')=='four_fault_coupling'],key=lambda c:(-c['expectedOptimum'],c['id'])):add(c,'four_fault')
 for model in ['v23-30181','v23-3223--deep']:add(next(c for c in rows if c['modelId']==model and c['kind']=='control'),'control')
 # Round-robin coverage: hard types, compound and controls before second examples.
 chosen.sort(key=lambda c:(0 if c['stratum']=='control' else 1 if c['stratum']=='hard_single' else 2 if c['stratum']=='four_fault' else 3,c['caseId']))
 # Interleave hard compound early enough that budget depletion cannot exclude it.
 hard=[c for c in chosen if c['stratum']=='four_fault'];other=[c for c in chosen if c['stratum']!='four_fault'];ordered=[]
 for i,c in enumerate(other):
  ordered.append(c)
  if i<len(hard):ordered.append(hard[i])
 obj={'models':MODELS,'tracks':['symbolic','visual'],'specs':ordered,'maxCalls':6,'maxOutputTokens':4096,'reasoningEffort':'low','selection':'Frozen before API: hardest + second distinct structure per available singleton kind, all eight four-fault cases, two controls. Not random bank sampling. No standalone extra case exists. Public pose order shuffled and candidate required. Matched 3-model x 2-input blocks; per-call cost cap may leave a block incomplete; skipped cells reported.'}
 f=run.OUT/'selection.json'
 if f.exists():assert json.loads(f.read_text())==obj
 else:run.dump(f,obj)
 print(json.dumps({'cases':len(ordered),'plannedEpisodes':len(ordered)*6,'structures':len({s['modelId'] for s in ordered}),'kindCounts':{k:sum(s['kind']==k for s in ordered) for k in KINDS+['compound','control']}}))
 return obj
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--select',action='store_true');args=p.parse_args();obj=select()
 if not args.select:
  schedule=json.loads((run.OUT/'schedule.json').read_text())
  jobs=schedule.get('jobs') or [{'spec':s,'model':m,'track':t} for s in schedule['specs'] for t in obj['tracks'] for m in MODELS]
  for job in jobs:
   spec,model,track=job['spec'],job['model'],job['track']
   try:run.run_one(spec,model,track,max_calls=obj['maxCalls'])
   except Exception as exc:
    run.dump(run.OUT/'stop.json',{'reason':str(exc),'spec':spec,'model':model,'track':track});raise
