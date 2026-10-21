"""Local scientific plots for the Markdown static-audit report; no web output."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap,BoundaryNorm
from matplotlib.patches import Patch
OUT=Path(__file__).resolve().parents[3]/'deliverables/brickplan-static-audit-2026-10-14'
s=json.loads((OUT/'summary.json').read_text());b=json.loads((OUT/'bank-audit.json').read_text())
models=s['models'];tracks=['symbolic','visual'];rows=s['rows'];lookup={(r['caseId'],r['model'],r['track']):r for r in rows}
specs=s['selection']['specs'];matrix=np.zeros((len(specs),6),int);labels=[]
for i,p in enumerate(specs):
 labels.append(f"{i+1:02d}  {p['modelId']} / {p['kind']}")
 for j,(m,t) in enumerate((m,t) for m in models for t in tracks):
  r=lookup.get((p['caseId'],m,t))
  if r:
   matrix[i,j]=4 if r['status']=='error' else 5 if r['status']=='budget_exhausted' else 1 if r['success'] else 2 if r['targetMatched'] else 6 if r['formatFailures']==r['responses'] and r['manipulations']==0 else 3
colors=['#edf0f4','#268873','#c3951a','#c55359','#66768c','#8165a5','#bd793c']
fig,ax=plt.subplots(figsize=(12,11));ax.imshow(matrix,cmap=ListedColormap(colors),norm=BoundaryNorm(np.arange(-.5,7.5),7),aspect='auto')
ax.set_xticks(range(6),['GPT-6.1\nText','GPT-6.1\nViews','Gemini 4\nText','Gemini 4\nViews','Sonnet 5.5\nText','Sonnet 5.5\nViews']);ax.xaxis.tick_top();ax.set_yticks(range(len(specs)),labels,fontsize=8)
for i in range(len(specs)):
 for j in range(6):
  code=matrix[i,j];ax.text(j,i,['—','OK','T','F','API','$','J'][code],ha='center',va='center',fontsize=8,color='#596475' if code==0 else 'white')
ax.set_xticks(np.arange(-.5,6,1),minor=True);ax.set_yticks(np.arange(-.5,len(specs),1),minor=True);ax.grid(which='minor',color='white',linewidth=2);ax.tick_params(which='both',length=0)
ax.set_title('Static repair · every preselected case and input condition',pad=38,loc='left',weight='bold')
fig.legend(handles=[Patch(color=colors[i],label=l) for i,l in enumerate(['Not run','Finished exactly','Target reached; no finish','Task failed','API interrupted','Budget stopped','Only format failures'])],loc='lower center',ncol=3,fontsize=9,frameon=False)
fig.subplots_adjust(left=.42,right=.98,top=.89,bottom=.08)
for ext in ['png','svg','pdf']:fig.savefig(OUT/f'static-result-matrix.{ext}',dpi=180)
plt.close(fig)
fig,axs=plt.subplots(1,2,figsize=(12,5.4));k=list(b['kindCounts'])+['extra (standalone)'];v=[b['kindCounts'].get(x,0) for x in k];order=np.argsort(v);axs[0].barh([k[i] for i in order],[v[i] for i in order],color='#268873')
for j,i in enumerate(order):axs[0].text(v[i]+8,j,str(v[i]),va='center',fontsize=9)
axs[0].set_xlim(0,max(v)*1.18);axs[0].set_title('Primary category coverage (2,541 cases)',loc='left');axs[0].set_xlabel('Cases; compound components not double-counted')
d=[f'D{i}' for i in range(6)];vals=[b['difficultyCounts'].get(x,0) for x in d];axs[1].bar(d,vals,color='#526c99')
for i,n in enumerate(vals):axs[1].text(i,n+20,str(n),ha='center',fontsize=9)
axs[1].set_ylim(0,max(vals)*1.16);axs[1].set_title('Bank difficulty labels',loc='left');axs[1].set_ylabel('Cases');axs[1].set_xlabel('Labels mix action length and structural features')
for ax in axs:
 ax.spines[['top','right']].set_visible(False);ax.grid(axis='x' if ax==axs[0] else 'y',alpha=.13);ax.set_axisbelow(True)
fig.tight_layout()
for ext in ['png','svg','pdf']:fig.savefig(OUT/f'bank-coverage.{ext}',dpi=180)
print('Local PNG / SVG / PDF figures generated.')
