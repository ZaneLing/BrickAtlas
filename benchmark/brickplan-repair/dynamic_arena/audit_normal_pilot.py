"""No-API audit of all normal and eligible incident pilot transcripts."""
import base64
import gzip
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from dynamic_arena import OUT
from dynamic_arena.demo import create
from dynamic_arena.normal_pilot import LEDGER, REPORT
from dynamic_arena.transport import write_json


def main():
    normal=json.loads(REPORT.read_text())
    incident_path=OUT/'incident-pilot-results.json'
    incident=json.loads(incident_path.read_text()) if incident_path.exists() else {'runs':[]}
    runs=[*normal['runs'],*incident['runs']]
    ledger=json.loads(LEDGER.read_text())
    report=[];images=0;verified_receipts=0
    with TemporaryDirectory(prefix='normal-pilot-audit-') as tmp:
        for item in runs:
            rid=item['runId'];directory=OUT/'runs'/rid
            record=json.loads(gzip.decompress((directory/'record.private.json.gz').read_bytes()))
            log=json.loads((directory/'log.json').read_text())
            charges=[c for c in ledger['charges'] if c['run']==rid]
            assert len(charges)==len(log['calls'])
            for charge,call in zip(charges,log['calls']):
                raw=gzip.decompress((directory/'api'/(charge['id']+'.request.json.gz')).read_bytes())
                assert charge['model']==item['model']
                assert b'eventLedger' not in raw and b'referenceActions' not in raw
                if charge['status']!='settled':
                    assert call.get('error') and not call.get('providerReceipt')
                    continue
                receipt=json.loads((directory/'api'/(charge['id']+'.private.json')).read_text())
                assert hashlib.sha256(raw).hexdigest()==call['providerReceipt']['requestBodySha256']
                assert receipt['requestShape']['model']==item['model']
                assert receipt['result']['id']==charge['generationId']==call['providerReceipt']['id']
                assert receipt['result']['usage']['cost']==charge['actualUSD']
                sent=json.loads(raw)['messages'][-1]['content']
                shown=call['modelInput']['messages'][-1]['content']
                original=[x for x in sent if x['type']=='image_url']
                readable=[x for x in shown if x['type']=='image_url']
                assert len(original)==len(readable)
                for a,b in zip(original,readable):
                    blob=base64.b64decode(a['image_url']['url'].split(',',1)[1])
                    assert hashlib.sha256(blob).hexdigest()==b['image_url']['sha256']
                    assert blob==(OUT/b['image_url']['url'].lstrip('/')).read_bytes()
                    images+=1
                verified_receipts+=1
            replay=create(Path(tmp)/rid,item['model'],events=rid.startswith('incident-'),model_id=item['objectId'])
            replay.autosave=False
            for entry in record['records']:
                replay.submit(entry['action'])
                current=replay.records[-1]
                for k in ('before','afterOwnActionBeforeExternalChange','after','newEventIndices','feedback'):
                    assert current[k]==entry[k],(rid,k)
            assert replay.ep.state==record['final']
            report.append(dict(runId=rid,model=item['model'],object=item['objectId'],
                terminal=item['result']['terminalStatus'],providerCalls=len(charges),
                settledCalls=sum(c['status']=='settled' for c in charges),
                replayedActions=len(record['records']),appliedEvents=len(record['eventLedger'])))
    out=dict(status='PASS',runs=len(report),verifiedProviderReceipts=verified_receipts,
        verifiedSentImages=images,confirmedCostUSD=sum(c['actualUSD'] or 0 for c in ledger['charges']),
        costUpperBoundUSD=sum(c['actualUSD'] if c['actualUSD'] is not None else c['reservedUSD'] for c in ledger['charges']),
        unsettledRequests=sum(c['status']!='settled' for c in ledger['charges']),
        modelCallsDuringAudit=0,rows=report)
    write_json(OUT/'normal-pilot-audit.json',out)
    print(json.dumps({k:out[k] for k in ('status','runs','verifiedProviderReceipts','verifiedSentImages','confirmedCostUSD','costUpperBoundUSD','unsettledRequests')},ensure_ascii=False))


if __name__=='__main__':main()
