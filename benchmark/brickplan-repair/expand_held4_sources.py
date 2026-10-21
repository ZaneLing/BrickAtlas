"""Add disjoint source-derived subassemblies and vetted static repair cases.

Each added structure uses original LDraw part identities and poses outside the
source indices already used by the 2,541-case bank. It is a new structure
configuration, never counted as a new independent source model.
"""
from collections import Counter, defaultdict
from copy import deepcopy
from itertools import combinations
from pathlib import Path
import hashlib
import json
import sys
import time
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from assembly import Assembly
from library import (Qualifier, read_source, select_cluster, qualify_candidates,
                     substitute, transformed, add_variant)
from static_bench import (Domain, TYPES, TAXONOMY, annotate_static, make_case,
                          groups_for, normalized_state, replacement_kind,
                          digest as source_digest)
from static_v4.certify import digest

ROOT = HERE.parents[1]
SOURCE = ROOT / 'deliverables/brickplan-repair-library'
OUT = ROOT / 'deliverables/brickplan-static-held4/expansion'
PROTOCOL = 'connector-workbench/4'


def read(path): return json.loads(path.read_text())


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def normalize(case, cert, source_id):
    c = deepcopy(case)
    for key in ('expectedOptimum', 'difficulty', 'repairEvidence', 'tags',
                'description', 'observation', 'counterfactuals'):
        c.pop(key, None)
    public_id = 'X' + hashlib.sha256(c['id'].encode()).hexdigest()[:11].upper()
    c.update(schema='brickplan-static-repair-case/held4', publicId=public_id,
             manipulationProtocol=PROTOCOL, category=c['kind'],
             title=('无故障对照' if c['kind'] == 'control' else
                    ' + '.join(dict.fromkeys(TYPES[r['type']] for r in c['roots']))),
             description='观察固定初态和目标，然后修复。',
             expectedOptimum=None, referenceCost=len(c['oraclePlan']),
             referenceIsOptimal=False, difficulty='未标定', tags=[],
             sourceExample=source_id, sourceModelId=source_id,
             targetProvenance=dict(kind='source_exact', scope='Disjoint original rigid-part subset'),
             observation=dict(protocol='visual-rgb-v3',
                              visualEligibility='pending-held4-render-review'),
             referenceValidation=dict(status='DIRECT_REPLAY_PASS', protocol=PROTOCOL,
                 qualificationSha256=cert['contentSha256'],
                 sha256=digest(dict(caseId=c['id'], initial=c['initial'], goal=c['goal'],
                                    plan=c['oraclePlan'], source=cert['contentSha256']))))
    return c


def make_structure(source_id, used):
    _, parts, adjacency, source = read_source(source_id)
    retained = [i for i, p in enumerate(parts) if p['sourceIndex'] not in used]
    mapping = {old: new for new, old in enumerate(retained)}
    available = [parts[i] for i in retained]
    edges = {mapping[i]: {mapping[j] for j in adjacency[i] if j in mapping}
             for i in retained}
    q = Qualifier()
    cert = select_cluster(available, edges, q, max_parts=11)
    selected = sorted([p['sourceIndex'] for p in cert['fixed'].values()]
                      + [r['part']['sourceIndex'] for r in cert['candidates'].values()])
    if len(selected) < 7: raise ValueError('Fewer than seven source parts')
    model_id = source_id + '--alt1'
    source.update(includedSourceIndices=selected, sourceGeometryModified=False,
                  variantOf=source_id)
    cert.update(modelId=model_id, source=source)
    goals = {r['actor']: k for k, r in cert['candidates'].items() if r['kind'] == 'goal'}
    # Produce a diverse proposal pool; failed geometry/repair checks never enter.
    proposals = [({}, [])]
    for actor in goals:
        proposals.append(({actor: ''}, []))
    admitted = []
    for actor, key in goals.items():
        p = cert['candidates'][key]['part']
        color = ('1', '#0055BF') if p['colorHex'].lower() != '#0055bf' else ('4', '#C91A09')
        spare = 'W' + actor[1:]
        alt = substitute(p, p['partNumber'], color)
        trial = add_variant(cert, q, spare + ':color', alt, TYPES['wrong_color'],
                            'wrong_color', {actor: '', spare: spare + ':color'}, model_id)
        if trial: admitted.append(({actor: '', spare: spare + ':color'}, 'wrong_color'))
        if len([x for x in admitted if x[1] == 'wrong_color']) >= 4: break
    for kind in ('offset', 'rotation', 'wrong_type', 'wrong_size'):
        for actor, key in goals.items():
            p = cert['candidates'][key]['part']; raw = np.asarray(p['rawMatrix'])
            options = []
            if kind == 'offset':
                options = [(actor + ':offset', transformed(p, delta=20 * raw[:3, 0]), {actor: actor + ':offset'})]
            elif kind == 'rotation':
                axis = raw[:3, 1]; cross = np.array([[0,-axis[2],axis[1]], [axis[2],0,-axis[0]], [-axis[1],axis[0],0]])
                rotation = np.outer(axis, axis) + cross
                options = [(actor + ':rotation', transformed(p, rotation=rotation, pivot=raw[:3, 3]),
                            {actor: actor + ':rotation'})]
            else:
                stems = ['3070b', '3069b', '3005', '3022'] if kind == 'wrong_type' else ['3023', '3022', '3710', '3623', '3004']
                for stem in stems:
                    if stem == p['partNumber']: continue
                    try:
                        alt = substitute(p, stem)
                        if replacement_kind(p, alt) != kind: continue
                    except (ValueError, KeyError, RuntimeError): continue
                    spare = ('T' if kind == 'wrong_type' else 'Z') + actor[1:]
                    options.append((spare + ':' + kind, alt,
                                    {actor: '', spare: spare + ':' + kind}))
            found = False
            for option_key, alt, edits in options:
                trial = add_variant(cert, q, option_key, alt, TYPES[kind], kind, edits, model_id)
                if trial:
                    admitted.append((edits, kind)); found = True; break
            if found: break
    # A genuinely superfluous physical plate, mounted above an existing piece.
    # It is an independent fault only when the whole state and removal path pass.
    for actor, key in goals.items():
        p = cert['candidates'][key]['part']
        extra_actor = 'E' + actor[1:]
        found = False
        for height in (8, 24, 32):
            try:
                alt = transformed(substitute(p, '3024'), delta=[0, -height, 0])
                extra_key = extra_actor + ':extra'
                trial = add_variant(cert, q, extra_key, alt, TYPES['extra'], 'extra',
                                    {extra_actor: extra_key}, model_id)
                if trial:
                    admitted.append(({extra_actor: extra_key}, 'extra'))
                    found = True; break
            except (ValueError, KeyError, RuntimeError): continue
        if found: break
    # Position exchange must move TWO distinguishable physical pieces. The
    # symmetry-aware live completion check below discards any visual no-op.
    goal_actors = list(goals)
    swap_pairs = list(combinations(goal_actors, 2))
    swap_pairs.sort(key=lambda pair: (
        cert['candidates'][goals[pair[0]]]['part']['canonical'] !=
        cert['candidates'][goals[pair[1]]]['part']['canonical'], pair))
    swaps = 0
    for actor_a, actor_b in swap_pairs[:24]:
        if swaps >= 2: break
        pa = cert['candidates'][goals[actor_a]]['part']
        pb = cert['candidates'][goals[actor_b]]['part']
        if pa['canonical'] == pb['canonical'] and pa['colorHex'].lower() == pb['colorHex'].lower():
            continue
        original = deepcopy(cert['candidates'])
        edits = {}
        for actor, partner, part, target in ((actor_a, actor_b, pa, pb),
                                             (actor_b, actor_a, pb, pa)):
            raw = np.asarray(target['rawMatrix'])
            alt = deepcopy(part)
            alt['matrix'] = (raw @ np.linalg.inv(np.asarray(part['rawMatrix']))
                             @ np.asarray(part['matrix'])).tolist()
            alt['rawMatrix'] = raw.tolist()
            alt['direction'] = target['direction']
            alt['swapPartner'] = partner
            option = actor + ':swap-' + partner
            cert['candidates'][option] = dict(actor=actor, part=alt,
                                              kind='swapped_positions', label=TYPES['swapped_positions'])
            edits[actor] = option
        try:
            qualify_candidates(cert, q)
            annotate_static(make_case(cert, model_id, edits, groups_for(cert, edits)), Domain(cert, {}))
            admitted.append((edits, 'swapped_positions'))
            swaps += 1
        except (ValueError, AssertionError):
            cert['candidates'] = original
    qualify_candidates(cert, q)
    domain = Domain(cert, {})
    cases = []; seen = set()
    for edits, _ in proposals + admitted:
        try:
            c = annotate_static(make_case(cert, model_id, edits, groups_for(cert, edits)), domain)
            physical = normalized_state(c, cert)
            if physical not in seen: cases.append(c); seen.add(physical)
        except (ValueError, AssertionError): continue
    singles = [c for c in cases if len(c['roots']) == 1]
    pairs = 0
    for i, a in enumerate(singles):
        for b in singles[i + 1:]:
            if pairs >= 8: break
            occupied = {x for r in a['roots'] for x in r['affectedActors']}
            if occupied.intersection(x for r in b['roots'] for x in r['affectedActors']): continue
            edits = {actor: key for c in (a, b) for actor, key in c['initial'].items()
                     if key != c['goal'].get(actor, '')}
            try:
                c = annotate_static(make_case(cert, model_id, edits, groups_for(cert, edits)), domain)
                physical = normalized_state(c, cert)
                if physical not in seen: cases.append(c); seen.add(physical); pairs += 1
            except (ValueError, AssertionError): continue
        if pairs >= 8: break
    if len(cases) < 8: raise ValueError('Fewer than eight qualified repair cases')
    cert['contentSha256'] = source_digest(cert)
    runtime = Assembly(cert)
    final = {}
    for old in cases:
        state = runtime.state(old['initial'])
        # Connector-aware physical symmetry can make an old pose edit a true
        # no-op. Such a proposal must not be sold as an error case.
        if runtime.complete(state) != (old['kind'] == 'control'):
            continue
        for action in old['oraclePlan']:
            state, feedback = runtime.check(state, action['partId'], action['type'],
                                            candidate=action.get('candidate'))
            if feedback['code'] != 'OK': raise ValueError(old['id'] + ':' + feedback['code'])
        if not runtime.complete(state): raise ValueError(old['id'] + ': incomplete')
        c = normalize(old, cert, source_id)
        c['qualificationSha256'] = cert['contentSha256']
        final[c['id']] = c
    if len(final) < 8: raise ValueError('Fewer than eight physical-fault cases after symmetry audit')
    folder = OUT / 'library/models' / model_id
    dump(folder / 'qualification.json', cert)
    dump(folder / 'cases.json', final)
    base = read(SOURCE / 'models' / source_id / 'record.json')
    record = dict(modelId=model_id, title=base['title'] + ' · 原模型另一处相连结构',
                  status='ready', sourceModelId=source_id, structureVariant='disjoint-source-subassembly',
                  sourceIndices=selected, originalParts=source['originalPartCount'],
                  caseParts=len(selected), mutableParts=len(goals), fixedParts=1,
                  caseCount=len(final), kinds=dict(Counter(c['kind'] for c in final.values())),
                  targetProvenance=dict(kind='source_exact', sourceGeometryModified=False),
                  qualificationSha256=cert['contentSha256'], manipulationProtocol=PROTOCOL)
    dump(folder / 'record.json', record)
    return record, list(final.values())


def main():
    index = read(SOURCE / 'index.json')
    used = defaultdict(set)
    for model in index['models']:
        source_id = model['modelId'].split('--deep')[0]
        used[source_id].update(model['sourceIndices'])
    eligible = [m for m in index['models'] if '--deep' not in m['modelId']
                and m.get('targetProvenance', {}).get('kind') == 'source_exact'
                and 25 <= m['source']['validRigidParts'] <= 120]
    eligible.sort(key=lambda m: (m['source']['validRigidParts'], m['modelId']))
    records, cases, rejected = [], [], []
    started = time.time()
    for model in eligible:
        if len(records) >= 40: break
        source_id = model['modelId']
        try:
            record, rows = make_structure(source_id, used[source_id])
            records.append(record); cases.extend(rows)
            print('ADDED', source_id, len(rows), 'total', len(records), flush=True)
        except (ValueError, AssertionError) as exc:
            rejected.append(dict(sourceModelId=source_id, reason=str(exc)[:180]))
            print('REJECT', source_id, str(exc)[:100], flush=True)
    library = OUT / 'library';library.mkdir(parents=True, exist_ok=True)
    (library / 'cases.jsonl').write_text(''.join(json.dumps(c, ensure_ascii=False) + '\n' for c in cases))
    (library / 'questions.jsonl').write_text(''.join(json.dumps(dict(publicId=c['publicId'], modelId=c['modelId'],
        observationProtocol='visual-rgb-v3', manipulationProtocol=PROTOCOL, environmentChanges=False),
        ensure_ascii=False) + '\n' for c in cases))
    dump(library / 'index.json', dict(schema='brickplan-static-repair-expansion/held4',
         benchmarkMode='static', manipulationProtocol=PROTOCOL, modelCount=len(records),
         caseCount=len(cases), models=records,
         taxonomy=[dict(id=k,label=l,kinds=v) for k,l,v in TAXONOMY], kinds=TYPES))
    dump(OUT / 'generation.json', dict(schema='source-disjoint-expansion/1',
         newStructureConfigurations=len(records), independentNewSourceModels=0,
         sourceFamilies=len({c['sourceExample'] for c in cases}), cases=len(cases),
         rejected=rejected, seconds=round(time.time()-started, 2)))
    print('DONE', len(records), len(cases), round(time.time()-started, 2), flush=True)


if __name__ == '__main__': main()
