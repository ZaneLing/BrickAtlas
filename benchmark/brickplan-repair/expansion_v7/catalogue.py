"""Reviewable Chinese documentation generated from admitted cases and audits."""
from collections import Counter
from pathlib import Path
import csv
import hashlib
import json
import shutil
from expansion_v7 import ROOT,OUT
from expansion_v7.build import read,write

LABELS={'control':'正常','missing':'少件','wrong-color':'错色','extra-layer':'局部多层／重复加件',
 'offset':'偏移一格','rotated':'装反','wrong-part':'错零件／厚度','early-cover':'提前封口',
 'buried-repair':'拆上层返修','left-right-swap':'左右互换','repeat-omission':'重复组件漏做',
 'cascade-removal':'连带掉件'}


def label(f):
    return LABELS.get(f,'连续：'+' → '.join(LABELS.get(x,x) for x in f.removeprefix('multiple-').split('then-')))


def main():
    summary=read(OUT/'release-summary.json');index=read(OUT/'index.json')
    gallery=read(OUT/'gallery.json');visual=read(OUT/'visibility.json');validation=read(OUT/'validation.json')
    master=read(OUT/'global-splits.json');aliases={r['originalId']:r['samePhysicalTaskAs'] for r in master['adapterAliases']}
    all_conditions=[c for m in gallery for c in m['cases']]
    controls={m['id']:next(c['id'] for c in m['cases'] if c['mode']=='dynamic' and c['family']=='control') for m in gallery}
    write(OUT/'evaluation-sets.json',dict(
        unit='Execution condition; includes the 83 explicitly listed adapters of baseline tasks',
        machineVisibleRepairCandidates=[c['id'] for c in all_conditions if c['profile']['machineVisible'] is True],
        lowVisibilityDiagnostics=[c['id'] for c in all_conditions if c['profile']['machineVisible'] is False],
        normalControls=[c['id'] for c in all_conditions if c['family']=='control'],
        multipleIncidentConditions=[c['id'] for c in all_conditions if c['eventCount']>=2],
        newSourceHoldout=[c['id'] for m in gallery if m['track']=='M-new-source' for c in m['cases']],
        pairedNormalControls={c['id']:controls[m['id']] for m in gallery for c in m['cases'] if c['mode']=='dynamic' and c['eventCount']},
        commonPrefixPolicy='Use runtime.fork with identical decisions and aliases before enabling the incident schedule.',
        humanQualifiedForPerceptionClaims=[],
        machineVisibilityIsNotHumanQualification=True,
        actualPolicyRouteVisibilityMustBeRechecked=True))
    rows=[];table=['| 配置 | 部分 | 正常拼装／模块块数 | 静态／动态条件 | 2／3次干扰 |', '|---|---|---:|---:|---:|']
    for m in gallery:
        counts=Counter(c['mode'] for c in m['cases']);events=Counter(c['eventCount'] for c in m['cases'])
        table.append(f'| {m["title"]} (`{m["id"]}`) | {m["track"]} | {m["activeParts"]} | {counts["static"]} / {counts["dynamic"]} | {events[2]} / {events[3]} |')
        for c in m['cases']:
            rows.append(dict(id=c['id'],module=m['id'],track=m['track'],mode=c['mode'],family=c['family'],
                moduleParts=m['activeParts'],events=c['eventCount'],structuralGroup=c['profile']['structuralGroup'],
                machineVisible=c['profile']['machineVisible'],humanErrorIds=';'.join(c['humanErrorIds']),
                reusedBaseline=aliases.get(c['id'],'')))
    passed=visual['passed'];checked=visual['events']
    lines=['# 按六个方向扩充题库：本轮实际完成情况', '',
        '版本：`brickplan-expansion/7`，2026-10-23。原始 S／D／M 题库保留；这是可执行的扩充版本。没有调用付费模型，没有新增真人成绩。', '',
        '## 直接看', '',
        '- [物件、当前／目标、错误和说明书展示](index.html)（设计页含参考信息，不能发给被测模型）。',
        '- [逐模型、逐条件清单](MODEL-CASE-CATALOG.zh-CN.md)。',
        '- [30个来源、18种人类错误／问题、纳入与排除理由](human-error-research/README.zh-CN.md)。',
        '- [用户确认的错误范围与H18库存信息核查](HUMAN-ERROR-SCOPE.zh-CN.md)：H12、H14–H17不做，H18待定。',
        '- [全部分组 CSV](global-splits.csv)、[结构难度与待测字段](difficulty-all.json)。', '',
        '- [正常对照、低可见诊断、新来源与动态配对题单](evaluation-sets.json)；真人合格题单目前为空，不能把像素检查冒充人审。', '',
        '## 数量怎么数', '',
        f'- 保存了 **{summary["extensionConditions"]} 条扩展运行条件**：静态 {summary["extensionModes"]["static"]}、动态 {summary["extensionModes"]["dynamic"]}。',
        f'- 其中 **{summary["reusedBaselineTasks"]} 条**与旧题的来源、操作范围、状态和参考事件效果一致，只换了接口／候选条件，不重复算新题。',
        f'- 当前扩展新增 **{summary["newPhysicalTasks"]} 道任务**：静态 {summary["newPhysicalModes"]["static"]}、动态 {summary["newPhysicalModes"]["dynamic"]}。与当前范围内的原题 {summary["baselineCases"]} 道合计 **{summary["combinedPhysicalTasks"]} 道物理任务**。正常对照也计入题目数。',
        '- 此前原题5,260道，其中D的160道H12题现已排除；扩展也排除了22条H12条件。旧记录保留以便追溯，当前总数不含它们。',
        '- 同一物件会产生多道相关题，题数不等于独立物件数。跨版本别名在 `global-splits.json` 的 `adapterAliases` 中。', '',
        '## 六个方向分别做了什么', '',
        '| 方向 | 本轮结果 | 还需什么证据 |','|---|---|---|',
        '| 更长过程 | 5个新增长流程完整物件，正常需操作21–32块；博物馆扩大至16块，新客运车厢模块19块 | 还需真人和模型的实际完成表现。新长流程有按需说明书，不能与旧无说明书D直接归因为长度差异 |',
        '| 社区错误更丰富 | 按可行性加入装反、偏移、错零件／厚度、提前封口、拆上层返修、左右互换、重复组件漏做；H12连带掉件已取消 | 每个物件只收录合法、可撤回的错误，不强行让所有物件拥有所有类别 |',
        f'| 连续多次干扰 | {summary["multipleIncidentConditions"]} 条条件含多次事件，其中 {summary["threeIncidentConditions"]} 条是3次，其余是2次；不是把两处同时出错叫两次 | 需模型实测。未触发全部事件单列；后台第二次事件不等于模型自己制造第二个错误 |',
        '| 人类错误依据 | 核对30个来源、整理18种情况；当前只做H01–H11和H13；H12、H14–H17不做，H18待定 | 不是随机人群样本，不能报告真实发生频率；没有伪造真人轨迹 |',
        '| 难度更可靠 | 全部任务有结构描述；扩展另测实际RGB变化、遮挡比例、参考返修步数、正确盖板拆除数与事件次数；提供真实结果导入工具 | 结构分组仍为暂定；人类／模型成功率保持空值 |',
        '| 新来源与隔离 | 新增10013、10015、10016三个OMR来源；S、D、M和扩展共用一份来源分组，同来源跨集合为0 | 新来源保留作评测候选，不用于后续调提示词；公开来源不保证训练语料未见过 |', '',
        '## 所有扩展配置', '', *table, '',
        'D-long 是原创简化物件。M-new-source 是原始 LDraw 社区文件的局部任务，包含绿色客运车厢、罐车和敞篷货车；没有把整体套装都当成待拼部分。M-long 是同一来源的另一种操作范围，不另算独立物件。', '',
        '## 合法性、顺序和输入', '',
        f'- {validation["cases"]} 条条件通过独立物理重放。每次干扰及其逆向恢复都检查连接、碰撞、规定进出路径；没有把零件直接移动到答案位置。',
        '- 当前条件是此前已验证题目的保留子集；本次只排除H12，没有改变保留题的状态、几何或GT。',
        f'- {validation["alternativeOrderConditions"]} 条条件还用另一条合法顺序通过，包含连续事件；审查记录也保留尝试集合。它们是程序回归样本，不是随机人类／模型路线。',
        '- 触发只看实际装上的数量、物理可行性和两次事件间的操作数，不要求中间状态与说明书相同。模型每轮继续操作，不会被叫停回答检测题。',
        '- 三视图当前／TARGET同画布，后续有时间对照；零件全部展示，候选数量对所有零件相同；说明书按步骤查看。不同颜色／类型一定是不同实物，不能通过切换候选把一块变成另一块。',
        '- 同形同色零件可互换；最终几何与颜色正确即可。反向顺序、先左后右等合法拼法均允许，参考路线不称最短解。', '',
        '## 图片和难度', '',
        f'- 实际检查 **{checked} 次参考事件画面**，其中 {passed} 次达到固定三视图像素差异门槛，{checked-passed} 次另列低可见诊断。一个多事件条件有多个检查，不能把事件数当题数。',
        '- 像素差异只证明有图像变化，不证明人一定看得懂。完全遮挡、低对比和需要额外检查的情况不进入普通视觉漏检结论。',
        '- `evaluation-sets.json` 已把低可见条件单列，并为每条动态干扰条件指定正常对照；实际运行仍须满足相同前半程及全部事件触发条件。',
        '- 短／中／长按当前任务的目标或拼装规模分组，静态阶段同时记录模块全长和本题目标件数。L1–L3是结构组合标签，实际成功率尚未收集。',
        '- 返修步数来自一条已验证路线；正确盖板拆除数也来自该路线，不冒充所有合法方案所需的最少值。', '',
        '## 评分', '',
        '- 单次运行先报告最终完成、实际事件数和合法／被拒绝动作；主修复分数仍为空。',
        '- 只有相同前半程、正常分支完成、计划事件全部触发、两条分支服务完整，才由 `evaluate.pair` 计算主修复结果。',
        '- 403、429、超时、输出格式和物理拒绝分开。未触发、只触发一部分、没有正常配对，均不能写成漏检或主修复失败。',
        '- 新事件的可见性证据要随实际状态复查，不能把参考路线图片的认证直接套给模型的其他路线。', '',
        '## 执行与复现', '',
        '在项目根目录运行，使用现有Python环境；以下命令不调用付费模型：', '',
        '```bash',
        'PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m expansion_v7.preview_server',
        '# 本机设计展示：http://127.0.0.1:8797/',
        'PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m expansion_v7.run_episode --case "'+index['cases'][0]['id']+'"',
        '```', '',
        '模型接口从标准输入接收一条动作JSON，每步返回新观察和实际图片路径。真人无需填写JSON；当前HTML是查看题目的设计页，正式真人操作记录仍需通过操作界面独立收集。', '',
        '完整重建依次运行 `expansion_v7.intake`、`prepare`、`build`、`validate`、`audit_visuals`、`global_splits`、`difficulty_all`、`catalogue`。原MPD、作者、许可、依赖哈希和被拒绝候选保留。预备目录可重建，正式发布用压缩的证书和案例文件。', '',
        '实际结果导入：先运行 `expansion_v7.calibrate` 生成空CSV模板；收集真人／模型结果后使用 `--results 文件.csv`。不自动调用模型，不用程序参考成功率填真人／模型成绩，也不按测试成绩重新划分结构标签。', '',
        '## 下一步', '',
        '先用新版可读性小面板让真人独立操作，再做正常／干扰配对和固定中途恢复的模型试跑，测量新版实际费用。三种输入T／V／TV依旧是后续适配计划，本轮没有声称完成它们。旧版静态3,292题的全量视觉审核也仍需继续。',
        ]
    (OUT/'README.zh-CN.md').write_text('\n'.join(lines)+'\n')
    catalog=['# 扩充清单：物件、错误、每条条件与配图','','所有配图和路线为设计展示；没有伪造模型或真人结果。', '']
    for m in gallery:
        catalog += [f'## {m["title"]} · `{m["id"]}`','',
            f'部分：{m["track"]}；正常拼装／模块全长：{m["activeParts"]}块；来源：`{m["sourceSetId"]}`。','']
        cert=read(OUT/'models'/m['id']/'certificate.private.json.gz');source=cert['source']
        if source.get('url'):catalog += [f'原模型作者：{source.get("author", "见原始文件")}；[来源]({source["url"]})。','']
        families=sorted({c['family'] for c in m['cases'] if c['family']!='control' and not c['family'].startswith('multiple-')})
        multiple=sorted({c['family'] for c in m['cases'] if c['eventCount']>=2})
        catalog += ['本物件包含：'+'、'.join(label(f) for f in families)+'。','']
        if multiple:catalog += ['连续干扰：'+'；'.join(label(f) for f in multiple)+'。','']
        example=next((c for c in m['cases'] if c['family'] in ('wrong-part','early-cover','buried-repair')),m['cases'][0])
        catalog += [f'![当前与唯一目标：{m["title"]}]({example["images"]["isometric"]["file"]})','',
            '| 条件ID | 静态／动态 | 错误 | 事件数 | 来源类别 | 暂定结构组 | 图片 | 复用旧题 |',
            '|---|---|---|---:|---|---|---|---|']
        for c in m['cases']:
            catalog.append(f'| `{c["id"]}` | {c["mode"]} | {label(c["family"])} | {c["eventCount"]} | {", ".join(c["humanErrorIds"]) or "正常"} | {c["profile"]["structuralGroup"]} | [三维画面]({c["images"]["isometric"]["file"]}) | {aliases.get(c["id"], "新增")} |')
        catalog += ['']
    (OUT/'MODEL-CASE-CATALOG.zh-CN.md').write_text('\n'.join(catalog).rstrip()+'\n')
    with (OUT/'cases.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
    shutil.copyfile(Path(__file__).with_name('index.html'),OUT/'index.html')
    dependencies={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
        for p in Path(__file__).parent.glob('*') if p.is_file()}
    write(OUT/'code-manifest.json',dependencies)
    print('CATALOGUE',len(gallery),len(rows),flush=True)


if __name__=='__main__':main()
