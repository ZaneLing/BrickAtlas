# BrickPlan 论文：按当前题库和评估规则更新

更新日期：**2026-10-25**。

- [正文 PDF](main.pdf)：CVPR 双栏，**8页正文＋1页参考文献**。
- [补充材料 PDF](supplement.pdf)：20页，含完整物件清单、指标细则、实验表与历史证据。
- [Overleaf 源文件包](brickplan-cvpr-overleaf.zip)：上传后选择 `main.tex` 或 `supplement.tex` 编译。
- [本次修改说明](REVISION-2026-10-25.zh-CN.md)。

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

## 图片

新制9张数据／示例图，保留有用的历史说明书、流程、非唯一顺序和真实小车轨迹图。当前论文共引用14张不同图。

场景用实际积木几何原生渲染，3200×2400、2倍超采样；组合图600dpi，PDF/SVG文字为矢量。一排保留7–8幅场景的紧凑展示。发表图的分辨率与模型收到的原生800×600场景分开说明。

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

当前：`evidence/current-dataset.json`、`current-experiment-design.json`、`current-results-template.json`、`figures-current/provenance.json`。

历史：`benchmark-coverage.json`、`experiment-design.json`、`results-template.json`、`budget-single-run.json` 和旧生成脚本对应10月23日及更早版本。保留追溯，**不能用作当前数量、费用和实验计划**。当前 `build.py --refresh-figures` 已改用新脚本，不会自动恢复旧计划。

## 仍未完成

正式模型／独立真人实验、当前完整背景画面的可读性审核、配对API批量执行与事件效果记录、来源组置信区间，以及真正未用于展示的新社区来源。论文把这些边界写明；排版完成不代表实验完成或保证CVPR录取。
