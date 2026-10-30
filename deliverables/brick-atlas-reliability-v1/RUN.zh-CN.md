# 从独立运行包安装和复查

## 环境

已检查的环境：macOS、Python 3.11。需要可用的 C 编译器来构建本地栅格化器。首次安装 Python 依赖需要网络，题库运行不再需要作者电脑的碰撞缓存或上游网格下载站。Linux／Windows 未在本轮实际安装验证。

下载同目录 `release/brick-atlas-runtime.zip`，解压到一个新目录。下面所有命令在解压后的根目录运行；不用原仓库的 Python 环境。

```bash
python3.11 -m venv .venv
.venv/bin/python -m pip install -r benchmark/brickplan-repair/reliability/requirements.lock.txt
export PYTHONPATH=benchmark/brickplan-repair
.venv/bin/python -m reliability.bootstrap
.venv/bin/python -m reliability.check
.venv/bin/python -m unittest bench_design.test_metrics dynamic_arena.test_transport_receipt
```

`bootstrap` 检查归档与每份网格的 SHA256，然后安装 919 份网格到这个解压目录的 `benchmark/.runtime/brick-atlas-data/`。如果自己设置了 `BRICKNET_DATA`，它会优先使用指定目录；独立复现时请不要指向旧作者缓存。

`reliability.check` 会执行静态修复、正常动态拼装、有事故动态修复、同现场两分支比较，以及技术故障剔除检查，覆盖 SC、D、E7 三个来源银行。结果在 `deliverables/brick-atlas-reliability-v1/checks/`。其中脚本使用评价者已知的参考路线，**用于检查接口和裁判，不是模型实验**。

### 检查解压文件是否被改动

```bash
.venv/bin/python - <<'PY'
import hashlib, json
from pathlib import Path
manifest = json.loads(Path('package-manifest.json').read_text())
for name, expected in manifest['files'].items():
    assert hashlib.sha256(Path(name).read_bytes()).hexdigest() == expected, name
print('全部文件哈希一致', len(manifest['files']))
PY
```

## 给真人打开页面

```bash
PYTHONPATH=benchmark/brickplan-repair .venv/bin/python -m reliability.review --port 8820
```

本机浏览器打开：

- A 看 GT：<http://127.0.0.1:8820/?person=A&role=gt>
- B 盲操作：<http://127.0.0.1:8820/?person=B&role=blind>
- C 单步拆装：<http://127.0.0.1:8820/?person=C&role=physics>

每页三选一提交，不需要 JSON 或文字。盲操作可以主动看当前／目标、换视角、看库存和候选位置、查说明书、回看历史、安装、拆卸和提交完成。答案保存在 `deliverables/brick-atlas-reliability-v1/review/responses/<版本>/<A或B或C>/<检查方式>/<题号>/`；旧版本不删除。自动化页面测试使用独立临时目录，不进入真人统计。

机器可读汇总：<http://127.0.0.1:8820/api/summary>。运行包不附带真人个人结果。这里没有用户认证系统，只供本人电脑上的本地检查使用。

## 接一个自己的模型程序

模型适配器通过标准输入接收一份 JSON：`model` 与完整 `messages`，图片为 base64 data URL。标准输出只返回一份工具调用 JSON，日志写标准错误。调用例子：

```bash
PYTHONPATH=benchmark/brickplan-repair .venv/bin/python -m reliability.run \
  --id 'SC:158-1:static:missing' \
  --actor 'your-model-id' --max-decisions 60 \
  --output deliverables/my-static-run \
  --policy-command .venv/bin/python your_policy.py
```

适配器例子骨架（请自行接入实际模型，当前不代选付费服务）：

```python
import json, sys
request = json.load(sys.stdin)
# response = call_your_model(request['messages'])
# print(response)  # 只能输出 {"tool": ..., "args": ...}
```

只测试接口也可用 `--actions actions.jsonl`，每行一个工具调用。手写动作属于脚本证据。`bench_design.run_episode` 和 `bench_design.run_autonomous` 默认也转入上述分页接口；只有显式传 `--legacy-full-context` 才运行旧版整包观察逻辑，供历史实验复查。

### 正常拼装，以及同故障现场的比较

`reliability.run --normal` 关闭该题的外部事故。完整的正常前置检查、事故前缀、复制现场、两分支继续执行：

```bash
PYTHONPATH=benchmark/brickplan-repair .venv/bin/python -m reliability.paired \
  --id 'SC:158-1:dynamic:missing' --actor 'your-model-id' \
  --max-decisions 60 --output deliverables/my-new-pair \
  --policy-command .venv/bin/python your_policy.py
```

输出目录必须是新目录，不能覆盖旧结果。模型、采样参数和适配器版本应固定；两分支共享同一故障现场但保留不同历史，定义见 [协议说明](INPUT-AND-PAIRED-PROTOCOL.zh-CN.md)。

外部命令可能自己调用收费 API；运行器不会替它限制服务商账单。费用为 `null`，不会把未知费用写成免费。此次交付中的检查没有运行这个付费适配器入口。

## 输出放在哪里

| 文件 | 用途 | 是否能给做题模型 |
|---|---|---|
| `log.json` | 每轮公开请求、图片 URL／哈希、模型工具调用、工具反馈、汇总指标 | 只能给该模型本轮应见的请求，不能把全局结果一次性发出 |
| `result.json` | 完成情况、合法性、格式错误、事故状态、输入负担等 | 运行结束后评价者使用 |
| `record.private.json.gz` | 内部状态、GT、事件和裁判审计 | 否 |
| `spectator.json` | 观看者的三视角过程、事件和结果 | 否 |
| `paired/pair.private.json` | 同现场证明、事故快照、完整前缀 | 否 |
| `paired/pair-result.json` | 两分支结果及比较是否有效 | 评价者使用 |

图片实际文件位于 `deliverables/brickplan-dynamic-arena/assets/<sha256>.png`；`/assets/…` 是服务端路由，不是互联网地址。分享运行结果时要一起保存日志引用的图片。原服务商适配器还会保存带请求哈希的原始收据；外部命令入口没有服务商收据时不会伪造 token 或美元用量。

归档包含评分所需的私有案例；要发布模型端数据，应仅通过工具接口暴露当前公开请求，不能把整个目录作为模型上下文。
