import * as THREE from '/vendor/three.module.min.js';

// Only the ended-practice endpoint provides these triangles and poses.
export function makeViewer(container,data){
  const scene=new THREE.Scene();scene.background=new THREE.Color('#edf1ed');
  const renderer=new THREE.WebGLRenderer({antialias:true});
  renderer.setPixelRatio(Math.min(devicePixelRatio,2));container.replaceChildren(renderer.domElement);
  const labels=document.createElement('div');labels.className='labels';container.append(labels);
  scene.add(new THREE.HemisphereLight(0xffffff,0x9aa293,2.8));
  const light=new THREE.DirectionalLight(0xffffff,2.4);light.position.set(150,400,250);scene.add(light);
  const base=new THREE.Group();scene.add(base);
  const palette={'0':'#202326','1':'#0055bf','4':'#c91a09','7':'#9ba19d','14':'#f2cd37','15':'#ffffff','71':'#a0a5a9','72':'#6c6e68'};
  const pieces=[],allBounds=new THREE.Box3(),geometries=[],materials=[];
  for(let local=0;local<data.parts.length;local++){
    const part=data.parts[local],group=new THREE.Group();
    const source=new THREE.Matrix4().set(...part.rawMatrix.flat());
    const matrix=new THREE.Matrix4().makeScale(1,-1,-1).multiply(source);
    for(const [color,vertices] of Object.entries(data.meshes[part.partNumber])){
      const geometry=new THREE.BufferGeometry();
      geometry.setAttribute('position',new THREE.Float32BufferAttribute(vertices,3));
      geometry.applyMatrix4(matrix);geometry.computeVertexNormals();geometries.push(geometry);
      const material=new THREE.MeshStandardMaterial({color:color==='16'?part.colorHex:(palette[color]||part.colorHex),
        roughness:.36,metalness:.03,side:THREE.DoubleSide});materials.push(material);
      group.add(new THREE.Mesh(geometry,material));
    }
    const bounds=new THREE.Box3().setFromObject(group);allBounds.union(bounds);
    const center=bounds.getCenter(new THREE.Vector3()),site=data.mutable.indexOf(local);
    let label=null;
    if(site>=0){label=document.createElement('span');label.className='part-label';
      label.textContent=`${data.partIds[site]} / ${data.siteIds[site]}`;labels.append(label);}
    pieces.push({group,center,site,label});base.add(group);
  }
  const center=allBounds.getCenter(new THREE.Vector3()),size=allBounds.getSize(new THREE.Vector3());
  const radius=size.length()*.65;
  const camera=new THREE.OrthographicCamera(-radius,radius,radius,-radius,1,radius*20);
  let azimuth=.72,elevation=.58,zoom=1,amount=0,currentFrame=0;
  function render(){
    const width=container.clientWidth,height=container.clientHeight;
    renderer.setSize(width,height,false);
    const half=radius/zoom;camera.left=-half*width/height;camera.right=half*width/height;
    camera.top=half;camera.bottom=-half;
    camera.position.copy(center).add(new THREE.Vector3(
      Math.sin(azimuth)*Math.cos(elevation),Math.sin(elevation),Math.cos(azimuth)*Math.cos(elevation)).multiplyScalar(radius*5));
    camera.lookAt(center);camera.updateProjectionMatrix();camera.updateMatrixWorld();
    renderer.render(scene,camera);
    for(const piece of pieces){
      if(!piece.label)continue;
      const p=piece.center.clone().add(piece.group.position).project(camera);
      piece.label.hidden=!piece.group.visible||Math.abs(p.x)>1||Math.abs(p.y)>1;
      piece.label.style.left=`${(p.x+1)*width/2}px`;piece.label.style.top=`${(1-p.y)*height/2}px`;
    }
  }
  function apply(){
    const mask=data.frames[currentFrame].assembly;
    for(const piece of pieces){
      piece.group.visible=piece.site<0||Boolean(mask&(1<<piece.site));
      piece.group.position.copy(piece.center).sub(center).multiplyScalar(amount*1.3);
    }
    render();
  }
  let pointer=null;
  renderer.domElement.onpointerdown=e=>{pointer={x:e.clientX,y:e.clientY};renderer.domElement.setPointerCapture(e.pointerId);};
  renderer.domElement.onpointermove=e=>{
    if(!pointer)return;azimuth-=(e.clientX-pointer.x)*.008;
    elevation=Math.max(-1.5,Math.min(1.5,elevation+(e.clientY-pointer.y)*.008));
    pointer={x:e.clientX,y:e.clientY};render();
  };
  renderer.domElement.onpointerup=()=>{pointer=null;};
  renderer.domElement.onpointercancel=()=>{pointer=null;};
  renderer.domElement.addEventListener('wheel',e=>{e.preventDefault();
    zoom=Math.max(.35,Math.min(3,zoom*Math.exp(-e.deltaY*.001)));render();},{passive:false});
  const resize=new ResizeObserver(render);resize.observe(container);apply();
  return {frame(n){currentFrame=n;apply();},explode(value){amount=value;apply();},dispose(){
    resize.disconnect();renderer.dispose();geometries.forEach(g=>g.dispose());materials.forEach(m=>m.dispose());container.replaceChildren();
  }};
}
