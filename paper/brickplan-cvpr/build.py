"""Compile the paper; optionally re-execute the offline study and native renders."""
from pathlib import Path
import argparse
import os
import shutil
import subprocess
import sys
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--refresh-figures',action='store_true')
    parser.add_argument('--refresh-typography',action='store_true',
                        help='Regenerate figure text/charts from cached scenes, without geometry rendering')
    parser.add_argument('--study',action='store_true')
    parser.add_argument('--skip-verification',action='store_true',
                        help='Compile-only, e.g. in a standalone Overleaf source extraction')
    args = parser.parse_args()
    project_python = ROOT/'benchmark/.runtime/mlx-env/bin/python'
    paper_python = os.environ.get('BRICKPLAN_PYTHON') or (str(project_python) if project_python.exists() else sys.executable)
    compiler = os.environ.get('TECTONIC') or shutil.which('tectonic')
    fallback = Path.home()/'.local/bin/tectonic'
    if not compiler and fallback.exists():
        compiler = str(fallback)
    if not compiler:
        raise SystemExit('Install Tectonic or set TECTONIC to its executable path.')
    if args.study:
        raise SystemExit('--study refers to an archived protocol. Current offline checks: scaling_release.arena_check and scaling_release.release_check.')
    # Counts and blank table schemas come only from the current checked release.
    subprocess.run([paper_python,str(HERE/'release_tables.py')],cwd=ROOT,check=True)
    if args.refresh_figures:
        subprocess.run([paper_python,str(HERE/'release_assets.py'),'--scenes'],cwd=ROOT,check=True)
        subprocess.run([paper_python,str(HERE/'arena_assets.py')],cwd=ROOT,check=True)
    if args.refresh_figures:
        node = os.environ.get('BRICKPLAN_NODE') or shutil.which('node')
        local_node=ROOT/'.tools/node-v22.23.2-darwin-arm64/bin/node'
        if not node and local_node.exists():node=str(local_node)
        if not node:raise SystemExit('Publication rendering needs Node 22+; set BRICKPLAN_NODE.')
        subprocess.run([node,str(HERE/'render_publication.mjs'),'--release'],cwd=ROOT,check=True)
        subprocess.run([node,str(HERE/'render_publication.mjs'),'--arena'],cwd=ROOT,check=True)
    if args.refresh_figures or args.refresh_typography:
        subprocess.run([paper_python,str(HERE/'release_figures.py')],cwd=ROOT,check=True)
    (HERE/'build').mkdir(exist_ok=True)
    for name in ['main','supplement']:
        log = HERE/'build'/f'{name}-compile.txt'
        with log.open('w') as out:
            result = subprocess.run([compiler,'--keep-logs','--keep-intermediates',
                                     '--outdir','build',name+'.tex'],cwd=HERE,
                                     stdout=out,stderr=subprocess.STDOUT)
        if result.returncode:
            raise SystemExit(log.read_text())
        print(f'Compiled {name}.pdf; compiler output: {log.relative_to(ROOT)}',flush=True)
    if not args.skip_verification:
        subprocess.run([paper_python,str(HERE/'verify.py')],cwd=ROOT,check=True)
    for name in ['main','supplement']:
        shutil.copyfile(HERE/'build'/f'{name}.pdf',HERE/f'{name}.pdf')
    # Portable LaTeX compilation package: no local data paths or private API logs.
    names = ['main.tex','supplement.tex','references.bib','cvpr.sty',
             'ieeenat_fullname.bst','template-provenance.json']
    # Include only figures referenced by the current TeX source.
    import re
    tex = '\n'.join(p.read_text() for p in [HERE/'main.tex',HERE/'supplement.tex',*sorted((HERE/'tables').glob('*.tex'))])
    figures = [HERE/p for p in sorted(set(re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}',tex)))]
    with zipfile.ZipFile(HERE/'brickplan-cvpr-overleaf.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in [HERE/n for n in names] + figures + sorted((HERE/'tables').glob('*.tex')):
            z.write(p,str(p.relative_to(HERE)))
        z.writestr('README.txt','Select main.tex or supplement.tex as the root document.\n'
                   'Use pdfLaTeX/BibTeX or Tectonic. Figures are already included.\n'
                   'CVPR 2026 official style; 2027 venue/year label remains a draft.\n'
                   'Replace Draft with the assigned submission ID before submission.\n'
                   'Dataset/metrics snapshot: 29 October 2026.\n'
                   '310 runnable objects; 4,685 checked questions: 1,600 static + 3,085 dynamic.\n'
                   'Normal-qualified recovery uses independent runs; causal forks remain a planned study.\n'
                   'Formal model and current-interface human experiments are not yet complete.\n')
    print('Published main.pdf, supplement.pdf, and brickplan-cvpr-overleaf.zip',flush=True)


if __name__ == '__main__':
    main()
