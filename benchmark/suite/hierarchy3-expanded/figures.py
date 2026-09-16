"""Figures from frozen base views plus new original-site canvas captures."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import json
import time

root = Path(__file__).resolve().parents[3]
out = root / 'benchmark/hierarchy-v3-expanded'
paper = root / 'benchmark/paper/figures'
catalog = json.loads((out / 'catalog.json').read_text())
audit = json.loads((out / 'audit.json').read_text())

def font(size):
    return ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc', size)

def save(image, name):
    image.save(out / f'{name}.png')
    image.save(out / f'{name}.pdf', resolution=180, creationDate=time.gmtime(0), modDate=time.gmtime(0))
    image.save(paper / f'hierarchy-expanded-{name}.png')
    image.save(paper / f'hierarchy-expanded-{name}.pdf', resolution=180, creationDate=time.gmtime(0), modDate=time.gmtime(0))

def sheet(models, columns=6):
    w, h = 340, 270
    image = Image.new('RGB', (columns*w, ((len(models)+columns-1)//columns)*h), '#edf1f4')
    draw = ImageDraw.Draw(image)
    for i, m in enumerate(models):
        x, y = i % columns * w, i // columns * h
        thumb = ImageOps.contain(Image.open(out / 'images' / f'{m["id"]}-iso.png').convert('RGB'), (w-12, h-72))
        image.paste(thumb, (x+(w-thumb.width)//2, y+5))
        title = m['nameZh']
        size = 16 if len(title) < 16 else 13
        draw.text((x+10, y+h-60), f'{m["difficulty"]} · {title}', font=font(size), fill='#1b3549')
        draw.text((x+10, y+h-33), f'{m["parts"]} parts / {m["modules"]} modules / 48 tasks', font=font(14), fill='#455f74')
    return image

for level in ['D1','D2','D3','D4']:
    save(sheet([m for m in catalog if m['difficulty']==level]), f'library-{level}')
save(sheet(catalog), 'library')
selected = [next(m for m in catalog if m['id']==f'exp-d{level}-{kind}-2')
            for level in [1,2,3,4] for kind in ['arm','gantry','wings']]
save(sheet(selected, 3), 'teaser')

image = Image.new('RGB', (1240, 730), 'white')
draw = ImageDraw.Draw(image)
draw.text((22,12), 'Hierarchy-3 expanded: 144 layouts × 48 task families', font=font(29), fill='#183149')
layers = [('atomic','Atomic'),('metacognitive','Meta / physics'),('procedural','Execution'),('integrative','Integration')]
for col, (_, label) in enumerate(layers):
    draw.text((220+col*245, 83), label, font=font(22), fill='#183149')
for row, label in enumerate(['D1 Components','D2 Assemblies','D3 Mechanisms','D4 Systems']):
    draw.text((15,158+row*135), label, font=font(20), fill='#183149')
    for col, (key, _) in enumerate(layers):
        x, y = 210+col*245, 130+row*135
        draw.rounded_rectangle((x,y,x+224,y+114), radius=10, fill=['#dceaf4','#f9edd8','#deeee5','#e8e2f2'][col])
        draw.text((x+16,y+20), f'{audit["byLayer"][key]//4} questions', font=font(26), fill='#183149')
        draw.text((x+16,y+65), '36 sources / level', font=font(17), fill='#455f74')
draw.text((22,697),'Coverage counts, not measured model accuracy.',font=font(18),fill='#455f74')
save(image, 'matrix')
print(json.dumps({'models': len(catalog), 'figures':7}))
