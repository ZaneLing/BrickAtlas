# BrickAtlas Hierarchy-1 问答库

> 90 道核心题全部由 18 个原创对象派生；OMR/LDraw 不进入模型、题目或分数。

## D1 部件级

### 检修信号转臂 / Signal Switch Stand

#### atomic · vertical-anchor-operation

- 题目：Which named module is highlighted?
- 形式：single-choice
- 能力：part and module recognition、visual grounding
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"A"}`
- 图片：[h1-signal-switch-stand-atomic-anchor](images/tasks/signal-switch-stand-atomic-anchor.png)

#### atomic · atomic-operation-coverage

- 题目：Which named module is highlighted?
- 形式：single-choice
- 能力：part and module recognition、visual grounding
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"B"}`
- 图片：[h1-signal-switch-stand-atomic-coverage](images/tasks/signal-switch-stand-atomic-coverage.png)

#### metacognitive · prefix-stability

- 题目：Which candidate preserves a supported dependency prefix after every placement?
- 形式：single-choice
- 能力：prefix stability、causal support、calibrated physical reasoning
- Oracle 方法：joint dependency graph enumeration
- 答案：`{"choiceId":"A"}`
- 图片：[h1-signal-switch-stand-meta](images/tasks/signal-switch-stand-meta.png)

#### procedural · assembly-sequencing

- 题目：Return a complete placement sequence that satisfies every declared dependency in the requested build prefix.
- 形式：ordered-actions
- 能力：assembly planning、ordering、prefix validity
- Oracle 方法：state-transition and dependency contract
- 答案：`{"actionIds":["place:base","place:post","place:signal-arm","place:lamp"]}`
- 图片：[h1-signal-switch-stand-procedural](images/tasks/signal-switch-stand-procedural.png)

#### integrative · diagnose-access-repair

- 题目：Select the only plan satisfying every hard safety, information, resource, access, and verification constraint.
- 形式：structured-plan
- 能力：cross-capability integration、resource-aware planning、risk control、verification
- Oracle 方法：complete hard-constraint plan filtering
- 答案：`{"planId":"P1","verificationId":"load-and-function-proof"}`
- 图片：[h1-signal-switch-stand-integrative](images/tasks/signal-switch-stand-integrative.png)

### 维修工具小车 / Maintenance Trolley

#### atomic · vertical-anchor-operation

- 题目：Which candidate module has the highest geometric centroid?
- 形式：single-choice
- 能力：3D spatial relation、multi-view correspondence
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"B"}`
- 图片：[h1-maintenance-trolley-atomic-anchor](images/tasks/maintenance-trolley-atomic-anchor.png)

#### atomic · atomic-operation-coverage

- 题目：How many visible pieces belong to the highlighted rigid subassembly?
- 形式：single-choice
- 能力：counting、instance grouping
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"C"}`
- 图片：[h1-maintenance-trolley-atomic-coverage](images/tasks/maintenance-trolley-atomic-coverage.png)

#### metacognitive · assembly-accessibility

- 题目：Select every service path whose minimum swept-volume clearance is strictly positive.
- 形式：multiple-choice
- 能力：assembly accessibility、continuous collision reasoning、set-valued decisions
- Oracle 方法：swept-volume clearance threshold
- 答案：`{"choiceIds":["A","D"]}`
- 图片：[h1-maintenance-trolley-meta](images/tasks/maintenance-trolley-meta.png)

#### procedural · safe-disassembly

- 题目：Return a complete safe removal sequence; independent modules may be ordered either way.
- 形式：ordered-actions
- 能力：disassembly planning、dependency reversal、safe removal
- Oracle 方法：state-transition and dependency contract
- 答案：`{"actionIds":["remove:handle","remove:tool-tray","remove:rear-axle","remove:front-axle"]}`
- 图片：[h1-maintenance-trolley-procedural](images/tasks/maintenance-trolley-procedural.png)

#### integrative · inventory-robustness

- 题目：Select the only plan satisfying every hard safety, information, resource, access, and verification constraint.
- 形式：structured-plan
- 能力：cross-capability integration、resource-aware planning、risk control、verification
- Oracle 方法：complete hard-constraint plan filtering
- 答案：`{"planId":"P2","verificationId":"load-and-function-proof"}`
- 图片：[h1-maintenance-trolley-integrative](images/tasks/maintenance-trolley-integrative.png)

### 铰接安全舱盖 / Hinged Safety Hatch

#### atomic · vertical-anchor-operation

- 题目：Which edit performs the requested local recolor without collateral changes?
- 形式：single-choice
- 能力：instruction editing、recolor、change isolation
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"C"}`
- 图片：[h1-hinged-safety-hatch-atomic-anchor](images/tasks/hinged-safety-hatch-atomic-anchor.png)

#### atomic · atomic-operation-coverage

- 题目：What is the dominant color of the highlighted subassembly?
- 形式：single-choice
- 能力：color recognition、attribute grounding
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"D"}`
- 图片：[h1-hinged-safety-hatch-atomic-coverage](images/tasks/hinged-safety-hatch-atomic-coverage.png)

#### metacognitive · support-counterfactual

- 题目：If the declared support interface is removed, which listed modules lose their certified support path?
- 形式：multiple-choice
- 能力：counterfactual support、dependency closure、set-valued prediction
- Oracle 方法：directed support-graph transitive closure
- 答案：`{"choiceIds":["C","D"]}`
- 图片：[h1-hinged-safety-hatch-meta](images/tasks/hinged-safety-hatch-meta.png)

#### procedural · edit-then-verify

- 题目：Return the minimum ordered actions for a local recolor followed by state verification.
- 形式：ordered-actions
- 能力：instruction execution、local editing、postcondition verification
- Oracle 方法：state-transition and dependency contract
- 答案：`{"actionIds":["isolate:latch","recolor:latch:safety-orange","restore:latch","verify:no-collateral-change"]}`
- 图片：[h1-hinged-safety-hatch-procedural](images/tasks/hinged-safety-hatch-procedural.png)

#### integrative · inspect-plan-execute

- 题目：Select the only plan satisfying every hard safety, information, resource, access, and verification constraint.
- 形式：structured-plan
- 能力：cross-capability integration、resource-aware planning、risk control、verification
- Oracle 方法：complete hard-constraint plan filtering
- 答案：`{"planId":"P3","verificationId":"load-and-function-proof"}`
- 图片：[h1-hinged-safety-hatch-integrative](images/tasks/hinged-safety-hatch-integrative.png)

### 阀门控制台 / Valve Control Stand

#### atomic · vertical-anchor-operation

- 题目：Which joint best explains the affected child and lost constraint?
- 形式：single-choice
- 能力：fault localization、causal diagnosis
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"D"}`
- 图片：[h1-valve-control-stand-atomic-anchor](images/tasks/valve-control-stand-atomic-anchor.png)

#### atomic · atomic-operation-coverage

- 题目：Which candidate module has the highest geometric centroid?
- 形式：single-choice
- 能力：3D spatial relation、multi-view correspondence
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"A"}`
- 图片：[h1-valve-control-stand-atomic-coverage](images/tasks/valve-control-stand-atomic-coverage.png)

#### metacognitive · dynamic-robustness

- 题目：What is the largest tested impulse satisfying both transient and residual motion limits?
- 形式：single-choice
- 能力：dynamic robustness、threshold estimation、multi-criterion checking
- Oracle 方法：two-threshold response-table evaluation
- 答案：`{"choiceId":"D"}`
- 图片：[h1-valve-control-stand-meta](images/tasks/valve-control-stand-meta.png)

#### procedural · fault-recovery

- 题目：Return the minimum certified recovery sequence for the declared failed joint.
- 形式：ordered-actions
- 能力：fault recovery、minimal repair、action sequencing
- Oracle 方法：state-transition and dependency contract
- 答案：`{"actionIds":["isolate-load","access-indicator","replace-indicator-coupler","reindex-mechanism"]}`
- 图片：[h1-valve-control-stand-procedural](images/tasks/valve-control-stand-procedural.png)

#### integrative · multiobjective-maintenance

- 题目：Select the only plan satisfying every hard safety, information, resource, access, and verification constraint.
- 形式：structured-plan
- 能力：cross-capability integration、resource-aware planning、risk control、verification
- Oracle 方法：complete hard-constraint plan filtering
- 答案：`{"planId":"P4","verificationId":"load-and-function-proof"}`
- 图片：[h1-valve-control-stand-integrative](images/tasks/valve-control-stand-integrative.png)

## D2 装配体级

### 仓储分流机 / Warehouse Sorter

#### atomic · vertical-anchor-operation

- 题目：Which named module is highlighted?
- 形式：single-choice
- 能力：part and module recognition、visual grounding
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"A"}`
- 图片：[h1-warehouse-sorter-atomic-anchor](images/tasks/warehouse-sorter-atomic-anchor.png)

#### atomic · atomic-operation-coverage

- 题目：Which motion primitive is assigned to the designated joint?
- 形式：single-choice
- 能力：joint recognition、kinematic semantics
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"B"}`
- 图片：[h1-warehouse-sorter-atomic-coverage](images/tasks/warehouse-sorter-atomic-coverage.png)

#### metacognitive · functional-kinematics

- 题目：Which motion statement is consistent with the designated functional joint?
- 形式：single-choice
- 能力：functional kinematics、joint semantics、axis and limit reasoning
- Oracle 方法：declared joint contract
- 答案：`{"choiceId":"A"}`
- 图片：[h1-warehouse-sorter-meta](images/tasks/warehouse-sorter-meta.png)

#### procedural · inventory-replan

- 题目：Return the ordered stockout-recovery actions using the only feasible replacement.
- 形式：ordered-actions
- 能力：inventory replanning、structural substitution、constraint-preserving execution
- Oracle 方法：state-transition and dependency contract
- 答案：`{"actionIds":["inspect:stock","select:long-beam","isolate:belt","install:long-beam","verify:stiffness","release:load"]}`
- 图片：[h1-warehouse-sorter-procedural](images/tasks/warehouse-sorter-procedural.png)

#### integrative · compound-edit-verification

- 题目：Select the only plan satisfying every hard safety, information, resource, access, and verification constraint.
- 形式：structured-plan
- 能力：cross-capability integration、resource-aware planning、risk control、verification
- Oracle 方法：complete hard-constraint plan filtering
- 答案：`{"planId":"P1","verificationId":"load-and-function-proof"}`
- 图片：[h1-warehouse-sorter-integrative](images/tasks/warehouse-sorter-integrative.png)

### 救援绞盘塔 / Rescue Winch Tower

#### atomic · vertical-anchor-operation

- 题目：Which candidate module has the highest geometric centroid?
- 形式：single-choice
- 能力：3D spatial relation、multi-view correspondence
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"B"}`
- 图片：[h1-rescue-winch-tower-atomic-anchor](images/tasks/rescue-winch-tower-atomic-anchor.png)

#### atomic · atomic-operation-coverage

- 题目：Which module is the direct structural parent of the highlighted service module?
- 形式：single-choice
- 能力：connectivity、attachment graph
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"C"}`
- 图片：[h1-rescue-winch-tower-atomic-coverage](images/tasks/rescue-winch-tower-atomic-coverage.png)

#### metacognitive · fault-diagnosis

- 题目：Which joint is the unique causal match for the observed child motion and lost constraint?
- 形式：single-choice
- 能力：fault diagnosis、causal localization、mechanism topology
- Oracle 方法：joint-to-child causal matching
- 答案：`{"choiceId":"B"}`
- 图片：[h1-rescue-winch-tower-meta](images/tasks/rescue-winch-tower-meta.png)

#### procedural · inspect-diagnose-act

- 题目：Return the ordered inspect-diagnose-act sequence; acting before inspection is invalid.
- 形式：ordered-actions
- 能力：active inspection、conditional planning、execution discipline
- Oracle 方法：state-transition and dependency contract
- 答案：`{"actionIds":["inspect:rescue-winch-tower-brace","interpret:observation","isolate:winch-drum","repair:cage-latch","verify:function","close:service-interface"]}`
- 图片：[h1-rescue-winch-tower-procedural](images/tasks/rescue-winch-tower-procedural.png)

#### integrative · multi-station-scheduling

- 题目：Select the only plan satisfying every hard safety, information, resource, access, and verification constraint.
- 形式：structured-plan
- 能力：cross-capability integration、resource-aware planning、risk control、verification
- Oracle 方法：complete hard-constraint plan filtering
- 答案：`{"planId":"P2","verificationId":"load-and-function-proof"}`
- 图片：[h1-rescue-winch-tower-integrative](images/tasks/rescue-winch-tower-integrative.png)

### 运河巡检艇 / Canal Inspection Skiff

#### atomic · vertical-anchor-operation

- 题目：Which edit performs the requested local recolor without collateral changes?
- 形式：single-choice
- 能力：instruction editing、recolor、change isolation
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"C"}`
- 图片：[h1-canal-inspection-skiff-atomic-anchor](images/tasks/canal-inspection-skiff-atomic-anchor.png)

#### atomic · atomic-operation-coverage

- 题目：Which module is directly anchored to the environment?
- 形式：single-choice
- 能力：support recognition、grounding
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"D"}`
- 图片：[h1-canal-inspection-skiff-atomic-coverage](images/tasks/canal-inspection-skiff-atomic-coverage.png)

#### metacognitive · active-inspection

- 题目：Which next inspection maximizes expected information gain per unit cost?
- 形式：single-choice
- 能力：active inspection、information gain、cost-aware metacognition
- Oracle 方法：finite-world entropy reduction divided by query cost
- 答案：`{"choiceId":"C"}`
- 图片：[h1-canal-inspection-skiff-meta](images/tasks/canal-inspection-skiff-meta.png)

#### procedural · assembly-sequencing

- 题目：Return a complete placement sequence that satisfies every declared dependency in the requested build prefix.
- 形式：ordered-actions
- 能力：assembly planning、ordering、prefix validity
- Oracle 方法：state-transition and dependency contract
- 答案：`{"actionIds":["place:hull","place:cabin","place:rudder","place:propeller","place:sensor-mast"]}`
- 图片：[h1-canal-inspection-skiff-procedural](images/tasks/canal-inspection-skiff-procedural.png)

#### integrative · diagnose-access-repair

- 题目：Select the only plan satisfying every hard safety, information, resource, access, and verification constraint.
- 形式：structured-plan
- 能力：cross-capability integration、resource-aware planning、risk control、verification
- Oracle 方法：complete hard-constraint plan filtering
- 答案：`{"planId":"P3","verificationId":"load-and-function-proof"}`
- 图片：[h1-canal-inspection-skiff-integrative](images/tasks/canal-inspection-skiff-integrative.png)

### 双轴太阳能跟踪阵列 / Solar Tracker Array

#### atomic · vertical-anchor-operation

- 题目：Which joint best explains the affected child and lost constraint?
- 形式：single-choice
- 能力：fault localization、causal diagnosis
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"D"}`
- 图片：[h1-solar-tracker-array-atomic-anchor](images/tasks/solar-tracker-array-atomic-anchor.png)

#### atomic · atomic-operation-coverage

- 题目：How many declared joints are incident on the highlighted module?
- 形式：single-choice
- 能力：contact counting、topology
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"A"}`
- 图片：[h1-solar-tracker-array-atomic-coverage](images/tasks/solar-tracker-array-atomic-coverage.png)

#### metacognitive · uncertainty-calibration

- 题目：Two hidden worlds remain action-incompatible under the current observation. What is the calibrated response?
- 形式：single-choice
- 能力：uncertainty calibration、abstention、clarification policy
- Oracle 方法：possible-world action-consistency check
- 答案：`{"choiceId":"D"}`
- 图片：[h1-solar-tracker-array-meta](images/tasks/solar-tracker-array-meta.png)

#### procedural · safe-disassembly

- 题目：Return a complete safe removal sequence; independent modules may be ordered either way.
- 形式：ordered-actions
- 能力：disassembly planning、dependency reversal、safe removal
- Oracle 方法：state-transition and dependency contract
- 答案：`{"actionIds":["remove:battery","remove:panel-right","remove:panel-left","remove:yoke","remove:mast","remove:foundation"]}`
- 图片：[h1-solar-tracker-array-procedural](images/tasks/solar-tracker-array-procedural.png)

#### integrative · inventory-robustness

- 题目：Select the only plan satisfying every hard safety, information, resource, access, and verification constraint.
- 形式：structured-plan
- 能力：cross-capability integration、resource-aware planning、risk control、verification
- Oracle 方法：complete hard-constraint plan filtering
- 答案：`{"planId":"P4","verificationId":"load-and-function-proof"}`
- 图片：[h1-solar-tracker-array-integrative](images/tasks/solar-tracker-array-integrative.png)

## D3 机构级

### 轨道检修车 / Orbital Service Rover

#### atomic · vertical-anchor-operation

- 题目：Which named module is highlighted?
- 形式：single-choice
- 能力：part and module recognition、visual grounding
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"A"}`
- 图片：[h1-orbital-service-rover-atomic-anchor](images/tasks/orbital-service-rover-atomic-anchor.png)

#### atomic · atomic-operation-coverage

- 题目：Which edit performs the requested local recolor without collateral changes?
- 形式：single-choice
- 能力：instruction editing、recolor、change isolation
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"B"}`
- 图片：[h1-orbital-service-rover-atomic-coverage](images/tasks/orbital-service-rover-atomic-coverage.png)

#### metacognitive · multiobjective-tradeoff

- 题目：Select every non-dominated buildable alternative under lower cost, lower mass, and higher stiffness.
- 形式：multiple-choice
- 能力：Pareto reasoning、multi-objective trade-off、engineering metacognition
- Oracle 方法：complete Pareto-set enumeration
- 答案：`{"choiceIds":["A","B","C"]}`
- 图片：[h1-orbital-service-rover-meta](images/tasks/orbital-service-rover-meta.png)

#### procedural · edit-then-verify

- 题目：Return the minimum ordered actions for a local recolor followed by state verification.
- 形式：ordered-actions
- 能力：instruction execution、local editing、postcondition verification
- Oracle 方法：state-transition and dependency contract
- 答案：`{"actionIds":["isolate:battery","recolor:battery:safety-orange","restore:battery","verify:no-collateral-change","verify:function","release:service-zone"]}`
- 图片：[h1-orbital-service-rover-procedural](images/tasks/orbital-service-rover-procedural.png)

#### integrative · inspect-plan-execute

- 题目：Select the only plan satisfying every hard safety, information, resource, access, and verification constraint.
- 形式：structured-plan
- 能力：cross-capability integration、resource-aware planning、risk control、verification、long-horizon coordination、hidden-state management
- Oracle 方法：complete hard-constraint plan filtering
- 答案：`{"planId":"P1","verificationId":"load-and-function-proof"}`
- 图片：[h1-orbital-service-rover-integrative](images/tasks/orbital-service-rover-integrative.png)

### 港口集装箱起重机 / Harbor Container Crane

#### atomic · vertical-anchor-operation

- 题目：Which candidate module has the highest geometric centroid?
- 形式：single-choice
- 能力：3D spatial relation、multi-view correspondence
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"B"}`
- 图片：[h1-harbor-container-crane-atomic-anchor](images/tasks/harbor-container-crane-atomic-anchor.png)

#### atomic · atomic-operation-coverage

- 题目：Which addition obeys the placement and non-interference constraints?
- 形式：single-choice
- 能力：part addition、interface selection、collision avoidance
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"C"}`
- 图片：[h1-harbor-container-crane-atomic-coverage](images/tasks/harbor-container-crane-atomic-coverage.png)

#### metacognitive · prefix-stability

- 题目：Which candidate preserves a supported dependency prefix after every placement?
- 形式：single-choice
- 能力：prefix stability、causal support、calibrated physical reasoning
- Oracle 方法：joint dependency graph enumeration
- 答案：`{"choiceId":"B"}`
- 图片：[h1-harbor-container-crane-meta](images/tasks/harbor-container-crane-meta.png)

#### procedural · fault-recovery

- 题目：Return the minimum certified recovery sequence for the declared failed joint.
- 形式：ordered-actions
- 能力：fault recovery、minimal repair、action sequencing
- Oracle 方法：state-transition and dependency contract
- 答案：`{"actionIds":["lower-hoist","stabilize-container","replace-hook-latch","tension-hoist","raise-test-load"]}`
- 图片：[h1-harbor-container-crane-procedural](images/tasks/harbor-container-crane-procedural.png)

#### integrative · multiobjective-maintenance

- 题目：Select the only plan satisfying every hard safety, information, resource, access, and verification constraint.
- 形式：structured-plan
- 能力：cross-capability integration、resource-aware planning、risk control、verification、long-horizon coordination、hidden-state management
- Oracle 方法：complete hard-constraint plan filtering
- 答案：`{"planId":"P2","verificationId":"load-and-function-proof"}`
- 图片：[h1-harbor-container-crane-integrative](images/tasks/harbor-container-crane-integrative.png)

### 双叶运河开启桥 / Bascule Canal Gate

#### atomic · vertical-anchor-operation

- 题目：Which edit performs the requested local recolor without collateral changes?
- 形式：single-choice
- 能力：instruction editing、recolor、change isolation
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"C"}`
- 图片：[h1-bascule-canal-gate-atomic-anchor](images/tasks/bascule-canal-gate-atomic-anchor.png)

#### atomic · atomic-operation-coverage

- 题目：Which removal is locally executable without first dismantling a dependent child?
- 形式：single-choice
- 能力：part removal、dependency reasoning
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"D"}`
- 图片：[h1-bascule-canal-gate-atomic-coverage](images/tasks/bascule-canal-gate-atomic-coverage.png)

#### metacognitive · assembly-accessibility

- 题目：Select every service path whose minimum swept-volume clearance is strictly positive.
- 形式：multiple-choice
- 能力：assembly accessibility、continuous collision reasoning、set-valued decisions
- Oracle 方法：swept-volume clearance threshold
- 答案：`{"choiceIds":["C","D"]}`
- 图片：[h1-bascule-canal-gate-meta](images/tasks/bascule-canal-gate-meta.png)

#### procedural · inventory-replan

- 题目：Return the ordered stockout-recovery actions using the only feasible replacement.
- 形式：ordered-actions
- 能力：inventory replanning、structural substitution、constraint-preserving execution
- Oracle 方法：state-transition and dependency contract
- 答案：`{"actionIds":["inspect:stock","select:tension-cable","isolate:west-deck","install:tension-cable","verify:stiffness","release:load"]}`
- 图片：[h1-bascule-canal-gate-procedural](images/tasks/bascule-canal-gate-procedural.png)

#### integrative · compound-edit-verification

- 题目：Select the only plan satisfying every hard safety, information, resource, access, and verification constraint.
- 形式：structured-plan
- 能力：cross-capability integration、resource-aware planning、risk control、verification、long-horizon coordination、hidden-state management
- Oracle 方法：complete hard-constraint plan filtering
- 答案：`{"planId":"P3","verificationId":"load-and-function-proof"}`
- 图片：[h1-bascule-canal-gate-integrative](images/tasks/bascule-canal-gate-integrative.png)

### 自适应射电观测站 / Adaptive Radio Observatory

#### atomic · vertical-anchor-operation

- 题目：Which joint best explains the affected child and lost constraint?
- 形式：single-choice
- 能力：fault localization、causal diagnosis
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"D"}`
- 图片：[h1-adaptive-radio-observatory-atomic-anchor](images/tasks/adaptive-radio-observatory-atomic-anchor.png)

#### atomic · atomic-operation-coverage

- 题目：Which replacement satisfies the finite inventory and stiffness requirements?
- 形式：single-choice
- 能力：replacement、finite inventory、constraint checking
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"A"}`
- 图片：[h1-adaptive-radio-observatory-atomic-coverage](images/tasks/adaptive-radio-observatory-atomic-coverage.png)

#### metacognitive · support-counterfactual

- 题目：If the declared support interface is removed, which listed modules lose their certified support path?
- 形式：multiple-choice
- 能力：counterfactual support、dependency closure、set-valued prediction
- Oracle 方法：directed support-graph transitive closure
- 答案：`{"choiceIds":["B","C","D"]}`
- 图片：[h1-adaptive-radio-observatory-meta](images/tasks/adaptive-radio-observatory-meta.png)

#### procedural · inspect-diagnose-act

- 题目：Return the ordered inspect-diagnose-act sequence; acting before inspection is invalid.
- 形式：ordered-actions
- 能力：active inspection、conditional planning、execution discipline
- Oracle 方法：state-transition and dependency contract
- 答案：`{"actionIds":["inspect:observatory-marker","interpret:observation","isolate:camera-pack","repair:camera-bayonet","verify:function","close:service-interface"]}`
- 图片：[h1-adaptive-radio-observatory-procedural](images/tasks/adaptive-radio-observatory-procedural.png)

#### integrative · multi-station-scheduling

- 题目：Select the only plan satisfying every hard safety, information, resource, access, and verification constraint.
- 形式：structured-plan
- 能力：cross-capability integration、resource-aware planning、risk control、verification、long-horizon coordination、hidden-state management
- Oracle 方法：complete hard-constraint plan filtering
- 答案：`{"planId":"P4","verificationId":"load-and-function-proof"}`
- 图片：[h1-adaptive-radio-observatory-integrative](images/tasks/adaptive-radio-observatory-integrative.png)

### 山火救援倾转旋翼机 / Wildfire Tiltrotor

#### atomic · vertical-anchor-operation

- 题目：Which module is directly anchored to the environment?
- 形式：single-choice
- 能力：support recognition、grounding
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"A"}`
- 图片：[h1-wildfire-tiltrotor-atomic-anchor](images/tasks/wildfire-tiltrotor-atomic-anchor.png)

#### atomic · atomic-operation-coverage

- 题目：Which local correction exactly inverts the observed pose error?
- 形式：single-choice
- 能力：pose estimation、inverse transform
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"B"}`
- 图片：[h1-wildfire-tiltrotor-atomic-coverage](images/tasks/wildfire-tiltrotor-atomic-coverage.png)

#### metacognitive · dynamic-robustness

- 题目：What is the largest tested impulse satisfying both transient and residual motion limits?
- 形式：single-choice
- 能力：dynamic robustness、threshold estimation、multi-criterion checking
- Oracle 方法：two-threshold response-table evaluation
- 答案：`{"choiceId":"A"}`
- 图片：[h1-wildfire-tiltrotor-meta](images/tasks/wildfire-tiltrotor-meta.png)

#### procedural · assembly-sequencing

- 题目：Return a complete placement sequence that satisfies every declared dependency in the requested build prefix.
- 形式：ordered-actions
- 能力：assembly planning、ordering、prefix validity
- Oracle 方法：state-transition and dependency contract
- 答案：`{"actionIds":["place:fuselage","place:water-tank","place:nacelle-left","place:nacelle-right","place:rotor-left","place:rotor-right"]}`
- 图片：[h1-wildfire-tiltrotor-procedural](images/tasks/wildfire-tiltrotor-procedural.png)

#### integrative · diagnose-access-repair

- 题目：Select the only plan satisfying every hard safety, information, resource, access, and verification constraint.
- 形式：structured-plan
- 能力：cross-capability integration、resource-aware planning、risk control、verification、long-horizon coordination、hidden-state management
- Oracle 方法：complete hard-constraint plan filtering
- 答案：`{"planId":"P1","verificationId":"load-and-function-proof"}`
- 图片：[h1-wildfire-tiltrotor-integrative](images/tasks/wildfire-tiltrotor-integrative.png)

### 极地科研站 / Polar Research Station

#### atomic · vertical-anchor-operation

- 题目：Which local correction exactly inverts the observed pose error?
- 形式：single-choice
- 能力：pose estimation、inverse transform
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"B"}`
- 图片：[h1-polar-research-station-atomic-anchor](images/tasks/polar-research-station-atomic-anchor.png)

#### atomic · atomic-operation-coverage

- 题目：Which joint best explains the affected child and lost constraint?
- 形式：single-choice
- 能力：fault localization、causal diagnosis
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"C"}`
- 图片：[h1-polar-research-station-atomic-coverage](images/tasks/polar-research-station-atomic-coverage.png)

#### metacognitive · functional-kinematics

- 题目：Which motion statement is consistent with the designated functional joint?
- 形式：single-choice
- 能力：functional kinematics、joint semantics、axis and limit reasoning
- Oracle 方法：declared joint contract
- 答案：`{"choiceId":"B"}`
- 图片：[h1-polar-research-station-meta](images/tasks/polar-research-station-meta.png)

#### procedural · safe-disassembly

- 题目：Return a complete safe removal sequence; independent modules may be ordered either way.
- 形式：ordered-actions
- 能力：disassembly planning、dependency reversal、safe removal
- Oracle 方法：state-transition and dependency contract
- 答案：`{"actionIds":["remove:airlock-door","remove:wind-rotor","remove:solar-carriage","remove:wind-mast","remove:station-base"]}`
- 图片：[h1-polar-research-station-procedural](images/tasks/polar-research-station-procedural.png)

#### integrative · inventory-robustness

- 题目：Select the only plan satisfying every hard safety, information, resource, access, and verification constraint.
- 形式：structured-plan
- 能力：cross-capability integration、resource-aware planning、risk control、verification、long-horizon coordination、hidden-state management
- Oracle 方法：complete hard-constraint plan filtering
- 答案：`{"planId":"P2","verificationId":"load-and-function-proof"}`
- 图片：[h1-polar-research-station-integrative](images/tasks/polar-research-station-integrative.png)

## D4 系统级

### 轨道综合对接场 / Orbital Docking Yard

#### atomic · vertical-anchor-operation

- 题目：Which named module is highlighted?
- 形式：single-choice
- 能力：part and module recognition、visual grounding
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"C"}`
- 图片：[h1-orbital-docking-yard-atomic-anchor](images/tasks/orbital-docking-yard-atomic-anchor.png)

#### atomic · atomic-operation-coverage

- 题目：Which module is the next valid placement in the certified assembly order?
- 形式：single-choice
- 能力：next-action prediction、assembly order
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"D"}`
- 图片：[h1-orbital-docking-yard-atomic-coverage](images/tasks/orbital-docking-yard-atomic-coverage.png)

#### metacognitive · fault-diagnosis

- 题目：Which joint is the unique causal match for the observed child motion and lost constraint?
- 形式：single-choice
- 能力：fault diagnosis、causal localization、mechanism topology
- Oracle 方法：joint-to-child causal matching
- 答案：`{"choiceId":"C"}`
- 图片：[h1-orbital-docking-yard-meta](images/tasks/orbital-docking-yard-meta.png)

#### procedural · edit-then-verify

- 题目：Return the minimum ordered actions for a local recolor followed by state verification.
- 形式：ordered-actions
- 能力：instruction execution、local editing、postcondition verification
- Oracle 方法：state-transition and dependency contract
- 答案：`{"actionIds":["isolate:airlock","recolor:airlock:safety-orange","restore:airlock","verify:no-collateral-change","verify:function","release:service-zone"]}`
- 图片：[h1-orbital-docking-yard-procedural](images/tasks/orbital-docking-yard-procedural.png)

#### integrative · inspect-plan-execute

- 题目：Select the only plan satisfying every hard safety, information, resource, access, and verification constraint.
- 形式：structured-plan
- 能力：cross-capability integration、resource-aware planning、risk control、verification、long-horizon coordination、hidden-state management
- Oracle 方法：complete hard-constraint plan filtering
- 答案：`{"planId":"P3","verificationId":"load-and-function-proof"}`
- 图片：[h1-orbital-docking-yard-integrative](images/tasks/orbital-docking-yard-integrative.png)

### 洪水应急船闸系统 / Flood Response Lock

#### atomic · vertical-anchor-operation

- 题目：Which candidate module has the highest geometric centroid?
- 形式：single-choice
- 能力：3D spatial relation、multi-view correspondence
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"D"}`
- 图片：[h1-flood-response-lock-atomic-anchor](images/tasks/flood-response-lock-atomic-anchor.png)

#### atomic · atomic-operation-coverage

- 题目：Which stock item is currently usable under all declared hard constraints?
- 形式：single-choice
- 能力：inventory checking、resource constraints
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"A"}`
- 图片：[h1-flood-response-lock-atomic-coverage](images/tasks/flood-response-lock-atomic-coverage.png)

#### metacognitive · active-inspection

- 题目：Which next inspection maximizes expected information gain per unit cost?
- 形式：single-choice
- 能力：active inspection、information gain、cost-aware metacognition
- Oracle 方法：finite-world entropy reduction divided by query cost
- 答案：`{"choiceId":"D"}`
- 图片：[h1-flood-response-lock-meta](images/tasks/flood-response-lock-meta.png)

#### procedural · fault-recovery

- 题目：Return the minimum certified recovery sequence for the declared failed joint.
- 形式：ordered-actions
- 能力：fault recovery、minimal repair、action sequencing
- Oracle 方法：state-transition and dependency contract
- 答案：`{"actionIds":["isolate-load","access-pump-a","replace-north-gate-hinge","reindex-mechanism","proof-test"]}`
- 图片：[h1-flood-response-lock-procedural](images/tasks/flood-response-lock-procedural.png)

#### integrative · multiobjective-maintenance

- 题目：Select the only plan satisfying every hard safety, information, resource, access, and verification constraint.
- 形式：structured-plan
- 能力：cross-capability integration、resource-aware planning、risk control、verification、long-horizon coordination、hidden-state management
- Oracle 方法：complete hard-constraint plan filtering
- 答案：`{"planId":"P4","verificationId":"load-and-function-proof"}`
- 图片：[h1-flood-response-lock-integrative](images/tasks/flood-response-lock-integrative.png)

### 自动化货运终端 / Automated Cargo Terminal

#### atomic · vertical-anchor-operation

- 题目：Which edit performs the requested local recolor without collateral changes?
- 形式：single-choice
- 能力：instruction editing、recolor、change isolation
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"A"}`
- 图片：[h1-automated-cargo-terminal-atomic-anchor](images/tasks/automated-cargo-terminal-atomic-anchor.png)

#### atomic · atomic-operation-coverage

- 题目：Which candidate corresponds to the declared replaceable subassembly boundary?
- 形式：single-choice
- 能力：subassembly segmentation、interface reasoning
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"B"}`
- 图片：[h1-automated-cargo-terminal-atomic-coverage](images/tasks/automated-cargo-terminal-atomic-coverage.png)

#### metacognitive · uncertainty-calibration

- 题目：Two hidden worlds remain action-incompatible under the current observation. What is the calibrated response?
- 形式：single-choice
- 能力：uncertainty calibration、abstention、clarification policy
- Oracle 方法：possible-world action-consistency check
- 答案：`{"choiceId":"A"}`
- 图片：[h1-automated-cargo-terminal-meta](images/tasks/automated-cargo-terminal-meta.png)

#### procedural · inventory-replan

- 题目：Return the ordered stockout-recovery actions using the only feasible replacement.
- 形式：ordered-actions
- 能力：inventory replanning、structural substitution、constraint-preserving execution
- Oracle 方法：state-transition and dependency contract
- 答案：`{"actionIds":["inspect:stock","select:long-beam","isolate:lift","install:long-beam","verify:stiffness","release:load"]}`
- 图片：[h1-automated-cargo-terminal-procedural](images/tasks/automated-cargo-terminal-procedural.png)

#### integrative · compound-edit-verification

- 题目：Select the only plan satisfying every hard safety, information, resource, access, and verification constraint.
- 形式：structured-plan
- 能力：cross-capability integration、resource-aware planning、risk control、verification、long-horizon coordination、hidden-state management
- Oracle 方法：complete hard-constraint plan filtering
- 答案：`{"planId":"P1","verificationId":"load-and-function-proof"}`
- 图片：[h1-automated-cargo-terminal-integrative](images/tasks/automated-cargo-terminal-integrative.png)

### 月面样品精炼站 / Lunar Sample Refinery

#### atomic · vertical-anchor-operation

- 题目：Which joint best explains the affected child and lost constraint?
- 形式：single-choice
- 能力：fault localization、causal diagnosis
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"B"}`
- 图片：[h1-lunar-sample-refinery-atomic-anchor](images/tasks/lunar-sample-refinery-atomic-anchor.png)

#### atomic · atomic-operation-coverage

- 题目：The requested state already matches the current state. What is the minimum valid action?
- 形式：single-choice
- 能力：no-op detection、minimal intervention
- Oracle 方法：exact authored model-state lookup
- 答案：`{"choiceId":"C"}`
- 图片：[h1-lunar-sample-refinery-atomic-coverage](images/tasks/lunar-sample-refinery-atomic-coverage.png)

#### metacognitive · multiobjective-tradeoff

- 题目：Select every non-dominated buildable alternative under lower cost, lower mass, and higher stiffness.
- 形式：multiple-choice
- 能力：Pareto reasoning、multi-objective trade-off、engineering metacognition
- Oracle 方法：complete Pareto-set enumeration
- 答案：`{"choiceIds":["A","B","D"]}`
- 图片：[h1-lunar-sample-refinery-meta](images/tasks/lunar-sample-refinery-meta.png)

#### procedural · inspect-diagnose-act

- 题目：Return the ordered inspect-diagnose-act sequence; acting before inspection is invalid.
- 形式：ordered-actions
- 能力：active inspection、conditional planning、execution discipline
- Oracle 方法：state-transition and dependency contract
- 答案：`{"actionIds":["inspect:lunar-sample-refinery-brace","interpret:observation","isolate:loading-arm","repair:conveyor-drive","verify:function","close:service-interface"]}`
- 图片：[h1-lunar-sample-refinery-procedural](images/tasks/lunar-sample-refinery-procedural.png)

#### integrative · multi-station-scheduling

- 题目：Select the only plan satisfying every hard safety, information, resource, access, and verification constraint.
- 形式：structured-plan
- 能力：cross-capability integration、resource-aware planning、risk control、verification、long-horizon coordination、hidden-state management
- Oracle 方法：complete hard-constraint plan filtering
- 答案：`{"planId":"P2","verificationId":"load-and-function-proof"}`
- 图片：[h1-lunar-sample-refinery-integrative](images/tasks/lunar-sample-refinery-integrative.png)
