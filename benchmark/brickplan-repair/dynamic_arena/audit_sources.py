"""Verify source counts, original bytes and task admission without API calls."""
from collections import Counter
import gzip,hashlib,json
from dynamic_arena import ROOT,OUT
from dynamic_arena.transport import write_json
from dynamic_arena.source_library import flatten
from expansion_v7.build import read


def main():
    data=read(OUT/'source-library.json');rows=data['models'];assert len(rows)==data['count'] and len({r['setNumber'] for r in rows})==len(rows)
    from dynamic_arena.curate_sources import FigureAudit
    figure_audit=FigureAudit()
    assert all(figure_audit.audit(r)['status']=='no-figure-parts-found' for r in rows)
    qualified=read(OUT/'new-objects/index.json');admitted={r['setNumber']:r for r in qualified['models']};rejected={r['setNumber']:r for r in qualified['rejected']};shapes=set();checked=[]
    for r in rows:
        mf=read(ROOT/r['manifest']);assert len(mf['instances'])==r['parts']
        if not r['id'].startswith('arena-omr-'):continue
        source=ROOT/r['sourceFile'];raw=source.read_bytes();assert hashlib.sha256(raw).hexdigest()==r['sourceHash']==mf['sourceHash']
        instances,author,license_=flatten(raw)
        assert instances==mf['instances'] and author==r['author'] and license_==r['license']
        assert r['shapeHash'] not in shapes;shapes.add(r['shapeHash'])
        assert mf['instancesDropped']==0 and not mf['sourceGeometryModified']
        folder=source.parent;page=folder/'page.html'
        if page.exists():
            (folder/'page.html.gz').write_bytes(gzip.compress(page.read_bytes(),mtime=0))
            r['sourcePageSha256']=hashlib.sha256(page.read_bytes()).hexdigest()
        r['qualification']='normal-and-repair-machine-checked' if r['setNumber'] in admitted else 'engine-withheld' if r['setNumber'] in rejected else 'not-checked'
        r['arenaTaskCount']=sum(c['mode']=='dynamic' for c in read(OUT/'new-objects'/admitted[r['setNumber']]['id']/'cases.private.json.gz')) if r['setNumber'] in admitted else 0
        modules=read(ROOT/'deliverables/brickplan-quality-round/source-expansion/index.json')
        mids={m['id'] for m in modules['models'] if m['sourceSetId']==r['setNumber']}
        r['moduleTaskCount']=sum(c['model'] in mids and c['mode']=='dynamic' for c in modules['cases'])
        if mids:r['moduleQualification']='named-module-machine-checked'
        if r['setNumber'] in rejected:r['qualificationReason']=rejected[r['setNumber']]['reason']
        checked.append(dict(setNumber=r['setNumber'],parts=r['parts'],sourceSha256=r['sourceHash'],qualification=r['qualification']))
    data['newQualificationCounts']=dict(Counter(r['qualification'] for r in rows if r['id'].startswith('arena-omr-')))
    data['rejected']=list({r['setNumber']:r for r in data['rejected'] if r['setNumber'] not in {m['setNumber'] for m in rows}}.values())
    write_json(OUT/'source-library.json',data)
    write_json(OUT/'source-audit.json',dict(passed=True,sourceSets=len(rows),newSourceSets=len(checked),retiredSourcesAbsent=all(r['setNumber'] not in ('21004-1','21007-1') for r in rows),newQualificationCounts=data['newQualificationCounts'],checked=checked,apiCalls=0,scope='Original file completeness and source identity. Physical admission is separately reported.'))
    print(json.dumps(dict(sourceSets=len(rows),newSourceSets=len(checked),qualification=data['newQualificationCounts']),ensure_ascii=False))


if __name__=='__main__':main()
