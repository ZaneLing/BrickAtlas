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

## 30 张预留结果表

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


现版机器可读方案为 `evidence/release-experiment-plan.json`；30 类表格的空结果为 `evidence/release-results-template.json`。`current-*` 文件属于历史快照。正文主要结果汇总表与补充材料使用同一候选名单。

## 新增 E20–E30：做什么，为什么做

原 E1–E19 保留，下面新增 11 组，合计 30 组。补充材料已为每组放好表格，所有结果留空。每组并不意味着要立刻把全部模型、全部题再跑一遍；先完成必要的主结果和可信性检查，再挑少量代表模型做有针对性的对照。

| 编号 | 用人话说要做什么 | 记什么结果 | 当前情况 |
|---|---|---|---|
| E20 | 用照说明书拼、不观察、定时查看等简单办法做对照 | 成功率、动作数、查看次数 | 策略对照待接入；有答案的程序单列 |
| E21 | 分别告诉模型事故时间、错的零件、精确状态、修复方案 | 给哪种帮助后提升多少 | 待实现；不能冒充普通输入成绩 |
| E22 | 出事以后，它过几轮才重新看？过几轮才修好？ | 首次新观察延迟、修复延迟、4/8 轮内修好比例 | 从完整日志补统计；看过不等于发现 |
| E23 | 同样的错误放在早期、中期、后期，或增加错误数量 | 触发率、修复率、剩余错误、返工量 | 变更条件后必须重新检查题可修 |
| E24 | 换一种正确顺序、换同型件编号，裁判还会判对吗？ | 成对评分一致率、不一致个数 | 部分单项检查已有；整组结果未测 |
| E25 | 让独立的人或另一套程序判断动作能不能做 | 错放行、错拒绝、意见不确定各多少 | 尚未完成独立核查 |
| E26 | 人只看模型可看的图，能看清目标、错误和操作吗？ | 初始可见、转视角后可见、始终不可见、意见一致性 | 待独立盲审；看 GT 的审核另列 |
| E27 | 换成从没参与出题调试的新来源，还能做好吗？ | 按新旧来源、完整件／收尾任务分别报告 | 需要另选真正新来源 |
| E28 | 按每题、每物件、每来源算，结论是否一致？ | 成功率、覆盖率、来源抽样的置信区间 | 待正式日志；不增加三次模型重复 |
| E29 | 同一个故障现场，让新模型接手，或原模型继续；分别主动看与定时看 | 4 种条件下的成功、返工、观察 | 需要保存真实中途状态并匹配权限和预算 |
| E30 | 看整个过程是在变好、返工、停滞，还是太早说完成 | 平均／最好 F1、停滞跨度、错误提交率 | 待补日志统计；必须同时报最终成功和长度 |

### 指标怎么防止算歪

- **重新观察的等待轮数**：事故后第一次主动获取当前图的轮次差；回看旧图不算。一直没看就记“未观察到”，不能填成 0。
- **4/8 轮内修好**：只统计有效事故、正常前测通过且运行有效的情况。提前结束按结束状态继续计算：没修好就提前提交仍算没修好，不能丢掉。4/8 轮内又发生新事故或出现技术中断的窗口单列，不把后一次干扰算到前一次头上。
- **错放行**：独立检查认为不合法的动作里，引擎却接受了多少。**错拒绝**：独立检查认为合法的动作里，引擎却拒绝了多少。两者分母不同。
- **过程质量**：按每轮真实积木状态算；不能把观察旧图当作状态变好了。平均分高而最终失败，仍然是失败。
- **停滞**：成功执行的拆装没有减少缺件／多件数量；事故前后分开算。为了修底层而先拆上层也可能被计到，因此必须与返修类型和最终结果一起解释，不能直接说模型乱做。
- **静态与动态对照**：场景、库存、目标、可选动作、看图权限和剩余轮数一样，再比较是否保留之前的操作历史。

### 建议执行次序

1. 先做 E24–E26：裁判、公平性和看图检查，主要不花 API 钱。
2. 然后跑 E1、E2、E5–E9、E17、E19：正式主结果、类别和费用。每条件一次。
3. 优先挑代表模型做 E20、E22、E29：把“静态到动态”的核心故事做扎实。
4. 再按剩余预算补 E21、E23、E27、E28、E30 和原有其他对照。

费用不从表格数量倒推。本次只补论文和离线轨迹检查，新增 API 费用为 0 美元。正式预算仍需要选定题单后，按当前协议的小样本真实计费估算。
