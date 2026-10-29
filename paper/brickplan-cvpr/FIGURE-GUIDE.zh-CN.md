# 现版图示索引

所有现用图在 `figures-release/`，图中文字和标题使用 Comic Sans MS，PDF 内嵌字体。积木场景由当前题目或明确标注的旧版轨迹的精确几何重新渲染为 3200 × 2400；示例不改变模型的真实输入。

| 文件 | 内容 |
|---|---|
| `teaser.pdf` | 一排八步的动态参考轨迹，下一排八个完整物件／收尾例子 |
| `errors.pdf` | 八列静态错误／正常对照，当前与唯一目标上下配对 |
| `interaction.pdf` | 模型主动观察、调用动作、收到反馈的实际流程 |
| `static-repair.pdf` | 当前书架错色题的合法修复过程 |
| `eligibility.pdf` | 正常拼装通过、事故触发、有效性与修复统计的条件 |
| `coverage.pdf` | 模型长度、题数与错误类别分布；不是模型成绩 |
| `gallery-1.pdf` 至 `gallery-8.pdf` | 全部 310 个模型的上下文缩略图 |

具体题目 ID 和原始状态见 `evidence/release-figure-selection.json`、`evidence/release-render-states.json`。文件哈希与字体证据见 `figures-release/provenance.json`。

正式题库示意轨迹标为参考脚本。新增真实 API 轨迹独立标为旧版 v2 开发案例。正式 API 模型没有在本版完成测试，因此不画虚假的模型雷达曲线或成功率。

| 新增文件 | 内容 |
|---|---|
| `arena-trajectories.pdf` | 四行，每行八格：小汽车模型／GT、椅子模型／GT。前缀及事故现场一致，之后比较真实模型与合法参考续接 |
| `arena-input-output.pdf` | Markdown 中的宽版：真实 observe 请求、原始当前图和目标图、响应及信息边界 |
| `arena-requested-views.pdf` | 补充材料中的紧凑版：原始当前图和目标图，配实际请求及响应说明 |

轨迹高分辨率渲染为 3200 × 2400。可视白色凸点底板按 Arena 传感器的尺寸、凸点和变换生成；不改变实际状态。实际输入图保持原始 800 × 600 像素，不用放大图片冒充更高清的模型输入。GT 续接可用私有状态，不能当作模型的第二次运行。

[完整步骤和 JSON](ARENA-TRAJECTORIES.zh-CN.md)；[旧版轨迹证据](evidence/arena-traces.json)。
