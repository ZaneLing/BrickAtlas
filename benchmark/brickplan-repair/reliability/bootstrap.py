"""Verify and install the attributed collision subset. Standard library only."""
from pathlib import Path
import argparse,hashlib,json,tarfile,sys
from reliability import ROOT

def main():
 p=argparse.ArgumentParser();p.add_argument('--data-root',type=Path,default=ROOT/'benchmark/.runtime/brick-atlas-data');args=p.parse_args()
 source=ROOT/'assets-source/benchmark-runtime';manifest=json.loads((source/'manifest.json').read_text())
 archive=source/'inset.tar.gz';assert hashlib.sha256(archive.read_bytes()).hexdigest()==manifest['archiveSha256']
 args.data_root.mkdir(parents=True,exist_ok=True)
 names={r['part']+'.ply':r['meshSha256'] for r in manifest['parts']}
 with tarfile.open(archive,'r:gz') as tar:
  members=tar.getmembers()
  assert len(members)==len(names) and all(m.isfile() and m.name=='inset/'+Path(m.name).name and Path(m.name).name in names for m in members)
  for m in members:
   raw=tar.extractfile(m).read();assert hashlib.sha256(raw).hexdigest()==names[Path(m.name).name]
   dest=args.data_root/m.name;dest.parent.mkdir(exist_ok=True);dest.write_bytes(raw)
 (args.data_root/'verified.json').write_text(json.dumps(dict(parts=len(names),archiveSha256=manifest['archiveSha256'])))
 print(json.dumps(dict(installedParts=len(names),dataRoot=str(args.data_root),noNetwork=True)))

if __name__=='__main__':main()
