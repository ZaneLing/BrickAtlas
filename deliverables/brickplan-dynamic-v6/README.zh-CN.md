# 动态 Bench v6：本轮已经做好的内容

## 先看结果

| 项目 | 之前 v5 | 现在 v6 |
|---|---:|---:|
| 全部动态题 | 317 | 1,872 |
| 全部结构 | 30 | 68 |
| 像实际物品的完整模型 | 4 | 42 |
| 完整物件题 | 32 | 1,588 |
| 中途干扰类别 | 10 | 12 |

这里“模型”指积木物件。没有把换颜色当作一个新物件：新增的是家具、交通工具、家电、机器、建筑等不同造型。[直接看全部物件](gallery.html)｜[一张总览图](object-gallery.png)

1,872 题里有 **160 道正常题、1,712 道干扰题**。42 个完整物件共 1,588 题，其余 284 题是用于测试连接、遮挡等问题的局部结构。完整物件 6–15 块，全部结构 4–15 块；这些是简化造型，尚不是上百块的大套装。

## 现在怎么用

- 真人直接打开 [A](http://127.0.0.1:8767/A)、[B](http://127.0.0.1:8767/B)、[C](http://127.0.0.1:8767/C)。每个入口有 126 道抽样操作题，覆盖 42 个物件；不用写文字、不用返回 JSON。每一步保存，换题后可继续。
- 先看右侧的最终目标，再选零件、看候选位置，点卡片安装。一回合中可以随时看当前状态，一次只装或拆一块。看明白中间变化后，继续修好同一个物件。
- [输入输出说明](INPUT-OUTPUT.zh-CN.md)：用图和例子解释每一步给什么、回什么。
- [修了什么、还欠什么](FIX-REPORT.zh-CN.md)；[正式评测办法](EVALUATION.zh-CN.md)；[物件逐项清单](OBJECTS.zh-CN.md)。

## 检查结果及边界

- 42/42 个完整物件能从空底板装起来，物件自身也连在一起；1,872/1,872 题的原始拼装、干扰和恢复路径通过几何检查。
- 一直照原说明拼、完全不处理干扰的程序：正常题 160/160 完成，干扰题 0/1,712 完成。能读取正确答案再拆开重拼的检查程序：1,872/1,872 完成。后者只用来证明题目能修，不代表 AI 成绩。
- 1,553 道干扰题通过当前图像差异筛选；136 道“自己的动作被抵消”和 23 道低对比变化分开报告，不能混作普通漏检题。
- 新版真人正式答卷 **0**，真实 API 模型实验 **0**；本轮实际 API 花费 **$0**。旧版真人与模型结果保留在 v5，不套用到新版。
- 机器检查并不能保证“模型失败一定是模型的问题”。仍要完成正常拼装对照、独立真人验证及完整回合评测，再讨论漏检和恢复能力。

## 文件

`cases.private.json`、`models/*/qualification.json`、`index.json`、`human-review/answer-key.private.json` 都是出题和评分资料，含类别或答案，**不得直接放进模型请求**。真正输入由 `interface.py` 的 `packet()` 生成。

程序在 `benchmark/brickplan-repair/dynamic_v6/`。旧 v5 的题目和实验保留；当前论文原有数字属于旧实验版本，不能把题量变大当成新增模型实验。

重新打开本机服务：项目根目录双击 `启动动态拼装v6.command`。不需要公网服务器。

### 重建及检查（给维护代码的人）

```bash
export PYTHONPATH=benchmark/brickplan-repair:benchmark/brickplan-repair/eval:benchmark/brickplan-v1
benchmark/.runtime/mlx-env/bin/python benchmark/brickplan-repair/dynamic_v6/admit_objects.py
benchmark/.runtime/mlx-env/bin/python benchmark/brickplan-repair/dynamic_v6/build.py --resume
benchmark/.runtime/mlx-env/bin/python benchmark/brickplan-repair/dynamic_v6/audit.py --resume
benchmark/.runtime/mlx-env/bin/python benchmark/brickplan-repair/dynamic_v6/test_contracts.py
benchmark/.runtime/mlx-env/bin/python benchmark/brickplan-repair/dynamic_v6/test_runner.py
benchmark/.runtime/mlx-env/bin/python benchmark/brickplan-repair/dynamic_v6/build_report.py
```

## 2026-10-23 开发试跑更新

本次对当前题库做了小规模真实 API 试跑，原文中的“API 为 0”指构建发布时的状态。正式模型主表仍未收集完成。实测逐题费用、接口问题和本轮修复见 [10 美元试跑报告](../brickplan-budget-pilot-2026-10-23/README.zh-CN.md)。模块版已修正查看操作之后的上一状态图片；付费旧记录保留原样，修复后只做了免费回归检查。
