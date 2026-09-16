## D1 三点弹性托盘

### 模块识别（h3-exp-d1-suspension-1-identify）

高亮的维修模块对应哪个 ID？

能力：模块识别；形式：single-choice；证据：model-state。

- A：cell-0-mount
- B：cell-0-support
- C：cell-0-elastic-tray
- D：foundation

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
        "id": "cell-0-support",
        "name": "cell 0 support"
      },
      {
        "id": "cell-0-elastic-tray",
        "name": "cell 0 elastic tray"
      },
      {
        "id": "cell-0-instrument",
        "name": "cell 0 instrument"
      }
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 部件计数（h3-exp-d1-suspension-1-count）

模块 cell-0-elastic-tray 有多少个可视零件？

能力：部件计数；形式：single-choice；证据：model-state。

- A：9
- B：10
- C：8
- D：12

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
        "id": "cell-0-support-p86",
        "moduleId": "cell-0-support",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-support-p87",
        "moduleId": "cell-0-support",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-support-p88",
        "moduleId": "cell-0-support",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-support-p89",
        "moduleId": "cell-0-support",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-support-p90",
        "moduleId": "cell-0-support",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-support-p91",
        "moduleId": "cell-0-support",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-support-p92",
        "moduleId": "cell-0-support",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-support-p93",
        "moduleId": "cell-0-support",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-support-p94",
        "moduleId": "cell-0-support",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-support-p95",
        "moduleId": "cell-0-support",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-support-p96",
        "moduleId": "cell-0-support",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-support-p97",
        "moduleId": "cell-0-support",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-support-p98",
        "moduleId": "cell-0-support",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-support-p99",
        "moduleId": "cell-0-support",
        "shape": "beam",
        "color": "#dfebed"
      },
      {
        "id": "cell-0-elastic-tray-p100",
        "moduleId": "cell-0-elastic-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-elastic-tray-p101",
        "moduleId": "cell-0-elastic-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-elastic-tray-p102",
        "moduleId": "cell-0-elastic-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-elastic-tray-p103",
        "moduleId": "cell-0-elastic-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-elastic-tray-p104",
        "moduleId": "cell-0-elastic-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-elastic-tray-p105",
        "moduleId": "cell-0-elastic-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-elastic-tray-p106",
        "moduleId": "cell-0-elastic-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-elastic-tray-p107",
        "moduleId": "cell-0-elastic-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-elastic-tray-p108",
        "moduleId": "cell-0-elastic-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "cell-0-instrument-p109",
        "moduleId": "cell-0-instrument",
        "shape": "cylinder",
        "color": "#387bb3"
      },
      {
        "id": "cell-0-instrument-p110",
        "moduleId": "cell-0-instrument",
        "shape": "sphere",
        "color": "#dc6040"
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 颜色识别（h3-exp-d1-suspension-1-color）

零件 cell-0-elastic-tray-p100 的颜色值是什么？

能力：颜色识别；形式：single-choice；证据：model-state。

- A：#45a080
- B：#2878b8
- C：#d43a32
- D：#f2bf3c

```json
{
  "input": {
    "part": {
      "id": "cell-0-elastic-tray-p100",
      "moduleId": "cell-0-elastic-tray",
      "shape": "plate",
      "position": [
        -1,
        -0.050000000000000266,
        -1
      ],
      "size": [
        0.96,
        0.24,
        0.96
      ],
      "color": "#45a080",
      "rotation": [
        0,
        0,
        0,
        1
      ]
    }
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 三维位置（h3-exp-d1-suspension-1-position）

模块 cell-0-elastic-tray 的世界包围盒中心是什么？

能力：三维位置；形式：single-choice；证据：model-state。

- A：[0,0.2,0]
- B：[0,0.7,0]
- C：[0,3.125,-0.07499999999999996]
- D：[0,3,0]

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
      "cell-0-support": [
        0,
        3.125,
        -0.07499999999999996
      ],
      "cell-0-elastic-tray": [
        0,
        3,
        0
      ],
      "cell-0-instrument": [
        0,
        4,
        0
      ]
    }
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 关节类型（h3-exp-d1-suspension-1-joint-type）

cell-0-instrument-joint 采用什么约束类型？

能力：关节类型；形式：single-choice；证据：model-state。

- A：revolute
- B：fixed
- C：prismatic
- D：spring

```json
{
  "input": {
    "joint": {
      "id": "cell-0-instrument-joint",
      "name": "cell-0-instrument interface",
      "parent": "cell-0-elastic-tray",
      "child": "cell-0-instrument",
      "type": "revolute",
      "anchorParent": [
        0,
        0.75,
        0
      ],
      "anchorChild": [
        0,
        -0.25,
        0
      ],
      "axis": [
        0,
        1,
        0
      ],
      "limits": [
        -0.6,
        0.6
      ]
    }
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 直接连接（h3-exp-d1-suspension-1-parent）

cell-0-elastic-tray 的直接父模块集合是什么？

能力：直接连接；形式：single-choice；证据：model-state。

- A：["foundation","cell-0-mount","cell-0-support","cell-0-elastic-tray","cell-0-instrument"]
- B：["cell-0-support"]
- C：["cell-0-elastic-tray"]
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
        "id": "cell-0-support-joint",
        "name": "cell-0-support interface",
        "parent": "cell-0-mount",
        "child": "cell-0-support",
        "type": "fixed",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
        ],
        "anchorChild": [
          0,
          -1.825,
          0.07499999999999996
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-elastic-tray-joint",
        "name": "cell-0-elastic-tray interface",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "type": "spring",
        "anchorParent": [
          0,
          -0.17500000000000027,
          0.07499999999999996
        ],
        "anchorChild": [
          0,
          -0.050000000000000266,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "stiffness": 4000,
        "damping": 160,
        "restLength": 0
      },
      {
        "id": "cell-0-elastic-tray-elastic-1",
        "name": "Separated elastic support",
        "type": "spring",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "anchorParent": [
          -1,
          -0.17500000000000027,
          -0.925
        ],
        "anchorChild": [
          -1,
          -0.050000000000000266,
          -1
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "cell-0-elastic-tray-elastic-2",
        "name": "Separated elastic support",
        "type": "spring",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "anchorParent": [
          1,
          -0.17500000000000027,
          -0.925
        ],
        "anchorChild": [
          1,
          -0.050000000000000266,
          -1
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "cell-0-instrument-joint",
        "name": "cell-0-instrument interface",
        "parent": "cell-0-elastic-tray",
        "child": "cell-0-instrument",
        "type": "revolute",
        "anchorParent": [
          0,
          0.75,
          0
        ],
        "anchorChild": [
          0,
          -0.25,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 基座识别（h3-exp-d1-suspension-1-anchor）

哪些模块被声明为固定基座？

能力：基座识别；形式：single-choice；证据：model-state。

- A：["foundation","cell-0-mount","cell-0-support","cell-0-elastic-tray","cell-0-instrument"]
- B：["cell-0-elastic-tray"]
- C：["foundation"]
- D：[]

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
        "id": "cell-0-support",
        "name": "cell 0 support",
        "role": "structure",
        "anchored": false,
        "mass": 1.2,
        "position": [
          0,
          3.125,
          -0.07499999999999996
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-0-elastic-tray",
        "name": "cell 0 elastic tray",
        "role": "actuator",
        "anchored": false,
        "mass": 1.2,
        "position": [
          0,
          3,
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
        "id": "cell-0-instrument",
        "name": "cell 0 instrument",
        "role": "actuator",
        "anchored": false,
        "mass": 0.25,
        "position": [
          0,
          4,
          0
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
    "choiceId": "C"
  }
}
```

### 接口计数（h3-exp-d1-suspension-1-degree）

cell-0-elastic-tray 连接几个声明关节？平行关节分别计数。

能力：接口计数；形式：single-choice；证据：model-state。

- A：6
- B：4
- C：5
- D：3

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
        "id": "cell-0-support-joint",
        "name": "cell-0-support interface",
        "parent": "cell-0-mount",
        "child": "cell-0-support",
        "type": "fixed",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
        ],
        "anchorChild": [
          0,
          -1.825,
          0.07499999999999996
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-elastic-tray-joint",
        "name": "cell-0-elastic-tray interface",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "type": "spring",
        "anchorParent": [
          0,
          -0.17500000000000027,
          0.07499999999999996
        ],
        "anchorChild": [
          0,
          -0.050000000000000266,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "stiffness": 4000,
        "damping": 160,
        "restLength": 0
      },
      {
        "id": "cell-0-elastic-tray-elastic-1",
        "name": "Separated elastic support",
        "type": "spring",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "anchorParent": [
          -1,
          -0.17500000000000027,
          -0.925
        ],
        "anchorChild": [
          -1,
          -0.050000000000000266,
          -1
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "cell-0-elastic-tray-elastic-2",
        "name": "Separated elastic support",
        "type": "spring",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "anchorParent": [
          1,
          -0.17500000000000027,
          -0.925
        ],
        "anchorChild": [
          1,
          -0.050000000000000266,
          -1
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "cell-0-instrument-joint",
        "name": "cell-0-instrument interface",
        "parent": "cell-0-elastic-tray",
        "child": "cell-0-instrument",
        "type": "revolute",
        "anchorParent": [
          0,
          0.75,
          0
        ],
        "anchorChild": [
          0,
          -0.25,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 局部改色（h3-exp-d1-suspension-1-recolor）

仅将 cell-0-elastic-tray-p100 改成 #e8792e，其他零件不变。选择正确补丁。

能力：局部改色；形式：single-choice；证据：model-state。

- A：{"id":"*","color":"#e8792e"}
- B：{"id":"cell-0-elastic-tray-p100","color":"#e8792e"}
- C：{"id":"cell-0-elastic-tray-p101","color":"#e8792e"}
- D：{"id":"cell-0-elastic-tray-p100","color":"#2878b8"}

```json
{
  "input": {
    "part": {
      "id": "cell-0-elastic-tray-p100",
      "moduleId": "cell-0-elastic-tray",
      "shape": "plate",
      "position": [
        -1,
        -0.050000000000000266,
        -1
      ],
      "size": [
        0.96,
        0.24,
        0.96
      ],
      "color": "#45a080",
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

### 补装部件（h3-exp-d1-suspension-1-add）

模块 cell-0-elastic-tray 缺失零件 cell-0-elastic-tray-p100。选择与目标清单一致的补装描述。

能力：补装部件；形式：single-choice；证据：model-state。

- A：{"id":"cell-0-elastic-tray-p100","moduleId":"foundation","shape":"plate","position":[-1,-0.050000000000000266,-1],"size":[0.96,0.24,0.96],"color":"#45a080","rotation":[0,0,0,1]}
- B：{"id":"cell-0-elastic-tray-p100","moduleId":"cell-0-elastic-tray","shape":"plate","position":[-1,-0.050000000000000266,-1],"size":[3,3,3],"color":"#45a080","rotation":[0,0,0,1]}
- C：{"id":"cell-0-elastic-tray-p100","moduleId":"cell-0-elastic-tray","shape":"plate","position":[-1,-0.050000000000000266,-1],"size":[0.96,0.24,0.96],"color":"#000000","rotation":[0,0,0,1]}
- D：{"id":"cell-0-elastic-tray-p100","moduleId":"cell-0-elastic-tray","shape":"plate","position":[-1,-0.050000000000000266,-1],"size":[0.96,0.24,0.96],"color":"#45a080","rotation":[0,0,0,1]}

```json
{
  "input": {
    "targetPart": {
      "id": "cell-0-elastic-tray-p100",
      "moduleId": "cell-0-elastic-tray",
      "shape": "plate",
      "position": [
        -1,
        -0.050000000000000266,
        -1
      ],
      "size": [
        0.96,
        0.24,
        0.96
      ],
      "color": "#45a080",
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
      "cell-0-support-p86",
      "cell-0-support-p87",
      "cell-0-support-p88",
      "cell-0-support-p89",
      "cell-0-support-p90",
      "cell-0-support-p91",
      "cell-0-support-p92",
      "cell-0-support-p93",
      "cell-0-support-p94",
      "cell-0-support-p95",
      "cell-0-support-p96",
      "cell-0-support-p97",
      "cell-0-support-p98",
      "cell-0-support-p99",
      "cell-0-elastic-tray-p101",
      "cell-0-elastic-tray-p102",
      "cell-0-elastic-tray-p103",
      "cell-0-elastic-tray-p104",
      "cell-0-elastic-tray-p105",
      "cell-0-elastic-tray-p106",
      "cell-0-elastic-tray-p107",
      "cell-0-elastic-tray-p108",
      "cell-0-instrument-p109",
      "cell-0-instrument-p110"
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 安全拆除（h3-exp-d1-suspension-1-remove）

按声明依赖图，当前可以先拆哪些叶模块？

能力：安全拆除；形式：single-choice；证据：model-state。

- A：["foundation","cell-0-mount","cell-0-support","cell-0-elastic-tray","cell-0-instrument"]
- B：["cell-0-instrument"]
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
        "id": "cell-0-support-joint",
        "name": "cell-0-support interface",
        "parent": "cell-0-mount",
        "child": "cell-0-support",
        "type": "fixed",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
        ],
        "anchorChild": [
          0,
          -1.825,
          0.07499999999999996
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-elastic-tray-joint",
        "name": "cell-0-elastic-tray interface",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "type": "spring",
        "anchorParent": [
          0,
          -0.17500000000000027,
          0.07499999999999996
        ],
        "anchorChild": [
          0,
          -0.050000000000000266,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "stiffness": 4000,
        "damping": 160,
        "restLength": 0
      },
      {
        "id": "cell-0-elastic-tray-elastic-1",
        "name": "Separated elastic support",
        "type": "spring",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "anchorParent": [
          -1,
          -0.17500000000000027,
          -0.925
        ],
        "anchorChild": [
          -1,
          -0.050000000000000266,
          -1
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "cell-0-elastic-tray-elastic-2",
        "name": "Separated elastic support",
        "type": "spring",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "anchorParent": [
          1,
          -0.17500000000000027,
          -0.925
        ],
        "anchorChild": [
          1,
          -0.050000000000000266,
          -1
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "cell-0-instrument-joint",
        "name": "cell-0-instrument interface",
        "parent": "cell-0-elastic-tray",
        "child": "cell-0-instrument",
        "type": "revolute",
        "anchorParent": [
          0,
          0.75,
          0
        ],
        "anchorChild": [
          0,
          -0.25,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      }
    ],
    "modules": [
      "foundation",
      "cell-0-mount",
      "cell-0-support",
      "cell-0-elastic-tray",
      "cell-0-instrument"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 替换选择（h3-exp-d1-suspension-1-replace）

在成本上限内选择刚度最大的替换件；并列选成本低者，再并列选ID字典序最小者。

能力：替换选择；形式：single-choice；证据：model-state。

- A：stock-0
- B：stock-2
- C：stock-3
- D：stock-1

```json
{
  "input": {
    "alternatives": [
      {
        "id": "stock-0",
        "cost": 7,
        "stiffness": 9,
        "mass": 0.5
      },
      {
        "id": "stock-1",
        "cost": 7,
        "stiffness": 11,
        "mass": 1.2
      },
      {
        "id": "stock-2",
        "cost": 4,
        "stiffness": 3,
        "mass": 0.8
      },
      {
        "id": "stock-3",
        "cost": 5,
        "stiffness": 7,
        "mass": 1
      }
    ],
    "maxCost": 8
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 平移纠偏（h3-exp-d1-suspension-1-translate）

观察到相对目标的平移误差 delta，选择补偿平移。

能力：平移纠偏；形式：single-choice；证据：model-state。

- A：[0,0,0]
- B：[0,2,0]
- C：[-1,0,2]
- D：[1,0,-2]

```json
{
  "input": {
    "delta": [
      1,
      0,
      -2
    ],
    "target": "cell-0-elastic-tray"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 姿态纠偏（h3-exp-d1-suspension-1-rotate）

选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。

能力：姿态纠偏；形式：single-choice；证据：model-state。

- A：90
- B：-135
- C：135
- D：0

```json
{
  "input": {
    "module": "cell-0-elastic-tray",
    "currentYaw": 45,
    "targetYaw": 270
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 下一步放置（h3-exp-d1-suspension-1-next-module）

已完成给定前缀，选择所有前置依赖已满足的下一模块集合。

能力：下一步放置；形式：single-choice；证据：model-state。

- A：["cell-0-elastic-tray","cell-0-instrument"]
- B：["cell-0-elastic-tray"]
- C：[]
- D：["foundation","cell-0-mount","cell-0-support"]

```json
{
  "input": {
    "prefix": [
      "foundation",
      "cell-0-mount",
      "cell-0-support"
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
        "id": "cell-0-support-joint",
        "name": "cell-0-support interface",
        "parent": "cell-0-mount",
        "child": "cell-0-support",
        "type": "fixed",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
        ],
        "anchorChild": [
          0,
          -1.825,
          0.07499999999999996
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-elastic-tray-joint",
        "name": "cell-0-elastic-tray interface",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "type": "spring",
        "anchorParent": [
          0,
          -0.17500000000000027,
          0.07499999999999996
        ],
        "anchorChild": [
          0,
          -0.050000000000000266,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "stiffness": 4000,
        "damping": 160,
        "restLength": 0
      },
      {
        "id": "cell-0-elastic-tray-elastic-1",
        "name": "Separated elastic support",
        "type": "spring",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "anchorParent": [
          -1,
          -0.17500000000000027,
          -0.925
        ],
        "anchorChild": [
          -1,
          -0.050000000000000266,
          -1
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "cell-0-elastic-tray-elastic-2",
        "name": "Separated elastic support",
        "type": "spring",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "anchorParent": [
          1,
          -0.17500000000000027,
          -0.925
        ],
        "anchorChild": [
          1,
          -0.050000000000000266,
          -1
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "cell-0-instrument-joint",
        "name": "cell-0-instrument interface",
        "parent": "cell-0-elastic-tray",
        "child": "cell-0-instrument",
        "type": "revolute",
        "anchorParent": [
          0,
          0.75,
          0
        ],
        "anchorChild": [
          0,
          -0.25,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      }
    ],
    "modules": [
      "foundation",
      "cell-0-mount",
      "cell-0-support",
      "cell-0-elastic-tray",
      "cell-0-instrument"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 库存核算（h3-exp-d1-suspension-1-inventory）

备件库有 17 件，替换模块需 9 件，还剩多少？

能力：库存核算；形式：single-choice；证据：model-state。

- A：9
- B：7
- C：11
- D：8

```json
{
  "input": {
    "available": 17,
    "required": 9
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 子装配边界（h3-exp-d1-suspension-1-boundary）

隔离 cell-0-elastic-tray 需要断开哪些边界关节？

能力：子装配边界；形式：single-choice；证据：model-state。

- A：["cell-0-instrument-joint"]
- B：["cell-0-elastic-tray-elastic-1","cell-0-elastic-tray-elastic-2","cell-0-elastic-tray-joint","cell-0-instrument-joint"]
- C：[]
- D：["cell-0-mount-joint","cell-0-support-joint","cell-0-elastic-tray-joint","cell-0-elastic-tray-elastic-1","cell-0-elastic-tray-elastic-2","cell-0-instrument-joint"]

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
        "id": "cell-0-support-joint",
        "name": "cell-0-support interface",
        "parent": "cell-0-mount",
        "child": "cell-0-support",
        "type": "fixed",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
        ],
        "anchorChild": [
          0,
          -1.825,
          0.07499999999999996
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-elastic-tray-joint",
        "name": "cell-0-elastic-tray interface",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "type": "spring",
        "anchorParent": [
          0,
          -0.17500000000000027,
          0.07499999999999996
        ],
        "anchorChild": [
          0,
          -0.050000000000000266,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "stiffness": 4000,
        "damping": 160,
        "restLength": 0
      },
      {
        "id": "cell-0-elastic-tray-elastic-1",
        "name": "Separated elastic support",
        "type": "spring",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "anchorParent": [
          -1,
          -0.17500000000000027,
          -0.925
        ],
        "anchorChild": [
          -1,
          -0.050000000000000266,
          -1
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "cell-0-elastic-tray-elastic-2",
        "name": "Separated elastic support",
        "type": "spring",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "anchorParent": [
          1,
          -0.17500000000000027,
          -0.925
        ],
        "anchorChild": [
          1,
          -0.050000000000000266,
          -1
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "cell-0-instrument-joint",
        "name": "cell-0-instrument interface",
        "parent": "cell-0-elastic-tray",
        "child": "cell-0-instrument",
        "type": "revolute",
        "anchorParent": [
          0,
          0.75,
          0
        ],
        "anchorChild": [
          0,
          -0.25,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      }
    ],
    "target": "cell-0-elastic-tray"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 最小干预（h3-exp-d1-suspension-1-no-op）

当前模块颜色已满足指令，且无需改变位姿。最少需要几次编辑？

能力：最小干预；形式：single-choice；证据：model-state。

- A：1
- B：2
- C：9
- D：0

```json
{
  "input": {
    "module": "cell-0-elastic-tray"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 全过程依赖（h3-exp-d1-suspension-1-prefix）

给定候选顺序，首次违反前置依赖的步骤是？从 0 编号，-1 表示没有违反。

能力：全过程依赖；形式：single-choice；证据：support-graph。

- A：-1
- B：2
- C：4
- D：1

```json
{
  "input": {
    "order": [
      "foundation",
      "cell-0-support",
      "cell-0-mount",
      "cell-0-elastic-tray",
      "cell-0-instrument"
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
        "id": "cell-0-support-joint",
        "name": "cell-0-support interface",
        "parent": "cell-0-mount",
        "child": "cell-0-support",
        "type": "fixed",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
        ],
        "anchorChild": [
          0,
          -1.825,
          0.07499999999999996
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-elastic-tray-joint",
        "name": "cell-0-elastic-tray interface",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "type": "spring",
        "anchorParent": [
          0,
          -0.17500000000000027,
          0.07499999999999996
        ],
        "anchorChild": [
          0,
          -0.050000000000000266,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "stiffness": 4000,
        "damping": 160,
        "restLength": 0
      },
      {
        "id": "cell-0-elastic-tray-elastic-1",
        "name": "Separated elastic support",
        "type": "spring",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "anchorParent": [
          -1,
          -0.17500000000000027,
          -0.925
        ],
        "anchorChild": [
          -1,
          -0.050000000000000266,
          -1
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "cell-0-elastic-tray-elastic-2",
        "name": "Separated elastic support",
        "type": "spring",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "anchorParent": [
          1,
          -0.17500000000000027,
          -0.925
        ],
        "anchorChild": [
          1,
          -0.050000000000000266,
          -1
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "cell-0-instrument-joint",
        "name": "cell-0-instrument interface",
        "parent": "cell-0-elastic-tray",
        "child": "cell-0-instrument",
        "type": "revolute",
        "anchorParent": [
          0,
          0.75,
          0
        ],
        "anchorChild": [
          0,
          -0.25,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 连续维修路径（h3-exp-d1-suspension-1-access）

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
          3,
          0
        ],
        "end": [
          0,
          3,
          0
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
          8.95,
          0
        ],
        "end": [
          0,
          3,
          0
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": false,
        "timeOfImpact": 0.6924370527267456
      },
      {
        "id": "path-2",
        "start": [
          0,
          3,
          7.48
        ],
        "end": [
          0,
          3,
          0
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

### 支撑反事实（h3-exp-d1-suspension-1-counterfactual）

移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。

能力：支撑反事实；形式：single-choice；证据：support-graph。

- A：["cell-0-elastic-tray","cell-0-instrument","cell-0-support"]
- B：["cell-0-mount"]
- C：[]
- D：["foundation","cell-0-mount","cell-0-support","cell-0-elastic-tray","cell-0-instrument"]

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
        "id": "cell-0-support-joint",
        "name": "cell-0-support interface",
        "parent": "cell-0-mount",
        "child": "cell-0-support",
        "type": "fixed",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
        ],
        "anchorChild": [
          0,
          -1.825,
          0.07499999999999996
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-elastic-tray-joint",
        "name": "cell-0-elastic-tray interface",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "type": "spring",
        "anchorParent": [
          0,
          -0.17500000000000027,
          0.07499999999999996
        ],
        "anchorChild": [
          0,
          -0.050000000000000266,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "stiffness": 4000,
        "damping": 160,
        "restLength": 0
      },
      {
        "id": "cell-0-elastic-tray-elastic-1",
        "name": "Separated elastic support",
        "type": "spring",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "anchorParent": [
          -1,
          -0.17500000000000027,
          -0.925
        ],
        "anchorChild": [
          -1,
          -0.050000000000000266,
          -1
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "cell-0-elastic-tray-elastic-2",
        "name": "Separated elastic support",
        "type": "spring",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "anchorParent": [
          1,
          -0.17500000000000027,
          -0.925
        ],
        "anchorChild": [
          1,
          -0.050000000000000266,
          -1
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "cell-0-instrument-joint",
        "name": "cell-0-instrument interface",
        "parent": "cell-0-elastic-tray",
        "child": "cell-0-instrument",
        "type": "revolute",
        "anchorParent": [
          0,
          0.75,
          0
        ],
        "anchorChild": [
          0,
          -0.25,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      }
    ],
    "modules": [
      "foundation",
      "cell-0-mount",
      "cell-0-support",
      "cell-0-elastic-tray",
      "cell-0-instrument"
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 冲击响应读数（h3-exp-d1-suspension-1-dynamic）

Rapier 实际采样轨迹中的最大平移位移是多少？按四位小数报告。

能力：冲击响应读数；形式：single-choice；证据：Rapier。

- A：0.0233
- B：0.2233
- C：0
- D：1.0233

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.0232513999841845
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.01586732875018424
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.010191893381138899
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.0059778121567880885
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.002763401870029097
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.0008626470199087201
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.00017404757503389608
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.00023480723905347237
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.00004715564515684885
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.000054628016617772
      },
      {
        "time": 1,
        "displacement": 0.00008302074132367934
      }
    ],
    "impulse": [
      10,
      1.8,
      3.5
    ],
    "nominalDrift": 0.005156034089523584,
    "scope": "采样轨迹极值，非连续时间极值；不代表实物安全阈值"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 关节限位推理（h3-exp-d1-suspension-1-kinematic）

下列目标位置/角度中哪些在关节声明限位内（含边界）？

能力：关节限位推理；形式：multiple-choice；证据：model-state。

- A：-0.6
- B：0
- C：-1.1
- D：1.1

```json
{
  "input": {
    "joint": "cell-0-instrument-joint",
    "limits": [
      -0.6,
      0.6
    ],
    "units": "radians"
  },
  "answer": {
    "choiceIds": [
      "A",
      "B"
    ]
  }
}
```

### 约束故障诊断（h3-exp-d1-suspension-1-diagnosis）

已检测到端点和约束类型如下，选择匹配的全部关节。

能力：约束故障诊断；形式：multiple-choice；证据：model-state。

- A：cell-0-elastic-tray-elastic-2
- B：cell-0-mount-joint
- C：cell-0-support-joint
- D：cell-0-instrument-joint
- O5：cell-0-elastic-tray-joint
- O6：cell-0-elastic-tray-elastic-1

```json
{
  "input": {
    "endpoints": [
      "cell-0-support",
      "cell-0-elastic-tray"
    ],
    "type": "spring",
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
        "id": "cell-0-support-joint",
        "name": "cell-0-support interface",
        "parent": "cell-0-mount",
        "child": "cell-0-support",
        "type": "fixed",
        "anchorParent": [
          0,
          0.6000000000000001,
          0
        ],
        "anchorChild": [
          0,
          -1.825,
          0.07499999999999996
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "cell-0-elastic-tray-joint",
        "name": "cell-0-elastic-tray interface",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "type": "spring",
        "anchorParent": [
          0,
          -0.17500000000000027,
          0.07499999999999996
        ],
        "anchorChild": [
          0,
          -0.050000000000000266,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "stiffness": 4000,
        "damping": 160,
        "restLength": 0
      },
      {
        "id": "cell-0-elastic-tray-elastic-1",
        "name": "Separated elastic support",
        "type": "spring",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "anchorParent": [
          -1,
          -0.17500000000000027,
          -0.925
        ],
        "anchorChild": [
          -1,
          -0.050000000000000266,
          -1
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "cell-0-elastic-tray-elastic-2",
        "name": "Separated elastic support",
        "type": "spring",
        "parent": "cell-0-support",
        "child": "cell-0-elastic-tray",
        "anchorParent": [
          1,
          -0.17500000000000027,
          -0.925
        ],
        "anchorChild": [
          1,
          -0.050000000000000266,
          -1
        ],
        "restLength": 0,
        "stiffness": 4000,
        "damping": 160
      },
      {
        "id": "cell-0-instrument-joint",
        "name": "cell-0-instrument interface",
        "parent": "cell-0-elastic-tray",
        "child": "cell-0-instrument",
        "type": "revolute",
        "anchorParent": [
          0,
          0.75,
          0
        ],
        "anchorChild": [
          0,
          -0.25,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.6,
          0.6
        ]
      }
    ]
  },
  "answer": {
    "choiceIds": [
      "A",
      "O5",
      "O6"
    ]
  }
}
```

### 主动检查收益（h3-exp-d1-suspension-1-information-gain）

均匀先验四个世界，选择信息增益/成本最大的全部检查。

能力：主动检查收益；形式：multiple-choice；证据：finite-world。

- A：query-0
- B：query-2
- C：query-1

```json
{
  "input": {
    "queries": [
      {
        "id": "query-0",
        "cost": 3,
        "returns": [
          0,
          0,
          1,
          1
        ]
      },
      {
        "id": "query-1",
        "cost": 1,
        "returns": [
          0,
          1,
          2,
          3
        ]
      },
      {
        "id": "query-2",
        "cost": 2,
        "returns": [
          0,
          0,
          0,
          1
        ]
      }
    ],
    "module": "cell-0-elastic-tray",
    "worlds": [
      "normal",
      "jammed",
      "reversed",
      "loose"
    ]
  },
  "answer": {
    "choiceIds": [
      "C"
    ]
  }
}
```

### 不确定性与弃答（h3-exp-d1-suspension-1-abstention）

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
        "action": "continue"
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 观测后信念更新（h3-exp-d1-suspension-1-posterior）

均匀先验，得到给定观测后，jammed 世界的后验概率是多少？

能力：观测后信念更新；形式：single-choice；证据：finite-world。

- A：0.5
- B：0.3333333333333333
- C：0
- D：0.25

```json
{
  "input": {
    "module": "cell-0-elastic-tray",
    "worlds": [
      "normal",
      "jammed",
      "reversed",
      "loose"
    ],
    "observationByWorld": [
      "positive",
      "negative",
      "negative",
      "negative"
    ],
    "observed": "negative"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 多目标工程权衡（h3-exp-d1-suspension-1-pareto）

最小成本、最小质量、最大刚度，选择完整非支配集合。

能力：多目标工程权衡；形式：multiple-choice；证据：model-state。

- A：stock-0
- B：stock-1
- C：stock-2
- D：stock-3

```json
{
  "input": {
    "alternatives": [
      {
        "id": "stock-0",
        "cost": 7,
        "stiffness": 9,
        "mass": 0.5
      },
      {
        "id": "stock-1",
        "cost": 7,
        "stiffness": 11,
        "mass": 1.2
      },
      {
        "id": "stock-2",
        "cost": 4,
        "stiffness": 3,
        "mass": 0.8
      },
      {
        "id": "stock-3",
        "cost": 5,
        "stiffness": 7,
        "mass": 1
      }
    ]
  },
  "answer": {
    "choiceIds": [
      "A",
      "B",
      "C",
      "D"
    ]
  }
}
```

### 依赖装配（h3-exp-d1-suspension-1-assembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖装配；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [],
    "initialModules": [],
    "actions": [
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
      },
      {
        "id": "place:cell-0-elastic-tray",
        "label": "安装 cell-0-elastic-tray",
        "requires": [
          "present:cell-0-support",
          "present:cell-0-support",
          "present:cell-0-support"
        ],
        "forbids": [
          "present:cell-0-elastic-tray"
        ],
        "adds": [
          "present:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray",
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
        "id": "place:cell-0-instrument",
        "label": "安装 cell-0-instrument",
        "requires": [
          "present:cell-0-elastic-tray"
        ],
        "forbids": [
          "present:cell-0-instrument"
        ],
        "adds": [
          "present:cell-0-instrument"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-instrument",
          "visible": true
        }
      },
      {
        "id": "place:cell-0-support",
        "label": "安装 cell-0-support",
        "requires": [
          "present:cell-0-mount"
        ],
        "forbids": [
          "present:cell-0-support"
        ],
        "adds": [
          "present:cell-0-support"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-support",
          "visible": true
        }
      }
    ],
    "goalFacts": [
      "present:foundation",
      "present:cell-0-mount",
      "present:cell-0-support",
      "present:cell-0-elastic-tray",
      "present:cell-0-instrument"
    ],
    "budget": 5,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "place:foundation",
      "place:cell-0-mount",
      "place:cell-0-support",
      "place:cell-0-elastic-tray",
      "place:cell-0-instrument"
    ]
  }
}
```

### 依赖拆解（h3-exp-d1-suspension-1-disassembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖拆解；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "present:foundation",
      "present:cell-0-mount",
      "present:cell-0-support",
      "present:cell-0-elastic-tray",
      "present:cell-0-instrument"
    ],
    "initialModules": [
      "foundation",
      "cell-0-mount",
      "cell-0-support",
      "cell-0-elastic-tray",
      "cell-0-instrument"
    ],
    "actions": [
      {
        "id": "remove:cell-0-support",
        "label": "拆除 cell-0-support",
        "requires": [
          "present:cell-0-support"
        ],
        "forbids": [
          "present:cell-0-elastic-tray",
          "present:cell-0-elastic-tray",
          "present:cell-0-elastic-tray"
        ],
        "adds": [
          "removed:cell-0-support"
        ],
        "deletes": [
          "present:cell-0-support"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-support",
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
          "present:cell-0-support"
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
      },
      {
        "id": "remove:cell-0-instrument",
        "label": "拆除 cell-0-instrument",
        "requires": [
          "present:cell-0-instrument"
        ],
        "forbids": [],
        "adds": [
          "removed:cell-0-instrument"
        ],
        "deletes": [
          "present:cell-0-instrument"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-instrument",
          "visible": false
        }
      },
      {
        "id": "remove:cell-0-elastic-tray",
        "label": "拆除 cell-0-elastic-tray",
        "requires": [
          "present:cell-0-elastic-tray"
        ],
        "forbids": [
          "present:cell-0-instrument"
        ],
        "adds": [
          "removed:cell-0-elastic-tray"
        ],
        "deletes": [
          "present:cell-0-elastic-tray"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray",
          "visible": false
        }
      }
    ],
    "goalFacts": [
      "removed:cell-0-instrument",
      "removed:cell-0-elastic-tray",
      "removed:cell-0-support",
      "removed:cell-0-mount",
      "removed:foundation"
    ],
    "budget": 5,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "remove:cell-0-instrument",
      "remove:cell-0-elastic-tray",
      "remove:cell-0-support",
      "remove:cell-0-mount",
      "remove:foundation"
    ]
  }
}
```

### 承载维修（h3-exp-d1-suspension-1-service-repair）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：承载维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:cell-0-elastic-tray",
      "closed:cell-0-elastic-tray"
    ],
    "initialModules": [
      "foundation",
      "cell-0-mount",
      "cell-0-support",
      "cell-0-elastic-tray",
      "cell-0-instrument"
    ],
    "actions": [
      {
        "id": "replace:cell-0-elastic-tray",
        "label": "replace cell-0-elastic-tray",
        "requires": [
          "done:remove:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:replace:cell-0-elastic-tray"
        ],
        "adds": [
          "done:replace:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray",
          "visible": true
        }
      },
      {
        "id": "support:cell-0-elastic-tray",
        "label": "support cell-0-elastic-tray",
        "requires": [
          "fault:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:support:cell-0-elastic-tray"
        ],
        "adds": [
          "done:support:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "open:cell-0-elastic-tray",
        "label": "open cell-0-elastic-tray",
        "requires": [
          "done:support:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:open:cell-0-elastic-tray"
        ],
        "adds": [
          "done:open:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "close:cell-0-elastic-tray",
        "label": "close cell-0-elastic-tray",
        "requires": [
          "done:verify:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:close:cell-0-elastic-tray"
        ],
        "adds": [
          "done:close:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "verify:cell-0-elastic-tray",
        "label": "verify cell-0-elastic-tray",
        "requires": [
          "done:replace:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:verify:cell-0-elastic-tray"
        ],
        "adds": [
          "done:verify:cell-0-elastic-tray"
        ],
        "deletes": [
          "fault:cell-0-elastic-tray"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "remove:cell-0-elastic-tray",
        "label": "remove cell-0-elastic-tray",
        "requires": [
          "done:open:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:remove:cell-0-elastic-tray"
        ],
        "adds": [
          "done:remove:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray",
          "visible": false
        }
      },
      {
        "id": "release:cell-0-elastic-tray",
        "label": "release cell-0-elastic-tray",
        "requires": [
          "done:close:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:release:cell-0-elastic-tray"
        ],
        "adds": [
          "done:release:cell-0-elastic-tray",
          "repaired:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      }
    ],
    "goalFacts": [
      "repaired:cell-0-elastic-tray"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:cell-0-elastic-tray",
      "open:cell-0-elastic-tray",
      "remove:cell-0-elastic-tray",
      "replace:cell-0-elastic-tray",
      "verify:cell-0-elastic-tray",
      "close:cell-0-elastic-tray",
      "release:cell-0-elastic-tray"
    ]
  }
}
```

### 复合编辑验证（h3-exp-d1-suspension-1-compound-edit）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：复合编辑验证；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:cell-0-elastic-tray",
      "closed:cell-0-elastic-tray"
    ],
    "initialModules": [
      "foundation",
      "cell-0-mount",
      "cell-0-support",
      "cell-0-elastic-tray",
      "cell-0-instrument"
    ],
    "actions": [
      {
        "id": "support:cell-0-elastic-tray",
        "label": "support cell-0-elastic-tray",
        "requires": [
          "fault:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:support:cell-0-elastic-tray"
        ],
        "adds": [
          "done:support:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "open:cell-0-elastic-tray",
        "label": "open cell-0-elastic-tray",
        "requires": [
          "done:support:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:open:cell-0-elastic-tray"
        ],
        "adds": [
          "done:open:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "recolor:cell-0-elastic-tray",
        "label": "recolor cell-0-elastic-tray",
        "requires": [
          "done:open:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:recolor:cell-0-elastic-tray"
        ],
        "adds": [
          "done:recolor:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray",
          "color": "#ea7635"
        }
      },
      {
        "id": "close:cell-0-elastic-tray",
        "label": "close cell-0-elastic-tray",
        "requires": [
          "done:verify:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:close:cell-0-elastic-tray"
        ],
        "adds": [
          "done:close:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "verify:cell-0-elastic-tray",
        "label": "verify cell-0-elastic-tray",
        "requires": [
          "done:recolor:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:verify:cell-0-elastic-tray"
        ],
        "adds": [
          "done:verify:cell-0-elastic-tray"
        ],
        "deletes": [
          "fault:cell-0-elastic-tray"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "release:cell-0-elastic-tray",
        "label": "release cell-0-elastic-tray",
        "requires": [
          "done:close:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:release:cell-0-elastic-tray"
        ],
        "adds": [
          "done:release:cell-0-elastic-tray",
          "repaired:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      }
    ],
    "goalFacts": [
      "repaired:cell-0-elastic-tray"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:cell-0-elastic-tray",
      "open:cell-0-elastic-tray",
      "recolor:cell-0-elastic-tray",
      "verify:cell-0-elastic-tray",
      "close:cell-0-elastic-tray",
      "release:cell-0-elastic-tray"
    ]
  }
}
```

### 跨区域联合维修（h3-exp-d1-suspension-1-multi-fault）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：跨区域联合维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:cell-0-instrument",
      "closed:cell-0-instrument"
    ],
    "initialModules": [
      "foundation",
      "cell-0-mount",
      "cell-0-support",
      "cell-0-elastic-tray",
      "cell-0-instrument"
    ],
    "actions": [
      {
        "id": "replace:cell-0-instrument",
        "label": "replace cell-0-instrument",
        "requires": [
          "done:remove:cell-0-instrument"
        ],
        "forbids": [
          "done:replace:cell-0-instrument"
        ],
        "adds": [
          "done:replace:cell-0-instrument"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-instrument",
          "visible": true
        }
      },
      {
        "id": "open:cell-0-instrument",
        "label": "open cell-0-instrument",
        "requires": [
          "done:support:cell-0-instrument"
        ],
        "forbids": [
          "done:open:cell-0-instrument"
        ],
        "adds": [
          "done:open:cell-0-instrument"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-instrument"
        }
      },
      {
        "id": "verify:cell-0-instrument",
        "label": "verify cell-0-instrument",
        "requires": [
          "done:replace:cell-0-instrument"
        ],
        "forbids": [
          "done:verify:cell-0-instrument"
        ],
        "adds": [
          "done:verify:cell-0-instrument"
        ],
        "deletes": [
          "fault:cell-0-instrument"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-instrument"
        }
      },
      {
        "id": "release:cell-0-instrument",
        "label": "release cell-0-instrument",
        "requires": [
          "done:close:cell-0-instrument"
        ],
        "forbids": [
          "done:release:cell-0-instrument"
        ],
        "adds": [
          "done:release:cell-0-instrument",
          "repaired:cell-0-instrument"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-instrument"
        }
      },
      {
        "id": "close:cell-0-instrument",
        "label": "close cell-0-instrument",
        "requires": [
          "done:verify:cell-0-instrument"
        ],
        "forbids": [
          "done:close:cell-0-instrument"
        ],
        "adds": [
          "done:close:cell-0-instrument"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-instrument"
        }
      },
      {
        "id": "support:cell-0-instrument",
        "label": "support cell-0-instrument",
        "requires": [
          "fault:cell-0-instrument"
        ],
        "forbids": [
          "done:support:cell-0-instrument"
        ],
        "adds": [
          "done:support:cell-0-instrument"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-instrument"
        }
      },
      {
        "id": "remove:cell-0-instrument",
        "label": "remove cell-0-instrument",
        "requires": [
          "done:open:cell-0-instrument"
        ],
        "forbids": [
          "done:remove:cell-0-instrument"
        ],
        "adds": [
          "done:remove:cell-0-instrument"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-instrument",
          "visible": false
        }
      }
    ],
    "goalFacts": [
      "repaired:cell-0-instrument"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:cell-0-instrument",
      "open:cell-0-instrument",
      "remove:cell-0-instrument",
      "replace:cell-0-instrument",
      "verify:cell-0-instrument",
      "close:cell-0-instrument",
      "release:cell-0-instrument"
    ]
  }
}
```

### 多工位资源调度（h3-exp-d1-suspension-1-scheduling）

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
        "module": "cell-0-support",
        "duration": 3,
        "resource": "test-bench",
        "after": [
          "job-0"
        ]
      },
      {
        "id": "job-3",
        "module": "cell-0-elastic-tray",
        "duration": 1,
        "resource": "technician",
        "after": [
          "job-1"
        ]
      }
    ],
    "deadline": 4
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

### 检查后条件策略（h3-exp-d1-suspension-1-policy）

提交一个检查及 observation→action 决策表，在所有相容世界中采取正确动作。

能力：检查后条件策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "cell-0-elastic-tray",
    "worlds": [
      {
        "id": "normal",
        "action": "replace"
      },
      {
        "id": "loose",
        "action": "continue"
      },
      {
        "id": "jammed",
        "action": "tighten"
      }
    ],
    "budget": 3,
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
          "normal": "same",
          "loose": "same",
          "jammed": "other"
        }
      },
      {
        "id": "thermal",
        "cost": 3,
        "returns": {
          "normal": "signal-0",
          "loose": "signal-1",
          "jammed": "signal-2"
        }
      }
    ]
  },
  "answer": {
    "queryId": "thermal",
    "decisions": {
      "signal-0": "replace",
      "signal-1": "continue",
      "signal-2": "tighten"
    }
  }
}
```

### 局部坐标变换（h3-exp-d1-suspension-1-local-frame）

将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。

能力：局部坐标变换；形式：single-choice；证据：model-state。

- A：[0,2.95,-1]
- B：[0,3.95,1]
- C：[-1,2.95,0]
- D：[0,-0.05,-1]

```json
{
  "input": {
    "localPoint": [
      0,
      -0.050000000000000266,
      -1
    ],
    "rotationXYZW": [
      0,
      0.7071067811865475,
      0,
      0.7071067811865476
    ],
    "translation": [
      0,
      3,
      0
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 正交视图投影（h3-exp-d1-suspension-1-projection）

按公开视图坐标约定，选择该世界点投影后的二维坐标。

能力：正交视图投影；形式：single-choice；证据：model-state。

- A：[2,3]
- B：[0,0]
- C：[2,-3]
- D：[5,2]

```json
{
  "input": {
    "view": "top",
    "point": [
      2,
      5,
      -3
    ],
    "convention": "front=(x,y), side=(z,y), top=(x,z)"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 空间相对关系（h3-exp-d1-suspension-1-relative-order）

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
      "id": "cell-0-instrument",
      "position": [
        0,
        4,
        0
      ]
    },
    "axis": "z"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 约束自由度（h3-exp-d1-suspension-1-joint-axis）

仅考虑这一声明约束，不计闭环、马达与限位激活，保留多少相对运动自由度？弹簧仅施力、不消除自由度。

能力：约束自由度；形式：single-choice；证据：model-state。

- A：3
- B：6
- C：1
- D：0

```json
{
  "input": {
    "joint": {
      "id": "cell-0-instrument-joint",
      "name": "cell-0-instrument interface",
      "parent": "cell-0-elastic-tray",
      "child": "cell-0-instrument",
      "type": "revolute",
      "anchorParent": [
        0,
        0.75,
        0
      ],
      "anchorChild": [
        0,
        -0.25,
        0
      ],
      "axis": [
        0,
        1,
        0
      ],
      "limits": [
        -0.6,
        0.6
      ]
    }
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 维修间隙预算（h3-exp-d1-suspension-1-clearance-margin）

给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？

能力：维修间隙预算；形式：single-choice；证据：model-state。

- A：feasible
- B：blocked

```json
{
  "input": {
    "module": "cell-0-elastic-tray",
    "aperture": 0.5900000000000001,
    "toolWidth": 0.35,
    "eachSideMargin": 0.1
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 载荷力矩（h3-exp-d1-suspension-1-load-moment）

绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。

能力：载荷力矩；形式：single-choice；证据：model-state。

- A：[0,-1,0]
- B：[0,0,-3]
- C：[0,0,3]
- D：[0,0,0]

```json
{
  "input": {
    "module": "cell-0-elastic-tray",
    "lever": [
      1,
      3,
      0
    ],
    "force": [
      0,
      -3,
      0
    ],
    "units": "scene-length × force"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 非均匀先验更新（h3-exp-d1-suspension-1-weighted-posterior）

先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。

能力：非均匀先验更新；形式：single-choice；证据：finite-world。

- A：1
- B：0.7142857142857143
- C：0.5555555555555556
- D：0

```json
{
  "input": {
    "module": "cell-0-elastic-tray",
    "worlds": [
      "normal",
      "jammed",
      "loose"
    ],
    "weights": [
      2,
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

### 风险最小决策（h3-exp-d1-suspension-1-expected-loss）

继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。

能力：风险最小决策；形式：single-choice；证据：finite-world。

- A：repair
- B：continue

```json
{
  "input": {
    "faultProbability": 0.2,
    "repairCost": 3,
    "failureLoss": 7,
    "module": "cell-0-elastic-tray"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 轨迹阈值判定（h3-exp-d1-suspension-1-trace-threshold）

实际采样轨迹中是否有位移严格超过给定阈值？只评价采样点。

能力：轨迹阈值判定；形式：single-choice；证据：Rapier。

- A：within
- B：exceeded

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.0232513999841845
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.01586732875018424
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.010191893381138899
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.0059778121567880885
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.002763401870029097
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.0008626470199087201
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.00017404757503389608
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.00023480723905347237
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.00004715564515684885
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.000054628016617772
      },
      {
        "time": 1,
        "displacement": 0.00008302074132367934
      }
    ],
    "threshold": 0.027901679981021398
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 安全联锁维修（h3-exp-d1-suspension-1-guarded-repair）

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
        "id": "release:cell-0-elastic-tray",
        "label": "release cell-0-elastic-tray",
        "requires": [
          "done:relock:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:release:cell-0-elastic-tray"
        ],
        "adds": [
          "done:release:cell-0-elastic-tray",
          "ready:cell-0-elastic-tray",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "relock:cell-0-elastic-tray",
        "label": "relock cell-0-elastic-tray",
        "requires": [
          "done:verify:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:relock:cell-0-elastic-tray"
        ],
        "adds": [
          "done:relock:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "verify:cell-0-elastic-tray",
        "label": "verify cell-0-elastic-tray",
        "requires": [
          "done:replace:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:verify:cell-0-elastic-tray"
        ],
        "adds": [
          "done:verify:cell-0-elastic-tray"
        ],
        "deletes": [
          "fault:cell-0-elastic-tray",
          "misaligned:cell-0-elastic-tray"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "replace:cell-0-elastic-tray",
        "label": "replace cell-0-elastic-tray",
        "requires": [
          "done:unlock:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:replace:cell-0-elastic-tray"
        ],
        "adds": [
          "done:replace:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "unlock:cell-0-elastic-tray",
        "label": "unlock cell-0-elastic-tray",
        "requires": [
          "done:support:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:unlock:cell-0-elastic-tray"
        ],
        "adds": [
          "done:unlock:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "support:cell-0-elastic-tray",
        "label": "support cell-0-elastic-tray",
        "requires": [
          "done:isolate:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:support:cell-0-elastic-tray"
        ],
        "adds": [
          "done:support:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "isolate:cell-0-elastic-tray",
        "label": "isolate cell-0-elastic-tray",
        "requires": [
          "tool:free",
          "fault:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:isolate:cell-0-elastic-tray"
        ],
        "adds": [
          "done:isolate:cell-0-elastic-tray"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:cell-0-elastic-tray"
    ],
    "initialModules": [
      "foundation",
      "cell-0-mount",
      "cell-0-support",
      "cell-0-elastic-tray",
      "cell-0-instrument"
    ],
    "goalFacts": [
      "ready:cell-0-elastic-tray"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 8
  },
  "answer": {
    "actionIds": [
      "isolate:cell-0-elastic-tray",
      "support:cell-0-elastic-tray",
      "unlock:cell-0-elastic-tray",
      "replace:cell-0-elastic-tray",
      "verify:cell-0-elastic-tray",
      "relock:cell-0-elastic-tray",
      "release:cell-0-elastic-tray"
    ]
  }
}
```

### 失败状态回退（h3-exp-d1-suspension-1-rollback）

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
        "id": "resume:cell-0-elastic-tray",
        "label": "resume cell-0-elastic-tray",
        "requires": [
          "done:verify:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:resume:cell-0-elastic-tray"
        ],
        "adds": [
          "done:resume:cell-0-elastic-tray",
          "ready:cell-0-elastic-tray",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "verify:cell-0-elastic-tray",
        "label": "verify cell-0-elastic-tray",
        "requires": [
          "done:align:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:verify:cell-0-elastic-tray"
        ],
        "adds": [
          "done:verify:cell-0-elastic-tray"
        ],
        "deletes": [
          "fault:cell-0-elastic-tray",
          "misaligned:cell-0-elastic-tray"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "align:cell-0-elastic-tray",
        "label": "align cell-0-elastic-tray",
        "requires": [
          "done:undo:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:align:cell-0-elastic-tray"
        ],
        "adds": [
          "done:align:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray",
          "visible": true
        }
      },
      {
        "id": "undo:cell-0-elastic-tray",
        "label": "undo cell-0-elastic-tray",
        "requires": [
          "done:isolate:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:undo:cell-0-elastic-tray"
        ],
        "adds": [
          "done:undo:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray",
          "visible": false
        }
      },
      {
        "id": "isolate:cell-0-elastic-tray",
        "label": "isolate cell-0-elastic-tray",
        "requires": [
          "tool:free",
          "fault:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:isolate:cell-0-elastic-tray"
        ],
        "adds": [
          "done:isolate:cell-0-elastic-tray"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:cell-0-elastic-tray",
      "misaligned:cell-0-elastic-tray"
    ],
    "initialModules": [
      "foundation",
      "cell-0-mount",
      "cell-0-support",
      "cell-0-elastic-tray",
      "cell-0-instrument"
    ],
    "goalFacts": [
      "ready:cell-0-elastic-tray"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 5
  },
  "answer": {
    "actionIds": [
      "isolate:cell-0-elastic-tray",
      "undo:cell-0-elastic-tray",
      "align:cell-0-elastic-tray",
      "verify:cell-0-elastic-tray",
      "resume:cell-0-elastic-tray"
    ]
  }
}
```

### 共享工具协同维修（h3-exp-d1-suspension-1-resource-repair）

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
        "id": "release:cell-0-instrument",
        "label": "release cell-0-instrument",
        "requires": [
          "done:relock:cell-0-instrument"
        ],
        "forbids": [
          "done:release:cell-0-instrument"
        ],
        "adds": [
          "done:release:cell-0-instrument",
          "ready:cell-0-instrument",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-instrument"
        }
      },
      {
        "id": "relock:cell-0-instrument",
        "label": "relock cell-0-instrument",
        "requires": [
          "done:verify:cell-0-instrument"
        ],
        "forbids": [
          "done:relock:cell-0-instrument"
        ],
        "adds": [
          "done:relock:cell-0-instrument"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-instrument"
        }
      },
      {
        "id": "verify:cell-0-instrument",
        "label": "verify cell-0-instrument",
        "requires": [
          "done:replace:cell-0-instrument"
        ],
        "forbids": [
          "done:verify:cell-0-instrument"
        ],
        "adds": [
          "done:verify:cell-0-instrument"
        ],
        "deletes": [
          "fault:cell-0-instrument",
          "misaligned:cell-0-instrument"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-instrument"
        }
      },
      {
        "id": "replace:cell-0-instrument",
        "label": "replace cell-0-instrument",
        "requires": [
          "done:unlock:cell-0-instrument"
        ],
        "forbids": [
          "done:replace:cell-0-instrument"
        ],
        "adds": [
          "done:replace:cell-0-instrument"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "cell-0-instrument"
        }
      },
      {
        "id": "unlock:cell-0-instrument",
        "label": "unlock cell-0-instrument",
        "requires": [
          "done:support:cell-0-instrument"
        ],
        "forbids": [
          "done:unlock:cell-0-instrument"
        ],
        "adds": [
          "done:unlock:cell-0-instrument"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-instrument"
        }
      },
      {
        "id": "support:cell-0-instrument",
        "label": "support cell-0-instrument",
        "requires": [
          "done:isolate:cell-0-instrument"
        ],
        "forbids": [
          "done:support:cell-0-instrument"
        ],
        "adds": [
          "done:support:cell-0-instrument"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-instrument"
        }
      },
      {
        "id": "isolate:cell-0-instrument",
        "label": "isolate cell-0-instrument",
        "requires": [
          "tool:free",
          "fault:cell-0-instrument"
        ],
        "forbids": [
          "done:isolate:cell-0-instrument"
        ],
        "adds": [
          "done:isolate:cell-0-instrument"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-instrument"
        }
      },
      {
        "id": "release:cell-0-elastic-tray",
        "label": "release cell-0-elastic-tray",
        "requires": [
          "done:relock:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:release:cell-0-elastic-tray"
        ],
        "adds": [
          "done:release:cell-0-elastic-tray",
          "ready:cell-0-elastic-tray",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "relock:cell-0-elastic-tray",
        "label": "relock cell-0-elastic-tray",
        "requires": [
          "done:verify:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:relock:cell-0-elastic-tray"
        ],
        "adds": [
          "done:relock:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "verify:cell-0-elastic-tray",
        "label": "verify cell-0-elastic-tray",
        "requires": [
          "done:replace:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:verify:cell-0-elastic-tray"
        ],
        "adds": [
          "done:verify:cell-0-elastic-tray"
        ],
        "deletes": [
          "fault:cell-0-elastic-tray",
          "misaligned:cell-0-elastic-tray"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "replace:cell-0-elastic-tray",
        "label": "replace cell-0-elastic-tray",
        "requires": [
          "done:unlock:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:replace:cell-0-elastic-tray"
        ],
        "adds": [
          "done:replace:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "unlock:cell-0-elastic-tray",
        "label": "unlock cell-0-elastic-tray",
        "requires": [
          "done:support:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:unlock:cell-0-elastic-tray"
        ],
        "adds": [
          "done:unlock:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "support:cell-0-elastic-tray",
        "label": "support cell-0-elastic-tray",
        "requires": [
          "done:isolate:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:support:cell-0-elastic-tray"
        ],
        "adds": [
          "done:support:cell-0-elastic-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      },
      {
        "id": "isolate:cell-0-elastic-tray",
        "label": "isolate cell-0-elastic-tray",
        "requires": [
          "tool:free",
          "fault:cell-0-elastic-tray"
        ],
        "forbids": [
          "done:isolate:cell-0-elastic-tray"
        ],
        "adds": [
          "done:isolate:cell-0-elastic-tray"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elastic-tray"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:cell-0-elastic-tray",
      "fault:cell-0-instrument"
    ],
    "initialModules": [
      "foundation",
      "cell-0-mount",
      "cell-0-support",
      "cell-0-elastic-tray",
      "cell-0-instrument"
    ],
    "goalFacts": [
      "ready:cell-0-elastic-tray",
      "ready:cell-0-instrument"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 16
  },
  "answer": {
    "actionIds": [
      "isolate:cell-0-instrument",
      "support:cell-0-instrument",
      "unlock:cell-0-instrument",
      "replace:cell-0-instrument",
      "verify:cell-0-instrument",
      "relock:cell-0-instrument",
      "release:cell-0-instrument",
      "isolate:cell-0-elastic-tray",
      "support:cell-0-elastic-tray",
      "unlock:cell-0-elastic-tray",
      "replace:cell-0-elastic-tray",
      "verify:cell-0-elastic-tray",
      "relock:cell-0-elastic-tray",
      "release:cell-0-elastic-tray"
    ]
  }
}
```

### 预算约束检查策略（h3-exp-d1-suspension-1-budget-policy）

提交预算内、对所有相容世界均正确的检查决策表。

能力：预算约束检查策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "cell-0-elastic-tray",
    "worlds": [
      {
        "id": "nominal",
        "action": "continue"
      },
      {
        "id": "fault",
        "action": "replace"
      }
    ],
    "queries": [
      {
        "id": "visual",
        "cost": 0,
        "returns": {
          "nominal": "clear",
          "fault": "clear"
        }
      },
      {
        "id": "probe",
        "cost": 4,
        "returns": {
          "nominal": "clear",
          "fault": "alert"
        }
      },
      {
        "id": "thermal",
        "cost": 3,
        "returns": {
          "nominal": "clear",
          "fault": "alert"
        }
      }
    ],
    "budget": 3
  },
  "answer": {
    "queryId": "thermal",
    "decisions": {
      "clear": "continue",
      "alert": "replace"
    }
  }
}
```
