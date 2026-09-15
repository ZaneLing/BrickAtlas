# BrickAtlas Hierarchy-1 分层基准报告

## 设计结论

Mechanism-1 被保留为 D3 机构级，不再承担全部难度。Hierarchy-1 在其上下补充部件级、装配体级和系统级原创对象。
难度不是只按零件数划分，还同时考虑模块数、运动关节、依赖深度、隐藏接口、耦合约束和操作步长。

## 数据规模

- 原创对象：18
- 可视零件：1773
- 核心题：90
- D3 Mechanism-1 扩展题：48
- 总问题数：138
- 每个对象：2 道原子单选 + 1 道元认知/物理题 + 1 道操作题 + 1 道综合题

## 难度层级

| 难度 | 对象数 | 核心题 | 定义 |
|---|---:|---:|---|
| D1 部件级 | 4 | 20 | 单一接口、局部状态变化和短依赖链。 |
| D2 装配体级 | 4 | 20 | 多个子装配、一个主要机构和局部遮挡。 |
| D3 机构级 | 6 | 30 | 完整多关节对象，包含维修可达、动力学与隐藏故障。 |
| D4 系统级 | 4 | 20 | 跨工位耦合、共享资源、长操作链和跨区域故障。 |

## 四级原创积木库

| 难度 | 对象 | 零件 | 模块 | 关节 | 复杂度指数 |
|---|---|---:|---:|---:|---:|
| D1 | 检修信号转臂 / Signal Switch Stand | 22 | 4 | 3 | 116 |
| D1 | 维修工具小车 / Maintenance Trolley | 21 | 5 | 4 | 136 |
| D1 | 铰接安全舱盖 / Hinged Safety Hatch | 28 | 3 | 2 | 107 |
| D1 | 阀门控制台 / Valve Control Stand | 25 | 3 | 2 | 96 |
| D2 | 仓储分流机 / Warehouse Sorter | 60 | 6 | 5 | 210 |
| D2 | 救援绞盘塔 / Rescue Winch Tower | 68 | 6 | 5 | 238 |
| D2 | 运河巡检艇 / Canal Inspection Skiff | 45 | 5 | 4 | 186 |
| D2 | 双轴太阳能跟踪阵列 / Solar Tracker Array | 66 | 6 | 5 | 238 |
| D3 | 轨道检修车 / Orbital Service Rover | 73 | 10 | 9 | 363 |
| D3 | 港口集装箱起重机 / Harbor Container Crane | 126 | 5 | 5 | 311 |
| D3 | 双叶运河开启桥 / Bascule Canal Gate | 142 | 6 | 7 | 342 |
| D3 | 自适应射电观测站 / Adaptive Radio Observatory | 92 | 4 | 3 | 244 |
| D3 | 山火救援倾转旋翼机 / Wildfire Tiltrotor | 43 | 6 | 5 | 239 |
| D3 | 极地科研站 / Polar Research Station | 66 | 5 | 4 | 237 |
| D4 | 轨道综合对接场 / Orbital Docking Yard | 233 | 11 | 10 | 578 |
| D4 | 洪水应急船闸系统 / Flood Response Lock | 214 | 11 | 10 | 527 |
| D4 | 自动化货运终端 / Automated Cargo Terminal | 231 | 13 | 12 | 608 |
| D4 | 月面样品精炼站 / Lunar Sample Refinery | 218 | 12 | 11 | 570 |

## 任务层与能力

| 任务层 | 题量 | 主要能力 |
|---|---:|---|
| 原子能力单选 | 36 | 识别、计数、颜色、位姿、连接、支撑、增删改换、局部修复 |
| 元认知与物理推理 | 18 | 前缀稳定、可达性、反事实、动力学、运动学、不确定性、信息增益、Pareto |
| 可执行操作题 | 18 | 装配、拆卸、编辑后验证、故障恢复、库存重规划、先检查后执行 |
| 综合复杂题 | 18 | 诊断 + 可达 + 维修 + 库存 + 风险 + 验证的联合决策 |

## 横向与纵向对照

- 四个难度都重复测量：模块识别、三维空间关系、局部改色和故障定位，形成纵向锚点。
- D3 额外加入支撑锚点和位姿纠正；18 道 coverage 原子题共同覆盖全部 18 种原子操作。
- 同一任务层的观察负担从 D1 单接口上升到 D4 跨工位、共享资源和 12–24 步操作链。
- 每个对象的操作题都在网页中展示编号 Oracle 动作轨迹；每个对象提供等轴、正、侧、俯四视图。

### 原子操作全集

module-identification、part-count、color-recognition、spatial-relation、joint-motion、connectivity、support-anchor、contact-count、recolor、add、remove、replace、pose-correction、fault-localization、next-step、inventory-check、subassembly-boundary、no-op-detection。

### 元认知/物理题族

prefix-stability、assembly-accessibility、support-counterfactual、dynamic-robustness、functional-kinematics、fault-diagnosis、active-inspection、uncertainty-calibration、multiobjective-tradeoff。

## 低成本流程试跑

- GPT-4.1 mini：13/16
- 未计分/已淘汰尝试：2 次；均保留 run、ledger 与 reconciliation 证据。

| 难度 | 任务层 | 样本 | 正确 |
|---|---|---:|---:|
| D1 | atomic | 1 | 1 |
| D1 | metacognitive | 1 | 1 |
| D1 | procedural | 1 | 1 |
| D1 | integrative | 1 | 1 |
| D2 | atomic | 1 | 1 |
| D2 | metacognitive | 1 | 0 |
| D2 | procedural | 1 | 1 |
| D2 | integrative | 1 | 1 |
| D3 | atomic | 1 | 1 |
| D3 | metacognitive | 1 | 0 |
| D3 | procedural | 1 | 1 |
| D3 | integrative | 1 | 1 |
| D4 | atomic | 1 | 1 |
| D4 | metacognitive | 1 | 1 |
| D4 | procedural | 1 | 0 |
| D4 | integrative | 1 | 1 |

该试跑只覆盖固定的 4×4 分层样本，用于验证请求、解析、评分、汇总和热力图链路，不用于模型排名。

## 科学边界

- 四个难度目前是工程定义的开发层级，尚未经过真人作答时间、通过率和 IRT 难度标定。
- D3 的物理任务有 Rapier 刚体、关节和 Shape Cast 证据；其他层的核心题同时包含符号约束与冻结响应表。
- 当前 18 个对象都是公开开发对象；正式论文仍需新增隐藏、来源隔离的确认集。
- 物理结果不是 LEGO 扣合力、ABS 形变、公差或机器人抓取实验的替代品。
