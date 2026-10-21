"""Verify manuscript evidence, source hashes, layout, fonts, and image resolution.

This checks recorded geometry audits. protocol_study.py separately executes the
route diagnostics. Neither script calls a learned model or certifies acceptance.
"""
from collections import Counter
from pathlib import Path
import hashlib
import json
import re
import fitz
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def read(path):
    return json.loads(path.read_text())


def rows(path):
    return [json.loads(x) for x in path.read_text().splitlines() if x]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_sources(sources):
    for name, expected in sources.items():
        assert digest(ROOT / name) == expected, f'Stale source: {name}'


def main():
    check_sources(read(HERE/'evidence/data-snapshot.json')['files'])
    static = ROOT / 'deliverables/brickplan-static-plate5'
    summary, audit = read(static/'summary.json'), read(static/'replay-audit.json')
    cases, questions = rows(static/'cases.jsonl'), rows(static/'questions.jsonl')
    assert len(cases) == len(questions) == 3292
    assert audit['total'] == audit['passed'] == 3292 and audit['failed'] == 0
    assert (summary['sourceCasesPreserved'], summary['sourceCasesReplaced']) == (3025,267)
    assert digest(static/'cases.jsonl') == summary['certifiedBankSha256']
    assert digest(static/'questions.jsonl') == summary['questionBankSha256']
    assert len({x['publicId'] for x in cases}) == 3292
    assert Counter(x['migrationMethod'] for x in cases) == summary['methods']
    assert sum(not x['oraclePlan'] for x in cases) == 160

    dyn = ROOT / 'deliverables/brickplan-dynamic-v6'
    release = read(dyn/'release-check.json')
    assert (release['cases'],release['controls'],release['interventions']) == (1872,160,1712)
    assert (release['structures'],release['completeObjectModels']) == (68,42)
    assert release['geometryPassed'] == release['privilegedResetSuccess'] == 1872
    assert release['blindControlSuccess'] == 160 and release['blindInterventionSuccess'] == 0
    assert release['humanValidatedCases'] == release['paidModelRuns'] == 0
    assert digest(dyn/'cases.private.json') == release['bankSha256']
    assert read(dyn/'verification.json')['status'] == 'PASS'

    comm = ROOT / 'deliverables/brickplan-community-modules'
    ca, modules = read(comm/'audit.json'), read(comm/'gallery-data.js.json')
    assert ca['status'] == ca['orderRegressionStatus'] == 'PASS'
    assert (ca['modules'],ca['cases'],ca['differingPhysicalPrefixes']) == (12,96,9)
    assert sum(m['remaining'] for m in modules) == 99
    assert sum(m['total'] for m in modules) == 2135
    assert ca['apiModelCalls'] == ca['humanValidationCount'] == 0
    assert read(comm/'interface-checks.json')['status'] == 'PASS'
    check_sources(read(comm/'source-manifest.json'))

    study = read(HERE/'evidence/protocol-study.json')
    check_sources(study['sources'])
    assert study['trials'] == len(study['rows']) == 96 and study['apiCalls'] == 0
    for route, exact, sequential in [('reference',36,12),('alternative',9,0)]:
        s = study['conditions'][route]
        assert (s['models'],s['faultTrials'],s['exactPrefixTriggers']) == (12,36,exact)
        assert (s['actualStateTriggers'],s['sequentialNormalAccepted']) == (36,sequential)
        assert s['terminalNormalAccepted'] == s['blindControlCompleted'] == 12
        assert s['blindFaultCompleted'] == 0 and s['privilegedCompleted'] == 48

    figs = HERE/'figures-v2'
    provenance = read(figs/'provenance.json')
    check_sources(provenance['sources'])
    assert provenance['renderPixels'] == [3200,2400] and provenance['supersampling'] == 2
    assert provenance['exportDpi'] == 600 and provenance['vectorText']
    assert len(provenance['figures']) == 8 and len(provenance['renders']) == 44
    for name, spec in provenance['renders'].items():
        p = figs/name
        assert digest(p) == spec['sha256'], name
        assert Image.open(p).size == (3200,2400), name
    for name, spec in provenance['figures'].items():
        assert digest(figs/(name+'.pdf')) == spec['pdfSha256'], name
        for ext in spec['formats']:
            assert (figs/(name+'.'+ext)).exists(), name
        assert Image.open(figs/(name+'.png')).size[0] == 4200, name

    style = read(HERE/'template-provenance.json')
    for name, expected in style['files'].items():
        assert digest(HERE/name) == expected, f'Official style changed: {name}'

    pdfs = {}
    for name in ['main','supplement']:
        path = HERE/'build'/f'{name}.pdf'
        document = fitz.open(path)
        log = (HERE/'build'/f'{name}.log').read_text(errors='replace')
        assert not re.search(r'(Citation|Reference) .*undefined|Overfull \\[hv]box',log), name
        text = '\n'.join(p.get_text() for p in document)
        assert not re.search(r'\b(?:TODO|TBD|PLACEHOLDER)\b',text), name
        assert '3,292' in text and '1,872' in text and '9/36' in text, name
        ppis, fonts = [], set()
        for page in document:
            assert abs(page.rect.width-612) < .1 and abs(page.rect.height-792) < .1
            for im in page.get_image_info():
                x0,y0,x1,y1 = im['bbox']
                ppis.append(min(im['width']*72/(x1-x0),im['height']*72/(y1-y0)))
            for font in page.get_fonts(full=True):
                xref = font[0]
                if xref not in fonts:
                    assert document.extract_font(xref)[3], f'Unembedded font: {font[3]}'
                    fonts.add(xref)
        assert min(ppis) >= 599, (name,min(ppis))
        if name == 'main':
            ref_page = next(i+1 for i,p in enumerate(document) if 'References' in p.get_text())
            assert ref_page == 9, f'Expected 8 content pages; references begin at {ref_page}'
            assert len(document) == 9
        pdfs[name] = dict(pages=len(document),sha256=digest(path),
                          minimumEmbeddedImagePpi=round(min(ppis)),embeddedFonts=len(fonts))
    result = dict(schema='brickplan-paper-verification/3',status='PASS',
                  snapshotDate='2026-10-21',mainBodyPages=8,pdfs=pdfs,
                  staticRecordedReplays=3292,dynamicRecordedReplays=1872,
                  communityCases=96,protocolStudyTrials=96,protocolStudyApiCalls=0,
                  nativeSceneRenders=44,nativeScenePixels=[3200,2400],figureCount=8,
                  figureExportDpi=600,sourceHashesVerified=True,
                  formalAgentStudyComplete=False,independentHumanAssemblyStudyComplete=False,
                  scope='Evidence/layout consistency; not a CVPR acceptance or visual-validity certificate.')
    (HERE/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
