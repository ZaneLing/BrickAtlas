import { Color, DataTexture, DoubleSide, LineBasicMaterial, MeshPhysicalMaterial, type Material } from 'three';
import { LDrawConditionalLineMaterial } from 'three/addons/materials/LDrawConditionalLineMaterial.js';
import type { GeometryBucket } from '../model/types';

const declarations = `
attribute float instanceIndex;
uniform sampler2D atlasState;
uniform float atlasWidth;
uniform float atlasXray;
varying float atlasVisibility;
varying float atlasSelected;
vec4 readAtlas() { return texture2D(atlasState, vec2((instanceIndex + 0.5) / atlasWidth, 0.25)); }
`;
const selectionDeclaration = `
uniform float atlasXray;
varying float atlasVisibility;
varying float atlasSelected;
`;

export function atlasMaterial(bucket: GeometryBucket, texture: DataTexture, count: number): Material {
  const { color, opacity, roughness, metalness } = bucket.material;
  const shared = { color, opacity, transparent: opacity < 1, depthWrite: opacity >= 1 };
  const atlasUniforms = { xray: { value: 0 } };
  const material = bucket.kind === 'mesh'
    ? new MeshPhysicalMaterial({
      ...shared, roughness: Math.max(0.24, roughness), metalness: Math.min(0.3, metalness),
      clearcoat: opacity < 1 ? 0.08 : 0.24, clearcoatRoughness: 0.32, ior: 1.46, side: DoubleSide,
    })
    : bucket.kind === 'conditional'
      ? new LDrawConditionalLineMaterial(shared)
      : new LineBasicMaterial(shared);
  material.onBeforeCompile = shader => {
    shader.uniforms.atlasState = { value: texture };
    shader.uniforms.atlasWidth = { value: count };
    shader.uniforms.atlasXray = atlasUniforms.xray;
    shader.vertexShader = declarations + shader.vertexShader;
    shader.fragmentShader = selectionDeclaration + shader.fragmentShader;
    shader.vertexShader = shader.vertexShader.replace('void main() {', `void main() {
      vec4 state = readAtlas();
      atlasVisibility = state.w;
      atlasSelected = texture2D(atlasState, vec2((instanceIndex + 0.5) / atlasWidth, 0.75)).x;
    `);
    if (bucket.kind === 'conditional') {
      shader.vertexShader = shader.vertexShader
        .replaceAll('vec4( position, 1.0 )', 'vec4( position + state.xyz, 1.0 )')
        .replace('vec4( position + direction, 1.0 )', 'vec4( position + direction + state.xyz, 1.0 )')
        .replace('vec4( control0, 1.0 )', 'vec4( control0 + state.xyz, 1.0 )')
        .replace('vec4( control1, 1.0 )', 'vec4( control1 + state.xyz, 1.0 )');
    } else {
      shader.vertexShader = shader.vertexShader.replace('#include <begin_vertex>', '#include <begin_vertex>\ntransformed += state.xyz;');
    }
    shader.fragmentShader = shader.fragmentShader.replace('void main() {', `void main() {
      if (atlasVisibility < 0.5) discard;
    `);
    shader.fragmentShader = shader.fragmentShader.replace('#include <color_fragment>', `
      #include <color_fragment>
      diffuseColor.rgb = mix(diffuseColor.rgb, vec3(0.18, 0.52, 0.96), atlasSelected * 0.72);
      diffuseColor.a *= mix(1.0, 0.2, atlasXray * (1.0 - atlasSelected));
    `);
  };
  material.customProgramCacheKey = () => `atlas-v1-${bucket.kind}`;
  material.userData.atlas = { xray: atlasUniforms.xray, opacity };
  if (material instanceof MeshPhysicalMaterial) material.emissive = new Color(0);
  return material;
}

export function setAtlasXray(material: Material, enabled: boolean) {
  const atlas = material.userData.atlas as { xray: { value: number }; opacity: number } | undefined;
  if (!atlas) return;
  atlas.xray.value = enabled ? 1 : 0;
  material.transparent = enabled || atlas.opacity < 1;
  material.depthWrite = !enabled && atlas.opacity >= 1;
  material.needsUpdate = true;
}
