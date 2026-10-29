"""Current-release panels plus explicitly separated archived Arena examples."""
from pathlib import Path
from collections import Counter
import hashlib,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch,Rectangle,FancyBboxPatch
from PIL import Image
from figure_typography import configure
from release_assets import HERE,ROOT,DATA,read,sha,write,lines
OUT=HERE/'figures-release';NATIVE=OUT/'native';OUT.mkdir(exist_ok=True)
typography=configure(7.3);INK='#25364b';MUTED='#5e6e80';TEAL='#087d79';CORAL='#cd523d';BLUE='#466fb3';GRAY='#dce3e9'
plt.rcParams.update({'text.color':INK,'axes.labelcolor':INK,'axes.spines.top':False,'axes.spines.right':False})
selection=read(HERE/'evidence/release-figure-selection.json');scenes=read(HERE/'evidence/release-render-states.json');stats=read(HERE/'evidence/release-dataset.json');models=lines(DATA/'models.jsonl')
manifest=dict(schema='brick-atlas-release-figures/1',nativePixels=[3200,2400],exportDpi=600,typography=typography,apiCalls=0,evaluationInputUnchanged=True,publicationOnly=True,sources={str(p.relative_to(ROOT)):sha(p) for p in [HERE/'evidence/release-figure-selection.json',HERE/'evidence/release-render-states.json',DATA/'models.jsonl',DATA/'questions/static.jsonl',DATA/'questions/dynamic.jsonl']},figures={},images={})
byname={s['name']:s for s in scenes['scenes']};crop_cache={}
def im(name):
 p=NATIVE/(name+'.png');manifest['images'][str(p.relative_to(HERE))]=dict(sha256=sha(p),pixels=list(Image.open(p).size));return np.asarray(Image.open(p).convert('RGB'))
def crop(name):
 group=byname[name]['group']
 if group not in crop_cache:
  rects=[]
  for s in scenes['scenes']:
   if s['group']!=group:continue
   a=np.asarray(Image.open(NATIVE/(s['name']+'.png')).resize((400,300)));yy,xx=np.nonzero(a.min(2)<240)
   if len(xx):rects.append((xx.min()*8,yy.min()*8,(xx.max()+1)*8,(yy.max()+1)*8))
  crop_cache[group]=(min(x[0] for x in rects),min(x[1] for x in rects),max(x[2] for x in rects),max(x[3] for x in rects))
 return crop_cache[group]
def panel(fig,box,name,label=None,color=INK,fs=6.6):
 ax=fig.add_axes(box);ax.imshow(im(name),interpolation='none');ax.axis('off');l,t,r,b=crop(name);cx,cy=(l+r)/2,(t+b)/2;w,h=(r-l)*1.08,(b-t)*1.08;asp=box[2]*fig.get_figwidth()/(box[3]*fig.get_figheight())
 if w/h>asp:h=w/asp
 else:w=h*asp
 ax.set_xlim(cx-w/2,cx+w/2);ax.set_ylim(cy+h/2,cy-h/2)
 if label:fig.text(box[0]+box[2]/2,box[1]-.01,label,ha='center',va='top',fontsize=fs,color=color)
 return ax
def heading(fig,x,y,text,color=INK,fs=8):fig.text(x,y,text,va='top',fontsize=fs,color=color,weight='bold')
def line(fig,a,b,color=GRAY):fig.lines.append(plt.Line2D([a[0],b[0]],[a[1],b[1]],transform=fig.transFigure,color=color,lw=.6))
def arrow(fig,a,b,color=TEAL):fig.patches.append(FancyArrowPatch(a,b,transform=fig.transFigure,arrowstyle='->',mutation_scale=8,color=color,lw=.8))
def save(fig,name,formats=('pdf','svg','png')):
 for ext in formats:
  path=OUT/f'{name}.{ext}';fig.savefig(path,dpi=600,facecolor='white')
  if ext=='svg':path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines())+'\n')
 manifest['figures'][name]=dict(pdfSha256=sha(OUT/f'{name}.pdf'),inches=list(fig.get_size_inches()),formats=list(formats));plt.close(fig);print('FIGURE',name,flush=True)

fig=plt.figure(figsize=(7,1.85))
for i,s in enumerate(selection['errors']):
 x=i/8+.002;heading(fig,x+.06,.99,s['label'],TEAL if 'control' in s['name'] else INK,6.6)
 # centered headings avoid overflowing eight narrow columns
 fig.texts[-1].set_ha('center')
 ax=panel(fig,(x,.53,.121,.35),s['name']+'-current','Current',CORAL if 'control' not in s['name'] else TEAL,6.3)
 if 'control' not in s['name']:
  a,b=im(s['name']+'-current').astype(np.int16),im(s['name']+'-target').astype(np.int16)
  yy,xx=np.nonzero(np.max(np.abs(a-b),axis=2)>38)
  if len(xx):ax.add_patch(Rectangle((xx.min()-14,yy.min()-14),xx.max()-xx.min()+28,yy.max()-yy.min()+28,fill=False,edgecolor=CORAL,lw=.65))
 panel(fig,(x,.075,.121,.35),s['name']+'-target','Target',TEAL,6.3)
 if i<7:line(fig,(x+.123,.07),(x+.123,.91))
save(fig,'errors')
fig=plt.figure(figsize=(7,1.65));boxes=[(.005,.25,.225,.60),(.26,.25,.225,.60),(.515,.25,.225,.60),(.77,.25,.225,.60)]
texts=[('1  Initial request','Rules + handles + budget\nNo automatic image'),('2  Agent requests evidence','observe: view + rotation\ninspect: part or manual'),('3  Agent changes one part','attach / detach\nParameters: handles'),('4  Action feedback','Accepted or rejected\nNo fresh scene image')]
for (x,y,w,h),(title,body) in zip(boxes,texts):
 fig.patches.append(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.003',transform=fig.transFigure,fill=False,edgecolor=GRAY,lw=.8));heading(fig,x+.012,y+h-.045,title,fs=7.3);fig.text(x+.012,y+h-.23,body,va='top',fontsize=7.0,linespacing=1.8)
for i in range(3):arrow(fig,(boxes[i][0]+.227,.54),(boxes[i+1][0]-.005,.54))
arrow(fig,(.88,.24),(.37,.24));fig.text(.63,.14,'Observe again when needed; finish explicitly.',ha='center',fontsize=7,color=TEAL)
fig.text(.5,.03,'Hidden edit changes the world. Only requested images enter the model conversation.',ha='center',fontsize=7,color=CORAL)
save(fig,'interaction')
fig=plt.figure(figsize=(3.35,1.45));steps=selection['repair'];n=len(steps)
for i,s in enumerate(steps):
 panel(fig,(i/n+.003,.17,.96/n,.75),s['name'],s['label'].capitalize(),TEAL if i==n-1 else INK,6.5)
 if i<n-1:arrow(fig,((i+1)/n-.025,.52),((i+1)/n+.015,.52))
heading(fig,.01,.99,'Reference actions; final geometry decides success',fs=7.2);save(fig,'static-repair')
fig=plt.figure(figsize=(3.35,1.80));labels=['Same task / model / input / budget','Normal run succeeded','Valid run + all effective events','Final success: qualified recovery']
for i,t in enumerate(labels):
 y=.86-i*.20;fig.patches.append(FancyBboxPatch((.02,y-.13),.96,.14,boxstyle='round,pad=0.004',transform=fig.transFigure,facecolor='#f0f8f7' if i==3 else '#f5f7fa',edgecolor=GRAY,lw=.6));fig.text(.5,y-.06,t,ha='center',va='center',fontsize=7.2,color=TEAL if i==3 else INK)
 if i<3:arrow(fig,(.5,y-.13),(.5,y-.19))
fig.text(.5,.045,'Causal paired effects additionally need a shared prefix.',ha='center',fontsize=6.6,color=MUTED);save(fig,'eligibility')
fig,axs=plt.subplots(1,3,figsize=(7,2.05),gridspec_kw={'width_ratios':[.8,1.0,1.7]});fig.subplots_adjust(left=.06,right=.99,top=.84,bottom=.25,wspace=.40)
diffs=['short','medium','long'];x=np.arange(3);vals=[stats['byLength'][d]['models'] for d in diffs];axs[0].bar(x,vals,color=[TEAL,BLUE,CORAL]);axs[0].set_xticks(x,diffs,fontsize=6.5);axs[0].set_title('Objects',fontsize=8,weight='bold');axs[0].tick_params(labelsize=6)
for i,v in enumerate(vals):axs[0].text(i,v+3,str(v),ha='center',fontsize=6.7)
for j,(mode,col) in enumerate([('static',TEAL),('dynamic',BLUE)]):axs[1].bar(x+(j-.5)*.34,[stats['byLength'][d][mode] for d in diffs],width=.32,color=col,label=mode.title())
axs[1].set_xticks(x,diffs,fontsize=6.5);axs[1].tick_params(labelsize=6);axs[1].set_title('Questions',fontsize=8,weight='bold');axs[1].legend(fontsize=6,frameon=False)
families=['missing','wrong-color','offset','buried-repair','rotated','multiple'];y=np.arange(len(families))
for j,(mode,col) in enumerate([('static',TEAL),('dynamic',BLUE)]):axs[2].barh(y+(j-.5)*.35,[stats['byFamily'][f][mode] for f in families],height=.32,color=col)
axs[2].set_yticks(y,['Missing','Color','Offset','Buried','Rotated','Repeated'],fontsize=6.4);axs[2].tick_params(labelsize=6);axs[2].invert_yaxis();axs[2].set_title('Selected families',fontsize=8,weight='bold');save(fig,'coverage')
# All 310 preview images at small native dimensions, never upscaled source pixels.
for start in range(0,len(models),40):
 fig=plt.figure(figsize=(7,6.6));heading(fig,.006,.995,f'Current object inventory {start+1}–{min(start+40,len(models))} / {len(models)}',fs=8)
 for j,m in enumerate(models[start:start+40]):
  row,col=divmod(j,8);x=col/8+.003;y=.815-row*.185;ax=fig.add_axes((x,y,.119,.135));p=DATA/m['preview'];im_=Image.open(p).convert('RGB');ax.imshow(im_,interpolation='none');ax.axis('off')
  manifest['images'][str(p.relative_to(HERE)) if p.is_relative_to(HERE) else str(p.relative_to(ROOT))]=dict(sha256=sha(p),pixels=list(im_.size),source='release-overview')
  label=m['id'].removeprefix('sc-').removeprefix('obj-').replace('v7-long-','long-');fig.text(x+.0595,y-.004,label,ha='center',va='top',fontsize=5.7);fig.text(x+.0595,y-.032,('Whole' if m['scope']['kind']=='complete-object' else 'Finish')+f" · {m['activeParts']} parts",ha='center',va='top',fontsize=5.6,color=MUTED)
 save(fig,f'gallery-{start//40+1}',formats=('pdf',))
# Two exact archived traces: four compact rows, eight states per row.
arena=read(HERE/'evidence/arena-traces.json');manifest['sources']['paper/brickplan-cvpr/evidence/arena-traces.json']=sha(HERE/'evidence/arena-traces.json')
arena_specs={s['name']:s for s in arena['scenes']};arena_crops={}
def arena_panel(fig,box,name,label,color=INK):
 p=OUT/'arena-native'/(name+'.png');a=np.asarray(Image.open(p).convert('RGB'));group=arena_specs[name]['group']
 manifest['images'][str(p.relative_to(HERE))]=dict(sha256=sha(p),pixels=list(Image.open(p).size))
 if group not in arena_crops:
  rects=[]
  for s in arena['scenes']:
   if s['group']!=group:continue
   b=np.asarray(Image.open(OUT/'arena-native'/(s['name']+'.png')).resize((400,300)));yy,xx=np.nonzero(b.min(2)<238)
   if len(xx):rects.append((xx.min()*8,yy.min()*8,(xx.max()+1)*8,(yy.max()+1)*8))
  arena_crops[group]=(min(x[0] for x in rects),min(x[1] for x in rects),max(x[2] for x in rects),max(x[3] for x in rects))
 ax=fig.add_axes(box);ax.imshow(a,interpolation='none');ax.axis('off');l,t,r,b=arena_crops[group]
 cx,cy=(l+r)/2,(t+b)/2;w,h=(r-l)*1.04,(b-t)*1.04;aspect=box[2]*fig.get_figwidth()/(box[3]*fig.get_figheight())
 if w/h>aspect:h=w/aspect
 else:w=h*aspect
 ax.set_xlim(cx-w/2,cx+w/2);ax.set_ylim(cy+h/2,cy-h/2)
 fig.text(box[0]+box[2]/2,box[1]-.005,label,ha='center',va='top',fontsize=6.0,color=color)
 return ax
# Lead with a real successful assembly; every accepted move is present.
fig=plt.figure(figsize=(7,2.10));heading(fig,.006,.99,'(a) A real model builds the car / Claude Sonnet 5.5 / archived Arena v2',fs=7.6)
for i,name in enumerate(arena['normalRuns'][0]['frames']):
 arena_panel(fig,(i/8+.003,.575,.119,.31),name,arena_specs[name]['label'])
 if i<7:arrow(fig,(i/8+.117,.73),(i/8+.131,.73))
line(fig,(.005,.49),(.995,.49));heading(fig,.006,.455,'(b) Current release / complete builds and contextual finishing tasks')
for i,s in enumerate(selection['objects']):panel(fig,(i/8+.003,.075,.119,.30),s['name'],s['label'],fs=6.4)
save(fig,'teaser')
fig=plt.figure(figsize=(7,2.18))
for j,run in enumerate(arena['normalRuns']):
 top=.985-j*.48;y=top-.325
 heading(fig,.005,top,('Car / Claude Sonnet 5.5' if j==0 else 'Chair / GPT-6.1 Sol')+' / actual successful normal build',fs=7.4)
 for i,name in enumerate(run['frames']):
  arena_panel(fig,(i/8+.003,y,.119,.255),name,arena_specs[name]['label'],TEAL if i==7 else INK)
  if i<7:arrow(fig,(i/8+.117,y+.13),(i/8+.131,y+.13))
 note=('6 accepted moves; 8 observations; 2 invalid requests; 17 decisions' if j==0 else
       '7 accepted moves; 7 observations; 2 physical rejections; 17 decisions')
 fig.text(.5,y-.077,note,ha='center',fontsize=6.6,color=MUTED)
 if j==0:line(fig,(.005,.52),(.995,.52))
fig.text(.5,.012,'Every accepted move is shown. Observations and rejected actions remain in the full JSON ledger.',ha='center',fontsize=6.5,color=MUTED)
save(fig,'arena-normal-builds')
audit=read(HERE/'evidence/pilot-error-audit.json');manifest['sources']['paper/brickplan-cvpr/evidence/pilot-error-audit.json']=sha(HERE/'evidence/pilot-error-audit.json')
fig=plt.figure(figsize=(7,2.18));heading(fig,.006,.99,'Observed behavior / all valid latest pilot runs / archived Arena v2',fs=8)
cols=['format','handle','connection','collision','path','wrongFinish','budget']
labels=['Format','Handle','No connection','Collision','Blocked path','Wrong finish','Budget limit']
groups=audit['groups'];values=np.array([[r['counts'].get(k,0) for k in cols] for r in groups]);ax=fig.add_axes((.245,.19,.745,.65))
ax.imshow(values,cmap='OrRd',vmin=0,vmax=max(1,values.max()),aspect='auto');ax.set_xticks(range(7),labels,fontsize=6.5);ax.xaxis.tick_top();ax.tick_params(length=0,pad=5)
ax.set_yticks(range(len(groups)),[r['label']+' (n='+str(r['validRuns'])+')' for r in groups],fontsize=6.4)
for j in range(len(groups)):
 for i in range(7):ax.text(i,j,str(values[j,i]),ha='center',va='center',fontsize=7,color='white' if values[j,i]>values.max()*.6 else INK)
for spine in ax.spines.values():spine.set_visible(False)
fig.text(.5,.09,'First five columns: action counts. Last two: episode counts. Different columns have different denominators.',ha='center',fontsize=6.6,color=MUTED)
fig.text(.5,.015,'3 Qwen service failures excluded from ability counts; all 19 attempts (7 service failures) remain in the audit.',ha='center',fontsize=6.6,color=MUTED)
save(fig,'pilot-error-map')
fig=plt.figure(figsize=(7,1.90));heading(fig,.006,.99,'Three evidence channels / proposed for both static and dynamic tasks',fs=8)
for i,(title,body) in enumerate([
 ('T / Text','Current + target: part, color, pose\nStock: part handles and availability\nText previews / optional manual'),
 ('I / Images','Current + target: matched views\nStock: labeled visual cards\nImage previews / optional manual'),
 ('TI / Text + images','Both encodings of the same state\nSame timestamps and anonymous IDs\nNo error label or repair answer')]):
 x=.006+i*.335;fig.patches.append(FancyBboxPatch((x,.34),.318,.48,boxstyle='round,pad=0.003',transform=fig.transFigure,fill=False,edgecolor=GRAY,lw=.8))
 heading(fig,x+.01,.78,title,TEAL,7.6);fig.text(x+.01,.62,body,fontsize=6.9,va='top',linespacing=1.7)
fig.text(.01,.24,'Static: supplied checkpoint. Dynamic: request evidence; retain history; hidden edits persist.',fontsize=7,color=INK)
fig.text(.01,.12,'Shared: goal, stock, actions, budgets, scoring. Text coordinates disclose more than native RGB.',fontsize=7,color=CORAL)
fig.text(.01,.02,'Matched-fact control: render the same ledger as image cards. This tests representation / OCR, not 3D perception.',fontsize=6.7,color=MUTED)
save(fig,'modality-design')
fig=plt.figure(figsize=(7,3.55))
for j,run in enumerate(arena['runs']):
 for k,role in enumerate(['model','gt']):
  row=j*2+k;top=.99-row*.242;y=top-.176
  title=(('Car / Claude Sonnet 5.5' if j==0 else 'Chair / GPT-6.1 Sol')+' — recorded model' if k==0 else 'Same prefix + incident / feasible GT continuation')
  heading(fig,.005,top,title,fs=7.1,color=INK if k==0 else TEAL)
  for i,name in enumerate(run[role+'Frames']):
   s=arena_specs[name];label=s['label'];color=CORAL if i==3 or ('wrong' in label or 'blocked' in label or 'rejected' in label) else TEAL if 'success' in label else INK
   arena_panel(fig,(i/8+.003,y,.119,.140),name,label,color)
   if i<7:arrow(fig,(i/8+.117,y+.075),(i/8+.131,y+.075),CORAL if i==2 else TEAL)
  if row<3:line(fig,(.003,top-.222),(.995,top-.222))
fig.text(.5,.014,'d = logged model decision · selected states, all decisions in the ledger · archival Arena v2, not a v3 score',ha='center',fontsize=6.6,color=MUTED)
save(fig,'arena-trajectories')
# Actual unmodified model-visible RGB; no upsampling or reviewer annotation.
fig=plt.figure(figsize=(7,1.85));heading(fig,.005,.99,'An actual observation request and its returned evidence (archived car episode, d15)',fs=8)
for i,im_ in enumerate(arena['io']['actualInputs']):
 p=ROOT/im_['path'];a=Image.open(p).convert('RGB');manifest['images'][im_['path']]=dict(sha256=sha(p),pixels=list(a.size),source='actual-model-requested-RGB')
 ax=fig.add_axes((.008+i*.177,.25,.165,.60));ax.imshow(a,interpolation='none');ax.axis('off');fig.text(.09+i*.177,.19,im_['role'].capitalize()+' · 800 × 600',ha='center',fontsize=6.8)
heading(fig,.382,.82,'Request',TEAL,7.5)
fig.text(.382,.69,'{"tool":"observe","args":{"view":"angled",\n "rotateDegrees":0,"show":["current","target","inventory"]}}',fontsize=6.8,va='top',linespacing=1.7)
heading(fig,.382,.43,'Response / evidence boundary',TEAL,7.5)
fig.text(.382,.31,'OBSERVED · camera azimuth 35°, elevation 30°\nAlso returns requested inventory; no event label or GT plan.\nThe model reads these images on its following decision.',fontsize=6.9,va='top',linespacing=1.6)
save(fig,'arena-input-output')
fig=plt.figure(figsize=(3.35,1.65));heading(fig,.015,.98,'Actual requested RGB / car d15 / Arena v2',fs=7.2)
for i,im_ in enumerate(arena['io']['actualInputs']):
 ax=fig.add_axes((.01+i*.50,.25,.475,.56));ax.imshow(Image.open(ROOT/im_['path']).convert('RGB'),interpolation='none');ax.axis('off')
 fig.text(.25+i*.50,.20,im_['role'].capitalize()+' / 800 x 600',ha='center',fontsize=6.7)
fig.text(.5,.055,'observe: current + target + inventory',ha='center',fontsize=7.0,color=TEAL)
save(fig,'arena-requested-views')
write(OUT/'provenance.json',manifest)
