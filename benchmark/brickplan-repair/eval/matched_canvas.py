"""Equal scene rectangles on one canvas; captions never overwrite scene pixels.

This deliberately leaves the historical v3/v5 image builders unchanged.
"""
from PIL import Image, ImageDraw
from render import FONT

SCENE_SIZE = (800, 600)
CANVAS_SIZE = (1600, 636)
RECTS = [[0, 36, 800, 636], [800, 36, 1600, 636]]


def comparison(renderer, left, right, view, left_label, right_label, **kwargs):
    page = Image.new('RGB', CANVAS_SIZE, 'white')
    for state, rect in zip((left, right), RECTS):
        scene = renderer.rgb(state, view, size=SCENE_SIZE, supersample=1, **kwargs)[0]
        page.paste(scene, (rect[0], rect[1]))
    draw = ImageDraw.Draw(page)
    draw.rectangle((0, 0, 1599, 35), fill=(27, 43, 57))
    for x, label in ((16, left_label), (816, right_label)):
        draw.text((x, 8), label, font=FONT, fill='white')
    return page


def panels(left, right):
    return [dict(role=role, rectanglePixels=rect) for role, rect in zip((left, right), RECTS)]
