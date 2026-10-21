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


labels=['Cottage / roof','Racer / cabin','Seaplane / tail','Museum / roof',
        'Repair truck / lights','Helicopter / tail','Police aircraft / rotor','Panda / head',
        'Burger stand / sign','White House / chimneys','Rockefeller / crown','Brandenburg / crest']
fig=plt.figure(figsize=(7.0,3.25))
for i,m in enumerate(modules):
    cert,manual,*_=data(m['id']);im=render(m['id'],'full-target',manual['states'][-1],full=True)
    row,col=divmod(i,4);ax=panel(fig,(.01+col*.25,.70-row*.31,.235,.25),im)
    ax.text(.5,-.04,labels[i],transform=ax.transAxes,ha='center',fontsize=7.3,color=INK)
    ax.text(.5,-.20,f"{m['remaining']} remaining parts",transform=ax.transAxes,ha='center',fontsize=6.8,color=GRAY)
figsave(fig,'teaser')

# End-to-end protocol: vector workflow and a genuine temporal observation.
fig=plt.figure(figsize=(7,2.9))
for x,title,body,color in [(0.02,'Task inputs','Fixed goal + reference manual\nInventory + current RGB',BLUE),
                           (.35,'One physical action','Attach / detach one brick\nInspect or finish',GREEN),
                           (.68,'World update','Check geometry and motion\nApply a feasible hidden edit',ORANGE)]:
    box(fig,(x,.72,.29,.21),title,body,color)
arrow(fig,(.315,.825),(.343,.825));arrow(fig,(.645,.825),(.673,.825))
cert,manual,changes,*_=data('racer-top');cp=cert['checkpoint']
imgs=[render('racer-top','protocol-before',manual['states'][cp-1]),
      render('racer-top','protocol-current',changes['extra-layer']['after']),
      render('racer-top','protocol-target',manual['states'][-1])]
for col,(im,label) in enumerate(zip(imgs,['Before the last action','Actual current state','Fixed acceptance target'])):
    panel(fig,(.02+col*.33,.10,.29,.52),im,label)
fig.text(.5,.015,'Observe the real state after every action. No error label or correction is returned.',ha='center',fontsize=8,color=INK)
arrow(fig,(.825,.705),(.495,.705),ORANGE)  # World update leads to actual current RGB, not the fixed target.
figsave(fig,'protocol')

# Matched stage targets and faults in three different physical objects.
fig=plt.figure(figsize=(7,3.8))
examples=[('cottage-roof','missing','Missing roof brick'),('panda-head','wrong-color','Wrong-color head brick'),('racer-top','extra-layer','Extra cabin plate')]
audit=source(OUT/'audit.json')
for col,(mid,family,label) in enumerate(examples):
    cert,manual,changes,*_=data(mid);cp=cert['checkpoint']
    result=next(r for r in audit['results'] if r['module']==mid)
    vis=next(v for v in result['visibility'] if v['family']==family)
    view='rear' if mid == 'panda-head' else 'isometric'  # Show the replaced head brick without occlusion.
    assert vis['changedPixels'][view] >= 128
    current=render(mid,'error-'+family,changes[family]['after'],view)
    target=render(mid,'stage-'+family,manual['states'][cp],view)
    ax=panel(fig,(.015+col*.333,.54,.31,.35),current,label,color=ORANGE)
    diff=np.max(np.abs(current.astype(np.int16)-target.astype(np.int16)),axis=2)>=24
    ys,xs=np.nonzero(diff)
    ax.add_patch(Rectangle((xs.min()-18,ys.min()-18),xs.max()-xs.min()+36,ys.max()-ys.min()+36,
                           linewidth=1.1,edgecolor=ORANGE,facecolor='none'))
    panel(fig,(.015+col*.333,.06,.31,.35),target,'Correct stage target',color=GREEN)
fig.text(.5,.46,'Current faulty state (top)  /  acceptance target at the same view (bottom)',ha='center',fontsize=7.8,color=INK)
figsave(fig,'errors')

# Reference assembly instructions, including the exact part to manipulate.
mid='repair-truck-cab';cert,manual,*_=data(mid)
fig=plt.figure(figsize=(7,2.35))
for i,a in enumerate(manual['actions']):
    part=render(mid,f'manual-piece-{i+1}',{a['actor']:a['candidate']},only=a['actor'])
    state=render(mid,f'manual-after-{i+1}',manual['states'][i+1],highlight=a['actor'])
    panel(fig,(.015+i*.20,.64,.17,.25),part,f'Reference {i+1}')
    panel(fig,(.005+i*.20,.08,.19,.52),state)
    if i<4:arrow(fig,(.19+i*.2,.34),(.21+i*.2,.34))
fig.text(.5,.02,'One brick per action. Orange outlines explain this reference manual; they are not fault labels.',ha='center',fontsize=7.2,color=INK)
figsave(fig,'instructions')

# A concrete two-route example at the same occupancy, sharing the final goal.
mid='cottage-roof';cert,manual,changes,rt,*_=data(mid)
ref=manual['states'][3];alt=dict(manual['states'][2]);a=manual['actions'][3];alt,res=rt.check(alt,a['actor'],'attach',candidate=a['candidate']);assert res['code']=='OK'
fig=plt.figure(figsize=(7,2.45))
for col,(state,name,label) in enumerate([(ref,'route-a','Route A: pieces 1, 2, 3'),(alt,'route-b','Route B: pieces 1, 2, 4'),(manual['states'][-1],'route-goal','Same completed target')]):
    panel(fig,(.01+col*.335,.17,.31,.72),render(mid,name,state),label)
fig.text(.325,.51,'≠',fontsize=16,ha='center',color=ORANGE)
arrow(fig,(.64,.48),(.68,.48),GREEN)
fig.text(.5,.04,'Different intermediate states are valid. Only legal actions and terminal equivalence determine completion.',ha='center',fontsize=7.6,color=INK)
figsave(fig,'alternative-orders')

# A complete hidden-event / recovery / completion trajectory, not an API result.
mid='racer-top';cert,manual,changes,rt,renderer=data(mid)
case=next(c for c in source(OUT/mid/'cases.private.json') if c['id'].endswith('dynamic-wrong-color'))
cp=cert['checkpoint'];states=[manual['states'][cp],changes['wrong-color']['after'],manual['states'][cp],manual['states'][-1]]
fig=plt.figure(figsize=(7,2.05))
for col,(s,label) in enumerate(zip(states,['Before intervention','Hidden color replacement','Repair: remove + restore','Continue to the fixed goal'])):
    panel(fig,(.005+col*.25,.12,.235,.72),render(mid,f'complete-trace-{col}',s),label)
    if col<3:arrow(fig,(.235+col*.25,.45),(.26+col*.25,.45),ORANGE if col==0 else GREEN)
fig.text(.5,.025,'Certified reference replay. The replacement uses two environment primitives; each agent action still moves one brick.',ha='center',fontsize=7.0,color=INK)
figsave(fig,'recovery')

# The legacy static figures are also rerendered, never enlarged from old PNGs.
from plate5_eval import load
fig=plt.figure(figsize=(7,3.45))
for col,(qid,label) in enumerate([('S01609','Color substitution'),('S00254','Orientation error'),('S00001','Compound repair')]):
    rt,case=load(qid);ren=DynamicVisionRenderer(rt.cert,rt)
    source((ROOT/'deliverables/brickplan-static-held4/combined'/case['qualificationFile']).resolve())
    for row,(role,state) in enumerate([('current',case['initial']),('target',case['goal'])]):
        image,_=ren.rgb(state,size=(3200,2400),supersample=2)
        path=RAW/f'legacy-{qid}-{role}.png';image.save(path,optimize=True)
        manifest['renders'][str(path.relative_to(FIG))]=dict(sha256=hashlib.sha256(path.read_bytes()).hexdigest(),publicId=qid,role=role,size=[3200,2400],protocol='connector-workbench/5-white-baseplate')
        panel(fig,(.015+col*.333,.53-row*.45,.31,.36),np.asarray(image),label if row==0 else 'Acceptance target')
figsave(fig,'legacy-static')
for name in ['cases.jsonl','summary.json','replay-audit.json']:
    p=ROOT/'deliverables/brickplan-static-plate5'/name;manifest['sources'][str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()

# Exact corpus counts as vector plots, with source provenance.
static=[json.loads(line) for line in (ROOT/'deliverables/brickplan-static-plate5/cases.jsonl').open()]
from collections import Counter
counts=Counter(c['category'] for c in static)
dynamic=source(ROOT/'deliverables/brickplan-dynamic-v6/expansion.json')['kinds']
fig,axs=plt.subplots(1,2,figsize=(7,3.4))
fig.subplots_adjust(left=.15,right=.98,bottom=.16,top=.88,wspace=.68)
for ax,c,title,color in [(axs[0],counts,'Static geometry bank (3,292)',BLUE),(axs[1],{k:v for k,v in dynamic.items() if k!='none'},'Dynamic interventions (1,712)',GREEN)]:
    keys=sorted(c,key=c.get,reverse=True);y=np.arange(len(keys));ax.barh(y,[c[k] for k in keys],color=color,height=.65)
    ax.set_yticks(y,[k.replace('_',' ') for k in keys],fontsize=6.7);ax.invert_yaxis();ax.set_title(title,fontsize=8)
    ax.spines[['top','right']].set_visible(False);ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True)
    ax.set_xlim(0,max(c.values())*1.20);ax.set_xlabel('Instances, not independent objects',fontsize=7)
    for i,k in enumerate(keys):ax.text(c[k]+max(c.values())*.025,i,str(c[k]),va='center',fontsize=6.6)
figsave(fig,'distributions')
manifest['sources'][str(Path(__file__).relative_to(ROOT))]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
(FIG/'provenance.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('DONE',len(manifest['figures']),'figures',len(manifest['renders']),'native renders',flush=True)
