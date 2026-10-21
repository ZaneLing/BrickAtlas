"""Native-geometry paper figures: lossless native renders, vector labels and diagrams.

Never enlarge a gallery screenshot. All visual states are re-rendered from the
versioned certificates; presentation callouts are explicitly figure-only.
"""
from pathlib import Path
from copy import deepcopy
import hashlib,json,sys,re
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch,Rectangle
from PIL import Image,ImageFilter

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'benchmark/brickplan-repair/community_modules'))
from core import ModuleAssembly,render_certificate,OUT
from dynamic_v5.vision import DynamicVisionRenderer
from render import PALETTE
FIG=HERE/'figures-v2';RAW=FIG/'native';RAW.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'pdf.fonttype':42,'ps.fonttype':42,
                     'svg.fonttype':'none','axes.titlesize':8,'axes.labelsize':8})
PALETTE.update(dict(re.findall(r'CODE\s+(\d+)\s+VALUE\s+(#[0-9A-Fa-f]{6})',
    (ROOT/'assets-source/ldraw-library/locked/LDConfig.ldr').read_text())))
INK='#162e3c';BLUE='#2166ac';ORANGE='#c75c19';GREEN='#167d72';GRAY='#63727b'
manifest={'schema':'native-geometry-publication-figures/2','renderPixels':[3200,2400],
          'supersampling':2,'exportDpi':600,'vectorText':True,'sources':{},'renders':{},'figures':{}}


def source(path):
    manifest['sources'][str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
    return json.loads(path.read_text())


modules=source(OUT/'gallery-data.js.json')
cache={}

def data(mid):
    if mid not in cache:
        base=OUT/mid;cert=source(base/'certificate.private.json');manual=source(base/'manual.private.json')
        change=source(base/'perturbations.private.json');rt=ModuleAssembly(cert)
        renderer=DynamicVisionRenderer(render_certificate(cert),runtime=rt)
        pts=np.concatenate([renderer.bounds[a['candidate']] for a in manual['actions']])
        lo,hi=pts.min(0)-[20,28,20],pts.max(0)+[20,20,20]
        renderer.bounds['_paper_frame']=np.array([[x,y,z] for x in (lo[0],hi[0]) for y in (lo[1],hi[1]) for z in (lo[2],hi[2])])
        cache[mid]=(cert,manual,change,rt,renderer)
    return cache[mid]


def render(mid,name,state,view='isometric',full=False,only=None,highlight=None):
    cert,manual,change,rt,renderer=data(mid)
    spec=dict(module=mid,state=state,view=view,full=full,only=only,highlight=highlight,
              certSha=manifest['sources'][str((OUT/mid/'certificate.private.json').relative_to(ROOT))],size=[3200,2400])
    token=hashlib.sha256(json.dumps(spec,sort_keys=True).encode()).hexdigest()
    path=RAW/(mid+'--'+name+'.png');meta=path.with_suffix('.json')
    if not path.exists() or not meta.exists() or json.loads(meta.read_text()).get('key')!=token:
        image,mask=renderer.rgb(state,view,size=(3200,2400),supersample=2,
                                only=only,frame_keys=None if full or only else ['_paper_frame'])
        if highlight:
            binary=Image.fromarray(np.uint8(mask==renderer.ids[highlight])*255)
            border=Image.fromarray(np.maximum(np.asarray(binary.filter(ImageFilter.MaxFilter(19)),dtype=np.int16)-np.asarray(binary,dtype=np.int16),0).astype('uint8'))
            image.paste((227,111,24),(0,0),border)
        image.save(path,optimize=True)
        meta.write_text(json.dumps({'key':token,'state':spec},indent=2)+'\n')
    manifest['renders'][str(path.relative_to(FIG))]=dict(sha256=hashlib.sha256(path.read_bytes()).hexdigest(),**spec)
    return np.asarray(Image.open(path).convert('RGB'))


def figsave(fig,name):
    fig.savefig(FIG/(name+'.pdf'),dpi=600,facecolor='white',metadata={'Creator':'BrickPlan native renderer / Matplotlib'})
    fig.savefig(FIG/(name+'.svg'),dpi=600,facecolor='white')
    fig.savefig(FIG/(name+'.png'),dpi=600,facecolor='white')
    manifest['figures'][name]=dict(inches=list(fig.get_size_inches()),formats=['pdf','svg','png'],dpi=600,
        pdfSha256=hashlib.sha256((FIG/(name+'.pdf')).read_bytes()).hexdigest())
    plt.close(fig);print('FIGURE',name,flush=True)


def panel(fig,box,im,title=None,subtitle=None,color=INK):
    ax=fig.add_axes(box);ax.imshow(im,interpolation='none');ax.axis('off')
    if title:ax.set_title(title,fontsize=8,color=color,fontweight='bold',pad=4)
    if subtitle:ax.text(.5,-.065,subtitle,transform=ax.transAxes,ha='center',va='top',fontsize=7,color=GRAY)
    return ax


def arrow(fig,start,end,color=GRAY,style='->',lw=1.2):
    fig.patches.append(FancyArrowPatch(start,end,transform=fig.transFigure,arrowstyle=style,
                                     mutation_scale=10,lw=lw,color=color,clip_on=False))


def box(fig,xywh,title,body,color=BLUE):
    x,y,w,h=xywh
    fig.patches.append(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.007,rounding_size=0.012',
        transform=fig.transFigure,linewidth=.9,edgecolor=color,facecolor='white'))
    fig.text(x+w/2,y+h*.69,title,ha='center',va='center',fontweight='bold',fontsize=8,color=color)
    fig.text(x+w/2,y+h*.30,body,ha='center',va='center',fontsize=7.1,color=INK,linespacing=1.3)


# Broad-bank scene access. Paper crops use the same framing for each matched pair.
from functools import lru_cache
from baseplate import PlateAssembly
from plate5_eval import load as load_static
from dynamic_v5.build import replay
STATIC=[json.loads(line) for line in (ROOT/'deliverables/brickplan-static-plate5/cases.jsonl').read_text().splitlines()]
DYNAMIC=source(ROOT/'deliverables/brickplan-dynamic-v6/cases.private.json')['cases']
COVER=source(HERE/'evidence/benchmark-coverage.json')
AUDIT={r['caseId']:r for r in source(ROOT/'deliverables/brickplan-dynamic-v6/audit.json')['rows']}
for name in ['cases.jsonl','summary.json','replay-audit.json']:
    p=ROOT/'deliverables/brickplan-static-plate5'/name;manifest['sources'][str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()


def frame(ren,keys):
    pts=np.concatenate([ren.bounds[k] for k in keys if k in ren.bounds]);lo=pts.min(0)-20;hi=pts.max(0)+20
    ren.bounds['_paper_frame']=np.array([[x,y,z] for x in (lo[0],hi[0]) for y in (lo[1],hi[1]) for z in (lo[2],hi[2])])


@lru_cache(maxsize=4)
def dd(mid):
    cert=source(ROOT/'deliverables/brickplan-dynamic-v6/models'/mid/'qualification.json')
    ev=source(ROOT/'deliverables/brickplan-dynamic-v6/models'/mid/'evidence.json')
    rt=PlateAssembly(cert);ren=DynamicVisionRenderer(rt.cert,rt);frame(ren,[k for k in rt.goal.values() if k])
    return rt,ren,ev


@lru_cache(maxsize=4)
def sd(qid):
    rt,c=load_static(qid);source((ROOT/'deliverables/brickplan-static-held4/combined'/c['qualificationFile']).resolve())
    ren=DynamicVisionRenderer(rt.cert,rt);frame(ren,[k for s in [c['goal'],c['initial']] for k in s.values() if k])
    return rt,ren,c


def bankrender(kind,key,name,state,view='isometric'):
    rt,ren,ev=dd(key) if kind=='D' else sd(key)
    spec=dict(track=kind,key=key,state=state,view=view,size=[3200,2400],certificateSha=rt.cert['contentSha256'],framing='goal-and-20LDU-v1' if kind=='D' else 'matched-current-target-20LDU-v1')
    token=hashlib.sha256(json.dumps(spec,sort_keys=True).encode()).hexdigest();path=RAW/f'{kind}-{key}--{name}.png';meta=path.with_suffix('.json')
    if not path.exists() or not meta.exists() or json.loads(meta.read_text()).get('key')!=token:
        im,_=ren.rgb(state,view=view,size=(3200,2400),supersample=2,frame_keys=['_paper_frame'])
        im.save(path,optimize=True);meta.write_text(json.dumps({'key':token,'state':spec},indent=2)+'\n')
    manifest['renders'][str(path.relative_to(FIG))]=dict(sha256=hashlib.sha256(path.read_bytes()).hexdigest(),**spec)
    return np.asarray(Image.open(path).convert('RGB'))


def dgoal(mid):
    rt,_,_=dd(mid);return bankrender('D',mid,'goal',rt.goal)


def sgoal(mid):
    c=next(c for c in STATIC if c['modelId']==mid and not c['oraclePlan']);rt,ren,c=sd(c['publicId'])
    return bankrender('S',c['publicId'],'target',c['goal'])


def dcase(kind,preferred=None):
    choices=[c for c in DYNAMIC if c['kind']==kind and c['modelId'].startswith('obj-') and AUDIT[c['id']]['primaryMachineCandidate']]
    if preferred and any(c['modelId']==preferred for c in choices):choices=[c for c in choices if c['modelId']==preferred]
    c=max(choices,key=lambda c:AUDIT[c['id']]['eventChangedPixels']['isometric'])
    rt,ren,ev=dd(c['modelId']);initial={a:'' for a in rt.actors}
    before=replay(rt,initial,ev['buildWitness'][:c['trigger']]);after=replay(rt,before,c['privateEvent']['transaction'])
    assert before is not None and after is not None
    return c,before,after


def dpair(kind,preferred=None):
    c,before,after=dcase(kind,preferred);view='isometric'
    if AUDIT[c['id']]['eventChangedPixels'][view]<1000:view=max(AUDIT[c['id']]['eventChangedPixels'],key=AUDIT[c['id']]['eventChangedPixels'].get)
    current=bankrender('D',c['modelId'],c['id']+'-after',after,view)
    target=bankrender('D',c['modelId'],c['id']+'-before',before,view)
    return current,target,c['id']


def spair(category,qid=None):
    c=next(c for c in STATIC if (c['publicId']==qid if qid else c['category']==category))
    rt,ren,c=sd(c['publicId'])
    return bankrender('S',c['publicId'],'current',c['initial']),bankrender('S',c['publicId'],'target',c['goal']),c['publicId']


def mpair(mid,kind):
    cert,manual,changes,*_=data(mid);view='rear' if mid=='panda-head' else 'isometric'
    return render(mid,'error-'+kind,changes[kind]['after'],view),render(mid,'stage-'+kind,manual['states'][cert['checkpoint']],view),mid+'-static-'+kind


def pairs_figure(items,name,cols=4):
    rows=(len(items)+cols-1)//cols;fig=plt.figure(figsize=(7,rows*.86+.14))
    for i,(label,fun) in enumerate(items):
        current,target,case=fun();row,col=divmod(i,cols);left=col/cols+.008;bottom=1-(row+1)/rows+.035/rows
        # Each compact cell has two equal-view panels, with vector labels.
        width=(1/cols-.022)/2;top=1-row/rows-.015
        fig.text(left+.5/cols-.008,top,label,ha='center',va='top',fontsize=7.1,fontweight='bold',color=INK)
        ax=panel(fig,(left,bottom+.17/rows,width,.61/rows),current)
        panel(fig,(left+width+.006,bottom+.17/rows,width,.61/rows),target)
        diff=np.max(np.abs(current.astype(np.int16)-target.astype(np.int16)),axis=2)>=24;ys,xs=np.nonzero(diff)
        if len(xs):ax.add_patch(Rectangle((xs.min()-12,ys.min()-12),xs.max()-xs.min()+24,ys.max()-ys.min()+24,linewidth=.8,edgecolor=ORANGE,facecolor='none'))
        fig.text(left+width/2,bottom+.05/rows,'Fault',ha='center',fontsize=6.6,color=ORANGE)
        fig.text(left+width*1.5+.006,bottom+.05/rows,'Correct stage',ha='center',fontsize=6.6,color=GREEN)
        manifest.setdefault('shownCases',{})[name+':'+str(i)]=case
    figsave(fig,name)


# Homepage overview: older configurations and designs have equal visual status.
fig=plt.figure(figsize=(7,2.1))
static_ids=['10001','31009','31027','31028','v23-31039','v23-21004','omr-21309','v23-3179']
obj_ids=['obj-chair','obj-table','obj-city-car','obj-crane','sr4-buried-3','sr4-shared-3','sr4-triple-2','sr4-suspended']
mod_ids=['cottage-roof','racer-top','seaplane-tail','museum-roof','repair-truck-cab','panda-head','white-house-roof','brandenburg-top']
sections=[('S  |  160 static configurations / 3,292 cases',[(mid,sgoal(mid)) for mid in static_ids]),
          ('D  |  68 structures (42 complete objects + 26 mechanisms) / 1,872 cases',[(mid.removeprefix('obj-').removeprefix('sr4-'),dgoal(mid)) for mid in obj_ids]),
          ('M  |  12 community modules / 48 static + 48 dynamic cases',[(mid.split('-')[0],render(mid,'full-target',data(mid)[1]['states'][-1],full=True)) for mid in mod_ids])]
for row,(label,items) in enumerate(sections):
    top=.99-row/3;fig.text(.01,top,label,fontsize=7.3,fontweight='bold',color=BLUE,va='top')
    for col,(name,im) in enumerate(items):
        panel(fig,(.006+col/8,top-.265,.113,.21),im)
        fig.text(.0625+col/8,top-.27,name,ha='center',va='top',fontsize=6.1,color=INK)
figsave(fig,'teaser')

# Compact column-width protocol; action loop and the two scene times are explicit.
fig=plt.figure(figsize=(3.35,2.0))
box(fig,(.02,.73,.96,.21),'Shared task information','Target + inventory + reference views / manual',BLUE)
box(fig,(.02,.43,.43,.21),'Agent action','One attach / detach\nInspect / finish',GREEN)
box(fig,(.55,.43,.43,.21),'Executor','Check legality\nApply hidden event',ORANGE)
arrow(fig,(.23,.72),(.23,.66));arrow(fig,(.46,.535),(.54,.535))
fig.text(.5,.34,'Actual RGB + action feedback',ha='center',fontsize=7.3,fontweight='bold',color=INK)
arrow(fig,(.77,.42),(.77,.36),ORANGE);arrow(fig,(.22,.35),(.22,.42),GREEN)
fig.text(.5,.18,'Previous scene  |  Current scene  |  Fixed target',ha='center',fontsize=6.8,color=INK)
fig.text(.5,.06,'Repeat until finish or budget. No error label is revealed.',ha='center',fontsize=6.5,color=GRAY)
figsave(fig,'protocol')

# Seven part-and-state columns: each reference action remains one brick.
mid='seaplane-tail';cert,manual,*_=data(mid);fig=plt.figure(figsize=(7,1.22))
assert len(manual['actions'])==7
for i,a in enumerate(manual['actions']):
    part=render(mid,f'manual-piece-{i+1}',{a['actor']:a['candidate']},only=a['actor'])
    state=render(mid,f'manual-after-{i+1}',manual['states'][i+1],highlight=a['actor'])
    panel(fig,(.008+i/7,.65,.125,.22),part)
    fig.text((i+.5)/7,.98,f'Part {i+1}',ha='center',va='top',fontsize=7,color=INK)
    panel(fig,(.004+i/7,.02,.135,.55),state)
    if i<6:arrow(fig,((i+1)/7-.009,.30),((i+1)/7+.009,.30))
figsave(fig,'instructions')

# A compact one-column order counterexample.
mid='cottage-roof';cert,manual,changes,rt,*_=data(mid)
ref=manual['states'][3];alt=dict(manual['states'][2]);a=manual['actions'][3];alt,res=rt.check(alt,a['actor'],'attach',candidate=a['candidate']);assert res['code']=='OK'
fig=plt.figure(figsize=(3.35,1.16))
for col,(state,name,label) in enumerate([(ref,'route-a','1, 2, 3'),(alt,'route-b','1, 2, 4'),(manual['states'][-1],'route-goal','Same goal')]):
    panel(fig,(.005+col/3,.04,.31,.70),render(mid,name,state),label)
fig.text(.326,.37,'≠',fontsize=13,ha='center',color=ORANGE);arrow(fig,(.65,.37),(.68,.37),GREEN)
figsave(fig,'alternative-orders')

pairs_figure([
 ('S: rotation',lambda:spair('rotation','S00254')),
 ('S: wrong size',lambda:spair('wrong_size')),
 ('D: shifted piece',lambda:dpair('shifted_piece','obj-house')),
 ('D: early cover',lambda:dpair('early_cover','obj-cabinet')),
 ('D: buried color',lambda:dpair('buried_wrong_color','obj-bookshelf')),
 ('D: compound fault',lambda:dpair('compound_fault','obj-chair')),
 ('M: missing roof',lambda:mpair('cottage-roof','missing')),
 ('M: extra cabin plate',lambda:mpair('racer-top','extra-layer'))], 'errors')

# Two independent recovery examples, eight images across one row.
fig=plt.figure(figsize=(7,1.03))
fig.text(.25,.98,'M racer: wrong-color repair',ha='center',va='top',fontsize=7.3,color=BLUE,fontweight='bold')
fig.text(.75,.98,'D table: cascade recovery',ha='center',va='top',fontsize=7.3,color=BLUE,fontweight='bold')
mid='racer-top';cert,manual,changes,rt,ren=data(mid);cp=cert['checkpoint']
seq=[manual['states'][cp],changes['wrong-color']['after'],manual['states'][cp],manual['states'][-1]]
for col,(state,label) in enumerate(zip(seq,['Before edit','Wrong-color spare','Remove + restore','Finish module'])):
    panel(fig,(.006+col/8,.19,.113,.57),render(mid,f'complete-trace-{col}',state))
    fig.text((col+.5)/8,.07,label,ha='center',fontsize=6.1,color=INK)
    if col<3:arrow(fig,((col+1)/8-.009,.48),((col+1)/8+.009,.48),ORANGE if col==0 else GREEN)
c,before,after=dcase('cascade_removal','obj-table');mid=c['modelId'];rt,ren,ev=dd(mid)
for col,(state,label) in enumerate(zip([before,after,before,rt.goal],['Before edit','Cascaded removal','Restore support','Finish object'])):
    panel(fig,(.506+col/8,.19,.113,.57),bankrender('D',mid,f'recovery-{col}',state))
    fig.text(.5+(col+.5)/8,.07,label,ha='center',fontsize=6.1,color=INK)
    if col<3:arrow(fig,(.5+(col+1)/8-.009,.48),(.5+(col+1)/8+.009,.48),ORANGE if col==0 else GREEN)
figsave(fig,'recovery')

# Every previous complete-object design appears in the supplement, not only a sample.
full=[r for r in COVER['models'] if r['track']=='D' and r['id'].startswith('obj-')]
mechs=[r for r in COVER['models'] if r['track']=='D' and not r['id'].startswith('obj-')]

def gallery(rows,figure_name,title,cols=7):
    nr=(len(rows)+cols-1)//cols;h=nr*.67+.30;fig=plt.figure(figsize=(7,h))
    fig.text(.01,1-.05/h,title,va='top',fontsize=8,fontweight='bold',color=BLUE)
    for i,r in enumerate(rows):
        row,col=divmod(i,cols);top=h-.28-row*.67
        im=dgoal(r['id']) if r['track']=='D' else render(r['id'],'full-target',data(r['id'])[1]['states'][-1],full=True)
        width=1/cols-.015;panel(fig,(.0075+col/cols,(top-.43)/h,width,.43/h),im)
        name=r['id'].removeprefix('obj-').removeprefix('sr4-')
        name=name.replace('alternative-release','alt. release').replace('-helicopter',' heli.').replace('-roof',' roof').replace('-tail',' tail')
        x=(col+.5)/cols
        fig.text(x,(top-.46)/h,name,ha='center',va='top',fontsize=6.1,color=INK)
        fig.text(x,(top-.57)/h,f"{r['parts']} parts / {r['cases']} cases",ha='center',va='top',fontsize=6.1,color=GRAY)
    figsave(fig,figure_name)

for gallery_name,rows,title in [(['objects-all'],full,'All 42 complete-object designs in D'),(['mechanisms-all'],mechs,'All 26 mechanism structures in D'),(['modules-all'],[r for r in COVER['models'] if r['track']=='M'],'All 12 community-source modules in M')]:
    gallery(rows,gallery_name[0],title,cols=8 if gallery_name[0]=='modules-all' else 7)

allkinds=[('removed_piece','Removed piece'),('shifted_piece','Shift'),('cascade_removal','Cascade'),('extra_layer','Extra layer'),('early_cover','Early cover'),('wrong_color','Wrong color'),('wrong_size','Wrong size'),('rotated_piece','Rotation'),('swapped_positions','Swap'),('wrong_part','Wrong type'),('buried_wrong_color','Buried color'),('compound_fault','Compound')]
pairs_figure([(label,lambda k=k:dpair(k)) for k,label in allkinds],'mechanism-errors')
def diverse_static_pair(category,preferred):
    choices=[c for c in STATIC if c['category']==category and c['modelId']==preferred]
    if not choices:choices=[c for c in STATIC if c['category']==category]
    best=None
    for c in choices[:3]:
        rt,ren,c=sd(c['publicId'])
        for view in ['isometric','rear','top']:
            a=np.asarray(ren.rgb(c['initial'],view=view,size=(480,360),supersample=1,frame_keys=['_paper_frame'])[0]).astype(np.int16)
            b=np.asarray(ren.rgb(c['goal'],view=view,size=(480,360),supersample=1,frame_keys=['_paper_frame'])[0]).astype(np.int16)
            score=int(np.count_nonzero(np.max(np.abs(a-b),axis=2)>=24))
            if best is None or score>best[0]:best=(score,c,view)
    score,c,view=best
    assert score>0
    return bankrender('S',c['publicId'],'current-'+view,c['initial'],view),bankrender('S',c['publicId'],'target-'+view,c['goal'],view),c['publicId']

static_examples=[('missing','31009'),('wrong_color','31027'),('wrong_type','v23-3179'),('wrong_size','10001'),('offset','v23-31039'),('rotation','31027-kart'),('height_layer','omr-21309'),('compound','v23-21004')]
pairs_figure([(k.replace('_',' '),lambda k=k,mid=mid:diverse_static_pair(k,mid)) for k,mid in static_examples],'legacy-static')

# Compact vector distribution plots.
from collections import Counter
counts=Counter(c['category'] for c in STATIC);dynamic=source(ROOT/'deliverables/brickplan-dynamic-v6/expansion.json')['kinds']
fig,axs=plt.subplots(1,2,figsize=(7,2.8));fig.subplots_adjust(left=.15,right=.98,bottom=.17,top=.89,wspace=.68)
for ax,c,title,color in [(axs[0],counts,'Static S (3,292)',BLUE),(axs[1],{k:v for k,v in dynamic.items() if k!='none'},'Dynamic D faults (1,712)',GREEN)]:
    keys=sorted(c,key=c.get,reverse=True);y=np.arange(len(keys));ax.barh(y,[c[k] for k in keys],color=color,height=.65)
    ax.set_yticks(y,[k.replace('_',' ') for k in keys],fontsize=6.6);ax.invert_yaxis();ax.set_title(title,fontsize=8)
    ax.spines[['top','right']].set_visible(False);ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True);ax.set_xlim(0,max(c.values())*1.20);ax.set_xlabel('Case records',fontsize=7)
    for i,k in enumerate(keys):ax.text(c[k]+max(c.values())*.025,i,str(c[k]),va='center',fontsize=6.4)
figsave(fig,'distributions')

# Archived model trajectories: exact replayed states, never synthetic outcomes.
qual=source(HERE/'evidence/repair-comparison.json');qrt=PlateAssembly(qual['certificate'])
qren=DynamicVisionRenderer(qrt.cert,qrt)
qrows=[('GT witness / extra layer / one valid order',qual['gt'])]
for trace in qual['traces']:
    title=('Model / external extra layer / different valid order' if trace['condition']=='extra_layer'
           else 'Model / normal condition / wrong placement and self-repair')
    qrows.append((title,[trace['frames'][i] for i in trace['selectedIndices']]))
frame(qren,[k for _,fs in qrows for f in fs for k in f['state'].values() if k])
def qrender(f):
    spec=dict(track='archived-v5',state=f['state'],view='isometric',size=[3200,2400],
              certificateSha=qrt.cert['contentSha256'],framing='all-shown-states-union-v1')
    key=hashlib.sha256(json.dumps(spec,sort_keys=True).encode()).hexdigest()
    path=RAW/f'archived-car--{key[:16]}.png';meta=path.with_suffix('.json')
    if not path.exists():
        im,_=qren.rgb(f['state'],view='isometric',size=(3200,2400),supersample=2,frame_keys=['_paper_frame'])
        im.save(path,optimize=True);meta.write_text(json.dumps({'key':key,'state':spec},indent=2)+'\n')
    manifest['renders'][str(path.relative_to(FIG))]=dict(sha256=hashlib.sha256(path.read_bytes()).hexdigest(),**spec)
    return np.asarray(Image.open(path).convert('RGB'))
fig=plt.figure(figsize=(7,2.62))
for row,(title,fs) in enumerate(qrows):
    top=.99-row/3
    fig.text(.01,top,title,va='top',fontsize=7.1,fontweight='bold',color=BLUE)
    for col,f in enumerate(fs):
        left=.006+col/8;center=(col+.5)/8;im=qrender(f)
        panel(fig,(left,top-.225,.113,.175),im)
        a=f['action'];name=('+' if a['type']=='attach' else '-')+a['partId'] if 'partId' in a else 'Finish'
        if f['eventOccurred']:name+=' + event'
        if row==2 and col==7:name='Finish*'
        verdict='SUCCESS' if f['feedback']=='SUCCESS' else 'EXT. FAULT' if f['eventOccurred'] else 'WRONG POSE' if f['outOfGoalPieces'] else 'VALID'
        color=ORANGE if f['eventOccurred'] else '#b52a31' if f['outOfGoalPieces'] else GREEN
        fig.text(center,top-.235,name,ha='center',va='top',fontsize=6.1,color=INK)
        fig.text(center,top-.282,verdict,ha='center',va='top',fontsize=6.0,fontweight='bold',color=color)
        fig.patches.append(Rectangle((left,top-.225),.113,.175,transform=fig.transFigure,
                                    linewidth=.6,edgecolor=color,facecolor='none'))
manifest['qualitativeComparison']=dict(source='evidence/repair-comparison.json',rows=3,columns=8,
    verifiedModelDecisions=32,referenceSteps=8,allShownEpisodesSucceed=True,formalCurrentBenchmark=False)
figsave(fig,'repair-comparison')

# Radar axes are data-bound templates. Missing measurements never become zeros.
results=source(HERE/'evidence/results-template.json')
main_axes=[('static_S_success','S static'),('static_M_success','M static'),
 ('dynamic_D_control_success','D normal'),('dynamic_D_trigger_coverage','D exposure'),
 ('dynamic_D_recovery','D recovery'),('dynamic_M_control_success','M normal'),
 ('dynamic_M_trigger_coverage','M exposure'),('dynamic_M_recovery','M recovery')]
error_axes=[(k,label.replace(' ','\n')) for k,label in allkinds]
radarspec=dict(schema='brickplan-radar-spec/1',input='evidence/results-template.json',
    inputRange=[0,1],displayRange=[0,100],missing='Omit series with any missing axis; never impute zero.',
    direction='Higher is better; exposure is protocol coverage, not detection accuracy.',
    aggregation='Source-macro estimates; show counts and clustered intervals in companion tables. No polygon-area score.',
    mainAxes=[dict(field=k,label=v) for k,v in main_axes],
    errorAxes=[dict(field=k,label=v.replace('\n',' ')) for k,v in error_axes])
(HERE/'evidence/radar-spec.json').write_text(json.dumps(radarspec,indent=2)+'\n')
source(HERE/'evidence/radar-spec.json')
def radar(name,axes,series):
    fig=plt.figure(figsize=(3.35,2.16 if name=='evaluation-radar' else 2.52))
    ax=fig.add_axes([.23,.18,.54,.68],projection='polar')
    ax.set_theta_offset(np.pi/2);ax.set_theta_direction(-1)
    theta=np.linspace(0,2*np.pi,len(axes),endpoint=False)
    ax.set_xticks(theta,[label for _,label in axes],fontsize=6.2)
    for angle,label in zip(theta,ax.get_xticklabels()):
        label.set_ha('left' if np.sin(angle)>.1 else 'right' if np.sin(angle)<-.1 else 'center')
    ax.tick_params(axis='x',pad=3);ax.set_ylim(0,100)
    ax.set_yticks([25,50,75,100],['25','50','75','100%'],fontsize=5.3,color=GRAY)
    ax.set_rlabel_position(12);ax.grid(color='#cbd5dc',linewidth=.6);ax.spines['polar'].set_color('#cbd5dc')
    plotted=[]
    for label,values in series:
        if any(v is None for v in values):continue
        assert all(isinstance(v,(int,float)) and 0<=v<=1 for v in values)
        ax.plot(np.r_[theta,theta[0]],100*np.r_[values,values[0]],label=label,lw=1.1)
        plotted.append(label)
    if not plotted:
        ax.text(.5,.5,'Awaiting\nmeasurements',transform=ax.transAxes,ha='center',va='center',
                fontsize=7,color=GRAY,bbox=dict(boxstyle='round,pad=.3',facecolor='white',edgecolor='none'))
    else:ax.legend(loc='lower center',bbox_to_anchor=(.5,-.36),ncol=3,fontsize=6,frameon=False)
    fig.text(.5,.025,'0–100%  |  unmeasured ≠ zero  |  no area-based ranking',ha='center',fontsize=6,color=GRAY)
    manifest.setdefault('radars',{})[name]=dict(axes=[k for k,_ in axes],plottedSeries=plotted,
                                               sourceStatus=results['status'],missingImputation=False)
    figsave(fig,name)
radar('evaluation-radar',main_axes,[(r['model'],[r[k] for k,_ in main_axes]) for r in results['main']])
errorrows={r['error']:r for r in results['perError']}
radar('error-radar',error_axes,[(m['id'],[errorrows[k][m['id']] for k,_ in error_axes]) for m in results['models']])
manifest['sources'][str(Path(__file__).relative_to(ROOT))]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
(FIG/'provenance.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('DONE',len(manifest['figures']),'figures',len(manifest['renders']),'native renders',flush=True)
