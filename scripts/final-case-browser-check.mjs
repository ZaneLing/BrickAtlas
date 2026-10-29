// Read-only smoke check of the released gallery and historical directory.
import {chromium} from 'playwright';
import {readFileSync,writeFileSync} from 'node:fs';
import assert from 'node:assert/strict';
const base=process.env.BRICK_REVIEW_URL||'http://127.0.0.1:8810';
const dir='deliverables/brick-atlas-dataset-v1';
const release=JSON.parse(readFileSync(dir+'/release.json'));
const history=JSON.parse(readFileSync(dir+'/checks/count-correction/summary.json'));
const questions=readFileSync(dir+'/questions/static.jsonl','utf8').trim().split('\n').map(JSON.parse);
const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
const errors=[];const page=await browser.newPage({viewport:{width:1440,height:1080}});page.on('pageerror',e=>errors.push(e.message));
try {
 await page.goto(base+'/dataset/');await page.waitForSelector('#list button');
 const counts=await page.locator('#stats').innerText();assert(counts.includes(String(release.counts.runnableModels)));
 assert(counts.includes(String(release.counts.staticQuestions)));assert(counts.includes(String(release.counts.dynamicQuestions)));
 const cow=questions.filter(q=>q.model==='sc-2132-1');const paths=[];
 for(const q of cow){
  await page.goto(base+'/dataset/index.html?question='+encodeURIComponent(q.id)+'#'+q.model);
  await page.waitForSelector('tr.selected');assert.equal(await page.locator('tr.selected').getAttribute('data-question'),q.id);
  const current=page.getByAltText('当前状态',{exact:true});await current.waitFor();paths.push(await current.getAttribute('src'));
  await page.waitForFunction(()=>Array.from(document.images).every(x=>x.complete&&x.naturalWidth>0));
  for(const view of ['rear','top','isometric']){await page.locator('[data-view="'+view+'"]').click();await page.waitForFunction(()=>Array.from(document.images).every(x=>x.complete&&x.naturalWidth>0));assert((await page.getByAltText('当前状态',{exact:true}).getAttribute('src')).includes(view));}
  await page.locator('summary').click();assert((await page.locator('details pre').innerText()).includes(q.id));
 }
 assert.equal(new Set(paths).size,cow.length);
 await page.goto(base+'/dataset/all-questions.html');await page.waitForSelector('#rows tr');
 assert((await page.locator('#counts').innerText()).includes(String(history.current.total)));
 assert((await page.locator('#counts').innerText()).includes(String(history.allRecordDirectory)));
 await page.selectOption('#status','withheld-reference-check');
 assert((await page.locator('#found').innerText()).includes(String(history.recordStatuses['withheld-reference-check'])));
 const bus='E7:v7::v7-long-city-bus::static::buried-repair::t21';await page.fill('#search',bus);assert.equal(await page.locator('#rows tr').count(),1);assert((await page.locator('#rows').innerText()).includes('invisible'));
 await page.selectOption('#status','current-machine-checked');assert.equal(await page.locator('#rows tr').count(),0);
 assert.deepEqual(errors,[]);
 const out={passed:true,jsErrors:errors,models:release.counts.runnableModels,questions:history.current.total,staticCasesSwitched:cow.length,historicalRecords:history.allRecordDirectory,withheld:history.recordStatuses['withheld-reference-check'],checks:['release counts','question deep link','unique static images','three view switching','GT','historical status filters','withheld invisible bus absent from active questions']};writeFileSync(dir+'/checks/browser-check.json',JSON.stringify(out,null,2)+'\n');console.log(JSON.stringify(out));
} finally {await browser.close();}
