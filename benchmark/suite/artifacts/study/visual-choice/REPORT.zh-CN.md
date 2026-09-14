# 公开输入视觉匹配专用基线

方法：从公开BOM、候选、目录和最小角原点约定枚举合法两件结构，复用已知渲染器生成三个正交视图；只比较蓝色查询件的像素掩膜IoU，按候选最优合法解释选择。标题、页脚、灰色底座与中性网格文字不参与匹配。无图、无蓝色掩膜或候选并列时拒答，不按标签打破平局。底座位置和朝向经过枚举，不读取真值。

| 开发集/条件 | 成功/题数 | 已答 | 拒答 | 来源对象 |
| --- | ---: | ---: | ---: | ---: |
| pose-probes:choice-rgb | 4/4 | 4 | 0 | 4 |
| pose-probes:choice-permuted | 4/4 | 4 | 0 | 4 |
| pose-probes:choice-no-image | 0/4 | 0 | 4 | 4 |
| order-study:original | 12/12 | 12 | 0 | 12 |
| order-study:repeat | 12/12 | 12 | 0 | 12 |
| order-study:permuted | 12/12 | 12 | 0 | 12 |
| order-study:no-image | 0/12 | 0 | 12 | 12 |

换序后选择相同位姿：16/16；换图共16次，其中1次拒答，其余15个有效配对中9次选择改变。拒答不计为“不变”。

实际生成384个候选视图，执行耗时29.7秒；0次API请求。重放会重算像素匹配，但使用已存候选图，不重新启动浏览器。

## 解释边界

- 4 pose sources and 12 order sources are reused development objects, not 60 independent objects.
- All image conditions use three orthographic views. The original LLMs also received isometric views.
- Same renderer and canonical colors strongly favor this specialized baseline; no general semantic reconstruction claim.
- No-image abstention is deliberate, not a stochastic chance baseline.
- Replacement controls are mismatched observations and BOM; report image dependence, never task accuracy or causality.
- Missing target masks or tied candidates abstain. No rejection threshold for nonmatching but nonblank out-of-domain images is calibrated.
- Candidate rendering uses known simulator access and additional compute. Do not pool with one-shot model scores.

本结果可检验此小型、已知渲染器域是否包含可利用的候选位置图像信号，不是独立人审、真实图像或任意CAD有效性证据。算法在既有开发结果之后设计，不作为事前冻结的独立确认研究。原模型结果保持不变。
