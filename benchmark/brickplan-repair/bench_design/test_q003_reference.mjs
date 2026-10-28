// Read-only verification of the live Q003 review page. No votes are submitted.
import {chromium} from 'playwright';
import assert from 'node:assert/strict';
import {mkdirSync,writeFileSync,readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const out='deliverables/brickplan-quality-round/reference-correction-evidence';mkdirSync(out,{recursive:true});
const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
try{
 const page=await browser.newPage({viewport:{width:1440,height:1120}}),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:8808/A?task=Q003');
 await page.locator('#content:not(.hidden)').waitFor({timeout:90000});
 assert.equal(await page.locator('.step').count(),9); // initial state + 8 actions
 assert((await page.locator('#description').textContent()).includes('左侧柱子全程不动'));
 const labels=await page.locator('.step span').allTextContents();assert(!labels.some(s=>s.includes('左柱')));
 for(const id of ['current','result','goal','context'])await page.locator('#'+id).evaluate(im=>im.decode());
 for(const im of await page.locator('.step img').all())await im.evaluate(im=>im.decode());
 await page.screenshot({path:out+'/q003.png'});
 await page.screenshot({path:'deliverables/brickplan-quality-round/feedback-interface-evidence/bookcase-stage.png'});
 await page.locator('.step').nth(1).click();
 for(const im of await page.locator('.pair img').all())await im.evaluate(im=>im.decode());
 assert((await page.locator('.modalbar span').textContent()).includes('2 / 9'));
 await page.screenshot({path:out+'/q003-step.png'});
 await page.screenshot({path:'deliverables/brickplan-quality-round/feedback-interface-evidence/step-before-after.png'});
 const original=JSON.parse(readFileSync('/tmp/brick-q003-original-votes.json'));
 for(const [p,hash] of Object.entries(original))assert.equal(createHash('sha256').update(readFileSync(p)).digest('hex'),hash);
 assert.deepEqual(errors,[]);
 writeFileSync(out+'/ui-check.json',JSON.stringify({status:'PASS',readOnly:true,referenceActions:8,frameCount:9,labels,participantFilesPreserved:Object.keys(original).length,newVotes:0},null,2)+'\n');
 console.log('PASS live Q003: eight actions, explicit left-column preservation, readable images, original participant files intact');
}finally{await browser.close();}
