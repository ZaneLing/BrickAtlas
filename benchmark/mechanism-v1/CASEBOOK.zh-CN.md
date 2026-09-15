# BrickAtlas Mechanism-1 全部题目

> OMR/LDraw 只用于设计复杂度参考，不是本套件 case。以下 48 道题全部来自 6 个原创机构对象。

## 模型实测总览

| 模型 | Exact Success |
|---|---:|
| Qwen3-0.6B 本地文本 | 3/48 |
| GPT-4.1 mini | 28/48 |
| Gemini 2.5 Flash | 31/48 |

## 轨道检修车 / Orbital Service Rover

A six-wheel pressurized rover with service battery, panoramic mast and articulated sampling arm.

- 可视零件：73
- 刚体模块：10
- 物理关节：9

### 全过程前缀动力学

- **题目**：Which candidate module order remains dynamically supported at every prefix, and where does the other first fail?
- **考察目标**：逐步装配时是否出现坠落、失稳或错误依赖
- **对应能力**：长程规划、前缀动力学、因果支撑
- **可视化**：[查看图片](images/tasks/orbital-service-rover-prefix-dynamics.png)
- **Oracle**：`{"validPlanId":"plan-a","invalidPlanFirstFailure":0}`
- **Qwen3-0.6B 本地文本**：通过，`{"validPlanId":"plan-a","invalidPlanFirstFailure":0}`
- **GPT-4.1 mini**：通过，`{"validPlanId":"plan-a","invalidPlanFirstFailure":0}`
- **Gemini 2.5 Flash**：通过，`{"validPlanId":"plan-a","invalidPlanFirstFailure":0}`

### 连续路径可达性

- **题目**：Which proposed swept-volume paths let the declared service tool reach the target interface without collision?
- **考察目标**：工具或零件的扫掠体能否无碰撞到达维修界面
- **对应能力**：连续碰撞检测、装配可达性、维修规划
- **可视化**：[查看图片](images/tasks/orbital-service-rover-insertion-access.png)
- **Oracle**：`{"accessiblePathIds":["rear-slide"]}`
- **Qwen3-0.6B 本地文本**：失败，`{"accessiblePathIds":["rear-slide","roof-drop","side-insert"]}`
- **GPT-4.1 mini**：失败，`{"accessiblePathIds":["rear-slide","roof-drop"]}`
- **Gemini 2.5 Flash**：失败，`{"accessiblePathIds":["rear-slide","roof-drop"]}`

### 故障诊断与最小返工

- **题目**：Identify the failed joint from the measured displacement and return the minimum certified recovery action sequence.
- **考察目标**：从动力学后果定位故障关节并给出最小维修
- **对应能力**：故障定位、因果诊断、最小返工
- **可视化**：[查看图片](images/tasks/orbital-service-rover-fault-recovery.png)
- **Oracle**：`{"faultJointId":"arm-shoulder","actions":["stow-arm","support-boom","replace-shoulder-pin","reindex-arm","release-boom"]}`
- **Qwen3-0.6B 本地文本**：失败，`{"faultJointId":"arm-shoulder","actions":["stow-arm","support-boom","replace-unrelated-panel"]}`
- **GPT-4.1 mini**：失败，`{"faultJointId":"arm-shoulder","actions":["stow-arm","replace-shoulder-pin","reindex-arm"]}`
- **Gemini 2.5 Flash**：通过，`{"faultJointId":"arm-shoulder","actions":["stow-arm","support-boom","replace-shoulder-pin","reindex-arm","release-boom"]}`

### 有限库存替代

- **题目**：A required brace is unavailable. Which listed replacement satisfies cost, piece-count and minimum-stiffness constraints?
- **考察目标**：缺件时满足成本、数量和刚度约束的替代
- **对应能力**：有限库存、结构替代、约束满足
- **可视化**：[查看图片](images/tasks/orbital-service-rover-inventory-substitution.png)
- **Oracle**：`{"alternativeId":"twin-truss"}`
- **Qwen3-0.6B 本地文本**：失败，`{"id":"twin-truss","label":"Two interlocked short trusses","pieces":2,"cost":6,"mass":2.2,"stiffness":11,"jointMode":"fixed"}`
- **GPT-4.1 mini**：通过，`{"alternativeId":"twin-truss"}`
- **Gemini 2.5 Flash**：通过，`{"alternativeId":"twin-truss"}`

### 动态扰动鲁棒性

- **题目**：What is the largest tested impulse that stays within the declared transient and residual displacement limits?
- **考察目标**：冲击下的最大瞬态位移和残余位移
- **对应能力**：动态物理推理、冲击鲁棒性、失效阈值估计
- **可视化**：[查看图片](images/tasks/orbital-service-rover-dynamic-robustness.png)
- **Oracle**：`{"maxSafeImpulse":20}`
- **Qwen3-0.6B 本地文本**：失败，`{"maxSafeImpulse":60}`
- **GPT-4.1 mini**：通过，`{"maxSafeImpulse":20}`
- **Gemini 2.5 Flash**：通过，`{"maxSafeImpulse":20}`

### 功能与运动学正确性

- **题目**：Under motor actuation, does the designated revolute or prismatic mechanism achieve the required motion?
- **考察目标**：铰链、滑轨、转台或旋翼能否完成目标运动
- **对应能力**：关节语义、功能预测、运动学推理
- **可视化**：[查看图片](images/tasks/orbital-service-rover-functional-kinematics.png)
- **Oracle**：`{"jointId":"arm-shoulder","reachesTarget":true}`
- **Qwen3-0.6B 本地文本**：失败，`{"id":"m1-orbital-service-rover-functional-kinematics","kind":"functional-kinematics","capability":["joint semantics","functional prediction","kinematic reasoning"],"question":"Under motor actuation, does the designated revolute or prismatic mechanism achieve the required motion?","responseSchema":{"jointId":"string","reachesTarget":"boolean"}}`
- **GPT-4.1 mini**：通过，`{"jointId":"arm-shoulder","reachesTarget":true}`
- **Gemini 2.5 Flash**：通过，`{"jointId":"arm-shoulder","reachesTarget":true}`

### 主动检查与澄清

- **题目**：Which inspection should be requested next to maximize expected information gain per unit cost?
- **考察目标**：选择单位成本信息增益最高的下一次检查
- **对应能力**：主动感知、信息增益、成本敏感澄清
- **可视化**：[查看图片](images/tasks/orbital-service-rover-active-inspection.png)
- **Oracle**：`{"queryIds":["rover-marker"]}`
- **Qwen3-0.6B 本地文本**：失败，`{"queryId":"rover-probe"}`
- **GPT-4.1 mini**：失败，`{"queryId":"rover-brace"}`
- **Gemini 2.5 Flash**：失败，`{"queryId":"rover-brace"}`

### 多目标工程权衡

- **题目**：Return every non-dominated buildable alternative under lower cost, lower mass and higher stiffness.
- **考察目标**：识别成本、质量、刚度之间的 Pareto 解
- **对应能力**：Pareto 推理、成本-质量-刚度权衡、工程设计
- **可视化**：[查看图片](images/tasks/orbital-service-rover-multiobjective-design.png)
- **Oracle**：`{"paretoIds":["carbon-beam","tension-cable","twin-truss"]}`
- **Qwen3-0.6B 本地文本**：失败，`{"paretoIds":["carbon-beam","twin-truss"]}`
- **GPT-4.1 mini**：失败，`{"paretoIds":["tension-cable","twin-truss"]}`
- **Gemini 2.5 Flash**：失败，`{"paretoIds":["tension-cable","twin-truss"]}`

## 港口集装箱起重机 / Harbor Container Crane

A twin-tower rail crane with traversing trolley, vertical hoist, control cabin and container payload.

- 可视零件：126
- 刚体模块：5
- 物理关节：5

### 全过程前缀动力学

- **题目**：Which candidate module order remains dynamically supported at every prefix, and where does the other first fail?
- **考察目标**：逐步装配时是否出现坠落、失稳或错误依赖
- **对应能力**：长程规划、前缀动力学、因果支撑
- **可视化**：[查看图片](images/tasks/harbor-container-crane-prefix-dynamics.png)
- **Oracle**：`{"validPlanId":"plan-a","invalidPlanFirstFailure":0}`
- **Qwen3-0.6B 本地文本**：失败，`{"validPlanId":"plan-a","invalidPlanFirstFailure":1}`
- **GPT-4.1 mini**：通过，`{"validPlanId":"plan-a","invalidPlanFirstFailure":0}`
- **Gemini 2.5 Flash**：通过，`{"validPlanId":"plan-a","invalidPlanFirstFailure":0}`

### 连续路径可达性

- **题目**：Which proposed swept-volume paths let the declared service tool reach the target interface without collision?
- **考察目标**：工具或零件的扫掠体能否无碰撞到达维修界面
- **对应能力**：连续碰撞检测、装配可达性、维修规划
- **可视化**：[查看图片](images/tasks/harbor-container-crane-insertion-access.png)
- **Oracle**：`{"accessiblePathIds":["rail-entry","tower-gap"]}`
- **Qwen3-0.6B 本地文本**：失败，`{"accessiblePathIds":["rail-entry","tower-gap","cabin-side"]}`
- **GPT-4.1 mini**：通过，`{"accessiblePathIds":["rail-entry","tower-gap"]}`
- **Gemini 2.5 Flash**：失败，`{"accessiblePathIds":["tower-gap"]}`

### 故障诊断与最小返工

- **题目**：Identify the failed joint from the measured displacement and return the minimum certified recovery action sequence.
- **考察目标**：从动力学后果定位故障关节并给出最小维修
- **对应能力**：故障定位、因果诊断、最小返工
- **可视化**：[查看图片](images/tasks/harbor-container-crane-fault-recovery.png)
- **Oracle**：`{"faultJointId":"hook-latch","actions":["lower-hoist","stabilize-container","replace-hook-latch","tension-hoist","raise-test-load"]}`
- **Qwen3-0.6B 本地文本**：失败，`{"faultJointId":"hook-latch","actions":["lower-hoist","stabilize-container"]}`
- **GPT-4.1 mini**：失败，`{"faultJointId":"hook-latch","actions":["replace-hook-latch","stabilize-container"]}`
- **Gemini 2.5 Flash**：通过，`{"faultJointId":"hook-latch","actions":["lower-hoist","stabilize-container","replace-hook-latch","tension-hoist","raise-test-load"]}`

### 有限库存替代

- **题目**：A required brace is unavailable. Which listed replacement satisfies cost, piece-count and minimum-stiffness constraints?
- **考察目标**：缺件时满足成本、数量和刚度约束的替代
- **对应能力**：有限库存、结构替代、约束满足
- **可视化**：[查看图片](images/tasks/harbor-container-crane-inventory-substitution.png)
- **Oracle**：`{"alternativeId":"carbon-beam"}`
- **Qwen3-0.6B 本地文本**：失败，`{"id":"twin-truss","label":"Two interlocked short trusses","pieces":2,"cost":6,"mass":1.5,"stiffness":11,"jointMode":"fixed"}`
- **GPT-4.1 mini**：通过，`{"alternativeId":"carbon-beam"}`
- **Gemini 2.5 Flash**：通过，`{"alternativeId":"carbon-beam"}`

### 动态扰动鲁棒性

- **题目**：What is the largest tested impulse that stays within the declared transient and residual displacement limits?
- **考察目标**：冲击下的最大瞬态位移和残余位移
- **对应能力**：动态物理推理、冲击鲁棒性、失效阈值估计
- **可视化**：[查看图片](images/tasks/harbor-container-crane-dynamic-robustness.png)
- **Oracle**：`{"maxSafeImpulse":40}`
- **Qwen3-0.6B 本地文本**：失败，`{"maxSafeImpulse":100}`
- **GPT-4.1 mini**：通过，`{"maxSafeImpulse":40}`
- **Gemini 2.5 Flash**：失败，`{"maxSafeImpulse":100}`

### 功能与运动学正确性

- **题目**：Under motor actuation, does the designated revolute or prismatic mechanism achieve the required motion?
- **考察目标**：铰链、滑轨、转台或旋翼能否完成目标运动
- **对应能力**：关节语义、功能预测、运动学推理
- **可视化**：[查看图片](images/tasks/harbor-container-crane-functional-kinematics.png)
- **Oracle**：`{"jointId":"trolley-rail","reachesTarget":false}`
- **Qwen3-0.6B 本地文本**：失败，`{"id":"m1-harbor-container-crane-functional-kinematics","kind":"functional-kinematics","capability":["joint semantics","functional prediction","kinematic reasoning"],"question":"Under motor actuation, does the designated revolute or prismatic mechanism achieve the required motion?","responseSchema":{"jointId":"string","reachesTarget":"boolean"}}`
- **GPT-4.1 mini**：失败，`{"jointId":"trolley-rail","reachesTarget":true}`
- **Gemini 2.5 Flash**：失败，`{"jointId":"trolley-rail","reachesTarget":true}`

### 主动检查与澄清

- **题目**：Which inspection should be requested next to maximize expected information gain per unit cost?
- **考察目标**：选择单位成本信息增益最高的下一次检查
- **对应能力**：主动感知、信息增益、成本敏感澄清
- **可视化**：[查看图片](images/tasks/harbor-container-crane-active-inspection.png)
- **Oracle**：`{"queryIds":["crane-probe"]}`
- **Qwen3-0.6B 本地文本**：通过，`{"queryId":"crane-probe"}`
- **GPT-4.1 mini**：通过，`{"queryId":"crane-probe"}`
- **Gemini 2.5 Flash**：通过，`{"queryId":"crane-probe"}`

### 多目标工程权衡

- **题目**：Return every non-dominated buildable alternative under lower cost, lower mass and higher stiffness.
- **考察目标**：识别成本、质量、刚度之间的 Pareto 解
- **对应能力**：Pareto 推理、成本-质量-刚度权衡、工程设计
- **可视化**：[查看图片](images/tasks/harbor-container-crane-multiobjective-design.png)
- **Oracle**：`{"paretoIds":["tension-cable","twin-truss"]}`
- **Qwen3-0.6B 本地文本**：失败，`{"paretoIds":["carbon-beam","twin-truss"]}`
- **GPT-4.1 mini**：通过，`{"paretoIds":["twin-truss","tension-cable"]}`
- **Gemini 2.5 Flash**：通过，`{"paretoIds":["tension-cable","twin-truss"]}`

## 双叶运河开启桥 / Bascule Canal Gate

A twin-tower canal crossing with two hinged decks, drive cartridge, counterweight gears and service galleries.

- 可视零件：142
- 刚体模块：6
- 物理关节：7

### 全过程前缀动力学

- **题目**：Which candidate module order remains dynamically supported at every prefix, and where does the other first fail?
- **考察目标**：逐步装配时是否出现坠落、失稳或错误依赖
- **对应能力**：长程规划、前缀动力学、因果支撑
- **可视化**：[查看图片](images/tasks/bascule-canal-gate-prefix-dynamics.png)
- **Oracle**：`{"validPlanId":"plan-a","invalidPlanFirstFailure":0}`
- **Qwen3-0.6B 本地文本**：失败，`{"validPlanId":"plan-b","invalidPlanFirstFailure":1}`
- **GPT-4.1 mini**：通过，`{"validPlanId":"plan-a","invalidPlanFirstFailure":0}`
- **Gemini 2.5 Flash**：通过，`{"validPlanId":"plan-a","invalidPlanFirstFailure":0}`

### 连续路径可达性

- **题目**：Which proposed swept-volume paths let the declared service tool reach the target interface without collision?
- **考察目标**：工具或零件的扫掠体能否无碰撞到达维修界面
- **对应能力**：连续碰撞检测、装配可达性、维修规划
- **可视化**：[查看图片](images/tasks/bascule-canal-gate-insertion-access.png)
- **Oracle**：`{"accessiblePathIds":["gallery-entry","deck-side"]}`
- **Qwen3-0.6B 本地文本**：失败，`{"accessiblePathIds":["gallery-entry"]}`
- **GPT-4.1 mini**：失败，`{"accessiblePathIds":["gallery-entry","tower-drop"]}`
- **Gemini 2.5 Flash**：失败，`{"accessiblePathIds":["gallery-entry","tower-drop"]}`

### 故障诊断与最小返工

- **题目**：Identify the failed joint from the measured displacement and return the minimum certified recovery action sequence.
- **考察目标**：从动力学后果定位故障关节并给出最小维修
- **对应能力**：故障定位、因果诊断、最小返工
- **可视化**：[查看图片](images/tasks/bascule-canal-gate-fault-recovery.png)
- **Oracle**：`{"faultJointId":"drive-lock","actions":["lock-decks-open","open-gallery","remove-damaged-drive","install-drive-cartridge","calibrate-hinge","close-gallery"]}`
- **Qwen3-0.6B 本地文本**：失败，`{"faultJointId":"tower--1-foot-a","actions":["lock-decks-open"]}`
- **GPT-4.1 mini**：失败，`{"faultJointId":"drive-lock","actions":["open-gallery","remove-damaged-drive","install-drive-cartridge","calibrate-hinge","close-gallery"]}`
- **Gemini 2.5 Flash**：失败，`{"faultJointId":"drive-lock","actions":["open-gallery","remove-damaged-drive","install-drive-cartridge","close-gallery"]}`

### 有限库存替代

- **题目**：A required brace is unavailable. Which listed replacement satisfies cost, piece-count and minimum-stiffness constraints?
- **考察目标**：缺件时满足成本、数量和刚度约束的替代
- **对应能力**：有限库存、结构替代、约束满足
- **可视化**：[查看图片](images/tasks/bascule-canal-gate-inventory-substitution.png)
- **Oracle**：`{"alternativeId":"tension-cable"}`
- **Qwen3-0.6B 本地文本**：失败，`{"id":"twin-truss","label":"Two interlocked short trusses","pieces":2,"cost":6,"mass":2.2,"stiffness":11,"jointMode":"fixed"}`
- **GPT-4.1 mini**：通过，`{"alternativeId":"tension-cable"}`
- **Gemini 2.5 Flash**：通过，`{"alternativeId":"tension-cable"}`

### 动态扰动鲁棒性

- **题目**：What is the largest tested impulse that stays within the declared transient and residual displacement limits?
- **考察目标**：冲击下的最大瞬态位移和残余位移
- **对应能力**：动态物理推理、冲击鲁棒性、失效阈值估计
- **可视化**：[查看图片](images/tasks/bascule-canal-gate-dynamic-robustness.png)
- **Oracle**：`{"maxSafeImpulse":100}`
- **Qwen3-0.6B 本地文本**：失败，`{"maxSafeImpulse":300}`
- **GPT-4.1 mini**：通过，`{"maxSafeImpulse":100}`
- **Gemini 2.5 Flash**：失败，`{"maxSafeImpulse":600}`

### 功能与运动学正确性

- **题目**：Under motor actuation, does the designated revolute or prismatic mechanism achieve the required motion?
- **考察目标**：铰链、滑轨、转台或旋翼能否完成目标运动
- **对应能力**：关节语义、功能预测、运动学推理
- **可视化**：[查看图片](images/tasks/bascule-canal-gate-functional-kinematics.png)
- **Oracle**：`{"jointId":"west-deck-hinge","reachesTarget":false}`
- **Qwen3-0.6B 本地文本**：失败，`null`
- **GPT-4.1 mini**：失败，`{"jointId":"west-deck-hinge","reachesTarget":true}`
- **Gemini 2.5 Flash**：失败，`{"jointId":"west-deck-hinge","reachesTarget":true}`

### 主动检查与澄清

- **题目**：Which inspection should be requested next to maximize expected information gain per unit cost?
- **考察目标**：选择单位成本信息增益最高的下一次检查
- **对应能力**：主动感知、信息增益、成本敏感澄清
- **可视化**：[查看图片](images/tasks/bascule-canal-gate-active-inspection.png)
- **Oracle**：`{"queryIds":["bridge-brace"]}`
- **Qwen3-0.6B 本地文本**：失败，`{"queryId":"bridge-probe"}`
- **GPT-4.1 mini**：通过，`{"queryId":"bridge-brace"}`
- **Gemini 2.5 Flash**：通过，`{"queryId":"bridge-brace"}`

### 多目标工程权衡

- **题目**：Return every non-dominated buildable alternative under lower cost, lower mass and higher stiffness.
- **考察目标**：识别成本、质量、刚度之间的 Pareto 解
- **对应能力**：Pareto 推理、成本-质量-刚度权衡、工程设计
- **可视化**：[查看图片](images/tasks/bascule-canal-gate-multiobjective-design.png)
- **Oracle**：`{"paretoIds":["tension-cable","twin-truss"]}`
- **Qwen3-0.6B 本地文本**：失败，`{"paretoIds":["carbon-beam","twin-truss","tension-cable","decorative-panel"]}`
- **GPT-4.1 mini**：通过，`{"paretoIds":["tension-cable","twin-truss"]}`
- **Gemini 2.5 Flash**：通过，`{"paretoIds":["tension-cable","twin-truss"]}`

## 自适应射电观测站 / Adaptive Radio Observatory

A terraced observatory with rotating segmented dome, elevation telescope and removable cryogenic camera.

- 可视零件：92
- 刚体模块：4
- 物理关节：3

### 全过程前缀动力学

- **题目**：Which candidate module order remains dynamically supported at every prefix, and where does the other first fail?
- **考察目标**：逐步装配时是否出现坠落、失稳或错误依赖
- **对应能力**：长程规划、前缀动力学、因果支撑
- **可视化**：[查看图片](images/tasks/adaptive-radio-observatory-prefix-dynamics.png)
- **Oracle**：`{"validPlanId":"plan-a","invalidPlanFirstFailure":0}`
- **Qwen3-0.6B 本地文本**：失败，`{"validPlanId":"plan-b","invalidPlanFirstFailure":1}`
- **GPT-4.1 mini**：失败，`{"validPlanId":"plan-a","invalidPlanFirstFailure":1}`
- **Gemini 2.5 Flash**：通过，`{"validPlanId":"plan-a","invalidPlanFirstFailure":0}`

### 连续路径可达性

- **题目**：Which proposed swept-volume paths let the declared service tool reach the target interface without collision?
- **考察目标**：工具或零件的扫掠体能否无碰撞到达维修界面
- **对应能力**：连续碰撞检测、装配可达性、维修规划
- **可视化**：[查看图片](images/tasks/adaptive-radio-observatory-insertion-access.png)
- **Oracle**：`{"accessiblePathIds":["optical-axis","dome-slot"]}`
- **Qwen3-0.6B 本地文本**：失败，`{"accessiblePathIds":["optical-axis","dome-slot","service-door"]}`
- **GPT-4.1 mini**：通过，`{"accessiblePathIds":["optical-axis","dome-slot"]}`
- **Gemini 2.5 Flash**：通过，`{"accessiblePathIds":["optical-axis","dome-slot"]}`

### 故障诊断与最小返工

- **题目**：Identify the failed joint from the measured displacement and return the minimum certified recovery action sequence.
- **考察目标**：从动力学后果定位故障关节并给出最小维修
- **对应能力**：故障定位、因果诊断、最小返工
- **可视化**：[查看图片](images/tasks/adaptive-radio-observatory-fault-recovery.png)
- **Oracle**：`{"faultJointId":"camera-bayonet","actions":["park-telescope","open-dome-slit","remove-camera","clean-bayonet","install-camera","recalibrate-optics"]}`
- **Qwen3-0.6B 本地文本**：失败，`{"faultJointId":"dome-ring","actions":["remove-camera","clean-bayonet","install-camera","recalibrate-optics"]}`
- **GPT-4.1 mini**：失败，`{"faultJointId":"camera-bayonet","actions":["remove-camera","clean-bayonet","install-camera"]}`
- **Gemini 2.5 Flash**：失败，`{"faultJointId":"camera-bayonet","actions":["park-telescope","remove-camera","clean-bayonet","install-camera","recalibrate-optics"]}`

### 有限库存替代

- **题目**：A required brace is unavailable. Which listed replacement satisfies cost, piece-count and minimum-stiffness constraints?
- **考察目标**：缺件时满足成本、数量和刚度约束的替代
- **对应能力**：有限库存、结构替代、约束满足
- **可视化**：[查看图片](images/tasks/adaptive-radio-observatory-inventory-substitution.png)
- **Oracle**：`{"alternativeId":"carbon-beam"}`
- **Qwen3-0.6B 本地文本**：失败，`null`
- **GPT-4.1 mini**：通过，`{"alternativeId":"carbon-beam"}`
- **Gemini 2.5 Flash**：通过，`{"alternativeId":"carbon-beam"}`

### 动态扰动鲁棒性

- **题目**：What is the largest tested impulse that stays within the declared transient and residual displacement limits?
- **考察目标**：冲击下的最大瞬态位移和残余位移
- **对应能力**：动态物理推理、冲击鲁棒性、失效阈值估计
- **可视化**：[查看图片](images/tasks/adaptive-radio-observatory-dynamic-robustness.png)
- **Oracle**：`{"maxSafeImpulse":100}`
- **Qwen3-0.6B 本地文本**：失败，`{"maxSafeImpulse":2000}`
- **GPT-4.1 mini**：通过，`{"maxSafeImpulse":100}`
- **Gemini 2.5 Flash**：失败，`{"maxSafeImpulse":500}`

### 功能与运动学正确性

- **题目**：Under motor actuation, does the designated revolute or prismatic mechanism achieve the required motion?
- **考察目标**：铰链、滑轨、转台或旋翼能否完成目标运动
- **对应能力**：关节语义、功能预测、运动学推理
- **可视化**：[查看图片](images/tasks/adaptive-radio-observatory-functional-kinematics.png)
- **Oracle**：`{"jointId":"elevation-axis","reachesTarget":false}`
- **Qwen3-0.6B 本地文本**：失败，`{"id":"m1-adaptive-radio-observatory-functional-kinematics","kind":"functional-kinematics","capability":["joint semantics","functional prediction","kinematic reasoning"],"question":"Under motor actuation, does the designated revolute or prismatic mechanism achieve the required motion?","responseSchema":{"jointId":"string","reachesTarget":"boolean"}}`
- **GPT-4.1 mini**：失败，`{"jointId":"elevation-axis","reachesTarget":true}`
- **Gemini 2.5 Flash**：失败，`{"jointId":"elevation-axis","reachesTarget":true}`

### 主动检查与澄清

- **题目**：Which inspection should be requested next to maximize expected information gain per unit cost?
- **考察目标**：选择单位成本信息增益最高的下一次检查
- **对应能力**：主动感知、信息增益、成本敏感澄清
- **可视化**：[查看图片](images/tasks/adaptive-radio-observatory-active-inspection.png)
- **Oracle**：`{"queryIds":["observatory-marker"]}`
- **Qwen3-0.6B 本地文本**：失败，`{"queryId":"observatory-probe"}`
- **GPT-4.1 mini**：失败，`{"queryId":"observatory-brace"}`
- **Gemini 2.5 Flash**：失败，`{"queryId":"observatory-brace"}`

### 多目标工程权衡

- **题目**：Return every non-dominated buildable alternative under lower cost, lower mass and higher stiffness.
- **考察目标**：识别成本、质量、刚度之间的 Pareto 解
- **对应能力**：Pareto 推理、成本-质量-刚度权衡、工程设计
- **可视化**：[查看图片](images/tasks/adaptive-radio-observatory-multiobjective-design.png)
- **Oracle**：`{"paretoIds":["carbon-beam","tension-cable"]}`
- **Qwen3-0.6B 本地文本**：失败，`{"paretoIds":["carbon-beam","twin-truss","decorative-panel"]}`
- **GPT-4.1 mini**：失败，`{"paretoIds":["decorative-panel","tension-cable","carbon-beam"]}`
- **Gemini 2.5 Flash**：通过，`{"paretoIds":["carbon-beam","tension-cable"]}`

## 山火救援倾转旋翼机 / Wildfire Tiltrotor

A twin-rotor firefighting aircraft with tilting nacelles, removable water tank and serviceable drivetrain.

- 可视零件：43
- 刚体模块：6
- 物理关节：5

### 全过程前缀动力学

- **题目**：Which candidate module order remains dynamically supported at every prefix, and where does the other first fail?
- **考察目标**：逐步装配时是否出现坠落、失稳或错误依赖
- **对应能力**：长程规划、前缀动力学、因果支撑
- **可视化**：[查看图片](images/tasks/wildfire-tiltrotor-prefix-dynamics.png)
- **Oracle**：`{"validPlanId":"plan-a","invalidPlanFirstFailure":0}`
- **Qwen3-0.6B 本地文本**：失败，`{"validPlanId":"plan-b","invalidPlanFirstFailure":1}`
- **GPT-4.1 mini**：通过，`{"validPlanId":"plan-a","invalidPlanFirstFailure":0}`
- **Gemini 2.5 Flash**：通过，`{"validPlanId":"plan-a","invalidPlanFirstFailure":0}`

### 连续路径可达性

- **题目**：Which proposed swept-volume paths let the declared service tool reach the target interface without collision?
- **考察目标**：工具或零件的扫掠体能否无碰撞到达维修界面
- **对应能力**：连续碰撞检测、装配可达性、维修规划
- **可视化**：[查看图片](images/tasks/wildfire-tiltrotor-insertion-access.png)
- **Oracle**：`{"accessiblePathIds":["belly-lift"]}`
- **Qwen3-0.6B 本地文本**：失败，`{"accessiblePathIds":["belly-lift","rear-ramp","side-door"]}`
- **GPT-4.1 mini**：通过，`{"accessiblePathIds":["belly-lift"]}`
- **Gemini 2.5 Flash**：通过，`{"accessiblePathIds":["belly-lift"]}`

### 故障诊断与最小返工

- **题目**：Identify the failed joint from the measured displacement and return the minimum certified recovery action sequence.
- **考察目标**：从动力学后果定位故障关节并给出最小维修
- **对应能力**：故障定位、因果诊断、最小返工
- **可视化**：[查看图片](images/tasks/wildfire-tiltrotor-fault-recovery.png)
- **Oracle**：`{"faultJointId":"tank-latch","actions":["secure-airframe","open-belly-panel","lower-tank","replace-latch","raise-tank","close-belly-panel"]}`
- **Qwen3-0.6B 本地文本**：失败，`{"faultJointId":"nacelle-left-tilt","actions":["lower-tank","secure-airframe"]}`
- **GPT-4.1 mini**：失败，`{"faultJointId":"tank-latch","actions":["open-belly-panel","lower-tank","replace-latch","raise-tank","close-belly-panel"]}`
- **Gemini 2.5 Flash**：通过，`{"faultJointId":"tank-latch","actions":["secure-airframe","open-belly-panel","lower-tank","replace-latch","raise-tank","close-belly-panel"]}`

### 有限库存替代

- **题目**：A required brace is unavailable. Which listed replacement satisfies cost, piece-count and minimum-stiffness constraints?
- **考察目标**：缺件时满足成本、数量和刚度约束的替代
- **对应能力**：有限库存、结构替代、约束满足
- **可视化**：[查看图片](images/tasks/wildfire-tiltrotor-inventory-substitution.png)
- **Oracle**：`{"alternativeId":"twin-truss"}`
- **Qwen3-0.6B 本地文本**：失败，`{"id":"carbon-beam","label":"One long carbon beam","pieces":1,"cost":7,"mass":1.8,"stiffness":9,"jointMode":"fixed"}`
- **GPT-4.1 mini**：通过，`{"alternativeId":"twin-truss"}`
- **Gemini 2.5 Flash**：通过，`{"alternativeId":"twin-truss"}`

### 动态扰动鲁棒性

- **题目**：What is the largest tested impulse that stays within the declared transient and residual displacement limits?
- **考察目标**：冲击下的最大瞬态位移和残余位移
- **对应能力**：动态物理推理、冲击鲁棒性、失效阈值估计
- **可视化**：[查看图片](images/tasks/wildfire-tiltrotor-dynamic-robustness.png)
- **Oracle**：`{"maxSafeImpulse":2}`
- **Qwen3-0.6B 本地文本**：失败，`{"maxSafeImpulse":20}`
- **GPT-4.1 mini**：失败，`{"maxSafeImpulse":8}`
- **Gemini 2.5 Flash**：失败，`{"maxSafeImpulse":20}`

### 功能与运动学正确性

- **题目**：Under motor actuation, does the designated revolute or prismatic mechanism achieve the required motion?
- **考察目标**：铰链、滑轨、转台或旋翼能否完成目标运动
- **对应能力**：关节语义、功能预测、运动学推理
- **可视化**：[查看图片](images/tasks/wildfire-tiltrotor-functional-kinematics.png)
- **Oracle**：`{"jointId":"nacelle-left-tilt","reachesTarget":true}`
- **Qwen3-0.6B 本地文本**：失败，`null`
- **GPT-4.1 mini**：通过，`{"jointId":"nacelle-left-tilt","reachesTarget":true}`
- **Gemini 2.5 Flash**：通过，`{"jointId":"nacelle-left-tilt","reachesTarget":true}`

### 主动检查与澄清

- **题目**：Which inspection should be requested next to maximize expected information gain per unit cost?
- **考察目标**：选择单位成本信息增益最高的下一次检查
- **对应能力**：主动感知、信息增益、成本敏感澄清
- **可视化**：[查看图片](images/tasks/wildfire-tiltrotor-active-inspection.png)
- **Oracle**：`{"queryIds":["tiltrotor-probe"]}`
- **Qwen3-0.6B 本地文本**：通过，`{"queryId":"tiltrotor-probe"}`
- **GPT-4.1 mini**：通过，`{"queryId":"tiltrotor-probe"}`
- **Gemini 2.5 Flash**：通过，`{"queryId":"tiltrotor-probe"}`

### 多目标工程权衡

- **题目**：Return every non-dominated buildable alternative under lower cost, lower mass and higher stiffness.
- **考察目标**：识别成本、质量、刚度之间的 Pareto 解
- **对应能力**：Pareto 推理、成本-质量-刚度权衡、工程设计
- **可视化**：[查看图片](images/tasks/wildfire-tiltrotor-multiobjective-design.png)
- **Oracle**：`{"paretoIds":["tension-cable","twin-truss"]}`
- **Qwen3-0.6B 本地文本**：失败，`{"paretoIds":["carbon-beam","twin-truss","tension-cable","decorative-panel"]}`
- **GPT-4.1 mini**：失败，`{"paretoIds":["twin-truss","carbon-beam"]}`
- **Gemini 2.5 Flash**：通过，`{"paretoIds":["twin-truss","tension-cable"]}`

## 极地科研站 / Polar Research Station

An elevated insulated station with pressure airlock, sliding solar array and serviceable wind turbine.

- 可视零件：66
- 刚体模块：5
- 物理关节：4

### 全过程前缀动力学

- **题目**：Which candidate module order remains dynamically supported at every prefix, and where does the other first fail?
- **考察目标**：逐步装配时是否出现坠落、失稳或错误依赖
- **对应能力**：长程规划、前缀动力学、因果支撑
- **可视化**：[查看图片](images/tasks/polar-research-station-prefix-dynamics.png)
- **Oracle**：`{"validPlanId":"plan-a","invalidPlanFirstFailure":0}`
- **Qwen3-0.6B 本地文本**：失败，`{"validPlanId":"plan-b","invalidPlanFirstFailure":1}`
- **GPT-4.1 mini**：通过，`{"validPlanId":"plan-a","invalidPlanFirstFailure":0}`
- **Gemini 2.5 Flash**：通过，`{"validPlanId":"plan-a","invalidPlanFirstFailure":0}`

### 连续路径可达性

- **题目**：Which proposed swept-volume paths let the declared service tool reach the target interface without collision?
- **考察目标**：工具或零件的扫掠体能否无碰撞到达维修界面
- **对应能力**：连续碰撞检测、装配可达性、维修规划
- **可视化**：[查看图片](images/tasks/polar-research-station-insertion-access.png)
- **Oracle**：`{"accessiblePathIds":["outside-swing"]}`
- **Qwen3-0.6B 本地文本**：失败，`{"accessiblePathIds":["outside-swing","interior-slide"]}`
- **GPT-4.1 mini**：失败，`{"accessiblePathIds":["outside-swing","roof-drop"]}`
- **Gemini 2.5 Flash**：通过，`{"accessiblePathIds":["outside-swing"]}`

### 故障诊断与最小返工

- **题目**：Identify the failed joint from the measured displacement and return the minimum certified recovery action sequence.
- **考察目标**：从动力学后果定位故障关节并给出最小维修
- **对应能力**：故障定位、因果诊断、最小返工
- **可视化**：[查看图片](images/tasks/polar-research-station-fault-recovery.png)
- **Oracle**：`{"faultJointId":"mast-foot","actions":["feather-rotor","lock-mast","replace-foot-brace","release-mast","spin-test"]}`
- **Qwen3-0.6B 本地文本**：失败，`{"faultJointId":"rotor-shaft","actions":["replace-foot-brace"]}`
- **GPT-4.1 mini**：失败，`{"faultJointId":"mast-foot","actions":["replace-foot-brace","lock-mast"]}`
- **Gemini 2.5 Flash**：失败，`{"faultJointId":"mast-foot","actions":["lock-mast","replace-foot-brace","release-mast","spin-test"]}`

### 有限库存替代

- **题目**：A required brace is unavailable. Which listed replacement satisfies cost, piece-count and minimum-stiffness constraints?
- **考察目标**：缺件时满足成本、数量和刚度约束的替代
- **对应能力**：有限库存、结构替代、约束满足
- **可视化**：[查看图片](images/tasks/polar-research-station-inventory-substitution.png)
- **Oracle**：`{"alternativeId":"tension-cable"}`
- **Qwen3-0.6B 本地文本**：失败，`{"id":"twin-truss","label":"Two interlocked short trusses","pieces":2,"cost":6,"mass":2.2,"stiffness":11,"jointMode":"fixed"}`
- **GPT-4.1 mini**：通过，`{"alternativeId":"tension-cable"}`
- **Gemini 2.5 Flash**：通过，`{"alternativeId":"tension-cable"}`

### 动态扰动鲁棒性

- **题目**：What is the largest tested impulse that stays within the declared transient and residual displacement limits?
- **考察目标**：冲击下的最大瞬态位移和残余位移
- **对应能力**：动态物理推理、冲击鲁棒性、失效阈值估计
- **可视化**：[查看图片](images/tasks/polar-research-station-dynamic-robustness.png)
- **Oracle**：`{"maxSafeImpulse":10}`
- **Qwen3-0.6B 本地文本**：失败，`{"maxSafeImpulse":20}`
- **GPT-4.1 mini**：通过，`{"maxSafeImpulse":10}`
- **Gemini 2.5 Flash**：通过，`{"maxSafeImpulse":10}`

### 功能与运动学正确性

- **题目**：Under motor actuation, does the designated revolute or prismatic mechanism achieve the required motion?
- **考察目标**：铰链、滑轨、转台或旋翼能否完成目标运动
- **对应能力**：关节语义、功能预测、运动学推理
- **可视化**：[查看图片](images/tasks/polar-research-station-functional-kinematics.png)
- **Oracle**：`{"jointId":"solar-rail","reachesTarget":true}`
- **Qwen3-0.6B 本地文本**：失败，`{"id":"solar-rail","reachesTarget":true}`
- **GPT-4.1 mini**：通过，`{"jointId":"solar-rail","reachesTarget":true}`
- **Gemini 2.5 Flash**：通过，`{"jointId":"solar-rail","reachesTarget":true}`

### 主动检查与澄清

- **题目**：Which inspection should be requested next to maximize expected information gain per unit cost?
- **考察目标**：选择单位成本信息增益最高的下一次检查
- **对应能力**：主动感知、信息增益、成本敏感澄清
- **可视化**：[查看图片](images/tasks/polar-research-station-active-inspection.png)
- **Oracle**：`{"queryIds":["station-brace"]}`
- **Qwen3-0.6B 本地文本**：失败，`{"queryId":"station-probe"}`
- **GPT-4.1 mini**：通过，`{"queryId":"station-brace"}`
- **Gemini 2.5 Flash**：通过，`{"queryId":"station-brace"}`

### 多目标工程权衡

- **题目**：Return every non-dominated buildable alternative under lower cost, lower mass and higher stiffness.
- **考察目标**：识别成本、质量、刚度之间的 Pareto 解
- **对应能力**：Pareto 推理、成本-质量-刚度权衡、工程设计
- **可视化**：[查看图片](images/tasks/polar-research-station-multiobjective-design.png)
- **Oracle**：`{"paretoIds":["tension-cable"]}`
- **Qwen3-0.6B 本地文本**：失败，`{"paretoIds":["carbon-beam","twin-truss"]}`
- **GPT-4.1 mini**：失败，`{"paretoIds":["tension-cable","twin-truss"]}`
- **Gemini 2.5 Flash**：失败，`{"paretoIds":["tension-cable","twin-truss"]}`
