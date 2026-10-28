"""Independent transcript checks for the pull-observation API run. No API calls."""
import base64
import gzip
import hashlib
import json
from pathlib import Path
import tempfile
from dynamic_arena import OUT
from dynamic_arena.demo import create
from dynamic_arena.tool_arena import PROTOCOL, parse
from dynamic_arena.transport import write_json


def main():
    runid = json.loads((OUT / 'latest.json').read_text())['runId']
    directory = OUT / 'runs' / runid
    spectator = json.loads((directory / 'spectator.json').read_text())
    assert spectator['protocol'] == PROTOCOL and spectator['phase'] == 'finished'
    calls = spectator['calls']
    ledger = json.loads((OUT / 'api-ledger.private.json').read_text())
    charges = [c for c in ledger['charges'] if c['run'] == runid]
    record = json.loads(gzip.decompress((directory / 'record.private.json.gz').read_bytes()))
    assert len(charges) == len(calls) and all(c['status'] == 'settled' for c in charges)
    image_count, observations, rotated = 0, 0, 0
    for charge, call in zip(charges, calls):
        receipt = json.loads((directory / 'api' / (charge['id'] + '.private.json')).read_text())
        raw = gzip.decompress((directory / 'api' / (charge['id'] + '.request.json.gz')).read_bytes())
        assert hashlib.sha256(raw).hexdigest() == call['providerReceipt']['requestBodySha256']
        sent = json.loads(raw)
        assert sent['model'] == spectator['model']
        assert parse(receipt['result']['choices'][0]['message']['content']) == call['modelOutput']
        assert receipt['result']['id'] == call['providerReceipt']['id'] == charge['generationId']
        assert receipt['result']['usage']['cost'] == charge['actualUSD'] == call['providerReceipt']['costUSD']
        current = sent['messages'][-1]['content']
        images = [block for block in current if block['type'] == 'image_url']
        readable_images = [block for block in call['modelInput']['messages'][-1]['content'] if block['type'] == 'image_url']
        assert len(images) == len(readable_images)
        for a, b in zip(images, readable_images):
            rawimage = base64.b64decode(a['image_url']['url'].split(',', 1)[1])
            assert hashlib.sha256(rawimage).hexdigest() == b['image_url']['sha256']
            assert rawimage == (OUT / b['image_url']['url'].lstrip('/')).read_bytes()
            image_count += 1
        previous = calls[call['index']-2]['modelOutput']['tool'] if call['index'] > 1 else None
        assert bool(images) == (previous in ('observe', 'recall') and bool(
            calls[call['index']-2]['environmentOutput']['images']))
        public = json.loads(current[0]['text'])
        assert public['protocol'] == PROTOCOL and public['decision'] == call['index']
        assert not any(k in public for k in ('events', 'goal', 'initial', 'referenceActions', 'eventLedger', 'scheduledEvents'))
        assert 'eventLedger' not in raw.decode()
        if call['modelOutput']['tool'] == 'observe':
            observations += 1
            args = call['modelOutput']['args']
            if args['rotateDegrees'] == 90: rotated += 1
            result = call['environmentOutput']
            assert result['code'] == 'OBSERVED' and len(result['images']) == len(args['show'])
        elif call['modelOutput']['tool'] == 'attach':
            assert not call['environmentOutput'].get('images')
    with tempfile.TemporaryDirectory(prefix='brick-tool-arena-replay-') as tmp:
        replay = create(Path(tmp), 'scripted:api-replay')
        replay.autosave = False
        for env in record['records']:
            feedback = replay.submit(env['action'])
            actual = replay.records[-1]
            for key in ('before', 'afterOwnActionBeforeExternalChange', 'after', 'newEventIndices', 'feedback'):
                assert actual[key] == env[key], (env['decision'], key)
        assert replay.ep.state == record['final']
        replay.terminal = record['normalizedResult']['terminalStatus']
        result = replay.result()
        for key in ('success', 'stateMetrics', 'executionMetrics', 'eventWindows', 'appliedEvents', 'incidentExposure'):
            assert result[key] == record['normalizedResult'][key], key
    usage = spectator['usage']
    assert usage['calls'] == len(charges)
    assert abs(usage['costUSD'] - sum(c['actualUSD'] for c in charges)) < 1e-10
    report = dict(status='PASS', runId=runid, protocol=PROTOCOL, calls=len(calls),
        modelRequestedObservations=observations, modelRequested90DegreeRotations=rotated,
        verifiedSentImages=image_count, environmentEvents=len(record['eventLedger']),
        costUSD=usage['costUSD'], chargesSettled=True, exactProviderBodiesChecked=True,
        finalStateReplayed=True, privateEventLabelsAbsentFromModelInputs=True, paidCallsDuringAudit=0,
        scope='One API demo. Spectator views and private event records are excluded from the model input.')
    write_json(OUT / 'audit-tools.json', report)
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__': main()
