# LDraw 社区模型：只补最后一个模块

## 直接看

- [打开图文展示页](index.html)，或双击项目根目录 `打开社区模块样例.command`。
- [完整 Markdown 清单：12 个模型、96 个 case、每个错误与配图](MODEL-CASE-CATALOG.zh-CN.md)。
- [模型接口：输入、输出、动态触发与评分](INPUT-OUTPUT.zh-CN.md)。

**顺序不限。** 说明书是一种参考拼法，每次操作真实合法、最终状态正确并结束就算完成。不会用中间状态是否匹配参考答案判断对错。相同形状与颜色的零件可以互换。

## 模型一览

| # | 模型 / 模块 | 原场景零件 | 已搭好 | 本题补几块 | 静态 / 动态 |
|---|---|---:|---:|---:|---|
| 1 | [小屋：补完屋顶](MODEL-CASE-CATALOG.zh-CN.md#cottage-roof) | 270 | 264 | 6 | 4 / 4 |
| 2 | [赛车：补完车身上半部](MODEL-CASE-CATALOG.zh-CN.md#racer-top) | 67 | 56 | 11 | 4 / 4 |
| 3 | [水上飞机：补完尾翼](MODEL-CASE-CATALOG.zh-CN.md#seaplane-tail) | 53 | 46 | 7 | 4 / 4 |
| 4 | [博物馆：补完长楼屋面](MODEL-CASE-CATALOG.zh-CN.md#museum-roof) | 208 | 196 | 12 | 4 / 4 |
| 5 | [维修卡车：补车顶灯架](MODEL-CASE-CATALOG.zh-CN.md#repair-truck-cab) | 128 | 123 | 5 | 4 / 4 |
| 6 | [橙色直升机：补尾部](MODEL-CASE-CATALOG.zh-CN.md#orange-helicopter-tail) | 52 | 45 | 7 | 4 / 4 |
| 7 | [警用直升机：补机顶与尾鳍](MODEL-CASE-CATALOG.zh-CN.md#police-helicopter-top) | 59 | 49 | 10 | 4 / 4 |
| 8 | [熊猫：补脸部与耳朵](MODEL-CASE-CATALOG.zh-CN.md#panda-head) | 61 | 55 | 6 | 4 / 4 |
| 9 | [汉堡店：补屋顶与招牌](MODEL-CASE-CATALOG.zh-CN.md#burger-stand-roof) | 79 | 72 | 7 | 4 / 4 |
| 10 | [白宫：补烟囱与屋脊](MODEL-CASE-CATALOG.zh-CN.md#white-house-roof) | 556 | 546 | 10 | 4 / 4 |
| 11 | [洛克菲勒中心：补主塔顶部](MODEL-CASE-CATALOG.zh-CN.md#rockefeller-crown) | 240 | 232 | 8 | 4 / 4 |
| 12 | [勃兰登堡门：补顶部装饰](MODEL-CASE-CATALOG.zh-CN.md#brandenburg-top) | 362 | 352 | 10 | 4 / 4 |

每个模型 4 个静态 + 4 个动态 case，包括无错误对照、少件、颜色换错和多叠一块。正常补装合计 99 步。每一步只装或拆一块，不把整个模块算作一块。

动态干扰根据当时实际状态发生：已安装的本模块零件达到最低数量后，找可行的旧零件或连接点改动；找不到就等待。不依赖说明书的特定顺序。未触发干扰但拼对仍算完成，单独报告触发率及触发后的修复成功率。

## 已验证与范围

96 条参考路线、48 条不同顺序的动态路线均跑通，后者的 36 条错误路线均真正触发并修复。安装、拆除和干扰经过连接、碰撞、直线路径检查。全部原场景保留，背景不能精细检查的零件采用外包盒保守阻挡。

这是短模块、一次干扰、三类错误的扩充组；还没有新增真人成绩或模型成绩。图片差异可见不等于真人一定看得懂。预装主体作为固定物件，不证明整套从空桌面可拼，也不模拟重力、手指或卡扣力度。

原 MPD、作者、链接、许可与文件校验值均保留。说明图是本项目按原位置生成的可行参考拼法，不是 LEGO 官方说明书。API 调用和费用均为 0，未混入旧题库的实验统计。

## 重新生成与本机预览

```bash
benchmark/.runtime/mlx-env/bin/python benchmark/brickplan-repair/community_modules/build.py
benchmark/.runtime/mlx-env/bin/python benchmark/brickplan-repair/community_modules/validate.py
python3 benchmark/brickplan-repair/community_modules/preview_server.py
```

预览地址：<http://127.0.0.1:8768>。服务只提供公开讲解资源，不提供私有证书或运行记录。

HTML 与 Markdown 是包含答案的设计展示，不应发给测试模型。正式输入使用接口返回的匿名零件、图像与动作结果。

## 2026-10-23 开发试跑更新

本次对当前题库做了小规模真实 API 试跑，原文中的“API 为 0”指构建发布时的状态。正式模型主表仍未收集完成。实测逐题费用、接口问题和本轮修复见 [10 美元试跑报告](../brickplan-budget-pilot-2026-10-23/README.zh-CN.md)。模块版已修正查看操作之后的上一状态图片；付费旧记录保留原样，修复后只做了免费回归检查。
