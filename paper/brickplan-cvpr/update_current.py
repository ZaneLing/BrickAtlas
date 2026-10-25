"""Build publication assets from the organized dataset; no model API calls.

Historical figures and route diagnostics remain versioned in figures-v2/evidence.
This script never regenerates the dataset or edits historical experiment evidence.
"""
from pathlib import Path
from collections import Counter
import hashlib, json, sys, re
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image
from figure_typography import configure

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SPEC = ROOT/'deliverables/brickplan-benchmark-spec'
FIG = HERE/'figures-current'
sys.path.insert(0, str(ROOT/'benchmark/brickplan-repair'))
from bench_design.catalogue import rows_with_cases, module_runtime
from community_modules.core import render_certificate
from community_modules.run_episode import PALETTE
from dynamic_v5.vision import DynamicVisionRenderer

def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p, d): p.write_text(json.dumps(d, indent=2, ensure_ascii=False)+'\n')
def tex(s): return str(s).replace('_', r'\_').replace('&', r'\&')

FIG.mkdir(exist_ok=True)
(FIG/'native').mkdir(exist_ok=True)
rows = [json.loads(l) for l in (SPEC/'questions.jsonl').read_text().splitlines()]
unique = [r for r in rows if not r['isAlias']]
main = [r for r in unique if r['mainTaskCandidate']]
dynamic = [r for r in main if r['mode']=='dynamic']
configs = {r['model']: r for r in dynamic}
raw = {r['key']:r for r in rows_with_cases()}
provenance = dict(schema='brickplan-current-paper-figures/1', date='2026-10-25',
    renderPixels=[3200,2400], supersampling=2, exportDpi=600,
    vectorText=True, sources={}, renders={}, figures={}, apiCalls=0)
for p in [SPEC/'questions.jsonl',SPEC/'summary.json',SPEC/'coverage.json',SPEC/'examples.json']:
    provenance['sources'][str(p.relative_to(ROOT))]=sha(p)
provenance['typography']=configure(8)
BLUE='#2166ac'; GREEN='#167d72'; ORANGE='#c75c19'; INK='#162e3c'; GRAY='#63727b'
PALETTE.update(dict(re.findall(r'CODE\s+(\d+)\s+VALUE\s+(#[0-9A-Fa-f]{6})',
    (ROOT/'assets-source/ldraw-library/locked/LDConfig.ldr').read_text())))

def save(fig,name):
    for ext in ['pdf','svg','png']:
        path=FIG/f'{name}.{ext}'
        fig.savefig(path, dpi=600, facecolor='white')
        if ext=='svg':path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines())+'\n')
    provenance['figures'][name]=dict(inches=list(fig.get_size_inches()),
        pdfSha256=sha(FIG/f'{name}.pdf'), formats=['pdf','svg','png'])
    plt.close(fig)
    print('FIGURE',name,flush=True)

def panel(fig,box,im):
    ax=fig.add_axes(box);ax.imshow(im,interpolation='none');ax.axis('off');return ax

cache={}
def render(row,state,label,full=False):
    key=(row['bank'],row['model'])
    if key not in cache:
        rt=module_runtime(*key);ren=DynamicVisionRenderer(render_certificate(rt.cert),rt)
        keys=[k for k,r in rt.cert['candidates'].items() if r['kind']=='goal']
        if full: keys+=list(ren.cert['fixed'])
        points=np.concatenate([ren.bounds[k] for k in keys])
        lo,hi=points.min(0)-[20,28,20],points.max(0)+[20,20,20]
        ren.bounds['_paper_frame']=np.array([[x,y,z] for x in (lo[0],hi[0]) for y in (lo[1],hi[1]) for z in (lo[2],hi[2])])
        cache[key]=(rt,ren)
    rt,ren=cache[key]
    spec=dict(bank=key[0],model=key[1],state=state,size=[3200,2400],fullContext=full,
        certificateSha256=hashlib.sha256(json.dumps(rt.cert,sort_keys=True).encode()).hexdigest())
    token=hashlib.sha256(json.dumps(spec,sort_keys=True).encode()).hexdigest()
    path=FIG/'native'/f'{row["model"]}-{label}-{token[:12]}.png'
    if not path.exists():
        image,_=ren.rgb(state,'isometric',size=(3200,2400),supersample=2,frame_keys=['_paper_frame'])
        image.save(path,optimize=True)
    provenance['renders'][str(path.relative_to(FIG))]=dict(**spec,sha256=sha(path))
    return np.asarray(Image.open(path).convert('RGB'))

oldprov=read(HERE/'figures-v2/provenance.json')
def oldimage(name):
    p=HERE/'figures-v2/native'/name
    provenance['sources'][str(p.relative_to(ROOT))]=sha(p)
    return np.asarray(Image.open(p).convert('RGB'))

def goal(mid):
    row=raw[next(r['id'] for r in dynamic if r['model']==mid)]
    rt=module_runtime(row['bank'],mid)
    return render(row,rt.goal,'goal',full=mid=='museum-roof-long')

def gallery(items,name,title,cols=7):
    nrows=(len(items)+cols-1)//cols;h=nrows*.73+.25
    fig=plt.figure(figsize=(7,h));fig.text(.01,.98,title,color=BLUE,weight='bold',va='top',fontsize=8)
    for i,(label,subtitle,im) in enumerate(items):
        r,c=divmod(i,cols);top=h-.27-r*.73;x=(c+.5)/cols
        panel(fig,(c/cols+.007,(top-.46)/h,1/cols-.014,.46/h),im)
        fig.text(x,(top-.48)/h,label,ha='center',va='top',fontsize=6.0,color=INK)
        fig.text(x,(top-.60)/h,subtitle,ha='center',va='top',fontsize=5.9,color=GRAY)
    save(fig,name)

# Eight panels per row retain the established compact paper layout.
static_ids=['10001','31009','31027','31028','v23-31039','v23-21004','omr-21309','v23-3179']
scases=[json.loads(l) for l in (ROOT/'deliverables/brickplan-static-plate5/cases.jsonl').read_text().splitlines()]
static_images=[]
for mid in static_ids:
    c=next(c for c in scases if c['modelId']==mid and not c['oraclePlan'])
    static_images.append((mid.removeprefix('v23-').removeprefix('omr-'),oldimage(f'S-{c["publicId"]}--target.png')))
object_images=[(mid.removeprefix('obj-'),oldimage(f'D-{mid}--goal.png')) for mid in ['obj-chair','obj-table','obj-city-car','obj-crane']]
object_images += [(label,goal(mid)) for mid,label in [('whole-4018','4018 ship'),('whole-4017','4017 heli.'),('whole-4037','4037 heli.'),('v7-long-city-bus','32-part bus')]]
module_ids=['cottage-roof','racer-top','seaplane-tail','museum-roof','repair-truck-cab','panda-head','white-house-roof','brandenburg-top']
module_images=[(mid.split('-')[0],oldimage(f'{mid}--full-target.png')) for mid in module_ids]
fig=plt.figure(figsize=(7,2.10))
sections=[('Static repair: 3,697 main candidates; local structures and object stages',static_images),
 ('Whole-object construction: 50 configurations; 1,534 dynamic tasks',object_images),
 ('Named remaining modules: 13 configurations; 221 dynamic tasks',module_images)]
for row,(title,items) in enumerate(sections):
    top=.99-row/3;fig.text(.01,top,title,color=BLUE,weight='bold',va='top',fontsize=7.3)
    for col,(label,im) in enumerate(items):
        panel(fig,(.006+col/8,top-.265,.113,.21),im)
        fig.text((col+.5)/8,top-.27,label,ha='center',va='top',fontsize=6.1,color=INK)
save(fig,'teaser')

# All seven atomic classes, process burdens, and a no-error control.
examples=read(SPEC/'examples.json')
labels=['E01 Missing','E02 Extra','E03 Color','E04 Part','E05 Offset','E06 Orientation','E07 Swap','P01 Early cover','P02 Buried repair','S0 Correct']
fig=plt.figure(figsize=(7,2.85))
for i,(example,title) in enumerate(zip(examples,labels)):
    row=raw[example['id']];c=row['case'];a=render(row,c['initial'],'current-'+example['code']);b=render(row,c['goal'],'target-'+example['code'])
    rr,cc=divmod(i,4);top=1-rr/3;left=cc/4+.006;bottom=top-.282
    fig.text(left+.119,top-.008,title,ha='center',va='top',fontsize=7.1,weight='bold',color=INK)
    ax=panel(fig,(left,bottom+.05,.115,.205),a);panel(fig,(left+.121,bottom+.05,.115,.205),b)
    diff=np.max(np.abs(a.astype(np.int16)-b.astype(np.int16)),axis=2)>=24;yy,xx=np.nonzero(diff)
    if len(xx):ax.add_patch(Rectangle((xx.min()-10,yy.min()-10),xx.max()-xx.min()+20,yy.max()-yy.min()+20,fill=False,edgecolor=ORANGE,linewidth=.8))
    fig.text(left+.058,bottom+.027,'Current',ha='center',fontsize=6.2,color=ORANGE)
    fig.text(left+.179,bottom+.027,'Stage target',ha='center',fontsize=6.2,color=GREEN)
    provenance.setdefault('shownCases',{})[example['code']]=example['id']
# Last two cells explain temporal errors without fictitious images.
fig.text(.625,.22,'T2: two separated accidents\nT3: three separated accidents\nRepair and continue without prompts',ha='center',va='center',fontsize=6.5,color=BLUE,linespacing=1.6)
fig.text(.875,.22,'Final geometry is scored.\nReference order is optional.\nPaper boxes are annotations only.',ha='center',va='center',fontsize=6.8,color=GRAY,linespacing=1.5)
save(fig,'errors')

extra=[('whole-4018','4018 ship'),('whole-4017','4017 sea heli.'),('whole-4037','4037 mini heli.'),
 ('v7-long-bookshelf','Bookshelf'),('v7-long-city-bus','City bus'),('v7-long-stone-bridge','Stone bridge'),
 ('v7-long-gantry-press','Gantry press'),('v7-long-cottage','Cottage'),('museum-roof-long','Museum roof +')]
gallery([(label,f'{configs[mid]["activeParts"]} parts / '+str(sum(r['model']==mid for r in dynamic))+' D tasks',goal(mid)) for mid,label in extra],
        'added-objects','Three complete original LDraw models, five longer objects, and an enlarged roof',cols=7)

# Update the old galleries' counts without re-rendering their native geometry.
oldcover=read(HERE/'evidence/benchmark-coverage.json')['models']
for name,predicate,title in [('objects-all',lambda r:r['track']=='D' and r['id'].startswith('obj-'),'42 retained procedural complete objects / distinct dynamic tasks'),
 ('mechanisms-all',lambda r:r['track']=='D' and not r['id'].startswith('obj-'),'26 historical structural configurations / diagnostic only'),
 ('modules-all',lambda r:r['track']=='M','12 original community modules / combined M and expansion tasks')]:
    items=[]
    for r in filter(predicate,oldcover):
        mid=r['id'];n=sum(q['model']==mid and (q['mode']=='dynamic' if r['track']=='D' else True) for q in unique)
        image=oldimage(f'D-{mid}--goal.png' if r['track']=='D' else f'{mid}--full-target.png')
        label=mid.removeprefix('obj-').removeprefix('sr4-').replace('alternative-release','alt. release')
        label=label.replace('-helicopter',' heli.').replace('-roof',' roof').replace('-tail',' tail')
        items.append((label,f'{r["parts"]} parts / {n} tasks',image))
    gallery(items,name,title,8 if name=='modules-all' else 7)

fig,axs=plt.subplots(1,3,figsize=(7,1.65));fig.subplots_adjust(left=.06,right=.99,bottom=.28,top=.82,wspace=.42)
for ax,field,title,keys in [(axs[0],'taskType','Main task types',['S0','S1','D0','D1','D2']),
 (axs[1],'planningLevel','Planning grades (not empirical)',['G1','G2','G3']),
 (axs[2],'eventLevel','Dynamic event counts',['T0','T1','T2','T3'])]:
    pool=dynamic if field=='eventLevel' else main;c=Counter(r[field] for r in pool);v=[c[k] for k in keys]
    ax.bar(keys,v,color=[BLUE,GREEN,ORANGE,GRAY,BLUE][:len(keys)],width=.6)
    ax.set_title(title,fontsize=7);ax.spines[['top','right']].set_visible(False);ax.tick_params(labelsize=6)
    ax.set_ylim(0,max(v)*1.25)
    for i,n in enumerate(v):ax.text(i,n+max(v)*.04,f'{n:,}',ha='center',fontsize=6.4)
save(fig,'distributions')

for name,labels in [('evaluation-radar',['S1 SR','Placement F1','1 - DR','1 - FR','D0 BCR','D1 CRR','D2 CRR','Retention']),
 ('error-radar',['E01 Missing','E02 Extra','E03 Color','E04 Part','E05 Offset','E06 Orientation','E07 Swap'])]:
    fig=plt.figure(figsize=(3.35,2.2));ax=fig.add_axes([.24,.19,.52,.67],projection='polar')
    ax.set_theta_offset(np.pi/2);ax.set_theta_direction(-1);theta=np.linspace(0,2*np.pi,len(labels),endpoint=False)
    ax.set_xticks(theta,labels,fontsize=6);ax.tick_params(axis='x',pad=4);ax.set_ylim(0,100)
    ax.set_yticks([25,50,75,100],['25','50','75','100%'],fontsize=5.3,color=GRAY)
    ax.grid(color='#cbd5dc',linewidth=.6);ax.spines['polar'].set_color('#cbd5dc')
    ax.text(.5,.5,'Unmeasured',transform=ax.transAxes,ha='center',va='center',fontsize=7,color=GRAY,bbox=dict(facecolor='white',edgecolor='none'))
    fig.text(.5,.025,'No missing-value imputation; no polygon-area ranking',ha='center',fontsize=6,color=GRAY)
    provenance.setdefault('radars',{})[name]=dict(labels=labels,plottedSeries=[],missingImputation=False)
    save(fig,name)

# Current data-derived inventories replace stale raw-case counts.
inventory=[]
smodels=sorted({r['model'] for r in unique if r['bank']=='S'})
for page in range(2):
    inventory += [r'\begin{table*}[p]',r'\centering\footnotesize',
        r'\caption{\textbf{Static source configuration inventory ('+str(page+1)+r'/2).} P: stage target parts; Q: distinct tasks after within-contract deduplication. All 160 configurations remain; Q sums to 3,265 across both tables.}',
        r'\begin{tabular}{@{}llrr@{\qquad}llrr@{}}',r'\toprule',r'Index & Configuration & P & Q & Index & Configuration & P & Q\\',r'\midrule']
    for j in range(40):
        entries=[]
        for i in [page*80+j,page*80+40+j]:
            mid=smodels[i];rs=[r for r in unique if r['bank']=='S' and r['model']==mid];ps=sorted({r['gradingParts'] for r in rs})
            p=str(ps[0]) if len(ps)==1 else f'{ps[0]}--{ps[-1]}'
            entries.append(f'S{i+1:03d} & \\texttt{{{tex(mid)}}} & {p} & {len(rs)}')
        inventory.append(' & '.join(entries)+r'\\')
    inventory += [r'\bottomrule',r'\end{tabular}',r'\end{table*}']
(HERE/'static-inventory.tex').write_text('\n'.join(inventory)+'\n')

for page in range(2):
    mids=list(configs)[page*32:(page+1)*32]
    lines=[r'\begin{table}[!ht]',r'\centering\footnotesize',
        r'\caption{\textbf{All main dynamic operation configurations ('+str(page+1)+r'/2).} W: whole object; M: named remaining module. Counts are distinct dynamic tasks. Sibling static tasks and diagnostic structures are excluded.}',
        r'\begin{tabularx}{\textwidth}{@{}Xcrrrrr@{}}',r'\toprule',r'Configuration & Scope & Parts & D0 & D1 & D2 & Total\\',r'\midrule']
    for mid in mids:
        rs=[r for r in dynamic if r['model']==mid];c=Counter(r['taskType'] for r in rs)
        lines.append(f'\\texttt{{{tex(mid)}}} & '+('W' if rs[0]['track']=='whole-object-dynamic' else 'M')+f' & {rs[0]["activeParts"]} & {c["D0"]} & {c["D1"]} & {c["D2"]} & {len(rs)}'+r'\\')
    lines += [r'\bottomrule',r'\end{tabularx}',r'\end{table}']
    (HERE/f'dynamic-inventory-{page+1}.tex').write_text('\n'.join(lines)+'\n')

sourcefiles=[p for p in SPEC.iterdir() if p.suffix in ('.json','.jsonl','.md','.csv') and p.name not in ('results-template.csv',)]
codefiles=list((ROOT/'benchmark/brickplan-repair/bench_design').glob('*.py'))
snapshot=dict(schema='brickplan-current-paper-snapshot/1',date='2026-10-25',
    counts=read(SPEC/'summary.json'),coverage=read(SPEC/'coverage.json'),
    mainStatic=sum(r['mode']=='static' for r in main),mainDynamic=len(dynamic),
    diagnosticDynamic=len(unique)-len(main),mainSourceSplit=dict(Counter(r['sourceSplit'] for r in main)),
    testMainTaskTypes=dict(Counter(r['taskType'] for r in main if r['sourceSplit']=='test-existing-source')),
    files={str(p.relative_to(ROOT)):sha(p) for p in sourcefiles+codefiles},
    resultStatus='NOT_RUN',apiCalls=0)
write(HERE/'evidence/current-dataset.json',snapshot)
provenance['sources'][str(Path(__file__).relative_to(ROOT))]=sha(Path(__file__))
provenance['sources'][str((HERE/'figure_typography.py').relative_to(ROOT))]=sha(HERE/'figure_typography.py')
write(FIG/'provenance.json',provenance)
print('CURRENT',len(unique),'distinct;',len(main),'main;',len(configs),'dynamic configurations',flush=True)
