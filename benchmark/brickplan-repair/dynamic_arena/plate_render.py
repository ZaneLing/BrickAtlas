"""Render the existing white stud baseplate as a visible solid plate patch.

The physical baseplate remains infinite. The bounded patch is purely a camera
visualization; it never changes placements, collisions or scoring.
"""
import numpy as np
from PIL import Image, ImageDraw
from dynamic_v5.vision import DynamicVisionRenderer
from vision import _camera


class ArenaVision(DynamicVisionRenderer):
    def rgb(self, state, view='isometric', size=(1600, 1200), only=None,
            angles=None, crop=None, frame_keys=None, supersample=2, fixtures=True):
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
        x0, x1 = xs[xmargin] - .15, xs[-1-xmargin] + .15
        z0, z1 = zs[zmargin] - .15, zs[-1-zmargin] + .15
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
        for x in xs:
            if not x0 < x < x1: continue
            for z in zs:
                if not z0 < z < z1: continue
                px, py = project(x, 0, z)
                radius = max(2, min(6, int(scale * 3.8)))
                draw.ellipse((px-radius, py-radius, px+radius, py+radius),
                             fill=(250, 252, 252), outline=(181, 194, 199), width=1)
                draw.arc((px-radius, py-radius, px+radius, py+radius), 195, 325,
                         fill=(255, 255, 255), width=2)
        # Geometry rendered by the real scene renderer is the foreground.
        board.paste(image, (0, 0), Image.fromarray(np.uint8(mask > 0) * 255))
        return board, mask
