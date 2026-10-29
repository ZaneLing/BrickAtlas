"""Integrity gate for the published subset, retaining rejected-candidate evidence."""
from collections import Counter,defaultdict
import hashlib,json,re
from pathlib import Path
from PIL import Image
from scaling_release import ROOT,OUT
from scaling_release.check import verified
from expansion_v7.build import read,write

def main():
 models=[json.loads(s) for s in (OUT/'models.jsonl').read_text().splitlines()]
 qs=[json.loads(s) for mode in ('dynamic','static') for s in (OUT/'questions'/f'{mode}.jsonl').read_text().splitlines()]
 assert len(models)==len({m['id'] for m in models})>=300
 assert len(qs)==len({q['id'] for q in qs})
 previous=OUT/'checks/count-correction/before/questions'
 if previous.exists():
  prior=[json.loads(s) for mode in ('dynamic','static') for s in (previous/f'{mode}.jsonl').read_text().splitlines()]
  current={q['id']:q for q in qs}
  withheld={r['id'] for p in (OUT/'legacy/checks').glob('*.json') for r in read(p).get('withheld',[])}
  assert {q['id'] for q in prior}<=set(current)|withheld,'Previously published questions were lost without an audit reason'
  for q in prior:
   if q.get('physicalTaskSha256') and q['id'] in current:assert current[q['id']]['physicalTaskSha256']==q['physicalTaskSha256']
 gt=json.loads((OUT/'review-gt.private.js').read_text().removeprefix('window.REVIEW_GT=').strip().removesuffix(';'))
 assert set(gt)=={q['id'] for q in qs}
 images=set();groups=defaultdict(set);alternate_orders=0
 for m in models:
  rows=[q for q in qs if q['model']==m['id']]
  assert sum(q['taskType']=='D0' for q in rows)==1
  assert sum(q['mode']=='dynamic' for q in rows)==m['dynamicCases']
  assert sum(q['mode']=='static' for q in rows)==m['staticCases']
  groups[m['sourceGroup']].add(m['split'])
  if not m.get('legacy'):
   folder=OUT/'private'/m['setNumber'];assert verified(folder)
   audit=read(folder/'check.json');caseids={c['id'] for c in read(folder/'cases.private.json.gz')}
   assert caseids=={q['id'] for q in rows}
   assert 2<=m['staticCases']<=6 and all(r['success'] for r in audit['cases'])
   alternate_orders+=bool(audit.get('alternateLegalOrder'))
   stamp=hashlib.sha256((folder/'certificate.private.json.gz').read_bytes()+(folder/'cases.private.json.gz').read_bytes()+Path(__file__).with_name('previews.py').read_bytes()).hexdigest()
   assert read(OUT/'previews'/m['setNumber']/'complete.json')['inputSha256']==stamp
  else:
   audit=read(OUT/'legacy/checks'/f'{m["id"]}.json')
   assert audit.get('publishedSubsetPassed',audit['passed']) and all(q['success'] for q in audit['questions'])
   assert {q['id'] for q in audit['questions']}=={q['id'] for q in rows}
  base=(OUT/m['preview']).parent;images.add(base/'overview.png')
  for q in rows:
   assert q['machineChecked'] and not q['humanValidated'] and not q['modelEvaluated']
   assert gt[q['id']]['legalWitnessOnly']
   roles=['static-current','static-target'] if q['mode']=='static' else ['initial','target']
   image_base=OUT/q['imageBase'] if q.get('imageBase') else base
   differences=[]
   for view in ('isometric','rear','top'):
    pair=[image_base/f'{role}-{view}.png' for role in roles];images.update(pair)
    assert Image.open(pair[0]).size==Image.open(pair[1]).size
    differences.append(pair[0].read_bytes()!=pair[1].read_bytes())
    if q['taskType']=='S0':assert pair[0].read_bytes()==pair[1].read_bytes()
   if q['taskType']=='S1':assert any(differences),(q['id'],'Static error invisible in all three exported views')
   if q['mode']=='dynamic':
    event_base=OUT/q['eventImageBase'] if q.get('eventImageBase') else base
    for i in range(q['scheduledEvents']):
     for role in ('before','after'):images.add(event_base/f'{q["assetFamily"]}-event-{i+1}-{role}.png')
 assert all(len(v)==1 for v in groups.values())
 for p in images:
  assert p.is_file(),p
  with Image.open(p) as im:im.verify()
 catalogue=read(ROOT/'deliverables/brickplan-dynamic-arena/catalogue.json')
 assert {r['caseId'] for r in catalogue['cases']}=={q['id'] for q in qs if q['mode']=='dynamic'}
 assert catalogue['models']==len(models)
 source=read(OUT/'checks/source-audit.json');assert source['byStatus']=={'source-audited':437}
 assert not read(OUT/'checks/source-duplicates.json')['duplicates']
 arena=read(OUT/'checks/arena-replays.json');assert arena['passed'] and len(arena['runs'])==6
 assets=set()
 for run in arena['runs']:
  directory=ROOT/'deliverables/brickplan-dynamic-arena/runs'/run['runId']
  log=read(directory/'log.json');spectator=read(directory/'spectator.json')
  assert log['result']['success'] and '非 API 模型' in spectator['model']
  for call in log['calls']:
   payload=json.dumps(call['modelInput'])
   for hidden in ('referenceActions','referenceEvents','recoveryActions','eventsApplied','triggerAfter'):
    assert hidden not in payload,(run['runId'],hidden)
  for asset in re.findall(r'/assets/([a-f0-9]{64}\.png)',json.dumps([log,spectator])):
   path=ROOT/'deliverables/brickplan-dynamic-arena/assets'/asset;assert path.exists();assets.add(str(path.relative_to(ROOT)))
 write(OUT/'checks/replay-assets.json',sorted(assets))
 out=dict(passed=True,scope='published questions only',runnableModels=len(models),questions=len(qs),byMode=dict(Counter(q['mode'] for q in qs)),imagesChecked=len(images),sourceAudited=source['checked'],sourceGroupSplitOverlap=False,exactStructureDuplicateGroups=0,communityModelsWithAnotherVerifiedLegalOrder=alternate_orders,arenaScriptedRuns=6,apiCalls=0,modelApiCostUSD=0,candidateAudit='full-replay.json',withheldCandidate='10220-1: raw-source color mismatch; excluded from all release counts',humanValidated=False,independentPhysicsValidated=False,modelPerformanceMeasured=False)
 write(OUT/'checks/release-check.json',out);print(json.dumps(out,ensure_ascii=False))

if __name__=='__main__':main()
