"""Expand complete objects with multiple timings, distinct fault locations and compound faults."""
from collections import Counter,defaultdict
from copy import deepcopy
from pathlib import Path
import json,sys,shutil,argparse,hashlib
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE.parent),str(HERE.parent/'eval')]
from dynamic_v6 import VERSION
from dynamic_v6.object_models import OBJECTS,certificate
from dynamic_v5.build import write,perform,replay,add_swaps,add_extra,add_variants,candidates as old_candidates
from static_v4.certify import digest
from static_v4.metrics import residual
from baseplate import PlateAssembly,PROTOCOL
OUT=HERE.parents[2]/'deliverables/brickplan-dynamic-v6'
OLD=HERE.parents[2]/'deliverables/brickplan-dynamic-v5'

def augmented(source):
    source=deepcopy(source)
    for actor,p in source['fixed'].items():
        source['candidates'][actor+':goal']=dict(actor=actor,kind='goal',label='part',part=deepcopy(p),support=[],pathBlocked=[])
    cert=add_variants(source)
    for key,row in list(cert['candidates'].items()):
        if row['kind']!='goal':continue
        actor=row['actor'];p=row['part'];stem=p['canonical']
        color=deepcopy(p);color['derivedFromSourceIndex']=p['sourceIndex']
        color['colorHex']='#c91a09' if p['colorHex'].lower() not in ('#c91a09','#f57d20') else '#0055bf'
        cert['candidates']['W'+actor+':color']=dict(actor='W'+actor,kind='wrong_color',part=color,label='available part',support=[],pathBlocked=[])
        replacement={'3010':'3004','3004':'3010','3020':'3022','3034':'3020','3039':'3004'}.get(stem)
        if replacement:
            wrong=deepcopy(p);wrong['derivedFromSourceIndex']=p['sourceIndex'];wrong['canonical']=wrong['partNumber']=replacement
            cert['candidates']['T'+actor+':type']=dict(actor='T'+actor,kind='wrong_type',part=wrong,label='available part',support=[],pathBlocked=[])
        if stem not in ('3005','3022','3024','3031'):
            turn=deepcopy(p);rot=np.asarray([[0,0,1,0],[0,1,0,0],[-1,0,0,0],[0,0,0,1]])
            for field in ('rawMatrix','matrix'):turn[field]=(np.asarray(turn[field])@rot).tolist()
            cert['candidates'][actor+':quarter_turn']=dict(actor=actor,kind='rotation',part=turn,label='grid placement',support=[],pathBlocked=[])
            # An even-by-odd footprint rotated around its geometric center
            # falls between studs. Register rotations about a stud instead.
            if stem in ('3004','3010'):
                for dx,dz in ((10,10),(10,-10),(-10,10),(-10,-10)):
                    pivot=deepcopy(turn)
                    for field in ('rawMatrix','matrix'):
                        offset=np.asarray(p[field])[:3,:3]@np.array([dx,0,dz])
                        for axis in range(3):pivot[field][axis][3]+=float(offset[axis])
                    cert['candidates'][f'{actor}:turn-stud-{dx}-{dz}']=dict(actor=actor,kind='rotation',part=pivot,label='grid placement',support=[],pathBlocked=[])
    add_swaps(cert)
    goals=[r for r in cert['candidates'].values() if r['kind']=='goal']
    for a in goals:
        for b in goals:
            if a['actor']==b['actor'] or (a['part']['canonical'],a['part']['colorHex'])==(b['part']['canonical'],b['part']['colorHex']):continue
            p=deepcopy(a['part'])
            for field in ('rawMatrix','matrix'):p[field]=deepcopy(b['part'][field])
            cert['candidates'][a['actor']+':swap-'+b['actor']]=dict(actor=a['actor'],kind='swap',part=p,label='grid placement',support=[],pathBlocked=[])
    cert['contentSha256']=digest({k:v for k,v in cert.items() if k!='contentSha256'})
    return cert

def event_candidates(rt,prefix,suffix,installed_order=None):
    rows=list(old_candidates(rt,prefix,suffix))
    installed=[a for a,k in prefix.items() if k and rt.goal.get(a)]
    for i,a in enumerate(installed):
        for b in installed[i+1:]:
            ka,kb=a+':swap-'+b,b+':swap-'+a
            if ka not in rt.candidates or kb not in rt.candidates:continue
            change=[dict(type='detach',partId=a),dict(type='detach',partId=b),dict(type='attach',partId=a,candidate=ka),dict(type='attach',partId=b,candidate=kb)]
            restore=[dict(type='detach',partId=a),dict(type='detach',partId=b),dict(type='attach',partId=a,candidate=prefix[a]),dict(type='attach',partId=b,candidate=prefix[b])]
            rows.append(('swapped_positions',change,restore))
    # Every registered extra location is retained; later timings cannot overwrite earlier ones.
    for key,row in rt.candidates.items():
        if key.startswith('X001:extra-t'):
            rows.append(('extra_layer',[dict(type='attach',partId='X001',candidate=key)],[dict(type='detach',partId='X001')]))
    # A wrong part hidden below an already-correct cover requires temporarily
    # removing correct geometry. The cover is restored in the event itself.
    order=installed_order or [a for a,k in prefix.items() if k]
    for actor in order:
        if not prefix.get(actor) or perform(rt,prefix,dict(type='detach',partId=actor)) is not None:continue
        wrong=next((k for k,r in rt.candidates.items() if r['kind']=='wrong_color' and r['part'].get('derivedFromSourceIndex')==rt.row(prefix[actor])['part'].get('sourceIndex')),None)
        if not wrong:continue
        shadow=dict(prefix);removed=[]
        for other in reversed(order):
            if other==actor:continue
            action=dict(type='detach',partId=other);after=perform(rt,shadow,action)
            if after is None:continue
            shadow=after;removed.append(other)
            base=perform(rt,shadow,dict(type='detach',partId=actor))
            if base is not None:
                wa=rt.candidates[wrong]['actor']
                remove=[dict(type='detach',partId=a) for a in removed]
                put=[dict(type='attach',partId=a,candidate=prefix[a]) for a in reversed(removed)]
                change=remove+[dict(type='detach',partId=actor),dict(type='attach',partId=wa,candidate=wrong)]+put
                restore=remove+[dict(type='detach',partId=wa),dict(type='attach',partId=actor,candidate=prefix[actor])]+put
                rows.append(('buried_wrong_color',change,restore));break
            if len(removed)>=3:break
    return rows

def sig(rt,state):return digest(sorted((repr(k),v) for k,v in rt.signature(state).items()))

def build_one(mid):
    source=certificate(mid,OBJECTS[mid]);cert=augmented(source);rt=PlateAssembly(cert);manual=rt.manual()
    assert manual['pathVerified'],mid
    order=manual['parts'];n=len(order);points=sorted({3,max(3,n//2),n-1})
    for at in points:
        add_extra(cert,manual['states'][at])
        row=cert['candidates'].pop('X001:extra',None)
        if row:cert['candidates'][f'X001:extra-t{at}']=row
    cert['contentSha256']=digest({k:v for k,v in cert.items() if k!='contentSha256'})
    rt=PlateAssembly(cert);manual=rt.manual();order=manual['parts'];cases=[];counts=Counter();reject=Counter()
    for at in points:
        prefix=manual['states'][at];previous=manual['states'][at-1];suffix=order[at:];accepted=defaultdict(list);seen=set()
        options=event_candidates(rt,prefix,suffix,order[:at])
        # Favor changes to an earlier installed part. Cancellations remain a
        # separately labeled challenge, never silently admitted to the main set.
        options.sort(key=lambda r:(r[0], any(a.get('partId')==order[at-1] for a in r[1]), len(r[1])))
        def accept(kind,change,restore):
            if len(accepted[kind])>=2:return
            after=replay(rt,prefix,change)
            if after is None or rt.complete(after):reject['illegal_or_complete']+=1;return
            if sig(rt,after)==sig(rt,prefix):reject['physically_equivalent']+=1;return
            token=sig(rt,after)
            if token in seen:return
            if replay(rt,after,restore)!=prefix:reject['cannot_restore_prefix']+=1;return
            seen.add(token)
            accepted[kind].append(dict(kind=kind,trigger=at,transaction=change,
                recoveryWitness=restore+[dict(type='attach',partId=a,candidate=rt.goal[a]) for a in suffix],
                beforeSha256=digest(prefix),afterSha256=digest(after),
                eventCancelsLastAction=sig(rt,after)==sig(rt,previous),
                repairPrefixMoves=len(restore),remainingBuildMoves=len(suffix),
                temporaryCorrectRemovals=sum(a['type']=='detach' and prefix.get(a['partId'])==after.get(a['partId']) and bool(after.get(a['partId'])) for a in restore),
                afterResidual=residual(rt,after)))
        for kind,change,restore in options:accept(kind,change,restore)
        # Two independent mistakes in the same incident, requiring two fixes.
        simple=[r for k,v in accepted.items() if k in ('wrong_color','shifted_piece','extra_layer','removed_piece') for r in v]
        for i,a in enumerate(simple):
            for b in simple[i+1:]:
                if a['kind']==b['kind']:continue
                actors_a={x['partId'] for x in a['transaction']};actors_b={x['partId'] for x in b['transaction']}
                if actors_a&actors_b:continue
                ra=a['recoveryWitness'][:-len(suffix)];rb=b['recoveryWitness'][:-len(suffix)]
                accept('compound_fault',a['transaction']+b['transaction'],rb+ra)
        stage='early' if at==3 else 'late' if at==n-1 else 'middle'
        group=f'{mid}--t{at}'
        common=dict(modelId=mid,sourceFamily=source['source']['modelId'],targetParts=n,trigger=at,stage=stage,pairedGroup=group,
                    protocol=VERSION,manipulationProtocol=PROTOCOL,objectCategory=OBJECTS[mid]['category'],objectNameZh=OBJECTS[mid]['name'],
                    track='complete-object',decisionBudget=max(40,6*n+20))
        cases.append(dict(common,id=group+'--control',kind='none'))
        for kind,rows in sorted(accepted.items()):
            for i,row in enumerate(rows,1):
                cases.append(dict(common,id=f'{group}--{kind}--v{i:02}',kind=kind,privateEvent=row,
                    eventVariant=i,repairDifficulty='temporary-disassembly' if row['temporaryCorrectRemovals'] else 'direct-repair',
                    temporalClass='action-cancellation' if row['eventCancelsLastAction'] else 'visible-change-candidate'))
                counts[kind]+=1
    evidence=dict(modelId=mid,sourceFamily=source['source']['modelId'],sourceCertificateSha256=source['contentSha256'],runtimeCertificateSha256=cert['contentSha256'],
                  buildWitness=[dict(type='attach',partId=a,candidate=rt.goal[a]) for a in order],goalSha256=digest(rt.goal),
                  admittedCases=len(cases),kinds=dict(counts),rejected=dict(reject),targetParts=n,triggerPoints=points)
    write(OUT/'models'/mid/'qualification.json',cert);write(OUT/'models'/mid/'evidence.json',evidence)
    return cases,evidence

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--resume',action='store_true');args=parser.parse_args()
    admissions=json.loads((OUT/'object-admission.json').read_text());assert all(r['passed'] for r in admissions)
    old=json.loads((OLD/'cases.private.json').read_text())['cases'];all_cases=[];audits=[]
    for c in old:
        if c['modelId'].startswith('obj-'):continue
        c=deepcopy(c);c.update(protocol=VERSION,track='legacy-mechanism',decisionBudget=max(40,6*c['targetParts']+20),stage='early' if c['trigger']==3 else 'middle')
        all_cases.append(c)
    for mid in sorted({c['modelId'] for c in all_cases}):
        dest=OUT/'models'/mid;dest.mkdir(parents=True,exist_ok=True)
        for name in ('qualification.json','evidence.json'):shutil.copy2(OLD/'models'/mid/name,dest/name)
        audits.append(json.loads((dest/'evidence.json').read_text()))
    generator_hash=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    for mid in sorted(OBJECTS):
        cache=OUT/'models'/mid/'cases.json'
        saved=json.loads(cache.read_text()) if cache.exists() else {}
        if args.resume and saved.get('generatorHash')==generator_hash and saved.get('sourceSha256')==certificate(mid,OBJECTS[mid])['contentSha256']:
            cases=saved['cases'];evidence=json.loads((cache.parent/'evidence.json').read_text())
        else:
            cases,evidence=build_one(mid);write(cache,dict(sourceSha256=certificate(mid,OBJECTS[mid])['contentSha256'],generatorHash=generator_hash,cases=cases))
        all_cases+=cases;audits.append(evidence);print(mid,len(cases),evidence['kinds'],flush=True)
    assert len({c['id'] for c in all_cases})==len(all_cases)
    # Remove inherited cross-label duplicates from the active bank as well.
    deduped=[];removed=[];runtime_cache={};seen={}
    for c in all_cases:
        if c['kind']=='none':deduped.append(c);continue
        mid=c['modelId']
        if mid not in runtime_cache:
            rt=PlateAssembly(json.loads((OUT/'models'/mid/'qualification.json').read_text()))
            plan=json.loads((OUT/'models'/mid/'evidence.json').read_text())['buildWitness']
            runtime_cache[mid]=(rt,plan)
        rt,plan=runtime_cache[mid];state={a:'' for a in rt.actors}
        for a in plan[:c['trigger']]:state[a['partId']]=a['candidate']
        for a in c['privateEvent']['transaction']:state[a['partId']]='' if a['type']=='detach' else a['candidate']
        token=(mid,c['trigger'],sig(rt,state))
        if token in seen:removed.append(dict(case=c,duplicateOf=seen[token],reason='identical physical event state at the same trigger'));continue
        seen[token]=c['id'];deduped.append(c)
    all_cases=deduped
    write(OUT/'excluded-duplicates.private.json',dict(rows=removed))
    for a in audits:
        a['generatedCases']=a['admittedCases'];a['admittedCases']=sum(c['modelId']==a['modelId'] for c in all_cases)
        write(OUT/'models'/a['modelId']/'evidence.json',a)
    write(OUT/'cases.private.json',dict(schema=VERSION,cases=all_cases))
    write(OUT/'index.json',dict(schema=VERSION,cases=[{k:v for k,v in c.items() if k!='privateEvent'} for c in all_cases],modelAudits=audits,counts=dict(Counter(c['kind'] for c in all_cases))))
    from dynamic_v6.catalog import seal
    seal(OUT)
    write(OUT/'expansion.json',dict(old=dict(cases=317,structures=30,completeObjects=4),new=dict(cases=len(all_cases),structures=len(audits),completeObjects=len(OBJECTS)),kinds=dict(Counter(c['kind'] for c in all_cases))))
    print('TOTAL',len(all_cases),'MODELS',len(audits),'OBJECTS',len(OBJECTS),flush=True)
if __name__=='__main__':main()
