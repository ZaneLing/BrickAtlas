"""Build an attributed, hash-checked runtime package for all admitted tasks."""
from pathlib import Path
import gzip,hashlib,json,shutil,tarfile,zipfile,argparse
from reliability import ROOT,OUT

DATA=ROOT/'deliverables/brick-atlas-dataset-v1'
def read(p):return json.loads(gzip.decompress(p.read_bytes()) if p.suffix=='.gz' else p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def certificates(models):
 for m in models:
  choices=[DATA/'private'/m['setNumber']/'certificate.private.json.gz',ROOT/'deliverables/brickplan-expansion-v7/models'/m['id']/'certificate.private.json.gz',ROOT/'deliverables/brickplan-dynamic-v6/models'/m['id']/'qualification.json']
  yield next(p for p in choices if p.exists())
def collect_names(x,names):
 if isinstance(x,dict):
  if isinstance(x.get('canonical'),str):names.add(x['canonical'])
  for v in x.values():collect_names(v,names)
 elif isinstance(x,list):
  for v in x:collect_names(v,names)

def meshes(models):
 names={'3024'};certs=list(certificates(models))
 for p in certs:collect_names(read(p),names)
 dest=ROOT/'assets-source/benchmark-runtime';dest.mkdir(exist_ok=True)
 lib=ROOT/'assets-source/ldraw-library/locked/parts';source=ROOT/'benchmark/.runtime/bricknet-data/inset'
 rows=[]
 with tarfile.open(dest/'inset.tar.gz','w:gz') as tar:
  for name in sorted(names):
   p=source/(name+'.ply');assert p.is_file(),name
   header=lib/(name+'.dat')
   if not header.exists():
    with zipfile.ZipFile(ROOT/'assets-source/ldraw-library/complete.zip') as z:content=z.read('ldraw/parts/'+name+'.dat')
    header=dest/'source-parts'/(name+'.dat');header.parent.mkdir(exist_ok=True);header.write_bytes(content)
   text=header.read_text(errors='replace');license_lines=[l for l in text.splitlines() if l.startswith('0 !LICENSE')]
   assert license_lines,(name,'No source license declaration')
   info=tar.gettarinfo(str(p),arcname='inset/'+p.name);info.mtime=0;info.uid=info.gid=0;info.uname=info.gname=''
   with p.open('rb') as f:tar.addfile(info,f)
   rows.append(dict(part=name,meshSha256=sha(p),sourcePart=str(header.relative_to(ROOT)),sourcePartSha256=sha(header),
       authors=[l for l in text.splitlines() if l.startswith('0 Author:')],license=license_lines,
       attribution='LDraw part authors; inset conversion: BrickNet (Peter Kulits and Cordelia Schmid); see upstream DATA.md',
       localPatch='assets-source/qualified-collision/3003pe2.json' if name=='3003pe2' else None))
 manifest=dict(schema='brick-atlas-runtime-meshes/1',parts=rows,count=len(rows),archiveSha256=sha(dest/'inset.tar.gz'),
   upstream='https://github.com/kulits/BrickNet/blob/master/DATA.md',pinnedPackage='bricknet==0.1.0',
   scope='LDraw-derived collision geometry; original per-part licenses apply. Not covered by repository MIT code license.',
   certificates={str(p.relative_to(ROOT)):sha(p) for p in certs})
 write(dest/'manifest.json',manifest)
 (dest/'README.md').write_text('# Runtime collision subset\n\nThe archive contains only the collision meshes referenced by the 310 admitted objects and their registered candidates. Mesh hashes, LDraw authors, source headers and per-part licenses are in `manifest.json`.\n\nCredit: original LDraw authors; BrickNet inset conversion by Peter Kulits and Cordelia Schmid. Original license texts are in `assets-source/license/CAreadme.txt`, `CAlicense.txt`, and `CAlicense4.txt`. Repository MIT applies to code only. No fonts are redistributed. The source-backed 3003pe2 repair is identified separately.\n\nInstall and verify with `python -m reliability.bootstrap`. No live upstream mesh server is required.\n')
 return manifest

def rights(models):
 sources=[json.loads(l) for l in (DATA/'sources.jsonl').read_text().splitlines()];rows=[]
 originals={}
 needed={s['sourceHash'] for s in sources if not s.get('sourceFile')}
 for p in sorted([*(ROOT/'assets-source').rglob('*.mpd'),*(ROOT/'benchmark/ldraw-v1/sources').glob('*.mpd')]):
  h=sha(p)
  if h in needed:originals[h]=p
 for s in sources:
  p=ROOT/s['sourceFile'] if s.get('sourceFile') else originals[s['sourceHash']]
  assert sha(p)==s['sourceHash'],('Source hash mismatch',s['id'])
  content=p.read_text(errors='replace');decl=[l for l in content.splitlines() if l.startswith('0 !LICENSE')]
  author=[l for l in content.splitlines() if l.startswith('0 Author:')]
  rows.append(dict(id=s['id'],setNumber=s['setNumber'],sourceFile=str(p.relative_to(ROOT)),sha256=sha(p),
      sourceUrl=s['sourceUrl'],author=s.get('author'),declaredAuthors=author,metadataLicense=s.get('license'),declaredLicenses=sorted(set(decl)),
      status='source-header-recorded' if decl and author else 'metadata-only-needs-review',
      redistributionRule='Preserve authors, source URL, license, and modification notice; no blanket MIT claim.'))
 write(OUT/'release/source-rights.json',dict(schema='brick-atlas-attribution-audit/1',sources=rows,
     acquiredSources=len(rows),admittedCommunityObjects=sum(not m.get('legacy') for m in models),
     retainedDesignedObjects=sum(bool(m.get('legacy')) for m in models),
     policySource='https://library.ldraw.org/documentation/licenses-and-legal/ldraworg-contributor-agreement',
     codeLicense='MIT; application code only',blanketDatasetLicense=None,automatedHeaderAuditNotLegalCertification=True))

def bundle(models):
 files=set()
 def add(path):
  if path.is_file():files.add(path)
  elif path.is_dir():files.update(p for p in path.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix not in ('.so','.pyc') and p.name!='work.lock')
 for name in ['LICENSE','benchmark/brickplan-repair','benchmark/brickplan-v1','assets-source/ldraw-library/locked',
              'assets-source/license','assets-source/qualified-collision','assets-source/benchmark-runtime']:
  add(ROOT/name)
 for name in ['release.json','models.jsonl','sources.jsonl','questions']:add(DATA/name)
 for m,p in zip(models,certificates(models)):
  if m['id'].startswith('sc-'):
   for name in ('metadata.json','certificate.private.json.gz','manual.private.json.gz','cases.private.json.gz','check.json'):add(p.parent/name)
   add(ROOT/read(p)['source']['original'])
  elif p.name.endswith('.gz'):
   for name in ('certificate.private.json.gz','manual.private.json.gz','cases.private.json.gz'):add(p.parent/name)
  else:
   for name in ('qualification.json','cases.json'):add(p.parent/name)
 for name in ['deliverables/brickplan-quality-round/gt-reference-revisions.private.json.gz',
    'deliverables/brickplan-dynamic-arena/source-curation.json','deliverables/brickplan-quality-round/source-expansion/index.json',
    'deliverables/brick-atlas-reliability-v1/review/tasks.private.json','deliverables/brick-atlas-reliability-v1/review/geometry.private.json',
    'deliverables/brick-atlas-reliability-v1/release/source-rights.json','deliverables/brick-atlas-reliability-v1/README.zh-CN.md',
    'deliverables/brick-atlas-reliability-v1/RUN.zh-CN.md',
    'deliverables/brick-atlas-reliability-v1/INPUT-AND-PAIRED-PROTOCOL.zh-CN.md']:
  add(ROOT/name)
 # The package is evaluator-side: private cases/witnesses are not model input.
 question_count=sum(len(p.read_text().splitlines()) for p in (DATA/'questions').glob('*.jsonl'))
 manifest=dict(schema='brick-atlas-runtime-package/1',objects=len(models),questions=question_count,apiKeysIncluded=False,
    scope='Evaluator runtime and all admitted tasks; excludes old web previews, provider logs, fonts and local virtual environments.',
    files={str(p.relative_to(ROOT)):sha(p) for p in sorted(files)})
 write(OUT/'release/package-manifest.json',manifest)
 archive=OUT/'release/brick-atlas-runtime.zip'
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
  for p in sorted(files):z.write(p,str(p.relative_to(ROOT)))
  z.write(OUT/'release/package-manifest.json','package-manifest.json')
 write(OUT/'release/package-summary.json',dict(objects=len(models),questions=question_count,files=len(files),bytes=archive.stat().st_size,sha256=sha(archive)))
 print('Runtime archive:',len(files),'files',round(archive.stat().st_size/1024**2,1),'MiB')

def main():
 p=argparse.ArgumentParser();p.add_argument('--bundle-only',action='store_true');args=p.parse_args()
 models=[json.loads(l) for l in (DATA/'models.jsonl').read_text().splitlines()]
 if not args.bundle_only:meshes(models);rights(models)
 bundle(models)

if __name__=='__main__':main()
