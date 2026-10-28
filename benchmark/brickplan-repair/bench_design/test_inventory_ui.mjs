// Read-only production UI check: images, inventory and actual reference steps.
import {chromium} from 'playwright';
import assert from 'node:assert/strict';
import {mkdirSync,readFileSync,writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const out='deliverables/brickplan-quality-round/inventory-equivalence/ui-evidence';mkdirSync(out,{recursive:true});
const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
try{
 const page=await browser.newPage({viewport:{width:1440,height:1400}}),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 const tasks=await (await page.request.get('http://127.0.0.1:8808/api/tasks?role=gt&reviewer=A')).json();
 assert.equal(tasks.tasks.filter(x=>x.code.startsWith('I')).length,12);
 assert(tasks.tasks.filter(x=>x.code.startsWith('I')).every(x=>x.isNew));
 assert(!tasks.tasks.some(x=>/洛克|博物馆/.test(x.title)));
 for(const [code,frames,stock] of [['I005',5,'已装3块，剩余0块'],['I011',4,'已装2块，剩余0块'],['I002',5,'已装0块，剩余4块'],['I006',5,'不可用']]){
  await page.goto('http://127.0.0.1:8808/A?task='+code);
  await page.locator('#content:not(.hidden)').waitFor({timeout:90000});
  assert.equal(await page.locator('.step').count(),frames,code);
  assert((await page.locator('#inventoryText').textContent()).includes(stock),code);
  for(const id of ['current','result','goal','context','inventoryImage'])await page.locator('#'+id).evaluate(im=>im.decode());
  for(const im of await page.locator('.angle img,.step img').all())await im.evaluate(im=>{im.loading='eager';return im.decode();});
  await page.screenshot({path:out+'/'+code+'.png',fullPage:true});
  if(code==='I005'){
   const labels=await page.locator('.step span').allTextContents();assert.equal(labels.filter(s=>s.includes('拆下')).length,3);assert.equal(labels.filter(s=>s.includes('装上2×4')).length,1);
   await page.locator('.step').nth(1).click();for(const im of await page.locator('.pair img').all())await im.evaluate(im=>im.decode());
   await page.screenshot({path:out+'/I005-step.png'});await page.locator('.modal .close').click();
   await page.locator('[data-view="rear"]').click();await page.locator('#current').evaluate(im=>im.decode());
   assert((await page.locator('#current').getAttribute('src')).includes('view=rear'));
  }
 }
 const baseline=JSON.parse(readFileSync('/tmp/brick-inventory-original-votes.json'));
 for(const [path,hash] of Object.entries(baseline))assert.equal(createHash('sha256').update(readFileSync(path)).digest('hex'),hash,path);
 assert.deepEqual(errors,[]);
 writeFileSync(out+'/check.json',JSON.stringify({status:'PASS',taskCount:tasks.tasks.length,newInventoryTasks:12,retiredModelsAbsent:true,participantFilesPreserved:Object.keys(baseline).length,newVotes:0,pageErrors:errors,checked:['I005','I011','I002','I006']},null,2)+'\n');
 console.log('PASS inventory UI: allocation, horizontal/vertical repair, dynamic inventory, actual images and no participant writes');
}finally{await browser.close();}
