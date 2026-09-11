# Brick Atlas 模型测试场

## 多任务套件（新）

覆盖八类能力的新套件位于 [suite/](suite/README.md)，入口默认 http://127.0.0.1:5175。
启动命令 `npm run suite:start`，数据准备 `npm run suite:prepare`。
查看 [详细计划](PLAN-multitask.md)、[数据卡](suite/DATASET_CARD.md)、[指标](suite/METRICS.md) 和 [多任务实测报告](suite/REPORT.md)。
不包含机械手、机器人或VLA。下面保留旧CARE-mini的文档和5174入口，旧实验不与新榜单合并。

## CARE-mini v1（保留）

独立的 **CARE-mini v1** benchmark 模块。原项目的浏览、拼装、DIY、资产和入口保持不变。

[v1 交付报告与实测结果](REPORT-v1.zh-CN.md)

## 启动

在本目录运行，使用父仓库已安装的依赖，要求 Node.js 22+：

```bash
npm start
```

默认地址是 `http://127.0.0.1:5174`。端口占用时自动向后寻找空闲端口，实际地址打印在终端，并写入 `.runtime/server.json`。不会重启或占用原项目的 5173 服务。

开发前台运行：

```bash
npm run dev
```

本机仓库自带 Node 时也可以从父目录运行：

```bash
.tools/node-v22.23.2-darwin-arm64/bin/node benchmark/launch.mjs
```

页面初次打开只启动免费的人工测试 episode，**不会调用付费模型**。

## 三个视图

- **测试场**：任务选择、Active/Passive 协议、三维视角、拆解预测、Blueprint JSON、重建编辑、结束评分。
- **试验结果**：真实 OpenRouter 运行结果、请求费用、逐步观测/动作回放、Markdown 报告下载。
- **协议与边界**：动作、坐标、预算、评分和未实现的物理能力。

人工测试和真实模型使用同一个 `Environment.step()` 与 scorer。人工页面“执行蓝图”是确定性快捷操作；真实运行器会调用新上下文的模型作为 Builder，不把快捷操作冒充模型结果。

## 首轮 Pilot

仅选用两个低成本视觉模型，而非全部 OpenRouter 模型：

- `openai/gpt-4.1-mini`
- `google/gemini-2.5-flash`

每模型 4 个 Active episode 和 2 个同目标、无故障 Passive 对照，共 12 个 episode。
每个目标只有 8 块积木；原仓库 15 个 OMR 套装不参与本轮全量测试。

运行前启动服务，然后在页面明确确认付费，或者在本目录执行：

```bash
npm run pilot
```

只测一个模型：

```bash
npm run pilot -- --model=openai/gpt-4.1-mini
```

非默认端口：

```bash
BENCHMARK_URL=http://127.0.0.1:5175 npm run pilot
```

默认模型适配器为 OpenRouter chat completions；API key 从服务端 `OPENROUTER_API_KEY` 或父目录已有的 `.env` 加载，不进入前端。

## 成本保护

- campaign 累计硬预算 **$4.50**，保留相对用户 $5 上限的 $0.50 缓冲。不是每次刷新网页都重新获得预算。
- `.runtime/campaign-ledger.json` 持久化每次请求的预留、实际成本和 generation ID。
- 请求前使用文本字节上界、每张 640x480 图片的保守 token 额度、输出上限和 provider 价格上限预留。
- 每个模型的 prompt/completion 单价有 allowlist 上限。禁止模型 fallback、自动重试和未列出的模型。
- 请求超时或响应缺少 `usage.cost` 时保留预留并停止，避免未知计费情况下继续花费。
- CLI 和页面共用 `.runtime/pilot.lock`；同一时间只允许一个付费 Pilot。
- `pending` 是正在发送或等待响应的预留，`uncertain` 是需要人工核对的费用。崩溃后的 pending 也会阻止继续运行。
- 若需要核对失败请求，应先通过 OpenRouter 活动记录或 `/generation` 核实；不要直接删除 ledger 或用新文件绕过累计预算。
- 这是本机预算控制，不替代 OpenRouter 账户级 spending limit。报告中的费用为推理 credits，不含充值手续费。

## v1 的实际测量

数据来自一个程序化密封盒结构族。两个变体拥有相同外壳、BOM 和可见身份，内部蓝色砖的位置/朝向不同。
闭壳下允许的四个镜头都由渲染像素测试验证一致；移除顶盖后可区分。
两者在粗粒度砖间连接图上同构，所以 v1 测的是**隐藏几何识别**，不是已经验证了不同受力拓扑的因果发现。

流程：

1. 模型观察 RGB 与可见 part ID/color，不提供目标坐标。
2. Active 可拆解；Passive 不可拆解。拆解前预测新增可见数量和剩余连通分量。
3. 模型提交有序网格位姿蓝图。没有正确性提示。
4. 丢弃全部探索上下文，同型号模型的新上下文只收到蓝图和库存。
5. Builder 执行真实编辑。有效但错误的放置保留，批量动作只保留合法前缀。
6. 部分任务会在足够多次放置后移除或偏移顶盖，模型只能从后续观察发现。
7. 模型主动 finish 或耗尽动作额度后，确定性 scorer 评分。

恢复成功只在“故障前已经正确建成、且故障实际触发”的 episode 中单列。不满足条件记 N/A，不能记为恢复成功。

### 规则而非真实物理

支持 6 个真实 Part ID 对应的简化矩形砖/薄板。渲染使用 Three.js 程序化几何。
所有位姿在整数 stud / plate 网格，方向限四个 yaw。
世界规则检查砖体重叠、下方 stud 支撑、向上移除通道。
`place` 是离散位姿操作，不检查连续插入路径，不认证真实可执行装配顺序。

尚不支持：任意 LDraw 几何、clip/pin/axle 连接器、连续 SE(3)、扣合力、承重、重心、机器人、步骤 DAG、跨模型 handoff。
请勿把 v1 分数描述成真实物理装配能力或“优于所有 benchmark”。

## 评分与统计

- 同型号/颜色/网格 footprint 的零件进行多重集匹配，ID 可互换，方砖 90 度和长砖 180 度对称被接受。
- Part F1、派生连接 Edge F1、blueprint executable、最终 exact、完整 lifecycle success。
- 拆解前预测准确率、非法动作数、决策数、primitive 编辑数、恢复成功、故障后编辑数。
- `run.json` 保存费用、tokens、provider、generation ID 和原始模型 JSON。
- 小样本 Wilson 区间仅为描述；共享结构族的 episode 非独立样本，不能据此判定可靠排名。
- Active 总集含故障，Passive 不含；只有相同无故障配对可用于 Active/Passive 对照。

## 验证

```bash
npm test
npm run check
npm run build
npm run test:ui
npm run test:replay
```

UI 测试需要服务已启动，但绝不发送付费请求；如果正在运行真实 Pilot，请等结束后再运行它的费用不变断言。
重放验证不调用模型；它核对保存的观察、动作、图像 hash、最终评分和实际费用。

## 输出和复现

```text
results/
  latest.json
  <run-id>/
    run.json
    protocol.json
    diagnostics.json
    REPORT.zh-CN.md
    verification.json
    replay-verification.json
    observations/<sha256>.png
  verification/
    desktop.png
    mobile.png
    closed.png
    opened-a.png
    opened-b.png
    verification.json
```

`protocolHash`、`taskHash`、`sourceHash` 和逐文件 hash 固定运行时实现。
本轮配置、模型输出与观察是 **public pilot**，不是私有测试数据，未来可被训练模型看见。
服务限制在 loopback；Vite 仅允许 web/shared/node_modules，私有 task 源、`.env`、ledger 不向浏览器静态服务。
本机管理员和 runner 可信，不把这种设计声称为抵抗恶意本地用户的远程沙箱。

重新生成最新报告，不产生推理费用：

```bash
npm run report
```

条件化 Builder 诊断使用 oracle 蓝图，另存结果，不计入主试验成功率：

```bash
npm run diagnostics
```

此命令会付费调用两个模型各三例，共用 $4.50 campaign 账本；如果本轮已有诊断结果会拒绝再次运行。

## 模块结构

- `core/world.ts`：规则、连接、库存和评分。
- `core/tasks.ts`：服务端任务生成，不导入前端。
- `core/environment.ts`：阶段、观察、动作、故障注入。
- `core/prompts.ts`：冻结的 Inspector/Builder 提示词。
- `core/budget.ts` / `core/openrouter.ts`：预算与付费模型适配。
- `run.ts` / `report.ts`：真实试验与报告生成。
- `server.ts`：独立 API 与 Vite 服务。
- `web/`：人工测试场与结果回放，`render.html` 为可信离屏 Three.js 渲染页。
- `shared/`：公开目录、类型与坐标规则。
- `tests/`：不付费的正确性、隔离与 UI 验证。
