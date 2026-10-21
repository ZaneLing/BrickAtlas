"""Infinite white stud surface for interactive practice; no fixed model actors.

The archived finite-fixture certificates stay immutable. Their former fixture is
a normal movable model piece here. The plate is environment geometry, excluded
from inventory, target signatures and operation costs.
"""
from copy import deepcopy
from functools import lru_cache
import numpy as np
from meshlib import mrmeshnumpy
from assembly import Assembly, compatible, info
from geometry import mesh_for

PLATE = '@baseplate'
PROTOCOL = 'connector-workbench/5-white-baseplate'
STUD = ('stud', 'stud', None, 0, 0)

@lru_cache(maxsize=256)
def vertices(canonical):
    return mrmeshnumpy.getNumpyVerts(mesh_for(canonical)[0])

def transformed_vertices(p, transform):
    m = transform @ np.asarray(p['matrix'])
    return vertices(p['canonical']) @ m[:3, :3].T + m[:3, 3]


class PlateAssembly(Assembly):
    def __init__(self, source):
        cert = deepcopy(source)
        self.former_fixed = {a: a + ':goal' for a in cert['fixed']}
        for actor, part in cert['fixed'].items():
            cert['candidates'][actor + ':goal'] = dict(actor=actor, kind='goal', label='模型零件',
                part=part, support=[], pathBlocked=[])
        cert['fixed'] = {}
        super().__init__(cert)
        self.anchor_ids = {PLATE}
        # Use the model's construction axes, including globally tilted sources.
        # A plane below the whole target replaces the arbitrary old anchor.
        rotation = np.asarray(next(iter(source['fixed'].values()))['rawMatrix'])[:3, :3]
        self.board = np.eye(4); self.board[:3, :3] = rotation
        to_local = np.linalg.inv(self.board)
        parts = self.present(self.goal)
        points = np.concatenate([transformed_vertices(p, to_local) for p in parts.values()])
        foot = points[np.argmax(points[:, 1])]; bottom = foot[1]
        holes = []
        for p in parts.values():
            data = info(p['canonical']); frames = to_local @ np.asarray(p['matrix']) @ data.frames
            holes += [frame[:3, 3] for conn, frame in zip(data.conns, frames)
                      if compatible(conn, STUD) and frame[1, 1] > .999 and abs(frame[1, 3] - bottom) < .6]
        # Connector planes are exact; collision meshes have a 0.25 LDU inset.
        origin = holes[0] if holes else foot + [0, 4.25, 0]
        self.board[:3, 3] = rotation @ origin
        self.inverse_board = np.linalg.inv(self.board)
        # Some source models have flat/sideways feet. Rest them on stud tops
        # instead of forcing incompatible bottom geometry through the studs.
        resting = not holes
        if any(self.plate_collision(p) for p in parts.values()):
            self.board[:3, 3] = rotation @ (foot + [0, 4.25, 0])
            self.inverse_board = np.linalg.inv(self.board)
            resting = True
        self.baseplate = dict(matrix=self.board.tolist(), pitch=20, studRadius=6, studHeight=4,
                             color='#ffffff', infinite=True, mounting='resting' if resting else 'studs')

    def migrate_state(self, state):
        """Only legacy state loading supplies the formerly implicit model piece."""
        return {**self.former_fixed, **state}

    def bounds_on_plate(self, p):
        points = transformed_vertices(p, self.inverse_board)
        return points.min(axis=0), points.max(axis=0)

    def on_plate(self, p):
        data = info(p['canonical']); frames = self.inverse_board @ np.asarray(p['matrix']) @ data.frames
        clutch = any(compatible(conn, STUD) and frame[1, 1] > .999 and abs(frame[1, 3]) < .025
                   and np.max(np.abs(frame[[0, 2], 3] / 20 - np.round(frame[[0, 2], 3] / 20))) < .00125
                   for conn, frame in zip(data.conns, frames))
        if clutch: return True
        points = transformed_vertices(p, self.inverse_board)
        feet = points[np.abs(points[:, 1] + 4.25) < .025]
        return bool(len(feet) and np.any(np.linalg.norm((feet[:, [0, 2]]+10) % 20 - 10, axis=1) < 5.5))

    def cells(self, lo, hi):
        # Canonical 1x1 plate meshes provide the real stud/hole collision shape;
        # the analytic half-space supplies the unbroken infinite solid below.
        for x in range(int(np.ceil((lo[0]-10)/20)), int(np.floor((hi[0]+10)/20))+1):
            for z in range(int(np.ceil((lo[2]-10)/20)), int(np.floor((hi[2]+10)/20))+1):
                local = np.eye(4); local[:3, 3] = [20*x, 0, 20*z]
                yield dict(canonical='3024', matrix=(self.board @ local).tolist())

    def plate_collision(self, p):
        lo, hi = self.bounds_on_plate(p)
        if hi[1] > .002: return True
        if hi[1] < -4.002: return False
        return any(self.q.endpoint(p, cell)['status'] != 'CLEAR' for cell in self.cells(lo, hi))

    def plate_path(self, p, direction, length):
        lo, hi = self.bounds_on_plate(p)
        d = self.inverse_board[:3, :3] @ direction
        if hi[1] + max(0., d[1]*length) > .002: return False
        if max(hi[1], hi[1] + d[1]*length) < -4.002: return True
        travel = length if d[1] >= -1e-6 else min(length, max(0., (hi[1]+4.002)/-d[1]))
        delta = d * travel
        return all(self.q.path({**p, 'direction': direction.tolist()}, cell, length)['status'] == 'CLEAR'
                   for cell in self.cells(lo + np.minimum(delta, 0), hi + np.maximum(delta, 0)))

    def connections(self, state):
        graph, _ = super().connections(state)
        graph[PLATE] = set()
        for a, p in self.present(state).items():
            if self.on_plate(p): graph[PLATE].add(a); graph[a].add(PLATE)
        groups = []; remaining = set(graph)
        while remaining:
            found, todo = set(), [min(remaining)]
            while todo:
                a = todo.pop()
                if a in found: continue
                found.add(a); todo.extend(graph[a]-found)
            groups.append(sorted(found)); remaining -= found
        return graph, groups

    def environment_blockers(self, p):
        return [PLATE] if self.plate_collision(p) else []

    def environment_connections(self, p):
        return [(PLATE, dict(axis=self.board[:3, 1].tolist()))] if self.on_plate(p) else []

    def environment_path_blockers(self, p, direction, length):
        return [] if self.plate_path(p, direction, length) else [PLATE]

    def path_lengths(self, p, direction):
        length = self.cert['extractionLengthLDU']
        d = self.inverse_board[:3, :3] @ direction
        if d[1] > 1e-6:
            # A fixed, long extraction distance would falsely send an already
            # released piece through the plate. Stop above the surface, while
            # still requiring separation from every other piece's bounds.
            available = max(0., (-self.bounds_on_plate(p)[1][1]-.01)/d[1])
            length = min(length, available)
        return list(dict.fromkeys([length, *[v for v in (4.5, 8.5, 12.5, 20.5, 24.5, 32.5) if v < length]]))

    def plate_snaps(self, actor, rotation):
        """Grid-translation templates, independent of all target placements.

        The client translates these by integer stud pitches near its ray/plane
        intersection. Every resulting pose still passes server-side validation.
        """
        base = self.parts[actor]
        alias = np.linalg.inv(np.asarray(base['rawMatrix'])) @ np.asarray(base['matrix'])
        data = info(base['canonical']); local = alias @ data.frames
        r = np.asarray(rotation); poses = {}
        for conn, frame in zip(data.conns, local):
            if not compatible(conn, STUD) or (r @ frame[:3, 1])[1] < .999: continue
            m = np.eye(4); m[:3, :3] = r; m[:3, 3] = -r @ frame[:3, 3]
            # Multiple holes differing by whole stud pitches define the same grid.
            token = tuple(np.round([m[0,3] % 20, m[1,3], m[2,3] % 20], 4))
            poses[token] = dict(rawMatrix=(self.board @ m).tolist(), anchor=self.board[:3,3].tolist(), other=PLATE)
        if not poses or self.baseplate['mounting'] == 'resting':
            r4 = np.eye(4); r4[:3, :3] = r
            points = transformed_vertices(base, r4 @ np.linalg.inv(np.asarray(base['rawMatrix'])))
            foot = points[np.argmax(points[:, 1])]
            m = r4.copy(); m[:3, 3] = -foot + [0, -4.25, 0]
            poses['resting'] = dict(rawMatrix=(self.board @ m).tolist(), anchor=self.board[:3,3].tolist(), other=PLATE)
        return list(poses.values())
