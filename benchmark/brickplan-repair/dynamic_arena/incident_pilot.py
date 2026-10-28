"""Run incident pilots only where the same model passed the normal prerequisite.

These are independent full episodes. They satisfy the prerequisite gate but
do not share an exact provider-context prefix, so causal recovery remains N/A.
"""
import json
import re
import time
from dynamic_arena import OUT
from dynamic_arena.demo import create
from dynamic_arena.tool_arena import ToolArena
from dynamic_arena.transport import Transport, write_json
from dynamic_arena.normal_pilot import LEDGER, REPORT
from bench_design.metrics import pair_metrics

DEST = OUT / 'incident-pilot-results.json'


def main():
    normal = json.loads(REPORT.read_text())['latestRuns']
    eligible = [x for x in normal if x['result']['terminalStatus'] == 'completed'
                and x['result']['success'] is True]
    old=json.loads(DEST.read_text())['runs'] if DEST.exists() else []
    done={(x['model'],x['objectId']) for x in old}
    for control in eligible:
        model,obj=control['model'],control['objectId']
        if (model,obj) in done:continue
        runid='incident-'+re.sub('[^a-z0-9]+','-',model.lower()).strip('-')+'-'+obj+'-'+time.strftime('%Y%m%d-%H%M%S')
        directory=OUT/'runs'/runid
        session=create(directory,model,events=True,model_id=obj)
        transport=Transport(directory,cap=3.0,model=model,ledger_path=LEDGER)
        result=ToolArena(session,transport,max_decisions=30).run()
        paired=pair_metrics(control['result'],result,shared_prefix_verified=False)
        item=dict(runId=runid,model=model,objectId=obj,normalRunId=control['runId'],
            normalSuccess=True,result=result,independentPrerequisiteComparison=paired)
        old.append(item);done.add((model,obj))
        ledger=json.loads(LEDGER.read_text())
        write_json(DEST,dict(schema='brick-atlas-incident-pilot/1',
            runs=old,matchedProviderPrefix=False,
            confirmedCostUSD=sum(c['actualUSD'] or 0 for c in ledger['charges']),
            chargedOrReservedUpperBoundUSD=sum(c['actualUSD'] if c['actualUSD'] is not None
                else c['reservedUSD'] for c in ledger['charges']),capUSD=ledger['capUSD'],
            note='Only normal-success model/object combinations were attempted. Independent controls do not qualify for causal recovery metrics.'))
        print(json.dumps(dict(runId=runid,model=model,object=obj,
            terminal=result['terminalStatus'],success=result['success'],
            appliedEvents=result['appliedEvents'],incidentExposure=result['incidentExposure'],
            fullPlacementF1=result['stateMetrics']['fullPlacement']['f1'],
            costUSD=result['providerUsage']['costUSD']),ensure_ascii=False),flush=True)


if __name__=='__main__':main()
