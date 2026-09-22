# 当前论文

唯一当前写作入口：[main.tex](main.tex) · [main.pdf](main.pdf)；
科学附录：[supplement.tex](supplement.tex) · [supplement.pdf](supplement.pdf)。
旧稿及中间审稿材料统一在 [../tem/](../tem/README.md)。
当前图文版为 10 页正文、1 页参考文献和 10 页附录。

论文主线是：问题动机 → Benchmark 定义 → 数据构建与资格审核 →
Metrics → 实验设计 → 局限与发布。正文和图注全部使用英文。

## 真实积木图、题目与 GT

正文有 4 幅图：模型总览加三道复杂复合题。颜色案例已撤出论文图示；
Part-type 和小型图删除控制放在附录。附录共 4 幅图，另有完整输入与 GT 证明表。
首页直接展示 8 个完整模型。

| 图示 | 内容 |
|---|---|
| [Source overview](figures/source-overview.pdf) | 每个 D1–D4 规模带两个真实源模型，附 ID 和零件数 |
| [CX1：多故障最小修复](figures/complex-repair.pdf) | 真实后铲的 36 零件、44 连接、8 个缺失候选；穷举 256 个子集，证明最小恢复集合 |
| [CX2：自适应故障诊断](figures/complex-diagnosis.pdf) | 4 个故障世界、3 种连接查询；条件决策树与最坏成本证明 |
| [CX3：位姿与对应关系恢复](figures/complex-registration.pdf) | 两套 12 零件轴组件；同型匹配、刚体旋转/平移、探针位置和方向 GT |
| [Part-type control](figures/type-question-gt.pdf) | 附录中的基础视觉控制，保留全部对象和 GT |
| [Graph control](figures/graph-question-gt.pdf) | 附录中的小型匹配图控制 |
| [Source atlas](figures/source-atlas.pdf) | 完整 24 模型图谱 |
| [Position panel + GT](figures/panel-question-gt.pdf) | 完整位置面板、题目、选项和正确候选 |

每张新图同时导出矢量文字 PDF 和 300 dpi PNG。积木部分只使用原始浏览器渲染
或冻结的观察图；仅裁去空白、按比例排版及必要的印刷降采样。
GT 标注放在图像之外，不写入模型输入。来源模型保留原始几何及位姿。

[visual-evidence.json](visual-evidence.json) 保存全部图片哈希、裁切框、原文问题、
选项、GT、观察 ID 和 wire 哈希。所有示例均为数据与 GT，不是模型回答或人审结果。
新题及完整验证位于 [complex-examples-v1](../benchmark/complex-examples-v1/README.md)：
256 个修复子集、27 种查询树、4 种同型对应、12 个完整源变换均已独立复算。
三道复杂题是待审核的设计示例，不混入 display-v3 的固定实验分母。

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
python3 benchmark/complex-examples-v1/build.py
python3 paper/build_tables.py
python3 paper/build_figures.py
cd paper
tectonic --keep-logs --keep-intermediates main.tex
tectonic --keep-logs --keep-intermediates supplement.tex
```

本机 Tectonic 位于 `benchmark/.runtime/tectonic`，在 `paper/` 内可用
`../benchmark/.runtime/tectonic` 替换上面的 `tectonic`。
旧 publication generator 只属于归档版本，不用于生成当前论文。

现有真实 3D 截图已随仓库保存。需要重新捕获时，先运行 `npm run dev`，
再在安装 Chrome 的本机运行：

```sh
npx tsx paper/capture_complex.ts
python3 paper/build_figures.py
```

交互查看入口为 `/paper/complex-render.html?model=omr-42004` 和
`/paper/complex-render.html?model=omr-42061`，支持完整模型及子装配的旋转、缩放。
`figures/complex-raw/captures.json` 记录截图、渲染器和源文件哈希，以及可见零件 ID。

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
- `complex_figures.py`：CX1–CX3 组图及附录完整邻接表、分量表和候选拟合表。
- `verification.json`：本次内容、空表和 PDF 验证结果。
- [../benchmark/METRICS.md](../benchmark/METRICS.md)：公式和评分函数映射。
- [../benchmark/DATASETS.md](../benchmark/DATASETS.md)：数据位置及各版本关系。
