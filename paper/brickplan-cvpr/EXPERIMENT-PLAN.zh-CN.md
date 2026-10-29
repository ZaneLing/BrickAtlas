# 当前论文实验计划

更新：2026-10-29。**这里是计划；没有调用付费API，也没有新模型成绩。**

## 先把样本和界面检查好

1. 对当前完整背景、唯一目标、同画布图片做真人可读性审核，保留不合格题和原因。
2. 确定同一份题单、预算、说明书／查看权限；每个模型／条件只测一次。
3. 先使用已接好的独立正常／干扰运行和 NQR，记录实际事故、恢复窗口和费用；需要因果下降结论时另接真实共享前缀。
4. 先以现有来源测试和公开开发样本分别汇报；不能拿公开示例声称新来源泛化。

正式题库 4,685 道（静态 1,600、动态 3,085）不等于最终开跑数量。310 个物件均有作者接触记录；现有 development/validation/test 按来源分开，但都不是未参与调试的新来源测试。最终实验题单仍待真人审查后确定。

## AI候选

下面沿用早期选定名单；实际可用端点、视觉支持、模型修订号和开放权重版本必须在开跑前核对。不能把候选名字写成已经测过。

| 候选 | 方式 | 原计划请求ID |
|---|---|---|
| GPT-6.1 Sol | API | `gpt-6.1-sol` |
| Claude Sonnet 5.5 | API | `claude-sonnet-5-5` |
| Gemini 3.8 Flash | API | `gemini-3.8-flash` |
| Claude Haiku 5.5 | API | `claude-haiku-5-5` |
| Qwen3.5-9B | Open | `Qwen/Qwen3.5-9B` |
| Qwen3.5-27B | Open | `Qwen/Qwen3.5-27B` |
| InternVL3.5-8B | Open | `OpenGVLab/InternVL3_5-8B-HF` |
| Qwen2.5-VL-7B | Open | `Qwen/Qwen2.5-VL-7B-Instruct` |
| Qwen2.5-VL-32B | Open | `Qwen/Qwen2.5-VL-32B-Instruct` |
| Gemma 3-12B | Open | `google/gemma-3-12b-it` |

## 19张预留结果表

| 编号／内容 | 对应文件 |
|---|---|
| E1: static repair (unmeasured). | `tables/main-models.tex` |
| E2: normal assembly and recovery (unmeasured). | `tables/main-dynamic.tex` |
| E3: strict shared-prefix paired outcomes (planned). | `tables/main-paired.tex` |
| E4: input controls (unmeasured). | `tables/main-ablations.tex` |
| E5: static error breakdown (unmeasured). | `tables/static-errors.tex` |
| E6: dynamic errors (unmeasured). | `tables/dynamic-errors.tex` |
| E7: stage-repair quality (unmeasured). | `tables/repair-quality.tex` |
| E8: structural strata (unmeasured). | `tables/difficulty.tex` |
| E9: repeated interventions (unmeasured). | `tables/multi-events.tex` |
| E10: checkpoint continuation (planned bank). | `tables/checkpoint.tex` |
| E11: input modality and state assistance (planned). | `tables/modality.tex` |
| E12: output localization (planned). | `tables/action-output.tex` |
| E13: independent snapshot detection (planned). | `tables/perception-probe.tex` |
| E14: same-state cross-model repair (planned). | `tables/cross-recovery.tex` |
| E15: observation robustness (unmeasured). | `tables/visual-robustness.tex` |
| E16: planning and computation (planned). | `tables/strategy-budget.tex` |
| E17: cost and action efficiency (unmeasured). | `tables/efficiency.tex` |
| E18: independent human operation (planned). | `tables/human-panel.tex` |
| E19: validity and failure ledger (unmeasured). | `tables/failures.tex` |

## 真人与尚未实现的对照

建议72个条件、6位独立操作参与者、每人36个条件，总216次；同一个人不看一对中的正常与错误两题。当前题单和排程需要按新来源重新选，历史“B/C说同意”不算独立数据。真人只点击，不写文字或JSON。

真人独立操作先报正常完成BCR、干扰题完成ICR和实际触发TR。不同人的操作历史不能复制成API分支，因此不能直接当作共用前半段的配对修复CRR；系统直接给定中途状态则标为C任务。真人的因果比较需要单独设计。

C指定中途开始、独立检测定位、文字状态／图文状态、自由坐标与跨模型失败状态库尚需补建或接入。表里留空，不能用参考路线填。

## 预算

旧版本8,030个工作单元和旧美元估算不适用于新题库。当前不新增预算承诺。先选定数量，再用当前输入的小样本记录每决策图片、token、价格和分支长度，按“正常运行＋干扰运行＋实际图片与历史token＋计费重试＋本地推理资源；严格配对时另记共享前缀”算钱。不得偷偷增加三次重复或顶级昂贵模型。


现版机器可读方案为 `evidence/release-experiment-plan.json`；19 类表格的空结果为 `evidence/release-results-template.json`。`current-*` 文件属于历史快照。正文主要结果汇总表与补充材料使用同一候选名单。
