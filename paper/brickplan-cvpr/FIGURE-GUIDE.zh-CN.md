# 新版出版图：怎么画、展示什么

当前使用 `figures-publication/` 的14张重设计图；补充材料保留一张原有的题库分布图。参考与前后对比见[设计修改记录](DESIGN-REVISION.zh-CN.md)。

| 图 | 文件 | 展示内容 |
|---|---|---|
| 任务总览 | `teaser.pdf` | 静态错误到修复、动态已有主体到被干扰后完成、8个物件。 |
| 输入输出循环 | `interaction.pdf` | 唯一目标、当前RGB、一个动作、合法性检查、下一状态。 |
| 物理错误 | `error-atlas.pdf` | E01–E07与正常S0；同组相机和灯光一致。厚度用特写，偏移／装反用后侧视角。 |
| 内部返修 | `access-repair.pdf` | 一个错件，四个正确盖件临时拆下，换件后恢复；真实10步可行路线。 |
| 配对资格 | `paired-recovery.pdf` | 共用前半段的正常／干扰分支；CRR与ΔSR分母不同。 |
| 静态计分实例 | `metric-example.pdf` | 残差2→1→0、F1与ER上升；未补回正确件仍未完成。直接调用当前计分器计算。 |
| 数据分析 | `dataset-analysis.pdf` | 各范围题数、按物件配置计权的安装量CDF、真实多标签错误覆盖。 |
| 路线诊断 | `route-diagnostic.pdf` | 实际脚本诊断9/36与36/36，无虚构模型曲线。 |
| GT与真实模型轨迹 | `repair-filmstrip.pdf` | 每排8个状态；参考、历史模型外部修复、历史模型自身纠错。 |
| 42个完整物件 | `whole-object-atlas.pdf` | 原有完整物件全部保留，统一材质／光照。 |
| 13个收尾配置 | `module-atlas.pdf` | 完整主体背景与实际操作件数。 |
| 26个诊断结构 | `diagnostic-atlas.pdf` | 历史结构诊断单列。 |
| 9个新增配置 | `added-atlas.pdf` | 3个原始完整LDraw、5个长程序物件、扩大屋顶。 |
| 两种合法顺序 | `alternative-orders.pdf` | 完整小屋作背景锚点；不同第三步、同一个最终屋顶。 |

## 质量与证据

- 所有当前论文图内的文字统一为**Comic Sans MS**：正文标注、图例、坐标轴、数字用常规体，标题和原有加粗标注用Bold。PDF嵌入字体，SVG文字转成矢量轮廓，PNG直接以该字体渲染。
- 152个出版场景来自题目证书、已验证参考动作或历史轨迹，不用AI画假积木。
- 场景3200×2400、抗锯齿、材质与接触阴影；组合图600dpi，注释和图表为矢量。
- 仅裁去画布留白，同一对照／轨迹共享取景，不拉伸积木几何。细节图明确标注。
- 论文橙框和状态颜色仅用于解释，不进入模型输入。
- **评测RGB、800×600原生场景、完整背景、数据和计分未因本轮排版改变。**

`publication_scenes.py`导出原始几何和状态，`render_publication.mjs`本地渲染，`design_figures.py`做版面和矢量注释。每张PNG有缓存与哈希记录，所有图由`figures-publication/provenance.json`追溯。

只重新生成图中文字和统计图，不重渲染积木几何：

```bash
benchmark/.runtime/mlx-env/bin/python paper/brickplan-cvpr/build.py --refresh-typography
```

字体在`figure_typography.py`统一设置；`verify.py`直接检查正文／补充材料引用的15张图的PDF字体，防止静默替换成其他字体。
