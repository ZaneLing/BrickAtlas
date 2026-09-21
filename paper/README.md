# 当前论文

唯一当前写作入口：[main.tex](main.tex) · [main.pdf](main.pdf)；
科学附录：[supplement.tex](supplement.tex) · [supplement.pdf](supplement.pdf)。
旧稿及中间审稿材料统一在 [../tem/](../tem/README.md)。
当前图文版为 9 页正文、1 页参考文献和 8 页附录。

论文主线是：问题动机 → Benchmark 定义 → 数据构建与资格审核 →
Metrics → 实验设计 → 局限与发布。正文和图注全部使用英文。

## 真实积木图、题目与 GT

正文有 4 幅图，附录有 4 幅图；其中 7 幅为此次从真实数据重新编排的图，
另 1 幅保留原始六步 3D 回放。首页直接展示 8 个完整模型。

| 图示 | 内容 |
|---|---|
| [Source overview](figures/source-overview.pdf) | 每个 D1–D4 规模带两个真实源模型，附 ID 和零件数 |
| [Color question + GT](figures/color-question-gt.pdf) | 原文题目、全部选项、A/B 图像、GT JSON、原始颜色与显示颜色的区别 |
| [Part-type question + GT](figures/type-question-gt.pdf) | 五个操作对象全部保留，包含远端交换候选、匹配零件类型和编号变化 |
| [Graph question + GT](figures/graph-question-gt.pdf) | 实际图删除题及连通分量 GT：一个六环与两个三角形 |
| [Source atlas](figures/source-atlas.pdf) | 完整 24 模型图谱 |
| [Additional examples](figures/additional-question-gt.pdf) | 另外四个来源的四对题目、图像和 GT |
| [Position panel + GT](figures/panel-question-gt.pdf) | 完整位置面板、题目、选项和正确候选 |
| [3D replay](figures/given-order-replay.pdf) | 六步原始位姿回放，附录附每步动作和新增零件 ID |

每张新图同时导出矢量文字 PDF 和 300 dpi PNG。积木部分只使用原始浏览器渲染
或冻结的观察图；仅裁去空白、按比例排版及必要的印刷降采样。
GT 标注放在图像之外，不写入模型输入。来源模型保留原始几何及位姿。

[visual-evidence.json](visual-evidence.json) 保存全部图片哈希、裁切框、原文问题、
选项、GT、观察 ID 和 wire 哈希。所有示例均为数据与 GT，不是模型回答或人审结果。
验证器重建 13 个视觉观察的答案，并独立计算两个图观察的连通分量。

## 正文实验表

| 表 | 内容 |
|---|---|
| Model inventory | 7 个闭源 VLM、6 个开放权重 VLM、2 个纯文本模型 |
| Primary visual results | Color / Part-type 各自的 A、New、Both |
| Response diagnostics | 两类各自的条件适应率、旧答案保留率、双端格式有效率 |
| Controls | 无图像 Both、位置面板准确率、QA 子集与完整集 Both 差值 |
| Text-graph results | strong / degree-visible 的 change / invariance Both、格式率 |
| Mode contrasts | Qwen27 thinking、Gemini Pro effort 的分数差、token 和成本 |

[experiments.json](experiments.json) 保存模型、类别、计划 ID 和 306 个待测值。
所有待测值均为 `null`，LaTeX 生成真正空白，不用 0、破折号或虚构成绩代替。
既有颜色/图算法审计作为已完成的确定性证据，单独写在正文和附录。

新 15 模型研究是待冻结方案，不修改旧 display-v3 三模型 roster。
当前未运行新推理、未采集人审；新提供商适配器和 MVP 子集 QA gate 尚待实现。
模型名称来自 2026-09-20 预算快照，正式采集前需重新核对服务可用性与修订版本。

## 构建

安装 [requirements.txt](requirements.txt) 后生成表格、科学图并编译：

```sh
python3 -m pip install -r paper/requirements.txt
python3 paper/build_tables.py
python3 paper/build_figures.py
cd paper
tectonic --keep-logs --keep-intermediates main.tex
tectonic --keep-logs --keep-intermediates supplement.tex
```

本机 Tectonic 位于 `benchmark/.runtime/tectonic`，在 `paper/` 内可用
`../benchmark/.runtime/tectonic` 替换上面的 `tectonic`。
旧 publication generator 只属于归档版本，不用于生成当前论文。

验证模型覆盖、空值、图表哈希、引用和 PDF：

```sh
python3 paper/verify.py
```

本机已安装绘图和 PDF 检查环境为 `benchmark/.runtime/mlx-env/bin/python`；
调用时建议清除继承的 `PYTHONPATH`：

```sh
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python paper/verify.py
```

文件说明：

- `generated/`：模型空表及引用的已完成资源审计表。
- `figures/`：真实积木渲染和 3D 回放图。
- `asset-provenance.json`、`figure-provenance.json`：复制来源、原始观察和哈希。
- `build_figures.py`、`visual-evidence.json`：新图生成器与完整图像/题目/GT 溯源。
- `verification.json`：本次内容、空表和 PDF 验证结果。
- [../benchmark/METRICS.md](../benchmark/METRICS.md)：公式和评分函数映射。
- [../benchmark/DATASETS.md](../benchmark/DATASETS.md)：数据位置及各版本关系。
