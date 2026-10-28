"""No-API gate check across each active source family."""
from pathlib import Path
from tempfile import TemporaryDirectory
from bench_design.session import Session, scheduled_of

CASES = (
    'D:obj-chair--t3--compound_fault--v01',
    'M:cottage-roof-dynamic-missing',
    'E7:v7::v7-long-bookshelf::dynamic::missing::t14',
    'O:objects::whole-4018::dynamic::missing::t7',
)


def main():
    with TemporaryDirectory(prefix='normal-gate-check-') as d:
        for i,cid in enumerate(CASES):
            event=Session.open(cid,Path(d)/f'{i}-event','gate-check')
            normal=Session.open(cid,Path(d)/f'{i}-normal','gate-check',control=True)
            assert event.initial==normal.initial and event.goal==normal.goal
            assert scheduled_of(event.ep)>0 and scheduled_of(normal.ep)==0
    print('PASS exact-case no-event control for D, M, E7 and O source banks')


if __name__=='__main__':main()
