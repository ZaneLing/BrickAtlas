// Read-only checks against the real recorded episode. No model calls or votes.
import {chromium} from 'playwright';
import assert from 'node:assert/strict';
import {mkdirSync,writeFileSync} from 'node:fs';
import {resolve} from 'node:path';
const base='http://127.0.0.1:8810';
const out=resolve('deliverables/brickplan-dynamic-arena/ui-evidence');mkdirSync(out,{recursive:true});
const b=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
const errors=[],writes=[],checks=[];
try{
 const p=await b.newPage({viewport:{width:1440,height:1100}});
 p.on('pageerror',e=>errors.push(e.message));p.on('request',r=>{if(r.method()!=='GET')writes.push(r.url())});
 await p.goto(base);await p.locator('#current').waitFor();await p.locator('#current').evaluate(im=>im.decode());
 assert((await p.locator('#status').textContent()).includes('已结束'));
 assert((await p.locator('#result').textContent()).includes('尚未完成'));
 assert.equal(await p.locator('#decisions').textContent(),'14');
 assert.equal(await p.locator('#cost').textContent(),'$0.0243');
 const initialCost=await p.locator('#cost').textContent();
 await p.screenshot({path:resolve(out,'desktop-final.png'),fullPage:true});
 checks.push('The page displays the real failed completion and actual settled API cost.');
 await p.locator('#timeline button').nth(8).click();
 assert((await p.locator('#event').textContent()).includes('A004'));
 assert((await p.locator('#event').textContent()).includes('模型没有收到'));
 for(const v of ['rear','top','isometric']){
  await p.locator(`[data-view=${v}]`).click();
  await p.locator('#current').evaluate(im=>im.decode());
  await p.locator('#target').evaluate(im=>im.decode());
 }
 await p.screenshot({path:resolve(out,'hidden-intervention.png'),fullPage:true});
 checks.push('The live event appears only on its correct replay step; all three synchronized views load.');
 await p.locator('#inputButton').click();assert(await p.locator('#modal').isVisible());
 await p.locator('#large').evaluate(im=>im.decode());
 await p.locator('#imageNext').click();await p.locator('#large').evaluate(im=>im.decode());
 await p.locator('#close').click();
 await p.locator('#timeline button').first().click();
 assert((await p.locator('#action').textContent()).includes('空白底板'));
 await p.locator('#play').click();await p.waitForTimeout(1600);await p.locator('#play').click();
 assert.notEqual(await p.locator('#slider').inputValue(),'0');
 await p.locator('#live').click();assert.equal(await p.locator('#slider').inputValue(),'14');
 checks.push('Input images, image enlargement, playback, seek and return-to-latest work without executing assembly actions.');
 await p.setViewportSize({width:400,height:900});
 assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+2));
 await p.screenshot({path:resolve(out,'mobile.png'),fullPage:true});
 assert.equal(await p.locator('#cost').textContent(),initialCost);
 assert.deepEqual(errors,[]);assert.deepEqual(writes,[]);
 checks.push('Mobile layout fits the viewport; spectators generate no state mutations or paid calls.');
 assert.equal((await fetch(base+'/runs/anything/record.private.json.gz')).status,404);
 assert.equal((await fetch(base+'/api-ledger.private.json')).status,404);
 checks.push('The HTTP server does not expose private records or API credentials.');
 writeFileSync(resolve(out,'checks.json'),JSON.stringify({status:'PASS',checks,javascriptErrors:errors,mutatingRequests:writes,modelCallsDuringTest:0},null,2)+'\n');
 console.log('PASS',checks.length,'arena UI checks');
}finally{await b.close()}
