/** Native scientific capture with a persistent, non-overwriting checkpoint. */
import { chromium } from '@playwright/test';
import { readFileSync,writeFileSync,mkdirSync,existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { resolve } from 'node:path';
import { parseArgs } from 'node:util';
import assert from 'node:assert/strict';
import type {} from '../../../src/evidence-v3/render';
const root=resolve(import.meta.dirname,'../../..'), data=resolve(root,'benchmark/ldraw-evidence-v3');
const hash=(b:Buffer|string)=>createHash('sha256').update(b).digest('hex');
const read=(p:string)=>JSON.parse(readFileSync(p,'utf8'));
const {values}=parseArgs({options:{model:{type:'string'},limit:{type:'string'},verify:{type:'boolean'}}});
const manifest=read(resolve(data,'visual-manifest.json'));
const checkpoint=resolve(data,'renders.json');
const rows:any[]=existsSync(checkpoint)?read(checkpoint).images:read(resolve(data,'retained-renders.json')).images;
const codeHash=hash(readFileSync(resolve(root,'src/evidence-v3/render.ts')));
for(const r of rows){
  assert.equal(hash(readFileSync(resolve(root,r.file))),r.sha256);
  if(r.kind==='candidate-labels')assert.equal(r.renderer_sha256,codeHash);
}
mkdirSync(resolve(root,'public/benchmark/evidence-v3/images'),{recursive:true});
mkdirSync(resolve(data,'render-audit'),{recursive:true});
function persist(){writeFileSync(checkpoint,JSON.stringify({dataset:manifest.dataset,
  status:rows.length===347?'rendered-human-qa-pending':'in-progress',images:rows},null,2)+'\n')}
persist();
const jobs=manifest.observations.filter((o:any)=>o.render_spec.kind==='candidate-labels')
  .sort((a:any,b:any)=>a.parent_task_id.localeCompare(b.parent_task_id)||a.arm.localeCompare(b.arm));
const browser=await chromium.launch({channel:'chrome',headless:true});
const context=await browser.newContext({viewport:{width:1320,height:900},deviceScaleFactor:1});
const page=await context.newPage();page.setDefaultTimeout(30000);
const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
let completed=0;
try{
  outer:for(const model of [...new Set<string>(jobs.map((o:any)=>o.source_id))]){
    if(values.model&&model!==values.model)continue;
    const pending=jobs.filter((o:any)=>o.source_id===model&&(values.verify||!rows.some(r=>r.observation_id===o.observation_id)));
    if(!pending.length)continue;
    await page.goto(`http://127.0.0.1:5173/evidence-v3-render.html?model=${encodeURIComponent(model)}`);
    await page.waitForFunction(()=>/^(Loaded|Error:)/.test(document.querySelector('#status')?.textContent??''));
    assert.equal(await page.locator('#status').textContent(),'Loaded',errors.join('\n'));
    for(const o of pending){
      await page.selectOption('#job',o.observation_id);
      await page.getByRole('button',{name:'Prepare image',exact:true}).click();
      await page.waitForFunction(()=>/^(Ready|Error:)/.test(document.querySelector('#status')?.textContent??''));
      assert.equal(await page.locator('#status').textContent(),'Ready',errors.join('\n'));
      const result=await page.evaluate(()=>window.__evidenceV3Capture!());assert.ok(result);
      const bytes=(key:'image'|'base'|'mask')=>Buffer.from(result[key].split(',')[1],'base64');
      const files={file:`public/benchmark/evidence-v3/images/${o.observation_id}.png`,
        base_file:`benchmark/ldraw-evidence-v3/render-audit/${o.observation_id}-base.png`,
        mask_file:`benchmark/ldraw-evidence-v3/render-audit/${o.observation_id}-labels.png`};
      if(values.verify){
        const old=rows.find(r=>r.observation_id===o.observation_id);assert.ok(old);
        assert.equal(hash(bytes('image')),old.sha256);assert.equal(hash(bytes('base')),old.base_sha256);
        assert.equal(hash(bytes('mask')),old.mask_sha256);
      }else{
        for(const [key,file]of Object.entries(files)){
          const b=bytes(key==='file'?'image':key==='base_file'?'base':'mask');
          assert.ok(!existsSync(resolve(root,file)));writeFileSync(resolve(root,file),b);
        }
        rows.push({observation_id:o.observation_id,kind:'candidate-labels',...files,
          sha256:hash(bytes('image')),base_sha256:hash(bytes('base')),mask_sha256:hash(bytes('mask')),
          renderer_sha256:codeHash,metadata:result.metadata});persist();
      }
      completed++;console.log(JSON.stringify({observation:o.observation_id,completed,total:134,saved:rows.length}));
      if(values.limit&&completed>=Number(values.limit))break outer;
    }
  }
  assert.equal(errors.length,0,errors.join('\n'));
}finally{await context.close();await browser.close()}
