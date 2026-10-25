"""Reserved result tables and task assignments for the current specification.

Every result field is null. The task lists are candidate pools, not visual admission.
"""
from pathlib import Path
from collections import Counter
import hashlib,json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
SPEC=ROOT/'deliverables/brickplan-benchmark-spec'
q=[json.loads(l) for l in (SPEC/'questions.jsonl').read_text().splitlines()]
q=[r for r in q if not r['isAlias'] and r['mainTaskCandidate']]
roster=json.loads((HERE/'evidence/model-roster.json').read_text())
models=roster['models']; names=[m['name'] for m in models]
TABLES={}

def table(file,label,title,columns,rows,wide=False,align=None,foot=None):
    env='table*' if wide else 'table'; width=r'\textwidth' if wide else r'\linewidth'
    align=align or ('X'+'r'*(len(columns)-1))
    lines=[r'\begin{'+env+'}[t]',r'\centering\small',r'\caption{\textbf{'+title.split('|')[0]+'} '+title.split('|',1)[1]+'}',
        r'\label{tab:'+label+'}',r'\begin{tabularx}{'+width+r'}{@{}'+align+r'@{}}',r'\toprule',
        ' & '.join(columns)+r'\\',r'\midrule']
    lines+=[' & '.join(str(x) for x in row)+r'\\' for row in rows]
    lines += [r'\bottomrule',r'\end{tabularx}']
    if foot:lines += [r'\par\vspace{2pt}{\footnotesize '+foot+'}']
    lines += [r'\end{'+env+'}']
    (HERE/'tables'/f'{file}.tex').write_text('\n'.join(lines)+'\n')
    TABLES[file]=dict(label=label,title=title.split('|')[0],columns=columns,
        rows=[dict(identifier=str(row[0]),results={c:None for c in columns[1:]}) for row in rows],
        status='NOT_RUN')

blank=lambda labels,n:[[x]+['---']*n for x in labels]
table('main-models','static-main','E1: static repair (unmeasured).| Local-static panel; repeat the same schema separately for whole-object and named-module stages. SR/F1/ER/DR use S1; FR uses S0. Source- and object-macro estimates, valid counts, and coverage accompany results. Dashes are unmeasured, never zero.',
 ['Model','SR $\\uparrow$','Place F1 $\\uparrow$','ER $\\uparrow$','DR $\\downarrow$','FR $\\downarrow$','Valid $N$'],blank(names,6),True)
table('main-dynamic','dynamic-main','E2: dynamic construction and recovery (unmeasured).| W/M: whole-object/named-module scope. BCR uses D0; CRR requires normal success and verified complete exposure; $\\Delta$ uses eligible pairs without filtering control success. Report D1 and D2 separately. ICR, TR and eligibility counts are retained in E3/E6/E9 and the ledger.',
 ['Model','W BCR','W CRR','W $\\Delta$','M BCR','M CRR','M $\\Delta$'],blank(names,6),True)
table('main-paired','paired','E3: paired outcomes (unmeasured).| Repeat for each model, dynamic scope, and D1/D2. $n_{cf}$ counts control/fault success. CRR uses $n_{11}/(n_{11}+n_{10})$; signed $\\Delta$ uses all four cells. Only prefix-, exposure-, and effect-qualified pairs enter.',
 ['Scope','$n_{11}$','$n_{10}$','$n_{01}$','$n_{00}$'],blank(['Whole / D1','Module / D1','Whole / D2','Module / D2'],4))
table('main-ablations','ablations','E4: input controls (unmeasured).| Sol, Flash, and Qwen 27B are preselected diagnostic candidates. Report track-specific SR/BCR/CRR and counts. Manual removal applies only where a manual exists. Explicit state is privileged.',
 ['Condition','Sol','Flash','Qwen'],blank(['Default RGB interface','No previous scene','No manual (supported tasks)','No candidate preview','Reduced legality feedback','Explicit state assistance'],3))

# Counts are catalogue assignments, not result denominators.
codes=['E01','E02','E03','E04','E05','E06','E07']; labels=['Missing','Extra','Color','Part','Position','Orientation','Swap']
static=[r for r in q if r['mode']=='static'];wd=[r for r in q if r['track']=='whole-object-dynamic'];md=[r for r in q if r['track']=='named-module-dynamic']
err_rows=[]
for code,name in zip(codes,labels):
    err_rows.append([code+' '+name,sum(code in r['errorCodes'] for r in static),'---','---','---','---'])
table('static-errors','static-errors','E5: static error breakdown (unmeasured).| Assigned counts are current main-static multilabel coverage, including process-tagged cases. Repeat results by source scope and model; controls are separate.',
 ['Label','Assigned','SR','F1','ER','DR'],err_rows,True)
dyn_rows=[]
for code,name in zip(codes,labels):
    dyn_rows.append([code+' '+name,sum(code in r['errorCodes'] for r in wd),sum(code in r['errorCodes'] for r in md),'---','---','---','---'])
table('dynamic-errors','dynamic-errors','E6: dynamic errors (unmeasured).| W/M assignment counts are multilabel. The module-swap cell has zero assigned tasks and yields N/A, not a model failure. ICR uses valid assigned runs; CRR and $\\Delta$ use their declared paired populations.',
 ['Label','W assigned','M assigned','ICR','TR','CRR','$\\Delta$'],dyn_rows,True)
table('repair-quality','repair-quality','E7: stage-repair quality (unmeasured).| Repeat for each named model and each scope. Missing/excess rates track only original defects; they cannot replace exact SR. Context is excluded. S0 false repair has a separate denominator.',
 ['Scope','SR','Place F1','Missing recovered','Excess cleared','DR','S0 FR'],blank(['Local structure','Whole-object stage','Named-module stage'],6),True)
strata=[]
for field,levels in [('buildLength',['B1','B2','B3']),('rework',['R0','R1','R2','R3']),('eventLevel',['T0','T1','T2','T3']),('planningLevel',['G1','G2','G3'])]:
    c=Counter(r[field] for r in q)
    for level in levels:strata.append([level,c[level],'---','---','---'])
table('difficulty','difficulty','E8: structural strata (unmeasured).| Counts include all main candidates. Static B uses the stage target; R uses a feasible witness. Report outcomes by track/task type rather than pooling these strata into one score. G is provisional, not measured difficulty.',
 ['Stratum','Assigned','SR/BCR','CRR','Eligible $N$'],strata)
table('multi-events','multi-events','E9: repeated interventions (unmeasured).| Main D2 has 37 two-event and six three-event tasks. All-event CRR requires successful normal control and complete effective exposure. Partial exposure is retained in the ledger. Retention needs sufficient follow-up.',
 ['Events','Assigned','All-event CRR','Event recovery','Retention','Partial $N$'],[[2,37,'---','---','---','---'],[3,6,'---','---','---','---']],True)
table('checkpoint','checkpoint','E10: checkpoint continuation (planned bank).| The system builds the prefix; this is not agent-built progress. No independent C bank or current CSR results exist. Repair@k requires adequate observation windows; censoring is separate.',
 ['Scope','CSR','Repair@2','@4','@8','Valid $N$'],blank(['Whole object','Named module'],5),True)
table('modality','modality','E11: input modality and state assistance (planned).| RGB means images plus neutral rules and anonymous action handles. Text state can expose occluded geometry and is not information-equivalent to RGB. No unified text-state task list has been executed.',
 ['Input','Static SR','D0 BCR','CRR','Valid $N$'],blank(['RGB + neutral task text','Explicit text state','RGB + explicit state'],4))
table('action-output','action-output','E12: output localization (planned).| Coordinates add pose estimation to action choice. Build the coordinate adapter and matched cases before comparison. Keep geometry, goals, and information fixed.',
 ['Output','SR/BCR','CRR','Schema errors','Valid $N$'],blank(['Anonymous candidate ID','Free position + orientation'],4),True)
table('perception-probe','perception','E13: independent snapshot detection (planned).| Includes normal controls and changed scenes. No in-loop diagnosis is required. Use multilabel location sets; the adapter and independent judgments are pending.',
 ['Agent','Precision','Recall','F1','False positive','Location F1'],blank(['Human panel','Sol','Flash','Qwen 27B'],5),True)
table('cross-recovery','cross','E14: same-state cross-model repair (planned).| Select witnessed off-target states independently of recoverer outcomes. Every recoverer receives the identical state. Repeat by track; these restarts do not measure uninterrupted self-repair.',
 ['State source / recoverer','Sol','Flash','Qwen 27B'],blank(['Sol','Flash','Qwen 27B'],3))
table('visual-robustness','visual','E15: observation robustness (unmeasured).| Keep camera/geometry fixed for resolution tests; restrict inspection too for single-view tests. Record delivered images and recheck visibility. Repeat separately by track and task type.',
 ['Condition','SR/BCR','CRR','Valid $N$'],blank(['Native comparison canvas','One fixed view','No previous scene','Half image resolution','Double image resolution'],3))
table('strategy-budget','strategy','E16: planning and computation (planned).| An open-loop script still executes one physical action at a time. Keep task lists and manipulation caps fixed; record computation and cost. No private reasoning trace is scored.',
 ['Strategy','SR/BCR','CRR','Decisions','USD'],blank(['Standard closed loop','Open-loop action script','Explicit visual checking','Double decision allowance'],4))
table('efficiency','efficiency','E17: cost and action efficiency (unmeasured).| Include shared prefixes, both continuations, billed errors and retries. Attempt/reference is relative to a feasible witness, not proven optimality. Repeat per scope, task type, and model.',
 ['Model','Decisions','Inspect','Attempt/ref.','Image tokens','USD/task','USD/success'],blank(names,6),True)
table('human-panel','human','E18: independent human operation (planned).| Graphical actions only. The proposed 72-condition panel spans static, whole-dynamic, and module-dynamic tasks; six participants provide three observations per condition without seeing both pair members. Current task selection and schedules require qualification. Independent humans are not cloned-prefix pairs; checkpoint comparisons are labeled C.',
 ['Agent','Static SR','BCR','ICR','TR','Valid $N$'],blank(['Human (independent)','Sol','Flash','Qwen 27B'],5))
table('failures','failures','E19: validity and failure ledger (unmeasured).| Format, schema/IDs, physics, construction, exposure, and service outcomes are separate. Categories can co-occur; do not force their sum to equal failure N.',
 ['Record','Count','Rate / coverage'],blank(['Planned / valid attempts','Parsing errors','Schema / handle errors','Physical rejections','Normal controls failed','Events untriggered','Events partially triggered','Incident effect unverified','Eligible CRR pairs','Model budget exhausted','Final service error','Harness error / external stop'],2))

# Evidence records contain candidate IDs, not old claimed evaluation allocations.
def ids(pool):return [r['id'] for r in pool]
plan=dict(schema='brickplan-current-experiment-design/1',date='2026-10-25',status='PLANNED_NOT_EXECUTED',
    inputVersion='brick-atlas-direct-actions-full-context/1',models=models,repetitions=1,handleSeeds=[41],
    mainCandidates=5452,requiresCurrentInterfaceVisualAdmission=True,
    candidatePools={t:ids([r for r in q if r['track']==t]) for t in sorted({r['track'] for r in q})},
    assignedExistingSourceTest={t:ids([r for r in q if r['track']==t and r['sourceSplit']=='test-existing-source']) for t in sorted({r['track'] for r in q})},
    testScope='Audited existing-source allocation, not untouched community/new-source generalization.',
    unknownFinalEvaluationN=True,independentCheckpointBankImplemented=False,
    independentDetectionBankImplemented=False,paidModelCalls=0,
    diagnosticModels=roster['diagnosticModels'],resultTables=list(TABLES),
    proposedDecisionCap='max(40,6*N+20), with native manipulation caps recorded',
    human=dict(status='PLANNED_REQUIRES_NEW_CASE_SELECTION',participants=6,pairs=36,conditions=72,
        operations=216,freeTextRequired=False,independentSubmissionsRequired=True),
    obsoletePlans='evidence/experiment-design.json and budget-single-run.json describe the 23 Oct historical plan only; no current work-unit or dollar estimate is claimed.')
(HERE/'evidence/current-experiment-design.json').write_text(json.dumps(plan,indent=2)+'\n')
(HERE/'evidence/current-results-template.json').write_text(json.dumps(dict(schema='brickplan-current-results/1',status='NOT_RUN',
    tables=TABLES,inputVersion=plan['inputVersion'],models=models,repetitions=1),indent=2)+'\n')
print('RESULT TABLES',len(TABLES),'all unmeasured')
