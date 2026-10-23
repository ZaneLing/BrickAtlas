"""Admit only source-preserving modules with a checked serial build witness."""
from copy import deepcopy
import json
import time
import numpy as np
from expansion_v7 import ROOT, OUT
from expansion_v7.runtime import runtime, execute, move
from expansion_v7.designs import designs, certificate
from community_modules.core import source_certificate, ModuleAssembly, dump
from community_modules.specs import SPECS
from geometry import load_source


def find_order(rt):
    state = dict(rt.goal)
    if not rt.anchored(state):
        return None
    removed = []
    while any(state.values()):
        choices = sorted((a for a,k in state.items() if k),
            key=lambda a: (rt.row(state[a])['part']['rawMatrix'][1][3], a))
        for actor in choices:
            after, _ = execute(rt, state, [move(actor)])
            if after is not None:
                removed.append(move(actor, state[actor])); state = after
                break
        else:
            return None
    actions = list(reversed(removed))
    end, evidence = execute(rt, state, actions)
    if end is None or not rt.complete(end):
        return None
    return actions


def record(cert, actions, title, track, new_source=False):
    directory = OUT/'prepared'/cert['id'];directory.mkdir(parents=True,exist_ok=True)
    dump(directory/'base-certificate.private.json', cert)
    dump(directory/'base-manual.private.json', dict(actions=actions))
    meta=dict(id=cert['id'],title=title,track=track,activeParts=len(actions),newSource=new_source,
              sourceSetId=cert['source'].get('sourceSetId',cert['source'].get('modelId')))
    dump(directory/'metadata.json',meta)
    print('ADMITTED',cert['id'],len(actions),track,flush=True)
    return meta


def discover(spec, target=20, minimum=14):
    mf=json.loads((ROOT/'web/public/models'/spec['model']/'manifest.json').read_text())
    seed=set(spec['indices'])
    matrices=[np.asarray(mf['instances'][i]['originalMatrix']).reshape(4,4).T for i in seed]
    center=np.median([m[:3,3] for m in matrices],axis=0)
    # Distance is used only for choosing a coherent author-time local module;
    # admitted geometry and source parts remain exact and all context is kept.
    ranked=sorted(range(len(mf['instances'])),key=lambda i:
        np.linalg.norm(np.asarray(mf['instances'][i]['originalMatrix']).reshape(4,4).T[:3,3]-center))
    eligible=[]
    for i in ranked:
        try:
            load_source(spec['model'],[i])
        except Exception:
            continue
        eligible.append(i)
        if len(eligible)>=target+12:
            break
    selected=list(dict.fromkeys([*spec['indices'],*eligible]))
    for n in (target,target-2,16,14):
        if len(selected)<n:continue
        proposed={**spec,'id':spec['id']+'-long','indices':selected[:n]}
        candidate=source_certificate(proposed)
        actions=find_order(ModuleAssembly(candidate))
        if actions:
            candidate['source'].update(moduleSourceIndices=[int(a['actor'][1:]) for a in actions],
                sourceSetId=spec['model'],longProcess=True)
            return candidate,actions
    # Start with the full original scene locked. Promote one source brick at a
    # time, remove it legally, and reverse the removal sequence into a manual.
    # This avoids selecting buried bricks while leaving their covers locked.
    trial_spec={**spec,'id':spec['id']+'-long','indices':[]}
    cert=source_certificate(trial_spec);shared=ModuleAssembly(cert).q
    removed=[];remaining=set(eligible)
    while remaining and len(removed)<target:
        advanced=False
        for index in eligible:
            if index not in remaining:continue
            fixed='F'+str(index);actor='P'+str(index);key=actor+':goal'
            if fixed not in cert['fixed']:
                remaining.remove(index);continue
            row=dict(actor=actor,kind='goal',part=cert['fixed'][fixed])
            trial={**cert,'fixed':{a:p for a,p in cert['fixed'].items() if a!=fixed},
                   'candidates':{**cert['candidates'],key:row}}
            rt=ModuleAssembly(trial);rt.q=shared
            state={a:'' for a in rt.actors};state[actor]=key
            if not rt.anchored(state):continue
            after,_=execute(rt,state,[move(actor)])
            if after is None:continue
            restored,_=execute(rt,after,[move(actor,key)])
            if restored!=state:continue
            cert=trial;removed.append(move(actor,key));remaining.remove(index);advanced=True
            break
        if not advanced:break
    if len(removed)<minimum:return None
    actions=list(reversed(removed));rt=ModuleAssembly(cert);rt.q=shared
    end,_=execute(rt,{a:'' for a in rt.actors},actions)
    if end is None or not rt.complete(end):return None
    cert['source']['moduleSourceIndices']=[int(a['actor'][1:]) for a in actions]
    cert['source']['sourceSetId']=spec['model']
    cert['source']['longProcess']=len(actions)>=14
    return cert,actions


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    rows=[];rejections=[]
    for key,spec in designs().items():
        cert=certificate(key,spec);actions=find_order(runtime(cert))
        if not actions:
            rejections.append(dict(id=cert['id'],reason='No legal greedy build witness'));continue
        rows.append(record(cert,actions,spec['name'],'D-long',True))
    for spec in SPECS:
        base=ROOT/'deliverables/brickplan-community-modules'/spec['id']
        cert=json.loads((base/'certificate.private.json').read_text())
        actions=json.loads((base/'manual.private.json').read_text())['actions']
        cert['source']['sourceSetId']=spec['model']
        rows.append(record(cert,actions,spec['title'],'M-expanded'))
    for key in ('cottage-roof','racer-top','seaplane-tail','museum-roof'):
        spec=next(s for s in SPECS if s['id']==key)
        print('DISCOVER_LONG',key,flush=True)
        found=discover(spec,20)
        if found:
            cert,actions=found
            rows.append(record(cert,actions,spec['title']+'：扩大操作模块','M-long'))
        else:
            rejections.append(dict(id=key+'-long',reason='No source-preserving serial module found in search'))
    new_sources=[('10002-1','铁路俱乐部车厢'),('10015-1','绿色客运车厢'),
                 ('10016-1','铁路罐车'),('10013-1','敞篷货运车厢')]
    for number,title in new_sources:
        model='v7-omr-'+number
        path=ROOT/'web/public/models'/model/'manifest.json'
        if not path.exists():
            continue
        mf=json.loads(path.read_text())
        candidates=[]
        for i in range(len(mf['instances'])):
            if 'minifig' in mf['instances'][i]['sourceFile']:continue
            try:part=load_source(model,[i])[0][0]
            except Exception:continue
            candidates.append((part['rawMatrix'][1][3],i))
        indices=[i for _,i in sorted(candidates)[:3]]
        spec=dict(id='new-'+number,model=model,indices=indices,author=mf['model']['author'],
                  url=mf['model']['sourceUrl'],original=mf['sourceFile'])
        print('DISCOVER_SOURCE',number,flush=True)
        found=discover(spec,20,minimum=5)
        if found:
            cert,actions=found
            cert['id']='new-'+number
            cert['source']['newSource']=True
            rows.append(record(cert,actions,title+'：局部补装','M-new-source',True))
        else:
            rejections.append(dict(id='new-'+number,reason='No qualified local module found'))
    dump(OUT/'prepared/index.json',rows)
    dump(OUT/'source-admission.json',dict(admitted=rows,rejected=rejections,
        sourcePartsMovedForAdmission=0,humanValidation=False))


if __name__=='__main__':main()
