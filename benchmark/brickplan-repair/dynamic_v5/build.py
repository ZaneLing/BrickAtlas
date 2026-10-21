"""Generate paired dynamic cases and replay every hidden event with /5 geometry.

Only events with a legal transaction and a complete recovery witness are admitted.
All candidate poses are fixed before model evaluation; event truth stays private.
"""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import json
import sys
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent))
from baseplate import PlateAssembly, PROTOCOL
from static_v4.certify import digest
from dynamic_v5 import VERSION

SOURCE = ROOT / 'deliverables/brickplan-static-v4/library/models'
OUT = ROOT / 'deliverables/brickplan-dynamic-v5'

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def add_variants(source):
    cert = deepcopy(source)
    # Every target brick gets the same set of small, target-independent slips.
    # Registration is performed once, prior to case selection.
    for key, row in list(cert['candidates'].items()):
        if row['kind'] != 'goal':
            continue
        for axis, amount, label in ((0, 20, 'xplus'), (0, -20, 'xminus'), (2, 20, 'zplus'), (2, -20, 'zminus')):
            part = deepcopy(row['part'])
            for field in ('rawMatrix', 'matrix'):
                part[field][axis][3] += amount
            name = row['actor'] + ':slip-' + label
            cert['candidates'][name] = dict(actor=row['actor'], kind='slip', label='grid placement',
                                             part=part, support=[], pathBlocked=[])
        if row['part']['canonical'] in ('3004','3001'):
            plate = deepcopy(row['part'])
            plate['canonical'] = plate['partNumber'] = {'3004':'3023','3001':'3020'}[plate['canonical']]
            for field in ('rawMatrix','matrix'):
                plate[field][1][3] += 16  # same underside, one-plate instead of one-brick height
            actor = 'Y' + row['actor'][1:]
            cert['candidates'][actor+':thin'] = dict(actor=actor, kind='wrong_size',label='available part',
                                                     part=plate,support=[],pathBlocked=[],replaces=row['actor'])
            turn = deepcopy(row['part'])
            rotation = np.asarray([[0,0,1,0],[0,1,0,0],[-1,0,0,0],[0,0,0,1]])
            for field in ('rawMatrix','matrix'):
                turn[field] = (np.asarray(turn[field]) @ rotation).tolist()
            cert['candidates'][row['actor']+':quarter_turn'] = dict(actor=row['actor'],kind='rotation',
                label='grid placement',part=turn,support=[],pathBlocked=[])
    # A spare 1x1 plate can be left on the build. The candidate location is
    # computed from the current assembly, then frozen in the qualified model.
    exemplar = deepcopy(next(r['part'] for r in cert['candidates'].values() if r['kind'] == 'goal'))
    exemplar.update(partNumber='3024', canonical='3024', name='1x1 plate', colorHex='#f2cd37')
    cert['candidates']['X001:seed'] = dict(actor='X001', kind='spare', label='spare plate',
                                             part=exemplar, support=[], pathBlocked=[])
    cert['contentSha256'] = digest({k:v for k,v in cert.items() if k != 'contentSha256'})
    return cert

def perform(rt, state, action):
    after, feedback = rt.check(state, action['partId'], action['type'], candidate=action.get('candidate'))
    return after if feedback['code'] == 'OK' else None

def replay(rt, state, actions):
    before = dict(state)
    for action in actions:
        state = perform(rt, state, action)
        if state is None:
            return None
    return state if state != before else None

def candidates(rt, prefix, suffix):
    events = []
    installed = [a for a, k in prefix.items() if k and rt.goal.get(a)]
    for actor in installed:
        key = prefix[actor]
        remove = [dict(type='detach', partId=actor)]
        if replay(rt, prefix, remove) is not None:
            events.append(('removed_piece', remove, [dict(type='attach', partId=actor, candidate=key)]))
        for other, row in rt.candidates.items():
            if row['kind'] == 'wrong_color' and row['part'].get('derivedFromSourceIndex') == rt.row(key)['part'].get('sourceIndex'):
                change = remove + [dict(type='attach', partId=row['actor'], candidate=other)]
                restore = [dict(type='detach', partId=row['actor']), dict(type='attach', partId=actor, candidate=key)]
                events.append(('wrong_color', change, restore))
            if row['kind'] == 'wrong_size' and row.get('replaces') == actor:
                change = remove + [dict(type='attach', partId=row['actor'], candidate=other)]
                restore = [dict(type='detach', partId=row['actor']), dict(type='attach', partId=actor, candidate=key)]
                events.append(('wrong_size', change, restore))
            if (row['kind'] == 'wrong_type'
                    and row['part'].get('derivedFromSourceIndex') == rt.row(key)['part'].get('sourceIndex')
                    and row['part']['canonical'] != rt.row(key)['part']['canonical']):
                change = remove + [dict(type='attach', partId=row['actor'], candidate=other)]
                restore = [dict(type='detach', partId=row['actor']), dict(type='attach', partId=actor, candidate=key)]
                events.append(('wrong_part', change, restore))
            if row['actor'] == actor and row['kind'] == 'slip':
                change = remove + [dict(type='attach', partId=actor, candidate=other)]
                restore = [dict(type='detach', partId=actor), dict(type='attach', partId=actor, candidate=key)]
                events.append(('shifted_piece', change, restore))
            if row['actor'] == actor and row['kind'] == 'rotation':
                change = remove + [dict(type='attach', partId=actor, candidate=other)]
                restore = [dict(type='detach', partId=actor), dict(type='attach', partId=actor, candidate=key)]
                events.append(('rotated_piece', change, restore))
    # Two correctly shaped, differently colored bricks accidentally trade places.
    for i, a in enumerate(installed):
        for b in installed[i+1:]:
            pa, pb = rt.row(prefix[a])['part'], rt.row(prefix[b])['part']
            if pa['canonical'] != pb['canonical'] or pa['colorHex'] == pb['colorHex']:
                continue
            ka, kb = a+':swap-'+b, b+':swap-'+a
            if ka not in rt.candidates or kb not in rt.candidates:
                continue
            change = [dict(type='detach', partId=a), dict(type='detach', partId=b),
                      dict(type='attach', partId=a, candidate=ka), dict(type='attach', partId=b, candidate=kb)]
            restore = [dict(type='detach', partId=a), dict(type='detach', partId=b),
                       dict(type='attach', partId=a, candidate=prefix[a]), dict(type='attach', partId=b, candidate=prefix[b])]
            events.append(('swapped_positions', change, restore))
    # A bump can dislodge two already installed pieces in one unnoticed
    # incident. Keep the first legally detachable pair per trigger, then let
    # the full recovery gate below decide whether this is a valid episode.
    for i, a in enumerate(installed):
        found = False
        for b in installed[i+1:]:
            for first, second in ((a, b), (b, a)):
                change = [dict(type='detach', partId=first), dict(type='detach', partId=second)]
                after = replay(rt, prefix, change)
                if after is None:
                    continue
                restore = [dict(type='attach', partId=second, candidate=prefix[second]),
                           dict(type='attach', partId=first, candidate=prefix[first])]
                if replay(rt, after, restore) == prefix:
                    events.append(('cascade_removal', change, restore))
                    found = True
                    break
            if found:
                break
        if found:
            break
    # A piece from a later page is installed early. Admit only when the next
    # planned move becomes illegal; otherwise it is harmless valid progress.
    for actor in suffix[1:]:
        key = rt.goal[actor]
        change = [dict(type='attach', partId=actor, candidate=key)]
        after = replay(rt, prefix, change)
        if after is not None and perform(rt, after, dict(type='attach', partId=suffix[0], candidate=rt.goal[suffix[0]])) is None:
            events.append(('early_cover', change, [dict(type='detach', partId=actor)]))
    # Extra attached plate, preferably on an installed brick. Plate-only spare
    # placements are retained as a separate weaker event label.
    extra = 'X001:extra'
    if extra in rt.candidates:
        events.append(('extra_layer', [dict(type='attach', partId='X001', candidate=extra)],
                       [dict(type='detach', partId='X001')]))
    return events

def add_swaps(cert):
    rows = cert['candidates']
    goals = [(a, r) for a, r in rows.items() if r['kind'] == 'goal']
    for key_a, ra in goals:
        for key_b, rb in goals:
            if key_a == key_b or ra['part']['canonical'] != rb['part']['canonical'] or ra['part']['colorHex'] == rb['part']['colorHex']:
                continue
            part = deepcopy(ra['part'])
            for field in ('rawMatrix', 'matrix'):
                part[field] = deepcopy(rb['part'][field])
            name = ra['actor']+':swap-'+rb['actor']
            rows[name] = dict(actor=ra['actor'], kind='swap', label='grid placement',
                              part=part, support=[], pathBlocked=[])

def add_extra(cert, prefix):
    temp = PlateAssembly(cert)
    if prefix['X001']:
        return None
    # Search snaps against the current physical structure. Prefer snaps above
    # a mounted brick; a separate baseplate placement does not count as layer.
    options = temp.snaps(prefix, 'X001', np.eye(3))
    options.sort(key=lambda p: float((temp.inverse_board @ np.asarray(p['rawMatrix']))[1,3]))
    for option in options:
        try:
            key = temp.register('X001', option['rawMatrix'])
            after = perform(temp, prefix, dict(type='attach', partId='X001', candidate=key))
        except (ValueError, KeyError):
            continue
        if after is not None and option['other'] != '@baseplate':
            cert['candidates']['X001:extra'] = {**deepcopy(temp.row(key)), 'kind':'spare'}
            return option['other']
    return None

def build_one(path):
    source = json.loads(path.read_text())
    cert = add_variants(source)
    add_swaps(cert)
    rt = PlateAssembly(cert)
    manual = rt.manual()
    if not manual['pathVerified']:
        return [], dict(modelId=source['modelId'], excluded='no verified from-empty path')
    order = manual['parts']
    trigger_points = sorted({3, max(3, len(order)//2)})
    event_rows = []
    proposed=Counter();rejected=Counter()
    for at in trigger_points:
        if at >= len(order):
            continue
        prefix = manual['states'][at]
        add_extra(cert, prefix)
    rt = PlateAssembly(cert)
    manual = rt.manual()
    for at in trigger_points:
        if at >= len(order):
            continue
        prefix = manual['states'][at]
        suffix = order[at:]
        for kind, change, restore in candidates(rt, prefix, suffix):
            proposed[kind]+=1
            after = replay(rt, prefix, change)
            if after is None or rt.complete(after):
                rejected['illegal_or_no_change']+=1
                continue
            recovered = replay(rt, after, restore)
            if recovered != prefix:
                rejected['cannot_restore_prefix']+=1
                continue
            final = dict(recovered)
            valid = True
            for actor in suffix:
                final = perform(rt, final, dict(type='attach', partId=actor, candidate=rt.goal[actor]))
                if final is None:
                    valid = False
                    break
            if not valid or not rt.complete(final):
                rejected['cannot_finish_after_repair']+=1
                continue
            event_rows.append(dict(kind=kind, trigger=at, transaction=change,
                                   recoveryWitness=restore+[dict(type='attach',partId=a,candidate=rt.goal[a]) for a in suffix],
                                   beforeSha256=digest(prefix), afterSha256=digest(after)))
    # Keep one deterministic case per model, timing, and mechanism. This makes
    # the bank balanced without choosing cases by a model's eventual behavior.
    selected = {}
    for row in event_rows:
        selected.setdefault((row['trigger'],row['kind']), row)
    cert['contentSha256'] = digest({k:v for k,v in cert.items() if k != 'contentSha256'})
    rt = PlateAssembly(cert)
    cases = []
    for at in trigger_points:
        if at >= len(order):
            continue
        group = f"{source['modelId']}--t{at}"
        cases.append(dict(id=group+'--control', modelId=source['modelId'], sourceFamily=source['source']['modelId'],
                          targetParts=len(order),kind='none', trigger=at,
                          pairedGroup=group, protocol=VERSION, manipulationProtocol=PROTOCOL))
    for (at, kind), row in selected.items():
        group = f"{source['modelId']}--t{at}"
        cases.append(dict(id=group+'--'+kind, modelId=source['modelId'],sourceFamily=source['source']['modelId'],
                          targetParts=len(order),kind=kind,
                          trigger=at, pairedGroup=group, protocol=VERSION, manipulationProtocol=PROTOCOL,
                          privateEvent=row))
    qualification = dict(modelId=source['modelId'], sourceFamily=source['source']['modelId'],
                         sourceCertificateSha256=source['contentSha256'], runtimeCertificateSha256=cert['contentSha256'],
                         buildWitness=[dict(type='attach',partId=a,candidate=rt.goal[a]) for a in order],
                         goalSha256=digest(rt.goal), proposedEventTransactions=dict(proposed),
                         qualifiedEventVariations=dict(Counter(r['kind'] for r in event_rows)),
                         rejectedTransactions=dict(rejected),admittedCases=len(cases),
                         deduplicatedQualifiedVariations=len(event_rows)-len(selected))
    write(OUT/'models'/source['modelId']/'qualification.json', cert)
    write(OUT/'models'/source['modelId']/'evidence.json', qualification)
    return cases, qualification

def main():
    all_cases = []
    audits = []
    for path in sorted(SOURCE.glob('*/qualification.json')):
        cases, audit = build_one(path)
        all_cases += cases
        audits.append(audit)
        print(audit['modelId'], len(cases), audit.get('qualifiedEventVariations', audit.get('excluded')), flush=True)
    write(OUT/'cases.private.json', dict(schema=VERSION, cases=all_cases))
    write(OUT/'index.json', dict(schema=VERSION, cases=[{k:v for k,v in c.items() if k!='privateEvent'} for c in all_cases],
                                 modelAudits=audits, counts=dict(Counter(c['kind'] for c in all_cases))))

if __name__ == '__main__':
    main()
