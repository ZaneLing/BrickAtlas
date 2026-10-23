"""Condition-independent inventory and reversible pose alternatives."""
from copy import deepcopy
import math
import numpy as np
from library import substitute
from community_modules.core import ModuleAssembly
from expansion_v7.runtime import runtime


def relocated(part, raw):
    part = deepcopy(part)
    raw = np.asarray(raw, dtype=float)
    alias = np.linalg.inv(np.asarray(part['rawMatrix'])) @ np.asarray(part['matrix'])
    part.update(rawMatrix=raw.tolist(), matrix=(raw @ alias).tolist(), direction=(-raw[:3, 1]).tolist())
    return part


def augment(source):
    cert = deepcopy(source)
    cert['candidates'] = {k: r for k, r in cert['candidates'].items() if r.get('kind') != 'catalog_distractor'}
    originals = {r['actor']: r['part'] for r in cert['candidates'].values() if r['kind'] == 'goal'}
    for original_key,replacement in cert.get('colorReplacements',{}).items():
        if original_key in cert['candidates'] and replacement['candidate'] in cert['candidates']:
            cert['candidates'][replacement['candidate']].update(faultFamily='wrong-color',
                originalActor=cert['candidates'][original_key]['actor'])
    for actor, part in originals.items():
        p = np.asarray(part['rawMatrix'])
        for j, (dx, dz) in enumerate(((20, 0), (-20, 0), (0, 20), (0, -20))):
            raw = p.copy(); raw[:3, 3] += p[:3, :3] @ [dx, 0, dz]
            cert['candidates'][f'{actor}:v7-offset{j}'] = dict(actor=actor, kind='alternative',
                faultFamily='offset', originalActor=actor, part=relocated(part, raw))
        for turn in (1, 2, 3):
            theta = turn*np.pi/2; c, s = round(np.cos(theta)), round(np.sin(theta))
            rotation = np.array([[c,0,s,0],[0,1,0,0],[-s,0,c,0],[0,0,0,1]])
            for j, (dx, dz) in enumerate(((0,0), (10,10), (10,-10), (-10,10), (-10,-10))):
                raw = p @ rotation; raw[:3, 3] += p[:3, :3] @ [dx,0,dz]
                cert['candidates'][f'{actor}:v7-turn{turn}-{j}'] = dict(actor=actor, kind='alternative',
                    faultFamily='rotated', originalActor=actor, part=relocated(part, raw))
        color = ('4', '#C91A09') if part['colorHex'].lower() != '#c91a09' else ('1', '#0055BF')
        if not any(r.get('faultFamily')=='wrong-color' and r.get('originalActor')==actor for r in cert['candidates'].values()):
            spare = 'V7W_'+actor
            cert['candidates'][spare+':v7-color'] = dict(actor=spare, kind='spare', faultFamily='wrong-color',
                originalActor=actor, part=substitute(part, part['partNumber'], color))
        stem = part['canonical']
        replacement = {'3001':'3020','3010':'3710','3004':'3023','3005':'3024',
                       '3020':'3001','3034':'3020','3023':'3004','3024':'3005',
                       '3022':'3023','3710':'3010','3039':'3004'}.get(stem)
        if replacement:
            spare = 'V7T_'+actor
            candidate = substitute(part, replacement, (part.get('colorCode', '7'), part['colorHex']))
            from assembly import info
            def underside(p):
                alias=np.linalg.inv(np.asarray(p['rawMatrix']))@np.asarray(p['matrix'])
                data=info(p['canonical'])
                return max(((alias@f)[1,3] for c,f in zip(data.conns,data.frames) if c[0]=='hole'),default=0.)
            dy=underside(part)-underside(candidate)
            for j,(dx,dz) in enumerate(((0,0),(10,0),(-10,0),(0,10),(0,-10),
                                       (20,0),(-20,0),(0,20),(0,-20),(40,0),(-40,0),(0,40),(0,-40))):
                raw=p.copy();raw[:3,3]+=p[:3,:3]@[dx,dy,dz]
                cert['candidates'][spare+f':v7-type{j}'] = dict(actor=spare,kind='spare',faultFamily='wrong-part',
                    originalActor=actor,part=relocated(candidate,raw))
    for a, pa in originals.items():
        for b, pb in originals.items():
            if a == b or pa['canonical'] != pb['canonical'] or pa['colorHex'].lower() == pb['colorHex'].lower():
                continue
            cert['candidates'][f'{a}:swap:{b}'] = dict(actor=a, kind='alternative',
                part=relocated(pa, pb['rawMatrix']))
    # Existing module spares keep their qualified connector poses. New objects
    # get a 1x1 plate on top of every upward-facing goal part (legality is checked
    # at use time); identical inventory is shared by all conditions.
    for key, row in cert['candidates'].items():
        if row['actor'] == 'E':
            row['faultFamily'] = 'extra-layer'
    if not any(r['actor'] == 'E' for r in cert['candidates'].values()):
        from assembly import info, compatible
        from baseplate import STUD
        prototype = substitute(next(iter(originals.values())), '3024', ('4', '#C91A09'))
        for parent, part in originals.items():
            data = info(part['canonical'])
            frames = np.asarray(part['matrix']) @ data.frames
            count = 0
            for conn, frame in zip(data.conns, frames):
                if conn[0] != 'stud' or frame[1,1] < .999:
                    continue
                # LDraw top stud connection plane: the plate's bottom is at +8.
                raw = np.eye(4); raw[:3,:3] = np.asarray(part['rawMatrix'])[:3,:3]
                raw[:3,3] = frame[:3,3] - raw[:3,:3] @ [0,8,0]
                cert['candidates'][f'E:mount:{parent}:{count}'] = dict(actor='E', kind='spare',
                    faultFamily='extra-layer', part=relocated(prototype, raw))
                count += 1
                if count >= 4:
                    break
    return cert


def pad(cert):
    """Uniform action counts, with no fixed-context actors added to inventory."""
    groups = {}
    for key, row in cert['candidates'].items():
        groups.setdefault(row['actor'], []).append(key)
    count = max(24, math.ceil(max(map(len, groups.values()))/12)*12)
    for actor, keys in groups.items():
        base = cert['candidates'][keys[0]]['part']
        seen = {tuple(np.round(np.asarray(cert['candidates'][k]['part']['rawMatrix']).ravel(), 4)) for k in keys}
        for dx in range(-100, 121, 20):
            for dz in range(-100, 121, 20):
                if len(keys) >= count:
                    break
                raw = np.asarray(base['rawMatrix']).copy(); raw[:3,3] += [dx,0,dz]
                token = tuple(np.round(raw.ravel(), 4))
                if token in seen:
                    continue
                key = f'{actor}:padding{len(keys)}'
                cert['candidates'][key] = dict(actor=actor, kind='catalog_distractor', part=relocated(base, raw))
                keys.append(key); seen.add(token)
            if len(keys) >= count:
                break
        if len(keys) != count:
            raise ValueError((actor, 'Cannot pad candidates'))
    cert['catalogPolicy'] = dict(candidatesPerActor=count, publicSort='random aliases only',
        sameAcrossConditions=True, fixedContextInInventory=False)
    return cert
