# LDraw-2 task contracts

No family currently requires chaining two observation contracts within a single item; the benchmark measures modular competencies separately.

Counts below are computed from all 617 frozen items. Model requests contain only the fixed system prompt, English question, format, necessary input, anonymous options, and image bytes for V. Internal source oracles do not certify human perceptual validity.

Known deterministic shortcuts S1--S4 were repaired (see PHASE-1-REPORT.md). Answer priors and the constant six-step program remain explicit limitations. No claim of universal shortcut absence is made. Instance answers are source-scoped when calculating semantic concentration; equal B-numbers in different sets are not equated.

## Color (color)

- **Count:** 73
- **Observation contract:** visual
- **Layer:** atomic
- **Exact public input:** {}; visualInput.numberedView supplies a frozen operand-isolation PNG; isolationAllowed=true
- **Required operation:** Bind the target B-number in the image; identify its source color name.
- **Scoring:** Exact anonymous choiceId of the semantic answer.
- **Measurement category:** Perception
- **Constant response:** False
- **Known shortcuts / priors:** No known deterministic S1--S4 request shortcut; semantic priors reported separately.
- **Construct validity:** Source color equality is an oracle, not proof of perceptual distinguishability.
- **Legacy paper location:** main.tex:244--246
- **V2 paper location:** main-v2.tex:sec:contracts

## Part type (shape-match)

- **Count:** 67
- **Observation contract:** visual
- **Layer:** atomic
- **Exact public input:** {}; visualInput.numberedView supplies a frozen operand-isolation PNG; isolationAllowed=true
- **Required operation:** Bind target and candidates in the image; match the source part type while ignoring color and pose.
- **Scoring:** Exact anonymous choiceId of the semantic answer.
- **Measurement category:** Perception
- **Constant response:** False
- **Known shortcuts / priors:** No known deterministic S1--S4 request shortcut; semantic priors reported separately.
- **Construct validity:** Near-identical source types require human adjudication; no unseen geometry is inferred.
- **Legacy paper location:** main.tex:244--246,531--532
- **V2 paper location:** main-v2.tex:sec:contracts

## Distance (distance)

- **Count:** 73
- **Observation contract:** source-data
- **Layer:** atomic
- **Exact public input:** centers, coordinateFrame
- **Required operation:** Read supplied bounding-box centers, compute Euclidean distance, select the unique minimum.
- **Scoring:** Exact anonymous choiceId of the semantic answer.
- **Measurement category:** Evidence reading / arithmetic
- **Constant response:** False
- **Known shortcuts / priors:** No known deterministic S1--S4 request shortcut; semantic priors reported separately.
- **Construct validity:** Coordinates are explicit, not visually estimated. Candidates are hash sampled, not nearest spatial neighbors.
- **Legacy paper location:** main.tex:245--247
- **V2 paper location:** main-v2.tex:sec:contracts

## Interface (interface)

- **Count:** 87
- **Observation contract:** connector-graph
- **Layer:** metacognitive
- **Exact public input:** connectorRecord.{family,aConnector,bConnector}; scope
- **Required operation:** Read connectorRecord.family and select the identical label.
- **Scoring:** Exact anonymous choiceId of the semantic answer.
- **Measurement category:** Evidence reading
- **Constant response:** False
- **Known shortcuts / priors:** No known deterministic S1--S4 request shortcut; semantic priors reported separately.
- **Construct validity:** An explicit record-reading control, not contact perception or load-capacity reasoning.
- **Legacy paper location:** main.tex:247--249
- **V2 paper location:** main-v2.tex:sec:contracts

## Neighbors (neighbors)

- **Count:** 73
- **Observation contract:** connector-graph
- **Layer:** metacognitive
- **Exact public input:** edges, graphMeaning
- **Required operation:** Collect candidate labels joined to the target by any supplied undirected edge; deduplicate.
- **Scoring:** Exact set of choiceIds; order ignored; duplicate IDs invalid.
- **Measurement category:** Graph operation
- **Constant response:** False
- **Known shortcuts / priors:** No known deterministic S1--S4 request shortcut; semantic priors reported separately.
- **Construct validity:** One-hop set extraction within the recognized graph, not physical connectivity discovery.
- **Legacy paper location:** main.tex:251--257
- **V2 paper location:** main-v2.tex:sec:contracts

## Graph deletion (graph-removal)

- **Count:** 73
- **Observation contract:** connector-graph
- **Layer:** graph-internal
- **Exact public input:** edges, graphMeaning, nodes
- **Required operation:** Delete the named vertex and incident edges; count connected components including remaining isolated vertices.
- **Scoring:** A safe JSON integer value exactly equal to the independent component count.
- **Measurement category:** Graph operation
- **Constant response:** False
- **Known shortcuts / priors:** No known deterministic S1--S4 request shortcut; semantic priors reported separately.
- **Construct validity:** An operation within a supplied local graph; no extraction trajectory or cross-contract chain.
- **Legacy paper location:** main.tex:252--256
- **V2 paper location:** main-v2.tex:sec:contracts

## Coverage (coverage)

- **Count:** 17
- **Observation contract:** source-data
- **Layer:** metacognitive
- **Exact public input:** coverage[].{label,supported}
- **Required operation:** Select the sole row whose supplied supported flag is false.
- **Scoring:** Exact anonymous choiceId of the semantic answer.
- **Measurement category:** Evidence reading
- **Constant response:** False
- **Known shortcuts / priors:** No known deterministic S1--S4 request shortcut; semantic priors reported separately.
- **Construct validity:** A definition-coverage control; unsupported does not imply floating or disconnected.
- **Legacy paper location:** main.tex:256--257
- **V2 paper location:** main-v2.tex:sec:contracts

## Evidence limit (evidence-limit)

- **Count:** 24
- **Observation contract:** source-data
- **Layer:** metacognitive
- **Exact public input:** available
- **Required operation:** Select Not established by this evidence for the stated gravitational-stability claim.
- **Scoring:** Exact anonymous choiceId of the semantic answer.
- **Measurement category:** Evidence scope control
- **Constant response:** True
- **Known shortcuts / priors:** No known deterministic S1--S4 request shortcut; semantic priors reported separately. Constant semantic answer.
- **Construct validity:** The semantic answer is constant; accuracy alone is not reasoning evidence.
- **Legacy paper location:** main.tex:258--259,388--390
- **V2 paper location:** main-v2.tex:sec:contracts

## Step lookup (source-step)

- **Count:** 55
- **Observation contract:** source-data
- **Layer:** procedural
- **Exact public input:** steps[].{index,numbers}; provenance
- **Required operation:** Find the target label in the supplied author-step table; select the smallest matching expanded index.
- **Scoring:** Exact anonymous choiceId of the semantic answer.
- **Measurement category:** Evidence reading / lookup
- **Constant response:** False
- **Known shortcuts / priors:** No known deterministic S1--S4 request shortcut; semantic priors reported separately.
- **Construct validity:** Table lookup; source order is not evidence of collision-free assembly.
- **Legacy paper location:** main.tex:270--277
- **V2 paper location:** main-v2.tex:sec:contracts

## Step sequence (source-sequence)

- **Count:** 17
- **Observation contract:** scene-edit
- **Layer:** procedural
- **Exact public input:** initialFacts; goalFacts; absentFacts; budget; actions[].{id,label,requires,forbids?,adds,deletes,cost}; editMode
- **Required operation:** Follow the public predecessor facts and reveal the supplied author window in order.
- **Scoring:** String actionIds; legal full replay under prerequisites, forbids and budget; all goal facts and no prohibited facts.
- **Measurement category:** Execution contract
- **Constant response:** True
- **Known shortcuts / priors:** No known deterministic S1--S4 request shortcut; semantic priors reported separately. Identical six-step action program in this release.
- **Construct validity:** A small explicit fact chain, not mechanical planning; the current six-step response template is constant.
- **Legacy paper location:** main.tex:270--274
- **V2 paper location:** main-v2.tex:sec:contracts

## Restoration (restore-instance)

- **Count:** 58
- **Observation contract:** scene-edit
- **Layer:** procedural
- **Exact public input:** initialFacts; goalFacts; absentFacts; budget; actions[].{id,label,requires,forbids?,adds,deletes,cost}; editMode
- **Required operation:** Choose the restore action whose missing fact holds; execute it within budget and satisfy all goals.
- **Scoring:** String actionIds; legal full replay under prerequisites, forbids and budget; all goal facts and no prohibited facts.
- **Measurement category:** Execution contract
- **Constant response:** False
- **Known shortcuts / priors:** No known deterministic S1--S4 request shortcut; semantic priors reported separately.
- **Construct validity:** One visibility edit at an original source pose, not insertion-feasibility planning.
- **Legacy paper location:** main.tex:301--308,529--530
- **V2 paper location:** main-v2.tex:sec:contracts
