"""Standalone research figure from certified costs, not model predictions."""
from pathlib import Path
import json,sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from static_v4.build_suite import OUT

cases={c['id']:c for c in map(json.loads,(OUT/'library/cases.jsonl').read_text().splitlines())}
ids=['sr4-independent-1','sr4-shared-1','sr4-shared-2','sr4-shared-3','sr4-triple-2','sr4-triple-6']
labels=['Independent\n2 faults','Shared 1 layer\n2 faults','Shared 2 layers\n2 faults','Shared 3 layers\n2 faults','Shared 2 layers\n3 faults','Shared 6 layers\n3 faults']
evidence=[cases[k+':joint']['pairEvidence'] for k in ids]
fig,ax=plt.subplots(figsize=(12,5.3),layout='constrained');x=np.arange(len(ids));width=.36
for shift,values,color,label in [(-width/2,[sum(e['singleCosts']) for e in evidence],'#8da6ba','Sum of singleton optima'),
                                (width/2,[e['jointCost'] for e in evidence],'#007f7f','Joint repair optimum')]:
    bars=ax.bar(x+shift,values,width,color=color,label=label);ax.bar_label(bars,padding=3,fontsize=10)
ax.set(xticks=x,xticklabels=labels,ylabel='Legal detach / attach actions',ylim=(0,49))
ax.set_title('Shared access changes repair cost under the same finite action domain',loc='left',pad=16)
ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.16);ax.set_axisbelow(True)
ax.legend(loc='upper left',frameon=False)
fig.supxlabel('Certified structural controls • privileged oracle, not VLM results',fontsize=10,color='#555555')
folder=OUT/'figures';folder.mkdir(exist_ok=True)
fig.savefig(folder/'joint-repair-cost.png',dpi=220);fig.savefig(folder/'joint-repair-cost.pdf');plt.close(fig)
