"""Visual capability dossier: measured traces, reference-only tasks, self-review.

Every performance statement is tied to a run; untested is never a failed model.
"""
from pathlib import Path
import gzip,json,hashlib
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle,FancyArrowPatch
from figure_typography import configure
from release_assets import HERE,ROOT,read,write,sha

OUT=HERE/'figures-capability';OUT.mkdir(exist_ok=True)
FONT=configure(8);INK='#24354a';GRAY='#647488';GREEN='#087d79';RED='#be4c3b';AMBER='#99651c';BLUE='#476fa5'
plt.rcParams.update({'text.color':INK,'text.parse_math':False})
ARENA=read(HERE/'evidence/arena-traces.json');REF=read(HERE/'evidence/capability-reference-scenes.json')
PILOT=read(HERE/'evidence/capability-pilot.json');REL=read(HERE/'evidence/release-render-states.json')
paths={};groups={};specs={}
for data,folder,tag in [(ARENA,'figures-release/arena-native','old'),(REL,'figures-release/native','release'),(REF,'figures-capability/native','reference')]:
 for s in data['scenes']:
  paths[s['name']]=HERE/folder/(s['name']+'.png');groups[s['name']]=tag+'/'+s['group'];specs[s['name']]=s
run=PILOT['runs'][0];folder=ROOT/'deliverables/brickplan-dynamic-arena/runs'/run['runId']
record=json.loads(gzip.decompress((folder/'record.private.json.gz').read_bytes()))
assert record['initial']==specs['repair-0']['state'] and record['final']==specs['repair-1']['state']
assert record['goal']==specs['repair-2']['state'] and len(record['records'])==2
assert record['records'][1]['action']==dict(type='detach',partId='A011')
assert record['records'][1]['feedback']['code']=='OK' and run['success'] is None
assert sum(record['initial'][k]!=record['final'][k] for k in record['initial'])==1
sources={str(p.relative_to(ROOT)):sha(p) for p in [HERE/'evidence/arena-traces.json',HERE/'evidence/release-render-states.json',HERE/'evidence/capability-reference-scenes.json',HERE/'evidence/capability-pilot.json',folder/'record.private.json.gz',folder/'log.json']}
used={};cropcache={}
def txt(fig,x,y,text,size=8,color=INK,bold=False,**kw):
 return fig.text(x,y,text,fontsize=size,color=color,weight='bold' if bold else 'normal',**kw)
def heading(fig,title,subtitle):
 txt(fig,.045,.963,title,14,bold=True);txt(fig,.045,.93,subtitle,7.7,color=GRAY)
def line(fig,y):fig.lines.append(plt.Line2D([.045,.955],[y,y],transform=fig.transFigure,color='#dbe2e9',lw=.8))
def panel(fig,box,name,label,focus=None,color=INK):
 p=paths[name];a=np.asarray(Image.open(p).convert('RGB'));used[str(p.relative_to(ROOT))]=sha(p)
 group=groups[name]
 if group not in cropcache:
  rects=[]
  for n,g in groups.items():
   if g!=group:continue
   v=np.asarray(Image.open(paths[n]).convert('RGB').resize((400,300)));yy,xx=np.nonzero(v.min(2)<238)
   if len(xx):rects.append([xx.min()*8,yy.min()*8,(xx.max()+1)*8,(yy.max()+1)*8])
  cropcache[group]=[min(r[0] for r in rects),min(r[1] for r in rects),max(r[2] for r in rects),max(r[3] for r in rects)]
 l,t,r,b=focus or cropcache[group];cx,cy=(l+r)/2,(t+b)/2;w,h=(r-l)*1.08,(b-t)*1.08
 aspect=box[2]*fig.get_figwidth()/(box[3]*fig.get_figheight())
 if w/h>aspect:h=w/aspect
 else:w=h*aspect
 ax=fig.add_axes(box);ax.imshow(a,interpolation='none');ax.set_xlim(cx-w/2,cx+w/2);ax.set_ylim(cy+h/2,cy-h/2);ax.axis('off')
 txt(fig,box[0]+box[2]/2,box[1]-.011,label,6.9,color=color,ha='center',va='top')
 return ax
def focus_difference(a,b):
 x=np.asarray(Image.open(paths[a])).astype(int);y=np.asarray(Image.open(paths[b])).astype(int)
 yy,xx=np.nonzero(np.max(np.abs(x-y),2)>40);return [int(v) for v in [max(0,xx.min()-270),max(0,yy.min()-240),min(3200,xx.max()+270),min(2400,yy.max()+240)]]
focus=focus_difference('repair-0','repair-1')
cases=[
 dict(id='A',title='Compare and change only the wrong part',badge='PARTIAL / current static API',color=AMBER,
      images=['repair-0','repair-1'],labels=['Wrong-color column','Model: wrong part removed'],focus=focus,
      body='GPT-6.1 Sol selected and removed the faulty part.\nNo collateral change; the service stopped before replacement.\nThis is correct partial action, not completed repair.'),
 dict(id='B',title='Build a complete object legally',badge='COMPLETED / archived Arena v2',color=GREEN,
      images=[ARENA['normalRuns'][0]['frames'][0],ARENA['normalRuns'][0]['frames'][-1]],labels=['Empty studded baseplate','Model: complete car'],
      body='Claude Sonnet 5.5 completed all six placements.\n17 decisions: 6 moves, 8 observations, 2 invalid requests.\nA legal alternative order can succeed.'),
 dict(id='C',title='Recover after an unannounced change',badge='COMPLETED / archived Arena v2',color=GREEN,
      images=[ARENA['runs'][0]['modelFrames'][3],ARENA['runs'][0]['modelFrames'][-1]],labels=['A built part was removed','Model: restored and finished'],
      body='The car run requested fresh evidence and restored the part.\nIts normal control succeeded independently.\nRecovery is demonstrated; detection time is not known.'),
 dict(id='D',title='Replan access and verify the result',badge='NOT COMPLETED / archived Arena v2',color=RED,
      images=[ARENA['runs'][1]['modelFrames'][-1],ARENA['runs'][1]['gtFrames'][-1]],labels=['Model: wrong explicit finish','Feasible GT endpoint'],
      body='GPT-6.1 Sol built further and encountered blocked access.\nFinal state: 5 correct, 1 excess, 2 missing placements.\nThe trace does not identify one internal cognitive cause.'),
 dict(id='E',title='Open, repair, and restore the context',badge='MODEL UNTESTED / reference only',color=BLUE,
      images=['access-00','access-09'],labels=['A buried wrong part','Reference: repaired stage'],
      body='The bookshelf requires legal access work and restoration.\nA feasible eight-move witness exists.\nNo completed API run supports this capability yet.'),
 dict(id='F',title='Stay correct across repeated changes',badge='MODEL UNTESTED / reference only',color=BLUE,
      images=['repeated-08','repeated-12'],labels=['Event 1: missing part','Event 2: displaced part'],
      body='The cow keeps one task and encounters two separate edits.\nThe scripted witness recovers and finishes.\nThis establishes solvability, not learned-agent resilience.')]
cases[0].update(caseId=run['caseId'],runId=run['runId'],model=run['model'],success=None)
for index,trace in [(1,ARENA['normalRuns'][0]),(2,ARENA['runs'][0]),(3,ARENA['runs'][1])]:
 cases[index].update(runId=trace['runId'],model=trace['model'],protocol=trace['protocol'],
                     success=trace.get('modelSuccess',trace.get('success')))
for index,trace in [(4,REF['traces'][0]),(5,REF['traces'][1])]:
 cases[index].update(caseId=trace['caseId'],referenceOnly=True,modelSuccess=None)

figs=[]
fig=plt.figure(figsize=(8.3,10.5));heading(fig,'Six cases that express the benchmark goal','A continuing agent must compare, act legally, update its state, replan, and verify completion.')
for j,c in enumerate(cases):
 row,col=divmod(j,2);x=.045+col*.475;top=.887-row*.286
 txt(fig,x,top,c['id']+'  '+c['title'],8.4,bold=True);txt(fig,x,top-.023,c['badge'],6.8,color=c['color'],bold=True)
 for k,(n,l) in enumerate(zip(c['images'],c['labels'])):panel(fig,(x+k*.218,top-.172,.207,.13),n,l,c.get('focus'),c['color'])
 txt(fig,x,top-.212,c['body'],7.1,va='top',linespacing=1.6)
 if col==0:fig.lines.append(plt.Line2D([.503,.503],[top+.005,top-.267],transform=fig.transFigure,color='#dbe2e9',lw=.7))
 if row<2 and col==1:line(fig,top-.273)
txt(fig,.045,.021,'Selected cases, not aggregate scores. High-resolution spectator renders; A is cropped for the reader only.',6.8,color=GRAY)
figs.append(('overview',fig))

fig=plt.figure(figsize=(8.3,10.5));heading(fig,'What the recorded models did','Normal success, successful recovery, failed recovery, and technical interruption remain separate.')
trajectory_path=HERE/'figures-release/arena-trajectories.png';used[str(trajectory_path.relative_to(ROOT))]=sha(trajectory_path)
im=Image.open(trajectory_path);ax=fig.add_axes((.08,.425,.84,.466));ax.imshow(im,interpolation='none');ax.axis('off')
txt(fig,.045,.405,'Top four rows: exact archived v2 model states and feasible, privileged GT continuations.',7.2,color=GRAY)
line(fig,.385);txt(fig,.045,.358,'Current static example: the model removed the correct wrong-color part',10,bold=True)
for i,(n,l) in enumerate([('repair-0','Input: wrong-color column'),('repair-1','Actual: detach A011'),('repair-2','Required target / reference')]):
 panel(fig,(.07+i*.305,.17,.25,.155),n,l,focus,AMBER if i==1 else INK)
txt(fig,.045,.117,'Actual calls: 1 inspect A011; 2 detach A011 (accepted); 3 receipt error, no scored action.',8)
txt(fig,.045,.087,'13 initially correct placements preserved; the correct replacement is still missing.',8)
txt(fig,.045,.057,'Completion is N/A. Confirmed new cost: $0.256830; unresolved reservation: $0.782538.',8,color=AMBER)
txt(fig,.045,.025,'No extra paid calls after the stop. The old $3 pilot ceiling remains in force; this is not a model failure.',7,color=GRAY)
figs.append(('model-evidence',fig))

fig=plt.figure(figsize=(8.3,10.5));heading(fig,'What remains unproven, and how ready the benchmark is','Reference sequences below use private state. Neither row is a model-generated solution.')
for row,(title,names,labels) in enumerate([
 ('E  Legal access: remove covers, replace the faulty part, restore the stage',
  ['access-00','access-01','access-02','access-04','access-05','access-07','access-08','access-09'],
  ['Faulty start','Open 1','Open 2','Fault removed','Replace','Restore','Target','Finish']),
 ('F  Repeated recovery: one continuous cow episode, two separate incidents',
  ['repeated-00','repeated-07','repeated-08','repeated-09','repeated-11','repeated-12','repeated-14','repeated-16'],
  ['Start','Before edit 1','Missing','Restored','Before edit 2','Displaced','Restored','Finish'])]):
 top=.883-row*.155;txt(fig,.045,top,title,8.5,bold=True,color=BLUE)
 for i,(n,l) in enumerate(zip(names,labels)):panel(fig,(.045+i*.115,top-.109,.107,.084),n,l,color=BLUE)
txt(fig,.045,.568,'Selected reference states. Access work is legitimate; references are feasible, not proved shortest.',7,color=GRAY)
line(fig,.547)
txt(fig,.045,.512,'Readiness review: about 70-75 / 100, excluding large model experiments',11,bold=True)
txt(fig,.045,.483,'Internal project judgment, not a CVPR rating or an acceptance probability.',7.5,color=GRAY)
scores=[('Scientific question',16,20),('Task coverage',12,15),('Autonomous environment',13,15),('Input fairness',10,15),('Scoring validity',10,15),('Annotation / independent checks',5,10),('Sources / reproducibility',8,10)]
for i,(label,value,total) in enumerate(scores):
 y=.445-i*.037;txt(fig,.045,y,label,8)
 fig.patches.append(Rectangle((.43,y-.002),.41,.014,transform=fig.transFigure,color='#e5ebef',lw=0))
 fig.patches.append(Rectangle((.43,y-.002),.41*value/total,.014,transform=fig.transFigure,color=GREEN if value/total>=.8 else AMBER,lw=0))
 txt(fig,.865,y,f'{value}/{total}',8)
txt(fig,.045,.155,'Before calling the benchmark complete:',9,bold=True)
txt(fig,.045,.127,'1  Match sensing / state / budgets before claiming static-to-dynamic transfer.\n2  Finish input adapters and payload checks; reduce avoidable image burden.\n3  Audit annotation visibility, action legality, source rights, and evaluation separation.',8,va='top',linespacing=1.7)
txt(fig,.045,.044,'CVPR basis: technical soundness, contribution, reproducibility, and data release. See the linked review notes.',6.9,color=GRAY)
txt(fig,.045,.022,'2027 submission format and LLM disclosure are separate requirements; the current 10-page paper is a working draft.',6.9,color=GRAY)
figs.append(('readiness',fig))

with PdfPages(HERE/'capability-atlas.pdf') as pdf:
 for name,fig in figs:
  fig.savefig(OUT/(name+'.png'),dpi=450,facecolor='white');pdf.savefig(fig,dpi=600,facecolor='white');plt.close(fig)
write(HERE/'evidence/capability-atlas.json',dict(schema='brick-atlas-capability-atlas/1',sources=sources,images=used,
  figureFont=FONT,pdfSha256=sha(HERE/'capability-atlas.pdf'),cases=cases,
  scorecard=[dict(dimension=n,points=a,maximum=b) for n,a,b in scores],score=74,scoreIsSubjective=True,
  currentStaticOutcome='technical interruption after a correct partial repair',oldDynamicScope='archived Arena v2',
  referenceOnly=['E','F'],newConfirmedCostUSD=PILOT['additionalConfirmedUSD'],newUpperCostUSD=PILOT['additionalUpperUSD']))
print('Created three-page capability dossier; six cases, no inferred cognitive labels.')
