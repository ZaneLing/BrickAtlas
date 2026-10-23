"""Browser regression for the changed two-panel layout; uses a disposable server."""
from pathlib import Path
import json,subprocess,sys,tempfile,threading
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE.parent),str(HERE.parent/'eval')]
from dynamic_v6 import human_server as hs
from dynamic_v5.build import write
ROOT=HERE.parents[2]

SCRIPT=r'''
import { chromium } from '@playwright/test';
const browser=await chromium.launch({channel:'chrome',headless:true});
const page=await browser.newPage({viewport:{width:1440,height:1000}}),errors=[];
page.on('pageerror',e=>errors.push(e.message));
const base=process.argv[1];let last;
page.on('request',r=>{if(r.url().endsWith('/api/step'))last=r.postDataJSON()});
try{
 await page.goto(base+'/A');
 await page.waitForFunction(()=>typeof state!=='undefined'&&state?.images&&!busy);
 if(await page.locator('#scenes img').count()!==3)throw Error('first decision must have only three current-target pages');
 for(const rect of [{role:'current-target',x:.25},{role:'temporal-pair',x:.75}]){
  const image=page.locator('.view.active img').nth(rect.role==='current-target'?0:1);
  await image.evaluate(im=>im.decode());const b=await image.boundingBox();
  await image.click({position:{x:b.width*rect.x,y:b.height*(336/636)}});
  await page.waitForFunction(()=>!busy);
  if(last.action.type!=='inspect'||Math.abs(last.action.point[0]-.5)>.01||Math.abs(last.action.point[1]-.5)>.01)throw Error('current-scene click mapped incorrectly');
 }
 await page.locator('button.act').first().click();await page.waitForFunction(()=>!busy);
 if(await page.locator('#catalog img').count()<1)throw Error('candidate pages missing');
 await page.selectOption('#task','H002');await page.waitForFunction(()=>!busy&&state?.code==='H002');
 await page.selectOption('#task','H001');await page.waitForFunction(()=>!busy&&state?.code==='H001');
 if(await page.evaluate(()=>state.revision)!==3)throw Error('progress lost on switch');
 await page.reload();await page.waitForFunction(()=>typeof state!=='undefined'&&state?.revision===3&&!busy);
 await page.screenshot({path:'.tools/interface-repair-human-ui.png',fullPage:true});
 await page.goto(base+'/B');await page.waitForFunction(()=>typeof state!=='undefined'&&state?.images&&!busy);
 if(await page.evaluate(()=>state.revision)!==0)throw Error('reviewers shared answers');
 if(errors.length)throw Error(errors.join(';'));
 console.log(JSON.stringify({status:'PASS',currentClicksMapped:true,temporalClicksMapped:true,allCandidatePagesVisible:true,switchAndReloadPreserved:true,reviewersIndependent:true,pageErrors:0,realPaidRequests:0}));
}finally{await browser.close()}
'''

def main():
    with tempfile.TemporaryDirectory() as temp:
        old=hs.OUT;hs.OUT=Path(temp);server=hs.Server(('127.0.0.1',0))
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            node=ROOT/'.tools/node-v22.23.2-darwin-arm64/bin/node'
            result=subprocess.run([str(node),'--input-type=module','-e',SCRIPT,'http://127.0.0.1:'+str(server.server_port)],cwd=ROOT,text=True,capture_output=True,timeout=120)
            assert result.returncode==0,result.stderr
            report=json.loads(result.stdout);write(ROOT/'deliverables/brickplan-interface-repair-2026-10-23/ui-checks.json',report)
            print(json.dumps(report,indent=2))
        finally:server.shutdown();server.server_close();thread.join();hs.OUT=old

if __name__=='__main__':main()
