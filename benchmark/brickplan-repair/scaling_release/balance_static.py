"""Replace, rather than add, one fifth of static errors with clean controls."""
from copy import deepcopy
import hashlib
from scaling_release import OUT
from expansion_v7.build import read,write,signature_key
from expansion_v7.runtime import Episode,runtime

def main():
 count=0
 for path in (OUT/'private').glob('*/cases.private.json.gz'):
  number=path.parent.name
  if int(hashlib.sha256(number.encode()).hexdigest()[:8],16)%5:continue
  cases=read(path);s=next(c for c in cases if c['mode']=='static')
  if s['family']=='control':continue
  cert=read(path.with_name('certificate.private.json.gz'))
  s.update(id=f'SC:{number}:static:control',family='control',initial=deepcopy(s['goal']),referenceActions=[],referenceIncident=None,visibilityCheck=None,humanErrorIds=[],pairedDynamicId=f'SC:{number}:dynamic:control')
  ep=Episode(cert,s);ep.step(dict(type='finish'));assert ep.score()['success'];s['referenceScore']=ep.score();s['physicalTaskSha256']=signature_key(ep.runtime,s);write(path,cases)
  meta=read(path.with_name('metadata.json'));meta['families']=sorted({c['family'] for c in cases});write(path.with_name('metadata.json'),meta)
  design=read(OUT/'designs'/f'{number}.json');design['cases']=[dict(id=c['id'],mode=c['mode'],family=c['family'],events=len(c['events']),referenceMoves=len(c['referenceActions'])) for c in cases];write(OUT/'designs'/f'{number}.json',design)
  (OUT/'previews'/number/'complete.json').unlink(missing_ok=True);count+=1
 print('Static controls updated:',count)

if __name__=='__main__':main()
