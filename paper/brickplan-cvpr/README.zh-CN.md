# BrickPlan 论文：按当前题库和评估规则更新

更新日期：**2026-10-25**。

- [正文 PDF](main.pdf)：CVPR 双栏，**8页正文＋1页参考文献**。
- [补充材料 PDF](supplement.pdf)：21页，含完整物件清单、指标细则、实验表与历史证据。
- [Overleaf 源文件包](brickplan-cvpr-overleaf.zip)：上传后选择 `main.tex` 或 `supplement.tex` 编译。
- [本次图形与版面修改、页面前后对比](DESIGN-REVISION.zh-CN.md)。
- [此前的数据与指标更新](REVISION-2026-10-25.zh-CN.md)。

## 论文现在用哪份数据

以 [题库规范](../../deliverables/brickplan-benchmark-spec/README.zh-CN.md) 和 [评估方案](../../deliverables/brickplan-benchmark-spec/EVALUATION.zh-CN.md) 为准。

| 单位 | 当前数量 | 论文怎么说 |
|---|---:|---|
| 保留目录记录 | 5,839 | 含同任务重复记录，不能全叫独立题目。 |
| 去重题目 | **5,720** | 同来源、配置和任务规则内，按实际物理状态去重。 |
| 主评测候选 | **5,452** | 静态3,697，动态1,755；还需要当前界面的图片／真人审核。 |
| 单列动态诊断 | 268 | 历史结构224、任意裁切44，不代表完整物件拼装。 |
| 参考路线运行条件 | 5,922 | 包含复用对照和历史接口别名；全部合法回放通过。不是模型成绩。 |
| 动态主配置 | **63** | 完整物件50、明确收尾13；不等于63个社区源物件。 |
| 来源组 | 154 | 不跨划分；45个已展示／调试来源归公开开发。 |

完整物件50＝原有程序物件42＋较长程序物件5＋完整LDraw小物件3。收尾13来自12个社区源物件，其中博物馆有扩大模块版本。

## 指标和实验怎么改了

- **静态**：S1完全修复SR、位置零件F1、错误减少ER、最终新损坏DR；S0正常验收另算误修FR。
- **动态**：正常完成BCR、干扰题原始完成ICR、实际触发TR、合格配对的恢复CRR、配对完成差ΔSR。
- **多次事故**：43道主任务，37道两次、6道三次；分开记录逐事件修复、修好后保持、部分触发。
- **结束对即可，顺序不必照GT**；同形同色可互换件不因编号不同判错。
- **403／429／超时、格式错误、字段错误、物理拒绝分开**；未触发不能说成漏检。
- 保留十个候选模型，每模型／条件一次。**19张实验结果表全部未测留空**。
- C中途开始、独立检测、文字状态、自由坐标等明确写成待补／待接入，不能当作已经跑完。

## 这一轮图形与排版升级

[对照正式论文的修改记录与前后对比](DESIGN-REVISION.zh-CN.md)。实际查看了BrickNet、VSI-Bench、Spatial457的CVPR原始页面和BrickGPT的ICCV原始页面。

- 全面重做14张出版图：任务总览、输入输出循环、错误细节、内部返修、配对资格、真实计分例子、数据覆盖、路线诊断、真实修复轨迹和完整物件图册。
- 场景来自真实LDraw几何，用材质、光照、接触阴影重新渲染；相同对照保持相机、光照和取景一致。厚度、偏移和装反用更清楚的细节／视角展示。
- 原生3200×2400，多重采样抗锯齿；组合图600dpi，图中文字、箭头和统计图为矢量。
- 所有图内文字统一为**Comic Sans MS**，标题及加粗文字使用Bold；PDF嵌入字体，SVG转为矢量轮廓，坐标轴、图例、数字和动作示例也统一。
- 正文围绕研究问题、任务、数据、评估和真实诊断；10个候选模型和受控实验设计仍列明。19张未测成绩表集中保留在补充材料，空雷达不进入当前稿。
- **论文图片的美化不改变模型答题时的800×600原生场景、完整背景、题目或计分规则。**

## 怎么编译和检查

```bash
benchmark/.runtime/mlx-env/bin/python paper/brickplan-cvpr/build.py
```

重新生成当前图、题目清单和空实验表：

```bash
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python paper/brickplan-cvpr/build.py --refresh-figures
```

重跑旧十二模块路线诊断，不调用模型：

```bash
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python paper/brickplan-cvpr/protocol_study.py
```

`verify.py` 检查当前题库／代码依赖哈希、去重和覆盖数量、空成绩、历史证据、官方样式文件、8页正文、引用、溢出、字体嵌入和图片分辨率。页面还需渲染后目视检查。

## 证据文件怎么读

当前：`evidence/current-dataset.json`、`current-experiment-design.json`、`current-results-template.json`、`figures-publication/provenance.json`。

历史：`benchmark-coverage.json`、`experiment-design.json`、`results-template.json`、`budget-single-run.json` 和旧生成脚本对应10月23日及更早版本。保留追溯，**不能用作当前数量、费用和实验计划**。当前 `build.py --refresh-figures` 已改用新脚本，不会自动恢复旧计划。

## 仍未完成

正式模型／独立真人实验、当前完整背景画面的可读性审核、配对API批量执行与事件效果记录、来源组置信区间，以及真正未用于展示的新社区来源。论文把这些边界写明；排版完成不代表实验完成或保证CVPR录取。
