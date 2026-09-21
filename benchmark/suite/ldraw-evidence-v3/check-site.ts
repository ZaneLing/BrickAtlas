/** Exercise evaluator delivery; this creates no human qualification evidence. */
import { chromium } from '@playwright/test';
import { createHash } from 'node:crypto';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import assert from 'node:assert/strict';

const root=resolve(import.meta.dirname,'../../..');
const data=resolve(root,'benchmark/ldraw-evidence-v3');
const output=resolve(data,'inspection/site');
mkdirSync(output,{recursive:true});
const browser=await chromium.launch({channel:'chrome',headless:true});
const context=await browser.newContext({viewport:{width:1440,height:1000}});
const page=await context.newPage();
const errors:string[]=[];
page.on('pageerror',e=>errors.push(e.message));
const base='http://127.0.0.1:5173';
const target='ld2-omr-42004-shape-match-1';
const digest=(bytes:Buffer)=>createHash('sha256').update(bytes).digest('hex');
const checks:Record<string,unknown>={};
try{
  await page.goto(base+'/evidence-v3.html');
  await page.locator('#load-status').filter({hasText:'Loaded 617'}).waitFor();
  assert.equal(await page.locator('#prior-rows tr').count(),9);
  assert.equal(await page.locator('#roster-rows tr').count(),3);
  assert.match(await page.locator('#availability').innerText(),/0\/694.*0\/9/);
  await page.screenshot({path:resolve(output,'desktop.png')});
  checks.loaded_inventory={dossiers:617,pairs:140,prior_rows:9,roster_rows:3};
  await page.locator('#pair-family').selectOption('shape-match');
  assert.equal(await page.locator('#pair-select option').count(),67);
  const option=page.locator('#pair-select option').filter({hasText:target});
  await page.locator('#pair-select').selectOption(await option.getAttribute('value') as string);
  await page.waitForFunction(()=>document.querySelectorAll('#pair-images [data-loaded=true]').length===2);
  assert.deepEqual(await page.locator('#pair-images strong').allTextContents(),
                   ['Gold: B0036 (C)','Gold: B0116 (D)']);
  await page.locator('#pair-images').screenshot({path:resolve(output,'part-type-pair.png')});
  await page.locator('#native').click();
  assert.equal(await page.locator('#pair-images canvas').first().evaluate(c=>c.getBoundingClientRect().width),1280);
  await page.locator('#native').click();
  await page.locator('#aux summary').click();
  assert.equal(await page.locator('#aux details').getAttribute('open'),'');
  checks.pair={parent:target,golds:['C','D'],native_width:1280,auxiliary_reveal:true};
  await page.locator('#search').fill(target);
  assert.match(await page.locator('#count').innerText(),/^1 of 617/);
  await page.locator('#dossier-rows button').click();
  assert.equal(await page.locator('#dossier-detail [data-pair]').getAttribute('data-pair'),
               'pair3-6c9207951ac68b039e3f152c');
  const sourceLink=await page.locator('#dossier-detail a').first().getAttribute('href');
  await page.locator('#dossier-detail [data-pair]').click();
  assert.equal(await page.locator('#pair-select').inputValue(),'pair3-6c9207951ac68b039e3f152c');
  await page.locator('#reset').click();
  assert.match(await page.locator('#count').innerText(),/^617 of 617/);
  await page.locator('#next').click();
  assert.match(await page.locator('#count').innerText(),/Page 2 of 25/);
  await page.locator('#previous').click();
  checks.dossier={search:true,pagination:true,current_pair_overlay:true,source_link:sourceLink};
  await page.setViewportSize({width:390,height:844});
  await page.goto(base+'/evidence-v3.html');
  await page.locator('#load-status').filter({hasText:'Loaded 617'}).waitFor();
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
  await page.screenshot({path:resolve(output,'mobile.png')});
  await page.locator('#pair-images').screenshot({path:resolve(output,'mobile-pair.png')});
  checks.mobile={width:390,horizontal_document_overflow:false};
  await page.setViewportSize({width:1440,height:1000});
  await page.goto(base+sourceLink);
  await page.locator('h3').filter({hasText:'B0035'}).waitFor();
  const slider=page.getByRole('slider',{name:'展开程度',exact:true});
  const canvas=page.locator('canvas').first();
  // Native UI input; the frozen viewer's WebGL result must change.
  const before=await canvas.screenshot();
  await slider.fill('0.35');
  assert.equal(await slider.inputValue(),'0.35');
  const expanded=await canvas.screenshot();
  assert.notEqual(digest(before),digest(expanded));
  await slider.fill('0');
  const box=await canvas.boundingBox();assert.ok(box);
  await page.mouse.move(box.x+box.width*.5,box.y+box.height*.5);
  await page.mouse.down();
  await page.mouse.move(box.x+box.width*.7,box.y+box.height*.58,{steps:12});
  await page.mouse.up();
  const rotated=await canvas.screenshot();
  assert.notEqual(digest(before),digest(rotated));
  await page.mouse.wheel(0,-180);
  const zoomed=await canvas.screenshot();
  assert.notEqual(digest(rotated),digest(zoomed));
  writeFileSync(resolve(output,'source-viewer.png'),zoomed);
  checks.source_viewer={canvas:true,expansion:true,rotation:true,zoom:true,source_poses_edited:false};
  assert.equal(errors.length,0,errors.join('\n'));
  const paired=JSON.parse(readFileSync(resolve(root,'public/benchmark/evidence-v3/paired-observations.json'),'utf8'));
  const responses=[];
  for(const pair of paired.pairs){
    for(const observation of pair.observations){
      const response=await page.request.get(base+observation.image);
      assert.equal(response.status(),200);
      const body=await response.body();
      const file=readFileSync(resolve(root,'public',observation.image.slice(1)));
      assert.equal(digest(body),digest(file));
      responses.push(observation.observation_id);
    }
  }
  checks.native_image_routes={checked:responses.length,http_200:true,exact_file_hashes:true};
  writeFileSync(resolve(data,'site-validation.json'),JSON.stringify({
    status:'passed',checks,browser_errors:errors,human_judgments_created:0,
    scope:'Evaluator UI and source-viewer delivery only; not human visual-task certification.'
  },null,2)+'\n');
  console.log(JSON.stringify({status:'passed',checks:Object.keys(checks),images:responses.length}));
}finally{await context.close();await browser.close()}
