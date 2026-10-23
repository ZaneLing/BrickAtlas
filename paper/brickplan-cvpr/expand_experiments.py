"""Prepare named, unmeasured experiments and LaTeX tables; never call a model API."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent

def read(p):return json.loads(p.read_text())
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def tex(s):return str(s).replace('_',r'\_').replace('%',r'\%').replace('&',r'\&')
models=read(HERE/'evidence/model-roster.json')['models'];names={m['id']:m['name'] for m in models}
selected=read(HERE/'evidence/model-roster.json')['diagnosticModels'];short=['Sol','Flash','Qwen 27B']
r=read(HERE/'evidence/results-template.json');plan=read(HERE/'evidence/experiment-design.json')
assert r['status']=='NOT_RUN' and all(v is None for row in r['main'] for k,v in row.items() if k!='model')
# All numerical measurements remain null, including newly added diagnostic tables.
def blanks(keys):return {k:None for k in keys.split()}
r['pairedOutcomes']=[dict(model=m['id'],track=t,**blanks('exposed n11 n10 n01 n00 controlSuccess faultSuccess pairedDrop lower95 upper95')) for m in models for t in ['D','M']]
staticpath=HERE.parents[1]/'deliverables/brickplan-static-plate5/cases.jsonl'
static=[json.loads(l) for l in staticpath.read_text().splitlines()];test=set(plan['primary']['S']['caseIds'])
categories=sorted({c['category'] for c in static if c['publicId'] in test})
r['staticErrors']=[dict(model=m['id'],category=k,assignedDefinitions=sum(c['publicId'] in test and c['category']==k for c in static),**blanks('completed sourceMacroSuccess lower95 upper95')) for m in models for k in categories]
r['repairQuality']=[dict(model=m['id'],track=t,**blanks('defectReduction collateralDamage exactCompletion partF1 normalUnnecessaryEdit')) for m in models for t in ['S','M-static']]
r['perceptionProbe']=[dict(model=m['id'],track=t,**blanks('balancedAccuracy anomalyRecall falseAlarmRate affectedSlotF1 humanReadableFraction n')) for m in models for t in ['D','M']]
r['crossRecovery']=[dict(source=a,recoverer=b,track=t,**blanks('admittedStates recovered recovery')) for a in selected for b in selected for t in ['D','M']]
visual=['full','current_only','one_fixed_view','half_resolution','double_resolution','no_candidate_preview','no_manual_M_only','success_failure_only','symbolic_privileged']
r['visualRobustness']=[dict(model=m,track=t,condition=v,**blanks('assigned exposed recovery decisions inputTokens')) for m in selected for t in ['D','M'] for v in visual if not(v=='no_manual_M_only' and t=='D')]
strategies=['closed_loop','open_loop_script','explicit_visual_check','double_decision_budget']
r['strategyBudget']=[dict(model=m,track=t,condition=v,**blanks('assigned exposed completion recovery decisions latency costUSD')) for m in selected for t in ['D','M'] for v in strategies]
r['perErrorM']=[dict(error=k,**{m['id']:None for m in models}) for k in ['missing','wrong-color','extra-layer']]
r['difficulty']=[dict(model=m['id'],track=t,partsBin=b,stage=stage,temporaryDisassembly=tmp,success=None,recovery=None,n=None,exposed=None) for m in models for t in ['S','D','M-static','M-dynamic'] for b in ['4-7','8-10','11-16'] for stage in (['early','middle','late'] if t in ['D','M-dynamic'] else [None]) for tmp in ([False,True] if t in ['D','M-dynamic'] else [None])]
r['diagnosticModels']=selected
r['tableMap']={
 'E1':dict(label='tab:planned-main',file='main-models.tex',field='main'),
 'E2':dict(label='tab:paired',file='main-paired.tex',field='pairedOutcomes'),
 'E3':dict(label='tab:ablations',file='main-ablations.tex',field='ablations'),
 'E4':dict(label='tab:errorresults',file='dynamic-errors.tex',field='perError'),
 'E5':dict(label='tab:humanpanel',file='human-panel.tex',field='humanPanel'),
 'E6':dict(label='tab:difficultyresults',file='difficulty.tex',field='difficulty'),
 'E7':dict(label='tab:failureledger',file='failures.tex',field='failureLedger'),
 'E8':dict(label='tab:efficiencyresults',file='efficiency.tex',field='efficiency'),
 'E9':dict(label='tab:staticerrors',file='static-errors.tex',field='staticErrors'),
 'E10':dict(label='tab:repairquality',file='repair-quality.tex',field='repairQuality'),
 'E11':dict(label='tab:perceptionprobe',file='perception-probe.tex',field='perceptionProbe'),
 'E12':dict(label='tab:crossrecovery',file='cross-recovery.tex',field='crossRecovery'),
 'E13':dict(label='tab:visualrobustness',file='visual-robustness.tex',field='visualRobustness'),
 'E14':dict(label='tab:strategybudget',file='strategy-budget.tex',field='strategyBudget')}
dump(HERE/'evidence/results-template.json',r)
plan['diagnosticModels']=selected
plan['experiments']=[dict(id=k,**v,status='NOT_RUN') for k,v in r['tableMap'].items()]
plan['modelRosterSha256']=hashlib.sha256((HERE/'evidence/model-roster.json').read_bytes()).hexdigest()
plan['additionalDesign']={
 'analysisOnly':['static error breakdown','difficulty','repair quality','failure ledger','paired outcomes','efficiency'],
 'perceptionProbe':dict(definitions=48,source='24 D/M pairs already selected in human schedules',images='certified fixed checkpoint before/after; same image pairs for all models',response='separate change/no-change and affected-piece/slot selection; no repair hint or legality feedback',purpose='not interrupting continuous episodes; human readability rated independently',repeatPerModel=1),
 'crossRecovery':dict(sourceModels=selected,recoveryModels=selected,bank='normal siblings of the 12 D + 12 M predefined panel pairs; no external intervention during source collection',stateAdmission='save the first accepted model attachment adding an off-target placement; certify a legal reconstruction witness; retain no-event or uncertified cases without substituting later states; off-target does not imply the original episode would fail',conditioning='identical state, target, remaining inventory, observations and fresh context for each recoverer; report source and recoverer; source identity hidden',controls='same-state source-model restart; original self-continuation reported separately',implementation='PLANNED; no state bank exists yet'),
 'robustness':dict(models=selected,definitions=48,panel='same 24 D/M pairs',conditions=visual,rule='identical task pixels/poses except intended observation change; no fabricated corruption or fault hints'),
 'strategies':dict(models=selected,conditions=strategies,panel='same 24 D/M pairs',openLoop='generate action script once, execute one brick at a time; record observations without giving them back; no scripted GT actions',doubleBudget='double decisions only; manipulation cap unchanged and reported',reasoning='no private chain-of-thought scoring; record supported native effort and token usage'),
 'implementationStatus':'design only; observation variants, paired runner, probe UI and recovery state bank require implementation before execution'}
dump(HERE/'evidence/experiment-design.json',plan)
T=HERE/'tables';T.mkdir(exist_ok=True)
def table(file,caption,label,header,rows,cols,wide=True):
 env='table*' if wide else 'table';width=r'\textwidth' if wide else r'\linewidth'
 text=[r'\begin{'+env+'}[t]',r'\centering\small',r'\caption{'+caption+'}',r'\label{'+label+'}',r'\begin{tabularx}{'+width+'}{@{}'+cols+'@{}}',r'\toprule',header+r'\\',r'\midrule']
 text += [' & '.join(row)+r'\\' for row in rows]
 text += [r'\bottomrule',r'\end{tabularx}',r'\end{'+env+'}']
 (T/file).write_text('\n'.join(text)+'\n')
D='---'
allrows=lambda n:[[tex(m['name'])]+[D]*n for m in models]
table('main-models.tex',r'\textbf{E1: named-model primary results (unmeasured).} S: 467 static test cases; M-S: 48 public static cases; D: 168 fault pairs and 72 normal definitions; M: 36 fault pairs and 12 normal episodes. C/T/R: normal completion, actual exposure, conditional recovery. One run per case; source-macro percentages with clustered intervals. Dashes are unmeasured, never zero.','tab:planned-main',r'Model & S & M-S & D C & D T & D R & M C & M T & M R',allrows(8),'Xrrrrrrrr')
table('main-paired.tex',r'\textbf{E2: paired intervention effect (unmeasured).} Same-prefix control/fault branches. $n$: exposed pairs; $\Delta=C_c-C_f$: signed completion drop in percentage points. Expand to all ten models; these three are selected before evaluation.','tab:paired',r'Model & D $n$ & D $\Delta$ & M $n$ & M $\Delta$',[[short[i]]+[D]*4 for i in range(3)],'Xrrrr',False)
table('main-ablations.tex',r'\textbf{E3: input ablations (unmeasured).} Each cell reports D/M recovery; use identical cases and seeds. Sol = GPT-6.1 Sol; Flash = Gemini 3.8 Flash; Qwen = Qwen3.5-27B. M-only manual ablation has no D value. Symbolic input is privileged.','tab:ablations',r'Input condition & Sol & Flash & Qwen',[[v]+([r'n/a / ---']*3 if v.startswith('No manual') else [D]*3) for v in ['Full visual interface','No previous image','No manual (M only)','No candidate preview','Success/failure feedback','Symbolic state']],'Xrrr',False)
# All named models appear in the primary and human tables. Mechanism tables are
# instantiated per model, avoiding 12 tiny score columns and hidden model slots.
kinds=['Removed piece','Shifted piece','Cascaded removal','Extra layer','Early cover','Wrong color','Wrong size','Rotated piece','Swapped positions','Wrong part','Buried color','Compound fault']
table('dynamic-errors.tex',r'\textbf{E4: dynamic error breakdown (unmeasured).} Instantiate one panel per named model in Table~\ref{tab:roster}. Each D family has 14 fault definitions and one run per case. M supports only missing, color, and extra-layer faults; it has 12 definitions per family. Report actual exposure, recovery, and source-clustered intervals separately.','tab:errorresults',r'Track / mechanism & Definitions & Exposed / assigned & Recovery & 95\% CI',[['D: '+k,'14',D,D,D] for k in kinds]+[['M: '+k,'12',D,D,D] for k in ['Missing','Wrong color','Extra layer']],'Xrrrr')
table('human-panel.tex',r'\textbf{E5: independent human/model common panel (unmeasured).} Same 72 conditions for all agents. Six humans yield three independent observations per condition; models have one run per case. Report static completion, D/M normal completion (C), exposure (T), recovery (R), static false alarms (FA), and median active seconds. This panel is separate from primary-table denominators.','tab:humanpanel',r'Agent & S & D C & D T & D R & M C & M T & M R & S FA & Time',[[r'Independent humans']+[D]*9]+allrows(9),'Xrrrrrrrrr')
table('difficulty.tex',r'\textbf{E6: difficulty and source breakdown (unmeasured).} Instantiate per track and named model. Part bands include the 16-piece S tasks; stage and temporary-removal rows apply to D/M. Dev/test comparisons use identical preregistered prompts, no tuning on test; M remains public development. Bands are not measured easy/hard labels.','tab:difficultyresults',r'Stratum & $n$ & Exposed & Success/R',[[x]+[D]*3 for x in ['4--7 parts','8--10 parts','11--16 parts','Early / middle / late','No temporary removal','Temporary removal','Source dev / source test']],'Xrrr',False)
table('failures.tex',r'\textbf{E7: failure ledger (unmeasured).} Per named model and track; attempts may have multiple counters. Do not infer visual detection failure from an incomplete object.','tab:failureledger',r'Observed event & Count & Unit',[[x,D,u] for x,u in [('Provider / transport failure','requests'),('Invalid action format','decisions'),('Rejected physical action','attempts'),('Fault not exposed','fault jobs'),('Wrong finish / budget end','episodes'),('Control pass, fault fail','exposed pairs'),('Wrong anomaly judgment','probe items')]],'Xrl',False)
table('efficiency.tex',r'\textbf{E8: efficiency (unmeasured).} Instantiate separately by track. Count shared prefixes, both continuations, retries, input/output tokens, and hosted charges or measured GPU-hours. $R_c$: fault recovery conditional on exposed pairs whose control succeeds; $n_c$ is its denominator. Report medians and dispersion for counts/time.','tab:efficiencyresults',r'Model & $R_c$ & $n_c$ & Decisions & Inspects & Rejected & Seconds & USD',allrows(7),'Xrrrrrrr')
static_names={'compound':'Compound','missing':'Missing','wrong_color':'Wrong color','repair_state':'Replacement repair state','offset':'Offset','rotation':'Rotation','control':'Normal control','wrong_type':'Wrong type','height_layer':'Layer height','wrong_size':'Wrong size','swapped_positions':'Swapped positions','extra':'Extra piece'}
table('static-errors.tex',r'\textbf{E9: static error breakdown (unmeasured).} Counts are definitions in the current 467-question S test split, not the 3,292-question bank. Instantiate per named model, with one run per case and source-macro completion. Sparse categories are descriptive; repair-state replacements are reported separately.','tab:staticerrors',r'S category & Definitions & Completed / trials & Success & 95\% CI',[[static_names[k],str(sum(c['publicId'] in test and c['category']==k for c in static)),D,D,D] for k in categories],'Xrrrr')
table('repair-quality.tex',r'\textbf{E10: correction quality and collateral damage (unmeasured).} For S and M-static, report terminal defect reduction (DR), target-multiset part F1, exact completion, new damage to initially correct placements (CD), and unnecessary edits on normal controls (UE). Report S and M-static separately; dynamic recovery is reported separately in E1/E2. Temporary removals are allowed; CD measures terminal damage only.','tab:repairquality',r'Model & DR $\uparrow$ & Part F1 $\uparrow$ & Exact $\uparrow$ & CD $\downarrow$ & UE $\downarrow$',allrows(5),'Xrrrrr')
table('perception-probe.tex',r'\textbf{E11: separate detection/localization probe (unmeasured).} Fixed certified snapshots from the 24 D/M control/fault pairs give 48 conditions. Queries never interrupt assembly. BA: balanced change-detection accuracy; TPR/FPR: anomaly recall/false alarms; Loc: affected piece/slot F1. Independent human readability is recorded with the same images.','tab:perceptionprobe',r'Agent & BA & TPR & FPR & Loc & Readable',[[r'Independent humans']+[D]*5]+allrows(5),'Xrrrrr')
table('cross-recovery.tex',r'\textbf{E12: same-state cross-model recovery (unmeasured).} Rows identify the agent that created an off-target placement; columns identify the recoverer. Sol, Flash, and Qwen denote the three diagnostic models. Save the first off-target attachment in normal panel cases, certify recovery; restart all recoverers with identical visible context. Report admitted-state $n$ and recovery separately for D/M. A diagonal restart is not the original uninterrupted self-repair.','tab:crossrecovery',r'State source & $n$ & Sol & Flash & Qwen',[[s]+[D]*4 for s in short],'Xrrrr',False)
table('visual-robustness.tex',r'\textbf{E13: observation robustness (unmeasured).} Same 48-condition D/M panel; instantiate per diagnostic model and track. Base views are $900\times660$; half/double resolution changes only image sampling. One-view hides all alternate views, including inspection. Compare visibility admission before attributing any drop to reasoning.','tab:visualrobustness',r'Observation & Exposed / assigned & Recovery & Decisions & Input tokens',[[x]+[D]*4 for x in ['Full, 900 x 660','Current image only','One fixed view only','Half, 450 x 330','Double, 1800 x 1320']],'Xrrrr')
table('strategy-budget.tex',r'\textbf{E14: planning strategy and budget (unmeasured).} Per diagnostic model and track on the same panel. Open-loop emits one script, still executed one brick at a time. The explicit-check variant uses the same images and public action history; it receives no error label. Double budget changes only the decision cap and retains the manipulation cap. Record native reasoning settings; no private reasoning trace is scored.','tab:strategybudget',r'Strategy & Completion & Exposure & Recovery & Decisions & Seconds & USD',[[x]+[D]*6 for x in ['Closed-loop baseline','One-shot open-loop script','Explicit visual check','Double decision budget']],'Xrrrrrr')
table('model-roster.tex',r'\textbf{Named evaluation candidates.} Official catalogs/model cards checked on 23 October 2026. These are requested IDs, not verified account access or pinned served revisions. Record returned API version or checkpoint commit, inference engine, precision, image processing, and decoding settings before execution. All rows remain unmeasured.','tab:roster',r'Model & Access & Requested API ID / checkpoint',[[tex(m['name']),m['access'],r'\path{'+m['providerModelId']+'}'] for m in models],'l l X')
print('Prepared',len(models),'named models;',len(r['tableMap']),'planned result tables;',plan['workUnits']['total'],'base work units.')
