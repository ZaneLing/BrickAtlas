"""Write the current static benchmark documentation from validated counts."""
import json
import shutil
from static_bench import OUT, ROOT, TYPES, CHALLENGES, dump

index=json.loads((OUT/'index.json').read_text());report=json.loads((OUT/'static-validation.json').read_text())
cases=[json.loads(l) for l in (OUT/'cases.jsonl').read_text().splitlines()]
examples=[]
for model in ('10001--deep','v23-3223--deep','v23-6678--deep'):
 rows=[c for c in cases if c['modelId']==model]
 examples.append(max(rows,key=lambda c:c['expectedOptimum']))
examples.append(max((c for c in cases if c['kind']=='swapped_positions'),key=lambda c:c['expectedOptimum']))
links='\n'.join(f"- [{c['title']} · {c['expectedOptimum']} 步](http://127.0.0.1:8783/#repairs/{c['modelId']}/{c['id']})" for c in examples)
counts='\n'.join(f"| {TYPES[k]} | {v} |" for k,v in index['kinds'].items())
difficulties=' / '.join(f"{k}: {index['difficulty'].get(k,0)}" for k in ('D0','D1','D2','D3','D4','D5'))
text=f'''# BrickPlan 静态错误修复 Bench

当前版本：static-repair/2。任务从一个固定错误状态开始，模型进行观察与拆修，直到当前状态等于目标。过程中没有外部取走、临时封顶、旧计划或动态干预，也不要求从零开始搭建。

入口：[静态修复工作台](http://127.0.0.1:8783/#repairs)。双击 `启动错误修复Bench.command`。机器人仿真属于单独的历史模块。

## 当前案例库

- {index['modelCount']} 个结构条目：123 个原有模型子结构，加 4 个由原始零件与位姿组成的 16 件相连结构变体。
- {index['caseCount']:,} 个生成案例，包含 {index['modelCount']} 个无故障对照；保留 2 个用户自定义案例。
- 每个结构 2–3 个单独错色题；错色还可以作为复合题的一部分。
- {index['kinds']['compound']} 个复合题，包含混合类型、多处错误、共享拆修通道与连接依赖耦合。每个结构内部按实体形状、颜色和位姿去重。
- 最优拆装成本 0–{report['maxOptimum']}；{difficulties}。

| 案例主类型 | 数量 |
|---|---:|
{counts}

“多余零件”同时作为静态属性统计；当前垫高案例包含多余垫片与高度错层，因此这些覆盖数不可直接相加。

## 类型的含义

错形状/功能是几何轮廓或连接功能不同，例如斜坡换成普通砖、光面板换成有凸点的板。同类错尺寸要求形状/特征描述一致，仅尺寸不同，例如普通 2×4 板换成普通 2×2 板。不能仅凭 LDraw 编号不同就判为错形状；每例都导出双方的实际编号、名称与颜色。

部件位置互换是两个真实原件占用了对方的位置；几何和颜色完全等价、视觉上毫无变化的互换不入库。高层复杂度来自实际初态的耦合约束，不从假想的历史动作推断错误。

已移出当前库：外部移除、旧计划失效、依赖顺序错误、过早封闭、合法但高返工、独立的插入路径被挡题。后几项曾复用同一漏件布局。现在保留其真实静态漏件/错件状态，把“需要拆开正确件”作为有成本证据的挑战属性，不重复当成新错误。

## 难度证据

D0 是无故障；D1=1–2 步，D2=3–5 步，D3=6–9 步，D4=10–15 步，D5=16 步以上。它们表示注册离散几何域内的精确最少拆装次数，并不直接等同于视觉推理难度。

`repairEvidence` 包括：无约束编辑下界、结构约束额外动作数、一条最优计划暂拆的正确件、直接修复被何种约束阻止，以及联合修复相对逐个单独修复的节省量。暂拆件清单是该条最优计划的证据，不声称是所有最优计划中最少的暂拆件集合。

推荐先看：

{links}

## LLM / VLM 到底能看见什么

当前 `#repairs` 是人工审核工作台。人可以自由转动、选择七个视角、展开、单件查看和回放答案。默认关闭可穿透遮挡的审核高亮。以上人工能力不能当作模型已经获得的输入能力。

当前仅保留 `visual-rgb-v3` 视觉输入。纯文本与旧 views 入口已停止新调用；旧实验作为历史证据保存，不能代表新版视觉成绩。新图与完整请求见 [视觉输入修正版](../brickplan-visual-input-v3/README.zh-CN.md)。

- 当前/目标每个视角单独发送 1600×1200 无损 PNG，场景不叠文字。首轮立体、背面、顶部；其余视角、任意旋转、高清局部均可按需请求。
- 文字仅保留任务、动作格式、匿名句柄和执行反馈；不提供型号/颜色描述、坐标矩阵、支撑图、阻挡关系或当前/目标状态映射。
- 独立零件参考卡仅在边栏标注匿名句柄；不再默认提供所有件的当前/目标配对答案表。图上位置可用于选择可见件。
- 统一单件隔离检查仍按需对所有件开放，并单独计数；它是辅助观察，不能声称仅靠外部相机解决了密封内部遮挡。
- 每例付费调用前按新版高清渲染重新做私有像素差异准入；旧版 256×192 全库检查是历史证据。
- 原题库最优值来自较小的动作域，不能直接用于新版操作域的最优率。

静态是指错误初态固定、无外部干预；模型在修复中进行拆装或改变观察视角仍然符合该定义。

## 验证与文件

[static-validation.json](static-validation.json) 记录 {report['caseCount']:,} 个案例的初态/目标、全部 {report['oracleActionsReplayed']:,} 个修复动作、精确最优解复算、{report['independentBfsChecks']} 个独立 BFS 交叉检查、错件分类、每模型错色上限与物理布局去重。当前注册域采用理想连接、离散位置、认证的碰撞与直线拆装约束，不包含机器人控制或真实力学结论。

- `index.json` / `cases.jsonl`：当前静态库。
- `models/<id>/qualification.json`：零件、候选位置及几何关系；`cases.json`：静态任务；`record.json`：模型统计。
- `observation-protocol.json`：观测规则与模型入口状态。
- `saved/` 与 `reviews.json`：用户自定义案例及审核记录。
- `archive/before-static-v2/`：迁移前的案例、证书、统计和说明。旧机器人验证报告只对应旧库，不能用于本版本。

从仓库根目录复查：

```bash
benchmark/.runtime/mlx-env/bin/python -B benchmark/brickplan-repair/validate_static.py
```
'''
(OUT/'README.zh-CN.md').write_text(text)
(OUT/'DATASET.md').write_text(f'''# BrickPlan Static Repair v2

This is a fixed-initial-state repair benchmark: observe an incorrect assembly, repair it, and finish at the target. No external event, old plan, erroneous action prefix, or from-empty assembly history is an input or task label.

The active bank contains {index['caseCount']:,} cases across {index['modelCount']} structure entries: 123 source models plus four expanded 16-piece source-derived structures. There are {index['kinds']['compound']} multi-defect cases and 2–3 standalone color cases per structure. Source-exact and previously declared reconstructed target provenance remains attached to every model and case.

## Labels and difficulty

Base static defects are missing, wrong color, wrong shape/function, same-family wrong size, horizontal offset, orientation, height layer, extra part, and swapped positions. A compound case has multiple independent state-defect groups. Extra spacers also carry height-layer effects. Shape/function and size substitutions use mutually exclusive actual-part descriptions, not stale copied names.

D0: control; D1: 1–2 operations; D2: 3–5; D3: 6–9; D4: 10–15; D5: 16+. The maximum exact repair cost is {report['maxOptimum']}. These bins measure planning cost in the registered geometric domain, not visual difficulty. Separate evidence records the unconstrained edit lower bound, additional actions imposed by constraints, collateral correct parts in one optimal witness, direct-action rejection checks, and shared-access savings.

| Primary type | Cases |
|---|---:|
{counts}

## Observation and evaluation status

The browser is an author/reviewer interface. The new `benchmark/brickplan-repair/eval/` OpenRouter adapter connects this bank; the legacy model page remains archived. Real pilot traces and results are reported separately in `../brickplan-api-pilot/`.

Only `visual-rgb-v3` is active. It sends individual 1600×1200 clean RGB images, separate inventory cards, and anonymous action handles. Text does not expose part descriptions, colors, transforms, support/blocking graphs, current/target assignments, or errors. Named views, arbitrary rotation, native-resolution crops and visual point selection are supported. Uniform part isolation is optional assisted observation, not exterior-only visibility. Each case must pass a new private native-resolution visibility gate before model calls. Historical text and annotated-view results are retired evidence and cannot be pooled with V3. The finite action space remains larger than the original per-case oracle space, so old optimal costs are reference-only. Eight new four-defect cases stress coupled access; `four-fault-expansion.json` records evidence.

## Verification

All {report['caseCount']:,} current cases were independently re-solved and their {report['oracleActionsReplayed']:,} oracle actions replayed. {report['independentBfsChecks']} representative kind/difficulty/structure groups were cross-checked with an independent FIFO BFS. Per-model color caps, static-only schema, replacement definitions, certificate digests, root partitions, unique physical layouts, and index/JSONL counts passed. See `static-validation.json`.

The scope is discrete certified geometric repair with ideal connections and registered straight extraction paths. Robot motion, dynamics, grasping, and physical-world accuracy are not evaluated. Older simulator reports describe the archived bank only.

Current files: `index.json`, `cases.jsonl`, `models/`, `saved/`, `reviews.json`. Prior data is archived under `archive/before-static-v2/`. See [Chinese usage and detailed definitions](README.zh-CN.md).
''')
p=ROOT/'brick_assembly_error_taxonomy.md';archive=OUT/'archive/before-static-v2/brick_assembly_error_taxonomy.md'
if not archive.exists():shutil.copy2(p,archive)
p.write_text('''# BrickPlan 当前静态错误分类

当前任务：给定错误状态与目标，完成拆装修复。这里的静态指没有外部环境干预；允许模型在修复过程中观察和拆装。

| 类型 | 定义与边界 |
|---|---|
| 漏件 | 目标要求的零件在初态中缺失 |
| 错颜色 | 几何与位置对应目标，颜色不同；每模型单题 2–3 道 |
| 错形状/功能 | 几何形状或连接功能不同，如斜坡换普通砖；不使用模糊的“错型号” |
| 同类错尺寸 | 形状/特征相同，仅长宽高不同；与错形状分类互斥 |
| 水平错位 | 正确原件位于错误水平位置 |
| 朝向错误 | 非对称原件朝向不同，排除对称等价旋转 |
| 高度错层 | 层高错误；当前多余垫片案例同时体现多余件和错层 |
| 多余零件 | 目标不需要的实体，当前主要是造成错层的垫片 |
| 部件位置互换 | 两个原件互占位置，排除视觉等价的无意义交换 |
| 复合错误 | 两处或多处静态差异同时存在，需联合修复 |

难度与类型分开记录：精确最少动作 D1–D5，是否需要暂拆正确件、深层嵌入、多错误共享拆修通道、连接依赖耦合、异类组合、三处及以上错误。遮挡是观察条件，不是虚构的历史错误。

删除当前标签：外部移除、旧计划失效、错误动作顺序、过早封闭、合法但高返工，以及重复使用漏件布局的“插入路径被挡”单独分类。实际路径约束仍会影响静态修复成本，并保留逐步验证证据。

完整数量、案例、可见性限制和验证见 [当前静态案例库说明](deliverables/brickplan-repair-library/README.zh-CN.md)。原始长程/动态研究分类保存在 `deliverables/brickplan-repair-library/archive/before-static-v2/brick_assembly_error_taxonomy.md`，不属于当前 active bench。
''')
launcher=OUT/'启动错误修复Bench.command';s=launcher.read_text().replace('"modelCount": 123','"benchmarkMode": "static"');launcher.write_text(s)
legacy=OUT/'启动全模型修复案例库.command';target=OUT/'archive/before-static-v2'/legacy.name
if not target.exists():shutil.copy2(legacy,target)
legacy.write_text('#!/bin/bash\nset -euo pipefail\nBRICKPLAN_FOLDER="$(cd "$(dirname "$0")" && pwd)"\nexec "$BRICKPLAN_FOLDER/启动错误修复Bench.command" "$@"\n')
print('Updated static docs, taxonomy and launchers.')
