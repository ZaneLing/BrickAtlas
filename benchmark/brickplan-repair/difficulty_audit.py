"""Measure current task complexity without pretending reference plans are optimal.

Produces organizer-side metadata only. Never adds difficulty/answer hints to
model observations and never changes the certified banks or their hashes.
"""
from collections import Counter
from pathlib import Path
import hashlib,json,statistics

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'deliverables/brickplan-difficulty-audit'
STATIC=ROOT/'deliverables/brickplan-static-plate5/cases.jsonl'
DYNAMIC=ROOT/'deliverables/brickplan-dynamic-v6/cases.private.json'

def write(name,value):
    (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

def stats(values):
    a=sorted(values)
    return dict(count=len(a),minimum=a[0],median=statistics.median(a),maximum=a[-1],histogram=dict(sorted(Counter(a).items())))

def size_band(n):
    return 'small-1-16' if n<=16 else 'medium-17-40' if n<=40 else 'large-41-100' if n<=100 else 'over-100'

def reference_band(n):
    return 'control-0' if n==0 else 'reference-1-2' if n<=2 else 'reference-3-5' if n<=5 else 'reference-6-9' if n<=9 else 'reference-10-plus'

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    static=[json.loads(line) for line in STATIC.read_text().splitlines()]
    dynamic=json.loads(DYNAMIC.read_text())['cases'];sr=[];dr=[];sm={};dm={}
    for c in static:
        n=sum(bool(k) for k in c['goal'].values());cost=len(c['oraclePlan'])
        if c['modelId'] in sm:assert sm[c['modelId']]==n
        sm[c['modelId']]=n
        assert c['referenceCost']==cost and c['referenceIsOptimal'] is False
        sr.append(dict(caseId=c['id'],publicId=c['publicId'],modelId=c['modelId'],targetParts=n,
                       modelSizeBand=size_band(n),existingDifficulty=c.get('difficulty'),
                       referenceRepairMoves=cost,referenceLengthBand=reference_band(cost),
                       referenceIsOptimal=False,migrationMethod=c['migrationMethod'],
                       calibratedDifficulty=None))
    for c in dynamic:
        n=c['targetParts'];dm[c['modelId']]=n;e=c.get('privateEvent')
        remaining=n-c['trigger'];cost=None
        if e:
            recovery=e['recoveryWitness']
            model=ROOT/'deliverables/brickplan-dynamic-v6/models'/c['modelId']/'evidence.json'
            plan=json.loads(model.read_text())['buildWitness']
            # Existing witnesses first restore the prefix, then finish its unchanged suffix.
            assert remaining>0 and recovery[-remaining:]==plan[c['trigger']:],c['id']
            cost=len(recovery)-remaining
            assert cost>0 and e.get('repairPrefixMoves',cost)==cost
        dr.append(dict(caseId=c['id'],modelId=c['modelId'],track=c['track'],targetParts=n,
                       modelSizeBand=size_band(n),kind=c['kind'],triggerProgress=c['trigger']/n,
                       referenceRepairMoves=cost,referenceLengthBand=reference_band(cost) if cost is not None else 'control-0',
                       remainingNormalBuildMoves=remaining if e else None,
                       referenceRecoveryMoves=len(e['recoveryWitness']) if e else None,
                       temporaryCorrectRemovals=e.get('temporaryCorrectRemovals') if e else None,
                       existingRepairTag=c.get('repairDifficulty'),referenceIsOptimal=False,
                       scheduledIncidents=int(e is not None),calibratedDifficulty=None))
    events=[c for c in dr if c['scheduledIncidents']];objects={m:n for m,n in dm.items() if m.startswith('obj-')}
    short=sum(c['referenceRepairMoves']<=2 for c in events)
    summary=dict(schema='brickplan-difficulty-audit/1',
        definitions=dict(modelSizeBand='Organizer planning bands only: <=16, 17-40, 41-100, >100 parts. Not calibrated task difficulty.',
                         referenceLengthBand='Length of a known feasible repair path; not a shortest-path lower bound or a human/model difficulty label.',
                         calibratedDifficulty='Unknown until independent human/model measurements; no overall easy/medium/hard claim.'),
        sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (STATIC,DYNAMIC)},
        static=dict(cases=len(sr),modelConfigurations=len(sm),difficultyField=dict(Counter(c['existingDifficulty'] for c in sr)),
                    targetPartsPerModel=stats(list(sm.values())),referenceRepairMoves=stats([c['referenceRepairMoves'] for c in sr]),
                    modelSizeBands=dict(Counter(size_band(n) for n in sm.values())),caseSizeBands=dict(Counter(c['modelSizeBand'] for c in sr)),
                    referenceLengthBands=dict(Counter(c['referenceLengthBand'] for c in sr)),optimalReferencePlans=0),
        dynamic=dict(cases=len(dr),models=len(dm),completeObjects=len(objects),interventions=len(events),
                     existingDifficultyFields=sum('difficulty' in c for c in dynamic),existingRepairTags=dict(Counter(c['existingRepairTag'] or 'missing' for c in dr)),
                     targetPartsPerModel=stats(list(dm.values())),completeObjectParts=stats(list(objects.values())),
                     modelSizeBands=dict(Counter(size_band(n) for n in dm.values())),
                     referenceRepairMoves=stats([c['referenceRepairMoves'] for c in events]),
                     oneOrTwoRepairMoves=short,oneOrTwoRepairFraction=short/len(events),
                     maxScheduledIncidents=1,calibratedDifficultyCases=0))
    write('summary.json',summary);write('static-profiles.private.json',dict(rows=sr));write('dynamic-profiles.private.json',dict(rows=dr))
    (OUT/'README.zh-CN.md').write_text(f'''# 静态、动态 Bench 的难度现状与补强办法

## 结论

**现在没有经过验证的简单／中等／困难分组。两套库的积木结构都偏小，真正复杂的完整物件不足。**

动态 v6 上一轮主要增加物件种类、错误种类和题量。1,872 道题来自 68 个结构，其中 42 个是完整物件；不能把 1,872 题理解成 1,872 个不同复杂物件，也不能据此说难度覆盖已经充分。

## 实际查到的数据

| 检查项 | 静态白底板版 | 动态 v6 |
|---|---|---|
| 题量 | {len(sr):,} | {len(dr):,} |
| 当前统一难度标签 | 全部“未标定” | 没有统一字段 |
| 结构数 | {len(sm)} 个模型配置 | {len(dm)} 个结构，其中 {len(objects)} 个完整物件 |
| 每个目标实际有多少块 | {min(sm.values())}–{max(sm.values())}；中位数 {statistics.median(sm.values()):g} | 全部 {min(dm.values())}–{max(dm.values())}；完整物件 {min(objects.values())}–{max(objects.values())}，中位数 {statistics.median(objects.values()):g} |
| 复杂度集中在哪里 | 150/160 个模型配置都是 11 块 | 完整物件全部不超过 15 块 |
| 已知参考修复步骤 | 0–32 步，中位数 5 | 干扰后的修复部分 1–8 步，中位数 2 |
| 中高规模物件 | 17 块及以上为 0 | 17 块及以上为 0 |

动态 {short}/{len(events)} 道干扰题（{100*short/len(events):.1f}%）有一两步的参考修复方案。这里**只算纠正干扰，不包含把剩下的正常零件继续拼完，也不包含看图和尝试错误的步骤**。

### 静态为什么以前有 D0–D5，现在却没有？

旧程序曾按修复动作数分：0 步为 D0，1–2 为 D1，3–5 为 D2，6–9 为 D3，10–15 为 D4，16 以上为 D5。

迁移到白底板规则后，3,292 题都只保留了已验证可行的修复方案，`referenceIsOptimal=false`，`expectedOptimum=null`，难度改为“未标定”。部分方案采用先拆后重拼。**一个参考方案有 22 步，不等于这道题最少必须做 22 步，更不等于真人一定觉得难。** 不能直接把旧等级重新贴上去。

### 动态已有的标签是什么？

`direct-repair` / `temporary-disassembly` 只说明参考修复过程是否拆了原本正确的上层件；`early` / `middle` / `late` 表示什么时候出事；12 类错误描述错在哪里。它们都不是统一难度等级。

当前每个回合最多一次外部事件，复合事件可以包含两处错误。“一次两处出错”不等于“一个长回合里先后发生两次事故”。

## 这次先补了什么

新增独立统计文件，逐题记录目标零件数、模型规模组、参考修复动作数；动态另外记录剩余正常拼装动作、触发进度、可用的临时拆件信息。

- [汇总数据](summary.json)
- `static-profiles.private.json`：3,292 题逐题记录。
- `dynamic-profiles.private.json`：1,872 题逐题记录。
- 生成程序：`benchmark/brickplan-repair/difficulty_audit.py`。

这些是出题者用的复杂度记录，不是新的正确答案或正式难度评级，不发送给被测模型。原题、几何证明和既有实验哈希不变。

## 下一步应怎么补强

先按下面的规模补物件，再按实际拼装和修复表现标难度。下列数量和区间是本项目建议的建设目标，不是其他论文规定的标准。

| 建设组 | 物件规模 | 应有的结构和错误 | 建议先补 |
|---|---|---|---|
| 小物件基础组 | 1–16 块 | 外露的一处错误，短回合；保留现有物件作为对照 | 现有库已经足够用于起步 |
| 中等规模组 | 17–40 块 | 多层和前后遮挡；需要先拆几块才能接近错件；两处相互影响的错误 | 至少 12 个新物件，覆盖 6 个来源家族 |
| 大物件复杂组 | 41–100 块 | 多个子结构组合；内部装错；拆装顺序互相制约；较长过程和分时发生的事故 | 至少 12 个新物件，覆盖 6 个来源家族 |

例子可以是带抽屉和隔层的柜子、带驾驶室和货厢的卡车、带转台和配重的起重机、双层房屋、传送带工作站。需要有实际连接关系和装配次序；不要用重复叠层、无关装饰或纯改颜色凑件数。

### 静态题怎么变难

1. 小模型和大模型都保留无错对照，以及外露的一处错误。
2. 加入被盖板遮住、拆错一处会影响另一处、多处错误共享拆卸通道的案例。
3. 分别记录：场景规模、多少处出错、是否可见、修复必须先拆什么、修复动作数。只有已证明的最短步数才叫最少动作数；其余写“已知可行方案”。
4. 遮挡题必须能通过允许的查看或合法拆装获得信息；完全没有线索且无法检查的题单独排除，不能当难题。

### 动态题怎么变难

1. 从空底板连续拼 20–100 块，让模型真正维持较长的过程和状态。
2. 同一物件分别在约 25%、50%、75% 进度施加干扰，并保留无干扰对照；不能都在第 3 步发生。
3. 除了单次事故，另建“先后两次／三次事故”组。第二次可以发生在修复期间，且每次都要验证有合法恢复路。
4. 增加早期装错、后来被其他零件盖住，直到后续装不上才暴露的问题；此时计发现延迟和恢复，不强求在不可见时立即发现。
5. 一直提供当前图和固定目标，保持一次只装／拆一块；不靠不给信息、限制看图或制造接口歧义增加难度。

## 最终怎么确定“难”

物件大不自动等于难，修复方案长也不自动等于难。先按物件规模、可见性、拆装依赖、错误数量和事故次数形成结构分组，再用独立真人和多个模型的成功率、耗时／决策数、误操作和恢复代价标定。

正式论文同时报告各分组和独立物件数量。当前应称为**小规模物件为主的静态修复与动态恢复题库，难度尚未标定**；不能宣称已经覆盖完整的简单到高难度范围。
''')
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
