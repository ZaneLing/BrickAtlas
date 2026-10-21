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
    for flag, script in [(args.study,'protocol_study.py'),(args.refresh_figures,'build_figures.py')]:
        if flag:
            subprocess.run([paper_python,str(HERE/script)],cwd=ROOT,check=True)
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
    figures = sorted((HERE/'figures-v2').glob('*.pdf'))
    with zipfile.ZipFile(HERE/'brickplan-cvpr-overleaf.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in [HERE/n for n in names] + figures:
            z.write(p,str(p.relative_to(HERE)))
        z.writestr('README.txt','Select main.tex or supplement.tex as the root document.\n'
                   'Use pdfLaTeX/BibTeX or Tectonic. Figures are already included.\n'
                   'CVPR 2026 official style; 2027 venue/year label remains a draft.\n'
                   'Replace Draft with the assigned submission ID before submission.\n'
                   'Formal model and human experiments are not yet complete.\n')
    print('Published main.pdf, supplement.pdf, and brickplan-cvpr-overleaf.zip',flush=True)


if __name__ == '__main__':
    main()
