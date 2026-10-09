import {firefox,expect} from '@playwright/test';
import {mkdir,writeFile} from 'node:fs/promises';
const base=process.env.BRICKPLAN_TEST_URL||'http://127.0.0.1:8771';
const output=new URL('../../tem/brickplan-v2.2/validation/',import.meta.url);
await mkdir(output,{recursive:true});
const browser=await firefox.launch({headless:true});
const page=await browser.newPage({viewport:{width:1440,height:1080},deviceScaleFactor:2});
page.setDefaultTimeout(30000);
const errors=[];page.on('pageerror',e=>errors.push(e.message));
try{
  await page.goto(base);
  await expect(page.locator('#hero-canvas')).toHaveAttribute('width','1920',{timeout:60000});
  await expect(page.locator('.type-card')).toHaveCount(7);
  await expect(page.locator('#census')).toContainText('739');
  await expect(page.locator('#question-detail')).toContainText('评分');
  const before=await (await page.request.get(base+'/api/tasks')).json();
  await page.screenshot({path:new URL('portal-desktop.png',output).pathname,fullPage:true});
  await page.locator('#hero-canvas').click();
  await expect(page.locator('#zoom-dialog')).toBeVisible();
  await page.locator('#zoom-native').click();
  expect(await page.locator('#zoom-canvas').evaluate(c=>c.style.width)).toBe('1920px');
  await page.locator('#zoom-close').click();
  await page.locator('[data-category="repair"]').click();
  await expect(page.locator('#results-count')).toContainText('333');
  await page.locator('.question-row').first().click();
  await expect(page.locator('.checkpoint')).toBeVisible({timeout:30000});
  await expect(page.locator('#checkpoint-current')).toHaveAttribute('width','1920');
  const after=await (await page.request.get(base+'/api/tasks')).json();
  expect(after.tasks.map(t=>t.sessions)).toEqual(before.tasks.map(t=>t.sessions));
  await page.locator('#language').click();
  await expect(page.locator('#question-detail')).toContainText('ANSWER FORMAT');
  await page.locator('#language').click();
  await page.setViewportSize({width:390,height:844});
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
  await page.screenshot({path:new URL('portal-mobile.png',output).pathname,fullPage:true});
  await page.setViewportSize({width:1440,height:1080});
  const catalogue=await (await page.request.get(base+'/api/catalogue')).json();
  const probeStates=await (await page.request.get(base+'/api/probes')).json();
  const repair=catalogue.questions.find(q=>q.category==='repair'&&!probeStates.probes.find(p=>p.id===q.id).answered);
  await page.goto(`${base}/play?probe=${repair.id}`);
  await expect(page.locator('#probe-panel')).toBeVisible({timeout:30000});
  await expect(page.locator('#repair-context')).toBeVisible();
  await expect(page.locator('#checkpoint')).toHaveAttribute('width','1920');
  await page.locator('#submit-answer').click();
  await expect(page.locator('#probe-review')).toBeVisible();
  await expect(page.locator('#submit-answer')).toBeDisabled();
  await page.screenshot({path:new URL('repair-question.png',output).pathname,fullPage:true});
  const modelInfo=await (await page.request.get(base+'/api/models')).json();
  if(modelInfo.cases.length){
    await page.goto(base+'/#case');
    await expect(page.locator('.step-button')).toHaveCount(4,{timeout:60000});
    await expect(page.locator('.raw-output')).not.toBeEmpty();
    await page.locator('.step-button').first().click();
    await expect(page.locator('#step-detail')).toContainText('CALL 1');
    await page.screenshot({path:new URL('model-case.png',output).pathname,fullPage:true});
    await expect(page.locator('#model-run')).toBeDisabled();
  }
  expect(errors).toEqual([]);
  await writeFile(new URL('portal-validation.json',output),JSON.stringify({status:'passed',browser:'Firefox',deviceScaleFactor:2,
    checks:['7 categorized families','739 diagnostic items','full question contracts','1920px zoom',
      'preview does not start sessions','333 delayed-repair questions with checkpoint','bilingual interface',
      'mobile width','repair submission and review','recorded case when present'],errors},null,2));
  console.log('Portal browser checks passed.');
}catch(e){
  console.log('Failure:',page.url(),await page.locator('#status,#message').allTextContents(),errors);
  await page.screenshot({path:new URL('portal-failure.png',output).pathname,fullPage:true});
  throw e;
}finally{await browser.close();}
