# 社区模块接口：给什么、做什么、怎么算完成

这是给后续接模型的程序接口说明。真人看 `index.html`，不需要填写这些字段。

## 一、两种任务分别怎么算完成

| 任务 | 初始状态 | 验收目标 | 结束要求 |
|---|---|---|---|
| 静态修复 | 已经做到指定步骤，可能有错误 | 指定步骤的正确状态 | 修到这一阶段，然后结束；不要装后续步骤 |
| 动态完成 | 主体已搭好，剩余模块还没开始 | 全部剩余步骤完成后的状态 | 中途发现并修复改动，继续完成模块，再结束 |

每个模型的静态目标图和最低干扰数量见 [完整清单](MODEL-CASE-CATALOG.zh-CN.md)。参考说明编号只是定位目标图，不要求沿着这些编号操作。完整物件最终图和“本题验收目标”使用不同图片角色。静态题不能因为看见完整物件最终图，就被要求完成后面所有步骤。

## 二、公开观察

`run_episode.py` 每轮输出一条 JSON，包含：

- `task`：这道题要做什么。
- `mode`、`acceptanceStage`：静态或动态，要做到指定步骤还是最终状态。
- `handles`：匿名零件编号和可尝试的放置选项编号。
- `images`：图片路径、图片校验值、角色、视角或说明书步数。
- `feedback`：上次操作是否被接受；不会解释隐藏干扰。
- 已用操作次数、操作上限和可用视角。

图片角色：

| role | 含义 |
|---|---|
| `scene-overview-initial` / `scene-overview-final` | 开始和完成时的整个物件，帮助理解背景 |
| `module-start` | 主体已搭好、模块尚未开始的近景 |
| `full-completion-reference` | 模块全部完成后的参考图 |
| `acceptance-target` | 这道题真正要达到的状态 |
| `instruction-piece` | 某一步要拿的那一块 |
| `instruction-after` | 这一步正确完成后的说明图，橙色轮廓标出新增零件 |
| `inventory` | 匿名零件的外形 |
| `before-last-action` | 上次操作之前的真实状态 |
| `current-now` | 上次操作和可能的隐藏改动之后的真实状态 |
| `candidate-preview` | 某个放置选项在当前场景中的外观，不代表它合法或正确 |

同一模型的条件共享说明书、预装主体、零件表、候选位置、相机与图像大小。动态各条件从相同的初始状态开始；静态条件按设计从不同的当前错误状态开始。图片文件名使用内容摘要，不把 `missing`、`goal` 或错误部位编号暴露给模型。

## 三、一次只提交一个动作

模型接口支持：

```json
{"type":"attach","partId":"A01","candidate":"C003"}
{"type":"detach","partId":"A01"}
{"type":"inspect","view":"top"}
{"type":"inspect","view":"isometric","candidate":"C003"}
{"type":"inspect","view":"rear","partId":"A01"}
{"type":"finish"}
```

上面每一行都是一个独立动作，不要把六行一次性提交。

- 一个 `attach` / `detach` 只处理一块积木。
- `inspect` 不改变积木，可以查看三个固定视角、某个候选位置或一块零件。
- 安装选项包括错误位置。需要先看候选预览，与说明图比较；编号本身不标正确答案。
- 每次操作后立即返回新画面；模型不会收到纠错提示或答案。
- 不接受直接设置整组状态。已搭好的主体不能被操作。
- 目前允许手或夹具托住子组件，不模拟重力或完整机器人运动规划。

## 四、中途干扰与计分

**不要求唯一安装顺序，也不比较中间状态是否等于参考答案。**

- 动态从主体已搭好、模块尚未开始的状态出发。达到最低“当前已装模块零件数”后，后台从实际状态选可行的干扰位置。
- 少件、换色只动先前装过的一块，保留刚刚装入的那块；多件在已安装模块上找真实可连接的位置。
- 干扰的操作及其反向修复均须通过连接、碰撞和直线路径检查；无可行位置时推迟到后续合法动作，不强行注入。
- 不读取“必须是参考图哪一步”或“必须有哪些正确零件”作为触发条件。换顺序可能导致具体受影响零件不同。
- 每条错误轨迹最多一次干扰。查看、失败操作、重复安装不会推进安装数量。

后台分别记录：

| 字段 | 意义 |
|---|---|
| `success` / `completionSuccess` | 已声明完成且最终几何、颜色正确；无论是否触发干扰 |
| `finalGeometryCorrect` | 当前物件是否达到本题验收目标 |
| `eventApplied` | 干扰是否确实发生 |
| `repairSuccess` | 有干扰且触发后，是否最终完成；未触发或无干扰对照为 `null` |
| `intermediateStateComparedToGT` | 恒为 `false`，不比较中间状态与参考路线 |
| `acceptedActionsPhysicallyChecked` | 每个接受的操作都经过物理几何检查 |

汇报实验时同时给出所有轨迹的完成率、错误条件的触发率，以及真正触发后的修复成功率。**没有发生干扰不能计成修复成功，也不能让已拼对的物件被判成完成失败。** 不把不同路线的适应性干扰说成完全相同的错误位置；需要固定干扰位置的对比实验，应另外定义条件并报告未触发记录。

评分按最终物理形状、位置、朝向和颜色比较，允许外形和颜色完全相同的零件互换；候选表也加入了同形同色零件可交换的位置。参考路线是可行路线，不宣称最短。正式观察不输出错误类别、触发条件、目标坐标、受影响编号或修复动作。

`orderPolicy` 为 `any-physically-legal-order`，`intermediateGTMatching` 为 `false`。当前接口仍是有限位置候选，不是任意连续坐标的机械臂控制。候选预览只是“如果放在那里会看到什么”，不代表已安装；只有 `attach` 返回 `OK` 才会改变实际状态。

## 五、无需 API 密钥即可运行本地接口

在项目根目录：

```bash
benchmark/.runtime/mlx-env/bin/python \
  benchmark/brickplan-repair/community_modules/run_episode.py \
  --module cottage-roof --condition dynamic-missing
```

程序先输出初始观察，之后从标准输入逐行读取动作。它只运行本地环境，**不会发起模型 API 请求**。

`--module` 可选：

```
cottage-roof                 racer-top
seaplane-tail                museum-roof
repair-truck-cab             orange-helicopter-tail
police-helicopter-top        panda-head
burger-stand-roof            white-house-roof
rockefeller-crown            brandenburg-top
```

`--condition` 是 `static-` 或 `dynamic-` 加上 `control`、`missing`、`wrong-color`、`extra-layer`。

正式请求模型时，接入程序要根据每条 `images` 记录读取 PNG，把图片内容连同角色说明发给支持图像的模型；不能只给模型一个本地文件路径。所有说明图在整个过程可取用。查看候选位置必须返回实际预览图。

`runs/<随机编号>/record.private.json` 是后台记录，不能发给模型。HTML 展示页、`cases.private.json`、`certificate.private.json`、`manual.private.json` 也不应发送给模型。
