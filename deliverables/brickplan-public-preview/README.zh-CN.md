# Brick Atlas 题库公开展示预览

这是本机数据浏览页，尚未上传Hugging Face，也不是隐藏测试集发布包。本轮没有改变已有题目、模型动作接口或参考答案，没有调用付费模型。

## 打开

在项目根目录双击`打开题库公开展示.command`，或运行：

```bash
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m public_preview_server --port 8799
```

浏览器打开 <http://127.0.0.1:8799/>。默认是赛车静态偏移题，上方可切换动态错色、连续三次干扰和正常对照。

## 实际展示范围

- 全部 **5,793题的目录**：静态3,699、动态2,094，含正常对照。
- **95个完整图例**：原始PNG、开始与已保存中途观察、原生动作格式和程序验证的参考路线。
- 其余题目明确标为“仅目录”，不拿其他题的图片代替本题。
- 1,080份原始图像保留原字节与SHA256，没有用生成图片替换几何图。
- L1–L3是暂定结构分组；参考路线不是模型成绩，不要求照抄，也未证明最短。

## 页面怎么看

1. **模型看到什么**：当前／目标三视图、保存的中途观察、全部零件目录，以及按需查看说明图的例子。
2. **怎么提交动作**：用这道题实际公开的编号生成动作格式示例。这里不执行安装、不提交真人答卷。
3. **正确结果与修复**：单独读取参考文件，查看最终状态、关键帧、错误讲解和逐步动作。
4. **数据怎么存**：查看来源分组、输入字段，分别下载模型输入和参考答案。

目录上的错误类别是审题信息。模型输入没有错误类别、后台事件、参考路线或目标坐标答案。S／D使用外层`action`字段，M／E7直接提交动作对象，页面保留真实差异。

## 编号、坐标与自由回答

当前是**交互动作任务，每一步从有限位置中选择**。模型决定查看、装拆顺序和结束时机，用结构化动作改变场景；不是整道题只选一个A/B/C，也不靠自由文本解释得分。

建议主实验保留位置编号；坐标与朝向另设定位组，两组成绩分开。接点配对也是可扩充接口，统一公开标记尚待补齐。

## 别人怎么发布

| 项目 | 实际存储与展示 |
|---|---|
| [LEGO-Puzzles](https://huggingface.co/datasets/KexianTang/LEGO-Puzzles) | TSV题目、选项、答案与图片字段；HF逐行查看，项目页配图。主VQA不是逐步改变现场。 |
| [PhyBlock](https://github.com/PhyBlock/PhyBlock) | PNG、目标／候选JSON，另有HF图片浏览和过程GIF。所查逐步执行器读取内部目标位姿，不能当作模型自己求落点。 |
| [BrickBench](https://brickben.ch/) | 设计任务JSON、评价问题图、构建代码和LDraw作品；可旋转作品画廊。任务是文字条件设计。 |
| [EmbodiedBench操作轨迹](https://huggingface.co/datasets/EmbodiedBench/EB-Man_trajectory_dataset/blob/main/README.md) | JSON逐步动作、图像路径与反馈，图片另存ZIP；项目页展示过程。所查轨迹使用7维离散动作。 |

页面第二栏附实际字段、原图和原始来源链接。作者原图未修改，版本与哈希在`references/source-manifest.json`。这是源码与资料核对，不是他人环境的运行复现。

## 数据文件

```text
catalogue.jsonl                  全部5,793题目录
metadata.jsonl                   95个图例索引
assets/*.png                     原始图片
samples/Q084/initial.model-input.json
samples/Q084/sample.json         浏览信息
samples/Q084/reference.answer.json
```

动态例子另有`observation-N.model-input.json`。输入文件的图片路径相对于展示包根目录；正式请求视觉模型时仍需读取图片内容，不能只发送文件路径。

Hugging Face支持图片配合`metadata.jsonl`、Parquet等组织方式，见[官方说明](https://huggingface.co/docs/hub/datasets-image)。本包展示存储方式；正式上传前仍需验证图片列、分组、许可与实际加载。完整动态评测还需要原运行环境及评分程序，下载一行题目不能运行全套评测。

## 重建

```bash
PYTHONPATH=benchmark/brickplan-repair benchmark/.runtime/mlx-env/bin/python -m public_preview
```

生成器复用`brickplan-question-showcase`的原始输入与已验证记录，核对图片哈希后导出。网页源码及同行资料保留，重建不调用付费模型。
