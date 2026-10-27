from bench_design.review_server import Server
from bench_design.source_expansion import OUT,index,source_row,visibility
from bench_design.session import Session,internal_action
from bench_design.independent_geometry import check
from expansion_v7.build import read,write
from pathlib import Path
from PIL import Image
import numpy as np,hashlib,time
def main():
    root=Path('deliverables/brickplan-quality-round');s=Server(('127.0.0.1',0),Path('/tmp/brick-gt-feedback-final'))
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument("--previews-only",action="store_true");parser.add_argument("--sources-only",action="store_true");args=parser.parse_args()
    start=time.time()
    if not args.previews_only:
        replays=[];geometry=[];visible=[];start=time.time()
        for row in index()['cases']:
         sess=Session.open(row['id'],Path('/tmp/brick-new-native')/row['model']/row['id'].split('::')[-1]/row['mode']);sess.autosave=False
         if row['mode']=='static':
          measured=visibility(sess.packet.renderer,sess.ep.state,sess.goal);visible.append(dict(id=row['id'],**measured))
         for a in sess.row['case']['referenceActions']:
          if row['mode']=='static':
           rt=sess.ep.runtime;_,v=rt.check(sess.ep.state,a['actor'],a['type'],candidate=a.get('candidate'))
           measured=check(rt,sess.ep.state,a,v);geometry.append(dict(caseId=row['id'],action=a,status=measured['status'],evidence=measured))
          assert sess.submit(internal_action(sess.ep,a))['code']=='OK'
         sess.submit(dict(type='finish'));result=sess.result();assert result['success']
         assert len(sess.events)==len(sess.row['case']['events'])
         assert all(e['native']['visibilityCheck']['visible'] for e in sess.events)
         replays.append(dict(id=row['id'],success=True,events=len(sess.events),acceptedMoves=result['executionMetrics']['acceptedMoves']))
         print('NEW',len(replays),row['id'],len(sess.events),flush=True)
        write(OUT/'native-replay-check.json',dict(status='PASS',runs=replays,apiCalls=0,realHumanSubmissions=0))
        write(OUT/'independent-geometry-check.json',dict(checks=geometry,allAgreed=all(r['status']=='agrees-on-accepted-geometry' for r in geometry),scope='Independent Boolean backend on source geometry; no gravity, clutch force, or physical-hardware claim.'))
        write(OUT/'visibility-check.json',dict(rows=visible,allVisible=all(v['visible'] for v in visible),apiCalls=0,humanRecognitionClaim=False))
        assert all(v['visible'] for v in visible),'Invisible source cases must be corrected before admission'
        assert all(r['status']=='agrees-on-accepted-geometry' for r in geometry),'Independent geometry requires resolution'
    if args.sources_only:
        s.server_close();return
    previews=[];visual=[];feedback=read(root/'A-feedback-resolution.json');flagged={r['code'] for r in feedback['rows'] if r['choice']!='correct'}
    for code in s.maps['gt']:
     b=s.gt.bundle(code);assert b['replaySuccess'],code
     previews.append(dict(code=code,caseId=b['caseId'],success=True,goalIsStage=b['goalIsStage'],stage=b['stageNumber']))
     # Prewarm all opening images, and measure visual differences in disputed views.
     diffs={}
     for view in ['isometric','rear','left']:
      p=s.gt.image(code,'current',view);g=s.gt.image(code,'goal',view);s.gt.image(code,'result',view)
      if code in flagged or code.startswith('N'):
       aa=np.asarray(Image.open(p)).astype(int);bb=np.asarray(Image.open(g)).astype(int)
       diffs[view]=int(np.count_nonzero(np.max(abs(aa-bb),axis=2)>24))
     preferred=s.gt.default_view(code);s.gt.image(code,'context',preferred)
     if diffs:visual.append(dict(code=code,changedPixels=diffs,replaySuccess=b['replaySuccess'],noErrorExpected=(b['mode']=='static' and len(b['frames'])==1)))
     print('PREVIEW',len(previews),code,flush=True)
    visible=all(max(v['changedPixels'].values())>=50 or v['noErrorExpected'] for v in visual)
    write(root/'feedback-preview-validation.json',dict(status='PASS' if visible else 'NEEDS_VISUAL_REVIEW',version=s.gt.version,replays=previews,visual=visual,allExpectedDifferencesVisible=visible,elapsedSeconds=time.time()-start,apiCalls=0,humanRechecks=0))
    assert visible,'Review images with expected differences remain indistinguishable'
    s.server_close()


if __name__=='__main__':main()
