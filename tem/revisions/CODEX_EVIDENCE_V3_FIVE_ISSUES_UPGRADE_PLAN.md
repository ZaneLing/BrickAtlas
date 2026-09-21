# BrickAtlas evidence-v3 五问题 Codex 分阶段升级计划

> **本文档用途**
>
> ：交给 Codex 逐步执行。每阶段有明确输入、可改范围、禁止改、机器 / 人工验收、失败回退。阶段未过不得进入下一阶段。
> **科学评审前提与执行状态必须分开**
>
> ：审稿判断按用户要求假设最终人审与模型实验将完整完成；Codex 执行时必须读取当前真实状态，不得把假设写回产物。当前冻结索引记录 9 个计划 run 尚未采集，QA 包已生成但真实反馈尚未导入；后续只能使用实际人审和真实 provider receipts，绝不制造结果。
> **方法学校准（写在最前，Codex 必须遵守）**
>
> ：
> v2 的 "67/67 Both 攻击" 是 
>
> **oracle-assisted 审计上界**
>
> （需已知 A gold），不是协议内单观察模型可实现的攻击。
> v3 Part-type oracle first-alt = 23/67 (34.3%) 是
>
> **受限设计审计**
>
> ，不是模型上限、不是泄漏证据、不是拒稿阈值。
> Color oracle last-alt/cyclic-previous = 32/73 (43.8%) 同理，
>
> **不构成模型上限、不设 .40 拒稿门**
>
> 。
> 不设 
>
> `invalid<10%`
>
> 、
>
> `QA排除>30%`
>
> 、
>
> `CI不重叠`
>
> 、
>
> `r=1`
>
>  等无依据阈值。
> 不把 rank reversal 作为成功必要条件。
> 不因 0/9 runs 或 0/280 QA 当前状态扣分。



***

## 0. 总原则、文件路径、保护线、证据状态

### 0.1 项目根与当前版本



```
项目根: /Users/bytedance/Documents/trae\_projects/brick-atlas

当前论文: benchmark/paper/evidence-v3/main.tex  (8页PDF, supplement 7页)

当前数据: benchmark/ldraw-evidence-v3/  (delivery-manifest 905 files)

当前代码: benchmark/suite/ldraw-evidence-v3/  (27 unittest, 全过)

历史版本: evidence-v1/evidence-v2/ldraw-v1/ldraw-v2 只读保留，禁止修改
```

### 0.1.1 默认版本策略（必须先执行）



* evidence-v3 已有 preservation/delivery/roster/observation hashes，应视为已封存基线。Codex **不得原地修改** `benchmark/ldraw-evidence-v3/`、`benchmark/suite/ldraw-evidence-v3/` 或 `benchmark/paper/evidence-v3/` 后仍沿用 v3 名称与旧 hash。

* Phase 0 默认先复制 / 生成一个明确的新工作版本目录（例如 `evidence-v4-draft`、`ldraw-evidence-v4-draft` 与对应 suite），新版本号由 Main 确认；文中后续写 “修改 v3” 均指 “以 v3 为输入，在新版本实施”。

* 如果实际尚未发布且 Main 明确决定 v3 只是未封存工作稿，可在分支内继续使用 v3 路径，但必须先重建所有受影响 hash/manifest/QA lineage/roster lock，且不得引用旧 seal。这个决定写入 tracker。

* 仅做工作稿（如 related-work-matrix、feasibility、ledger）可放新版本的`.runtime/`或`work/`目录，不进入最终 sealed 包，除非发布合同明确纳入。

### 0.2 冻结资产（禁止 Codex 修改）



| 资产                 | 路径                                                                         | 理由                                                  |
| ------------------ | -------------------------------------------------------------------------- | --------------------------------------------------- |
| identity contract  | `ldraw-evidence-v3/identity-contract.json`                                 | 显示语义已自洽，evidence-v1 构念问题已关闭                         |
| Part-type 联合分配     | `ldraw-evidence-v3/part-type-assignment.json` + `assignment-contract.json` | B marginal 17/17/17/16，off-diagonal 5–6，已通过 .40 设计门 |
| Color 干预           | 146 endpoints，body-color counterfactual，已冻结字节                              | 单因素渲染，像素差在 mask 内                                   |
| parent-disjoint QA | `suite/ldraw-evidence-v3/qa.py` SLOTS=6                                    | cross\_arm\_exposures=0                             |
| roster             | `model-roster.json` + `roster-lock.json` (sha256 bee85470…)                | 3 models exact-set 冻结                               |
| author sensitivity | `source-dependence.json` (18 authors / 17 clusters)                        | 已含 leave-one-author-out                             |
| graph partitions   | `graph-partitions.json` (12 strong / 61 degree-visible)                    | 1-WL 盲点已诚实声明                                        |
| 27 unittest        | `test_*.py`                                                                | 全过，禁止删改通过的测试                                        |

### 0.3 证据状态（Codex 必须区分）



* **已核验事实**：代码行、JSON 数值、hash、test 输出。

* **Main 独立核验**：Color 146 endpoints 全为 render\_operands 长度 1 /labels 长度 1；no-image 去图后 A/B messages 文本完全相同。

* **待真实结果**：0/9 model runs、0/280 human QA。本计划不假设其数值。

* **外部近邻**：VisualFLIP (arXiv:2606.07872, 2026-06-05 preprint)。Codex 引用前必须 fetch 原文核对，不得凭本摘要写引用细节。

### 0.4 五个问题与优先级



| # | 问题                                            | 严重度                    | 对应阶段    |
| - | --------------------------------------------- | ---------------------- | ------- |
| 1 | VisualFLIP 近邻遗漏，主张定位风险                        | MAJOR                  | Phase 1 |
| 2 | 图像依赖≠正确指代；Color 单 operand；no-image Both 机械为 0 | MAJOR                  | Phase 2 |
| 3 | analyze.py prior baseline 未按 QA subset 重算     | MAJOR (统计口径)           | Phase 3 |
| 4 | 三模型冻结范围与逐模型证据接入                               | MAJOR（外推边界）+ MUST（证据链） | Phase 5 |
| 5 | 论文修复叙事过重，缺科学发现槽位                              | MAJOR（写作）              | Phase 6 |

Phase 7 是横跨五个问题的**交付质量门**，不计作第六个科学问题。



***

## Phase 0：冻结与分支隔离

**目标**：在动任何东西之前，确保 v3 当前字节可回滚。

### 输入



* `benchmark/ldraw-evidence-v3/preservation-lock.json`

* `benchmark/ldraw-evidence-v3/delivery-manifest.json`

### 允许修改



* 新建 git branch `codex/v3-five-issues`。

* 新建当前工作版本的 `CODEX_PHASE_TRACKER.md` 记录版本决策和每阶段状态。

### 禁止修改



* 任何 evidence-v3 `observations/*.json` 字节。若 Phase 2 选择新增 control，必须创建新 study version；不得在原地改 v3。

* `model-roster.json`、`roster-lock.json`、`identity-contract.json`。

* 历史 v1/v2 目录。

* 封存的 `paper/evidence-v3/main.tex` 与 `supplement.tex`；Phase 6 修改新论文版本。

### 动作



1. `git status` 确认干净。

2. `git checkout -b codex/v3-five-issues`。

3. 记录当前 git HEAD、main.pdf sha256、supplement.pdf sha256 到 tracker。

4. 跑一次 baseline：



```
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python \\

&#x20; -m unittest discover -s benchmark/suite/ldraw-evidence-v3 -p 'test\*.py'
```

预期 27 tests OK。记录到 tracker。

### 机器验收



* unittest 27 全过。

* 记录进入本阶段前的工作树状态；不要假定默认分支名为`main`。若用户工作树已有修改，禁止覆盖或以`git reset --hard`清理。

### 失败停止



* unittest 失败 → 停止，报告当前 HEAD 与失败 test 名。不进 Phase 1。

### Codex 阶段报告模板



```
Phase 0: PASS

branch\_and\_head: 填写 \`git branch --show-current\` 与 \`git rev-parse HEAD\` 的原样输出

baseline\_tests: 填写 unittest 的实际通过/失败数

baseline\_pdf\_hash: 填写 main.pdf 的实际 SHA-256

next\_stage: Phase 1
```



***

## Phase 1：近邻文献定位与主张重构

**目标**：把 VisualFLIP 等直接近邻补进 Related Work，并把贡献从 "修复自己上版 bug" 重写为独立增量。

### 输入



* `paper/evidence-v3/main.tex` §2 (L114–156)

* `paper/evidence-v3/references.bib` (13 entries)

* `paper/evidence-v3/additions.bib`

* 近邻 URL：[https://arxiv.org/abs/2606.07872](https://arxiv.org/abs/2606.07872) 与 [https://arxiv.org/html/2606.07872v1](https://arxiv.org/html/2606.07872v1)

### 允许修改



* 只编辑源文件 `additions.bib`：新增 VisualFLIP bib entry；`references.bib` 是由 `publication.py` 生成的产物，不手工编辑。

* `main.tex` §2：新增一段对比；调整贡献段措辞。

* 新增 `benchmark/paper/evidence-v3/related-work-matrix.md`（工作稿，不进 PDF）。

### 禁止修改



* 不编 VisualFLIP 的具体数字。Codex 必须先 fetch arXiv HTML，只读以下字段：标题、作者、日期、是否 preprint、图像干预机制、pair 指标名称、属性数、图数、模型数、是否区分 sequential。其他未读到的字段不写。

* 不把 "补引用" 写成贡献。

* 不删现 13 条引用。

### 逐文件动作

#### 1.1 fetch 并核对 VisualFLIP



```
\# Codex 自行 fetch，不编造

\# 记录到 related-work-matrix.md：

\# - title / authors / date / arXiv id / preprint or published

\# - intervention type (minimal edit flipping gold?)

\# - pair metric name (Both? Collapse Rate?)

\# - attribute families count

\# - image count / model count

\# - sequential vs simultaneous
```

#### 1.2 在 additions.bib 新增并重新生成 references.bib

按 arXiv 实际元数据写一个完整的 `@misc` 条目，key 必须按实际第一作者姓氏确定。**不写未读到的 venue**。保持 `publication.py` 的 “冻结 base bib + additions.bib → references.bib” 单向生成关系；不得让生成脚本读取自己的输出。生成后检查新条目只出现一次。

#### 1.3 main.tex §2 新增段落

位置：在现 "Contrastive and consistent answers" 段之后。要点（用 Codex 自己的话，不照本摘要）：



* VisualFLIP 做最小图像干预翻转 gold，两侧独立调用，报告 pair-level 指标。

* BrickAtlas v3 的**独立增量**必须落在以下三点之一（按实际证据选）：


  * (a) **显示指代合同**：labels 是 image-local display reference 而非 source identity；VisualFLIP 的干预是否也区分了 source truth vs display referent？（需 fetch 确认；若未区分，这是增量。）

  * (b) **预注册捷径审计**：13 个 oracle-A 规则在推理前冻结 .40 门、HiGHS 联合分配、transition matrix 公开。VisualFLIP 是否做了等价的 shortcut bound？（需 fetch 确认。）

  * (c) **exact-wire 人审可审计性**：parent-disjoint 6-reviewer + receipt-derived transition。

* **明确不主张**：pair accuracy / Both /minimal image edit 本身不是首创。

#### 1.4 贡献段重写

现 main.tex L86–92 把 "paired image-dependent answers have substantial precedent" 已写得诚实。Codex 要做的是：



* 把 L106–112 以 “An earlier Part-type assignment always chose” 开头的段落**修复叙事**从贡献中移出，改放 §7 limitations 或 footnote。

* 贡献改为：(1) display-grounded referent contract；(2) pre-registered shortcut audit on paired visual interventions；(3) receipt-derived transition analysis with parent-disjoint human review。

* 不写 "首个"。

### 机器验收



* 先查看当前 `publication.py` / BUILD 的生成流程，再由源 bib 重新生成 `references.bib`。

* `tectonic main.tex` 编译通过，无 undefined citation。

* 用现有 `verify_publication.py` 核验实际 `main.bbl` 引用数与 PDF；不以简单 `grep` 代替 BibTeX 解析。

* related-work-matrix.md 列出 VisualFLIP 每行字段并标注 "fetch 自 arXiv HTML v1, <日期>"。

### 人工验收



* Main 核对 VisualFLIP 对比矩阵无编造数字。

* 贡献段不再以 "修复 v2 bug" 为主要卖点。

### 失败停止



* fetch 不到 arXiv HTML → 停止，只写 "VisualFLIP 已识别为近邻，待人工核对后再写对比矩阵"。不编。



***

## Phase 2：题目级测量审计与最小控制决策

**目标**：把 "图像依赖≠正确指代" 这个构念问题落到题级台账，并在两条路线中选一条（见决策点 2.4）。

### 输入



* `visual-manifest.json`（140 pairs / 280 endpoints + 67 auxiliary）

* `observation-index.json`（347 observations）

* `prepare.py`（color L75–97, shape-match L98–160）

* `answer-prior-audit.json`

* 219 graph observations（`graph-partitions.json`）

### 允许修改



* 新增审计台账（JSON）。

* 若选路线 B：新增 Part-type answer-preserving invariance control（见 2.4）。

* 不删改现有 140 pairs / 67 auxiliary / 219 graph。

### 禁止修改



* 不重做 Color 干预（已冻结、单因素干净）。

* 不把 Color 从主表移除。

* 不假设 dominant-color baseline 满分。

### 2.1 建立全题审计台账 schema

新建两个派生台账：`visual-observation-audit-ledger.jsonl`（347 行）与 `graph-observation-audit-ledger.jsonl`（219 行）。一行对应一个 observation；台账可从权威文件重新生成，不反向驱动评分。visual 行 schema 示例：



```
{

&#x20; "observation\_id": "从 observation-index.json 读取",

&#x20; "pair\_id": "从 visual-manifest.json 的 pair 关系读取；auxiliary 可为 null",

&#x20; "parent\_task\_id": "从 visual-manifest.json 读取",

&#x20; "source\_id": "10001",

&#x20; "author\_id": "从 source-dependence.json 读取",

&#x20; "family": "color|shape-match",

&#x20; "arm": "A|B|null(position-control)",

&#x20; "role": "primary|position-reference-control",

&#x20; "wire\_sha256": "从 observation-index.json 读取",

&#x20; "image\_sha256": "从 observation-index.json 读取",

&#x20; "image\_pixels\_unchanged\_vs\_counterpart": true|false,

&#x20; "prompt\_text\_sha256": "由 model-visible prompt bytes 计算",

&#x20; "options": "原样复制 payload.options 数组",

&#x20; "gold\_choice\_id": "C",

&#x20; "gold\_semantics": "Red",

&#x20; "gold\_independently\_recomputed": true|false,

&#x20; "reference\_is\_unique\_in\_image": "pending-human|true|false",

&#x20; "visibility\_sufficient": "pending-human|true|false",

&#x20; "qa\_final\_decision": "pending|decidable|ambiguous|unanswerable|contradictory",

&#x20;   "human\_qa": {

&#x20;   "review\_count": 0,

&#x20;   "final\_decision": "pending",

&#x20;   "final\_visual\_choice": null,

&#x20;   "exclusion\_reasons": \[]

&#x20; },

&#x20; "legal\_baseline\_predictions": {},

&#x20; "model\_results\_join\_key": "observation\_id",

&#x20; "exclusion\_reason": null|string,

&#x20; "source\_cluster": "从 source-dependence.json 读取",

&#x20; "author\_cluster": "从 source-dependence.json 读取"

}
```

对 **347 visual observations** 与 **219 graph observations** 分别全量建账，共 566 行，禁止抽样。视觉唯一性只存在于 visual 台账，保持 `pending` 直到 Phase 4；图台账使用 node/edge/gold/partition/baseline 字段，不伪造图片、选项或真人评审字段。模型输出不在 Phase 2 写入，Phase 5 通过`observation_id`连接独立的 run-observation ledger。

### 2.2 Color 定位：appearance sanity track

Color 的事实（Main 已核验，Codex 复核）：



* 146 endpoints 全为 `render_operands` 长度 1、`labels` 长度 1。

* 单 operand body-color 变化，不交换候选标签。

* 合法单图 dominant-color 程序可作为待测 baseline——**未跑不得写满分**。

Codex 动作：



1. **拟新增** `single_image_baselines.py`。合法基线只能读取与模型相同的单张 PNG、题干与选项；禁止读取 `render_spec`、body mask、target ID、gold、pair ID、A 侧答案或 source record。推荐先做确定性的全图颜色分割：排除接近白色背景与小面积文字 / 引线颜色后，将剩余高饱和像素映射到四个公开选项色原型；算法、阈值与失败规则必须在看模型结果前冻结。

2. 先用合成小图测试证明该程序确实只消费 model-visible bytes；再跑全部 146 个 Color endpoints，记录逐题输出、失败与 A\_acc / NewAcc / Both。**结果未知，不预判满分**。

3. 如果无法构造不依赖私有 mask 的可靠基线，保留为 `not-implemented`，不要降级为使用评测器私有区域。

4. 论文措辞把 Color 定位从 "reference selection" 改为 "appearance sanity track"：它测模型是否跟随当前渲染颜色，不宣称测到 "在多候选间正确选择指代"。

### 2.3 no-image 条件的正确解释

Main 已核验：no-image 去图后，140/140 pair 的 A/B messages 文本完全相同，但 gold 不同。因此若模型确定性响应：



* A 与 B 必然答同一个选项；

* 两 gold 不同 → Both 必为 0；

* endpoint 平均最多 1/2。

Codex 动作：



1. 在 `analyze.py` 的 no-image 报告段（L237 附近）加显式注释："when the stripped A/B requests are byte-identical and decoding is deterministic, joint Both is mechanically 0 because the two golds differ; symmetric endpoint accuracy is at most 1/2. This is an image-content dependency floor, not proof of reference selection."

2. 论文 §5.4 或 §6 加一句："The no-image condition provides an image-content floor, not a reference-selection floor."

3. **不得**把 visual-no-image Both 差独立写成 "指代跟随证据"。

### 2.4 决策点：Part-type reference selection 走哪条路

Codex 必须在此暂停并向 Main 报告，不得自选：

**路线 A（收窄主张，最小工程）**：



* 将 Part-type 准确限定为 “answer-changing candidate-label reassignment 下的 paired correctness”。

* 承认没有 answer-preserving nuisance control 时，无法单独估计不应改变答案时的错误更新率，因此不扩大为一般 reference robustness。

* 不新增刺激，现有 v3 字节与 QA lineage 保持冻结。

**路线 B（新增最小 invariance control，推荐但工作量大）**：



* 新增一组 Part-type **answer-preserving** control：交换两个**错误**候选的显示标签，使正确答案不变。

* 在这种 control 上错误改答案，表示系统对与正确指代无关的标签变化不稳健；与 answer-changing pair 联合报告，才能区分 “该更新时更新” 和 “不该更新时保持”。它仍是行为证据，不直接揭示内部机制。

* 工作量：候选可行性筛查（逐 pair 找两个视觉可区分的错误候选）、平衡无新 shortcut、重渲、hash、全量 QA、受影响 run 重跑。

Codex 动作：



1. 先做可行性筛查：遍历 67 个 Part-type parent，看每个 parent 有多少对**非正确**候选标签可交换，并记录候选是否均已在当前 operand set、投影标签是否可见、交换是否保持唯一 gold。机器检查只能判结构条件，视觉可区分性留待盲审。

2. 把所有 parent（包括零可行候选）写入 `part-type-invariance-feasibility.json`，报告 pair/source/author 覆盖和缺失模式，不设置拍脑袋的数量门槛。

3. Main 根据覆盖是否足以支撑目标主张、是否偏置到少数来源以及新增 QA / 运行成本选择路线 A/B。**Codex 不擅自决定**。

4. 若选路线 B，禁止修改 evidence-v3 冻结观察：创建新的 study version（例如 evidence-v4），重新冻结 observation IDs、hash、QA 包、roster 与受影响 run。

### 2.5 position-reference control 的措辞



* 论文已诚实写 "changes several factors at once"。Codex 不改设计，只在 §5.3 加一句："This control cannot isolate geometry vs position; it is descriptive only."

### 机器验收



* 两个 ledger 分别严格 347 行与 219 行，主键唯一，合并覆盖 566 个冻结 observation，无重复 / 遗漏。

* Color 合法单图 baseline 逐题结果已填入 visual ledger；若无法在不使用私有字段时实现，则状态为`not-implemented`并说明原因。

* `part-type-invariance-feasibility.json` 存在。

### 人工验收



* Main 确认 Color 定位措辞收窄。

* Main 决策路线 A/B。

### 失败停止



* 可行性筛查无法在 67 pairs 上完成 → 停止，报告阻塞点。



***

## Phase 3：QA subset 统计同口径

**目标**：`analyze.py` L275 的 `answer_position_baselines` 现在加载全量 audit，但模型结果按 `qa_both_decidable` 子集报告。必须按同一 subset 重算 baseline。

### 输入



* `analyze.py` L69–72 (`family_report`), L91–119 (`comparisons`), L275 (`answer_position_baselines`)

* `answer-prior-audit.json`

* QA 冻结 snapshot（Phase 4 完成后才有；Phase 3 先实现函数与合成反例测试，真实集成在 Phase 4 后执行）

### 允许修改



* `analyze.py`：把 L275 的全量加载改为按当前 subset 重算。

* 新增 `test_qa_subset_priors.py`：反例单测。

### 禁止修改



* 不改 Phase 2 的 67 题平衡结论。

* 不要求 QA subset 继续满足旧 .40 设计门 ——.40 是全量设计门，subset 失衡只报告，不报错。

### 逐文件动作

#### 3.1 新增函数 `priors_on_subset(family_audit, subset_pair_ids)`



* 输入：单个 family 的 `baselines[*].per_pair` 明细与当前 subset 的 pair\_id 集合；不要只传已经聚合的数值。

* 逐 baseline 按 pair\_id 筛选后，复用现有`estimate()`重算 A\_acc / NewAcc / Both 的 micro、equal-source、interval 和 source coverage。

* 同时由筛选明细重算 A/B marginals 与 transition matrix。source weighting 沿用`estimate()`的现有等 source 定义，不额外传入一套可漂移权重。

* 输出保留每条 baseline 的`access`（no-image/text-only/oracle-A-no-B-image），防止把 oracle 审计与合法模型输入基线混报。

#### 3.2 修改 L275



```
\# 旧:

"answer\_position\_baselines": load(DATA/"answer-prior-audit.json")\["families"],

\# 新:

"answer\_position\_baselines": {

&#x20;   "full": load(DATA/"answer-prior-audit.json")\["families"],

&#x20;   "qa\_both\_decidable": priors\_on\_subset(

&#x20;       load(DATA/"answer-prior-audit.json")\["families"],

&#x20;       selected\_pair\_ids)

},
```

#### 3.3 反例单测

新建 `test_qa_subset_priors.py`：



* 用小型合成 rows 直接测试 subset 函数，不伪造 “真实 human-qa” 文件；另由现有 QA synthetic fixture 测试端到端连接。

* 人为选择会让 fixed-A 命中改变的 pair 集合，断言 full/subset 的 n、sources、marginals、transition 与 fixed-A NewAcc 按明细精确重算；不要写 “约等于 0.25” 这类不确定断言。

* 断言 subset 上的 oracle 规则不继承全量设计门，差异只报告、不触发篡改题目。

### 机器验收



* 新单测通过。

* `analyze.py` 在合成 fixture 上输出 full 与 subset 两个 key；这是 Phase 3A 代码门。

* Phase 4 生成真实 QA snapshot 后执行 Phase 3B 集成门：用真实 selected pair IDs 重算并锁定 subset baselines，核对 pair/source coverage。未完成 3B 不得进入 Phase 5 live runs。

* 论文 caption 修改延后到 Phase 6，但 Phase 3 输出必须提供可直接生成 caption 的 n/source/baseline 元数据。

### 人工验收



* Main 确认论文不会出现 "全量 baseline vs 筛选模型" 混报。

### 失败停止



* subset 与 full 有任何差异都如实记录；若差异改变论文结论或来源覆盖，停止自动发布并交 Main 解释。不得用任意百分比阈值决定是否报告。



***

## Phase 4：人审与每题视觉验收

**目标**：在任何 visual /no-image live inference 之前，完成 347 个视觉 observation 的 694 份独立判断；219 个图 observation 不做视觉人审，走独立算法 gold 与输入合同审计。

### 输入与真实状态



* `benchmark/ldraw-evidence-v3/qa/initial/`：已含 6 个冻结 reviewer queue、private mapping 与 pending summary；不是 “空目录”，只是尚无真人反馈。

* `qa.py`：6 reviewer parent-disjoint；每个视觉 observation 两份判断。

* Phase 2 的视觉台账、图台账。

### 禁止修改



* 不抽样替代 347 个视觉 observation 的全量初审。

* 不把机器检查写成视觉唯一性认证。

* 不把 219 个纯文本图输入塞给视觉评审员；图 gold 必须由当前 BFS/union-find 双实现和输入重建全量验证。

* 不删除 raw review；任一 final decidable choice 与机器 gold 冲突时，该 item 回 pending。

### 4.1 人审逐题流程



1. 对 6 个现有 reviewer 包先运行现有 mapping/queue hash 校验，不重新随机分配。

2. 每位真实评审者完成其 115/116/114/115/115/119 条队列；每条保存 decision、visual choice、4 checks、reason、timestamp、native-size/independence attestation。

3. 用 `qa.py` 的现有 combine 入口导入反馈。执行前先运行 `$PY benchmark/suite/ldraw-evidence-v3/qa.py --help`，只使用帮助中真实存在的参数。

4. decision、choice 或任一 check 不一致时进入独立 adjudication；裁决人不得看同 parent 其他观察。

5. 人类最终 choice 与 generated gold 冲突时停止该 item：核查图、题干、显示映射和 gold；若需改数据，创建新 observation/hash 并重新双评，不能静默换答案。

6. 把每个视觉 observation 的两份原始判断、裁决、最终状态和排除理由写回视觉台账。

### 4.2 每个视觉 observation 验收清单（347 条逐条）



* [ ] observation-index 中的 wire/image hash 与文件一致

* [ ] PNG 为 1280×800 且可读取；题干、options 和图片与 review queue 一致

* [ ] machine gold 由 source/render contract 独立重算

* [ ] target reference 唯一

* [ ] exactly one option visually correct

* [ ] visibility sufficient

* [ ] no reference contradiction

* [ ] 两份真人判断齐全，分歧已裁决

* [ ] 最终状态不是 pending；若 nondecidable，保留原因并仍进入 full denominator

* [ ] source /primary author /contributor cluster 已绑定

### 4.3 每个图 observation 验收清单（219 条逐条）



* [ ] wire hash、node list、edge list、deleted node、最大合法输出一致

* [ ] duplicate edge 处理与合同一致

* [ ] BFS 和 union-find 独立重算 gold 且相等

* [ ] strong/degree-visible/change/invariance role 与 partition 一致

* [ ] shallow baseline 逐题预测和 abstention 状态存在

* [ ] 不声称人类视觉可答性或物理连接真实性

### 机器验收



* QA 重建报告：347 endpoints、694 raw reviews、cross-parent exposure=0；所有分歧有合法裁决，所有 gold conflict 仍 pending。

* 图审计：219/219 双算法 gold 一致。

* 仅当所有 planned 视觉 endpoint 有 nonpending final decision 后，live visual/no-image gate 才开放。

### 失败停止



* 任一 gold conflict 或缺失判断都阻塞对应 live run；不得设 “允许少量冲突” 的比例。

* 发现 queue/hash 变化即整个相关 review lineage 作废，重新导出新版本。



***

## Phase 5：逐模型运行链、2,739 条结果接入与题级诊断

**目标**：在 Phase 4 人审门通过后，完成 3 个冻结模型 × 3 conditions = 9 runs；为每个计划请求建立一条可审计记录。总调用数为每模型 347 visual + 347 no-image + 219 graph = 913，三模型合计 2,739。

### 输入



* `model-roster.json` / `roster-lock.json`

* `adapters/gpt41.json`、`gpt4o.json`、`gpt4o-mini.json`

* `run.py`（真实 CLI：`run`、`verify`、`close`）

* 已完成的 human QA snapshot

### 禁止修改



* 不给 v3 roster 追加模型；跨 provider / 开源扩展创建新 study version。

* 不替换失败 run、不 resume 不明确的远端调用、不挑最好的一次。

* 不添加 roster 未声明的 top\_p/seed；真实 request 只含 transport.py 生成的 model/messages/temperature/max\_tokens/stream。

* Codex 本身不启动付费调用；它只完成预检、命令清单、验证与真实结果导入。用户在有凭证环境执行 live run。

### 5.1 三个模型各自的冻结核查



| model\_id    | expected served revision | visual | no-image | graph | calls |
| ------------ | ------------------------ | ------ | -------- | ----- | ----- |
| `gpt41`      | `gpt-4.1-2025-04-14`     | 347    | 347      | 219   | 913   |
| `gpt4o`      | `gpt-4o-2024-08-06`      | 347    | 347      | 219   | 913   |
| `gpt4o-mini` | `gpt-4o-mini-2024-07-18` | 347    | 347      | 219   | 913   |

对每个模型逐项：adapter\_file\_sha256、adapter\_hash、endpoint、requested/served revision、max\_tokens=128、timeout=90、temperature=0、one attempt/no retry、QA snapshot hash。

### 5.2 真实命令骨架（执行前必须先看 `--help`）



```
PY=benchmark/.runtime/mlx-env/bin/python

\$PY benchmark/suite/ldraw-evidence-v3/run.py --help

\$PY benchmark/suite/ldraw-evidence-v3/run.py run --help

\$PY benchmark/suite/ldraw-evidence-v3/run.py verify --help

\$PY benchmark/suite/ldraw-evidence-v3/run.py close --help

\# live run使用roster固定root和自动生成的run\_id；visual/no-image必须传冻结QA：

运行时在当前shell中设置BRICKATLAS\_API\_KEY后执行 \$PY benchmark/suite/ldraw-evidence-v3/run.py run \\

&#x20; \--model gpt41 --condition visual --qa /absolute/path/to/final-human-qa.json --live

\# verify的真实位置参数：directory output；output必须不存在

\$PY benchmark/suite/ldraw-evidence-v3/run.py verify \\

&#x20; benchmark/ldraw-evidence-v3/model-runs/gpt41-visual-r1 \\

&#x20; benchmark/ldraw-evidence-v3/model-runs/gpt41-visual-r1-verified.json

\# 仅中断且仍running的run使用close；正常complete不得再close

\$PY benchmark/suite/ldraw-evidence-v3/run.py close \\

&#x20; benchmark/ldraw-evidence-v3/model-runs/RUN\_ID --reason "填写真实中断原因"
```

依次替换 model 和 condition，严格完成 roster 的 9 个 run。不要使用文档中不存在的`--out`、`--run-dir`。

### 5.3 2,739 条 run-observation 台账

新建**派生**文件 `run-observation-ledger.jsonl`，每行一个 `run_id × observation_id`，至少含：



```
{"run\_id":"gpt41-visual-r1","model\_id":"gpt41","condition":"visual",

&#x20;"observation\_id":"从对应run manifest.requests读取","family":"从validated row读取","pair\_id":"由visual-manifest关系连接；graph按graph audit连接","arm":"A",

&#x20;"request\_sha256":"从run manifest读取","attempt\_file":"从run目录派生","attempt\_sha256":"对attempt文件计算",

&#x20;"receipt\_file":"从validated row读取；无receipt时为null","receipt\_sha256":"有receipt时计算，否则null","http\_status":200,

&#x20;"served\_revision":"从provider raw response校验后读取","raw\_output":"从receipt解析，缺失时为null",

&#x20;"parsed\_answer":{"choiceId":"C"},"valid\_format":true,"failure\_reason":null,

&#x20;"gold":{"choiceId":"C"},"success":1,"qa\_decidable":true,

&#x20;"source\_id":"从validated row读取","primary\_author\_id":"从source-dependence连接","contributor\_cluster":"从source-dependence连接"}
```

此 ledger 只从 immutable manifests/attempts/receipts/QA/gold 派生，不能成为新的权威状态；修改它不应影响评分。raw provider response 仍以 receipt 文件为准。

### 5.4 每个 run 和每道题的验收



* 每个 run：initial/terminal manifest 一致，request 数量符合计划，每个 request 只有一个 pre-call intent；complete 时每题有 receipt，closed-interrupted 时 closure 明确列出 unattempted 和 attempted-without-receipt。

* 每题：request bytes 复现冻结 wire+adapter；served model 等于 roster；strict JSON 解析；timeout/refusal/API/invalid/missing 分类并留在分母。

* 每 pair：visual 与 no-image 分别重建 AAcc/NewAcc/Both/R\_old/other\_wrong/invalid；Color 和 Part-type 分开，不与 graph pooled。

* 每模型：full 与 QA subset、source macro、author/contributor sensitivity、failure breakdown、真实 case selection 均来自相同 receipts。

### 5.4.1 每个模型的逐观察关账矩阵

Codex 必须为三个模型各生成一张 913 行完成矩阵（可由 JSONL 筛选得到），按冻结 input 顺序列出：



* visual 347：每一行含 family/role/arm、QA final、request/attempt/receipt、parse、gold、success、failure；position-reference auxiliary 单独标记，不进入 primary Both。

* no-image 347：验证除 image block 外消息完全相同；逐观察连接对应 visual observation，保存 answer 是否变化，但不把变化本身等同正确。

* graph 219：保存整数 prediction、validity、gold、partition 和 pair membership；与视觉结果不合并。

* 每个 primary pair 再生成一行 pair ledger，列 A/B 两侧输出及`correct→new-gold`、`correct→old-gold`、`wrong→new-gold`、`same-valid-wrong`等互斥分类。

* 在最终发布前，分别断言三个 913 行矩阵主键完整；全局 2,739 行无重复、无未解释缺失。中断项也有一行并携带 closure 原因。

### 5.5 分析接入



1. 9 个 run 必须 terminal；extra/missing run 阻止 analysis。

2. 执行 `analyze.py --help`，按真实位置参数和`--run-root`生成新 analysis snapshot；不得覆盖旧文件。

3. 生成 model-run-index 并验证 9 行、2739 个计划请求、同一 QA snapshot。

4. Phase 3 的 full/subset baselines 与对应模型分母并排发布。

5. 不把 rank reversal、任何准确率或失败比例预设为成功门槛。

### 失败停止



* served revision mismatch：run 不可伪装为计划模型，按当前验证失败上报；是否创建新 study version 由 Main 决定。

* provider 不可用：保留真实中断 / 失败，不删除目录，不用另一模型替代。



***

## Phase 6：论文重写与图表

**目标**：把论文从 "修复叙事" 重排为 "科学发现 + 测量协议"。

### 输入



* `main.tex`（616 行）

* Phase 1–5 的产出

### 允许修改



* 在新论文版本或获准的工作分支上修改 `main.tex` / `supplement.tex` 源稿。

* 修改表格生成逻辑及其源数据；`generated/` 是产物，禁止只手改表文件而不改生成源。

* 不删已诚实声明的 limitations。

### 禁止修改



* identity 语义（§3.2 L177–201）不动。

* 不写 "首个"。

* 不预设 rank reversal 或数字阈值。

### 6.1 章节重排



* Intro 贡献段：三条增量（referent contract /pre-registered shortcut audit /receipt-derived transition），把 "修复 v2 first-non-A" 移到 §7 footnote。

* §2 加 VisualFLIP 对比（Phase 1）。

* §4.3 把 Color 定位为 appearance sanity track；Part-type 定位为 reference selection（或按 Phase 2 决策收窄）。

* §5.4 no-image 注释加 "image-content floor, not reference floor"。

* §5.5 roster 表注脚："3 OpenAI models, transport-controlled; not a cross-provider leaderboard."

* 在 “Human Qualification and Response Analysis” 之后新增 / 更新真实模型结果节（不要与现有 Graph §6 混号）：AAcc / NewAcc / Both / R\_old /valid-format/family-separated /source-macro/author sensitivity。

* §7 limitations：保留 identity 语义、.40 是全量设计门、subset 不继承、24 sources / 18 authors。运行状态由当前 analysis artifact 生成：有真实结果后替换协议占位，绝不手工删除或编数字。

### 6.2 图表



* Table `tab:priors`：caption 注明 full 与 qa\_both\_decidable 两列。

* Table `tab:roster`：3 models × 3 conditions = 9 runs。

* 新增 Table：逐模型 failure breakdown（timeout/refusal/invalid）。

* 不新增 pooled visual score。

### 机器验收



* `tectonic` 编译通过。

* 所有 `\ref` 有目标。

* 无 undefined citation。

### 人工验收



* Main 确认贡献段不再以修复叙事为主。

* Main 确认 VisualFLIP 对比矩阵无编造。



***

## Phase 7：交付复现门

**目标**：把 "编译通过 / 离线 wire 验证 / 全资产重建" 三层分开写清。

### 输入



* `BUILD.md`

* `publication.py`（L77 读 v1 figure, L205 读 v1 bib）

* `package-validation.json`

### 已核实事实



* `references.bib` 是生成产物；字节核对已确认 v3 文件等于 “v1 base bib + 换行 + v3 additions.bib”。`publication.py` 读取 v1 base bib 是显式生成逻辑，不是内容错误；真正问题是全资产重建对旧路径的传递依赖未在自包含材料中闭合。

* v1 `given-order-replay.pdf` 被 supplement Fig 2 引用；该文件在 v1 目录，不在 v3 sealed zip。

* 论文 ZIP（29 files）含预生成 figure/bib/generated tables，可独立编译 PDF。

* 全资产重建需要 observations + suite + adapters + renders，以及可安装、版本受控的 Python/TeX/Node 依赖说明；无需捆绑虚拟环境、Node 二进制或 node\_modules。

### 7.1 BUILD.md 分层

改写 BUILD.md 为三节：

**A. 编译 PDF（最轻）**：



* 仅需 tectonic。

* 输入：paper/evidence-v3/ 全部 29 文件（含预生成 figure 与 generated tables）。

* 命令：`tectonic main.tex && tectonic supplement.tex`。

* 不依赖 observations /suite/adapters。

**B. 离线 wire 验证（中等）**：



* 需 Python + sealed 905 文件。

* 先分别运行各脚本 `--help`（若脚本无 help 则读其 argparse/main），再执行 `verify_publication.py`（无 `--render`）、`wire_audit.py` 和 unittest；不得猜位置参数。

* 当前已在作者本机跑通；隔离空环境未验证。

**C. 全资产重建（最重）**：



* 需 Python + Node + 所有运行时。

* 先查每个入口的真实参数，再执行 `publication.py`、`preserve.py`、`tsc -b`。

* **显式记录**：publication.py 当前从 v1 读取历史图和 base bib。不要改成自读 v3 输出 bib；按 7.2 把两项都变成可恢复、带 hash 的 v3 输入，或清楚声明历史归档恢复步骤。

### 7.2 闭合 base bib 与历史图的传递依赖



* **禁止**把 `publication.py` 改为读取输出文件 `evidence-v3/references.bib` 后再覆盖它，这会造成自读取 / 重复追加。

* 推荐在 v3 源目录新增只读 `base-references.bib`（从当前已核验的 v1 base 固化并记录 SHA-256），让生成器读取 `base-references.bib + additions.bib`，输出 `references.bib`。增加幂等测试：连续生成两次，`references.bib` 字节不变且每个 bib key 唯一。

* 对 `given-order-replay.pdf` 同理：将已核验历史图作为带 provenance/hash 的 v3 输入资产，或在 BUILD 中提供历史归档恢复命令；生成器不再依赖作者目录里碰巧存在的 v1 路径。

### 7.3 不做的事



* 不捆绑 venv。

* 不捆绑 node\_modules。

* 不要求第三方安装相同 Python 版本；BUILD.md 只声明 checked runtime。

### 7.4 干净目录回放（Codex 执行）



```
\# 建临时目录，只解压 sealed 包

mkdir -p /tmp/brickatlas-repro && cd /tmp/brickatlas-repro

\# 解压 paper source zip + delivery-manifest 覆盖的 905 文件

\# 尝试 B 层命令

env -u PYTHONPATH python benchmark/suite/ldraw-evidence-v3/verify\_publication.py
```

记录哪些步骤在干净目录失败。不要求全部通过；要求**如实记录**。

### 机器验收



* BUILD.md 三节分离。

* publication.py 的 base bib 与历史图依赖可从声明的 v3 输入或公开归档恢复；references 生成幂等。

* 干净目录回放结果写入 `repro-attempt.md`。



***

## 附录 A：MUST / SHOULD / OPTIONAL



| 项                                       | 优先级                       |
| --------------------------------------- | ------------------------- |
| Phase 0 分支隔离                            | MUST                      |
| Phase 1 VisualFLIP fetch + 贡献重写         | MUST                      |
| Phase 2 audit-ledger 全题 + Color 定位收窄    | MUST                      |
| Phase 2 Part-type invariance control    | SHOULD（看可行性）              |
| Phase 3 QA-subset prior 重算 + 单测         | MUST                      |
| Phase 4 全量视觉人审 + 图输入机器验收                | MUST                      |
| Phase 5 9 runs / 2739 条结果接入             | MUST                      |
| Phase 6 论文重排                            | MUST                      |
| Phase 7 BUILD 分层 + base bib / 历史图传递依赖闭合 | MUST                      |
| 跨家族新模型                                  | OPTIONAL（新 study version） |
| 第三视觉属性                                  | OPTIONAL（future work）     |
| 跨模板 strong graph pairs                  | OPTIONAL                  |

## 附录 B：最小可投稿路线

若时间紧张，最小可投稿路线为：



1. Phase 0 + Phase 1（补 VisualFLIP + 贡献重写）。

2. Phase 2 路线 A（收窄 Color/Part-type 主张）+ audit-ledger。

3. Phase 3（QA-subset prior 重算）。

4. Phase 4 先完成人审与图审计，再由用户环境执行 Phase 5 的 9 个 live runs 和结果接入。

5. Phase 6（论文重排）。

6. Phase 7（BUILD 分层 + base bib / 历史图传递依赖闭合）。

不做 Part-type invariance control、不加第三属性、不加新模型。

## 附录 C：Codex 每阶段报告模板



```
phase: 填写阶段编号与名称

status: 只能填写 PASS 或 FAIL

objective: 用一句话填写本阶段目标

inputs: 列出实际读取文件

allowed\_scope: 列出实际授权范围

changes: 粘贴实际 git diff --stat 并列出新增产物

machine\_verification: 粘贴命令、退出码与摘要

human\_verification: 填写评审人及结论；未完成则为 pending

failures\_and\_rollback: 填写真实失败及恢复点；无则写 none

next\_stage: 仅当前阶段PASS后填写下一阶段
```