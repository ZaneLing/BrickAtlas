"""Reproducible Chinese, illustrated per-model/per-case catalogue (design preview)."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'deliverables/brickplan-community-modules'
LABELS = {'control':'无错误对照', 'missing':'少一块', 'wrong-color':'颜色被换错', 'extra-layer':'多叠一块'}
COLORS = {'0':'黑色','1':'蓝色','2':'绿色','4':'红色','14':'黄色','15':'白色',
          '19':'米黄色','25':'橙色','71':'浅灰色','72':'深灰色','36':'透明红色',
          '47':'透明色','46':'透明黄色','57':'透明橙色','40':'透明烟灰色','34':'透明绿色',
          '272':'深蓝色','378':'浅沙绿色'}

def color(p):
    return COLORS.get(str(p['colorCode']), p['colorHex'])


def enrich(m, cert):
    normal = m['orderChecks']['referenceOrder']
    def desc(family):
        if family=='control':
            return '保持正常状态，不做后台改动。'
        change = m['perturbations'][family]
        if family=='extra-layer':
            n=normal.index(change['extraParent'])+1
            return f'在参考图 {n} 的零件上，多装一块红色 1×1 薄板（3024）。'
        actor=change['affected']
        n=normal.index(actor)+1
        p=cert['candidates'][change['before'][actor]]['part']
        if family=='missing':
            return f'拿走参考图 {n} 的{color(p)}零件（{p["partNumber"]}），保留刚刚新装的一块。'
        wrong=cert['candidates'][change['changes'][1]['candidate']]['part']
        return f'把参考图 {n} 的{color(p)}零件（{p["partNumber"]}）换成同形状的{color(wrong)}零件。'
    for c in m['cases']:
        c['description']=desc(c['family'])
    return m


def main():
    modules=json.loads((OUT/'gallery-data.js.json').read_text())
    for m in modules:
        cert=json.loads((OUT/m['id']/'certificate.private.json').read_text())
        enrich(m,cert)
    (OUT/'gallery-data.js.json').write_text(json.dumps(modules,ensure_ascii=False,indent=2)+'\n')
    (OUT/'data.js').write_text('window.MODULES='+json.dumps(modules,ensure_ascii=False)+';\n')
    case_count=sum(len(m['cases']) for m in modules)
    steps=sum(m['remaining'] for m in modules)
    lines=['# 12 个社区模型：模型、错误与 case 完整清单', '',
        '更新：2026-10-21。可以直接打开 [图文展示页](index.html)，或双击项目根目录的 `打开社区模块样例.command`。无需写文字、提交 JSON 或调用模型 API。', '',
        '## 先说明白：不要求照着唯一顺序拼', '',
        '**说明书只是一种参考拼法。中间状态不用和参考答案逐步相同。每次装、拆都真实合法，最后形状、位置、朝向和颜色正确，并声明完成，就算完成。**', '',
        '- 可以先装左边再装右边，也可以反过来，只要连接、碰撞和装入路径检查通过。',
        '- 相同形状、相同颜色的积木可以互换身份；不会因为编号与参考答案不同扣分。',
        '- 不能穿过其他积木、凭空漂浮、重复装同一块或直接复制整个目标状态。每次只装或拆一块。',
        '- 动态干扰看当时真的装了哪些零件。达到最低已装数量后，选择可拆、可换或可添加的位置；不会等待“恰好拼成参考图第几步”。找不到合法位置就继续等待，不能硬改出不可能状态。',
        '- 没发生干扰但最终拼对，仍然算完成；这条记录不用于计算“发生干扰后的修复成功率”。另报干扰触发率，防止把没有遇到错误的完成当成修复成绩。', '',
        '## 总量与怎么读这份清单', '',
        f'**{len(modules)} 个不同原模型 × 每个 8 个 case = {case_count} 个 case：48 个静态、48 个动态。** 正常补装一共 {steps} 步。每个模型补 5–12 块，不要求从零搭整个物件。', '',
        '每个模型各有：静态无错误、静态少一块、静态换错颜色、静态多一块；动态无干扰、动态少一块、动态换错颜色、动态多一块。共 3 类错误，重复到不同物件和结构上，不应写成 96 种错误。', '',
        '表中的“参考图编号”只用于定位哪块积木，**不是必须遵守的操作次序**。动态表列的是展示路线实际发生的错误；改用另一条拼法时，受影响零件可能不同，选择依据是实际状态。', '',
        '| # | 模型 / 模块 | 原场景零件 | 已搭好 | 本题补几块 | 静态 / 动态 |',
        '|---|---|---:|---:|---:|---|']
    for i,m in enumerate(modules,1):
        lines.append(f'| {i} | [{m["title"]}](#{m["id"]}) | {m["total"]} | {m["fixed"]} | {m["remaining"]} | 4 / 4 |')
    lines += ['', '原场景零件数按原 MPD 展开的实际实例计，包括人物和配景，不是包装盒上的零件数。每个模块另有“每块正常积木对应的一块异色备用件 + 1 块红色薄板”，所有条件都给同一份零件和候选位置，避免从零件表猜出错误类型。', '']
    for i,m in enumerate(modules,1):
        cert=json.loads((OUT/m['id']/'certificate.private.json').read_text())
        normal=m['orderChecks']['referenceOrder']
        link=f'index.html#model={m["id"]}'
        cp=m['staticStage']
        lines += [f'<a id="{m["id"]}"></a>', '', f'## {i}. {m["title"]}', '',
            f'**本题做什么：**{m["explanation"]}', '',
            f'- 模块：{m["module"]}。',
            f'- 开始已搭好 {m["fixed"]} 块；只补 {m["remaining"]} 块。零件盘共 {m["inventoryCount"]} 块，含备用件。',
            f'- 静态目标：参考图 {cp} 的正确状态；提供目标图，修到这幅图即可。',
            f'- 动态目标：整个剩余模块完成。安装数量达到 {cp} 块后尝试一次干扰；具体改哪块取决于实际拼法。',
            f'- 社区原模型：`{m["model"]}`；作者：{m["author"]}；[来源]({m["url"]})；[原 MPD]({m["id"]}/original.mpd)。',
            f'- [查看这个模型的说明与全部 case]({link}&mode=manual)。', '',
            '| 本题开始 | 最终完成 |', '|---|---|',
            f'| ![开始状态]({m["images"]["full-initial"]["file"]}) | ![完整目标]({m["images"]["full-final"]["file"]}) |', '',
            '### 剩余哪些零件', '',
            '下表数字对应说明图，不是评分要求的顺序。LDraw 名称保留原文方便查零件；直接看小图即可识别。', '',
            '| 参考图编号 | 零件小图 | 零件号 / 颜色 | 原文件中的零件名称 |', '|---|---|---|---|']
        for step,actor in zip(m['manual'],normal):
            p=cert['candidates'][actor+':goal']['part']
            lines.append(f'| {step["step"]} | <img src="{step["partImage"]}" width="95" alt="零件 {step["step"]}"> | {p["partNumber"]} / {color(p)} | {p["name"]} |')
        alt=' → '.join(str(normal.index(a)+1) for a in m['orderChecks']['alternateOrder'])
        lines += ['',f'**已实际跑通的另一种顺序：{alt}。** 这条路线的无干扰、少件、换色、多件都通过了逐次操作检查，最终正确。', '',
            '### 8 个 case', '', '| case 编号 | 类型 | 具体错误 / 对照 | 做到什么算完成 | 展示 |', '|---|---|---|---|---|']
        for mode in ('static','dynamic'):
            for family in LABELS:
                c=next(c for c in m['cases'] if c['mode']==mode and c['family']==family)
                target=f'修成参考图 {cp} 的目标状态' if mode=='static' else '最终补完全部模块'
                lines.append(f'| `{c["id"]}` | {"静态" if mode=="static" else "动态"}·{LABELS[family]} | {c["description"]} | {target} | [查看]({link}&mode={mode}&family={family}) |')
        lines += ['', '### 同一阶段的正确状态与三种错误', '',
            '以下配图来自展示路线。每种错误选画面变化最大的固定视角，并列出同视角的正确目标；展示页可切换三个方向。正式模型不会收到错误标签或这张对照表。', '',
            '| 错误 | 应有状态 | 实际错误状态 |', '|---|---|---|']
        audit=json.loads((OUT/'audit.json').read_text())
        result=next(r for r in audit['results'] if r['module']==m['id'])
        for family in ('missing','wrong-color','extra-layer'):
            vis=next(v for v in result['visibility'] if v['family']==family)
            view=max(vis['changedPixels'],key=vis['changedPixels'].get)
            lines.append(f'| {LABELS[family]} | ![正确目标]({m["images"]["checkpoint-"+view]["file"]}) | ![错误状态]({m["images"][family+"-"+view]["file"]}) |')
        lines += ['']
    lines += ['## 这次真正验证了什么', '',
        f'- {len(modules)} 个模型，{steps} 个正常安装步骤；{case_count} 个 case 的参考处理路线全部走通。',
        '- 每个模型另找到一种不同的合法顺序；共 48 次额外动态回放（12 × 无干扰/少件/换色/多件），都完成，36 次错误条件都真正触发并修复。',
        '- 其中 9 个模型的替代路线在达到干扰数量时，实际形状也不同于参考路线；相应 27 条错误回放仍然成功触发并修复。这专门检查了“不必先拼成参考中间状态”的要求。',
        '- 12 个模型都另外检查了交换同形同色零件的身份，最终仍算完成。',
        '- 每次安装、干扰和参考修复都检查真实连接、位置碰撞和直线装入/拆出路径；重复安装、悬空安装被拒绝。',
        '- 三种错误在每个模型至少一个固定视角有可见的像素变化。这是机器检查，不替代真人可理解性验证。',
        '- 完整场景保留原模型全部零件；不能可靠计算精细碰撞的背景件用外包盒保守阻挡，不能当成不存在。',
        '- 证据：[audit.json](audit.json)；各模块的 `order-checks.json`；原文件校验值与来源在各模块 `provenance.json`。', '',
        '## 当前范围与还没证明的事', '',
        '这是社区模型模块扩充组，未混入旧题库或论文成绩。12 个物件增加了外形和结构种类，但仍是短模块、一次干扰、三类错误，不能声称覆盖全部人类拼装错误或已经达到高难度。', '',
        '主体作为已经搭好的固定物件提供，允许夹具托住；没有模拟重力、手指、摩擦或卡扣力度。动作接口当前使用有限候选位置；不能据此声称测了任意连续位姿控制。', '',
        '**本次模型 API 调用 0 次，API 费用 0；新增真人评测 0 次。** 下一步是让真人确认说明/画面清楚，再比较模型无干扰与有干扰的表现。', '',
        '说明图由本项目按原模型位置生成并检查，不是 LEGO 官方说明书。社区原文件、作者和许可声明均保留，未把原模型修改成自造外形。', '',
        '接口详细说明：[INPUT-OUTPUT.zh-CN.md](INPUT-OUTPUT.zh-CN.md)。本目录 HTML 和此清单是讲解页，包含答案；测试时只使用 `run_episode.py` 返回的公开观察。', '']
    (OUT/'MODEL-CASE-CATALOG.zh-CN.md').write_text('\n'.join(lines))
    overview='\n'.join(lines[lines.index('| # | 模型 / 模块 | 原场景零件 | 已搭好 | 本题补几块 | 静态 / 动态 |'):][:14]).replace('](#','](MODEL-CASE-CATALOG.zh-CN.md#')
    (OUT/'README.zh-CN.md').write_text('''# LDraw 社区模型：只补最后一个模块

## 直接看

- [打开图文展示页](index.html)，或双击项目根目录 `打开社区模块样例.command`。
- [完整 Markdown 清单：12 个模型、96 个 case、每个错误与配图](MODEL-CASE-CATALOG.zh-CN.md)。
- [模型接口：输入、输出、动态触发与评分](INPUT-OUTPUT.zh-CN.md)。

**顺序不限。** 说明书是一种参考拼法，每次操作真实合法、最终状态正确并结束就算完成。不会用中间状态是否匹配参考答案判断对错。相同形状与颜色的零件可以互换。

## 模型一览

'''+overview+'''

每个模型 4 个静态 + 4 个动态 case，包括无错误对照、少件、颜色换错和多叠一块。正常补装合计 99 步。每一步只装或拆一块，不把整个模块算作一块。

动态干扰根据当时实际状态发生：已安装的本模块零件达到最低数量后，找可行的旧零件或连接点改动；找不到就等待。不依赖说明书的特定顺序。未触发干扰但拼对仍算完成，单独报告触发率及触发后的修复成功率。

## 已验证与范围

96 条参考路线、48 条不同顺序的动态路线均跑通，后者的 36 条错误路线均真正触发并修复。安装、拆除和干扰经过连接、碰撞、直线路径检查。全部原场景保留，背景不能精细检查的零件采用外包盒保守阻挡。

这是短模块、一次干扰、三类错误的扩充组；还没有新增真人成绩或模型成绩。图片差异可见不等于真人一定看得懂。预装主体作为固定物件，不证明整套从空桌面可拼，也不模拟重力、手指或卡扣力度。

原 MPD、作者、链接、许可与文件校验值均保留。说明图是本项目按原位置生成的可行参考拼法，不是 LEGO 官方说明书。API 调用和费用均为 0，未混入旧题库的实验统计。

## 重新生成与本机预览

```bash
benchmark/.runtime/mlx-env/bin/python benchmark/brickplan-repair/community_modules/build.py
benchmark/.runtime/mlx-env/bin/python benchmark/brickplan-repair/community_modules/validate.py
python3 benchmark/brickplan-repair/community_modules/preview_server.py
```

预览地址：<http://127.0.0.1:8768>。服务只提供公开讲解资源，不提供私有证书或运行记录。

HTML 与 Markdown 是包含答案的设计展示，不应发给测试模型。正式输入使用接口返回的匿名零件、图像与动作结果。

## 2026-10-23 输入与开发试跑更新

构建发布时 API 为 0；同日已有小规模 [开发试跑](../brickplan-budget-pilot-2026-10-23/README.zh-CN.md)，不是正式模型主表。旧输入和回答保留原样。

默认现在只有本题 TARGET，当前与目标放在同一张图里；说明书按步骤查看，不再每轮重发整本。全部零件合并成每页十二块，首轮 4–6 张、后续 7–9 张；看一步说明书加一张。未来说明必须明确请求，不会替换本题目标。单条动态完成不进入主修复成功率。[看修复说明和图示](../brickplan-interface-repair-2026-10-23/README.zh-CN.md)。
''')
    print('CATALOGUE',len(modules),case_count,flush=True)


if __name__=='__main__':
    main()
