"""Keep historical records discoverable; never equate their count with revalidated tasks."""
from collections import Counter
import json
from scaling_release import ROOT,OUT
from scaling_release.export import jsonl
from expansion_v7.build import read,write
from bench_design.selection import retired

def main():
 old=[json.loads(s) for s in (ROOT/'deliverables/brickplan-benchmark-spec/questions.jsonl').read_text().splitlines()]
 core=[json.loads(s) for mode in ('dynamic','static') for s in (OUT/'questions'/f'{mode}.jsonl').read_text().splitlines()]
 rejected={r['id']:r for p in (OUT/'legacy/checks').glob('*.json') for r in read(p).get('withheld',[])}
 rows={};aliases=[]
 for r in old:
  key=r.get('canonicalId',r['id'])
  if r.get('isAlias') or key in rows:
   aliases.append(dict(id=r['id'],canonicalId=key));continue
  excluded=retired(r['id'],r['model'],r.get('source'))
  status='retired-source-or-human-selection' if excluded else 'withheld-reference-check' if r['id'] in rejected else 'historical-not-rechecked-in-this-round'
  rows[key]=dict(id=key,model=r['model'],title=r.get('title',r['model']),mode=r['mode'],taskType=r['taskType'],family=r['family'],track=r['track'],status=status,reason=rejected.get(r['id'],{}).get('reason'),sourceRecord='deliverables/brickplan-benchmark-spec/questions.jsonl',core=False)
 old_distinct=len(rows)
 before_ids={json.loads(line)['id'] for mode in ('dynamic','static') for line in (OUT/'checks/count-correction/before/questions'/f'{mode}.jsonl').read_text().splitlines()}
 previous_withheld=sorted(before_ids&set(rejected))
 for r in read(ROOT/'deliverables/brickplan-dynamic-arena/catalogue-all-conditions.json')['cases']:
  if r['caseId'] not in rows:
   rows[r['caseId']]=dict(id=r['caseId'],model=r['model'],title=r.get('title',r['model']),mode='dynamic',taskType=r['taskType'],family=r['family'],track=r['track'],status='historical-not-rechecked-in-this-round',sourceRecord='deliverables/brickplan-dynamic-arena/catalogue-all-conditions.json',core=False)
 pending=ROOT/'deliverables/brickplan-quality-round/current-release/pending-additions.jsonl'
 if pending.exists():
  for line in pending.read_text().splitlines():
   r=json.loads(line)
   if r['id'] not in rows:rows[r['id']]=dict(id=r['id'],model=r['model'],title=r.get('title',r['model']),mode=r['mode'],taskType=r['taskType'],family=r['family'],track=r['track'],status='historical-pending-review',sourceRecord=str(pending.relative_to(ROOT)),core=False)
 for q in core:rows[q['id']]=dict(q,status='current-machine-checked',core=True)
 records=list(rows.values());statuses=dict(Counter(r['status'] for r in records));before=read(OUT/'checks/count-correction/before/release.json')['counts'];release=read(OUT/'release.json')['counts']
 report=dict(oldRawRecords=len(old),oldDistinctCanonicalRecords=old_distinct,oldAliases=len(aliases),previousSubset=dict(dynamic=before['dynamicQuestions'],static=before['staticQuestions']),current=dict(dynamic=release['dynamicQuestions'],static=release['staticQuestions'],total=release['dynamicQuestions']+release['staticQuestions'],models=release['runnableModels']),allRecordDirectory=len(records),recordStatuses=statuses,restoredLegacyCases=sum(q.get('legacy',False) for q in core),withheldAfterCurrentReplay=len(rejected),previouslyPublishedNowWithheld=previous_withheld,apiCalls=0,allRecordCountIsNotValidatedTaskCount=True)
 write(OUT/'checks/count-correction/summary.json',report);jsonl(OUT/'all-questions.jsonl',records)
 (OUT/'all-questions.js').write_text('window.ALL_QUESTIONS='+json.dumps(dict(report=report,questions=records),ensure_ascii=False)+';\n')
 text=f'''# 为什么题量从五千多变成了两千多，以及这次怎么改

## 原因

你记得的数量没错。旧基准的清单有 **{old_distinct:,} 道按 canonical ID 去重的题目**；更早的网页曾展示 5,793 条。它们包含完整物件、指定模块和大量静态局部结构题，版本和去重范围并不完全相同。

上一轮我把新社区模型压成每模型一道静态代表题，并且把旧物件的动态题也只选了几个代表条件。随后把这个 **{before['dynamicQuestions']+before['staticQuestions']:,} 题的精选子集** 当成最终题库交付，没有把范围变化讲清楚。这不是“旧题全坏了”，也不是它们全部被删除了，是选题和交付统计做错了。

## 这次修正后的数量

| 项目 | 上一轮精选子集 | 本次当前可运行题库 |
|---|---:|---:|
| 模型 | {before['runnableModels']} | {release['runnableModels']} |
| 静态题 | {before['staticQuestions']} | {release['staticQuestions']} |
| 动态题 | {before['dynamicQuestions']} | {release['dynamicQuestions']} |
| 合计 | {before['dynamicQuestions']+before['staticQuestions']} | {release['dynamicQuestions']+release['staticQuestions']} |

- 社区静态题按不同错误保留，通常每物件 4–6 道，含正常对照。少数物件没有那么多可行错误，就保留实际通过检查的数量。
- 旧完整物件取消动态题的代表数量限制，重新检查已有的不同阶段和不同干扰条件。每道题有独立的事件图片，避免同名错误的不同题共用错图。
- 当前复查有 {len(rejected)} 道旧题的参考过程或默认视图可见性没有通过，原因逐条保存。其中 {len(previous_withheld)} 道曾进入上一轮精选清单，这次因有效干扰或可见性检查未通过而退回。其余题目没有因数量限制而删掉。这些题不会被算成模型失败，也不冒充已验证的题。
- 完整旧题仍可检索：新增 [全部题目记录页面](all-questions.html) 和 [机器可读清单](all-questions.jsonl)。当前通过、历史待复查、退回和已停用分别标记。

## 两个数字怎么使用

**写当前已检查题库的规模，使用 {release['dynamicQuestions']+release['staticQuestions']:,} 道：静态 {release['staticQuestions']:,}、动态 {release['dynamicQuestions']:,}。** 它们对应 {release['runnableModels']} 个完整物件或明确收尾部分。

完整记录目录共有 {len(records):,} 条，它包含上述题目，也包含旧结构诊断题、其他模块、待复查题和已停用记录。它是查找历史数据的目录，不能把这个数直接写成“全部验证合格”。目录按旧 canonical ID 合并别名；跨版本相同场景仍可能有不同记录，所以它也不声称是完全去重的物理场景总数。

| 完整目录中的状态 | 记录数 |
|---|---:|
'''
 names={'current-machine-checked':'当前程序检查通过','historical-not-rechecked-in-this-round':'历史记录，本轮未重新验证','historical-pending-review':'历史新增候选，待审查','retired-source-or-human-selection':'此前已停用（来源筛选／人工要求）','withheld-reference-check':'本轮参考回放未通过'}
 text+='\n'.join(f'| {names.get(k,k)} | {v} |' for k,v in statuses.items())
 text+='\n\n没有调用付费模型。程序检查成功不等于真人已认可，也不等于 API 模型做对。之前的报告保存在 `checks/count-correction/before/`，不会覆盖成仿佛当时就有这些题。\n'
 (OUT/'COUNT-CHANGES.zh-CN.md').write_text(text);print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':main()
