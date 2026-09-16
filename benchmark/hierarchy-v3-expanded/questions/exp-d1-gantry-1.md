## D1 龙门巡检滑台

### 模块识别（h3-exp-d1-gantry-1-identify）

高亮的维修模块对应哪个 ID？

能力：模块识别；形式：single-choice；证据：model-state。

- A：cell-0-probe-0
- B：foundation
- C：cell-0-mount
- D：cell-0-overhead

```json
{
  "input": {
    "moduleNames": [
      {
        "id": "foundation",
        "name": "foundation"
      },
      {
        "id": "cell-0-mount",
        "name": "cell 0 mount"
      },
      {
        "id": "cell-0-overhead",
        "name": "cell 0 overhead"
      },
      {
        "id": "cell-0-trolley-0",
        "name": "cell 0 trolley 0"
      },
      {
        "id": "cell-0-probe-0",
        "name": "cell 0 probe 0"
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 部件计数（h3-exp-d1-gantry-1-count）

模块 cell-0-probe-0 有多少个可视零件？

能力：部件计数；形式：single-choice；证据：model-state。

- A：4
- B：5
- C：3
- D：7

```json
{
  "input": {
    "parts": [
      {
        "id": "foundation-p0",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p1",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p2",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p3",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p4",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p5",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p6",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p7",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p8",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p9",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p10",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p11",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p12",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p13",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p14",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p15",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p16",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p17",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p18",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p19",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p20",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p21",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p22",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p23",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p24",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p25",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p26",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p27",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p28",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p29",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p30",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p31",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p32",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p33",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p34",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p35",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p36",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p37",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p38",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p39",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p40",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p41",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p42",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p43",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p44",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p45",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p46",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p47",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p48",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p49",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p50",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p51",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p52",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p53",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p54",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p55",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p56",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p57",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p58",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p59",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p60",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p61",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p62",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p63",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p64",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p65",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p66",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p67",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p68",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p69",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p70",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p71",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p72",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p73",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p74",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p75",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p76",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p77",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p78",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p79",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p80",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p81",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p82",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p83",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p84",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-mount-p85",
        "moduleId": "cell-0-mount",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "cell-0-overhead-p86",
        "moduleId": "cell-0-overhead",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-overhead-p87",
        "moduleId": "cell-0-overhead",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-overhead-p88",
        "moduleId": "cell-0-overhead",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-overhead-p89",
        "moduleId": "cell-0-overhead",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-overhead-p90",
        "moduleId": "cell-0-overhead",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-overhead-p91",
        "moduleId": "cell-0-overhead",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-overhead-p92",
        "moduleId": "cell-0-overhead",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-overhead-p93",
        "moduleId": "cell-0-overhead",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-overhead-p94",
        "moduleId": "cell-0-overhead",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-overhead-p95",
        "moduleId": "cell-0-overhead",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-overhead-p96",
        "moduleId": "cell-0-overhead",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-overhead-p97",
        "moduleId": "cell-0-overhead",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-overhead-p98",
        "moduleId": "cell-0-overhead",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-overhead-p99",
        "moduleId": "cell-0-overhead",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-overhead-p100",
        "moduleId": "cell-0-overhead",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-overhead-p101",
        "moduleId": "cell-0-overhead",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-trolley-0-p102",
        "moduleId": "cell-0-trolley-0",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-trolley-0-p103",
        "moduleId": "cell-0-trolley-0",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-trolley-0-p104",
        "moduleId": "cell-0-trolley-0",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-trolley-0-p105",
        "moduleId": "cell-0-trolley-0",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-probe-0-p106",
        "moduleId": "cell-0-probe-0",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-probe-0-p107",
        "moduleId": "cell-0-probe-0",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-probe-0-p108",
        "moduleId": "cell-0-probe-0",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-probe-0-p109",
        "moduleId": "cell-0-probe-0",
        "shape": "sphere",
        "color": "#45a080"
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 颜色识别（h3-exp-d1-gantry-1-color）

零件 cell-0-probe-0-p106 的颜色值是什么？

能力：颜色识别；形式：single-choice；证据：model-state。

- A：#2878b8
- B：#d43a32
- C：#f2bf3c
- D：#dfebed

```json
{
  "input": {
    "part": {
      "id": "cell-0-probe-0-p106",
      "moduleId": "cell-0-probe-0",
      "shape": "beam",
      "position": [
        0,
        -0.4249999999999997,
        0
      ],
      "size": [
        0.18,
        0.7000000000000001,
        0.18
      ],
      "color": "#dfebed",
      "rotation": [
        0,
        0,
        0,
        1
      ]
    }
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 三维位置（h3-exp-d1-gantry-1-position）

模块 cell-0-probe-0 的世界包围盒中心是什么？

能力：三维位置；形式：single-choice；证据：model-state。

- A：[0,3.7249999999999996,0.9]
- B：[0,0.2,0]
- C：[0,0.7,0]
- D：[0,3.3374999999999995,0]

```json
{
  "input": {
    "centers": {
      "foundation": [
        0,
        0.2,
        0
      ],
      "cell-0-mount": [
        0,
        0.7,
        0
      ],
      "cell-0-overhead": [
        0,
        3.3374999999999995,
        0
      ],
      "cell-0-trolley-0": [
        0,
        5.9,
        0
      ],
      "cell-0-probe-0": [
        0,
        3.7249999999999996,
        0.9
      ]
    }
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 关节类型（h3-exp-d1-gantry-1-joint-type）

cell-0-trolley-0-joint 采用什么约束类型？

能力：关节类型；形式：single-choice；证据：model-state。

- A：prismatic
- B：fixed
- C：revolute
- D：spring

```json
{
  "input": {
    "joint": {
      "id": "cell-0-trolley-0-joint",
      "name": "cell-0-trolley-0 interface",
      "parent": "cell-0-overhead",
      "child": "cell-0-trolley-0",
      "type": "prismatic",
      "anchorParent": [
        0,
        2.5125000000000015,
        0
      ],
      "anchorChild": [
        0,
        -0.04999999999999982,
        0
      ],
      "axis": [
        1,
        0,
        0
      ],
      "limits": [
        -0.45,
        0.45
      ]
    }
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 直接连接（h3-exp-d1-gantry-1-parent）

cell-0-probe-0 的直接父模块集合是什么？

能力：直接连接；形式：single-choice；证据：model-state。

- A：[]
- B：["foundation","cell-0-mount","cell-0-overhead","cell-0-trolley-0","cell-0-probe-0"]
- C：["cell-0-trolley-0"]
- D：["cell-0-probe-0"]

```json
{
  "input": {
    "joints": [
      {
        "id": "cell-0-mount-joint",
        "name": "cell-0-mount interface",
        "parent": "foundation",
        "child": "cell-0-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          0,
          -0.04999999999999993,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-overhead-joint",
        "name": "cell-0-overhead interface",
        "parent": "cell-0-mount",
        "child": "cell-0-overhead",
        "type": "fixed",
        "anchorParent": [
          0,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          0,
          -2.1874999999999996,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-trolley-0-joint",
        "name": "cell-0-trolley-0 interface",
        "parent": "cell-0-overhead",
        "child": "cell-0-trolley-0",
        "type": "prismatic",
        "anchorParent": [
          0,
          2.5125000000000015,
          0
        ],
        "anchorChild": [
          0,
          -0.04999999999999982,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-probe-0-joint",
        "name": "cell-0-probe-0 interface",
        "parent": "cell-0-trolley-0",
        "child": "cell-0-probe-0",
        "type": "prismatic",
        "anchorParent": [
          0,
          -1.6500000000000004,
          0.9
        ],
        "anchorChild": [
          0,
          0.5250000000000004,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 基座识别（h3-exp-d1-gantry-1-anchor）

哪些模块被声明为固定基座？

能力：基座识别；形式：single-choice；证据：model-state。

- A：["foundation"]
- B：[]
- C：["foundation","cell-0-mount","cell-0-overhead","cell-0-trolley-0","cell-0-probe-0"]
- D：["cell-0-probe-0"]

```json
{
  "input": {
    "modules": [
      {
        "id": "foundation",
        "name": "foundation",
        "role": "foundation",
        "anchored": true,
        "mass": 30,
        "position": [
          0,
          0.2,
          0
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-0-mount",
        "name": "cell 0 mount",
        "role": "structure",
        "anchored": false,
        "mass": 1.2,
        "position": [
          0,
          0.7,
          0
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-0-overhead",
        "name": "cell 0 overhead",
        "role": "structure",
        "anchored": false,
        "mass": 1.2,
        "position": [
          0,
          3.3374999999999995,
          0
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-0-trolley-0",
        "name": "cell 0 trolley 0",
        "role": "actuator",
        "anchored": false,
        "mass": 1.2,
        "position": [
          0,
          5.9,
          0
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-0-probe-0",
        "name": "cell 0 probe 0",
        "role": "actuator",
        "anchored": false,
        "mass": 0.3,
        "position": [
          0,
          3.7249999999999996,
          0.9
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 接口计数（h3-exp-d1-gantry-1-degree）

cell-0-probe-0 连接几个声明关节？平行关节分别计数。

能力：接口计数；形式：single-choice；证据：model-state。

- A：0
- B：3
- C：1
- D：2

```json
{
  "input": {
    "joints": [
      {
        "id": "cell-0-mount-joint",
        "name": "cell-0-mount interface",
        "parent": "foundation",
        "child": "cell-0-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          0,
          -0.04999999999999993,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-overhead-joint",
        "name": "cell-0-overhead interface",
        "parent": "cell-0-mount",
        "child": "cell-0-overhead",
        "type": "fixed",
        "anchorParent": [
          0,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          0,
          -2.1874999999999996,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-trolley-0-joint",
        "name": "cell-0-trolley-0 interface",
        "parent": "cell-0-overhead",
        "child": "cell-0-trolley-0",
        "type": "prismatic",
        "anchorParent": [
          0,
          2.5125000000000015,
          0
        ],
        "anchorChild": [
          0,
          -0.04999999999999982,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-probe-0-joint",
        "name": "cell-0-probe-0 interface",
        "parent": "cell-0-trolley-0",
        "child": "cell-0-probe-0",
        "type": "prismatic",
        "anchorParent": [
          0,
          -1.6500000000000004,
          0.9
        ],
        "anchorChild": [
          0,
          0.5250000000000004,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 局部改色（h3-exp-d1-gantry-1-recolor）

仅将 cell-0-probe-0-p106 改成 #e8792e，其他零件不变。选择正确补丁。

能力：局部改色；形式：single-choice；证据：model-state。

- A：{"id":"*","color":"#e8792e"}
- B：{"id":"cell-0-probe-0-p106","color":"#e8792e"}
- C：{"id":"cell-0-probe-0-p107","color":"#e8792e"}
- D：{"id":"cell-0-probe-0-p106","color":"#2878b8"}

```json
{
  "input": {
    "part": {
      "id": "cell-0-probe-0-p106",
      "moduleId": "cell-0-probe-0",
      "shape": "beam",
      "position": [
        0,
        -0.4249999999999997,
        0
      ],
      "size": [
        0.18,
        0.7000000000000001,
        0.18
      ],
      "color": "#dfebed",
      "rotation": [
        0,
        0,
        0,
        1
      ]
    }
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 补装部件（h3-exp-d1-gantry-1-add）

模块 cell-0-probe-0 缺失零件 cell-0-probe-0-p106。选择与目标清单一致的补装描述。

能力：补装部件；形式：single-choice；证据：model-state。

- A：{"id":"cell-0-probe-0-p106","moduleId":"cell-0-probe-0","shape":"beam","position":[0,-0.4249999999999997,0],"size":[3,3,3],"color":"#dfebed","rotation":[0,0,0,1]}
- B：{"id":"cell-0-probe-0-p106","moduleId":"cell-0-probe-0","shape":"beam","position":[0,-0.4249999999999997,0],"size":[0.18,0.7000000000000001,0.18],"color":"#000000","rotation":[0,0,0,1]}
- C：{"id":"cell-0-probe-0-p106","moduleId":"cell-0-probe-0","shape":"beam","position":[0,-0.4249999999999997,0],"size":[0.18,0.7000000000000001,0.18],"color":"#dfebed","rotation":[0,0,0,1]}
- D：{"id":"cell-0-probe-0-p106","moduleId":"foundation","shape":"beam","position":[0,-0.4249999999999997,0],"size":[0.18,0.7000000000000001,0.18],"color":"#dfebed","rotation":[0,0,0,1]}

```json
{
  "input": {
    "targetPart": {
      "id": "cell-0-probe-0-p106",
      "moduleId": "cell-0-probe-0",
      "shape": "beam",
      "position": [
        0,
        -0.4249999999999997,
        0
      ],
      "size": [
        0.18,
        0.7000000000000001,
        0.18
      ],
      "color": "#dfebed",
      "rotation": [
        0,
        0,
        0,
        1
      ]
    },
    "existingIds": [
      "foundation-p0",
      "foundation-p1",
      "foundation-p2",
      "foundation-p3",
      "foundation-p4",
      "foundation-p5",
      "foundation-p6",
      "foundation-p7",
      "foundation-p8",
      "foundation-p9",
      "foundation-p10",
      "foundation-p11",
      "foundation-p12",
      "foundation-p13",
      "foundation-p14",
      "foundation-p15",
      "foundation-p16",
      "foundation-p17",
      "foundation-p18",
      "foundation-p19",
      "foundation-p20",
      "foundation-p21",
      "foundation-p22",
      "foundation-p23",
      "foundation-p24",
      "foundation-p25",
      "foundation-p26",
      "foundation-p27",
      "foundation-p28",
      "foundation-p29",
      "foundation-p30",
      "foundation-p31",
      "foundation-p32",
      "foundation-p33",
      "foundation-p34",
      "foundation-p35",
      "foundation-p36",
      "foundation-p37",
      "foundation-p38",
      "foundation-p39",
      "foundation-p40",
      "foundation-p41",
      "foundation-p42",
      "foundation-p43",
      "foundation-p44",
      "foundation-p45",
      "foundation-p46",
      "foundation-p47",
      "foundation-p48",
      "foundation-p49",
      "foundation-p50",
      "foundation-p51",
      "foundation-p52",
      "foundation-p53",
      "foundation-p54",
      "foundation-p55",
      "cell-0-mount-p56",
      "cell-0-mount-p57",
      "cell-0-mount-p58",
      "cell-0-mount-p59",
      "cell-0-mount-p60",
      "cell-0-mount-p61",
      "cell-0-mount-p62",
      "cell-0-mount-p63",
      "cell-0-mount-p64",
      "cell-0-mount-p65",
      "cell-0-mount-p66",
      "cell-0-mount-p67",
      "cell-0-mount-p68",
      "cell-0-mount-p69",
      "cell-0-mount-p70",
      "cell-0-mount-p71",
      "cell-0-mount-p72",
      "cell-0-mount-p73",
      "cell-0-mount-p74",
      "cell-0-mount-p75",
      "cell-0-mount-p76",
      "cell-0-mount-p77",
      "cell-0-mount-p78",
      "cell-0-mount-p79",
      "cell-0-mount-p80",
      "cell-0-mount-p81",
      "cell-0-mount-p82",
      "cell-0-mount-p83",
      "cell-0-mount-p84",
      "cell-0-mount-p85",
      "cell-0-overhead-p86",
      "cell-0-overhead-p87",
      "cell-0-overhead-p88",
      "cell-0-overhead-p89",
      "cell-0-overhead-p90",
      "cell-0-overhead-p91",
      "cell-0-overhead-p92",
      "cell-0-overhead-p93",
      "cell-0-overhead-p94",
      "cell-0-overhead-p95",
      "cell-0-overhead-p96",
      "cell-0-overhead-p97",
      "cell-0-overhead-p98",
      "cell-0-overhead-p99",
      "cell-0-overhead-p100",
      "cell-0-overhead-p101",
      "cell-0-trolley-0-p102",
      "cell-0-trolley-0-p103",
      "cell-0-trolley-0-p104",
      "cell-0-trolley-0-p105",
      "cell-0-probe-0-p107",
      "cell-0-probe-0-p108",
      "cell-0-probe-0-p109"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 安全拆除（h3-exp-d1-gantry-1-remove）

按声明依赖图，当前可以先拆哪些叶模块？

能力：安全拆除；形式：single-choice；证据：model-state。

- A：["foundation","cell-0-mount","cell-0-overhead","cell-0-trolley-0","cell-0-probe-0"]
- B：["cell-0-probe-0"]
- C：["foundation"]
- D：[]

```json
{
  "input": {
    "joints": [
      {
        "id": "cell-0-mount-joint",
        "name": "cell-0-mount interface",
        "parent": "foundation",
        "child": "cell-0-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          0,
          -0.04999999999999993,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-overhead-joint",
        "name": "cell-0-overhead interface",
        "parent": "cell-0-mount",
        "child": "cell-0-overhead",
        "type": "fixed",
        "anchorParent": [
          0,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          0,
          -2.1874999999999996,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-trolley-0-joint",
        "name": "cell-0-trolley-0 interface",
        "parent": "cell-0-overhead",
        "child": "cell-0-trolley-0",
        "type": "prismatic",
        "anchorParent": [
          0,
          2.5125000000000015,
          0
        ],
        "anchorChild": [
          0,
          -0.04999999999999982,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-probe-0-joint",
        "name": "cell-0-probe-0 interface",
        "parent": "cell-0-trolley-0",
        "child": "cell-0-probe-0",
        "type": "prismatic",
        "anchorParent": [
          0,
          -1.6500000000000004,
          0.9
        ],
        "anchorChild": [
          0,
          0.5250000000000004,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      }
    ],
    "modules": [
      "foundation",
      "cell-0-mount",
      "cell-0-overhead",
      "cell-0-trolley-0",
      "cell-0-probe-0"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 替换选择（h3-exp-d1-gantry-1-replace）

在成本上限内选择刚度最大的替换件；并列选成本低者，再并列选ID字典序最小者。

能力：替换选择；形式：single-choice；证据：model-state。

- A：stock-3
- B：stock-1
- C：stock-0
- D：stock-2

```json
{
  "input": {
    "alternatives": [
      {
        "id": "stock-0",
        "cost": 5,
        "stiffness": 3,
        "mass": 1.2
      },
      {
        "id": "stock-1",
        "cost": 2,
        "stiffness": 7,
        "mass": 1.1
      },
      {
        "id": "stock-2",
        "cost": 5,
        "stiffness": 7,
        "mass": 1.3
      },
      {
        "id": "stock-3",
        "cost": 5,
        "stiffness": 5,
        "mass": 1.2
      }
    ],
    "maxCost": 7
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 平移纠偏（h3-exp-d1-gantry-1-translate）

观察到相对目标的平移误差 delta，选择补偿平移。

能力：平移纠偏；形式：single-choice；证据：model-state。

- A：[0,2,0]
- B：[-1,0,2]
- C：[1,0,-2]
- D：[0,0,0]

```json
{
  "input": {
    "delta": [
      1,
      0,
      -2
    ],
    "target": "cell-0-probe-0"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 姿态纠偏（h3-exp-d1-gantry-1-rotate）

选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。

能力：姿态纠偏；形式：single-choice；证据：model-state。

- A：45
- B：0
- C：90
- D：-45

```json
{
  "input": {
    "module": "cell-0-probe-0",
    "currentYaw": 180,
    "targetYaw": 135
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 下一步放置（h3-exp-d1-gantry-1-next-module）

已完成给定前缀，选择所有前置依赖已满足的下一模块集合。

能力：下一步放置；形式：single-choice；证据：model-state。

- A：["cell-0-trolley-0","cell-0-probe-0"]
- B：["cell-0-trolley-0"]
- C：[]
- D：["foundation","cell-0-mount","cell-0-overhead"]

```json
{
  "input": {
    "prefix": [
      "foundation",
      "cell-0-mount",
      "cell-0-overhead"
    ],
    "joints": [
      {
        "id": "cell-0-mount-joint",
        "name": "cell-0-mount interface",
        "parent": "foundation",
        "child": "cell-0-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          0,
          -0.04999999999999993,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-overhead-joint",
        "name": "cell-0-overhead interface",
        "parent": "cell-0-mount",
        "child": "cell-0-overhead",
        "type": "fixed",
        "anchorParent": [
          0,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          0,
          -2.1874999999999996,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-trolley-0-joint",
        "name": "cell-0-trolley-0 interface",
        "parent": "cell-0-overhead",
        "child": "cell-0-trolley-0",
        "type": "prismatic",
        "anchorParent": [
          0,
          2.5125000000000015,
          0
        ],
        "anchorChild": [
          0,
          -0.04999999999999982,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-probe-0-joint",
        "name": "cell-0-probe-0 interface",
        "parent": "cell-0-trolley-0",
        "child": "cell-0-probe-0",
        "type": "prismatic",
        "anchorParent": [
          0,
          -1.6500000000000004,
          0.9
        ],
        "anchorChild": [
          0,
          0.5250000000000004,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      }
    ],
    "modules": [
      "foundation",
      "cell-0-mount",
      "cell-0-overhead",
      "cell-0-trolley-0",
      "cell-0-probe-0"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 库存核算（h3-exp-d1-gantry-1-inventory）

备件库有 11 件，替换模块需 4 件，还剩多少？

能力：库存核算；形式：single-choice；证据：model-state。

- A：8
- B：6
- C：10
- D：7

```json
{
  "input": {
    "available": 11,
    "required": 4
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 子装配边界（h3-exp-d1-gantry-1-boundary）

隔离 cell-0-probe-0 需要断开哪些边界关节？

能力：子装配边界；形式：single-choice；证据：model-state。

- A：["cell-0-trolley-0-joint"]
- B：["cell-0-probe-0-joint"]
- C：[]
- D：["cell-0-mount-joint","cell-0-overhead-joint","cell-0-trolley-0-joint","cell-0-probe-0-joint"]

```json
{
  "input": {
    "joints": [
      {
        "id": "cell-0-mount-joint",
        "name": "cell-0-mount interface",
        "parent": "foundation",
        "child": "cell-0-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          0,
          -0.04999999999999993,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-overhead-joint",
        "name": "cell-0-overhead interface",
        "parent": "cell-0-mount",
        "child": "cell-0-overhead",
        "type": "fixed",
        "anchorParent": [
          0,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          0,
          -2.1874999999999996,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-trolley-0-joint",
        "name": "cell-0-trolley-0 interface",
        "parent": "cell-0-overhead",
        "child": "cell-0-trolley-0",
        "type": "prismatic",
        "anchorParent": [
          0,
          2.5125000000000015,
          0
        ],
        "anchorChild": [
          0,
          -0.04999999999999982,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-probe-0-joint",
        "name": "cell-0-probe-0 interface",
        "parent": "cell-0-trolley-0",
        "child": "cell-0-probe-0",
        "type": "prismatic",
        "anchorParent": [
          0,
          -1.6500000000000004,
          0.9
        ],
        "anchorChild": [
          0,
          0.5250000000000004,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      }
    ],
    "target": "cell-0-probe-0"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 最小干预（h3-exp-d1-gantry-1-no-op）

当前模块颜色已满足指令，且无需改变位姿。最少需要几次编辑？

能力：最小干预；形式：single-choice；证据：model-state。

- A：0
- B：1
- C：2
- D：4

```json
{
  "input": {
    "module": "cell-0-probe-0"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 全过程依赖（h3-exp-d1-gantry-1-prefix）

给定候选顺序，首次违反前置依赖的步骤是？从 0 编号，-1 表示没有违反。

能力：全过程依赖；形式：single-choice；证据：support-graph。

- A：0
- B：4
- C：-1

```json
{
  "input": {
    "order": [
      "foundation",
      "cell-0-mount",
      "cell-0-overhead",
      "cell-0-trolley-0",
      "cell-0-probe-0"
    ],
    "joints": [
      {
        "id": "cell-0-mount-joint",
        "name": "cell-0-mount interface",
        "parent": "foundation",
        "child": "cell-0-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          0,
          -0.04999999999999993,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-overhead-joint",
        "name": "cell-0-overhead interface",
        "parent": "cell-0-mount",
        "child": "cell-0-overhead",
        "type": "fixed",
        "anchorParent": [
          0,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          0,
          -2.1874999999999996,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-trolley-0-joint",
        "name": "cell-0-trolley-0 interface",
        "parent": "cell-0-overhead",
        "child": "cell-0-trolley-0",
        "type": "prismatic",
        "anchorParent": [
          0,
          2.5125000000000015,
          0
        ],
        "anchorChild": [
          0,
          -0.04999999999999982,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-probe-0-joint",
        "name": "cell-0-probe-0 interface",
        "parent": "cell-0-trolley-0",
        "child": "cell-0-probe-0",
        "type": "prismatic",
        "anchorParent": [
          0,
          -1.6500000000000004,
          0.9
        ],
        "anchorChild": [
          0,
          0.5250000000000004,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 连续维修路径（h3-exp-d1-gantry-1-access）

根据实际 Rapier shape cast 记录，选择全部无碰撞路径。

能力：连续维修路径；形式：multiple-choice；证据：Rapier。

- A：path-2
- B：path-1
- C：path-0

```json
{
  "input": {
    "paths": [
      {
        "id": "path-0",
        "start": [
          7.98,
          3.7249999999999996,
          0.9
        ],
        "end": [
          0,
          3.7249999999999996,
          0.9
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": true,
        "timeOfImpact": null
      },
      {
        "id": "path-1",
        "start": [
          0,
          10.07,
          0.9
        ],
        "end": [
          0,
          3.7249999999999996,
          0.9
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": false,
        "timeOfImpact": 0.6020486950874329
      },
      {
        "id": "path-2",
        "start": [
          0,
          3.7249999999999996,
          7.48
        ],
        "end": [
          0,
          3.7249999999999996,
          0.9
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": true,
        "timeOfImpact": null
      }
    ],
    "simulator": "stud-inclusive conservative cuboids; anchored base; force-limited position servos; no clutch/material calibration"
  },
  "answer": {
    "choiceIds": [
      "A",
      "C"
    ]
  }
}
```

### 支撑反事实（h3-exp-d1-gantry-1-counterfactual）

移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。

能力：支撑反事实；形式：single-choice；证据：support-graph。

- A：["cell-0-mount"]
- B：[]
- C：["foundation","cell-0-mount","cell-0-overhead","cell-0-trolley-0","cell-0-probe-0"]
- D：["cell-0-overhead","cell-0-probe-0","cell-0-trolley-0"]

```json
{
  "input": {
    "removed": "cell-0-mount",
    "roots": [
      "foundation"
    ],
    "joints": [
      {
        "id": "cell-0-mount-joint",
        "name": "cell-0-mount interface",
        "parent": "foundation",
        "child": "cell-0-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          0,
          -0.04999999999999993,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-overhead-joint",
        "name": "cell-0-overhead interface",
        "parent": "cell-0-mount",
        "child": "cell-0-overhead",
        "type": "fixed",
        "anchorParent": [
          0,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          0,
          -2.1874999999999996,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-trolley-0-joint",
        "name": "cell-0-trolley-0 interface",
        "parent": "cell-0-overhead",
        "child": "cell-0-trolley-0",
        "type": "prismatic",
        "anchorParent": [
          0,
          2.5125000000000015,
          0
        ],
        "anchorChild": [
          0,
          -0.04999999999999982,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-probe-0-joint",
        "name": "cell-0-probe-0 interface",
        "parent": "cell-0-trolley-0",
        "child": "cell-0-probe-0",
        "type": "prismatic",
        "anchorParent": [
          0,
          -1.6500000000000004,
          0.9
        ],
        "anchorChild": [
          0,
          0.5250000000000004,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      }
    ],
    "modules": [
      "foundation",
      "cell-0-mount",
      "cell-0-overhead",
      "cell-0-trolley-0",
      "cell-0-probe-0"
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 冲击响应读数（h3-exp-d1-gantry-1-dynamic）

Rapier 实际采样轨迹中的最大平移位移是多少？按四位小数报告。

能力：冲击响应读数；形式：single-choice；证据：Rapier。

- A：0.2053
- B：0
- C：1.0053
- D：0.0053

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.005275406147658841
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.00008038731182632717
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.0000012211905447674176
      },
      {
        "time": 0.30833333333333335,
        "displacement": 1.723792966969672e-8
      },
      {
        "time": 0.4083333333333333,
        "displacement": 3.653725447463007e-8
      },
      {
        "time": 0.5083333333333333,
        "displacement": 3.6835426628264436e-8
      },
      {
        "time": 0.6083333333333333,
        "displacement": 3.683775010301037e-8
      },
      {
        "time": 0.7083333333333334,
        "displacement": 3.683775010301037e-8
      },
      {
        "time": 0.8083333333333333,
        "displacement": 3.683775010301037e-8
      },
      {
        "time": 0.9083333333333333,
        "displacement": 3.683775010301037e-8
      },
      {
        "time": 1,
        "displacement": 3.683775010301037e-8
      }
    ],
    "impulse": [
      10,
      1.8,
      3.5
    ],
    "nominalDrift": 0.00006828338178241204,
    "scope": "采样轨迹极值，非连续时间极值；不代表实物安全阈值"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 关节限位推理（h3-exp-d1-gantry-1-kinematic）

下列目标位置/角度中哪些在关节声明限位内（含边界）？

能力：关节限位推理；形式：multiple-choice；证据：model-state。

- A：-0.45
- B：0
- C：-0.95
- D：0.95

```json
{
  "input": {
    "joint": "cell-0-trolley-0-joint",
    "limits": [
      -0.45,
      0.45
    ],
    "units": "scene units"
  },
  "answer": {
    "choiceIds": [
      "A",
      "B"
    ]
  }
}
```

### 约束故障诊断（h3-exp-d1-gantry-1-diagnosis）

已检测到端点和约束类型如下，选择匹配的全部关节。

能力：约束故障诊断；形式：multiple-choice；证据：model-state。

- A：cell-0-trolley-0-joint
- B：cell-0-probe-0-joint
- C：cell-0-mount-joint
- D：cell-0-overhead-joint

```json
{
  "input": {
    "endpoints": [
      "cell-0-trolley-0",
      "cell-0-probe-0"
    ],
    "type": "prismatic",
    "joints": [
      {
        "id": "cell-0-mount-joint",
        "name": "cell-0-mount interface",
        "parent": "foundation",
        "child": "cell-0-mount",
        "type": "fixed",
        "anchorParent": [
          0,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          0,
          -0.04999999999999993,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-overhead-joint",
        "name": "cell-0-overhead interface",
        "parent": "cell-0-mount",
        "child": "cell-0-overhead",
        "type": "fixed",
        "anchorParent": [
          0,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          0,
          -2.1874999999999996,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-trolley-0-joint",
        "name": "cell-0-trolley-0 interface",
        "parent": "cell-0-overhead",
        "child": "cell-0-trolley-0",
        "type": "prismatic",
        "anchorParent": [
          0,
          2.5125000000000015,
          0
        ],
        "anchorChild": [
          0,
          -0.04999999999999982,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      },
      {
        "id": "cell-0-probe-0-joint",
        "name": "cell-0-probe-0 interface",
        "parent": "cell-0-trolley-0",
        "child": "cell-0-probe-0",
        "type": "prismatic",
        "anchorParent": [
          0,
          -1.6500000000000004,
          0.9
        ],
        "anchorChild": [
          0,
          0.5250000000000004,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.45,
          0.45
        ]
      }
    ]
  },
  "answer": {
    "choiceIds": [
      "B"
    ]
  }
}
```

### 主动检查收益（h3-exp-d1-gantry-1-information-gain）

均匀先验四个世界，选择信息增益/成本最大的全部检查。

能力：主动检查收益；形式：multiple-choice；证据：finite-world。

- A：query-2
- B：query-0
- C：query-1

```json
{
  "input": {
    "queries": [
      {
        "id": "query-0",
        "cost": 2,
        "returns": [
          0,
          0,
          1,
          1
        ]
      },
      {
        "id": "query-1",
        "cost": 3,
        "returns": [
          0,
          1,
          2,
          3
        ]
      },
      {
        "id": "query-2",
        "cost": 1,
        "returns": [
          0,
          0,
          0,
          1
        ]
      }
    ],
    "module": "cell-0-probe-0",
    "worlds": [
      "normal",
      "jammed",
      "reversed",
      "loose"
    ]
  },
  "answer": {
    "choiceIds": [
      "A"
    ]
  }
}
```

### 不确定性与弃答（h3-exp-d1-gantry-1-abstention）

所有相容世界是否允许同一个后续动作？选择继续执行或请求检查。

能力：不确定性与弃答；形式：single-choice；证据：finite-world。

- A：commit
- B：inspect

```json
{
  "input": {
    "worlds": [
      {
        "id": "w0",
        "action": "continue"
      },
      {
        "id": "w1",
        "action": "repair"
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 观测后信念更新（h3-exp-d1-gantry-1-posterior）

均匀先验，得到给定观测后，jammed 世界的后验概率是多少？

能力：观测后信念更新；形式：single-choice；证据：finite-world。

- A：0.25
- B：0.5
- C：0.3333333333333333
- D：0

```json
{
  "input": {
    "module": "cell-0-probe-0",
    "worlds": [
      "normal",
      "jammed",
      "reversed",
      "loose"
    ],
    "observationByWorld": [
      "negative",
      "negative",
      "positive",
      "negative"
    ],
    "observed": "negative"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 多目标工程权衡（h3-exp-d1-gantry-1-pareto）

最小成本、最小质量、最大刚度，选择完整非支配集合。

能力：多目标工程权衡；形式：multiple-choice；证据：model-state。

- A：stock-3
- B：stock-1
- C：stock-0
- D：stock-2

```json
{
  "input": {
    "alternatives": [
      {
        "id": "stock-0",
        "cost": 5,
        "stiffness": 3,
        "mass": 1.2
      },
      {
        "id": "stock-1",
        "cost": 2,
        "stiffness": 7,
        "mass": 1.1
      },
      {
        "id": "stock-2",
        "cost": 5,
        "stiffness": 7,
        "mass": 1.3
      },
      {
        "id": "stock-3",
        "cost": 5,
        "stiffness": 5,
        "mass": 1.2
      }
    ]
  },
  "answer": {
    "choiceIds": [
      "B"
    ]
  }
}
```

### 依赖装配（h3-exp-d1-gantry-1-assembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖装配；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [],
    "initialModules": [],
    "actions": [
      {
        "id": "place:cell-0-trolley-0",
        "label": "安装 cell-0-trolley-0",
        "requires": [
          "present:cell-0-overhead"
        ],
        "forbids": [
          "present:cell-0-trolley-0"
        ],
        "adds": [
          "present:cell-0-trolley-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-trolley-0",
          "visible": true
        }
      },
      {
        "id": "place:cell-0-probe-0",
        "label": "安装 cell-0-probe-0",
        "requires": [
          "present:cell-0-trolley-0"
        ],
        "forbids": [
          "present:cell-0-probe-0"
        ],
        "adds": [
          "present:cell-0-probe-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0",
          "visible": true
        }
      },
      {
        "id": "place:cell-0-overhead",
        "label": "安装 cell-0-overhead",
        "requires": [
          "present:cell-0-mount"
        ],
        "forbids": [
          "present:cell-0-overhead"
        ],
        "adds": [
          "present:cell-0-overhead"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-overhead",
          "visible": true
        }
      },
      {
        "id": "place:cell-0-mount",
        "label": "安装 cell-0-mount",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:cell-0-mount"
        ],
        "adds": [
          "present:cell-0-mount"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-mount",
          "visible": true
        }
      },
      {
        "id": "place:foundation",
        "label": "安装 foundation",
        "requires": [],
        "forbids": [
          "present:foundation"
        ],
        "adds": [
          "present:foundation"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "foundation",
          "visible": true
        }
      }
    ],
    "goalFacts": [
      "present:foundation",
      "present:cell-0-mount",
      "present:cell-0-overhead",
      "present:cell-0-trolley-0",
      "present:cell-0-probe-0"
    ],
    "budget": 5,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "place:foundation",
      "place:cell-0-mount",
      "place:cell-0-overhead",
      "place:cell-0-trolley-0",
      "place:cell-0-probe-0"
    ]
  }
}
```

### 依赖拆解（h3-exp-d1-gantry-1-disassembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖拆解；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "present:foundation",
      "present:cell-0-mount",
      "present:cell-0-overhead",
      "present:cell-0-trolley-0",
      "present:cell-0-probe-0"
    ],
    "initialModules": [
      "foundation",
      "cell-0-mount",
      "cell-0-overhead",
      "cell-0-trolley-0",
      "cell-0-probe-0"
    ],
    "actions": [
      {
        "id": "remove:cell-0-probe-0",
        "label": "拆除 cell-0-probe-0",
        "requires": [
          "present:cell-0-probe-0"
        ],
        "forbids": [],
        "adds": [
          "removed:cell-0-probe-0"
        ],
        "deletes": [
          "present:cell-0-probe-0"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0",
          "visible": false
        }
      },
      {
        "id": "remove:cell-0-trolley-0",
        "label": "拆除 cell-0-trolley-0",
        "requires": [
          "present:cell-0-trolley-0"
        ],
        "forbids": [
          "present:cell-0-probe-0"
        ],
        "adds": [
          "removed:cell-0-trolley-0"
        ],
        "deletes": [
          "present:cell-0-trolley-0"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-trolley-0",
          "visible": false
        }
      },
      {
        "id": "remove:cell-0-overhead",
        "label": "拆除 cell-0-overhead",
        "requires": [
          "present:cell-0-overhead"
        ],
        "forbids": [
          "present:cell-0-trolley-0"
        ],
        "adds": [
          "removed:cell-0-overhead"
        ],
        "deletes": [
          "present:cell-0-overhead"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-overhead",
          "visible": false
        }
      },
      {
        "id": "remove:foundation",
        "label": "拆除 foundation",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:cell-0-mount"
        ],
        "adds": [
          "removed:foundation"
        ],
        "deletes": [
          "present:foundation"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "foundation",
          "visible": false
        }
      },
      {
        "id": "remove:cell-0-mount",
        "label": "拆除 cell-0-mount",
        "requires": [
          "present:cell-0-mount"
        ],
        "forbids": [
          "present:cell-0-overhead"
        ],
        "adds": [
          "removed:cell-0-mount"
        ],
        "deletes": [
          "present:cell-0-mount"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-mount",
          "visible": false
        }
      }
    ],
    "goalFacts": [
      "removed:cell-0-probe-0",
      "removed:cell-0-trolley-0",
      "removed:cell-0-overhead",
      "removed:cell-0-mount",
      "removed:foundation"
    ],
    "budget": 5,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "remove:cell-0-probe-0",
      "remove:cell-0-trolley-0",
      "remove:cell-0-overhead",
      "remove:cell-0-mount",
      "remove:foundation"
    ]
  }
}
```

### 承载维修（h3-exp-d1-gantry-1-service-repair）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：承载维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:cell-0-probe-0",
      "closed:cell-0-probe-0"
    ],
    "initialModules": [
      "foundation",
      "cell-0-mount",
      "cell-0-overhead",
      "cell-0-trolley-0",
      "cell-0-probe-0"
    ],
    "actions": [
      {
        "id": "open:cell-0-probe-0",
        "label": "open cell-0-probe-0",
        "requires": [
          "done:support:cell-0-probe-0"
        ],
        "forbids": [
          "done:open:cell-0-probe-0"
        ],
        "adds": [
          "done:open:cell-0-probe-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0"
        }
      },
      {
        "id": "close:cell-0-probe-0",
        "label": "close cell-0-probe-0",
        "requires": [
          "done:verify:cell-0-probe-0"
        ],
        "forbids": [
          "done:close:cell-0-probe-0"
        ],
        "adds": [
          "done:close:cell-0-probe-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0"
        }
      },
      {
        "id": "release:cell-0-probe-0",
        "label": "release cell-0-probe-0",
        "requires": [
          "done:close:cell-0-probe-0"
        ],
        "forbids": [
          "done:release:cell-0-probe-0"
        ],
        "adds": [
          "done:release:cell-0-probe-0",
          "repaired:cell-0-probe-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0"
        }
      },
      {
        "id": "remove:cell-0-probe-0",
        "label": "remove cell-0-probe-0",
        "requires": [
          "done:open:cell-0-probe-0"
        ],
        "forbids": [
          "done:remove:cell-0-probe-0"
        ],
        "adds": [
          "done:remove:cell-0-probe-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0",
          "visible": false
        }
      },
      {
        "id": "support:cell-0-probe-0",
        "label": "support cell-0-probe-0",
        "requires": [
          "fault:cell-0-probe-0"
        ],
        "forbids": [
          "done:support:cell-0-probe-0"
        ],
        "adds": [
          "done:support:cell-0-probe-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0"
        }
      },
      {
        "id": "replace:cell-0-probe-0",
        "label": "replace cell-0-probe-0",
        "requires": [
          "done:remove:cell-0-probe-0"
        ],
        "forbids": [
          "done:replace:cell-0-probe-0"
        ],
        "adds": [
          "done:replace:cell-0-probe-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0",
          "visible": true
        }
      },
      {
        "id": "verify:cell-0-probe-0",
        "label": "verify cell-0-probe-0",
        "requires": [
          "done:replace:cell-0-probe-0"
        ],
        "forbids": [
          "done:verify:cell-0-probe-0"
        ],
        "adds": [
          "done:verify:cell-0-probe-0"
        ],
        "deletes": [
          "fault:cell-0-probe-0"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0"
        }
      }
    ],
    "goalFacts": [
      "repaired:cell-0-probe-0"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:cell-0-probe-0",
      "open:cell-0-probe-0",
      "remove:cell-0-probe-0",
      "replace:cell-0-probe-0",
      "verify:cell-0-probe-0",
      "close:cell-0-probe-0",
      "release:cell-0-probe-0"
    ]
  }
}
```

### 复合编辑验证（h3-exp-d1-gantry-1-compound-edit）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：复合编辑验证；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:cell-0-probe-0",
      "closed:cell-0-probe-0"
    ],
    "initialModules": [
      "foundation",
      "cell-0-mount",
      "cell-0-overhead",
      "cell-0-trolley-0",
      "cell-0-probe-0"
    ],
    "actions": [
      {
        "id": "open:cell-0-probe-0",
        "label": "open cell-0-probe-0",
        "requires": [
          "done:support:cell-0-probe-0"
        ],
        "forbids": [
          "done:open:cell-0-probe-0"
        ],
        "adds": [
          "done:open:cell-0-probe-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0"
        }
      },
      {
        "id": "close:cell-0-probe-0",
        "label": "close cell-0-probe-0",
        "requires": [
          "done:verify:cell-0-probe-0"
        ],
        "forbids": [
          "done:close:cell-0-probe-0"
        ],
        "adds": [
          "done:close:cell-0-probe-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0"
        }
      },
      {
        "id": "release:cell-0-probe-0",
        "label": "release cell-0-probe-0",
        "requires": [
          "done:close:cell-0-probe-0"
        ],
        "forbids": [
          "done:release:cell-0-probe-0"
        ],
        "adds": [
          "done:release:cell-0-probe-0",
          "repaired:cell-0-probe-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0"
        }
      },
      {
        "id": "support:cell-0-probe-0",
        "label": "support cell-0-probe-0",
        "requires": [
          "fault:cell-0-probe-0"
        ],
        "forbids": [
          "done:support:cell-0-probe-0"
        ],
        "adds": [
          "done:support:cell-0-probe-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0"
        }
      },
      {
        "id": "verify:cell-0-probe-0",
        "label": "verify cell-0-probe-0",
        "requires": [
          "done:recolor:cell-0-probe-0"
        ],
        "forbids": [
          "done:verify:cell-0-probe-0"
        ],
        "adds": [
          "done:verify:cell-0-probe-0"
        ],
        "deletes": [
          "fault:cell-0-probe-0"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0"
        }
      },
      {
        "id": "recolor:cell-0-probe-0",
        "label": "recolor cell-0-probe-0",
        "requires": [
          "done:open:cell-0-probe-0"
        ],
        "forbids": [
          "done:recolor:cell-0-probe-0"
        ],
        "adds": [
          "done:recolor:cell-0-probe-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0",
          "color": "#ea7635"
        }
      }
    ],
    "goalFacts": [
      "repaired:cell-0-probe-0"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:cell-0-probe-0",
      "open:cell-0-probe-0",
      "recolor:cell-0-probe-0",
      "verify:cell-0-probe-0",
      "close:cell-0-probe-0",
      "release:cell-0-probe-0"
    ]
  }
}
```

### 跨区域联合维修（h3-exp-d1-gantry-1-multi-fault）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：跨区域联合维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:cell-0-probe-0",
      "closed:cell-0-probe-0"
    ],
    "initialModules": [
      "foundation",
      "cell-0-mount",
      "cell-0-overhead",
      "cell-0-trolley-0",
      "cell-0-probe-0"
    ],
    "actions": [
      {
        "id": "open:cell-0-probe-0",
        "label": "open cell-0-probe-0",
        "requires": [
          "done:support:cell-0-probe-0"
        ],
        "forbids": [
          "done:open:cell-0-probe-0"
        ],
        "adds": [
          "done:open:cell-0-probe-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0"
        }
      },
      {
        "id": "close:cell-0-probe-0",
        "label": "close cell-0-probe-0",
        "requires": [
          "done:verify:cell-0-probe-0"
        ],
        "forbids": [
          "done:close:cell-0-probe-0"
        ],
        "adds": [
          "done:close:cell-0-probe-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0"
        }
      },
      {
        "id": "release:cell-0-probe-0",
        "label": "release cell-0-probe-0",
        "requires": [
          "done:close:cell-0-probe-0"
        ],
        "forbids": [
          "done:release:cell-0-probe-0"
        ],
        "adds": [
          "done:release:cell-0-probe-0",
          "repaired:cell-0-probe-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0"
        }
      },
      {
        "id": "remove:cell-0-probe-0",
        "label": "remove cell-0-probe-0",
        "requires": [
          "done:open:cell-0-probe-0"
        ],
        "forbids": [
          "done:remove:cell-0-probe-0"
        ],
        "adds": [
          "done:remove:cell-0-probe-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0",
          "visible": false
        }
      },
      {
        "id": "support:cell-0-probe-0",
        "label": "support cell-0-probe-0",
        "requires": [
          "fault:cell-0-probe-0"
        ],
        "forbids": [
          "done:support:cell-0-probe-0"
        ],
        "adds": [
          "done:support:cell-0-probe-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0"
        }
      },
      {
        "id": "replace:cell-0-probe-0",
        "label": "replace cell-0-probe-0",
        "requires": [
          "done:remove:cell-0-probe-0"
        ],
        "forbids": [
          "done:replace:cell-0-probe-0"
        ],
        "adds": [
          "done:replace:cell-0-probe-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0",
          "visible": true
        }
      },
      {
        "id": "verify:cell-0-probe-0",
        "label": "verify cell-0-probe-0",
        "requires": [
          "done:replace:cell-0-probe-0"
        ],
        "forbids": [
          "done:verify:cell-0-probe-0"
        ],
        "adds": [
          "done:verify:cell-0-probe-0"
        ],
        "deletes": [
          "fault:cell-0-probe-0"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0"
        }
      }
    ],
    "goalFacts": [
      "repaired:cell-0-probe-0"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:cell-0-probe-0",
      "open:cell-0-probe-0",
      "remove:cell-0-probe-0",
      "replace:cell-0-probe-0",
      "verify:cell-0-probe-0",
      "close:cell-0-probe-0",
      "release:cell-0-probe-0"
    ]
  }
}
```

### 多工位资源调度（h3-exp-d1-gantry-1-scheduling）

为所有工单提交整数 starts，满足先后关系、独占工位及截止时间。

能力：多工位资源调度；形式：schedule；证据：resource-schedule。


```json
{
  "input": {
    "jobs": [
      {
        "id": "job-0",
        "module": "foundation",
        "duration": 1,
        "resource": "test-bench",
        "after": []
      },
      {
        "id": "job-1",
        "module": "cell-0-mount",
        "duration": 3,
        "resource": "technician",
        "after": []
      },
      {
        "id": "job-2",
        "module": "cell-0-overhead",
        "duration": 2,
        "resource": "test-bench",
        "after": [
          "job-0"
        ]
      },
      {
        "id": "job-3",
        "module": "cell-0-trolley-0",
        "duration": 2,
        "resource": "technician",
        "after": [
          "job-1"
        ]
      }
    ],
    "deadline": 5
  },
  "answer": {
    "starts": {
      "job-0": 0,
      "job-1": 0,
      "job-2": 1,
      "job-3": 3
    }
  }
}
```

### 检查后条件策略（h3-exp-d1-gantry-1-policy）

提交一个检查及 observation→action 决策表，在所有相容世界中采取正确动作。

能力：检查后条件策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "cell-0-probe-0",
    "worlds": [
      {
        "id": "normal",
        "action": "tighten"
      },
      {
        "id": "loose",
        "action": "replace"
      },
      {
        "id": "jammed",
        "action": "continue"
      }
    ],
    "budget": 2,
    "queries": [
      {
        "id": "visual",
        "cost": 1,
        "returns": {
          "normal": "same",
          "loose": "same",
          "jammed": "other"
        }
      },
      {
        "id": "probe",
        "cost": 2,
        "returns": {
          "normal": "signal-0",
          "loose": "signal-1",
          "jammed": "signal-2"
        }
      },
      {
        "id": "thermal",
        "cost": 3,
        "returns": {
          "normal": "same",
          "loose": "same",
          "jammed": "other"
        }
      }
    ]
  },
  "answer": {
    "queryId": "probe",
    "decisions": {
      "signal-0": "tighten",
      "signal-1": "replace",
      "signal-2": "continue"
    }
  }
}
```

### 局部坐标变换（h3-exp-d1-gantry-1-local-frame）

将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。

能力：局部坐标变换；形式：single-choice；证据：model-state。

- A：[2,4.3,1.9]
- B：[1,3.3,0.9]
- C：[1,-0.425,0]

```json
{
  "input": {
    "localPoint": [
      1,
      -0.4249999999999997,
      0
    ],
    "rotationXYZW": [
      0,
      0,
      0,
      1
    ],
    "translation": [
      0,
      3.7249999999999996,
      0.9
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 正交视图投影（h3-exp-d1-gantry-1-projection）

按公开视图坐标约定，选择该世界点投影后的二维坐标。

能力：正交视图投影；形式：single-choice；证据：model-state。

- A：[-3,5]
- B：[5,2]
- C：[2,3]
- D：[0,0]

```json
{
  "input": {
    "view": "side",
    "point": [
      2,
      5,
      -3
    ],
    "convention": "front=(x,y), side=(z,y), top=(x,z)"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 空间相对关系（h3-exp-d1-gantry-1-relative-order）

比较B相对A在指定世界轴上的模块原点坐标。

能力：空间相对关系；形式：single-choice；证据：model-state。

- A：equal
- B：greater
- C：less

```json
{
  "input": {
    "A": {
      "id": "foundation",
      "position": [
        0,
        0.2,
        0
      ]
    },
    "B": {
      "id": "cell-0-probe-0",
      "position": [
        0,
        3.7249999999999996,
        0.9
      ]
    },
    "axis": "y"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 约束自由度（h3-exp-d1-gantry-1-joint-axis）

仅考虑这一声明约束，不计闭环、马达与限位激活，保留多少相对运动自由度？弹簧仅施力、不消除自由度。

能力：约束自由度；形式：single-choice；证据：model-state。

- A：6
- B：0
- C：1
- D：3

```json
{
  "input": {
    "joint": {
      "id": "cell-0-mount-joint",
      "name": "cell-0-mount interface",
      "parent": "foundation",
      "child": "cell-0-mount",
      "type": "fixed",
      "anchorParent": [
        0,
        0.44999999999999996,
        0
      ],
      "anchorChild": [
        0,
        -0.04999999999999993,
        0
      ],
      "axis": [
        0,
        1,
        0
      ]
    }
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 维修间隙预算（h3-exp-d1-gantry-1-clearance-margin）

给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？

能力：维修间隙预算；形式：single-choice；证据：model-state。

- A：feasible
- B：blocked

```json
{
  "input": {
    "module": "cell-0-probe-0",
    "aperture": 0.41999999999999993,
    "toolWidth": 0.35,
    "eachSideMargin": 0.05
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 载荷力矩（h3-exp-d1-gantry-1-load-moment）

绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。

能力：载荷力矩；形式：single-choice；证据：model-state。

- A：[0,0,0]
- B：[0,-1,0]
- C：[0,0,-2]
- D：[0,0,2]

```json
{
  "input": {
    "module": "cell-0-probe-0",
    "lever": [
      1,
      2,
      0
    ],
    "force": [
      0,
      -2,
      0
    ],
    "units": "scene-length × force"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 非均匀先验更新（h3-exp-d1-gantry-1-weighted-posterior）

先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。

能力：非均匀先验更新；形式：single-choice；证据：finite-world。

- A：1
- B：0.8333333333333334
- C：0.625
- D：0

```json
{
  "input": {
    "module": "cell-0-probe-0",
    "worlds": [
      "normal",
      "jammed",
      "loose"
    ],
    "weights": [
      1,
      5,
      2
    ],
    "compatible": [
      "normal",
      "jammed"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 风险最小决策（h3-exp-d1-gantry-1-expected-loss）

继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。

能力：风险最小决策；形式：single-choice；证据：finite-world。

- A：repair
- B：continue

```json
{
  "input": {
    "faultProbability": 0.5,
    "repairCost": 3,
    "failureLoss": 7,
    "module": "cell-0-probe-0"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 轨迹阈值判定（h3-exp-d1-gantry-1-trace-threshold）

实际采样轨迹中是否有位移严格超过给定阈值？只评价采样点。

能力：轨迹阈值判定；形式：single-choice；证据：Rapier。

- A：exceeded
- B：within

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.005275406147658841
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.00008038731182632717
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.0000012211905447674176
      },
      {
        "time": 0.30833333333333335,
        "displacement": 1.723792966969672e-8
      },
      {
        "time": 0.4083333333333333,
        "displacement": 3.653725447463007e-8
      },
      {
        "time": 0.5083333333333333,
        "displacement": 3.6835426628264436e-8
      },
      {
        "time": 0.6083333333333333,
        "displacement": 3.683775010301037e-8
      },
      {
        "time": 0.7083333333333334,
        "displacement": 3.683775010301037e-8
      },
      {
        "time": 0.8083333333333333,
        "displacement": 3.683775010301037e-8
      },
      {
        "time": 0.9083333333333333,
        "displacement": 3.683775010301037e-8
      },
      {
        "time": 1,
        "displacement": 3.683775010301037e-8
      }
    ],
    "threshold": 0.004220324918127073
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 安全联锁维修（h3-exp-d1-gantry-1-guarded-repair）

从给定故障状态提交动作序列，满足联锁、独占工具、终态及预算。不要跳过验证。

能力：安全联锁维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "actions": [
      {
        "id": "skip-inspection",
        "label": "跳过检查",
        "requires": [
          "tool:free"
        ],
        "forbids": [],
        "adds": [
          "unverified"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 0
      },
      {
        "id": "release:cell-0-probe-0",
        "label": "release cell-0-probe-0",
        "requires": [
          "done:relock:cell-0-probe-0"
        ],
        "forbids": [
          "done:release:cell-0-probe-0"
        ],
        "adds": [
          "done:release:cell-0-probe-0",
          "ready:cell-0-probe-0",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0"
        }
      },
      {
        "id": "relock:cell-0-probe-0",
        "label": "relock cell-0-probe-0",
        "requires": [
          "done:verify:cell-0-probe-0"
        ],
        "forbids": [
          "done:relock:cell-0-probe-0"
        ],
        "adds": [
          "done:relock:cell-0-probe-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0"
        }
      },
      {
        "id": "verify:cell-0-probe-0",
        "label": "verify cell-0-probe-0",
        "requires": [
          "done:replace:cell-0-probe-0"
        ],
        "forbids": [
          "done:verify:cell-0-probe-0"
        ],
        "adds": [
          "done:verify:cell-0-probe-0"
        ],
        "deletes": [
          "fault:cell-0-probe-0",
          "misaligned:cell-0-probe-0"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0"
        }
      },
      {
        "id": "replace:cell-0-probe-0",
        "label": "replace cell-0-probe-0",
        "requires": [
          "done:unlock:cell-0-probe-0"
        ],
        "forbids": [
          "done:replace:cell-0-probe-0"
        ],
        "adds": [
          "done:replace:cell-0-probe-0"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "cell-0-probe-0"
        }
      },
      {
        "id": "unlock:cell-0-probe-0",
        "label": "unlock cell-0-probe-0",
        "requires": [
          "done:support:cell-0-probe-0"
        ],
        "forbids": [
          "done:unlock:cell-0-probe-0"
        ],
        "adds": [
          "done:unlock:cell-0-probe-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0"
        }
      },
      {
        "id": "support:cell-0-probe-0",
        "label": "support cell-0-probe-0",
        "requires": [
          "done:isolate:cell-0-probe-0"
        ],
        "forbids": [
          "done:support:cell-0-probe-0"
        ],
        "adds": [
          "done:support:cell-0-probe-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0"
        }
      },
      {
        "id": "isolate:cell-0-probe-0",
        "label": "isolate cell-0-probe-0",
        "requires": [
          "tool:free",
          "fault:cell-0-probe-0"
        ],
        "forbids": [
          "done:isolate:cell-0-probe-0"
        ],
        "adds": [
          "done:isolate:cell-0-probe-0"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:cell-0-probe-0"
    ],
    "initialModules": [
      "foundation",
      "cell-0-mount",
      "cell-0-overhead",
      "cell-0-trolley-0",
      "cell-0-probe-0"
    ],
    "goalFacts": [
      "ready:cell-0-probe-0"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 8
  },
  "answer": {
    "actionIds": [
      "isolate:cell-0-probe-0",
      "support:cell-0-probe-0",
      "unlock:cell-0-probe-0",
      "replace:cell-0-probe-0",
      "verify:cell-0-probe-0",
      "relock:cell-0-probe-0",
      "release:cell-0-probe-0"
    ]
  }
}
```

### 失败状态回退（h3-exp-d1-gantry-1-rollback）

从给定故障状态提交动作序列，满足联锁、独占工具、终态及预算。不要跳过验证。

能力：失败状态回退；形式：actions；证据：state-machine。


```json
{
  "input": {
    "actions": [
      {
        "id": "skip-inspection",
        "label": "跳过检查",
        "requires": [
          "tool:free"
        ],
        "forbids": [],
        "adds": [
          "unverified"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 0
      },
      {
        "id": "resume:cell-0-probe-0",
        "label": "resume cell-0-probe-0",
        "requires": [
          "done:verify:cell-0-probe-0"
        ],
        "forbids": [
          "done:resume:cell-0-probe-0"
        ],
        "adds": [
          "done:resume:cell-0-probe-0",
          "ready:cell-0-probe-0",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0"
        }
      },
      {
        "id": "verify:cell-0-probe-0",
        "label": "verify cell-0-probe-0",
        "requires": [
          "done:align:cell-0-probe-0"
        ],
        "forbids": [
          "done:verify:cell-0-probe-0"
        ],
        "adds": [
          "done:verify:cell-0-probe-0"
        ],
        "deletes": [
          "fault:cell-0-probe-0",
          "misaligned:cell-0-probe-0"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0"
        }
      },
      {
        "id": "align:cell-0-probe-0",
        "label": "align cell-0-probe-0",
        "requires": [
          "done:undo:cell-0-probe-0"
        ],
        "forbids": [
          "done:align:cell-0-probe-0"
        ],
        "adds": [
          "done:align:cell-0-probe-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0",
          "visible": true
        }
      },
      {
        "id": "undo:cell-0-probe-0",
        "label": "undo cell-0-probe-0",
        "requires": [
          "done:isolate:cell-0-probe-0"
        ],
        "forbids": [
          "done:undo:cell-0-probe-0"
        ],
        "adds": [
          "done:undo:cell-0-probe-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0",
          "visible": false
        }
      },
      {
        "id": "isolate:cell-0-probe-0",
        "label": "isolate cell-0-probe-0",
        "requires": [
          "tool:free",
          "fault:cell-0-probe-0"
        ],
        "forbids": [
          "done:isolate:cell-0-probe-0"
        ],
        "adds": [
          "done:isolate:cell-0-probe-0"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:cell-0-probe-0",
      "misaligned:cell-0-probe-0"
    ],
    "initialModules": [
      "foundation",
      "cell-0-mount",
      "cell-0-overhead",
      "cell-0-trolley-0",
      "cell-0-probe-0"
    ],
    "goalFacts": [
      "ready:cell-0-probe-0"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 5
  },
  "answer": {
    "actionIds": [
      "isolate:cell-0-probe-0",
      "undo:cell-0-probe-0",
      "align:cell-0-probe-0",
      "verify:cell-0-probe-0",
      "resume:cell-0-probe-0"
    ]
  }
}
```

### 共享工具协同维修（h3-exp-d1-gantry-1-resource-repair）

从给定故障状态提交动作序列，满足联锁、独占工具、终态及预算。不要跳过验证。

能力：共享工具协同维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "actions": [
      {
        "id": "skip-inspection",
        "label": "跳过检查",
        "requires": [
          "tool:free"
        ],
        "forbids": [],
        "adds": [
          "unverified"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 0
      },
      {
        "id": "release:cell-0-probe-0",
        "label": "release cell-0-probe-0",
        "requires": [
          "done:relock:cell-0-probe-0"
        ],
        "forbids": [
          "done:release:cell-0-probe-0"
        ],
        "adds": [
          "done:release:cell-0-probe-0",
          "ready:cell-0-probe-0",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0"
        }
      },
      {
        "id": "relock:cell-0-probe-0",
        "label": "relock cell-0-probe-0",
        "requires": [
          "done:verify:cell-0-probe-0"
        ],
        "forbids": [
          "done:relock:cell-0-probe-0"
        ],
        "adds": [
          "done:relock:cell-0-probe-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0"
        }
      },
      {
        "id": "verify:cell-0-probe-0",
        "label": "verify cell-0-probe-0",
        "requires": [
          "done:replace:cell-0-probe-0"
        ],
        "forbids": [
          "done:verify:cell-0-probe-0"
        ],
        "adds": [
          "done:verify:cell-0-probe-0"
        ],
        "deletes": [
          "fault:cell-0-probe-0",
          "misaligned:cell-0-probe-0"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0"
        }
      },
      {
        "id": "replace:cell-0-probe-0",
        "label": "replace cell-0-probe-0",
        "requires": [
          "done:unlock:cell-0-probe-0"
        ],
        "forbids": [
          "done:replace:cell-0-probe-0"
        ],
        "adds": [
          "done:replace:cell-0-probe-0"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "cell-0-probe-0"
        }
      },
      {
        "id": "unlock:cell-0-probe-0",
        "label": "unlock cell-0-probe-0",
        "requires": [
          "done:support:cell-0-probe-0"
        ],
        "forbids": [
          "done:unlock:cell-0-probe-0"
        ],
        "adds": [
          "done:unlock:cell-0-probe-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0"
        }
      },
      {
        "id": "support:cell-0-probe-0",
        "label": "support cell-0-probe-0",
        "requires": [
          "done:isolate:cell-0-probe-0"
        ],
        "forbids": [
          "done:support:cell-0-probe-0"
        ],
        "adds": [
          "done:support:cell-0-probe-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0"
        }
      },
      {
        "id": "isolate:cell-0-probe-0",
        "label": "isolate cell-0-probe-0",
        "requires": [
          "tool:free",
          "fault:cell-0-probe-0"
        ],
        "forbids": [
          "done:isolate:cell-0-probe-0"
        ],
        "adds": [
          "done:isolate:cell-0-probe-0"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-probe-0"
        }
      },
      {
        "id": "release:cell-0-trolley-0",
        "label": "release cell-0-trolley-0",
        "requires": [
          "done:relock:cell-0-trolley-0"
        ],
        "forbids": [
          "done:release:cell-0-trolley-0"
        ],
        "adds": [
          "done:release:cell-0-trolley-0",
          "ready:cell-0-trolley-0",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-trolley-0"
        }
      },
      {
        "id": "relock:cell-0-trolley-0",
        "label": "relock cell-0-trolley-0",
        "requires": [
          "done:verify:cell-0-trolley-0"
        ],
        "forbids": [
          "done:relock:cell-0-trolley-0"
        ],
        "adds": [
          "done:relock:cell-0-trolley-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-trolley-0"
        }
      },
      {
        "id": "verify:cell-0-trolley-0",
        "label": "verify cell-0-trolley-0",
        "requires": [
          "done:replace:cell-0-trolley-0"
        ],
        "forbids": [
          "done:verify:cell-0-trolley-0"
        ],
        "adds": [
          "done:verify:cell-0-trolley-0"
        ],
        "deletes": [
          "fault:cell-0-trolley-0",
          "misaligned:cell-0-trolley-0"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-trolley-0"
        }
      },
      {
        "id": "replace:cell-0-trolley-0",
        "label": "replace cell-0-trolley-0",
        "requires": [
          "done:unlock:cell-0-trolley-0"
        ],
        "forbids": [
          "done:replace:cell-0-trolley-0"
        ],
        "adds": [
          "done:replace:cell-0-trolley-0"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "cell-0-trolley-0"
        }
      },
      {
        "id": "unlock:cell-0-trolley-0",
        "label": "unlock cell-0-trolley-0",
        "requires": [
          "done:support:cell-0-trolley-0"
        ],
        "forbids": [
          "done:unlock:cell-0-trolley-0"
        ],
        "adds": [
          "done:unlock:cell-0-trolley-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-trolley-0"
        }
      },
      {
        "id": "support:cell-0-trolley-0",
        "label": "support cell-0-trolley-0",
        "requires": [
          "done:isolate:cell-0-trolley-0"
        ],
        "forbids": [
          "done:support:cell-0-trolley-0"
        ],
        "adds": [
          "done:support:cell-0-trolley-0"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-trolley-0"
        }
      },
      {
        "id": "isolate:cell-0-trolley-0",
        "label": "isolate cell-0-trolley-0",
        "requires": [
          "tool:free",
          "fault:cell-0-trolley-0"
        ],
        "forbids": [
          "done:isolate:cell-0-trolley-0"
        ],
        "adds": [
          "done:isolate:cell-0-trolley-0"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-trolley-0"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:cell-0-trolley-0",
      "fault:cell-0-probe-0"
    ],
    "initialModules": [
      "foundation",
      "cell-0-mount",
      "cell-0-overhead",
      "cell-0-trolley-0",
      "cell-0-probe-0"
    ],
    "goalFacts": [
      "ready:cell-0-trolley-0",
      "ready:cell-0-probe-0"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 16
  },
  "answer": {
    "actionIds": [
      "isolate:cell-0-probe-0",
      "support:cell-0-probe-0",
      "unlock:cell-0-probe-0",
      "replace:cell-0-probe-0",
      "verify:cell-0-probe-0",
      "relock:cell-0-probe-0",
      "release:cell-0-probe-0",
      "isolate:cell-0-trolley-0",
      "support:cell-0-trolley-0",
      "unlock:cell-0-trolley-0",
      "replace:cell-0-trolley-0",
      "verify:cell-0-trolley-0",
      "relock:cell-0-trolley-0",
      "release:cell-0-trolley-0"
    ]
  }
}
```

### 预算约束检查策略（h3-exp-d1-gantry-1-budget-policy）

提交预算内、对所有相容世界均正确的检查决策表。

能力：预算约束检查策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "cell-0-probe-0",
    "worlds": [
      {
        "id": "nominal",
        "action": "continue"
      },
      {
        "id": "fault",
        "action": "tighten"
      }
    ],
    "queries": [
      {
        "id": "visual",
        "cost": 3,
        "returns": {
          "nominal": "pass",
          "fault": "fail"
        }
      },
      {
        "id": "probe",
        "cost": 2,
        "returns": {
          "nominal": "pass",
          "fault": "fail"
        }
      },
      {
        "id": "thermal",
        "cost": 0,
        "returns": {
          "nominal": "pass",
          "fault": "pass"
        }
      }
    ],
    "budget": 2
  },
  "answer": {
    "queryId": "probe",
    "decisions": {
      "pass": "continue",
      "fail": "tighten"
    }
  }
}
```
