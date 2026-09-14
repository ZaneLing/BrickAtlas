import { execFileSync } from 'node:child_process';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { renameSync } from 'node:fs';

const here = dirname(fileURLToPath(import.meta.url));
const output = resolve(here, 'brickatlas-cvpr-source.zip');
const temporary = resolve(here, `.source-${process.pid}.zip`);
execFileSync('zip', ['-q', '-r', temporary, 'main.tex', 'supplement.tex', 'references.bib', 'cvpr.sty', 'ieeenat_fullname.bst',
  'tables', 'figures', 'README.md', 'BUILD.md', 'evidence.json', 'pdf-verification.json',
  'generate-tables.mjs', 'generate-study.mjs', 'study-evidence.json', 'check_pdf.py', 'supplement-verification.json',
  'generate-audit.mjs', 'generate-figures.py', 'audit-evidence.json', 'figure-evidence.json',
  'experiments.json', 'requirements.txt', 'verify-artifacts.mjs', 'REVIEW.zh-CN.md'], { cwd: here });
renameSync(temporary, output);
console.log(output);
