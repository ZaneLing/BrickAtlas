# 当前论文：Brick Atlas

更新：2026-10-29。正文 10 页＋参考文献 1 页，补充材料 33 页。这是供后续删减的工作稿，不表示满足投稿页数上限。现稿聚焦 **从静态修复到自主动态恢复**，名称沿用仓库的 Brick Atlas。

- [正文 PDF](main.pdf)
- [补充材料 PDF](supplement.pdf)
- [Overleaf 上传包](brickplan-cvpr-overleaf.zip)
- [正文源码](main.tex) / [补充材料源码](supplement.tex)
- [最终编译与证据检查](verification.json)

## 本版同步了什么

1. 数量改为当前正式索引：310 个模型、4,685 题，静态 1,600、动态 3,085。
2. 区分 57 个完整拼装、253 个收尾任务，以及 437 个原始来源素材；不把素材池计成可运行模型。
3. 描述真实 Arena：模型主动调用观察、安装、拆卸和回看；动作后不自动发新图。
4. 区分独立正常运行通过后的修复率 NQR，以及另需共享前缀的严格配对实验。
5. 正式题库图绑定当前题目；展示四条明确标注的旧版 Arena API 轨迹（两条正常拼好、两条事故修复）。场景使用精确几何的 3200 × 2400 原生渲染；图中文字保持 Comic Sans MS。补充材料列出全部 310 个模型。
6. 保留 32 类空白实验表和 10 个既有候选模型；正文另有主要结果汇总表。没有用脚本成绩填模型成绩。
7. 最终检查退回的 7 道问题题已从现版统计和题库移出，原始数据和原因保留。

## 现在能说明什么

程序能证明：正式题有可执行参考动作，当前图和目标图使用一致画布，正确中途阶段不会被强迫继续拼完整件，替代合法顺序可接受，未触发事故与技术故障分开统计。

**还不能说明已经达到 CVPR 录取水平。** 本版正式模型结果、独立真人操作和独立机械可行性审查尚未完成。所有候选来源在出题时都见过，不能声称是未见来源测试。详见 [投稿前还要完成的事](SUBMISSION-READINESS.zh-CN.md)。

## 构建

在仓库根目录运行：

```bash
npm run paper:build
```

重建现版高清场景与图：

```bash
benchmark/.runtime/mlx-env/bin/python paper/brickplan-cvpr/build.py --refresh-figures
```

仅重新排图中文字：`--refresh-typography`。当前构建器只使用 `release_assets.py`、`release_tables.py`、`release_figures.py` 、`arena_assets.py` 和现版索引；旧版轨迹使用独立证据文件，不进入现版题数。旧 `update_current.py`、`make_current_tables.py` 等属于历史稿，不再由默认构建调用。

正文继续使用仓库已记录来源的 CVPR 官方样式。2027 年份和 Draft 投稿号仍为草稿标记，投稿时须核对当届要求；本次没有改动模板本体。

## 证据入口

- `evidence/release-dataset.json`：当前题量及依赖文件哈希。
- `evidence/release-render-states.json`：每个论文场景的原始题目与状态。
- `figures-release/provenance.json`：原生图、字体、PDF 和源文件哈希。
- `evidence/release-results-template.json`：32 类实验的空结果；字段为 null。
- `evidence/release-experiment-plan.json`：实验范围、每条件运行一次及未完成状态。
- `evidence/release-model-inventory.json`：全部 310 个模型。

旧 `current-*` 证据和 `figures-publication/` 等旧图仍可追溯，但不被现稿引用。本次没有新增付费 API 调用。

## 本次扩充：Arena 过程、32 组实验与 15 篇论文对照

- [真实模型和 GT 过程：含每轮 JSON、图片和反馈](ARENA-TRAJECTORIES.zh-CN.md)
- [15 篇相关论文与审稿问题逐项对照](RELATED-BENCHMARK-REVIEW.zh-CN.md)
- [新增 11 组实验，用普通话说明做什么](EXPERIMENT-PLAN.zh-CN.md)

模型案例来自旧版 Arena v2：小汽车成功、椅子错误完成。全部动作重新检查，与原日志一致。GT 从同一事故现场继续，使用答案信息；不把它当作模型成绩，不声称全局最少动作。新版正式结果仍留空。本次新增付费调用 0 次。

## 本次增加：真实正常拼装与分类型错误分析

[先看这份中文图文说明](MODEL-ERRORS-AND-MODALITIES.zh-CN.md)：两个模型真实拼好物件的全部安装步骤、完整 34 轮动作、19 次已有试跑审计，以及文字/图片/组合如何进入静态和动态题。

正文首图现在展示模型真实拼好的小汽车；补充材料同时展示小汽车和椅子。错误统计区分格式、编号、连接、碰撞、拆卸路径、错误提交和服务故障。三种输入已形成明确实验设计，严格的三套运行适配器尚未接完，未虚构对照成绩。
