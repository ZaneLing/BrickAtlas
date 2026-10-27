"""Start the local review application without touching any existing task server."""
from pathlib import Path
import argparse,json,os,subprocess,time,urllib.request,webbrowser
from bench_design import ROOT
from bench_design.challenges import QUALITY
from bench_design.session import INPUT_VERSION
from bench_design.gt_review import REVIEW_VERSION


def main():
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8808)
    p.add_argument('--no-open',action='store_true');p.add_argument('--manager',action='store_true');a=p.parse_args()
    base=f'http://127.0.0.1:{a.port}'
    def ready():
        try:
            with urllib.request.urlopen(base+'/health',timeout=1) as r:value=json.load(r)
            if value.get('inputVersion')!=INPUT_VERSION:raise RuntimeError('This port belongs to another interface; do not stop it automatically.')
            if value.get('reviewVersion')!=REVIEW_VERSION:raise RuntimeError('旧版检查服务仍在运行，需要重启本项目的检查服务。')
            return True
        except (OSError,TimeoutError):return False
    if not ready():
        python=ROOT/'benchmark/.runtime/mlx-env/bin/python'
        log=QUALITY/'server.log';log.parent.mkdir(parents=True,exist_ok=True)
        with log.open('ab') as stream:
            process=subprocess.Popen([str(python),'-m','bench_design.review_server','--port',str(a.port)],
                cwd=ROOT,env={**os.environ,'PYTHONPATH':str(ROOT/'benchmark/brickplan-repair')},
                stdin=subprocess.DEVNULL,stdout=stream,stderr=stream,start_new_session=True)
        (QUALITY/'server.pid').write_text(str(process.pid)+'\n')
        for _ in range(80):
            if ready():break
            if process.poll() is not None:raise SystemExit('启动失败，请查看 '+str(log))
            time.sleep(.25)
        else:raise SystemExit('页面仍未就绪，请查看 '+str(log))
    key=json.loads((QUALITY/'submissions/manager-key.private.json').read_text())['key']
    for reviewer in ['A','B','C']:print(reviewer+'：'+base+'/'+reviewer)
    manager=base+'/?manager='+key;print('组织者汇总：'+manager)
    if not a.no_open:webbrowser.open(manager if a.manager else base+'/A')


if __name__=='__main__':main()
