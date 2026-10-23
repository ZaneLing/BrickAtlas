"""Generate and physically replay the additive extension; no model API calls."""
from collections import Counter
from copy import deepcopy
import argparse
import gzip
import hashlib
import json
import time
from expansion_v7 import ROOT, OUT, PROTOCOL
from expansion_v7.runtime import Episode, execute, move, public_action, runtime
from expansion_v7.variants import augment, pad
from expansion_v7.scope import require_allowed

FAMILIES = ('missing','wrong-color','extra-layer','offset','rotated','wrong-part',
            'early-cover','buried-repair','left-right-swap','repeat-omission',
            'repeated-step')
HUMAN = {'missing':['H01'],'repeat-omission':['H02'],'repeated-step':['H03'],
    'extra-layer':['H03','H11'],'wrong-color':['H04'],'wrong-part':['H05'],
    'rotated':['H06'],'offset':['H07'],'left-right-swap':['H08'],
    'early-cover':['H09'],'buried-repair':['H10']}


def write(path, data):
    path.parent.mkdir(parents=True,exist_ok=True)
    value=(json.dumps(data,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode()
    if path.suffix=='.gz':
        path.write_bytes(gzip.compress(value,mtime=0))
    else:path.write_bytes(value)


def read(path):
    data=path.read_bytes()
    return json.loads(gzip.decompress(data) if path.suffix=='.gz' else data)


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True).encode()).hexdigest()


def states_for(rt, normal):
    state={a:'' for a in rt.actors};states=[dict(state)]
    for action in normal:
        state, evidence=execute(rt,state,[action])
        if state is None:raise AssertionError((action,evidence))
        states.append(dict(state))
    if not rt.complete(state):raise AssertionError('Manual fails target')
    return states


def run_witness(cert, case, normal, cache=None):
    ep=Episode(cert,case)
    if cache is not None:ep.runtime.q=cache
    actions=[];seen=0;events=[]
    for action in normal:
        ep.step(public_action(ep,action));actions.append(action)
        if ep.feedback['code']!='OK':raise AssertionError((case['id'],action,ep.feedback))
        if len(ep.events)>seen:
            incident=deepcopy(ep.events[-1]);events.append(incident);seen=len(ep.events)
            for undo in incident['recovery']:
                ep.step(public_action(ep,undo));actions.append(undo)
                if ep.feedback['code']!='OK':raise AssertionError((case['id'],'recovery',ep.feedback))
            if len(ep.events)!=seen:raise AssertionError('Another event occurred inside recovery witness')
            if ep.state!=incident['before']:raise AssertionError('Incident not restored')
    ep.step({'type':'finish'})
    score=ep.score()
    if not score['success'] or len(ep.events)!=len(case['events']):
        raise AssertionError((case['id'],score,ep.trigger_attempts))
    return dict(referenceActions=actions,referenceEvents=events,referenceScore=score,
                legalWitnessOnly=True,humanValidated=False,modelEvaluated=False)


def signature_key(rt, case):
    # Actor IDs and unused inventory do not make a new physical state task.
    def sig(state):return sorted((repr(k),v) for k,v in rt.signature(state).items())
    event=[dict(minimumInstalled=e['minimumInstalled'],before=sig(r['before']),after=sig(r['after']))
           for e,r in zip(case.get('events',[]),case.get('referenceEvents',[]))]
    return digest(dict(source=rt.cert['source'].get('sourceSetId',rt.cert['source'].get('modelId')),
        mode=case['mode'],initial=sig(case['initial']),goal=sig(case['goal']),events=event))


def build_one(meta):
    mid=meta['id'];prepared=OUT/'prepared'/mid
    cert=pad(augment(read(prepared/'base-certificate.private.json')))
    rt=runtime(cert)
    manual=read(prepared/'base-manual.private.json')
    normal=manual.get('actions') or [move(a,rt.goal[a]) for a in manual['parts']]
    states=states_for(rt,normal);n=len(normal);cases=[];rejected=[];seen=set()
    initial=states[0];goal=states[-1]
    def add(case):
        require_allowed(case)
        key=signature_key(rt,case)
        if key in seen:return
        seen.add(key);case['physicalTaskSha256']=key
        cases.append(case)
    def base(mode,family,cp=0):
        return dict(id=f'v7::{mid}::{mode}::{family}::t{cp}',module=mid,mode=mode,family=family,
            completedInstructionStep=cp if mode=='static' else 0,
            initial=deepcopy(states[cp] if mode=='static' else initial),
            goal=deepcopy(states[cp] if mode=='static' else goal),events=[],
            humanErrorIds=HUMAN.get(family,[]),protocol=PROTOCOL,
            sourceSetId=meta['sourceSetId'],track=meta['track'])
    control=base('dynamic','control');control.update(run_witness(cert,control,normal,rt.q));add(control)
    # At most two checkpoints per family, assigned from physical feasibility,
    # never from a policy's success or model outputs.
    checkpoints=sorted(set([max(3,n//3),max(3,2*n//3),max(3,n-1)]))
    search=checkpoints+[cp for cp in range(3,n) if cp not in checkpoints]
    feasible={}
    for family in FAMILIES:
        accepted=[]
        for cp in search:
            if cp>=n:continue
            incident=rt.incident(family,states[cp],latest=normal[cp-1]['actor'],
                placement_order={a['actor']:i+1 for i,a in enumerate(normal[:cp])})
            if incident is None:continue
            if any(rt.signature(incident['after'])==rt.signature(x['after']) and cp==x['cp'] for x in accepted):continue
            dynamic=base('dynamic',family,cp)
            dynamic['events']=[dict(family=family,minimumInstalled=cp,minimumActionsSincePrevious=1,
                humanErrorIds=HUMAN[family],variant=0)]
            try:dynamic.update(run_witness(cert,dynamic,normal,rt.q))
            except AssertionError as exc:
                rejected.append(dict(family=family,checkpoint=cp,reason=str(exc)[:200]));continue
            accepted.append(dict(cp=cp,**incident))
            add(dynamic)
            static=base('static',family,cp);static['initial']=incident['after']
            end,evidence=execute(rt,static['initial'],incident['recovery'])
            if end!=static['goal']:raise AssertionError('Invalid static repair')
            static.update(referenceActions=incident['recovery'],referenceChecks=evidence,
                referenceIncident=incident,legalWitnessOnly=True,humanValidated=False,modelEvaluated=False)
            add(static)
            static_control=base('static','control',cp);static_control['referenceActions']=[];add(static_control)
            if len(accepted)>=2:break
        feasible[family]=[r['cp'] for r in accepted]
        if not accepted:rejected.append(dict(family=family,reason='No qualified reversible event in searched states'))
    # Distinct temporal incidents. Occupancy thresholds and action gaps use only
    # actual progress, with no requirement to match a reference prefix.
    for sequence in (('missing','wrong-color'),('offset','extra-layer'),
                     ('wrong-part','missing'),('missing','wrong-color','offset')):
        if len(sequence)==3 and n<14:continue
        points=[max(3,round(n*(i+1)/(len(sequence)+1))) for i in range(len(sequence))]
        if any(b-a<2 for a,b in zip(points,points[1:])):continue
        name='then-'.join(sequence)
        case=base('dynamic','multiple-'+name)
        case['id']=f'v7::{mid}::dynamic::multiple::{name}'
        case['humanErrorIds']=sorted({h for f in sequence for h in HUMAN[f]}|{'H13'})
        case['events']=[dict(family=f,minimumInstalled=cp,minimumActionsSincePrevious=3 if i else 1,
            humanErrorIds=HUMAN[f],variant=i) for i,(f,cp) in enumerate(zip(sequence,points))]
        try:case.update(run_witness(cert,case,normal,rt.q));add(case)
        except AssertionError as exc:rejected.append(dict(family='multiple',sequence=sequence,reason=str(exc)[:200]))
    write(OUT/'models'/mid/'certificate.private.json.gz',cert)
    write(OUT/'models'/mid/'manual.private.json.gz',dict(actions=normal,states=states))
    write(OUT/'models'/mid/'cases.private.json.gz',cases)
    write(OUT/'models'/mid/'admission.json',dict(status='PASS',metadata=meta,
        activeParts=n,cases=len(cases),feasibleCheckpoints=feasible,rejected=rejected,
        witnessPolicy='Legal feasible reference, not shortest path',humanValidated=False,modelEvaluated=False))
    return cases


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--only');parser.add_argument('--resume',action='store_true')
    args=parser.parse_args();started=time.time()
    metadata=read(OUT/'prepared/index.json');all_cases=[]
    for meta in metadata:
        if args.only and args.only!=meta['id']:continue
        path=OUT/'models'/meta['id']/'cases.private.json.gz'
        if args.resume and path.exists():cases=read(path)
        else:
            print('BUILD',meta['id'],meta['activeParts'],flush=True)
            cases=build_one(meta)
        all_cases.extend(cases)
        print('PASS',meta['id'],len(cases),Counter(c['family'] for c in cases),flush=True)
    index=[{k:c[k] for k in ('id','module','mode','family','sourceSetId','track','humanErrorIds','physicalTaskSha256')}
           |dict(eventCount=len(c['events'])) for c in all_cases]
    write(OUT/'index.json',dict(protocol=PROTOCOL,cases=index,models=metadata,
        counts=dict(Counter(c['family'] for c in all_cases)),seconds=round(time.time()-started,2),
        apiCalls=0,humanValidationCount=0,modelEvaluationCount=0))
    print('DONE',len(all_cases),round(time.time()-started,2),flush=True)


if __name__=='__main__':main()
