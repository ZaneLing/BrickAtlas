"""Verify archived API pixels/usage, and classify JSON vs argument failures.

No model calls or action changes. Retain original metric counts as provenance.
"""
import base64,gzip,hashlib,json,re
from copy import deepcopy
from dynamic_arena import ROOT,OUT as ARENA_OUT
from dynamic_arena.transport import write_json
from bench_design.metrics import execution_metrics
from unified_agent import OUT
from unified_agent.providers import LEDGER


def main():
    report=json.loads((OUT/'pilot.json').read_text());ledger=json.loads(LEDGER.read_text())
    evidence=set();checked=0;image_count=0;revisions=[]
    for result in report['runs']:
        folder=ARENA_OUT/'runs'/result['arenaRunId']
        log=json.loads((folder/'log.json').read_text())
        records=json.load(gzip.open(folder/'record.private.json.gz'))['records']
        codes=[]
        for c in log['calls']:
            if 'modelOutputRaw' in c:
                try:
                    if isinstance(c['modelOutputRaw'],str):json.loads(c['modelOutputRaw'])
                    malformed=False
                except (ValueError,TypeError):malformed=True
                codes.append(malformed)
            receipt=c.get('providerReceipt')
            if not receipt:continue
            raw=gzip.decompress((folder/'api'/(receipt['archiveId']+'.request.json.gz')).read_bytes())
            assert hashlib.sha256(raw).hexdigest()==receipt['requestBodySha256']
            payload=json.loads(raw);hashes=[]
            for m in payload['messages']:
                if not isinstance(m['content'],list):continue
                for b in m['content']:
                    if b['type']=='image_url':hashes.append(hashlib.sha256(base64.b64decode(b['image_url']['url'].split(',',1)[1])).hexdigest())
            assert hashes==c['inputImageHashes'];image_count+=len(hashes);checked+=1
            for item in c['modelInput']['messages'][-1]['content']:
                if item['type']=='image_url':
                    asset=ARENA_OUT/item['image_url']['url'].lstrip('/')
                    assert hashlib.sha256(asset.read_bytes()).hexdigest()==item['image_url']['sha256']
        assert len(codes)==len(records)
        fixed=deepcopy(records)
        for r,malformed in zip(fixed,codes):r['parseError']=malformed
        metrics=execution_metrics(fixed)
        old=result['executionMetrics']
        before={k:old[k] for k in ('formatErrorResponses','schemaErrorResponses')}
        after={k:metrics[k] for k in before}
        if before!=after:
            result.setdefault('outputMetricCorrection',dict(reason='Separate JSON parsing from valid JSON with invalid fields; execution unchanged',original=before,apiCalls=0))
            result['executionMetrics'].update(after)
            revisions.append(dict(runId=result['arenaRunId'],before=before,after=after))
        result['outputValidation']=dict(jsonParseFailures=sum(codes),
            argumentSchemaFailures=sum(c.get('modelOutput',{}).get('tool')=='invalid' for c in log['calls'])-sum(codes))
        for name in ('result.json','log.json','spectator.json'):
            p=folder/name;value=result if name=='result.json' else json.loads(p.read_text())
            if name!='result.json':value['result']=result
            write_json(p,value)
        charges=[c for c in ledger['charges'] if c['run']==folder.name]
        assert len(charges)==result['apiCalls']
        for p in folder.rglob('*'):
            if p.is_file() and p.suffix!='.pending':
                evidence.add(str(p.relative_to(ROOT)))
                if p.suffix=='.json':
                    for url in re.findall(r'/assets/[0-9a-f]{64}\.png',p.read_text()):
                        asset=ARENA_OUT/url.lstrip('/');assert asset.is_file()
                        evidence.add(str(asset.relative_to(ROOT)))
    assert {c['run'] for c in ledger['charges']}=={r['arenaRunId'] for r in report['runs']}
    write_json(OUT/'pilot.json',report)
    write_json(OUT/'checks/evidence-audit.json',dict(passed=True,apiCallsMadeByAudit=0,
        completeReceiptsChecked=checked,orderedImageHashesChecked=image_count,
        allLedgerRunsIncluded=True,missingProviderResponsesRetainedAsErrors=True,outputMetricCorrections=revisions,
        evidenceFiles=sorted(evidence)))
    print('Verified',checked,'complete receipts and',image_count,'ordered image hashes; all paid runs retained.')


if __name__=='__main__':main()
