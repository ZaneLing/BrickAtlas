"""Admit independently sourced static models into the dynamic bank.

The selection is fixed before model evaluation. Every admitted event is
replayed from an empty plate through recovery before changing the bank index.
"""
from collections import Counter
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent))
from dynamic_v5 import VERSION
from dynamic_v5.build import OUT, build_one, write
from dynamic_v5.episode import DynamicEpisode

SOURCE = ROOT / 'deliverables/brickplan-static-held4/library/models'
MODEL_IDS = (
    '10001', '10213', '31027-kart', '31028-sailboat',
    'omr-10269', 'omr-21309', 'v23-10158', 'v23-10233',
    'v23-1632', 'v23-1854', 'v23-21006', 'v23-21303',
    'v23-30023', 'v23-30025', 'v23-31039', 'v23-3223',
    'v23-4018', 'v23-6753',
)


def verify(cert, case, witness):
    ep = DynamicEpisode(cert, case)
    for action in witness:
        public = dict(type='attach', partId=ep.alias[action['partId']],
                      candidate=ep.pose(action['candidate']))
        assert ep.step(public) == {'code': 'OK'}, case['id']
        if ep.event:
            break
    if case['kind'] != 'none':
        assert ep.event and ep.event['kind'] == case['kind'], case['id']
        suffix = case['privateEvent']['recoveryWitness']
    else:
        assert not ep.event, case['id']
        suffix = witness[ep.manipulations:]
    for action in suffix:
        public = dict(type=action['type'], partId=ep.alias[action['partId']])
        if 'candidate' in action:
            public['candidate'] = ep.pose(action['candidate'])
        assert ep.step(public) == {'code': 'OK'}, (case['id'], action)
    assert ep.step({'type': 'finish'}) == {'code': 'SUCCESS'}, case['id']


def main():
    # Do not re-run source selection based on any model's performance.
    existing = json.loads((OUT / 'cases.private.json').read_text())
    original = [c for c in existing['cases'] if c['modelId'] not in MODEL_IDS]
    extension, decisions = [], []
    for model_id in MODEL_IDS:
        source_path = SOURCE / model_id / 'qualification.json'
        try:
            cases, evidence = build_one(source_path)
            if cases:
                cert = json.loads((OUT / 'models' / model_id / 'qualification.json').read_text())
                for case in cases:
                    verify(cert, case, evidence['buildWitness'])
                extension.extend(cases)
            decisions.append(dict(modelId=model_id, admittedCases=len(cases),
                                  reason=evidence.get('excluded'),
                                  sourceFamily=evidence.get('sourceFamily')))
        except Exception as exc:
            decisions.append(dict(modelId=model_id, admittedCases=0,
                                  reason=f'{type(exc).__name__}: {exc}'))
        print(model_id, decisions[-1], flush=True)
    assert extension, 'No source models qualified; original bank remains intact'
    combined = original + extension
    assert len({c['id'] for c in combined}) == len(combined)
    index = json.loads((OUT / 'index.json').read_text())
    audits = [a for a in index['modelAudits'] if a['modelId'] not in MODEL_IDS]
    audits += [json.loads((OUT / 'models' / d['modelId'] / 'evidence.json').read_text())
               for d in decisions if d['admittedCases']]
    write(OUT / 'cases.private.json', dict(schema=VERSION, cases=combined))
    write(OUT / 'index.json', dict(schema=VERSION,
          cases=[{k: v for k, v in c.items() if k != 'privateEvent'} for c in combined],
          modelAudits=audits, counts=dict(Counter(c['kind'] for c in combined))))
    write(OUT / 'source-extension.json', dict(schema='brickplan-dynamic-source-extension/1',
          selection=list(MODEL_IDS), decisions=decisions,
          admittedModels=sum(bool(d['admittedCases']) for d in decisions),
          admittedCases=len(extension), counts=dict(Counter(c['kind'] for c in extension)),
          note='Original source-derived rigid-part subsets; not complete commercial kits.'))
    print('extension', len(extension), 'combined', len(combined), flush=True)


if __name__ == '__main__':
    main()
