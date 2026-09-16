import { execFileSync } from 'node:child_process';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { renameSync } from 'node:fs';

const here = dirname(fileURLToPath(import.meta.url));
const output = resolve(here, 'brickatlas-cvpr-source.zip');
const temporary = resolve(here, `.source-${process.pid}.zip`);
execFileSync('zip', ['-q', '-r', temporary, 'main.tex', 'main.zh-CN.md', 'supplement.tex', 'references.bib', 'cvpr.sty', 'ieeenat_fullname.bst',
  'hierarchy-expanded-results.tex', 'hierarchy-expanded-cases.tex', 'hierarchy-expanded-evidence.json',
  'publication-worked.tex', 'publication-analysis.json', 'publication-capture.json', 'publication-figures.json',
  'analyze-publication.ts', 'capture-publication.ts', 'compose-publication.py', 'verify-hierarchy-expanded.mjs',
  'WRITING_NOTES.md',
  'tables/publication-structure.tex', 'tables/publication-controls.tex', 'tables/publication-families.tex',
  'tables/hierarchy3-pilot.tex', 'tables/hierarchy3-contracts.tex',
  'figures/hierarchy-expanded', 'figures/publication-frames',
  ...['teaser', 'disassembly', 'repair', 'invalid', 'steps'].flatMap(name =>
    ['pdf', 'png'].map(ext => `figures/publication-${name}.${ext}`)),
  'README.md', 'BUILD.md', 'pdf-verification.json', 'check_pdf.py',
  'supplement-verification.json', 'requirements.txt'], { cwd: here });
renameSync(temporary, output);
console.log(output);
