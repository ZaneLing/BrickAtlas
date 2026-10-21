# 静态视觉修复评测：visual-rgb-v3

当前仅接受 VLM / 支持图片输入的多模态模型。纯文本 symbolic/text 入口与 v1/v2 views 新调用已停用，历史请求、结果与费用账本保留。

## 输入

- 每个场景视角是独立 **1600×1200 PNG**，从 3200×2400 渲染后进行抗锯齿下采样。没有上采样、JPEG 压缩、表面编号、型号文字或错误框。
- 首轮提供 current/target 的立体、背面、顶部，共 6 张完整图，以及独立零件参考卡。卡片匿名句柄仅在 24 像素标题条里。
- 其余四个标准视角、任意角度、高清 crop 和按图中 point 选择都可通过 inspect 获取。
- 文本仅包含任务、操作格式、匿名动作句柄、视角元数据、计数与执行反馈。移除了零件型号、形状/颜色描述、坐标矩阵、支撑关系、阻挡关系、状态映射与错误标签。
- 放置仍使用离散注册候选。`inspect candidate` 返回无标签的放置预览，无合法性/正确性提示；这是图像驱动的离散操作接口，不是连续控制 VLA。
- `inspect partId` 是统一的辅助隔离观察，提供同相机坐标下该件的当前和目标图；对所有件开放，不使用故障件列表。必须报告其次数，不能把使用隔离观察的成绩称为仅外部相机的识别效果。
- 所有像素掩码、真值、错误根与可见性准入结果保留在评估器内，禁止放进提示词。

## 无费用检查与输入导出

在仓库根目录执行：

```bash
benchmark/.runtime/mlx-env/bin/python -B benchmark/brickplan-repair/eval/export_visual.py
benchmark/.runtime/mlx-env/bin/python -B benchmark/brickplan-repair/eval/test_vision.py
benchmark/.runtime/mlx-env/bin/python -B benchmark/brickplan-repair/eval/audit_vision_v3.py
```

交付见 `deliverables/brickplan-visual-input-v3/README.zh-CN.md`，包含高清图、完整请求 JSON、文献核对和验证结果。

## 后续模型实验

`run.py --select --models <vision-model-id>` 仅生成新版静态选题，默认目录 `deliverables/brickplan-visual-v3/`。运行时明确给出模型名；每例调用前重新检查高清像素差异准入。适配器拒绝没有 V3 协议或没有高清图片的请求。旧 `latest.py` 和 `static_audit.py` 已停止新调用。

目前没有新版付费模型结果。本轮只做离线修正，不增加 API 费用。历史 $2/$5 授权与费用账本不重置、不自动续用。原有预算保护继续生效。

旧 renderer/protocol/report 路径仅用于原始证据重放；旧最优代价也不能直接当新版扩展候选域的最优值。V3 的整库逐例准入由运行前检查执行；目前离线抽检 10 种案例主类型，不声称全库视觉或实物质量已完成验证。
