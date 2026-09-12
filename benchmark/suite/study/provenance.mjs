import { copyFileSync, readFileSync, mkdirSync, writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';

const here = dirname(fileURLToPath(import.meta.url)), bench = resolve(here, '../..');
const out = resolve(here, '../artifacts/study/provenance'); mkdirSync(out, { recursive: true });
copyFileSync(resolve(bench, '.runtime/models/smolvlm-256m/README.md'), resolve(out, 'SMOLVLM_MODEL_CARD.md'));
copyFileSync(resolve(bench, 'suite/artifacts/research/QWEN_LICENSE.txt'), resolve(out, 'APACHE-2.0.txt'));
const names = ['torch', 'transformers', 'peft', 'accelerate', 'safetensors', 'pillow', 'numpy',
  'huggingface-hub', 'mlx', 'mlx-vlm', 'mlx-lm', 'tokenizers'];
const environments = Object.fromEntries(['train-env', 'mlx-env'].map(name => {
  const packages = JSON.parse(execFileSync(resolve(bench, '.runtime', name, 'bin/python'),
    ['-m', 'pip', 'list', '--format=json'], { encoding: 'utf8' }));
  return [name, packages.filter(p => names.includes(p.name.toLowerCase()))];
}));
writeFileSync(resolve(out, 'environment.json'), JSON.stringify({ environments,
  scope: 'Versions observed in actual environments, not an OS-independent dependency lock.' }, null, 2) + '\n');
writeFileSync(resolve(out, 'model.json'), JSON.stringify({
  model: 'HuggingFaceTB/SmolVLM-256M-Instruct', revision: '7e3e67edbbed1bf9888184d9df282b700a323964',
  modelCard: 'SMOLVLM_MODEL_CARD.md',
  modelCardSha256: createHash('sha256').update(readFileSync(resolve(out, 'SMOLVLM_MODEL_CARD.md'))).digest('hex'),
  license: 'Apache-2.0 per upstream card; generic license text retained without Qwen-specific attribution.',
  weightsSha256: createHash('sha256').update(readFileSync(resolve(bench, '.runtime/models/smolvlm-256m/model.safetensors'))).digest('hex'),
  modifications: 'Language-side rank-8 q/v LoRA trained on procedural BrickAtlas data. Base weights not redistributed.',
}, null, 2) + '\n');
