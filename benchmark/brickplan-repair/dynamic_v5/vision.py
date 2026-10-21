"""Dynamic visual interface: visible plate grid and uniform candidate catalog.

The grid is computed from every registered pose, not from a hidden event or
the target. Catalog pages show every option for the inspected actor.
"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from baseplate import PlateAssembly
from vision import VisionRenderer as BaseVisionRenderer, _camera, FONT


class DynamicVisionRenderer(BaseVisionRenderer):
    no_target_isolation = True
    catalog_in_context = False

    def __init__(self, cert, runtime=None):
        super().__init__(cert)
        rt = runtime or PlateAssembly(cert)
        self.board = np.asarray(rt.board)
        inv = np.asarray(rt.inverse_board)
        raw = self.envelope * np.array([1, -1, -1])
        local = (np.c_[raw, np.ones(len(raw))] @ inv.T)[:, :3]
        lo, hi = local.min(0), local.max(0)
        self.grid_x = range(math.floor(lo[0]/20)-1, math.ceil(hi[0]/20)+2)
        self.grid_z = range(math.floor(lo[2]/20)-1, math.ceil(hi[2]/20)+2)

    def _project_board(self, x, z, camera, center, scale, size, crop):
        raw = self.board @ np.array([x, 0, z, 1.])
        point = (raw[:3] * np.array([1, -1, -1])) @ camera
        w, h = size
        left, top, right, bottom = crop or (0., 0., 1., 1.)
        crop_scale = min(1/(right-left), 1/(bottom-top))
        shift_x = ((left+right)/2-.5)*w
        shift_y = ((top+bottom)/2-.5)*h
        return (((point[0]-center[0])*scale-shift_x)*crop_scale+w/2,
                (-(point[1]-center[1])*scale-shift_y)*crop_scale+h/2)

    def rgb(self, state, view='isometric', size=(1600, 1200), only=None,
            angles=None, crop=None, frame_keys=None, supersample=2, fixtures=True):
        image, mask = super().rgb(state, view, size, only, angles, crop,
                                  frame_keys, supersample, fixtures)
        # Individual inventory cards retain a clean neutral background.
        if only is not None or not fixtures:
            return image, mask
        camera = _camera(view, angles)
        envelope = self.envelope if frame_keys is None else np.concatenate(
            [self.bounds[k] for k in frame_keys if k in self.bounds])
        projected = envelope @ camera
        lo, hi = projected.min(0), projected.max(0)
        center = (lo+hi)/2
        w, h = size
        scale = min(w*.88/max(hi[0]-lo[0], 1), h*.88/max(hi[1]-lo[1], 1))
        overlay = Image.new('RGB', size, (246, 246, 246))
        draw = ImageDraw.Draw(overlay)
        xs, zs = list(self.grid_x), list(self.grid_z)
        if len(xs) > 90 or len(zs) > 90:
            return image, mask
        proj = lambda x, z: self._project_board(20*x, 20*z, camera, center, scale, size, crop)
        for x in xs:
            draw.line([proj(x, zs[0]), proj(x, zs[-1])], fill=(225, 228, 231), width=2)
        for z in zs:
            draw.line([proj(xs[0], z), proj(xs[-1], z)], fill=(225, 228, 231), width=2)
        for x in xs:
            for z in zs:
                px, py = proj(x, z)
                if -6 <= px < w+6 and -6 <= py < h+6:
                    draw.ellipse((px-3, py-3, px+3, py+3),
                                 fill=(204, 210, 216), outline=(186, 193, 200))
        pixels = np.asarray(image).copy()
        grid = np.asarray(overlay)
        background = mask == 0
        pixels[background] = grid[background]
        return Image.fromarray(pixels), mask

    def catalog(self, ep, public_actor):
        actor = ep.reverse[public_actor]
        keys = sorted(ep.case['choices'][actor], key=ep.pose)
        pages = []
        for offset in range(0, len(keys), 12):
            group = keys[offset:offset+12]
            page = Image.new('RGB', (1600, math.ceil(len(group)/4)*316), 'white')
            draw = ImageDraw.Draw(page)
            for i, key in enumerate(group):
                x, y = i%4*400, i//4*316
                # Every registered placement is shown with the same camera
                # and envelope, independent of target correctness or legality.
                state = {**ep.assignments(), actor:key} if self.catalog_in_context else {actor:key}
                card, mask = self.rgb(state, size=(400, 288), supersample=1)
                if self.catalog_in_context:
                    actor_mask = Image.fromarray(np.uint8(mask == self.ids[actor])*255)
                    border = Image.fromarray(np.asarray(actor_mask.filter(ImageFilter.MaxFilter(7))) - np.asarray(actor_mask))
                    card.paste((0, 166, 190), (0, 0), border)
                page.paste(card, (x, y+28))
                draw.text((x+8, y+5), public_actor+' / '+ep.pose(key),
                          font=FONT, fill='#17283a')
            pages.append(page)
        return pages
