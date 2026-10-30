# 查看这批实验与另开新批次

## 先看结果

- [中文报告](README.zh-CN.md)：逐题结果、指标解释、费用、图表和限制。
- [本机回放](http://127.0.0.1:8831/ark)：逐轮实际输入、输出、环境返回、当前图与目标图。
- [结果网页](http://127.0.0.1:8831/ark-results/index.html)：完整表格和高清图。

`pilot.json` 是先启动的 Qwen 进程报告，`workers/` 是其他模型的独立报告。
看全部模型应使用 `combined-pilot.json` 或本机页面。它们合并同一批证据，不重复计算同一个 run ID。

## 接口

| 模型 | 服务商 | 本地配置 |
|---|---|---|
| GPT-6.1 Sol | Ark | ARK_API_KEY、ARK_SOL_ENDPOINT |
| Seed 2.1 Pro | Ark | ARK_API_KEY、ARK_SEED_PRO_ENDPOINT |
| DeepSeek V4.1 Flash | Ark | ARK_API_KEY、ARK_DEEPSEEK_ENDPOINT |
| Qwen3.8 Flash | Aliyun | ALIYUN_API_KEY |

配置放在项目 `.env`，不要提交该文件，也不要把 Key 放到命令参数中。
三个 Ark 接入点只用于用户指定的模型，不使用 Terra、DeepSeek 经济版、Seed Lite，也不转到 OpenRouter。

Sol 的 Ark 价格未核实，用户已授权直接运行。程序按暂定参考价记预算，不能保证实际 Ark 账单不超过该估值。
本批费用账本为 `ledger.private.json`，累计记账额度为 40 元。不得删除账本或调大额度来绕过限制。

## 本批已结束

`completed.json` 标记本批已归档，运行器会在任何付费请求前拒绝继续写入这个目录。
36 项运行保存原始 v2 输入；后续 v3 修正见 [输入问题与修复](INPUT-FIX.zh-CN.md)。

若以后要运行新的对照批次，先复制 `plan.json` 到一个新的输出目录，并将 `BRICK_ARK_PILOT_OUT` 设置为该目录的绝对路径。该设置同时适用于运行器、报告和检查脚本。新批次使用独立账本和证书，不改写旧成绩。以下执行命令只用于已明确配置的新目录。

## 运行前检查

本批预检包括初始图片包和带历史/候选页的图片包，验证图片提交、JSON 动作和生成参数。
它不能证明所有后续大输入都不受 TPM 限流。本批 Seed Pro 已暴露这一限制。
后续正式实验应增加最大图片包与长历史的额度检查，并确认接入点有足够 TPM。

```bash
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m unified_agent.ark_batch --models ark/gpt-6-1-sol-260929 --preflight-only --refresh-preflight
```

以上会产生付费接口检查。只在修复权限或配置后使用；不是无限重试。
已经成功的预检可复用 24 小时，核心输入/执行代码或配置改变后需要重新检查。

## 正式执行

每个条件一次。先检查参考动作可执行，再调用模型。正常拼装成功后才开放该模型的同题事故分支。

```bash
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m unified_agent.ark_batch --models ark/gpt-6-1-sol-260929 --isolated-worker
```

其他模型同样传入它们的完整 ID。Qwen 本批已从主报告执行，不要重新创建同一批实验。
`--resume` 保留已完成条件；发现尚未核对的中断运行时会停止，不会悄悄重跑。
API/格式/截断/几何拒绝分别保存。模型没有 GT、脚本前缀或自动修复。

Seed Pro 当前每次请求间等待至少 65 秒，避免简单的连发限流。超过一分钟仍报 TPM 时，应检查接入点的 token 限额和单请求预留，不能把问题归到模型能力。

## 不调用模型地重新生成报告和检查证据

```bash
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m unified_agent.ark_report
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m unified_agent.ark_audit
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m unified_agent.ark_visual_audit
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m unified_agent.ark_fairness
```

启动只读回放服务：

```bash
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m dynamic_arena.server --port 8831
```

这些检查证明请求、图片、记录和裁判之间的一致性；不替代真人盲操作、独立物理引擎和正式大样本实验。
