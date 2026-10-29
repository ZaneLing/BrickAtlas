"""Summarize audited release changes without conflating reference and model results."""
from pathlib import Path
from collections import Counter
import json,subprocess,hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'deliverables/brick-atlas-dataset-v1';BASE='fc22e3c8da2a60412fcf0e0936cdf07abd854c4a'
def read(p):return json.loads(p.read_text())
def rows(p):return list(map(json.loads,p.read_text().splitlines()))
check=read(OUT/'checks/release-check.json');assert check['passed']
legacy=read(OUT/'checks/legacy-replay.json');assert legacy['publishedSubsetPassed']
community=read(OUT/'checks/full-replay.json');assert community['passed'] and not community['failed']
current=sum([rows(OUT/'questions'/f'{mode}.jsonl') for mode in ['static','dynamic']],[])
old=sum([[json.loads(l) for l in subprocess.check_output(['git','show',BASE+':deliverables/brick-atlas-dataset-v1/questions/'+mode+'.jsonl'],cwd=ROOT,text=True).splitlines()] for mode in ['static','dynamic']],[])
reasons={x['id']:x for x in legacy['failures']};removed=[reasons[q['id']] for q in old if q['id'] not in {r['id'] for r in current}]
assert len(current)==len(old)-len(removed) and len(current)==check['questions']
tests=read(OUT/'checks/unit-tests.json');browser=read(OUT/'checks/browser-check.json');assert browser['passed'] and browser['questions']==len(current)
report=dict(schema='brick-atlas-final-audit/1',date='2026-10-29',baseCommit=BASE,passed=True,previousQuestions=len(old),publishedQuestions=len(current),runnableModels=check['runnableModels'],byMode=dict(Counter(q['mode'] for q in current)),byTaskType=dict(Counter(q['taskType'] for q in current)),freshCommunityQuestions=community['checkedQuestions'],freshLegacyQuestions=len(legacy['questions']),allLegacyWithheld=len(legacy['failures']),newlyWithheld=removed,allWithheldReasons=dict(Counter(x['reason'] for x in legacy['failures'])),imagesChecked=check['imagesChecked'],alternativeLegalOrders=check['communityModelsWithAnotherVerifiedLegalOrder'],arenaScriptedRuns=check['arenaScriptedRuns'],unitTests=tests,browser=browser,apiCalls=0,modelApiCostUSD=0,humanValidated=False,independentPhysicsValidated=False,modelPerformanceMeasured=False)
(OUT/'checks/final-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
body=f'''# 最终 case 检查报告

更新：2026-10-29。对照上版提交 `{BASE[:8]}`，本次重新执行参考动作，未使用旧回放缓存；没有调用付费模型。

## 最终正式数量

| 项目 | 数量 |
|---|---:|
| 模型 | {check['runnableModels']} |
| 静态题 | {report['byMode']['static']} |
| 动态题 | {report['byMode']['dynamic']} |
| 合计 | {len(current)} |
| 原生图片检查 | {check['imagesChecked']} |

**上版 4,692 题，本次退回 7 题，正式保留 4,685 题；310 个模型全部保留。** 退回题没有删除，只移出正式题单，保留原因供后续修改。

## 查出了什么、怎么处理

1. **6 道“提前封口”没有形成已验证的错误。** 它们虽然发生了状态变化，但只是提前装了正确内容，没有验证出新增错误或有效阻挡。不能把这种情况当成修复题，也不能把未修复算成模型失败。这 6 道退回。
2. **1 道公交车内部错件，三个默认视角都看不到差异。** 当前图与目标图导出的像素一致，题目可读性无法通过。该题退回，等有合理观察方式且真人认可后再恢复。
3. **旧回放缓存不够严格。** 新增强制全量检查开关；既有物件缓存现在绑定实际题目、物理证书和当前代码，不能仅因为旧图片还在就跳过新的判断。
4. **论文和入口用了旧统计、旧输入规则。** 当前首页、题单、Arena 目录、论文与图示统一到正式索引。历史版本另设入口。

## 这 7 道题

| 题目 ID | 原因 |
|---|---|
'''
for r in removed:body+=f"| `{r['id']}` | {'三个默认视角的当前／目标完全相同' if 'invisible' in r['reason'] else '未验证出有效错误或阻挡'} |\n"
body+=f'''
## 本次确实检查了哪些

- 新社区 {community['checkedModels']} 个模型、{community['checkedQuestions']} 题：源文件零件／颜色／位置完整性、正常拼装、修复参考、事件数量、最终验收。
- 既有 47 个模型：{len(legacy['questions'])} 题通过；全部 {len(legacy['failures'])} 道退回题单独记录，包括之前已退回的 24 道。
- {check['communityModelsWithAnotherVerifiedLegalOrder']} 个社区模型找到另一条合法顺序并完成；剩余模型没找到相邻交换，不代表只能有一种顺序。
- {check['imagesChecked']} 张图片：存在性、可解码、当前／目标画布一致、S0 无变化、所有发布 S1 至少一个默认视角有变化。
- 6 个实际 Arena 工具回放：牛、卡车收尾、较长建筑收尾，各自正常和事故分支；检查主动观察、JSON、图片引用、动作反馈、事件、正常通过后的修复率和最终结果。
- 16 项指标与接口回归通过；包括正确中途阶段直接结束、正常分支失败、未触发、多次事故、技术失败、临时拆装和等价零件。
- 页面检查通过：题量、逐题链接、六道牛静态题不串图、三个角度、GT、历史状态过滤及退回题不再进入正式列表。

这些是程序和页面检查。**不能说每题都已被真人认可，也不能说真实机器人一定可以拆装。** 实际模型能力仍需要正式实验；本次费用 $0。

## 完整复查顺序

以下在仓库根目录运行，前一步完成后再运行下一步：

```bash
export PYTHONPATH=benchmark/brickplan-repair
benchmark/.runtime/mlx-env/bin/python -m scaling_release.check --force
benchmark/.runtime/mlx-env/bin/python -m scaling_release.legacy_check --force
benchmark/.runtime/mlx-env/bin/python -m scaling_release.export
benchmark/.runtime/mlx-env/bin/python -m scaling_release.publish_sources
benchmark/.runtime/mlx-env/bin/python -m dynamic_arena.catalogue
benchmark/.runtime/mlx-env/bin/python -m scaling_release.docs
benchmark/.runtime/mlx-env/bin/python -m scaling_release.count_history
benchmark/.runtime/mlx-env/bin/python -m scaling_release.arena_check
benchmark/.runtime/mlx-env/bin/python -m unittest scaling_release.test_contract bench_design.test_metrics
benchmark/.runtime/mlx-env/bin/python -m scaling_release.release_check
node scripts/final-case-browser-check.mjs
benchmark/.runtime/mlx-env/bin/python scripts/finalize-brick-audit.py
npm run paper:build
```

程序回放不是 API 模型成绩。原始证据见 [最终汇总](checks/final-audit.json)、[发布检查](checks/release-check.json)、[社区全量回放](checks/full-replay.json)、[既有题逐题回放](checks/legacy-replay.json) 和 [页面检查](checks/browser-check.json)。
'''
(OUT/'FINAL-CHECK.zh-CN.md').write_text(body);print(json.dumps({k:v for k,v in report.items() if k not in ['newlyWithheld','unitTests','browser']},ensure_ascii=False))
