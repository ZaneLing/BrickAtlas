# 中间产物与历史归档

此目录集中保存中间审稿、修改指导、阶段验收、旧版论文及构建产物。
**当前论文入口是 [../paper/](../paper/README.md)。**

| 目录 | 内容 |
|---|---|
| `papers/legacy-tree/` | 原 `benchmark/paper/` 整棵目录，含 v1/v2/v3/v4-draft 论文、附录、图表、构建说明、截图 |
| `revisions/` | 原目录结构下的 CODEX 计划、CVPR 审稿、修订契约、回应、阶段报告、工作文件及旧网页论文副本 |
| `recovery/` | 本地大型恢复 tarball；不提交 Git |
| `paper/previous-assets/` | 当前论文已弃用的图表、截图原件及历史生成脚本 |
| `assets-built/` | 既有资产构建报告、性能报告与验收数据 |
| `build/` | 网页构建、论文编译、TypeScript 和 Vite 缓存；不提交 Git |
| `verification/` | 验证报告；浏览器运行附件不提交 Git |
| `local/` | 本地预览、调试、录制和开发服务日志；不提交 Git |
| [repository-layout-20260924/](repository-layout-20260924/README.md) | 本轮目录整理计划、文件迁移清单及验证记录 |
| [relocation-manifest.json](relocation-manifest.json) | 旧路径、新路径、每个文件的 SHA-256、大小和同步策略 |

历史数据、评测代码、真实算法输出和操作性人审指南仍在 `benchmark/`。
旧 `benchmark/paper` 等封存路径保留相对符号链接，方便历史引用及哈希校验。
根目录 CODEX/CVPR/debug 别名已移除，直接从 `revisions/` 阅读；
验证器通过显式迁移表检查原始哈希。
在归档原文中阅读相对链接时，可从旧兼容路径打开；原文不为移动而改写。
不要运行历史 publication generator 来生成当前论文，应使用 `paper/build_tables.py`。

## Git 与复现范围

Git 包含来源文件、当前及继承的精确刺激、PNG、盲审包、代码、各版本论文和清单。
`recovery/` 中的六个重复恢复压缩包（其中五个大包）共约 1.63 GiB，保留在本机，
原来的 `.tar.gz` 路径也不纳入 Git。它们用于逐字节还原旧工作区，
不是查看当前数据或构建当前论文所需的输入。原始锁文件及预期哈希继续保留。
本地 Python/Node 运行时、下载缓存、构建分发目录不提交。

因此，普通克隆可以构建当前论文并检查已同步数据；
要求验证每个旧恢复压缩包的完整 `preserve.py` 检查还需要另行取得这些包。
部分历史锁记录了编译中间文件及 Python 缓存，这些少量锁定文件随证据保留，
不代表提交一般运行缓存。

验证本次移动没有改变历史文件内容：

```sh
python3 scripts/organize-research.py --verify
python3 scripts/verify-research-sync.py
```

该命令在新克隆上跳过未同步的本地恢复包；本地有包时同时校验其哈希。
第二条命令验证 Git 索引里的历史文件字节及兼容链接。`.gitattributes` 对证据、
归档和来源模型关闭自动换行转换，保留包括许可文本在内的原始字节。
归档保留旧说法与未完成计划，不自动将其中的模型结果、论文主张或阶段要求视为当前状态。
