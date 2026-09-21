# Benchmark data 索引

## 当前视觉数据：brickatlas-display-v3

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

## 版本与存放规则

- 新稿、图表和空实验表：`../paper/`。
- 可执行评测代码：`suite/`；输入数据与输出报告留在版本化 `ldraw-*` 目录。
- 历史论文、审稿、修改指导：`../tem/`，旧路径保留兼容链接。
- `hierarchy-*`、`mechanism-*` 等是早期独立实验，不混入 display-v3。
- 所有当前模型成绩仍待真实采集；`dry-runs`、fixtures、算法基线不是模型实测。

Git 同步当前输入、审核包、代码、图像和论文；本地恢复 tarball 的排除范围见
[tem/README.md](../tem/README.md)。完整旧版恢复校验需要这些本地压缩包。
