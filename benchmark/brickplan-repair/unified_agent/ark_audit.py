"""Check saved raw API receipts and exact image bytes; makes no API calls."""
import base64,gzip,hashlib,json,time
from pathlib import Path
from dynamic_arena import OUT as ARENA
from dynamic_arena.transport import write_json
from unified_agent.ark_batch import OUT,LEDGER,combined_report

def main():
 ledger=json.loads(LEDGER.read_text());report=combined_report();folders={p.name:p for p in (OUT/'preflight').glob('*/attempt-*')}
 folders.update({p.name:p for p in (OUT/'diagnostics').iterdir() if p.is_dir()})
 folders.update({r['arenaRunId']:ARENA/'runs'/r['arenaRunId'] for r in report['runs']})
 for r in report.get('activeRuns',[]):folders[r['arenaRunId']]=ARENA/'runs'/r['arenaRunId']
 image_counts=0;returned=0;rejected=0;issues=[];bindings={};archives={}
 for c in ledger['charges']:
  # A live response can be archived just before its ledger entry is settled.
  # Reconcile it on the next audit; do not call this race corrupt evidence.
  if c['status']=='pending':continue
  try:
   folder=folders[c['run']];request=folder/'api'/(c['id']+'.request.json.gz');raw=gzip.decompress(request.read_bytes());body=json.loads(raw)
   assert not any(k.lower() in ('authorization','api_key','apikey') for k in body)
   if c['provider']=='ark' and c['status']=='usage_estimated':assert body['model'].startswith('ep-')
   hashes=[]
   for m in body['messages']:
    if isinstance(m['content'],list):
     for b in m['content']:
      if b['type']=='image_url':hashes.append(hashlib.sha256(base64.b64decode(b['image_url']['url'].split(',',1)[1],validate=True)).hexdigest())
   image_counts+=len(hashes);archives[c['id']]=(hashlib.sha256(raw).hexdigest(),hashes)
   response=folder/'api'/(c['id']+'.response.private.json.gz')
   if response.exists():
    r=json.loads(gzip.decompress(response.read_bytes()));u=r['usage'];assert u['prompt_tokens']==c['promptTokens'];assert u['completion_tokens']==c['completionTokens']
    returned+=1;bindings[c['model']]=r.get('model')
   elif c['status']=='rejected_before_generation':
    assert (folder/'api'/(c['id']+'.error.json.gz')).exists();rejected+=1
   elif c['status'] not in ('pending','uncertain'):raise AssertionError('Response missing for accounted usage')
  except Exception as exc:issues.append(dict(id=c['id'],run=c['run'],error=type(exc).__name__+': '+str(exc)))
 matched=0
 for r in report['runs']:
  log=json.loads((folders[r['arenaRunId']]/'log.json').read_text())
  for call in log['calls']:
   receipt=call.get('providerReceipt') or {};uid=receipt.get('archiveId')
   if not uid:continue
   try:
    sha,hashes=archives[uid];assert sha==receipt['requestBodySha256'];assert hashes==call['inputImageHashes'];matched+=1
   except Exception as exc:issues.append(dict(run=r['arenaRunId'],decision=call['index'],error='Receipt/image mismatch: '+str(exc)))
 result=dict(passed=not issues,checkedAt=time.time(),requests=len(ledger['charges']),responses=returned,rejectedBeforeGeneration=rejected,
  embeddedImages=image_counts,matchedTaskReceipts=matched,actualReturnedModelBindings=bindings,issues=issues,apiCalls=0,
  purpose='Stored receipt/image consistency, not semantic image comprehension or independent physics proof')
 write_json(OUT/'checks/evidence-audit.json',result);print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
