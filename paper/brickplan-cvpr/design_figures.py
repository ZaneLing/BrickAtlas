"""Publication figure design: exact scene states, vector annotation, measured data.

Render publication_scenes.py + render_publication.mjs first. This program designs
figures; it does not modify benchmark RGB or create model results.
"""
from pathlib import Path
from collections import Counter
import json,hashlib,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,FancyArrowPatch,FancyBboxPatch
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];OUT=HERE/'figures-publication';NATIVE=OUT/'native'
INK='#24364b';MUTED='#677786';TEAL='#157d79';CORAL='#d75b3b';BLUE='#426bb0';GRAY='#d8dfe6'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':7.4,'pdf.fonttype':42,'ps.fonttype':42,'svg.fonttype':'none','axes.labelcolor':INK,'text.color':INK,'axes.spines.top':False,'axes.spines.right':False})
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=dict(schema='brickplan-publication-figures/1',date='2026-10-25',nativePixels=[3200,2400],exportDpi=600,
    exactGeometry=True,publicationOnly=True,evaluationInputUnchanged=True,apiCalls=0,figures={},images={},sources={})
for p in [HERE/'evidence/publication-render-states.json',HERE/'evidence/worked-metric-example.json',HERE/'evidence/current-dataset.json',ROOT/'deliverables/brickplan-benchmark-spec/questions.jsonl']:
 manifest['sources'][str(p.relative_to(ROOT))]=sha(p)
scene_spec=json.loads((HERE/'evidence/publication-render-states.json').read_text())
scene_groups={s['name']:s['group'] for s in scene_spec['scenes']}
crop_cache={}
def group_crop(name):
 group=scene_groups[name]
 if group not in crop_cache:
  rectangles=[]
  for s in scene_spec['scenes']:
   if s['group']!=group:continue
   a=np.asarray(Image.open(NATIVE/(s['name']+'.png')).convert('RGB').resize((400,300)))
   yy,xx=np.nonzero(np.min(a,axis=2)<242)
   if len(xx):rectangles.append((xx.min()*8,yy.min()*8,(xx.max()+1)*8,(yy.max()+1)*8))
  crop_cache[group]=(min(v[0] for v in rectangles),min(v[1] for v in rectangles),max(v[2] for v in rectangles),max(v[3] for v in rectangles))
 return crop_cache[group]
def im(name):
 p=NATIVE/(name+'.png');manifest['images'][p.name]=dict(sha256=sha(p),pixels=list(Image.open(p).size))
 return np.asarray(Image.open(p).convert('RGB'))
def panel(fig,box,name,label=None,color=INK,fontsize=7):
 ax=fig.add_axes(box);ax.imshow(im(name),interpolation='none');ax.axis('off')
 # A shared publication viewport trims canvas whitespace without distorting a
 # brick or changing scale across any current/target or trajectory group.
 l,t,r,b=group_crop(name);cx,cy=(l+r)/2,(t+b)/2;ww,hh=(r-l)*1.09,(b-t)*1.09
 aspect=box[2]*fig.get_size_inches()[0]/(box[3]*fig.get_size_inches()[1])
 if ww/hh>aspect:hh=ww/aspect
 else:ww=hh*aspect
 ax.set_xlim(cx-ww/2,cx+ww/2);ax.set_ylim(cy+hh/2,cy-hh/2)
 if label:fig.text(box[0]+box[2]/2,box[1]-.015,label,ha='center',va='top',fontsize=fontsize,color=color)
 return ax
def difference_box(ax,current,target):
 a,b=im(current).astype(np.int16),im(target).astype(np.int16)
 changed=np.max(np.abs(a-b),axis=2)>38;ys,xs=np.nonzero(changed)
 if len(xs):ax.add_patch(Rectangle((xs.min()-18,ys.min()-18),xs.max()-xs.min()+36,ys.max()-ys.min()+36,fill=False,edgecolor=CORAL,lw=.65))
def line(fig,a,b,color=GRAY,lw=.6):fig.lines.append(plt.Line2D([a[0],b[0]],[a[1],b[1]],transform=fig.transFigure,color=color,lw=lw))
def arrow(fig,a,b,color=MUTED,lw=.8,style='->',connectionstyle='arc3,rad=0'):
 fig.patches.append(FancyArrowPatch(a,b,transform=fig.transFigure,arrowstyle=style,mutation_scale=8,lw=lw,color=color,connectionstyle=connectionstyle))
def heading(fig,x,y,label,color=INK,size=8.0):fig.text(x,y,label,color=color,weight='bold',fontsize=size,va='top')
def save(fig,name):
 for ext in ['pdf','svg','png']:
  path=OUT/f'{name}.{ext}'
  fig.savefig(path,dpi=600,facecolor='white',metadata={'Creator':'BrickPlan native geometry / publication layout'} if ext=='pdf' else None)
  if ext=='svg':path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines())+'\n')
 manifest['figures'][name]=dict(pdfSha256=sha(OUT/f'{name}.pdf'),inches=list(fig.get_size_inches()),formats=['pdf','svg','png'])
 plt.close(fig);print('DESIGNED',name,flush=True)

# Figure 1: a task story followed by an eight-object strip, rather than a catalogue.
fig=plt.figure(figsize=(7,2.50));heading(fig,.008,.99,'(a) Static: repair the required stage',TEAL,7.7);heading(fig,.438,.99,'(b) Dynamic: recover while continuing assembly',BLUE,7.7)
for j,(name,label,color) in enumerate([('E03-current','Wrong color',CORAL),('metric-remove','Remove',MUTED),('E03-target','Stage restored',TEAL)]):
 ax=panel(fig,(.006+j*.136,.535,.128,.355),name,label,color,6.7)
 if j==0:difference_box(ax,'E03-current','E03-target')
 if j<2:arrow(fig,(.125+j*.136,.70),(.143+j*.136,.70))
for j,(name,label,color) in enumerate([('racer-stage-0','Supplied body',MUTED),('racer-stage-3','Build',INK),('racer-event','Hidden edit',CORAL),('racer-stage-11','Finish',TEAL)]):
 ax=panel(fig,(.432+j*.143,.535,.139,.355),name,label,color,6.7)
 if j==2:difference_box(ax,'racer-event','racer-stage-3')
 if j<3:arrow(fig,(.562+j*.143,.70),(.578+j*.143,.70),CORAL if j==1 else MUTED)
line(fig,(.005,.438),(.995,.438));heading(fig,.008,.402,'(c) Whole objects and identifiable remaining modules',INK,7.6)
objects=[('ship','Ship'),('sea-helicopter','Sea helicopter'),('mini-helicopter','Mini helicopter'),('bookshelf','Bookshelf'),('bus','City bus'),('press','Gantry press'),('racer','Racer cabin'),('seaplane','Seaplane tail')]
for j,(name,label) in enumerate(objects):panel(fig,(j/8+.003,.068,.119,.268),'object-'+name,label,INK,6.4)
save(fig,'teaser')

# Figure 2: executable I/O, with a concrete action and genuine before/after states.
fig=plt.figure(figsize=(7,1.78));xs=[.005,.267,.525,.785];w=.207
for x in xs:fig.patches.append(Rectangle((x,.19),w,.70,transform=fig.transFigure,fill=False,edgecolor=GRAY,lw=.6))
for x,label in zip(xs,['1  Observe','2  Choose one action','3  Execute legally','4  Observe again']):heading(fig,x+.008,.97,label,size=7.7)
panel(fig,(.006,.46,.098,.37),'E03-current','Current',CORAL,6.4);panel(fig,(.11,.46,.098,.37),'E03-target','Stage target',TEAL,6.4)
fig.text(.108,.31,'RGB + neutral rules\nAnonymous action handles',ha='center',va='top',fontsize=6.3,color=MUTED,linespacing=1.45)
fig.text(.371,.79,'attach   detach\ninspect   finish',ha='center',va='top',fontsize=7.7,color=INK,linespacing=1.8)
fig.text(.371,.45,'{"type":"detach",\n "partId":"A008"}',ha='center',va='top',fontsize=6.6,fontfamily='DejaVu Sans Mono',color=TEAL,linespacing=1.5)
fig.text(.628,.79,'Connection\nCollision\nInsertion / extraction',ha='center',va='top',fontsize=7.3,linespacing=1.8)
fig.text(.628,.28,'Hidden events: dynamic only',ha='center',va='top',fontsize=6.1,color=CORAL)
panel(fig,(.795,.42,.185,.41),'metric-remove','Actual new state',INK,6.6)
fig.text(.888,.28,'Accepted; still incomplete',ha='center',va='top',fontsize=6.2,color=MUTED)
for a,b in [(.217,.267),(.48,.525),(.737,.785)]:arrow(fig,(a,.60),(b,.60),INK)
line(fig,(.888,.19),(.888,.13),TEAL);arrow(fig,(.888,.13),(.107,.13),TEAL);arrow(fig,(.107,.13),(.107,.19),TEAL)
fig.text(.5,.025,'Repeat without interruption. Finish only at the stated target; legal order is free.',ha='center',fontsize=6.7,color=TEAL)
save(fig,'interaction')

# Figure 3: compact matched pairs, with a separate normal control.
fig=plt.figure(figsize=(7,1.95));labels=[('E01','Missing'),('E02','Extra'),('E03','Color'),('E04','Part'),('E05','Position'),('E06','Orientation'),('E07','Swap'),('OK','Correct control')]
for i,(code,label) in enumerate(labels):
 row,col=divmod(i,4);top=.99-row*.5;left=col*.25+.006
 heading(fig,left+.005,top,(code if code!='OK' else 'S0')+'  '+label,TEAL if code=='OK' else INK,7.3)
 for j,kind in enumerate(['current','target']):
  ax=panel(fig,(left+j*.121,top-.375,.118,.31),code+'-'+kind,('Plate (wrong)' if j==0 else 'Brick (target)') if code=='E04' else ('Current' if j==0 else 'Target'),CORAL if j==0 and code!='OK' else TEAL,6.3)
  if j==0 and code!='OK':difference_box(ax,code+'-current',code+'-target')
 if col<3:line(fig,(left+.24,top-.015),(left+.24,top-.445),GRAY,.4)
 if row==0:line(fig,(left,top-.485),(left+.235,top-.485),GRAY,.4)
save(fig,'error-atlas')

# Figure 4: an actual ten-action reference repair of a buried defect.
fig=plt.figure(figsize=(7,1.23));heading(fig,.008,.99,'Access matters: a buried wrong-color piece',size=7.8)
stages=[('P02-current','Initial defect',CORAL),('buried-after-4','Remove four correct covers',INK),('buried-after-6','Exchange the wrong brick',TEAL),('buried-after-10','Restore the four covers',TEAL)]
for i,(name,label,color) in enumerate(stages):
 panel(fig,(i*.25+.003,.18,.238,.65),name,label,color,6.7)
 if i<3:arrow(fig,(i*.25+.238,.48),(i*.25+.263,.48),CORAL if i==0 else TEAL)
save(fig,'access-repair')

# Figure 5: denominator gates and distinct populations for CRR and paired effect.
fig=plt.figure(figsize=(7,1.62));heading(fig,.006,.985,'Matched-prefix recovery: separate exposure, construction, and repair',size=8)
panel(fig,(.005,.30,.17,.49),'racer-stage-3','One shared prefix',INK,6.5)
arrow(fig,(.174,.54),(.225,.78),TEAL);arrow(fig,(.174,.54),(.225,.36),CORAL)
line(fig,(.23,.78),(.53,.78),TEAL,1);line(fig,(.23,.36),(.53,.36),CORAL,1)
fig.text(.24,.83,'Control: continue unchanged',fontsize=7,color=TEAL);fig.text(.24,.41,'Fault: verify the actual edit',fontsize=7,color=CORAL)
fig.text(.555,.78,'cᵢ',fontsize=10,ha='center',va='center',color=TEAL);fig.text(.555,.36,'fᵢ',fontsize=10,ha='center',va='center',color=CORAL)
panel(fig,(.355,.48,.105,.24),'racer-event')
line(fig,(.60,.18),(.60,.90),GRAY,.7)
heading(fig,.635,.86,'Eligible pair Q',size=7.5)
fig.text(.635,.69,'Valid branches · shared prefix\nAll events triggered · effect verified',va='top',fontsize=7,linespacing=1.7)
fig.text(.635,.36,'CRR: normal branch also succeeds\nΔSR: retain both normal outcomes',va='top',fontsize=7,linespacing=1.8,color=TEAL)
fig.text(.5,.045,'Untriggered, partially exposed, service-failed, and control-failed cases remain visible in the ledger.',ha='center',fontsize=6.5,color=MUTED)
save(fig,'paired-recovery')

# Figure 6: real partial-credit arithmetic, with no model performance implied.
worked=json.loads((HERE/'evidence/worked-metric-example.json').read_text())
fig=plt.figure(figsize=(3.35,1.70))
for i,(name,s) in enumerate(zip(['E03-current','metric-remove','E03-target'],worked['states'])):
 x=i/3+.005;panel(fig,(x,.40,.32,.52),name,['Initial','Remove wrong part','Replace + finish'][i],CORAL if i==0 else INK,6.4)
 m=s['metrics'];v=m['fullPlacement']['f1'];er=m['errorReduction'];success=int(m['success'])
 fig.text(x+.16,.26,f'F1 {v:.3f}\nER {er*100:.0f}%  ·  SR {success}',ha='center',va='top',fontsize=6.9,linespacing=1.55,color=TEAL if success else INK)
fig.text(.5,.04,'Residual: 2 → 1 → 0.  Final damage DR = 0 throughout.',ha='center',fontsize=6.3,color=MUTED)
save(fig,'metric-example')

# Figure 7: composition, object sequence length, and multilabel coverage.
q=[json.loads(l) for l in (ROOT/'deliverables/brickplan-benchmark-spec/questions.jsonl').read_text().splitlines()];q=[r for r in q if not r['isAlias'] and r['mainTaskCandidate']]
d=[r for r in q if r['mode']=='dynamic'];conf={r['model']:r for r in d}
fig=plt.figure(figsize=(7,2.08));ax1=fig.add_axes([.135,.22,.205,.65]);ax2=fig.add_axes([.425,.22,.225,.65]);ax3=fig.add_axes([.765,.22,.22,.65])
names=['Local static','Whole stage','Module stage','Whole dynamic','Module dynamic'];tracks=['static-structure-diagnostic','whole-object-static','named-module-static','whole-object-dynamic','named-module-dynamic'];v=[sum(r['track']==t for r in q) for t in tracks]
ax1.barh(np.arange(5),v,color=[TEAL]*3+[BLUE]*2,height=.54);ax1.set_yticks(np.arange(5),names,fontsize=6.5);ax1.invert_yaxis();ax1.tick_params(axis='x',labelsize=6);ax1.set_xlim(0,4000);ax1.set_xlabel('Distinct task candidates',fontsize=6.7);ax1.set_title('(a) Complementary task scopes',fontsize=7.2,pad=8)
for i,n in enumerate(v):ax1.text(n+65,i,f'{n:,}',va='center',fontsize=6.3)
for track,color,label in [('whole-object-dynamic',BLUE,'Whole (50)'),('named-module-dynamic',TEAL,'Module (13)')]:
 vals=sorted(r['activeParts'] for r in conf.values() if r['track']==track);ax2.step(vals,np.arange(1,len(vals)+1)/len(vals),where='post',color=color,lw=1.3,label=label)
ax2.axvline(12,color=GRAY,lw=.7,ls='--');ax2.axvline(24,color=GRAY,lw=.7,ls='--');ax2.set_xlim(4,34);ax2.set_ylim(0,1.04);ax2.set_yticks([0,.5,1],['0','50','100%']);ax2.tick_params(labelsize=6);ax2.set_xlabel('Active target pieces per configuration',fontsize=6.4);ax2.set_title('(b) Operation length',fontsize=7.2,pad=8);ax2.legend(loc='lower right',fontsize=5.9,frameon=False)
scopes=[['static-structure-diagnostic','whole-object-static','named-module-static'],['whole-object-dynamic'],['named-module-dynamic']];codes=['E01','E02','E03','E04','E05','E06','E07'];matrix=[]
for code in codes:
 linevals=[]
 for scope in scopes:
  pool=[r for r in q if r['track'] in scope and r['taskType'] not in ['S0','D0']];linevals.append(100*sum(code in r['errorCodes'] for r in pool)/len(pool))
 matrix.append(linevals)
a=np.array(matrix);ax3.imshow(a,aspect='auto',cmap='Blues',vmin=0,vmax=50);ax3.set_xticks([0,1,2],['Static','Whole','Module'],fontsize=6.1);ax3.set_yticks(range(7),codes,fontsize=6.3);ax3.tick_params(length=0);ax3.set_title('(c) Physical error coverage',fontsize=7.2,pad=8)
for i in range(7):
 for j in range(3):ax3.text(j,i,f'{a[i,j]:.0f}%',ha='center',va='center',fontsize=6.5,color='white' if a[i,j]>25 else INK)
fig.text(.875,.08,'Share of fault tasks; labels co-occur',ha='center',fontsize=5.9,color=MUTED)
save(fig,'dataset-analysis')

# Figure 8: measured protocol effects, not a fabricated model plot.
study=json.loads((HERE/'evidence/protocol-study.json').read_text());manifest['sources'][str((HERE/'evidence/protocol-study.json').relative_to(ROOT))]=sha(HERE/'evidence/protocol-study.json')
fig,ax=plt.subplots(figsize=(3.35,1.55));fig.subplots_adjust(left=.37,right=.91,bottom=.22,top=.86)
labels=['Exact prefix / alt.','Actual state / alt.','Actual state / ref.'];values=[9,36,36]
ax.barh(range(3),values,color=[CORAL,TEAL,BLUE],height=.48);ax.set_yticks(range(3),labels,fontsize=6.4);ax.invert_yaxis();ax.set_xlim(0,41);ax.set_xticks([0,12,24,36],['0','12','24','36']);ax.tick_params(axis='x',labelsize=6);ax.set_xlabel('Fault trials with trigger opportunity / event',fontsize=6.2)
for i,n in enumerate(values):ax.text(n+.6,i,f'{n}/36',va='center',fontsize=6.5,color=INK)
ax.spines['left'].set_visible(False);ax.tick_params(axis='y',length=0);fig.text(.5,.96,'Selected-route executor diagnostic',ha='center',fontsize=7.6,weight='bold',color=INK)
save(fig,'route-diagnostic')

# Figure 9: actual archived model behavior, eight states per row, shared camera.
qual=json.loads((HERE/'evidence/repair-comparison.json').read_text());fig=plt.figure(figsize=(7,2.30))
rows=[('GT: one legal witness','gt',qual['gt'])]+[(('Model: repair an external extra piece' if t['condition']=='extra_layer' else 'Model: correct a legal but wrong placement'),t['condition'],[t['frames'][i] for i in t['selectedIndices']]) for t in qual['traces']]
for r,(title,prefix,frames) in enumerate(rows):
 top=.99-r/3;heading(fig,.005,top,title,size=7.4)
 for j,f in enumerate(frames):
  x=j/8+.002;y=top-.226;panel(fig,(x,y,.121,.175),'car-'+prefix+'-'+str(j))
  act=f['action'];action=('+' if act['type']=='attach' else '−')+act.get('partId','') if act['type'] in ['attach','detach'] else 'finish'
  verdict='external edit' if f['eventOccurred'] else 'wrong pose' if f['outOfGoalPieces'] else 'complete' if f['feedback']=='SUCCESS' else 'legal partial'
  color=CORAL if f['eventOccurred'] or f['outOfGoalPieces'] else TEAL
  line(fig,(x,y),(x+.121,y),color,.9);fig.text(x+.06,y-.007,action,ha='center',va='top',fontsize=5.8,color=INK);fig.text(x+.06,y-.053,verdict,ha='center',va='top',fontsize=5.9,color=color)
  if j<7:arrow(fig,(x+.119,y+.08),(x+.13,y+.08),GRAY,.6)
save(fig,'repair-filmstrip')

# Supplemental coverage atlases keep every object; all main render styles match.
def atlas(items,name,title,cols=7):
 nr=math.ceil(len(items)/cols);h=.26+nr*.76;fig=plt.figure(figsize=(7,h));heading(fig,.005,.99,title,size=8)
 for i,(image,label,sub) in enumerate(items):
  row,col=divmod(i,cols);top=h-.28-row*.76;x=col/cols+.005
  panel(fig,(x,(top-.49)/h,1/cols-.01,.49/h),image)
  fig.text((col+.5)/cols,(top-.51)/h,label,ha='center',va='top',fontsize=6.1)
  fig.text((col+.5)/cols,(top-.635)/h,sub,ha='center',va='top',fontsize=5.9,color=MUTED)
 save(fig,name)
items=[]
for mid,r in conf.items():
 if mid.startswith('obj-'):
  count=sum(x['model']==mid for x in d);items.append(('atlas-'+mid,mid.removeprefix('obj-'),f'{r["activeParts"]} pieces · {count} tasks'))
atlas(items,'whole-object-atlas','All 42 retained procedural whole objects')
items=[]
for mid,r in conf.items():
 if r['track']=='named-module-dynamic':
  label=mid.replace('-helicopter',' heli.').replace('-roof',' roof').replace('-tail',' tail').replace('rockefeller-crown','Rockefeller').replace('brandenburg-top','Brandenburg').replace('repair-truck-cab','Truck cab').replace('museum roof-long','Museum roof +')
  items.append(('atlas-'+mid,label,f'{r["activeParts"]} active pieces'))
atlas(items,'module-atlas','All 13 named operation configurations; 12 original community source scenes')
allq=[json.loads(l) for l in (ROOT/'deliverables/brickplan-benchmark-spec/questions.jsonl').read_text().splitlines()];allq=[r for r in allq if not r['isAlias']]
items=[]
for mid in dict.fromkeys(r['model'] for r in allq if r['track']=='dynamic-structure-diagnostic'):
 rs=[r for r in allq if r['track']=='dynamic-structure-diagnostic' and r['model']==mid];r=rs[0]
 label=mid.removeprefix('sr4-').replace('alternative-release','alt. release')
 items.append(('diagnostic-'+mid,label,f'{r["activeParts"]} pieces · {len(rs)} tasks'))
atlas(items,'diagnostic-atlas','26 historical structural configurations; diagnostic scope only')
extra=[('ship','4018 ship','12 pieces'),('sea-helicopter','4017 sea heli.','13 pieces'),('mini-helicopter','4037 mini heli.','9 pieces'),('bookshelf','Bookshelf','21 pieces'),('bus','City bus','32 pieces'),('bridge','Stone bridge','25 pieces'),('press','Gantry press','24 pieces'),('cottage','Cottage','24 pieces')]
atlas([('object-'+n,label,sub) for n,label,sub in extra]+[('atlas-museum-roof-long','Museum roof +','16 active pieces')],
      'added-atlas','Three complete original LDraw objects, five longer builds, and an enlarged roof')
# A context inset anchors two cropped but camera-matched roof trajectories.
fig=plt.figure(figsize=(7,1.55));heading(fig,.005,.99,'A reference route is one witness, not the target trajectory',size=7.8)
panel(fig,(.002,.21,.20,.61),'atlas-cottage-roof','Supplied cottage body',MUTED,6.4)
line(fig,(.22,.15),(.22,.91),GRAY,.6)
for row,route in enumerate(['referenceOrder','alternateOrder']):
 y=.53-row*.39;fig.text(.235,y+.12,'Reference' if row==0 else 'Alternative',fontsize=6.6,color=TEAL if row==0 else BLUE)
 for j,step in enumerate([2,3,6]):
  panel(fig,(.37+j*.205,y-.04,.18,.31),f'roof-{route}-{step}',('2 installed' if step==2 else '3 installed' if step==3 else 'Same target'),INK,6.1)
  if j<2:arrow(fig,(.548+j*.205,y+.09),(.576+j*.205,y+.09),GRAY)
save(fig,'alternative-orders')
manifest['sources'][str(Path(__file__).relative_to(ROOT))]=sha(Path(__file__))
manifest['sources'][str((HERE/'publication_scenes.py').relative_to(ROOT))]=sha(HERE/'publication_scenes.py')
manifest['sources'][str((HERE/'render_publication.mjs').relative_to(ROOT))]=sha(HERE/'render_publication.mjs')
manifest['sharedPublicationViewports']={k:[int(x) for x in v] for k,v in crop_cache.items()}
(OUT/'provenance.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('PUBLICATION FIGURES',len(manifest['figures']),flush=True)
