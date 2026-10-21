"""Offline salvage of a logged response, never replacing strict primary metrics."""
from pathlib import Path
from copy import deepcopy
import json
from protocol import Episode,load
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'deliverables/brickplan-static-audit-2026-10-14'
def objects(text):
 decoder=json.JSONDecoder()
 for i,c in enumerate(text):
  if c!='{':continue
  try:obj,_=decoder.raw_decode(text[i:])
  except ValueError:continue
  if isinstance(obj,dict) and isinstance(obj.get('actions'),list) and 1<=len(obj['actions'])<=8:yield obj
rows=[]
for file in (OUT/'runs').glob('*.json'):
 r=json.loads(file.read_text());s=r['spec'];cert,cs=load(s['modelId']);ep=Episode(cert,cs[s['caseId']],seed=s['seed'],protocol_version=s['protocolVersion'])
 for st in r['steps']:
  response=st.get('response')
  if response:
   try:json.loads(response['content']);valid=True
   except ValueError:valid=False
   if not valid:
    candidates=list(objects(response['content'])); unique={json.dumps(o,sort_keys=True):o for o in candidates}
    row={'runId':r['id'],'model':r['model'],'track':r['track'],'caseId':s['caseId'],'callIndex':st['callIndex'],'candidateJSONObjects':len(unique),'primaryMetricUnchanged':True}
    if len(unique)==1:
     obj=next(iter(unique.values()));probe=deepcopy(ep);codes=[]
     for a in obj['actions']:
      feedback=probe.step(a);codes.append(feedback['code'])
      if feedback['code']!='OK':break
     row.update(salvagedActions=obj['actions'],feedbackCodes=codes,successIfOnlyFormattingRelaxed=probe.success,remainingMismatches=probe.score()['remainingMismatches'])
    rows.append(row)
  for ex in st.get('executions',[]):assert ep.step(ex['action'])==ex['feedback']
(OUT/'format-diagnostic.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print('invalid JSON responses',len(rows),'uniquely salvageable',sum(r['candidateJSONObjects']==1 for r in rows),'immediate success if relaxed',sum(r.get('successIfOnlyFormattingRelaxed',False) for r in rows))
