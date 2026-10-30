"""Verify archived interface evidence and replay old invalid outputs, without API calls."""
import base64,gzip,hashlib,json
from pathlib import Path
from dynamic_arena import OUT as ARENA
from dynamic_arena.contract import validate
from dynamic_arena.transport import write_json
from unified_agent import ROOT,RUN_OUT
from unified_agent.readiness import source_digest
from unified_agent.providers import total


def main():
    report=json.loads((RUN_OUT/'api-preflight.json').read_text());rows=[];assets=set();ids=[]
    for certificate in report['rows']:
        # Archived evidence remains auditable after a live certificate expires.
        # Freshness/source checks belong to readiness.require before new calls.
        model=certificate['model'];assert certificate['passed']
        directory=ROOT/certificate['archiveDirectory'] if certificate.get('archiveDirectory') else RUN_OUT/'preflight'/model.replace('/','--')
        for probe in certificate['probes']:
            receipt=probe['receipt'];uid=receipt['archiveId'];ids.append(uid)
            raw=gzip.decompress((directory/'api'/(uid+'.request.json.gz')).read_bytes())
            assert hashlib.sha256(raw).hexdigest()==receipt['requestBodySha256']
            request=json.loads(raw)
            response=json.loads(gzip.decompress((directory/'api'/(uid+'.response.private.json.gz')).read_bytes()))
            assert response['choices'][0]['finish_reason']=='stop'
            assert response['choices'][0]['message']['content']==probe['rawOutput']
            assert response['usage']==probe['usage']
            assert validate(probe['rawOutput'],memory=True,limits=certificate['profile'])['valid']
            actual=[b for m in request['messages'] if isinstance(m['content'],list) for b in m['content'] if b['type']=='image_url']
            readable=[b['image_url'] for m in probe['input']['messages'] if isinstance(m['content'],list) for b in m['content'] if b['type']=='image_url']
            assert len(actual)==len(readable)==probe['inputImages']
            for a,r in zip(actual,readable):
                pixels=base64.b64decode(a['image_url']['url'].split(',',1)[1],validate=True)
                assert hashlib.sha256(pixels).hexdigest()==r['sha256']
                p=ARENA/r['url'].lstrip('/');assert p.read_bytes()==pixels
                assets.add(str(p.relative_to(ROOT)))
            if model.startswith('qwen/'):
                assert request['enable_thinking'] is False and request['max_completion_tokens']==8192
            elif model.startswith('deepseek/'):
                assert request['thinking']['type']=='disabled' and request['reasoning_effort']=='none' and request['max_tokens']==8192
            elif model.startswith('openai/'):
                assert request['reasoning']=={'effort':'low'} and 'temperature' not in request and request['max_tokens']==8192
            else:assert request['reasoning']=={'enabled':False} and request['max_tokens']==8192
            rows.append(dict(model=model,index=probe['index'],images=len(actual),passed=True,archiveId=uid))
    ledger=json.loads((RUN_OUT/'preflight-ledger.private.json').read_text())
    assert len(ids)==len(set(ids))==2*len(report['rows'])
    assert set(ids)<={c['id'] for c in ledger['charges']}
    assert all(c['status'] in ('settled','usage_estimated') for c in ledger['charges'] if c['id'] in ids)
    write_json(RUN_OUT/'checks/api-archive-audit.json',dict(passed=True,apiCalls=0,archivedRequests=len(rows),
        archivedImageOccurrences=sum(r['images'] for r in rows),uniqueImages=len(assets),assets=sorted(assets),
        sourceSha256=source_digest(),budgetAccountedUpperUSD=total(ledger),rows=rows))
    # This is parser replay only: never execute old model actions or change old scores.
    regression=[]
    pilot=json.loads((ROOT/'deliverables/brick-atlas-unified-agent-v1/pilot.json').read_text())
    for run in pilot['runs']:
        path=ARENA/'runs'/run['arenaRunId']/'log.json'
        if not path.exists():continue
        for call in json.loads(path.read_text()).get('calls',[]):
            if call.get('modelOutput',{}).get('tool')!='invalid':continue
            validation=validate(call['modelOutputRaw'],memory=True)
            regression.append(dict(runId=run['arenaRunId'],decision=call['index'],acceptedNow=validation['valid'],
                normalization=validation['normalizations'],errors=validation['errors'],jsonError=validation['jsonError']))
    write_json(RUN_OUT/'checks/historical-output-regression.json',dict(apiCalls=0,actionsExecuted=0,historicalScoresChanged=False,
        checked=len(regression),acceptedNow=sum(r['acceptedNow'] for r in regression),
        stillRejected=sum(not r['acceptedNow'] for r in regression),rows=regression))
    print('PASS: archive hashes, image bytes, provider settings, receipts and ledger; historical output replay',len(regression))


if __name__=='__main__':main()
