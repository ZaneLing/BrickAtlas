# v2 非人工研究补强：实际进展报告

本报告只列当前有产物支持的结果。完整目标未因本轮进展被缩小。
总体文字说明见 [OVERVIEW.zh-CN.md](OVERVIEW.zh-CN.md)。

## 已完成的新证据

- 两API模型674次主实验，24个共同留出对象、8策略各3对象及25个已知目录题。
- 固定对照56次：无图、错配图、符号参考、重复、同首答反思/反馈、相对表示。
- 两个run共730次新增请求，新增费用$1.50635072，全部收据已结算、分数可复算。
- 15360个正确/扰动结构，138240项独立指标比对，没有差异。
- 10240道关系独立算法一致；高度规划器全10240道装拆通过。
- train-only检索覆盖2430个非训练对象的重建题，无测试对象检索进训练索引。
- 严格schema版本拒绝数组冒充字符串；全117910真值与118640条既有记录的指标保持不变，5120个畸形答案被拒绝。
- 337道测试题的Torch/MLX输入token、像素与mask哈希全部一致；840行训练/验证数据及480张PNG已打包并核对。
- 全107520项错误答案/等价性检查通过：规划缺步、重复、未知ID和反序，编辑无操作，修复误报，结构ID与等价旋转。
- 1177条训练/验证/测试输入共1970图像使用、626独立渲染，全部重新渲染后与原题图片一致。

高度规划全通过意味着当前竖直插拔域不需要复杂搜索；不能再用贪心失败作为该域很难的证据。
独立checker只验证名义网格，不代表任意CAD、力学或语义真值正确。

## 主实验

| 模型 / 任务 / 变体 | n | 成功 |
| --- | ---: | ---: |
| openai/gpt-4.1-mini / relations / contact | 24 | 7 |
| google/gemini-2.5-flash / relations / contact | 24 | 7 |
| openai/gpt-4.1-mini / relations / separated | 24 | 0 |
| google/gemini-2.5-flash / relations / separated | 24 | 0 |
| openai/gpt-4.1-mini / reconstruct / full | 24 | 0 |
| google/gemini-2.5-flash / reconstruct / full | 24 | 0 |
| openai/gpt-4.1-mini / generate / constraints | 24 | 0 |
| google/gemini-2.5-flash / generate / constraints | 24 | 0 |
| openai/gpt-4.1-mini / complete / suffix | 24 | 0 |
| google/gemini-2.5-flash / complete / suffix | 24 | 0 |
| openai/gpt-4.1-mini / edit / rotate | 24 | 0 |
| google/gemini-2.5-flash / edit / rotate | 24 | 0 |
| openai/gpt-4.1-mini / edit / recolor | 24 | 24 |
| google/gemini-2.5-flash / edit / recolor | 24 | 24 |
| openai/gpt-4.1-mini / edit / remove | 24 | 24 |
| google/gemini-2.5-flash / edit / remove | 24 | 24 |
| openai/gpt-4.1-mini / plan / assemble | 24 | 1 |
| google/gemini-2.5-flash / plan / assemble | 24 | 12 |
| openai/gpt-4.1-mini / plan / disassemble | 24 | 1 |
| google/gemini-2.5-flash / plan / disassemble | 24 | 7 |
| openai/gpt-4.1-mini / repair / none | 24 | 21 |
| google/gemini-2.5-flash / repair / none | 24 | 17 |
| openai/gpt-4.1-mini / repair / color | 24 | 4 |
| google/gemini-2.5-flash / repair / color | 24 | 6 |
| openai/gpt-4.1-mini / repair / shift | 24 | 0 |
| google/gemini-2.5-flash / repair / shift | 24 | 0 |
| openai/gpt-4.1-mini / parts / red | 5 | 1 |
| google/gemini-2.5-flash / parts / red | 5 | 4 |
| openai/gpt-4.1-mini / parts / blue | 4 | 1 |
| google/gemini-2.5-flash / parts / blue | 4 | 4 |
| openai/gpt-4.1-mini / parts / green | 4 | 2 |
| google/gemini-2.5-flash / parts / green | 4 | 0 |
| openai/gpt-4.1-mini / parts / yellow | 4 | 3 |
| google/gemini-2.5-flash / parts / yellow | 4 | 3 |
| openai/gpt-4.1-mini / parts / gray | 4 | 0 |
| google/gemini-2.5-flash / parts / gray | 4 | 0 |
| openai/gpt-4.1-mini / parts / white | 4 | 1 |
| google/gemini-2.5-flash / parts / white | 4 | 1 |

变体不能当独立对象。当前对象仅24个，不能宣称具有充分统计功效。
更完整的格式/几何/表面/定位指标、分母、延迟、tokens及截断数见artifacts/study/statistics.json。

## 固定对照

| 条件 | n | 原始成功 | 对照成功 | 增益 / 退化 |
| --- | ---: | ---: | ---: | --- |
| no-image | 8 | 0 | 0 | 0 / 0 |
| mismatched-images | 8 | 0 | 0 | 0 / 0 |
| symbolic-reference | 8 | 0 | 8 | 8 / 0 |
| reflection | 8 | 0 | 0 | 0 / 0 |
| validation | 8 | 0 | 0 | 0 / 0 |
| repeat | 8 | 0 | 0 | 0 / 0 |
| relative | 8 | 6 | 0 | 0 / 6 |

每策略选首个已冻结对象，不按分数筛选。符号参考是额外真值信息；相对表示不等于连接器程序。
全零成功造成地板效应，不能根据无图与正常图都0分断言模型没有利用图像。
跨任务相关性按24个对象计算，常量边际返回null，不强行编造相关系数或显著性。

## 多模态训练状态

固定SmolVLM-256M、真实四视图、96训练对象/24验证对象、七装配任务。
每优化步512个监督答案tokens；单任务/多任务/留编辑任务各三个seed。
所有条件的正式推理统一MLX、无量化、完整337题和2200-token输出上限。
PyTorch未完成的测速样本已归档，不作为训练/模型对照成绩。
输入一致性测试核对token、像素及mask；不同数值kernel仍可能改变输出。

| job | 状态 | 优化步 | 监督tokens | 测试预测 |
| --- | --- | ---: | ---: | ---: |
| base-seed17 | complete | 0/0 | 0 | 337/337 |
| single-seed17 | complete | 120/120 | 61440 | 337/337 |
| single-seed29 | complete | 120/120 | 61440 | 337/337 |
| single-seed43 | complete | 120/120 | 61440 | 337/337 |
| multi-seed17 | in-progress-or-interrupted | 61/120 | 31232 | 0/337 |
| multi-seed29 | pending | 0/120 | 0 | 0/337 |
| multi-seed43 | pending | 0/120 | 0 | 0/337 |
| leave-edit-seed17 | pending | 0/120 | 0 | 0/337 |
| leave-edit-seed29 | pending | 0/120 | 0 | 0/337 |
| leave-edit-seed43 | pending | 0/120 | 0 | 0/337 |

已完成并导入的训练run：4/10。未完成的run不计算训练收益。
匹配监督量和步数不代表相同输入/图像token、耗时或计算量。
验证NLL仅使用每任务固定两例，不代表全部168条验证样本。
840条训练/验证样本的题面token前缀与监督边界已逐条核对，最大完整序列5176。
337条测试oracle在SmolVLM tokenizer下最长1793 token，均未超过2200输出上限；
oracle仅用于离线长度诊断，没有附加到模型输入。
逐任务、变体、信息条件、split、seed的结果、配对变化及真实预算见local-statistics.json。

## 评分版本与复现

新提交的v2:score与网页评价默认采用v2-strict-schema-1；
score-legacy仅用于明确的历史复现。已有付费run不改写。
严格批量run同时保存缺答、原始坏答案、源码哈希与对象级统计；
replay按版本复算所有指标、所有分层与完整状态链。
旧解码器的类型转换漏洞曾真实存在，不因新增测试就声称历史软件绝对无错。

## 未完成目标

- 全部训练及对照输出完成前，不能报告多模态迁移结论。
- 目前仍缺充分规模多模型确认性实验、丰富真实外部结构和自由语义评价。
- 通用CAD连接/力学不在现有验证范围；需要新域协议，不能对网格结果外推。
- 独立人审按要求单列，当前没有完成的真实审核。
- 每环提供有范围的证据；不能承诺绝对无错或录用。
