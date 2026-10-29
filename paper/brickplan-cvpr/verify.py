"""Verify release-backed manuscript, figure lineage, unmeasured tables and PDFs.

No model API calls. Reference replay is never model or independent human evidence.
"""
from pathlib import Path
from collections import Counter
import hashlib,json,re
import fitz
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];DATA=ROOT/'deliverables/brick-atlas-dataset-v1'
def read(p):return json.loads(p.read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dependencies(files):
 for p,h in files.items():assert digest(ROOT/p)==h,('Stale dependency',p)
def main():
 snapshot=read(HERE/'evidence/release-dataset.json');dependencies(snapshot['files'])
 release=read(DATA/'release.json');check=read(DATA/'checks/release-check.json')
 models=[json.loads(l) for l in (DATA/'models.jsonl').read_text().splitlines()]
 questions=[json.loads(l) for mode in ['static','dynamic'] for l in (DATA/'questions'/f'{mode}.jsonl').read_text().splitlines()]
 assert check['passed'] and check['questions']==snapshot['questions']==len(questions)
 assert len(models)==snapshot['models']==release['counts']['runnableModels']==310
 assert Counter(q['taskType'] for q in questions)==snapshot['taskTypes']
 assert sum(q['mode']=='static' for q in questions)==release['counts']['staticQuestions']
 assert sum(q['mode']=='dynamic' for q in questions)==release['counts']['dynamicQuestions']
 assert snapshot['allAuthoringExposed'] and not release['humanValidated'] and not release['independentPhysicsValidated']
 legacy=read(DATA/'checks/legacy-replay.json');assert legacy['publishedSubsetPassed']
 assert set(q['id'] for q in questions if q.get('legacy'))=={q['id'] for q in legacy['questions']}
 scenes=read(HERE/'evidence/release-render-states.json');ids={q['id'] for q in questions}
 assert scenes['apiCalls']==0 and scenes['publicationOnly'] and scenes['evaluationInputUnchanged']
 for s in scenes['scenes']:
  assert s['caseId'] in ids,('Non-current figure case',s['caseId'])
  assert digest_state(s['state'])==s['stateSha256']
 prov=read(HERE/'figures-release/provenance.json');dependencies(prov['sources']);assert prov['typography']['family']=='Comic Sans MS'
 for name,x in prov['images'].items():
  p=HERE/name if name.startswith('figures-release/') else ROOT/name
  assert digest(p)==x['sha256'] and list(Image.open(p).size)==x['pixels'],name
  if name.startswith('figures-release/native/'):
   assert x['pixels']==[3200,2400]
   assert read(p.with_suffix('.png.json'))['sha256']==x['sha256']
 for name,x in prov['figures'].items():assert digest(HERE/'figures-release'/f'{name}.pdf')==x['pdfSha256']
 results=read(HERE/'evidence/release-results-template.json');plan=read(HERE/'evidence/release-experiment-plan.json')
 assert results['status']=='NOT_RUN' and results['apiCalls']==0 and results['repetitions']==1
 assert len(results['tables'])==19 and len(results['models'])==10
 assert plan['finalEvaluationIds'] is None and plan['allSourcesAuthoringExposed']
 for name,table in results['tables'].items():
  assert (HERE/'tables'/f'{name}.tex').is_file()
  assert all(v is None for row in table['rows'] for v in row['results'].values())
 for name,h in read(HERE/'template-provenance.json')['files'].items():assert digest(HERE/name)==h
 texpaths=[HERE/'main.tex',HERE/'supplement.tex',*sorted((HERE/'tables').glob('*.tex'))]
 tex='\n'.join(p.read_text() for p in texpaths)
 referenced=set(re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}',tex))
 fonts={}
 for name in referenced:
  assert name.startswith('figures-release/'),('Historical figure referenced',name)
  d=fitz.open(HERE/name);names=set()
  for page in d:
   for font in page.get_fonts(full=True):
    assert 'ComicSansMS' in font[3],(name,font[3]);assert d.extract_font(font[0])[3];names.add(font[3])
  assert names;fonts[name]=sorted(names)
 pdfs={}
 for name in ['main','supplement']:
  p=HERE/'build'/f'{name}.pdf';d=fitz.open(p);log=(HERE/'build'/f'{name}.log').read_text(errors='replace')
  assert not re.search(r'(Citation|Reference) .*undefined|Overfull \\[hv]box',log),(name,'Unresolved reference or overflow')
  text='\n'.join(page.get_text() for page in d);normalized=re.sub(r'\s+',' ',text)
  expected_total='Total '+str(len(models))+' '+' '.join(f'{snapshot["taskTypes"][t]:,}' for t in ['S0','S1','D0','D1','D2'])+' '+f'{len(questions):,}'
  assert expected_total in normalized,(name,'Dataset table total disagrees with release',expected_total)
  for value in [snapshot['questions'],release['counts']['staticQuestions'],release['counts']['dynamicQuestions']]:assert f'{value:,}' in text,(name,value)
  assert not re.search(r'\b(?:TODO|TBD|PLACEHOLDER)\b',text)
  assert 'BrickPlan' not in text and '5,452' not in text
  for m in results['models']:assert m['name'] in normalized,(name,m['name'])
  if name=='main':
   reference=[i+1 for i,page in enumerate(d) if page.get_text().lstrip().startswith('References') or re.search(r'\nReferences\n',page.get_text())]
   assert reference and reference[0]<=9,('More than eight body pages',reference,len(d))
  ppis=[];fontids=set()
  for page in d:
   assert abs(page.rect.width-612)<.1 and abs(page.rect.height-792)<.1
   for im in page.get_image_info():
    x0,y0,x1,y1=im['bbox'];ppis.append(min(im['width']*72/max(x1-x0,.001),im['height']*72/max(y1-y0,.001)))
   for font in page.get_fonts(full=True):
    if font[0] not in fontids:assert d.extract_font(font[0])[3];fontids.add(font[0])
  assert min(ppis)>=599,(name,'Embedded scene below 600 ppi',min(ppis))
  pdfs[name]=dict(pages=len(d),sha256=digest(p),minimumEmbeddedImagePpi=round(min(ppis)),embeddedFonts=len(fontids))
 out=dict(schema='brick-atlas-paper-verification/5',date='2026-10-29',status='PASS',pdfs=pdfs,questions=len(questions),models=len(models),taskTypes=snapshot['taskTypes'],figures=len(referenced),nativeScenes=len(scenes['scenes']),figureFontAudit=fonts,plannedModels=10,unmeasuredResultTables=19,apiCalls=0,formalModelStudyComplete=False,humanQualificationComplete=False,independentPhysicsValidated=False)
 (HERE/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='figureFontAudit'},indent=2))
def digest_state(state):return hashlib.sha256(json.dumps(state,sort_keys=True).encode()).hexdigest()
if __name__=='__main__':main()
