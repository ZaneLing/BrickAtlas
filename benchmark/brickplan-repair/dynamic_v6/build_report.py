"""Generate reproducible review artifacts and a plain-language release report."""
from pathlib import Path
from collections import Counter,defaultdict
import hashlib,html,json,sys
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE.parent),str(HERE.parent/'eval')]
from dynamic_v6.episode import BANK
from dynamic_v6.object_models import OBJECTS
from dynamic_v6.human_server import review_tasks
from dynamic_v5.build import write
from static_v4.certify import digest

NAMES={'none':'正常拼装，没有人为干扰','removed_piece':'一块被拿走／漏件','shifted_piece':'位置装偏','cascade_removal':'连带掉下多块','extra_layer':'多装一层／多出零件','early_cover':'过早盖住后续安装位置','wrong_color':'颜色拿错','wrong_size':'尺寸或厚度拿错','rotated_piece':'方向装反','swapped_positions':'两块位置互换','wrong_part':'零件类型拿错','buried_wrong_color':'底层装错，需要拆开上层返修','compound_fault':'一次同时发生两种错误'}
def read(name):return json.loads((BANK/name).read_text())
def hashed(text):return hashlib.sha256(text.encode()).hexdigest()
def md(name,text):(BANK/name).write_text(text.strip()+'\n')

def main():
    cases=read('cases.private.json')['cases'];byid={c['id']:c for c in cases};index=read('index.json');release=read('release-check.json');audit=read('audit.json');sets=read('evaluation-sets.json')['sets'];splits=read('splits.json');counts=Counter(c['kind'] for c in cases)
    assert len(byid)==len(cases)==release['cases']==audit['total']
    assert not audit['duplicateTargetModels'] and not audit['duplicateEpisodeStates']
    assert release['bankSha256']==hashlib.sha256((BANK/'cases.private.json').read_bytes()).hexdigest()
    assert {c['id'] for c in index['cases']}==set(byid)
    assert all(r['geometryPassed'] for r in audit['rows'])
    groups=defaultdict(list)
    for c in cases:
        groups[c['modelId']].append(c)
        assert c['pairedGroup']+'--control' in byid
        assert splits['caseAssignments'][c['id']]==splits['sourceFamilies'][c['sourceFamily']]
    for mid,rows in groups.items():
        cert=read(f'models/{mid}/qualification.json');cache=read(f'models/{mid}/audit-v6.json')
        assert cache['sourceHash']==digest(dict(cert=cert,cases=rows)),mid
        assert cert['contentSha256']==digest({k:v for k,v in cert.items() if k!='contentSha256'}),mid
        epath=BANK/'models'/mid/'evidence.json';e=json.loads(epath.read_text())
        e['generatedCases']=e.get('generatedCases',e['admittedCases']);e['admittedCases']=len(rows);write(epath,e)
        assert e['runtimeCertificateSha256']==cert['contentSha256']
    # Equal category counts, with a deterministic family round-robin within each split.
    balanced={};kinds=sorted(set(counts)-{'none'})
    for split in ('development','evaluation'):
        available={k:[byid[i] for i in sets['primary-machine-candidates'] if byid[i]['kind']==k and splits['caseAssignments'][i]==split] for k in kinds}
        quota=min(map(len,available.values()));chosen=[]
        for kind,rows in available.items():
            families=defaultdict(list)
            for c in sorted(rows,key=lambda c:hashed('balanced-v6:'+c['id'])):families[c['sourceFamily']].append(c)
            ordered=[]
            while any(families.values()):
                for family in sorted(families,key=hashed):
                    if families[family]:ordered.append(families[family].pop(0)['id'])
            chosen+=ordered[:quota]
        balanced[split]=dict(perCategory=quota,interventions=chosen,controls=sorted({byid[i]['pairedGroup']+'--control' for i in chosen}),availablePerCategory={k:len(v) for k,v in available.items()})
    write(BANK/'balanced-evaluation.json',dict(rule='Equal category quota within each source-family split; SHA256 and family round-robin, no model results used. Report full-bank macro results as well.',sets=balanced))
    tasks=review_tasks();tasks_by_model=defaultdict(list)
    for code,cid in tasks.items():tasks_by_model[byid[cid]['modelId']].append(code)
    write(BANK/'human-review/answer-key.private.json',tasks)
    rows=[];cards=[]
    catnames={'furniture':'家具','vehicle':'车辆','vehicles':'车辆','machine':'机器','machines':'机器','architecture':'建筑','building':'建筑与街景','household':'家居设备','appliance':'家电','appliances':'家电','equipment':'设备','street':'街景','transport':'交通工具'}
    for mid,spec in sorted(OBJECTS.items()):
        n=groups[mid][0]['targetParts'];num=len(groups[mid]);code=tasks_by_model[mid][0]
        name=spec['name'];category=catnames.get(spec['category'],spec['category'])
        rows.append(f'| {name} | `{mid}` | {n} | {num} | {spec["family"]} |')
        cards.append(f'<article data-search="{html.escape(name+mid+category)}"><img src="models/{mid}/target.png" alt="{html.escape(name)}" loading="lazy"><div><h3>{html.escape(name)}</h3><p>{category} · {n} 块 · {num} 题</p><small>{mid}</small><p><a href="http://127.0.0.1:8767/A?task={code}">打开这个物件的拼装题</a></p></div></article>')
    gallery='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>动态积木 v6 · 42 个完整物件</title><style>body{margin:0;background:#f0f4f6;color:#143349;font:16px/1.65 -apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif}main{max-width:1400px;margin:auto;padding:36px 24px}h1{margin:0;font-size:32px}h2{font-size:21px}p{margin:8px 0}a{color:#096c88}header{background:white;border-radius:16px;padding:28px;margin-bottom:24px}.stats{display:flex;gap:24px;flex-wrap:wrap}.stats b{font-size:25px;display:block}input{font:inherit;padding:10px 14px;border:1px solid #a8bfca;border-radius:8px;width:min(500px,80%)}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px}article{background:white;border-radius:12px;overflow:hidden;border:1px solid #dbe5eb}article img{width:100%;display:block}article div{padding:0 18px 16px}h3{margin:5px 0}small{color:#657b8c}.note{border-left:4px solid #d9a441;padding-left:12px;color:#5e531f}</style><main><header><h1>动态积木：看得出是什么，拼错了要会修</h1><p>从空白底板开始，一次装或拆一块。中间可以出现错误，继续观察、修复，直到和最终目标一致。</p><div class="stats"><p><b>42</b>完整物件</p><p><b>68</b>全部结构</p><p><b>1,872</b>动态题目</p><p><b>12</b>干扰类别</p></div><p>真人入口：<a href="http://127.0.0.1:8767/A">A</a> · <a href="http://127.0.0.1:8767/B">B</a> · <a href="http://127.0.0.1:8767/C">C</a>（本机服务运行时可打开；进度分别保存）</p><p><a href="README.zh-CN.md">版本说明</a> · <a href="FIX-REPORT.zh-CN.md">修复清单</a> · <a href="INPUT-OUTPUT.zh-CN.md">输入输出</a></p><p class="note">已通过全部机器检查；新增题目尚未完成真人验证和正式模型实验。图片为简化积木造型，完整物件为 6–15 块。</p><input id="search" placeholder="按物件名筛选，例如：车、床、椅" aria-label="筛选物件"></header><section class="grid">'''+''.join(cards)+'''</section></main><script>document.querySelector('#search').addEventListener('input',e=>{const q=e.target.value.trim().toLowerCase();document.querySelectorAll('article').forEach(c=>c.hidden=!c.dataset.search.toLowerCase().includes(q));});</script></html>'''
    (BANK/'gallery.html').write_text(gallery)
    fontfile='/System/Library/Fonts/Supplemental/Arial Unicode.ttf'
    font=ImageFont.truetype(fontfile,20);small=ImageFont.truetype(fontfile,14)
    sheet=Image.new('RGB',(1800,7*270+80),'#f0f4f6');draw=ImageDraw.Draw(sheet);draw.text((24,22),'BrickPlan Dynamic v6 | 42 complete objects',font=ImageFont.truetype(fontfile,28),fill='#143349')
    for i,(mid,s) in enumerate(sorted(OBJECTS.items())):
        x=(i%6)*300;y=(i//6)*270+80;im=Image.open(BANK/'models'/mid/'target.png').convert('RGB');im.thumbnail((296,222));sheet.paste(im,(x,y))
        draw.text((x+10,y+222),s['name'],font=font,fill='#143349');draw.text((x+10,y+247),f'{groups[mid][0]["targetParts"]} parts | {len(groups[mid])} cases',font=small,fill='#526a7b')
    sheet.save(BANK/'object-gallery.png')
    kindtable='\n'.join(f'| {NAMES[k]} | `{k}` | {counts[k]} |' for k in NAMES)
    md('README.zh-CN.md',f'''# 动态 Bench v6：本轮已经做好的内容

## 先看结果

| 项目 | 之前 v5 | 现在 v6 |
|---|---:|---:|
| 全部动态题 | 317 | {len(cases):,} |
| 全部结构 | 30 | {len(groups)} |
| 像实际物品的完整模型 | 4 | {len(OBJECTS)} |
| 完整物件题 | 32 | {release['completeObjectCases']:,} |
| 中途干扰类别 | 10 | 12 |

这里“模型”指积木物件。没有把换颜色当作一个新物件：新增的是家具、交通工具、家电、机器、建筑等不同造型。[直接看全部物件](gallery.html)｜[一张总览图](object-gallery.png)

1,872 题里有 **160 道正常题、1,712 道干扰题**。42 个完整物件共 1,588 题，其余 284 题是用于测试连接、遮挡等问题的局部结构。完整物件 6–15 块，全部结构 4–15 块；这些是简化造型，尚不是上百块的大套装。

## 现在怎么用

- 真人直接打开 [A](http://127.0.0.1:8767/A)、[B](http://127.0.0.1:8767/B)、[C](http://127.0.0.1:8767/C)。每个入口有 126 道抽样操作题，覆盖 42 个物件；不用写文字、不用返回 JSON。每一步保存，换题后可继续。
- 先看当前／目标对照图右半的唯一目标，再选零件、看候选位置，点卡片安装。一回合中可以随时看当前状态，一次只装或拆一块。看明白中间变化后，继续修好同一个物件。
- [输入输出说明](INPUT-OUTPUT.zh-CN.md)：用图和例子解释每一步给什么、回什么。
- [修了什么、还欠什么](FIX-REPORT.zh-CN.md)；[正式评测办法](EVALUATION.zh-CN.md)；[物件逐项清单](OBJECTS.zh-CN.md)。

## 检查结果及边界

- 42/42 个完整物件能从空底板装起来，物件自身也连在一起；1,872/1,872 题的原始拼装、干扰和恢复路径通过几何检查。
- 一直照原说明拼、完全不处理干扰的程序：正常题 160/160 完成，干扰题 0/1,712 完成。能读取正确答案再拆开重拼的检查程序：1,872/1,872 完成。后者只用来证明题目能修，不代表 AI 成绩。
- 1,553 道干扰题通过当前图像差异筛选；136 道“自己的动作被抵消”和 23 道低对比变化分开报告，不能混作普通漏检题。
- 新版真人正式答卷 **0**，真实 API 模型实验 **0**；本轮实际 API 花费 **$0**。旧版真人与模型结果保留在 v5，不套用到新版。
- 机器检查并不能保证“模型失败一定是模型的问题”。仍要完成正常拼装对照、独立真人验证及完整回合评测，再讨论漏检和恢复能力。

## 文件

`cases.private.json`、`models/*/qualification.json`、`index.json`、`human-review/answer-key.private.json` 都是出题和评分资料，含类别或答案，**不得直接放进模型请求**。真正输入由 `interface.py` 的 `packet()` 生成。

程序在 `benchmark/brickplan-repair/dynamic_v6/`。旧 v5 的题目和实验保留；当前论文原有数字属于旧实验版本，不能把题量变大当成新增模型实验。

重新打开本机服务：项目根目录双击 `启动动态拼装v6.command`。不需要公网服务器。

### 重建及检查（给维护代码的人）

```bash
export PYTHONPATH=benchmark/brickplan-repair:benchmark/brickplan-repair/eval:benchmark/brickplan-v1
benchmark/.runtime/mlx-env/bin/python benchmark/brickplan-repair/dynamic_v6/admit_objects.py
benchmark/.runtime/mlx-env/bin/python benchmark/brickplan-repair/dynamic_v6/build.py --resume
benchmark/.runtime/mlx-env/bin/python benchmark/brickplan-repair/dynamic_v6/audit.py --resume
benchmark/.runtime/mlx-env/bin/python benchmark/brickplan-repair/dynamic_v6/test_contracts.py
benchmark/.runtime/mlx-env/bin/python benchmark/brickplan-repair/dynamic_v6/test_runner.py
benchmark/.runtime/mlx-env/bin/python benchmark/brickplan-repair/dynamic_v6/build_report.py
```
''')
    md('OBJECTS.zh-CN.md','# 完整物件清单\n\n42 个物件均为原创简化积木造型；包括保留的 4 个旧物件。题量不包含其余 26 个局部机制结构。每个家族的变体放在同一数据分组，避免相似模型分别进入开发和评测。\n\n| 物件 | ID | 目标零件数 | 题量 | 来源家族 |\n|---|---|---:|---:|---|\n'+'\n'.join(rows))
    md('FIX-REPORT.zh-CN.md',f'''# 本轮动态 Bench 修复记录

## 一、物件和题太少

完整物件从 4 个增至 42 个：凳、椅、沙发、书桌、床、上下铺、书架、柜子；小汽车、皮卡、公交、货车、救护车、拖拉机、叉车、消防车、火车、船、飞机、直升机；咖啡机、洗衣机、冰箱、机器人、冲压机；桥、房子、钟楼、楼梯等。新增件没有仅靠改颜色充数。全部形状和装配顺序有机器验证。

题目从 317 增至 1,872；同一物件在早、中、晚多个时点发生不同变化。物理结果完全相同的事件不重复计数；1 道旧的跨类别重复题已从活动题库移出，原记录留在 `excluded-duplicates.private.json`。

## 二、人类拼装会犯什么错

| 情况 | 程序类别 | 题数 |
|---|---|---:|
{kindtable}

“底层装错”会先合法拆开盖住它的 1–3 块，再替换底层、装回盖板；修复时也要考虑拆开上层。它是可执行的结构返修题，但错色有可能完全被遮住，所以并非每一道都能用于看图漏检结论。

“同时两种错误”要求处理两个不同受影响部位，例如一处缺件、另一处多件；不是把同一变化换个名字重复算两遍。

这些是对人类常见拼装失误的结构化模拟，不是从真人实验统计出的真实错误频率。当前每个回合最多注入一次事件，复合事件里可含两处错误；还没有在一个回合反复随机注入多次事故。

## 三、输入输出问题

| 原问题 | 本轮修复 |
|---|---|
| 不知道哪张是现在、目标、上一步 | 三个视角都给有标题的“上一步之前／现在”，目标单独显示；第一步明确只有空底板 |
| 看到左右相同就不知道怎么选 | 明确比较的是同一场景的两个时刻；自己的安装被拿走可能造成左右相同，这类题单列 |
| 零件或候选只显示第一页 | API 与真人页面都提供全部页；零件展开、小卡片展示 |
| 候选图让人误以为是正确答案 | 每个候选都在当前场景中显示，仅标所选零件，不标正确与否；移除目标零件单独抠图 |
| 编号顺序或候选数量暗示哪些是目标零件 | 公开编号随机化后再排序；同一题中所有零件的候选数量相同（12 或 24） |
| 换题丢进度、重复点出错、提交不了 | A/B/C 分开保存、每题单独保存、逐步保存；重复请求只执行一次；旧页面状态会同步，不重复操作；提交只结束本题 |
| 一次输出多步、错误 JSON 没统计 | 一次只接受一个动作；非法动作不改变场景，单独记录格式错误；操作预算包含查看和失败动作 |
| 不回答异常判断就当作没发现 | 缺失／看不清记为未知，不算 false；区分漏检、未答、格式错误、没触发、API 失败 |

## 四、实验比较不公平的问题

旧方式把正常题和干扰题各自跑一遍，两边可能在干扰前已经选了不同动作。新版先运行一次共同过程，在同一条动作后分成两个分支：一边保持正常，一边注入干扰。两边已发生的动作、文字历史和干扰前场景完全一致。

模型若换一种合法顺序拼，系统只在能证明后续仍可修复时，寻找同类变化；这类现场生成事件单列，不能直接冒用原题的可见性结论。没能触发的回合记录原因，不算“模型没发现”。

## 五、通过了哪些检查

- 全部 1,872 题合法原始路径、干扰路径、恢复路径：通过。
- 全部 68 个结构目标不同；同一结构同一时点无重复事件结果。
- 42 个完整物件均能逐件搭建且自身连通。
- 正常题盲执行 160/160 成功；干扰题盲执行 0/1,712 成功；读取答案的清空重拼检查 1,872/1,872 成功。
- 图像分组：正常 160；普通机器可见候选 1,553；动作抵消 136；低对比 23。
- 54 个代表回合覆盖全部完整物件和 12 类干扰，完整运行回合对象；接口、全部页码、点击映射、换题、刷新重放、独立审查者、重复点击及旧状态保护均有回归检查。
- 真正的 API 请求格式已做本地试生成；完整配对执行链用模拟回复检查。没有把模拟回复算成模型成绩，也没有付费调用。

检查原始证据：[release-check.json](release-check.json)、[audit.json](audit.json)、[contract-tests.json](contract-tests.json)、[runner-contract.json](runner-contract.json)、[verification.json](verification.json)。

## 六、仍需补的证据

1. **真人看不看得懂、能不能拼成。** 126 道入口题已可用；至少按物件、错误类别和时点分层收集独立原始操作记录。旧版 A 的少量判断不能证明新版全部题正确。代表抽样也不能替代“逐题都验证”的说法。
2. **正常题能否做成。** 正常拼装失败时，不能直接把干扰题失败归为漏检。需要同时报告正常、受干扰、恢复成功、误报和未答。
3. **规模仍有限。** 完整物件为 6–15 块；类别题量仍不均衡，提供等类别子集和按类别平均分以减轻影响。以后才扩到更长回合、更复杂遮挡、多次事故。
4. **不是真实机器人。** 当前检查刚性几何、连接和规定装拆路径，不模拟摩擦、材料形变、动力学和手爪接触。不能据此声称真实机器人一定可操作。
5. **动作空间仍有限。** 每个零件用候选卡片选位置，主测离散选择、观察与恢复，不是连续三维自由放置。
6. **论文不能只改题量。** 正式论文还需新版多模型重复实验、完整人类基线、输入信息消融、按家族及难度分组结果；本轮没有生成这些尚不存在的成绩。
''')
    md('INPUT-OUTPUT.zh-CN.md','''# 动态拼装：每一步到底给什么、做什么

## 真人操作

第一张对照图里，左半是现在，右半是本题唯一 TARGET。操作后另有时间对照图：左半是自己上一步之前，右半是现在。两种对照图都为 1600×636，场景均为 800×600。第一步没有时间对照图；从空底板开始。不要把不同时间或角度的零件加起来。

1. 看目标图，决定先装什么。白色底板固定，不需要安装，也不能拆。
2. 点下面的小零件图片，或选择编号后点“查看这个零件能放哪里”。所有零件页都展开。
3. 候选图中点一张卡片安装。**候选不保证正确，也不保证此刻装得上。** 一次只安装一块；移动需要先拆、再装。
4. 每次操作后都给最新画面。可切换斜视、俯视、背面；目标图可点击放大。查看也计一次决策，但不动积木。
5. 中间可能有额外变化。勾选“没有／有／看不清”，继续修好；不需要写解释。不选会记为未回答，不会自动当成“没有”。
6. 完成后点“我拼好了，提交本题”。程序按最终结构判定；未完成也可以提交并保留失败记录。换题或刷新不丢之前进度。

**左右相同不一定是错误页面。** 例如上一步本应装上一块，之后那块又被拿走，结果会和上一步之前相同。普通静态图片差异不能判定这种情况，需要结合动作记录；这类题单独统计。

## API 模型输入

每个决策收到：

| 信息 | 内容 |
|---|---|
| 固定目标 | 三张“现在／TARGET”对照，当前和唯一目标在同一张图上，同尺度、同相机 |
| 中间状态 | 首轮没有；之后每个视角一张带标题的“上一步动作前／现在”图，画布与目标对照相同 |
| 零件区 | 每页最多十二块，全部页可见；随机编号，包括备用件，不透露哪些属于目标 |
| 候选位置 | 查看零件后提供它的全部候选页，以当前场景为背景；每个候选显示统一轮廓 |
| 上一步和历史 | 自己之前输出的动作、普通动作反馈；回合不中断，不重置 |
| 操作限制 | 已用决策数和总预算；同一物件的预算不随隐藏错误类别变化 |

模型拿不到：题目 ID 中的错误类别、触发时点、私有状态、目标件名单、正确位置列表、修复答案或“刚发生了某种错误”的通知。候选位置编号仅是动作接口，不是答案标签。出题用 JSON 不可以直接发送。

## API 模型输出

每次只返回一个 JSON 对象、一个动作。无需推理文字。

查看零件：

```json
{"action":{"type":"inspect","partId":"A01"},"unexpectedChange":false}
```

安装一块：

```json
{"action":{"type":"attach","partId":"A01","candidate":"C037"},"unexpectedChange":false}
```

也可以点击某页候选图：

```json
{"action":{"type":"attach","partId":"A01","catalogPage":2,"catalogPoint":[0.375,0.5]},"unexpectedChange":true}
```

拆一块 / 换视角 / 提交：

```json
{"action":{"type":"detach","partId":"A01"},"unexpectedChange":true}
{"action":{"type":"inspect","view":"rear"},"unexpectedChange":false}
{"action":{"type":"finish"},"unexpectedChange":false}
```

上面三行是三种独立示例，不是允许一次发三个动作。`unexpectedChange` 问的是“这一轮观察是否出现超出自己上一步动作的额外变化”，不是“整个物件还没拼完”。第一步填 false。ID 仅为格式示例，每个回合会重新对应。

动作反馈只报告本次是否成功、是否挡住／碰撞；失败动作不改变现场。反馈 OK 也不保证其他部分没发生变化。任何额外变化都只能通过后续正常观察发现。

## 时间顺序

```mermaid
flowchart LR
  A[看目标和当前场景] --> B[输出一个动作]
  B --> C[执行动作并返回普通反馈]
  C --> D[在满足条件的回合中注入一次干扰]
  D --> E[获得动作前与现在的画面]
  E --> A
  A --> F[提交完成并评分]
```

两个配对分支在同一个动作后分开。主接口不提供“系统推算的正确当前状态”；额外给预期画面的版本只能作为单独诊断实验，不能和主成绩混算。
''')
    splittext='\n'.join(f'- {s}：每类 {v["perCategory"]} 道干扰，共 {len(v["interventions"])} 道，配 {len(v["controls"])} 道不同正常题。' for s,v in balanced.items())
    md('EVALUATION.zh-CN.md',f'''# 动态 Bench 怎么测、怎么报结果

## 先确认题和接口，再比较模型

1. 真人直接用 A/B/C 页面完成正常拼装和受干扰拼装，记录完整操作。三人独立做，不能复制 A 的答案。新题的人类验证状态目前为待完成。
2. 先在开发组检查正常拼装。记录失败是看不清、不会选位置、动作错误还是拼装顺序问题。发现接口错误就改后重测，不保留旧版成绩冒充新版。
3. 正式对比采用同一段前序过程的正常／干扰分支。记录图像、动作、反馈、实际事件、费用、模型精确版本和配置。
4. 模型至少覆盖不同厂商的强视觉模型和可复现的开放权重模型；选定时记录实际可用的精确 ID、提供方、日期、图像模式、采样配置和价格。不得把名称相似但版本不同的模型混为同一个。
5. 当前实验方案每个模型／题目跑一次，不重复三次；按来源家族报告区间，不把同一物件的很多变体当成独立的新物件样本。

## 数据怎么分

43 个来源家族固定分到 development / evaluation，相近物件家族不跨组。可用开发组调整提示词，评测组不用于挑选提示词或挑题。

主机器候选集合：1,553 个干扰；对照正常题 160 个。136 个动作抵消和 23 个低对比挑战单独测。机器可见候选仍需相应的人类可理解性证据，不能直接写成“已经人类认证”。

等类别子集在 `balanced-evaluation.json`：

{splittext}

全库仍须给出每类、每个来源家族的结果以及宏平均；不要只给被多数类别支配的一个总正确率。子集大小由最少类别决定，所以应同时保留全库结果。全部配对关系和集合在 `evaluation-sets.json`、`splits.json`。

动态库的部分旧结构也出现在静态库，因此本次只保证动态开发／评测按家族分组；**没有宣称静态训练到动态评测的来源完全隔离**。

## 分清楚几个分母

| 指标 | 怎么算／不能怎么说 |
|---|---|
| 正常拼装成功 | 正常分支最终拼对并提交的比例；先回答模型原本会不会拼 |
| 端到端受干扰成功 | 所有计划施加干扰的尝试都要列出，附实际触发率；没触发要单列 |
| 条件恢复成功 | 两条分支无接口中断、正常分支拼成、干扰实际触发的同前序配对中，受干扰分支拼成的比例；否则分数为空 |
| 异常发现 | 触发后第一次普通观察是否回答 true；缺失不能算 false；报告有效判断数量和未答数 |
| 误报 | 正常分支、干扰前没有新外部变化时回答 true 的比例，同时报每回合和每决策 |
| 格式／操作失败 | JSON 格式、无效候选、碰撞、路径阻挡分别统计，不都归为视觉错误 |
| 反应与代价 | 首个降低实际结构差异的动作要多少决策，检查多少次，拆过多少本来正确的零件，最终差多少 |
| 实验异常 | 拒绝、限流、超时分开；没发生干扰记未触发，不计漏检或修复失败；单条 M 观察不进入主修复率 |

“模型漏检”的最低条件：同前序；正常题拼成且无误报；干扰确实发生；该场景有可理解性证据；模型在对应观察给出有效的异常判断。再核对是否是一次视觉漏检或后续修复策略失败。只看最终没拼成无法区分这些原因。

现场按模型不同合法顺序重新生成的干扰标为 `adaptive-certified`，已有恢复路径，但不可直接继承原题的图像可见性认证。此类回合单列或重新检查。

## 运行和费用

目前已做本地输入生成与模拟回复的配对执行检查，实际付费调用为 0。默认命令不会联网调用模型：

```bash
export PYTHONPATH=benchmark/brickplan-repair:benchmark/brickplan-repair/eval:benchmark/brickplan-v1
benchmark/.runtime/mlx-env/bin/python benchmark/brickplan-repair/dynamic_v6/run_paired.py --case obj-city-car--t3--extra_layer--v01 --model dry-run
```

付费执行需显式传入 `--execute --max-cost <美元上限> --model <精确模型ID>`。上限在每次请求前按已结算费用检查，最后一次请求自己的费用可能超过剩余额度；API 报错的未知费用单列，不能称为精确零费用。

每个物件决策上限为 `max(40, 6×目标零件数+20)`。完整物件 6–15 块，对应 56–110 次；查看、无效操作也计数。一个配对最多共享一次前序后跑两个后半程。

不要先报一个没有依据的全库预算。先用少量正常题及配对试跑取得每对真实均价和最坏成本，再按“配对数 × 模型数 × 重复次数 × 每对均价”估算，另留 20% 余量。本轮本地扩充和验证 API 费用为 **$0**。

## 论文中还不能写的结论

没有新版实测就不能写排行榜；没有真人操作证据就不能说输入输出已经完全排除问题；没有真实物理验证就不能说机器人现实中可靠。现有论文的旧版实验与本版题库说明需要分清版本，再补实验更新表格和图。
''')
    md('human-review/README.zh-CN.md','''# 直接点击操作，不需要写文字

在本机打开 [A](http://127.0.0.1:8767/A)、[B](http://127.0.0.1:8767/B)、[C](http://127.0.0.1:8767/C)。服务未启动时，在项目根目录双击 `启动动态拼装v6.command`。

每位有 126 题：42 个物件，每个抽一题正常、早期干扰、后期干扰。题号不标正确答案或类别。不是要求一次做完；每一步自动保存，关页面、换题、重新打开都可继续。只点选和拼装，不需要文字或 JSON。

三位分别使用自己的字母，不复制答案。完成记录保存在本目录 `runs/`，重新开始的旧回合保存在 `runs/archive/`。自动化测试记录放在 `automation-checks/`，不属于真人答卷。

这些是全程操作题，与旧版只判断两张图有无异常的 12 道题不同。新版本没有继承旧版的已审查标记。抽样操作能检查代表案例，不能证明所有 1,872 题都经过真人验证。
''')
    verification=dict(status='PASS',cases=len(cases),uniqueCaseIds=True,uniqueTargets=True,duplicateActiveEventStates=0,pairedControlsPresent=True,
        cachedAuditsMatchCurrentCertificates=True,certificatesSelfHashed=True,sourceFamilySplitsDisjoint=True,catalogCountsUniform=read('catalog-audit.json')['status']=='PASS',
        contractTests=read('contract-tests.json')['status'],runnerContract=read('runner-contract.json')['status'],humanReviewTasks=len(tasks),newHumanValidationCompleted=False,paidRequestsThisRevision=0)
    assert verification['catalogCountsUniform'] and verification['contractTests']=='PASS' and verification['runnerContract']=='PASS'
    write(BANK/'verification.json',verification)
    files=[*sorted(HERE.glob('*.py')),HERE/'human.html',BANK/'cases.private.json',BANK/'index.json',BANK/'audit.json',BANK/'splits.json',BANK/'balanced-evaluation.json']
    # Include shared mechanics/rendering dependencies, which also affect reproducibility.
    files += [HERE.parent/'baseplate.py',HERE.parent/'eval/vision.py',HERE.parent/'eval/matched_canvas.py',HERE.parent/'evaluation_outcomes.py',HERE.parent/'static_v4/certify.py',HERE.parent/'static_v4/metrics.py',HERE.parent/'dynamic_v5/episode.py',HERE.parent/'dynamic_v5/vision.py',HERE.parent/'dynamic_v5/build.py',HERE.parent/'dynamic_v5/run_api.py']
    write(BANK/'source-manifest.json',dict(schema='brickplan-v6-source-hashes/1',files={str(p.relative_to(HERE.parents[2])):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}))
    print(json.dumps(verification,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
