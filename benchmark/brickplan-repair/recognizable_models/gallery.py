"""Render whole source objects and named completion tasks in their full context."""
from collections import Counter
from copy import deepcopy
import hashlib
import json
import shutil
import numpy as np
from PIL import Image,ImageFilter
from recognizable_models import ROOT,OUT
from recognizable_models.specs import MODULE_IDS
from community_modules.specs import SPECS
from community_modules.core import ModuleAssembly,render_certificate
from community_modules.run_episode import PALETTE
from dynamic_v5.vision import DynamicVisionRenderer
from expansion_v7.build import read,write,states_for
from expansion_v7.runtime import runtime
from expansion_v7.scope import require_allowed
import re

PUBLIC=OUT/'public'


def render_model(meta,cert,manual,cases):
    mid=meta['id'];folder=PUBLIC/'assets'/mid;folder.mkdir(parents=True,exist_ok=True)
    if meta['kind']=='complete':
        rt=runtime(cert);visual=render_certificate(rt.cert)
    else:
        rt=ModuleAssembly(cert);visual=render_certificate(cert)
    renderer=DynamicVisionRenderer(visual,runtime=rt)
    normal=manual['actions'];states=states_for(rt,normal)
    goals=[k for k,r in cert['candidates'].items() if r['kind']=='goal']
    keys=list(visual['fixed'])+goals
    def save(state,name,highlight=False,frame=keys):
        image,mask=renderer.rgb(state,'isometric',size=(1600,1200),supersample=1,frame_keys=frame)
        if highlight:
            ids=[renderer.ids[cert['candidates'][k]['actor']] for k in goals]
            active=Image.fromarray(np.uint8(np.isin(mask,ids))*255)
            border=np.asarray(active.filter(ImageFilter.MaxFilter(11)))-np.asarray(active)
            image.paste((226,114,29),(0,0),Image.fromarray(border))
        path=folder/(name+'.png');image.save(path)
        return str(path.relative_to(PUBLIC))
    full=save(states[-1],'full');start=save(states[0],'start')
    marked=save(states[-1],'remaining-highlight',True) if meta['kind']=='module' else full
    # Fixed framing for every stage. Never zoom the initial empty scene differently.
    shown=list(range(len(normal)+1)) if meta['kind']=='complete' else sorted({0,len(normal)//2,len(normal)})
    stages=[dict(step=i,image=start if i==0 else full if i==len(normal) else save(states[i],f'step-{i:02}')) for i in shown]
    families=dict(Counter(c['family'] for c in cases))
    # These public files are explicitly reference demonstrations, never model inputs.
    reference=dict(model=mid,referenceOnly=True,notModelInput=True,orderRequired=False,
        actions=normal,states=states,caseIds=[c['id'] for c in cases])
    write(folder/'reference.json',reference)
    public=dict(meta,images=dict(full=full,start=start,highlight=marked),stages=stages,
        reference=str((folder/'reference.json').relative_to(PUBLIC)),
        caseCount=len(cases),families=families,referenceOrderIsRequired=False,
        humanValidated=False,modelEvaluated=False)
    print('RENDER',mid,meta['sourceParts'],meta['parts'],flush=True)
    return public


def main():
    PUBLIC.mkdir(parents=True,exist_ok=True)
    PALETTE.update(dict(re.findall(r'CODE\s+(\d+)\s+VALUE\s+(#[0-9A-Fa-f]{6})',
        (ROOT/'assets-source/ldraw-library/locked/LDConfig.ldr').read_text())))
    rows=[];screen=read(OUT/'admission-screen.json')
    for meta in screen['admitted']:
        folder=OUT/'models'/meta['id']
        rows.append(render_model(dict(**meta,explanation='从空白底板开始，装完原始 LDraw 文件里的所有零件；不是裁下来的结构。'),
            read(folder/'certificate.private.json.gz'),read(folder/'manual.private.json.gz'),read(folder/'cases.private.json.gz')))
    for mid in MODULE_IDS:
        spec=next(s for s in SPECS if s['id']==mid);folder=ROOT/'deliverables/brickplan-community-modules'/mid
        cert=read(folder/'certificate.private.json');manual=read(folder/'manual.private.json')
        cases=[c for c in read(folder/'cases.private.json') if set(c.get('humanErrorIds',[])).isdisjoint({'H12','H14','H15','H16','H17','H18'})]
        meta=dict(id=mid,model=spec['model'],title=spec['title'],object=spec['module'],kind='module',
            parts=len(spec['indices']),sourceParts=cert['source']['totalInstances'],source=cert['source'],
            explanation=spec['explanation'],sourceInstancesDropped=0,sourceGeometryModified=False,
            status='EXISTING_VERIFIED_MODULE_REDISPLAYED',newModel=False)
        rows.append(render_model(meta,cert,manual,cases))
    write(PUBLIC/'models.json',dict(models=rows,wholeCount=len(screen['admitted']),moduleCount=len(MODULE_IDS),
        apiCalls=0,newCompleteObjectCases=read(OUT/'case-index.json'),humanValidationPending=True,
        historicalCatalogueCountUnchanged=True))
    for name in ('index.html','style.css','app.js'):
        shutil.copyfile(ROOT/'benchmark/brickplan-repair/recognizable_models'/name,PUBLIC/name)
    table=['# 完整小物件与有明确用途的收尾模块','','## 这次怎么改',
        '',f"- 新增 **{len(screen['admitted'])} 个完整小物件**，保留下载文件的全部零件，从空白白色底板开始。",
        '- 把已有 **12 个有明确用途的收尾模块**集中展示，每个同时给完整成品、已装主体和本次待装部分。它们不是新增 12 个模型。',
        '- 不再用从大模型按距离截取的小块来代表“一个物件”。原有局部结构保留作结构诊断资料，不作为这个物件页的动态主展示。',
        '- 目标状态正确、每次操作实际合法即可；参考说明的先后顺序不唯一，不要求照抄。',
        '- 这是程序验证的可行路线，尚未经过本轮真人审查或模型测试。付费 API 调用：0。',
        '', '本机看图：<http://127.0.0.1:8799/objects/index.html>。',
        '', '## 小物件：完整搭建', '', '| 模型 | 原文件零件 | 本次安装 | 开始状态 |', '|---|---:|---:|---|']
    for row in rows:
        if row['kind']=='complete':table.append(f"| {row['title']} | {row['sourceParts']} | {row['parts']} | 空白底板 |")
    for kind,title in [('complete','完整小物件图例'),('module','大物件：最后补什么')]:
        table+=['',f'## {title}','']
        for row in rows:
            if row['kind']!=kind:continue
            source=row['source'];table += [f"### {row['title']} · {row['parts']} 块",'',row['explanation'],'',
                f"原文件共 {row['sourceParts']} 块；原始零件移除数：0。来源：[LDraw OMR]({source['url']})，作者：{source['author']}。",'',
                '| 已装主体／开始 | 完整目标 | 本次补装部分（橙边仅用于讲解） |','|---|---|---|',
                f"| ![开始](public/{row['images']['start']}) | ![成品](public/{row['images']['full']}) | ![范围](public/{row['images']['highlight']}) |",'']
    table+=['## 输入、输出与判分','','- 输入：当前场景、唯一目标、零件目录；说明步骤随时可查看。大物件的主体从开局就已装好，不让模型从零猜整栋建筑。',
        '- 输出：每次装一块、拆一块、查看或结束。现有匿名零件编号／位置编号接口沿用。',
        '- 静态修复以题目当前阶段的目标为准；动态拼装的目标是本页完整成品或指定部分全部补齐。',
        '- 动态错误从实际中途状态触发；未到干扰位置列“未触发”。正常分支与干扰分支分开记录。',
        '- 静态正常对照和动态正常对照都保留，防止模型看到题目就乱拆。',
        '- 不同合法装配顺序均可；程序参考路线用于验证可行性，不作为中间步骤必须一致的答案。',
        '', '## 哪些暂时没有作为完整动态物件加入','',
        '下列为候选筛选结果，不等于模型能力不足。原文件完整下载保留；没有删掉不支持的零件来凑“完整”。','',
        '| 候选 | 尚未加入的原因 |','|---|---|']
    def plain_reason(row):
        reason=row['reason']
        if '50-part' in reason:return '零件偏多，后续应挑有明确用途的收尾部分。'
        if 'Open collision mesh' in reason:return '部分零件的碰撞模型有缺口，暂时不能可靠判断装拆是否合法。'
        if 'Non-rigid' in reason:return '源文件部分零件的转角精度尚未通过检查，需要先处理。'
        if 'legal build witness' in reason:return '目前的执行程序还没有找到能从头装完的合法路线。'
        return '还没有通过完整模型的技术检查，详情见 admission-screen.json。'
    table += [f"| {r['title']} | {plain_reason(r)} |" for r in screen['rejected']]
    table += ['', '## 统计范围','','新增完整物件题目单独保存在 `case-index.json`，已有收尾模块是重新展示。尚未与全库做跨库去重，因此没有直接加到历史 5,793 题的总数里。',
        '', '原文件、来源哈希、碰撞代理修补说明、逐步运行证据保存在本目录；`public/` 仅放展示材料。',
        '', '## 本机运行实际题目', '', '下面的入口沿用现有的一步一操作接口；收尾模块的当前／目标图保留完整物件背景。示例：', '', '```bash',
        'PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m recognizable_models.run_episode --case objects::whole-4018::dynamic::control::t0',
        'PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m recognizable_models.run_episode --case cottage-roof-dynamic-missing',
        '```', '', '第一条从零拼小船；第二条从已装主体补屋顶，中途发生少件。每条命令逐行接收一个动作对象，不会调用任何付费 API。',
        '', '重建顺序：`recognizable_models.intake` → `recognizable_models.prepare` → `recognizable_models.build` → `recognizable_models.gallery` → `recognizable_models.audit`（都用上述 Python 环境）。']
    (OUT/'README.zh-CN.md').write_text('\n'.join(table)+'\n')
    print('GALLERY',len(rows),flush=True)


if __name__=='__main__':main()
