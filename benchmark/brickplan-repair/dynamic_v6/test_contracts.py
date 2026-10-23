"""Regression tests for actual failure modes: prefix identity, bad outputs, pagination and persistence."""
from pathlib import Path
from collections import Counter
import json,sys,tempfile,threading,urllib.request,urllib.error
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE.parent),str(HERE.parent/'eval')]
from dynamic_v6.episode import BANK,DynamicEpisode,load_case,branch_before_action
from dynamic_v6.interface import renderer_for,packet
from static_v4.certify import digest
from dynamic_v5.build import write
from expansion_v7.scope import allowed

def pub(ep,a):return dict(type=a['type'],partId=ep.alias[a['partId']],**({'candidate':ep.pose(a['candidate'])} if 'candidate' in a else {}))
def witness(mid):return json.loads((BANK/'models'/mid/'evidence.json').read_text())['buildWitness']

def episodes():
    cases=[c for c in json.loads((BANK/'cases.private.json').read_text())['cases'] if allowed(c)];chosen={}
    for mid in {c['modelId'] for c in cases}:
        cert=json.loads((BANK/'models'/mid/'qualification.json').read_text())
        counts=Counter(r['actor'] for r in cert['candidates'].values())
        assert len(set(counts.values()))==1,(mid,'catalog count reveals actor class')
    for c in cases:
        if c['track']=='complete-object':
            if c['kind']=='none':chosen.setdefault(c['modelId'],c)
            else:chosen.setdefault(c['kind'],c)
    for c in chosen.values():
        cert,_=load_case(c['id']);ep=DynamicEpisode(cert,c)
        for a in witness(c['modelId']):
            assert ep.submit({'action':pub(ep,a),'unexpectedChange':False})['code']=='OK'
            if ep.event:break
        if ep.event:
            for a in ep.event['recoveryWitness']:assert ep.submit({'action':pub(ep,a),'unexpectedChange':False})['code']=='OK'
        assert ep.submit({'action':{'type':'finish'},'unexpectedChange':False})['code']=='SUCCESS',c['id']
        assert ep.score()['invalidOutputs']==0
    print('episode replay variants',len(chosen),flush=True)
    c=next(c for c in cases if c['modelId']=='obj-city-car' and c['kind']=='extra_layer')
    cert,control_case=load_case(c['pairedGroup']+'--control');ep=DynamicEpisode(cert,control_case)
    plan=witness(c['modelId'])
    for a in plan[:c['trigger']-1]:ep.submit({'action':pub(ep,a),'unexpectedChange':False})
    control,event=branch_before_action(ep,c,pub(ep,plan[c['trigger']-1]))
    assert control.history==event.history and control.observe()==event.observe()
    assert control.state!=event.state and not control.event and event.event
    assert control.expected_after_last_action==event.expected_after_last_action
    assert event.export()['branchOrigin']['sharedPrefixHash']==ep.chain
    print('same-prefix branch and public-field isolation PASS',flush=True)
    # A free policy can assemble a different correct set before the trigger.
    # Compound faults must still have a certified live-generation path.
    c=next(c for c in cases if c['modelId']=='obj-table' and c['kind']=='compound_fault' and c['trigger']==3)
    cert,_=load_case(c['id']);ep=DynamicEpisode(cert,c);plan=witness(c['modelId'])
    for a in [plan[2],plan[3],plan[4]]:
        assert ep.submit({'action':pub(ep,a),'unexpectedChange':False})['code']=='OK'
    assert ep.event and ep.event['provenance']=='adaptive-certified'
    for a in ep.event['recoveryWitness']:assert ep.submit({'action':pub(ep,a),'unexpectedChange':False})['code']=='OK'
    assert ep.submit({'action':{'type':'finish'},'unexpectedChange':False})['code']=='SUCCESS'
    print('alternate build prefix with compound live recovery PASS',flush=True)
    cert,_=load_case(control_case['id'])
    ep=DynamicEpisode(cert,control_case);initial=ep.assignments()
    malformed=[{'type':'finish','actions':[{'type':'attach'}]},{'type':[]},{'type':'attach','partId':[]},['attach'],{'type':'attach','partId':'A01','candidate':[]},{'type':'detach','partId':'A01','candidate':'C001'}]
    for a in malformed:assert ep.step(a)['code']=='INVALID_ACTION' and ep.state==initial and not ep.finished
    assert ep.score()['invalidOutputs']==len(malformed)
    assert ep.submit({'action':{'type':'finish'},'actions':[{'type':'finish'}]})['code']=='INVALID_ACTION'
    assert not ep.finished and ep.state==initial
    ep.decision_budget=len(ep.records)+1;ep.step({'type':'inspect'})
    assert ep.finished and ep.budget_exhausted and not ep.success
    print('malformed output and decision-budget accounting PASS',flush=True)
    # Multi-page inventory and catalogs must survive the exact packet builder.
    c=next(c for c in cases if c['modelId']=='obj-ambulance' and c['kind']=='none');cert,_=load_case(c['id']);ep=DynamicEpisode(cert,c)
    actor=max(ep.actors,key=lambda a:len(ep.case['choices'][a]));renderer=renderer_for(ep)
    with tempfile.TemporaryDirectory() as temp:
        obs,ims=packet(ep,renderer,temp,dict(type='inspect',partId=ep.alias[actor]))
        assert all(h['candidates']==sorted(h['candidates']) for h in obs['actionHandles'])
        inv=[x for x in ims if x['role']=='inventory'];cat=[x for x in ims if x['role']=='candidate-catalog']
        assert len(inv)==(len(ep.actors)+11)//12 and len(inv)>1
        assert len(cat)==(len(ep.case['choices'][actor])+11)//12
        assert not any(x['role']=='target-inspection' for x in ims)
        assert {x['view'] for x in ims if x['role']=='current-target'}=={'isometric','top','rear'}
        assert not any(x['role']=='temporal-pair' for x in ims)  # no invented prior scene
        for i,key in enumerate(sorted(ep.case['choices'][actor],key=ep.pose)):
            page,pos=divmod(i,12);n=min(12,len(ep.case['choices'][actor])-page*12);row,col=divmod(pos,4)
            assert ep.catalog_click_candidate(dict(partId=ep.alias[actor],catalogPage=page+1,catalogPoint=[(col+.5)/4,(row+.5)/((n+3)//4)]))==key
    print('all inventory pages, all candidate cards and three views PASS',flush=True)
    return len(chosen)

def human():
    from dynamic_v6 import human_server as hs
    with tempfile.TemporaryDirectory() as temp:
        hs.OUT=Path(temp);server=hs.Server(('127.0.0.1',0));thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        base='http://127.0.0.1:'+str(server.server_port)
        def post(path,data):
            req=urllib.request.Request(base+path,data=json.dumps(data).encode(),headers={'Content-Type':'application/json'})
            try:
                with urllib.request.urlopen(req) as r:return r.status,json.load(r)
            except urllib.error.HTTPError as e:return e.code,json.load(e)
        try:
            _,first=post('/api/open',dict(reviewer='A',code='H001'))
            action=dict(type='inspect',partId=first['handles'][0]['id'])
            body=dict(reviewer='A',code='H001',revision=0,requestId='same-click',action=action,unexpectedChange=False)
            _,once=post('/api/step',body);_,twice=post('/api/step',body);assert once['revision']==twice['revision']==1
            status,stale=post('/api/step',{**body,'requestId':'stale-click'});assert status==409 and stale['revision']==1
            post('/api/open',dict(reviewer='A',code='H002'))
            _,back=post('/api/open',dict(reviewer='A',code='H001'));assert back['revision']==1
            _,other=post('/api/open',dict(reviewer='B',code='H001'));assert other['revision']==0
            server.sessions.clear()
            _,restored=post('/api/open',dict(reviewer='A',code='H001'));assert restored['revision']==1
            _,restarted=post('/api/open',dict(reviewer='A',code='H001',restart=True));assert restarted['revision']==0
            assert list((Path(temp)/'runs/archive').glob('A-H001-*.json'))
        finally:server.shutdown();server.server_close();thread.join()
    print('human switch/resume/restart, A/B independence, duplicate-click and stale-state PASS',flush=True)

if __name__=='__main__':
    count=episodes();human()
    write(BANK/'contract-tests.json',dict(status='PASS',episodeVariantsReplayed=count,samePrefixBranch=True,malformedOutputAccounting=True,allPagesAvailable=True,humanProgressPersisted=True,duplicateClicksIdempotent=True,staleStateRejected=True,reviewersIndependent=True))
