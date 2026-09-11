# 任务协议与初步指标

## 排行榜单位

实验条件由 model、mode、representation、task kind、split、frozen selection共同定义。
one-shot：一次请求、一次JSON提交；不提供后验修复机会。
validator-once：总共两次请求，中间一次仅语法/状态合法性反馈；不提供缺件位置、正确位姿或目标分数。
两者分别报告。旧CARE-mini是交互系统，与这两榜也不合并。
VLA、机器人和机械手不是本benchmark目标。符号题测LLM推理；图像题测MLLM视觉到结构能力。
多模态题输入级别明确为“图像 + 文字/目录”，不把符号真值换进去后仍叫视觉题。

## 统一结构评分

- 输出严格JSON，接受绝对坐标 parts 或可逆相对 nodes；先decode为统一结构再评测。
- 相对nodes的offset是父节点最小角到子节点最小角的全局轴偏移，turn是绝对yaw。
- 它是相对位置程序，**不是完整BrickNet连接器端口表示**；不能因存在parent就判为真正连接。
- 同型号、颜色、x/y/z和实际footprint构成精确匹配类。平方砖四向等价，长方砖180度等价。
- 通过多重集一一配对，任意ID/输出排列都能得同样的分数；重复砖不能赚额外分数。
- Part F1 = 2 * matched / (target pieces + submitted pieces)。
- BOM F1只比较型号/颜色计数，供诊断，不替代位姿评分。
- Edge F1比较匹配后节点间的连接以及交叠stud数量。当前只覆盖stud，不覆盖pin/hinge等。
- Occupancy IoU以名义砖体整数体素集合计算，忽略顶部stud的几何细节。
- exact要求所有目标实例匹配、没有多余实例，并且世界合法。格式或合法性失败不能通过exact。

## 八任务

| task | 输出 | 成功标准 | 细项 |
| --- | --- | --- | --- |
| parts | partId, color, studs | 全部字段正确 | fieldAccuracy |
| relations | connected, above, components | 全部字段正确 | fieldAccuracy |
| reconstruct | 完整结构 | exact | Part/BOM/Edge F1, occupancyIoU |
| generate | 任一完整结构 | 合法、占用体积一致、颜色在允许集 | constraintSuccess, occupancyIoU |
| complete | 完整结构 | exact | preservation + 几何分数 |
| edit | 完整结构 | exact | preservation + 几何分数 |
| plan | order数组 | 所有ID恰好一次且每步可执行 | legalPrefix, coverage |
| repair | structure与faultIds | exact并且定位F1=1 | restorationSuccess, localizationF1, falseAlarm |

parts/relations的valid表示类型/字段可用，不是物理验证。不能跨任务直接把valid平均解释为“物理能力”。
generate不使用参考Part F1为主分，替代铺砌只要满足体积和颜色约束就可通过。
这是受控体积条件生成，不使用CLIP冒充精确几何评测，也不声称已经测自由文本审美质量。

## 修改与规划

preservation为源模型中不该变化的零件在输出中仍精确存在的比例。
空的应保留集合定义为1，独立目标exact仍必须满足。
repair的错误ID指输入CURRENT里错放/错色/多余的实例；不要求输出沿用这些ID。
正常样本的faultIds必须为空；falseAlarm只在正常样本有意义，其他记null。
plan在指定方向从空场/完整模型开始逐步执行，遇到第一个非法动作停止prefix统计；
即使最终集合碰巧正确，也不能绕过非法中间步骤。
支持和装配都是数字几何约束，不评测承载强度、扣合力、重心或机械臂可达性。

## 失败、统计与成本

错误JSON、拒答、超长截断、目标错配是已完成请求中的失败。网络、授权和计费异常独立记error，
同时报告覆盖率，不在不足样本时暗示全套实验完成。
完整总成功必须对应同一冻结样本集；小样本比例加Wilson描述区间，但样本共享模板，
该区间不表示经过族级聚类校正，不支持SOTA/显著性结论。
缺失任务记N/A；不能把未测任务当0或1而形成貌似完整的总分。
费用来自OpenRouter usage.cost；tokens、latency、provider、generation ID均留存。
既有累计账本4.50美元为整个campaign上限，不是本命令每次重置4.50。

## 验证协议

所有样本都用oracle验证裁判；空输出和copy-input是低阶参考，不能视为训练模型。
测试涵盖替代合法生成、任意独立装配顺序、重复实例、非法结构、无故障误报及相对表示往返。
模型运行保存输入图像和输出原文。replay重新解析原文、生成同一题、复算指标与费用收据。
人工网页允许反复试答，仅用于开发练习；网页手工得分不进入模型主榜。
