"""Open every dynamic object adapter and resolve every published case ID."""
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from tempfile import TemporaryDirectory
from pathlib import Path
import json
from dynamic_arena import OUT
from dynamic_arena.run import open_session,NoProvider
from dynamic_arena.tool_arena import ToolArena
from bench_design.run_episode import source_rows
from expansion_v7.build import read,write


def check(r):
    try:
        with TemporaryDirectory(prefix='arena-load-') as d:
            s=open_session(r['caseId'],Path(d),'scripted:catalogue-load',True)
            a=ToolArena(s,NoProvider(),min(30,s.cap))
            _,_,public,images=a.request()
            assert not images and public['actionHandles']
            assert all(h['candidates'] for h in public['actionHandles'])
            assert s.row['key']==r['caseId']
            return dict(model=r['model'],caseId=r['caseId'],passed=True,handles=len(public['actionHandles']),inventoryPages=a.sensors.inventory_count,manualSteps=a.sensors.manual_count)
    except Exception as e:return dict(model=r['model'],caseId=r['caseId'],passed=False,error=type(e).__name__+': '+str(e))


def main():
    rows=read(OUT/'catalogue.json')['cases'];groups={}
    known=source_rows();missing=[]
    for r in rows:
        if not r['caseId'].startswith(('QX:','QN:','QI:','A4:')) and r['caseId'] not in known:missing.append(r['caseId'])
        groups.setdefault((r['caseId'].split(':')[0],r['model']),r)
    results=[]
    with ProcessPoolExecutor(max_workers=2) as pool:
        for r in pool.map(check,groups.values()):
            results.append(r);print('PASS' if r['passed'] else 'FAIL',r['model'],r.get('error',''),flush=True)
            write(OUT/'migration-catalogue-check.json',dict(totalCases=len(rows),resolvedBaseIds=not missing,missing=missing,representativeAdaptersChecked=len(results),expectedAdapters=len(groups),checks=results,apiCalls=0,passed=len(results)==len(groups) and not missing and all(x['passed'] for x in results)))
    assert not missing and all(r['passed'] for r in results)


if __name__=='__main__':main()
