// Actual DOM actions, no state mutation or private scene inspection.
import {firefox,expect} from '@playwright/test';
import {readFile,writeFile} from 'node:fs/promises';
const out='tem/brickplan-v1.2/validation';
const {url,fixtures}=JSON.parse(await readFile(`${out}/ui-fixtures.json`,'utf8'));
const browser=await firefox.launch({headless:true});
const page=await browser.newPage({viewport:{width:1440,height:1080}});
const errors=[],completed=[];
page.on('pageerror',e=>errors.push(e.message));
try {
  for(const fixture of fixtures) {
    const key=`${fixture.case}-${fixture.mode}`;
    await page.goto(`${url}/?session=${fixture.sessionId}`);
    await expect(page.locator('#message')).toContainText('Workcell ready',{timeout:20000});
    await expect(page.locator('canvas')).toHaveCount(4);
    const obs=JSON.parse(await page.locator('#observation').textContent());
    if(obs.track!=='image-id' || 'sites' in obs || 'inventory' in obs)throw Error('Visual leakage');
    if(completed.length===0)await page.locator('.renders').screenshot({path:`${out}/arena-initial.png`});
    await page.locator('#view').selectOption('exploded-reference');
    await page.locator('#inspect').click();
    await expect(page.locator('#inspection-count')).toContainText('31 inspections');
    await page.locator('#rework-yes').click();
    await expect(page.locator('#message')).toContainText('DIAGNOSIS_RECORDED');
    let revision=2;
    for(const a of fixture.actions) {
      if(a.type==='attach') {
        await page.locator('#part').selectOption(a.partId);
        await page.locator('#site').selectOption(a.siteId);
        await page.locator('#attach').click();
      } else if(a.type==='detach') {
        await page.locator('#part').selectOption(a.partId);
        await page.locator('#detach').click();
      } else await page.locator('#finish').click();
      revision++;
      await expect(page.locator('#counts')).toContainText(`revision ${revision}`,{timeout:20000});
      if(a.type!=='finish')await expect(page.locator('#message')).toContainText('· OK');
    }
    await expect(page.locator('#review')).toBeVisible();
    const score=JSON.parse(await page.locator('#score').textContent());
    if(score.status!=='success'||score.actionRegret!==0)throw Error(`Unexpected ${key} score`);
    const exported=page.waitForEvent('download');
    await page.locator('#export').click();
    await (await exported).saveAs(`${out}/${key}-public-trajectory.json`);
    const trajectory=JSON.parse(await readFile(`${out}/${key}-public-trajectory.json`,'utf8'));
    if(trajectory.events.length!==revision||trajectory.events.some(e=>'before'in e))throw Error('Export invalid');
    await page.locator('#replay').focus();
    await page.locator('#replay').press('Home');
    await expect(page.locator('#counts')).toContainText('revision 0',{timeout:20000});
    await expect(page.locator('#attach')).toBeDisabled();
    await page.locator('#feedback').fill('Software acceptance: original geometry, view budget, authoritative replay.');
    const feedback=page.waitForEvent('download');
    await page.locator('#export-feedback').click();
    await (await feedback).saveAs(`${out}/${key}-feedback.json`);
    completed.push({case:fixture.case,mode:fixture.mode,actions:fixture.optimalActions,
                    exportAndReplay:true,inspections:1});
    console.log('VERIFIED',key);
  }
  await page.locator('#mode').selectOption('probes');
  await expect(page.locator('#probe-panel')).toBeVisible();
  const shown=await page.locator('#session-label').textContent();
  await page.locator('#view').selectOption('top');
  await page.locator('#inspect').click();
  await expect(page.locator('#inspection-count')).toContainText('31 inspections');
  const ids=await page.locator('#task-select option').evaluateAll(items=>items.map(i=>i.value));
  await page.locator('#task-select').selectOption(ids.find(i=>i!==shown));
  await page.locator('#probe-form button').click();
  await expect(page.locator('#message')).toContainText(`Answer frozen for ${shown}`);
  await page.locator('#start').click();
  await expect(page.locator('#session-label')).not.toHaveText(shown);
  await page.setViewportSize({width:390,height:844});
  if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1))throw Error('Mobile overflow');
  await page.screenshot({path:`${out}/arena-mobile.png`,fullPage:true});
  if(errors.length)throw Error(errors.join('\n'));
  await writeFile(`${out}/browser-summary.json`,JSON.stringify({
    passed:true,softwareValidationOnly:true,browser:`Firefox ${browser.version()}`,
    completed,consoleErrors:errors,probeIdentityAndBudget:true,mobileOverflow:false,
  },null,2)+'\n');
} finally {await browser.close();}
