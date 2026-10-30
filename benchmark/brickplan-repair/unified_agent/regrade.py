"""Replay stored physical actions under the corrected scorer; no model calls."""
import gzip,json,tempfile,time
from pathlib import Path
from copy import deepcopy
from dynamic_arena import OUT as ARENA_OUT
from dynamic_arena.run import open_session
from dynamic_arena.transport import write_json
from unified_agent import OUT
from unified_agent.providers import LEDGER,total


def main():
    report=json.loads((OUT/'pilot.json').read_text())
    before=OUT/'checks/pilot-before-scorer-fix.json'
    if not before.exists():write_json(before,report)
    changes=[]
    for result in report['runs']:
        folder=ARENA_OUT/'runs'/result['arenaRunId']
        record=json.load(gzip.open(folder/'record.private.json.gz'))
        with tempfile.TemporaryDirectory() as tmp:
            s=open_session(result['caseId'],tmp,'scripted:regrade',result['arenaBranch']=='normal');s.autosave=False
            for r in record['records']:
                feedback=s.submit(r['action'],parse_error=r.get('parseError',False))
                if s.ep.state!=r['after']:raise ValueError('Replayed physical state changed')
                if feedback['code']!=r['feedback']['code']:raise ValueError('Replayed action feedback changed')
            s.terminal=result['terminalStatus'];updated=s.result()
            original=deepcopy(result)
            for k in ['success','stateMetrics','executionMetrics','eventWindows','allIncidentCompletion','allWindowsRecovered','repairApplicable']:
                result[k]=updated[k]
            result['evaluationRevision']=dict(scorer='connector-workbench/5',reason='3023 plain plate resolves to canonical 3023b; preserve half-turn symmetry',physicalReplayIdentical=True,apiRerun=False)
            if not (folder/'result.before-scorer-fix.json').exists():write_json(folder/'result.before-scorer-fix.json',original)
            for name in ['result.json','log.json','spectator.json']:
                path=folder/name;value=result if name=='result.json' else json.loads(path.read_text())
                if name!='result.json':value['result']=result
                write_json(path,value)
            changes.append(dict(runId=result['arenaRunId'],beforeSuccess=original['success'],afterSuccess=result['success'],
                beforeF1=original['stateMetrics']['fullPlacement']['f1'],afterF1=result['stateMetrics']['fullPlacement']['f1']))
    report['scorerCorrection']=changes
    # A corrected normal pass is no longer classified as a failed prerequisite.
    successful={(r['caseId'],r['model']) for r in report['runs'] if r['arenaBranch']=='normal' and r['success']}
    report['notRun']=[r for r in report.get('notRun',[]) if (r['caseId'],r['model']) not in successful]
    report['stoppedForScorerReview']=json.loads((OUT/'checks/stopped-for-scorer-review.json').read_text())
    report['finishedAt']=time.time()
    write_json(OUT/'pilot.json',report)
    write_json(OUT/'checks/regrade.json',dict(apiCalls=0,physicalReplayIdentical=True,runs=changes))
    print(json.dumps(changes,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
