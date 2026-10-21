"""Exercise the real paired runner with local scripted replies; never calls an API."""
from pathlib import Path
import json,sys,tempfile
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE.parent),str(HERE.parent/'eval')]
from dynamic_v6 import run_paired as runner
from dynamic_v6.episode import BANK,DynamicEpisode,load_case
from dynamic_v6.test_contracts import pub,witness
from dynamic_v5.build import write

def main():
    cid='obj-city-car--t3--extra_layer--v01';cert,case=load_case(cid)
    ep=DynamicEpisode(cert,case);plan=witness(case['modelId']);at=case['trigger']
    moves=[(pub(ep,a),False) for a in plan[:at]]
    moves += [(pub(ep,a),False) for a in plan[at:]]+[({'type':'finish'},False)]
    moves += [(pub(ep,a),i==0) for i,a in enumerate(case['privateEvent']['recoveryWitness'])]+[({'type':'finish'},False)]
    seq=iter(moves);calls=[]
    assert runner.parse('{"action":{"type":"finish"},"actions":[]}')[0]['type']=='invalid'
    def fake_call(payload):
        assert payload['model']=='scripted-contract-only'
        observation=json.loads(payload['messages'][-1]['content'][0]['text'])
        for k in ('caseId','kind','trigger','privateEvent','current','target','buildGuide','legalActions'):assert k not in observation
        action,judgment=next(seq);calls.append(payload['seed'])
        return dict(content=json.dumps(dict(action=action,unexpectedChange=judgment)),cost=0,model='scripted-contract-only')
    oldcall,oldbank=runner.call,runner.BANK
    try:
        with tempfile.TemporaryDirectory() as temp:
            runner.call=fake_call;runner.BANK=Path(temp)
            (runner.BANK/'audit.json').write_bytes((BANK/'audit.json').read_bytes())
            result=runner.run(cid,'scripted-contract-only',execute=True,max_cost=1)
            assert result['status']=='complete',result
            a=result['attribution'];assert a['controlSuccess'] and a['interventionSuccess'] and a['eventTriggered']
            assert a['declaredAtEvent'] is True and a['detectionPairMachineEligible']
            assert result['branchStateVerified'] and result['requests']==len(moves)==len(calls)
            assert result['costUSD']==0 and not a['paperDetectionClaimEligible']
            trace=json.loads(next((runner.BANK/'pilot-v6').rglob('trace.json')).read_text())
            assert trace['branches']['control']['steps'][0]['priorDialogueSha256']==trace['branches']['intervention']['steps'][0]['priorDialogueSha256']
            assert trace['branches']['intervention']['episode']['event']['provenance']=='precertified'
            initial=json.loads(next((runner.BANK/'pilot-v6').rglob('initial-input.json')).read_text())
            assert len([i for i in initial['images'] if i['role']=='temporal-pair'])==3
    finally:runner.call=oldcall;runner.BANK=oldbank
    report=dict(status='PASS',testType='local scripted replies, not model performance',realPaidRequests=0,scriptedDecisions=len(calls),
                sharedPrefix=True,identicalBranchDialogue=True,controlAndRecoveryCompleted=True,eventJudgmentAligned=True,strictSingleAction=True,privateInputFieldsAbsent=True)
    write(BANK/'runner-contract.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
