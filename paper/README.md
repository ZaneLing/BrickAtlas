# 当前论文

唯一当前写作入口：[main.tex](main.tex) · [main.pdf](main.pdf)；
科学附录：[supplement.tex](supplement.tex) · [supplement.pdf](supplement.pdf)。
旧稿及中间审稿材料统一在 [../tem/](../tem/README.md)。
当前编译结果为 8 页正文、1 页参考文献和 6 页附录。

论文主线是：问题动机 → Benchmark 定义 → 数据构建与资格审核 →
Metrics → 实验设计 → 局限与发布。正文和图注全部使用英文。

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

Python 3 标准库可生成全部空表并复制有来源哈希的图表和 CVPR 样式：

```sh
python3 paper/build_tables.py
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

PDF 检查需要 PyMuPDF（`python3 -m pip install pymupdf`）。
本机已安装环境为 `benchmark/.runtime/mlx-env/bin/python`；
调用时建议清除继承的 `PYTHONPATH`：

```sh
env -u PYTHONPATH PYTHONNOUSERSITE=1 benchmark/.runtime/mlx-env/bin/python paper/verify.py
```

文件说明：

- `generated/`：模型空表及引用的已完成资源审计表。
- `figures/`：真实积木渲染和 3D 回放图。
- `asset-provenance.json`、`figure-provenance.json`：复制来源、原始观察和哈希。
- `verification.json`：本次内容、空表和 PDF 验证结果。
- [../benchmark/METRICS.md](../benchmark/METRICS.md)：公式和评分函数映射。
- [../benchmark/DATASETS.md](../benchmark/DATASETS.md)：数据位置及各版本关系。
