# BrickAtlas LDraw-1 Benchmark 分阶段升级指导（Codex 实施手册）

> **文档版本**：v1.0-draft  
> **生成日期**：2026-09-18  
> **适用对象**：Codex（自动化代码/论文/数据升级执行器）  
> **项目根目录**：`/Users/bytedance/Documents/trae_projects/brick-atlas`  
> **本文档性质**：只读指导文档，不修改现有论文/代码/数据/实验状态。所有升级操作由 Codex 按阶段执行，每阶段须过质量门方可继续。

---

## 0. 文档元信息与保护声明

### 0.1 证据状态分类

本文档中所有陈述按以下三类标注：

- **【已核验】**：有代码/数据/论文原文直接证据，路径和行号可追溯。
- **【假设】**：基于设计逻辑的推断，尚未经实验或全量数据验证。
- **【待实现】**：当前不存在，需 Codex 新增设计或代码。

### 0.2 Codex 执行纪律（必须遵守）

- 一次会话只执行一个 Phase。进入阶段前先读取该阶段列出的全部输入与现有脚本 `--help`；不得猜命令参数。
- 先创建阶段分支/隔离目录和阶段验收清单，再修改文件。不得一口气执行 Phase 0–5。
- 阶段结束时运行本阶段全部机器验收，生成 `PHASE-{N}-REPORT.md`，列出文件差异、命令、结果、失败项和未解决歧义，然后停止等待人工确认。
- 质量门未通过时只修当前阶段；禁止用论文改写掩盖数据、代码或测量失败。
- `【已核验】` 只表示本指导编写时核验过；Codex 仍须在当前工作树重新验证。

### 0.3 保护声明（必须遵守）

1. **v1 实验保护**：论文实验计划当前仍为 `proposed-not-run`；若另有模型实验正在运行，必须以其真实运行清单和请求快照为准。不得原地修改 `public/benchmark/ldraw/inputs/*.json`（模型侧公开输入）、`public/benchmark/ldraw/models/*.json`（含答案的内部评审/评分 bundle）、`benchmark/ldraw-v1/` 或 `benchmark/suite/ldraw/questions.ts`。所有升级在独立版本命名空间下进行，旧结果只能标为对应版本结果，不能静默迁移。
2. **原始资产保护**：`benchmark/ldraw-v1/sources/` 下的原始 LDraw/OMR 文件（含 SHA256、作者、许可证）不得修改。升级版本引用原始源但不覆盖。
3. **不编造数据**：未运行的实验结果保持空白，不得用零、占位符或历史 pilot 分数填充。
4. **不启动模型训练**：本文档不要求任何模型训练或微调。所有"模型实验"指在冻结题集上运行现成 MLLM API 的推理评估。
5. **不伪造物理标注**：涉及物理真实性、重力稳定性、接触力的内容，保留不确定性，不得伪精确。

### 0.4 关键路径速查

| 组件 | 绝对路径 |
|------|---------|
| 题目生成器 | `benchmark/suite/ldraw/questions.ts`（192行） |
| 评分器（批量） | `benchmark/suite/ldraw/score.ts` |
| 动作执行引擎 | `src/benchmark/engine.ts`（含 `replay()`、`score()`、`solveActions()`） |
| 冻结模型侧公开输入 | `public/benchmark/ldraw/inputs/{modelId}.json`（24个文件；任务已去除 `answer` / `evidenceDetail`） |
| 冻结内部评审/评分 bundle | `public/benchmark/ldraw/models/{modelId}.json`（24个文件；含参考答案，不得直接作为模型输入） |
| 源目录 | `benchmark/ldraw-v1/` |
| 论文主文件 | `benchmark/paper/main.tex`（552行） |
| 实验计划 | `benchmark/paper/ldraw-experiments.json`（9张表，全部null） |
| 评估协议 | `benchmark/ldraw-v1/PROTOCOL.md` |
| CLI 入口 | `npm run --prefix benchmark ldraw:build / ldraw:verify / ldraw:score / ldraw:publish` |
| 任务类型定义 | `src/benchmark/ldrawTypes.ts` |
| 参考文献 | `benchmark/paper/references.bib` |

---

## 1. 科学定位与主张校准

### 1.1 当前定位问题【已核验】

论文标题为 "BrickAtlas LDraw-1: Instance-Grounded Visual and Structural Reasoning over Original Brick Assemblies"，摘要和引言暗示测量综合装配推理。但代码核验表明：

- 11个任务族中，每族的 `input` 仅含单一模态（V/S/G/E 四选一）【已核验：`questions.ts` 全文】。
- 不存在任何单题要求模型联合完成视觉定位→图推理→场景编辑【已核验】。
- 在当前生成器中，9/11 族的目标证据由 `input` 明确提供；这些题分别测量字段读取、表格查找、数值/图运算或动作契约执行，而不是视觉感知【已核验】。
- 仅 Color（73题）和 Part-type（67题）的 `input` 为 `{}`，需依赖 `visualInput` 中的编号渲染图【已核验：`questions.ts` L40, L50】。

### 1.2 推荐定位【假设，需论文改写验证】

将基准定位从可能被读成“端到端综合装配推理”的表述，明确为：

> **跨观测契约、实例对齐的模块化评测基准**：在不变的原始 LDraw 源装配上，用同一实例 ID 对齐视觉渲染（V）、源数据记录（S）、连接器图（G）和可执行场景编辑（E）四种观测契约，分别测量同一个零件实例上的视觉识别、证据读取、图运算与执行契约遵循。只有在完成受控故障注入、非目标模块稳定性和证据恢复实验后，才能进一步声称具有“错误归因/诊断定位”能力。

这一定位可与显式分解推理操作的工作形成对话，但不得直接声称为 CLEVR 的跨模态类比或“故障定位仪”，除非文献对比和诊断效度实验均已完成。

### 1.3 必须收窄的主张【已核验+待实现】

| 当前主张（原文位置） | 问题 | 推荐改写方向 |
|----------------------|------|-------------|
| "visual and structural reasoning"（标题） | 容易被读成跨模块综合推理 | 在诊断效度未完成前用 "modular evaluation of visual, source-data, graph and scene-edit competencies"；实证通过后再考虑 diagnostic |
| 贡献段三条交付物描述（main.tex L81-89） | 尚未实证“为何重要” | 改为“实例对齐支持可审计的模块化比较”；完成诊断干预后才可升级为“错误归因可分” |
| Table 1 仅 "Setting \| Evaluation object"（main.tex L123-139） | 未说明差异为何重要 | 加“研究问题 / 所需观测契约 / 本文是否已验证”列；避免替邻近工作断言其“不能回答什么” |
| "Integrative"层标签（main.tex L226-227） | 仅含 G-only 的 Graph deletion，非跨模态 | 改名 "graph-internal" 或加脚注明确 |
| Abstract "real 3D inputs"（main.tex L28-29） | 暗示单题需理解完整3D场景 | 加"single items are operand-isolated; source scale measures corpus diversity, not per-item difficulty" |

### 1.4 与邻近工作的差异：当前证据边界【部分核验】

| 工作 | 当前可支持的表述 | 仍须核验后才能写入正文 |
|------|------------------|------------------------|
| BrickNet（CVPR 2026） | 本文已经实际复用其公开连接器实现来审计固定源放置；本基准的评测对象是固定源上的问题与场景编辑，而非生成结果【本地全文已读】 | 更细的表示、索引和评测能力差异须逐节对照，不得声称其“没有实例ID”或“不能问答” |
| LEGO-Puzzles（2025） | 本文当前把它定位为空间推理评测；LDraw-1 额外显式提供源记录/连接器图/编辑契约【仅有引用页与当前论文陈述】 | 实例引用方式、任务分层、是否支持错误区分须读取并引用全文后确认 |
| PhyBlock（2025） | 其在自身仿真契约下评测物理理解与规划；LDraw-1 明确采用更窄的图与显示编辑语义【当前论文与摘要层证据】 | 数据生成方式、任务分支和错误分类细节须全文核验后确认 |

**Codex 规则**：Table 1 和 Related Work 只能写已核验事实。凡没有全文证据的单元格标为 `to verify`，不得用“无/不能/首个/唯一”补齐。
---

## 2. 已确认的测量效度问题（P0 修复项）

### 2.1 四个已实证 Shortcuts【已核验：Main 在冻结公开题集上独立只读预测确认】

| # | 任务族 | 题数 | Shortcut 机制 | 代码位置 | 冻结题集验证 |
|---|--------|------|---------------|---------|-------------|
| S1 | graph-removal | 73 | 正确答案恒为数值选项第二小。`numbers(n)` 构造 `[n, max(0,n-1), n+1, n+2]`，n≥1 时排序后第二小恒为 n | `questions.ts` L33, L110-113 | 73/73 |
| S2 | source-step | 55 | 同上，`i+1 ≥ 1`，正确答案恒为第二小数值 | `questions.ts` L33, L143-146 | 55/55 |
| S3 | shape-match | 67 | `references[1]` 恒为正确答案（同型零件）。refs = `[target, same, ...distractors]`，references 数组按此顺序序列化 | `questions.ts` L43-51 | 67/67 |
| S4 | neighbors | 73 | `references[1:-2]` 恒为正确邻居集合。refs = `[target, ...neighbors, ...distractors(2)]` | `questions.ts` L82-96 | 73/73 |

**影响范围分两层**：
- S1+S2（128/617）仅依赖模型侧公开输入中的数值选项，确定是现有 `inputs/*.json` 可用的非目标捷径。
- S3+S4（140/617）依赖 `references` 的有序数组。该字段存在于当前模型侧 `inputs/*.json`，但是否实际传给正在运行的模型必须以保存的真实请求体为准。
- 四条规则合计可在冻结模型侧公开输入上预测 268/617 题（43.4%）。这证明“捷径可用”，不证明任何模型已利用它。

`release.ts` 已实现内部 bundle 与模型侧公开输入的分离：
- `public/benchmark/ldraw/models/*.json`：含 `answer` / `evidenceDetail`，供内部评审与现有 scorer 使用；不是模型输入。
- `public/benchmark/ldraw/inputs/*.json`：通过 `publicTask()` 去除 `answer` / `evidenceDetail`，才是协议所称的 public question export。

因此 P0 不是“尚未实现答案字段剥离”，而是：建立唯一的模型请求序列化器，只允许从 `inputs/*.json` 构造请求；对其做字段白名单和捷径测试；保存真实请求快照；禁止把 `models/*.json` 交给模型。

### 2.2 构念效度问题（非 shortcut，但影响测量解释）【已核验】

| 任务族 | N | 实际测量 | 论文声称 | 构念差距 |
|--------|---|---------|---------|---------|
| Interface | 87 | 读取 `input.connectorRecord.family` 字段做字符串匹配 | "Connector record classification" | 论文自认 "evidence reading, not visual contact inference"（main.tex L247-249） |
| Evidence limit | 24 | 语义答案恒为 "not established by this evidence" | "Limits of stability evidence" | 论文自认固定答案（main.tex L258-259, L388-390） |
| Coverage | 17 | 查找 `input.coverage` 中 `supported:false` 的条目 | "Unsupported-instance evidence" | 纯字段查找 |
| Step lookup | 55 | 在 `input.steps` 表中查找目标编号首次出现的 index | "Author step lookup" | 纯表格查找 |
| Distance | 73 | 对 `input.centers` 坐标做欧氏距离算术 | "Nearest instance" | 坐标直给，纯算术；候选非空间邻近（SHA256 随机，`questions.ts` L53） |
| Step sequence | 17 | 跟随线性前驱链 `done-(k-1) → done-k` | "Author step sequence" | 论文自认 "following supplied author order, not discovering a new assembly plan"（main.tex L273-274） |
| Restoration | 58 | 匹配 `input.initialFacts` 中的 `missing-{id}` 到对应动作 | "Restore numbered instance" | `missingInstanceIds` 字段在 input 中（`questions.ts` L184）；论文自认动作族不要求机械规划（main.tex L529-530） |
| Graph deletion | 73 | 在 `input.edges` 局部图上做连通分量计数 | "Components after deletion" | 属于图运算；答案高度集中（60.3% 为 4，【已核验】），且叠加 S1 shortcut；局部图规模分布须由脚本全量重算后再写 |
| Neighbors | 73 | 从 `input.edges` 收集一跳邻居 | "Direct connector neighbors" | 属于图集合运算；叠加 S4 shortcut |
| Color | 73 | 从编号渲染图识别颜色 | "Color identification" | 预期直接测视觉颜色识别；仍需无图/错图对照和逐图人审确认 |
| Part-type | 67 | 从编号渲染图匹配零件形状（忽略颜色/姿态） | "Part-type correspondence" | 预期直接测视觉对应；S3修复后仍需无图/错图对照与近同型逐题人审 |

### 2.3 视觉族输入说明【已核验，纠正前述"输入为空"的过度简化】

Color 和 Part-type 族的 `input` 字段为 `{}`（JSON 空对象），但这不等于"无输入"。`questions.ts` L187-190 在生成末尾为所有 `modality === 'visual'` 的任务附加：
```typescript
task.visualInput = {
  numberedView: `benchmark/ldraw/inputs/views/${task.id}.png`,
  isolationAllowed: true,
};
```
因此视觉族的完整输入 = 空 JSON input + `visualInput.numberedView` 指向的编号渲染 PNG + 题目文本中的 operand B-number 引用。**不得将"input 为 {}"简化为"无输入"**。

---

## 3. 分阶段升级计划

### 阶段总览与依赖关系

```
Phase 0: 版本冻结与隔离（所有后续阶段的前提）
    ↓
Phase 1: 测量效度修复（shortcuts + 字段暴露 + 选项构造）
    ↓ （必须通过，否则后续所有实验无效）
Phase 2: 任务族构念校准（每族输入/输出/评分契约 + 恒答族标记）
    ↓
Phase 3: 跨模块链路设计（可选增强，非必须）
    ↓ （若跳过，论文定位正式收窄为"分模块诊断"）
Phase 4: 证据实验与消融设计（background-mask + 字段剥离 + 鲁棒性）
    ↓
Phase 5: 论文/图表/代码/数据同步
```

**优先级原则**：先修复测量效度（Phase 1），再校准构念（Phase 2），再考虑跨模块（Phase 3，可选），再设计实验（Phase 4），最后改论文（Phase 5）。避免全面膨胀成新项目。

---

### Phase 0：版本冻结与隔离

**目标**：保护正在运行的 v1 实验和原始资产，建立 v2 隔离升级命名空间。

#### 输入
- 当前 v1 模型侧输入：`public/benchmark/ldraw/inputs/*.json`（24个文件）
- 当前 v1 内部评审/评分 bundle：`public/benchmark/ldraw/models/*.json`（24个文件）
- 当前 v1 生成器：`benchmark/suite/ldraw/questions.ts`
- 当前 v1 评分器：`benchmark/suite/ldraw/score.ts`
- 当前 v1 实验计划：`benchmark/paper/ldraw-experiments.json`

#### 可改范围
- **仅新增** v2 目录和文件，不修改 v1 任何文件。
- 新增 `benchmark/suite/ldraw-v2/` 目录（v2 生成器、评分器）。
- 新增 `public/benchmark/ldraw-v2/models/` 目录（v2 冻结题集）。
- 新增 `benchmark/ldraw-v2/` 目录（v2 源数据引用，软链接或复制 v1 源）。

#### 具体产出
1. `benchmark/suite/ldraw-v2/questions.ts`：从 v1 复制，作为 v2 修改起点。
2. `benchmark/suite/ldraw-v2/score.ts`：从 v1 复制。
3. 版本清单文件 `benchmark/ldraw-v2/VERSION.md`：记录 v1→v2 的变更日志、冻结时间、源文件 SHA256。
4. v1 冻结快照：分别将 `public/benchmark/ldraw/inputs/*.json` 和 `public/benchmark/ldraw/models/*.json` 的 SHA256 写入 `benchmark/ldraw-v2/v1-frozen-manifest.json`，并显式标记 `model_input` / `internal_scoring` 角色。

#### 机器验收
- [ ] `benchmark/suite/ldraw/questions.ts` 的 SHA256 与冻结清单一致（未被修改）。
- [ ] 两类24文件的 SHA256 与冻结清单一致，角色没有混淆。
- [ ] v2 目录存在且包含从 v1 复制的文件。
- [ ] `npm run --prefix benchmark ldraw:build`（v1）仍可正常执行，输出与 v1 冻结一致。

#### 人工验收
- [ ] 确认无 v1 实验进程正在写入 v1 目录（检查 `.runtime/` 下的 lock 文件）。
- [ ] 确认 v1 实验结果（如有）已备份。

#### 失败回退/停止
- 如果发现 v1 文件已被修改，**立即停止**，报告修改内容和时间，不得继续。
- 如果 v1 实验正在运行，等待其完成或确认其不读取 v1 题集文件后再继续。

#### 完成后 Codex 报告内容
- v1 冻结清单（24个 model-input 与24个 internal-scoring 文件的 SHA256，另含生成器/评分器/协议哈希）。
- v2 目录结构。
- 确认 v1 未被修改的验证输出。

---

### Phase 1：测量效度修复（P0，必须通过）

**目标**：消除 4 个已实证 shortcuts 和答案字段暴露问题，确保 v2 题集的答案不能从公开输入字段直接推导。

#### 输入
- v2 生成器起点：`benchmark/suite/ldraw-v2/questions.ts`（Phase 0 复制）
- v1 冻结题集（用于对比验证）

#### 可改范围
- 仅修改 `benchmark/suite/ldraw-v2/questions.ts`。
- 修改/复用 v2 的 `release.ts` 与 `publicTask` 等价逻辑，保留 internal-scoring 与 model-input 双产物；新增唯一请求序列化器与隔离测试。
- 不修改 v1 任何文件。

#### 具体产出

**1.1 修复 S1（graph-removal 第二小数值）**

问题代码（`questions.ts` L33）：
```typescript
const numbers = (n: number) => [...new Set([n, Math.max(0, n - 1), n + 1, n + 2])].map(...)
```

- **实现规则（唯一方案）**：生成至少4个互不相同且合法的数值候选；将正确值与干扰值合并后，以与答案无关的独立种子置换**数值语义位置**。干扰值必须来自合法域并通过边界处理，但不得由固定的相对偏移模板决定答案排名。
- `source-step` 的干扰步骤必须落在该源实际步骤范围内；当合法候选不足4个时，改变输出格式或不生成该题，不得使用越界步骤。
- 不通过“增大图规模”修复表示捷径；那会同时改变任务构念。

验证：对每道题验证正确值不由任何固定排名规则、固定相对偏移规则或选项序列位置确定；汇总时报告正确值排名分布，但不以小样本 `p>0.05` 作为通过证据。生成器应通过构造保证每个可用排名的计数差不超过1（若选项数一致），或记录并解释不可避免的边界例外。

**1.2 修复 S2（source-step 第二小数值）**

同 S1，`numbers(i+1)` 用于 source-step（`questions.ts` L146）。修复方案同 S1。注意 source-step 的步骤号有上限（作者步骤总数），干扰项不得超过最大步骤号。

**1.3 修复 S3（shape-match references[1]）**

问题：`references` 数组顺序为 `[target, same, distractor1, distractor2, distractor3]`，references[1] 恒为正确答案。

修复方向【待实现】：
- **必须同时做两层修复**：内部任务对象中的 `references` 先按与答案角色无关的稳定键规范化或独立置换；模型请求序列化器默认不发送 `references`，只发送题目文本已明确引用的目标/候选标签。不能只在最后一步洗牌，因为其他渲染、UI或runner可能直接使用内部任务对象。

验证：内部 `references` 不再保留固定正确角色；最终 request snapshot 默认不含该字段。若保留标签集合，任何固定索引、前缀、后缀或切片规则在逐题审计中均不得命中。

**1.4 修复 S4（neighbors references[1:-2]）**

问题：`references` 数组顺序为 `[target, ...neighbors, distractor1, distractor2]`，references[1:-2] 恒为正确邻居集合。

修复方向：同 S3 的双层规则。目标由题目文本明确引用；邻居与干扰项不得通过内部数组顺序或请求元数据暴露角色。

验证：对生成的 v2 neighbors 题集，正确邻居集合不再等于 references 的任何固定切片。

**1.5 内部 bundle、模型输入与请求快照的强隔离**

现状：`release.ts` 已写出两套文件；`publicTask()` 已从模型侧 `inputs/*.json` 去除 `answer` 和 `evidenceDetail`。问题在于：`references` 顺序仍可能编码答案，现有 scorer 又直接读取 `models/*.json`，因此任何新 runner 都必须显式选择正确一侧。

修复方向【待实现】：
- 保留现有双产物架构，但将目录角色写入 README/类型名/运行器检查：
  - `models/*.json`：`internal-scoring-review`，含答案，只允许 scorer/review 工具读取。
  - `inputs/*.json`：`model-input`，不含答案，runner 只允许读取这一目录。
- 新增一个**唯一**的请求序列化函数（例如 `serializeModelRequest(publicTask, condition)`），用白名单生成实际发给模型的文本、选项、结构化证据和图像引用；runner 不得 `JSON.stringify(task)`。
- 模型请求默认移除 `references`、`targetModule`、`capabilities`、`evidence` 等非必要元数据。若某条件确需 operand 列表，只发送无角色、无顺序语义的标签集合，并在协议中声明。
- 每次运行保存最终请求快照及其哈希；实验报告基于请求快照判断字段是否暴露，而不是根据仓库文件位置猜测。
- CI 检查 model-input 和 request snapshot 都不含 `answer` / `evidenceDetail`，且 internal bundle 的路径不能进入 runner。

验证：
- [ ] `inputs/*.json` 和实际 request snapshot 均不含答案字段。
- [ ] 公开 `references` 顺序规则在 request snapshot 上不可执行。
- [ ] scorer 继续只使用内部 bundle 正确评分，runner 只使用 model-input。
- [ ] deliberate canary 字段写入 internal bundle 后绝不出现在 request snapshot。

#### 机器验收
- [ ] 对 v2 实际生成的全部题运行 shortcut 检测脚本（Codex 须新增 `benchmark/suite/ldraw-v2/shortcut-check.ts`）：
  - graph-removal / source-step：固定第二小、固定第 k 小、固定相对偏移等预注册规则必须逐题失败；排名计数由构造保证平衡或记录合法域例外。
  - shape-match / neighbors：`references` 不进入模型请求；同时内部顺序不得保留固定答案角色。
- [ ] 对**最终 request snapshot**运行 only-public-feature baselines；禁止只检查中间 JSON。
- [ ] 模型输入与内部评分 bundle 隔离验证：request 无 `answer` / `evidenceDetail`，canary 不可达。
- [ ] v2 题集可通过 `ldraw:build` 和 `ldraw:verify`（v2 版本命令）。
- [ ] v1 题集未被修改（SHA256 与 Phase 0 冻结清单一致）。

#### 人工验收
- [ ] 抽查 10 道 v2 题（每族至少 1 道），人工确认答案不能从公开输入直接读出。
- [ ] 确认视觉题的编号渲染图仍可正常生成（`visualInput.numberedView` 路径有效）。

#### 失败回退/停止
- 如果任一已知确定性 shortcut 在任何题目上仍可用，或未知表面 baseline 在人工审查后确认利用了非目标生成规律，**停止发布**，修复后全量重检。不得设置“允许5%泄漏”的阈值。
- 如果请求白名单或隔离导致评分器/runner角色混淆，**停止**，修复内部评分与模型输入分离后继续。
- 如果 v1 文件被意外修改，**立即停止**，保留差异并报告；不要自动执行 `git restore` 覆盖可能属于用户或实验进程的变更。

#### 完成后 Codex 报告内容
- 4 个 shortcut 的修复方案、逐题确定性规则结果与正确排名计数；统计检验仅作描述，不作为唯一质量门。
- 请求序列化白名单、内部/模型输入隔离清单以及实际 request snapshot 样例。
- v2 题集统计（题数、族分布、模态分布；任何与 v1 的差异均逐项解释，不为凑数生成无效题）。
- v1 未被修改的确认。

---

### Phase 2：任务族构念校准

**目标**：为每个任务族建立明确的输入/输出/评分契约，标记恒答族和证据读取族，确保论文主张与实际测量一致。

#### 输入
- v2 题集（Phase 1 产出）
- v1 任务分解表：`benchmark/paper/ldraw-operators.tex`
- 论文 §3-§4：`benchmark/paper/main.tex`

#### 可改范围
- 新增 `benchmark/ldraw-v2/TASK_CONTRACTS.md`（每族契约文档）。
- 修改 `benchmark/suite/ldraw-v2/questions.ts` 中的族标签和注释（不改变题数和答案）。
- 新增描述性分析脚本和结果（band×模态交叉表等，从现有数据计算，不需模型）。

#### 具体产出

**2.1 每任务族契约文档**

为 11 族各建立契约卡，包含以下字段：

| 字段 | 说明 |
|------|------|
| 族名 / 题数 / 模态 / 层 | 基本信息 |
| 公开输入包含什么 | 精确列出 `input` 字段和 `visualInput`（如有） |
| 解题需要模型做什么 | 精确描述操作（如"读取 connectorRecord.family，在选项中找相同标签"） |
| 评分规则 | 精确匹配 / 集合匹配 / 动作合法+目标达成 |
| 测量对象分类 | ①真感知 ②证据读取/元认知 ③图运算 ④执行格式 |
| 是否恒答族 | 是/否；若是，标注 † |
| 已知捷径 | Phase 1 修复后的残余捷径（应为空） |
| 构念效度声明 | 该族实际测量的能力，与论文声称的对比 |
| 论文中对应位置 | main.tex 行号 |

**2.2 恒答族与证据读取族标记**

在任务分解表（v2 版本的 `ldraw-operators.tex`）中增加"测量对象"列，并对以下族加标记：

- **Evidence limit（24题）**：† 恒答族，语义答案固定为 "not established by this evidence"。准确率本身不构成推理证据。
- **Interface（87题）**：‡ 证据读取控制项，connectorRecord.family 已在输入中提供。
- **Coverage（17题）**：‡ 证据读取控制项，supported 标志已在输入中提供。
- **Step lookup（55题）**：‡ 表格查找控制项，步骤表已在输入中提供。
- **Distance（73题）**：‡ 算术控制项，坐标已在输入中提供。

在正文增加声明："No family currently requires chaining two observation contracts within a single item; the benchmark measures modular competencies separately."

**2.3 "Integrative"层标签修正**

当前 "Integrative" 层仅含 Graph deletion（G-only，图内运算）。建议：
- 改名为 "graph-internal" 或 "multi-step graph"。
- 或在表注中明确："Integrative here means multi-step operations within the supplied graph, not across V/S/G/E observation contracts."

**2.4 描述性分析（从现有数据计算，不需模型）**

新增以下分析，结果写入 `benchmark/ldraw-v2/descriptive-analysis/`：

1. **band×模态交叉表**：D1-D4 中 V/S/G/E 各占多少题。用于回应"复杂场景≠复杂任务"——若 D4 以 G/S 字段题为主，明示"D4 规模优势体现在素材多样性与图结构复杂度，而非单题认知难度"。
2. **答案集中度量化**：每族的语义多数派比例（如 Graph deletion 60.3% 为 4，Evidence limit 100%）。计算"总是猜最常见答案"基线。
3. **题目冗余度分析**：同一源内多题共享同一组被选零件（2-5个目标件）的比例。
4. **源大小×题目数关系**：验证源大小（零件数）与该源题目数的相关性。

#### 机器验收
- [ ] 11 族契约文档完整，每族所有字段填写。
- [ ] 描述性分析脚本可执行，结果可复现（固定随机种子）。
- [ ] band×模态交叉表数值与 v2 题集一致（可独立验证）。
- [ ] 恒答族标记与实际答案分布一致（Evidence limit 100% 固定答案等）。

#### 人工验收
- [ ] 抽查 3 族契约文档，确认"解题需要做什么"的描述与实际题目一致。
- [ ] 确认描述性分析的结论未过度推断（如不得从 band×模态表直接得出"D4 更难"或"D4 更易"）。

#### 失败回退/停止
- 如果契约文档中某族的"测量对象"分类与代码实际行为不符，**停止**，修正后继续。
- 如果描述性分析发现 v2 题集统计与 v1 显著不一致（非预期），**停止**，排查原因。

#### 完成后 Codex 报告内容
- 11 族契约卡摘要。
- 描述性分析结果（4 个分析的数值结论）。
- 恒答族/证据读取族清单。
- "Integrative"标签修正方案。

---

### Phase 3：跨模块链路设计（可选增强）

**目标**：评估是否需要设计真正的跨模块联合推理任务。如果跳过此阶段，论文定位正式收窄为"可解释的分模块评测"（审稿人明确表示这是可接受的）。

#### 输入
- v2 题集（Phase 1-2 产出）
- 论文 §4 评估协议

#### 可改范围
- **仅新增** v2-cross 任务族设计文档和原型代码，不修改已有 11 族。
- 新增 `benchmark/suite/ldraw-v2/cross-module/` 目录。

#### 决策点（必须先回答再决定是否实施）

**问题**：是否需要跨模块联合任务？

**支持实施的理由**：
- 若论文希望保留"综合装配推理"定位，必须有至少一个任务要求单题内 V→G→E 联合。
- 审稿人意见2 明确要求区分"模块诊断价值"和"跨模块价值"。

**反对实施的理由**：
- 设计和验证跨模块任务成本高，可能引入新的构念问题。
- 审稿人明确说"不一定非要增加后者，但如果只做前者，就应把贡献准确定位为可解释的分模块评测"。
- 当前617题的模块化、可审计设计具有潜在价值，但需先通过shortcut修复与构念干预，不能仅凭类比断言诊断效度。

**推荐**：**默认跳过**，将论文定位收窄为"分模块诊断"。仅当用户明确要求保留"综合推理"定位时，才实施以下设计。

#### 若实施：跨模块任务原型设计【待实现】

设计 1-2 个跨模块任务族，要求单题内联合多个观测契约：

**候选设计 A：视觉目标属性→图验证→编辑决策**
- 输入：完整编号渲染图（V）+ 候选的连接器图（G）+ 不含目标答案的编辑动作集合（E）。
- 任务：例如“在图像中找到满足指定视觉属性的唯一实例；根据图证据判断删除它是否会使指定两候选断开；若会，执行对应的可见性编辑，否则执行 `no-op`”。视觉属性应由图像而非题目中的 B-number 给出，图和动作中只能以候选 ID 表示。
- 评分：最终决策与动作合法性为主指标；另记录视觉目标、图判断和动作选择三个中间输出，以支持 oracle-conditioned 及 model-conditioned 两种评估。
- 必要性检查：若只读 G/E 就能定位正确 ID，或三个子答案可以互不依赖地分别完成，则该题不得发布为跨模块任务。

**候选设计 B：视觉选择→源/图证据→认识论判断**
- 输入：图像给出需要选择的目标属性，S/G 提供候选实例的结构证据。
- 任务：先用视觉属性选择唯一候选，再对该候选执行图运算，并明确回答该图结论是否足以支持某项物理断言。
- 约束：认识论判断不能仍然是全题固定答案；至少要包含“证据足以回答图问题”和“证据不足以回答物理问题”等不同、由问题对象决定的合法标签，并在单题链中依赖上游选出的候选。

**实施要求**：
- 跨模块任务必须有独立的评分器，不能复用单族评分。
- 必须有消融设计：移除 V 输入 / 移除 G 输入 / 移除 E 接口，分别测量各环节的贡献。
- 必须用题内必要性干预和oracle-conditioned/model-conditioned级联验证每一阶段确实被使用；不得用单族得分的简单组合或乘积作整合零模型。

#### 机器验收（若实施）
- [ ] 跨模块任务原型可生成、可评分。
- [ ] 消融设计完整（至少 3 个输入条件）。
- [ ] 逐题证明每个声明为必要的模态都有改变正确输出的配对干预；删除任一必要模态后任务信息不足或性能显著改变。

#### 人工验收（若实施）
- [ ] 人工确认跨模块任务确实要求联合推理，而非三个独立子题的拼接。
- [ ] 确认评分规则合理（部分正确如何计分）。

#### 失败回退/停止
- 如果跨模块任务设计无法避免"三个独立子题拼接"的问题，**停止**，回退到"分模块诊断"定位。
- 如果消融设计无法隔离各环节贡献，**停止**，重新设计。

#### 完成后 Codex 报告内容
- 决策记录（是否实施跨模块任务，理由）。
- 若实施：原型设计文档、消融方案、验证结果。
- 若跳过：论文定位收窄声明。

---

### Phase 4：证据实验与消融设计

**目标**：在 v2 题集上设计可执行的实验方案，回应审稿人关于"复杂场景必要性"和"视觉贡献"的质疑。不要求立即运行模型，但实验设计必须完整可执行。

#### 输入
- v2 题集（Phase 1-2 产出）
- v1 实验计划：`benchmark/paper/ldraw-experiments.json`

#### 可改范围
- 新增 `benchmark/paper/ldraw-v2-experiments.json`（v2 实验计划）。
- 新增实验运行脚本（`benchmark/suite/ldraw-v2/run-model.ts`，若不存在）。
- 不修改 v1 实验计划。

#### 具体产出

**4.1 现有实验覆盖检查【已核验】**

v1 `ldraw-experiments.json` 中已定义的消融和鲁棒性实验（全部 proposed-not-run）：

| 实验表 | 条件 | 题数 | 回应什么问题 |
|--------|------|------|-------------|
| ablations | Static numbered image | 140 | 视觉题基线 |
| ablations | + rotate / zoom | 140 | 交互式视觉访问 |
| ablations | + ID isolation | 140 | 隔离视图访问 |
| ablations | Text without image | 140 | **无图像控制**——测试视觉题是否可纯文本解答 |
| ablations | Structured public input | 477 | 非视觉题基线 |
| ablations | Graph edges withheld | 233 | **撤回边列表**——测试图题是否需要图 |
| ablations | Public action solver | 75 | 动作求解器基线 |
| robustness | ID permutation | 617 | 编号绑定鲁棒性 |
| robustness | Choice-order permutation | 542 | 选项位置偏置 |
| robustness | Camera perturbation | V:140 | 视觉敏感性 |
| robustness | Color nuisance | Type:67 | 颜色干扰 |
| robustness | Equivalent edge ordering | G:233 | 序列化敏感性 |

**缺失的实验（v2 须新增）**：

1. **background-mask 消融**（回应意见3）："完整场景编号图 vs 仅操作数裁剪图"。当前计划表中不存在这一行。现有 "+ID isolation" 测的是"隔离是否帮助视觉"，不是"背景装配是否提供难度"。
   - 条件 A：完整装配编号渲染图（当前 visualInput）。
   - 条件 B：仅包含操作数（≤12个标签）的裁剪渲染图。
   - 判读：报告同题配对差值和区间；未检出差异只表示“大型背景提升当前视觉题难度”的主张未获支持，不能证明真实效应为零。
   - 注意：此消融需要新的渲染图（条件 B），Codex 须新增渲染脚本。

2. **旧请求重放与去捷径配对**（回应意见2）：仅当保存的 v1 真实 request snapshot 确实含 `references` 或数值模板时，构造保持目标语义不变、仅去除该表面规律的配对请求。性能下降只说明模型对该表面规律敏感；结合逐题输出转移后才能讨论是否利用捷径。若真实请求从未发送该字段，则不得制造一个“含字段基线”来推断旧实验。

3. **模块化结果与链式能力的区分**：
   - 现有 V/S/G/E 聚合只能描述不同观测契约下的表现，不能通过它们的线性组合、乘积或 R² 推断“是否存在整合能力”。
   - 若 Phase 3 跳过：明确写明 benchmark 不测单题跨模块整合，不再设计“整合残差”统计。
   - 若 Phase 3 实施：在同一链式题上报告 oracle-conditioned 与 model-conditioned 级联、阶段转移错误矩阵，以及针对每个必要输入的配对干预；整合结论只来自这些题内证据。

**4.2 实验运行基础设施【待实现】**

当前仓库未发现一个由 `ldraw:*` 命令直接调用、可冻结多模型请求与回执的 LDraw-1 runner；现有通用/历史 runner 不能在未核对输入契约时复用。Codex 须新增或明确适配：
- `benchmark/suite/ldraw-v2/run-model.ts`：读取公开题集，构造模型输入（文本+图像），调用 MLLM API，解析输出，调用评分器，记录结果。
- 输入构造规范：明确哪些字段发送给模型（必须与 Phase 1 请求白名单一致），图像如何编码（base64 / URL），系统提示词模板。
- 模型 adapter 规范：见 §5。

**4.3 消融判读规则【待实现，必须预注册估计量但不写死武断阈值】**

在 v2 实验协议中明确：
- 使用同题/同源配对差值，报告点估计、source-cluster bootstrap 区间、正确→错误与错误→正确的转移计数；“未检出差异”不能表述为“贡献为0”。
- 视觉族：正确图像、无图和语义错配图像三条件分别报告。区间包含0只能写“未检测到稳定增益”；只有等效性界值事先有科学依据时，才能支持“影响小于该界值”。
- 图族：证据撤回会改变可解性，主要验证信息依赖；更强证据来自答案随受控边干预而改变、但在等价边序置换下保持不变。
- 完整场景：完整图、操作数裁剪图、仅题目/选项三条件按源配对；未检出差异只能说明“大场景增加当前题集单题难度”未获支持，不能证明所有规模效应为零。
- 所有判读先按任务族报告，再考虑预先定义的聚合；不得由总体 micro 结果替代。

#### 机器验收
- [ ] v2 实验计划 JSON 完整，包含所有新增消融行。
- [ ] 实验运行脚本可执行（`--help` 输出可用参数），不实际调用 API。
- [ ] 消融判读规则写入实验协议文档。
- [ ] v1 实验计划未被修改。

#### 人工验收
- [ ] 确认 background-mask 消融的条件 B（裁剪图）渲染方案合理（不泄漏答案，不改变任务语义）。
- [ ] 确认模型输入构造规范与 Phase 1 请求白名单、canary 隔离和快照规则一致。

#### 失败回退/停止
- 如果实验运行脚本无法构造与公开题集一致的模型输入，**停止**，修复后继续。
- 如果 background-mask 的条件 B 渲染无法实现（如裁剪图丢失必要上下文），**停止**，重新设计消融条件。

#### 完成后 Codex 报告内容
- v2 实验计划（新增消融行清单）。
- 实验运行基础设施（脚本路径、输入构造规范）。
- 消融判读规则。
- 现有 v1 实验覆盖与缺失的对比表。

---

### Phase 5：论文/图表/代码/数据同步

**目标**：将 v2 的变更同步到论文、图表、代码和数据，确保主张-任务-证据一致。

#### 输入
- v2 题集、契约文档、实验计划（Phase 1-4 产出）
- v1 论文：`benchmark/paper/main.tex`、`supplement.tex`
- v1 图表：`benchmark/paper/figures/`、`benchmark/paper/tables/`

#### 可改范围
- 新增 `benchmark/paper/main-v2.tex`（v2 论文草稿，从 v1 复制修改）。
- 新增 v2 图表（`benchmark/paper/figures-v2/`）。
- 不修改 v1 论文和图表。

#### 具体产出

**5.1 论文改写清单**

| 位置 | v1 内容 | v2 改写方向 | 优先级 |
|------|---------|-------------|--------|
| 标题 | "Instance-Grounded Visual and Structural Reasoning" | 诊断效度未完成时改为 "Instance-Grounded Modular Evaluation of Visual, Source-Data, Graph and Scene-Edit Competencies"；完成故障注入/恢复验证后才考虑 Diagnostic | 必须 |
| 摘要 L22-37 | 可能被读成端到端综合推理 | 明确“modular evaluation with aligned instance identity”；诊断效度实验未完成前不使用“diagnostic instrument”强主张 | 必须 |
| 贡献段 L81-89 | 三条交付物描述 | 先写“实例对齐与可审计的模块化比较”；仅在诊断干预实证通过后写“失败归因可分” | 必须 |
| Related Work L91-121 | 否定式差异化 | 每段加"缝隙句"；新增"Diagnostic benchmarks vs capability benchmarks"段落 | 必须 |
| Table 1 L123-139 | 两列 | 加“研究问题 / 所需观测契约 / 本文是否实证”列，不替邻近工作写未经全文核验的负面能力判断 | 必须 |
| 任务分解表 L232-240 | 无"测量对象"列 | 加"测量对象"列；恒答族加 †；证据读取族加 ‡ | 必须 |
| "Integrative" L226-227 | 层标签 | 改名或加脚注 | 必须 |
| §4 评估协议 L406-517 | 无消融判读规则 | 加入 Phase 4 的判读规则 | 必须 |
| §5 描述分析 L310-404 | 无 band×模态交叉表 | 加入 Phase 2 的描述性分析 | 推荐 |
| §6 讨论 L519-539 | 未承认跨模块缺位 | 明确声明"No family currently requires chaining two observation contracts" | 必须 |
| 实验表 | v1 计划表 | 替换为 v2 实验计划（含 background-mask 等新增行） | 必须 |

**5.2 图表更新**

- 任务分解表（tab:operators）：增加“直接构念 / 必要输入 / 非目标捷径控制”列。
- Table 1（tab:related）：增加“研究问题 / 所需观测契约 / 本文是否实证”列。
- 新增 band×模态交叉表（描述性分析）。
- 新增答案集中度图（每族语义多数派比例）。
- 实验表：替换为 v2 计划。

**5.3 代码/数据同步检查清单**

- [ ] v2 生成器 `questions.ts` 与论文任务分解表一致（族名、题数、模态、层）。
- [ ] v2 公开题集与论文描述一致（题数 617，族分布）。
- [ ] v2 评分器与论文评分规则一致（精确匹配 / 集合匹配 / 动作合法+目标）。
- [ ] v2 实验计划与论文实验表一致。
- [ ] v2 契约文档与论文 §3 任务描述一致。
- [ ] 参考文献与实际引用一致（references.bib 中的 URL 可访问）。

#### 机器验收
- [ ] v2 论文可编译（`tectonic` 或 `latexmk`，使用项目现有构建工具 `benchmark/paper/BUILD.md` 中记录的方式）。
- [ ] v2 论文无 CJK 字符（保持全英文）。
- [ ] v2 论文页数在 CVPR 8 页主内容限制内（参考文献可附后）。
- [ ] 所有图表引用有效（无 ?? 引用）。
- [ ] 代码/数据同步检查清单全部通过。

#### 人工验收
- [ ] 通读 v2 论文，确认主张-任务-证据一致。
- [ ] 确认 Related Work 的差异化表述准确（不夸大、不贬低邻近工作）。
- [ ] 确认讨论部分诚实承认局限性。

#### 失败回退/停止
- 如果 v2 论文无法编译，**停止**，修复 LaTeX 错误后继续。
- 如果代码/数据同步检查发现不一致，**停止**，以代码/数据为准修正论文。
- 如果 v2 论文超出页数限制，**停止**，精简内容或将部分移至补充材料。

#### 完成后 Codex 报告内容
- v2 论文改写清单的执行状态（每项是否完成）。
- v2 图表清单。
- 代码/数据同步检查结果。
- v2 论文编译验证输出。
- v1 论文未被修改的确认。

---

## 4. 每源装配与每题审计契约

### 4.1 源装配审计【已核验部分，待全量验证】

当前 24 个源装配的基本信息：
- 源目录：`benchmark/ldraw-v1/sources/`
- 目录清单：`benchmark/ldraw-v1/catalog.json`（24个条目）
- 规模分布：D1(≤150件)=5源，D2(151-400)=9源，D3(401-1000)=2源，D4(>1000)=8源【已核验：`ldraw-scale.tex`】
- 源大小范围：53-1,978 实例，中位数 274【已核验：main.tex L325】

**每个源装配必须有的审计字段**【待实现，Codex 须验证 v2 源数据是否包含】：
- [ ] 原始 LDraw/OMR 文件 SHA256
- [ ] 作者、许可证、源 URL
- [ ] 零件实例数、零件类型数、颜色数
- [ ] 源装配报告中的连接器类型分布、unsupported 数量、交叠候选和 STEP 可用性从冻结数据全量重算，不从论文常量回填。
- [ ] 未支持定义的零件数
- [ ] 交叠候选数（无已识别配对接口的）
- [ ] 作者 STEP 元数据可用性（当前论文报告17/24，升级时须从冻结 manifest 重算）
- [ ] 独立重解析验证状态（类型、颜色、变换、层次是否通过）

**源级验收必须是 24/24 全量机器验证**，包括上述字段、源哈希、解析一致性和统计再计算；任何失败均进入源级阻断清单。人工检查只用于无法由机器确定的语义、许可解释和物理/视觉歧义，不能替代全量机器验证。

**当前覆盖限制**【已核验】：
- 仅 24 个源，覆盖 24 个 set family。
- D3 仅 2 源，统计功效有限。
- 论文已承认 "corpus is small and uneven"（main.tex L528）。
- **不得声称** 24 源代表全部乐高装配分布；应明确为"覆盖范围限制"。

### 4.2 每题审计契约【待实现】

每道题必须可追溯以下信息（v2 题集须包含）：
- 题 ID（`ld1-{modelId}-{family}-{serial}`）
- 源装配 ID 和 SHA256
- 任务族、模态、层
- 操作数列表（B-number + instanceId）
- 公开输入（字段剥离后的版本）
- 参考答案（内部 bundle，不公开）
- 证据来源（源属性 / 连接器审计 / 作者 STEP / 渲染图）
- 答案推导路径（可复现的计算过程）
- 等价类声明（如同型零件可替换、对称旋转可接受等）
- 歧义标记（视觉不可辨 / 物理不确定 / 图证据不完整）

**每题机器验收必须覆盖全部617题**：schema、唯一ID、字段白名单、option有效性、独立oracle重算、模型侧/内部侧映射、图像路径、等价答案、确定性shortcut、执行可达性均逐题记录；任何未通过题不得进入冻结发布。

**人工验收不得以随机抽查替代需要人判断的全量检查**：当前140道视觉题须逐题检查；其他477题先由机器全量检查，再将物理不确定、unsupported、交叠、近似等规则命中的题全部进入人工裁决队列，并记录判定者、理由和状态。
- 编号渲染图必须可复现（固定视角、光照、渲染参数）。
- 操作数隔离视图必须与完整场景视图配对保存。
- **当前未做全量逐题视觉人工核查**【已核验：论文无人类审核结果，human 表全部 null】。不得声称视觉题已认证准确。
- 后续全量验收方案：对 140 道视觉题逐题人工核查 ID 可读性、颜色准确性、形状可辨性，记录分歧和不确定。

### 4.3 答案与执行 Oracle【已核验部分】

- 选择题答案：`answer.choiceId`（单选）或 `answer.choiceIds`（多选），由 `questions.ts` 中的 `choice()` 函数生成【已核验：questions.ts L27-32】。
- 动作题答案：`answer.actionIds`，由 `questions.ts` 直接构造【已核验：questions.ts L166, L185】。
- 动作执行验证：`src/benchmark/engine.ts` 的 `replay()` 函数检查前置条件、禁止条件、预算，执行事实转移，验证目标状态【已核验：engine.ts L3-34】。
- 公开前置条件求解器：`engine.ts` 的 `solveActions()` 函数（Kahn-like），不读取参考答案【已核验：engine.ts L75-92】。v1 中 75/75 动作题通过【已核验：main.tex L454-455】。
- 评分：`engine.ts` 的 `score()` 函数，支持 single-choice / multiple-choice / actions / schedule / policy 格式【已核验：engine.ts L36-72】。

**Oracle 验证要求**【待实现】：
- 每道选择题的答案必须可由公开输入 + 证据来源独立复现（不依赖 `questions.ts` 中的内部变量）。
- 每道动作题必须可由 `solveActions()` 从公开前置条件求解（不读取答案）。
- v2 须新增全量 Oracle 验证脚本，对 617 题逐题验证。

---

## 5. 被测模型 Adapter 规范

### 5.1 模型歧义问题【已核验】

论文和实验计划中提及的模型家族包括：SmolVLM、Qwen3-VL、Llama 4、GPT-4.1、Gemini、Claude【已核验：ldraw-experiments.json】。但存在以下歧义：
- "Llama 4" 是否指 Meta Llama 4 多模态版本？（Llama 4 有 Scout/Maverick 等变体）
- "Gemini" 具体版本？（Gemini 1.5 Pro / 2.0 Flash / 2.5 Pro 等）
- "Claude" 具体版本？（Claude 3.5 Sonnet / 3 Opus / 4 等）
- "GPT-4.1" 具体版本？（GPT-4.1 / 4.1 mini / 4.1 nano）
- API 接入方式？（OpenRouter / 官方 API / 本地推理）

### 5.2 Adapter 规范【待实现】

每个被测模型必须有明确的 adapter 配置，包含：

| 字段 | 说明 |
|------|------|
| 模型家族 | 如 "Qwen3-VL" |
| 精确模型 ID | 如 "qwen/qwen3-vl-72b-instruct"（OpenRouter 格式）或官方模型名 |
| 提供商 | OpenRouter / 官方 API / 本地 |
| API revision / checkpoint | 冻结的版本号或日期 |
| 输入格式 | 文本+图像（base64 / URL）/ 纯文本 |
| 系统提示词 | 固定模板（不得随题变化） |
| 解码参数 | temperature（建议 0）、max_tokens、top_p |
| 工具调用 | 是否允许工具调用 / 工具列表 |
| 图像分辨率 | 发送给模型的图像尺寸 |
| 输出解析 | 从模型输出中提取答案的规则（JSON 解析 / 正则） |
| 成本记录 | tokens / 调用次数 / 费用 |

**v2 须新增** `benchmark/suite/ldraw-v2/model-adapters/` 目录，每个模型一个 JSON 配置文件。实验运行时从配置加载，不得在代码中硬编码模型参数。

### 5.3 模型输入构造规范【待实现】

发送给模型的每道题输入必须包含（且仅包含）：
1. 系统提示词（固定）。
2. 题目文本（`question` 或 `promptEn` 字段）。
3. 由 Phase 1 白名单序列化器从 model-input 中提取的必要 `input` 字段。
4. 选项列表（`options`，含 id 和 label/value）。
5. 视觉题：编号渲染图（`visualInput.numberedView`）。
6. 动作题：动作列表（`input.actions`）、初始事实（`input.initialFacts`）、目标（`input.goalFacts`）、预算（`input.budget`）。

**不得发送给模型**：`answer`、`evidenceDetail`、内部评审元数据及默认的 `references` 有序数组。即使内部 references 已规范化，runner 也不得整对象透传；所有实际发送字段以 Phase 1 的白名单序列化器和 request snapshot 为准。

---

## 6. 统计口径与可复现

### 6.1 指标定义【已核验】

- **Micro**：所有题目成功数 / 总题数【已核验：main.tex L423-424】。
- **Macro**：按源平均（每源内先算平均，再跨源平均）【已核验：main.tex L425-427】。
- **精确匹配**：单选 exact choiceId；多选 exact set（重复 ID 无效）【已核验：main.tex L417-418, engine.ts L63-71】。
- **动作成功**：合法完整执行 + 指定目标状态【已核验：main.tex L418-419, engine.ts L31-33】。
- **Valid %**：输出格式有效率（动作题）【已核验：ldraw-experiments.json actions 表】。
- **Goal %**：动作目标达成率【已核验：ldraw-experiments.json actions 表】。

**注意**：Valid % 和 Goal % 的关系不能作为规划能力的证据。在当前动作设计中，动作空间极小（Step sequence 6个线性动作，Restoration 2个动作），公开求解器 75/75 满分，Goal % 不可能显著高于 Valid %。**不得声称 Goal≫Valid 证明规划能力**。

### 6.2 置信区间【已核验】

- 按源组 bootstrap（10,000 次重采样，固定种子）【已核验：main.tex L433-435】。
- 训练方法的 folds 必须按源分组（同一源的所有实例/视图/题目在同一 fold）【已核验：main.tex L436-438】。
- **当前无 train/test split**（benchmark 无训练集），bootstrap 仅用于描述性置信区间。

### 6.3 答案先验基线【已核验】

- Always-A：26.652%（469 道单选题）【已核验：main.tex L385】。
- Uniform expected：27.342%（考虑每题选项数）【已核验：main.tex L386】。
- **v2 须新增**：每族的"总是猜最常见答案"基线（如 Graph deletion 60.3%，Evidence limit 100% 语义）。

### 6.4 可复现要求【待实现】

- 所有随机操作使用固定种子（`questions.ts` 已使用 SHA256 确定性采样【已核验：L6-8】）。
- 模型 API 调用记录：模型 ID、API revision、prompt、解码参数、图像分辨率、工具预算、超时、任务清单（main.tex L413-415 已要求）。
- v2 须新增：实验运行的完整输入快照（发送给模型的实际 JSON），存储在结果目录中，便于独立复现。
- 代码版本：实验运行时的 git commit hash。
- 环境：Node.js 版本、依赖版本（package-lock.json）。

---

## 7. 观测权限、泄漏与等价性

### 7.1 观测权限矩阵【待实现，v2 须明确】

每道题的模型可观测信息必须明确：

| 信息类型 | 视觉族(V) | 源数据族(S) | 图族(G) | 编辑族(E) |
|---------|----------|-----------|--------|---------|
| 编号渲染图 | ✓ | ✗ | ✗ | ✗ |
| 交互旋转/缩放 | 可选(+rotate条件) | ✗ | ✗ | ✗ |
| 操作数隔离视图 | 可选(+isolation条件) | ✗ | ✗ | ✗ |
| 源坐标/字段 | ✗ | ✓(input中) | ✗ | ✗ |
| 连接器记录/边列表 | ✗ | ✗ | ✓(input中) | ✗ |
| 动作列表/事实状态 | ✗ | ✗ | ✗ | ✓(input中) |
| 完整装配上下文 | ✓（静态编号图保留完整场景；隔离/裁剪为显式对照） | ✗（仅给题目所需源字段） | ✗（仅给局部诱导图） | 执行引擎可维护完整可见集合；模型是否接收渲染或仅接收事实由条件声明 |
| 参考答案 | ✗ | ✗ | ✗ | ✗ |
| evidenceDetail | ✗ | ✗ | ✗ | ✗ |

**关键原则**：模型不得访问未在其观测契约中声明的信息。评分器和 Oracle 使用内部 bundle（含答案），但模型输入必须来自公开导出（字段剥离后）。

### 7.2 泄漏检查清单【待实现，v2 须全量执行】

对 v2 公开题集逐题检查：
- **内部评审/评分 bundle**：`models/*.json` 中含参考答案是预期行为，不属于模型输入泄漏；但必须通过路径隔离、类型隔离和 canary 测试保证 runner 不可读取。
- [ ] 模型侧 `inputs/*.json` 与最终 request snapshot 均不含 `answer`、`evidenceDetail` 或内部 canary。
- [ ] `references` 默认不进入最终请求；若某条件必须提供，只允许无角色、无答案顺序语义的 operand 标签，并做确定性捷径审计。
- [ ] `input` 可以包含任务定义所需的目标证据（例如图边或动作前置条件），但不得包含与该构念无关、由生成顺序产生的答案编码；每族须在契约卡里逐字段说明必要性。
- [ ] 选项的 `value` 若是模型输出/评分所必需，可在请求序列化时映射为匿名 choice ID；不得暴露由内部 instanceId、排序或相对数值模板形成的额外线索。
- [ ] 视觉题渲染只含完成任务所需的 B-number 定位标签，不含颜色名、partNumber、正确选项标记等答案属性；逐图用真实像素核查。
- [ ] 动作题中 `initialFacts`、目标和动作列表是声明的执行契约，不按“出现目标身份”自动判泄漏；检查重点是它们是否把本应推断的变量直接给出，以及论文是否准确把任务称为契约遵循而非规划发现。

**关于 Restoration 的 `missingInstanceIds` 字段**【已核验，需审慎判断】：
- `questions.ts` L184：`missingInstanceIds: [target]` 在 `input` 中。
- 同时 `initialFacts: [\`missing-${target}\`, ...]` 也编码了目标身份。
- 这两个字段是执行契约的一部分（模型需要知道恢复哪个实例），**不应简单定性为"答案泄漏"**。
- 但 `missingInstanceIds` 是冗余的（`initialFacts` 已包含 `missing-{target}`），移除 `missingInstanceIds` 而保留 `initialFacts` 不构成任务升级，只是消除冗余。
- **推荐**：v2 中移除冗余的 `missingInstanceIds`，保留 `initialFacts`（执行契约必要信息）。这不是修复泄漏，是消除冗余。

### 7.3 等价性与歧义【已核验部分，待全量标记】

**已声明的等价类**：
- 同型零件（相同 partNumber）在 Part-type 任务中视为正确答案【已核验：questions.ts L43】。
- 多选答案的集合匹配不考虑顺序【已核验：engine.ts L70】。
- 动作的 `visual` 效果（可见性变化）不影响事实评分【已核验：engine.ts L24-28】。

**待标记的歧义**【待实现，v2 须逐题检查】：
- 视觉近同型零件（Part-type 任务中，两个不同 partNumber 但视觉几乎相同的零件）——论文已承认需要人工裁决【已核验：main.tex L531-532】，但未逐题标记。
- 颜色不可辨（在特定渲染条件下，两个颜色码视觉上难以区分）。
- 连接器证据不完整（unsupported 零件的连接状态未知）。
- 交叠候选（573 对无已识别配对接口的交叠【已核验：main.tex L524】，物理状态不确定）。
- 源场景包含多个独立对象（如车辆和驾驶员），连接器图可能不连通。

**处理原则**：涉及视觉不可辨、物理真实性、图证据来源时，必须保留不确定性标记，不得伪精确。歧义题不得从题集中删除（除非确认题目无效），应标记为"需人工裁决"并在报告中单独统计。

---

## 8. 采样与划分

### 8.1 题目采样【已核验】

- 确定性采样：使用 SHA256 哈希，种子为 modelId + 字段名【已核验：questions.ts L6-8】。
- 每源目标零件数：`sampleCount = min(5, 2 + floor(parts.length / 400))`【已核验：questions.ts L14】。即小源(≤400件)选2-3个，大源(>800件)选4-5个。
- 题目生成仅在证据支持契约时创建（如 Part-type 需要同型零件+异型干扰项）【已核验：questions.ts L45】。
- 选项洗牌：使用 task.id 作为种子【已核验：questions.ts L28】。

### 8.2 题目相关性【已核验，待量化】

- 同一源内的 Color、Part-type、Distance、Restoration 题共享同一组被选零件（2-5个目标件）【已核验：questions.ts L34 的 `for (const p of selected)` 循环】。
- 论文已承认 "Tasks within a source are correlated"【已核验：main.tex L433】，计划用 source-group bootstrap 处理。
- **待量化**：族间题目重叠率（同一目标零件出现在多少族的题目中）、源内题目冗余度。

### 8.3 训练/测试划分【已核验】

- **当前无训练集**：LDraw-1 是纯评测基准，不提供训练数据。
- 论文已声明 "No train/test split or confidence interval is presented as already established"【已核验：main.tex L438-439】。
- 商业套装可能来自预训练（论文已承认污染风险【已核验：main.tex L535】），但无测量。
- [ ] 对最终模型输入执行逐题字段白名单检查并生成真实 request snapshot；`models/*.json` 只供评分，`inputs/*.json` 不能直接整对象透传。

---

## 9. 外部事实与原始 URL

### 9.1 邻近工作参考文献【已核验：references.bib】

| 工作 | 引用键 | 原始 URL | 本地副本 |
|------|--------|---------|---------|
| BrickNet | kulits2026bricknet | https://openaccess.thecvf.com/content/CVPR2026/html/Kulits_BrickNet_Graph-Backed_Generative_Brick_Assembly_CVPR_2026_paper.html | `benchmark/.runtime/paper-reference/bricknet.pdf` (+ .txt) |
| LEGO-Puzzles | tang2025legopuzzles | https://openreview.net/forum?id=jQh9SUrnev | 无本地副本 |
| PhyBlock | ma2025phyblock | https://arxiv.org/abs/2506.08708 | 无本地副本 |
| Break and Make | walsman2022break | https://arxiv.org/abs/2207.13738 | `benchmark/.runtime/paper-reference/break-and-make.pdf` (+ .txt) |
| Visual LEGO Manual | wang2022manual | https://arxiv.org/abs/2207.12572 | 无本地副本 |
| BrickGPT | pun2025brickgpt | https://arxiv.org/abs/2505.05469 | 无本地副本 |
| CLEVR | johnson2017clevr | https://svl.stanford.edu/assets/publications/pdfs/johnson2017cvpr.pdf | 无本地副本 |
| GQA | hudson2019gqa | https://openaccess.thecvf.com/content_CVPR_2019/html/Hudson_GQA_A_New_Dataset_for_Real-World_Visual_Reasoning_and_Compositional_CVPR_2019_paper.html | `benchmark/.runtime/paper-reference/gqa.pdf` (+ .txt) |
| BLINK | fu2024blink | https://arxiv.org/abs/2404.12390 | 无本地副本 |

### 9.2 差异声明的使用规则【部分核验】

- **BrickNet**：当前可写“LDraw-1 将其公开连接器实现用于固定源审计，并评测固定源上的问题/场景编辑”；更细的表示差异只能引用已读全文中的具体章节。
- **LEGO-Puzzles**：当前仅可写“论文将其定位为多步空间推理评测”；实例指代、结构化证据与错误分层必须取得全文后逐项核验。
- **PhyBlock**：当前仅可写“其在仿真契约下评测物理理解与规划，而 LDraw-1 的图和显示编辑语义更窄”；数据形态、任务分支与错误分类必须全文核验。
- `references.bib` 或摘要只证明文献和高层主题存在，不足以支持否定式能力断言。

### 9.3 工具与基础设施引用【已核验】

- BrickNet 0.1.0 连接器实现：PyPI `bricknet` 包，本地安装在 `benchmark/.runtime/mlx-env/lib/python3.11/site-packages/bricknet/`【已核验】。
- LDraw 标准：https://www.ldraw.org/article/218.html【已核验：references.bib】。
- Three.js：https://threejs.org/docs/【已核验：references.bib】。

---

## 10. 未完成核验与待用户决策

### 10.1 未完成核验（Codex 须在对应阶段完成）

| 项目 | 状态 | 负责阶段 |
|------|------|---------|
| v1 冻结题集的 SHA256 清单 | 未完成 | Phase 0 |
| v2 shortcut 全量检测（覆盖v2实际生成的每题） | 未完成 | Phase 1 |
| 模型请求序列化与实际字段暴露验证 | 未实现/未核对正在运行请求 | Phase 0+1 |
| 11 族契约文档 | 未完成 | Phase 2 |
| band×模态交叉表 | 未完成（可从现有数据计算） | Phase 2 |
| 答案集中度全量量化 | 未完成 | Phase 2 |
| 视觉题全量人工核查（140题） | 未完成（当前无任何人审结果） | Phase 2+后续 |
| 歧义题逐题标记 | 未完成 | Phase 2 |
| 跨模块任务设计（可选） | 未实施 | Phase 3 |
| background-mask 消融渲染 | 未实现 | Phase 4 |
| 模型 runner 基础设施 | 未实现（v1 无专门 runner） | Phase 4 |
| 模型 adapter 配置 | 未实现 | Phase 4+5 |
| v2 论文编译验证 | 未完成 | Phase 5 |
| Oracle 全量验证（覆盖v2实际生成的每题，可由独立实现复现） | 未完成 | Phase 1+2 |

### 10.2 待用户决策的阻塞点

**决策点 1：是否实施跨模块联合任务（Phase 3）？**
- 默认推荐：跳过，将论文定位收窄为"可解释的分模块评测"。
- 若用户要求保留"综合装配推理"定位，则必须实施。
- 此决策影响论文标题、摘要、贡献段的改写方向。

**决策点 2：v2 题集是否改变题数和族分布？**
- Phase 1 的 shortcut 修复（选项构造、内部references规范化与请求剥离）原则上不改变题数和oracle，但可能使极短步骤序列因合法干扰项不足而需要改变输出格式或暂不生成；任何题数变化必须重算全部统计并版本化。
- 若用户希望增加新任务族（如跨模块任务），题数会增加，需重新计算所有描述性统计。
- 默认推荐：先保持11族语义不变完成P0；题数以合法生成结果为准，不为维持617而制造无效题。跨模块任务采用独立扩展版本。

**决策点 3：现有 v1 实验（如有正在运行的）如何处理？**
- 如果 v1 实验正在运行，v2 升级不得中断。
- v1 实验结果（如有）仅用于 v1 论文，不迁移到 v2。
- 用户须确认是否有正在运行的 v1 实验进程。

**决策点 4：视觉题渲染图的重新生成**
- Phase 1 的字段剥离不改变视觉题渲染图。
- 但若 background-mask 消融（Phase 4）需要裁剪图，须新增渲染。
- 渲染需要启动开发服务器（`npm run dev`，端口 5173）和 Playwright，可能耗时。用户须确认是否允许。

### 10.3 明确不做的事项

- 不修改 v1 任何文件（题集、生成器、评分器、论文、图表）。
- 不启动模型训练或微调。
- 不编造未运行的实验结果。
- 不伪造物理标注或稳定性声明。
- 不删除歧义题（除非确认无效）。
- 不将"组合增量"包装成"独特贡献"——定位必须诚实。
- 不声称视觉题已人工核查准确（当前无全量核查）。
- 不声称 24 源代表全部乐高装配分布。
- 不用单模块分数的乘积、线性组合或 R² 推断跨模块整合能力；链式结论只来自同题级联与受控干预。
- 不声称 Goal≫Valid 证明规划能力。

---

## 11. 阶段质量门汇总

| 阶段 | 必须通过的质量门 | 未通过的后果 |
|------|----------------|-------------|
| Phase 0 | v1 冻结确认 + v2 隔离目录 | 不得进入 Phase 1 |
| Phase 1 | 4 shortcut 全量消除 + 模型请求/内部bundle隔离验证 + v1 未修改 | 不得进入 Phase 2（所有后续实验无效） |
| Phase 2 | 11 族契约完整 + 描述性分析可复现 + 恒答族标记准确 | 不得进入 Phase 3/4 |
| Phase 3（可选） | 跨模块任务确需联合推理 + 消融可隔离 | 若不通过，回退到分模块定位 |
| Phase 4 | 实验计划完整 + runner 可执行（`--help`）+ 真实请求快照与配对判读规则写入协议 | 不得进入 Phase 5 |
| Phase 5 | v2 论文可编译 + 主张-任务-证据一致 + 代码/数据同步 | 交付 v2 论文 |

---

*本文档为 Codex 实施指导，所有升级操作须按阶段执行，每阶段通过质量门后方可继续。现有 v1 实验和原始资产受保护，不得修改。*
