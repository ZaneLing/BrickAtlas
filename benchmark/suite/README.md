# BrickAtlas Multitask Suite

多任务结构数据与LLM/MLLM评测。**不包括机械手、机器人或VLA。**
旧CARE-mini保留在benchmark根目录，新套件不修改原项目src、资产和入口。

## 文档

- [研究版逐项目标验收](ACCEPTANCE.md)
- [研究版操作与复现](research/README.md)
- [576几何组数据卡与局限](research/DATASET_CARD.md)
- [详细分阶段计划](../PLAN-multitask.md)
- [数据卡](DATASET_CARD.md)
- [任务协议与指标](METRICS.md)
- [实验结果](REPORT.md)

## 一次性准备

在 `brick-atlas/benchmark` 目录，使用 Node.js 22+ 和父仓库已安装依赖：

```bash
npm run suite:prepare
npm run suite:start
```

默认地址 `http://127.0.0.1:5175`；有占用则自动使用后续空闲端口。
真实地址保存在 `.runtime/suite-server.json`。旧的5174与原项目5173不受影响。
页面加载、浏览、人工提交与oracle自测都不会调用付费模型。

本机没有PATH里的Node时，从仓库根运行：

```bash
.tools/node-v22.23.2-darwin-arm64/bin/node benchmark/suite/launch.mjs
```

## 数据

25种标准矩形砖/薄板，8结构族，552配色样本，138规范化几何组，4,416任务。
每结构包含部件、位姿、stud连接数量、可执行数字装配顺序与来源标识。
train/validation/test_id按几何组划分，test_ood整族留出。
导出的模型及SFT配方放在 `.runtime/suite-exports`，由代码可重建，不将大文件塞入Git。
公开manifest、族样例、全量oracle/empty/copy-input统计在 `suite/artifacts/`。

八任务：

| ID | 测量 | 输出 |
| --- | --- | --- |
| parts | 从两张图识别目录零件与凸点数量 | 三字段JSON |
| relations | 从结构判断连接、上下、连通分量 | 三字段JSON |
| reconstruct | 根据组装及逐层图重建 | 绝对/相对结构程序 |
| generate | 根据文字和体积约束生成合法铺砌 | 结构程序，允许多个答案 |
| complete | 保留现有结构并补全 | 完整结构 |
| edit | 改色、顶部复制增件或移除指定件 | 完整结构 |
| plan | 任一可执行装配或拆解顺序 | ID列表 |
| repair | 错色/错位/额外零件与正常样本判断 | 完整结构与错误ID |

## 实际模型评测

one-shot主榜默认2模型，每模型每任务2例，共32次推理。
选择在调用前冻结，只取test_id/test_ood，样本不随模型改变：

```bash
npm run suite:run -- --paid
```

辅助模式同样本、恰好一次合法性反馈，共最多64次推理，单独分榜：

```bash
npm run suite:run -- --paid --mode=validator-once
```

只评一个模型或部分任务：

```bash
npm run suite:run -- --paid --models=google/gemini-2.5-flash --tasks=relations,generate,edit,plan
```

相对程序输入条件：

```bash
npm run suite:run -- --paid --models=google/gemini-2.5-flash --representation=relative --tasks=relations,edit,plan
```

`absolute/relative`指提供给模型的结构输入表示；输出两种合法结构程序都接受，按同一geometry scorer评分。
相对表示不是完整BrickNet的connector program，不用parent字段冒充几何连接。

### 成本和密钥

使用既有服务端 `.env` 中OPENROUTER_API_KEY，或进程环境变量。
沿用CARE-mini的 `.runtime/campaign-ledger.json` 和 `.runtime/pilot.lock`。
累计上限4.50美元，历史花费计入，不可通过新套件重置预算。
每次请求先预留、按usage.cost结算；unknown/timeout不重试，保留预留并停止。
Provider价格上限、模型allowlist、输出token上限均在共享适配器中。
没有自动训练、自动调用全部模型或页面后台收费。

## 外部模型

生成带本地PNG路径、无目标几何答案的输入：

```bash
npm run suite:export
```

输出 `.runtime/suite-exports/inputs.jsonl`：

```json
{"taskId":"...","system":"...","input":{"prompt":"...","input":{},"responseSchema":{}},"images":["images/hash.png"],"modality":"RGB+text"}
```

外部模型逐条读取system/input与图像，生成如下 `predictions.jsonl`：

```json
{"taskId":"...","answer":{"version":1,"parts":[]}}
```

评分不调用API，缺失题目计失败，重复ID或未知题目拒绝：

```bash
npm run suite:score -- --predictions=/absolute/path/predictions.jsonl
```

当前CLI scorer对应默认冻结的16题开发smoke。它不是允许参与者任意选题的正式leaderboard。

## 训练与基线

`suite:prepare` 导出2368条train和320条validation的SFT配方；没有导出测试答案到训练文件。
每条包含taskId、group、split、kind、messages、needsImages和renderRequests。
renderRequests仅供可信离线渲染预处理，**不可作为图像题的模型输入**。
对需要图像的SFT条目，必须先生成对应图片再使用支持视觉的训练器。
初始版仅导出配方；研究扩展现已完成五组真实 Qwen3-0.6B 文本/结构基线，包括四组短程 LoRA。
权重、训练步骤和预测已打包，见 `research/README.md`。这不是多模态微调，也未证明多任务迁移。
另有真实通用模型API评测，以及oracle、空答案和copy-input诊断基线。

## 验证

```bash
npm test
npm run check
npm run suite:build
npm run suite:ui
npm run suite:replay
```

UI需要服务启动且没有付费任务正在运行。UI测试不产生模型请求。
replay核对数据、协议、源码、选择哈希；从原文重新解析答案、复算所有分数与账单。
每个run目录包含run.json、protocol.json、ledger.json、REPORT.md和实际观测PNG。
同题的oracle成功是裁判验证，不作为学习系统成绩。

## 不应做出的声明

- 不把552配色样本说成552个独立人工设计对象。
- 不把受控体积生成说成已解决自由自然语言设计。
- 不把支撑/碰撞规则说成验证了承重、扣合力或机器人执行。
- 不把known-part识别说成未见零件泛化。
- 不合并单次提交、一次反馈、旧交互agent的成绩。
- 不用每任务两例的结果宣称显著优于别的模型或已有论文。

后续论文级扩展及未完成研究工作均在计划末尾列出，不包含机器人。
