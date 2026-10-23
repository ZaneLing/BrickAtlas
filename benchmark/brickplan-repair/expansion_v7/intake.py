"""Flatten pinned OMR files without changing poses or dropping source parts."""
from pathlib import Path
import hashlib
import json
import re
import zipfile
import numpy as np
from expansion_v7 import ROOT, OUT

LOCKED = ROOT / 'assets-source/ldraw-library/locked'


def ensure_dependencies(path):
    """Extract missing files only from the existing hash-pinned library archive."""
    archive=ROOT/'assets-source/ldraw-library/complete.zip'
    source=path.read_text(encoding='utf-8-sig')
    embedded={};current=None
    for line in source.splitlines():
        if line.upper().startswith('0 FILE '):
            current=line[7:].strip().lower().replace('\\','/');embedded[current]=[]
        elif current and line.upper()!='0 NOFILE':embedded[current].append(line)
    records={};visited=set()
    with zipfile.ZipFile(archive) as z:
        names={n.lower().removeprefix('ldraw/'):n for n in z.namelist()}
        def visit(name):
            name=name.lower().replace('\\','/')
            if name in visited:return
            visited.add(name)
            if '..' in Path(name).parts or Path(name).is_absolute():raise ValueError('Unsafe dependency path')
            if name in embedded and name.endswith('.ldr'):
                content='\n'.join(embedded[name]);relative=None
            else:
                options=['parts/'+name,'p/'+name,name]
                relative=next((n for n in options if (LOCKED/n).is_file()),None)
                if relative:
                    content=(LOCKED/relative).read_text(errors='strict')
                elif name in embedded:
                    relative='parts/'+name;content='\n'.join(embedded[name])+'\n'
                    (LOCKED/relative).parent.mkdir(parents=True,exist_ok=True)
                    (LOCKED/relative).write_text(content)
                else:
                    relative=next((n for n in options if n in names),None)
                    if relative is None:raise FileNotFoundError(name)
                    data=z.read(names[relative]);(LOCKED/relative).parent.mkdir(parents=True,exist_ok=True)
                    (LOCKED/relative).write_bytes(data);content=data.decode('utf-8')
                records[str((LOCKED/relative).relative_to(ROOT))]=hashlib.sha256((LOCKED/relative).read_bytes()).hexdigest()
            for line in content.splitlines():
                fields=line.split()
                if fields and fields[0]=='1':visit(' '.join(fields[14:]))
        visit(next(iter(embedded)))
    return records


def flatten(path, model_id, title):
    data = path.read_bytes()
    text = data.decode('utf-8-sig')
    files, name = {}, None
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if line.upper().startswith('0 FILE '):
            name = line[7:].lower().replace('\\', '/')
            if name in files:
                raise ValueError('Duplicate source file '+name)
            files[name] = []
        elif line.upper() == '0 NOFILE':
            name = None
        elif name:
            files[name].append((number, line))
    root = next(iter(files))
    colors = {m[0]: m[1] for m in re.findall(r'CODE\s+(\d+)\s+VALUE\s+(#[0-9A-Fa-f]{6})',
                                                       (LOCKED/'LDConfig.ldr').read_text())}
    instances = []
    axis = np.diag([.4,-.4,-.4,1])
    def walk(name, parent, inherited, stack):
        if name in stack:
            raise ValueError('Cyclic source model')
        for number, line in files[name]:
            if not line.startswith('1 '):
                continue
            cols = line.split(); values = list(map(float, cols[2:14]))
            x,y,z,a,b,c,d,e,f,g,h,i = values
            m = np.array([[a,b,c,x],[d,e,f,y],[g,h,i,z],[0,0,0,1]])
            world = parent @ m
            color = inherited if cols[1] == '16' else cols[1]
            child = ' '.join(cols[14:]).lower().replace('\\', '/')
            if child in files and child.endswith('.ldr'):
                walk(child, world, color, stack | {name})
                continue
            # Embedded unofficial part files remain source parts, never flattened
            # into their individual triangle primitives as separate bricks.
            part_path = LOCKED/'parts'/child
            part_text = '\n'.join(l for _,l in files[child]) if child in files else (
                part_path.read_text(errors='replace') if part_path.exists() else '')
            description = next((l[2:] for l in part_text.splitlines() if l.startswith('0 ')), child)
            n = len(instances)
            matrix = axis @ world
            value=colors.get(color) or ('#'+color[3:] if re.fullmatch(r'0x2[0-9a-fA-F]{6}',color) else None)
            if value is None:raise ValueError('Unknown source color '+color)
            instances.append(dict(instanceId=f'brick_{n+1:06}', index=n, partNumber=child.removesuffix('.dat'),
                colorCode=color, colorHex=value, displayName=description,
                originalMatrix=matrix.T.ravel().tolist(), sourceFile=name, sourceLine=number,
                embeddedPart=child in files))
    walk(root, np.eye(4), '7', set())
    header = '\n'.join(l for _,l in files[root])
    author = re.search(r'^0 Author:\s*(.+)$', header, re.M).group(1)
    license_text = re.search(r'^0 !LICENSE\s*(.+)$', header, re.M).group(1)
    digest = hashlib.sha256(data).hexdigest()
    manifest = dict(schema='brickplan-v7-original-source/1', model=dict(id=model_id, title=title,
        setNumber=path.stem, author=author, license=license_text,
        sourceUrl='https://library.ldraw.org/library/omr/'+path.name),
        sourceHash=digest, sourceFile=str(path.relative_to(ROOT)), instances=instances,
        transformConvention='Column-major diag(0.4,-0.4,-0.4,1) * composed source transform',
        instancesDropped=0, geometryQualification=None)
    target = ROOT/'web/public/models'/model_id
    if target.exists():
        raise ValueError('Refusing to replace an existing source manifest')
    target.mkdir(parents=True)
    (target/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
    provenance = dict(model=manifest['model'], source=dict(path=manifest['sourceFile'], sha256=digest,
        bytes=len(data)), sourceGeometryModified=False, sourceInstances=len(instances),
        completeSourceRetained=True, embeddedPartLockedPathConflicts=[],
        parser='expansion_v7/intake.py')
    (target/'provenance.json').write_text(json.dumps(provenance, ensure_ascii=False, indent=2)+'\n')
    return manifest


def main():
    titles={'1210-2':'Small Store Set','10002-1':'Railroad Club Car',
            '10015-1':'Passenger Wagon','10016-1':'Tanker','10013-1':'Open Freight Wagon'}
    for number, title in titles.items():
        source=ROOT/'assets-source/brickplan-v7/original'/(number+'.mpd')
        target=ROOT/'web/public/models'/('v7-omr-'+number)/'manifest.json'
        if not source.exists():
            continue
        dependencies=ensure_dependencies(source)
        lock=OUT/'intake-dependencies'/('v7-omr-'+number+'.json');lock.parent.mkdir(parents=True,exist_ok=True)
        lock.write_text(json.dumps(dependencies,indent=2)+'\n')
        if target.exists():
            continue
        manifest=flatten(source,'v7-omr-'+number,title)
        print('INTAKE',number,len(manifest['instances']),flush=True)


if __name__=='__main__':
    main()
