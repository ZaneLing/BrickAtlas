// Read-only checks of the real tool-controlled API run. No model calls.
import {chromium} from 'playwright';
import assert from 'node:assert/strict';
import {mkdirSync,writeFileSync} from 'node:fs';
import {resolve} from 'node:path';
const base='http://127.0.0.1:8810';
const out=resolve('deliverables/brickplan-dynamic-arena/ui-evidence');mkdirSync(out,{recursive:true});
const state=await(await fetch(base+'/api/state')).json();
assert.equal(state.protocol,'brick-atlas-tool-arena/2');assert.equal(state.calls.length,30);
const run=state.runId;
const log=await(await fetch(base+'/api/log?run='+run)).json();assert.equal(log.calls.length,30);
const raw=await(await fetch(base+'/api/raw-request?run='+run+'&call=1')).json();
assert.equal(raw.messages.at(-1).content.filter(x=>x.type==='image_url').length,0);
const raw2=await(await fetch(base+'/api/raw-request?run='+run+'&call=2')).json();
assert.equal(raw2.messages.at(-1).content.filter(x=>x.type==='image_url').length,3);
const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
const errors=[],writes=[],checks=[];
try{
 const page=await browser.newPage({viewport:{width:1440,height:1100}});
 page.on('pageerror',e=>errors.push(e.message));
 page.on('request',r=>{if(r.method()!=='GET')writes.push(r.url())});
 await page.goto(base);await page.locator('#logbox').waitFor({state:'visible'});
 await page.locator('#current').evaluate(im=>im.decode());await page.locator('#target').evaluate(im=>im.decode());
 assert((await page.locator('#result').textContent()).includes('尚未完成'));
 assert.equal(await page.locator('#decisions').textContent(),'30');
 assert.equal(await page.locator('#cost').textContent(),'$0.0143');
 assert((await page.locator('#inputJSON').textContent()).includes('availableTools'));
 assert((await page.locator('#outputJSON').textContent()).includes('tool'));
 assert((await page.locator('#environmentJSON').textContent()).includes('code'));
 await page.screenshot({path:resolve(out,'desktop-tool-final.png'),fullPage:true});
 checks.push('The viewer shows three JSON stages, the actual final state and settled API cost.');
 await page.locator('#timeline button').nth(1).click();
 assert((await page.locator('#action').textContent()).includes('主动观察'));
 assert.equal((await page.locator('#outputJSON').textContent()).includes('"observe"'),true);
 await page.locator('#timeline button').nth(4).click();
 assert((await page.locator('#event').textContent()).includes('模型没有收到'));
 for(const view of ['rear','top','isometric']){
  await page.locator(`[data-view=${view}]`).click();
  await page.locator('#current').evaluate(im=>im.decode());
 }
 await page.screenshot({path:resolve(out,'tool-hidden-intervention.png'),fullPage:true});
 checks.push('The event appears only in spectator replay and all scene angles load.');
 await page.locator('#timeline button').nth(2).click();await page.locator('#inputButton').click();
 assert(await page.locator('#modal').isVisible());await page.locator('#large').evaluate(im=>im.decode());
 await page.locator('#close').click();
 assert((await page.locator('#rawRequest').getAttribute('href')).includes('call=2'));
 assert.equal((await fetch(base+'/api/raw-request?run='+run+'&call=9999')).status,400);
 assert.equal((await fetch(base+'/api-ledger.private.json')).status,404);
 checks.push('The model-requested images, entire readable log and exact raw request are accessible without exposing the private ledger.');
 await page.setViewportSize({width:400,height:900});
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+2));
 await page.screenshot({path:resolve(out,'tool-mobile.png'),fullPage:true});
 assert.deepEqual(errors,[]);assert.deepEqual(writes,[]);
 checks.push('Mobile layout fits; viewing creates no API or assembly actions.');
 writeFileSync(resolve(out,'tools-checks.json'),JSON.stringify({status:'PASS',runId:run,checks,javascriptErrors:errors,mutatingRequests:writes,modelCallsDuringTest:0},null,2)+'\n');
 console.log('PASS',checks.length,'tool-arena UI checks');
}finally{await browser.close()}
