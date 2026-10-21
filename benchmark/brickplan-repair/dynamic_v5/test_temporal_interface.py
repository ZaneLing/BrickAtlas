"""Meaningful contract checks for the paired-image dynamic interface."""
import hashlib
import io
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parent/'eval'))
from dynamic_v5.episode import BANK, DynamicEpisode, load_case
from dynamic_v5.vision import DynamicVisionRenderer
from vision import images, temporal_pair, temporal_target


def png_hash(image):
    stream = io.BytesIO()
    image.save(stream, format='PNG')
    return hashlib.sha256(stream.getvalue()).hexdigest()


def case_run(case_id, directory):
    cert, case = load_case(case_id)
    ep = DynamicEpisode(cert, case)
    renderer = DynamicVisionRenderer(ep.cert, ep.runtime)
    renderer.catalog_in_context = True
    witness = json.loads((BANK/'models'/case['modelId']/'evidence.json').read_text())['buildWitness']
    first = images(ep, renderer, directory, views=('isometric','top'))
    assert [r['role'] for r in first] == ['current','target','current','target','inventory']
    previous = None
    for i, action in enumerate(witness[:3]):
        actor, key = action['partId'], action['candidate']
        if i == 0:
            options = sorted(ep.case['choices'][actor], key=ep.pose)
            index = options.index(key)
            page, within = divmod(index, 12)
            row, col = divmod(within, 4)
            count = len(options[page*12:(page+1)*12])
            rows = (count+3)//4
            public = dict(type='attach', partId=ep.alias[actor], catalogPage=page+1,
                          catalogPoint=[(col+.5)/4,(row+.5)/rows])
            assert ep.catalog_click_candidate(public) == key
        else:
            public = dict(type='attach',partId=ep.alias[actor],candidate=ep.pose(key))
        previous = ep.assignments()
        assert ep.step(public)['code'] == 'OK'
    records = images(ep,renderer,directory,views=('isometric','top'),previous_state=previous)
    assert [r['role'] for r in records] == ['before-last-action','current','target',
                                           'before-last-action','current','target','inventory']
    assert 'privateEvent' not in json.dumps(ep.observe())
    paired=images(ep,renderer,Path(directory)/'paired',views=('isometric','top'),
                  previous_state=previous,paired_layout=True)
    assert [r['role'] for r in paired]==['temporal-pair','target','temporal-pair','target','inventory']
    for view in ('isometric','top'):
        assert next(r['sha256'] for r in paired if r['role']=='temporal-pair' and r['view']==view)==\
               png_hash(temporal_pair(renderer,previous,ep.assignments(),view))
        assert next(r['sha256'] for r in paired if r['role']=='target' and r['view']==view)==\
               png_hash(temporal_target(renderer,ep.runtime.goal,view))
    for view in ('isometric','top'):
        before = next(r for r in records if r['role']=='before-last-action' and r['view']==view)
        assert before['sha256'] == png_hash(renderer.rgb(previous,view)[0])
        current = next(r for r in records if r['role']=='current' and r['view']==view)
        assert current['sha256'] == png_hash(renderer.rgb(ep.assignments(),view)[0])
    expected=images(ep,renderer,Path(directory)/'expected',views=('isometric','top'),
                    previous_state=previous,paired_layout=True,
                    expected_state=ep.expected_after_last_action)
    for view in ('isometric','top'):
        assert next(r['sha256'] for r in expected if r['role']=='temporal-pair' and r['view']==view)==\
               png_hash(temporal_pair(renderer,ep.expected_after_last_action,ep.assignments(),view,
                                     left_label='EXPECTED AFTER YOUR ACTION'))
    assert ep.catalog_click_candidate({'partId':[],'catalogPage':1,'catalogPoint':[.1,.1]}) is None
    actor = ep.alias[witness[0]['partId']]
    assert ep.step(dict(type='inspect',partId=actor))['code']=='OBSERVED'
    inspected=images(ep,renderer,directory,extra=dict(partId=actor),views=('isometric','top'),previous_state=ep.assignments())
    roles=[r['role'] for r in inspected]
    assert 'current-inspection' in roles and 'candidate-catalog' in roles
    assert 'target-inspection' not in roles
    return ep, records, expected


def main():
    with tempfile.TemporaryDirectory() as directory:
        control, control_images, control_expected = case_run('obj-city-car--t3--control',Path(directory)/'control')
        event, event_images, event_expected = case_run('obj-city-car--t3--extra_layer',Path(directory)/'event')
        assert event.event and not control.event
        assert control.observe() == event.observe()
        for role in ('before-last-action','target'):
            for view in ('isometric','top'):
                a=next(r['sha256'] for r in control_images if r['role']==role and r['view']==view)
                b=next(r['sha256'] for r in event_images if r['role']==role and r['view']==view)
                assert a==b,(role,view)
        assert any(next(r['sha256'] for r in control_images if r['role']=='current' and r['view']==view) !=
                   next(r['sha256'] for r in event_images if r['role']=='current' and r['view']==view)
                   for view in ('isometric','top'))
        assert all(next(r['sha256'] for r in control_expected if r['role']=='temporal-pair' and r['view']==view) !=
                   next(r['sha256'] for r in event_expected if r['role']=='temporal-pair' and r['view']==view)
                   for view in ('isometric','top'))
        print('temporal interface contract: PASS')


if __name__=='__main__': main()
