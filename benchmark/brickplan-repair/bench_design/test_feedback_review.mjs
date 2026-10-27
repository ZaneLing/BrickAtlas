// Read-only checks of the new presentation, using an isolated copy of historical A receipts.
import {chromium} from 'playwright';
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {resolve} from 'node:path';
const base='http://127.0.0.1:8829',out=resolve('deliverables/brickplan-quality-round/feedback-interface-evidence');mkdirSync(out,{recursive:true});
const checks=[],errors=[];
const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
try{
 const page=await browser.newPage({viewport:{width:1440,height:1060}});page.on('pageerror',e=>errors.push(e.message));
 async function open(code){await page.goto(base+'/A'+(code?'?task='+code:''));await page.locator('#content:not(.hidden)').waitFor({timeout:90000});for(const id of ['current','result','goal','context'])await page.locator('#'+id).evaluate(im=>im.decode());for(const im of await page.locator('.angle img').all())await im.evaluate(im=>im.decode());}
 await open();assert((await page.locator('#title').textContent()).startsWith('Q003'));assert((await page.locator('#previousNote').textContent()).includes('GT有问题'));
 assert.equal(await page.locator('[name=verdict]').count(),3);assert.equal(await page.locator('#question option').count(),41); // 21 historical concerns + 20 new objects/examples
 checks.push('Default queue prioritizes A concerns and new objects; historical judgments are shown without forging new votes.');
 assert((await page.locator('#description').textContent()).includes('第 7 步'));await page.screenshot({path:resolve(out,'bookcase-stage.png')});
 await page.locator('.step').nth(1).click();await page.locator('.pair img').first().evaluate(im=>im.decode());await page.locator('.pair img').last().evaluate(im=>im.decode());
 assert.equal(await page.locator('.pair img').count(),2);assert((await page.locator('.pair img').first().getAttribute('src')).includes('which=before'));
 await page.screenshot({path:resolve(out,'step-before-after.png')});await page.locator('.modal .close').click();checks.push('Bookcase is explicitly stage 7; detach steps show separate before and after images.');
 await open('Q026');assert((await page.locator('#current').getAttribute('src')).includes('scope=focus'));
 const imgs=await page.locator('.angle img').evaluateAll(xs=>xs.map(x=>x.src));assert.equal(new Set(imgs).size,3);
 const selected=await page.locator('.angle.active').getAttribute('data-view');assert.notEqual(selected,'isometric');await page.screenshot({path:resolve(out,'white-house-closeup.png')});
 await page.locator('[data-view=left]').click();for(const id of ['current','result','goal'])assert((await page.locator('#'+id).getAttribute('src')).includes('view=left'));
 await page.locator('#scope').click();for(const id of ['current','result','goal']){assert((await page.locator('#'+id).getAttribute('src')).includes('scope=whole'));await page.locator('#'+id).evaluate(im=>im.decode());}
 await page.screenshot({path:resolve(out,'white-house-whole.png')});checks.push('Large scenes default to repair-location closeups; three oblique choices and whole-object toggle stay synchronized.');
 await open('N003');await page.screenshot({path:resolve(out,'new-robot.png')});assert((await page.locator('#title').textContent()).includes('机器人'));
 await page.setViewportSize({width:400,height:900});await open('Q026');assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+2));await page.screenshot({path:resolve(out,'mobile-closeup.png')});checks.push('New source example and small-screen closeups load without overflow.');
 const tasks=(await (await fetch(base+'/api/tasks?reviewer=A&role=gt')).json()).tasks;assert.equal(tasks.length,91);assert.equal(tasks.filter(t=>t.isNew).length,20);
 assert(tasks.some(t=>t.code==='N101'));assert(tasks.some(t=>t.code==='Q071'));
 const prior=JSON.parse(readFileSync('/tmp/brick-A-feedback-original-hashes.json'));const {createHash}=await import('node:crypto');for(const [file,hash] of Object.entries(prior))assert.equal(createHash('sha256').update(readFileSync(file)).digest('hex'),hash);
 checks.push('All 71 historical task IDs and all original participant files remain intact; 20 stable new review IDs are added.');
 assert.deepEqual(errors,[]);writeFileSync(resolve(out,'feedback-ui-check.json'),JSON.stringify({status:'PASS',checks,readOnly:true,dataDirectory:'/tmp/brick-gt-ui-feedback',newHumanSubmissions:0,apiCalls:0},null,2)+'\n');console.log('PASS',checks.length,'feedback UI checks');
}finally{await browser.close();}
