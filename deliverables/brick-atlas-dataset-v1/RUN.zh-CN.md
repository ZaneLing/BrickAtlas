# 本机查看与复查

在仓库根目录运行。下列命令不会调用付费模型。

## 看题、GT 和 Arena 回放

```bash
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m dynamic_arena.server --port 8810
```

打开 <http://127.0.0.1:8810/dataset/>。即使不启动服务，也可以直接打开本目录的 `index.html` 看模型、图片和 GT。

## 复查发布文件

```bash
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m scaling_release.release_check
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m unittest scaling_release.test_contract bench_design.test_metrics
```

`release_check` 核对全部发布题、逐模型回放证据、图片版本、GT 和 Arena 清单。原始候选检查报告中的房车颜色问题有意保留；那组题已经退回，不在发布清单中。

## 重新执行几何和接口回放

```bash
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m scaling_release.check --workers 3
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m scaling_release.legacy_check
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m scaling_release.arena_check
```

社区检查默认复用内容哈希一致的通过记录。需要强制重放某一模型时，先备份其 `private/<编号>/check.json`，将该检查文件移出目录后再运行。不要删除题目、原始来源或失败证据。

## 换一台电脑时

2026-10-30 起提供 [独立运行包与安装步骤](../brick-atlas-reliability-v1/RUN.zh-CN.md)，附带当前 310 个物件及候选位置需要的 919 份碰撞网格、逐件来源与许可、固定版本 Python 依赖和加载／观察／评分检查。已有题目不再要求准备作者电脑的隐藏网格缓存；导入全新来源仍属于另一条采集流程。

干净环境复现范围是同一台 macOS 的项目外目录和新 Python 环境，不声称已在 Linux／Windows 完成安装。真人审题、全面独立物理复核和新版真实 API 模型实验仍待开展。
