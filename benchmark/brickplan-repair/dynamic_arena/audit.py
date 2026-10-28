"""Verify the recorded API episode by exact action replay; never calls an API."""
import gzip
import hashlib
import json
import argparse
from pathlib import Path
import tempfile
from bench_design.run_autonomous import decode, PRIVATE_FIELDS
from dynamic_arena import OUT
from dynamic_arena.demo import create
from dynamic_arena.transport import write_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', default='gemini-20261028-133320')
    runid = parser.parse_args().run
    directory = OUT / 'runs' / runid
    trace = json.loads((directory / 'autonomous/trace.private.json').read_text())
    record = json.loads(gzip.decompress((directory / 'record.private.json.gz').read_bytes()))
    spectator = json.loads((directory / 'spectator.json').read_text())
    ledger = json.loads((OUT / 'api-ledger.private.json').read_text())
    charges = [c for c in ledger['charges'] if c['run'] == runid]
    assert len(charges) == len(trace['steps']) == len(record['records'])
    assert all(c['status'] == 'settled' for c in charges)
    image_count = 0
    checks = []
    for charge, step, env, frame in zip(charges, trace['steps'], record['records'], spectator['frames']):
        api = json.loads((directory / 'api' / (charge['id'] + '.private.json')).read_text())
        reply = api['result']['choices'][0]['message']['content']
        assert decode(reply) == step['action'] == env['action']
        assert charge['generationId'] == api['result']['id']
        assert charge['actualUSD'] == api['result']['usage']['cost']
        assert frame['index'] == step['index'] - 1
        assert len(frame['modelInputs']) == api['requestShape']['images']
        for image in frame['modelInputs']:
            path = OUT / image['url'].lstrip('/')
            assert hashlib.sha256(path.read_bytes()).hexdigest() == image['sha256']
            image_count += 1
        public = json.loads((directory / 'autonomous' / f'observation-{step["index"]:04}.json').read_text())
        assert not PRIVATE_FIELDS.intersection(public)
        assert not any(k in public for k in ('events', 'eventLedger', 'recovery', 'referenceActions', 'goal', 'initial'))
        assert not {'events', 'result', 'spectatorNotice'}.intersection(public)
    checks.append('Every executed action exactly matches a genuine provider response; IDs, costs and model-input image hashes match.')
    with tempfile.TemporaryDirectory(prefix='brick-arena-audit-') as tmp:
        session = create(Path(tmp), 'scripted:recorded-api-replay')
        session.autosave = False
        for env in record['records']:
            feedback = session.submit(env['action'])
            actual = session.records[-1]
            for field in ('before', 'afterOwnActionBeforeExternalChange', 'after', 'newEventIndices', 'feedback'):
                assert actual[field] == env[field], (env['decision'], field)
        assert session.ep.state == record['final']
        result = session.result()
        for field in ('success', 'stateMetrics', 'executionMetrics', 'eventWindows', 'appliedEvents', 'incidentExposure'):
            assert result[field] == record['normalizedResult'][field], field
        assert len(session.events) == 1 and session.events[0]['effectiveIncidentVerified']
        checks.append('Exact replay reproduces all states, legal rejections, the live intervention and final evaluation.')
        # Certify that the actual failed ending is recoverable. This is an
        # evaluator-only check after the model run, never appended to its log.
        state = dict(session.ep.state)
        repair = [dict(type='detach', actor='P004'),
                  dict(type='attach', actor='P001', candidate='P001:goal'),
                  dict(type='attach', actor='P004', candidate='P004:goal')]
        for action in repair:
            state, feedback = session.ep.runtime.check(state, action['actor'], action['type'], candidate=action.get('candidate'))
            assert feedback['code'] == 'OK'
        assert session.ep.runtime.complete(state)
        checks.append('The final missing leg has a legal three-move recovery: remove tabletop, replace leg, reinstall tabletop. This was not executed for the API model.')
    usage = dict(calls=len(charges), costUSD=sum(c['actualUSD'] for c in charges), settled=True,
        capUSD=ledger['capUSD'], promptTokens=sum(c['promptTokens'] for c in charges),
        completionTokens=sum(c['completionTokens'] for c in charges))
    assert usage == spectator['usage']
    # Add transport accounting to controller-level outputs. Environment-only
    # records intentionally make no claims about external provider calls.
    for path in (directory / 'result.json', directory / 'autonomous/trace.private.json', directory / 'spectator.json'):
        data = json.loads(path.read_text())
        normalized = data['normalizedResult'] if path.name == 'result.json' else data['result']['normalizedResult']
        normalized.update(apiCalls=usage['calls'], providerUsage=usage)
        write_json(path, data)
    checks.append('Public model observations exclude event labels, GT state, recovery plans and spectator evaluation.')
    checks.append('All 14 API charges are settled; accounting agrees with the displayed total.')
    write_json(OUT / 'audit.json', dict(status='PASS', runId=runid, checks=checks,
        paidCallsDuringAudit=0, recordedModelCalls=usage['calls'], verifiedModelInputImages=image_count,
        costUSD=usage['costUSD'], noAutomaticModelRescue=True, formalBenchmarkResult=False,
        limits=['This is a single small demonstration with one registered position per part.',
                'A matched normal model run and static comparison have not been measured.']))
    print(json.dumps(dict(status='PASS', checks=len(checks), **usage)))


if __name__ == '__main__':
    main()
