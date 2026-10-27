"""Write owner documentation and a separate quality-round manifest.

Does not alter task identities, participant answers, the published snapshot,
or the paper. This report contains privileged condition labels: not for blind
participants before they submit their own operation.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
from bench_design import ROOT
from bench_design.challenges import QUALITY,PATTERNS
from bench_design.session import INPUT_VERSION
from bench_design.policy import INPUT_VERSION as SNAPSHOT_VERSION
from expansion_v7.build import read,write

NAMES={
    'v7-long-bookshelf':'书架','v7-long-city-bus':'城市巴士',
    'v7-long-stone-bridge':'石桥','v7-long-gantry-press':'龙门压力机',
    'v7-long-cottage':'小屋','museum-roof-long':'博物馆屋顶',
    'cottage-roof':'小屋屋顶','racer-top':'赛车上部','seaplane-tail':'水上飞机尾部',
    'repair-truck-cab':'维修车驾驶室','panda-head':'熊猫头',
    'burger-stand-roof':'汉堡摊屋顶','white-house-roof':'白宫屋顶',
    'police-helicopter-top':'警用直升机顶部','rockefeller-crown':'洛克菲勒大厦顶部',
    'brandenburg-top':'勃兰登堡门顶部'}
FAMILIES={'offset':'位置偏移','extra-layer':'偷偷多装一层','buried-repair':'内部错色，需要拆上层返修',
    'wrong-color':'换错颜色','missing':'少件','wrong-part':'换错零件',
    'rotated':'装反／方向错误','early-cover':'提前封口挡路','left-right-swap':'不同零件互换位置'}


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    items=read(QUALITY/'challenges.private.json.gz')['cases']
    tasks=read(QUALITY/'review-tasks.private.json')
    codes={r['caseId']:r['code'] for r in tasks['blind']}
    probes=read(QUALITY/'physics-probes.private.json.gz')['probes']
    checks=read(QUALITY/'targeted-judge-check.json')
    published=[json.loads(l) for l in (ROOT/'deliverables/brickplan-benchmark-spec/questions.jsonl').read_text().splitlines()]
    old={r['id']:r for r in published}
    assert len(items)==len({r['id'] for r in items})==44
    assert len(tasks['blind'])==len(set(codes.values()))==71
    assert all(x['id'] in codes for x in items)
    assert all(x['evaluationMetadata']['source']==old[x['evaluationMetadata']['normalCanonicalId']]['source'] for x in items)
    assert not {h for x in items for h in x['case']['humanErrorIds']}&{'H12','H14','H15','H16','H17','H18'}
    assert checks['status']=='PASS' and checks['passed']==44 and checks['events']==92
    assert len(probes)==32
    uncertain=[p for p in probes if p['independentResult']['status'] in
               ('needs-review','accepted-action-has-independent-collision')]
    lines=['# 关键题目清单：检查什么、给什么、怎样算完成','',
        '**新版页面用于看图检查GT，不需要亲自拼装。** 默认展示当前、GT结果和本题目标；只选GT正确、有问题或看不清。模型实验和旧版盲做仍使用各自的原协议，本页不计盲做成绩。','',
        '## 先看6道重点题','',
        '| 页面题号 | 检查重点 | 为什么保留 |','|---|---|---|',
        '| [Q001](http://127.0.0.1:8808/A?task=Q001) | 原有完整物件的错色静态修复 | 检查当前图、目标图和选位置能否看懂。 |',
        '| [Q002](http://127.0.0.1:8808/A?task=Q002) | 原有完整物件的无错静态对照 | 左右一样时允许直接结束，不能诱导多拆多装。 |',
        '| [Q003](http://127.0.0.1:8808/A?task=Q003) | 书架内部返修 | 检查遮挡、拆上层、换内部件和装回。 |',
        '| [Q004](http://127.0.0.1:8808/A?task=Q004) | 小屋屋顶正常拼装 | 检查没有事故时，能否按说明和实际状态完成。 |',
        '| [Q005](http://127.0.0.1:8808/A?task=Q005) | 书架修到一半又有事故 | 检查两个问题重叠时，记录与返修是否正确。 |',
        '| [Q006](http://127.0.0.1:8808/A?task=Q006) | 连续三次事故 | 检查修过之后是否仍能继续观察、恢复、完成。 |','',
        '上面链接以A为例。B、C使用自己的入口再选同一题，答案不会互相复制。每题单独提交，不要求做完整个列表。以下输入输出表描述原题；看GT的审查页会额外展示参考修复结果和步骤。','',
        '## 题目的输入、操作与GT','',
        '| 项目 | 具体内容 |','|---|---|',
        '| 输入 | 左边当前状态，右边本题唯一目标；相同画布的多个视角；全部零件；按需查看的说明和位置假设图。 |',
        '| 中间操作 | 一次装一块或拆一块；可以换视角、点当前积木、查看该零件全部位置、看说明；过程不会插入“是否发现故障”的问卷。 |',
        '| 输出 | 真人点按钮完成动作，最后结束并选择检查选项；模型调用相同动作接口。 |',
        '| GT | 最终可操作部分的形状、颜色和位置与目标物理等价，且每个动作合法。相同零件换编号、合法顺序改变，不扣分。 |',
        '| 参考动作 | 证明存在一种合法做法；不代表唯一顺序，也不保证最短。下表的动作数不含查看和结束。 |',
        '| 事故时刻 | 由当前安装情况和动作间隔触发。下表给出参考运行里实际发生的位置，不要求参与者按此步数操作。 |',
        '| 未触发 | 单列“不适用”；没有经历事故，不能算漏检或修复失败。 |',
        '| 连续事故 | 记录每次事故后到下一次事故前是否修复，同时独立记录最终是否拼好。 |','',
        '## 级别用人话解释','',
        '- B1：目标不超过12块；B2：13–24块；B3：超过24块。固定背景不计入操作目标。',
        '- R1：参考返修较短；R2：需要多步；R3：要拆正确的盖件，或参考返修至少7步。',
        '- T1/T2/T3：一轮中安排1/2/3次事故。',
        '- G1/G2/G3：按件数、返修和事故数得到的结构级别；不是已经由真人或模型验证的简单／中等／困难。',
        '- 实际难度还要结合真人完成率、耗时、查看次数和模型运行结果判断。','',
        '## 16个物件／模块','',
        '| 物件 | 内容范围 | 本轮条件数 | 可操作目标件数 |','|---|---|---:|---:|']
    for model in sorted({x['model'] for x in items}):
        group=[x for x in items if x['model']==model]
        lines.append(f"| {NAMES[model]}（`{model}`） | {'完整物件' if model.startswith('v7-long-') else '有完整物件背景的命名模块'} | {len(group)} | {group[0]['descriptors']['activeParts']} |")
    for category,families,purpose,gap in PATTERNS:
        group=[x for x in items if x['category']==category]
        lines+=['',f'## {purpose}（{len(group)}题）','',
            '| 页面 | 物件 | 实际错误顺序 | 件数 | 级别 B/R/T/G | 参考总动作数 | 参考事故动作点 | 前错未修完又出错 |',
            '|---|---|---|---:|---|---:|---|---|']
        for x in group:
            d=x['descriptors'];case=x['case'];code=codes[x['id']]
            levels='/'.join(d[k] for k in ['buildLength','rework','eventLevel','planningLevel'])
            errors=' → '.join(FAMILIES[e['family']] for e in case['events'])
            timing='、'.join(str(e['atManipulation']) for e in case['referenceEvents'])
            lines.append(f"| [{code}](http://127.0.0.1:8808/A?task={code}) | {NAMES[x['model']]} | {errors} | {d['activeParts']} | {levels} | {len(case['referenceActions'])} | {timing} | {'是' if case['actualOverlapDuringUnrepairedWindow'] else '否'} |")
    lines+=['','## 已检查与待检查','',
        '- 44题均通过真实运行器回放；92次事故全部实际触发，并通过效果核验。参考动作使用答案，不能当作模型成绩。',
        '- 独立布尔几何算法抽查32个动作：31项在相应几何范围内结论一致，1项信息不足，保持待查。',
        '- 这32个动作不是对44题所有合法／非法动作的穷举；没有抽查到的动作不能据此自动通过。',
        '- 44个新增条件目前全部等待真人和相应独立复核，未计入原5,720题的正式目录。',
        '- 无真人提交时只显示待审；看不懂、不会操作、判断分歧、没有完成，均留下具体记录再检查。','',
        '| 待查项 | 关联盲做题 | 具体原因 | 当前处理 |','|---|---|---|---|']
    for p in uncertain:
        why='；'.join(x['actor']+'背景件缺少可靠碰撞体，且其范围与待查路径相交' for x in p['independentResult']['unresolved']) or p['independentResult']['status']
        lines.append(f"| {p['code']} | {p['sameAsBlindCase']}，{NAMES[next(x['model'] for x in items if x['id']==p['caseId'])]} | {why} | 暂停本项纳入；补可靠网格或第三方／实物证据。 |")
    lines+=['','## 页面截图','',
        '下面是隔离测试账户的界面截图，模拟答案不计入真人统计。每道题的实际图像在对应页面中查看。','',
        '![简版GT检查：当前、参考修复结果与目标](gt-interface-evidence/desktop.png)','']
    (QUALITY/'KEY-CASES.zh-CN.md').write_text('\n'.join(lines))
    contract=dict(activeInputVersion=INPUT_VERSION,publishedSnapshotInputVersion=SNAPSHOT_VERSION,
        sameModelHumanActionInformation=True,humanGUIFormattingBurdenDifferent=True,
        positionCards='All registered candidates, neutral ordering; no correctness/legality labels',
        finalCriterion='Physical target multiset equivalence, explicit finish, legal direct actions; no unique reference order',
        mechanicsScope='Fixed context, rigid inset meshes, continuous straight paths; fixtures allowed; no gravity/friction/clutch certification',
        newConditions=44,existingPublishedTasks=5720,newConditionsAddedToPublishedSnapshot=False,
        blindTasks=71,priorityTasks=6,physicalProbes=32,independentGeometryUnresolved=[p['code'] for p in uncertain],
        noRealHumanResultClaimed=True,noProviderCalls=True,noPaperChanges=True,
        defaultHumanReview='Answer-visible GT inspection, three choices; no assembly required',
        gtInspectionIsBlindHumanPerformance=False,priorOperationAnswersPreserved=True)
    write(QUALITY/'runtime-contract.json',contract)
    code=list((ROOT/'benchmark/brickplan-repair/bench_design').glob('*.py'))+[
        ROOT/'benchmark/brickplan-repair/bench_design/human_review.html',
        ROOT/'benchmark/brickplan-repair/bench_design/gt_review.html',
        ROOT/'benchmark/brickplan-repair/bench_design/test_gt_review.mjs',
        ROOT/'benchmark/brickplan-repair/bench_design/test_quality_ui.mjs',
        ROOT/'benchmark/brickplan-repair/bench_design/requirements-quality.txt']
    native=['assembly.py','baseplate.py','library.py','qualify.py','evaluation_outcomes.py',
        'community_modules/core.py','community_modules/run_episode.py',
        'recognizable_models/run_episode.py','dynamic_v5/vision.py',
        'dynamic_v6/episode.py','dynamic_v6/interface.py','budget_pilot/run.py',
        'expansion_v7/runtime.py','expansion_v7/build.py','expansion_v7/scope.py',
        'expansion_v7/run_episode.py','eval/render.py','eval/matched_canvas.py']
    code.extend(ROOT/'benchmark/brickplan-repair'/p for p in native)
    code.append(ROOT/'benchmark/brickplan-v1/geometry.py')
    data=[QUALITY/n for n in ['challenges.private.json.gz','challenge-catalogue.json','challenge-generation.json',
        'review-tasks.private.json','physics-probes.private.json.gz','targeted-judge-check.json',
        'evaluation-wiring-checks.json','independent-geometry-check.json','runtime-contract.json',
        'interface-evidence/automated-ui-check.json','metric-unit-check.json',
        'paired-cli-evidence/scored.json','paired-cli-evidence/run/pair.private.json',
        'gt-preview-replay-check.json','gt-interface-evidence/ui-check.json']]
    unchanged=[ROOT/'deliverables/brickplan-benchmark-spec/questions.jsonl']
    generation=read(QUALITY/'challenge-generation.json')
    for group in generation['sources'].values():
        for name,expected in group.items():
            assert sha(ROOT/name)==expected,'Source changed: '+name
            unchanged.append(ROOT/name)
    manifest=dict(schema='brick-atlas-quality-round-manifest/1',
        code={str(p.relative_to(ROOT)):sha(p) for p in code},
        evidence={str(p.relative_to(ROOT)):sha(p) for p in data},
        originalSourceInputs={str(p.relative_to(ROOT)):sha(p) for p in sorted(set(unchanged))},
        checks=dict(conditions=44,effectiveIncidents=92,blindTasks=71,physicalProbes=32,
                    independentGeometryResolved=32-len(uncertain),independentGeometryUnresolved=len(uncertain),
                    sourceGroupsInherited=True,excludedHumanCategoriesAbsent=True),
        apiCalls=0,humanResults='Use actual local owner summary; never this generated manifest',
        archivedPaperSnapshot='Unchanged; old paper code-hash snapshot is not a certificate of this new runtime')
    write(QUALITY/'quality-manifest.json',manifest)
    print(json.dumps(manifest['checks'],ensure_ascii=False))


if __name__=='__main__':main()
