import {firefox,expect as baseExpect} from '@playwright/test';
import {mkdir,writeFile} from 'node:fs/promises';

const url=process.env.BRICKPLAN_TEST_URL||'http://127.0.0.1:8770';
const expect=baseExpect.configure({timeout:30000});
const output=new URL('../../tem/brickplan-v2.3/validation/',import.meta.url);
await mkdir(output,{recursive:true});
const browser=await firefox.launch({headless:true});
const page=await browser.newPage({viewport:{width:1460,height:1050}});
page.setDefaultTimeout(30000);
const errors=[];page.on('pageerror',e=>errors.push(e.message));
try{
  const catalogue=await (await page.request.get(url+'/api/catalogue')).json();
  const episode=catalogue.questions.find(q=>q.form==='episode'&&q.stableId==='kart-deck-08');
  await page.goto(url+'/play?task='+episode.id);
  await expect(page.locator('#message')).toContainText('Workcell ready',{timeout:30000});
  await expect(page.locator('#current')).toHaveAttribute('width','1920');
  await expect(page.locator('#rack-count')).toContainText('holders occupied');
  await page.screenshot({path:new URL('arena-desktop.png',output).pathname,fullPage:true});
  const identity=new URL(page.url()).searchParams.get('session');
  const initial=await (await page.request.get(`${url}/api/sessions/${identity}`)).json();
  expect(initial.observation.track).toBe('image-id');
  expect(initial.observation.sites).toBeUndefined();
  await page.locator('#view').selectOption('top');
  await page.locator('#inspect').click();
  await expect(page.locator('#inspection-count')).toContainText('11 views');
  await page.locator('#view').selectOption('front');
  await page.locator('#inspect').click();
  await expect(page.locator('#inspection-count')).toContainText('10 views');
  await page.locator('#saved-view').selectOption('0');
  await page.locator('#show-view').click();
  await expect(page.locator('#attach')).toBeDisabled();
  await page.locator('#saved-view').selectOption('');
  await page.locator('#show-view').click();
  await expect(page.locator('#attach')).toBeEnabled();
  // Exercise operation accounting using only the public interface.
  await page.locator('#audit').click();
  await expect(page.locator('#counts')).toContainText('1 /');
  await page.locator('#error-no').click();
  await expect(page.locator('#inspection-count')).toContainText('11 diagnoses');
  await page.locator('#finish').click();
  await expect(page.locator('#review')).toBeVisible();
  await expect(page.locator('#attach')).toBeDisabled();
  await page.locator('#replay').focus();
  await page.locator('#replay').press('Home');
  await page.locator('#replay').press('Tab');
  await expect(page.locator('#frame-label')).toContainText('0 /');
  await page.locator('#show-view').click();
  await expect(page.locator('#attach')).toBeDisabled();
  await page.locator('#open-3d').click();
  await expect(page.locator('#three-stage canvas')).toBeVisible({timeout:20000});
  const box=await page.locator('#three-stage canvas').boundingBox();
  await page.mouse.move(box.x+box.width*.5,box.y+box.height*.5);
  await page.mouse.down();await page.mouse.move(box.x+box.width*.65,box.y+box.height*.6,{steps:8});await page.mouse.up();
  await page.locator('#explode').focus();await page.locator('#explode').press('End');
  await expect(page.locator('#explode-note')).toContainText('not an executable assembly');
  await page.locator('#free-review').screenshot({path:new URL('arena-3d-review.png',output).pathname});
  await page.locator('#mode').selectOption('probes');
  await expect(page.locator('#task-select')).toHaveValue(/^Q/);
  const probeCatalog=await (await page.request.get(`${url}/api/probes`)).json();
  await page.locator('#task-select').selectOption(probeCatalog.probes.find(p=>!p.answered).id);
  await page.locator('#start').click();
  await expect(page.locator('#probe-panel')).toBeVisible();
  await expect(page.locator('#attach')).toBeDisabled();
  await page.locator('#view').selectOption('rear');
  await page.locator('#inspect').click();
  await expect(page.locator('#inspection-count')).toContainText('11 views');
  await page.locator('#submit-answer').click();
  await expect(page.locator('#message')).toContainText('Answer frozen');
  await expect(page.locator('#submit-answer')).toBeDisabled();
  await expect(page.locator('#inspect')).toBeDisabled();
  await page.reload();
  await expect(page.locator('#message')).toContainText('Answer recorded and frozen');
  await page.setViewportSize({width:390,height:844});
  await page.screenshot({path:new URL('arena-mobile.png',output).pathname,fullPage:true});
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBe(true);
  expect(errors).toEqual([]);
  await writeFile(new URL('browser-validation.json',output),JSON.stringify({
    status:'passed',browser:'Firefox',checks:['source rasters','image-track isolation','multi-view history',
      'saved-view action guard','operation and diagnosis','ended-frame guard','3D orbit and explosion',
      'probe inspection and answer freeze','reload persistence','mobile width'],errors},null,2));
  console.log('Browser checks passed.');
}catch(error){
  console.log('Visible failure state:',await page.evaluate(()=>({
    message:document.getElementById('message').textContent,
    mode:document.getElementById('mode').value,
    selectedTask:document.getElementById('task-select').value,
    startDisabled:document.getElementById('start').disabled,
    url:location.href})),errors);
  throw error;
}finally{await browser.close();}
