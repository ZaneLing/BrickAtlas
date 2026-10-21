"""Protocol gates: true empty start, exact replay, intervention accounting and no label leakage."""
from pathlib import Path
import json,sys
from copy import deepcopy
from protocol import Episode,load
from render import Renderer
from static_bench import Domain,exact_plan
OUT=Path(__file__).resolve().parents[3]/'deliverables/brickplan-api-pilot'

def build_plan(ep):
    state=ep.target;reverse=[]
    while any(state):
        options=[]
        for a,k in ep.domain.unpack(ep.case,state).items():
            if not k:continue
            after,code=ep.domain.transition(ep.case,state,{'type':'detach','partId':a})
            if code['code']=='OK':options.append((a,k,after))
        if not options:raise ValueError('No legal construction witness')
        a,k,state=options[0];reverse.append({'type':'attach','partId':a,'candidate':k})
    return list(reversed(reverse))

def public(ep,a):return {k:ep.alias[v] if k=='partId' else ep.pose(v) if k=='candidate' else v for k,v in a.items()}

def repair_witness(ep):
    # Guaranteed finite witness via legal complete disassembly and reassembly,
    # with shortest search when cheap. Neither witness is sent to models.
    case=deepcopy(ep.case);case['initial']=ep.assignments()
    try:return exact_plan(ep.domain,case,max_expansions=20000)[0]
    except ValueError:
        state=ep.state;result=[]
        while any(state):
            options=[]
            for a,k in ep.domain.unpack(ep.case,state).items():
                if not k:continue
                after,check=ep.domain.transition(ep.case,state,{'type':'detach','partId':a})
                if check['code']=='OK':options.append((a,after))
            if not options:raise ValueError('No recovery witness')
            a,state=options[0];result.append({'type':'detach','partId':a})
        return result+build_plan(ep)

if __name__=='__main__':
    rows=[]
    for model in ['v23-3223','v23-3223--deep']:
        cert,cs=load(model);c=next(c for c in cs.values() if c['kind']=='control')
        for event in ['none','remove','color','pose','closure']:
            ep=Episode(cert,c,'dynamic',event)
            assert all(k=='' for k in ep.assignments().values())
            assert all(v.get('virtual') for v in ep.cert['fixed'].values())
            assert not any(k in json.dumps(ep.observe('visual')) for k in ['expectedOptimum','oraclePlan',':goal',':color','wrong_color'])
            for a in build_plan(ep):
                result=ep.step(public(ep,a))
                if result['code']=='ENVIRONMENT_CHANGED':break
                assert result['code']=='OK',result
            injected=bool(ep.events)
            for a in repair_witness(ep):
                result=ep.step(public(ep,a));assert result['code'] in ('OK','ENVIRONMENT_CHANGED'),result
            ep.step({'type':'finish'});assert ep.success
            rows.append({'model':model,'event':event,'eventTriggered':injected,'success':ep.success,'actions':ep.manipulations})
    assert all(r['eventTriggered'] for r in rows if r['model']=='v23-3223' and r['event']!='none')
    # Preserve failures to trigger closure as unsupported scenarios, not fake perturbations.
    # Action assistance returns all and only legal operations, and cannot depend on the target.
    cert,cs=load('v23-3223');c=next(c for c in cs.values() if c['kind']=='control')
    ep=Episode(cert,c,'dynamic','color',action_mask=True)
    for a in build_plan(ep):
        assert public(ep,a) in ep.observe('symbolic')['legalActions']
        result=ep.step(public(ep,a))
        if result['code']=='ENVIRONMENT_CHANGED':break
    assert ep.events
    mask=ep.observe('visual')['legalActions'];old=ep.target;ep.target=tuple('' for _ in old)
    assert mask==ep.observe('visual')['legalActions'];ep.target=old
    before=ep.assignments().copy()
    for action in ({'type':'inspect','azimuth':75,'elevation':-30},{'type':'inspect','view':'bottom'},{'type':'inspect','partId':next(iter(ep.alias.values()))}):
        assert ep.step(action)['code']=='OBSERVATION_READY';assert ep.assignments()==before
    assert ep.step({'type':'inspect','azimuth':float('nan'),'elevation':0})['code']=='INVALID_CAMERA'
    report={'passed':True,'oracleRows':rows,'policy':'untriggered event is not counted as recovery','emptyStart':True,'goalLabelLeakage':False,'actionMaskTargetIndependent':True,'inspectNonmutating':True}
    (OUT/'protocol-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
