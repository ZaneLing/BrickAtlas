// Verify the actual local gallery and every image it references. No model calls.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { readFileSync, writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { request } from 'node:http';

const out='deliverables/brickplan-expansion-v7', base=process.env.BRICKPLAN_GALLERY_URL||'http://127.0.0.1:8797';
const models=JSON.parse(readFileSync(`${out}/gallery.json`,'utf8'));
async function status(path,method='GET'){
  return new Promise((resolve,reject)=>{
    const req=request(base+path,{method},res=>{res.resume();res.on('end',()=>resolve(res.statusCode));});
    req.on('error',reject);req.end();
  });
}
const assets=new Map();
for(const m of models){
  for(const a of [m.fullImage,...m.manual,...m.cases.flatMap(c=>[...Object.values(c.images),...c.timeline.map(e=>e.image)])]){
    const bytes=readFileSync(`${out}/${a.file}`);
    assert.equal(createHash('sha256').update(bytes).digest('hex'),a.sha256,a.file);
    assert.equal(bytes.readUInt32BE(16),a.width);assert.equal(bytes.readUInt32BE(20),a.height);
    assets.set(a.file,a);
  }
}
for(const path of ['/models/','/models/v7-long-city-bus/certificate.private.json.gz','/prepared/index.json','/runs/','/gallery.json']){
  assert.equal(await status(path),404,path);
  assert.equal(await status(path,'HEAD'),404,path);
}
for(const path of ['/README.zh-CN.md','/MODEL-CASE-CATALOG.zh-CN.md','/human-error-research/README.zh-CN.md',
  '/global-splits.csv','/difficulty-all.json','/evaluation-sets.json'])assert.equal(await status(path),200,path);
const browser=await chromium.launch({channel:'chrome',headless:true});
const page=await browser.newPage({viewport:{width:1440,height:1000}}), errors=[];
page.on('pageerror',e=>errors.push(e.message));
await page.goto(base);await page.waitForSelector('article');
assert.equal(await page.locator('article').count(),21);
assert.match(await page.locator('#counts').innerText(),/798/);
await page.locator('#events').selectOption('3');assert.equal(await page.locator('article').count(),7);
assert.equal(await page.locator('article').first().locator('.timeline>div').count(),3);
assert.match(await page.locator('article').first().innerText(),/第一次干扰后的状态/);
await page.locator('#events').selectOption('');await page.locator('#track').selectOption('M-new-source');
assert.equal(await page.locator('article').count(),3);
const first=page.locator('article').first();
await first.locator('details summary').click();
const previous=await first.locator('.manual img').getAttribute('src');
await first.locator('.manual select').selectOption('1');
assert.notEqual(await first.locator('.manual img').getAttribute('src'),previous);
await first.locator('.compare').click();assert.equal(await page.locator('dialog[open]').count(),1);
await page.getByRole('button',{name:'关闭',exact:true}).click();
assert.equal(await page.locator('dialog[open]').count(),0);
await page.locator('#family').selectOption('early-cover');
assert.ok(await page.locator('article').count()>0);
await page.screenshot({path:`${out}/gallery-check.png`});
await page.setViewportSize({width:390,height:844});
assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth));
assert.deepEqual(errors,[]);
await browser.close();
const report={status:'PASS',models:models.length,conditions:models.reduce((n,m)=>n+m.cases.length,0),
  assetFiles:assets.size,allReferencedAssetHashesAndDimensions:'PASS',threeEventFilter:'PASS',
  newSourceFilter:'PASS',manualStepSwitch:'PASS',imageZoom:'PASS',mobileWidth:'PASS',
  privateRoutesBlocked:'PASS',browserErrors:errors,apiModelCalls:0};
writeFileSync(`${out}/gallery-checks.json`,JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report));
