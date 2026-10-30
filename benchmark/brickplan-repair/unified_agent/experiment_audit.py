"""Read-only evidence and cross-backbone contract audit; no inference calls."""
import base64,gzip,hashlib,json,time
from collections import defaultdict
from dynamic_arena import OUT as ARENA
from dynamic_arena.transport import write_json
from unified_agent.experiment_batch import OUT,MODELS,merged,ledger_path


def main():
    report=merged();folders={p.name:p for p in (OUT/'preflight').glob('*/attempt-*')}
    folders.update({r['arenaRunId']:ARENA/'runs'/r['arenaRunId'] for r in report['runs']+report['activeRuns']})
    issues=[];archives={};bindings=defaultdict(set);counts=dict(requests=0,pending=0,responses=0,rejected=0,uncertain=0,images=0,matchedReceipts=0)
    for model in MODELS:
        lp=ledger_path(model)
        if not lp.exists():continue
        for c in json.loads(lp.read_text())['charges']:
            counts['requests']+=1
            if c['status']=='pending':counts['pending']+=1;continue
            try:
                folder=folders[c['run']];raw=gzip.decompress((folder/'api'/(c['id']+'.request.json.gz')).read_bytes());body=json.loads(raw)
                assert not any(k.lower() in ('authorization','api_key','apikey') for k in body),'Credential header in request body'
                if c['provider']=='ark':assert body['model'].startswith('ep-'),'Ark endpoint missing'
                hashes=[]
                for msg in body['messages']:
                    if isinstance(msg['content'],list):
                        for b in msg['content']:
                            if b['type']=='image_url':hashes.append(hashlib.sha256(base64.b64decode(b['image_url']['url'].split(',',1)[1],validate=True)).hexdigest())
                counts['images']+=len(hashes);archives[c['id']]=(hashlib.sha256(raw).hexdigest(),hashes)
                response=folder/'api'/(c['id']+'.response.private.json.gz')
                if response.exists():
                    r=json.loads(gzip.decompress(response.read_bytes()));u=r['usage']
                    assert u['prompt_tokens']==c['promptTokens'];assert u['completion_tokens']==c['completionTokens']
                    counts['responses']+=1;bindings[model].add(r.get('model'))
                elif c['status']=='rejected_before_generation':
                    assert (folder/'api'/(c['id']+'.error.json.gz')).exists();counts['rejected']+=1
                elif c['status']=='uncertain':counts['uncertain']+=1
                else:raise AssertionError('Accounted response absent')
            except Exception as exc:issues.append(dict(run=c['run'],archiveId=c['id'],error=str(exc)))
    groups=defaultdict(list)
    for r in report['runs']:
        log=json.loads((folders[r['arenaRunId']]/'log.json').read_text())
        for c in log['calls']:
            rec=c.get('providerReceipt') or {};uid=rec.get('archiveId')
            if not uid:continue
            try:
                sha,hashes=archives[uid];assert sha==rec['requestBodySha256'];assert hashes==c['inputImageHashes'];counts['matchedReceipts']+=1
            except Exception as exc:issues.append(dict(run=r['arenaRunId'],decision=c['index'],error='Receipt/image mismatch: '+str(exc)))
        groups[r['caseId'],r['arenaBranch'],r['inputVersion']].append(dict(model=r['model'],runId=r['arenaRunId'],contract=r['agentContractSha256'],
            profile=r['agentProfile'],initialImages=log['calls'][0]['inputImageHashes'] if log['calls'] else []))
    comparisons=[]
    for (cid,arm,version),rs in groups.items():
        if len({r['model'] for r in rs})<2:continue
        same=len({r['contract'] for r in rs})==1 and all(r['profile']==rs[0]['profile'] and r['initialImages']==rs[0]['initialImages'] for r in rs)
        comparisons.append(dict(caseId=cid,arm=arm,inputVersion=version,models=[r['model'] for r in rs],same=same))
        if not same:issues.append(dict(caseId=cid,arm=arm,error='Cross-backbone initial input/profile/contract mismatch'))
    result=dict(passed=not issues,checkedAt=time.time(),counts=counts,actualReturnedModelBindings={m:sorted(v) for m,v in bindings.items()},
        crossBackboneComparisons=comparisons,issues=issues,apiCalls=0,
        scope='Raw request/response, exact image-byte and initial same-condition contract consistency. Pending calls skipped; hello diagnosis is separate. Not independent physics.')
    write_json(OUT/'checks/evidence-audit.json',result);print(json.dumps({k:v for k,v in result.items() if k!='crossBackboneComparisons'},ensure_ascii=False))


if __name__=='__main__':main()
