/** Publication-only synchronization; source geometry, tasks and reviews stay frozen. */
import { copyFileSync, mkdirSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';

const paper = import.meta.dirname;
const docs = resolve(paper, '../../public/benchmark/docs');
mkdirSync(docs, { recursive: true });
for (const file of ['main.pdf', 'supplement.pdf', 'main.zh-CN.md',
  'ldraw-experiments.json', 'brickatlas-cvpr-source.zip']) {
  if (existsSync(resolve(paper, file))) copyFileSync(resolve(paper, file), resolve(docs, file));
}
console.log('Synchronized current PDFs, companion, experiment plan and source package.');
