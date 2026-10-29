"""Generate current counts, complete model inventory and unmeasured result schemas."""
from pathlib import Path
from collections import Counter
import json,re
from release_assets import snapshot,write,HERE,DATA
models,questions,stats=snapshot();OUT=HERE/'tables';OUT.mkdir(exist_ok=True)
def escape(x):
 return str(x).replace('&',r'\&').replace('_',r'\_').replace('%',r'\%').replace('#',r'\#').replace('—','--').replace('–','--').replace('’',"'").replace('é',r"\'e")
def table(name,caption,columns,rows,label=None,wide=True):
 env='table*' if wide else 'table';width=r'\textwidth' if wide else r'\linewidth'
 text='\\begin{'+env+'}[t]\n\\centering\\small\n\\caption{'+caption+'}\n'+('\\label{'+label+'}\n' if label else '')+'\\begin{tabularx}{'+width+'}{@{}X'+('r'*(len(columns)-1))+'@{}}\\toprule\n'+' & '.join(columns)+r'\\\midrule'+'\n'
 text+='\n'.join(' & '.join(map(str,r))+r'\\' for r in rows)+'\n\\bottomrule\n\\end{tabularx}\n\\end{'+env+'}\n'
 (OUT/(name+'.tex')).write_text(text)
rows=[]
for label,kind in [('Complete build','complete-object'),('Finishing task','finishing')]:
 mids={m['id'] for m in models if (m['scope']['kind']=='complete-object')==(kind=='complete-object')};qs=[q for q in questions if q['model'] in mids];c=Counter(q['taskType'] for q in qs)
 rows.append([label,len(mids),*[f'{c[t]:,}' for t in ['S0','S1','D0','D1','D2']],f'{len(qs):,}'])
totals=Counter(q['taskType'] for q in questions)
rows.append(['Total',len(models),*[f'{totals[t]:,}' for t in ['S0','S1','D0','D1','D2']],f'{len(questions):,}'])
table('release-dataset',r'\textbf{Current runnable dataset.} S0/S1 are correct-stage acceptance/static repair; D0/D1/D2 are normal construction/one incident/repeated incidents. Source acquisitions and historical records do not enter these counts.',['Scope','Objects','S0','S1','D0','D1','D2','Questions'],rows,'tab:dataset')
table('release-families',r'\textbf{Published question families.} One catalogue family per question; this table is not an exclusive physical-error ontology.',['Family','Static','Dynamic','Total'],[[escape(f),v['static'],v['dynamic'],v['static']+v['dynamic']] for f,v in stats['byFamily'].items()],'tab:families')
table('release-length',r'\textbf{Length descriptors, not calibrated difficulty.} Active parts exclude fixed context.',['Length','Objects','Static','Dynamic'],[[f'{d} ({rng})',v['models'],v['static'],v['dynamic']] for (d,v),rng in zip(stats['byLength'].items(),['3--7','8--15','16+'])],'tab:length')
roster=json.loads((HERE/'evidence/model-roster.json').read_text());names=[m['name'] for m in roster['models']]
# Keep the inherited names explicitly provisional. Serving availability is not probed.
configs=[
('main-models','E1: static repair',['Model','SR','F1','ER','DR','S0 FR','Valid N'],names,'Implemented. Separate whole-object and finishing stages; SR/F1/ER/DR use S1 and FR uses S0.'),
('main-dynamic','E2: normal assembly and recovery',['Model','BCR','D1 NQR','D2 NQR','ICR','TR','Eligible N'],names,'Implemented normal-qualified recovery uses independent matched runs, not causal forks.'),
('main-paired','E3: strict paired outcomes',['Model','Pairs','Control SR','Fault SR','CRR',r'$\Delta$SR'],names,'Planned shared-prefix study. Only genuine cloned-prefix pairs enter CRR or the paired difference.'),
('main-ablations','E4: evidence ablations',['Condition','SR','BCR','NQR','Queries','USD'],['Full tools','No manual pages','One requested view','No recall','Scheduled observations'],'Planned matched-sensor comparison; change one factor and report actual images.'),
('static-errors','E5: static families',['Family','SR','F1','ER','DR','Valid N'],list(stats['byFamily']),'Implemented breakdown; fit only families with static support; do not pool controls.'),
('dynamic-errors','E6: dynamic families',['Family','ICR','TR','NQR','Eligible N'],list(stats['byFamily']),'Implemented breakdown; do not infer detection from completion.'),
('repair-quality','E7: preservation and partial repair',['Model','F1','Missing fixed','Excess cleared','Damage','Moves'],names,'Implemented; temporary removal is effort, not final damage.'),
('difficulty','E8: length and access',['Stratum','Objects','SR','BCR','NQR','Moves'],['Short (3--7)','Medium (8--15)','Long (16+)','Accessible defect','Buried repair'],'Length bands are current. Access calibration and empirical difficulty require independent evidence.'),
('multi-events','E9: repeated incidents',['Model','All-event SR','Exposure','Recovered','Retention','Eligible N'],names,'Implemented event windows end before the next external incident; short retention windows are N/A.'),
('checkpoint','E10: supplied checkpoints',['Model','SR','Repair@2','Repair@4','Repair@8','Valid N'],names,'Planned separate bank; system-supplied progress is not model-built progress.'),
('modality','E11: input representation',['Input','SR','BCR','NQR','Queries','USD'],['RGB + neutral rules','Structured text state','RGB + structured state'],'Text adapters and matched-information policy remain to be integrated. Exact state is privileged assistance.'),
('action-output','E12: localization interface',['Output','SR','BCR','NQR','Schema err.','Phys. reject'],['Candidate handle','Discrete coordinates','Continuous coordinates'],'Current handles are implemented; coordinate variants require matched action domains.'),
('perception-probe','E13: independent detection',['Model','Detection','Localization','False alarm','Visible N'],names,'Planned independent snapshot bank; no label inferred from episode failure.'),
('cross-recovery','E14: repair of another agent state',['Repairer','Own state SR','Other state SR','Residual','Valid N'],names,'Planned shared failed-state bank with matched checkpoints and no hidden reference access.'),
('visual-robustness','E15: observation robustness',['Condition','SR','BCR','NQR','Queries'],['Matched native views','Higher resolution','Restricted camera','Occluded initial view','Changed handle seed'],'Planned controlled visual variants; recheck visibility and legality.'),
('strategy-budget','E16: planning and budget',['Condition','SR','BCR','NQR','Decisions','USD'],['Default decision cap','Half decision cap','Double decision cap','Observation schedule'],'Planned study; charge all decisions and queries, and change one budget at a time.'),
('efficiency','E17: effort and cost',['Model','Moves/ref.','Observe','Recall','Tokens','USD'],names,'Implemented logging. Reference is feasible, not optimal; retry costs remain included.'),
('human-panel','E18: independent human study',['Panel','N','Completion','Exposure','Agreement','Time'],['Blind normal assembly','Blind incident recovery','GT correctness review','Physical feasibility review'],'Planned. GT review is not blind ability evidence; responses must be independent.'),
('failures','E19: validity ledger',['Model','Planned','Valid','Service err.','Format err.','Untriggered'],names,'Implemented status separation. Planned and valid denominators are both reported.')]
results={}
for name,title,cols,labels,note in configs:
 rows=[[escape(x)]+['---']*(len(cols)-1) for x in labels]
 table(name,r'\textbf{'+title+' (unmeasured).} '+note+' Dashes mean not run, never zero.',cols,rows)
 results[name]=dict(title=title,columns=cols,note=note,rows=[dict(label=x,results={c:None for c in cols[1:]}) for x in labels])
table('release-main-results',r'\textbf{Primary model results (reserved; unmeasured).} Candidate names are inherited planning labels; exact serving versions remain to be verified. Static SR uses S1, FR uses S0, BCR uses D0, and NQR reports fully exposed runs with successful matched normal controls. Each populated rate must include its denominator.', ['Model','S1 SR','S0 FR','D0 BCR','D1 NQR','D2 NQR','Valid N'], [[escape(n)]+['---']*6 for n in names], 'tab:mainresults')
write(HERE/'evidence/release-results-template.json',dict(status='NOT_RUN',repetitions=1,apiCalls=0,rosterStatus='Inherited candidates; serving versions and access not verified in this revision',models=roster['models'],tables=results))
# Machine-readable inventory and readable LaTeX rows, with IDs rather than uncertain translations.
write(HERE/'evidence/release-model-inventory.json',models)
text=r'\small\begin{longtable}{@{}p{.40\textwidth}llrrr@{}}\caption{All 310 runnable object IDs. W: complete build; F: finishing task. S/M/L are length strata.}\\\toprule Object ID & Scope & Length & Parts & Static & Dynamic\\\midrule\endfirsthead\toprule Object ID & Scope & Length & Parts & Static & Dynamic\\\midrule\endhead'+'\n'
for m in models:text+=' & '.join([escape(m['id']),'W' if m['scope']['kind']=='complete-object' else 'F',m['difficulty'][0].upper(),str(m['activeParts']),str(m['staticCases']),str(m['dynamicCases'])])+r'\\'+'\n'
text+=r'\bottomrule\end{longtable}'+'\n';(OUT/'release-model-inventory.tex').write_text(text)
write(HERE/'evidence/release-experiment-plan.json',dict(schema='brick-atlas-plan/1',candidateQuestions=len(questions),finalEvaluationIds=None,allSourcesAuthoringExposed=True,tables=list(results),repetitions=1,formalStudyComplete=False,apiCalls=0))
print('Generated current counts, 19 blank experiment tables, and 310-model inventory')
