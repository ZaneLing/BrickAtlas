# OpenRouter 多模型验证报告

## 执行与结论边界

- 固定主验证状态：complete；已返回 180/180 个响应；新增费用 $0.603614，该阶段结束累计 $2.560990。
- 4个模型共享3个验证对象（12/20/29件），每模型39个主任务、6个诊断任务。不是180个独立对象，也不是全量评测。
- 样本、模型、提示、JSON模式、2200输出token上限和每题1次提交在运行前冻结；模型顺序轮转，失败不重试、不修答、不按结果选样。
- 所有成绩按原响应重算并核对账单。无图和完整符号参考独立列出，不混入主榜。
- 尺寸和结构族混杂；此次不覆盖独立零件识别、OOD结构族、复杂连接或真实人类设计对象。
- 模型选择覆盖一个同家族大小对照、一个Google模型和一个开放权重VLM，不代表覆盖所有前沿模型。统一JSON输出模式也是Harness条件，不能称为完全无约束的原生能力。

## 综合判断

在13个任务变体中，有5个在同题上表现出模型差异，说明这个小样本已有局部区分信号。
同时有6个变体全零、2个全满。
这是一轮有用的诊断结果，但不是充分成熟的benchmark证据：任务分层不等于可靠模型排名，三个独立对象也无法证明总体难度曲线。
普通重建在精确成功上仍为地板，应先校准更低难度和局部指标，再扩大相同难度的调用量。
报告不把较大的型号预设为赢家，也不因为出现预期排序就宣称结果更好。

## 能力矩阵

| 任务/变体 | gpt-4.1-mini | gpt-4.1 | gemini-2.5-flash | qwen3-vl-32b-instruct | 样本内形态 |
| --- | ---: | ---: | ---: | ---: | --- |
| relations/contact | 3/3 | 1/3 | 2/3 | 0/3 | mixed |
| relations/separated | 0/3 | 0/3 | 0/3 | 0/3 | floor |
| reconstruct/full | 0/3 | 0/3 | 0/3 | 0/3 | floor |
| generate/constraints | 0/3 | 0/3 | 0/3 | 0/3 | floor |
| complete/suffix | 0/3 | 0/3 | 0/3 | 0/3 | floor |
| edit/rotate | 0/3 | 0/3 | 0/3 | 0/3 | floor |
| edit/recolor | 3/3 | 3/3 | 3/3 | 3/3 | ceiling |
| edit/remove | 3/3 | 3/3 | 3/3 | 3/3 | ceiling |
| plan/assemble | 1/3 | 2/3 | 1/3 | 0/3 | mixed |
| plan/disassemble | 1/3 | 0/3 | 1/3 | 0/3 | mixed |
| repair/none | 3/3 | 1/3 | 2/3 | 1/3 | mixed |
| repair/color | 1/3 | 1/3 | 1/3 | 0/3 | mixed |
| repair/shift | 0/3 | 0/3 | 0/3 | 0/3 | floor |

分母是实际返回数；未返回数量见analysis.json，不能把服务失败解释为模型不会。
floor=全部模型精确成功为零；ceiling=全部成功；mixed=其他情况。该分类仅描述这3个对象，不是总体难度标签。

## 格式、成本与规模

| 模型 | 主任务成功* | 格式合法 | 截断 | 主任务费用 | 平均延迟ms |
| --- | ---: | ---: | ---: | ---: | ---: |
| gpt-4.1-mini | 15/39 | 38/39 | 0 | $0.071077 | 4761 |
| gpt-4.1 | 11/39 | 35/39 | 0 | $0.341298 | 3501 |
| gemini-2.5-flash | 13/39 | 34/39 | 1 | $0.089190 | 3174 |
| qwen3-vl-32b-instruct | 7/39 | 22/39 | 3 | $0.025229 | 17606 |

*混合任务成功总数仅作执行摘要，不能作为统一“智能分数”或可靠排名。

| 件数/结构族 | gpt-4.1-mini | gpt-4.1 | gemini-2.5-flash | qwen3-vl-32b-instruct |
| --- | ---: | ---: | ---: | ---: |
| 12/shallow-terrace | 7/13 | 5/13 | 7/13 | 3/13 |
| 20/shallow-terrace | 4/13 | 4/13 | 3/13 | 2/13 |
| 29/column-field | 4/13 | 2/13 | 3/13 | 2/13 |

## 分层指标

以下指标以所有已返回响应为分母，畸形答案仍保留零分；N/A表示任务不适用。

| 任务 | 模型 | 指标及均值 |
| --- | --- | --- |
| relations/contact | gpt-4.1-mini | fieldAccuracy=100.0%; connectedAccuracy=100.0%; aboveAccuracy=100.0%; contactStudsAccuracy=100.0%; shortestPathAccuracy=100.0% |
| relations/contact | gpt-4.1 | fieldAccuracy=66.7%; connectedAccuracy=66.7%; aboveAccuracy=66.7%; contactStudsAccuracy=66.7%; shortestPathAccuracy=66.7% |
| relations/contact | gemini-2.5-flash | fieldAccuracy=75.0%; connectedAccuracy=66.7%; aboveAccuracy=100.0%; contactStudsAccuracy=66.7%; shortestPathAccuracy=66.7% |
| relations/contact | qwen3-vl-32b-instruct | fieldAccuracy=25.0%; connectedAccuracy=33.3%; aboveAccuracy=33.3%; contactStudsAccuracy=33.3%; shortestPathAccuracy=0.0% |
| relations/separated | gpt-4.1-mini | fieldAccuracy=75.0%; connectedAccuracy=100.0%; aboveAccuracy=100.0%; contactStudsAccuracy=100.0%; shortestPathAccuracy=0.0% |
| relations/separated | gpt-4.1 | fieldAccuracy=58.3%; connectedAccuracy=66.7%; aboveAccuracy=100.0%; contactStudsAccuracy=66.7%; shortestPathAccuracy=0.0% |
| relations/separated | gemini-2.5-flash | fieldAccuracy=75.0%; connectedAccuracy=100.0%; aboveAccuracy=100.0%; contactStudsAccuracy=100.0%; shortestPathAccuracy=0.0% |
| relations/separated | qwen3-vl-32b-instruct | fieldAccuracy=66.7%; connectedAccuracy=100.0%; aboveAccuracy=66.7%; contactStudsAccuracy=100.0%; shortestPathAccuracy=0.0% |
| reconstruct/full | gpt-4.1-mini | partF1=4.3%; bomF1=93.1%; surfaceF1=18.6% |
| reconstruct/full | gpt-4.1 | partF1=2.4%; bomF1=98.8%; surfaceF1=18.2% |
| reconstruct/full | gemini-2.5-flash | partF1=5.8%; bomF1=96.1%; surfaceF1=29.0% |
| reconstruct/full | qwen3-vl-32b-instruct | partF1=0.0%; bomF1=0.0%; surfaceF1=0.0% |
| generate/constraints | gpt-4.1-mini | constraintAccuracy=50.0% |
| generate/constraints | gpt-4.1 | constraintAccuracy=77.8% |
| generate/constraints | gemini-2.5-flash | constraintAccuracy=55.6% |
| generate/constraints | qwen3-vl-32b-instruct | constraintAccuracy=33.3% |
| complete/suffix | gpt-4.1-mini | partF1=78.0%; bomF1=94.7%; surfaceF1=76.3%; additionF1=0.0%; preservation=98.5% |
| complete/suffix | gpt-4.1 | partF1=74.9%; bomF1=98.3%; surfaceF1=73.4%; additionF1=0.0%; preservation=100.0% |
| complete/suffix | gemini-2.5-flash | partF1=52.8%; bomF1=66.7%; surfaceF1=53.6%; additionF1=11.1%; preservation=66.7% |
| complete/suffix | qwen3-vl-32b-instruct | partF1=28.8%; bomF1=28.8%; surfaceF1=27.2%; additionF1=0.0%; preservation=33.3% |
| edit/rotate | gpt-4.1-mini | partF1=1.1%; bomF1=66.7%; surfaceF1=7.5%; preservation=66.7% |
| edit/rotate | gpt-4.1 | partF1=2.8%; bomF1=100.0%; surfaceF1=14.5%; preservation=100.0% |
| edit/rotate | gemini-2.5-flash | partF1=6.1%; bomF1=66.7%; surfaceF1=8.8%; preservation=66.7% |
| edit/rotate | qwen3-vl-32b-instruct | partF1=6.1%; bomF1=100.0%; surfaceF1=10.4%; preservation=100.0% |
| edit/recolor | gpt-4.1-mini | partF1=100.0%; bomF1=100.0%; surfaceF1=100.0%; preservation=100.0% |
| edit/recolor | gpt-4.1 | partF1=100.0%; bomF1=100.0%; surfaceF1=100.0%; preservation=100.0% |
| edit/recolor | gemini-2.5-flash | partF1=100.0%; bomF1=100.0%; surfaceF1=100.0%; preservation=100.0% |
| edit/recolor | qwen3-vl-32b-instruct | partF1=100.0%; bomF1=100.0%; surfaceF1=100.0%; preservation=100.0% |
| edit/remove | gpt-4.1-mini | partF1=100.0%; bomF1=100.0%; surfaceF1=100.0%; preservation=100.0% |
| edit/remove | gpt-4.1 | partF1=100.0%; bomF1=100.0%; surfaceF1=100.0%; preservation=100.0% |
| edit/remove | gemini-2.5-flash | partF1=100.0%; bomF1=100.0%; surfaceF1=100.0%; preservation=100.0% |
| edit/remove | qwen3-vl-32b-instruct | partF1=100.0%; bomF1=100.0%; surfaceF1=100.0%; preservation=100.0% |
| plan/assemble | gpt-4.1-mini | legalPrefix=65.2% |
| plan/assemble | gpt-4.1 | legalPrefix=72.4% |
| plan/assemble | gemini-2.5-flash | legalPrefix=49.4% |
| plan/assemble | qwen3-vl-32b-instruct | legalPrefix=0.0% |
| plan/disassemble | gpt-4.1-mini | legalPrefix=33.3% |
| plan/disassemble | gpt-4.1 | legalPrefix=31.2% |
| plan/disassemble | gemini-2.5-flash | legalPrefix=39.1% |
| plan/disassemble | qwen3-vl-32b-instruct | legalPrefix=2.8% |
| repair/none | gpt-4.1-mini | partF1=100.0%; bomF1=100.0%; surfaceF1=100.0%; preservation=100.0%; localizationF1=100.0%; restorationSuccess=100.0% |
| repair/none | gpt-4.1 | partF1=33.3%; bomF1=33.3%; surfaceF1=33.3%; preservation=33.3%; localizationF1=33.3%; restorationSuccess=33.3% |
| repair/none | gemini-2.5-flash | partF1=98.3%; bomF1=100.0%; surfaceF1=99.5%; preservation=98.3%; localizationF1=66.7%; restorationSuccess=66.7% |
| repair/none | qwen3-vl-32b-instruct | partF1=33.3%; bomF1=33.3%; surfaceF1=33.3%; preservation=33.3%; localizationF1=33.3%; restorationSuccess=33.3% |
| repair/color | gpt-4.1-mini | partF1=98.0%; bomF1=98.0%; surfaceF1=97.3%; preservation=100.0%; localizationF1=66.7%; restorationSuccess=33.3% |
| repair/color | gpt-4.1 | partF1=64.2%; bomF1=65.9%; surfaceF1=62.0%; preservation=66.7%; localizationF1=33.3%; restorationSuccess=33.3% |
| repair/color | gemini-2.5-flash | partF1=97.2%; bomF1=97.2%; surfaceF1=95.5%; preservation=98.2%; localizationF1=55.6%; restorationSuccess=33.3% |
| repair/color | qwen3-vl-32b-instruct | partF1=0.0%; bomF1=0.0%; surfaceF1=0.0%; preservation=0.0%; localizationF1=0.0%; restorationSuccess=0.0% |
| repair/shift | gpt-4.1-mini | partF1=94.4%; bomF1=100.0%; surfaceF1=94.0%; preservation=100.0%; localizationF1=0.0%; restorationSuccess=0.0% |
| repair/shift | gpt-4.1 | partF1=62.2%; bomF1=66.7%; surfaceF1=61.8%; preservation=66.7%; localizationF1=0.0%; restorationSuccess=0.0% |
| repair/shift | gemini-2.5-flash | partF1=30.6%; bomF1=33.3%; surfaceF1=30.9%; preservation=33.3%; localizationF1=0.0%; restorationSuccess=0.0% |
| repair/shift | qwen3-vl-32b-instruct | partF1=30.6%; bomF1=33.3%; surfaceF1=30.9%; preservation=33.3%; localizationF1=0.0%; restorationSuccess=0.0% |

## 同对象诊断

| 模型 | 无图重建 | 符号参考重建 | 符号参考完整结构正确率 |
| --- | ---: | ---: | ---: |
| gpt-4.1-mini | 0/3 | 3/3 | 100.0% |
| gpt-4.1 | 0/3 | 3/3 | 100.0% |
| gemini-2.5-flash | 0/3 | 2/3 | 66.7% |
| qwen3-vl-32b-instruct | 0/3 | 1/3 | 33.3% |

为控制评分变化，主实验与两个对照沿用相同的普通重建成功判据（合法性+BOM+可见表面）；完整结构正确率另列。
符号参考提供额外真值信息，改善不等于纯视觉因果效应；无图仍保留BOM。需要结合表面/部件分数与格式失败，而非只看0/1。

## 高分是否只是复制输入

复制基线只返回公开current结构；修复题额外返回空faultIds，不读取目标来构造答案。
保留区域占比高时，partF1很高也可能没有修好任何错误。以下差值只作诊断，不替代原评分。

| 任务 | 模型 | 复制基线Part-F1 | 模型Part-F1 | 差值 | 输出结构未变 |
| --- | --- | ---: | ---: | ---: | ---: |
| complete/suffix | gpt-4.1-mini | 85.9% | 78.0% | -7.9 pp | 0/3 |
| complete/suffix | gpt-4.1 | 85.9% | 74.9% | -11.0 pp | 0/3 |
| complete/suffix | gemini-2.5-flash | 85.9% | 52.8% | -33.1 pp | 0/3 |
| complete/suffix | qwen3-vl-32b-instruct | 85.9% | 28.8% | -57.1 pp | 1/3 |
| edit/rotate | gpt-4.1-mini | 1.7% | 1.1% | -0.5 pp | 0/3 |
| edit/rotate | gpt-4.1 | 1.7% | 2.8% | 1.1 pp | 0/3 |
| edit/rotate | gemini-2.5-flash | 1.7% | 6.1% | 4.4 pp | 0/3 |
| edit/rotate | qwen3-vl-32b-instruct | 1.7% | 6.1% | 4.4 pp | 0/3 |
| edit/recolor | gpt-4.1-mini | 82.0% | 100.0% | 18.0 pp | 0/3 |
| edit/recolor | gpt-4.1 | 82.0% | 100.0% | 18.0 pp | 0/3 |
| edit/recolor | gemini-2.5-flash | 82.0% | 100.0% | 18.0 pp | 0/3 |
| edit/recolor | qwen3-vl-32b-instruct | 82.0% | 100.0% | 18.0 pp | 0/3 |
| edit/remove | gpt-4.1-mini | 97.1% | 100.0% | 2.9 pp | 0/3 |
| edit/remove | gpt-4.1 | 97.1% | 100.0% | 2.9 pp | 0/3 |
| edit/remove | gemini-2.5-flash | 97.1% | 100.0% | 2.9 pp | 0/3 |
| edit/remove | qwen3-vl-32b-instruct | 97.1% | 100.0% | 2.9 pp | 0/3 |
| repair/none | gpt-4.1-mini | 100.0% | 100.0% | 0.0 pp | 3/3 |
| repair/none | gpt-4.1 | 100.0% | 33.3% | -66.7 pp | 1/3 |
| repair/none | gemini-2.5-flash | 100.0% | 98.3% | -1.7 pp | 2/3 |
| repair/none | qwen3-vl-32b-instruct | 100.0% | 33.3% | -66.7 pp | 1/3 |
| repair/color | gpt-4.1-mini | 94.4% | 98.0% | 3.6 pp | 1/3 |
| repair/color | gpt-4.1 | 94.4% | 64.2% | -30.2 pp | 0/3 |
| repair/color | gemini-2.5-flash | 94.4% | 97.2% | 2.8 pp | 1/3 |
| repair/color | qwen3-vl-32b-instruct | 94.4% | 0.0% | -94.4 pp | 0/3 |
| repair/shift | gpt-4.1-mini | 94.4% | 94.4% | 0.0 pp | 3/3 |
| repair/shift | gpt-4.1 | 94.4% | 62.2% | -32.2 pp | 2/3 |
| repair/shift | gemini-2.5-flash | 94.4% | 30.6% | -63.9 pp | 1/3 |
| repair/shift | qwen3-vl-32b-instruct | 94.4% | 30.6% | -63.9 pp | 1/3 |

正常无故障题上不修改是正确控制行为；在有故障题上必须结合定位和目标区域恢复判断。
补全应同时看新增部分F1，修复应同时看故障定位、恢复成功，不能仅凭整体Part-F1判断能力。

## 结果是否“漂亮”

- 模型逐题结果确实不同的任务：relations/contact、plan/assemble、plan/disassemble、repair/none、repair/color。
- 样本内兼有成功/失败的任务：relations/contact、plan/assemble、plan/disassemble、repair/none、repair/color；这本身不等于模型之间有差异。
- 精确成功地板：relations/separated、reconstruct/full、generate/constraints、complete/suffix、edit/rotate、repair/shift。
- 精确成功天花板：edit/recolor、edit/remove。
- 好的结果应能解释差异来自哪里，并经新对象复现；不要求模型按预设顺序排列。当前只能判断局部可区分性，不能宣布benchmark已得到充分验证或达到CVPR录用水平。
- 若某任务全零，先看格式、几何和局部指标；若全满，将其保留为基础控制，不让它支配总分。模型间只有一两题差异时不作显著性解释。
- 已有完整算法审计中，高度排序解完全部10240道装拆题。因此本轮规划差异可说明固定输入下的约束遵循差异，不能证明需要复杂搜索。

## 已落实的改进

1. 从单一成功总数改为“任务变体×模型×件数”诊断，保留格式、几何、结构、执行与故障定位的分层指标。
2. 为无图/符号参考建立同对象配对记录；新增模型测试与既有730条API证据隔离，评分器不变。
3. 新增缺失、截断、成本、实际provider和token记录；账单未确定就停止，不把网络故障写成能力零分。
4. analysis.json保留每对模型的对象级差值，不把同对象13道题当独立统计样本。
5. 新增只用公开输入构造的复制基线，量化整体结构分数中“原本就正确”的部分，保留原始成功判据。

## 下一阶段

先在其余未用验证对象上扩展重复，分开控制件数、结构族、遮挡和连接复杂度。针对地板任务设计更小结构/局部位姿/连接问答的阶梯，针对天花板保留基础控制并增加真实子装配编辑。新题需先独立验证，不为拉开模型差距而定制答案。
冻结当前报告后才设计后续提示或工具消融；这些开发对象不得升级成“未见正式测试”。需另有授权语义数据、人工指标校准和更充分模型比较，才能支持广泛能力主张。

## 重建难度阶梯

已追加 24/24 次独立记录的开发调用，新增费用 $0.045679。
主验证与阶梯合计费用 $0.649294。

| 件数/输入 | gpt-4.1-mini | gpt-4.1 | gemini-2.5-flash | qwen3-vl-32b-instruct |
| --- | ---: | ---: | ---: | ---: |
| 2/RGB+BOM | 0/1 | 0/1 | 0/1 | 0/1 |
| 2/符号参考 | 1/1 | 1/1 | 1/1 | 1/1 |
| 4/RGB+BOM | 0/1 | 0/1 | 0/1 | 0/1 |
| 4/符号参考 | 1/1 | 1/1 | 1/1 | 1/1 |
| 8/RGB+BOM | 0/1 | 0/1 | 0/1 | 0/1 |
| 8/符号参考 | 1/1 | 1/1 | 1/1 | 1/1 |

这六道题来自一个其他验证对象的嵌套前缀，不能当成六个独立对象。它检查更低复杂度区间是否有可测信号；前缀变化同时改变几何，不能归因于件数本身。后续需扩展多个独立来源，按遮挡和连接分层重复。

### 原点问题与修订验证

逐答复查发现v1裁剪前缀未重新归一化：2件和4件结构的最小Z为1，但图像页脚仍沿用“原点为最小角”的说明。
Gemini的2件输出与真值只差整体平移；这是评价接口的干扰因素，不能将v1全零无条件解释为视觉能力缺失。
v1原答、费用和分数保持不变，originAudit只作事后诊断；不把平移对齐后的结果补记模型成功。

v2将每个前缀重新平移到最小XYZ均为0，并明确写入题面，另行调用24/24次，新增费用$0.045780。
全部三轮合计新增$0.695073，没有重置累计账本。

| 件数/归一化输入 | gpt-4.1-mini | gpt-4.1 | gemini-2.5-flash | qwen3-vl-32b-instruct |
| --- | ---: | ---: | ---: | ---: |
| 2/RGB+BOM | 1/1 | 0/1 | 0/1 | 0/1 |
| 2/符号参考 | 1/1 | 1/1 | 1/1 | 1/1 |
| 4/RGB+BOM | 0/1 | 0/1 | 0/1 | 0/1 |
| 4/符号参考 | 1/1 | 1/1 | 1/1 | 0/1 |
| 8/RGB+BOM | 0/1 | 0/1 | 0/1 | 0/1 |
| 8/符号参考 | 1/1 | 1/1 | 1/1 | 1/1 |

两版同时改变了坐标原点、对应图片和说明文字，并重新采样，不能把全部分数变化因果归于某一个改动。v2仍是同一来源的自适应开发验证，不是独立确认集。

归一化后RGB+BOM成功1/12，
符号参考成功11/12。
修正原点后出现有限成功信号，但当前数据仍不足以形成稳定的重建能力阶梯。“已修复题面原点问题”和“已建立有效能力分层”是两件不同的事。

下一项优先检查是具有明确相机/坐标约定的局部位姿、候选判别与逐字段任务，区分视觉理解、坐标映射和长JSON生成。不要继续扩大未经这种校准的全结构重建调用。

## 复现

运行 `node node_modules/tsx/dist/cli.mjs benchmark/suite/study/cli.ts replay-model-validation` 可离线复算，不需要API密钥。
原始响应、固定输入、价目快照、账单、分析和源码版本分别见同目录run.json、protocol.json、ledger.json、analysis.json。
