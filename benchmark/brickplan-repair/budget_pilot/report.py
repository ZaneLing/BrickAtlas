"""Build auditable per-case usage tables and explicitly conditional projections."""
from pathlib import Path
from collections import defaultdict,Counter
import csv,hashlib,html,json,statistics,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import run as pilot
from evaluation_outcomes import assess_run

def mean(xs):return statistics.mean(xs) if xs else None
def calls(r):return r.get('steps',[])+[s for b in r.get('branches',{}).values() for s in b.get('steps',[])]
def label(mid):
    return {'openai/gpt-6.1-sol':'GPT-6.1 Sol','google/gemini-3.8-flash':'Gemini 3.8 Flash','anthropic/claude-sonnet-5.5':'Claude Sonnet 5.5','anthropic/claude-haiku-5.5':'Claude Haiku 5.5','qwen/qwen3.5-27b':'Qwen3.5-27B','qwen/qwen3.5-9b':'Qwen3.5-9B','qwen/qwen3-vl-8b-instruct':'Qwen3-VL-8B','qwen/qwen2.5-vl-72b-instruct':'Qwen2.5-VL-72B','google/gemma-3-12b-it':'Gemma 3-12B'}[mid]

def main():
    out=pilot.OUT;ledger=json.loads((out/'ledger.json').read_text());assert not any(c['status']=='pending' for c in ledger['charges'])
    traces=[json.loads(p.read_text()) for p in sorted((out/'runs').glob('*/trace.json'))]
    rows=[];all_calls=[];hashes={};audit=[]
    for r in traces:
        steps=calls(r);all_calls.extend((r,s) for s in steps)
        score=r.get('moduleScore') or r.get('replayScore') or r.get('episode',{}).get('score',{})
        root=out/'runs'/r['runId'];input_ok=0
        for p in root.glob('**/input-*.json'):
            packet=json.loads(p.read_text())
            for im in packet['images']:
                f=p.parent/im['file'];assert f.exists(),str(f)
                if str(f) not in hashes:hashes[str(f)]=hashlib.sha256(f.read_bytes()).hexdigest()
                assert hashes[str(f)]==im['sha256'];input_ok+=1
            for key in ['oraclePlan','privateEvent','trigger','roots','legalActions','current','target']:
                assert key not in packet['observation'],(r['runId'],key)
        usage=[s['response']['usage'] for s in steps]
        errors=r.get('errors',[])
        evaluation=assess_run(r)
        eligible=r['status'] not in ['api_error','reservation_budget_stop','interface_update_stop']
        row=dict(runId=r['runId'],track=r['track'],caseId=r['caseId'],model=r['model'],label=label(r['model']),status=r['status'],
            modelRequests=r['requests'],returnedResponses=len(steps),inputTokens=sum(u.get('prompt_tokens',0) for u in usage),
            outputTokens=sum(u.get('completion_tokens',0) for u in usage),reasoningTokens=sum(u.get('completion_tokens_details',{}).get('reasoning_tokens',0) for u in usage),
            cachedInputTokens=sum(u.get('prompt_tokens_details',{}).get('cached_tokens',0) for u in usage),
            inputImages=sum(len(s['images']) for s in steps),meanInputTokens=mean([u.get('prompt_tokens',0) for u in usage]),
            meanImages=mean([len(s['images']) for s in steps]),costUSD=r['costUSD'],meanCostPerResponseUSD=r['costUSD']/len(steps) if steps else None,
            success=evaluation['success'],finalEquivalent=score.get('finalEquivalent',score.get('finalGeometryCorrect')) if eligible else None,
            eventTriggered=evaluation['eventTriggered'],
            completionSuccess=evaluation['completionSuccess'],repairSuccess=evaluation['repairSuccess'],
            recoveryPairEligible=evaluation['recoveryPairEligible'],detectionMiss=evaluation['detectionMiss'],
            outcome=evaluation['outcome'],serviceErrors=evaluation['serviceErrors'],
            visualFailure=evaluation['visualFailure'],placementFailure=evaluation['placementFailure'],
            formatErrorResponses=evaluation['formatErrorResponses'],
            actionSchemaErrorResponses=evaluation['actionSchemaErrorResponses'],physicalActionRejections=evaluation['physicalActionRejections'],
            invalidFormatResponses=sum(s['action'].get('type')=='invalid' for s in steps),
            rejectedActions=sum(s.get('feedback',{}).get('code') not in ['OK','OBSERVED','INSPECT','SUCCESS','FINISHED','INCOMPLETE'] for s in steps),
            providers=sorted({s['response'].get('provider','unknown') for s in steps}),
            parserPolicy=r.get('parserPolicy','one-explicit-json-object-with-optional-prose' if r['track'].startswith('M-') else 'strict-json-only (before compatibility repair)'),
            coordinateGuidePresent=any('inspectionCoordinates' in s['observation'] for s in steps),
            errorCodes=[e.get('httpStatus',e.get('message')) for e in errors],
            elapsedSeconds=r.get('elapsedSeconds'),scope=r['scope'])
        row['uncertainReservedUSD']=sum(c['reservedUSD'] for c in ledger['charges'] if c['run']==r['runId'] and c['actualUSD'] is None)
        row['costUpperBoundUSD']=row['costUSD']+row['uncertainReservedUSD']
        assert abs(sum(s['response']['costUSD'] for s in steps)-r['costUSD'])<1e-8
        rows.append(row);audit.append(dict(runId=r['runId'],imageReferencesVerified=input_ok,privateAnswerFieldsAbsent=True))
    confirmed=sum(c['actualUSD'] or 0 for c in ledger['charges']);upper=sum(c['actualUSD'] if c['actualUSD'] is not None else c['reservedUSD'] for c in ledger['charges'])
    assert upper<=10 and abs(sum(r['costUSD'] for r in rows)-confirmed)<1e-8
    summary=dict(schema='brickplan-budget-pilot-summary/2',date='2026-10-23',capUSD=10,confirmedCostUSD=confirmed,
        uncertainReservedUSD=upper-confirmed,spendUpperBoundUSD=upper,submittedRequests=len(ledger['charges']),returnedResponses=len(all_calls),
        attemptedModelCount=len({r['model'] for r in rows}),modelsWithReturnedResponses=len({r['model'] for r,s in all_calls}),
        caseModelJobs=len(rows),distinctCases=len({(r['track'],r['caseId']) for r in rows}),
        inputTokens=sum(r['inputTokens'] for r in rows),outputTokens=sum(r['outputTokens'] for r in rows),reasoningTokens=sum(r['reasoningTokens'] for r in rows),
        outcomeCounts=dict(Counter(r['outcome'] for r in rows)),
        serviceErrorCounts=dict(sum((Counter(r['serviceErrors']) for r in rows),Counter())),
        repairEligiblePairs=sum(r['recoveryPairEligible'] for r in rows),
        formatErrorResponses=sum(r['formatErrorResponses'] for r in rows),
        rows=rows,limits=['Development pilot; one attempt per model/case.',
            'Historical requests use the old image protocol. Reclassification changes accounting only; it is not a rerun of the repaired interface.',
            'Untriggered episodes have null repair/detection scores. Unpaired M dynamic outcomes are descriptive observations, not main recovery evidence.',
            'S uses a new three-view visual API adapter over the current plate5 cases/executor; it is not a formal score collection.',
            'Input/response compatibility was repaired between cases; phases must not be pooled into a leaderboard.',
            'D from-empty runs did not produce a completed matched-prefix control/fault pair. M dynamic episodes are full policy runs, unpaired.',
            'M trial images predate the inspection-timeline repair. Original images are preserved; these trials cannot certify the repaired interface.',
            'Provider-rejected or timed-out jobs have no model ability score; uncertain charges retain their full reservation.',
            'Small, purposive development sample; no population success rate or exact full-suite quote.'])
    pilot.dump(out/'summary.json',summary)
    with (out/'per-case.csv').open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in r.items()} for r in rows)
    public_ledger={k:v for k,v in ledger.items() if k!='charges'}
    public_ledger['charges']=[{k:v for k,v in c.items() if not k.startswith('accountUsage')} for c in ledger['charges']]
    pilot.dump(out/'ledger-public.json',public_ledger)
    pilot.dump(out/'verification.json',dict(status='PASS',scope='Billing, image hashes and submitted observation-field isolation; no population/human validity certificate.',
        confirmedCostUSD=confirmed,upperBoundUSD=upper,budgetCapUSD=10,noPendingRequests=True,distinctImagesVerified=len(hashes),
        sourceImagesVerified=audit,singleAttemptKeysUnique=len({r['runId'] for r in rows})==len(rows),
        requestedApiErrorsHaveNoAbilityScore=True))
    projection=project(summary,all_calls)
    pilot.dump(out/'projection.json',projection)
    make_html(out,summary,traces,projection)
    print(json.dumps({k:v for k,v in summary.items() if k not in ['rows','limits']},ensure_ascii=False,indent=2))
    print('PROJECTION',json.dumps(projection['totals'],ensure_ascii=False))

def project(summary,all_calls):
    """Keep request-count assumptions separate from measured per-request prices."""
    catalogue={m['id']:m for m in json.loads((pilot.OUT/'catalogue.json').read_text())['data']}
    original=['openai/gpt-6.1-sol','anthropic/claude-sonnet-5.5','google/gemini-3.8-flash','anthropic/claude-haiku-5.5','qwen/qwen3.5-9b','qwen/qwen3.5-27b','google/gemma-3-12b-it']
    profiles=defaultdict(list)
    for r,s in all_calls:profiles[(r['model'],r['track'])].append(s['response'])
    common={t:[s['response'] for r,s in all_calls if r['track']==t] for t in ['S','D','M-S','M-D']}
    def unit(m,t):
        rs=profiles[(m,t)]
        if rs:return mean([r['costUSD'] for r in rs]),'measured per-response mean'
        rs=common[t] or common['S'];p=mean([r['usage']['prompt_tokens'] for r in rs]);q=mean([r['usage']['completion_tokens'] for r in rs])
        price=catalogue[m]['pricing'];return (p*float(price['prompt'])+q*float(price['completion']))*1.15,'price-converted from other models; not measured on this track'
    counts=json.loads((pilot.OUT/'preflight/module-image-counts.json').read_text());module_factor=mean([x['laterDynamicImages'] for x in counts])/48
    plan=json.loads((pilot.ROOT/'paper/brickplan-cvpr/evidence/experiment-design.json').read_text())['primary']
    # Baseline counts reproduce the previous plan; expanded counts allow the
    # inspection/search overhead observed here. These remain assumptions.
    scenarios={'previous-request-counts':dict(static=10,normal=22,paired=38),
               'more-inspection-and-search':dict(static=22,normal=40,paired=70)}
    result=[]
    for m in original:
        units={t:dict(zip(['usd','basis'],unit(m,t))) for t in common}
        costs={}
        for name,n in scenarios.items():
            s=len(plan['S']['caseIds'])*n['static']*units['S']['usd']
            d=(len(plan['D']['normalIds'])*n['normal']+len(plan['D']['faultIds'])*n['paired'])*units['D']['usd']
            ms=len(plan['M']['staticIds'])*n['static']*units['M-S']['usd']*module_factor
            md=(len(plan['M']['normalIds'])*n['normal']+len(plan['M']['faultIds'])*n['paired'])*units['M-D']['usd']*module_factor
            costs[name]=dict(S=round(s,2),D=round(d,2),MStatic=round(ms,2),MDynamic=round(md,2),total=round(s+d+ms+md,2))
        result.append(dict(model=m,unitCosts=units,scenarios=costs))
    base=[sum(r['scenarios'][n]['total'] for r in result) for n in scenarios]
    # The original three diagnostic models, 48 conditions, 10.5 nonbaseline
    # panel equivalents, 30 decisions/condition. Half the panel is D, half M.
    diagnostics=0
    for m in ['openai/gpt-6.1-sol','google/gemini-3.8-flash','qwen/qwen3.5-27b']:
        diagnostics+=15120*(unit(m,'D')[0]+unit(m,'M-D')[0]*module_factor)/2
    totals=dict(sevenCatalogModelsPrimaryUSD=[round(x,2) for x in base],additionalVariantPanelUSD=round(diagnostics,2),
        additionalOtherAnalysisAllowanceUSD=[150,400],missingThreeModelDeploymentAllowanceUSD=[300,1000],reserveFraction=.2)
    totals['primaryWithMissingModelsAndReserveUSD']=[round((base[0]+300)*1.2,2),round((base[1]+1000)*1.2,2)]
    totals['allPlannedWithAllowancesAndReserveUSD']=[round((base[0]+300+diagnostics+150)*1.2,2),round((base[1]+1000+diagnostics+400)*1.2,2)]
    return dict(status='CONDITIONAL_ESTIMATE_NOT_FULL_RUN',models=result,requestCounts=scenarios,moduleImageScaleFactor=module_factor,
        inputProtocol='Historical pilot before matched-canvas/on-demand-manual changes; NOT a price estimate measured under the new protocol.',
        totals=totals,limits=['Only seven original-roster IDs are in the API catalogue; InternVL3.5-8B and Qwen2.5-VL-7B/32B require a different serving route.',
          'The missing-model deployment allowance is a planning reserve, not measured GPU throughput or a vendor quote.',
          'All D branching costs remain projected; service refusals and untriggered runs do not measure recovery.',
          'Additional variants retain the prior design of 15120 decisions per diagnostic model; not a measured job count.',
          'Prices/routes and tokenization differ. No cache discount assumed; M size scaling is approximate and must be piloted on larger modules.',
          'Excludes human pay, tax, full 5260-record sweep and repeated model runs. No hard upper bound.'])

def make_html(out,s,traces,p):
    e=html.escape
    body=f'<h1>10 美元静态／动态试跑</h1><p>2026-10-23 · 已确认 ${s["confirmedCostUSD"]:.4f}；含未确认请求全部预留的上界 ${s["spendUpperBoundUSD"]:.4f}；授权上限 $10。</p><p>尝试 {s["attemptedModelCount"]} 个模型，{s["caseModelJobs"]} 个模型×题目组合。每个组合只尝试一次。接口修正前后的记录分开保留，不作为正式排名。</p><p><a href="README.zh-CN.md">中文总结与预算</a> · <a href="per-case.csv">逐题用量 CSV</a> · <a href="projection.json">预算计算</a></p>'
    body+='<table><thead><tr><th>模型</th><th>部分／题目</th><th>调用／返回</th><th>输入／输出 token</th><th>美元</th><th>结果</th></tr></thead><tbody>'
    for row,r in zip(s['rows'],traces):
        labels={'service_error':'接口故障，不计能力','evaluation_stopped':'评测中止，不计能力',
                'untriggered':'未触发干扰，不计漏检／修复失败','unpaired_observation':'干扰已触发；单条观察，缺正常对照',
                'completed':'完成','task_incomplete':'任务未完成','control_failed':'正常分支未成功，不计修复分数',
                'repair_completed':'配对修复完成','repair_incomplete':'配对修复未完成','run_interrupted':'运行中断'}
        result=labels.get(row['outcome'],row['outcome'])
        if row['serviceErrors']:
            categories={'request_rejected':'请求被拒绝','rate_limited':'限流','timeout':'超时',
                        'provider_unavailable':'服务不可用','request_error':'请求错误',
                        'transport_or_adapter_error':'传输／适配器错误'}
            result+='；'+ '，'.join(f'{categories.get(k,k)} {v} 次' for k,v in row['serviceErrors'].items())
        if row['outcome']=='unpaired_observation':result+='；本条'+('完成' if row['completionSuccess'] else '未完成')
        if row['formatErrorResponses']:result+=f'；格式错误 {row["formatErrorResponses"]} 次'
        cost=f'${row["costUSD"]:.4f}' if not row['uncertainReservedUSD'] else f'未确认；预留 ${row["uncertainReservedUSD"]:.4f}'
        body+=f'<tr><td>{e(row["label"])}</td><td>{e(row["track"])} / {e(row["caseId"])}</td><td>{row["modelRequests"]} / {row["returnedResponses"]}</td><td>{row["inputTokens"]:,} / {row["outputTokens"]:,}</td><td>{cost}</td><td>{result}<br>{e(row["status"])}</td></tr>'
    body+='</tbody></table><h2>逐步记录</h2><p>展开后可看模型原始回答、动作反馈和实际收到的图片。图片在本机运行目录；仓库中的汇总文件不包含大批原始图片。</p>'
    for r in traces:
        body+=f'<details><summary>{e(label(r["model"]))} · {e(r["track"])} · {e(r["caseId"])}</summary>'
        for st in calls(r):
            response=st['response'];body+=f'<section><h3>决策 {st["index"]+1} · ${response["costUSD"]:.5f}</h3><pre>{e(response["content"])}</pre><p>执行反馈：{e(json.dumps(st.get("feedback"),ensure_ascii=False))}</p><div class="images">'
            for im in st['images']:
                # S/D images are under prefix; module assets are at run root.
                prefix='prefix/' if r['track'] in ('S','D') else ''
                src=f'runs/{r["runId"]}/{prefix}{im["file"]}'
                body+=f'<figure><a href="{e(src)}"><img loading="lazy" src="{e(src)}"></a><figcaption>{e(im["role"])} {e(str(im.get("view",im.get("step",""))))}</figcaption></figure>'
            body+='</div></section>'
        body+='</details>'
    style='body{font:16px/1.6 system-ui;max-width:1400px;margin:36px auto;padding:0 24px;color:#203040}table{width:100%;border-collapse:collapse;font-size:14px}th,td{padding:9px;border-bottom:1px solid #ddd;text-align:left}th{background:#edf2f7}details{border:1px solid #ddd;margin:12px 0;padding:12px}summary{cursor:pointer;font-weight:600}pre{white-space:pre-wrap;background:#f5f7fa;padding:12px}.images{display:flex;flex-wrap:wrap;gap:8px}figure{margin:0;width:260px}img{max-width:100%;max-height:240px;object-fit:contain}figcaption{font-size:12px}section{border-top:1px solid #ddd;margin-top:18px}'
    (out/'report.html').write_text('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>BrickPlan $10 pilot</title><style>'+style+'</style>'+body+'</html>')

if __name__=='__main__':main()
