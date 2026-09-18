import { execFileSync } from 'node:child_process';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { renameSync } from 'node:fs';

const here = dirname(fileURLToPath(import.meta.url));
const output = resolve(here, 'brickatlas-cvpr-source.zip');
const temporary = resolve(here, `.source-${process.pid}.zip`);
execFileSync('zip', ['-q', '-r', temporary, 'main.tex', 'main.zh-CN.md', 'supplement.tex', 'references.bib', 'cvpr.sty', 'ieeenat_fullname.bst',
  'ldraw-results.tex', 'ldraw-cases.tex', 'ldraw-families.tex', 'ldraw-controls.tex',
  'ldraw-scale.tex', 'ldraw-evidence.json', 'figures/ldraw/print', 'figures/ldraw/teaser.png', 'verify-artifacts.mjs',
  'README.md', 'BUILD.md', 'pdf-verification.json', 'check_pdf.py',
  'supplement-verification.json', 'requirements.txt'], { cwd: here });
renameSync(temporary, output);
console.log(output);
