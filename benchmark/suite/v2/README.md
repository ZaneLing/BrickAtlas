# Casebank v2

本版本提供5,120个独立结构和117,910个任务条件case，以及全部逐题GT与传统算法基线。
先读 [中文报告](REPORT.zh-CN.md) 和 [指标合同](METRICS.md)。
英文现状论文位于 `benchmark/paper/`，使用官方CVPR模板；不是投稿完成声明。
新增研究与严格评分修复见 [当前能力说明](../study/OVERVIEW.zh-CN.md)、
[最新实测报告](../study/REPORT.zh-CN.md) 和 [研究复现](../study/README.md)。

## 开始使用

要求Node 22+及父仓库依赖。在 `benchmark/` 中运行：

```bash
npm run suite:start
```

打开启动器报告的URL，默认 `http://127.0.0.1:5175`，选择 **Casebank v2**。
旧Pilot、composition-v1和历史模型结果仍保留。
本机Node不在PATH时可从仓库根运行：

```bash
.tools/node-v22.23.2-darwin-arm64/bin/node benchmark/suite/launch.mjs
```

Casebank页是研究者界面：可显式访问裁判真值。不要将该界面或GT下载权限当作模型输入。

## 文件组织

`suite/artifacts/casebank-v2/`：

- `manifest.json`：版本、规模、split、全部源码/分片hash。
- `structures.jsonl.gz`：5,120个源结构。
- `case-index.jsonl.gz`：117,910题索引，含裁判变体标签，**不是模型输入**。
- `inputs-{split}.jsonl.gz`：公开题面；只含caseId和input，不含oracle、变体spec。
- `ground-truth-{split}.jsonl.gz`：逐题完整真值与oracle评分，**裁判专用**。
- `render-private-{split}.jsonl.gz`：离线渲染用几何配方，**不能发给视觉模型**。
- `baseline-audit.json`：oracle/empty/copy-input全量审计，不是模型成绩。
- `verification.json`、`replay-evaluations.json`、`clean-verification.json`：复算证据。
- `quality-audit.json`：策略分布与近重复筛查范围。

`suite/artifacts/evaluations-v2/<run>/`：

- `selection.json`：运行前冻结的题目选择。
- `cases.jsonl.gz`：所有提交、漏答、逐指标及诊断。
- `summary.json`：任务/条件/split、策略、难度分层与指标分母。

没有预渲染全量PNG；导出按需生成。数据和评测结果已压缩存储，不依赖原runtime目录。

## 重建与复现

```bash
npm run v2:verify
npm run v2:replay
npm run v2:clean
npm run v2:check
```

`v2:verify`逐条重建并核对所有GT、公开输入、私有渲染配方和压缩分片hash。
`v2:replay`复算全部提交和回放状态链。
`v2:clean`复制源码与产物，不复制runtime/API key，再跑全量验证。
它共享已安装依赖，不是第二台机器上的独立复现。
`v2:check`需要本地server和下述46题导出已存在；包含浏览器检查，不触发收费。

修改生成器/任务/评分器后，使用新版本或明确重建未发布版本：

```bash
npm run v2:build
```

该命令会重建完整产物，不能用它悄悄覆盖已经发表实验所依赖的版本。
中断时`.building`目录保留，需先确认没有构建进程并检查原因，不能并发重建。

## 外部模型评测

1. 冻结选择，可按split、condition以及源对象组数选取；不根据模型成功率选题：

```bash
npm run v2:select -- --split=test_id --condition=all --objects=2
```

输出selection文件路径。已提供这个确定性两对象选择：
`suite/artifacts/casebank-v2/selections/selection-11834ad4590d368f.json`。
它覆盖46题，用于输入导出验收，不作为大样本模型实验。

2. 生成模型真正使用的PNG和题面（需要server）：

```bash
npm run v2:export -- --selection=suite/artifacts/casebank-v2/selections/selection-11834ad4590d368f.json
```

输出到 `.runtime/casebank-exports/<selection>/inputs.jsonl` 和 `images/`。
每行含 `caseId, system, input, images`。普通输入不包含故障变体标签。
完整symbolic参考属于显式特权条件，不能与普通视觉成绩混淆。
已完成导出不会自动覆盖；需要重复时先显式归档旧目录。

3. 外部模型逐题提交：

```json
{"caseId":"...","answer":{"version":1,"parts":[]}}
```

```bash
npm run v2:score -- --selection=/absolute/selection.json --predictions=/absolute/predictions.jsonl --model=model-name
```

此命令不调用模型API。漏答记失败；重复/未知题目拒绝。
新提交默认使用`v2-strict-schema-1`，拒绝旧decoder可隐式转换的数组型号/颜色。
原评分器仅通过CLI `score-legacy`用于历史复现；既有结果不改写。
`v2:replay`按保存的评分版本分派，严格版本另核对全分层统计与源码hash。
第三方模型身份是提交者声明；没有提供的原始API日志、时间、token、费用不伪造。
批量结果自动显示在Casebank页，可逐题打开回放。
API适配器仍限16图片，部分v2分层题会超过该上限；不能静默删图，应由支持完整输入的外部模型适配器处理。
v2没有默认全量收费按钮，避免无意扫测11万题。

## 传统基线

```bash
npm run v2:baseline -- --selection=suite/artifacts/casebank-v2/selections/selection-996286b8b0439c39.json
```

这是全题库选择。基线只读取PublicTask，支持符号关系、编辑、贪心装拆和特权符号比对。
不支持的视觉/约束生成题返回空答案并显式计0；这不是视觉模型结果。
每次执行新建run，不覆盖已有评测。

## 边界

数字名义网格和25目录类型；无机器人、通用CAD连接或力学模拟。
5,120对象均程序生成，不是独立人工设计。8策略、近重复筛查均有局限，见中文报告。
人审仍未完成。最新扩展已完成674次v2主实验与56次对照；
多模态训练矩阵的完成组数以最新报告为准，不能把启动实验当作完成。
历史神经实验和费用保留在旧目录，不挪用为v2结果。
