"""Combine two fully replayed /4 banks without duplicating source geometry."""
from collections import Counter
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'deliverables/brickplan-static-held4'
BASE = OUT / 'library'
EXTRA = OUT / 'expansion/library'
COMBINED = OUT / 'combined'


def read(path): return json.loads(path.read_text())


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def rows(path): return [json.loads(line) for line in path.read_text().splitlines()]


def main():
    sources = [(BASE, OUT / 'replay-audit/summary.json', '../library'),
               (EXTRA, OUT / 'expansion/replay-audit/summary.json', '../expansion/library')]
    models, cases, public = [], [], []
    audit_records = []
    for bank, report_path, relative in sources:
        report = read(report_path)
        case_bytes = (bank / 'cases.jsonl').read_bytes()
        assert report['bankSha256'] == hashlib.sha256(case_bytes).hexdigest()
        assert report['protocol'] == 'connector-workbench/4'
        assert report['passed'] == report['cases'] and report['failed'] == 0
        index = read(bank / 'index.json')
        model_rows = rows(bank / 'cases.jsonl')
        assert len(model_rows) == report['cases'] == index['caseCount']
        models.extend(index['models'])
        for case in model_rows:
            c = dict(case, qualificationFile=f'{relative}/models/{case["modelId"]}/qualification.json')
            cases.append(c)
            public.append(dict(publicId=c['publicId'], modelId=c['modelId'],
                               observationProtocol='visual-rgb-v3',
                               manipulationProtocol='connector-workbench/4',
                               environmentChanges=False))
        audit_records.append(dict(bank=str(bank.relative_to(ROOT)), sha256=report['bankSha256'],
                                  models=index['modelCount'], cases=report['cases'],
                                  actionsReplayed=report['actionsReplayed']))
    assert len({m['modelId'] for m in models}) == len(models) == 160
    assert len({c['id'] for c in cases}) == len({c['publicId'] for c in cases}) == len(cases) == 3292
    assert len({c['sourceExample'] for c in cases}) == 123
    occupied = {}
    for model in read(BASE / 'index.json')['models']:
        source_id = model['modelId'].split('--deep')[0]
        occupied.setdefault(source_id, set()).update(model['sourceIndices'])
    for model in read(EXTRA / 'index.json')['models']:
        assert not occupied[model['sourceModelId']].intersection(model['sourceIndices'])
    assert all((COMBINED / c['qualificationFile']).exists() for c in cases)
    assert all(c['expectedOptimum'] is None and c['referenceIsOptimal'] is False for c in cases)
    COMBINED.mkdir(parents=True, exist_ok=True)
    (COMBINED / 'cases.jsonl').write_text(''.join(json.dumps(c, ensure_ascii=False) + '\n' for c in cases))
    (COMBINED / 'questions.jsonl').write_text(''.join(json.dumps(c, ensure_ascii=False) + '\n' for c in public))
    base_index = read(BASE / 'index.json')
    dump(COMBINED / 'index.json', dict(schema='brickplan-static-repair-library/held4-combined',
         benchmarkMode='static', manipulationProtocol='connector-workbench/4',
         observationProtocol='visual-rgb-v3', modelCount=len(models),
         independentSourceModels=123, caseCount=len(cases), models=models,
         kinds=base_index['kinds'], taxonomy=base_index['taxonomy'],
         kindCounts=dict(Counter(c['kind'] for c in cases)),
         difficulty={'未标定': len(cases)}))
    old_splits = read(OUT / 'splits.json')['splits']
    split_of = {family: name for name, detail in old_splits.items()
                for family in detail['sourceModels']}
    assert len(split_of) == 123
    dump(COMBINED / 'splits.json', dict(schema='source-family-split/1', seed=214,
         rule='All configurations of an original source model stay in one split.',
         splits={name: dict(sourceModels=detail['sourceModels'],
                            publicIds=[c['publicId'] for c in cases if split_of[c['sourceExample']] == name],
                            cases=sum(split_of[c['sourceExample']] == name for c in cases),
                            kinds=dict(Counter(c['kind'] for c in cases
                                               if split_of[c['sourceExample']] == name)))
                 for name, detail in old_splits.items()}))
    dump(COMBINED / 'verification.json', dict(schema='brickplan-held4-combined-validation/1',
         bankSha256=hashlib.sha256((COMBINED/'cases.jsonl').read_bytes()).hexdigest(),
         modelConfigurations=len(models), independentSourceModels=123,
         cases=len(cases), directlyReplayedActions=sum(a['actionsReplayed'] for a in audit_records),
         allReferencePathsLegal=True, exactOptimumClaims=0,
         visualEvidenceStatus='pending-held4-render-review', componentAudits=audit_records))
    print('COMBINED', len(models), len(cases), sum(a['actionsReplayed'] for a in audit_records))


if __name__ == '__main__': main()
