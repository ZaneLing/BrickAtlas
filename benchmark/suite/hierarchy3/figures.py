"""Publication figures composed exclusively from original-site canvas renders and receipts."""
from pathlib import Path
import json
import time
from PIL import Image, ImageFont, ImageDraw, ImageOps

root = Path(__file__).resolve().parents[3]
out = root / 'benchmark/hierarchy-v3'
paper = root / 'benchmark/paper/figures'
catalog = json.loads((out / 'catalog.json').read_text())
pilot = json.loads((out / 'pilot/run.json').read_text()) if (out / 'pilot/run.json').exists() else {'results': []}
font_path = '/System/Library/Fonts/STHeiti Medium.ttc'
def font(size): return ImageFont.truetype(font_path, size)
def save(im, name):
    im.save(out / f'{name}.png')
    im.save(out / f'{name}.pdf', resolution=180, creationDate=time.gmtime(0), modDate=time.gmtime(0))
    im.save(paper / f'{name}.png')
    im.save(paper / f'{name}.pdf', resolution=180, creationDate=time.gmtime(0), modDate=time.gmtime(0))

def overview(per_level, name, label_size):
    w, h = 340, 300
    im = Image.new('RGB', (w * per_level, h * 4), '#edf1f4')
    draw = ImageDraw.Draw(im)
    for row, level in enumerate(['D1', 'D2', 'D3', 'D4']):
        models = [m for m in catalog if m['difficulty'] == level]
        chosen = models if per_level == 12 else [models[i] for i in [0, 4, 8]]
        for col, m in enumerate(chosen):
            image = Image.open(out / 'images' / f"{m['id']}-iso.png").convert('RGB')
            image = ImageOps.contain(image, (w - 12, h - 64))
            x, y = col*w, row*h
            im.paste(image, (x + (w-image.width)//2, y + 5))
            draw.text((x+10, y+h-55), f"{level} · {m['nameZh']}", font=font(label_size), fill='#182d42')
            draw.text((x+10, y+h-26), f"{m['parts']} parts / {m['modules']} modules / 48 tasks", font=font(15), fill='#546b7e')
    save(im, name)
overview(12, 'hierarchy3-library', 17)
overview(3, 'hierarchy3-teaser', 18)

im = Image.new('RGB', (1240, 720), 'white')
draw = ImageDraw.Draw(im)
draw.text((20, 12), 'Hierarchy-3: structural scope × task composition', font=font(30), fill='#183149')
layers = [('atomic', 'Atomic',264), ('metacognitive', 'Meta / physics',180), ('procedural','Execution',72), ('integrative','Integration',60)]
for col, (_, label, _) in enumerate(layers):
    draw.text((220+col*245, 83), label, font=font(22), fill='#183149')
for row, level in enumerate(['D1 Components', 'D2 Assemblies', 'D3 Mechanisms', 'D4 Systems']):
    draw.text((15, 158+row*135), level, font=font(20), fill='#183149')
    for col, (_, _, n) in enumerate(layers):
        x,y=210+col*245, 130+row*135
        draw.rounded_rectangle((x,y,x+224,y+114), radius=10, fill=['#dceaf4','#f9edd8','#deeee5','#e8e2f2'][col])
        draw.text((x+16,y+20), f'{n} questions', font=font(26), fill='#183149')
        draw.text((x+16,y+65), '12 sources / level', font=font(17), fill='#546b7e')
save(im, 'hierarchy3-matrix')

im=Image.new('RGB',(1050,710),'white'); draw=ImageDraw.Draw(im)
draw.text((22,16), 'GPT-4.1 mini · 16-case pipeline pilot',font=font(28),fill='#183149')
for col, (_, label, _) in enumerate(layers):
    draw.text((210+col*205,85),label,font=font(20),fill='#183149')
for row, level in enumerate(['D1','D2','D3','D4']):
    draw.text((50,165+row*120),level,font=font(26),fill='#183149')
    for col, (layer, _, _) in enumerate(layers):
        rows=[r for r in pilot['results'] if r['difficulty']==level and r['layer']==layer]
        successes=sum(r['verdict']['success'] for r in rows)
        x,y=195+col*205,130+row*120
        draw.rectangle((x,y,x+180,y+98),fill=('#79b6a6' if successes else '#e6967f') if rows else '#dce3e8')
        draw.text((x+35,y+20),f'{successes}/{len(rows)}',font=font(28),fill='#183149')
        draw.text((x+30,y+61),'n=1 (pilot)' if rows else 'not measured',font=font(17),fill='#183149')
draw.text((22,665),'Descriptive cells only. Not population accuracy or calibrated difficulty.',font=font(20),fill='#546b7e')
save(im,'hierarchy3-pilot')
print(json.dumps({'models':len(catalog),'pilot':len(pilot['results']),'figures':4}))
