"""Small complete objects, with matched normal and qualified repair episodes."""
from copy import deepcopy
from recognizable_models import OUT
from expansion_v7 import PROTOCOL
from expansion_v7.build import read, write, states_for, run_witness, signature_key, HUMAN
from expansion_v7.runtime import runtime, execute
from expansion_v7.variants import augment, pad
from expansion_v7.scope import require_allowed


def main():
    index=[]
    for meta in read(OUT/'admission-screen.json')['admitted']:
        folder=OUT/'models'/meta['id']
        cert=pad(augment(read(folder/'base-certificate.private.json.gz')))
        rt=runtime(cert);normal=read(folder/'base-manual.private.json.gz')['actions']
        states=states_for(rt,normal);cases=[];rejected=[];seen=set()
        def base(mode,family,cp=0):
            return dict(id=f"objects::{meta['id']}::{mode}::{family}::t{cp}",
                module=meta['id'],mode=mode,family=family,protocol=PROTOCOL,
                sourceSetId=cert['source']['sourceSetId'],track='complete-object',
                completedInstructionStep=cp if mode=='static' else 0,
                initial=deepcopy(states[cp] if mode=='static' else states[0]),
                goal=deepcopy(states[cp] if mode=='static' else states[-1]),
                events=[],humanErrorIds=HUMAN.get(family,[]))
        def add(case):
            require_allowed(case);key=signature_key(rt,case)
            if key in seen:return
            seen.add(key);case['physicalTaskSha256']=key;cases.append(case)
        control=base('dynamic','control');control.update(run_witness(cert,control,normal,rt.q));add(control)
        for family in ('missing','wrong-color','extra-layer','offset','rotated','wrong-part'):
            for cp in sorted(range(3,len(normal)),key=lambda n:(abs(n-len(normal)*.6),n)):
                incident=rt.incident(family,states[cp],latest=normal[cp-1]['actor'],
                    placement_order={a['actor']:i+1 for i,a in enumerate(normal[:cp])})
                if incident is None:continue
                dynamic=base('dynamic',family,cp)
                dynamic['events']=[dict(family=family,minimumInstalled=cp,
                    minimumActionsSincePrevious=1,humanErrorIds=HUMAN[family],variant=0)]
                try:dynamic.update(run_witness(cert,dynamic,normal,rt.q))
                except AssertionError:continue
                add(dynamic)
                static=base('static',family,cp);static['initial']=incident['after']
                end,evidence=execute(rt,static['initial'],incident['recovery'])
                assert end==static['goal']
                static.update(referenceActions=incident['recovery'],referenceChecks=evidence,
                    referenceIncident=incident,legalWitnessOnly=True,humanValidated=False,modelEvaluated=False)
                add(static)
                if not any(c['mode']=='static' and c['family']=='control' and c['completedInstructionStep']==cp for c in cases):
                    sc=base('static','control',cp);sc['referenceActions']=[];add(sc)
                break
            else:rejected.append(dict(family=family,reason='No reversible qualified incident found; no case added'))
        write(folder/'certificate.private.json.gz',cert)
        write(folder/'manual.private.json.gz',dict(actions=normal,states=states))
        write(folder/'cases.private.json.gz',cases)
        write(folder/'case-admission.json',dict(cases=len(cases),rejected=rejected,
            programWitnessVerified=True,humanValidated=False,modelEvaluated=False))
        index.extend({k:c[k] for k in ('id','module','mode','family','physicalTaskSha256')} for c in cases)
        print('CASES',meta['id'],len(cases),flush=True)
    write(OUT/'case-index.json',dict(cases=index,apiCalls=0,
        scope='Separate complete-object collection; not added to historical global distinct-task totals without cross-bank deduplication.'))


if __name__=='__main__':main()
