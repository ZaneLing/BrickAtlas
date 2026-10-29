"""Audit every archived pilot attempt; descriptive errors, never v3 scores."""
from collections import Counter, defaultdict
import gzip, json
from release_assets import HERE, ROOT, read, write, sha

BASE=ROOT/'deliverables/brickplan-dynamic-arena'
NAMES={'google/gemini-2.5-flash':'Gemini 2.5 Flash','openai/gpt-6.1-sol':'GPT-6.1 Sol',
       'anthropic/claude-sonnet-5.5':'Claude Sonnet 5.5',
       'qwen/qwen3-vl-235b-a22b-instruct':'Qwen3-VL-235B'}
CODES={'INVALID_REQUEST':'format','UNREGISTERED_POSE':'handle',
       'NO_CONNECTION':'connection','ENDPOINT_COLLISION':'collision','PATH_BLOCKED':'path'}

def main():
 normal=read(BASE/'normal-pilot-results.json');incident=read(BASE/'incident-pilot-results.json')
 selected={x['runId'] for x in normal['latestRuns']+incident['runs']}
 sources={str((BASE/n).relative_to(ROOT)):sha(BASE/n) for n in ['normal-pilot-results.json','incident-pilot-results.json']}
 rows=[];errors=[]
 for x in normal['runs']+incident['runs']:
  folder=BASE/'runs'/x['runId'];rp=folder/'record.private.json.gz';r=read(folder/'result.json')
  record=json.loads(gzip.decompress(rp.read_bytes()));log=read(folder/'log.json')
  assert r==x['result']
  for p in [rp,folder/'log.json',folder/'result.json']:sources[str(p.relative_to(ROOT))]=sha(p)
  codes=Counter(a['feedback']['code'] for a in record['records'])
  assert set(codes)<={'OK','INSPECT','FINISHED',*CODES}
  counts={v:codes[k] for k,v in CODES.items()}
  assert counts['format']==r['executionMetrics']['formatErrorResponses']
  assert sum(counts[k] for k in ['handle','connection','collision','path'])==sum(r['executionMetrics']['physicalRejections'].values())
  valid=r['terminalStatus'] in ('completed','model_budget_exhausted')
  counts.update(wrongFinish=int(valid and r['terminalStatus']=='completed' and not r['success']),
                budget=int(r['terminalStatus']=='model_budget_exhausted'))
  item=dict(runId=x['runId'],selected=x['runId'] in selected,model=r['model'],
    modelLabel=NAMES[r['model']],object=x['objectId'],taskType=r['taskType'],valid=valid,
    status=r['terminalStatus'],success=r['success'] if valid else None,
    decisions=r['executionMetrics']['decisions'],providerCalls=len(log['calls']),
    acceptedMoves=r['executionMetrics']['acceptedMoves'],observations=r['controllerMetrics']['observeCalls'],
    counts=counts,fullPlacement=r['stateMetrics']['fullPlacement'] if valid else None,
    appliedEvents=r['appliedEvents'],normalRunId=x.get('normalRunId'),
    rawPhysicalRejections=r['executionMetrics']['physicalRejections'])
  rows.append(item)
  for rec in record['records']:
   code=rec['feedback']['code']
   if code in CODES:errors.append(dict(runId=x['runId'],selected=item['selected'],decision=rec['decision'],
       category=CODES[code],code=code,action=rec['action'],stateChanged=rec['after']!=rec['before']))
 assert len(rows)==19 and sum(x['selected'] for x in rows)==15
 latest=[x for x in rows if x['selected']];groups=[]
 for model in [*NAMES][:3]:
  for task in ['D0','D1']:
   subset=[x for x in latest if x['model']==model and x['taskType']==task and x['valid']]
   if not subset:continue
   groups.append(dict(label=NAMES[model]+' / '+task,validRuns=len(subset),
     success=sum(x['success'] for x in subset),counts=dict(sum((Counter(x['counts']) for x in subset),Counter()))))
 out=dict(schema='brick-atlas-archived-pilot-audit/1',apiCalls=0,protocol='brick-atlas-tool-arena/2',
   currentProtocolResult=False,selection='Latest recorded attempt per normal model/object; all three incident runs. All retries retained separately.',
   allAttempts=len(rows),selectedAttempts=len(latest),allServiceErrors=sum(not x['valid'] for x in rows),
   selectedServiceErrors=sum(not x['valid'] for x in latest),sources=sources,runs=rows,groups=groups,errorEvents=errors,
   interpretation='Descriptive counts from a small development pilot, not a ranking or internal-cause labels. UNREGISTERED_POSE is handle grounding, not geometry.')
 write(HERE/'evidence/pilot-error-audit.json',out)
 # One row per latest condition; source retries remain in the machine-readable ledger.
 text=r'''\begin{table*}[!ht]\centering\small
\caption{\textbf{All latest archived pilot conditions (Arena v2).} Fmt: invalid request; ID: unregistered pose handle; Conn/Coll/Path: rejected connection, endpoint collision, or extraction path. Counts are actions, not independent cases. Service errors have no ability outcome. Four earlier service-interrupted attempts remain in the all-attempt ledger (19 total). These are not v3 benchmark results.}
\label{tab:pilot-all}
\begin{tabularx}{\textwidth}{@{}Xllrrrrrr@{}}\toprule
Model / object & Task & Outcome & Fmt & ID & Conn & Coll & Path & Moves\\\midrule
'''
 for x in latest:
  outcome=('success' if x['success'] else 'wrong finish' if x['counts']['wrongFinish'] else 'budget' if x['valid'] else 'service')
  vals=[x['modelLabel']+' / '+x['object'].replace('obj-',''),x['taskType'],outcome,
    *[str(x['counts'][k]) if x['valid'] else '---' for k in ['format','handle','connection','collision','path']],
    str(x['acceptedMoves']) if x['valid'] else '---']
  text+=' & '.join(vals)+r'\\'+'\n'
 text+=r'\bottomrule\end{tabularx}\end{table*}'+'\n';(HERE/'tables/pilot-all.tex').write_text(text)
 print('Audited 19 archived attempts, 15 latest conditions, 12 valid latest runs; no API calls.')

if __name__=='__main__':main()
