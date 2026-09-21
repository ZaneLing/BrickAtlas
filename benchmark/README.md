# BrickAtlas Benchmark

主要入口：[数据目录](DATASETS.md) · [指标与评分代码](METRICS.md) ·
[当前英文论文](../paper/README.md) · [历史审稿与论文归档](../tem/README.md)。

## 当前研究

本项目评测模型能否根据当前图像中的证据回答问题，并在成对观察改变后继续答对。
Color 测试渲染颜色，Part-type 测试几何匹配后的候选编号选择，两类分别报告。
文本图测试显式图上的连通分量，独立于视觉分数。

| 内容 | 规模 | 目录 |
|---|---:|---|
| Color | 73 对 / 146 张图 | `ldraw-evidence-v3/` |
| Part-type | 67 对 / 134 张图 | `ldraw-evidence-v3/` |
| 位置面板 | 67 张图 | `ldraw-evidence-v3/` |
| 文本图 | 219 条独立观察 | `ldraw-evidence-v1/matched-graphs-v1/` |
| 原始来源 | 24 个模型 / 15,334 个实例 | `ldraw-v2/sources/` |
| 历史题目档案 | 617 道 | `../public/benchmark/evidence-v3/dossiers.json` |

数据版本仍为 `brickatlas-display-v3`；`ldraw-evidence-v4-draft/` 增加测量审计，
不代表另生成一批视觉题。当前论文的 15 模型实验是待冻结的新方案；
v3 已封存的三模型运行清单不能直接替换成这 15 个模型。
真人资格审核尚未完成，没有新模型实验结果。

## 数据检查与三维查看

从仓库根目录运行：

```sh
npm ci
npm run dev
```

- 数据、pair、答案和历史档案：`http://127.0.0.1:5173/benchmark/evidence-v3/index.html`
- 原始积木三维旋转、缩放、按编号隔离及回放：`http://127.0.0.1:5173/benchmark`
- 正式盲审：[QA-AND-RUN.md](ldraw-evidence-v3/QA-AND-RUN.md)，使用独立审核包。

## 代码与实验

| 用途 | 目录或文件 |
|---|---|
| 成对评分、统计、人审、推理 | `suite/ldraw-evidence-v3/` |
| 逐观察审计、单图像颜色基线 | `suite/ldraw-evidence-v4-draft/` |
| 模型名单与空白表格生成 | `../paper/experiments.json`、`../paper/build_tables.py` |
| 预算与 MVP 设计 | `experiment-plans/model-budget-20260920/` |
| 历史多任务评分 | `suite/METRICS.md`、`core/world.ts` |

MVP 覆盖 15 个模型，按既有预算快照建议准备 ¥800–1,000。
接入计划为 12 个 OpenRouter 模型、3 个自部署模型；可用性、精度和价格需在正式采集前重新冻结。
抽样 ID、新提供商适配器、MVP 子集人审 gate 尚未实现，不应将预算文件当作可运行实验。

## 历史版本

`ldraw-v1/`、`ldraw-v2/` 保存来源与旧题；`ldraw-evidence-v1/`、`ldraw-evidence-v2/`
保留旧协议及当前版本所继承的精确资产。`hierarchy-*`、`mechanism-v1/`、
`constructibility-v1/`、`diagnostic-v2/`、`suite/` 中的早期合成数据和实测结果
独立保留，不并入当前视觉 benchmark。

所有中间论文、审稿、修改指导已归档至 `../tem/`。旧路径兼容链接用于历史脚本、
网页和哈希校验；当前论文统一修改 `../paper/`。
