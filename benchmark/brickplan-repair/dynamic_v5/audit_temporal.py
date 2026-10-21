"""Audit what the agent can actually compare around each scheduled intervention.

This is a machine image gate, not a claim that a person or VLM recognized it.
The normal build witness and event transaction were certified by audit.py.
"""
from collections import Counter
from pathlib import Path
import json
import sys
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parent / 'eval'))
from dynamic_v5.episode import BANK, DynamicEpisode, load_case
from dynamic_v5.vision import DynamicVisionRenderer


def changed(a, b):
    return int(np.count_nonzero(np.max(np.abs(a.astype(np.int16)-b.astype(np.int16)), axis=2) >= 24))


def main():
    cases = json.loads((BANK/'cases.private.json').read_text())['cases']
    prior = {r['caseId']:r for r in json.loads((BANK/'visual-audit.json').read_text())['rows']}
    models = {}
    rows = []
    for case in cases:
        model = case['modelId']
        if model not in models:
            cert, _ = load_case(case['id'])
            ep = DynamicEpisode(cert, case)
            renderer = DynamicVisionRenderer(ep.cert, ep.runtime)
            witness = json.loads((BANK/'models'/model/'evidence.json').read_text())['buildWitness']
            models[model] = (renderer, witness, {})
        renderer, witness, cache = models[model]
        trigger = case['trigger']
        before = {a['partId']:a['candidate'] for a in witness[:trigger-1]}
        expected = {a['partId']:a['candidate'] for a in witness[:trigger]}
        actual = dict(expected)
        for action in case.get('privateEvent', {}).get('transaction', []):
            if action['type'] == 'detach':
                actual.pop(action['partId'], None)
            else:
                actual[action['partId']] = action['candidate']
        if trigger not in cache:
            cache[trigger] = {
                'before':np.asarray(renderer.rgb(before, 'isometric', size=(800,600), supersample=1)[0]),
                'expected':np.asarray(renderer.rgb(expected, 'isometric', size=(800,600), supersample=1)[0]),
            }
        pre, normal = cache[trigger]['before'], cache[trigger]['expected']
        observed = normal if case['kind'] == 'none' else np.asarray(renderer.rgb(actual, 'isometric', size=(800,600), supersample=1)[0])
        pair_delta = changed(pre, observed)
        event_delta = changed(normal, observed)
        assert event_delta == prior[case['id']]['changedPixels']['isometric'], case['id']
        cancelled = case['kind'] != 'none' and actual == before
        category = ('control' if case['kind'] == 'none' else
                    'last-action-cancelled' if cancelled else
                    'pair-below-pixel-gate' if pair_delta < 128 else
                    'low-event-contrast' if event_delta < 2000 else
                    'candidate-for-human-validation')
        rows.append(dict(caseId=case['id'],kind=case['kind'],modelId=model,
                         pairChangedPixels=pair_delta,eventChangedPixels=event_delta,
                         sameStateAsBeforeLastAction=actual == before,
                         primaryCandidate=category == 'candidate-for-human-validation',
                         category=category))
        print(case['id'],category,pair_delta,event_delta,flush=True)
    report = dict(schema='brickplan-dynamic-temporal-interface-audit/1',
                  interface='source scenes for visual-v9/v10, monitor-v3/v4, and monitor-v5; panels use the same 800x600 renders',resolution=[800,600],view='isometric',
                  rgbThreshold=24,minimumChangedPixels=128,
                  lowContrastBelowPixels=2000,
                  scope='Machine visibility and last-action timing only. Human usability and semantic detection remain unverified.',
                  total=len(rows),counts=dict(Counter(r['category'] for r in rows)),rows=rows)
    (BANK/'temporal-interface-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report['counts'],ensure_ascii=False))


if __name__ == '__main__': main()
