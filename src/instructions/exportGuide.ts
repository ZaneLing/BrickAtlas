import type { jsPDF as JsPdfType } from 'jspdf';
import type { ModelConfig } from '../../atlas.config';
import type { AtlasManifest, PartInstance } from '../model/types';
import type { AtlasScene } from '../scene/AtlasScene';

export interface StepPartGroup {
  key: string;
  partNumber: string;
  name: string;
  colorName: string;
  colorHex: string;
  quantity: number;
  instanceIds: string[];
}

export function groupStepParts(parts: PartInstance[]): StepPartGroup[] {
  const groups = new Map<string, StepPartGroup>();
  for (const part of parts) {
    const key = `${part.partNumber}:${part.colorCode}`;
    const item = groups.get(key) ?? {
      key, partNumber: part.partNumber, name: part.displayName, colorName: part.colorName,
      colorHex: part.colorHex, quantity: 0, instanceIds: [],
    };
    item.quantity++;
    item.instanceIds.push(part.instanceId);
    groups.set(key, item);
  }
  return [...groups.values()].sort((a, b) => b.quantity - a.quantity || a.partNumber.localeCompare(b.partNumber));
}

function blobDataUrl(blob: Blob) {
  return new Promise<string>((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result));
    reader.onerror = () => reject(reader.error);
    reader.readAsDataURL(blob);
  });
}

function hexRgb(hex: string): [number, number, number] {
  const normalized = hex.replace('#', '').padEnd(6, '0').slice(0, 6);
  return [0, 2, 4].map(index => Number.parseInt(normalized.slice(index, index + 2), 16)) as [number, number, number];
}

function cover(doc: JsPdfType, config: ModelConfig, manifest: AtlasManifest) {
  doc.setFillColor(232, 240, 235);
  doc.rect(0, 0, 297, 210, 'F');
  doc.setFillColor(38, 92, 66);
  doc.rect(0, 0, 297, 18, 'F');
  doc.setTextColor(255, 255, 255);
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(11);
  doc.text('BRICK ATLAS  /  UNOFFICIAL COMMUNITY BUILD GUIDE', 14, 12);
  doc.setTextColor(31, 48, 39);
  doc.setFontSize(42);
  doc.text(config.title, 18, 68, { maxWidth: 245 });
  doc.setFont('helvetica', 'normal');
  doc.setFontSize(18);
  doc.text(`SET ${config.setNumber}  /  ${config.year}  /  ${config.theme}`, 19, 88);
  doc.setFillColor(255, 255, 255);
  doc.roundedRect(18, 112, 260, 45, 2, 2, 'F');
  doc.setFontSize(11);
  doc.setTextColor(81, 105, 91);
  doc.text(`${manifest.stats.instances} BRICKS`, 31, 132);
  doc.text(`${manifest.stats.uniqueParts} PART TYPES`, 105, 132);
  doc.text(`${manifest.instructions?.steps.length ?? 0} BUILD STEPS`, 195, 132);
  doc.setFontSize(8);
  doc.text(
    manifest.instructions?.provenance === 'source'
      ? 'Step sequence is derived from the LDraw OMR author metadata.'
      : 'The source has no STEP metadata. Sequence is an editorial structural walkthrough.',
    18, 178,
  );
  doc.text('Not affiliated with or endorsed by the LEGO Group. Model and part attribution is retained in the project assets.', 18, 188);
}

function stepPage(
  doc: JsPdfType, config: ModelConfig, manifest: AtlasManifest, stepIndex: number,
  image: string, groups: StepPartGroup[],
) {
  const step = manifest.instructions!.steps[stepIndex];
  doc.addPage('a4', 'landscape');
  doc.setFillColor(234, 244, 248);
  doc.rect(0, 0, 297, 210, 'F');
  doc.setFillColor(255, 255, 255);
  doc.rect(0, 0, 66, 210, 'F');
  doc.setTextColor(22, 34, 29);
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(8);
  doc.text(`BRICK ATLAS  /  ${config.setNumber} ${config.title}`, 12, 12);
  doc.setFontSize(38);
  doc.text(String(stepIndex + 1), 74, 30);
  doc.setFontSize(11);
  doc.text(step.title.replace(/[^\x20-\x7E]/g, ' ').replace(/\s+/g, ' ').trim() || `Build step ${stepIndex + 1}`, 96, 25, { maxWidth: 180 });
  doc.setFont('helvetica', 'normal');
  doc.setTextColor(76, 98, 86);
  doc.setFontSize(7);
  doc.text(`STEP ${stepIndex + 1} OF ${manifest.instructions!.steps.length}`, 96, 31);
  doc.addImage(image, 'JPEG', 75, 38, 211, 151, undefined, 'FAST');

  doc.setTextColor(31, 48, 39);
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(11);
  doc.text(step.kind === 'placement' ? 'PLACE ASSEMBLY' : 'NEW PARTS', 10, 28);
  doc.setFontSize(7);
  doc.setFont('helvetica', 'normal');
  doc.setTextColor(91, 111, 100);
  const itemCount = step.kind === 'placement' ? step.motionInstanceIds?.length ?? 0 : step.instanceIds.length;
  doc.text(
    step.kind === 'placement'
      ? `${itemCount} brick subassembly moves into place`
      : `${itemCount} brick${itemCount === 1 ? '' : 's'} in this step`,
    10, 35,
  );
  let y = 46;
  for (const group of groups) {
    const [r, g, b] = hexRgb(group.colorHex);
    doc.setFillColor(r, g, b);
    doc.roundedRect(10, y, 8, 8, 1, 1, 'F');
    doc.setDrawColor(205, 215, 209);
    doc.roundedRect(10, y, 8, 8, 1, 1, 'S');
    doc.setTextColor(31, 48, 39);
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(8);
    doc.text(`${group.quantity}x  ${group.partNumber}`, 22, y + 3.5);
    doc.setFont('helvetica', 'normal');
    doc.setTextColor(91, 111, 100);
    doc.setFontSize(6.5);
    const label = `${group.name} / ${group.colorName}`.replace(/[^\x20-\x7E]/g, '');
    doc.text(label.slice(0, 44), 22, y + 7.3);
    y += 13.5;
  }
  doc.setDrawColor(46, 126, 90);
  doc.setLineWidth(1.2);
  doc.line(57, 104, 69, 104);
  doc.line(69, 104, 65, 101);
  doc.line(69, 104, 65, 107);
  doc.setFont('helvetica', 'normal');
  doc.setTextColor(70, 91, 79);
  doc.setFontSize(6.5);
  doc.text('New bricks are highlighted green.', 75, 198);
  doc.text(
    manifest.instructions!.provenance === 'source' ? 'OMR AUTHOR STEP' : 'EDITORIAL STRUCTURE STEP',
    285, 198, { align: 'right' },
  );
  doc.text('UNOFFICIAL GUIDE', 285, 204, { align: 'right' });
}

export async function exportBuildGuide(
  scene: AtlasScene,
  config: ModelConfig,
  manifest: AtlasManifest,
  onProgress: (current: number, total: number) => void,
) {
  if (!manifest.instructions?.steps.length) throw new Error('模型没有可导出的步骤');
  const { jsPDF } = await import('jspdf');
  const doc = new jsPDF({ orientation: 'landscape', unit: 'mm', format: 'a4', compress: true });
  cover(doc, config, manifest);
  for (let index = 0; index < manifest.instructions.steps.length; index++) {
    const step = manifest.instructions.steps[index];
    const parts = (step.kind === 'placement' ? [] : step.instanceIds)
      .map(id => manifest.instances.find(part => part.instanceId === id))
      .filter((part): part is PartInstance => !!part);
    const frame = await scene.captureBuildStep(index + 1, 1120, 800);
    stepPage(doc, config, manifest, index, await blobDataUrl(frame), groupStepParts(parts));
    onProgress(index + 1, manifest.instructions.steps.length);
  }
  return doc.output('blob');
}
