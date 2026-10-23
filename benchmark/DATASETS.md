# Benchmark data 索引

## 拼装与修复扩展：expansion-v7（2026-10-23）

按用户确认范围，扩展当前新增693道物理任务：静态359、动态334；与保留原题5,100道合计5,793道。扩展保存776条运行条件，83条是旧题的新接口条件，不重复计数。原D的160道及扩展22条H12条件已排除，旧记录保留追溯。同物件题目彼此相关，不能把总题数当独立来源数。

5 个长流程原创物件需操作 21–32 块；原社区物件补充更多错误与较长模块，另收录 10013／10015／10016 三个新 OMR 来源。47 条条件包含分时发生的两次／三次事件。统一来源分组包含 152 组，同来源不跨集合；公开新来源只表示未参与本项目模型调试，不保证预训练未见过。

当前776条扩展条件是此前独立物理重放通过的798条中的保留子集，状态和GT未修改。717次保留参考事件中，688次达到图像差异门槛，29次单列低可见诊断。难度仍为结构描述，没有新增真人／模型成绩。只做H01–H11、H13；H12及H14–H17不做，H18待定。[范围与库存核查](../deliverables/brickplan-expansion-v7/HUMAN-ERROR-SCOPE.zh-CN.md)。

[报告](../deliverables/brickplan-expansion-v7/README.zh-CN.md) · [全量配图清单](../deliverables/brickplan-expansion-v7/MODEL-CASE-CATALOG.zh-CN.md) · [网上人类错误研究](../deliverables/brickplan-expansion-v7/human-error-research/README.zh-CN.md) · [统一来源分组](../deliverables/brickplan-expansion-v7/global-splits.json) · [生成、运行与验证代码](brickplan-repair/expansion_v7/)。

## 当前规划任务：BrickPlan 2.3

从冻结的 100 个新增 OMR 套装候选中执行来源准入，并保留全部排除记录。
实际任务、题目、独立来源和留出来源规模见[公开目录](brickplan-v2.3/release/catalogue.json)。
七类题面覆盖装配、有限资源、检修历史、下一步选择、未来序列、
视觉几何/外观对照及延迟恢复。D1–D4 仅表示最优操作长度。
校准题与区分性题目分开评分，诊断题按独立题目定义和来源聚合。
主评估几何配对严格匹配零件总数、型号与颜色库存，要求两侧首次非法操作位置
都正确；历史不等数量对照单独保留。来源、干预与起始状态不混作独立样本。

| 数据与入口 | 路径 |
|---|---|
| 分类体验页面、启动与验证 | [README](brickplan-v2.3/README.md) |
| 官方 CVPR 格式论文 | [正文](brickplan-v2.3/paper.pdf) · [补充材料](brickplan-v2.3/supplement.pdf) |
| 公共题目表及完整运行包 | [JSONL](brickplan-v2.3/release/questions.jsonl) · [ZIP](brickplan-v2.3/release/brickplan-v2.3-release.zip) |
| 数据卡、Dataset/Space/静态站发布 | [DATASET-CARD](brickplan-v2.3/DATASET-CARD.md) |
| 历史真实模型逐步反馈 | [接入说明](brickplan-v2.3/MODEL-INTEGRATION.md) · [完整实录](brickplan-v2.3/cases/local-vlm.json) |
| 构造有效性、来源与范围 | [VALIDITY](brickplan-v2.3/VALIDITY.md) |
| 全量来源题目审计与捷径对照 | [来源审计](brickplan-v2.3/data/source-question-audit.json) · [对照结果](brickplan-v2.3/data/matched-controls.json) |

入口为 `http://127.0.0.1:8783/`，真实模型案例为 `/#case`。
SmolVLM 的四次真实调用均出现格式失败，2.1 原始任务和输出完整保留；它不代表新版或总体模型成绩。
发布目录已准备，尚未上传公开平台。冻结的旧 BrickPlan 版本独立保留。
[BrickPlan 2.2](brickplan-v2.2/README.md) 保留原来的 377 个交互任务、
1,952 道诊断题、188 对题目与 16 个来源组，文件不变。

## 独立视觉修复任务：visual-repair-v1

视觉绑定与组合修复：真实参考图决定第三个图终端，给定的连接图和故障状态
决定全部最小修复集合。构造内有视觉变化/保持、故障变化与重编号重复，
不能将这些观察当成独立来源。

| 数据 | 路径 |
|---|---|
| 使用与复现 | [README.md](visual-repair-v1/README.md) |
| 公共索引与条件输入 | [public.json](visual-repair-v1/public.json) · [native/](visual-repair-v1/native/) |
| GT 与独立语义核验 | [gold.json](visual-repair-v1/gold.json) · [dependency-audit.json](visual-repair-v1/dependency-audit.json) |
| 候选、排除和划分台账 | [sampling-ledger.json](visual-repair-v1/sampling-ledger.json) |
| 实际规模与依赖组 | [summary.json](visual-repair-v1/summary.json) |
| 原生图片和源上下文 | [public assets](../public/benchmark/visual-repair-v1/) |
| 图像哈希与拍摄记录 | [captures.json](visual-repair-v1/captures.json) |
| 执行与结果协议 | [study-manifest.json](visual-repair-v1/study-manifest.json) |
| 本地确定性算法结果 | [baseline-report.json](visual-repair-v1/baseline-report.json) |

公共索引含分组元数据，**模型实际输入使用 native packet**，只包含声明允许的信息。
真实人审和模型结果仍未采集；算法结果不代表模型实验。
联合条件分析和人审合格子集共用构造身份及资格锁。完整集、合格集、待审和拒绝数量
分别保留；尚无人审时合格集为空，其估计保持 `null`。详见当前版本的
[资格审核与执行说明](visual-repair-v1/README.md)。

## 历史原子视觉数据：brickatlas-display-v3

| 数据 | 路径 | 用途 |
|---|---|---|
| 配对和 gold 总表 | [visual-manifest.json](ldraw-evidence-v3/visual-manifest.json) | 140 个 parent、140 对、280 个主要端点 |
| 观察索引 | [observation-index.json](ldraw-evidence-v3/observation-index.json) | 347 个观察的文件路径、图像哈希、角色 |
| 精确模型输入 | [observations/](ldraw-evidence-v3/observations/) | system/user 消息、选项及图像绑定 |
| PNG 与网页资产 | [public/benchmark/evidence-v3/](../public/benchmark/evidence-v3/) | 通过索引读取；部分图像继承 v2 |
| 显示编号与来源身份契约 | [identity-contract.json](ldraw-evidence-v3/identity-contract.json) | 区分源实例和当前图像编号 |
| 候选赋值与先验审计 | [part-type-assignment.json](ldraw-evidence-v3/part-type-assignment.json)、[answer-prior-audit.json](ldraw-evidence-v3/answer-prior-audit.json) | 选项平衡、受限规则测试 |
| 六人盲审材料 | [qa/initial/](ldraw-evidence-v3/qa/initial/) | 每个观察两次独立判断，真人反馈尚未收集 |
| 来源/作者依赖 | [source-dependence.json](ldraw-evidence-v3/source-dependence.json) | 24 来源、18 主作者组、17 贡献者连通组 |
| 逐观察机器审计 | [ldraw-evidence-v4-draft/](ldraw-evidence-v4-draft/) | 347 视觉 + 219 图观察；不是新数据版本 |

Color 有 73 对，Part-type（schema 中为 `shape-match`）有 67 对；
67 个位置面板是辅助观察，不能叠加为新 pair。Color 与 Part-type 不汇总成一个视觉分数。
题目中的 B0001 等编号按当前图像解析，来源文件中的稳定身份另外保存。

## 文本图与来源资源

| 数据 | 路径 | 数量及解释 |
|---|---|---|
| 假设图输入 | [inputs.json](ldraw-evidence-v1/matched-graphs-v1/inputs.json) | 73 parent × anchor/change/invariance = 219 独立观察 |
| 图分区 | [graph-partitions.json](ldraw-evidence-v2/graph-partitions.json) | 12 对 degree-matched、61 对 degree-visible；分别报告 invariance |
| 图算法审计 | [graph-audit.json](ldraw-evidence-v2/graph-audit.json) | BFS、union-find、degree、1-WL 等实际算法输出 |
| 原始来源目录 | [catalog.json](ldraw-v2/catalog.json)、[sources/](ldraw-v2/sources/) | 24 个 OMR/LDraw 模型、15,334 个实例 |
| 完整历史题档案 | [dossiers.json](../public/benchmark/evidence-v3/dossiers.json) | 617 道历史题，保留来源、操作和答案 |
| 继承关系及哈希 | [retained-components.json](ldraw-evidence-v3/retained-components.json) | 当前版本明确引用的旧版组件 |

图的 change/invariance 共用 anchor，不可将端点出现次数当作独立观察数。
来源 D1–D4 是模型规模带，不是已经验证的认知难度分层。
隔离视图和三维展开是检查方式，不能当作新的可独立站立装配。

## 复杂复合题示例：complex-examples-v1

[独立目录](complex-examples-v1/README.md) 包含三道新设计题：
CX1 多故障最小修复、CX2 自适应故障诊断、CX3 重复轴组件的对应与刚体位姿恢复。
输入分别来自真实 OMR 42004 的 36 顶点/44 边连接记录和 OMR 42061 的两套 12 零件轴组件。

[public.json](complex-examples-v1/public.json) 保存完整输入；
[gold.json](complex-examples-v1/gold.json) 保存可重算 GT；
[verification.json](complex-examples-v1/verification.json) 记录独立核验。
这些是尚未进行人审和模型采集的三个案例，**不增加 display-v3 的 140 对规模**。

## 版本与存放规则

- 新稿、图表和空实验表：`../paper/`。
- 当前复杂任务的构造、评分和运行：`visual-repair-v1/`；
  旧原子任务代码保留在 `suite/` 和版本化 `ldraw-*` 目录。
- 历史论文、审稿、修改指导：`../tem/`，旧路径保留兼容链接。
- `hierarchy-*`、`mechanism-*` 等是早期独立实验，不混入 display-v3。
- 所有当前模型成绩仍待真实采集；`dry-runs`、fixtures、算法基线不是模型实测。

Git 同步当前输入、审核包、代码、图像和论文；本地恢复 tarball 的排除范围见
[tem/README.md](../tem/README.md)。完整旧版恢复校验需要这些本地压缩包。
