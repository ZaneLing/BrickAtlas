"""Human-readable, source-backed organization; computed counts never hand-filled."""
from collections import Counter,defaultdict
import json
from bench_design import ROOT,OUT
from expansion_v7.build import read,write

TRACK_NAMES={'static-structure-diagnostic':'静态局部结构诊断','whole-object-static':'完整物件的阶段静态修复',
 'named-module-static':'大物件收尾的阶段静态修复','whole-object-dynamic':'完整物件动态拼装',
 'named-module-dynamic':'大物件收尾动态拼装','dynamic-structure-diagnostic':'历史动态机制诊断（单列）',
 'archived-crop-dynamic':'历史任意裁切动态（不进主组）'}


def main():
    summary=read(OUT/'summary.json');audit=read(OUT/'physical-audit.json')
    rows=[json.loads(l) for l in (OUT/'questions.jsonl').read_text().splitlines()]
    unique=[r for r in rows if not r['isAlias']];main=[r for r in unique if r['mainTaskCandidate']]
    dynamic=[r for r in main if r['mode']=='dynamic'];modelids={r['model'] for r in dynamic}
    counts=Counter(r['taskType'] for r in main)
    doc=['# 我们的 Bench：题库组成、错误类别、级别和题型', '',
      '**先看这份总览；具体怎么算分看 [评估方案](EVALUATION.zh-CN.md)。**', '',
      '## 先说结论', '',
      f"- 这轮对 **{audit['executionConditionsPassed']:,} 个保留运行条件**重新执行参考路线，全部通过。包括要复用的正常对照和历史接口条件，不把它们全部算成新题。",
      f"- 统一目录有 **{summary['rawRetainedConditions']:,} 条记录**：以前的5,793条，加上完整小物件46条。发现119条同任务重复记录后，保留 **{summary['distinctTaskRecords']:,} 条去重题目**。",
      '- 去重是同一来源、物件配置和任务规则下的物理等价检查；不是声称把所有不同来源的相似设计都识别成了同一物件。',
      f"- 主任务候选 **{len(main):,} 题**：静态{sum(r['mode']=='static' for r in main):,}、动态{len(dynamic):,}。另有268题历史动态结构／裁切诊断，单列，不拿来代表完整物件拼装。",
      f"- 动态主组覆盖 **{len(modelids)} 种操作配置**：50个完整物件配置、13个明确收尾配置。不是只有这次的小船和两架直升机。",
      '- 这些是程序可行性证据。**不等于全部题图已经让真人逐题看懂，也没有产生新的模型实验成绩。** 本轮付费API为0。',
      '', '## 1. 题库到底包含什么', '', '| 部分 | 去重题数 | 为什么保留 |', '|---|---:|---|']
    why={'static-structure-diagnostic':'只测局部结构修复，不要求局部像完整物件。',
      'whole-object-static':'同一个完整物件的某阶段出错，修到该阶段目标。',
      'named-module-static':'主体已经装好，检查屋顶、尾翼等部分的阶段状态。',
      'whole-object-dynamic':'从空白底板完整拼，可能有中途事故。',
      'named-module-dynamic':'从已装主体开始，补完有明确用途的部分。',
      'dynamic-structure-diagnostic':'保留机制与接口研究价值；不放进物件动态主表。',
      'archived-crop-dynamic':'旧记录用于追溯；这类碎片不再用于主组动态结论。'}
    for track in TRACK_NAMES:doc.append(f"| {TRACK_NAMES[track]} | {summary['perTrack'][track]} | {why[track]} |")
    doc+=['', '以前的完整家具、车辆、机器、长过程物件和社区模块都保留。[逐物件清单：63种动态配置与配图](MODEL-LIST.zh-CN.md)。',
      '', '**来源也分清楚：** 50个完整物件配置里，42个是原有程序设计物件、5个是较长的程序设计物件、3个是完整LDraw小物件。13个收尾配置来自12个社区源物件，其中一个有扩大操作范围版本。63种配置不等于63个社区来源。',
      '', '### 你认可的几个小例子', '', '| 小船，12块 | 海上直升机，13块 | 迷你直升机，9块 |', '|---|---|---|',
      '| ![小船](../brickplan-recognizable-models/public/assets/whole-4018/full.png) | ![海上直升机](../brickplan-recognizable-models/public/assets/whole-4017/full.png) | ![迷你直升机](../brickplan-recognizable-models/public/assets/whole-4037/full.png) |',
      '', '小物件保留下载文件的全部零件，从空白底板开始。大物件给已经装好的主体，只补屋顶、驾驶舱、尾翼等明确部分。没有删掉轮子或旋翼来冒充完整模型。',
      '', '## 2. 错误类别：分三层，不能混着数', '',
      '### 第一层：实际哪里错了（7个基本标签）', '',
      '| 编号 | 类别 | 人话例子 |', '|---|---|---|',
      '| E01 | 少件 | 该装的一块没装，或中途被拿走。 |',
      '| E02 | 多件 | 多装了一块，或局部重复铺了一层。当前不是整套模型整层重复。 |',
      '| E03 | 错色 | 位置和形状看起来对，但颜色不对。 |',
      '| E04 | 错零件 | 拿错类型、尺寸、长度或厚度。 |',
      '| E05 | 位置偏移 | 偏了一格、放错高度。高度错不再不加区分地叫一种新错误。 |',
      '| E06 | 方向错误 | 旋转成了不等价的方向；对称等价不算错。 |',
      '| E07 | 位置关系互换 | 两侧或两件放反位置；不是把积木镜像变形。 |',
      '', '### 第二层：修复时多了什么麻烦', '',
      '| 标签 | 含义 | 与第一层的关系 |', '|---|---|---|',
      '| P01 提前封口 | 太早盖上正确的盖件，挡住后续安装通路。 | 动态才真正测试继续施工；静态对应题主要检查当前阶段不该提前装。 |',
      '| P02 内部返修 | 错件被上层遮住，需要暂时拆开再恢复。 | 往往同时有E03等基本错误，不额外虚增一种颜色错误。 |',
      '| 重复次数漏做 | 应重复装两份，却少做一份。 | 最终仍属于少件，是人类原因／场景标签。 |',
      '| 同时多错 | 一个状态或同一次事故造成多处错误。 | 与“前后两次事故”不同，可有多个基本标签。 |',
      '', '### 第三层：过程怎么变长', '',
      '- T0：没有外部事故。静态题也是T0，因为错误在开局就存在。',
      '- T1：中途一次事故；这一次也可能同时造成多处错误。',
      '- T2：前后两次事故。',
      '- T3：前后三次事故。',
      '', '**人类错误的来源标签另保留H01–H11、H13，共12类。** 它们解释题目受哪种真实情况启发，不代表12个互斥的物理错误，也不是采集了真人轨迹。H12、H14–H17不做；H18待定。目前零件目录不是实时剩件清单。',
      '', '### 各类题目前有多少', '', '| 类别／标签 | 静态主候选 | 完整物件动态 | 收尾动态 |', '|---|---:|---:|---:|']
    for code,name in [('E01','少件'),('E02','多件'),('E03','错色'),('E04','错零件'),('E05','位置偏移'),('E06','方向错误'),('E07','位置互换'),('P01','提前封口'),('P02','内部返修')]:
        nums=[]
        for scope in ('static','whole-object-dynamic','named-module-dynamic'):
            rr=[r for r in main if (r['mode']=='static' if scope=='static' else r['track']==scope)]
            nums.append(sum(code in r['errorCodes'] or code in r['processTags'] for r in rr))
        doc.append('| '+name+' | '+' | '.join(map(str,nums))+' |')
    doc+=['', '表中为多标签统计，不能把各行直接相加。连续事故可以包含错色和少件；内部错色也同时属于E03与P02。历史复合事故仍保留MIX条件标签，不能把它当第八个基本错误。',
      '', '## 3. 难度与级别：不再只看有多少块', '',
      '先给每题可核对的结构标签，再用真人和模型结果检验它是否真的难。旧L1–L3保留作历史字段，不混用为新的实测等级。',
      '', '| 维度 | 分级规则 | 它告诉我们什么 |', '|---|---|---|',
      '| B：规模／过程长度 | B1≤12块；B2为13–24块；B3≥25块 | 动态看本次完整安装量；静态只看当前阶段目标，不能拿未来零件或整栋楼的件数抬高等级。 |',
      '| R：参考返工量 | R0正常对照；R1无拆正确盖件且参考修复≤2步；R2其余普通返修／多错／3–6步；R3参考路线拆正确件或≥7步 | 这是可行参考路线的负担，不保证最少必须拆这么多。 |',
      '| T：事故次数 | T0／T1／T2／T3 | 是否需要修好后继续应对下一次变化。 |',
      '| V：可见性 | 机器可见、低可见、动作被抵消、新画布待检查、真人待检查 | 单独报告。完全看不见不能简单当作“更难的视觉题”。 |',
      '', '### 给下一阶段排题用的三个等级', '',
      '| 等级 | 明确规则 | 主候选题数 |', '|---|---|---:|']
    grade=Counter(r['planningLevel'] for r in main)
    doc += [f"| G1 基础结构 | 没有下列升级条件。 | {grade['G1']} |",
      f"| G2 进阶结构 | B2、R2／R3或两次事故，且不满足G3。 | {grade['G2']} |",
      f"| G3 挑战结构 | B3，或三次事故，或两次以上事故叠加R3。 | {grade['G3']} |", '',
      '**G不是已经验证的“简单／中等／困难”标签。** 当前G3只有52题，且主要来自长过程的程序物件；社区长模块与实测难度仍偏少。',
      '', '## 4. 每种题输入什么、输出什么、GT是什么', '',
      '| 题型 | 输入／开始状态 | 输出 | GT／结束条件 | 主候选题数 |', '|---|---|---|---|---:|',
      f"| S0 正常验收 | 当前已达到阶段目标；有备用件。 | 查看或finish，不应随便装拆。 | 最后仍正确；另记是否误修。 | {counts['S0']} |",
      f"| S1 静态修复 | 当前错误状态＋本阶段唯一目标＋零件目录。 | 每次装一块、拆一块、查看或结束。 | 达到该阶段几何、颜色和类型。 | {counts['S1']} |",
      f"| D0 正常拼装 | 空底板，或大物件已装主体；最终目标＋按需说明。 | 持续一步步操作，中间可看状态。 | 完整物件／指定部分完成。 | {counts['D0']} |",
      f"| D1 一次干扰 | 与D0相同，开局不告诉会发生什么事故。 | 自主观察、修复、继续拼完。 | 最终目标正确；修复评分另要求配对正常分支成功和事故真正触发。 | {counts['D1']} |",
      f"| D2 连续干扰 | 与D0相同；不提示事故次数和时间。 | 一直拼，遇到问题自行处理。 | 最终目标正确，并分别核对实际发生的事件。 | {counts['D2']} |",
      '| C 指定中途开始 | 系统已装到中途，并给错误状态。 | 修好并完成剩下部分。 | 独立统计，不算模型自己从零拼到了这里。 | 待补题单 |',
      '', '说明书随时可以查看，但静态题的未来步骤不是验收目标。模型输入不能含错误类别、后台事故、GT动作、隐藏状态或哪一个候选是正确答案。',
      '', '新主入口统一为一个直接动作对象，保持一次只操作一块。位置编号是主实验；自由坐标另设定位实验。真人界面仍可点选，不要求真人写JSON或自由文字。',
      '', '## 5. 看具体错误图：输入、输出与GT', '',
      '下面是实际几何渲染，不是示意画。**每张左边是当前，右边是该阶段唯一目标。** 小直升机有9块，但这些静态例子可能只验收到第5步，不要求继续拼成完整9块。输出只是可行参考的第一步，完整路线可以不同。']
    exp_names={'E01':'少件','E02':'多件','E03':'错色','E04':'错零件','E05':'位置偏移','E06':'方向错误','E07':'位置互换','P01':'提前封口的阶段对照','P02':'内部返修','OK':'正常验收'}
    for e in read(OUT/'examples.json'):
        doc += ['',f"### {e['code']} · {exp_names[e['code']]}：{e['title']}", '',
          f"- 当前验收到第 **{e['targetStage']} / {e['totalParts']}** 个安装步骤；右图是GT。",
          '- 输入还包括匿名零件目录、可查看的位置选项和该轨支持的说明步骤。',
          '- 一条可行的首步输出：`'+json.dumps(e['referenceActions'][0],ensure_ascii=False)+'`。',
          f"- 题目ID：`{e['id']}`；参考动作不是模型成绩。", '',f"![{exp_names[e['code']]}的当前状态与唯一阶段目标]({e['image']})"]
    doc+=['', '## 6. 这次已经解决／核对的问题', '',
      '| 问题 | 处理结果 |', '|---|---|',
      '| 同形同色换编号算新题 | 找出27条静态物理重复，映射到同一规范任务。 |',
      '| 不同阶段的正常对照重复计题 | 找出92条重复对照。运行时仍可用于配对，统计时不当新题。 |',
      '| 旧接口重复包装同一题 | 既有83条跨接口别名继续单列。 |',
      '| 随机局部结构混进物件动态主组 | 44题裁切动态、224题机制动态放诊断组；新主运行入口默认拒绝混入。 |',
      '| repair_state被当成新错误类别 | 对原静态题按物理等价匹配后核对实际候选类型；267条替换记录得到标准错误标签，保留原标签作追溯。 |',
      '| 静态题误提示从空底板重搭 | 修正E7完整物件静态题，明确从当前场景修到指定阶段。 |',
      '| 多次事故只发生一部分也算完整修复 | 评分资格加上“全部计划事件真正发生”。 |',
      '| 事件已发生却在汇总变成未触发 | 修正eventApplied／eventTriggered字段兼容。 |',
      '| 大物件只看到孤立局部 | 新统一入口给收尾模块保留完整主体背景。画布变化后，旧局部图的可见性结论不直接冒用。 |',
      '| 新的3个完整物件是否有图像差异 | 46条条件已核对：36条错误参考场景有机器可见变化，10条正常对照；真人逐题可读性仍待确认。 |',
      f"| 参考路线是否实际可执行 | 本轮{audit['executionConditionsPassed']:,}个保留条件重新检查，0失败；原始题目状态与GT文件未改写。 |",
      '| 展示过的物件还声称是新来源测试 | 已知45个展示来源整体归到开发材料，同来源不跨分组。 |',
      '', '## 7. 还缺什么，下一阶段按什么顺序补', '',
      '| 优先级 | 具体做什么 | 完成标准 |', '|---|---|---|',
      '| 先做 | 对新完整物件、收尾题做逐题真人可读性确认。 | 人能说清楚当前状态、唯一目标、剩哪部分；无需写自由文字，可点选。不要用本轮展示认可代替所有题的操作验证。 |',
      '| 先做 | 补指定中途开始的C组。 | 从同一已验证中途状态比较模型修复能力，输入明确系统预装；不需要模型先会完整拼。 |',
      '| 先做 | 核对新完整背景下的全部收尾题可见性。 | 按实际输入尺寸、视角、查询能力检查；遮挡与低对比单列。 |',
      '| 然后 | 补新来源的完整小物件和明确社区收尾部分。 | 在调提示前先定评测来源；当前社区收尾的开发／演示例子不能证明新来源泛化。 |',
      '| 然后 | 补长社区模块和G3题。 | 优先15–30块、有实际用途的部分；不用任意截块或大背景来假装困难。 |',
      '| 然后 | 平衡错误、等级和物件来源。 | 小规模主评测可先每轨60–120题、至少10个来源组；每个有效错误／等级单元尽量有≥3个来源。做不到就留空并报原因，不硬凑满所有组合。 |',
      '| 最后 | 独立检测、文字状态、坐标和活动关节实验。 | 每一项先补清楚输入与判分，再做对照；活动件的固定姿态不等于模拟铰链旋转、卡扣弹性或真实装配力。 |',
      '', '### 已经明确的缺口，按这个补', '',
      '| 缺口 | 目前 | 下一批的具体目标（尚未完成） |','|---|---|---|',
      '| 完整社区小物件种类少 | 3个，且有两架直升机 | 扩到至少10个，优先小车、船、家具、小机器等不同外形；全件保留并通过正常拼装。 |',
      '| 收尾模块的位置互换 | 当前动态主组为0题 | 找至少3个有明确左右部位的来源，生成合法可修复的互换题。 |',
      '| 长社区模块／挑战组偏少 | G3主候选52题，主要来自程序物件 | 增加至少5个有用途的15–30块社区模块；允许其他合法顺序，不靠重复换色凑数量。 |',
      '| 新社区来源测试 | 现有收尾来源都已用于开发／展示 | 另选至少5个未用于调提示的来源，与开发来源分组保存，仍需真人可读性审查。 |',
      '| 中途开始独立修复 | C组独立题单尚未生成 | 从已验证场景导出固定中途状态，在相同初始错误和目标上公平比较模型。 |',
      '', '**数量已经不是当前最主要的问题。** 更需要补的是社区物件的来源多样性、长模块、可读性确认和可以独立测修复的中途题。已有A/B/C旧版审查保留；画面与规则变化后，不能自动把它们当作新版所有题的真人操作验证。',
      '', '## 8. 具体文件与本机入口', '',
      '- [逐题CSV](questions.csv)：可以直接筛选题型、物件、错误、B/R/T、来源分组和主组资格。',
      '- [逐题JSONL](questions.jsonl)：包含原ID、规范ID、是否重复、原历史字段和新分类。',
      '- [63种动态配置的配图列表](MODEL-LIST.zh-CN.md)。',
      '- [参考路线重放结果](physical-audit.json) · [分类核查](classification-audit.json) · [重复关系](duplicates.json) · [新物件图像检查](new-object-visibility.json)。',
      '- [评估指标、分母与实验设计](EVALUATION.zh-CN.md)。',
      '', '本机统一入口示例（只启动环境，不会调用API）：', '', '```bash',
      'PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m bench_design.run_episode --id O:objects::whole-4037::dynamic::control::t0',
      '```', '', '它逐行接收一个动作对象。已有静态、完整物件动态和收尾模块都使用同一层动作输出；S／D不再要求额外包一层action。旧展示页及旧结果保留历史版本，新旧成绩分开。']
    (OUT/'README.zh-CN.md').write_text('\n'.join(doc)+'\n')
    gallery={m['id']:m for m in read(ROOT/'deliverables/brickplan-expansion-v7/gallery.json')}
    models=['# 动态主组：63种操作配置','','同一物件的短、长收尾范围可能是两个配置，不冒充两个原始套装。题数为去重记录；正常、单次事故、连续事故分别列出。所有图片都是原有几何成品参考，不是模型实验结果。','','| 成品参考 | 物件／本次做什么 | 来源组 | 静态 | 正常动态 | 一次事故 | 连续事故 | G3 |','|---|---|---|---:|---:|---:|---:|---:|']
    whole={r['model'] for r in main if r['track']=='whole-object-dynamic'}
    for mid in sorted(modelids,key=lambda m:(m not in whole,m)):
        rr=[r for r in main if r['model']==mid];first=rr[0]
        if mid.startswith('whole-') or (ROOT/'deliverables/brickplan-recognizable-models/public/assets'/mid/'full.png').exists():image='../brickplan-recognizable-models/public/assets/'+mid+'/full.png'
        elif mid.startswith('obj-'):image='../brickplan-dynamic-v6/models/'+mid+'/target.png'
        else:image='../brickplan-expansion-v7/'+gallery[mid]['fullImage']['file']
        numbers=[sum(r['mode']=='static' for r in rr),sum(r['taskType']=='D0' for r in rr),sum(r['taskType']=='D1' for r in rr),sum(r['taskType']=='D2' for r in rr),sum(r['planningLevel']=='G3' for r in rr)]
        models.append(f'| <img src="{image}" width="140" alt="{first["title"]}"> | {first["title"]}<br>`{mid}` | `{first["source"]}` | '+' | '.join(map(str,numbers))+' |')
    models += ['', '静态局部结构的所有物件配置另在 [逐题CSV](questions.csv) 中，不能把它们作为完整物件成品展示。']
    (OUT/'MODEL-LIST.zh-CN.md').write_text('\n'.join(models)+'\n')
    write(OUT/'coverage.json',dict(mainTaskTypeCounts=dict(counts),mainPlanningLevels=dict(grade),
        dynamicConfigurations=len(modelids),wholeObjectConfigurations=len(whole),namedModuleConfigurations=len(modelids-whole),
        coverage=[dict(track=t,count=sum(r['track']==t for r in unique)) for t in TRACK_NAMES],
        empiricalDifficultyValidated=False,paidApiCalls=0))
    print('DOCS',len(modelids),'configurations',len(main),'main candidates',flush=True)


if __name__=='__main__':main()
