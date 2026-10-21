import { readFileSync, writeFileSync } from 'node:fs';
process.loadEnvFile('.env');
const out='deliverables/brickplan-static-audit-2026-10-14';
const snapshot={at:new Date().toISOString(),endpoint:'https://openrouter.ai/api/v1/key',attribution:'Account may contain other concurrent callers. This snapshot is not the experimental bill.'};
try {
 const r=await fetch(snapshot.endpoint,{headers:{Authorization:`Bearer ${process.env.OPENROUTER_API_KEY}`},signal:AbortSignal.timeout(20000)});
 snapshot.httpStatus=r.status;
 if(r.ok){const {data}=await r.json();for(const k of ['usage','usage_daily','usage_weekly','usage_monthly'])if(typeof data[k]==='number')snapshot[k]=data[k];}
}catch{snapshot.error='Account snapshot request failed; no model inference requested.';}
writeFileSync(`${out}/account-after.json`,JSON.stringify(snapshot,null,2)+'\n');
console.log('Non-billable account metadata snapshot saved.');
