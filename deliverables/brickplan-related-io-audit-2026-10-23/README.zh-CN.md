# 别人的积木与动态 benchmark，到底给模型什么、让它回什么？

核对日期：2026-10-23。查阅 10 项工作，读取其中 8 个公开代码仓库的实际输入构造、提示词或环境代码；BrickGPT 另查官方仓库说明，MEPNet 以论文任务定义为依据。没有运行这些模型或仿真，没有调用付费 API。

## 先用人话说结论

**不是所有 benchmark 都只发图，也不是都让模型自己一步步选积木、选位置。** 有的给文字让模型设计新物件，有的给说明图和三维零件，有的只让模型从候选里挑下一块，位置由程序处理。要比较的是“模型收到多少信息、自己负责哪些决定”，不能只数图。

与我们最相关的是：**PhyBlock 的逐步规划、AsgardBench 的观察与行动循环、SCANet 的单步纠错**。但三者的额外信息和动作定义都有明显区别，下面逐项说明。

## 一、逐项输入输出对照

| 工作 | 实际给模型什么 | 模型返回什么 | 有没有一步步看当前状态 | 核对依据 |
|---|---|---|---|---|
| LEGO-Puzzles | 题目相关图片，问题、选项，部分题有提示；支持多图和图文交错 | 选择答案；排序题返回字母顺序；另有生成图片的扩展任务 | 主 VQA 没有执行动作的循环 | [代码：LEGO 类](https://github.com/Tangkexian/LEGO-Puzzles/blob/1413d2c236879573cc0afff646bae5e3d04023bd/vlmeval/dataset/image_mcq.py#L1335-L1411)、[论文 §3.1](https://arxiv.org/html/2503.19990v1#S3.SS1) |
| MEPNet | **本步骤说明图**，当前主体的三维体素，本步要新增组件的三维体素 | 本步骤各组件相对于主体的三维位置和旋转 | 按说明步骤预测，不是通用聊天模型自由操作 | [论文 §3](https://arxiv.org/html/2207.12572v1#S3) |
| SCANet / LEGO-ECA | 说明图、错误装配图，以及主体／零件的三维形状、组件当前姿态和组件渲染图 | 每个组件的正确／错误状态，以及修正后的位置和旋转 | 主任务是某一步的组件纠错，不是从空底板进行任意装拆 | [论文 §IV](https://arxiv.org/html/2403.18195v1#S4)、[组件编码代码](https://github.com/Yaser-wyx/SCANet/blob/2cca7ba523b8aa26d9fdc2a7fd90e3fce682dea8/src/SCANet/SCANet.py#L193-L219) |
| PhyBlock：一次规划 | GPT-4V 脚本发送**一张合并的目标与候选图**，加文字任务 | 描述完整拼装步骤的文本，保存到结果 JSON | 此模式没有每步重新观察 | [推理脚本](https://github.com/PhyBlock/PhyBlock/blob/da81ed9cad8184509aadb6f01af83d53e5c9d6fa/inference_scripts/infer_gpt4v_api.py#L15-L49) |
| PhyBlock：逐步规划 | **3 张图：目标、候选积木总览、当前状态**，另加已执行计划文本 | 下一条 `Move(编号)`，或 `Done` | 有，执行后再给当前画面 | [请求构造](https://github.com/PhyBlock/PhyBlock/blob/da81ed9cad8184509aadb6f01af83d53e5c9d6fa/step_by_step_inference/vlm_planner.py#L88-L137)、[动作定义](https://github.com/PhyBlock/PhyBlock/blob/da81ed9cad8184509aadb6f01af83d53e5c9d6fa/step_by_step_inference/prompts/block_build/env_action.txt) |
| Break and Make / LTRON | 场景和手中零件的渲染观察；先允许查看、拆开原物件，再清空重建；重建依靠此前观察 | 视角、光标／连接点选择、取放、拆除、旋转、选零件等离散动作 | 有，属于视觉交互环境 | [论文 §3.2](https://arxiv.org/html/2207.13738v1#S3.SS2)、[环境代码](https://github.com/aaronwalsman/ltron/blob/253be3e55cef068c1842fd9a7d2e2b3c22d19d7b/ltron/gym/envs/break_and_make_env.py#L257-L326) |
| AsgardBench | 文字目标，默认**当前和上一步之前两张图**，可用对象名称、动作、规则、动作历史与成功／失败；还可回传模型自己提出的计划和笔记 | 文本动作，如 `Action: PICKUP Mug`；全计划模式还输出剩余计划，但每轮只执行一个动作 | 有；目标通常是文字任务，不是成品目标图 | [论文附录 A.2](https://arxiv.org/html/2603.15888v1#A1.SS2)、[实际图片请求](https://github.com/microsoft/AsgardBench/blob/4d38d380362d767893611fc160dc78665d1356b8/AsgardBench/Model/openrouter_actor.py#L271-L305) |
| BrickGPT | **文字描述**，模型接着生成积木序列；物理检查程序可拒绝或回退不合法生成 | 每块积木的尺寸和坐标文本，之后可转换成 LDraw 和渲染图 | 自回归生成不是每轮看真实当前图再修复 | [官方推理与输出说明](https://github.com/AvaLovelace1/BrickGPT#running-inference-interactively)、[方法](https://arxiv.org/html/2505.05469v1#S4) |
| BrickNet | 条件生成读取 **caption 文字**；也有无条件生成模式 | 零件、颜色、连接关系等组成的构建序列文本，可转成 LDraw | 官方生成脚本不是图像闭环操作 | [生成脚本](https://github.com/kulits/BrickNet/blob/283faf73063d3af4eb378b624df68dec683e4695/scripts/generate.py#L48-L108)、[序列格式](https://github.com/kulits/BrickNet/blob/283faf73063d3af4eb378b624df68dec683e4695/src/bricknet/tree.py#L1-L24) |
| BrickBench / BrickAgent | 初始是**设计需求文字和 Python 工具说明**；代理可查询零件、连接器和几何信息，可渲染查看自己的设计 | `build.py` 和 `model.mpd`；中途可以写代码、运行检查、改设计 | 可以自行检查和迭代，但不是规定每轮一块的外部干扰修复任务 | [完整代理提示词](https://github.com/kulits/BrickAgent/blob/b3df55e36c669b22ef089b13db1ee841907d09b3/scripts/prompt.md)、[查看工具](https://github.com/kulits/BrickAgent/blob/b3df55e36c669b22ef089b13db1ee841907d09b3/src/brickagent/view.py#L15-L25) |
| RoboRecover | 各机器人策略接口不同；核对的 OpenPI / LIBERO 适配器给**场景相机图、手腕相机图、机械臂与夹爪状态、文字任务** | 数值动作序列，再逐步送入环境 | 有；先由评测器重放前序动作，把策略放到指定偏差状态开始恢复 | [观察字段](https://github.com/RUCKBReasoning/RoboRecover/blob/089b9420e8b7c303e2338a8212a8b6c27c26a79b/overlays/openpi/examples/libero/eval_filtered_repro.py#L256-L272)、[动作推理](https://github.com/RUCKBReasoning/RoboRecover/blob/089b9420e8b7c303e2338a8212a8b6c27c26a79b/overlays/openpi/examples/libero/eval_filtered_repro.py#L844-L903) |

图片张数指模型请求中的图像条目，不等于画面里有几个视角：**一张合并图可以包含多个视角或许多零件。** VQA 的答案、机器人的动作数组、以及提交的结果文件也不是同一种输出。

### 实际输入图长什么样？

下面是 PhyBlock 官方一次规划脚本对应目录中的第 000 张图片：**一个 1024×512 的 PNG，左边一个目标，右边十六个带编号的积木候选。** 这叫“一张输入图”，不是十七次图像上传。图片来自作者公开仓库，未修改。[原图](https://github.com/PhyBlock/PhyBlock/blob/da81ed9cad8184509aadb6f01af83d53e5c9d6fa/data/SCENEs_400_Goal_and_Cand_Imgs_resized/000.png)

![PhyBlock 官方示例：左边目标，右边十六个候选](https://raw.githubusercontent.com/PhyBlock/PhyBlock/da81ed9cad8184509aadb6f01af83d53e5c9d6fa/data/SCENEs_400_Goal_and_Cand_Imgs_resized/000.png)

## 二、最重要的新发现：PhyBlock 的 Move 并不要求模型自己选安装位置

这是代码里对我们最有用的区别。

在其公开 `BlockEnv.move_cube()` 中，模型只提交候选编号。环境查找当前层匹配的目标块，从内部任务记录读取该块的 `position` 和 `euler`，再设置积木位置和旋转。也就是说，**这里模型主要选择积木／姿态候选及次序，程序处理落到哪里；不是我们“选一块，再从多个位置中选安装位置”的同一动作任务。** [代码](https://github.com/PhyBlock/PhyBlock/blob/da81ed9cad8184509aadb6f01af83d53e5c9d6fa/step_by_step_inference/block_env.py#L146-L177)

所以它每轮三张图和我们多图接口可以比较信息组织，却不能直接比较拼装成功率。给模型自动放到目标位置，会省掉一部分空间定位问题。

一次规划还有论文与具体脚本的描述粒度差异：论文实验设置提到 RGB-D 初始场景；本次查看的 GPT-4V 脚本实际构造的是一个 PNG 图像条目和文字，没有单独传入深度图或坐标字段。因此表中按这份脚本报告，不能推广为其所有方法都只用同样的一张图。[论文设置](https://arxiv.org/html/2506.08708v1#S4.SS1)、[实际请求](https://github.com/PhyBlock/PhyBlock/blob/da81ed9cad8184509aadb6f01af83d53e5c9d6fa/inference_scripts/infer_gpt4v_api.py#L29-L49)

还发现公开交互脚本与规划器有接线不一致：入口导入的规划器模块名未出现在所查目录，入口调用 `reset` 的参数个数与现有类定义不同，更新历史的方法名也不同。这是**静态阅读发现，未运行复现**；不能把当前公开代码片段当作已经完整跑通的论文实验包，也不应照抄其接线。[入口](https://github.com/PhyBlock/PhyBlock/blob/da81ed9cad8184509aadb6f01af83d53e5c9d6fa/step_by_step_inference/evaluate_block_vlm_step.py#L1-L13)、[调用位置](https://github.com/PhyBlock/PhyBlock/blob/da81ed9cad8184509aadb6f01af83d53e5c9d6fa/step_by_step_inference/evaluate_block_vlm_step.py#L103-L130)、[规划器定义](https://github.com/PhyBlock/PhyBlock/blob/da81ed9cad8184509aadb6f01af83d53e5c9d6fa/step_by_step_inference/vlm_planner.py#L31-L74)

## 三、AsgardBench 接近我们的动态观察方式，但不只是“两张图”

其主提示词还给可用对象名称、世界规则、示例和历史。模型可以保留自己提出的后续计划，观察后修改；这份计划不是答案提供的正确路线。图像模式默认使用上一状态和当前状态；首轮只使用当前图。论文说明两图为 1024×1024。[完整提示词](https://github.com/microsoft/AsgardBench/blob/4d38d380362d767893611fc160dc78665d1356b8/AsgardBench/Data/prompts/main_prompt.prompt#L16-L139)、[论文附录](https://arxiv.org/html/2603.15888v1#A1.SS2)

**输出并不必须是 JSON。** 其提示词约定最后给一行文本动作；全计划配置还输出剩余计划，但环境每轮只执行一个动作。这说明“输出整个计划”和“一次只执行一步”可以并存。[输出约定](https://github.com/microsoft/AsgardBench/blob/4d38d380362d767893611fc160dc78665d1356b8/AsgardBench/Data/prompts/task_instructions.prompt#L102-L158)

它主要测试根据物体状态和场景条件调整计划，不能直接称为与我们完全相同的“拼到中途，后台偷偷拆件／加件”任务。另外，作者也发现手持物体在画面中有歧义，于是添加手部提示并做消融；这支持我们先验证输入可理解性，不能只凭最后失败判定模型能力。[论文 §5.1](https://arxiv.org/html/2603.15888v1#S5.SS1)

## 四、关于“说明书”和“很多图”，要分清用途

1. **说明书是合理输入。** MEPNet 明确按本步骤目标说明图、当前主体三维形状和新增组件三维形状进行预测。它不是凭最终一张照片猜整个内部结构。我们提供模块说明书有依据。[MEPNet 任务定义](https://arxiv.org/html/2207.12572v1#S3)
2. **但“说明书按需查询”是我们自己的接口选择。** 本次核对没有依据说它是这些工作的统一标准；不能拿别人的论文代替我们验证查看步骤是否方便、信息是否足够。
3. **BrickBench 的八视图属于评分输入。** `scripts/vqa.py` 把成品八视图给评价模型回答问题；拼装代理起始任务是文字和工具。这八张不能算成“它每轮拼装默认收到八张目标图”。[评分代码](https://github.com/kulits/BrickAgent/blob/b3df55e36c669b22ef089b13db1ee841907d09b3/scripts/vqa.py#L1-L15)
4. **BrickGPT 的二十四视图用于生成训练数据描述。** 主模型推理仍从文字生成积木；不能把制作数据时的图片当作生成模型的每轮输入。[官方流程](https://avalovelace1.github.io/BrickGPT/)
5. 在核对的交互例子中，没有找到“每轮都发送几十张整本说明图和逐件图片”是必要条件的证据。我们的新版 7–9 张也不能仅凭文献宣布最合适，需要用实际任务对照验证。

## 五、这些结果对我们意味着什么？

下面是根据论文和代码作出的设计判断，不是已经完成的新实验。

| 我们需要确认的问题 | 从别人那里得到的提醒 | 我建议怎么验证 |
|---|---|---|
| 为什么拼不起来 | PhyBlock 可自动处理目标位姿，SCANet / MEPNet 另有三维输入；输入和动作难度并不相同 | 把“能认出下一块”和“能自己选位置”分开做少量诊断；自动目标放置只能另列辅助条件 |
| 7–9 张是否合适 | AsgardBench 两图、PhyBlock 交互三图，但视角和任务不同 | 对照单视角、三视角、按需视角；先确保干扰可见，不直接把减图后的下降归为推理问题 |
| JSON 是否拖累 | 相近工作也用固定单行文本动作 | 用相同场景对照现有 JSON 和简单动作文本；不把格式错误记为看不见错误 |
| 要不要每轮只输出一步 | AsgardBench 可以输出计划而只执行首个动作 | 可另设“保留自己的计划、每步执行一个动作”条件，检查是否改善长回合记忆 |
| 动态题没到干扰位置 | RoboRecover 明确从重放后的指定中途状态评估恢复 | 保留端到端配对，同时可另做中途起点恢复组；不把系统完成的前序算成模型拼装能力 |
| 是否已经排除我们的问题 | 任务像、都发图，不等于接口同样容易或信息同样充分 | 仍需正常拼装对照、真人可理解性、新接口实测，以及格式／服务故障独立统计 |

**结论：我们的“看图—动作—新画面”方向有相关工作支持；但“他们也发图，所以我们的失败一定是模型问题”这个推论不成立。** 现阶段最该补的是可比较的输入与动作诊断，不是继续单纯增加每轮图片数量。

## 六、证据与版本

[source-manifest.json](source-manifest.json) 记录实际读取的源码路径、Git 提交号、文件 SHA256 和对应永久链接。代码副本仅保存在本机研究缓存，不把别人的整库提交进我们的仓库。

这是论文与代码静态核对，不是他人系统的复现报告；仓库当前公开代码与论文当年的运行版本也可能不同。AsgardBench 的旧 OpenRouter 适配器由作者注明保留用于论文结果追溯，因此本次查看了该文件；不能据此声称它现在无需修改即可运行。RoboRecover 的具体输入说明仅覆盖核对的 OpenPI / LIBERO 适配器，不能扩大到所有策略。
