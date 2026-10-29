"""Evidence-based whole-source withdrawal and diversity-aware OMR intake.

Never remove individual figure parts to make a source pass. Unresolved part
headers are withheld for review, not counted as figure-free.
"""
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from pathlib import Path
import argparse, json, re, zipfile
from dynamic_arena import ROOT, OUT
from dynamic_arena.source_library import acquire, fetch, Document, DEST
from expansion_v7.build import read, write

BODY = re.compile(r'\b(?:Minifig (?:Statuette|Head(?:\s|$)|Torso|Hips|Leg(?:\s|$)|Arm (?:Left|Right)|Hand(?:\s*\(|\s*$))|Figure Friends (?:(?:Girl |Boy |Female |Male )?(?:Head|Torso|Hips|Legs|Left Arm|Right Arm)|Hair)|Minidoll|Mini Doll|Fabuland (?:Figure|Head|Torso|Body)|(?:Technic|Duplo|Belville|Scala) (?:Figure|Head|Torso)|Figure (?:Head|Torso|Body))', re.I)
RULES = [
 ('animal',r'animal|reindeer|elephant|giraffe|alligator|bear|pug|bee\b|butterfly|crab|scorpion|pteranodon|duck|cow\b|impala|bison|turkey|bat\b|dinosaur|apatosaurus|dragon|bird|parrot|pelican|sheep|frog|fish|shark|creature|rabbit|bunny|dog\b|cat\b|lion|tiger|panda|penguin|turtle|monkey|puppy|rooster|t-rex|stegosaurus'),
 ('plant-food',r'wreath|pear|orange|melon|flower|tree\b|mango|apple\b|pumpkin|fruit|carrot|pineapple|cherry'),
 ('house-building',r'gate|hotel|memorial|palace|louvre|headquarters|villa|fallingwater|sungnyemun|marina bay|trafalgar|store|house|cabin|cottage|lighthouse|building|windmill|tower|bridge|castle|church|temple'),
 ('furniture-object',r'chair|table|desk|clock|camera|skate|piano|guitar|gramophone|telephone|flag|fountain|mailbox|bench|lamp'),
 ('robot-machine',r'wall.e|telehandler|xerion|backhoe|construction|dumper|robot|machine|crane|excavator|digger|bulldozer|forklift|tractor|loader|roller|dynamo'),
 ('railway',r'tender|tanker|train|wagon|rail|caboose|locomotive|metroliner|engine|hopper'),
 ('boat',r'maersk|ocean|boat|ship|yacht|sail|catamaran|tug|raft|canoe|kayak|submarine'),
 ('aircraft',r'sopwith|propellor|aero pod|plane|aircraft|helicopter|soarer|flyer|jet\b|rotor|glider'),
 ('spacecraft',r'apollo|tie interceptor|slave i|droid|aat|star wars|space|shuttle|rocket|fighter|wing|destroyer|speeder|at-st|at-at'),
 ('road-vehicle',r'cooper|mustang|harley|ferrari|aston martin|f40|fxx|berlinetta|tumbler|batmobile|wheels|auto pod|rally|terrain crusher|track marshal|car\b|truck|racer|race|road|jeep|buggy|coupe|convertible|cruiser|pickup|transport|speed|motor|cycle|bus\b|kart|van\b|vehicle'),
]
DIVERSITY_HOLD={'2134-1':'与本轮小牛的身体结构相近，优先保留已通过拆装检查的小牛。','3219-1':'与 8028-1 同为 TIE Fighter，本轮只保留一个清楚预览。','4484-1':'一个来源同时包含两个独立飞行器，本轮优先单一完整物件。','4486-1':'一个来源同时包含两个独立物件，本轮优先单一完整物件。','40013-1':'人形幽灵角色，本轮优先非人形日常物件与动物。'}

def category(row):
    title=row['title'].lower()
    if 'Star Wars' in row.get('theme',''):return 'spacecraft'
    if 'Architecture' in row.get('theme',''):return 'house-building'
    caption=(row.get('sourceModelName') or '').lower()
    if caption and caption!='main model' and any(re.search(p,caption) for _,p in RULES):title=caption
    if re.search(r'\b(?:house|hotel|cafe|school|apartment|building|cottage|castle)\b',title):return 'house-building'
    if 'cherry picker' in title:return 'robot-machine'
    if 'racer' in title:return 'road-vehicle'
    for cat,pat in RULES:
        if re.search(pat,title):return cat
    return 'other'

class FigureAudit:
    def __init__(self):
        self.zip=zipfile.ZipFile(ROOT/'assets-source/ldraw-library/complete.zip')
        self.names=set(self.zip.namelist())
    @lru_cache(maxsize=None)
    def library(self,name):
        for relative in ('parts/'+name,'p/'+name,name):
            path=ROOT/'assets-source/ldraw-library/locked'/relative
            if path.exists():return path.read_text(errors='replace')
            key='ldraw/'+relative
            if key in self.names:return self.zip.read(key).decode('utf8',errors='replace')
        return None
    def audit(self,row):
        mf=read(ROOT/row['manifest']);embedded={};source=row.get('sourceFile') or mf.get('sourceFile')
        if source and (ROOT/source).exists():
            raw=(ROOT/source).read_text(errors='replace');name=None
            for line in raw.splitlines():
                if line.upper().startswith('0 FILE '):name=line[7:].strip().lower().replace('\\','/');embedded[name]=[]
                elif name:embedded[name].append(line)
        evidence=[];unresolved=[]
        def inspect(name,seen):
            name=name.lower().replace('\\','/')
            if name in seen:return
            seen.add(name)
            raw='\n'.join(embedded[name]) if name in embedded else self.library(name)
            if raw is None:unresolved.append(name);return
            desc=next((l[2:].strip() for l in raw.splitlines() if l.startswith('0 ') and not l.startswith(('0 Name:','0 Author:','0 !'))),'')
            if BODY.search(desc):evidence.append(dict(part=name,description=desc));return
            # Follow aliases and assemblies, not merely top-level names.
            for l in raw.splitlines():
                t=l.split()
                if len(t)>=15 and t[0]=='1':inspect(' '.join(t[14:]),seen)
        for p in mf['instances']:
            name=p['partNumber'].lower().removesuffix('.dat')+'.dat'
            desc=p.get('displayName','')
            if BODY.search(desc):evidence.append(dict(part=name,description=desc))
            if name not in embedded and self.library(name) is None and not desc:unresolved.append(name)
            inspect(name,set())
        evidence=list({x['part']:x for x in evidence}.values())
        return dict(status='contains-figure' if evidence else 'unresolved' if unresolved else 'no-figure-parts-found',evidence=evidence,unresolved=sorted(set(unresolved)))

def refresh_index():
    def page(n):
        try:raw=fetch(f'https://library.ldraw.org/omr/sets?page={n}',DEST/'curation-index'/f'{n:02}.html')
        except Exception:return []
        rows=[]
        for tr in Document(raw).root.all('tr'):
            cells=list(tr.all('td'))
            if len(cells)!=6:continue
            t=[c.text() for c in cells]
            if not re.fullmatch(r'\d+-\d+',t[1]):continue
            rows.append(dict(zip(('setNumber','title','theme','year','modelCount'),t[1:]),sourceUrl=next(cells[1].all('a')).attrs['href']))
        return rows
    with ThreadPoolExecutor(max_workers=8) as pool:
        rows=[r for rs in pool.map(page,range(1,60)) for r in rs]
    rows=list({r['setNumber']:r for r in read(DEST/'source-candidates.json')+rows}.values())
    write(DEST/'source-candidates-current.json',rows);return rows

def main():
    p=argparse.ArgumentParser();p.add_argument('--acquire',type=int,default=0);p.add_argument('--refresh',action='store_true');args=p.parse_args()
    path=OUT/'source-library.json';data=read(path);baseline=OUT/'source-library-before-curation.json'
    if not baseline.exists():write(baseline,data)
    audit=FigureAudit();reportpath=OUT/'source-curation.json'
    report=read(reportpath) if reportpath.exists() else dict(schema='brick-atlas-source-curation/1',withdrawn=[],candidateRejected=[],screened=[])
    rows=[];removed={r['setNumber']:r for r in report['withdrawn']}
    for r in data['models']:
        check=audit.audit(r);r['figureAudit']=check;r['objectCategory']=category(r);r['addedAfterFigureCuration']=r['setNumber'] not in {b['setNumber'] for b in read(baseline)['models']}
        if check['status']=='no-figure-parts-found' and r['addedAfterFigureCuration'] and (r['setNumber'] in DIVERSITY_HOLD or not r.get('thumbnail')):
            removed[r['setNumber']]=dict(**r,withdrawalReason=DIVERSITY_HOLD.get(r['setNumber'],'尚无可核对的完整预览，先留在候选层。'));continue
        if check['status']=='no-figure-parts-found':rows.append(r)
        else:removed[r['setNumber']]=dict(**r,withdrawalReason=check['status'])
    candidates=refresh_index() if args.refresh else read(DEST/('source-candidates-current.json' if (DEST/'source-candidates-current.json').exists() else 'source-candidates.json'))
    seen={r['setNumber'] for r in rows}|set(removed)|{r['setNumber'] for r in report['candidateRejected']}
    choices=[r for r in candidates if r['setNumber'] not in seen and r['setNumber'] not in ('21004-1','21007-1')]
    counts=Counter(category(r) for r in rows)
    # Prefer recognizable complete small objects in underrepresented categories.
    # No arbitrary count target: disallowed figures or unreadable sources cannot fill a quota.
    buckets={}
    for r in choices:buckets.setdefault(category(r),[]).append(r)
    for bucket in buckets.values():bucket.sort(key=lambda r:(not any(x in r['theme'] for x in ['Creator','Basic','Seasonal']),r['setNumber']))
    choices=[]
    while any(buckets.values()):
        for cat in sorted(buckets,key=lambda c:(c=='other',counts[c])):
            if buckets[cat]:choices.append(buckets[cat].pop(0))
    def save():
        report['withdrawn']=list(removed.values());report['activeCount']=len(rows);report['byCategory']=dict(Counter(r['objectCategory'] for r in rows));report['apiCalls']=0
        data.update(models=rows,count=len(rows),newSourceCount=sum(r['id'].startswith('arena-omr-') for r in rows),curation='source-curation.json',note='Curated active sources, not a claim of Arena qualification. Entire figure-containing sources are withdrawn. Original files retained as historical evidence.')
        write(path,data);write(reportpath,report)
    save();print('CURATED',len(rows),'WITHDRAWN',len(removed),flush=True)
    with ThreadPoolExecutor(max_workers=8) as pool:
        for start in range(0,min(args.acquire,len(choices)),16):
            for r in pool.map(acquire,choices[start:start+min(16,args.acquire-start)]):
                if 'rejected' in r:report['candidateRejected'].append(r);continue
                check=audit.audit(r);r['figureAudit']=check;r['objectCategory']=category(r);r['addedAfterFigureCuration']=r['setNumber'] not in {b['setNumber'] for b in read(baseline)['models']}
                if check['status']!='no-figure-parts-found':removed[r['setNumber']]=dict(**r,withdrawalReason=check['status']);continue
                if r.get('shapeHash') in {x.get('shapeHash') for x in rows}:report['candidateRejected'].append(dict(setNumber=r['setNumber'],rejected='duplicate complete geometry'));continue
                if r['setNumber'] in DIVERSITY_HOLD or not r.get('thumbnail'):
                    removed[r['setNumber']]=dict(**r,withdrawalReason=DIVERSITY_HOLD.get(r['setNumber'],'尚无可核对的完整预览，先留在候选层。'));continue
                rows.append(r);report['screened'].append(r['setNumber']);print('ADDED',r['setNumber'],r['parts'],r['objectCategory'],r['title'],flush=True)
            save()
    save()

if __name__=='__main__':main()
