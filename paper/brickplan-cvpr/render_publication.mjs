// Publication-only rendering of certified geometry, isolated from model inputs.
import { createServer } from 'node:http';
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { dirname, resolve, extname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';
import { createHash } from 'node:crypto';
const here=dirname(fileURLToPath(import.meta.url)),root=resolve(here,'../..');
const release=process.argv.includes('--release');
const arena=process.argv.includes('--arena');
const capability=process.argv.includes('--capability');
const cache=resolve(here,capability?'build/capability-scenes':arena?'build/arena-scenes':release?'build/release-scenes':'build/publication-scenes'),out=resolve(here,capability?'figures-capability/native':arena?'figures-release/arena-native':release?'figures-release/native':'figures-publication/native');mkdirSync(out,{recursive:true});
const manifest=JSON.parse(readFileSync(resolve(cache,'scenes.json')));
const html=`<!doctype html><html><head><style>html,body{margin:0;background:white}canvas{display:block}</style>
<script type="importmap">{"imports":{"three":"/node_modules/three/build/three.module.js"}}</script></head><body><script type="module">
import * as THREE from 'three';
import {toCreasedNormals} from '/node_modules/three/examples/jsm/utils/BufferGeometryUtils.js';
import {RoomEnvironment} from '/node_modules/three/examples/jsm/environments/RoomEnvironment.js';
const spec=await (await fetch('/scenes.json')).json();
const renderer=new THREE.WebGLRenderer({antialias:true,alpha:false,preserveDrawingBuffer:true,powerPreference:'high-performance'});
renderer.setSize(...spec.size);renderer.setPixelRatio(1);renderer.outputColorSpace=THREE.SRGBColorSpace;
renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.05;
renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.setClearColor(0xffffff);document.body.append(renderer.domElement);
const scene=new THREE.Scene();scene.background=new THREE.Color('white');
scene.environment=new THREE.PMREMGenerator(renderer).fromScene(new RoomEnvironment(),.04).texture;
scene.add(new THREE.HemisphereLight(0xf5f8ff,0xc5c3bc,1.5));
const key=new THREE.DirectionalLight(0xfff8ed,2.0);key.castShadow=true;key.shadow.mapSize.set(4096,4096);key.shadow.bias=-0.00006;key.shadow.normalBias=.014;key.shadow.radius=4;scene.add(key);scene.add(key.target);
const fill=new THREE.DirectionalLight(0xebf3ff,.65);scene.add(fill);const rim=new THREE.DirectionalLight(0xffffff,.7);scene.add(rim);
const objects=new THREE.Group();scene.add(objects);const geometry=new Map();
const material=new THREE.MeshPhysicalMaterial({vertexColors:true,roughness:.28,metalness:0,clearcoat:.2,clearcoatRoughness:.3,envMapIntensity:.65,side:THREE.DoubleSide});
const floor=new THREE.Mesh(new THREE.PlaneGeometry(1,1),new THREE.ShadowMaterial({color:0x80898f,opacity:.13}));floor.rotation.x=-Math.PI/2;floor.receiveShadow=true;scene.add(floor);
const srgb=v=>v<=.04045?v/12.92:Math.pow((v+.055)/1.055,2.4);
async function mesh(id){if(geometry.has(id))return geometry.get(id);const a=spec.assets[id];const buf=await(await fetch('/mesh/'+a.file)).arrayBuffer();const src=new Float32Array(buf);const pos=new Float32Array(a.vertices*3),col=new Float32Array(a.vertices*3);for(let i=0;i<a.vertices;i++){for(let j=0;j<3;j++){pos[i*3+j]=src[i*6+j];col[i*3+j]=srgb(src[i*6+3+j]);}}
let g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.BufferAttribute(pos,3));g.setAttribute('color',new THREE.BufferAttribute(col,3));g=toCreasedNormals(g,Math.PI/5);geometry.set(id,g);return g;}
window.drawScene=async function(name){while(objects.children.length)objects.remove(objects.children[0]);const s=spec.scenes.find(x=>x.name===name);if(!s)throw Error(name);for(const id of s.meshes){const m=new THREE.Mesh(await mesh(id),material);m.castShadow=true;m.receiveShadow=true;objects.add(m);}
const b=spec.groups[s.group],lo=new THREE.Vector3(...b.min),hi=new THREE.Vector3(...b.max),center=lo.clone().add(hi).multiplyScalar(.5),extent=hi.clone().sub(lo),span=Math.max(...extent.toArray(),1);const az=(b.angles?.[0]??35)*Math.PI/180,el=(b.angles?.[1]??25)*Math.PI/180;
const dir=new THREE.Vector3(Math.sin(az)*Math.cos(el),Math.sin(el),Math.cos(az)*Math.cos(el));const right=new THREE.Vector3(Math.cos(az),0,-Math.sin(az)),up=new THREE.Vector3().crossVectors(dir,right);
let minX=Infinity,maxX=-Infinity,minY=Infinity,maxY=-Infinity;for(const x of [lo.x,hi.x])for(const y of [lo.y,hi.y])for(const z of [lo.z,hi.z]){const p=new THREE.Vector3(x,y,z).sub(center),u=p.dot(right),v=p.dot(up);minX=Math.min(minX,u);maxX=Math.max(maxX,u);minY=Math.min(minY,v);maxY=Math.max(maxY,v);}
const aspect=spec.size[0]/spec.size[1],height=Math.max(maxY-minY,(maxX-minX)/aspect)*1.16,width=height*aspect;
const camera=new THREE.OrthographicCamera(-width/2,width/2,height/2,-height/2,.01,span*20);camera.position.copy(center).addScaledVector(dir,span*5);camera.lookAt(center);
floor.position.set(center.x,(b.groundY??lo.y)-.025,center.z);floor.scale.set(span*12,span*12,1);
key.position.copy(center).add(new THREE.Vector3(-span*1.4,span*2.5,span*1.5));key.target.position.copy(center);key.shadow.camera.left=-span*1.2;key.shadow.camera.right=span*1.2;key.shadow.camera.top=span*1.2;key.shadow.camera.bottom=-span*1.2;key.shadow.camera.near=.1;key.shadow.camera.far=span*10;key.shadow.camera.updateProjectionMatrix();
fill.position.copy(center).add(new THREE.Vector3(span*2,span,span));rim.position.copy(center).add(new THREE.Vector3(0,span*1.5,-span*2));
renderer.render(scene,camera);await new Promise(r=>requestAnimationFrame(r));renderer.render(scene,camera);return renderer.domElement.toDataURL('image/png');};window.ready=true;
</script></body></html>`;
const hash=x=>createHash('sha256').update(x).digest('hex');
const policyHash=hash(html);
const server=createServer((req,res)=>{try{const u=new URL(req.url,'http://localhost');if(u.pathname==='/'){res.setHeader('Content-Type','text/html');res.end(html);return;}let p;if(u.pathname==='/scenes.json')p=resolve(cache,'scenes.json');else if(u.pathname.startsWith('/mesh/'))p=resolve(cache,u.pathname.slice(6));else if(u.pathname.startsWith('/node_modules/three/'))p=resolve(root,'.'+u.pathname);else{res.writeHead(404);res.end();return;}if(!p.startsWith(cache)&&!p.startsWith(resolve(root,'node_modules/three')))throw Error('path');res.setHeader('Content-Type',extname(p)==='.js'?'text/javascript':extname(p)==='.json'?'application/json':'application/octet-stream');res.end(readFileSync(p));}catch(e){res.writeHead(500);res.end(String(e));}});
await new Promise(r=>server.listen(0,'127.0.0.1',r));let browser;
try{browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--disable-dev-shm-usage']});const page=await browser.newPage({viewport:{width:3200,height:2400},deviceScaleFactor:1});page.on('pageerror',e=>console.error(e));await page.goto('http://127.0.0.1:'+server.address().port);await page.waitForFunction(()=>window.ready,{timeout:120000});
const adopt=process.argv.includes('--adopt-existing');
const selected=process.argv.slice(2).filter(x=>!x.startsWith('--'));
for(const s of manifest.scenes){if(selected.length&&!selected.includes(s.name))continue;
const file=resolve(out,s.name+'.png'),metaFile=file+'.json';
const sceneKey=hash(JSON.stringify({scene:s,group:manifest.groups[s.group],meshes:s.meshes.map(id=>manifest.assets[id].sha256),policyHash}));
let meta=existsSync(metaFile)?JSON.parse(readFileSync(metaFile)):null;
if(existsSync(file)&&!process.env.BRICKPLAN_FORCE_RENDER){
 const digest=hash(readFileSync(file));
 if(meta?.sceneKey===sceneKey&&meta.sha256===digest){console.log('CACHED',s.name);continue;}
 // One-time migration for scenes rendered by this same studio policy during
 // this revision, before provenance sidecars were introduced.
 if(adopt&&!meta){writeFileSync(metaFile,JSON.stringify({sceneKey,sha256:digest,policyHash,cacheMigration:true}));console.log('ADOPTED',s.name);continue;}}
const data=await page.evaluate(name=>window.drawScene(name),s.name);writeFileSync(file,Buffer.from(data.split(',')[1],'base64'));
writeFileSync(metaFile,JSON.stringify({sceneKey,sha256:hash(readFileSync(file)),policyHash,browserVersion:browser.version(),cacheMigration:false}));
console.log('RENDERED',s.name);}
}finally{if(browser)await browser.close();await new Promise(r=>server.close(r));}
