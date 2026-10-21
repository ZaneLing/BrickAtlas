"""Publish the archived 2,541 cases with one explicit, executable protocol.

The old exact costs remain in the immutable source bank, but are not exported as
scores for connector-workbench/4. This command makes no external API calls.
"""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import shutil
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from static_bench import TYPES, TAXONOMY, digest as source_digest
from static_v4.certify import digest

ROOT = HERE.parents[1]
SOURCE = ROOT / 'deliverables/brickplan-repair-library'
AUDIT = ROOT / 'deliverables/brickplan-plate-audit-2026-10-16/held4'
OUT = ROOT / 'deliverables/brickplan-static-held4'
PROTOCOL = 'connector-workbench/4'


def read(path): return json.loads(path.read_text())


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main():
    source_hash = hashlib.sha256((SOURCE / 'cases.jsonl').read_bytes()).hexdigest()
    audit = read(AUDIT / 'summary.json')
    assert audit['bankSha256'] == source_hash
    assert audit['protocol'] == PROTOCOL and audit['passed'] == audit['cases'] == 2541
    assert audit['failed'] == 0
    audit_rows = {r['caseId']: r for r in (json.loads(line) for line in (AUDIT / 'rows.jsonl').read_text().splitlines())}
    source_index = read(SOURCE / 'index.json')
    cases, models, public, manifest = [], [], [], []
    for model in source_index['models']:
        model_id = model['modelId']
        old_folder = SOURCE / 'models' / model_id
        folder = OUT / 'library/models' / model_id
        folder.mkdir(parents=True, exist_ok=True)
        cert = read(old_folder / 'qualification.json')
        assert source_digest({k: v for k, v in cert.items() if k != 'contentSha256'}) == cert['contentSha256']
        shutil.copyfile(old_folder / 'qualification.json', folder / 'qualification.json')
        old_cases = read(old_folder / 'cases.json')
        new_cases = {}
        for old in old_cases.values():
            assert audit_rows[old['id']]['status'] == 'PASS'
            changed = {a for a in old['actors'] if old['initial'][a] != old['goal'][a]}
            covered = [a for root in old['roots'] for a in root['affectedActors']]
            assert len(covered) == len(set(covered)) and set(covered) == changed
            assert old['kind'] in TYPES and old['benchmarkMode'] == 'static'
            assert old['environmentChanges'] is False
            c = deepcopy(old)
            public_id = f'S{len(cases) + 1:05d}'
            # These values were exact only for the older Domain planner; the
            # held-subassembly action engine has a larger transition relation.
            for key in ('expectedOptimum', 'difficulty', 'repairEvidence', 'tags',
                        'description', 'observation', 'counterfactuals'):
                c.pop(key, None)
            c.update(schema='brickplan-static-repair-case/held4',
                     publicId=public_id,
                     manipulationProtocol=PROTOCOL,
                     category=c['kind'],
                     title=('无故障对照' if c['kind'] == 'control' else
                            ' + '.join(dict.fromkeys(TYPES[r['type']] for r in c['roots']))),
                     description='观察固定初态和目标，然后修复。',
                     expectedOptimum=None, difficulty='未标定', tags=[],
                     referenceCost=len(c['oraclePlan']), referenceIsOptimal=False,
                     observation=dict(protocol='visual-rgb-v3',
                                      visualEligibility='pending-held4-render-review'),
                     referenceValidation=dict(status='DIRECT_REPLAY_PASS',
                         protocol=PROTOCOL, sourceBankSha256=source_hash,
                         qualificationSha256=cert['contentSha256'],
                         sha256=digest(dict(caseId=c['id'], initial=c['initial'],
                                            goal=c['goal'], plan=c['oraclePlan'],
                                            source=cert['contentSha256']))))
            new_cases[c['id']] = c
            cases.append(c)
            public.append(dict(publicId=public_id, modelId=model_id,
                               observationProtocol='visual-rgb-v3',
                               manipulationProtocol=PROTOCOL,
                               environmentChanges=False))
            manifest.append(dict(caseId=c['id'], modelId=model_id,
                                 publicId=public_id,
                                 status='DIRECT_REPLAY_PASS',
                                 witnessActions=len(c['oraclePlan']),
                                 referenceSha256=c['referenceValidation']['sha256']))
        dump(folder / 'cases.json', new_cases)
        m = deepcopy(model)
        m.update(caseCount=len(new_cases), kinds=dict(Counter(c['kind'] for c in new_cases.values())),
                 difficulty={'未标定': len(new_cases)}, manipulationProtocol=PROTOCOL,
                 witnessStatus='DIRECT_REPLAY_PASS')
        for key in ('coverage', 'attempts', 'staticCuration'):
            m.pop(key, None)
        dump(folder / 'record.json', m)
        models.append(m)
    assert len(cases) == 2541 and len({c['id'] for c in cases}) == 2541
    bank = OUT / 'library'
    (bank / 'cases.jsonl').write_text(''.join(json.dumps(c, ensure_ascii=False) + '\n' for c in cases))
    (bank / 'questions.jsonl').write_text(''.join(json.dumps(c, ensure_ascii=False) + '\n' for c in public))
    dump(bank / 'index.json', dict(schema='brickplan-static-repair-library/held4',
         modelCount=len(models), caseCount=len(cases), benchmarkMode='static',
         manipulationProtocol=PROTOCOL, observationProtocol='visual-rgb-v3',
         models=models, taxonomy=[dict(id=k, label=label, kinds=kinds) for k, label, kinds in TAXONOMY], kinds=TYPES,
         difficulty={'未标定': len(cases)},
         sourceBankSha256=source_hash))
    families = sorted({c['sourceExample'] for c in cases},
                      key=lambda name: hashlib.sha256(('brickplan-held4-split-214:' + name).encode()).hexdigest())
    family_splits = dict(train=families[:85], dev=families[85:103], test=families[103:])
    assert len(families) == 123 and len(family_splits['test']) == 20
    dump(OUT / 'splits.json', dict(schema='source-family-split/1', seed=214,
         rule='Group every case from one original source model, including --deep variants, in one split.',
         splits={name: dict(sourceModels=group,
                            publicIds=[c['publicId'] for c in cases if c['sourceExample'] in group],
                            cases=sum(c['sourceExample'] in group for c in cases),
                            kinds=dict(Counter(c['kind'] for c in cases if c['sourceExample'] in group)))
                 for name, group in family_splits.items()}))
    (OUT / 'normalization.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in manifest))
    dump(OUT / 'verification.json', dict(schema='brickplan-static-normalization/1',
         sourceBankSha256=source_hash,
         normalizedBankSha256=hashlib.sha256((bank/'cases.jsonl').read_bytes()).hexdigest(),
         models=len(models), cases=len(cases), replayedActions=audit['actionsReplayed'],
         directReplayPass=2541, exactOptimumClaimCount=0,
         visualEvidenceStatus='pending-held4-render-review'))
    print('NORMALIZED', len(models), len(cases), audit['actionsReplayed'])


if __name__ == '__main__': main()
