"""Render the existing white stud baseplate as a visible solid plate patch.

The physical baseplate remains infinite. The bounded patch is purely a camera
visualization; it never changes placements, collisions or scoring.
"""
import math
import numpy as np
from PIL import Image, ImageDraw
from dynamic_v5.vision import DynamicVisionRenderer
from vision import _camera


class ArenaVision(DynamicVisionRenderer):
    def __init__(self, cert, runtime=None):
        super().__init__(cert, runtime)
        plate = (runtime.baseplate if runtime is not None else {})
        # Geometry is in LDraw units; the grid and project() use 20 units/stud.
        self.stud_radius = plate.get('studRadius', 6) / plate.get('pitch', 20)
        self.stud_height = plate.get('studHeight', 4)

    def rgb(self, state, view='isometric', size=(1600, 1200), only=None,
            angles=None, crop=None, frame_keys=None, supersample=2, fixtures=True):
        # The physical plate extends beyond the object's envelope. Give both
        # the object renderer and plate projection identical camera headroom.
        if crop is None and only is None and fixtures:
            crop = (-.12, -.12, 1.12, 1.12)
        image, mask = super().rgb(state, view, size, only, angles, crop,
                                  frame_keys, supersample, fixtures)
        if only is not None or not fixtures:
            return image, mask
        camera = _camera(view, angles)
        envelope = self.envelope if frame_keys is None else np.concatenate(
            [self.bounds[k] for k in frame_keys if k in self.bounds])
        projected = envelope @ camera
        lo, hi = projected.min(0), projected.max(0)
        center = (lo + hi) / 2
        w, h = size
        scale = min(w * .88 / max(hi[0] - lo[0], 1), h * .88 / max(hi[1] - lo[1], 1))
        left, top, right, bottom = crop or (0., 0., 1., 1.)
        zoom = min(1 / (right - left), 1 / (bottom - top))
        sx = ((left + right) / 2 - .5) * w
        sy = ((top + bottom) / 2 - .5) * h

        def project(x, y, z):
            world = self.board @ np.array([20 * x, y, 20 * z, 1.])
            p = (world[:3] * [1, -1, -1]) @ camera
            return (((p[0] - center[0]) * scale - sx) * zoom + w / 2,
                    (-(p[1] - center[1]) * scale - sy) * zoom + h / 2)

        xs, zs = list(self.grid_x), list(self.grid_z)
        # One finite visible window of the infinite white LEGO baseplate.
        xmargin = max(1, len(xs) // 4)
        zmargin = max(1, len(zs) // 4)
        # Leave half a pitch at the edge, as on a real studded plate.
        x0, x1 = xs[xmargin] - .5, xs[-1-xmargin] + .5
        z0, z1 = zs[zmargin] - .5, zs[-1-zmargin] + .5
        corners = [(x0, z0), (x1, z0), (x1, z1), (x0, z1)]
        top_points = [project(x, 0, z) for x, z in corners]
        lower_points = [project(x, 8, z) for x, z in corners]
        board = Image.new('RGB', size, (243, 246, 247))
        draw = ImageDraw.Draw(board)
        for i in range(4):
            j = (i + 1) % 4
            draw.polygon([top_points[i], top_points[j], lower_points[j], lower_points[i]],
                         fill=(209, 218, 220), outline=(172, 184, 188))
        draw.polygon(top_points, fill=(255, 255, 255), outline=(154, 170, 175), width=2)
        # Raised, solid cylindrical studs. Draw distant studs first so their
        # sidewalls and top rims occlude correctly at low camera elevations.
        plate_studs = [(x, z) for x in xs for z in zs if x0 < x < x1 and z0 < z < z1]
        def depth(x, z):
            world = (self.board @ np.array([20*x, 0, 20*z, 1.]))[:3] * [1, -1, -1]
            return world @ camera[:, 2]
        plate_studs.sort(key=lambda p: depth(*p))
        ring = [(math.cos(i * math.tau / 20), math.sin(i * math.tau / 20))
                for i in range(20)]
        for x, z in plate_studs:
            lower = [project(x + self.stud_radius*dx, 0, z + self.stud_radius*dz)
                     for dx, dz in ring]
            upper = [project(x + self.stud_radius*dx, -self.stud_height,
                             z + self.stud_radius*dz) for dx, dz in ring]
            faces = []
            for i in range(len(ring)):
                j = (i + 1) % len(ring)
                midpoint = (ring[i][0] + ring[j][0], ring[i][1] + ring[j][1])
                face_depth = depth(x + self.stud_radius*midpoint[0]/2,
                                   z + self.stud_radius*midpoint[1]/2)
                faces.append((face_depth, i, j))
            for _, i, j in sorted(faces):
                shade = 222 + int(17 * ring[i][0] + 7 * ring[i][1])
                shade = min(245, max(202, shade))
                draw.polygon([lower[i], lower[j], upper[j], upper[i]],
                             fill=(shade, shade+2, shade+3))
            draw.polygon(upper, fill=(252, 253, 253),
                         outline=(150, 164, 169), width=1)
        # Geometry rendered by the real scene renderer is the foreground.
        board.paste(image, (0, 0), Image.fromarray(np.uint8(mask > 0) * 255))
        return board, mask
