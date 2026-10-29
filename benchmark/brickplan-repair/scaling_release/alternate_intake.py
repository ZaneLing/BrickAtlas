"""Distinct authored alternate objects, with source-set grouping retained."""
from concurrent.futures import ThreadPoolExecutor
import re
from dynamic_arena.source_library import Document,DEST,acquire
from dynamic_arena.curate_sources import FigureAudit,category
from scaling_release import ROOT,OUT
from expansion_v7.build import read,write


def main():
 rows=read(OUT/'source-pool.json')['models'];candidates=[]
 for row in rows:
  if '-alt-' in row['setNumber']:continue
  path=DEST/row['setNumber']/'page.html'
  if not path.exists():continue
  doc=Document(path.read_bytes()).root;names=set();opts=[]
  for a in doc.all('a'):
   url=a.attrs.get('href','')
   if '/media/omr_models/' not in url or not re.search(r'\.(mpd|ldr)(\?|$)',url,re.I):continue
   node=a.parent
   while node.parent and not all(k in node.text() for k in ['Author:','Missing Parts','Missing Patterns','Missing Stickers']):node=node.parent
   label=node.text();name=label.split('Author:')[0].strip()
   if not re.search(r'Missing Parts\s+No',label) or name.lower()=='main model' or name in names or re.search(r'combin',name,re.I) or url==row.get('downloadUrl'):continue
   names.add(name);ident=re.search(r'/omr_models/(\d+)/',url).group(1)
   opts.append(dict(setNumber=row['setNumber']+'-alt-'+ident,sourceSetNumber=row['setNumber'],title=row['title']+' — '+name,theme=row.get('theme',''),sourceUrl=row['sourceUrl'],selectedModelUrl=url,cachedPage=str(path.relative_to(ROOT)),maxSourceParts=1500))
  # Different authored objects may share a Creator set. Limit repeated named
  # vehicle variants within that set (e.g. Experienced Build Car 1/2/3).
  kinds=set();chosen=[]
  for option in opts:
   caption=option['title'].split(' — ')[-1].lower()
   kind=re.sub(r'\b(?:advanced|experienced|quick)\s+build\s*','',caption)
   kind=re.sub(r'\s+\d+$','',kind).strip()
   if kind in kinds:continue
   kinds.add(kind);chosen.append(option)
  candidates.extend(chosen[:8])
 audit=FigureAudit();out=dict(models=[],rejected=[],countUnit='distinct complete authored objects; alternate models grouped by original source set',apiCalls=0)
 hashes={r.get('shapeHash') for r in rows}
 with ThreadPoolExecutor(max_workers=6) as ex:
  for source,r in zip(candidates,ex.map(acquire,candidates)):
   if 'rejected' in r:out['rejected'].append(r);continue
   evidence=audit.audit(r)
   if evidence['status']!='no-figure-parts-found' or r['shapeHash'] in hashes:
    out['rejected'].append(dict(setNumber=r['setNumber'],reason='figure, unresolved dependency or duplicate',figureAudit=evidence));continue
   hashes.add(r['shapeHash']);r.update(sourceSetNumber=source['sourceSetNumber'],officialAlternate=True,figureAudit=evidence,objectCategory=category(r),addedForScaling=True)
   out['models'].append(r);print('ALTERNATE',len(out['models']),r['setNumber'],r['title'],flush=True)
   write(OUT/'alternate-pool.json',out)
 write(OUT/'alternate-pool.json',out)

if __name__=='__main__':main()
