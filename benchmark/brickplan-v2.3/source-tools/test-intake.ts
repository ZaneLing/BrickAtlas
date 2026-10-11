import assert from 'node:assert/strict';
import { readFile, mkdtemp, mkdir } from 'node:fs/promises';
import { resolve } from 'node:path';
import { splitMpd, reference, dependencyClosure, buildManifest, hash } from '../../../scripts/ldraw.ts';
import { validateTransforms, writeNew } from './intake.ts';

const here = process.env.SOURCE_INTAKE_OUTPUT ?? '/tmp/brickplan-v23-work/source-intake';
await mkdir(here, { recursive: true });
const license = '0 Author: Synthetic parser fixture\n0 !LICENSE Redistributable under CC BY 4.0 : see CAreadme.txt';
const source = [
  '0 FILE main.ldr', '0 Synthetic parser test', license, '0 !LDRAW_ORG Model',
  '1 4 10 20 30 0 -1 0 1 0 0 0 0 1 sub.ldr',
  '1 2 0 0 0 -1 0 0 0 1 0 0 0 1 part.dat',
  '1 0x2123456 2 3 4 1 0.2 0 0 1 0 0 0 1 part.dat',
  '0 FILE sub.ldr', '0 Submodel', license, '0 !LDRAW_ORG Model',
  '1 16 3 4 5 1 0 0 0 1 0 0 0 1 part.dat',
  '1 4294967295 3 4 5 1 0 0 0 1 0 0 0 1 part.dat',
  '0 FILE part.dat', '0 Test brick', license, '0 !LDRAW_ORG Part',
  '3 16 0 0 0 1 0 0 0 1 0',
].join('\r\n');
const colors = [
  '0 !COLOUR Red CODE 4 VALUE #C91A09 EDGE #333333',
  '0 !COLOUR Green CODE 2 VALUE #237841 EDGE #333333',
].join('\n');
const files = splitMpd(source);
const semantic = buildManifest(files, 'main.ldr', colors, () => 'body');
assert.equal(dependencyClosure(files, 'main.ldr').length, 3);
assert.equal(semantic.instances.length, 4);
assert.deepEqual(semantic.instances.map(p => p.colorCode), ['4', '4', '2', '0x2123456']);
assert.equal(semantic.instances[3].colorHex, '#123456');
assert.deepEqual(semantic.instances[0].originalMatrix.slice(12, 15).map(v => Number(v.toFixed(8))),
  [2.4, -9.2, -14]);
assert.notEqual(semantic.instances[0].instanceId, semantic.instances[1].instanceId);
const report = validateTransforms(files, 'main.ldr', semantic.instances);
assert.equal(report.sourceReflectionsPreserved, 1);
assert.equal(report.sourceNonRigidTransformsPreserved, 1);
assert.equal(report.instancesDropped, 0);
const corrupt = structuredClone(semantic.instances);
corrupt[0].originalMatrix[12] += 0.1;
assert.throws(() => validateTransforms(files, 'main.ldr', corrupt), /Composition mismatch/);
assert.throws(() => splitMpd('0 FILE main.ldr\n0 FILE MAIN.LDR\n'), /Duplicate FILE/);
assert.throws(() => reference('1 4 0 0 0 0 0 0 0 0 0 0 0 0 part.dat', 1), /Singular/);
assert.throws(() => reference('1 4 0 0 NaN 1 0 0 0 1 0 0 0 1 part.dat', 1), /Non-finite/);
assert.throws(() => reference('1 4 0 0 0 1 0 0 0 1 0 0 0 1 ../part.dat', 1), /Unsafe/);
const cycle = splitMpd(`0 FILE main.ldr\n${license}\n1 16 0 0 0 1 0 0 0 1 0 0 0 1 main.ldr\n`);
assert.throws(() => dependencyClosure(cycle, 'main.ldr'), /Circular reference/);
const missing = splitMpd(`0 FILE main.ldr\n${license}\n1 16 0 0 0 1 0 0 0 1 0 0 0 1 missing.dat\n`);
assert.throws(() => dependencyClosure(missing, 'main.ldr'), /Missing dependency/);
const unlicensed = splitMpd('0 FILE main.ldr\n0 Model\n0 Author: Test\n');
assert.throws(() => dependencyClosure(unlicensed, 'main.ldr'), /Missing or unapproved license/);
const temp = await mkdtemp(resolve(here, 'write-guard-test-'));
const target = resolve(temp, 'original.bin');
const bytes = Buffer.from([0, 10, 13, 128, 255]);
await writeNew(target, bytes);
await writeNew(target, bytes);
await assert.rejects(() => writeNew(target, Buffer.from('replacement')), /Refusing overwrite/);
assert.equal(hash(await readFile(target)), hash(bytes));
await writeNew(resolve(here, 'unit-test-results.json'), JSON.stringify({
  status: 'pass', syntheticOnly: true, geometryQualificationRun: false,
  checks: ['nested transform and axis conversion', 'inherited and sentinel colors', 'direct colors',
    'duplicate instances retained', 'reflections and shear preserved', 'matrix corruption rejected',
    'duplicate FILE rejected', 'singular matrix rejected', 'NaN rejected', 'path traversal rejected',
    'cycle rejected', 'missing dependency rejected', 'missing license rejected',
    'binary byte preservation', 'idempotent writes', 'overwrite rejected'],
  transforms: report,
}, null, 2) + '\n');
console.log('PASS: 16 synthetic source-intake checks; no geometry qualification.');
