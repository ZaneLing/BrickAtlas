import { firefox, expect as baseExpect } from '@playwright/test';
import { mkdir, writeFile, readFile, readdir } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { spawnSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const base = process.env.BRICKPLAN_TEST_URL || 'http://127.0.0.1:8771';
const out = path.join(root, 'tem/research/20261009-react-workbench');
const expect = baseExpect.configure({ timeout: 30000 });
await mkdir(out, { recursive: true });
const browser = await firefox.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1480, height: 1050 }, deviceScaleFactor: 2 });
page.setDefaultTimeout(30000);
const errors = [], checks = [];
page.on('pageerror', e => errors.push(e.message));
const check = name => { checks.push(name); console.log('PASS', name); };
const waitIdle = () => expect(page.getByRole('status')).not.toContainText('Working');
async function frontendFiles() {
  const hashes = {};
  async function visit(folder) {
    for (const entry of await readdir(folder, { withFileTypes: true })) {
      if (entry.name.startsWith('.') || entry.name === 'node_modules') continue;
      const file = path.join(folder, entry.name);
      if (entry.isDirectory()) await visit(file);
      else hashes[path.relative(root, file)] = createHash('sha256').update(await readFile(file)).digest('hex');
    }
  }
  await visit(path.join(root, 'web/brickplan'));
  await visit(path.join(root, 'benchmark/brickplan-v2.1/arena/app'));
  return hashes;
}
try {
  const cat = await (await page.request.get(base + '/api/catalogue')).json();
  const before = await (await page.request.get(base + '/api/tasks')).json();
  await page.goto(base);
  await expect(page.locator('[class*="families"] > button')).toHaveCount(7);
  await expect(page.locator('canvas')).toHaveCount(2);
  await expect(page.locator('[class*="scene-labels"]').first()).toContainText('P');
  await page.screenshot({ path: path.join(out, 'workbench-library.png'), fullPage: true });
  check('seven families, complete contracts, two native WebGL2 scenes');
  const canvas = page.locator('canvas').first(), box = await canvas.boundingBox();
  const labelBefore = await page.locator('.scene-labels').first().getAttribute('style');
  const pixelsBefore = await canvas.screenshot();
  await page.mouse.move(box.x + box.width * .5, box.y + box.height * .5);
  await page.mouse.down(); await page.mouse.move(box.x + box.width * .7, box.y + box.height * .6, { steps: 6 }); await page.mouse.up();
  expect((await canvas.screenshot()).equals(pixelsBefore)).toBe(false);
  await page.getByLabel('Explode diagram').fill('70');
  await expect(page.locator('[class*="visualNote"]')).toContainText('Exploded diagram only');
  check('camera orbit changes rendered pixels and explosion is labeled');
  await page.getByRole('button', { name: '高清图 HD', exact: true }).click();
  await page.getByRole('button', { name: '放大 当前结构 Current', exact: true }).click();
  await page.getByRole('button', { name: '原生像素 1:1', exact: true }).click();
  expect(await page.getByRole('dialog').locator('img').evaluate(i => [i.naturalWidth, i.clientWidth])).toEqual([1920, 1920]);
  await page.getByRole('button', { name: '关闭 Close', exact: true }).click();
  check('Radix image dialog preserves 1920-pixel native zoom');
  const after = await (await page.request.get(base + '/api/tasks')).json();
  expect(after.tasks.map(t => t.sessions)).toEqual(before.tasks.map(t => t.sessions));
  check('library preview creates no attempts');
  // An independent oracle fixture drives the UI solely through visible controls.
  // It is a software acceptance test, never a human or model benchmark result.
  const env = { ...process.env, PYTHONNOUSERSITE: '1' }; delete env.PYTHONPATH;
  const fixture = spawnSync(path.join(root, 'benchmark/.runtime/mlx-env/bin/python'), ['-c', `
import sys,json
sys.path.insert(0,'benchmark/brickplan-v2.1')
from bank import task_bank,make_mission,load_oracle
from probes import public_mapping
from session import Session
task=next(t for t in task_bank()['episodes'] if t['optimalCost']==5)
s=Session(make_mission(task),task,0,'image-id')
oracle=load_oracle(task['id']); actions=[]
while oracle.distance(s.state):
    a=oracle.optimal_actions(s.state)[0]
    public=s.public_action(a);actions.append(public)
    s.submit({'requestId':str(len(actions)),'revision':s.revision,'action':public})
mapping=public_mapping([t['id'] for t in task_bank()['episodes']],0,'E')
print(json.dumps({'id':next(k for k,v in mapping.items() if v==task['id']),'actions':actions}))
`], { cwd: root, env, encoding: 'utf8' });
  if (fixture.status) throw Error(fixture.stderr);
  const solution = JSON.parse(fixture.stdout);
  await page.goto(`${base}/play?task=${solution.id}`);
  await page.getByRole('button', { name: '开始作答 Start', exact: true }).click();
  await expect(page.getByRole('button', { name: '安装 Attach', exact: true })).toBeEnabled();
  const sid = new URL(page.url()).searchParams.get('session');
  await page.getByLabel('Acquisition view', { exact: true }).selectOption('top');
  await page.getByRole('button', { name: '获取并记录 Acquire', exact: true }).click(); await waitIdle();
  await page.getByLabel('Saved view', { exact: true }).selectOption('0');
  await expect(page.getByRole('button', { name: '安装 Attach', exact: true })).toBeDisabled();
  await page.getByRole('button', { name: '返回当前 Return to live', exact: true }).click();
  await expect(page.getByRole('button', { name: '安装 Attach', exact: true })).toBeEnabled();
  check('acquired view history disables mutations until returning to live');
  for (const action of solution.actions) {
    await page.getByLabel('Piece', { exact: true }).selectOption(action.partId);
    if (action.type === 'attach') await page.getByLabel('Site', { exact: true }).selectOption(action.siteId);
    const names = { attach: '安装 Attach', detach: '拆卸 Detach', audit: '离架检修 Audit' };
    await page.getByRole('button', { name: names[action.type], exact: true }).click(); await waitIdle();
    await expect(page.getByRole('status')).toContainText('OK');
  }
  await page.getByRole('button', { name: '无错误 No', exact: true }).click(); await waitIdle();
  await page.getByRole('button', { name: '结束 Finish', exact: true }).click(); await waitIdle();
  await expect(page.locator('[class*="_score_"]')).toContainText('Success');
  const scored = await (await page.request.get(`${base}/api/sessions/${sid}/score`)).json();
  expect(scored.success).toBe(true); expect(scored.regret).toBe(0);
  await page.getByLabel('Replay revision', { exact: true }).fill('0'); await waitIdle();
  await expect(page.getByRole('button', { name: '安装 Attach', exact: true })).toBeDisabled();
  await page.reload(); await expect(page.locator('[class*="_score_"]')).toContainText('Success');
  await page.screenshot({ path: path.join(out, 'workbench-human.png'), fullPage: true });
  check('human UI solves an episode optimally, diagnoses, finishes, replays and persists');
  const states = await (await page.request.get(base + '/api/probes')).json();
  for (const category of ['continuation', 'repair']) {
    const q = cat.questions.find(q => q.category === category && !states.probes.find(p => p.id === q.id).answered);
    await page.goto(`${base}/play?probe=${q.id}`);
    await expect(page.getByLabel('Probe answer', { exact: true })).toBeEnabled();
    if (category === 'repair') await expect(page.getByText('错误前检查点与后续历史 / Repair checkpoint', { exact: true })).toBeVisible();
    await page.getByLabel('Probe answer', { exact: true }).selectOption(category === 'repair' ? '0' : 'null');
    await page.getByRole('button', { name: '提交答案 Submit', exact: true }).click(); await waitIdle();
    await expect(page.getByRole('button', { name: '提交答案 Submit', exact: true })).toBeDisabled();
    await expect(page.getByText('已提交答案解析 / Answer review', { exact: true })).toBeVisible();
    await page.reload(); await expect(page.getByText('答案已冻结 / Answer frozen', { exact: true })).toBeVisible();
  }
  check('sequence and repair probes submit once, preserve checkpoints and freeze after reload');
  await page.goto(base + '/#case');
  await expect(page.getByLabel('Model call timeline').locator('button')).toHaveCount(4);
  await expect(page.locator('[class*="_raw_"]')).not.toBeEmpty();
  await page.getByRole('button', { name: 'Next model step', exact: true }).click();
  await expect(page.locator('[class*="_callDetail_"]')).toContainText('INVALID_ACTION');
  await page.getByRole('button', { name: '执行后 After', exact: true }).click();
  await expect(page.locator('[class*="_scene_"]').first()).toHaveAttribute('data-mask', /[0-9]+/);
  await page.screenshot({ path: path.join(out, 'workbench-model.png'), fullPage: true });
  check('recorded four-call model timeline exposes input, raw response, feedback and after state');
  await page.setViewportSize({ width: 390, height: 844 });
  await page.getByRole('button', { name: '打开导航 Open navigation', exact: true }).click();
  await page.getByRole('dialog').getByRole('button', { name: /题目库/ }).click();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
  await page.screenshot({ path: path.join(out, 'workbench-mobile.png'), fullPage: true });
  await page.getByRole('button', { name: '打开导航 Open navigation', exact: true }).click();
  await page.getByRole('dialog').getByRole('button', { name: /论文与下载/ }).click();
  const overleaf = await page.getByRole('link', { name: 'Overleaf ZIP', exact: true }).getAttribute('href');
  expect((await page.request.get(overleaf)).ok()).toBe(true);
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
  check('mobile navigation, width and independent Overleaf download');
  expect(errors).toEqual([]);
  await writeFile(path.join(out, 'workbench-validation.json'), JSON.stringify({ status: 'passed', browser: 'Firefox', checks, errors, frontendFiles: await frontendFiles() }, null, 2));
} catch (e) {
  console.log('FAILED', e.message, page.url(), errors);
  await page.screenshot({ path: path.join(out, 'workbench-failure.png'), fullPage: true }).catch(() => {});
  await writeFile(path.join(out, 'workbench-validation.json'), JSON.stringify({ status: 'failed', checks, errors: [...errors, e.message] }, null, 2));
  process.exitCode = 1;
} finally { await browser.close(); }
