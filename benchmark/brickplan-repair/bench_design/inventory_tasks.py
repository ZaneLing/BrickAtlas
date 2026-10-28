"""Inventory-constrained equivalent builds, with real one-piece geometry checks.

Only this explicitly declared track accepts different decompositions of the same
colored stud/plate volume. Ordinary exact-part tasks keep their existing rules.
"""
from collections import Counter
from copy import deepcopy
from functools import lru_cache
from pathlib import Path
import random
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from bench_design.challenges import QUALITY
from community_modules.core import ModuleAssembly,Episode as BaseEpisode
from community_modules.run_episode import ModulePacket
from static_v4.build_suite import part
from expansion_v7.build import read,write
from expansion_v7.runtime import execute
from matched_canvas import comparison,panels
from render import FONT
COMIC=Path('/System/Library/Fonts/Supplemental/Comic Sans MS.ttf')
if COMIC.exists():FONT=ImageFont.truetype(str(COMIC),22)

OUT=QUALITY/'inventory-equivalence'
PROTOCOL='inventory-equivalent-colored-volume/1'
DIMS={'3001':(4,2,3),'3003':(2,2,3),'3004':(2,1,3),
      '3020':(4,2,1),'3022':(2,2,1),'3023':(2,1,1)}
SIZE_LABELS={'3001':'2×4','3003':'2×2','3004':'2×1','3020':'2×4','3022':'2×2','3023':'2×1'}
BLUE='#0055bf';RED='#c91a09'
RULE='允许换用不同大小的零件组合。目标要求外形范围、颜色、总高度及最终连接一致；内部拼缝和零件数量可以不同。每次只装或拆一块，只能使用库中实际可用的零件。'


def cells(stem,x,y,z,turn=0):
    nx,nz,nh=DIMS[stem]
    if turn%2:nx,nz=nz,nx
    xs=[int(round((x+(i-(nx-1)/2)*20)/10)) for i in range(nx)]
    zs=[int(round((z+(i-(nz-1)/2)*20)/10)) for i in range(nz)]
    # Each cell is one stud by one stud by one plate, body only (not studs).
    hs=[int(round((-y-8*i-4)/4)) for i in range(nh)]
    return [tuple((xx,zz,hh)) for xx in xs for zz in zs for hh in hs]


class EquivalentAssembly(ModuleAssembly):
    def __init__(self,cert):
        super().__init__(cert)
        self.actors=[a for a in self.actors if a!='TARGET']
        self.available=set(self.actors)
        self.parts.pop('TARGET',None)

    def signature(self,state):
        out=Counter()
        for key in state.values():
            if not key:continue
            r=self.row(key)
            for cell in r['cells']:out[('occupied-cell',r['part']['colorHex'].lower(),tuple(cell))]+=1
        return out

    def check(self,state,actor,kind,raw=None,candidate=None):
        if actor not in self.available:return dict(state),dict(code='OUT_OF_STOCK',blockers=[])
        return super().check(state,actor,kind,raw,candidate)

    def final_constraints(self,state):
        return self.anchored(state)

    def complete(self,state):
        return self.signature(state)==self.signature(self.goal) and self.final_constraints(state)


class InventoryEpisode(BaseEpisode):
    def __init__(self,cert,case):
        super().__init__(cert,deepcopy(case),41)
        self.runtime=EquivalentAssembly(cert);self.runtime.goal=dict(case['goal'])
        rng=random.Random(41);actors=list(self.runtime.actors);keys=[k for k,r in cert['candidates'].items() if r['actor']!='TARGET']
        rng.shuffle(actors);rng.shuffle(keys)
        self.actor_alias={a:f'A{i+1:03}' for i,a in enumerate(actors)}
        self.pose_alias={k:f'C{i+1:04}' for i,k in enumerate(keys)}
        self.actors={v:k for k,v in self.actor_alias.items()};self.poses={v:k for k,v in self.pose_alias.items()}
        self.schedule=deepcopy(case.get('events',[]));self.events=[]
        self.manipulation_budget=40

    def inventory(self):
        return [dict(partId=self.actor_alias[a],status='installed' if self.state.get(a) else
            'available' if a in self.runtime.available else 'unavailable') for a in sorted(self.actor_alias,key=self.actor_alias.get)]

    def observe(self):
        obs=super().observe()
        obs.update(task=RULE+' 对照 TARGET 完成本题。',targetContract=dict(protocol=PROTOCOL,
            required=['colored occupied stud/plate cells','height','final connection to supplied object'],
            allowedToDiffer=['internal seams','part count','part numbers'],
            targetImageIsOneIllustration=True),inventoryAvailability=self.inventory(),
            availableViews=['isometric','rear','top','front'],manualAvailableThroughout=False)
        return obs

    def step(self,action):
        if action.get('type')=='inspect' and 'manualStep' in action:raise ValueError('This task has no prescribed build manual; inspect views, parts or candidates.')
        if action.get('type')=='inspect' and action.get('view')=='front':
            if set(action)-{'type','view','partId','candidate'}:raise ValueError('Invalid inspection')
            validated={**action,'view':'rear'};super().step(validated)
            self.feedback={**self.feedback,'view':'front'}
        else:super().step(action)
        if self.schedule and not self.events and self.feedback['code']=='OK':
            small=self.case['resourceActors'];installed=[a for a in small if self.state.get(a)]
            candidates=[a for a in small if not self.state.get(a) and a in self.runtime.available]
            if len(installed)>=self.schedule[0]['minimumSmallInstalled'] and candidates:
                # Actual installed pieces determine the event, never reference IDs/order.
                removed=candidates[0];before=sorted(self.runtime.available)
                self.runtime.available.remove(removed)
                event=dict(family='inventory-shortage',before=dict(self.state),after=dict(self.state),changes=[],
                    inventoryBefore=before,inventoryAfter=sorted(self.runtime.available),withdrawnActors=[removed],
                    inventoryOnlyEvent=True,atManipulation=self.actions,
                    priorDecompositionNowImpossible=True)
                self.events.append(event);self.last_event=event;self.event_applied=True
        return self.observe()


class InventoryPacket(ModulePacket):
    def __init__(self,ep,directory):
        super().__init__(ep,{'manual':[]},directory)
        # Keep the complete small object visible; the target patch is the only
        # operable region. All frames and scales are fixed across states.
        self.renderer.bounds['_module_frame']=self.renderer.envelope

    def inventory_pages(self):
        pages=[];actors=sorted(self.ep.actor_alias,key=self.ep.actor_alias.get)
        for offset in range(0,len(actors),12):
            group=actors[offset:offset+12];im=Image.new('RGB',(1600,((len(group)+3)//4)*336),'white');draw=ImageDraw.Draw(im)
            for i,a in enumerate(group):
                k=next(k for k,r in self.ep.cert['candidates'].items() if r['actor']==a)
                x,y=(i%4)*400,(i//4)*336
                card=self.renderer.rgb({a:k},'isometric',only=a,fixtures=False,frame_keys=[k],size=(400,270),supersample=1)[0]
                im.paste(card,(x,y+58));r=self.ep.cert['candidates'][k];nx,nz,h=DIMS[r['part']['canonical']]
                status='INSTALLED' if self.ep.state.get(a) else 'AVAILABLE' if a in self.ep.runtime.available else 'UNAVAILABLE'
                label=SIZE_LABELS[r['part']['canonical']].replace('×',' x ')
                draw.text((x+8,y+3),self.ep.actor_alias[a]+f' | {label} | {h} plate high',font=FONT,fill='#17283a')
                draw.text((x+8,y+29),status,font=FONT,fill='#a51e1e' if status=='UNAVAILABLE' else '#17283a')
            pages.append(self.asset(im,'inventory',page=len(pages)+1))
        return pages

    def observation(self):
        ep=self.ep;obs=ep.observe();assets=[]
        for view in ('isometric','rear','top'):
            assets.append(self.asset(comparison(self.renderer,ep.state,ep.case['goal'],view,'CURRENT NOW','TARGET SHAPE / COLOR / HEIGHT',frame_keys=['_module_frame']),
                'current-target',view=view,panels=panels('current-now','target')))
            if ep.previous is not None:
                assets.append(self.asset(comparison(self.renderer,ep.previous,ep.state,view,'BEFORE LAST ACTION','CURRENT NOW',frame_keys=['_module_frame']),
                    'temporal-pair',view=view,panels=panels('before-last-action','current-now')))
        inventory=self.inventory_pages();assets+=inventory
        fb=ep.feedback or {}
        if fb.get('code')=='INSPECT':
            view=fb.get('view','isometric')
            if 'candidate' in fb:
                key=ep.poses[fb['candidate']];a=ep.cert['candidates'][key]['actor']
                assets.append(self.asset(self.render({**ep.state,a:key},view),'candidate-preview',view=view,hypothetical=True))
            elif 'partId' in fb:
                a=ep.actors[fb['partId']];key=next(k for k,r in ep.cert['candidates'].items() if r['actor']==a)
                assets.append(self.asset(self.render({a:key},view,only=a),'inventory-inspection',view=view,partId=fb['partId']))
            else:assets.append(self.asset(self.render(ep.state,view),'current-inspection',view=view))
        obs.update(images=assets,inventoryPages=len(inventory),manual=dict(totalSteps=0,defaultImages=0,policy='No prescribed decomposition or manual.'),
            viewInputPolicy=dict(defaultViews=['isometric','rear','top'],automaticallyIncludedEachDecision=True,
                optionalViewRequest={'type':'inspect','view':'front'},sameAssemblyAcrossViews=True),
            remainingPartsPolicy='Each listed handle is one physical part. Installed, available and unavailable status is updated every decision.')
        return obs


def primitive(stem,x,y,z,color,turn=0):
    p=part(stem,x,y,z,index=0,quarter=turn);p['colorHex']=color
    return p


def certificate(axis,counts):
    color=BLUE if axis=='horizontal' else RED
    fixed={}
    if axis=='horizontal':
        for i,(x,z) in enumerate([(-30,-10),(-30,10),(30,-10),(30,10)]):
            fixed[f'F{i}']=primitive('3005',x,-24,z,'#a66b35')
        fixed['Ftop']=primitive('3020',0,-32,0,'#a66b35');bottom=-32;stem='3001';xs=4
    else:
        fixed['Fbase']=primitive('3031',0,-8,0,'#646464');bottom=-8;stem='3003';xs=2
    target_y=bottom-24;candidates={}
    def add(actor,number,poses,goal=False):
        for i,(x,y,z,turn) in enumerate(poses):
            key=actor+(':goal' if goal else f':p{i}')
            candidates[key]=dict(actor=actor,kind='goal' if goal else 'choice',
                part=primitive(number,x,y,z,color,turn),cells=cells(number,x,y,z,turn))
    add('TARGET',stem,[(0,target_y,0,0)],True)
    if axis=='horizontal':
        configs={'small':('3004',[(x,target_y,z,0) for x in (-20,0,20) for z in (-10,10)]+[(x,target_y,0,1) for x in (-30,-10,10,30)]),
                 'large':('3001',[(0,target_y,0,0),(20,target_y,0,0),(0,target_y,0,1)]),
                 'medium':('3003',[(x,target_y,0,0) for x in (-20,0,20)])}
    else:
        configs={'small':('3022',[(0,bottom-h,0,0) for h in (8,16,24)]),
                 'large':('3003',[(0,target_y,0,0),(20,target_y,0,0)]),
                 'halfbrick':('3004',[(0,target_y,z,0) for z in (-10,10)]),
                 'halfplate':('3023',[(0,bottom-h,z,0) for z in (-10,10) for h in (8,16,24)])}
    for kind,count in counts.items():
        number,poses=configs[kind]
        for i in range(count):add(kind+str(i+1),number,poses)
    actors=sorted({r['actor'] for r in candidates.values()}-{'TARGET'})
    cert=dict(schema=PROTOCOL,id=axis,modelId='inventory-'+axis,fixed=fixed,candidates=candidates,
        conservativeContext={},tableY=.1,extractionLengthLDU=160,scaleMetresPerLDU=.0004,
        source=dict(kind='original-recognizable-inventory-task',modelId='inventory-'+axis,
            moduleSourceIndices=list(range(len(actors))),generator='bench_design/inventory_tasks.py'),
        targetContract=PROTOCOL,boundary='Ideal rigid connectors, endpoint collisions and straight paths. No force simulation.')
    return cert,bottom


def placement(cert,actor,x,y,z,turn=0):
    return next(k for k,r in cert['candidates'].items() if r['actor']==actor and
        np.allclose(np.asarray(r['part']['rawMatrix'])[:3,3],[x,y,z]) and
        np.allclose(np.asarray(r['part']['rawMatrix'])[:3,:3],np.asarray(primitive(r['part']['canonical'],0,0,0,BLUE,turn)['rawMatrix'])[:3,:3]))


def build():
    records=[];tasks=[]
    for axis in ('horizontal','vertical'):
        for variant in ('large-required','small-required','mixed','either','repair','dynamic-shortage'):
            count=4 if axis=='horizontal' else 3
            counts=({'small':count-1,'large':1} if variant in ('large-required','repair') else
                {'small':count} if variant=='small-required' else
                ({'small':2,'medium':1} if axis=='horizontal' else {'halfbrick':1,'halfplate':3}) if variant=='mixed' else
                {'small':count,'large':1})
            cert,bottom=certificate(axis,counts);rt=EquivalentAssembly(cert)
            initial={a:'' for a in rt.actors};goal={**initial,'TARGET':'TARGET:goal'}
            def put(a,x,y,z,turn=0):return dict(type='attach',actor=a,candidate=placement(cert,a,x,y,z,turn))
            big=put('large1',0,bottom-24,0) if counts.get('large') else None
            small=([put('small'+str(i+1),x,bottom-24,0,1) for i,x in enumerate([-30,-10,10,30][:counts.get('small',0)])] if axis=='horizontal' else
                   [put('small'+str(i+1),0,bottom-8*(i+1),0) for i in range(counts.get('small',0))])
            if variant in ('large-required','either'):actions=[big]
            elif variant=='small-required':actions=small
            elif variant=='mixed':
                actions=([put('medium1',-20,bottom-24,0),put('small1',20,bottom-24,-10),put('small2',20,bottom-24,10)] if axis=='horizontal' else
                    [put('halfbrick1',0,bottom-24,-10)]+[put('halfplate'+str(i+1),0,bottom-8*(i+1),10) for i in range(3)])
            elif variant=='repair':
                initial,checks=execute(rt,initial,small);assert initial is not None,checks
                actions=[dict(type='detach',actor=a['actor']) for a in reversed(small)]+[big]
            else:
                actions=small[:-1]+[dict(type='detach',actor=a['actor']) for a in reversed(small[:-1])]+[big]
            cid=f'QI:{axis}::{variant}';mode='dynamic' if variant=='dynamic-shortage' else 'static'
            case=dict(id=cid,mode=mode,family='inventory-shortage' if mode=='dynamic' else 'inventory-replan' if variant=='repair' else 'inventory-allocation',
                initial=initial,goal=goal,events=[dict(minimumSmallInstalled=count-1)] if mode=='dynamic' else [],event=None,
                resourceActors=[a for a in rt.actors if a.startswith('small')],completedInstructionStep=1,
                referenceActions=actions,normalReferenceActions=small if mode=='dynamic' else actions,
                targetContract=PROTOCOL,humanErrorIds=[],humanValidated=False,
                referenceRepairNote=RULE,referenceActorLabels={a:(('2×1标准砖' if axis=='horizontal' else '2×2薄板')+f'（第{i+1}块）') for i,a in enumerate(sorted(a for a in rt.actors if a.startswith('small')))})
            case['referenceActorLabels']['large1']='2×4标准砖' if axis=='horizontal' else '2×2标准砖'
            folder=OUT/'cases'/axis/variant;write(folder/'certificate.private.json.gz',cert);write(folder/'case.private.json.gz',case)
            title=('工作台：2×4台面' if axis=='horizontal' else '展示台：三薄板高的立柱')
            records.append(dict(id=cid,model='inventory-'+axis,title=title,axis=axis,variant=variant,mode=mode,
                folder=str(folder.relative_to(OUT)),referenceMoves=len(actions),inventoryCounts=counts,caseType=case['family']))
            tasks.append(dict(code=f'I{len(tasks)+1:03}',caseId=cid,mode=mode,isNew=True))
    write(OUT/'index.json',dict(protocol=PROTOCOL,cases=records,models=2,caseCount=len(records),apiCalls=0,humanValidated=False))
    write(OUT/'review-tasks.json',dict(tasks=tasks))


@lru_cache(maxsize=1)
def index():return read(OUT/'index.json')


def source_row(cid):
    r=next(r for r in index()['cases'] if r['id']==cid);c=read(OUT/r['folder']/'case.private.json.gz')
    return dict(key=cid,bank='QI',model=r['model'],title=r['title'],mode=r['mode'],family=c['family'],case=c,
        evaluationMetadata=dict(canonicalId=cid,taskType='D3' if r['mode']=='dynamic' else 'S3' if r['variant']=='repair' else 'S2',
            track='inventory-equivalent-'+r['mode'],source='original:inventory:'+r['axis'],model=r['model']))


def load(cid,directory):
    row=source_row(cid);r=next(r for r in index()['cases'] if r['id']==cid)
    ep=InventoryEpisode(read(OUT/r['folder']/'certificate.private.json.gz'),row['case'])
    return row,ep,InventoryPacket(ep,directory),None


if __name__=='__main__':build()
