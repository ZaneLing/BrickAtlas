# Benchmark data 索引

## 当前主任务：visual-repair-v1

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
