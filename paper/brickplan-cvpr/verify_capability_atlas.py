"""Offline evidence and presentation checks for the six-case capability dossier."""
import base64,gzip,hashlib,json
from collections import Counter
import fitz
from PIL import Image
from release_assets import HERE,ROOT,read,write,sha
from bench_design.session import Session

FIELDS=['before','afterOwnActionBeforeExternalChange','after','feedback','newEventIndices']

def replay(case,records,key):
 s=Session.open(case,HERE/'build/capability-verify'/key,'scripted:evidence-check');s.autosave=False
 for rec in records:
  s.submit(rec['action'])
  for field in FIELDS:assert s.records[-1][field]==rec[field],(key,rec['decision'],field)
 return s

def main():
 manifest=read(HERE/'evidence/capability-atlas.json')
 for field in ['sources','images']:
  for name,h in manifest[field].items():assert sha(ROOT/name)==h,('Stale source',name)
 arena=read(HERE/'evidence/arena-traces.json')
 for name,h in arena['sources'].items():assert sha(ROOT/name)==h,('Stale archived trace',name)
 pilot=read(HERE/'evidence/capability-pilot.json');run=pilot['runs'][0]
 folder=ROOT/'deliverables/brickplan-dynamic-arena/runs'/run['runId']
 record=json.loads(gzip.decompress((folder/'record.private.json.gz').read_bytes()));log=read(folder/'log.json')
 s=replay(run['caseId'],record['records'],'static')
 assert s.ep.state==record['final'] and s.initial==record['initial'] and s.goal==record['goal']
 assert run['status']=='service_error' and run['success'] is None and len(record['records'])==2
 assert record['records'][1]['action']==dict(type='detach',partId='A011')
 assert run['result']['stateMetrics']['initiallyCorrectPlacements']==13
 assert run['result']['stateMetrics']['finalDamageCount']==0
 assert sum(record['initial'][a]!=record['final'][a] for a in record['initial'])==1
 # Verify the bytes in the actual serialized API requests, not only log labels.
 requests={}
 for path in (folder/'api').glob('*.request.json.gz'):
  raw=gzip.decompress(path.read_bytes());payload=json.loads(raw)
  hashes=[hashlib.sha256(base64.b64decode(b['image_url']['url'].split(',',1)[1])).hexdigest()
          for b in payload['messages'][-1]['content'] if b['type']=='image_url']
  requests[hashlib.sha256(raw).hexdigest()]=hashes
 counts=[]
 for c in log['calls']:
  images=c['modelInput']['images'];hashes=[im['sha256'] for im in images]
  for im in images:
   assert sha(ROOT/im['file'])==im['sha256']
   assert list(Image.open(ROOT/im['file']).size)==[im['width'],im['height']]
  if c.get('providerReceipt'):assert requests[c['providerReceipt']['requestBodySha256']]==hashes
  else:assert hashes in requests.values()
  counts.append(dict(decision=c['index'],images=len(images),roles=dict(Counter(im['role'] for im in images))))
 assert [c['images'] for c in counts]==[9,18,12]
 write(HERE/'evidence/capability-static-audit.json',dict(exactRecordedActionReplay=True,exactSerializedRequestImages=True,
    acceptedPhysicalMoves=1,changedPart='A011',correctInitialPlacementsPreserved=13,completedRepair=None,
    technicalStop='API response missing a verifiable charge',imageCounts=counts))
 ref=read(HERE/'evidence/capability-reference-scenes.json')
 for trace in ref['traces']:
  s=replay(trace['caseId'],trace['records'],trace['key'])
  assert s.result()['success'] and s.events==trace['events']
  assert trace['referenceOnly'] and trace['apiCalls']==0 and not trace['referenceOptimal']
 assert [len(t['events']) for t in ref['traces']]==[0,2]
 for scene in ref['scenes']:
  assert hashlib.sha256(json.dumps(scene['state'],sort_keys=True).encode()).hexdigest()==scene['stateSha256']
  p=HERE/'figures-capability/native'/(scene['name']+'.png')
  assert Image.open(p).size==(3200,2400) and read(p.with_suffix('.png.json'))['sha256']==sha(p)
 pdf=HERE/'capability-atlas.pdf';assert sha(pdf)==manifest['pdfSha256']
 doc=fitz.open(pdf);assert len(doc)==3
 output=HERE/'build/capability-pdf-preview';output.mkdir(exist_ok=True)
 fonts=set();resolutions=[]
 for i,page in enumerate(doc):
  for font in page.get_fonts(full=True):
   assert 'ComicSansMS' in font[3] and doc.extract_font(font[0])[3];fonts.add(font[3])
  for block in page.get_text('dict')['blocks']:
   if block['type']==0:
    x0,y0,x1,y1=block['bbox'];assert x0>=0 and y0>=0 and x1<=page.rect.width and y1<=page.rect.height,('Clipped text',i,block)
  for im in page.get_image_info():
   r=fitz.Rect(im['bbox']);resolutions.append(min(im['width']*72/r.width,im['height']*72/r.height))
  page.get_pixmap(matrix=fitz.Matrix(2,2),alpha=False).save(output/f'page-{i+1}.png')
 # Cropped reader close-ups preserve native pixels instead of claiming an
 # artificial resolution increase. Require >=450 ppi at their printed size.
 assert fonts and min(resolutions)>=450
 assert '$0.256830' in doc[1].get_text() and '$0.782538' in doc[1].get_text()
 assert manifest['referenceOnly']==['E','F'] and manifest['scoreIsSubjective']
 assert sum(x['points'] for x in manifest['scorecard'])==manifest['score']==74
 assert pilot['finalLedger']['upperUSD']<=pilot['finalLedger']['capUSD']==3
 report=dict(passed=True,apiCallsByVerifier=0,pages=3,embeddedFonts=sorted(fonts),
   minimumEffectiveImagePPI=round(min(resolutions),2),pdfSha256=sha(pdf),
   sourceHashesVerified=True,staticActionReplay=True,actualRequestImageCounts=[9,18,12],
   referenceReplayPassed=True,referenceScenes=len(ref['scenes']),referenceOnlyCases=['E','F'],
   oldDynamicProtocol='brick-atlas-tool-arena/2',currentStaticOutcome='service_error',
   subjectiveScore=74,newConfirmedUSD=pilot['additionalConfirmedUSD'],newCostUpperUSD=pilot['additionalUpperUSD'])
 write(HERE/'evidence/capability-atlas-verification.json',report)
 print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
