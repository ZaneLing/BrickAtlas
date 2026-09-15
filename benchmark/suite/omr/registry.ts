import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

export const OMR_CASE_VERSION = 'brickatlas-omr-cases-1';

interface ManifestInstance {
  instanceId: string;
  partNumber: string;
  colorCode: string;
  parentSubmodelId: string;
  bounds: { min: [number, number, number]; max: [number, number, number] };
}

interface ManifestSubmodel {
  id: string;
  name: string;
  parentId: string | null;
  sourceFile: string;
}

interface Manifest {
  model: {
    id: string; title: string; author: string; sourceUrl: string;
    license: string; year: number; notes: string[];
  };
  stats: { instances: number; uniqueParts: number; colors: number; triangles: number; compressedBytes: number };
  instances: ManifestInstance[];
  submodels: ManifestSubmodel[];
  instructions: { provenance: 'source' | 'editorial'; steps: unknown[] };
}

const MODEL_LABELS: Record<string, { setNumber: string; titleZh: string; category: string }> = {
  '5867': { setNumber: '5867', titleZh: '超级跑车', category: '车辆' },
  '31027': { setNumber: '31027', titleZh: '蓝色赛车', category: '车辆' },
  '31027-kart': { setNumber: '31027', titleZh: '卡丁车', category: '车辆' },
  '31028': { setNumber: '31028', titleZh: '水上飞机', category: '飞行器' },
  '31028-sailboat': { setNumber: '31028', titleZh: '帆船', category: '船舶' },
  '31009': { setNumber: '31009', titleZh: '田园小屋', category: '建筑' },
  '10014': { setNumber: '10014', titleZh: '铁路守车', category: '铁路' },
  '10156': { setNumber: '10156', titleZh: '品牌运输卡车', category: '车辆' },
  '10001': { setNumber: '10001', titleZh: '城际特快列车', category: '铁路' },
  '10128': { setNumber: '10128', titleZh: '铁路道口', category: '铁路' },
  '10036': { setNumber: '10036', titleZh: '披萨餐厅', category: '建筑' },
  '10159': { setNumber: '10159', titleZh: '城市机场', category: '场景' },
  '10220': { setNumber: '10220', titleZh: '大众 T1 露营车', category: '车辆' },
  '10214': { setNumber: '10214', titleZh: '伦敦塔桥', category: '地标建筑' },
  '10213': { setNumber: '10213', titleZh: '航天飞机探险', category: '航天' },
};

interface SemanticSelection { submodelId: string; slug: string; titleZh: string; role: string }
const SEMANTIC_SELECTIONS: Record<string, SemanticSelection[]> = {
  '5867': [
    { submodelId: 's-bc74613b28f381fa', slug: 'front-grille', titleZh: '前格栅', role: 'vehicle-component' },
    { submodelId: 's-e8e14cb4a41bf78b', slug: 'rear-bumper', titleZh: '后保险杠', role: 'vehicle-component' },
    { submodelId: 's-45a121e7c176504f', slug: 'rear-window', titleZh: '后窗总成', role: 'vehicle-component' },
    { submodelId: 's-d4edd726bb251fe9', slug: 'left-door', titleZh: '左车门', role: 'vehicle-component' },
    { submodelId: 's-b3e25cc333f0eb2f', slug: 'front-hood', titleZh: '前引擎盖', role: 'vehicle-component' },
  ],
  '10001': [
    { submodelId: 's-31d4c500cdbcc303', slug: 'platform', titleZh: '站台', role: 'infrastructure' },
    { submodelId: 's-a375cf004b059d5e', slug: 'train-3', titleZh: '第三节列车', role: 'rail-car' },
    { submodelId: 's-4377bce057f59232', slug: 'train-2', titleZh: '第二节列车', role: 'rail-car' },
    { submodelId: 's-3bfeac8f3f2cd922', slug: 'train-1', titleZh: '第一节列车', role: 'rail-car' },
  ],
  '10036': [
    { submodelId: 's-899287cb1cc01716', slug: 'pizzeria', titleZh: '披萨店建筑', role: 'building' },
    { submodelId: 's-62d147d98f95b0af', slug: 'delivery-car', titleZh: '配送汽车', role: 'vehicle' },
  ],
  '10128': [
    { submodelId: 's-4c9787cc2b8faffd', slug: 'level-crossing', titleZh: '铁路道口主体', role: 'infrastructure' },
    { submodelId: 's-1305f3d9fd668a84', slug: 'barrier', titleZh: '道口栏杆', role: 'moving-component' },
    { submodelId: 's-2df14f4efa56e9fc', slug: 'road-car', titleZh: '道路汽车', role: 'vehicle' },
  ],
  '10156': [
    { submodelId: 's-d92f741c926e170f', slug: 'truck', titleZh: '运输卡车主体', role: 'vehicle' },
  ],
  '10159': [
    { submodelId: 's-2e4a9d96f5d41867', slug: 'runway', titleZh: '机场跑道', role: 'infrastructure' },
    { submodelId: 's-668820f3087f9c75', slug: 'terminal-building', titleZh: '航站楼', role: 'building' },
    { submodelId: 's-203219218a121d01', slug: 'airplane', titleZh: '客机', role: 'aircraft' },
    { submodelId: 's-90802c90d6f053ed', slug: 'helicopter', titleZh: '直升机', role: 'aircraft' },
    { submodelId: 's-ee47f3690a084bdf', slug: 'baggage-car', titleZh: '行李牵引车', role: 'service-vehicle' },
    { submodelId: 's-38dc3174ea2dd443', slug: 'baggage-trailer', titleZh: '行李拖车', role: 'service-vehicle' },
    { submodelId: 's-bac674169251c68c', slug: 'radar', titleZh: '机场雷达', role: 'infrastructure' },
  ],
  '10213': [
    { submodelId: 's-89a7d36ac780fa20', slug: 'launch-platform', titleZh: '发射平台', role: 'infrastructure' },
    { submodelId: 's-bea32b30c654d049', slug: 'space-shuttle', titleZh: '航天飞机', role: 'spacecraft' },
    { submodelId: 's-760bc312254d23a2', slug: 'service-car', titleZh: '地勤车辆', role: 'service-vehicle' },
  ],
  '10214': [
    { submodelId: 's-7516ef847430f894', slug: 'center-road', titleZh: '中央开合桥面', role: 'bridge-deck' },
    { submodelId: 's-a5a321fe6a3ed1c0', slug: 'tower', titleZh: '桥塔', role: 'tower' },
    { submodelId: 's-0169fcbb2f586148', slug: 'top-beam', titleZh: '顶部横梁', role: 'bridge-structure' },
    { submodelId: 's-ae86430339f13683', slug: 'tower-roof', titleZh: '桥塔屋顶', role: 'roof' },
    { submodelId: 's-02acf2a32f4174a1', slug: 'side-road', titleZh: '侧引桥', role: 'bridge-deck' },
    { submodelId: 's-65facd9d51d0e096', slug: 'cables', titleZh: '悬索总成', role: 'cable-system' },
    { submodelId: 's-b20981205ebca3c6', slug: 'double-decker-bus', titleZh: '双层巴士', role: 'vehicle' },
    { submodelId: 's-64fb16f396905e9e', slug: 'taxi', titleZh: '出租车', role: 'vehicle' },
    { submodelId: 's-92dd1bc76b17f749', slug: 'lorry', titleZh: '货车', role: 'vehicle' },
    { submodelId: 's-ff342028b175e28e', slug: 'coupe', titleZh: '轿跑车', role: 'vehicle' },
  ],
  '31009': [
    { submodelId: 's-5b1f42303e31b316', slug: 'roof', titleZh: '小屋屋顶', role: 'roof' },
  ],
  '31027': [
    { submodelId: 's-56f71c81d8b7810d', slug: 'rear', titleZh: '赛车尾部总成', role: 'vehicle-component' },
  ],
  '31028': [
    { submodelId: 's-2e8412350e41ed60', slug: 'underside', titleZh: '水上飞机浮筒底部', role: 'aircraft-component' },
  ],
  '31028-sailboat': [
    { submodelId: 's-85a3e0f3224a4259', slug: 'sail', titleZh: '帆装总成', role: 'marine-component' },
  ],
};

function bounds(instances: ManifestInstance[]) {
  return {
    min: [0, 1, 2].map(axis => Math.min(...instances.map(p => p.bounds.min[axis]))),
    max: [0, 1, 2].map(axis => Math.max(...instances.map(p => p.bounds.max[axis]))),
  };
}

function descendants(manifest: Manifest, id: string) {
  const result = new Set([id]), queue = [id];
  while (queue.length) {
    const parent = queue.shift()!;
    for (const child of manifest.submodels.filter(s => s.parentId === parent)) {
      if (!result.has(child.id)) { result.add(child.id); queue.push(child.id); }
    }
  }
  return result;
}

function stats(instances: ManifestInstance[]) {
  return {
    instances: instances.length,
    uniqueParts: new Set(instances.map(p => p.partNumber)).size,
    colors: new Set(instances.map(p => p.colorCode)).size,
    bounds: bounds(instances),
  };
}

const here = dirname(fileURLToPath(import.meta.url));
export function omrCaseRegistry(repositoryRoot = resolve(here, '../../..')) {
  const whole: any[] = [], semantic: any[] = [];
  const allInstances: ManifestInstance[] = [];
  for (const [modelId, label] of Object.entries(MODEL_LABELS)) {
    const manifest = JSON.parse(readFileSync(resolve(repositoryRoot, `public/models/${modelId}/manifest.json`), 'utf8')) as Manifest;
    assert.equal(manifest.model.id, modelId);
    assert.equal(manifest.model.license, 'CC BY 2.0');
    assert.equal(manifest.instances.length, manifest.stats.instances);
    const common = {
      sourceGroup: modelId,
      sourceFamily: label.setNumber,
      sourceModelId: modelId,
      setNumber: label.setNumber,
      title: manifest.model.title,
      titleZh: label.titleZh,
      category: label.category,
      author: manifest.model.author,
      sourceUrl: manifest.model.sourceUrl,
      license: manifest.model.license,
      year: manifest.model.year,
      instructionProvenance: manifest.instructions.provenance,
      instructionSteps: manifest.instructions.steps.length,
    };
    whole.push({
      id: `omr-${modelId}-whole`, scope: 'whole-model', ...common,
      preview: `public/models/${modelId}/preview.png`,
      ...stats(manifest.instances),
    });
    allInstances.push(...manifest.instances);
    const selectedFiles = new Set<string>();
    for (const selection of SEMANTIC_SELECTIONS[modelId] ?? []) {
      const submodel = manifest.submodels.find(s => s.id === selection.submodelId);
      assert.ok(submodel, `${modelId}/${selection.submodelId}`);
      assert.ok(!/step\d+|minifig|lamp|cone/i.test(submodel.name), `${modelId}/${submodel.name}`);
      assert.ok(!selectedFiles.has(submodel.sourceFile), `${modelId}/${submodel.sourceFile}`);
      selectedFiles.add(submodel.sourceFile);
      const ids = descendants(manifest, submodel.id);
      const instances = manifest.instances.filter(p => ids.has(p.parentSubmodelId));
      assert.ok(instances.length >= 6, `${modelId}/${submodel.name}`);
      semantic.push({
        id: `omr-${modelId}-${selection.slug}`, scope: 'semantic-subassembly', ...common,
        title: submodel.name, titleZh: selection.titleZh, role: selection.role,
        submodelId: submodel.id, sourceFile: submodel.sourceFile,
        ...stats(instances),
      });
    }
  }
  assert.equal(whole.length, 15);
  assert.equal(semantic.length, 39);
  return {
    version: OMR_CASE_VERSION,
    status: 'primary-object-source',
    policy: {
      wholeModels: 'All 15 licensed OMR files already used by the BrickAtlas web application.',
      semanticSubassemblies: 'Source-named descendant closures only; no random growth, step fragments, minifig-only cases, lamps, or cones.',
      statisticalUnit: 'Group by 13 setNumber families; 54 cases are not 54 independent objects.',
      proceduralV2: 'Retired from primary data; retained only as historical mechanism regression.',
    },
    summary: {
      wholeModels: whole.length,
      semanticSubassemblies: semantic.length,
      totalCases: whole.length + semantic.length,
      sourceModelFiles: whole.length,
      sourceFamilies: new Set(whole.map(c => c.sourceFamily)).size,
      placedInstances: allInstances.length,
      uniqueParts: new Set(allInstances.map(p => p.partNumber)).size,
      colors: new Set(allInstances.map(p => p.colorCode)).size,
      instructionSteps: whole.reduce((sum, c) => sum + c.instructionSteps, 0),
      sourceInstructionModels: whole.filter(c => c.instructionProvenance === 'source').length,
      editorialInstructionModels: whole.filter(c => c.instructionProvenance === 'editorial').length,
      minWholeParts: Math.min(...whole.map(c => c.instances)),
      maxWholeParts: Math.max(...whole.map(c => c.instances)),
    },
    wholeModels: whole,
    semanticSubassemblies: semantic,
  };
}
