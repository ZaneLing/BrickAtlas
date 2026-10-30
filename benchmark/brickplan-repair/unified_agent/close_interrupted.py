"""Close the interrupted diagnostic run from stored actions, with no API calls."""
import gzip,json,tempfile
from copy import deepcopy
from dynamic_arena import OUT as ARENA_OUT
from dynamic_arena.run import open_session
from dynamic_arena.transport import write_json
from unified_agent import OUT,PROTOCOL


def main():
    stop=json.loads((OUT/'checks/stopped-for-scorer-review.json').read_text())
    folder=ARENA_OUT/'runs'/stop['run']
    record=json.load(gzip.open(folder/'record.private.json.gz'))
    spectator=json.loads((folder/'spectator.json').read_text())
    calls=spectator['calls'];assert len(calls)==stop['completedCalls']==len(record['records'])
    with tempfile.TemporaryDirectory() as tmp:
        session=open_session(spectator['caseId'],tmp,'scripted:offline-close',True);session.autosave=False
        for row in record['records']:
            feedback=session.submit(row['action'],parse_error=row.get('parseError',False))
            assert session.ep.state==row['after'] and feedback['code']==row['feedback']['code']
        session.terminal='external_stop';result=session.result()
    profile=spectator['agentProfile']
    result.update(actor=spectator['model'],model=spectator['model'],arenaRunId=stop['run'],arenaBranch='normal',
        inputVersion=PROTOCOL,arenaProtocol=PROTOCOL,experimentArm='dynamic-visual-agent',agentProfile=profile,
        agentMemory=spectator['agentMemory'],providerUsage=spectator['usage'],apiCalls=len(calls),
        repairPrerequisite=None,normalQualifiedRecovery=None,
        externalStop=dict(reason=stop['reason'],betweenCalls=True,offlineStateReplayIdentical=True,extraApiCalls=0),
        controllerMetrics=dict(decisions=len(calls),actionAttempts=sum(c['modelOutput']['tool'] in ('attach','detach') for c in calls),
            observationRequests=sum(c['modelOutput']['tool'] in ('observe','inspect','recall') for c in calls),
            observeCalls=sum(c['modelOutput']['tool']=='observe' for c in calls),
            inspectCalls=sum(c['modelOutput']['tool']=='inspect' for c in calls),
            recallCalls=sum(c['modelOutput']['tool']=='recall' for c in calls),
            formatErrors=sum(c['modelOutput']['tool']=='invalid' for c in calls),
            actionBudget=profile['maxActions'],observationBudget=profile['maxObservations'],budget=profile['maxDecisions']),
        inputMetrics=dict(imageCounts=[len(c['inputImageHashes']) for c in calls],
            totalImages=sum(len(c['inputImageHashes']) for c in calls),
            maxImagesPerRequest=max(len(c['inputImageHashes']) for c in calls),
            imagePixels=sum(c['inputImagePixels'] for c in calls),serializedRequestBytes=sum(c['requestBytes'] for c in calls),
            configuredTwoImageLimit=False,initialImages=len(spectator['initialImages'])))
    assert result['success'] is None
    if not (folder/'spectator.before-close.json').exists():write_json(folder/'spectator.before-close.json',deepcopy(spectator))
    spectator.update(phase='finished',result=result)
    write_json(folder/'result.json',result);write_json(folder/'spectator.json',spectator)
    write_json(folder/'log.json',dict(protocol=PROTOCOL,profile=profile,initialImages=spectator['initialImages'],calls=calls,result=result))
    report=json.loads((OUT/'pilot.json').read_text())
    if not any(r['arenaRunId']==stop['run'] for r in report['runs']):report['runs'].append(result)
    write_json(OUT/'pilot.json',report)
    print('Closed interrupted run; success=null, 8 prior calls, 0 new calls.')


if __name__=='__main__':main()
