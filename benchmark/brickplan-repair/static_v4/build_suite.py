"""Deterministic paired structural challenges, certified with the live validator."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import json,sys,time
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from baseplate import PlateAssembly, PROTOCOL
from static_bench import difficulty, TYPES, CHALLENGES, PROTOCOL as OBSERVATION
from static_v4.certify import TransitionIndex, FiniteGraph, digest

OUT=HERE.parents[2]/'deliverables/brickplan-static-v4'
COLORS=['#c91a09','#0055bf','#f2cd37','#237841','#ffffff','#f57d20']
def dump(path,value):
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def part(stem,x,y,z,color=0,quarter=0,index=0):
    c,s=round(np.cos(quarter*np.pi/2)),round(np.sin(quarter*np.pi/2))
    m=np.asarray([[c,0,s,x],[0,1,0,y],[-s,0,c,z],[0,0,0,1]],dtype=float).tolist()
    return dict(partNumber=stem,canonical=stem,rawMatrix=deepcopy(m),matrix=m,colorHex=COLORS[color],
                name='LDraw '+stem,sourceIndex=index,direction=[0,-1,0])

class Builder:
    def __init__(self,name,family,title):
        self.name='sr4-'+name;self.family=family;self.title=title;self.fixed={};self.candidates={};self.defects={};self.specs=[]
    def add(self,actor,stem,x,y,z=0,color=0):
        p=part(stem,x,y,z,color,index=len(self.fixed)+len(self.candidates))
        if actor=='F001':self.fixed[actor]=p
        else:self.candidates[actor+':goal']=dict(actor=actor,kind='goal',label='模型零件',part=p,support=[],pathBlocked=[])
        return actor
    def wrong_color(self,actor):
        source=self.candidates[actor+':goal']['part']; p=deepcopy(source);p['derivedFromSourceIndex']=p['sourceIndex']
        p['colorHex']='#9b59b6';wrong='W'+actor[1:];key=wrong+':wrong_color'
        self.candidates[key]=dict(actor=wrong,kind='wrong_color',label='替件',part=p,support=[],pathBlocked=[])
        return {actor:'',wrong:key}
    def shifted(self,actor,offset):
        p=deepcopy(self.candidates[actor+':goal']['part'])
        for field in ('matrix','rawMatrix'):p[field][0][3]+=offset
        key=actor+':offset';self.candidates[key]=dict(actor=actor,kind='offset',label='位置',part=p,support=[],pathBlocked=[])
        return {actor:key}
    def case(self,name,edits,roots,mechanism):
        self.specs.append((name,edits,roots,mechanism))
    def cert(self):
        value=dict(schema='brickplan-geometry/procedural-selective-v1',fixed=self.fixed,candidates=self.candidates,
                   extractionLengthLDU=320,scaleMetresPerLDU=.0004,modelId=self.name,
                   source=dict(modelId=self.family,kind='procedural-mechanism',generator='static_v4/build_suite.py'),
                   boundary='Ideal rigid parts, connector paths, white environmental plate; no force/gravity claim.')
        value['contentSha256']=digest(value);return value

def root(actor,kind='wrong_color',affected=None):return dict(partId=actor,type=kind,affectedActors=affected or [actor])
def replacement(actor):return root('W'+actor[1:],'wrong_color',[actor,'W'+actor[1:]])

def shared(depth=1,independent=False,three=False):
    b=Builder(('independent' if independent else 'triple' if three else 'shared')+f'-{depth}',
              'cover-comparison','独立通道' if independent else f'三处错误 · {depth} 层共享通道' if three else f'{depth} 层共享拆修通道')
    b.add('F001','3009' if three else '3001',0,-24,color=4)
    xs=[-40,0,40] if three else [-20,20]
    targets=[]
    for i,x in enumerate(xs):targets.append(b.add(f'P{i+1:03}','3004',x,-48,z=0 if three else 10,color=i+1))
    for level in range(depth):
        if independent:
            for i,x in enumerate(xs):b.add(f'P{10+level*2+i:03}','3004',x,-72-level*24,z=10,color=5)
        else:b.add(f'P{10+level:03}','3009' if three else '3001',0,-72-level*24,color=5)
    defects=[b.wrong_color(a) for a in targets]
    for i,a in enumerate(targets):b.case(f'single-{i+1}',defects[i],[replacement(a)],'independent_access' if independent else 'shared_access')
    joined={k:v for d in defects for k,v in d.items()}
    b.case('joint',joined,[replacement(a) for a in targets],'joint_repair_savings')
    mixed={**defects[0],**{a:'' for a in targets[1:]}}
    b.case('mixed',mixed,[replacement(targets[0]),*[root(a,'missing') for a in targets[1:]]],'mixed_faults')
    b.case('control',[],[],'no_op');return b

def buried(depth):
    b=Builder(f'buried-{depth}','buried-depth',f'嵌入深度 {depth}')
    b.add('F001','3001',0,-24,color=4);b.add('P001','3001',0,-48,color=1)
    for i in range(depth):b.add(f'P{i+2:03}','3001',0,-72-i*24,color=(i%3)+2)
    b.add('P020','3001',100,-24,color=0) # correct, irrelevant beside the core
    d=b.wrong_color('P001');b.case('color',d,[replacement('P001')],'deep_access')
    b.case('missing',{'P001':''},[root('P001','missing')],'deep_access')
    b.case('control',{},[],'no_op');return b

def alternatives(floor=True):
    b=Builder('alternative-release' if floor else 'suspended','release-comparison',
              '上下两条合法拆修通道' if floor else '悬挂件连接修复')
    b.add('F001','3004',-60,-24,z=10,color=4);b.add('P001','3004',60,-24,z=10,color=4)
    for i,x in enumerate([-60,60]):
        b.add(f'P{2+i:03}','3004',x,-48,z=10,color=2);b.add(f'P{4+i:03}','3022',x,-56,color=2)
    b.add('P006','3034',0,-64,color=0);b.add('P007','3001',0,-56,color=1)
    if floor:b.add('P008','3020',0,-32,color=3)
    d=b.wrong_color('P007');b.case('color',d,[replacement('P007')],'alternative_release' if floor else 'suspended_coupling')
    b.case('missing',{'P007':''},[root('P007','missing')],'alternative_release' if floor else 'suspended_coupling')
    if floor:
        shifted=b.shifted('P006',100)
        b.case('order',dict(d,**shifted),[replacement('P007'),root('P006','offset')],'order_interference')
    b.case('control',{},[],'no_op');return b

def equivalence():
    b=Builder('equivalence','equivalence-control','等价件互换与对称朝向')
    b.add('F001','3020',0,-8,color=4)
    for a,x in [('P001',-20),('P002',20)]:b.add(a,'3004',x,-32,z=10,color=1)
    b.add('P003','3020',0,-40,color=3)
    edits={}
    for a,other in [('P001','P002'),('P002','P001')]:
        p=deepcopy(b.candidates[other+':goal']['part']);key=a+':equivalent'
        b.candidates[key]=dict(actor=a,kind='equivalent',label='同款互换',part=p,support=[],pathBlocked=[]);edits[a]=key
    b.case('permutation',edits,[],'equivalence_control')
    p=deepcopy(b.candidates['P003:goal']['part']);r=np.diag([-1,1,-1,1])
    for field in ['matrix','rawMatrix']:p[field]=(np.asarray(p[field])@r).tolist()
    b.candidates['P003:symmetric']=dict(actor='P003',kind='equivalent',label='对称朝向',part=p,support=[],pathBlocked=[])
    b.case('symmetry',{'P003':'P003:symmetric'},[],'equivalence_control')
    b.case('control',{},[],'no_op');return b

def build():
    models=[];all_cases=[];audit=[];started=time.time()
    builders=[shared(i) for i in (1,2,3)]+[shared(1,independent=True),shared(2,three=True),shared(6,three=True),buried(1),buried(3),alternatives(),alternatives(False),equivalence()]
    for b in builders:
        cert=b.cert();runtime=PlateAssembly(cert);folder=OUT/'library/models'/b.name
        choices={a:[k for k,r in runtime.candidates.items() if r['actor']==a] for a in runtime.actors}
        index=TransitionIndex(runtime,choices);model_cases={};proofs={}
        # One complete reachable graph usually serves every case of a model.
        graph=None
        for name,edits,roots,mechanism in b.specs:
            initial={**runtime.goal,**dict(edits)}
            pieces=list(runtime.present(initial).values())
            assert all(not runtime.plate_collision(p) for p in pieces),(b.name,name,'plate collision')
            assert all(runtime.q.endpoint(p,q)['status']=='CLEAR' for i,p in enumerate(pieces) for q in pieces[i+1:]),(b.name,name,'overlap')
            state=index.state(initial)
            if graph is None or state not in graph.states:graph=FiniteGraph(index).build(initial)
            else:graph.initial=state
            proof=graph.proof(initial)
            assert proof['status']=='CERTIFIED_FINITE',(b.name,name,proof['status'])
            physical_error=not runtime.complete(initial)
            kind='control' if not physical_error else roots[0]['type'] if len(roots)==1 else 'compound'
            cid=b.name+':'+name;plan=proof['referencePlan']
            case=dict(id=cid,modelId=b.name,title=b.title+' · '+name,kind=kind,category=kind,
                difficulty=difficulty(len(plan)),expectedOptimum=None,referenceCost=len(plan),referenceIsOptimal=False,
                initial=initial,goal=runtime.goal,actors=runtime.actors,roots=roots,oraclePlan=plan,
                tags=[mechanism]+(['requires_disassembly'] if proof['allShortest']['mayRemove'] else []),
                structuralTypes=sorted({r['type'] for r in roots}),description='',
                benchmarkMode='static',environmentChanges=False,manipulationProtocol=PROTOCOL,
                sourceFamily=b.family,mechanism=mechanism,pairedGroup=b.name,
                observation=dict(visualEligibility='pending-v4-evidence-gate'),
                certificate=dict(file=f'certificates/{cid.replace(":","--")}.json',sha256=proof['certificateSha256'],
                                 finiteOptimalCost=proof['optimalCost'],globalOptimalCost=None))
            dump(OUT/case['certificate']['file'],proof);model_cases[cid]=case;proofs[name]=proof;all_cases.append(case)
            audit.append(dict(caseId=cid,modelId=b.name,sourceFamily=b.family,mechanism=mechanism,cost=len(plan),
                              shortestPlans=proof['optimalPlanCount'],must=proof['allShortest']['mustRemove'],
                              may=proof['allShortest']['mayRemove'],collateralSets=proof['allShortest']['collateralSets'],
                              states=proof['states']))
        if 'joint' in proofs:
            single=[p['optimalCost'] for n,p in proofs.items() if n.startswith('single-')]
            joint=model_cases[b.name+':joint'];joint['pairEvidence']=dict(singleCosts=single,jointCost=proofs['joint']['optimalCost'],
                savings=sum(single)-proofs['joint']['optimalCost'],scope='same finite domain, same target and board, single-error counterparts')
        dump(folder/'qualification.json',cert);dump(folder/'cases.json',model_cases)
        kinds=Counter(c['kind'] for c in model_cases.values())
        models.append(dict(modelId=b.name,title=b.title,caseCount=len(model_cases),caseParts=len(runtime.present(runtime.goal)),originalParts=len(runtime.present(runtime.goal)),
                           sourceModelId=b.family,kinds=dict(kinds),coverage=[],sourceFamily=b.family,
                           targetProvenance=dict(kind='procedural-mechanism',generatorSha256=digest(Path(__file__).read_text()))))
        print(b.name,len(model_cases),'cases',[(n,p['optimalCost'],p['optimalPlanCount']) for n,p in proofs.items()],flush=True)
    dump(OUT/'library/index.json',dict(schema='selective-repair-extension/1',models=models,caseCount=len(all_cases),sourceFamilies=len({m['sourceFamily'] for m in models})))
    (OUT/'library/cases.jsonl').write_text(''.join(json.dumps(c,ensure_ascii=False)+'\n' for c in all_cases))
    dump(OUT/'audit.json',dict(models=len(models),cases=len(all_cases),seconds=time.time()-started,rows=audit))
    print('DONE',len(models),len(all_cases),round(time.time()-started,2),flush=True)

if __name__=='__main__':build()
