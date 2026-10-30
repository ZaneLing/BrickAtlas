# 查看与运行统一视觉 Agent

## 1. 直接看这次已经跑完的过程

在项目根目录执行（本机已有服务时不用重复执行）：

```bash
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m dynamic_arena.server --port 8830
```

打开 [Agent 回放](http://127.0.0.1:8830/agent?run=agent-incident-openai-gpt-6-1-sol-20261030-175050-6d0c)。可逐步播放、换三种观看角度、放大图片，查看模型自己的计划、实际收到的图片、原始 JSON、执行反馈和最终评分。这里只读回放，不会产生 API 费用。

上方“操作后的真实状态”是给人看的。它不会自动发给模型；下面“本轮实际输入”才是模型当时看到的材料。

## 2. 新电脑安装

需要 Python 3.11、C 编译器、curl。克隆包含本次提交的完整仓库后，在根目录执行：

```bash
python3.11 -m venv .venv
.venv/bin/python -m pip install -r benchmark/brickplan-repair/reliability/requirements.lock.txt
export PYTHONPATH=benchmark/brickplan-repair
.venv/bin/python -m reliability.bootstrap
.venv/bin/python -m unittest unified_agent.test_agent unified_agent.test_symmetry unified_agent.test_providers bench_design.test_metrics dynamic_arena.test_transport_receipt
.venv/bin/python -m dynamic_arena.server --port 8830
```

`bootstrap` 安装仓库附带的碰撞网格，不依赖作者电脑上的旧缓存。原独立运行包仍保留其原版本；新 Agent 请使用本次源码。无付费凭证时，离线检查和本次日志回放仍可用。

API key 放在根目录 `.env` 或进程环境，变量名分别为 `DEEPSEEK_API_KEY`、`ALIYUN_API_KEY`、`OPENROUTER_API_KEY`。不要写进代码或提交仓库。

## 3. 以后真的再跑一次

以下命令会产生 API 费用。为新实验指定新的结果文件和费用账本；不要删除旧账本来绕过原费用上限。

```bash
PYTHONPATH=benchmark/brickplan-repair .venv/bin/python -m unified_agent.run \
  --models qwen/qwen3.8-flash \
  --cases 'SC:4096-1-alt-1488:dynamic:buried-repair' \
  --cap-usd 0.50 \
  --report next-qwen.json \
  --ledger deliverables/brick-atlas-unified-agent-v1/next-qwen-ledger.private.json
```

它会先独立正常拼装；成功才运行事故版本。一次最多装／拆一块，动作后是否观察由模型决定。不要拿新的正常成绩去放行旧配置的事故分支：程序检查同一题、同一 backbone、同一 Agent 配置及实现哈希。

阿里云／DeepSeek 直接调用，不回退到 OpenRouter。模型不可用、限流、超时、费用停止都会单列。当前普通回放页读取本次 `pilot.json`；其他实验可以用 `/agent?run=<结果里的 arenaRunId>` 查看单次完整日志。

## 4. 文件对应关系

| 文件 | 内容 |
|---|---|
| `EXPERIMENTS.zh-CN.md` | 三组实验、统一规则、预算和还没做的对照 |
| `pilot.json` | 本轮计划、补测说明、结果与费用汇总 |
| `case-audit.json` | 截断、参数错误、执行反馈、观察次数和分数 |
| `../brickplan-dynamic-arena/runs/agent-*/log.json` | 每一轮真实输入、原始输出、实际执行和反馈 |
| 同目录 `spectator.json` | 给人回放用的三视图、计划和步骤 |
| 同目录 `api/*.request.json.gz` | 真正发送的请求体，包含图片字节；不含认证头 |
| 同目录 `api/*.response.private.json.gz` | 服务商完整返回与用量 |
| 同目录 `record.private.json.gz` | 评价者保存的状态和事故信息；模型看不到 |
| `checks/` | 裁判修复复查、离线测试、界面截图 |

历史正常试跑被发现评分错误后，保留原结果，再离线重放原动作重新评分。`result.before-scorer-fix.json` 是原值；最终 `result.json` 记录修改原因。中止的运行也保留，不能把它当作完整失败题或丢掉费用。
