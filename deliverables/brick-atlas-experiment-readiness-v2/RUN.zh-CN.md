# 后续实验怎么运行

从仓库根目录执行，使用现有环境。密钥只从 `.env` 或进程环境读取，不放进命令。

## 1. 免费检查

```bash
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m unittest unified_agent.test_agent unified_agent.test_symmetry unified_agent.test_providers unified_agent.test_readiness bench_design.test_metrics dynamic_arena.test_transport_receipt
```

逐题重新检查全部 4,685 题的可执行性（需要较长时间，不调用模型）：

```bash
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m unified_agent.casecheck --all --workers 3
```

核对保存的 API 图片、请求和费用回执（不再调用模型；历史记录过期后仍能核对）：

```bash
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m unified_agent.audit_readiness
```

## 2. 正式实验之前：少量付费接口检查

```bash
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m unified_agent.readiness --cap-usd 0.40
```

检查 DeepSeek Flash、Qwen3.8 Flash、Gemini 2.5 Flash 和 GPT-6.1 Sol，每个模型两个真实多模态请求。已有通过证书且代码、配置未变、未过期时显示 `CACHED PASS`，不重复付费。

证书过期或实现变化时，显式加 `--refresh` 才会重新付费。旧证书和原请求会保留在历史目录。费用使用同一个累计账本；**不要删账本来绕过预算**。

只检查某个模型：

```bash
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m unified_agent.readiness --models qwen/qwen3.8-flash --cap-usd 0.40 --refresh
```

## 3. 跑 case

下面是运行示例，执行会产生模型费用；本次修复没有启动此项完整拼装实验。

```bash
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m unified_agent.run --models qwen/qwen3.8-flash --cases SC:4096-1-alt-1488:dynamic:buried-repair --cap-usd 1.00 --report pilot.json
```

入口会先验证接口证书和当前 case，然后跑正常分支，正常成功才跑事故分支。同一题的两个分支和不同模型共用同一套预算规则。`--cap-usd` 是该账本的累计金额上限，不是每个 case 的上限；已有账本的较低上限不会被自动提高。

结果在本目录的 `pilot.json`，每轮原始 API 请求、模型动作和现场图在 `../brickplan-dynamic-arena/runs/agent-*/`。已存在的报告不能覆盖；新批次应明确指定新的 `--report`，并保留同一费用账本。

## 4. 看日志

```bash
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m dynamic_arena.server --port 8831
```

打开 `http://127.0.0.1:8831/agent`。默认显示新版 `pilot.json`，尚未运行新版完整实验时显示旧版试跑；`?version=1` 可固定看旧版。单条运行可用 `?run=运行目录名` 打开。网页只能读日志，不会调用模型。

## 5. 遇到问题时

| 状态 | 下一步 |
|---|---|
| `preflight_failed` | 看具体缺哪个证书／哪条 case 检查失败，修复后重新检查 |
| `output_truncated` | 该次请求不执行动作，保留原输出；统一调整整个实验条件后新建批次，不单独给某个模型加额度 |
| `API_MODEL_NOT_FOUND` / 403 | 核对该账户和模型权限；不自动换平台或模型 |
| `API_RATE_LIMIT` | 当次停止；另设明确的新批次重试，保留原记录 |
| `API_TIMEOUT` | 先向服务商核对该请求是否扣费，处理未结算账本后再运行 |
| JSON／参数不合法 | 日志保留原回复和反馈；单列接口指标，不把它直接解释成看不懂积木 |
| 碰撞、无连接、无法拆出、最终状态错误 | 属于动作或任务结果，继续按正式规则记录 |
