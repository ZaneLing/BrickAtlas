"""Acquire 400 distinct OMR source sets, without claiming physical admission.

Keep original bytes, author/license, source URL, complete leaf inventory and
source thumbnails. One set is one model; no color variants or crops inflate it.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlparse, unquote, urljoin
import hashlib,json,re,subprocess,sys
import numpy as np
from dynamic_arena import ROOT, OUT
from expansion_v7.build import write,read
from dynamic_arena.transport import write_json
TOOLS=ROOT/'benchmark/brickplan-v2.3/source-tools'
sys.path.insert(0,str(TOOLS))
from discover import Document
DEST=ROOT/'assets-source/arena-400'


def fetch(url,path):
    if path.exists():return path.read_bytes()
    assert urlparse(url).netloc=='library.ldraw.org'
    raw=subprocess.check_output(['curl','-fLsS','--connect-timeout','10','--max-time','20','--retry','0',url],stderr=subprocess.DEVNULL,timeout=25)
    path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw);return raw


def flatten(raw):
    text=raw.decode('utf-8-sig');files={};name=None
    if not re.search(r'^0 FILE ',text,re.M|re.I):name='root.ldr';files[name]=[]
    for number,line in enumerate(text.splitlines(),1):
        line=line.strip()
        if line.upper().startswith('0 FILE '):
            name=line[7:].strip().lower().replace('\\','/')
            if name in files:raise ValueError('Duplicate embedded file')
            files[name]=[]
        elif line.upper()=='0 NOFILE':name=None
        elif name:files[name].append((number,line))
    root=next(iter(files));out=[];axis=np.diag([.4,-.4,-.4,1.])
    def walk(name,parent,color,stack):
        if name in stack:raise ValueError('Cyclic source')
        for number,line in files[name]:
            if not re.match(r'^1\s',line):continue
            t=line.split();v=list(map(float,t[2:14]));m=np.eye(4);m[:3,3]=v[:3];m[:3,:3]=np.array(v[3:]).reshape(3,3)
            if not np.isfinite(m).all():raise ValueError('Nonfinite transform')
            world=parent@m;c=color if t[1]=='16' else t[1];child=' '.join(t[14:]).lower().replace('\\','/')
            if child in files and (child.endswith(('.ldr','.mpd')) or any('!LDRAW_ORG Model' in l for _,l in files[child])):walk(child,world,c,(*stack,name))
            else:out.append(dict(instanceId=f'brick_{len(out)+1:06}',index=len(out),partNumber=child.removesuffix('.dat'),colorCode=c,originalMatrix=(axis@world).T.ravel().tolist(),sourceFile=name,sourceLine=number))
    walk(root,np.eye(4),'7',())
    header='\n'.join(l for _,l in files[root]);author=re.search(r'^0 Author:\s*(.+)$',header,re.M);license_=re.search(r'^0 !LICENSE\s*(.+)$',header,re.M)
    if not author or not license_:raise ValueError('Missing author/license')
    return out,author.group(1),license_.group(1)


def acquire(row):
    number=row['setNumber'];folder=DEST/number
    try:
        raw=fetch(row['sourceUrl'],folder/'page.html');doc=Document(raw).root;options=[]
        for a in doc.all('a'):
            url=a.attrs.get('href','')
            if not (url.startswith('https://library.ldraw.org/library/omr/') or url.startswith('https://library.ldraw.org/media/omr_models/')) or not urlparse(url).path.lower().endswith(('.mpd','.ldr')):continue
            node=a.parent
            while node.parent and not all(k in node.text() for k in ['Author:','Missing Parts','Missing Patterns','Missing Stickers']):node=node.parent
            label=node.text()
            if not re.search(r'Missing Parts\s+No',label):continue
            thumb=next((i.attrs.get('src') for i in doc.all('img') if '/omr_models/'+urlparse(url).path.split('/')[-2]+'/' in i.attrs.get('src','')),None)
            options.append((0 if 'Main Model' in label else 1,url,thumb,label))
        if not options:raise ValueError('No complete source model listed')
        _,url,thumb,label=sorted(options)[0];name=Path(unquote(urlparse(url).path)).name
        raw=fetch(url,folder/name);instances,author,license_=flatten(raw)
        if not 4<=len(instances)<=250:raise ValueError(f'Complete model has {len(instances)} parts; outside 4–250 source intake range')
        shape=hashlib.sha256(json.dumps(sorted((p['partNumber'],p['colorCode'],p['originalMatrix']) for p in instances),separators=(',',':')).encode()).hexdigest()
        mid='arena-omr-'+number
        thumbnail=None
        if thumb:
            thumb=urljoin(row['sourceUrl'],thumb)
            try:
                data=fetch(thumb,folder/'preview.png')
                from PIL import Image
                import io
                im=Image.open(io.BytesIO(data));im.thumbnail((640,480));im.convert('RGB').save(folder/'thumbnail.jpg',quality=90)
                thumbnail=str((folder/'thumbnail.jpg').relative_to(ROOT))
            except Exception:pass
        manifest=dict(schema='brick-atlas-omr-source/1',model=dict(id=mid,setNumber=number,title=row['title'],author=author,license=license_,sourceUrl=row['sourceUrl'],downloadUrl=url),sourceFile=str((folder/name).relative_to(ROOT)),sourceHash=hashlib.sha256(raw).hexdigest(),instances=instances,instancesDropped=0,sourceGeometryModified=False)
        write(folder/'manifest.json',manifest)
        return dict(id=mid,setNumber=number,title=row['title'],parts=len(instances),theme=row['theme'],author=author,license=license_,sourceUrl=row['sourceUrl'],downloadUrl=url,sourceFile=manifest['sourceFile'],sourceHash=manifest['sourceHash'],shapeHash=shape,sourceCompleteness={k:re.search(k+r'\s+(Yes|No)',label).group(1) if re.search(k+r'\s+(Yes|No)',label) else None for k in ['Missing Parts','Missing Patterns','Missing Stickers']},manifest=str((folder/'manifest.json').relative_to(ROOT)),thumbnail=thumbnail,status='source-complete-awaiting-assembly-check',arenaTaskCount=0,completeObject=True)
    except Exception as e:return dict(setNumber=number,rejected=str(e)[:200])


def existing():
    rows={}
    for p in sorted((ROOT/'web/public/models').glob('*/manifest.json')):
        m=read(p);md=m.get('model',{});number=md.get('setNumber')
        if not number:
            found=re.search(r'\d{4,7}',p.parent.name)
            if not found:continue
            number=found.group()+'-1'
        if number in ('21004-1','21007-1'):continue
        # Earlier source manifests used sourceSet rather than setNumber.
        if number in rows:continue
        rows[number]=dict(id=p.parent.name,setNumber=number,title=md.get('title',p.parent.name),parts=len(m['instances']),sourceUrl=md.get('sourceUrl',md.get('url')),author=md.get('author'),license=md.get('license'),manifest=str(p.relative_to(ROOT)),sourceFile=m.get('sourceFile'),sourceHash=m.get('sourceHash'),status='existing-source; see task-level qualification',arenaTaskCount=None,completeObject=True)
    return list(rows.values())


def main():
    if (OUT/'source-curation.json').exists():
        raise SystemExit('Curation is active. Use dynamic_arena.curate_sources; the old fill-to-400 importer is disabled.')
    DEST.mkdir(parents=True,exist_ok=True);out=OUT/'source-library.json'
    prior=read(out) if out.exists() else dict(models=existing(),rejected=[])
    selected=prior['models'];seen={r['setNumber'] for r in selected};hashes={r.get('shapeHash') for r in selected}
    index=ROOT/'tem/research/20261010-brickplan-v23-diversity/source-intake/index'
    if not index.exists():index=TOOLS.parent/'data/source-intake/index'
    candidates=[r for p in index.glob('*.json') for r in read(p)]
    if candidates:write(DEST/'source-candidates.json',candidates)
    else:candidates=read(DEST/'source-candidates.json')
    def priority(r):
        theme=r['theme'];title=r['title'].lower();num=int(r['setNumber'].split('-')[0]);year=int(r['year']) if r['year'].isdigit() else 2000
        return (0 if any(k in title for k in ['mini ','small ','little ','polybag']) or 30000<=num<31000 else 1 if theme.startswith(('Town','City','Creator','Racers','Train','Basic')) else 2,year,num)
    candidates=sorted({r['setNumber']:r for r in candidates if r['setNumber'] not in seen and r['setNumber'] not in ('21004-1','21007-1')}.values(),key=priority)
    def save():
        write_json(out,dict(schema='brick-atlas-source-library/1',count=len(selected),countUnit='distinct official source set; one selected complete model per set',models=selected,rejected=prior['rejected'],newSourceCount=sum(r['id'].startswith('arena-omr-') for r in selected),note='Source count is NOT the number of physically qualified Arena objects. New sources need connector/path, normal-build and image/human checks.'))
    with ThreadPoolExecutor(max_workers=8) as pool:
        for offset in range(0,len(candidates),16):
            if len(selected)>=400:break
            batch=candidates[offset:offset+min(16,400-len(selected))]
            for r in pool.map(acquire,batch):
                if 'rejected' in r:prior['rejected'].append(r)
                elif r.get('shapeHash') in hashes:prior['rejected'].append(dict(setNumber=r['setNumber'],rejected='duplicate complete geometry'))
                else:selected.append(r);seen.add(r['setNumber']);hashes.add(r.get('shapeHash'));print('SOURCE',len(selected),r['setNumber'],r['parts'],r['title'],flush=True)
            save()
    save();print('TOTAL',len(selected),flush=True)


if __name__=='__main__':main()
