import { describe, expect, it } from 'vitest';
import { DataTexture } from 'three';
import { atlasMaterial, setAtlasXray } from '../../src/scene/materials';
import { useViewerStore } from '../../src/store/viewerStore';
import { readLocal, writeLocal } from '../../src/app/storage';

describe('viewer state regressions', () => {
  it('preserves transparent, non-depth-writing outlines through X-Ray toggles', () => {
    const texture = new DataTexture();
    const material = atlasMaterial({
      kind: 'line', material: { color: '#111111', opacity: 1, roughness: 0.3, metalness: 0 },
      attributes: {},
    }, texture, 1);
    setAtlasXray(material, false);
    expect(material.transparent).toBe(true);
    expect(material.depthWrite).toBe(false);
    setAtlasXray(material, true);
    setAtlasXray(material, false);
    expect(material.transparent).toBe(true);
    material.dispose(); texture.dispose();
  });

  it('reset actually clears persisted build progress', () => {
    useViewerStore.getState().loadModel('audit', 'build', 10);
    useViewerStore.getState().patch({ buildStep: 5 });
    useViewerStore.getState().reset('build');
    expect(useViewerStore.getState().buildProgress.audit).toBe(0);
    useViewerStore.getState().loadModel('audit', 'build', 10);
    expect(useViewerStore.getState().currentBuildStep).toBe(0);
  });

  it('missing browser storage does not crash the application', () => {
    expect(readLocal('audit')).toBeNull();
    expect(writeLocal('audit', 'value')).toBe(false);
  });
});
