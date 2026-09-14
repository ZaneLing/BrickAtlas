# 六项总体计划：证据汇总

本报告持续累积同一个总体目标，不把阶段性交付等同于研究完成。当前完整就绪：否。

| 总工作包 | 已具备 | 尚未完成 |
| --- | --- | --- |
| 1. 研究定位 | 最近邻核心比较、H1-H5及反证条件、信息/统计合同 | 最终全文相关工作核对与独立研究判断 |
| 2. 数据与划分 | 暴露登记、分组隔离、许可发布检查 | 实际有授权的外部语义层、新冻结确认测试 |
| 3. 测量有效性 | 多解/原点/复制基线/字段诊断，重复对照complete | 人类指标校准及外部域有效性 |
| 4. 模型与统计 | 既有四模型验证、10组训练、重复/换序192/192调用，已知渲染器视觉基线complete | 更广任务的有效专用基线、充分来源与独立确认性结论 |
| 5. 独立审核复现 | 96候选审核包、不可覆盖导入、哈希绑定仲裁、来源级校准统计、同机离线复算 | 0条提交标签；身份独立性与第二人复现仍待完成 |
| 6. 论文与交付 | 论文、表格、原始日志、证据与总验收报告 | 主张收敛、科学门槛和实际届次提交核验 |

## 核心结果与解释

数据为5,120个程序结构、117,910个任务条件，不能将题数视为独立样本数。10组本地训练/基线共3,370条预测；没有编辑迁移正证据。四模型180次验证只有3个来源对象，不能据此确定稳定排名。

| 模型 | 同序重复不一致 | 换序不一致 | 超额不一致均值 [95%来源bootstrap区间] |
| --- | ---: | ---: | --- |
| openai/gpt-4.1-mini | 2/12 | 9/12 | 0.583 [0.333, 0.833] |
| openai/gpt-4.1 | 2/12 | 11/12 | 0.750 [0.500, 1.000] |
| google/gemini-2.5-flash | 0/12 | 6/12 | 0.500 [0.250, 0.750] |
| qwen/qwen3-vl-32b-instruct | 0/12 | 9/12 | 0.750 [0.500, 1.000] |

本次192次调用、12个来源，新费用$0.282100356；原累计账本$3.097410574。比较实际位姿而非选项标签。结果支持当前开发样本内的候选顺序敏感性，不证明总体规律、认知原因或稳定模型排名；各模型共享来源，不能合并扩大独立样本数。

## 技术交付

无runtime/无密钥同机复算：通过，21个命令；不等于外部独立安装。主文与补充材料见../../../../paper/，页数和编译检查以各自verification.json为准。技术发布清单与本研究就绪门槛分离。

## 人审指标校准

已有0条标签、0条仲裁，0/96候选形成明确结论。报告见../human-audit/CALIBRATION.md。误接受以人类拒绝数为分母，误拒绝以人类接受数为分母；没有有效分母时为不可估计，不报告零错误率。原标签及仲裁理由留在私有目录，公开聚合不包含审核者代码或自由文本。程序完成不代表真人审核完成。

## 专用视觉基线

公开输入渲染匹配基线已完成60题、16次换图控制，生成384个候选视图，0次API调用。图像条件成功44/44，换序保持同位姿16/16。只有4+12个既有开发来源；重复/换序不增加独立样本数。使用已知渲染器、规范配色和候选信息，不能当通用模型、真人观察验证或独立确认。报告见../visual-choice/REPORT.zh-CN.md。

## 门槛明细

- 通过：research-contract。Closest-work core, falsifiable questions and information/statistical boundaries are documented; not an exhaustive novelty certification.
- 通过：source-exposure-accounting。Training, validation, published pilot and merely prepared sources are distinguished.
- 待完成：external-semantic-data。No actual licensed human-designed/semantic structure layer has been integrated and audited.
- 通过：measurement-repeat-control。Same-order resampling and permutation must be paired on all 12 selected sources; completion is not proof of an effect.
- 待完成：independent-confirmation。All current model experiments remain adaptive development. A separately sourced frozen confirmation and justified precision are absent.
- 待完成：independent-human-review。0 submitted self-attested labels; 0/96 resolved items. Human identity/independence and wider calibration coverage remain unverified.
- 通过：runtime-free-replay。Same-machine copied environment without runtime/key; does not certify a second-person install.
- 待完成：external-reproduction。No independently executed second-environment reproduction receipt is available.
- 待完成：submission-manuscript。Development manuscript and supplement can be built; scientific gates and target-year submission checks remain outstanding.

## 必须由外部提供的证据

真实审核者的独立标签与仲裁、数据权利方许可及实际结构文件、第二环境执行记录。若确认研究超出原累计$4.50预算，需要新的明确费用授权，不能重置账本。

具体交接与冻结要求见../../../study/EXTERNAL_VALIDATION.md。剩余研究不只需要外部参与：外部数据适配、有效专用基线及确认性实验仍需实现和验证，不能把全部缺口转交给人工。

这些门槛没有通过时，不报告“已达到录取标准”。代码生成的许可字段、审核模板、统计表和PDF不是独立研究证据。
