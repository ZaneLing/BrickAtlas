"""Frozen latest-model subset, preserving the original pilot and shared $2 ceiling."""
if __name__ == '__main__':
 raise SystemExit('Retired protocol. Use run.py --select --models <vision-model-id> for visual v3. Historical files are retained.')
import os,json,shutil
from pathlib import Path
os.environ['BRICKPLAN_EVAL_OUT']='deliverables/brickplan-api-latest-2026-10-14'
import run
MODELS=['openai/gpt-6.1-sol','google/gemini-4-argon']
run.OUT.mkdir(parents=True,exist_ok=True)
source=json.loads((run.ROOT/'deliverables/brickplan-api-pilot/selection.json').read_text())
specs=[s for s in source['specs'] if s.get('kind') in ('height_layer','compound') or s['mode']=='dynamic' and s.get('event')=='color']
selection={'models':MODELS,'tracks':['symbolic','visual'],'specs':specs,'maxCalls':4,'maxOutputTokens':4096,'reasoningEffort':'low','selection':'Preselected before API: short static repair, hardest compound, from-empty color disturbance. Matched source cases; 4 calls vs prior 8, reasoning enabled. Not a population score.'}
p=run.OUT/'selection.json'
if p.exists():assert json.loads(p.read_text())==selection
else:run.dump(p,selection)
shutil.copy('/tmp/brickplan-model-catalog.json',run.OUT/'model-catalog.json')
for spec in specs:
 for track in selection['tracks']:
  for model in MODELS:
   try:run.run_one(spec,model,track,max_calls=4)
   except Exception as exc:
    print(json.dumps({'stopped':str(exc),'model':model,'spec':spec,'track':track}),flush=True)
    raise
