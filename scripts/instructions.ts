import type { AtlasManifest, AssemblyStep, InstructionPlan } from '../src/model/types';
import { header, reference, resolveFile, type LDrawFile } from './ldraw';

export function instructionPlan(files: Map<string, LDrawFile>, root: string, manifest: Pick<AtlasManifest, 'instances' | 'groups'>): InstructionPlan {
  const hasSteps = [...files.values()].some(f => !f.name.endsWith('.dat') && f.lines.some(l => /^0 (STEP|ROTSTEP)( |$)/.test(l.text)));
  const steps: AssemblyStep[] = [];
  const add = (ids: string[], file: string, sourceStep: number | null, title: string) => {
    if (ids.length) steps.push({ id: `step-${steps.length + 1}`, title, sourceFile: file, sourceStep, instanceIds: ids });
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
    // Spatial layers are an inspection aid, not a claim of physical buildability.
    const ordered = [...manifest.instances].sort((a, b) => a.bounds.min[1] - b.bounds.min[1] || a.index - b.index);
    for (let i = 0; i < ordered.length; i += 6) {
      const batch = ordered.slice(i, i + 6);
      const group = manifest.groups.find(g => g.id === batch[0].groupId);
      add(batch.map(p => p.instanceId), batch[0].sourceFile, null, `${group?.name ?? '结构'} · 分层演示`);
    }
  }
  const ids = steps.flatMap(s => s.instanceIds);
  if (ids.length !== manifest.instances.length || new Set(ids).size !== manifest.instances.length) throw new Error('Incomplete instruction coverage');
  return {
    provenance: hasSteps ? 'source' : 'editorial',
    disclaimer: hasSteps
      ? 'OMR 作者步骤，按源层级展开子装配；非官方说明书页码，入位动画不模拟碰撞。'
      : '源模型无 STEP：以下为按高度分层的结构演示，未验证实物可拼搭性；请以官方说明书为准。',
    steps,
  };
}
