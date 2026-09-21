# BrickAtlas evidence-v1：第三轮 CVPR 模拟审稿

> 审稿对象：`benchmark/paper/evidence-v1/main.pdf`、`main.tex`、`supplement.pdf`，以及 `benchmark/ldraw-evidence-v1/` 与 `benchmark/suite/ldraw-evidence/`。
>
> 评审前提：按作者要求，**假设计划中的模型实验均已完成**。仓库中尚未出现真实模型数值，因此本文不因表格中的 `–` 或 `not-run` 扣分，也不虚构模型排名、效应方向或显著性。下面的推荐是对研究问题、任务定义、实现和统计协议的条件性评价；真实模型结果仍会改变最终推荐。

## 一、总体结论

**当前推荐：Weak Reject（4/10），高置信度。**

相较上一版，这一稿有实质性进步：论文不再把“任务组合”本身当贡献，而是围绕可证伪问题组织——模型对同一标识零件的回答是否随任务相关证据变化，并在语义保持扰动下保持正确。相关工作定位更谨慎；任务角色被拆为视觉、结构证据、非恒定控制和恒定控制；旧的公开字段捷径与模型输入泄漏风险得到工程隔离；模型请求、原始回执、gold来源、统计估计和论文表格之间形成了很强的可审计链。

但我仍不会给到 Borderline Accept，原因不是实验数量，而是**论文的核心视觉估计量仍存在身份语义漂移，且人类可判定性协议在实现上没有闭环**。此外，新 matched-graph challenge 的多数答案变化对仍可被不计算连通分量的度数启发式完美解出。因此，当前实现尚不足以支持论文最强的“same-target evidence following”与“graph evidence beyond priors”解释。

### 分项评分

| 维度 | 评分（10分） | 判断 |
|---|---:|---|
| 研究问题重要性 | 7 | “正确但是否真的跟随了证据”是合理且重要的benchmark问题。 |
| 新颖性 | 6 | 明确绑定exact observation、condition-specific gold与paired correctness，有非平凡协议贡献；但视觉干预语义必须先成立。 |
| 技术可靠性 | 5 | 工程与审计链很强；核心视觉gold语义、QA闭环和图挑战浅层捷径仍削弱构念效度。 |
| 实验设计 | 6（条件性） | NewAcc、Both、转移类型和源平衡估计合理；需要真实结果显示该协议带来新诊断，而非只增加报表。 |
| 清晰度与诚实性 | 8 | 主张边界、控制任务含义、源规模限制和人工审核状态写得较诚实。 |
| 可复现性 | 9 | wire snapshot、哈希、原始回执重算、不可覆盖运行目录、双oracle和报告索引均很好。 |
| CVPR契合度 | 6 | 有视觉证据跟随主题，但核心视觉部分仅140题、两类任务，且当前干预仍偏display binding。 |

---

## 二、主要优点

### 1. 论文主线终于是一个可证伪的科学问题

`main.tex:20–40` 把问题定义为：普通正确率不能证明模型跟随了识别目标的证据；需要condition-specific gold和paired both-correct。这比旧版“我们有V/S/G/E四类任务”强得多。

### 2. 主张—任务—指标的角色划分明显改善

`main.tex:170–210` 明确：视觉题、结构题、记录读取和执行控制不是一个端到端装配智能链；Step sequence与Restoration被降格为合同执行/输出合规，而非机械规划。这准确回应了旧审稿意见中“模型区分度不等于目标能力”。

617题被互斥地划为140个核心视觉题、146个结构证据题、290个非恒定控制和41个恒定控制，不再把异质任务混为一个能力总分。这个决定是正确的。

### 3. 证据适应指标优于普通前后准确率差

`main.tex:304–325` 定义 NewAcc、Both、条件适应率和错误转移类别；缺失响应保留在分母，非法输出不被当成稳定。这能区分“正确跟随新证据”“保留旧答案”“转向其他错误”“格式/API失败”。13项适应指标测试已实际通过。

### 4. 工程可审计性达到较高水平

我核验了 `validate-run.ts`、`evidence_adaptation.py`、`reporting.py`、`run-matched-graphs.ts` 等实现：

- 只从公开input序列化模型请求，internal scoring bundle不进入prompt；
- 保存真实wire request及SHA-256；
- 保存并复核原始provider response，再重新解析submission；
- model revision、adapter、prompt、dataset、code hash均绑定；
- wrong-image alternate gold和graph-intervention gold均重新验证；
- 缺失、超时、拒答、非法JSON和格式错误不会缩小分母；
- 新运行目录禁止覆盖，合成fixture不能注册成真实结果。

这是论文很有价值的一部分，也比多数benchmark实现更严谨。

### 5. 论文对局限的表述比上一版成熟

例如：

- `main.tex:153–157` 不把源装配规模当认知难度；
- `main.tex:183–190` 不把source oracle自动当作视觉可判定；
- `main.tex:222–236` 承认Color wrong-image并非color-only因果干预；
- `main.tex:398–404` 承认Mask会同时去掉背景并暴露遮挡面、Crop还改变放大率；
- `main.tex:376–400` 限定24源、connector覆盖和人工验证边界。

这些都减少了过度声明。

---

## 三、足以拒稿的问题（CRITICAL）

## C1. 核心“same-target fact change”存在canonical identity与display-conditioned identity的语义冲突

### 位置

- 标题与核心主张：`main.tex:13–14`、`20–32`、`47–55`。
- 身份定义：`main.tex:150–155`，canonical identity由source hash与instance ID组成。
- paired fact-change：`main.tex:212–228`。
- 真实问题生成：`benchmark/suite/ldraw-v2/questions.ts:39–50`。
- alternate gold赋值：`benchmark/suite/ldraw-evidence/validate-run.ts:133–151`。
- worked example：`benchmark/ldraw-evidence-v1/literature/protocol-evidence.md:87–115`。

### 具体矛盾

论文同时主张：

1. 研究“同一个已识别、位于原始装配中的零件”；
2. Bxxxx是canonical source identity的显示标签；
3. wrong-image中，图像上被贴上Bxxxx标签的几何/零件决定新的gold。

这三点不能同时无条件成立。

**Color示例的真实wire payload**仍问：

> `Identify the original color of B0115; numbered isolation is allowed.`

wrong-image却把另一个donor实例单独渲染为B0115，并将donor颜色设为新gold。若B0115指canonical source instance，那么它的“original color”没有改变；B图只是错误地标注了另一个实例，canonical gold应保持不变，或该输入应归为矛盾/信息污染，而不是fact change。若B0115指“当前图像中带此显示标签的对象”，则题目不应再写“original”，论文也不应称其为same canonical target。

**Part-type**更接近visual binding intervention：候选实例的显示标签被交换，问题与选项固定，因此“哪个显示标签当前附着在匹配几何上”确实改变。但这改变的是display reference，不是原始source entity的part type。论文称“B0035 remains the target”尚可，但两侧不是对同一套canonical candidate identities做事实判断，而是对显示标签—几何绑定做重新解释。

### 为什么足以拒稿

论文最主要的新颖性和最主要指标就是condition-specific gold。如果gold改变的语义基础不明确，NewAcc与Both可能把“服从错误标签”“忽略canonical source truth”计为正确适应。这样即使所有模型数字都完整，核心结果也无法回答标题中的same-part问题。

### 必须怎么改

选择一个语义，不要混用：

**方案A（推荐）：把核心任务明确改为display-grounded reference binding。**

1. 将问题改成例如：
   - Color：`What color is the object currently marked B0115 in this image?`
   - Part-type：`Which displayed label currently marks a candidate with the same visible geometry/type as the target marked B0035?`
2. 将论文主张从“same canonical part fact changes”改为“the referent selected by a display label changes while the query token stays fixed”。
3. 明确区分：
   - canonical source identity：只用于生成、审计和跨条件配对；
   - display referent：模型在当前观测中应解析的对象；
   - source truth：不随wrong-image变化；
   - observation-conditioned answer：随display referent变化。
4. 将Color donor限制为只改变需要测的属性，至少保持几何/尺寸/姿态类别一致；否则只声称general referent following，不声称attribute-specific adaptation。
5. 重新生成A/B请求、重新人审、重新跑模型；旧结果不能直接迁移。

**方案B：坚持canonical source identity。**

则wrong-image不能拥有alternate semantic gold；它应作为evidence corruption / contradiction / dependency test，报告original-gold retention、拒答与矛盾识别。真正fact-change必须在source-consistent条件下修改目标属性或新建明确的counterfactual scene，并同步改变题目世界状态，而不是只换标签/换图。

### 验收标准

随机抽取任何一对，审稿人仅看question、image和identity contract，就能唯一回答：Bxxxx在两侧究竟指canonical entity还是current display referent；gold变化不需要阅读内部生成代码才能解释。

---

## C2. 论文要求A/B两侧独立answerability，但现有QA实现只为B侧生成模板，闭环实际上不能成立

### 位置

- 论文要求：`main.tex:288–295`：paired visual comparison requires independent answerability decisions for both observations。
- QA配对逻辑：`wire_qa.py:61–83`，只有A、B两侧都为`decidable`才进入comparable subset。
- 当前QA产物：`benchmark/ldraw-evidence-v1/qa/wrong-image*/`。
- 自报状态：`ISSUE-4-REPORT.md:63–75`、`final-validation.json:26–29`。

### 实证结果

当前仅存在两份内容相同方向的wrong-image QA导出，均为：

- condition = `wrong-image`；
- 140个观测；
- Color与Part-type；
- 全部pending；
- reviewer数为0。

需要区分**渲染资产**与**人工QA记录**：`paired-renders.json`中已经存在operand-only A侧图像及其渲染元数据，缺失的不是A侧图片，而是与A侧exact wire request绑定的QA模板和人工反馈。当前`qa/`目录中的`validated-run.json`与`qa-template.json`只覆盖wrong-image B侧。`qualify_pairs()`会为每个pair计算A/B observation ID；缺失的A侧QA决定默认为pending。因此，即使把当前140个B侧全部标为decidable，**QA-comparable pairs仍会是0**。

此外，当前schema只容纳每个observation一个reviewer结果，重复observation ID会被当作冲突拒绝，并没有两位独立标注者、一致率和adjudication后的最终判断数据结构。对一个以人类可判定性为关键门控的新视觉benchmark，这比LEGO-Puzzles已报告的三人验证弱。

### 为什么足以拒稿

Part-type gold来自source partNumber，并不保证输入像素足以区分近似几何；Color wrong-image还可能标签或轮廓不一致。若没有成对、双侧、独立的人类可判定性验证，模型的NewAcc/Both下降可能来自不可判定图像，而非证据跟随失败。论文自己已经承认这一逻辑，因此实现不闭环会直接破坏核心分析。

### 必须怎么改

1. 对每个核心视觉pair同时生成A侧operand-only与B侧wrong-image QA记录，固定280个观测的完整分母；去重只能基于exact wire hash，不能只基于task ID。
2. 至少两位独立评审者在不知道模型输出、条件名称、alternate gold和另一侧判断的情况下审核每个observation。
3. 将schema改为：
   - `reviews[]`：reviewer、decision、reason、timestamp、native-size attestation；
   - `agreement`：原始一致率及适合多分类的可靠性统计；
   - `adjudication`：仅不一致项，记录最终决定与理由；
   - `final_decision`：由预先冻结规则生成，而非覆盖原始review。
4. 评审问题不能只问“answerable吗”，还要验证：目标标签是否唯一指向一个可见对象、答案选项是否包含唯一视觉答案、变体是否引入矛盾或遮挡。
5. 主结果同时报告：
   - 全分母结果；
   - 双侧最终decidable子集；
   - 每个排除原因和来源数；
   - full vs QA-subset结论是否一致。
6. 若某任务改过prompt或render，原QA作废，按wire hash重新审。

### 验收标准

对每个用于NewAcc/Both的pair，A/B两侧都有非pending最终判断；不存在因缺A侧模板导致的系统性pending；双评审原始判断、分歧和裁决均可追溯。

---

## 四、一审会被点的问题（MAJOR）

## M1. matched-graph challenge仍主要测度数统计，而非必须使用连通关系

### 位置

- 摘要：`main.tex:33–37`，“controls additional surface statistics”。
- §5.4：`main.tex:340–365`。
- 数据：`matched-graphs-v1/manifest.json`。
- 生成器：`matched-graphs.py:24–37`。

### 实证结果

73个answer-changing pair中：

- 73/73匹配surviving node数、surviving edge数和target degree；
- 只有12/73匹配完整surviving degree sequence；
- 其余61/73使用path vs triangle-plus-isolates，度数序列不同。

我额外计算了一个**不做BFS/union-find、不计算连通分量**的启发式：

> 预测值 = 度数为0的存活节点数 +（若存在任何非孤立节点则加1）

它在整个219-observation challenge上答对201/219（91.78%）；在73个answer-changing pair的146个观测上答对134/146（91.78%）。更关键的是：

- 对61个未匹配度数序列的答案变化pair，paired both-correct = 61/61；
- 对12个真正匹配度数序列的答案变化pair，paired both-correct = 0/12。

因此扩展的大多数pair并没有迫使模型读取非局部连通结构；一个浅层度数启发式即可完美通过61个主要pair。论文虽然披露了12/61的限制，但“graph evidence beyond priors”的解释仍过强。

### 改法

1. 把主挑战限定为12个degree-sequence-matched answer-changing pairs，或生成更多满足至少以下约束的pairs：相同node set、edge count、target degree、surviving degree multiset、孤立节点数、答案频率平衡。
2. 将61个弱匹配pairs单列为`degree-visible control`，不能与强匹配pairs合并成主结论。
3. 正式加入并报告以下基线：node count、edge count、degree histogram lookup、isolates+one启发式、1-WL/简单GNN、BFS/union-find。
4. 主张应为：模型是否超越指定浅层图统计；不要把所有matched pairs统称为“超越priors”。
5. 若强匹配pair数量仍小，诚实称为proof-of-concept challenge，并报告pair级置信区间/逐题结果，不将其扩展为广泛图推理结论。

---

## M2. 真实模型结果必须证明“协议带来新诊断”，不能只把模型排成另一张表

### 位置

- 贡献主张：`main.tex:91–114`。
- 指标：`main.tex:304–325`。
- 当前表结构：Table 2/3与paired analyses。

### 需要看到的证据

按你的前提，模型指标已完成。最终论文必须呈现至少一种ordinary accuracy无法揭示的稳定现象，例如：

- 相近的A侧准确率，对应显著不同的Both或NewAcc；
- 模型在source-macro准确率高，但频繁保留old gold；
- 模型对semantic invariance稳定，却不跟随fact change，或相反；
- 错误类型随模型/任务族产生可解释分化；
- node/degree启发式与学习模型在自然题上接近，却在强匹配pairs上分离。

如果所有模型的NewAcc/Both与普通准确率几乎单调一致，或主要差异来自invalid-format/API失败，那么协议的新诊断价值有限，最终仍可能Weak Reject。

### 改法

1. 主表按Color与Part-type分开，报告A Acc、B/NewAcc、Both、old-gold retention、other/invalid、source count和区间。
2. 加一张“普通准确率排名 vs Both排名”的对照；报告模型间是否发生rank reversal，但不要用无根据阈值。
3. 给出2–3个真实pair级案例：A正确→B新gold、A正确→B旧gold、A/B均错但同答；必须展示真实模型原始响应而非合成示例。
4. 报告格式有效率，证明主要结论不是JSON合规差异。
5. 做family×model×condition误差分析，但不要用共享ID声称已定位模型内部因果失败。

---

## M3. 论文的视觉贡献范围仍偏窄，且Color与Part-type不能共享同一种因果解释

### 位置

- `main.tex:52–55`：两类核心视觉任务。
- `main.tex:183–186`：Color与Part-type定义。
- `main.tex:222–228`：wrong-image机制。

140个视觉题来自24个源，每源约2–5题，核心仅Color与Part-type。Color通过donor replacement改变可见内容，可能同时改变形状；Part-type通过候选标签交换改变display binding。二者都可用于“evidence following”，但干预机制与错误含义不同，不能只汇总成一个视觉能力。

### 改法

1. 永远分开报告Color与Part-type，不给统一视觉总分。
2. 对每个family写清：变化的是目标属性、显示引用，还是证据可靠性。
3. 为Color选择同part-type、姿态与尺度尽可能匹配、仅颜色不同的donor；无法满足的项不进入color-specific主分析，只进入general binding分析。
4. 为Part-type增加无标签视觉对照或位置/框引用对照，用来区分几何判断与OCR/标签追踪。
5. 结论限定为“instance-label grounded evidence following on two atomic visual attributes”，不要升级成“comprehensive assembly intelligence”。

---

## 五、打磨级问题（MINOR）

1. **摘要仍写未运行状态。** 用户要求假设实验已完成，则最终稿必须重写`main.tex:37–40`及Table 1/2/3中的“unrun”，用真实结果回答核心问题；不能只把横线换成数字。
2. **第8页参考文献过于空。** 版式合法，但只有6篇参考文献会强化“定位不足”的观感。当前积木邻近工作核验扎实；还应补充直接相关的contrast sets、counterfactual/consistency VQA、visual grounding/label binding评测文献。此项需要正式学术检索后决定，不应凭印象硬加。
3. **图3仍可能被误读为难度图。** caption已说明两侧尺度不同且不是难度，但视觉上并排柱状图仍诱导比较。可改为两个明确标注“different statistic / different scale”的独立小图或表。
4. **补充材料过长。** 182页全量dossier适合artifact，不适合让审稿人承担阅读成本。主supplement应保留协议、统计、关键审计和失败案例；完整617题dossier作为单独machine-readable/HTML artifact。
5. **命名一致性。** 代码family为`shape-match`，论文称`Part-type`；建议结果索引和公开schema提供稳定display name映射，避免读者以为是不同任务。

---

## 六、假设实验完成后，什么结果会改变我的推荐

### 可升为 Borderline Accept / Weak Accept 的条件

必须同时满足：

1. C1身份语义被修正，所有core pair的question、observation、gold在一个统一contract下成立；
2. C2完成A/B双侧独立人审，核心结论在QA-decidable子集和全分母上方向一致；
3. 至少若干模型出现普通准确率无法解释的NewAcc/Both差异或rank reversal；
4. 模型错误主要不是invalid format或调用失败；
5. graph结论以12个强匹配pair或扩充后的强控制集为主，并加入度数启发式基线；
6. 结论严格限定到两个视觉family和24个源。

### 会维持Reject的结果形态

- Core A侧准确率很低，导致条件适应率分母过小；
- B侧下降主要来自不可判定、标签错位或invalid output；
- 各模型Both仅复制A/B普通准确率排序，没有新增诊断；
- matched graph上的学习模型优势在加入degree heuristic后消失；
- 结果只显示模型有差异，却不能把差异对应到明确的证据跟随错误类型。

---

## 七、建议修改顺序

1. **先冻结身份与问题语义**：canonical entity还是display referent，只能选一个主语义。
2. **重建视觉pair和gold**：按统一contract重生成，先机器验证再人工验证。
3. **补齐A/B双侧双人QA**：这是运行模型之前的门，不是结果出来后的筛选。
4. **修强图挑战**：主分析只用真正控制degree statistics的pairs，加入浅层启发式基线。
5. **重跑受影响模型条件**：旧wrong-image结果不能迁移到新prompt/新render。
6. **最后写结果叙事**：用真实rank reversal、old-gold retention和pair级案例证明诊断价值。

---

## 八、最终审稿意见摘要

这版已经不是简单的任务拼盘。它提出了一个有价值的测量问题，并在请求隔离、provenance、raw receipt、条件gold、失败分母、源平衡统计和可复现发布方面做得很强。作者也诚实拆除了“复杂装配=复杂题”“共享ID=端到端能力”“控制任务=规划能力”等旧主张。

然而，论文最中心的视觉干预仍没有稳定地区分canonical source identity与current display referent；现有human QA管线又只覆盖B侧，因此其自定的A/B可判定门目前无法闭合。图挑战也在61/73个答案变化pair上保留了可被简单度数启发式利用的捷径。这些问题影响核心结果的含义，而不是补一行实验即可解决。

**投稿建议：投之前需要大改。** 修完C1/C2并以强控制图挑战和真实模型诊断现象收尾后，这篇可以进入Borderline Accept讨论；在当前定义下，我仍给Weak Reject。
