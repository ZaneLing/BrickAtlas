import * as THREE from 'three';
import type { MechanismPart } from '../../benchmark/suite/mechanism/types';

// size describes the complete body extent on each local axis. Studs are
// separate visible geometry, included in the shared conservative envelope.
export function bodyGeometry(p: MechanismPart): THREE.BufferGeometry {
  const [x, y, z] = p.size;
  let geometry: THREE.BufferGeometry;
  if (p.shape === 'sphere') {
    geometry = new THREE.SphereGeometry(0.5, 24, 16).scale(x, y, z);
  } else if (['gear', 'wheel', 'axle', 'cylinder'].includes(p.shape)) {
    geometry = new THREE.CylinderGeometry(0.5, 0.5, 1, 24).scale(x, y, z);
  } else if (p.shape === 'arch') {
    geometry = new THREE.TorusGeometry(1, 0.25, 12, 24, Math.PI);
    geometry.computeBoundingBox();
    const bounds = geometry.boundingBox!, size = bounds.getSize(new THREE.Vector3());
    const center = bounds.getCenter(new THREE.Vector3());
    geometry.translate(-center.x, -center.y, -center.z).scale(x / size.x, y / size.y, z / size.z);
  } else if (p.shape === 'slope') {
    geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.Float32BufferAttribute([
      -x/2,-y/2,-z/2, x/2,-y/2,-z/2, x/2,-y/2,z/2, -x/2,-y/2,z/2,
      -x/2,y/2,z/2, -x/2,y/2,-z/2,
    ], 3));
    geometry.setIndex([0,1,2,0,2,3,0,4,5,0,3,4,3,2,4,2,1,4,1,5,4,0,5,1]);
    geometry.computeVertexNormals();
  } else geometry = new THREE.BoxGeometry(x, y, z);
  return geometry;
}

export function studs(p: MechanismPart) {
  if (!['brick', 'plate'].includes(p.shape)) return [];
  const [x, y, z] = p.size, nx = Math.max(1, Math.round(x)), nz = Math.max(1, Math.round(z));
  const radius = Math.min(0.19, x / nx / 2, z / nz / 2);
  return Array.from({ length: nx * nz }, (_, n) => ({
    radius, height: 0.1,
    position: [(Math.floor(n / nz) + 0.5) * x / nx - x / 2, y / 2 + 0.05,
      (n % nz + 0.5) * z / nz - z / 2] as [number, number, number],
  }));
}

export function partEnvelope(p: MechanismPart) {
  const extra = ['brick', 'plate'].includes(p.shape) ? 0.1 : 0;
  return {
    center: new THREE.Vector3(0, extra / 2, 0),
    half: new THREE.Vector3(p.size[0] / 2, (p.size[1] + extra) / 2, p.size[2] / 2),
  };
}

export function partMatrix(position: number[], rotation: number[]) {
  return new THREE.Matrix4().compose(new THREE.Vector3(...position),
    new THREE.Quaternion(...rotation), new THREE.Vector3(1, 1, 1));
}
