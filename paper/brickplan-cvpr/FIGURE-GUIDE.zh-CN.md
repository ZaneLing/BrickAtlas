# 现版图示索引

所有现用图在 `figures-release/`，图中文字和标题使用 Comic Sans MS，PDF 内嵌字体。积木场景由当前题目的精确几何重新渲染为 3200 × 2400；示例不改变模型的真实输入。

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

所有修复轨迹明确标为参考脚本。正式 API 模型没有在本版完成测试，因此不画虚假的模型雷达曲线或成功率。
