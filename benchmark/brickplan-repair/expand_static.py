"""Build larger source-derived static challenge structures, without a simulator."""
from copy import deepcopy
import argparse
import json
import sys
from itertools import combinations
import numpy as np
from library import (Qualifier, read_source, select_cluster, qualify_candidates,
                     substitute, OUT, ROOT)
from static_bench import (Domain, TYPES, annotate_static, curate_model, aggregate,
                          digest, dump, groups_for, make_case, part_name)


def build(source_id, maximum=16):
    model=source_id+'--deep'
    base=json.loads((OUT/'archive/before-static-v2/models'/source_id/'qualification.json').read_text())
    base_record=json.loads((OUT/'models'/source_id/'record.json').read_text())
    manifest,parts,adjacency,source=read_source(source_id)
    print('EXPAND',source_id,len(parts),flush=True)
    q=Qualifier();cert=select_cluster(parts,adjacency,q,max_parts=maximum,prefer_complex=True)
    goals={r['actor']:k for k,r in cert['candidates'].items()}
    if len(goals)+1 <= base_record['caseParts']:
        raise ValueError('No larger connected structure found')
    cert.update(modelId=model,source=source)
    source['includedSourceIndices']=sorted([p['sourceIndex'] for p in cert['fixed'].values()]+[r['part']['sourceIndex'] for r in cert['candidates'].values()])
    source_to_actor={r['part']['sourceIndex']:r['actor'] for r in cert['candidates'].values()}
    # Carry over actual admitted alternatives for source pieces still present.
    for key,row in base['candidates'].items():
        if row['kind']=='goal':continue
        p=row['part'];index=p.get('derivedFromSourceIndex',p.get('sourceIndex'))
        if index not in source_to_actor:continue
        target=source_to_actor[index]
        actor=target if p.get('sourceIndex') is not None else row['actor'][0]+target[1:]
        new_key=actor+':'+key.split(':',1)[1]
        cert['candidates'][new_key]=dict(actor=actor,kind=row['kind'],label=row['label'],part=deepcopy(p))
    for actor,key in goals.items():
        p=cert['candidates'][key]['part'];spare='W'+actor[1:]
        color=('1','#0055BF') if p['colorHex'].lower()!='#0055bf' else ('4','#C91A09')
        cert['candidates'][spare+':color']=dict(actor=spare,kind='wrong_color',label='错色替件',part=substitute(p,p['partNumber'],color))
    # Position exchanges are relational faults. Identical-looking permutations are excluded.
    pairs=list(combinations(goals,2))
    pairs.sort(key=lambda ab: (cert['candidates'][goals[ab[0]]]['part']['canonical']!=cert['candidates'][goals[ab[1]]]['part']['canonical'],ab))
    swapped=[]
    for a,b in pairs:
        pa,pb=cert['candidates'][goals[a]]['part'],cert['candidates'][goals[b]]['part']
        if pa['canonical']==pb['canonical'] and pa['colorHex'].lower()==pb['colorHex'].lower():continue
        # Same shape, differently colored source pieces are guaranteed visually distinct;
        # dissimilar shapes also go through the same endpoint/connection admission.
        if len(swapped)>=4:break
        entries={}
        for actor,partner,p,target in ((a,b,pa,pb),(b,a,pb,pa)):
            alt=deepcopy(p);raw=np.asarray(target['rawMatrix'])
            alt['matrix']=(raw @ np.linalg.inv(np.asarray(p['rawMatrix'])) @ np.asarray(p['matrix'])).tolist()
            alt['rawMatrix']=raw.tolist();alt['direction']=target['direction'];alt['swapPartner']=partner
            key=f'{actor}:swap-{partner}'
            entries[key]=dict(actor=actor,kind='swapped_positions',label=f'放错到 {partner} 的位置',part=alt)
        original=deepcopy(cert['candidates']);cert['candidates'].update(entries)
        qualify_candidates(cert,q)
        edits={a:f'{a}:swap-{b}',b:f'{b}:swap-{a}'}
        try:
            case=make_case(cert,model,edits,groups_for(cert,edits));annotate_static(case,Domain(cert,{}))
            swapped.append(edits)
        except ValueError:cert['candidates']=original
        if len(swapped)==0 and pairs.index((a,b))>=12:break
    qualify_candidates(cert,q);domain=Domain(cert,{})
    cases=[]
    proposals=[{}]+[{a:''} for a in goals]
    for key,row in cert['candidates'].items():
        actor=row['actor']
        if row['kind'] in ('goal','swapped_positions','extra'):continue
        if actor in goals:
            if row['kind']=='height_layer':
                extra='E'+actor[1:]+':extra'
                if extra in cert['candidates']:proposals.append({actor:key,extra.split(':')[0]:extra})
            else:proposals.append({actor:key})
        else:
            target=source_to_actor[row['part']['derivedFromSourceIndex']]
            proposals.append({target:'',actor:key})
    proposals.extend(swapped)
    for edits in proposals:
        try:
            c=annotate_static(make_case(cert,model,edits,groups_for(cert,edits)),domain)
            cases.append(c)
        except ValueError as exc:print('REJECT',model,edits,str(exc),flush=True)
    cert['contentSha256']=digest(cert)
    folder=OUT/'models'/model
    record=dict(modelId=model,title=base_record['title']+' · 深层相连结构',status='ready',
                sourceModelId=source_id,structureVariant='expanded-connected-source',
                originalParts=len(manifest['instances']),caseParts=len(goals)+len(cert['fixed']),
                mutableParts=len(goals),fixedParts=len(cert['fixed']),sourceIndices=source['includedSourceIndices'],
                sourceNotes=source['fullModelFidelityNotes'],source=source,
                targetProvenance=base_record['targetProvenance'],qualificationSha256=cert['contentSha256'])
    dump(folder/'qualification.json',cert);dump(folder/'record.json',record);dump(folder/'cases.json',{c['id']:c for c in cases})
    dump(folder/'static-proposals.json',{c['id']:c for c in cases})
    result=curate_model(folder,pair_budget=56)
    print('EXPANDED',model,result['caseParts'],'parts',result['caseCount'],'cases',flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--model',action='append',required=True);p.add_argument('--parts',type=int,default=16)
    args=p.parse_args()
    for source in args.model:
        try:build(source,args.parts)
        except Exception:
            import traceback;traceback.print_exc()
    aggregate()
