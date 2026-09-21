/** Verify six independent native-image queues without creating human judgments. */
import { chromium } from '@playwright/test';
import { createHash } from 'node:crypto';
import { readFileSync,writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import assert from 'node:assert/strict';
const root=resolve(import.meta.dirname,'../../..');
const browser=await chromium.launch({channel:'chrome',headless:true});
const context=await browser.newContext({viewport:{width:1460,height:1000},acceptDownloads:true});
const page=await context.newPage();
const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
const checks:any[]=[];
try{
  for(let i=1;i<=6;i++){
    const relative=`benchmark/ldraw-evidence-v3/qa/initial/reviewer-${i}`;
    const bytes=readFileSync(resolve(root,relative,'queue.json')),queue=JSON.parse(bytes.toString());
    await page.goto(`http://127.0.0.1:5173/${relative}/index.html`);
    await page.waitForFunction(()=>document.querySelector('#progress')?.textContent?.includes('0 saved'));
    assert.equal(await page.locator('#token').textContent(),queue.queue[0].review_id);
    await page.locator('#stimulus').evaluate(async (img:HTMLImageElement)=>{await img.decode()});
    const image=await page.locator('#stimulus').evaluate((img:HTMLImageElement)=>({
      size:[img.naturalWidth,img.naturalHeight,img.width,img.height],src:img.src}));
    assert.deepEqual(image.size,[1280,800,1280,800]);assert.equal(image.src,queue.queue[0].image);
    assert.equal(await page.locator('#question').textContent(),queue.queue[0].payload.question);
    await page.getByRole('button',{name:'Next',exact:true}).click();
    assert.equal(await page.locator('#token').textContent(),queue.queue[1].review_id);
    await page.getByRole('button',{name:'Previous',exact:true}).click();
    assert.equal(await page.locator('#token').textContent(),queue.queue[0].review_id);
    const promise=page.waitForEvent('download');
    await page.getByRole('button',{name:'Export feedback JSON',exact:true}).click();
    const download=await promise,file=await download.path();assert.ok(file);
    const feedback=JSON.parse(readFileSync(file,'utf8'));
    assert.equal(feedback.reviews.length,0);
    assert.equal(feedback.queue_sha256,createHash('sha256').update(bytes).digest('hex'));
    checks.push({slot:queue.slot,observations:queue.queue.length,native_pixels:true,
                 exact_question_and_image:true,navigation:true,empty_feedback_export:true});
  }
  assert.equal(errors.length,0,errors.join('\n'));
  writeFileSync(resolve(root,'benchmark/ldraw-evidence-v3/qa/ui-validation.json'),
    JSON.stringify({status:'passed',checks,human_judgments_created:0,browser_errors:errors},null,2)+'\n');
  console.log(JSON.stringify({status:'passed',queues:6,human_judgments_created:0}));
}finally{await context.close();await browser.close()}
