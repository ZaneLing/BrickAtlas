"""Exercise source banks through actual pull sensors/actions, without paid APIs."""
from pathlib import Path
from tempfile import TemporaryDirectory
import json
from dynamic_arena import OUT
from dynamic_arena.catalogue import entry
from dynamic_arena.run import open_session,NoProvider
from dynamic_arena.tool_arena import ToolArena,parse
from bench_design.session import scheduled_of
from expansion_v7.build import write


def main():
    catalogue=json.loads((OUT/'catalogue.json').read_text());chosen={}
    for r in catalogue['cases']:
        kind=r['caseId'].split(':')[0]
        if kind not in chosen and r['incidentBranch'] and not r['diagnostic']:chosen[kind]=r['caseId']
    results=[]
    with TemporaryDirectory(prefix='arena-migration-') as temp:
        for bank,cid in chosen.items():
            print('CHECK',bank,cid,flush=True)
            s=open_session(cid,Path(temp)/bank,'scripted:migration',False)
            n=open_session(cid,Path(temp)/(bank+'-normal'),'scripted:migration',True)
            assert n.initial==s.initial and n.goal==s.goal
            assert scheduled_of(n.ep)==0 and scheduled_of(s.ep)>0
            arena=ToolArena(s,NoProvider(),min(30,s.cap))
            provider,_,request,refs=arena.request();assert not refs
            assert cid not in json.dumps(request) and request['episode'].startswith('episode-')
            assert not any(k in request for k in ['events','goal','referenceActions','family','taskType'])
            before=dict(s.ep.state)
            out,images=arena.execute(dict(tool='observe',args=dict(view='angled',rotateDegrees=90,show=['current','target','inventory'],inventoryPage=arena.sensors.inventory_count)),1)
            assert out['code']=='OBSERVED' and s.ep.state==before and len(images)==3
            assert images[0]['width']==images[1]['width']==800 and images[0]['height']==images[1]['height']==600
            assert images[-1]['page']==arena.sensors.inventory_count
            h=request['actionHandles'][0]
            feedback,positions=arena.execute(dict(tool='inspect',args=dict(partId=h['id'],page=1)),2)
            assert feedback['code']=='OBSERVED' and positions and positions[0]['items']
            assert not positions[0]['legalityOrCorrectnessShown']
            if arena.sensors.manual_count:
                feedback,manual=arena.execute(dict(tool='inspect',args=dict(manualStep=1)),3)
                assert feedback['code']=='OBSERVED' and not manual[0]['isTarget']
            _,fresh=arena.execute(dict(tool='recall',args=dict(decision=1)),4)
            assert fresh==images
            results.append(dict(bank=bank,caseId=cid,normalSameTask=True,normalEvents=0,requestedViews=True,inventoryPages=arena.sensors.inventory_count,positionsVisible=True,manualSteps=arena.sensors.manual_count))
    write(OUT/'migration-sensor-check.json',dict(passed=True,checks=results,apiCalls=0,scope='Representative real case from every dynamic adapter; full catalogue metadata coverage is separate.'))
    print('PASS',len(results),'dynamic adapters',flush=True)


if __name__=='__main__':main()
