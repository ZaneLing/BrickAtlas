# 这批实验怎么继续、怎么查看

## 题量与设置

- 四个模型各 50 道静态阶段题 + 50 道正常拼装题，共 400 个新基础条件。
- 同题正常拼装成功后，才增加事故修复分支；未通过时，修复能力是“未测到”，不是零分。
- 上一批缺失/中断条件：Sol 12 个、Seed Pro 8 个，另列补测。
- 静态也使用统一视觉 Agent 的观察和拆装工具。本批不是一次性静态问答实验。
- 50 个物件、49 个原始来源组。完整题单、抽样规则与每个条件的来源见 `plan.json`。
- 新接口版本为 `brick-atlas-unified-visual-agent/5`，输入策略为 `visual-memory-pull-v5`。v4发现参数说明歧义，作为接口排查数据保留；所有条件（包括v4成功题）用v5统一重跑。账本累计，不清零，历史实验不改分。

## 运行命令

从仓库根目录执行。模型名单固定为 Ark 的 Sol、Seed Pro、DeepSeek Flash，以及 Aliyun 的 Qwen。

```bash
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m unified_agent.experiment_batch --model ark/gpt-6-1-sol-260929
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m unified_agent.experiment_batch --model ark/doubao-seed-2-1-pro-260915
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m unified_agent.experiment_batch --model ark/deepseek-v4-1-flash-261017
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m unified_agent.experiment_batch --model qwen/qwen3.8-flash
```

每个模型一个进程、一个账本。不要同时启动同一模型的第二个进程。同一条件和预算在各模型间保持一致。

已有报告时必须显式加 `--resume`，已归档条件不会重新生成。`--resume` 不等于重试失败题。一次已确认的输出截断可以保留为技术中断，检查原因后继续其他题；不能偷偷增大这个模型的输出额度或反复重跑到成功。存在未结算请求时，先核对响应/账本，不能删除账本或直接重试。

接入点、权限或限流设置有真实变更后，用 `--refresh-preflight --resume` 重新检查；旧证据保存在 `preflight/*/history/`。检查先覆盖初始多图，再覆盖候选与历史，最后覆盖较大的图片/历史组合。hello 成功不代替这些检查。

程序仅对服务器明确返回的 HTTP 429、且确认未生成内容的请求，按 65/130/195 秒等待最多三次；请求内容和环境状态不变。403、超时、截断不自动重试。所有尝试都记录。

## 查看和重建报告

本机回放：<http://127.0.0.1:8832/experiments>。报告：<http://127.0.0.1:8832/experiment-results/index.html>。

下列命令只读取现有结果，不调用模型：

```bash
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m unified_agent.experiment_audit
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m unified_agent.experiment_geometry_audit
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m unified_agent.experiment_reference
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m unified_agent.experiment_report
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m unified_agent.experiment_pdf
```

`report.pdf`、`README.zh-CN.md`、`index.html`、`metrics.json` 和 `plots/` 都显示已归档结果。只有四个模型的任务列表都结束，才标记全部完成。报告中没有结果的格子是未运行、未满足前置条件或技术中断，不是模型得零分。

`experiment_monitor` 当前每约三分钟更新已归档结果的报告。它只在单次孤立截断后继续尚未运行的题目，不重复截断题、不增加预算；连续两次截断、权限/限流失败、程序错误、费用停止或计费不确定时均不自动放行。`monitor.json` 记录进度与继续执行的原因。

## 原始证据在哪里

- `workers/`：逐模型进度和结果。
- `ledgers/`：累计用量和请求状态；不得清空绕过预算。
- `preflight/`：接口检查请求、响应、通过/失败证书。
- `diagnostics/hello-20261030/`：最小 hello 诊断，另列，不冒充正式题目。
- `checks/`：题目可执行性、图片/用量一致性、视觉相似性检查。
- `reference/`：报告用的合法参考过程，未提供给模型，不声称最短路线。
- `deliverables/brickplan-dynamic-arena/runs/<run-id>/`：逐轮完整输入、原始响应、动作反馈、场景图与状态。

这些程序检查不替代真人盲操作或独立的真实拆装验证。费用来自返回 token 和所记录单价，包含检查/补测开销；Sol 的 Ark 单价尚未核实，只能标暂估。
