import { audit } from './audit';
import { exactNearDuplicates } from './near-duplicates';
import { auditV2Connectors } from './connector-audit';
import { prepareStudy } from './protocol';
import { prepareTraining } from './prepare-training';
import { runAPI } from './run-api';
import { runControls } from './control';
import { replayStudy } from './results';
import { statistics } from './statistics';
import { importVLM } from './import-local';
import { replayLocalEvidence } from './local-evidence';
import { writeStudyReport } from './report';
import { strictAudit } from './strict-audit';
import { trainingBundle } from './training-bundle';
import { localStatistics } from './local-statistics';
import { mutationAudit } from './mutation-audit';
import { failureDiagnostics } from './failure-diagnostics';
import { observabilityAudit } from './observability';
import { prepareInterfaceProbes, replayInterfaceProbes } from './interface-probes';
import { freezeCalibration } from './calibration';
import { exportCalibration, verifyCalibrationInputs } from './calibration-export';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { BENCHMARK } from '../storage';
import { SuiteRenderer } from '../render';
import { prepareModelValidation, runModelValidation, replayModelValidation } from './model-validation';
import { validationReport } from './model-validation-report';
import { prepareLadder, runLadder, replayLadder } from './reconstruction-ladder';
import { preparePoseProbes } from './pose-probes';
import { runPoseProbes, replayPoseProbes } from './pose-run';
import { poseReport } from './pose-report';

const [command, ...args] = process.argv.slice(2);
let result: unknown;
if (command === 'audit') result = await audit();
else if (command === 'prepare-pose-probes') {
  const { url } = JSON.parse(readFileSync(resolve(BENCHMARK, '.runtime/suite-server.json'), 'utf8'));
  const renderer = new SuiteRenderer(url);
  try { result = await preparePoseProbes(renderer); } finally { await renderer.close(); }
}
else if (command === 'run-pose-probes') {
  if (!args.includes('--paid')) throw new Error('Explicit --paid required');
  result = await runPoseProbes();
}
else if (command === 'replay-pose-probes') result = replayPoseProbes();
else if (command === 'report-pose-probes') result = poseReport();
else if (command === 'prepare-model-validation') result = prepareModelValidation();
else if (command === 'replay-model-validation') result = replayModelValidation();
else if (command === 'report-model-validation') result = validationReport();
else if (command === 'replay-ladder') result = replayLadder();
else if (command === 'replay-normalized-ladder') result = replayLadder(true);
else if (command === 'prepare-normalized-ladder') {
  const { url } = JSON.parse(readFileSync(resolve(BENCHMARK, '.runtime/suite-server.json'), 'utf8'));
  const renderer = new SuiteRenderer(url);
  try { result = await prepareLadder(renderer, true); } finally { await renderer.close(); }
}
else if (command === 'run-normalized-ladder') {
  if (!args.includes('--paid')) throw new Error('Explicit --paid required');
  result = await runLadder(true);
}
else if (command === 'prepare-ladder') {
  const { url } = JSON.parse(readFileSync(resolve(BENCHMARK, '.runtime/suite-server.json'), 'utf8'));
  const renderer = new SuiteRenderer(url);
  try { result = await prepareLadder(renderer); } finally { await renderer.close(); }
}
else if (command === 'run-ladder') {
  if (!args.includes('--paid')) throw new Error('Explicit --paid required');
  result = await runLadder();
}
else if (command === 'run-model-validation') {
  if (!args.includes('--paid')) throw new Error('Explicit --paid required');
  result = await runModelValidation();
}
else if (command === 'diagnose') result = failureDiagnostics();
else if (command === 'observability') result = observabilityAudit();
else if (command === 'prepare-probes') result = prepareInterfaceProbes();
else if (command === 'replay-probes') result = replayInterfaceProbes();
else if (command === 'freeze-calibration') result = freezeCalibration();
else if (command === 'verify-calibration') result = verifyCalibrationInputs();
else if (command === 'export-calibration') {
  const { url } = JSON.parse(readFileSync(resolve(BENCHMARK, '.runtime/suite-server.json'), 'utf8'));
  const renderer = new SuiteRenderer(url);
  try { result = await exportCalibration(renderer); } finally { await renderer.close(); }
}
else if (command === 'mutation-audit') result = mutationAudit();
else if (command === 'duplicates') result = exactNearDuplicates();
else if (command === 'connectors') result = auditV2Connectors();
else if (command === 'prepare') result = await prepareStudy();
else if (command === 'prepare-training') result = await prepareTraining();
else if (command === 'run' || command === 'controls') {
  if (!args.includes('--paid')) throw new Error('Explicit --paid required; original cumulative cap retained');
  result = command === 'run' ? await runAPI() : await runControls();
} else if (command === 'replay') result = replayStudy();
else if (command === 'statistics') result = statistics();
else if (command === 'import-local') result = importVLM();
else if (command === 'strict-audit') result = await strictAudit();
else if (command === 'export-training') result = trainingBundle('export');
else if (command === 'verify-training') result = trainingBundle('verify');
else if (command === 'restore-training') result = trainingBundle('restore');
else if (command === 'replay-local') result = replayLocalEvidence();
else if (command === 'local-statistics') result = localStatistics();
else if (command === 'report') result = writeStudyReport();
else throw new Error('Commands: diagnose | observability | prepare-probes | replay-probes | freeze-calibration | export-calibration | verify-calibration | audit | strict-audit | duplicates | connectors | prepare | prepare-training | export-training | verify-training | restore-training | run --paid | controls --paid | replay | statistics | import-local | replay-local | local-statistics | report');
console.log(JSON.stringify(result, null, 2));
