import type { AtlasManifest, AssemblyStep, InstructionPlan, PartInstance, Vec3 } from '../src/model/types';
import { header, reference, resolveFile, type LDrawFile } from './ldraw';

export function instructionPlan(files: Map<string, LDrawFile>, root: string, manifest: Pick<AtlasManifest, 'instances' | 'groups'>): InstructionPlan {
  const hasSteps = [...files.values()].some(f => !f.name.endsWith('.dat') && f.lines.some(l => /^0 (STEP|ROTSTEP)( |$)/.test(l.text)));
  const steps: AssemblyStep[] = [];
  const add = (ids: string[], file: string, sourceStep: number | null, title: string, extra: Partial<AssemblyStep> = {}) => {
    if (ids.length || extra.kind === 'placement') {
      steps.push({ id: `step-${steps.length + 1}`, title, sourceFile: file, sourceStep, instanceIds: ids, ...extra });
    }
  };
  if (hasSteps) {
    let index = 0;
    const visit = (file: LDrawFile) => {
      let ids: string[] = [], local = 1;
      const stepped = file.lines.some(l => /^0 (STEP|ROTSTEP)( |$)/.test(l.text));
      const flush = () => { add(ids, file.name, stepped ? local : null, header(file, '') || file.name); ids = []; };
      for (const line of file.lines) {
        if (/^0 (STEP|ROTSTEP)( |$)/.test(line.text)) { flush(); local++; continue; }
        if (!line.text.startsWith('1 ')) continue;
        const child = resolveFile(files, reference(line.text, line.line).file);
        if (child.name.endsWith('.ldr') || /(?:^|_)Model\b/.test(header(child, '!LDRAW_ORG'))) {
          flush();
          visit(child);
        } else {
          const part = manifest.instances[index++];
          if (!part || part.sourceFile !== file.name || part.sourceLine !== line.line) throw new Error('Instruction/source traversal mismatch');
          ids.push(part.instanceId);
        }
      }
      flush();
    };
    visit(resolveFile(files, root));
  } else {
    const assemblies = new Map<string, PartInstance[]>();
    for (const part of manifest.instances) {
      const key = part.path[1] ?? root;
      if (!assemblies.has(key)) assemblies.set(key, []);
      assemblies.get(key)!.push(part);
    }
    const cleanName = (name: string) => (header(resolveFile(files, name), '') || name)
      .replace(/\.(ldr|mpd)$/i, '')
      .replace(/^\d+\s*-\s*/, '');
    const foundation = /runway|airport|base|ground|platform|station|building|road|track/i;
    const mobile = /airplane|plane|helicopter|train|car|truck|trailer|vehicle|boat|ship|minifig|figure/i;
    const isScene = [...assemblies.keys()].some(name => foundation.test(cleanName(name)));
    const rank = (name: string) => {
      const label = cleanName(name);
      if (!isScene) return name === root ? 0 : 1;
      if (/airplane|plane/i.test(label)) return 0;
      if (/helicopter/i.test(label)) return 1;
      if (/train|car|truck|trailer|vehicle|boat|ship/i.test(label)) return 2;
      if (/minifig|figure/i.test(label)) return 3;
      if (/runway|base|ground|platform|road|track/i.test(label)) return 5;
      if (/airport|station|building/i.test(label)) return 6;
      return 4;
    };
    const orderedAssemblies = [...assemblies.entries()].sort(([a, aParts], [b, bParts]) =>
      isScene
        ? rank(a) - rank(b) || a.localeCompare(b)
        : bParts.length - aParts.length || a.localeCompare(b),
    );
    const movableAssemblies = orderedAssemblies.filter(([name]) => isScene && mobile.test(cleanName(name)));
    const extentX = Math.max(...manifest.instances.map(part => part.bounds.max[0]))
      - Math.min(...manifest.instances.map(part => part.bounds.min[0]));
    const extentZ = Math.max(...manifest.instances.map(part => part.bounds.max[2]))
      - Math.min(...manifest.instances.map(part => part.bounds.min[2]));
    const distance = Math.min(180, Math.max(70, Math.max(extentX, extentZ) * 0.2));
    const offsets = new Map<string, Vec3>(movableAssemblies.map(([name], index) => {
      const angle = -Math.PI * 0.7 + index / Math.max(1, movableAssemblies.length - 1) * Math.PI * 1.4;
      return [name, [Math.cos(angle) * distance, 28 + index % 2 * 18, Math.sin(angle) * distance] as Vec3];
    }));
    for (const [name, parts] of orderedAssemblies) {
      const groupOrder = ['chassis', 'body', 'cockpit', 'front', 'rear', 'wheels'];
      const sequences = name === root
        ? [...manifest.groups].sort((a, b) => groupOrder.indexOf(a.id) - groupOrder.indexOf(b.id)).map(group => ({
          name: group.name,
          parts: parts.filter(part => part.groupId === group.id),
        })).filter(group => group.parts.length)
        : [{ name: cleanName(name), parts }];
      for (const sequence of sequences) {
        const ordered = [...sequence.parts].sort((a, b) =>
          a.bounds.min[1] - b.bounds.min[1]
          || a.bounds.min[2] - b.bounds.min[2]
          || a.bounds.min[0] - b.bounds.min[0]
          || a.index - b.index,
        );
        for (let index = 0; index < ordered.length; index += 6) {
          const batch = ordered.slice(index, index + 6);
          add(batch.map(part => part.instanceId), batch[0].sourceFile, null, `${sequence.name} · 子装配`, {
            kind: 'parts',
            assemblyId: name,
            stagingOffset: offsets.get(name),
          });
        }
      }
    }
    for (const [name, parts] of movableAssemblies) {
      add([], parts[0].sourceFile, null, `${cleanName(name)} · 放置总成`, {
        kind: 'placement',
        assemblyId: name,
        motionInstanceIds: parts.map(part => part.instanceId),
        stagingOffset: offsets.get(name),
      });
    }
  }
  const ids = steps.flatMap(s => s.instanceIds);
  if (ids.length !== manifest.instances.length || new Set(ids).size !== manifest.instances.length) throw new Error('Incomplete instruction coverage');
  return {
    provenance: hasSteps ? 'source' : 'editorial',
    disclaimer: hasSteps
      ? 'OMR 作者步骤，按源层级展开子装配；非官方说明书页码，入位动画不模拟碰撞。'
      : '源模型无 STEP：以下先构建独立子装配，再构建场景基础并完成总装；这是编辑演示，未验证实物可拼搭性。',
    steps,
  };
}
