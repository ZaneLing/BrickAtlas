"""Compile both manuscript roots from the portable ZIP in a fresh directory."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,tempfile,zipfile
import fitz
HERE=Path(__file__).resolve().parent
compiler=os.environ.get('TECTONIC') or shutil.which('tectonic') or str(Path.home()/'.local/bin/tectonic')
archive=HERE/'brickplan-cvpr-overleaf.zip';outputs={}
with tempfile.TemporaryDirectory(prefix='brick-atlas-paper-portable-') as tmp:
 root=Path(tmp)
 with zipfile.ZipFile(archive) as z:
  assert all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in z.namelist());z.extractall(root)
 for name in ['main','supplement']:
  result=subprocess.run([compiler,'--keep-logs',name+'.tex'],cwd=root,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
  if result.returncode:raise RuntimeError(result.stdout)
  actual=fitz.open(root/(name+'.pdf'));expected=fitz.open(HERE/(name+'.pdf'))
  assert len(actual)==len(expected)
  assert [p.get_text() for p in actual]==[p.get_text() for p in expected],name
  outputs[name]=dict(pages=len(actual),textMatchesPublished=True)
report=dict(status='PASS',archiveSha256=hashlib.sha256(archive.read_bytes()).hexdigest(),outputs=outputs,isolatedTemporaryDirectory=True,noRepositoryDataRequired=True,apiCalls=0)
(HERE/'evidence/portable-archive-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
