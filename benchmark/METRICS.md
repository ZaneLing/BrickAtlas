# Metrics 与代码索引

## 当前复杂修复：visual-repair-v1

语义评分器：[evaluate.py](visual-repair-v1/evaluate.py)；
收据检查、条件汇总与分组分析：[study.py](visual-repair-v1/study.py)。

| Metric | 定义 |
|---|---|
| `repair_exact` | 绑定终端、全部最优恢复集合、最小成本、预算判定及每个最优解的分量均正确 |
| `binding_accuracy` | 当前图像匹配候选的图 ID 正确 |
| `changing_both_correct` | 视觉改变前后均完整正确 |
| `preserving_both_correct` | 无关视觉改变前后均完整正确；仅回答相同不算成功 |
| `structural_both_correct` | 同一图像下两种故障状态均完整正确 |
| `factorial_all_correct` | 同一重编号下 2×3 的全部六个格子正确 |
| `repair_given_binding` | 在绑定正确的观察中完整修复正确；无合格观察时未定义 |
| `invalid_rate` / `missing_rate` | 非法响应与未收到响应，均保留在预定分母 |

输出中的集合和解列表不依赖顺序，但遗漏等价最优解、增加非最优解或重复 ID 会失败。
原子绑定、无图像、oracle 绑定和多模态条件单独报告。
先在依赖组内平均，再作等组平均；同时报告 micro、实际组数、组重采样敏感性和
逐组剔除结果。重复渲染、共享 anchor 和重编号不会增加独立组数。
当前有限来源组不足以满足文中 25 组的粗略精度目标，不声称总体泛化。

跨条件分析按同一任务、故障/视觉格子和重编号对齐，令 `A` 为原子绑定正确、
`O` 为 oracle 完整修复正确、`M` 为多模态完整修复正确、`B` 为多模态绑定正确：

| 联合或配对指标 | 定义 |
|---|---|
| 八格联合计数 | 保留 `(A,O,M)` 的全部八种二元组合，不能用边缘正确率乘积代替 |
| 联合条件失败率 J | `sum(A*O*(1-M)) / sum(A*O)`；同时报告分子、合格观察数与组数 |
| 修复配对差值 | 同题 `M-O` 的 micro 与等组均值 |
| 绑定配对差值 | 同题 `B-A` 的 micro 与等组均值 |

J 的等组均值只平均存在 `A=O=1` 观察的组，零合格组单独计数；
整体无合格观察时结果为 `null`。这是一项行为诊断，不证明内部因果机制。
条件必须来自兼容的模型修订、适配器、设置、预定任务及资格审核锁。
已计划但缺失/非法的响应按错误保留；未计划的条件不能凭空补成一次测量。
重采样共同依赖组，完整保留各条件、共享图像和重编号。

完整集与人审合格集分别输出。资格筛选以整个构造为单位，所有条件共同应用，
区分待审和拒绝，不用筛选后的结果覆盖完整分母。详细字段与执行命令见
[当前版本说明](visual-repair-v1/README.md)。

## 历史原子视觉指标

历史评分实现：[analyze.py](suite/ldraw-evidence-v3/analyze.py)；
统计实现：[estimates.py](suite/ldraw-evidence-v3/estimates.py)。
Color、Part-type、文本图分别报告，不合成总榜单分数。

令每对预测为 `p_A, p_B`，答案为 `y_A != y_B`，共有预先冻结的 N 对。
缺失、超时、拒答和无效格式在固定分母中保留为错误。

| 论文名 | 代码 key | 定义 |
|---|---|---|
| A accuracy | `A_acc` | A 端正确比例 |
| New accuracy | `NewAcc` | B 端回答新 gold 的比例 |
| Both | `Both` | A、B 同时正确的比例；主要成对指标 |
| Old-gold retention | `old_gold_retention` | B 为有效格式且仍选择 A gold 的比例 |
| Other wrong | `other_wrong` | B 有效，但既非新 gold 也非旧 gold |
| Invalid B | `invalid_B` | B 无有效选项的比例 |
| Valid A / B / both | `valid_A`, `valid_B`, `valid_both` | 单端/双端格式有效率 |
| Conditional adaptation | `conditional_adaptation` | 在 A 正确的 pair 中，B 也正确的比例 |
| Conditional retention | `conditional_old_retention` | 在 A 正确的 pair 中，B 保留旧 gold 的比例 |

`NewAcc + old_gold_retention + other_wrong + invalid_B = 1`。
微平均条件适应率等于 `Both / A_acc`；分母为零时为 `null`。
source-macro 条件率先在各来源内部计算，再对有合格 pair 的来源平均，
不能用两个宏平均值相除代替。

## 汇总及诊断

| 项目 | 实现 | 报告方式 |
|---|---|---|
| 微平均与等来源平均 | [estimate](suite/ldraw-evidence-v3/estimates.py) | 主要报告等来源平均，同时给 pair/source 分母 |
| 95% 区间 | 同上 | 10,000 次 whole-source bootstrap，seed 20260920 |
| full / QA 子集差异 | `family_report`、`selection_shift` | 完整集与双端可答子集同时报告，共享来源重采样 |
| 模型配对差异与排名 | `comparisons`、`exact_macro`、`ranks` | 同题比较；精确有理数排名、并列中秩、区间 |
| 作者依赖 | [authors.py](suite/ldraw-evidence-v3/authors.py) | 等作者均值、作者重采样、逐作者剔除 |
| 图指标 | `graph_report` | 各分区的对称端点准确率、Both、valid-both |
| 位置面板 | `auxiliary` | 面板准确率、格式率及相对 label-A 的差值 |
| 图像依赖 | `image_minus_no_image` | 相同消息去图后的逐对分数差 |
| 人审一致性 | [qa.py](suite/ldraw-evidence-v3/qa.py) | 原始判断、选项、结构检查一致性和 kappa |

位置面板同时改变布局、可见性及编号界面，其差值不能解释为纯 OCR 因果效应。
旧答案保留只是输出行为，不证明模型记忆或内部机制。
来源区间不测量跨次 API 波动；跨重复运行的统计需在新研究中另行冻结。

## 确定性基线

- [priors.py](suite/ldraw-evidence-v3/priors.py)：固定选项、数字标签及 13 个 oracle-A 规则。Oracle-A 规则得到 A gold，有些还得到来源几何，不能当作合法单图像模型。
- [single_image_baselines.py](suite/ldraw-evidence-v4-draft/single_image_baselines.py)：仅使用当前 PNG 和文本的颜色基线。
- [graph_audit.py](suite/ldraw-evidence-v3/graph_audit.py)：文本图的组件调用边界；算法定义与分区审计见 [v2 graph_audit.py](suite/ldraw-evidence-v2/graph_audit.py)。
- [measurement_audit.py](suite/ldraw-evidence-v4-draft/measurement_audit.py)：逐观察显示、像素、图输入和去图一致性审计。

## 实验和历史指标

当前论文的模型与待填结果定义在 [paper/experiments.json](../paper/experiments.json)。
该文件的结果值全部为 `null`，生成 LaTeX 时输出真正的空白。
旧三模型 scorer 的 roster gate 仍有效。当前修复版本有可执行本地算法研究，
15 个模型是待锁定的实验计划，正式接入须固定实际修订、适配器和输入策略。

早期任务的 Part/Edge F1、装配成功等指标位于
[suite/METRICS.md](suite/METRICS.md)、[suite/v2/METRICS.md](suite/v2/METRICS.md)
及 [core/world.ts](core/world.ts)。这些指标属于不同任务，不用于替代当前的 Both。
