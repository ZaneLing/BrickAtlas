"""Audit original source inventories; publish provenance and figure evidence."""
from collections import Counter
import hashlib
from scaling_release import ROOT,OUT
from expansion_v7.build import read,write
from dynamic_arena.source_library import flatten
from dynamic_arena.curate_sources import FigureAudit,category

def main():
 audit=FigureAudit();rows=[]
 for r in read(OUT/'source-pool.json')['models']:
  number=r['setNumber'];mfpath=ROOT/r['manifest'];mf=read(mfpath);original=r.get('sourceFile') or mf.get('sourceFile')
  if not original and mfpath.with_name('provenance.json').exists():
   p=read(mfpath.with_name('provenance.json'));original=p.get('source',{}).get('path') or next((x['file'] for x in p.get('resources',[]) if x.get('file','').lower().endswith(('.mpd','.ldr'))),None)
  if not original and (OUT/'private'/number/'certificate.private.json.gz').exists():original=read(OUT/'private'/number/'certificate.private.json.gz')['source']['original']
  try:
   assert original and (ROOT/original).exists(),'Original source path unavailable'
   raw=(ROOT/original).read_bytes();instances,author,license_=flatten(raw)
   path=OUT/'checks/original-manifests'/f'{number}.json';write(path,dict(instances=instances))
   evidence=audit.audit(dict(manifest=str(path.relative_to(ROOT)),sourceFile=original))
   rows.append(dict(setNumber=number,sourceFile=original,sha256=hashlib.sha256(raw).hexdigest(),author=author,license=license_,instances=len(instances),figureAudit=evidence,status='source-audited' if evidence['status']=='no-figure-parts-found' else 'source-withheld'))
  except Exception as e:rows.append(dict(setNumber=number,status='source-withheld',reason=str(e)))
 write(OUT/'checks/source-audit.json',dict(checked=len(rows),byStatus=dict(Counter(r['status'] for r in rows)),sources=rows,apiCalls=0))
 print('SOURCE AUDIT',dict(Counter(r['status'] for r in rows)))

if __name__=='__main__':main()
