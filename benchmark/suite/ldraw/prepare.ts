/** Preserve complete sources; build real LDraw geometry with the existing loader. */
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { modelCatalog, type ModelConfig } from '../../../atlas.config';
import { readZip } from '../../../scripts/readZip';
import { splitMpd, normalize, reference, buildManifest } from '../../../scripts/ldraw';

const root = resolve(import.meta.dirname, '../../..'), out = resolve(root, 'benchmark/ldraw-v1');
mkdirSync(resolve(out, 'configs'), { recursive: true });
mkdirSync(resolve(out, 'flat'), { recursive: true });
const acquired = JSON.parse(readFileSync(resolve(out, 'acquired.json'), 'utf8'));
const names: Record<string, [string, string]> = {
  '42004': ['Mini Backhoe Loader', '小型两头挖掘机'], '42020': ['Twin-Rotor Helicopter', '双旋翼直升机'],
  '42042': ['Crawler Crane', '履带起重机'], '42043': ['Mercedes-Benz Arocs 3245', '奔驰工程卡车'],
  '42054': ['CLAAS XERION 5000 TRAC VC', 'CLAAS 农用拖拉机'], '42055': ['Bucket Wheel Excavator', '斗轮挖掘机'],
  '42061': ['Telehandler', '伸缩臂叉装车'], '42064': ['Ocean Explorer', '海洋科考船'],
  '42065': ['RC Tracked Racer', '遥控履带赛车'], '42066': ['Air Race Jet', '竞速喷气机'],
  '42074': ['Racing Yacht', '竞速帆船'], '42075': ['First Responder', '应急救援车'],
  '42078': ['Mack Anthem', '麦克半挂卡车'], '42081': ['Volvo Concept Wheel Loader ZEUX', '沃尔沃概念装载机'],
  '42082': ['Rough Terrain Crane', '全地形起重机'], '42102': ['Mini CLAAS XERION', '迷你农用拖拉机'],
  '42105': ['Catamaran', '双体帆船'], '42110': ['Land Rover Defender', '路虎卫士'],
  '9391': ['Crawler Crane', '小型履带吊'], '9396': ['Helicopter', '救援直升机'],
  '8110': ['Mercedes-Benz Unimog U 400', '乌尼莫克工程车'],
  '31031': ['Rainforest Animals', '雨林动物'], '31088': ['Deep Sea Creatures', '深海生物'],
  '31109': ['Pirate Ship', '海盗船'], '31112': ['Wild Lion', '雄狮'],
  '31120': ['Medieval Castle', '中世纪城堡'], '31121': ['Crocodile', '鳄鱼'],
  '21303': ['WALL-E', '瓦力机器人'], '21309': ['NASA Apollo Saturn V', '土星五号运载火箭'],
  '21318': ['Tree House', '树屋'], '10231': ['Shuttle Expedition', '航天飞机远征'],
  '10242': ['MINI Cooper', '迷你库珀'], '10252': ['Volkswagen Beetle', '大众甲壳虫'],
  '10258': ['London Bus', '伦敦巴士'], '10265': ['Ford Mustang', '福特野马'],
  '10266': ['NASA Apollo 11 Lunar Lander', '阿波罗登月舱'], '10269': ['Harley-Davidson Fat Boy', '哈雷摩托车'],
};
const existing = modelCatalog.filter(m => !['31027-kart', '31028-sailboat', '10214'].includes(m.id));
const extras: ModelConfig[] = acquired.filter((r: any) => names[r.id] && r.author && r.license).map((r: any) => ({
  id: `omr-${r.id}`, setNumber: r.id, title: names[r.id][0], subtitle: names[r.id][1],
  theme: /^(42|93|81)/.test(r.id) ? 'Technic' : 'Creator / Ideas', category: 'LDraw',
  year: 0, sourceFile: `benchmark/ldraw-v1/sources/${r.id}-1.mpd`, sourceUrl: r.url,
  downloadUrl: r.url, sourceHash: r.sha256, author: r.author,
  license: /4\.0/.test(r.license) ? 'CC BY 4.0' : 'CC BY 2.0',
  licenseUrl: `https://creativecommons.org/licenses/by/${/4\.0/.test(r.license) ? '4.0' : '2.0'}/`,
  notes: ['Unmodified OMR source. Source STEP metadata, if present, is not a collision-free insertion trajectory.'],
}));
const entries = new Map((await readZip(readFileSync(resolve(root, 'assets-source/ldraw-library/complete.zip'))))
  .map(e => [normalize(e.entryName.replace(/^ldraw\//, '')), e]));
const all: any[] = [];
for (const config of [...existing, ...extras]) {
  const configPath = resolve(out, 'configs', `${config.id}.json`);
  writeFileSync(configPath, JSON.stringify(config, null, 2) + '\n');
  const manifestPath = resolve(root, 'public/models', config.id, 'manifest.json');
  try {
    if (!existsSync(manifestPath)) {
      // Dependency and size preflight before expensive geometry conversion.
      const files = splitMpd(readFileSync(resolve(root, config.sourceFile), 'utf8'));
      const first = [...files.keys()][0], seen = new Set<string>();
      const collect = async (name: string): Promise<void> => {
        const key = [name, `parts/${name}`, `p/${name}`].find(n => files.has(n) || entries.has(n));
        if (!key) throw new Error(`Missing dependency: ${name}`);
        if (seen.has(key)) return;
        seen.add(key);
        if (!files.has(key)) files.set(key, splitMpd((await entries.get(key)!.getData()).toString('utf8'), key).get(key)!);
        for (const row of files.get(key)!.lines) if (row.text.startsWith('1 ')) await collect(reference(row.text, row.line).file);
      };
      await collect(first);
      const colors = (await entries.get('ldconfig.ldr')!.getData()).toString('utf8');
      const parsed = buildManifest(files, first, colors, () => 'body');
      if (parsed.instances.length > 2400) throw new Error(`Oversize candidate: ${parsed.instances.length} parts`);
      const run = spawnSync(process.execPath, [resolve(root, 'node_modules/tsx/dist/cli.mjs'),
        'scripts/build-assets.ts', config.id, `--config=${configPath}`], {
        cwd: root, encoding: 'utf8', maxBuffer: 10_000_000,
      });
      writeFileSync(resolve(root, 'benchmark/.runtime', `ldraw-build-${config.id}.log`), run.stdout + run.stderr);
      if (run.status !== 0) throw new Error((run.stderr || run.stdout).slice(-700));
    }
    const manifest = JSON.parse(readFileSync(manifestPath, 'utf8'));
    if (manifest.sourceHash !== config.sourceHash) throw new Error('Source hash mismatch');
    const axis = [2.5, -2.5, -2.5];
    const lines = manifest.instances.map((p: any) => {
      const e = p.originalMatrix;
      const vals = [e[12]*axis[0], e[13]*axis[1], e[14]*axis[2],
        e[0]*axis[0], e[4]*axis[0], e[8]*axis[0],
        e[1]*axis[1], e[5]*axis[1], e[9]*axis[1],
        e[2]*axis[2], e[6]*axis[2], e[10]*axis[2]];
      return `1 ${p.colorCode.startsWith('0x') ? parseInt(p.colorCode) : p.colorCode} ${vals.join(' ')} ${p.partNumber}.dat`;
    });
    writeFileSync(resolve(out, 'flat', `${config.id}.ldr`), lines.join('\n') + '\n');
    all.push({ ...config, instances: manifest.instances.length, status: 'prepared',
      manifestSha256: createHash('sha256').update(readFileSync(manifestPath)).digest('hex') });
    console.log(`Prepared ${config.id}: ${manifest.instances.length} parts`);
  } catch (error) {
    all.push({ ...config, status: 'excluded', reason: String(error) });
    console.log(`Excluded ${config.id}: ${String(error).slice(0,250)}`);
  }
  writeFileSync(resolve(out, 'candidates.json'), JSON.stringify(all, null, 2) + '\n');
}
