# BrickAtlas evidence-v2：第四轮 CVPR 模拟审稿

> 审稿对象：`benchmark/paper/evidence-v2/main.pdf`、`benchmark/paper/evidence-v2/supplement.pdf`、`benchmark/ldraw-evidence-v2/`、`benchmark/suite/ldraw-evidence-v2/` 及相关冻结输入与发布链。  
> 审稿前提：按照作者要求，**假设计划中的所有真人 QA 与模型实验均已完成**。仓库当前没有可见的真实模型数值，因此本文不因“结果文件尚为空”扣分，也不虚构模型排名、效应方向或显著性。结论针对测量设计、实现与在何种结果条件下能够支撑论文主张。

---

## 1. 总体结论

### 推荐

- **Recommendation：Weak Reject / Borderline Reject**
- **建议分数：5/10**
- **Confidence：4/5**
- **相对 evidence-v1：明显上调**。上一轮两个最严重问题——canonical identity 与 display referent 的语义冲突、仅 B 侧 exact-wire QA——已经在设计层被实质修复；图任务也不再把 61 个 degree-visible pair 当成强结构挑战。

### 一句话判断

这已经从“核心构念不自洽”进步为一篇**定位谨慎、协议严密、实现可审计**的测量论文；但目前 Part-type 干预新引入了一个可直接击穿 paired metric 的确定性规则泄漏：模型只要正确解出 A 侧，再选择 option order 中第一个不同于 A-side gold 的选项，就能在完全不读取 B 图像的情况下预测 67/67 个 B-side gold，并取得 67/67 的 `Both`。模型实验的完整纳入集合也没有冻结。两项解决之前，我不会给接收。

### 结论边界

- 如果作者修复 Part-type 刺激、重新做人审和该族模型推理，冻结并强制执行模型 roster，而且真实结果显示 `Both` 提供了与 ordinary-A accuracy 不同且跨来源稳定的诊断信息，我会把推荐提高到 **Weak Accept（6/10）**。
- 如果最终结果只表现为 ordinary accuracy 的另一种排序，或 Part-type 的结论主要由 B 侧选项 A 集中驱动，即使表格完整，我仍会维持拒稿。
- 如果作者不重做 Part-type，而仅把 `Both` 改名为“主要指标”，不足以解决问题。

---

## 2. 本轮确认已经关闭的问题

这些不应继续作为拒稿理由，否则会错误地沿用旧版本意见。

### 2.1 display-grounded 语义已经自洽

**论文位置**：`main.tex` 第 44–68、210–234、278–301 行。

- 论文明确区分 canonical identity、source truth、observation-specific display mapping 与 scored answer。
- Color 询问当前渲染外观，不再询问“original color”。
- Part-type 询问当前图像中哪个显示标签指向与目标相同的可见几何，不再声称源零件的 canonical type 被改写。
- 模型请求显式声明“References select objects in the supplied image only”。

**审稿判断**：evidence-v1 的语义矛盾已关闭。

### 2.2 Color 干预现在接近单因素变化

**论文位置**：`main.tex` 第 251–276 行。  
**实现证据**：`benchmark/ldraw-evidence-v2/stimulus-validation.json`。

- 两臂保持原始几何、source pose、camera、scale、label projections、visibility 与 material settings。
- 仅 body-color 参数变化。
- 146 个端点的语义颜色计数为 Red 37、Blue 37、Yellow 36、Black 36。
- 像素变化被限制在共同投影 body mask 的一像素抗锯齿膨胀范围内。

**审稿判断**：Color 是当前最干净、最有说服力的视觉子基准。

### 2.3 双侧 exact-wire QA 与审计链已经成立

**论文位置**：`main.tex` 第 303–355 行。  
**实现位置**：`benchmark/suite/ldraw-evidence-v2/qa.py`、`run.py`。

- 280 个 primary endpoints 和 67 个 auxiliary observations 全部具有冻结 observation/hash。
- 两个不同真人对每个 observation 分别判断；decision、visual choice 或任一 check 不一致时进入第三人裁决。
- human choice 与机器 gold 冲突时会阻止 finalization，而不是静默覆盖。
- 模型请求必须复现经过 QA 的 exact messages 与 image bytes；QA gate 早于网络调用。
- synthetic fixture、单人 QA、同一人占两个 slot、B-only QA、请求篡改与 dry-run 发布均被测试拒绝。

**审稿判断**：上一轮“只有 B 侧 QA”的问题已关闭。

### 2.4 图挑战的强弱分区现在诚实且正确

**论文位置**：摘要第 31–35 行、正文第 97–105 行、图任务章节及补充材料。  
**实现位置**：`graph_audit.py`、`graph_run.py`、`graph-partitions.json`。

- 12 个 strong-change pairs 匹配 node set、edge count、target degree、完整 surviving degree multiset 和 isolate count。
- anonymous uniform-feature 1-WL 在这些 pair 上不可区分。
- 61 个 degree-visible change pairs 被明确列为 control，不再承担强结构推理主张。
- isolates-plus-one 在 strong-change 上 `Both=0/12`，BFS/union-find 为 `12/12`；论文明确称其为 8 个来源、单一构造模板的 small proof of concept。

**审稿判断**：实现与措辞一致，没有发现新的 graph scoring bug。

### 2.5 工程协议质量较高

本轮重新运行：

```text
python3 -m unittest discover -s benchmark/suite/ldraw-evidence-v2 -p "test*.py" -v
Ran 26 tests in 4.014s — OK
```

覆盖 strict JSON、provider revision、request/receipt hash、QA 重建、缺失失败进入固定分母、source-macro、graph partition、1-WL blind spot 和发布门。测试通过不证明 benchmark 构念有效，但证明许多协议承诺不是只写在论文里。

---

## 3. CRITICAL：Part-type 的确定性交换规则可在不读取 B 图像时取得 67/67 Both

### 3.1 可复现事实

**数据位置**：`benchmark/ldraw-evidence-v2/visual-manifest.json`。  
**生成根因**：`src/benchmark-v2/render.ts` 的旧 Part-type wrong-render 选择逻辑，以及 `benchmark/suite/ldraw-evidence-v2/prepare.py` 对其 `alternateChoiceId` 的继承。  
**论文涉及位置**：`main.tex` 第 278–301、357–387、389–414 行。

67 个 Part-type pairs 的 choice-ID gold 分布：

| Arm | A | B | C | D |
|---|---:|---:|---:|---:|
| A side | 10 | 23 | 16 | 18 |
| B side | **57** | 10 | **0** | **0** |

因此：

- B 侧永远回答 `A` 的 `NewAcc = 57/67 = 85.07%`。
- 按论文的 equal-source estimator，固定 `A` 的 B 侧 source-macro 为 **83.82%**，source bootstrap 95% 区间为 **[72.78%, 93.13%]**。
- 给定 A-side gold，按 options 顺序选择第一个不同于 A gold 的选项，可预测 B-side gold **67/67**。

生成偏差的结构性原因是：交换对象不是从所有合格 distractors 中经过联合平衡选择，而是取 option order 中第一个不等于原答案的候选。于是 B gold 被压到 A/B 两个位置。

### 3.2 该规则会直接绕过 `Both`

这不是“固定回答 A 只能污染 NewAcc、但 Both 会保护结果”的轻度问题。固定 A 同时回答两臂时确实得到 `Both=0`；然而攻击规则可以利用模型刚刚求出的 A-side gold：

1. 若 A gold 为 A，则 B gold 恒为 B（10/10）。
2. 若 A gold 为 B、C 或 D，则 B gold 恒为 A（57/57）。
3. 等价地，B gold 总是 option order 中第一个不同于 A gold 的选项。

因此，一个系统可以**只读取并正确解出 A 图像，完全忽略 B 图像**，然后套用 first-non-A 规则，便在所有 67 个 Part-type pairs 上得到 `Both=1`。这直接破坏了“Both 证明模型在两侧均跟随当前视觉证据”的核心解释，也使条件适应率 `Both/AAcc` 可在不读取 B 证据时达到 100%。

附带影响还包括：

- `NewAcc`、B-side accuracy、B-side model ranking 和错误转移分解被固定选择先验直接污染；
- 两臂答案熵与基线难度严重不对称；
- 若模型具有不同 choice-position bias，Part-type 的排序还会混入选项偏好。

这意味着仅把 `Both` 设为唯一主要指标、仅补 always-A baseline，或仅淡化 NewAcc，均不能修复构念。

### 3.3 必须采取的修复

不能只补一行 always-A baseline。建议按以下顺序重做 Part-type：

#### Step 1：重选交换候选

- 对每个 parent 枚举全部满足视觉与语义约束的 nonmatching candidate。
- 在全体 67 pairs 上联合优化 `(A_gold, B_gold)` 转移矩阵。
- 保证 `A_gold != B_gold`。
- 让 B 边际尽量接近四个 choice IDs 的均匀分布。
- 同时避免某个简单规则（first non-A、last non-A、固定位置、目标最近/最远候选）取得异常高分。

不要依赖随机种子碰巧平衡；应写确定性的 assignment/optimization，并把目标、tie-break 和最终矩阵固化到 manifest。

#### Step 2：把答案先验审计变成发布硬门

在 `stimulus-validation.json` 和测试中新增：

- 每个 family、每个 arm 的 gold marginal；
- `(A_gold, B_gold)` 4×4 transition matrix；
- fixed-choice A/B/C/D baselines；
- first/last non-A-gold、option-index、label-number/order 等生成规则基线；
- micro 与 equal-source 两种口径；
- 对每条 heuristic 输出逐题 prediction 与错误列表，而非只给总分。

验收规则应由作者预先写入合同；不要在看到模型结果后再选择阈值。

#### Step 3：重新生成并重新冻结

交换候选改变意味着：

- B 侧图片、gold、observation ID/hash、wire snapshot、review package 全部变化；
- 所有受影响的 Part-type 两侧最好一并进入新版本，以免混用旧 A 与新 B 的 QA lineage；
- 更新 figures、manifest、download routes、checksums 和 release version。

#### Step 4：重做该族 QA 与模型推理

- 旧 Part-type human QA 与模型 responses 不得迁移到新 observation。
- Color、graph 和历史 dossier 可保持冻结，不必全面重跑。
- 最终论文同时报告新的 answer-position baselines。

### 3.4 严重度

**CRITICAL / 足以拒稿。** 这是当前版本最重要的问题，也是最应该先修的地方。

---

## 4. MAJOR：模型实验没有冻结完整纳入集合，存在选择性报告空间

### 4.1 证据

**实现位置**：`benchmark/suite/ldraw-evidence-v2/analyze.py` 第 175–225 行。  
**当前配置**：`benchmark/ldraw-evidence-v2/adapter.example.json`。

`build(run_directories, destination)` 会严格验证传入的每个 live run，也会拒绝同一 `provider/model_revision/adapter_hash` 重复，但它接受调用者提供的**任意 run 目录列表**。当前发布物中没有：

- 冻结的 planned model roster；
- 每个模型对应的 adapter hash/transport；
- expected run set；
- 纳入、排除与失败规则；
- “所有计划模型均已进入最终分析”的机器断言。

因此，即使每个纳入结果都是真实 receipt，也无法从 artifact 判断是否漏掉某个计划模型，或者作者只把有利的一部分 run 交给 analyzer。

### 4.2 具体修复

新增不可变的 `model-roster.json`，至少包括：

- public display name；
- provider；
- exact served model revision；
- adapter file 与 SHA-256；
- endpoint/API revision；
- image-detail policy、resolution、temperature、max tokens、single-attempt policy；
- planned visual run ID 与 graph run ID；
- 是否 primary、为何纳入；
- 冻结日期；
- 预定义 exclusion/failure handling。

然后修改分析入口：

1. `analyze.py` 必须读取 roster，而不是只接收自由的 run list。
2. 验证 observed run set 与 expected run set 完全相等；缺少、多出或 hash 不符均停止生成论文表。
3. 失败、拒答、超时也必须作为 roster 中已完成的 run 进入固定分母，不能靠删除目录排除。
4. 发布 `model-run-index.json`，把 roster entry、run manifest、request index、receipt set、QA snapshot 和论文表行一一绑定。
5. 在论文实验设置中列出确切模型名、版本、provider、运行日期、adapter 差异和纳入规则。

### 4.3 严重度

**MAJOR，接近 CRITICAL。** 若论文的主要价值依赖多模型诊断与排名，而最终 release 仍不能证明所有计划模型完整纳入，我会把它提升为拒稿级问题。

---

## 5. MAJOR：真人 QA 保证了“人际独立”，但没有保证 pair 两臂的记忆独立

### 5.1 证据

**论文位置**：`main.tex` 第 322–355 行。  
**实现位置**：`qa.py` 第 31–62 行。

每位 reviewer 都会收到全部 347 observations。pair membership 与 condition name 被隐藏，队列分别随机，但同一个人仍会先后看到同一 pair 的 A/B 两侧。

对当前冻结队列的距离审计：

- reviewer-1：同 pair 距离最小 2，中位数 99.5；5 对距离不超过 10，14 对不超过 25；
- reviewer-2：同 pair 距离最小 1，中位数 99；7 对距离不超过 10，16 对不超过 25；其中 1 对相邻。

大多数 pair 相距较远，所以这不是全面失效；但对高度相似的 Color/Part-type 两臂，近邻出现会让第二次判断可能受到第一次观察的记忆或对比影响。当前的 `independence_attestation` 无法排除这种协议层暴露。

### 5.2 具体修复

最佳方案是在尚未正式 QA 前改成 **arm-disjoint review assignment**：

- 每个 endpoint 仍获得两份独立真人判断；
- 同一 reviewer 永远不看同一 pair 的另一臂；
- 至少使用四名 reviewer，以两两交叉分配 A/B；
- adjudicator 对该 observation 独立，且最好未看过其 counterpart；
- assignment validator 对每个 pair 检查 reviewer 集合的交集为空。

如果真实 QA 已完成且不能重做：

1. 披露每个 reviewer 的 within-pair queue distance 分布。
2. 预先定义近邻阈值后，报告排除近邻 pairs 的敏感性结果；阈值选择需说明，不能根据模型结果调节。
3. 比较 near 与 far observations 的 decidable rate、choice agreement 和 gold-conflict rate。
4. 把这项限制写入正文，而不只放实现说明。

### 5.3 严重度

**MAJOR，但不是当前首要拒稿点。** 若敏感性分析显示 near/far 无差异，可降为 limitation；若存在明显 carryover，则需重新分配 QA。

---

## 6. MAJOR/MINOR：统计独立性仍只在 source 层处理，未覆盖重复作者

### 6.1 证据

**论文位置**：`main.tex` 第 389–405 行已诚实承认 source bootstrap 不能消除 shared parts 或 authoring conventions 的依赖。

24 个 source 实际来自 18 个不同作者；10/24 source 属于 4 个重复作者组：

- Robert Paciorek：3 个 source；
- Philippe Hurbain：3 个 source；
- Merlijn Wissink：2 个 source；
- Zoltan Keri：2 个 source。

全部 24 个 source 均有作者、URL、SHA-256 和 CC BY 2.0 归因，因此**授权不是问题**。问题是推断单元可能相关。

### 6.2 具体修复

- 保留 equal-source estimate 作为 primary，避免临时改变主口径。
- 新增 author-cluster sensitivity：先在作者内聚合 source，再对 18 个作者等权或按作者 cluster bootstrap。
- 报告 source-macro 与 author-macro 的差异，不要求二者完全一致。
- 对 inventory/geometry 高相似的 source 做一个透明的相似度附录或 leave-one-author-out 分析。
- 若模型排序或主要效应在 leave-one-author-out 下改变，降低跨来源稳定性的主张。

### 6.3 严重度

- 若真实结论对 author sensitivity 稳定：**MINOR/limitation**。
- 若主要结论只在 source-independent 假设下成立：**MAJOR**。

---

## 7. MINOR 到条件性 MAJOR：单次闭源推理没有稳定性协议

### 7.1 现状

runner 的优点是 temperature=0、单次请求、无自动 retry、固定 model revision/adapter、保留 provider receipt。可惜 temperature=0 不等于托管服务绝对确定；当前 analyzer 还明确禁止相同 model/adapter 的重复 run，除非先冻结 repeat-run protocol。

### 7.2 建议

二选一即可，不必把项目无限扩张：

**方案 A：把 estimand 明确定义为一次冻结调用。**

- 论文不声称模型排名具有跨调用稳定性；
- pairwise difference 区间包含 0 时不下排名结论；
- 只把结果表述为该服务版本、该请求快照的一次 auditable evaluation。

**方案 B：预注册重复运行。**

- 对所有模型采用同次数完整重复，而非只重复表现接近的模型；
- run 是第二层随机单元，报告 run-to-run 波动与 source 变异；
- analyzer 依据 roster 中 repeat count 接纳重复 run，禁止事后选择“最好的一次”。

### 7.3 严重度

若模型间差距大且主张克制，这是 **MINOR**。若文章依赖很小的 rank reversal 或接近零的差异，则升级为 **MAJOR**。

---

## 8. 论文层面的剩余评价

### 8.1 新颖性与贡献定位

当前版本没有再把工作包装成“综合装配智能”。它将贡献收窄为：

1. current-display referent 的明确测量合同；
2. 两个分开计分的 paired visual interventions；
3. exact-observation dual review 与 receipt-derived transitions；
4. 用强/弱图控制说明错误对照如何破坏构念解释。

这比原始“把多个已有要素组合起来”的叙事更可信。论文还主动承认 pairing、Both scoring、1-WL limitation 都不是首创，这提升了可信度。

但影响面依然偏窄：视觉主实验只有两个 atomic attributes、140 pairs、24 sources；strong graph 只有 12 pairs、8 sources、单一 six-cycle/two-triangles 模板。若真实模型结果没有显示 ordinary accuracy 之外的新诊断现象，审稿人仍可能认为它更像一个高质量测量案例，而非足够广的 CVPR benchmark。

### 8.2 图任务与视觉主线的关系

图挑战作为 methodological audit 是成立的，但它是 text-graph input，不是视觉感知。正文目前已较好地写成 supporting audit，而非与视觉 family 混为一个总分。最终实验表也必须保持分离：

- 不做 visual+graph pooled score；
- 不用 graph strong subset 证明视觉 evidence following；
- 不用视觉结果证明结构推理；
- graph 只支持“control construction affects interpretation”这一方法论结论。

### 8.3 论文写作与版面

主文 8 页，正文 7 页、参考文献从第 8 页开始；科学补充材料 6 页。逐页视觉检查未发现明显 overfull、裁切、空页或不可读图。Part-type 图已放大，图注清楚说明 remote candidate 被裁掉、模型实际输入是完整 1280×800 PNG。

当前写作的主要问题不是语言，而是需要在实验表旁直接披露 answer-position baselines 与 roster completeness；否则读者无法从论文表格发现上述风险。

---

## 9. 最终实验结果必须满足的证据条件

由于本审稿不虚构未见数值，以下是“哪些结果会改变接收判断”的明确标准，而不是预设结果：

### 支持接收的结果形态

- 修复后的 Color 与 Part-type 中，多个模型的 `Both` 与 `AAcc` 呈现不完全相同的行为谱系；
- 报告 fixed-choice、option-order、text-only/no-image 等基线，且 learned models 的主要结论不能由这些基线解释；
- full 与 both-decidable 子集方向基本一致，排除原因与 source coverage 透明；
- source-macro、author sensitivity 和 micro 结论不发生实质性冲突，或冲突被准确限定；
- 图 strong-change 上浅层规则失败而真正 component reasoning 方法成功，学习模型结果不被夸大为内部机制证据；
- 完整 roster 中的失败与无效输出仍保留在分母。

### 不足以支持接收的结果形态

- 只有模型间分数有差异，但 `Both` 基本由 ordinary A 能力或 B 侧答案先验解释；
- 只报告 NewAcc，不报告 AAcc、Both、old-gold retention、invalid 与固定选项基线；
- 只挑选若干表现有趣的模型进入主比较；
- 大量 pair 被 QA 排除后仍用“140 pairs”描述有效证据；
- 把 12 个 graph pairs 的表现推广到一般图推理或装配规划；
- 把“显示标签跟随”扩大表述为完整 perception-to-action assembly intelligence。

---

## 10. 投稿前优先级

### P0：必须完成

1. **重做 Part-type candidate swap assignment，平衡 B gold 与联合转移矩阵。**
2. **重新生成、QA、运行受影响的 Part-type observations。**
3. **增加固定选项与生成规则 baselines，并把审计做成发布硬门。**
4. **冻结 model roster，并让 analyzer 强制 exact expected run set。**

### P1：强烈建议

5. 改为 arm-disjoint human review；若 QA 已完成，则加入 carryover sensitivity。
6. 增加 author-cluster / leave-one-author-out sensitivity。
7. 在主实验表旁明确写出每个 family 的 A/B gold marginals、有效 pair/source 数与失败分母。

### P2：根据真实结果决定

8. 若模型差距或 rank reversal 很小，执行预注册重复运行；否则将 estimand 明确限定为一次冻结调用。
9. 增加少量跨模板 strong graph pairs 只能作为增强项，不应阻塞当前主线。
10. 不再扩回 11 个 family 的“统一智能总分”，也不要新增大规模训练任务。

---

## 11. 给作者的最终建议

**现在不建议直接投稿。** 但与 evidence-v1 不同，这次不需要再次推翻整篇论文：主问题已经被收窄且定义清楚，Color 与图审计基本成立，协议工程也有可信度。当前最有效的路线是一次集中修复：只重做 Part-type 刺激与其 QA/推理，同时冻结模型 roster；完成后根据真实 `Both` 诊断结果决定是否投稿。

如果 P0 全部完成且结果确实显示 paired evaluation 揭示了 ordinary accuracy 看不到的稳定差异，这篇论文已经具备从 **5/10 提升到 6/10** 的现实空间。若不修 Part-type 先验，当前最核心的视觉贡献只剩 Color 一族足够干净，证据宽度不足以支撑 CVPR 接收。

---

## 12. 本轮核验范围与未核验项

### 已核验

- 主文 8 页与补充材料 6 页全部审读、视觉检查；
- `visual-manifest.json` 的 140 pairs / 280 endpoints 与 67 auxiliary observations；
- Color 语义分布与干预验证；
- Part-type A/B gold choice 分布和 fixed-A source-macro；
- QA assignment、合并、裁决、gold-conflict 和推理 gate；
- visual runner、graph runner、analysis 与发布边界；
- 12/61 graph 分区及 shallow/BFS 基线；
- 24 source 的作者重复与许可证记录；
- 26 项测试重新运行并全部通过。

### 因审稿前提而未据实判断

- 任何具体模型的真实 AAcc、NewAcc、Both、排名或失败类型；
- 模型差异是否统计稳定；
- 真人 QA 的实际 agreement、kappa、排除率与 gold conflicts；
- Part-type 先验在具体模型输出中造成了多大实际影响。

这些必须由最终冻结结果填写；本报告没有将“假设实验完成”等同于“假设实验结果有利”。
