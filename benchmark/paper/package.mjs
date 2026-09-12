import { execFileSync } from 'node:child_process';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { existsSync, unlinkSync } from 'node:fs';

const here = dirname(fileURLToPath(import.meta.url));
const output = resolve(here, 'brickatlas-cvpr-source.zip');
if (existsSync(output)) unlinkSync(output);
execFileSync('zip', ['-q', '-r', output, 'main.tex', 'references.bib', 'cvpr.sty', 'ieeenat_fullname.bst',
  'tables', 'figures', 'README.md', 'BUILD.md', 'evidence.json', 'pdf-verification.json',
  'generate-tables.mjs', 'check_pdf.py'], { cwd: here });
console.log(output);
