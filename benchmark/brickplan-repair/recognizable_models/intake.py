"""Acquire small complete source files, including single-model LDR syntax."""
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from pathlib import Path
import json
import re
import subprocess
import zipfile
import numpy as np

from recognizable_models import ROOT, OUT
from expansion_v7.build import read, write

LOCKED=ROOT/'assets-source/ldraw-library/locked'
ORIGINAL=ROOT/'assets-source/brickplan-recognizable/original'
SOURCES=[('4016-1','Racer',134),('4017-1','Sea Helicopter',135),
         ('4019-1','Aeroplane',137),('4002-1','Riptide Racer',670),('4005-1','Tug Boat',671)]
SOURCES += [('4037-1','Helicopter',154),('4903-1','Lion',156),
            ('4904-1','Elephant',157),('4905-1','Giraffe',158),('4906-1','Helicopter',155)]


def lock_embedded_parts(path):
    """Make original MPD DAT definitions resolvable without changing geometry.

    OMR names these parts with the source set prefix. A conflicting definition
    is an intake error; never overwrite another source's geometry.
    """
    files={};current=None
    for raw in path.read_text(encoding='utf-8-sig').splitlines():
        line=raw.strip()
        if line.upper().startswith('0 FILE '):
            current=line[7:].lower().replace('\\','/');files[current]=[]
        elif line.upper()=='0 NOFILE':current=None
        elif current:files[current].append(raw)
    audit=[]
    for name,lines in files.items():
        if not name.endswith('.dat'):continue
        if '..' in Path(name).parts or Path(name).is_absolute():raise ValueError('Unsafe embedded part name')
        dest=LOCKED/'parts'/name;data=('\n'.join(lines)+'\n').encode()
        if dest.exists() and dest.read_bytes().strip()!=data.strip():
            raise ValueError('Conflicting embedded part definition: '+name)
        dest.parent.mkdir(parents=True,exist_ok=True)
        if not dest.exists():dest.write_bytes(data)
        audit.append(dict(name=name,path=str(dest.relative_to(ROOT)),sha256=sha256(dest.read_bytes()).hexdigest(),source=str(path.relative_to(ROOT))))
    return audit


def acquire(row):
    number,title,page=row;path=ORIGINAL/(number+'.mpd')
    url='https://library.ldraw.org/library/omr/'+path.name
    if not path.exists():
        result=subprocess.run(['curl','-fLsS','--connect-timeout','8','--max-time','25','--retry','1',url],capture_output=True)
        if result.returncode:return dict(set=number,status='download-failed',reason=result.stderr.decode()[-200:])
        data=result.stdout
        if not re.search(rb'^1\s+\S+\s+[-.\d]',data,re.M):
            return dict(set=number,status='invalid-source',bytes=len(data))
        path.write_bytes(data)
    data=path.read_bytes()
    return dict(set=number,title=title,pageUrl=f'https://library.ldraw.org/omr/sets/{page}',
                file=str(path.relative_to(ROOT)),url=url,bytes=len(data),sha256=sha256(data).hexdigest(),status='downloaded')


def ingest(record,model_prefix='r-omr-'):
    path=ROOT/record['file'];source=path.read_text(encoding='utf-8-sig');files={};current=None
    embedded=lock_embedded_parts(path)
    has_mpd=bool(re.search(r'^0 FILE ',source,re.M|re.I))
    if not has_mpd:current=path.name.lower();files[current]=[]
    for line_no,raw in enumerate(source.splitlines(),1):
        line=raw.strip()
        if line.upper().startswith('0 FILE '):
            current=line[7:].lower().replace('\\','/');files[current]=[]
        elif line.upper()=='0 NOFILE':current=None
        elif current:files[current].append((line_no,line))
    root=next(iter(files));dependencies={};visited=set()
    with zipfile.ZipFile(ROOT/'assets-source/ldraw-library/complete.zip') as archive:
        archive_names={n.lower().removeprefix('ldraw/'):n for n in archive.namelist()}
        def content(name):
            if name in files:return '\n'.join(l for _,l in files[name])
            choices=['parts/'+name,'p/'+name,name]
            relative=next((n for n in choices if (LOCKED/n).is_file()),None)
            if relative is None:
                relative=next((n for n in choices if n in archive_names),None)
                if relative is None:raise FileNotFoundError(name)
                dest=LOCKED/relative;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(archive.read(archive_names[relative]))
            data=(LOCKED/relative).read_bytes();dependencies[str((LOCKED/relative).relative_to(ROOT))]=sha256(data).hexdigest()
            return data.decode('utf-8-sig')
        def visit(name):
            if name in visited:return
            if '..' in Path(name).parts or Path(name).is_absolute():raise ValueError('Unsafe LDraw dependency')
            visited.add(name)
            for line in content(name).splitlines():
                cols=line.split()
                if cols and cols[0]=='1':visit(' '.join(cols[14:]).lower().replace('\\','/'))
        visit(root)
        palette=dict(re.findall(r'CODE\s+(\d+)\s+VALUE\s+(#[0-9a-fA-F]{6})',(LOCKED/'LDConfig.ldr').read_text()))
        instances=[];axis=np.diag([.4,-.4,-.4,1.])
        def walk(name,parent,inherited,stack,instance_stack=()):
            if name in stack:raise ValueError('Cyclic model')
            step=0
            for line_no,line in files[name]:
                if line.upper()=='0 STEP':step+=1
                if not line.startswith('1 '):continue
                cols=line.split();values=list(map(float,cols[2:14]));m=np.eye(4)
                m[:3,3]=values[:3];m[:3,:3]=np.asarray(values[3:]).reshape(3,3)
                world=parent@m;color=inherited if cols[1]=='16' else cols[1]
                child=' '.join(cols[14:]).lower().replace('\\','/')
                if child in files and (child.endswith(('.ldr','.mpd')) or any('!LDRAW_ORG Model' in l for _,l in files[child])):
                    walk(child,world,color,(*stack,name),(*instance_stack,f'{name}@{line_no}:{child}'));continue
                n=len(instances);text=content(child)
                description=next((l[2:] for l in text.splitlines() if l.startswith('0 ')),child)
                instances.append(dict(instanceId=f'brick_{n+1:06}',index=n,partNumber=child.removesuffix('.dat'),
                    colorCode=color,colorHex=palette[color],displayName=description,
                    originalMatrix=(axis@world).T.ravel().tolist(),sourceFile=name,sourceLine=line_no,
                    sourceStep=step,sourceSubmodelPath=list(stack)+[name],sourceSubmodelInstancePath=list(instance_stack),embeddedPart=child in files))
        walk(root,np.eye(4),'7',())
    text='\n'.join(l for _,l in files[root]);author=re.search(r'^0 Author:\s*(.+)$',text,re.M).group(1)
    license_text=re.search(r'^0 !LICENSE\s*(.+)$',text,re.M).group(1)
    mid=model_prefix+record['set'];dest=ROOT/'web/public/models'/mid
    manifest=dict(schema='recognizable-source/1',model=dict(id=mid,setNumber=record['set'],title=record['title'],
        author=author,license=license_text,sourceUrl=record['pageUrl'],downloadUrl=record['url']),
        sourceFile=record['file'],sourceHash=record['sha256'],instances=instances,instancesDropped=0,
        sourceGeometryModified=False,sourceFileSyntax='MPD' if has_mpd else 'single model; original bytes unchanged')
    dest.mkdir(parents=True,exist_ok=True)
    write(dest/'manifest.json',manifest)
    write(dest/'provenance.json',dict(model=manifest['model'],source=dict(path=record['file'],sha256=record['sha256']),
        completeSourceRetained=True,sourceGeometryModified=False,sourceInstances=len(instances),embeddedParts=embedded,embeddedPartLockedPathConflicts=[]))
    write(OUT/'source-dependencies'/f'{mid}.json',dependencies)
    print('INTAKE',mid,len(instances),'parts',flush=True)


def main():
    ORIGINAL.mkdir(parents=True,exist_ok=True)
    with ThreadPoolExecutor(max_workers=5) as pool:records=list(pool.map(acquire,SOURCES))
    write(ROOT/'assets-source/brickplan-recognizable/downloads.json',records)
    for row in records:
        if row['status']=='downloaded':ingest(row)
        else:print('DOWNLOAD',row,flush=True)


if __name__=='__main__':main()
