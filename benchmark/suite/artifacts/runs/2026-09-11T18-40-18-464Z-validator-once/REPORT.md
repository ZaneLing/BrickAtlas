# BrickAtlas 多任务评测报告

## 运行与费用

- Run: 2026-09-11T18-40-18-464Z-validator-once
- 状态: complete; 无运行错误
- 协议: validator-once; 输入结构表示: absolute
- 已处理 32/32 例，64 次实际 OpenRouter 请求。
- 本次费用 $0.05218306；campaign 历史累计 $0.19531848，沿用 $4.50 上限。
- 2026-09-11T18:40:18.465Z -> 2026-09-11T18:43:10.962Z
- 错误JSON与错误答案算任务失败，网络/计费失败单列，不筛掉差结果。

## 数据范围

数据版本 brickatlas-multitask-1.0：552 个程序化结构样本，138 个去色/平移/yaw规范化几何组，
8 个结构族，4416 个绝对表示任务。颜色变体不是新结构组；相对表示不是新独立样本。
两类结构整个留出为test_ood。此次模型试验是冻结的小规模分层抽样，不是全数据评测。
没有人工设计资产被伪装为已认证规则砖模型；OMR只读盘点另见数据卡。

## 分任务结果

| 模型 | 任务 | n | 网络错误 | 成功率 | 95% Wilson描述区间 | 格式率 | 状态合法率 | 费用 |
| --- | --- | ---: | ---: | --- | --- | --- | --- | ---: |
| openai/gpt-4.1-mini | parts | 2 | 0 | 0.0% | 0.0% - 65.8% | 100.0% | 100.0% | $0.001901 |
| openai/gpt-4.1-mini | relations | 2 | 0 | 0.0% | 0.0% - 65.8% | 100.0% | 100.0% | $0.000837 |
| openai/gpt-4.1-mini | reconstruct | 2 | 0 | 50.0% | 9.5% - 90.5% | 100.0% | 100.0% | $0.003909 |
| openai/gpt-4.1-mini | generate | 2 | 0 | 0.0% | 0.0% - 65.8% | 100.0% | 0.0% | $0.004597 |
| openai/gpt-4.1-mini | complete | 2 | 0 | 100.0% | 34.2% - 100.0% | 100.0% | 100.0% | $0.005513 |
| openai/gpt-4.1-mini | edit | 2 | 0 | 100.0% | 34.2% - 100.0% | 100.0% | 100.0% | $0.001624 |
| openai/gpt-4.1-mini | plan | 2 | 0 | 100.0% | 34.2% - 100.0% | 100.0% | 100.0% | $0.001473 |
| openai/gpt-4.1-mini | repair | 2 | 0 | 50.0% | 9.5% - 90.5% | 100.0% | 100.0% | $0.003741 |
| google/gemini-2.5-flash | parts | 2 | 0 | 100.0% | 34.2% - 100.0% | 100.0% | 100.0% | $0.002087 |
| google/gemini-2.5-flash | relations | 2 | 0 | 100.0% | 34.2% - 100.0% | 100.0% | 100.0% | $0.001782 |
| google/gemini-2.5-flash | reconstruct | 2 | 0 | 50.0% | 9.5% - 90.5% | 100.0% | 100.0% | $0.004544 |
| google/gemini-2.5-flash | generate | 2 | 0 | 0.0% | 0.0% - 65.8% | 100.0% | 50.0% | $0.004420 |
| google/gemini-2.5-flash | complete | 2 | 0 | 100.0% | 34.2% - 100.0% | 100.0% | 100.0% | $0.006334 |
| google/gemini-2.5-flash | edit | 2 | 0 | 100.0% | 34.2% - 100.0% | 100.0% | 100.0% | $0.003207 |
| google/gemini-2.5-flash | plan | 2 | 0 | 100.0% | 34.2% - 100.0% | 100.0% | 100.0% | $0.002392 |
| google/gemini-2.5-flash | repair | 2 | 0 | 50.0% | 9.5% - 90.5% | 100.0% | 100.0% | $0.003822 |

宏平均仅用于同协议、同输入信息和同样本集合的描述，不合并one-shot与validator-once。
样本共享生成模板且每单元很少，区间不构成显著性或模型能力排名结论。

## 逐例与细项

| 模型 | taskId | family / split | 成功 | 指标 | 问题 |
| --- | --- | --- | --- | --- | --- |
| openai/gpt-4.1-mini | d751edac4dbbb2c674e7397c | platform / test_id | 0 | format=1.000; valid=1.000; success=0.000; fieldAccuracy=0.667 | answer_mismatch |
| openai/gpt-4.1-mini | 8405791930190e2dcf13c5f1 | staircase / test_ood | 0 | format=1.000; valid=1.000; success=0.000; fieldAccuracy=0.667 | answer_mismatch |
| openai/gpt-4.1-mini | bb84c76aa90de82fa59f1488 | tower / test_id | 0 | format=1.000; valid=1.000; success=0.000; fieldAccuracy=0.667 | answer_mismatch |
| openai/gpt-4.1-mini | b3aa9894ff79739181e6a57b | staircase / test_ood | 0 | format=1.000; valid=1.000; success=0.000; fieldAccuracy=0.667 | answer_mismatch |
| openai/gpt-4.1-mini | 56e6c3d5b38841d6c1373195 | bridge / test_id | 0 | format=1.000; valid=1.000; success=0.000; partF1=0.333; bomF1=1.000; edgeF1=0.000; occupancyIoU=0.600 | target_mismatch |
| openai/gpt-4.1-mini | f578c0bfd98b93ce88d3e93e | staircase / test_ood | 1 | format=1.000; valid=1.000; success=1.000; partF1=1.000; bomF1=1.000; edgeF1=1.000; occupancyIoU=1.000 |  |
| openai/gpt-4.1-mini | 28e1dee957b301c2a9f0f4a1 | bench / test_id | 0 | format=1.000; valid=0.000; success=0.000; occupancyIoU=0.600; constraintSuccess=0.000 | overlap, unsupported |
| openai/gpt-4.1-mini | a4f5d824f9c7b2633fcc0af4 | gate / test_ood | 0 | format=1.000; valid=0.000; success=0.000; occupancyIoU=0.222; constraintSuccess=0.000 | overlap, unsupported |
| openai/gpt-4.1-mini | 9b6ac0346f252ef6a4d16a9e | bench / test_id | 1 | format=1.000; valid=1.000; success=1.000; partF1=1.000; bomF1=1.000; edgeF1=1.000; occupancyIoU=1.000; preservation=1.000 |  |
| openai/gpt-4.1-mini | 3b45dd848f6edaaeb1db8851 | staircase / test_ood | 1 | format=1.000; valid=1.000; success=1.000; partF1=1.000; bomF1=1.000; edgeF1=1.000; occupancyIoU=1.000; preservation=1.000 |  |
| openai/gpt-4.1-mini | 6163943e35f5fa7de23004ce | tower / test_id | 1 | format=1.000; valid=1.000; success=1.000; partF1=1.000; bomF1=1.000; edgeF1=1.000; occupancyIoU=1.000; preservation=1.000 |  |
| openai/gpt-4.1-mini | d38c594ff2a8d49e315fbb32 | staircase / test_ood | 1 | format=1.000; valid=1.000; success=1.000; partF1=1.000; bomF1=1.000; edgeF1=1.000; occupancyIoU=1.000; preservation=1.000 |  |
| openai/gpt-4.1-mini | ccd0cf9531742fa70b099df5 | bridge / test_id | 1 | format=1.000; valid=1.000; success=1.000; legalPrefix=1.000; coverage=1.000 |  |
| openai/gpt-4.1-mini | c55f88c6ffa44cf8ec9d244d | staircase / test_ood | 1 | format=1.000; valid=1.000; success=1.000; legalPrefix=1.000; coverage=1.000 |  |
| openai/gpt-4.1-mini | 1b33a3c2d64930b5da657a5d | wall / test_id | 1 | format=1.000; valid=1.000; success=1.000; partF1=1.000; bomF1=1.000; edgeF1=1.000; occupancyIoU=1.000; preservation=1.000; localizationF1=1.000; restorationSuccess=1.000; falseAlarm=N/A |  |
| openai/gpt-4.1-mini | 31d572b415a044ecd5b889b5 | gate / test_ood | 0 | format=1.000; valid=1.000; success=0.000; partF1=0.889; bomF1=0.889; edgeF1=0.800; occupancyIoU=0.923; preservation=1.000; localizationF1=1.000; restorationSuccess=0.000; falseAlarm=N/A | target_mismatch |
| google/gemini-2.5-flash | d751edac4dbbb2c674e7397c | platform / test_id | 1 | format=1.000; valid=1.000; success=1.000; fieldAccuracy=1.000 |  |
| google/gemini-2.5-flash | 8405791930190e2dcf13c5f1 | staircase / test_ood | 1 | format=1.000; valid=1.000; success=1.000; fieldAccuracy=1.000 |  |
| google/gemini-2.5-flash | bb84c76aa90de82fa59f1488 | tower / test_id | 1 | format=1.000; valid=1.000; success=1.000; fieldAccuracy=1.000 |  |
| google/gemini-2.5-flash | b3aa9894ff79739181e6a57b | staircase / test_ood | 1 | format=1.000; valid=1.000; success=1.000; fieldAccuracy=1.000 |  |
| google/gemini-2.5-flash | 56e6c3d5b38841d6c1373195 | bridge / test_id | 0 | format=1.000; valid=1.000; success=0.000; partF1=0.333; bomF1=1.000; edgeF1=0.000; occupancyIoU=0.600 | target_mismatch |
| google/gemini-2.5-flash | f578c0bfd98b93ce88d3e93e | staircase / test_ood | 1 | format=1.000; valid=1.000; success=1.000; partF1=1.000; bomF1=1.000; edgeF1=1.000; occupancyIoU=1.000 |  |
| google/gemini-2.5-flash | 28e1dee957b301c2a9f0f4a1 | bench / test_id | 0 | format=1.000; valid=0.000; success=0.000; occupancyIoU=0.321; constraintSuccess=0.000 | overlap |
| google/gemini-2.5-flash | a4f5d824f9c7b2633fcc0af4 | gate / test_ood | 0 | format=1.000; valid=1.000; success=0.000; occupancyIoU=0.250; constraintSuccess=0.000 | target_mismatch |
| google/gemini-2.5-flash | 9b6ac0346f252ef6a4d16a9e | bench / test_id | 1 | format=1.000; valid=1.000; success=1.000; partF1=1.000; bomF1=1.000; edgeF1=1.000; occupancyIoU=1.000; preservation=1.000 |  |
| google/gemini-2.5-flash | 3b45dd848f6edaaeb1db8851 | staircase / test_ood | 1 | format=1.000; valid=1.000; success=1.000; partF1=1.000; bomF1=1.000; edgeF1=1.000; occupancyIoU=1.000; preservation=1.000 |  |
| google/gemini-2.5-flash | 6163943e35f5fa7de23004ce | tower / test_id | 1 | format=1.000; valid=1.000; success=1.000; partF1=1.000; bomF1=1.000; edgeF1=1.000; occupancyIoU=1.000; preservation=1.000 |  |
| google/gemini-2.5-flash | d38c594ff2a8d49e315fbb32 | staircase / test_ood | 1 | format=1.000; valid=1.000; success=1.000; partF1=1.000; bomF1=1.000; edgeF1=1.000; occupancyIoU=1.000; preservation=1.000 |  |
| google/gemini-2.5-flash | ccd0cf9531742fa70b099df5 | bridge / test_id | 1 | format=1.000; valid=1.000; success=1.000; legalPrefix=1.000; coverage=1.000 |  |
| google/gemini-2.5-flash | c55f88c6ffa44cf8ec9d244d | staircase / test_ood | 1 | format=1.000; valid=1.000; success=1.000; legalPrefix=1.000; coverage=1.000 |  |
| google/gemini-2.5-flash | 1b33a3c2d64930b5da657a5d | wall / test_id | 0 | format=1.000; valid=1.000; success=0.000; partF1=1.000; bomF1=1.000; edgeF1=1.000; occupancyIoU=1.000; preservation=1.000; localizationF1=0.000; restorationSuccess=1.000; falseAlarm=N/A | target_mismatch |
| google/gemini-2.5-flash | 31d572b415a044ecd5b889b5 | gate / test_ood | 1 | format=1.000; valid=1.000; success=1.000; partF1=1.000; bomF1=1.000; edgeF1=1.000; occupancyIoU=1.000; preservation=1.000; localizationF1=1.000; restorationSuccess=1.000; falseAlarm=N/A |  |

## 指标解释与不可测范围

- parts/relations: 类型正确的字段准确率，全部字段正确才成功。
- 重建/补全/编辑: 颜色、型号和对称足迹的最优精确多重集匹配；额外零件扣分；状态还须合法。
- Edge F1包括连接节点与实际对接stud数量；不是仅对BOM评分。
- 生成: 当前是受控文字+体积约束；任何合法的目录零件铺砌均可，比较占用IoU及允许颜色，不要求参考拆砖方式。
- 补全/编辑/修复: 独立报告非目标部分保持率。编辑覆盖改色、顶部复制增件、局部删件，尚非任意语义几何改造。
- 修复: 目标复原与故障定位都正确才成功，正常无故障样本报告误报；不是在线机械故障恢复。
- 规划: 检查任一完整顺序的逐步支撑、碰撞与垂直通道，不按唯一作者序列打分。
- 输入图像包含明确披露的逐层视图，不能称为单视图隐藏结构推断；relations/plan等结构任务是符号输入。
- 状态合法不等于承重稳定；不含机械手、机器人、VLA、力学扣合、非网格关节与连续运动。
- Oracle全量通过是裁判自测，不能拿来当学习模型分数。未进行神经网络微调，训练导出不是训练完成。

## 可复现证据

- Dataset hash: a3c18d9a99da4fb20880c7e7ee1f1dc22a83cf18e8421a7d9db08bb8a6a6e3da
- Protocol hash: 35b1aa6e70f890ab94cec9a4cfb44b26c04a58e89cf7d0126ea799c38cd6ec36
- Frozen selection hash: 797edec16f53c5bca7966c1125c6f412f8323bda5e304ce6cf4824b2809825ad
- run.json: 输入、原始响应、解析答案、分数、每次generation ID/provider/tokens/cost。
- protocol.json: 请求前冻结的选择与提示词。
- ledger.json: campaign账本快照；frames/: 模型实际看到的PNG。
- 运行 suite:replay 会重新构造任务、解析原始响应、核对图片、计费收据与评分。

## 下一步

先根据分任务失败定位视觉识别、表示解码、关系推理和规划差异，再扩大held-out组数。
研究级发布仍需更广的有许可人工模型、完整连接器、语义生成评价、人工标签审计以及训练对照。
不要从本次小规模工程实验宣称超过BrickNet、BrickGPT或其他已发表基准。
