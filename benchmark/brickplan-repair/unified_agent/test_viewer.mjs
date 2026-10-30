import {chromium} from 'playwright';
import {mkdirSync,writeFileSync} from 'node:fs';
const root='http://127.0.0.1:8830',out='deliverables/brick-atlas-unified-agent-v1/checks';
mkdirSync(out,{recursive:true});
const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
try{
 const page=await browser.newPage({viewport:{width:1440,height:1100}}),errors=[];page.on('pageerror',e=>errors.push(String(e)));
 await page.goto(root+'/agent?run=agent-incident-openai-gpt-6-1-sol-20261030-175050-6d0c');await page.locator('#replay:not([hidden])').waitFor({timeout:60000});
 await page.locator('#next').click();await page.waitForFunction(()=>document.querySelector('#frameTitle').textContent.includes('第 1'));
 await page.locator('[data-view="rear"]').click();const rear=await page.locator('#current').getAttribute('src');
 await page.locator('[data-view="top"]').click();if(rear===await page.locator('#current').getAttribute('src'))throw Error('View did not change');
 await page.locator('#images img').first().click();if(await page.locator('#modal').isHidden())throw Error('Image zoom failed');
 await page.locator('#close').click();await page.getByText('模型输入 JSON',{exact:true}).click();
 const raw=await page.locator('#rawInput').getAttribute('href');const response=await fetch(root+raw);
 if(!response.ok)throw Error('Raw API request link broken');const body=await response.json();
 if(!body.messages?.some(m=>Array.isArray(m.content)&&m.content.some(b=>b.type==='image_url')))throw Error('Raw API request lacks images');
 await page.getByText('模型输入 JSON',{exact:true}).click();await page.locator('[data-view="isometric"]').click();
 await page.locator('#slider').fill('16');await page.locator('#slider').dispatchEvent('input');
 await page.screenshot({path:out+'/viewer.png',fullPage:true});
 if(errors.length)throw Error(errors.join('\n'));
 writeFileSync(out+'/viewer.json',JSON.stringify({passed:true,actualApiRun:true,viewSwitch:true,stepNavigation:true,imageZoom:true,rawRequestWithImages:true,errors},null,2));
 console.log('PASS agent replay: real run, steps, cameras, image zoom, raw API image bytes.');
}finally{await browser.close()}
