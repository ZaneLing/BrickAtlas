# 当前论文图片说明

更新：2026-10-25。全部场景来自实际几何，不用AI画示意积木代替题目。

| 图 | 文件 | 放什么 |
|---|---|---|
| 总览 | `figures-current/teaser.pdf` | 24幅小场景，静态／完整拼装／明确收尾。 |
| 错误 | `figures-current/errors.pdf` | 七类实际错误、提前封口、内部返修、正常对照；每对同框当前与阶段GT。 |
| 新增配置 | `figures-current/added-objects.pdf` | 三个完整原始LDraw、五个长程序物件、扩大屋顶。 |
| 原有完整物件 | `figures-current/objects-all.pdf` | 全部42个，按当前去重题数重标。 |
| 历史机制 | `figures-current/mechanisms-all.pdf` | 全部26个，只作诊断。 |
| 社区主体 | `figures-current/modules-all.pdf` | 12个原始收尾来源，显示完整主体；扩大屋顶另示。 |
| 分布 | `figures-current/distributions.pdf` | 当前主题型、结构G分级和动态事故数。 |
| 雷达模版 | `figures-current/*radar.pdf` | 两张无模型曲线的空模板，未测不补0，不用面积排名。 |
| 交互循环 | `figures-v2/protocol.pdf` | 观察、单块动作、执行器、未提示变化。 |
| 说明书 | `figures-v2/instructions.pdf` | 一排7步、单块零件与状态。 |
| 不同合法顺序 | `figures-v2/alternative-orders.pdf` | 中途不同，最终一样。 |
| 真模型旧示例 | `figures-v2/repair-comparison.pdf` | 一排8状态，GT／旧模型外部修复／自身纠错，明确历史版本。 |
| 可行返修路线 | `figures-v2/recovery.pdf` | 旧执行器路线，不能说成模型成绩。 |

共14张不同图。场景3200×2400、2倍超采样、组合图600dpi，文字和箭头保留矢量。几何小图保持紧凑，一排7–8幅为主。

论文的橙框、正确性颜色和标注用于解释。不能原封不动放入盲测模型的当前状态图。模型收到的是原生800×600场景等接口图片；高清发表图不等于提高了模型的输入质量。

`figures-current/provenance.json`记录新图来源、状态、分辨率和哈希；旧图仍由`figures-v2/provenance.json`追溯。`build.py --refresh-figures`只更新当前图与清单，不重写旧计划。
