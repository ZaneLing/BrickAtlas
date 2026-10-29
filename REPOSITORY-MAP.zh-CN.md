# 仓库目录：现用、历史、运行产物

更新：2026-10-29。

## 现在用这几处

| 目录 | 放什么 | 使用规则 |
|---|---|---|
| `deliverables/brick-atlas-dataset-v1/` | 正式题单、模型表、图片、GT、检查报告 | 题数以 `release.json` 和 `questions/` 为准 |
| `benchmark/brickplan-repair/scaling_release/` | 新题库构建、检查、导出代码 | 改数据后重新检查，不能沿用旧通过记录 |
| `benchmark/brickplan-repair/dynamic_arena/` | 动态工具、观察接口、运行器、日志页面 | 模型主动看图；观众图不等于模型输入 |
| `benchmark/brickplan-repair/bench_design/` | 共用会话、静态接口、metrics | 包含历史适配器；不代表全部历史题都正式入选 |
| `deliverables/brickplan-dynamic-arena/` | 当前 Arena 目录与明确标记的脚本/历史运行 | `catalogue.json` 是正式动态题；`catalogue-all-conditions.json` 是历史候选合集 |
| `paper/brickplan-cvpr/` | 当前正文、补充材料、高清图、空白实验表、Overleaf 包 | 以 `README.zh-CN.md` 和 `verification.json` 为入口 |

## 保留，但不混进当前统计

- `deliverables/brickplan-benchmark-spec/` 等旧题库：保留原始题目、旧 GT、旧实验，不删除历史。
- `benchmark/brickplan-v*/`、`web/brickplan/`：既有规划题与交互工作台；有独立版本和未提交开发内容。
- `paper/brickplan-cvpr/figures-publication/`、`figures-current/`、`figures-v2/`：旧论文图。现稿只引用 `figures-release/`。
- 论文中的 `evidence/release-*.json` 是现版证据。`current-*` 等旧文件保留作历史，不再被现版构建器引用。
- 根目录旧版说明已放入 `REPOSITORY-HISTORY.md` 和中文版；其中日期和数量只属于当时。
- `paper/` 中其余早期稿、`tem/` 是本地历史归档，不是本次现用论文。

## 不应当提交什么

密钥、`.env`、API 原始私人账单、Python/Node 环境、编译缓存，以及未入选的临时下载不进入本次发布。`paper/brickplan-cvpr/build/` 是编译与看图检查缓存。不要用 `git add .` 把所有候选和其他开发修改一起提交。

## 重新导出顺序

先重新回放社区题和既有物件题，再运行 `scaling_release.export`、`scaling_release.publish_sources`、`dynamic_arena.catalogue`、`scaling_release.docs`、`scaling_release.count_history`。然后跑 Arena 脚本、metrics 回归、`scaling_release.release_check`，最后重建论文。

现用题库、网页和论文读取同一组正式索引。退回题保留原因，不能为了维持整数数量而重新放进去。
