"""Interactive rigid LEGO assembly: connector snaps, arbitrary order, held subassemblies.

The hand/fixture holds disconnected components during manipulation. There is no
bottom-support or gravity predicate. Collision and a certified straight insertion
path still apply. This is ideal rigid manipulation, not clutch/force simulation.
"""
from collections import Counter
from copy import deepcopy
from functools import lru_cache
import hashlib
import json
import numpy as np
from library import Qualifier, line
from geometry import parse_ldr
from bricknet.graph import _part_info
from bricknet.core import _STUD_MATES, _AXLE_MATES

PROTOCOL = 'connector-workbench/5'

@lru_cache(maxsize=256)
def info(canonical):
    p = {'canonical': canonical, 'matrix': np.eye(4).tolist()}
    return _part_info(parse_ldr(line(p)).part_ids[0])

def compatible(a, b):
    ka, sa, pa, *_ = a
    kb, sb, pb, *_ = b
    if {ka, kb} == {'stud', 'hole'}:
        return (sa, sb) in _STUD_MATES or (sb, sa) in _STUD_MATES
    if ka == kb == 'axle':
        return (sa, sb) in _AXLE_MATES or (sb, sa) in _AXLE_MATES
    return ka == kb and ka in ('hinge', 'fixed', 'ball') and sa == sb and pa != pb and pa is not None and pb is not None

class Assembly:
    def __init__(self, certificate):
        self.cert = certificate
        self.candidates = certificate['candidates']
        self.q = Qualifier()
        self.actors = sorted({r['actor'] for r in self.candidates.values()})
        self.goal = {a: '' for a in self.actors}
        self.goal.update({r['actor']: k for k, r in self.candidates.items() if r['kind'] == 'goal'})
        self.parts = {a: next(r['part'] for r in self.candidates.values() if r['actor'] == a) for a in self.actors}
        self.extra = {}
        self.anchor_ids = set(certificate['fixed'])

    def row(self, key):
        return self.candidates.get(key) or self.extra[key]

    def state(self, supplied):
        if not isinstance(supplied, dict) or set(supplied) - set(self.actors):
            raise ValueError('零件状态无效')
        out = {a: supplied.get(a, '') for a in self.actors}
        for a, k in out.items():
            if not isinstance(k, str) or (k and (k not in self.candidates and k not in self.extra or self.row(k)['actor'] != a)):
                raise ValueError('未知的零件位置')
        return out

    def present(self, state):
        return {**self.cert['fixed'], **{a: self.row(k)['part'] for a, k in state.items() if k}}

    def environment_blockers(self, part): return []
    def environment_connections(self, part): return []
    def environment_path_blockers(self, part, direction, length): return []
    def path_lengths(self, part, direction): return [self.cert['extractionLengthLDU']]

    def register(self, actor, raw):
        if actor not in self.parts:
            raise ValueError('请选择可移动积木')
        m = np.asarray(raw, dtype=float)
        if (m.shape != (4, 4) or not np.isfinite(m).all() or not np.allclose(m[3], [0, 0, 0, 1])
                or not np.allclose(m[:3, :3].T @ m[:3, :3], np.eye(3), atol=1e-5)
                or abs(np.linalg.det(m[:3, :3])-1) > 1e-5 or np.max(np.abs(m[:3, 3])) > 10000):
            raise ValueError('安装姿态无效')
        for k, row in self.candidates.items():
            if row['actor'] == actor and np.allclose(row['part']['rawMatrix'], m, atol=.001):
                return k
        base = self.parts[actor]
        alias = np.linalg.inv(np.asarray(base['rawMatrix'])) @ np.asarray(base['matrix'])
        p = deepcopy(base)
        p.update(rawMatrix=m.tolist(), matrix=(m @ alias).tolist(), direction=(-m[:3, 1]).tolist())
        key = actor+':free-'+hashlib.sha256(np.round(m, 5).tobytes()).hexdigest()[:16]
        self.extra[key] = dict(actor=actor, kind='interactive', label='手动安装', part=p, support=[], pathBlocked=[])
        return key

    def connections(self, state):
        parts = self.present(state)
        graph = {a: set() for a in parts}
        keys = list(parts)
        for i, a in enumerate(keys):
            for b in keys[i+1:]:
                if self.q.connection(parts[a], parts[b]):
                    graph[a].add(b); graph[b].add(a)
        groups = []
        remaining = set(parts)
        while remaining:
            found, todo = set(), [min(remaining)]
            while todo:
                a = todo.pop()
                if a in found: continue
                found.add(a); todo.extend(graph[a]-found)
            groups.append(sorted(found)); remaining -= found
        return graph, groups

    def check(self, supplied, actor, kind, raw=None, candidate=None):
        state = self.state(supplied)
        if actor not in state or kind not in ('attach', 'detach'):
            return state, dict(code='INVALID_ACTION', blockers=[])
        if (kind == 'detach') != bool(state[actor]):
            return state, dict(code='ALREADY_IN_RACK' if kind == 'detach' else 'ALREADY_INSTALLED', blockers=[])
        key = state[actor] if kind == 'detach' else (self.register(actor, raw) if raw is not None else candidate)
        if not key or (key not in self.candidates and key not in self.extra) or self.row(key)['actor'] != actor:
            return state, dict(code='UNREGISTERED_POSE', blockers=[])
        moving = self.row(key)['part']
        others = self.present({**state, actor: ''})
        blocked = self.environment_blockers(moving) + [a for a, p in others.items() if self.q.endpoint(moving, p)['status'] != 'CLEAR']
        if blocked:
            return state, dict(code='ENDPOINT_COLLISION', blockers=blocked)
        connections = self.environment_connections(moving) + [(a, c) for a, p in others.items() for c in self.q.connection(moving, p)]
        if kind == 'attach' and not connections:
            return state, dict(code='NO_CONNECTION', blockers=[])
        # Test both senses of connector axes and part axes, never one prescribed
        # upward path. Every accepted path is checked against every present part.
        directions = [np.asarray(moving['direction'])]
        directions += [np.asarray(c['axis']) * sign for _, c in connections for sign in (1, -1)]
        directions += [np.asarray(moving['matrix'])[:3, i] * sign for i in range(3) for sign in (1, -1)]
        seen, witnesses, collisions = set(), [], set()
        for d in directions:
            d = d / np.linalg.norm(d)
            token = tuple(np.round(d, 5))
            if token in seen: continue
            seen.add(token)
            p = {**moving, 'direction': d.tolist()}
            for length in self.path_lengths(moving, d):
                hits = self.environment_path_blockers(moving, d, length)
                for a, obstacle in others.items():
                    if self.q.path(p, obstacle, length)['status'] != 'CLEAR':
                        hits.append(a)
                if not hits:
                    witnesses.append((d.tolist(), length)); break
                collisions.update(hits)
            if witnesses: break
        if not witnesses:
            return state, dict(code='PATH_BLOCKED', blockers=sorted(collisions))
        after = {**state, actor: '' if kind == 'detach' else key}
        _, groups = self.connections(after)
        return after, dict(code='OK', blockers=[], path=witnesses[0][0], pathLengthLDU=witnesses[0][1], components=groups, candidate=key)

    def snaps(self, supplied, actor, rotation):
        state = self.state(supplied)
        if actor not in state or state[actor]: raise ValueError('先拆下这块积木')
        r = np.asarray(rotation, dtype=float)
        if r.shape != (3, 3) or not np.isfinite(r).all() or not np.allclose(r.T@r, np.eye(3), atol=1e-5) or abs(np.linalg.det(r)-1) > 1e-5:
            raise ValueError('旋转无效')
        base = self.parts[actor]
        alias = np.linalg.inv(np.asarray(base['rawMatrix'])) @ np.asarray(base['matrix'])
        moving = info(base['canonical'])
        local = alias @ moving.frames
        poses = {}
        # Only current physical geometry enters this calculation. No target,
        # oracle, labelled candidate or case error is read here.
        for other, p in self.present(state).items():
            target = info(p['canonical'])
            frames = np.asarray(p['matrix']) @ target.frames
            # User rotations are relative to the actual mounting piece. This
            # also snaps correctly on tilted/SNOT assemblies, without reading
            # the target pose or assuming a global horizontal build plane.
            mounting_rotation = np.asarray(p['rawMatrix'])[:3, :3] @ r
            for i, a in enumerate(moving.conns):
                for j, b in enumerate(target.conns):
                    if not compatible(a, b): continue
                    dot = float(np.dot(mounting_rotation @ local[i, :3, 1], frames[j, :3, 1]))
                    if a[0] != 'ball' and (abs(dot) if a[0] in ('hinge', 'axle') else dot) < .999: continue
                    m = np.eye(4); m[:3, :3] = mounting_rotation
                    m[:3, 3] = frames[j, :3, 3] - mounting_rotation @ local[i, :3, 3]
                    token = tuple(np.round(m.ravel(), 3))
                    if token not in poses:
                        poses[token] = dict(rawMatrix=m.tolist(), anchor=frames[j, :3, 3].tolist(), other=other)
        return list(poses.values())

    def signature(self, state):
        # Explicit symmetry of plain rectangular LEGO bricks/plates. Do not
        # infer symmetry for hinges, clips, slopes, printed or asymmetric parts.
        rectangles = {'3001','3002','3003','3004','3005','3008','3009','3010',
                      '3020','3021','3022','3023','3023b','3024','3031','3032','3034',
                      '3035','3036','3460','3666','3710','4477'}
        squares = {'3003','3005','3022','3024','3031'}
        # BrickNet resolves the plain LDraw 3023 plate to canonical 3023b with
        # the identity alias transform. It has the same half-turn symmetry.
        # Do not strip arbitrary suffixes: printed/asymmetric parts must retain
        # their own orientation. Regression evidence includes connector/mesh
        # checks and a real API rollout, not just equality in one rendered view.
        result = []
        for key in state.values():
            if not key: continue
            p = self.row(key)['part']; m = np.asarray(p['matrix'])
            angles = (0, 1, 2, 3) if p['canonical'] in squares else (0, 2) if p['canonical'] in rectangles else (0,)
            variants = []
            for quarter in angles:
                c, sn = round(np.cos(quarter*np.pi/2)), round(np.sin(quarter*np.pi/2))
                r = np.array([[c,0,sn,0],[0,1,0,0],[-sn,0,c,0],[0,0,0,1]])
                variants.append(tuple(np.round((m @ r).ravel(), 3)))
            result.append((p['canonical'], p['colorHex'].lower(), min(variants)))
        return Counter(result)

    def complete(self, state):
        return self.signature(state) == self.signature(self.goal)

    def manual(self, initial=None):
        # Find a build witness, with the base connected throughout. Practice
        # permits held components; a serial instruction book needs a connected
        # predecessor for each newly installed piece.
        origin = dict(self.goal if initial is None else initial)
        failed = set()
        def dismantle(state):
            token = tuple(state.values())
            if not any(token): return []
            if token in failed: return None
            for actor, key in state.items():
                if not key: continue
                after = {**state, actor: ''}
                _, groups = self.connections(after)
                if any(not set(group).intersection(self.anchor_ids) for group in groups): continue
                after, check = self.check(state, actor, 'detach')
                if check['code'] != 'OK': continue
                tail = dismantle(after)
                if tail is not None: return [(actor, after)] + tail
            failed.add(token); return None
        _, groups = self.connections(origin)
        anchored = all(set(group).intersection(self.anchor_ids) for group in groups)
        steps = dismantle(origin) if anchored else None
        if steps is not None:
            states = [origin] + [state for _, state in steps]
            return dict(states=list(reversed(states)), parts=list(reversed([a for a,_ in steps])),
                        complete=True, pathVerified=True)
        # Still supply every construction state, but never misrepresent an
        # unverified clipped/curved insertion as a certified motion witness.
        state = {a: '' for a in self.actors}; states = [dict(state)]; order = []
        graph, _ = self.connections(origin); present = set(self.anchor_ids)
        remaining = {a for a,k in origin.items() if k}
        while remaining:
            choices = sorted(a for a in remaining if graph[a].intersection(present))
            if not choices: choices = sorted(remaining)
            a = choices[0]; state[a] = origin[a]; present.add(a);remaining.remove(a)
            states.append(dict(state));order.append(a)
        return dict(states=states, parts=order, complete=not remaining, pathVerified=False,
                    reason='连接顺序图；弯曲路径或卡扣释放尚未通过运动校验')
