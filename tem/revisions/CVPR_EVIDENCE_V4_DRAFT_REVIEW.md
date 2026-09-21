# BrickAtlas evidence-v4-draft：第六轮 CVPR 模拟审稿

## 1. 总体结论

**模拟推荐：Borderline，当前略偏 Weak Reject（5/10）；置信度：中等。**

这是论文贡献与证据解释的条件性判断，不是接收概率，也不是对工程质量的否定。与 v3 相比，本版已经实质修复近邻定位、Color 角色、合法单图基线与 no-image 解释。本轮没有确认新的协议内满分捷径、gold 计算错误或足以单独拒稿的新增 CRITICAL。

但现在还不能仅凭修复完成给出 Weak Accept：**QA 子集基线的同口径分析尚未实现；Part-type 的主张与保持答案对照的范围尚未最终确定；独立科学增量虽然表述更清楚，仍需要由真实诊断发现体现。**

继续采用作者指定前提：**假设所有计划模型实验均已完成**，不因当前文件里的 0/9 模型运行、0/280 主视觉最终判断而扣分。不进一步假设实验结果有利，不虚构任何模型排名、效应大小或人审一致性。实际代码的分析能力与论文所声明的推断口径仍然需要检查。

建议不再推倒重建 benchmark，也不要为了获得“更难题目”而删除 Color。最短路线是：确定 Part-type 的对照范围，完成 QA 子集同口径基线及真实结果到论文的绑定，然后围绕研究发现收束正文。

## 2. 本次审稿对象与边界

### 锁定对象

- 主文：`benchmark/paper/evidence-v4-draft/main.pdf`，**8 页**。
- 补充材料：`benchmark/paper/evidence-v4-draft/supplement.pdf`，**8 页**；不是上一个草稿阶段的 7 页。
- 新增代码：`benchmark/suite/ldraw-evidence-v4-draft/`。
- 新增审计：`benchmark/ldraw-evidence-v4-draft/`。
- 依赖基线：封存的 `ldraw-evidence-v3` 输入、运行协议与分析器；视觉数据集仍是 `brickatlas-display-v3`，不是已经生成了新的 invariance 数据集。

```text
main.pdf SHA-256
7010033fa51ff57c9aec07b7748061dc05b03177cb6cb77ca9f34a84e0811e13

supplement.pdf SHA-256
28484173a15af8b33ef7e1e0bb71efc287fcdcfd1cbccf5d04e143b5d66541b5

main.tex SHA-256
dfcbaffae5567ff810d309e5d6712c1cfedceacc656026426d0523014507b606

supplement.tex SHA-256
34ac8ba553c3189470ba7c7e8a6490eabdba4a8c563bbcdbd38418d3ff614078
```

主文、补充材料均完整阅读源码并逐页查看当前 PDF。以下代码行号对应本次读取的文件；论文位置同时给出章节，避免源码行号与审稿版蓝色行号混淆。

### 实际进度

`CODEX_PHASE_TRACKER.md` 明确记录：Phase 1 完成，Phase 2 机器审计通过；Phase 2.4 路线待决定，Phase 3A 子集基线实现尚未开始。**这份草稿不是声称完整执行了上一轮所有升级阶段。** 因此，本审稿将“尚未接入”与“实现错误”分开处理。

## 3. 上轮五项问题，现在解决到哪一步

| 上轮问题 | 当前判断 | 理由 |
|---|---|---|
| VisualFLIP 直接近邻未进入定位 | 引用与比较层面关闭；科学增量仍需结果支撑 | §2 明确独立配对、pair accuracy、人工审查等是已有内容；没有夸大首创 |
| 图像依赖与指代依赖混淆 | Color 与 no-image 解释已关闭；Part-type 的广泛稳健性范围待定 | Color 明确为 appearance sanity track；no-image 的条件性机械性质已说明 |
| QA 子集缺同口径先验基线 | 未关闭 | 新 draft analyzer 只有去图/文本辅助函数，继承 v3 analyzer 仍加载全量 prior |
| 三模型同 provider 的外推边界 | 范围表述已关闭 | 明确不是跨 provider 或最新模型排行榜；不再按不存在的“六模型承诺”扣分 |
| 修复叙事重于科学发现 | 明显改善，但结果叙事仍需收束 | 引言已给独立贡献，旧 oracle 例子移到局限；方法篇幅仍偏审计合同 |

## 4. 已确认的优点

### 4.1 近邻定位不再只是补一条引用

**位置**：主文 §1、§2，`main.tex:84–104,126–136`；`related-work-matrix.md`。

论文明确承认 pair accuracy、Both、最小图像编辑不是贡献，比较只声称“所读章节未规定相同的 CAD/display-reference、有限分配与精确观测审查合同”，而不是断言近邻没有 identity modeling、shortcut control 或人工审查。此前的文献定位问题在写法上已经正面回应。

本轮复核的是新增比较及其本地来源记录，没有开展一次新的全领域查新；不将其解释成已经证明新颖性或优越性。

### 4.2 Color 基线是合法视觉方法，而不是私有字段查询

**位置**：主文 §4.1；补充 §2.3；`single_image_baselines.py:36–115`。

预测器只消费单个 model-visible wire 内的 PNG、文字和选项，拒绝额外 metadata、私有 mask、文件路径与第二张图片。算法从整图颜色连通域投票，不读取目标编号、不读取源模型或另一侧 gold。评测侧在预测完成后连接 observation ID 和 gold。

本轮额外只读重跑全部 **146 个预测**，每个输出与冻结记录完全一致；未修改预测器、阈值或结果文件。对应输入边界的合成单元测试也通过，包括空工作目录调用和拒绝私有字段。

### 4.3 Color 数值应准确区分端点与配对

从逐题明细重算：

| 指标 | 命中数 | 百分比 |
|---|---:|---:|
| 所有单图端点正确率 | 141/146 | 96.58% |
| A 侧准确率 | 71/73 | 97.26% |
| B 侧 NewAcc | 70/73 | 95.89% |
| 双侧正确率 Both | 68/73 | 93.15% |
| 等源权重 Both | — | 91.875% |

只有 **5 个弃答**，原因全部是 `no-color-region`；其余 141 个预测全部正确。没有“另外 6 个 no-vote”或“11 个错误”的事实。论文和补充材料中的 141/146、68/73 对应关系是正确的。

**高基线不等于任务无效，也不是任何模型的能力上限。** 一个感知检查项本就可以让简单方法表现很好。模型比它好、与它相当或明显更差，都可能有用途；价值取决于结论，而不是必须超过某个分数。本稿不汇总两视觉族总分，所以“Color 占主 pair 数较多”也不能直接推导它稀释了综合评分。

### 4.4 输入与统计语义更清楚

主文 §5.4 明确：去图后相同请求、不同 gold，仅在相同确定性输出条件下推出 Both=0；这不是 reference-selection floor。主文 §7 也已将历史 67/67 规则准确写成 oracle-assisted，而非协议内合法攻击。

这些修改关闭了上轮的重要解释风险，不应再重复扣分。

### 4.5 图挑战没有新增的强弱分区错误

主文 Table 5、§6.3 的正确口径是：

- **Strong change**：匿名 1-WL lookup 为 0/12 Both，BFS/union-find 为 12/12。
- **Strong invariance**：匿名 1-WL lookup 为 6/12 Both，BFS/union-find 为 12/12。

前者是不同 gold 的结构挑战，后者是同构、相同 gold 的保持性检查，不能混写。Table 5 caption 已说明 small proof of concept 和 invariance reuses anchors；§6.3 已限制在八个源、一个构造。无需为这项已明确的限制再添加一个拒稿级意见。

## 5. 仍影响接收的意见

### M1. QA 子集基线尚未与模型结果形成同口径闭环

**严重度：MAJOR，分析与证据可解释性；不是“模型还没跑”的扣分。**

**位置**：

- `suite/ldraw-evidence-v4-draft/analyze.py:1–29` 只定义去图和 prompt bytes 辅助函数，并明确 live/subset integration 待后续阶段。
- 继承的 `suite/ldraw-evidence-v3/analyze.py:69–78` 对模型计算 full / both-decidable。
- 同文件第 275 行仍加载全量 `answer-prior-audit.json`。
- 新的 `single-image-color-baseline.json` 也只有当前全量统计，尚未连接最终 QA 筛选集。

必须同时承认：**v3 已有完整模型 runner、receipt 验证与分析框架，不能因为 v4 文件短就说整个项目没有运行链。** 尚缺的是新版同口径子集整合及其发布入口。

即使模型指标已经做完，若把筛选后模型结果与全量基线并列，差异仍可能来自所评题集或来源权重，而非模型能力。这个缺口不会因填完分数自动消失。

**最小修法**：

1. 从同一最终 QA snapshot 构造每个 family 的 full / both-decidable pair 集合。
2. 对固定选项、文字规则、额外权限 oracle 审计，以及新 Color 单图基线的逐题记录，按同一 pair 集合筛选。
3. 复用相同 source 聚合定义重算 micro、source-macro、区间与 coverage；保留 baseline access 标签。
4. 增加反例单测：QA 选择改变某个答案位置或来源构成时，报告必须显示新边际及新基线，不能继续引用全量平衡保证。
5. 让新分析结果绑定既有真实回执，不要删除 protocol-only 的保护断言来假装发布实证结果。应建立明确的 empirical 分支或新分析入口。

**关闭条件**：每条模型结论都能对应同题集、同权重基线；没有真实 QA 时先通过合成反例，真实子集接入后再完成最终验收。无需重跑输入未变的模型，也无需为了恢复 .40 门而调整人审结果。

### M2. Part-type 需要确定主张边界，不宜把可行性当成已完成对照

**严重度：条件性 MAJOR。若只主张当前 answer-changing 干预下的 paired correctness，可作为显式局限；若主张普遍稳健的指代选择，则需额外证据。**

**位置**：主文 §4.2、§5.5、§7；`part-type-invariance-feasibility.json`；`PHASE_2_ROUTE_DECISION.md`。

本轮核实了全部 67 个 parent：

- 共枚举 **201** 个错误候选间交换，全部满足机器结构、唯一 gold 保持和投影边界检查。
- 其中 **192** 个交换涉及不同 source part types，覆盖 **66** 个 parent。
- 67 个 parent 全保留，未静默排除；source type 不同只是筛查代理，不是视觉可区分性的证明。
- `route_selected` 与 `selected_swap` 仍未选择，也没有新增保持答案刺激或相应模型结果。

当前 A/B 证明的是在指定改动下能否同时答对，不覆盖“不应改变答案的无关标签变化”。缺少后一类控制不等于现有 gold 错，也不能据此断言模型实际在机械追随标签。尤其模型两侧独立调用，不能假设它知道某个标签刚被交换。

**推荐修法**：

- 若继续强化 evidence selection 主线，选择路线 B：每个合格 parent 增加 A/I 保持答案对照，交换两个非正确候选标签；保持题干、选项、正确对象、几何和相机不变。
- 同时报告 A/B 的正确改变、A/I 的正确保持、错误改变、稳定错误和格式失败，分别给分母；共享 A 不能重复算独立样本。
- 新控制需新版本、观察 hash 和真实人审。不能把 201 个机器可行候选直接认定为 201 个可判定题。
- 若选择路线 A，则在摘要/主结论/局限中一致限定为当前 candidate-label reassignment 的 paired correctness，明确尚未估计 answer-preserving nuisance 下的稳健性。

**我的建议**：优先路线 B，因为已做的结构筛查覆盖全部来源；但不强迫固定数量或新增第三种任务。新增控制的价值是补齐一个科学对照，不是让工程继续膨胀。

### M3. 独立贡献的表述已改善，但还需展示为何值得使用

**严重度：MAJOR，科学价值判断；结论取决于结果内容，而不是有没有结果文件。**

主文 §1 已不再把 pairing/Both 当首创，也将“修复旧版”移出主要贡献。现在的三项贡献是 source/display contract、受限先验审计、exact-observation 与 receipt lineage。这些组合可以成为有价值的诊断工具，但不能仅凭协议完备自动证明新增视觉认识。

即使三个模型的每个指标都填好，审稿人仍会问：

- 哪一类看似正确的视觉表现，在正确处理指代或可判定性后得到不同解释？
- 什么失败在 ordinary accuracy 中被遮蔽，而通过配对或保持性对照能分辨？
- 读者得到结果后，能据此改进什么，或避免哪种错误评估结论？

**最小修法**：

1. 让主结果节围绕一到两个真实、可复核的诊断现象组织，而不是仅列完整排行榜。
2. 把场景、exact wire、真人判断、逐端点响应和对应对照放在一起解释；具体案例由真实回执选择，不补造缺失类别。
3. 不要求出现排名翻转；同序模型也可能有不同错误结构。负面发现也能成立，不必要求模型明显超过所有算法。
4. 同 provider 三模型结论只限于其实际范围。已经声明不是通用排行榜，无须再机械增加模型数量来“过关”。

## 6. 值得保留的题级诊断：五个 Color 弃答

这五个端点都是 Yellow，预测器均输出 `no-color-region`，即没有颜色连通域通过冻结筛选规则。本轮逐张查看了原始 PNG，物体实际存在，颜色较浅；**程序无有效投票区域不等于图片无物体，也不等于人类无法判断。** 尚不能把具体根因完全归到一个阈值，需进一步记录每级筛选后的像素/连通域数量。

| Parent task | Arm | Source | 机器输出 |
|---|---|---|---|
| `ld2-omr-42061-color-2` | B | omr-42061 | abstained / no-color-region |
| `ld2-omr-42020-color-2` | B | omr-42020 | abstained / no-color-region |
| `ld2-10156-color-2` | B | 10156 | abstained / no-color-region |
| `ld2-omr-21309-color-1` | A | omr-21309 | abstained / no-color-region |
| `ld2-10001-color-1` | A | 10001 | abstained / no-color-region |

对应 observation IDs 和支持像素数已经保存在 `single-image-color-baseline.json`，不是缺少失败记录。建议补充一个按语义颜色/来源分组的小结，以及算法内部的筛选诊断；不要看完这五个失败后偷偷重调主基线阈值。如果做后验修订算法，作为单独的探索性 baseline v2 报告。

这项工作是 MINOR 级解释改进，不是追加一条致命问题。

## 7. 论文与 benchmark 的一致性检查

### 7.1 版本用词可更明确

补充 §1 明确“v4-draft 对封存 display-v3 输入增加审计”，这条边界是对的。但主文 §4.2 中“Both Part-type arms receive new …”容易让新读者误解为此次 v4 又重渲。建议注明这些变化发生于 display-v3，相对更早版本而言；本轮 v4 保留其字节。

### 7.2 当前 publication 路径仍是协议/审计草稿生成器

`v4-draft/publication.py:31–35,60–71` 保留 v3 表并加入新 Color 宏，`verify_publication.py` 仍验证 protocol-ready 状态。这并非已有错误模型结果，而是一个明确的尚待完成的 empirical publication 分支。

最终应从经过验证的 analysis artifact 生成模型表，并保留对原协议稿的隔离。不要直接改 Excel 式汇总数字或删除 hash/QA 检查。此项并入 M1，不重复扣分。

### 7.3 复现有所改善，但完整独立重建未认证

新 `publication.py:20–30` 已读取当前目录的 `base-references.bib` 与 `additions.bib`，使用当前 `inputs/given-order-replay.pdf`，没有自读输出 bib；幂等检查也存在。此前关于这两项输入依赖的建议已部分落实。

但 generator 与 audit 仍明确依赖封存 v3 的数据/辅助函数。当前 draft 不是独立全包；完整干净环境恢复与公开发布路径本轮未测试，不宣称失败，也不宣称全部通过。只需按最后交付阶段完成依赖闭合，不要求捆绑 venv 或 node_modules。

### 7.4 版面

主文8页与补充8页均已逐页检查。公式与表格可读，没有看到明显遮挡或空白正文页；补充第8页内容只占左栏，属于紧凑度可优化项，不是科学缺陷。Figure 1 仍裁掉远端被交换候选，图注明示此事；加全图 inset 有帮助，但不是模型缺输入的证据。

## 8. 推荐与验收边界

### 当前为什么仍是 Borderline

本版相比 v3 的确更接近可提交的测量论文，但主要完成的是定位与审计层。能够支撑最终结论的 QA 子集同口径分析和 Part-type 对照范围还没有最终合上；只因为完成更多测试就升为 Weak Accept，会把工程完成度误当学术贡献。

### 什么会使我转向 Weak Accept

- full/QA 子集的模型与基线同题同权重，差异有正确解释；
- Part-type 明确选择窄主张，或用有效保持性对照支撑更强主张；
- 真实结果给出一个与近邻相比确有用途的诊断发现；
- 科学结论不被接口失败、选择性排除或跨来源偏差替代。

不要求：模型超过 BFS 的100%、Color 超过96.58%、Part-type 超过某个 oracle 数字、R_old 大于 NewAcc、必须排名反转。上述都不是合理的录用门槛。

### 下一步优先级

1. 在已有 `PHASE_2_ROUTE_DECISION.md` 上确定 A/B，不再新增另一份大规划。
2. 完成 Phase 3A/3B：QA 子集先验及新 Color 基线同口径重算和反例测试。
3. 依原有冻结运行合同接入真实结果，建立独立 empirical publication 路径。
4. 围绕真实诊断发现改主结果节，再做最后一轮科学性审查。

## 9. 本轮核验记录

### 实际执行

- 完整读取主文、补充源码，查看当前主文8页与补充8页。
- 读取新版 predictor、measurement audit、analyze helper、baseline import 边界、publication、验证脚本和阶段记录。
- 以只读方式执行全量 measurement audit 验证：347个视觉、219个图观察及其关联检查全部通过；仅将最终验证报告的写文件动作替换为标准输出，未修改任何验证断言或作者产物。
- 只读重跑146个Color预测，全部与冻结结果一致，原JSON hash不变。
- 从146条端点记录独立计算单图正确率、从73对记录独立计算Both；检查全部5个弃答PNG。
- 复核67个Part-type parent 的201个候选交换及192个不同类型代理计数。
- 复跑 v4-draft 新增 **11项测试：全部通过，2.050秒**。
- 在独立进程复跑继承的 v3 **27项测试：全部通过，4.576秒**。

复跑命令以项目根目录为起点：

```bash
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python -B \
  -m unittest discover -s benchmark/suite/ldraw-evidence-v4-draft -p 'test*.py' -v

env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python -B \
  -m unittest discover -s benchmark/suite/ldraw-evidence-v3 -p 'test*.py' -v
```

### 没有声称完成的工作

- 未调用任何付费模型接口，未构造真实模型排名或输出。
- 未充当347条视觉观察的两位独立真人评审者。
- 未把201个结构候选认定为已通过视觉人审。
- 未实施保持答案控制，未修改作者论文、数据、代码或冻结结果。
- 未执行干净环境的完整资产重建，也未重新穷尽性检索全领域文献。

**最终判断：本轮没有新的致命捷径；需要完成的是已有两项关键闭环，而不是重新推翻 benchmark。**
