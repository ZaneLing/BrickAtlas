# Brick Atlas

在积木世界里，测试模型能否发现错误、合法修复，并在连续拼装时恢复进度。

[English](README.md) · [仓库目录说明](REPOSITORY-MAP.zh-CN.md) · [历史版本](REPOSITORY-HISTORY.zh-CN.md)

## 当前正式版本

**310 个模型，4,685 道程序检查通过的题目：静态 1,600，动态 3,085。**

模型包含 57 个完整拼装、253 个明确收尾任务。437 个原始来源模型是素材池，不是 437 个可运行模型。历史记录和退回题目保留，但不算正式题量。

| 要看什么 | 入口 |
|---|---|
| 数据集状态、组成、题目 | [数据集说明](deliverables/brick-atlas-dataset-v1/README.zh-CN.md) |
| 最终检查发现什么、修了什么 | [最终检查报告](deliverables/brick-atlas-dataset-v1/FINAL-CHECK.zh-CN.md) |
| 每个模型、每类错误与题数 | [模型和题目列表](deliverables/brick-atlas-dataset-v1/MODEL-AND-QUESTION-LIST.zh-CN.md) |
| 图片、当前状态、目标、GT | [本地题库页面](http://127.0.0.1:8810/dataset/) · [Markdown 示例](deliverables/brick-atlas-dataset-v1/EXAMPLES.zh-CN.md) |
| 输入输出及评分 | [接口与 metrics](deliverables/brick-atlas-dataset-v1/INPUT-OUTPUT-AND-METRICS.zh-CN.md) |
| 统一视觉 Agent、真实 API 试跑 | [结果、回放、裁判修复与费用](deliverables/brick-atlas-unified-agent-v1/README.zh-CN.md) · [三组实验设计](deliverables/brick-atlas-unified-agent-v1/EXPERIMENTS.zh-CN.md) |
| 为什么和旧版五千多题不同 | [题量变化说明](deliverables/brick-atlas-dataset-v1/COUNT-CHANGES.zh-CN.md) |
| 英文论文 | [正文 PDF](paper/brickplan-cvpr/main.pdf) · [补充材料](paper/brickplan-cvpr/supplement.pdf) |
| 论文源码和预留实验表 | [论文说明](paper/brickplan-cvpr/README.zh-CN.md) · [Overleaf 包](paper/brickplan-cvpr/brickplan-cvpr-overleaf.zip) |

动态题统一进入 Arena：模型主动请求观察、选择角度、安装、拆卸、回看和结束。每次只操作一块；允许不同合法顺序。正式结果以实际最终状态为准，不照着 GT 的中间顺序判分。

**目前是程序检查通过，尚未完成本版独立真人审查、独立物理验证和全库正式模型实验。** 已归档一轮统一视觉 Agent 的真实 API 小样本试跑，不能当作全库排行榜。参考脚本成功不能当作模型成功。Qwen 固定走阿里云，DeepSeek 固定走官方 API，规则保存在 `AGENTS.md`。

## 本地打开

在仓库根目录执行（使用已有 Python 环境）：

```bash
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m dynamic_arena.server --port 8810
```

打开 [正式题库](http://127.0.0.1:8810/dataset/)；[全部历史记录](http://127.0.0.1:8810/dataset/all-questions.html) 按当前、退回、停用和待检查区分。Arena 的具体运行链接在 [运行指南](deliverables/brick-atlas-dataset-v1/RUN.zh-CN.md)。

## 重建和检查

```bash
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m scaling_release.release_check
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m unittest scaling_release.test_contract bench_design.test_metrics
npm run paper:build
```

全量重新执行参考动作使用 `scaling_release.check --force` 和 `scaling_release.legacy_check --force`，随后重新导出题单并执行发布检查。完整步骤见最终检查报告。

现用论文只有 `paper/brickplan-cvpr/`。旧网页、旧论文、旧题库按版本保留，不把它们的数量或模型成绩拼进现版。前端工程与历史功能说明见 [web/](web/README.md) 和 [历史说明](REPOSITORY-HISTORY.zh-CN.md)。
