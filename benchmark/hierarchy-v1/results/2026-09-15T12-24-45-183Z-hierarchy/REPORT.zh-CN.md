# Hierarchy-1 低成本流程试跑

- 状态：superseded
- 错误：无
- 固定样本：16 题（每个难度 × 任务层一个）
- 请求：16
- 本轮费用：$0.012887
- 累计费用：$3.772978 / $4.50

| 模型 | 完成 | Exact Success |
|---|---:|---:|
| openai/gpt-4.1-mini | 16 | 11 |

| 难度 | 任务层 | 样本 | Exact Success |
|---|---|---:|---:|
| D1 | atomic | 1 | 1 |
| D1 | metacognitive | 1 | 1 |
| D1 | procedural | 1 | 1 |
| D1 | integrative | 1 | 1 |
| D2 | atomic | 1 | 1 |
| D2 | metacognitive | 1 | 0 |
| D2 | procedural | 1 | 0 |
| D2 | integrative | 1 | 1 |
| D3 | atomic | 1 | 1 |
| D3 | metacognitive | 1 | 0 |
| D3 | procedural | 1 | 0 |
| D3 | integrative | 1 | 1 |
| D4 | atomic | 1 | 1 |
| D4 | metacognitive | 1 | 1 |
| D4 | procedural | 1 | 0 |
| D4 | integrative | 1 | 1 |

这是流程与可视化管线检查，不是模型排名。每个单模型单元格只有 1 题。

- 淘汰原因：操作题旧评分器只接受唯一线性顺序；最终协议改为接受所有依赖合法的拓扑顺序。
- 替代 run：2026-09-15T12-28-48-667Z-hierarchy
