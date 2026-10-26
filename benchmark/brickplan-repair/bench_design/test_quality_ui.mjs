// Real local HTTP/UI regressions. Run against an isolated --data-dir, never live human data.
import {chromium} from 'playwright';
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {resolve,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
const here=dirname(fileURLToPath(import.meta.url)),root=resolve(here,'../../..');
const base=process.env.BRICK_QUALITY_TEST_URL||'http://127.0.0.1:8818';
const data=process.env.BRICK_QUALITY_TEST_DATA||'/tmp/brick-quality-ui-qa-v2';
assert(data.startsWith('/tmp/'),'Do not run automated responses in real participant storage.');
const out=resolve(root,'deliverables/brickplan-quality-round/interface-evidence');mkdirSync(out,{recursive:true});
const errors=[],checks=[];
async function request(path,body){const response=await fetch(base+path,body?{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}:{});return {status:response.status,data:await response.json()};}
const id=(reviewer,code,role='blind')=>({reviewer,code,role});
for(let i=0;i<60;i++){
 try{if((await request('/health')).status===200)break;}catch{}
 if(i===59)throw Error('Isolated review server did not start');
 await new Promise(r=>setTimeout(r,500));
}
const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
try{
const page=await browser.newPage({viewport:{width:1440,height:1100}});page.on('pageerror',e=>errors.push(e.message));
await page.goto(base+'/A');await page.locator('#reviewFields [name=goal]').first().waitFor({timeout:90000});
await page.locator('[name=goal][value=yes]').check();await page.waitForFunction(()=>document.querySelector('#saveStatus').textContent.includes('已保存'));
await page.locator('[data-code=Q002]').click();await page.waitForFunction(()=>document.querySelector('#taskIntro h2')?.textContent==='Q002 · 独立操作');
assert.equal(await page.locator('[name=goal]:checked').count(),0,'Q001 choices must not leak to Q002');
await page.locator('[data-code=Q001]').click();await page.waitForFunction(()=>document.querySelector('#taskIntro h2')?.textContent==='Q001 · 独立操作');
assert(await page.locator('[name=goal][value=yes]').isChecked());
await page.reload();await page.locator('#reviewFields [name=goal]').first().waitFor({timeout:90000});
assert(await page.locator('[name=goal][value=yes]').isChecked());checks.push('Answers survive task navigation and browser reload.');
// Save complete snapshots: rapid answers arriving out of order cannot drop fields.
await page.evaluate(()=>{document.querySelector('[name=view][value=clear_after_views]').click();document.querySelector('[name=operation][value=clear]').click();document.querySelector('[name=change][value=unsure]').click();});
await page.waitForFunction(()=>document.querySelector('#saveStatus').textContent.includes('已保存'));
await page.reload();await page.locator('#reviewFields [name=goal]').first().waitFor({timeout:90000});
assert(await page.locator('[name=view][value=clear_after_views]').isChecked());assert(await page.locator('[name=operation][value=clear]').isChecked());assert(await page.locator('[name=change][value=unsure]').isChecked());
await page.evaluate(()=>scrollTo(0,0));await page.locator('#scenes img').first().evaluate(image=>image.decode());
await page.screenshot({path:resolve(out,'desktop.png')});
// Pick an actual visible colored piece through exactly the public current-image coordinates.
const picture=page.locator('#scenes img').first();await picture.waitFor();
const point=await picture.evaluate(async image=>{await image.decode();const c=document.createElement('canvas');c.width=image.naturalWidth;c.height=image.naturalHeight;const ctx=c.getContext('2d');ctx.drawImage(image,0,0);const p=ctx.getImageData(0,0,c.width,c.height).data;for(let y=80;y<580;y+=4)for(let x=30;x<770;x+=4){const i=(y*c.width+x)*4;if(p[i]>170&&p[i+1]<120&&p[i+2]<120){const b=image.getBoundingClientRect();return {x:x/c.width*b.width,y:y/c.height*b.height};}}throw Error('No visible red test piece found');});
await picture.click({position:point});await page.waitForFunction(()=>document.querySelectorAll('#catalogues img').length>0,{},{timeout:90000});
assert((await page.locator('#feedback').textContent()).includes('检查图'));
await page.locator('#catalogues img').first().click({position:{x:40,y:40}});
assert((await page.locator('#feedback').textContent()).includes('已选择位置'));
checks.push('Visible-piece pointing returns an anonymous handle and neutral complete position cards; clicking a card selects without installing.');
await page.screenshot({path:resolve(out,'positions.png')});
// A correct control can be submitted by itself, without filling the whole bank.
await page.locator('[data-code=Q002]').click();await page.waitForFunction(()=>document.querySelector('#taskIntro h2')?.textContent==='Q002 · 独立操作');
await page.locator('#finish').click();await page.waitForFunction(()=>document.querySelector('#taskIntro').textContent.includes('操作已结束'),{},{timeout:90000});
for(const [key,value] of Object.entries({goal:'yes',view:'clear',operation:'clear',change:'no',effort:'independent'})){
 await page.locator(`[name=${key}][value=${value}]`).check();await page.waitForTimeout(60);
}
await page.locator('#independent').check();await page.locator('#submitReview').click();
await page.waitForFunction(()=>document.querySelector('#saveStatus').textContent.includes('本题已提交'),{},{timeout:90000});
checks.push('One finished question submits independently; no all-questions gate.');
const b=await browser.newPage();await b.goto(base+'/B');await b.locator('#reviewFields [name=goal]').first().waitFor({timeout:90000});
await b.locator('[data-code=Q002]').click();await b.waitForFunction(()=>document.querySelector('#taskIntro h2')?.textContent==='Q002 · 独立操作');
assert.equal(await b.locator('[name=goal]:checked').count(),0);checks.push('Reviewer B has independent empty answers, not copied from A.');
const opened=await request('/api/open',id('B','Q002'));
const action={...id('B','Q002'),revision:opened.data.revision,requestId:'duplicate-finish-test',action:{type:'finish'}};
const one=await request('/api/action',action),two=await request('/api/action',action);
assert.equal(one.data.revision,1);assert.equal(two.data.revision,1);
const stale=await request('/api/action',{...action,requestId:'stale-other-request'});assert.equal(stale.status,409);assert.equal(stale.data.revision,1);
checks.push('Duplicate and stale action requests do not execute twice.');
// The physical page is gated until the corresponding blind operation is submitted.
const locked=await request('/api/open',id('A','P001','physics'));assert(locked.data.locked);
const required=locked.data.requiredBlindTask;await request('/api/open',id('A',required));
const current=await request('/api/open',id('A',required));
await request('/api/action',{...id('A',required),revision:current.data.revision,requestId:'end-unfinished-qa',action:{type:'finish'}});
const ratings={goal:'yes',view:'clear',operation:'clear',change:'unsure',effort:'unfinished',independent:true};
assert.equal((await request('/api/submit',{...id('A',required),answerRevision:99,ratings})).status,200);
const physical=await request('/api/open',id('A','P001','physics'));assert(!physical.data.locked);assert(physical.data.images.length>=4);
assert(!('engineResult' in physical.data)&&!('independentResult' in physical.data));
assert(physical.data.externalScenePackage.notTarget);
const external=await fetch(base+physical.data.externalScenePackage.file),archive=Buffer.from(await external.arrayBuffer());
assert.equal(external.status,200);assert.equal(archive.subarray(0,2).toString(),'PK');
for(const name of ['before.ldr','proposed.ldr','moving-part.ldr','environment.json'])assert(archive.includes(Buffer.from(name)));
checks.push('After the blind gate, independent reviewers can download exact before/proposed LDraw scenes without a target or engine verdict.');
await request('/api/submit',{...id('A','P001','physics'),answerRevision:1,ratings:{verdict:'uncertain',reason:'unclear_image',method:'images',independent:true}});
checks.push('Mechanical checks are blinded to engine/backend verdicts and keep uncertainty rather than forcing a guess.');
for(const code of ['Q008','Q009','Q010','Q011','Q012'])await request('/api/open',id('A',code));
const resumed=await request('/api/open',id('A','Q001'));assert.equal(resumed.status,200);assert.equal(resumed.data.ratings.goal,'yes');assert(resumed.data.revision>=1);
checks.push('Evicted sessions reconstruct from the saved action log without losing answers or operations.');
await page.locator('[data-role=physics]').click();await page.locator('[data-code=P001]').waitFor();await page.locator('[data-code=P001]').click();await page.waitForFunction(()=>document.querySelector('#taskIntro h2')?.textContent==='P001 · 拆装合理性检查',{},{timeout:90000});
assert((await page.locator('#sceneTitle').textContent()).includes('不是目标答案'));assert.equal(await page.locator('#taskIntro img').count(),1);
await page.evaluate(()=>scrollTo(0,0));await page.locator('#scenes img').first().evaluate(image=>image.decode());
await page.screenshot({path:resolve(out,'physics.png')});
await page.setViewportSize({width:400,height:900});await page.goto(base+'/C');await page.locator('#reviewFields [name=goal]').first().waitFor({timeout:90000});
assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+2),'No narrow-screen horizontal overflow');
await page.screenshot({path:resolve(out,'mobile.png')});checks.push('The 400px page fits without horizontal overflow.');
const manager=JSON.parse(readFileSync(resolve(data,'manager-key.private.json'))).key;
const helped=await request('/api/open',id('C','Q002'));
await request('/api/action',{...id('C','Q002'),revision:helped.data.revision,requestId:'helped-feedback-qa',action:{type:'finish'}});
assert.equal((await request('/api/submit',{...id('C','Q002'),answerRevision:1,ratings:{goal:'yes',view:'clear',operation:'clear',change:'no',effort:'helped',independent:false}})).status,200);
checks.push('Helped/non-independent feedback can be submitted and retained without earning independent qualification.');
const summary=await request('/api/summary?key='+encodeURIComponent(manager));
assert.equal(summary.data.submittedBlind,2);assert.equal(summary.data.submittedPhysics,1);
assert.equal(summary.data.receivedBlindResponses,3);assert.equal(summary.data.blind.find(x=>x.code==='Q002').nonIndependentSubmissions,1);
assert(summary.data.admission.some(x=>x.unresolvedPhysics.includes('P024')));
assert(summary.data.physics.find(p=>p.code==='P001').status.includes('分歧'));
assert.equal((await request('/api/summary')).status,403);
assert.equal((await request('/challenges.private.json.gz')).status,404);
checks.push('Manager summary counts actual distinct submissions; disagreement pauses admission and private records are not served.');
assert.deepEqual(errors,[]);
writeFileSync(resolve(out,'automated-ui-check.json'),JSON.stringify({status:'PASS',checks,javascriptErrors:errors,automated:true,participantDataDirectory:data,realHumanSubmissions:0,scope:'Coding/UI regression fixtures only. All simulated choices are in /tmp, isolated from participant storage.'},null,2)+'\n');
console.log('PASS',checks.length,'real HTTP/UI regressions; QA responses isolated from participants.');
}finally{await browser.close();}
