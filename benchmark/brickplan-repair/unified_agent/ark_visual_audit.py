"""Flag final pixel-equivalent but geometry-inequivalent states for review."""
import gzip,json,tempfile,time
from bench_design.session import Session
from dynamic_arena import OUT as ARENA
from dynamic_arena.sensors import Sensors
from dynamic_arena.transport import write_json
from unified_agent.ark_batch import OUT,combined_report

def main():
 path=OUT/'checks/final-visual-audit.json';old=json.loads(path.read_text()) if path.exists() else {'rows':[]}
 rows={r['runId']:r for r in old['rows']}
 for r in combined_report()['runs']:
  if r['arenaRunId'] in rows:continue
  saved=json.loads(gzip.decompress((ARENA/'runs'/r['arenaRunId']/'record.private.json.gz').read_bytes()))
  with tempfile.TemporaryDirectory() as tmp:
   s=Session.open(r['caseId'],tmp,'scripted:final-visual-audit',control=r['arenaBranch']=='normal');se=Sensors(s)
   matches={v:se.render(saved['final'],v).tobytes()==se.render(saved['goal'],v).tobytes() for v in ('isometric','rear','top')}
   row=dict(runId=r['arenaRunId'],model=r['model'],caseId=r['caseId'],viewPixelMatches=matches,
    finalEquivalent=r['stateMetrics']['finalEquivalent'],reviewRequired=all(matches.values()) and not r['stateMetrics']['finalEquivalent'])
   rows[row['runId']]=row
 result=dict(checkedAt=time.time(),rows=list(rows.values()),flagged=sum(r['reviewRequired'] for r in rows.values()),apiCalls=0,
  scope='Three standard views; cannot prove absence of hidden errors or independent physical validity. Pixel equality alone never changes a score.')
 write_json(path,result);print('FINAL VISUAL AUDIT',len(rows),'flagged',result['flagged'])

if __name__=='__main__':main()
