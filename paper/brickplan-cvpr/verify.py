"""Verify the current paper against organized dataset/metric evidence and PDF layout.

No model API calls. Recorded replay checks are not reinterpreted as human or model
performance. Historical diagnostics are checked only within their original scope.
"""
from pathlib import Path
from collections import Counter
import hashlib,json,re
import fitz
from PIL import Image

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
SPEC=ROOT/'deliverables/brickplan-benchmark-spec'
def read(p):return json.loads(p.read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check_sources(files):
    for name,h in files.items():assert digest(ROOT/name)==h,f'Stale dependency: {name}'

def main():
    snapshot=read(HERE/'evidence/current-dataset.json');check_sources(snapshot['files'])
    check_sources(read(SPEC/'data-manifest.json'))
    check_sources(read(SPEC/'code-manifest.json'))
    rows=[json.loads(l) for l in (SPEC/'questions.jsonl').read_text().splitlines()]
    unique=[r for r in rows if not r['isAlias']];candidate=[r for r in unique if r['mainTaskCandidate']]
    dynamic=[r for r in candidate if r['mode']=='dynamic'];summary=read(SPEC/'summary.json')
    assert len(rows)==5839 and len(unique)==5720 and len(candidate)==5452
    assert len(dynamic)==1755 and len(candidate)-len(dynamic)==3697
    assert Counter(r['bank'] for r in unique)==summary['perBank']
    assert Counter(r['track'] for r in unique)==summary['perTrack']
    assert Counter(r['taskType'] for r in candidate)==dict(S0=260,S1=3437,D0=63,D1=1649,D2=43)
    assert Counter(r['planningLevel'] for r in candidate)==dict(G1=2577,G2=2823,G3=52)
    assert Counter(r['sourceSplit'] for r in unique)==summary['splitCounts']
    assert len({r['model'] for r in dynamic})==63
    assert len({r['model'] for r in dynamic if r['track']=='whole-object-dynamic'})==50
    assert len({r['model'] for r in dynamic if r['track']=='named-module-dynamic'})==13
    assert sum(r['eventLevel']=='T2' for r in dynamic)==37 and sum(r['eventLevel']=='T3' for r in dynamic)==6
    src={}
    for row in unique:src.setdefault(row['source'],set()).add(row['sourceSplit'])
    assert len(src)==154 and all(len(v)==1 for v in src.values())
    assert sum(next(iter(v))=='development-public' for v in src.values())==45
    assert sum(r['sourceSplit']=='test-existing-source' for r in candidate)==392
    audit=read(SPEC/'physical-audit.json')
    assert audit['status']=='PASS' and audit['executionConditionsPassed']==5922 and not audit['failures']
    assert audit['paidApiCalls']==0 and not audit['humanCaseReview']
    assert audit['perBank']==dict(S=3292,D=1712,M=96,E7=776,O=46)
    release=read(SPEC/'release-check.json')
    assert release['inputVersion']=='brick-atlas-direct-actions-full-context/1'
    assert not release['humanPerCaseQualification'] and release['physicalFailures']==0
    assert read(SPEC/'classification-audit.json')['falseStaticErrors']==[]
    visibility=read(SPEC/'new-object-visibility.json')
    assert visibility['cases']==46
    assert Counter(r['status'] for r in visibility['rows'])=={'machine-visible':36,'control':10}

    # Data-derived coverage, compared to the explicit numbers printed in both PDFs.
    coverage=[]
    for code in ['E01','E02','E03','E04','E05','E06','E07']:
        coverage.append(tuple(sum(code in r['errorCodes'] for r in candidate if r['track'] in tracks)
            for tracks in [('static-structure-diagnostic','whole-object-static','named-module-static'),('whole-object-dynamic',),('named-module-dynamic',)]))
    assert coverage==[(1361,209,60),(356,167,36),(1458,426,60),(339,185,15),(804,227,32),(489,130,25),(31,20,0)]

    study=read(HERE/'evidence/protocol-study.json');check_sources(study['sources'])
    assert study['trials']==len(study['rows'])==96 and study['apiCalls']==0
    assert study['conditions']['alternative']['exactPrefixTriggers']==9
    assert study['conditions']['alternative']['actualStateTriggers']==36
    qual=read(HERE/'evidence/repair-comparison.json')
    assert qual['status']=='REPLAY_VERIFIED' and qual['apiCallsThisExport']==0
    assert sum(t['decisions'] for t in qual['traces'])==32
    for frame in qual['gt']+[f for t in qual['traces'] for f in t['frames']]:
        assert hashlib.sha256(json.dumps(frame['state'],sort_keys=True,separators=(',',':')).encode()).hexdigest()==frame['stateSha256']

    plan=read(HERE/'evidence/current-experiment-design.json')
    template=read(HERE/'evidence/current-results-template.json')
    roster=read(HERE/'evidence/model-roster.json')
    assert plan['models']==template['models']==roster['models'] and len(roster['models'])==10
    assert plan['repetitions']==template['repetitions']==1 and plan['paidModelCalls']==0
    assert len(template['tables'])==len(plan['resultTables'])==19
    assert template['status']=='NOT_RUN' and plan['unknownFinalEvaluationN']
    assert not plan['independentCheckpointBankImplemented'] and not plan['independentDetectionBankImplemented']
    assert set(x for pool in plan['candidatePools'].values() for x in pool)=={r['id'] for r in candidate}
    assert sum(len(p) for p in plan['assignedExistingSourceTest'].values())==392
    for name,table in template['tables'].items():
        assert (HERE/'tables'/f'{name}.tex').exists()
        # Only these prefilled columns are assignment metadata, never measurements.
        metadata={'Assigned','W assigned','M assigned'}
        for row in table['rows']:
            assert all(value is None for key,value in row['results'].items() if key not in metadata)
    prov=read(HERE/'figures-current/provenance.json');check_sources(prov['sources'])
    assert prov['renderPixels']==[3200,2400] and prov['supersampling']==2 and prov['exportDpi']==600
    assert len(prov['figures'])==9
    for name,r in prov['renders'].items():
        assert digest(HERE/'figures-current'/name)==r['sha256']
        assert Image.open(HERE/'figures-current'/name).size==(3200,2400)
    for name,r in prov['figures'].items():
        assert digest(HERE/'figures-current'/f'{name}.pdf')==r['pdfSha256']
        assert abs(Image.open(HERE/'figures-current'/f'{name}.png').size[0]-600*r['inches'][0])<=1
    assert all(not r['plottedSeries'] and not r['missingImputation'] for r in prov['radars'].values())
    publication=read(HERE/'figures-publication/provenance.json');check_sources(publication['sources'])
    assert publication['nativePixels']==[3200,2400] and publication['exportDpi']==600
    assert publication['exactGeometry'] and publication['publicationOnly'] and publication['evaluationInputUnchanged']
    assert publication['apiCalls']==0 and len(publication['figures'])==14
    for name,r in publication['images'].items():
        p=HERE/'figures-publication/native'/name
        assert digest(p)==r['sha256'] and Image.open(p).size==(3200,2400),name
        assert read(p.with_suffix('.png.json'))['sha256']==r['sha256'],name
    for name,r in publication['figures'].items():
        assert digest(HERE/'figures-publication'/f'{name}.pdf')==r['pdfSha256'],name
    scenes=read(HERE/'evidence/publication-render-states.json')
    assert scenes['evaluationInputUnchanged'] and scenes['publicationOnly'] and scenes['apiCalls']==0
    byname={s['name']:s for s in scenes['scenes']}
    for s in scenes['scenes']:
        assert hashlib.sha256(json.dumps(s['state'],sort_keys=True).encode()).hexdigest()==s['stateSha256']
    for step in [2,6]:
        assert byname[f'roof-referenceOrder-{step}']['state']==byname[f'roof-alternateOrder-{step}']['state']
    assert byname['roof-referenceOrder-3']['state']!=byname['roof-alternateOrder-3']['state']
    worked=read(HERE/'evidence/worked-metric-example.json')
    assert worked['referenceOnly'] and not worked['modelPerformance']
    assert [r['metrics']['finalEditResidual'] for r in worked['states']]==[2,1,0]
    assert [r['metrics']['errorReduction'] for r in worked['states']]==[0,.5,1]
    assert [r['metrics']['success'] for r in worked['states']]==[False,False,True]
    for name,h in read(HERE/'template-provenance.json')['files'].items():assert digest(HERE/name)==h

    # Ensure every referenced old figure remains its recorded native export.
    tex='\n'.join((HERE/n).read_text() for n in ['main.tex','supplement.tex'])
    old=read(HERE/'figures-v2/provenance.json')
    referenced=set(re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}',tex))
    main_tex=(HERE/'main.tex').read_text()
    assert 'evaluation-radar.pdf' not in main_tex and r'\input{tables/main-models}' not in main_tex
    assert r'\input{tables/main-dynamic}' not in main_tex
    for name in referenced:
        p=HERE/name;assert p.exists()
        if p.parent.name=='figures-v2':assert digest(p)==old['figures'][p.stem]['pdfSha256']
    assert r'\"type' not in tex, 'Accented quotes instead of JSON quotes'
    pdfs={}
    for name in ['main','supplement']:
        path=HERE/'build'/f'{name}.pdf';d=fitz.open(path)
        log=(HERE/'build'/f'{name}.log').read_text(errors='replace')
        assert not re.search(r'(Citation|Reference) .*undefined|Overfull \\[hv]box',log),name
        text='\n'.join(p.get_text() for p in d);normalized=re.sub(r'\s+',' ',text)
        assert all(x in text for x in ['5,720','5,452','3,697','1,755','5,922','9/36']),name
        assert not re.search(r'\b(?:TODO|TBD|PLACEHOLDER)\b',text),name
        assert all(m['name'] in normalized for m in roster['models']),name
        if name=='supplement':assert 'A023' in text and 'C00523' in text
        pp=[i+1 for i,p in enumerate(d) if 'References' in p.get_text()]
        if name=='main':assert pp==[9] and len(d)==9, ('Expected 8 body + 1 references',pp,len(d))
        ppis=[];fonts=set()
        for page in d:
            assert abs(page.rect.width-612)<.1 and abs(page.rect.height-792)<.1
            for im in page.get_image_info():
                x0,y0,x1,y1=im['bbox'];ppis.append(min(im['width']*72/(x1-x0),im['height']*72/(y1-y0)))
            for font in page.get_fonts(full=True):
                xref=font[0]
                if xref not in fonts:
                    assert d.extract_font(xref)[3],f'Unembedded font: {font[3]}'
                    fonts.add(xref)
        assert min(ppis)>=599,(name,min(ppis))
        pdfs[name]=dict(pages=len(d),sha256=digest(path),minimumEmbeddedImagePpi=round(min(ppis)),embeddedFonts=len(fonts))
    result=dict(schema='brickplan-paper-verification/4',date='2026-10-25',status='PASS',pdfs=pdfs,
        distinctTaskRecords=5720,mainCandidates=5452,mainStatic=3697,mainDynamic=1755,
        diagnosticDynamic=268,retainedReferenceConditions=5922,recordedReplayFailures=0,
        dynamicConfigurations=63,wholeObjectConfigurations=50,namedModuleConfigurations=13,
        sourceGroups=154,sourceGroupsCrossingSplits=0,mainRepeatedEventTasks=43,
        basicPhysicalErrorLabels=7,plannedResultTables=19,plannedModels=10,plannedRepetitions=1,
        bodyPages=8,figureCount=len(referenced),currentNativeRenders=len(prov['renders']),
        publicationFigures=len(publication['figures']),publicationSceneStates=len(scenes['scenes']),
        nativeModelInputUnchanged=True,emptyResultSheetsInSupplement=True,
        formalModelStudyComplete=False,currentInterfaceHumanQualificationComplete=False,
        paidApiCallsThisRevision=0,scope='Current evidence, hash, layout and output consistency; not human visual validation or an acceptance certificate.')
    (HERE/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
