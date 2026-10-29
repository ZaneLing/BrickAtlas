"""Update the local source browser only from the audited source registry."""
from collections import Counter
import json
from scaling_release import ROOT,OUT
from expansion_v7.build import read,write
from dynamic_arena import OUT as ARENA
from dynamic_arena.curate_sources import category
from scaling_release.export import display_title

def main():
 checks={r['setNumber']:r for r in read(OUT/'checks/source-audit.json')['sources']}
 models={r['setNumber']:r for r in map(json.loads,(OUT/'models.jsonl').read_text().splitlines()) if not r.get('legacy')}
 sources=list(map(json.loads,(OUT/'sources.jsonl').read_text().splitlines()));rows=[]
 baseline={r['setNumber'] for r in read(ARENA/'source-library-before-curation.json')['models']}
 for r in sources:
  a=checks[r['setNumber']]
  if a['status']!='source-audited':continue
  r.update(sourceFile=a['sourceFile'],sourceHash=a['sha256'],author=a['author'],license=a['license'],parts=a['instances'],figureAudit=a['figureAudit'],objectCategory=category(r),title=display_title(r),addedAfterFigureCuration=r['setNumber'] not in baseline)
  m=models.get(r['setNumber']);r['arenaTaskCount']=m['dynamicCases'] if m else 0;r['moduleTaskCount']=m['dynamicCases'] if m and m['scope']['kind']!='complete-object' else 0
  r['qualification']='normal-and-repair-machine-checked' if m else 'engine-withheld';r['qualificationReason']='通过原文件、正常拼装、修复与图像检查；真人待确认。' if m else r.get('reason','尚无通过检查的任务。')
  if m:r['datasetModel']=m['id'];r['datasetPreview']='deliverables/brick-atlas-dataset-v1/'+m['preview']
  rows.append(r)
 old=read(ARENA/'source-library.json');old.update(models=rows,count=len(rows),distinctSourceSets=len({r['sourceGroup'] for r in rows}),countUnit='distinct complete authored objects; alternate objects share their original source set',qualifiedCommunityModels=len(models),note='Source objects and runnable models are separate counts. Figures are excluded from whole source inventories. Released questions are listed in deliverables/brick-atlas-dataset-v1; held sources contribute zero questions.')
 write(ARENA/'source-library.json',old)
 cur=read(ARENA/'source-curation.json')
 reactivated=[r for r in cur['withdrawn'] if r['setNumber'] in models and r.get('withdrawalReason','').startswith('尚无可核对的完整预览') and (OUT/models[r['setNumber']]['preview']).exists()]
 cur['withdrawn']=[r for r in cur['withdrawn'] if r not in reactivated]
 cur.setdefault('reactivatedAfterSourceAndTaskAudit',[]).extend(dict(setNumber=r['setNumber'],previousReason=r['withdrawalReason'],reason='完整原模型预览、无小人检查及题目回放现已通过。') for r in reactivated)
 cur.update(activeCount=len(rows),byCategory=dict(Counter(r['objectCategory'] for r in rows)),latestSourceAudit='deliverables/brick-atlas-dataset-v1/checks/source-audit.json',latestRelease='deliverables/brick-atlas-dataset-v1/release.json');write(ARENA/'source-curation.json',cur)
 print('Published sources',len(rows),'qualified community objects',len(models))

if __name__=='__main__':main()
