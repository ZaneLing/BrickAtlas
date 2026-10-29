# 本机查看与复查

在仓库根目录运行。下列命令不会调用付费模型。

## 看题、GT 和 Arena 回放

```bash
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m dynamic_arena.server --port 8810
```

打开 <http://127.0.0.1:8810/dataset/>。即使不启动服务，也可以直接打开本目录的 `index.html` 看模型、图片和 GT。

## 复查发布文件

```bash
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m scaling_release.release_check
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m unittest scaling_release.test_contract bench_design.test_metrics
```

`release_check` 核对全部发布题、逐模型回放证据、图片版本、GT 和 Arena 清单。原始候选检查报告中的房车颜色问题有意保留；那组题已经退回，不在发布清单中。

## 重新执行几何和接口回放

```bash
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m scaling_release.check --workers 3
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m scaling_release.legacy_check
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m scaling_release.arena_check
```

社区检查默认复用内容哈希一致的通过记录。需要强制重放某一模型时，先备份其 `private/<编号>/check.json`，将该检查文件移出目录后再运行。不要删除题目、原始来源或失败证据。

## 换一台电脑时

看静态网页只需仓库中的 HTML、JS 和 PNG。执行裁判还需 Python 3.11、NumPy、Pillow、Matplotlib、MeshLib 和 BrickNet，当前版本记录在 `checks/runtime-versions.json`。原始 LDraw 依赖随仓库保存；本机的虚拟环境和 BrickNet 碰撞网格目录 `benchmark/.runtime/bricknet-data/inset/` 不随 Git 上传，需按项目现有环境准备。新下载来源的导入还使用 LDraw 完整库压缩包 `assets-source/ldraw-library/complete.zip`，已有题目的查看不需要重新下载它。

本次交付是已核对的数据与本机可执行环境，不声称已经做成跨平台的一键安装包。真人审题、独立物理复核和真实 API 模型实验仍待开展。
