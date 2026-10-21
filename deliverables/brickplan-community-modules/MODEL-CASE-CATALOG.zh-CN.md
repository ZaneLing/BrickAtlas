# 12 个社区模型：模型、错误与 case 完整清单

更新：2026-10-21。可以直接打开 [图文展示页](index.html)，或双击项目根目录的 `打开社区模块样例.command`。无需写文字、提交 JSON 或调用模型 API。

## 先说明白：不要求照着唯一顺序拼

**说明书只是一种参考拼法。中间状态不用和参考答案逐步相同。每次装、拆都真实合法，最后形状、位置、朝向和颜色正确，并声明完成，就算完成。**

- 可以先装左边再装右边，也可以反过来，只要连接、碰撞和装入路径检查通过。
- 相同形状、相同颜色的积木可以互换身份；不会因为编号与参考答案不同扣分。
- 不能穿过其他积木、凭空漂浮、重复装同一块或直接复制整个目标状态。每次只装或拆一块。
- 动态干扰看当时真的装了哪些零件。达到最低已装数量后，选择可拆、可换或可添加的位置；不会等待“恰好拼成参考图第几步”。找不到合法位置就继续等待，不能硬改出不可能状态。
- 没发生干扰但最终拼对，仍然算完成；这条记录不用于计算“发生干扰后的修复成功率”。另报干扰触发率，防止把没有遇到错误的完成当成修复成绩。

## 总量与怎么读这份清单

**12 个不同原模型 × 每个 8 个 case = 96 个 case：48 个静态、48 个动态。** 正常补装一共 99 步。每个模型补 5–12 块，不要求从零搭整个物件。

每个模型各有：静态无错误、静态少一块、静态换错颜色、静态多一块；动态无干扰、动态少一块、动态换错颜色、动态多一块。共 3 类错误，重复到不同物件和结构上，不应写成 96 种错误。

表中的“参考图编号”只用于定位哪块积木，**不是必须遵守的操作次序**。动态表列的是展示路线实际发生的错误；改用另一条拼法时，受影响零件可能不同，选择依据是实际状态。

| # | 模型 / 模块 | 原场景零件 | 已搭好 | 本题补几块 | 静态 / 动态 |
|---|---|---:|---:|---:|---|
| 1 | [小屋：补完屋顶](#cottage-roof) | 270 | 264 | 6 | 4 / 4 |
| 2 | [赛车：补完车身上半部](#racer-top) | 67 | 56 | 11 | 4 / 4 |
| 3 | [水上飞机：补完尾翼](#seaplane-tail) | 53 | 46 | 7 | 4 / 4 |
| 4 | [博物馆：补完长楼屋面](#museum-roof) | 208 | 196 | 12 | 4 / 4 |
| 5 | [维修卡车：补车顶灯架](#repair-truck-cab) | 128 | 123 | 5 | 4 / 4 |
| 6 | [橙色直升机：补尾部](#orange-helicopter-tail) | 52 | 45 | 7 | 4 / 4 |
| 7 | [警用直升机：补机顶与尾鳍](#police-helicopter-top) | 59 | 49 | 10 | 4 / 4 |
| 8 | [熊猫：补脸部与耳朵](#panda-head) | 61 | 55 | 6 | 4 / 4 |
| 9 | [汉堡店：补屋顶与招牌](#burger-stand-roof) | 79 | 72 | 7 | 4 / 4 |
| 10 | [白宫：补烟囱与屋脊](#white-house-roof) | 556 | 546 | 10 | 4 / 4 |
| 11 | [洛克菲勒中心：补主塔顶部](#rockefeller-crown) | 240 | 232 | 8 | 4 / 4 |
| 12 | [勃兰登堡门：补顶部装饰](#brandenburg-top) | 362 | 352 | 10 | 4 / 4 |

原场景零件数按原 MPD 展开的实际实例计，包括人物和配景，不是包装盒上的零件数。每个模块另有“每块正常积木对应的一块异色备用件 + 1 块红色薄板”，所有条件都给同一份零件和候选位置，避免从零件表猜出错误类型。

<a id="cottage-roof"></a>

## 1. 小屋：补完屋顶

**本题做什么：**房子、花园、烟囱和大部分屋顶已经装好，只补前侧屋面和屋脊的 6 块。不是从零搭房子，也不是重搭整个屋顶。

- 模块：屋顶前面的斜面和屋脊收尾。
- 开始已搭好 264 块；只补 6 块。零件盘共 13 块，含备用件。
- 静态目标：参考图 3 的正确状态；提供目标图，修到这幅图即可。
- 动态目标：整个剩余模块完成。安装数量达到 3 块后尝试一次干扰；具体改哪块取决于实际拼法。
- 社区原模型：`31009`；作者：Stefan Frenz [smf]；[来源](https://library.ldraw.org/omr/sets/1164)；[原 MPD](cottage-roof/original.mpd)。
- [查看这个模型的说明与全部 case](index.html#model=cottage-roof&mode=manual)。

| 本题开始 | 最终完成 |
|---|---|
| ![开始状态](cottage-roof/images/full-initial.png) | ![完整目标](cottage-roof/images/full-final.png) |

### 剩余哪些零件

下表数字对应说明图，不是评分要求的顺序。LDraw 名称保留原文方便查零件；直接看小图即可识别。

| 参考图编号 | 零件小图 | 零件号 / 颜色 | 原文件中的零件名称 |
|---|---|---|---|
| 1 | <img src="cottage-roof/images/part01.png" width="95" alt="零件 1"> | 3039 / 深蓝色 | Slope Brick 45  2 x  2 |
| 2 | <img src="cottage-roof/images/part02.png" width="95" alt="零件 2"> | 3039 / 深蓝色 | Slope Brick 45  2 x  2 |
| 3 | <img src="cottage-roof/images/part03.png" width="95" alt="零件 3"> | 3046 / 深蓝色 | Slope Brick 45  2 x  2 Double Concave |
| 4 | <img src="cottage-roof/images/part04.png" width="95" alt="零件 4"> | 3038 / 深蓝色 | Slope Brick 45  2 x  3 |
| 5 | <img src="cottage-roof/images/part05.png" width="95" alt="零件 5"> | 3046 / 深蓝色 | Slope Brick 45  2 x  2 Double Concave |
| 6 | <img src="cottage-roof/images/part06.png" width="95" alt="零件 6"> | 3038 / 深蓝色 | Slope Brick 45  2 x  3 |

**已实际跑通的另一种顺序：1 → 2 → 4 → 3 → 5 → 6。** 这条路线的无干扰、少件、换色、多件都通过了逐次操作检查，最终正确。

### 8 个 case

| case 编号 | 类型 | 具体错误 / 对照 | 做到什么算完成 | 展示 |
|---|---|---|---|---|
| `cottage-roof-static-control` | 静态·无错误对照 | 保持正常状态，不做后台改动。 | 修成参考图 3 的目标状态 | [查看](index.html#model=cottage-roof&mode=static&family=control) |
| `cottage-roof-static-missing` | 静态·少一块 | 拿走参考图 1 的深蓝色零件（3039），保留刚刚新装的一块。 | 修成参考图 3 的目标状态 | [查看](index.html#model=cottage-roof&mode=static&family=missing) |
| `cottage-roof-static-wrong-color` | 静态·颜色被换错 | 把参考图 1 的深蓝色零件（3039）换成同形状的黄色零件。 | 修成参考图 3 的目标状态 | [查看](index.html#model=cottage-roof&mode=static&family=wrong-color) |
| `cottage-roof-static-extra-layer` | 静态·多叠一块 | 在参考图 1 的零件上，多装一块红色 1×1 薄板（3024）。 | 修成参考图 3 的目标状态 | [查看](index.html#model=cottage-roof&mode=static&family=extra-layer) |
| `cottage-roof-dynamic-control` | 动态·无错误对照 | 保持正常状态，不做后台改动。 | 最终补完全部模块 | [查看](index.html#model=cottage-roof&mode=dynamic&family=control) |
| `cottage-roof-dynamic-missing` | 动态·少一块 | 拿走参考图 1 的深蓝色零件（3039），保留刚刚新装的一块。 | 最终补完全部模块 | [查看](index.html#model=cottage-roof&mode=dynamic&family=missing) |
| `cottage-roof-dynamic-wrong-color` | 动态·颜色被换错 | 把参考图 1 的深蓝色零件（3039）换成同形状的黄色零件。 | 最终补完全部模块 | [查看](index.html#model=cottage-roof&mode=dynamic&family=wrong-color) |
| `cottage-roof-dynamic-extra-layer` | 动态·多叠一块 | 在参考图 1 的零件上，多装一块红色 1×1 薄板（3024）。 | 最终补完全部模块 | [查看](index.html#model=cottage-roof&mode=dynamic&family=extra-layer) |

### 同一阶段的正确状态与三种错误

以下配图来自展示路线。每种错误选画面变化最大的固定视角，并列出同视角的正确目标；展示页可切换三个方向。正式模型不会收到错误标签或这张对照表。

| 错误 | 应有状态 | 实际错误状态 |
|---|---|---|
| 少一块 | ![正确目标](cottage-roof/images/checkpoint-isometric.png) | ![错误状态](cottage-roof/images/missing-isometric.png) |
| 颜色被换错 | ![正确目标](cottage-roof/images/checkpoint-top.png) | ![错误状态](cottage-roof/images/wrong-color-top.png) |
| 多叠一块 | ![正确目标](cottage-roof/images/checkpoint-top.png) | ![错误状态](cottage-roof/images/extra-layer-top.png) |

<a id="racer-top"></a>

## 2. 赛车：补完车身上半部

**本题做什么：**底盘、车轮和尾部已经装好，只补驾驶舱周围的 11 块。车旁的交通锥也是原模型的一部分，不需要操作。

- 模块：驾驶舱周围的车身、挡风玻璃和盖板。
- 开始已搭好 56 块；只补 11 块。零件盘共 23 块，含备用件。
- 静态目标：参考图 3 的正确状态；提供目标图，修到这幅图即可。
- 动态目标：整个剩余模块完成。安装数量达到 3 块后尝试一次干扰；具体改哪块取决于实际拼法。
- 社区原模型：`31027`；作者：Merlijn Wissink [legolijntje]；[来源](https://library.ldraw.org/omr/sets/223)；[原 MPD](racer-top/original.mpd)。
- [查看这个模型的说明与全部 case](index.html#model=racer-top&mode=manual)。

| 本题开始 | 最终完成 |
|---|---|
| ![开始状态](racer-top/images/full-initial.png) | ![完整目标](racer-top/images/full-final.png) |

### 剩余哪些零件

下表数字对应说明图，不是评分要求的顺序。LDraw 名称保留原文方便查零件；直接看小图即可识别。

| 参考图编号 | 零件小图 | 零件号 / 颜色 | 原文件中的零件名称 |
|---|---|---|---|
| 1 | <img src="racer-top/images/part01.png" width="95" alt="零件 1"> | 2420 / 蓝色 | Plate  2 x  2 Corner |
| 2 | <img src="racer-top/images/part02.png" width="95" alt="零件 2"> | 11477 / 蓝色 | Slope Brick Curved  2 x  1 |
| 3 | <img src="racer-top/images/part03.png" width="95" alt="零件 3"> | 2420 / 蓝色 | Plate  2 x  2 Corner |
| 4 | <img src="racer-top/images/part04.png" width="95" alt="零件 4"> | 3022 / 白色 | Plate  2 x  2 |
| 5 | <img src="racer-top/images/part05.png" width="95" alt="零件 5"> | 11477 / 蓝色 | Slope Brick Curved  2 x  1 |
| 6 | <img src="racer-top/images/part06.png" width="95" alt="零件 6"> | 54200 / 透明烟灰色 | Slope Brick 31  1 x  1 x  0.667 |
| 7 | <img src="racer-top/images/part07.png" width="95" alt="零件 7"> | 54200 / 透明烟灰色 | Slope Brick 31  1 x  1 x  0.667 |
| 8 | <img src="racer-top/images/part08.png" width="95" alt="零件 8"> | 54200 / 透明烟灰色 | Slope Brick 31  1 x  1 x  0.667 |
| 9 | <img src="racer-top/images/part09.png" width="95" alt="零件 9"> | 54200 / 透明烟灰色 | Slope Brick 31  1 x  1 x  0.667 |
| 10 | <img src="racer-top/images/part10.png" width="95" alt="零件 10"> | 3024 / 蓝色 | Plate  1 x  1 |
| 11 | <img src="racer-top/images/part11.png" width="95" alt="零件 11"> | 3024 / 蓝色 | Plate  1 x  1 |

**已实际跑通的另一种顺序：1 → 6 → 3 → 4 → 5 → 2 → 7 → 8 → 9 → 10 → 11。** 这条路线的无干扰、少件、换色、多件都通过了逐次操作检查，最终正确。

### 8 个 case

| case 编号 | 类型 | 具体错误 / 对照 | 做到什么算完成 | 展示 |
|---|---|---|---|---|
| `racer-top-static-control` | 静态·无错误对照 | 保持正常状态，不做后台改动。 | 修成参考图 3 的目标状态 | [查看](index.html#model=racer-top&mode=static&family=control) |
| `racer-top-static-missing` | 静态·少一块 | 拿走参考图 2 的蓝色零件（11477），保留刚刚新装的一块。 | 修成参考图 3 的目标状态 | [查看](index.html#model=racer-top&mode=static&family=missing) |
| `racer-top-static-wrong-color` | 静态·颜色被换错 | 把参考图 2 的蓝色零件（11477）换成同形状的黄色零件。 | 修成参考图 3 的目标状态 | [查看](index.html#model=racer-top&mode=static&family=wrong-color) |
| `racer-top-static-extra-layer` | 静态·多叠一块 | 在参考图 1 的零件上，多装一块红色 1×1 薄板（3024）。 | 修成参考图 3 的目标状态 | [查看](index.html#model=racer-top&mode=static&family=extra-layer) |
| `racer-top-dynamic-control` | 动态·无错误对照 | 保持正常状态，不做后台改动。 | 最终补完全部模块 | [查看](index.html#model=racer-top&mode=dynamic&family=control) |
| `racer-top-dynamic-missing` | 动态·少一块 | 拿走参考图 2 的蓝色零件（11477），保留刚刚新装的一块。 | 最终补完全部模块 | [查看](index.html#model=racer-top&mode=dynamic&family=missing) |
| `racer-top-dynamic-wrong-color` | 动态·颜色被换错 | 把参考图 2 的蓝色零件（11477）换成同形状的黄色零件。 | 最终补完全部模块 | [查看](index.html#model=racer-top&mode=dynamic&family=wrong-color) |
| `racer-top-dynamic-extra-layer` | 动态·多叠一块 | 在参考图 1 的零件上，多装一块红色 1×1 薄板（3024）。 | 最终补完全部模块 | [查看](index.html#model=racer-top&mode=dynamic&family=extra-layer) |

### 同一阶段的正确状态与三种错误

以下配图来自展示路线。每种错误选画面变化最大的固定视角，并列出同视角的正确目标；展示页可切换三个方向。正式模型不会收到错误标签或这张对照表。

| 错误 | 应有状态 | 实际错误状态 |
|---|---|---|
| 少一块 | ![正确目标](racer-top/images/checkpoint-top.png) | ![错误状态](racer-top/images/missing-top.png) |
| 颜色被换错 | ![正确目标](racer-top/images/checkpoint-top.png) | ![错误状态](racer-top/images/wrong-color-top.png) |
| 多叠一块 | ![正确目标](racer-top/images/checkpoint-top.png) | ![错误状态](racer-top/images/extra-layer-top.png) |

<a id="seaplane-tail"></a>

## 3. 水上飞机：补完尾翼

**本题做什么：**机身、主机翼和浮筒已经装好，只补尾部的 7 块。每次装一块，灯和盖板也分别算一步。

- 模块：尾部两侧的翼面、尾鳍、盖板和灯。
- 开始已搭好 46 块；只补 7 块。零件盘共 15 块，含备用件。
- 静态目标：参考图 3 的正确状态；提供目标图，修到这幅图即可。
- 动态目标：整个剩余模块完成。安装数量达到 3 块后尝试一次干扰；具体改哪块取决于实际拼法。
- 社区原模型：`31028`；作者：Merlijn Wissink [legolijntje]；[来源](https://library.ldraw.org/omr/sets/259)；[原 MPD](seaplane-tail/original.mpd)。
- [查看这个模型的说明与全部 case](index.html#model=seaplane-tail&mode=manual)。

| 本题开始 | 最终完成 |
|---|---|
| ![开始状态](seaplane-tail/images/full-initial.png) | ![完整目标](seaplane-tail/images/full-final.png) |

### 剩余哪些零件

下表数字对应说明图，不是评分要求的顺序。LDraw 名称保留原文方便查零件；直接看小图即可识别。

| 参考图编号 | 零件小图 | 零件号 / 颜色 | 原文件中的零件名称 |
|---|---|---|---|
| 1 | <img src="seaplane-tail/images/part01.png" width="95" alt="零件 1"> | 43723 / 白色 | ~Moved to 43723a |
| 2 | <img src="seaplane-tail/images/part02.png" width="95" alt="零件 2"> | 3070b / 黑色 | Tile  1 x  1 with Groove |
| 3 | <img src="seaplane-tail/images/part03.png" width="95" alt="零件 3"> | 43722 / 白色 | ~Moved to 43722a |
| 4 | <img src="seaplane-tail/images/part04.png" width="95" alt="零件 4"> | 44661 / 白色 | Tail  2 x  3 x  2 Fin |
| 5 | <img src="seaplane-tail/images/part05.png" width="95" alt="零件 5"> | 3070b / 黑色 | Tile  1 x  1 with Groove |
| 6 | <img src="seaplane-tail/images/part06.png" width="95" alt="零件 6"> | 6141 / 透明绿色 | Plate  1 x  1 Round |
| 7 | <img src="seaplane-tail/images/part07.png" width="95" alt="零件 7"> | 6141 / 透明红色 | Plate  1 x  1 Round |

**已实际跑通的另一种顺序：1 → 6 → 3 → 4 → 5 → 2 → 7。** 这条路线的无干扰、少件、换色、多件都通过了逐次操作检查，最终正确。

### 8 个 case

| case 编号 | 类型 | 具体错误 / 对照 | 做到什么算完成 | 展示 |
|---|---|---|---|---|
| `seaplane-tail-static-control` | 静态·无错误对照 | 保持正常状态，不做后台改动。 | 修成参考图 3 的目标状态 | [查看](index.html#model=seaplane-tail&mode=static&family=control) |
| `seaplane-tail-static-missing` | 静态·少一块 | 拿走参考图 2 的黑色零件（3070b），保留刚刚新装的一块。 | 修成参考图 3 的目标状态 | [查看](index.html#model=seaplane-tail&mode=static&family=missing) |
| `seaplane-tail-static-wrong-color` | 静态·颜色被换错 | 把参考图 2 的黑色零件（3070b）换成同形状的黄色零件。 | 修成参考图 3 的目标状态 | [查看](index.html#model=seaplane-tail&mode=static&family=wrong-color) |
| `seaplane-tail-static-extra-layer` | 静态·多叠一块 | 在参考图 1 的零件上，多装一块红色 1×1 薄板（3024）。 | 修成参考图 3 的目标状态 | [查看](index.html#model=seaplane-tail&mode=static&family=extra-layer) |
| `seaplane-tail-dynamic-control` | 动态·无错误对照 | 保持正常状态，不做后台改动。 | 最终补完全部模块 | [查看](index.html#model=seaplane-tail&mode=dynamic&family=control) |
| `seaplane-tail-dynamic-missing` | 动态·少一块 | 拿走参考图 2 的黑色零件（3070b），保留刚刚新装的一块。 | 最终补完全部模块 | [查看](index.html#model=seaplane-tail&mode=dynamic&family=missing) |
| `seaplane-tail-dynamic-wrong-color` | 动态·颜色被换错 | 把参考图 2 的黑色零件（3070b）换成同形状的黄色零件。 | 最终补完全部模块 | [查看](index.html#model=seaplane-tail&mode=dynamic&family=wrong-color) |
| `seaplane-tail-dynamic-extra-layer` | 动态·多叠一块 | 在参考图 1 的零件上，多装一块红色 1×1 薄板（3024）。 | 最终补完全部模块 | [查看](index.html#model=seaplane-tail&mode=dynamic&family=extra-layer) |

### 同一阶段的正确状态与三种错误

以下配图来自展示路线。每种错误选画面变化最大的固定视角，并列出同视角的正确目标；展示页可切换三个方向。正式模型不会收到错误标签或这张对照表。

| 错误 | 应有状态 | 实际错误状态 |
|---|---|---|
| 少一块 | ![正确目标](seaplane-tail/images/checkpoint-top.png) | ![错误状态](seaplane-tail/images/missing-top.png) |
| 颜色被换错 | ![正确目标](seaplane-tail/images/checkpoint-top.png) | ![错误状态](seaplane-tail/images/wrong-color-top.png) |
| 多叠一块 | ![正确目标](seaplane-tail/images/checkpoint-top.png) | ![错误状态](seaplane-tail/images/extra-layer-top.png) |

<a id="museum-roof"></a>

## 4. 博物馆：补完长楼屋面

**本题做什么：**圆形展馆和后方长楼已经装好。只补后方长楼的 12 块屋面，不要求重建整座博物馆。

- 模块：后方长楼的两条承托板和十块屋面盖板。
- 开始已搭好 196 块；只补 12 块。零件盘共 25 块，含备用件。
- 静态目标：参考图 4 的正确状态；提供目标图，修到这幅图即可。
- 动态目标：整个剩余模块完成。安装数量达到 4 块后尝试一次干扰；具体改哪块取决于实际拼法。
- 社区原模型：`v23-21004`；作者：Orion Pobursky [OrionP]；[来源](https://library.ldraw.org/omr/sets/12)；[原 MPD](museum-roof/original.mpd)。
- [查看这个模型的说明与全部 case](index.html#model=museum-roof&mode=manual)。

| 本题开始 | 最终完成 |
|---|---|
| ![开始状态](museum-roof/images/full-initial.png) | ![完整目标](museum-roof/images/full-final.png) |

### 剩余哪些零件

下表数字对应说明图，不是评分要求的顺序。LDraw 名称保留原文方便查零件；直接看小图即可识别。

| 参考图编号 | 零件小图 | 零件号 / 颜色 | 原文件中的零件名称 |
|---|---|---|---|
| 1 | <img src="museum-roof/images/part01.png" width="95" alt="零件 1"> | 4477 / 米黄色 | Plate  1 x 10 |
| 2 | <img src="museum-roof/images/part02.png" width="95" alt="零件 2"> | 4477 / 米黄色 | Plate  1 x 10 |
| 3 | <img src="museum-roof/images/part03.png" width="95" alt="零件 3"> | 3069b / 米黄色 | Tile  1 x  2 with Groove |
| 4 | <img src="museum-roof/images/part04.png" width="95" alt="零件 4"> | 3069b / 米黄色 | Tile  1 x  2 with Groove |
| 5 | <img src="museum-roof/images/part05.png" width="95" alt="零件 5"> | 3069b / 米黄色 | Tile  1 x  2 with Groove |
| 6 | <img src="museum-roof/images/part06.png" width="95" alt="零件 6"> | 3069b / 米黄色 | Tile  1 x  2 with Groove |
| 7 | <img src="museum-roof/images/part07.png" width="95" alt="零件 7"> | 3069b / 米黄色 | Tile  1 x  2 with Groove |
| 8 | <img src="museum-roof/images/part08.png" width="95" alt="零件 8"> | 3069b / 米黄色 | Tile  1 x  2 with Groove |
| 9 | <img src="museum-roof/images/part09.png" width="95" alt="零件 9"> | 3069b / 米黄色 | Tile  1 x  2 with Groove |
| 10 | <img src="museum-roof/images/part10.png" width="95" alt="零件 10"> | 3069b / 米黄色 | Tile  1 x  2 with Groove |
| 11 | <img src="museum-roof/images/part11.png" width="95" alt="零件 11"> | 3069b / 米黄色 | Tile  1 x  2 with Groove |
| 12 | <img src="museum-roof/images/part12.png" width="95" alt="零件 12"> | 3069b / 米黄色 | Tile  1 x  2 with Groove |

**已实际跑通的另一种顺序：1 → 2 → 3 → 5 → 4 → 6 → 7 → 8 → 9 → 10 → 11 → 12。** 这条路线的无干扰、少件、换色、多件都通过了逐次操作检查，最终正确。

### 8 个 case

| case 编号 | 类型 | 具体错误 / 对照 | 做到什么算完成 | 展示 |
|---|---|---|---|---|
| `museum-roof-static-control` | 静态·无错误对照 | 保持正常状态，不做后台改动。 | 修成参考图 4 的目标状态 | [查看](index.html#model=museum-roof&mode=static&family=control) |
| `museum-roof-static-missing` | 静态·少一块 | 拿走参考图 3 的米黄色零件（3069b），保留刚刚新装的一块。 | 修成参考图 4 的目标状态 | [查看](index.html#model=museum-roof&mode=static&family=missing) |
| `museum-roof-static-wrong-color` | 静态·颜色被换错 | 把参考图 3 的米黄色零件（3069b）换成同形状的黄色零件。 | 修成参考图 4 的目标状态 | [查看](index.html#model=museum-roof&mode=static&family=wrong-color) |
| `museum-roof-static-extra-layer` | 静态·多叠一块 | 在参考图 1 的零件上，多装一块红色 1×1 薄板（3024）。 | 修成参考图 4 的目标状态 | [查看](index.html#model=museum-roof&mode=static&family=extra-layer) |
| `museum-roof-dynamic-control` | 动态·无错误对照 | 保持正常状态，不做后台改动。 | 最终补完全部模块 | [查看](index.html#model=museum-roof&mode=dynamic&family=control) |
| `museum-roof-dynamic-missing` | 动态·少一块 | 拿走参考图 3 的米黄色零件（3069b），保留刚刚新装的一块。 | 最终补完全部模块 | [查看](index.html#model=museum-roof&mode=dynamic&family=missing) |
| `museum-roof-dynamic-wrong-color` | 动态·颜色被换错 | 把参考图 3 的米黄色零件（3069b）换成同形状的黄色零件。 | 最终补完全部模块 | [查看](index.html#model=museum-roof&mode=dynamic&family=wrong-color) |
| `museum-roof-dynamic-extra-layer` | 动态·多叠一块 | 在参考图 1 的零件上，多装一块红色 1×1 薄板（3024）。 | 最终补完全部模块 | [查看](index.html#model=museum-roof&mode=dynamic&family=extra-layer) |

### 同一阶段的正确状态与三种错误

以下配图来自展示路线。每种错误选画面变化最大的固定视角，并列出同视角的正确目标；展示页可切换三个方向。正式模型不会收到错误标签或这张对照表。

| 错误 | 应有状态 | 实际错误状态 |
|---|---|---|
| 少一块 | ![正确目标](museum-roof/images/checkpoint-isometric.png) | ![错误状态](museum-roof/images/missing-isometric.png) |
| 颜色被换错 | ![正确目标](museum-roof/images/checkpoint-top.png) | ![错误状态](museum-roof/images/wrong-color-top.png) |
| 多叠一块 | ![正确目标](museum-roof/images/checkpoint-top.png) | ![错误状态](museum-roof/images/extra-layer-top.png) |

<a id="repair-truck-cab"></a>

## 5. 维修卡车：补车顶灯架

**本题做什么：**底盘、驾驶室和维修设备已经装好，只补车顶灯架；路灯与工人保留作背景。

- 模块：驾驶室车顶的支撑条、格栅和两侧警示灯。
- 开始已搭好 123 块；只补 5 块。零件盘共 11 块，含备用件。
- 静态目标：参考图 4 的正确状态；提供目标图，修到这幅图即可。
- 动态目标：整个剩余模块完成。安装数量达到 4 块后尝试一次干扰；具体改哪块取决于实际拼法。
- 社区原模型：`v23-3179`；作者：Marc Giraudet [Mad_Marc]；[来源](https://library.ldraw.org/omr/sets/1053)；[原 MPD](repair-truck-cab/original.mpd)。
- [查看这个模型的说明与全部 case](index.html#model=repair-truck-cab&mode=manual)。

| 本题开始 | 最终完成 |
|---|---|
| ![开始状态](repair-truck-cab/images/full-initial.png) | ![完整目标](repair-truck-cab/images/full-final.png) |

### 剩余哪些零件

下表数字对应说明图，不是评分要求的顺序。LDraw 名称保留原文方便查零件；直接看小图即可识别。

| 参考图编号 | 零件小图 | 零件号 / 颜色 | 原文件中的零件名称 |
|---|---|---|---|
| 1 | <img src="repair-truck-cab/images/part01.png" width="95" alt="零件 1"> | 3666 / 黄色 | Plate  1 x  6 |
| 2 | <img src="repair-truck-cab/images/part02.png" width="95" alt="零件 2"> | 3666 / 白色 | Plate  1 x  6 |
| 3 | <img src="repair-truck-cab/images/part03.png" width="95" alt="零件 3"> | 2412b / 深灰色 | Tile  1 x  2 Grille with Groove |
| 4 | <img src="repair-truck-cab/images/part04.png" width="95" alt="零件 4"> | 3069b / 透明橙色 | Tile  1 x  2 with Groove |
| 5 | <img src="repair-truck-cab/images/part05.png" width="95" alt="零件 5"> | 3069b / 透明橙色 | Tile  1 x  2 with Groove |

**已实际跑通的另一种顺序：1 → 2 → 3 → 5 → 4。** 这条路线的无干扰、少件、换色、多件都通过了逐次操作检查，最终正确。

### 8 个 case

| case 编号 | 类型 | 具体错误 / 对照 | 做到什么算完成 | 展示 |
|---|---|---|---|---|
| `repair-truck-cab-static-control` | 静态·无错误对照 | 保持正常状态，不做后台改动。 | 修成参考图 4 的目标状态 | [查看](index.html#model=repair-truck-cab&mode=static&family=control) |
| `repair-truck-cab-static-missing` | 静态·少一块 | 拿走参考图 3 的深灰色零件（2412b），保留刚刚新装的一块。 | 修成参考图 4 的目标状态 | [查看](index.html#model=repair-truck-cab&mode=static&family=missing) |
| `repair-truck-cab-static-wrong-color` | 静态·颜色被换错 | 把参考图 3 的深灰色零件（2412b）换成同形状的黄色零件。 | 修成参考图 4 的目标状态 | [查看](index.html#model=repair-truck-cab&mode=static&family=wrong-color) |
| `repair-truck-cab-static-extra-layer` | 静态·多叠一块 | 在参考图 2 的零件上，多装一块红色 1×1 薄板（3024）。 | 修成参考图 4 的目标状态 | [查看](index.html#model=repair-truck-cab&mode=static&family=extra-layer) |
| `repair-truck-cab-dynamic-control` | 动态·无错误对照 | 保持正常状态，不做后台改动。 | 最终补完全部模块 | [查看](index.html#model=repair-truck-cab&mode=dynamic&family=control) |
| `repair-truck-cab-dynamic-missing` | 动态·少一块 | 拿走参考图 3 的深灰色零件（2412b），保留刚刚新装的一块。 | 最终补完全部模块 | [查看](index.html#model=repair-truck-cab&mode=dynamic&family=missing) |
| `repair-truck-cab-dynamic-wrong-color` | 动态·颜色被换错 | 把参考图 3 的深灰色零件（2412b）换成同形状的黄色零件。 | 最终补完全部模块 | [查看](index.html#model=repair-truck-cab&mode=dynamic&family=wrong-color) |
| `repair-truck-cab-dynamic-extra-layer` | 动态·多叠一块 | 在参考图 2 的零件上，多装一块红色 1×1 薄板（3024）。 | 最终补完全部模块 | [查看](index.html#model=repair-truck-cab&mode=dynamic&family=extra-layer) |

### 同一阶段的正确状态与三种错误

以下配图来自展示路线。每种错误选画面变化最大的固定视角，并列出同视角的正确目标；展示页可切换三个方向。正式模型不会收到错误标签或这张对照表。

| 错误 | 应有状态 | 实际错误状态 |
|---|---|---|
| 少一块 | ![正确目标](repair-truck-cab/images/checkpoint-top.png) | ![错误状态](repair-truck-cab/images/missing-top.png) |
| 颜色被换错 | ![正确目标](repair-truck-cab/images/checkpoint-top.png) | ![错误状态](repair-truck-cab/images/wrong-color-top.png) |
| 多叠一块 | ![正确目标](repair-truck-cab/images/checkpoint-top.png) | ![错误状态](repair-truck-cab/images/extra-layer-top.png) |

<a id="orange-helicopter-tail"></a>

## 6. 橙色直升机：补尾部

**本题做什么：**机身和主旋翼已经装好，只操作尾部剩余零件。

- 模块：尾鳍、尾桨及尾部盖板。
- 开始已搭好 45 块；只补 7 块。零件盘共 15 块，含备用件。
- 静态目标：参考图 3 的正确状态；提供目标图，修到这幅图即可。
- 动态目标：整个剩余模块完成。安装数量达到 3 块后尝试一次干扰；具体改哪块取决于实际拼法。
- 社区原模型：`v23-30181`；作者：Merlijn Wissink [legolijntje]；[来源](https://library.ldraw.org/omr/sets/145)；[原 MPD](orange-helicopter-tail/original.mpd)。
- [查看这个模型的说明与全部 case](index.html#model=orange-helicopter-tail&mode=manual)。

| 本题开始 | 最终完成 |
|---|---|
| ![开始状态](orange-helicopter-tail/images/full-initial.png) | ![完整目标](orange-helicopter-tail/images/full-final.png) |

### 剩余哪些零件

下表数字对应说明图，不是评分要求的顺序。LDraw 名称保留原文方便查零件；直接看小图即可识别。

| 参考图编号 | 零件小图 | 零件号 / 颜色 | 原文件中的零件名称 |
|---|---|---|---|
| 1 | <img src="orange-helicopter-tail/images/part01.png" width="95" alt="零件 1"> | 60470a / 白色 | Plate  1 x  2 with  2 Clips Horizontal (Thick U-Clips) |
| 2 | <img src="orange-helicopter-tail/images/part02.png" width="95" alt="零件 2"> | 3794b / 白色 | Plate  1 x  2 with Groove with 1 Centre Stud |
| 3 | <img src="orange-helicopter-tail/images/part03.png" width="95" alt="零件 3"> | 3794b / 白色 | Plate  1 x  2 with Groove with 1 Centre Stud |
| 4 | <img src="orange-helicopter-tail/images/part04.png" width="95" alt="零件 4"> | 3040b / 橙色 | Slope Brick 45  2 x  1 |
| 5 | <img src="orange-helicopter-tail/images/part05.png" width="95" alt="零件 5"> | 4697b / 浅灰色 | Technic Pneumatic T-Piece - Type 2 |
| 6 | <img src="orange-helicopter-tail/images/part06.png" width="95" alt="零件 6"> | 30663 / 黑色 | Car Steering Wheel 2L |
| 7 | <img src="orange-helicopter-tail/images/part07.png" width="95" alt="零件 7"> | 50746 / 橙色 | =Slope Brick 31  1 x  1 x  0.667 |

**已实际跑通的另一种顺序：1 → 3 → 2 → 4 → 5 → 6 → 7。** 这条路线的无干扰、少件、换色、多件都通过了逐次操作检查，最终正确。

### 8 个 case

| case 编号 | 类型 | 具体错误 / 对照 | 做到什么算完成 | 展示 |
|---|---|---|---|---|
| `orange-helicopter-tail-static-control` | 静态·无错误对照 | 保持正常状态，不做后台改动。 | 修成参考图 3 的目标状态 | [查看](index.html#model=orange-helicopter-tail&mode=static&family=control) |
| `orange-helicopter-tail-static-missing` | 静态·少一块 | 拿走参考图 2 的白色零件（3794b），保留刚刚新装的一块。 | 修成参考图 3 的目标状态 | [查看](index.html#model=orange-helicopter-tail&mode=static&family=missing) |
| `orange-helicopter-tail-static-wrong-color` | 静态·颜色被换错 | 把参考图 2 的白色零件（3794b）换成同形状的黄色零件。 | 修成参考图 3 的目标状态 | [查看](index.html#model=orange-helicopter-tail&mode=static&family=wrong-color) |
| `orange-helicopter-tail-static-extra-layer` | 静态·多叠一块 | 在参考图 2 的零件上，多装一块红色 1×1 薄板（3024）。 | 修成参考图 3 的目标状态 | [查看](index.html#model=orange-helicopter-tail&mode=static&family=extra-layer) |
| `orange-helicopter-tail-dynamic-control` | 动态·无错误对照 | 保持正常状态，不做后台改动。 | 最终补完全部模块 | [查看](index.html#model=orange-helicopter-tail&mode=dynamic&family=control) |
| `orange-helicopter-tail-dynamic-missing` | 动态·少一块 | 拿走参考图 2 的白色零件（3794b），保留刚刚新装的一块。 | 最终补完全部模块 | [查看](index.html#model=orange-helicopter-tail&mode=dynamic&family=missing) |
| `orange-helicopter-tail-dynamic-wrong-color` | 动态·颜色被换错 | 把参考图 2 的白色零件（3794b）换成同形状的黄色零件。 | 最终补完全部模块 | [查看](index.html#model=orange-helicopter-tail&mode=dynamic&family=wrong-color) |
| `orange-helicopter-tail-dynamic-extra-layer` | 动态·多叠一块 | 在参考图 2 的零件上，多装一块红色 1×1 薄板（3024）。 | 最终补完全部模块 | [查看](index.html#model=orange-helicopter-tail&mode=dynamic&family=extra-layer) |

### 同一阶段的正确状态与三种错误

以下配图来自展示路线。每种错误选画面变化最大的固定视角，并列出同视角的正确目标；展示页可切换三个方向。正式模型不会收到错误标签或这张对照表。

| 错误 | 应有状态 | 实际错误状态 |
|---|---|---|
| 少一块 | ![正确目标](orange-helicopter-tail/images/checkpoint-isometric.png) | ![错误状态](orange-helicopter-tail/images/missing-isometric.png) |
| 颜色被换错 | ![正确目标](orange-helicopter-tail/images/checkpoint-top.png) | ![错误状态](orange-helicopter-tail/images/wrong-color-top.png) |
| 多叠一块 | ![正确目标](orange-helicopter-tail/images/checkpoint-top.png) | ![错误状态](orange-helicopter-tail/images/extra-layer-top.png) |

<a id="police-helicopter-top"></a>

## 7. 警用直升机：补机顶与尾鳍

**本题做什么：**浮筒、机身和尾梁已经装好，只补机顶与尾部的收尾部分。

- 模块：机顶盖板、主旋翼和尾鳍收尾。
- 开始已搭好 49 块；只补 10 块。零件盘共 21 块，含备用件。
- 静态目标：参考图 4 的正确状态；提供目标图，修到这幅图即可。
- 动态目标：整个剩余模块完成。安装数量达到 4 块后尝试一次干扰；具体改哪块取决于实际拼法。
- 社区原模型：`v23-30311`；作者：Merlijn Wissink [Legolijntje]；[来源](https://library.ldraw.org/omr/sets/344)；[原 MPD](police-helicopter-top/original.mpd)。
- [查看这个模型的说明与全部 case](index.html#model=police-helicopter-top&mode=manual)。

| 本题开始 | 最终完成 |
|---|---|
| ![开始状态](police-helicopter-top/images/full-initial.png) | ![完整目标](police-helicopter-top/images/full-final.png) |

### 剩余哪些零件

下表数字对应说明图，不是评分要求的顺序。LDraw 名称保留原文方便查零件；直接看小图即可识别。

| 参考图编号 | 零件小图 | 零件号 / 颜色 | 原文件中的零件名称 |
|---|---|---|---|
| 1 | <img src="police-helicopter-top/images/part01.png" width="95" alt="零件 1"> | 44661 / 白色 | Tail  2 x  3 x  2 Fin |
| 2 | <img src="police-helicopter-top/images/part02.png" width="95" alt="零件 2"> | 2421 / 黑色 | Propeller  3 Blade  4 Diameter |
| 3 | <img src="police-helicopter-top/images/part03.png" width="95" alt="零件 3"> | 3040b / 白色 | Slope Brick 45  2 x  1 |
| 4 | <img src="police-helicopter-top/images/part04.png" width="95" alt="零件 4"> | 3040b / 白色 | Slope Brick 45  2 x  1 |
| 5 | <img src="police-helicopter-top/images/part05.png" width="95" alt="零件 5"> | 3062b / 深灰色 | Brick  1 x  1 Round with Hollow Stud |
| 6 | <img src="police-helicopter-top/images/part06.png" width="95" alt="零件 6"> | 3062b / 深灰色 | Brick  1 x  1 Round with Hollow Stud |
| 7 | <img src="police-helicopter-top/images/part07.png" width="95" alt="零件 7"> | 2460 / 深灰色 | Tile  2 x  2 with Pin |
| 8 | <img src="police-helicopter-top/images/part08.png" width="95" alt="零件 8"> | 2479 / 黑色 | Propeller  4 Blade  5 Diameter |
| 9 | <img src="police-helicopter-top/images/part09.png" width="95" alt="零件 9"> | 6636 / 黑色 | Tile  1 x  6 |
| 10 | <img src="police-helicopter-top/images/part10.png" width="95" alt="零件 10"> | 6636 / 黑色 | Tile  1 x  6 |

**已实际跑通的另一种顺序：1 → 2 → 3 → 5 → 4 → 6 → 7 → 8 → 9 → 10。** 这条路线的无干扰、少件、换色、多件都通过了逐次操作检查，最终正确。

### 8 个 case

| case 编号 | 类型 | 具体错误 / 对照 | 做到什么算完成 | 展示 |
|---|---|---|---|---|
| `police-helicopter-top-static-control` | 静态·无错误对照 | 保持正常状态，不做后台改动。 | 修成参考图 4 的目标状态 | [查看](index.html#model=police-helicopter-top&mode=static&family=control) |
| `police-helicopter-top-static-missing` | 静态·少一块 | 拿走参考图 1 的白色零件（44661），保留刚刚新装的一块。 | 修成参考图 4 的目标状态 | [查看](index.html#model=police-helicopter-top&mode=static&family=missing) |
| `police-helicopter-top-static-wrong-color` | 静态·颜色被换错 | 把参考图 1 的白色零件（44661）换成同形状的黄色零件。 | 修成参考图 4 的目标状态 | [查看](index.html#model=police-helicopter-top&mode=static&family=wrong-color) |
| `police-helicopter-top-static-extra-layer` | 静态·多叠一块 | 在参考图 3 的零件上，多装一块红色 1×1 薄板（3024）。 | 修成参考图 4 的目标状态 | [查看](index.html#model=police-helicopter-top&mode=static&family=extra-layer) |
| `police-helicopter-top-dynamic-control` | 动态·无错误对照 | 保持正常状态，不做后台改动。 | 最终补完全部模块 | [查看](index.html#model=police-helicopter-top&mode=dynamic&family=control) |
| `police-helicopter-top-dynamic-missing` | 动态·少一块 | 拿走参考图 1 的白色零件（44661），保留刚刚新装的一块。 | 最终补完全部模块 | [查看](index.html#model=police-helicopter-top&mode=dynamic&family=missing) |
| `police-helicopter-top-dynamic-wrong-color` | 动态·颜色被换错 | 把参考图 1 的白色零件（44661）换成同形状的黄色零件。 | 最终补完全部模块 | [查看](index.html#model=police-helicopter-top&mode=dynamic&family=wrong-color) |
| `police-helicopter-top-dynamic-extra-layer` | 动态·多叠一块 | 在参考图 3 的零件上，多装一块红色 1×1 薄板（3024）。 | 最终补完全部模块 | [查看](index.html#model=police-helicopter-top&mode=dynamic&family=extra-layer) |

### 同一阶段的正确状态与三种错误

以下配图来自展示路线。每种错误选画面变化最大的固定视角，并列出同视角的正确目标；展示页可切换三个方向。正式模型不会收到错误标签或这张对照表。

| 错误 | 应有状态 | 实际错误状态 |
|---|---|---|
| 少一块 | ![正确目标](police-helicopter-top/images/checkpoint-rear.png) | ![错误状态](police-helicopter-top/images/missing-rear.png) |
| 颜色被换错 | ![正确目标](police-helicopter-top/images/checkpoint-rear.png) | ![错误状态](police-helicopter-top/images/wrong-color-rear.png) |
| 多叠一块 | ![正确目标](police-helicopter-top/images/checkpoint-rear.png) | ![错误状态](police-helicopter-top/images/extra-layer-rear.png) |

<a id="panda-head"></a>

## 8. 熊猫：补脸部与耳朵

**本题做什么：**身体、四肢和头部主体已经装好，只补能辨认出熊猫面部的几个零件。

- 模块：头部两侧斜面、耳朵和鼻子。
- 开始已搭好 55 块；只补 6 块。零件盘共 13 块，含备用件。
- 静态目标：参考图 4 的正确状态；提供目标图，修到这幅图即可。
- 动态目标：整个剩余模块完成。安装数量达到 4 块后尝试一次干扰；具体改哪块取决于实际拼法。
- 社区原模型：`v23-30026`；作者：Takeshi Takahashi [RainbowDolphin]；[来源](https://library.ldraw.org/omr/sets/1406)；[原 MPD](panda-head/original.mpd)。
- [查看这个模型的说明与全部 case](index.html#model=panda-head&mode=manual)。

| 本题开始 | 最终完成 |
|---|---|
| ![开始状态](panda-head/images/full-initial.png) | ![完整目标](panda-head/images/full-final.png) |

### 剩余哪些零件

下表数字对应说明图，不是评分要求的顺序。LDraw 名称保留原文方便查零件；直接看小图即可识别。

| 参考图编号 | 零件小图 | 零件号 / 颜色 | 原文件中的零件名称 |
|---|---|---|---|
| 1 | <img src="panda-head/images/part01.png" width="95" alt="零件 1"> | 54200 / 白色 | Slope Brick 31  1 x  1 x  0.667 |
| 2 | <img src="panda-head/images/part02.png" width="95" alt="零件 2"> | 54200 / 白色 | Slope Brick 31  1 x  1 x  0.667 |
| 3 | <img src="panda-head/images/part03.png" width="95" alt="零件 3"> | 61252 / 黑色 | Plate  1 x  1 with Clip Horizontal (Thick C-Clip) |
| 4 | <img src="panda-head/images/part04.png" width="95" alt="零件 4"> | 61252 / 黑色 | Plate  1 x  1 with Clip Horizontal (Thick C-Clip) |
| 5 | <img src="panda-head/images/part05.png" width="95" alt="零件 5"> | 30367a / 白色 | Cylinder  2 x  2 with Dome Top with Blocked Stud |
| 6 | <img src="panda-head/images/part06.png" width="95" alt="零件 6"> | 6141 / 黑色 | Plate  1 x  1 Round |

**已实际跑通的另一种顺序：1 → 2 → 3 → 5 → 4 → 6。** 这条路线的无干扰、少件、换色、多件都通过了逐次操作检查，最终正确。

### 8 个 case

| case 编号 | 类型 | 具体错误 / 对照 | 做到什么算完成 | 展示 |
|---|---|---|---|---|
| `panda-head-static-control` | 静态·无错误对照 | 保持正常状态，不做后台改动。 | 修成参考图 4 的目标状态 | [查看](index.html#model=panda-head&mode=static&family=control) |
| `panda-head-static-missing` | 静态·少一块 | 拿走参考图 1 的白色零件（54200），保留刚刚新装的一块。 | 修成参考图 4 的目标状态 | [查看](index.html#model=panda-head&mode=static&family=missing) |
| `panda-head-static-wrong-color` | 静态·颜色被换错 | 把参考图 1 的白色零件（54200）换成同形状的黄色零件。 | 修成参考图 4 的目标状态 | [查看](index.html#model=panda-head&mode=static&family=wrong-color) |
| `panda-head-static-extra-layer` | 静态·多叠一块 | 在参考图 3 的零件上，多装一块红色 1×1 薄板（3024）。 | 修成参考图 4 的目标状态 | [查看](index.html#model=panda-head&mode=static&family=extra-layer) |
| `panda-head-dynamic-control` | 动态·无错误对照 | 保持正常状态，不做后台改动。 | 最终补完全部模块 | [查看](index.html#model=panda-head&mode=dynamic&family=control) |
| `panda-head-dynamic-missing` | 动态·少一块 | 拿走参考图 1 的白色零件（54200），保留刚刚新装的一块。 | 最终补完全部模块 | [查看](index.html#model=panda-head&mode=dynamic&family=missing) |
| `panda-head-dynamic-wrong-color` | 动态·颜色被换错 | 把参考图 1 的白色零件（54200）换成同形状的黄色零件。 | 最终补完全部模块 | [查看](index.html#model=panda-head&mode=dynamic&family=wrong-color) |
| `panda-head-dynamic-extra-layer` | 动态·多叠一块 | 在参考图 3 的零件上，多装一块红色 1×1 薄板（3024）。 | 最终补完全部模块 | [查看](index.html#model=panda-head&mode=dynamic&family=extra-layer) |

### 同一阶段的正确状态与三种错误

以下配图来自展示路线。每种错误选画面变化最大的固定视角，并列出同视角的正确目标；展示页可切换三个方向。正式模型不会收到错误标签或这张对照表。

| 错误 | 应有状态 | 实际错误状态 |
|---|---|---|
| 少一块 | ![正确目标](panda-head/images/checkpoint-top.png) | ![错误状态](panda-head/images/missing-top.png) |
| 颜色被换错 | ![正确目标](panda-head/images/checkpoint-top.png) | ![错误状态](panda-head/images/wrong-color-top.png) |
| 多叠一块 | ![正确目标](panda-head/images/checkpoint-rear.png) | ![错误状态](panda-head/images/extra-layer-rear.png) |

<a id="burger-stand-roof"></a>

## 9. 汉堡店：补屋顶与招牌

**本题做什么：**店铺墙体、柜台和大部分屋顶已经装好，只补屋顶上方的收尾零件。

- 模块：屋顶边缘、招牌支撑和条纹装饰。
- 开始已搭好 72 块；只补 7 块。零件盘共 15 块，含备用件。
- 静态目标：参考图 3 的正确状态；提供目标图，修到这幅图即可。
- 动态目标：整个剩余模块完成。安装数量达到 3 块后尝试一次干扰；具体改哪块取决于实际拼法。
- 社区原模型：`v23-6683`；作者：Robert Paciorek [bercik]；[来源](https://library.ldraw.org/omr/sets/642)；[原 MPD](burger-stand-roof/original.mpd)。
- [查看这个模型的说明与全部 case](index.html#model=burger-stand-roof&mode=manual)。

| 本题开始 | 最终完成 |
|---|---|
| ![开始状态](burger-stand-roof/images/full-initial.png) | ![完整目标](burger-stand-roof/images/full-final.png) |

### 剩余哪些零件

下表数字对应说明图，不是评分要求的顺序。LDraw 名称保留原文方便查零件；直接看小图即可识别。

| 参考图编号 | 零件小图 | 零件号 / 颜色 | 原文件中的零件名称 |
|---|---|---|---|
| 1 | <img src="burger-stand-roof/images/part01.png" width="95" alt="零件 1"> | 4161 / 黑色 | Slope Brick 33  3 x  3 |
| 2 | <img src="burger-stand-roof/images/part02.png" width="95" alt="零件 2"> | 4161 / 黑色 | Slope Brick 33  3 x  3 |
| 3 | <img src="burger-stand-roof/images/part03.png" width="95" alt="零件 3"> | 3010 / 白色 | Brick  1 x  4 |
| 4 | <img src="burger-stand-roof/images/part04.png" width="95" alt="零件 4"> | 3010 / 白色 | Brick  1 x  4 |
| 5 | <img src="burger-stand-roof/images/part05.png" width="95" alt="零件 5"> | 3666 / 白色 | Plate  1 x  6 |
| 6 | <img src="burger-stand-roof/images/part06.png" width="95" alt="零件 6"> | 3666 / 蓝色 | Plate  1 x  6 |
| 7 | <img src="burger-stand-roof/images/part07.png" width="95" alt="零件 7"> | 3666 / 白色 | Plate  1 x  6 |

**已实际跑通的另一种顺序：2 → 1 → 3 → 4 → 5 → 6 → 7。** 这条路线的无干扰、少件、换色、多件都通过了逐次操作检查，最终正确。

### 8 个 case

| case 编号 | 类型 | 具体错误 / 对照 | 做到什么算完成 | 展示 |
|---|---|---|---|---|
| `burger-stand-roof-static-control` | 静态·无错误对照 | 保持正常状态，不做后台改动。 | 修成参考图 3 的目标状态 | [查看](index.html#model=burger-stand-roof&mode=static&family=control) |
| `burger-stand-roof-static-missing` | 静态·少一块 | 拿走参考图 1 的黑色零件（4161），保留刚刚新装的一块。 | 修成参考图 3 的目标状态 | [查看](index.html#model=burger-stand-roof&mode=static&family=missing) |
| `burger-stand-roof-static-wrong-color` | 静态·颜色被换错 | 把参考图 1 的黑色零件（4161）换成同形状的黄色零件。 | 修成参考图 3 的目标状态 | [查看](index.html#model=burger-stand-roof&mode=static&family=wrong-color) |
| `burger-stand-roof-static-extra-layer` | 静态·多叠一块 | 在参考图 1 的零件上，多装一块红色 1×1 薄板（3024）。 | 修成参考图 3 的目标状态 | [查看](index.html#model=burger-stand-roof&mode=static&family=extra-layer) |
| `burger-stand-roof-dynamic-control` | 动态·无错误对照 | 保持正常状态，不做后台改动。 | 最终补完全部模块 | [查看](index.html#model=burger-stand-roof&mode=dynamic&family=control) |
| `burger-stand-roof-dynamic-missing` | 动态·少一块 | 拿走参考图 1 的黑色零件（4161），保留刚刚新装的一块。 | 最终补完全部模块 | [查看](index.html#model=burger-stand-roof&mode=dynamic&family=missing) |
| `burger-stand-roof-dynamic-wrong-color` | 动态·颜色被换错 | 把参考图 1 的黑色零件（4161）换成同形状的黄色零件。 | 最终补完全部模块 | [查看](index.html#model=burger-stand-roof&mode=dynamic&family=wrong-color) |
| `burger-stand-roof-dynamic-extra-layer` | 动态·多叠一块 | 在参考图 1 的零件上，多装一块红色 1×1 薄板（3024）。 | 最终补完全部模块 | [查看](index.html#model=burger-stand-roof&mode=dynamic&family=extra-layer) |

### 同一阶段的正确状态与三种错误

以下配图来自展示路线。每种错误选画面变化最大的固定视角，并列出同视角的正确目标；展示页可切换三个方向。正式模型不会收到错误标签或这张对照表。

| 错误 | 应有状态 | 实际错误状态 |
|---|---|---|
| 少一块 | ![正确目标](burger-stand-roof/images/checkpoint-rear.png) | ![错误状态](burger-stand-roof/images/missing-rear.png) |
| 颜色被换错 | ![正确目标](burger-stand-roof/images/checkpoint-top.png) | ![错误状态](burger-stand-roof/images/wrong-color-top.png) |
| 多叠一块 | ![正确目标](burger-stand-roof/images/checkpoint-top.png) | ![错误状态](burger-stand-roof/images/extra-layer-top.png) |

<a id="white-house-roof"></a>

## 10. 白宫：补烟囱与屋脊

**本题做什么：**建筑主体与大部分黑色屋顶已经装好，只补屋脊和白色烟囱。

- 模块：屋脊盖板和八个烟囱收尾。
- 开始已搭好 546 块；只补 10 块。零件盘共 21 块，含备用件。
- 静态目标：参考图 4 的正确状态；提供目标图，修到这幅图即可。
- 动态目标：整个剩余模块完成。安装数量达到 4 块后尝试一次干扰；具体改哪块取决于实际拼法。
- 社区原模型：`v23-21006`；作者：Damien Roux [Darats]；[来源](https://library.ldraw.org/omr/sets/74)；[原 MPD](white-house-roof/original.mpd)。
- [查看这个模型的说明与全部 case](index.html#model=white-house-roof&mode=manual)。

| 本题开始 | 最终完成 |
|---|---|
| ![开始状态](white-house-roof/images/full-initial.png) | ![完整目标](white-house-roof/images/full-final.png) |

### 剩余哪些零件

下表数字对应说明图，不是评分要求的顺序。LDraw 名称保留原文方便查零件；直接看小图即可识别。

| 参考图编号 | 零件小图 | 零件号 / 颜色 | 原文件中的零件名称 |
|---|---|---|---|
| 1 | <img src="white-house-roof/images/part01.png" width="95" alt="零件 1"> | 87079 / 黑色 | Tile  2 x  4 |
| 2 | <img src="white-house-roof/images/part02.png" width="95" alt="零件 2"> | 87079 / 黑色 | Tile  2 x  4 |
| 3 | <img src="white-house-roof/images/part03.png" width="95" alt="零件 3"> | 3005 / 白色 | Brick  1 x  1 |
| 4 | <img src="white-house-roof/images/part04.png" width="95" alt="零件 4"> | 3005 / 白色 | Brick  1 x  1 |
| 5 | <img src="white-house-roof/images/part05.png" width="95" alt="零件 5"> | 3005 / 白色 | Brick  1 x  1 |
| 6 | <img src="white-house-roof/images/part06.png" width="95" alt="零件 6"> | 3005 / 白色 | Brick  1 x  1 |
| 7 | <img src="white-house-roof/images/part07.png" width="95" alt="零件 7"> | 3005 / 白色 | Brick  1 x  1 |
| 8 | <img src="white-house-roof/images/part08.png" width="95" alt="零件 8"> | 3005 / 白色 | Brick  1 x  1 |
| 9 | <img src="white-house-roof/images/part09.png" width="95" alt="零件 9"> | 3005 / 白色 | Brick  1 x  1 |
| 10 | <img src="white-house-roof/images/part10.png" width="95" alt="零件 10"> | 3005 / 白色 | Brick  1 x  1 |

**已实际跑通的另一种顺序：1 → 2 → 3 → 5 → 4 → 6 → 7 → 8 → 9 → 10。** 这条路线的无干扰、少件、换色、多件都通过了逐次操作检查，最终正确。

### 8 个 case

| case 编号 | 类型 | 具体错误 / 对照 | 做到什么算完成 | 展示 |
|---|---|---|---|---|
| `white-house-roof-static-control` | 静态·无错误对照 | 保持正常状态，不做后台改动。 | 修成参考图 4 的目标状态 | [查看](index.html#model=white-house-roof&mode=static&family=control) |
| `white-house-roof-static-missing` | 静态·少一块 | 拿走参考图 1 的黑色零件（87079），保留刚刚新装的一块。 | 修成参考图 4 的目标状态 | [查看](index.html#model=white-house-roof&mode=static&family=missing) |
| `white-house-roof-static-wrong-color` | 静态·颜色被换错 | 把参考图 1 的黑色零件（87079）换成同形状的黄色零件。 | 修成参考图 4 的目标状态 | [查看](index.html#model=white-house-roof&mode=static&family=wrong-color) |
| `white-house-roof-static-extra-layer` | 静态·多叠一块 | 在参考图 3 的零件上，多装一块红色 1×1 薄板（3024）。 | 修成参考图 4 的目标状态 | [查看](index.html#model=white-house-roof&mode=static&family=extra-layer) |
| `white-house-roof-dynamic-control` | 动态·无错误对照 | 保持正常状态，不做后台改动。 | 最终补完全部模块 | [查看](index.html#model=white-house-roof&mode=dynamic&family=control) |
| `white-house-roof-dynamic-missing` | 动态·少一块 | 拿走参考图 1 的黑色零件（87079），保留刚刚新装的一块。 | 最终补完全部模块 | [查看](index.html#model=white-house-roof&mode=dynamic&family=missing) |
| `white-house-roof-dynamic-wrong-color` | 动态·颜色被换错 | 把参考图 1 的黑色零件（87079）换成同形状的黄色零件。 | 最终补完全部模块 | [查看](index.html#model=white-house-roof&mode=dynamic&family=wrong-color) |
| `white-house-roof-dynamic-extra-layer` | 动态·多叠一块 | 在参考图 3 的零件上，多装一块红色 1×1 薄板（3024）。 | 最终补完全部模块 | [查看](index.html#model=white-house-roof&mode=dynamic&family=extra-layer) |

### 同一阶段的正确状态与三种错误

以下配图来自展示路线。每种错误选画面变化最大的固定视角，并列出同视角的正确目标；展示页可切换三个方向。正式模型不会收到错误标签或这张对照表。

| 错误 | 应有状态 | 实际错误状态 |
|---|---|---|
| 少一块 | ![正确目标](white-house-roof/images/checkpoint-rear.png) | ![错误状态](white-house-roof/images/missing-rear.png) |
| 颜色被换错 | ![正确目标](white-house-roof/images/checkpoint-top.png) | ![错误状态](white-house-roof/images/wrong-color-top.png) |
| 多叠一块 | ![正确目标](white-house-roof/images/checkpoint-top.png) | ![错误状态](white-house-roof/images/extra-layer-top.png) |

<a id="rockefeller-crown"></a>

## 11. 洛克菲勒中心：补主塔顶部

**本题做什么：**各栋建筑主体已经装好，只补最高塔楼最上方的一小段。

- 模块：主塔顶部与邻近外墙盖板。
- 开始已搭好 232 块；只补 8 块。零件盘共 17 块，含备用件。
- 静态目标：参考图 7 的正确状态；提供目标图，修到这幅图即可。
- 动态目标：整个剩余模块完成。安装数量达到 7 块后尝试一次干扰；具体改哪块取决于实际拼法。
- 社区原模型：`v23-21007`；作者：Damien Roux [Darats]；[来源](https://library.ldraw.org/omr/sets/75)；[原 MPD](rockefeller-crown/original.mpd)。
- [查看这个模型的说明与全部 case](index.html#model=rockefeller-crown&mode=manual)。

| 本题开始 | 最终完成 |
|---|---|
| ![开始状态](rockefeller-crown/images/full-initial.png) | ![完整目标](rockefeller-crown/images/full-final.png) |

### 剩余哪些零件

下表数字对应说明图，不是评分要求的顺序。LDraw 名称保留原文方便查零件；直接看小图即可识别。

| 参考图编号 | 零件小图 | 零件号 / 颜色 | 原文件中的零件名称 |
|---|---|---|---|
| 1 | <img src="rockefeller-crown/images/part01.png" width="95" alt="零件 1"> | 3004 / 米黄色 | Brick  1 x  2 |
| 2 | <img src="rockefeller-crown/images/part02.png" width="95" alt="零件 2"> | 3623 / 米黄色 | Plate  1 x  3 |
| 3 | <img src="rockefeller-crown/images/part03.png" width="95" alt="零件 3"> | 3623 / 米黄色 | Plate  1 x  3 |
| 4 | <img src="rockefeller-crown/images/part04.png" width="95" alt="零件 4"> | 3070b / 米黄色 | Tile  1 x  1 with Groove |
| 5 | <img src="rockefeller-crown/images/part05.png" width="95" alt="零件 5"> | 3069b / 米黄色 | Tile  1 x  2 with Groove |
| 6 | <img src="rockefeller-crown/images/part06.png" width="95" alt="零件 6"> | 3710 / 米黄色 | Plate  1 x  4 |
| 7 | <img src="rockefeller-crown/images/part07.png" width="95" alt="零件 7"> | 4162 / 米黄色 | Tile  1 x  8 |
| 8 | <img src="rockefeller-crown/images/part08.png" width="95" alt="零件 8"> | 2431 / 米黄色 | Tile  1 x  4 with Groove |

**已实际跑通的另一种顺序：1 → 2 → 3 → 5 → 4 → 6 → 7 → 8。** 这条路线的无干扰、少件、换色、多件都通过了逐次操作检查，最终正确。

### 8 个 case

| case 编号 | 类型 | 具体错误 / 对照 | 做到什么算完成 | 展示 |
|---|---|---|---|---|
| `rockefeller-crown-static-control` | 静态·无错误对照 | 保持正常状态，不做后台改动。 | 修成参考图 7 的目标状态 | [查看](index.html#model=rockefeller-crown&mode=static&family=control) |
| `rockefeller-crown-static-missing` | 静态·少一块 | 拿走参考图 4 的米黄色零件（3070b），保留刚刚新装的一块。 | 修成参考图 7 的目标状态 | [查看](index.html#model=rockefeller-crown&mode=static&family=missing) |
| `rockefeller-crown-static-wrong-color` | 静态·颜色被换错 | 把参考图 4 的米黄色零件（3070b）换成同形状的黄色零件。 | 修成参考图 7 的目标状态 | [查看](index.html#model=rockefeller-crown&mode=static&family=wrong-color) |
| `rockefeller-crown-static-extra-layer` | 静态·多叠一块 | 在参考图 6 的零件上，多装一块红色 1×1 薄板（3024）。 | 修成参考图 7 的目标状态 | [查看](index.html#model=rockefeller-crown&mode=static&family=extra-layer) |
| `rockefeller-crown-dynamic-control` | 动态·无错误对照 | 保持正常状态，不做后台改动。 | 最终补完全部模块 | [查看](index.html#model=rockefeller-crown&mode=dynamic&family=control) |
| `rockefeller-crown-dynamic-missing` | 动态·少一块 | 拿走参考图 4 的米黄色零件（3070b），保留刚刚新装的一块。 | 最终补完全部模块 | [查看](index.html#model=rockefeller-crown&mode=dynamic&family=missing) |
| `rockefeller-crown-dynamic-wrong-color` | 动态·颜色被换错 | 把参考图 4 的米黄色零件（3070b）换成同形状的黄色零件。 | 最终补完全部模块 | [查看](index.html#model=rockefeller-crown&mode=dynamic&family=wrong-color) |
| `rockefeller-crown-dynamic-extra-layer` | 动态·多叠一块 | 在参考图 6 的零件上，多装一块红色 1×1 薄板（3024）。 | 最终补完全部模块 | [查看](index.html#model=rockefeller-crown&mode=dynamic&family=extra-layer) |

### 同一阶段的正确状态与三种错误

以下配图来自展示路线。每种错误选画面变化最大的固定视角，并列出同视角的正确目标；展示页可切换三个方向。正式模型不会收到错误标签或这张对照表。

| 错误 | 应有状态 | 实际错误状态 |
|---|---|---|
| 少一块 | ![正确目标](rockefeller-crown/images/checkpoint-isometric.png) | ![错误状态](rockefeller-crown/images/missing-isometric.png) |
| 颜色被换错 | ![正确目标](rockefeller-crown/images/checkpoint-top.png) | ![错误状态](rockefeller-crown/images/wrong-color-top.png) |
| 多叠一块 | ![正确目标](rockefeller-crown/images/checkpoint-top.png) | ![错误状态](rockefeller-crown/images/extra-layer-top.png) |

<a id="brandenburg-top"></a>

## 12. 勃兰登堡门：补顶部装饰

**本题做什么：**门柱、横梁和大部分屋面已经装好，只补顶部的盖板与装饰。

- 模块：门楼屋面盖板和顶部雕塑的积木化装饰。
- 开始已搭好 352 块；只补 10 块。零件盘共 21 块，含备用件。
- 静态目标：参考图 6 的正确状态；提供目标图，修到这幅图即可。
- 动态目标：整个剩余模块完成。安装数量达到 6 块后尝试一次干扰；具体改哪块取决于实际拼法。
- 社区原模型：`v23-21011`；作者：Orion Pobursky [OrionP]；[来源](https://library.ldraw.org/omr/sets/16)；[原 MPD](brandenburg-top/original.mpd)。
- [查看这个模型的说明与全部 case](index.html#model=brandenburg-top&mode=manual)。

| 本题开始 | 最终完成 |
|---|---|
| ![开始状态](brandenburg-top/images/full-initial.png) | ![完整目标](brandenburg-top/images/full-final.png) |

### 剩余哪些零件

下表数字对应说明图，不是评分要求的顺序。LDraw 名称保留原文方便查零件；直接看小图即可识别。

| 参考图编号 | 零件小图 | 零件号 / 颜色 | 原文件中的零件名称 |
|---|---|---|---|
| 1 | <img src="brandenburg-top/images/part01.png" width="95" alt="零件 1"> | 3069b / 浅沙绿色 | Tile  1 x  2 with Groove |
| 2 | <img src="brandenburg-top/images/part02.png" width="95" alt="零件 2"> | 3069b / 浅沙绿色 | Tile  1 x  2 with Groove |
| 3 | <img src="brandenburg-top/images/part03.png" width="95" alt="零件 3"> | 3069b / 浅沙绿色 | Tile  1 x  2 with Groove |
| 4 | <img src="brandenburg-top/images/part04.png" width="95" alt="零件 4"> | 3069b / 浅沙绿色 | Tile  1 x  2 with Groove |
| 5 | <img src="brandenburg-top/images/part05.png" width="95" alt="零件 5"> | 4733 / 浅灰色 | Brick  1 x  1 with Studs on Four Sides |
| 6 | <img src="brandenburg-top/images/part06.png" width="95" alt="零件 6"> | 6141 / 浅灰色 | Plate  1 x  1 Round |
| 7 | <img src="brandenburg-top/images/part07.png" width="95" alt="零件 7"> | 6141 / 浅灰色 | Plate  1 x  1 Round |
| 8 | <img src="brandenburg-top/images/part08.png" width="95" alt="零件 8"> | 6141 / 浅灰色 | Plate  1 x  1 Round |
| 9 | <img src="brandenburg-top/images/part09.png" width="95" alt="零件 9"> | 4599a / 浅灰色 | Tap  1 x  1 with Hole in Spout |
| 10 | <img src="brandenburg-top/images/part10.png" width="95" alt="零件 10"> | 4599a / 浅灰色 | Tap  1 x  1 with Hole in Spout |

**已实际跑通的另一种顺序：1 → 2 → 3 → 4 → 5 → 7 → 6 → 8 → 9 → 10。** 这条路线的无干扰、少件、换色、多件都通过了逐次操作检查，最终正确。

### 8 个 case

| case 编号 | 类型 | 具体错误 / 对照 | 做到什么算完成 | 展示 |
|---|---|---|---|---|
| `brandenburg-top-static-control` | 静态·无错误对照 | 保持正常状态，不做后台改动。 | 修成参考图 6 的目标状态 | [查看](index.html#model=brandenburg-top&mode=static&family=control) |
| `brandenburg-top-static-missing` | 静态·少一块 | 拿走参考图 1 的浅沙绿色零件（3069b），保留刚刚新装的一块。 | 修成参考图 6 的目标状态 | [查看](index.html#model=brandenburg-top&mode=static&family=missing) |
| `brandenburg-top-static-wrong-color` | 静态·颜色被换错 | 把参考图 1 的浅沙绿色零件（3069b）换成同形状的黄色零件。 | 修成参考图 6 的目标状态 | [查看](index.html#model=brandenburg-top&mode=static&family=wrong-color) |
| `brandenburg-top-static-extra-layer` | 静态·多叠一块 | 在参考图 5 的零件上，多装一块红色 1×1 薄板（3024）。 | 修成参考图 6 的目标状态 | [查看](index.html#model=brandenburg-top&mode=static&family=extra-layer) |
| `brandenburg-top-dynamic-control` | 动态·无错误对照 | 保持正常状态，不做后台改动。 | 最终补完全部模块 | [查看](index.html#model=brandenburg-top&mode=dynamic&family=control) |
| `brandenburg-top-dynamic-missing` | 动态·少一块 | 拿走参考图 1 的浅沙绿色零件（3069b），保留刚刚新装的一块。 | 最终补完全部模块 | [查看](index.html#model=brandenburg-top&mode=dynamic&family=missing) |
| `brandenburg-top-dynamic-wrong-color` | 动态·颜色被换错 | 把参考图 1 的浅沙绿色零件（3069b）换成同形状的黄色零件。 | 最终补完全部模块 | [查看](index.html#model=brandenburg-top&mode=dynamic&family=wrong-color) |
| `brandenburg-top-dynamic-extra-layer` | 动态·多叠一块 | 在参考图 5 的零件上，多装一块红色 1×1 薄板（3024）。 | 最终补完全部模块 | [查看](index.html#model=brandenburg-top&mode=dynamic&family=extra-layer) |

### 同一阶段的正确状态与三种错误

以下配图来自展示路线。每种错误选画面变化最大的固定视角，并列出同视角的正确目标；展示页可切换三个方向。正式模型不会收到错误标签或这张对照表。

| 错误 | 应有状态 | 实际错误状态 |
|---|---|---|
| 少一块 | ![正确目标](brandenburg-top/images/checkpoint-top.png) | ![错误状态](brandenburg-top/images/missing-top.png) |
| 颜色被换错 | ![正确目标](brandenburg-top/images/checkpoint-top.png) | ![错误状态](brandenburg-top/images/wrong-color-top.png) |
| 多叠一块 | ![正确目标](brandenburg-top/images/checkpoint-isometric.png) | ![错误状态](brandenburg-top/images/extra-layer-isometric.png) |

## 这次真正验证了什么

- 12 个模型，99 个正常安装步骤；96 个 case 的参考处理路线全部走通。
- 每个模型另找到一种不同的合法顺序；共 48 次额外动态回放（12 × 无干扰/少件/换色/多件），都完成，36 次错误条件都真正触发并修复。
- 其中 9 个模型的替代路线在达到干扰数量时，实际形状也不同于参考路线；相应 27 条错误回放仍然成功触发并修复。这专门检查了“不必先拼成参考中间状态”的要求。
- 12 个模型都另外检查了交换同形同色零件的身份，最终仍算完成。
- 每次安装、干扰和参考修复都检查真实连接、位置碰撞和直线装入/拆出路径；重复安装、悬空安装被拒绝。
- 三种错误在每个模型至少一个固定视角有可见的像素变化。这是机器检查，不替代真人可理解性验证。
- 完整场景保留原模型全部零件；不能可靠计算精细碰撞的背景件用外包盒保守阻挡，不能当成不存在。
- 证据：[audit.json](audit.json)；各模块的 `order-checks.json`；原文件校验值与来源在各模块 `provenance.json`。

## 当前范围与还没证明的事

这是社区模型模块扩充组，未混入旧题库或论文成绩。12 个物件增加了外形和结构种类，但仍是短模块、一次干扰、三类错误，不能声称覆盖全部人类拼装错误或已经达到高难度。

主体作为已经搭好的固定物件提供，允许夹具托住；没有模拟重力、手指、摩擦或卡扣力度。动作接口当前使用有限候选位置；不能据此声称测了任意连续位姿控制。

**本次模型 API 调用 0 次，API 费用 0；新增真人评测 0 次。** 下一步是让真人确认说明/画面清楚，再比较模型无干扰与有干扰的表现。

说明图由本项目按原模型位置生成并检查，不是 LEGO 官方说明书。社区原文件、作者和许可声明均保留，未把原模型修改成自造外形。

接口详细说明：[INPUT-OUTPUT.zh-CN.md](INPUT-OUTPUT.zh-CN.md)。本目录 HTML 和此清单是讲解页，包含答案；测试时只使用 `run_episode.py` 返回的公开观察。
