"""Readable source inventory and illustrated, machine-checked question examples."""
from collections import Counter
import hashlib,json
from pathlib import Path
from dynamic_arena import ROOT,OUT
from expansion_v7.build import read,write
from expansion_v7.runtime import runtime
from community_modules.core import render_certificate
from dynamic_arena.plate_render import ArenaVision
from dynamic_v5.vision import DynamicVisionRenderer

CN={'animal':'动物','plant-food':'植物、食物','house-building':'房屋、建筑','furniture-object':'家具、日常物件','robot-machine':'机器人、机械','railway':'铁路','boat':'船艇','aircraft':'飞机','spacecraft':'航天器','road-vehicle':'道路车辆','other':'其他'}
F={'missing':'少装／被拆走','wrong-color':'颜色被换错','offset':'位置偏移','rotated':'方向装反','extra-layer':'多装一层','wrong-part':'零件换错','control':'正常拼装'}
NEW_MODULES={'flag-top-1869','helicopter-rotor-7609','house-roof-7796','christmas-treetop-561412','turkey-tail-40011'}

def main():
    lib=read(OUT/'source-library.json');cur=read(OUT/'source-curation.json');base=read(OUT/'source-library-before-curation.json');old={r['setNumber'] for r in base['models']};active={r['setNumber'] for r in lib['models']}
    removed=[r for r in cur['withdrawn'] if r['setNumber'] in old];new=[r for r in lib['models'] if r['setNumber'] not in old]
    qn=read(ROOT/'deliverables/brickplan-quality-round/source-expansion/index.json');a4=read(OUT/'new-objects/index.json')
    objects=[]
    for m in a4['models']:
        if m['setNumber'] in active:objects.append((m,OUT/'new-objects'/m['id'],'完整物件',m['setNumber'] not in old))
    for m in qn['models']:
        if m['id'] in NEW_MODULES and m['sourceSetId'] in active:objects.append((m,ROOT/'deliverables/brickplan-quality-round/source-expansion/models'/m['id'],'指定模块',True))
    new_cases=sum(len(read(folder/'cases.private.json.gz')) for m,folder,kind,isnew in objects if isnew)
    report=['# 无小人模型整理与新题说明','',f'更新：2026-10-29。原库 400 个；其中 {len(removed)} 个整件移出；新增保留 {len(new)} 个；当前来源库 **{len(active)} 个**。', '', '**没有为了凑回 400 个而保留人物或把同一个模型换色重复计数。来源数量不是合格动态题数量。**','',f'本次新增可运行物件／模块 **{sum(isnew for _,_,_,isnew in objects)} 个，{new_cases} 道题**。原有铁路道口和芒果也补齐了静态／动态配对条件。每个物件最多 5 道。','', '所有新题通过程序合法动作回放和错误可见性检查；尚未经过这轮真人确认，也没有调用付费 API。','', '## 怎么筛选','', '- 检查完整零件清单、零件名称、别名及组合件；人头、躯干、手脚、Friends 人偶、微型人形雕像都排除。座椅、杯子等配件不会仅因名字带 Minifig 而误删。','- 带人物的整件来源退出，同时阻止其旧模块进入当前 Arena；原文件和历史实验记录保留。','- 新增优先考虑动物、植物、建筑和机械；重复角色、相似造型、多个对象混在一起或没有可核对预览的候选先留在候选记录中。','- 最终结构和合法性决定成功，GT 动作只是一个可行例子，不要求模型按唯一顺序拼。','', '## 当前来源类别','', '|类别|来源数|','|---|---:|']
    report += [f'|{CN.get(k,k)}|{v}|' for k,v in Counter(r['objectCategory'] for r in lib['models']).items()]
    report += ['', '## 本次补充的模型','', '|原模型预览|来源|类别／零件数|当前用途|','|---|---|---|---|']
    for r in new:
        image=f"![{r['title']}](../../{r['thumbnail']})" if r.get('thumbnail') else '暂无预览，待补'
        uses=[]
        for m,folder,kind,_ in objects:
            if m.get('setNumber',m.get('sourceSetId'))==r['setNumber']:uses.append(kind+'：'+m['title'])
        report.append(f"|{image}|[{r['setNumber']} {r['title']}]({r['sourceUrl']})|{CN.get(r['objectCategory'])} / {r['parts']}|{'；'.join(uses) or '来源候选；尚不算合格题目'}|")
    report += ['', '## 题目如何输入、输出和判分','', '|题型|给模型什么|模型输出什么|GT 与判分|','|---|---|---|---|','|正常拼装|唯一目标、库存、动作接口；通过 observe 请求当前图或目标图，通过 inspect 看零件、位置、说明书|observe / inspect / attach / detach / finish 及参数|无干扰完成全部目标；不限定合法顺序|','|静态修复|出错的当前状态、当前阶段的唯一验收目标、可用零件与操作接口|拆装动作序列或完成声明|恢复当前阶段目标；不强迫提前完成后续步骤|','|动态修复|从白色凸点底板或明确预装模块开始，模型持续接管；中途发生隐藏变化|模型主动观察、拆装、继续完成|实际触发后是否恢复并继续成功；未触发单列，接口错误单列|','', '下面的错误起点、GT 和触发详情用于人工审查，不会提前透露给模型。','']
    rendered=OUT/'curation-images';rendered.mkdir(exist_ok=True);allrows=[]
    for m,folder,kind,isnew in objects:
        cert=read(folder/'certificate.private.json.gz');cases=read(folder/'cases.private.json.gz');rt=runtime(cert)
        renderer=(ArenaVision if hasattr(rt,'baseplate') else DynamicVisionRenderer)(render_certificate(cert),rt)
        n=m.get('parts',m.get('activeParts'));difficulty='短流程' if n<=6 else '中等流程' if n<=12 else '较长流程'
        report += [f'## {m["title"]}', '', f'{kind}；操作 {n} 块；**{difficulty}**。这只是步骤规模分组，还不是经过真人表现验证的难度结论。','', '|Case ID|类型|错误|GT 动作数|','|---|---|---|---:|']
        for c in cases:
            mode='静态修复' if c['mode']=='static' else '正常拼装' if not c['events'] else '动态修复'
            report.append(f"|`{c['id']}`|{mode}|{F.get(c['family'],c['family'])}|{len(c['referenceActions'])}|")
            allrows.append(dict(caseId=c['id'],model=m['id'],newSource=isnew,mode=c['mode'],family=c['family'],gtFile=str((folder/'cases.private.json.gz').relative_to(ROOT)),machineChecked=True,humanValidated=False))
        report += ['',f"完整 GT（目标状态、合法动作、触发记录）：[数据文件](../../{(folder/'cases.private.json.gz').relative_to(ROOT)})。",'']
        for c in cases:
            if c['mode']!='static':continue
            report += [f'### {F.get(c["family"],c["family"])}：当前状态与正确目标','', '|当前：正面斜视|目标：相同视角|当前：背面斜视|目标：相同视角|','|---|---|---|---|']
            images=[]
            for view in ['isometric','rear']:
                for label,state in [('current',c['initial']),('target',c['goal'])]:
                    key=hashlib.sha256((c['id']+label+view).encode()).hexdigest()[:14];path=rendered/(key+'.png')
                    renderer.rgb(state,view,size=(800,600),supersample=1)[0].save(path)
                    images.append(f'![{label} {view}](curation-images/{key}.png)')
            report.append('|'+ '|'.join(images)+'|');report += ['', 'GT 可行操作（不是唯一顺序）：','']
            for i,a in enumerate(c['referenceActions'],1):
                actor=a.get('actor');key=a.get('candidate');part=next(r['part'] for r in cert['candidates'].values() if r['actor']==actor)
                report.append(f"{i}. {'安装' if a['type']=='attach' else '拆下'} `{actor}`（{part['partNumber']}，{part['name']}）"+(f"，位置 `{key}`。" if key else '。'))
            report.append('')
    report += ['## 还没有通过的部分','', '部分新来源仍缺少闭合碰撞网格、连接定义或完整合法拼装路径，仍留在来源候选层，不拿它们统计模型失败。模块题的预装上下文作为固定装配体；不声称验证了整套大模型从零拼装。像素差异检查也不等同于真人一定看得懂。','', '## 移出的原库模型','', '|套装|名称|依据|','|---|---|---|']
    for r in removed:
        evidence=r['figureAudit']['evidence'];why='；'.join(x['description'] for x in evidence[:2]) or r['withdrawalReason'];report.append(f"|{r['setNumber']}|{r['title']}|{why}|")
    (OUT/'NO-FIGURES-AND-NEW-CASES.zh-CN.md').write_text('\n'.join(report)+'\n')
    write(OUT/'curated-questions.json',dict(cases=allrows,counts=dict(Counter(r['mode'] for r in allrows)),newSourceCases=new_cases,apiCalls=0,referenceOnly=True))
    print('REPORT',len(active),'sources',len(new),'new',len(removed),'removed',new_cases,'new-source questions',flush=True)

if __name__=='__main__':main()
