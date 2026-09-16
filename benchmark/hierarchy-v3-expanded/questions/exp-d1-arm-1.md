## D1 折肘检修臂

### 模块识别（h3-exp-d1-arm-1-identify）

高亮的维修模块对应哪个 ID？

能力：模块识别；形式：single-choice；证据：model-state。

- A：cell-0-shoulder
- B：cell-0-tool
- C：foundation
- D：cell-0-mount

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
        "id": "cell-0-shoulder",
        "name": "cell 0 shoulder"
      },
      {
        "id": "cell-0-elbow",
        "name": "cell 0 elbow"
      },
      {
        "id": "cell-0-wrist",
        "name": "cell 0 wrist"
      },
      {
        "id": "cell-0-tool",
        "name": "cell 0 tool"
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 部件计数（h3-exp-d1-arm-1-count）

模块 cell-0-tool 有多少个可视零件？

能力：部件计数；形式：single-choice；证据：model-state。

- A：1
- B：5
- C：2
- D：3

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
        "id": "cell-0-shoulder-p86",
        "moduleId": "cell-0-shoulder",
        "shape": "cylinder",
        "color": "#387bb3"
      },
      {
        "id": "cell-0-elbow-p87",
        "moduleId": "cell-0-elbow",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-elbow-p88",
        "moduleId": "cell-0-elbow",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-elbow-p89",
        "moduleId": "cell-0-elbow",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "cell-0-wrist-p90",
        "moduleId": "cell-0-wrist",
        "shape": "beam",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-wrist-p91",
        "moduleId": "cell-0-wrist",
        "shape": "beam",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-wrist-p92",
        "moduleId": "cell-0-wrist",
        "shape": "beam",
        "color": "#dc6040"
      },
      {
        "id": "cell-0-tool-p93",
        "moduleId": "cell-0-tool",
        "shape": "arch",
        "color": "#45a080"
      },
      {
        "id": "cell-0-tool-p94",
        "moduleId": "cell-0-tool",
        "shape": "axle",
        "color": "#dfebed"
      }
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 颜色识别（h3-exp-d1-arm-1-color）

零件 cell-0-tool-p93 的颜色值是什么？

能力：颜色识别；形式：single-choice；证据：model-state。

- A：#f2bf3c
- B：#45a080
- C：#2878b8
- D：#d43a32

```json
{
  "input": {
    "part": {
      "id": "cell-0-tool-p93",
      "moduleId": "cell-0-tool",
      "shape": "arch",
      "position": [
        0,
        0.26249999999999973,
        0
      ],
      "size": [
        0.65,
        0.65,
        0.65
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

### 三维位置（h3-exp-d1-arm-1-position）

模块 cell-0-tool 的世界包围盒中心是什么？

能力：三维位置；形式：single-choice；证据：model-state。

- A：[1.9,3.3875,1.3]
- B：[0,0.2,0]
- C：[0,0.7,0]
- D：[-1.7,1.35,0]

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
      "cell-0-shoulder": [
        -1.7,
        1.35,
        0
      ],
      "cell-0-elbow": [
        -0.95,
        3.1999999999999997,
        0
      ],
      "cell-0-wrist": [
        0.8,
        4.050000000000001,
        0.7
      ],
      "cell-0-tool": [
        1.9,
        3.3875,
        1.3
      ]
    }
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 关节类型（h3-exp-d1-arm-1-joint-type）

cell-0-elbow-joint 采用什么约束类型？

能力：关节类型；形式：single-choice；证据：model-state。

- A：fixed
- B：prismatic
- C：spring
- D：revolute

```json
{
  "input": {
    "joint": {
      "id": "cell-0-elbow-joint",
      "name": "cell-0-elbow interface",
      "parent": "cell-0-shoulder",
      "child": "cell-0-elbow",
      "type": "revolute",
      "anchorParent": [
        0,
        0.6499999999999999,
        0
      ],
      "anchorChild": [
        -0.75,
        -1.1999999999999997,
        0
      ],
      "axis": [
        0,
        0,
        1
      ],
      "limits": [
        -0.6,
        0.6
      ]
    }
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 直接连接（h3-exp-d1-arm-1-parent）

cell-0-tool 的直接父模块集合是什么？

能力：直接连接；形式：single-choice；证据：model-state。

- A：["cell-0-tool"]
- B：[]
- C：["foundation","cell-0-mount","cell-0-shoulder","cell-0-elbow","cell-0-wrist","cell-0-tool"]
- D：["cell-0-wrist"]

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
        "id": "cell-0-shoulder-joint",
        "name": "cell-0-shoulder interface",
        "parent": "cell-0-mount",
        "child": "cell-0-shoulder",
        "type": "revolute",
        "anchorParent": [
          -1.7,
          0.6500000000000001,
          0
        ],
        "anchorChild": [
          0,
          0,
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
      },
      {
        "id": "cell-0-elbow-joint",
        "name": "cell-0-elbow interface",
        "parent": "cell-0-shoulder",
        "child": "cell-0-elbow",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6499999999999999,
          0
        ],
        "anchorChild": [
          -0.75,
          -1.1999999999999997,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-0-wrist-joint",
        "name": "cell-0-wrist interface",
        "parent": "cell-0-elbow",
        "child": "cell-0-wrist",
        "type": "revolute",
        "anchorParent": [
          0.75,
          1.2000000000000006,
          0.7
        ],
        "anchorChild": [
          -1,
          0.34999999999999964,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-0-tool-joint",
        "name": "cell-0-tool interface",
        "parent": "cell-0-wrist",
        "child": "cell-0-tool",
        "type": "prismatic",
        "anchorParent": [
          1.1,
          -0.4000000000000008,
          0.6000000000000001
        ],
        "anchorChild": [
          0,
          0.26249999999999973,
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
    "choiceId": "D"
  }
}
```

### 基座识别（h3-exp-d1-arm-1-anchor）

哪些模块被声明为固定基座？

能力：基座识别；形式：single-choice；证据：model-state。

- A：["cell-0-tool"]
- B：["foundation"]
- C：[]
- D：["foundation","cell-0-mount","cell-0-shoulder","cell-0-elbow","cell-0-wrist","cell-0-tool"]

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
        "id": "cell-0-shoulder",
        "name": "cell 0 shoulder",
        "role": "actuator",
        "anchored": false,
        "mass": 1.2,
        "position": [
          -1.7,
          1.35,
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
        "id": "cell-0-elbow",
        "name": "cell 0 elbow",
        "role": "actuator",
        "anchored": false,
        "mass": 1.2,
        "position": [
          -0.95,
          3.1999999999999997,
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
        "id": "cell-0-wrist",
        "name": "cell 0 wrist",
        "role": "actuator",
        "anchored": false,
        "mass": 1.2,
        "position": [
          0.8,
          4.050000000000001,
          0.7
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cell-0-tool",
        "name": "cell 0 tool",
        "role": "actuator",
        "anchored": false,
        "mass": 1.2,
        "position": [
          1.9,
          3.3875,
          1.3
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
    "choiceId": "B"
  }
}
```

### 接口计数（h3-exp-d1-arm-1-degree）

cell-0-tool 连接几个声明关节？平行关节分别计数。

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
        "id": "cell-0-shoulder-joint",
        "name": "cell-0-shoulder interface",
        "parent": "cell-0-mount",
        "child": "cell-0-shoulder",
        "type": "revolute",
        "anchorParent": [
          -1.7,
          0.6500000000000001,
          0
        ],
        "anchorChild": [
          0,
          0,
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
      },
      {
        "id": "cell-0-elbow-joint",
        "name": "cell-0-elbow interface",
        "parent": "cell-0-shoulder",
        "child": "cell-0-elbow",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6499999999999999,
          0
        ],
        "anchorChild": [
          -0.75,
          -1.1999999999999997,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-0-wrist-joint",
        "name": "cell-0-wrist interface",
        "parent": "cell-0-elbow",
        "child": "cell-0-wrist",
        "type": "revolute",
        "anchorParent": [
          0.75,
          1.2000000000000006,
          0.7
        ],
        "anchorChild": [
          -1,
          0.34999999999999964,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-0-tool-joint",
        "name": "cell-0-tool interface",
        "parent": "cell-0-wrist",
        "child": "cell-0-tool",
        "type": "prismatic",
        "anchorParent": [
          1.1,
          -0.4000000000000008,
          0.6000000000000001
        ],
        "anchorChild": [
          0,
          0.26249999999999973,
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

### 局部改色（h3-exp-d1-arm-1-recolor）

仅将 cell-0-tool-p93 改成 #e8792e，其他零件不变。选择正确补丁。

能力：局部改色；形式：single-choice；证据：model-state。

- A：{"id":"cell-0-tool-p94","color":"#e8792e"}
- B：{"id":"cell-0-tool-p93","color":"#2878b8"}
- C：{"id":"*","color":"#e8792e"}
- D：{"id":"cell-0-tool-p93","color":"#e8792e"}

```json
{
  "input": {
    "part": {
      "id": "cell-0-tool-p93",
      "moduleId": "cell-0-tool",
      "shape": "arch",
      "position": [
        0,
        0.26249999999999973,
        0
      ],
      "size": [
        0.65,
        0.65,
        0.65
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
    "choiceId": "D"
  }
}
```

### 补装部件（h3-exp-d1-arm-1-add）

模块 cell-0-tool 缺失零件 cell-0-tool-p93。选择与目标清单一致的补装描述。

能力：补装部件；形式：single-choice；证据：model-state。

- A：{"id":"cell-0-tool-p93","moduleId":"foundation","shape":"arch","position":[0,0.26249999999999973,0],"size":[0.65,0.65,0.65],"color":"#45a080","rotation":[0,0,0,1]}
- B：{"id":"cell-0-tool-p93","moduleId":"cell-0-tool","shape":"arch","position":[0,0.26249999999999973,0],"size":[3,3,3],"color":"#45a080","rotation":[0,0,0,1]}
- C：{"id":"cell-0-tool-p93","moduleId":"cell-0-tool","shape":"arch","position":[0,0.26249999999999973,0],"size":[0.65,0.65,0.65],"color":"#000000","rotation":[0,0,0,1]}
- D：{"id":"cell-0-tool-p93","moduleId":"cell-0-tool","shape":"arch","position":[0,0.26249999999999973,0],"size":[0.65,0.65,0.65],"color":"#45a080","rotation":[0,0,0,1]}

```json
{
  "input": {
    "targetPart": {
      "id": "cell-0-tool-p93",
      "moduleId": "cell-0-tool",
      "shape": "arch",
      "position": [
        0,
        0.26249999999999973,
        0
      ],
      "size": [
        0.65,
        0.65,
        0.65
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
      "cell-0-shoulder-p86",
      "cell-0-elbow-p87",
      "cell-0-elbow-p88",
      "cell-0-elbow-p89",
      "cell-0-wrist-p90",
      "cell-0-wrist-p91",
      "cell-0-wrist-p92",
      "cell-0-tool-p94"
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 安全拆除（h3-exp-d1-arm-1-remove）

按声明依赖图，当前可以先拆哪些叶模块？

能力：安全拆除；形式：single-choice；证据：model-state。

- A：["foundation","cell-0-mount","cell-0-shoulder","cell-0-elbow","cell-0-wrist","cell-0-tool"]
- B：["cell-0-tool"]
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
        "id": "cell-0-shoulder-joint",
        "name": "cell-0-shoulder interface",
        "parent": "cell-0-mount",
        "child": "cell-0-shoulder",
        "type": "revolute",
        "anchorParent": [
          -1.7,
          0.6500000000000001,
          0
        ],
        "anchorChild": [
          0,
          0,
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
      },
      {
        "id": "cell-0-elbow-joint",
        "name": "cell-0-elbow interface",
        "parent": "cell-0-shoulder",
        "child": "cell-0-elbow",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6499999999999999,
          0
        ],
        "anchorChild": [
          -0.75,
          -1.1999999999999997,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-0-wrist-joint",
        "name": "cell-0-wrist interface",
        "parent": "cell-0-elbow",
        "child": "cell-0-wrist",
        "type": "revolute",
        "anchorParent": [
          0.75,
          1.2000000000000006,
          0.7
        ],
        "anchorChild": [
          -1,
          0.34999999999999964,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-0-tool-joint",
        "name": "cell-0-tool interface",
        "parent": "cell-0-wrist",
        "child": "cell-0-tool",
        "type": "prismatic",
        "anchorParent": [
          1.1,
          -0.4000000000000008,
          0.6000000000000001
        ],
        "anchorChild": [
          0,
          0.26249999999999973,
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
      "cell-0-shoulder",
      "cell-0-elbow",
      "cell-0-wrist",
      "cell-0-tool"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 替换选择（h3-exp-d1-arm-1-replace）

在成本上限内选择刚度最大的替换件；并列选成本低者，再并列选ID字典序最小者。

能力：替换选择；形式：single-choice；证据：model-state。

- A：stock-3
- B：stock-2
- C：stock-0
- D：stock-1

```json
{
  "input": {
    "alternatives": [
      {
        "id": "stock-0",
        "cost": 7,
        "stiffness": 6,
        "mass": 1.7
      },
      {
        "id": "stock-1",
        "cost": 4,
        "stiffness": 4,
        "mass": 1.2
      },
      {
        "id": "stock-2",
        "cost": 7,
        "stiffness": 11,
        "mass": 1.6
      },
      {
        "id": "stock-3",
        "cost": 5,
        "stiffness": 10,
        "mass": 0.5
      }
    ],
    "maxCost": 7
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 平移纠偏（h3-exp-d1-arm-1-translate）

观察到相对目标的平移误差 delta，选择补偿平移。

能力：平移纠偏；形式：single-choice；证据：model-state。

- A：[1,0,-2]
- B：[0,0,0]
- C：[0,2,0]
- D：[-1,0,2]

```json
{
  "input": {
    "delta": [
      1,
      0,
      -2
    ],
    "target": "cell-0-tool"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 姿态纠偏（h3-exp-d1-arm-1-rotate）

选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。

能力：姿态纠偏；形式：single-choice；证据：model-state。

- A：90
- B：135
- C：-135
- D：0

```json
{
  "input": {
    "module": "cell-0-tool",
    "currentYaw": 270,
    "targetYaw": 45
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 下一步放置（h3-exp-d1-arm-1-next-module）

已完成给定前缀，选择所有前置依赖已满足的下一模块集合。

能力：下一步放置；形式：single-choice；证据：model-state。

- A：["cell-0-elbow"]
- B：[]
- C：["foundation","cell-0-mount","cell-0-shoulder"]
- D：["cell-0-elbow","cell-0-wrist","cell-0-tool"]

```json
{
  "input": {
    "prefix": [
      "foundation",
      "cell-0-mount",
      "cell-0-shoulder"
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
        "id": "cell-0-shoulder-joint",
        "name": "cell-0-shoulder interface",
        "parent": "cell-0-mount",
        "child": "cell-0-shoulder",
        "type": "revolute",
        "anchorParent": [
          -1.7,
          0.6500000000000001,
          0
        ],
        "anchorChild": [
          0,
          0,
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
      },
      {
        "id": "cell-0-elbow-joint",
        "name": "cell-0-elbow interface",
        "parent": "cell-0-shoulder",
        "child": "cell-0-elbow",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6499999999999999,
          0
        ],
        "anchorChild": [
          -0.75,
          -1.1999999999999997,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-0-wrist-joint",
        "name": "cell-0-wrist interface",
        "parent": "cell-0-elbow",
        "child": "cell-0-wrist",
        "type": "revolute",
        "anchorParent": [
          0.75,
          1.2000000000000006,
          0.7
        ],
        "anchorChild": [
          -1,
          0.34999999999999964,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-0-tool-joint",
        "name": "cell-0-tool interface",
        "parent": "cell-0-wrist",
        "child": "cell-0-tool",
        "type": "prismatic",
        "anchorParent": [
          1.1,
          -0.4000000000000008,
          0.6000000000000001
        ],
        "anchorChild": [
          0,
          0.26249999999999973,
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
      "cell-0-shoulder",
      "cell-0-elbow",
      "cell-0-wrist",
      "cell-0-tool"
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 库存核算（h3-exp-d1-arm-1-inventory）

备件库有 6 件，替换模块需 2 件，还剩多少？

能力：库存核算；形式：single-choice；证据：model-state。

- A：5
- B：3
- C：7
- D：4

```json
{
  "input": {
    "available": 6,
    "required": 2
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 子装配边界（h3-exp-d1-arm-1-boundary）

隔离 cell-0-tool 需要断开哪些边界关节？

能力：子装配边界；形式：single-choice；证据：model-state。

- A：["cell-0-tool-joint"]
- B：[]
- C：["cell-0-mount-joint","cell-0-shoulder-joint","cell-0-elbow-joint","cell-0-wrist-joint","cell-0-tool-joint"]
- D：["cell-0-elbow-joint"]

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
        "id": "cell-0-shoulder-joint",
        "name": "cell-0-shoulder interface",
        "parent": "cell-0-mount",
        "child": "cell-0-shoulder",
        "type": "revolute",
        "anchorParent": [
          -1.7,
          0.6500000000000001,
          0
        ],
        "anchorChild": [
          0,
          0,
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
      },
      {
        "id": "cell-0-elbow-joint",
        "name": "cell-0-elbow interface",
        "parent": "cell-0-shoulder",
        "child": "cell-0-elbow",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6499999999999999,
          0
        ],
        "anchorChild": [
          -0.75,
          -1.1999999999999997,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-0-wrist-joint",
        "name": "cell-0-wrist interface",
        "parent": "cell-0-elbow",
        "child": "cell-0-wrist",
        "type": "revolute",
        "anchorParent": [
          0.75,
          1.2000000000000006,
          0.7
        ],
        "anchorChild": [
          -1,
          0.34999999999999964,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-0-tool-joint",
        "name": "cell-0-tool interface",
        "parent": "cell-0-wrist",
        "child": "cell-0-tool",
        "type": "prismatic",
        "anchorParent": [
          1.1,
          -0.4000000000000008,
          0.6000000000000001
        ],
        "anchorChild": [
          0,
          0.26249999999999973,
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
    "target": "cell-0-tool"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 最小干预（h3-exp-d1-arm-1-no-op）

当前模块颜色已满足指令，且无需改变位姿。最少需要几次编辑？

能力：最小干预；形式：single-choice；证据：model-state。

- A：2
- B：0
- C：1

```json
{
  "input": {
    "module": "cell-0-tool"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 全过程依赖（h3-exp-d1-arm-1-prefix）

给定候选顺序，首次违反前置依赖的步骤是？从 0 编号，-1 表示没有违反。

能力：全过程依赖；形式：single-choice；证据：support-graph。

- A：2
- B：5
- C：1
- D：-1

```json
{
  "input": {
    "order": [
      "foundation",
      "cell-0-shoulder",
      "cell-0-mount",
      "cell-0-elbow",
      "cell-0-wrist",
      "cell-0-tool"
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
        "id": "cell-0-shoulder-joint",
        "name": "cell-0-shoulder interface",
        "parent": "cell-0-mount",
        "child": "cell-0-shoulder",
        "type": "revolute",
        "anchorParent": [
          -1.7,
          0.6500000000000001,
          0
        ],
        "anchorChild": [
          0,
          0,
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
      },
      {
        "id": "cell-0-elbow-joint",
        "name": "cell-0-elbow interface",
        "parent": "cell-0-shoulder",
        "child": "cell-0-elbow",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6499999999999999,
          0
        ],
        "anchorChild": [
          -0.75,
          -1.1999999999999997,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-0-wrist-joint",
        "name": "cell-0-wrist interface",
        "parent": "cell-0-elbow",
        "child": "cell-0-wrist",
        "type": "revolute",
        "anchorParent": [
          0.75,
          1.2000000000000006,
          0.7
        ],
        "anchorChild": [
          -1,
          0.34999999999999964,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-0-tool-joint",
        "name": "cell-0-tool interface",
        "parent": "cell-0-wrist",
        "child": "cell-0-tool",
        "type": "prismatic",
        "anchorParent": [
          1.1,
          -0.4000000000000008,
          0.6000000000000001
        ],
        "anchorChild": [
          0,
          0.26249999999999973,
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

### 连续维修路径（h3-exp-d1-arm-1-access）

根据实际 Rapier shape cast 记录，选择全部无碰撞路径。

能力：连续维修路径；形式：multiple-choice；证据：Rapier。

- A：path-1
- B：path-2
- C：path-0

```json
{
  "input": {
    "paths": [
      {
        "id": "path-0",
        "start": [
          7.98,
          3.3875,
          1.3
        ],
        "end": [
          1.9,
          3.3875,
          1.3
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
          1.9,
          8.541578753454903,
          1.3
        ],
        "end": [
          1.9,
          3.3875,
          1.3
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
        "id": "path-2",
        "start": [
          1.9,
          3.3875,
          7.48
        ],
        "end": [
          1.9,
          3.3875,
          1.3
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
      "B",
      "C"
    ]
  }
}
```

### 支撑反事实（h3-exp-d1-arm-1-counterfactual）

移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。

能力：支撑反事实；形式：single-choice；证据：support-graph。

- A：[]
- B：["foundation","cell-0-mount","cell-0-shoulder","cell-0-elbow","cell-0-wrist","cell-0-tool"]
- C：["cell-0-elbow","cell-0-shoulder","cell-0-tool","cell-0-wrist"]
- D：["cell-0-mount"]

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
        "id": "cell-0-shoulder-joint",
        "name": "cell-0-shoulder interface",
        "parent": "cell-0-mount",
        "child": "cell-0-shoulder",
        "type": "revolute",
        "anchorParent": [
          -1.7,
          0.6500000000000001,
          0
        ],
        "anchorChild": [
          0,
          0,
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
      },
      {
        "id": "cell-0-elbow-joint",
        "name": "cell-0-elbow interface",
        "parent": "cell-0-shoulder",
        "child": "cell-0-elbow",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6499999999999999,
          0
        ],
        "anchorChild": [
          -0.75,
          -1.1999999999999997,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-0-wrist-joint",
        "name": "cell-0-wrist interface",
        "parent": "cell-0-elbow",
        "child": "cell-0-wrist",
        "type": "revolute",
        "anchorParent": [
          0.75,
          1.2000000000000006,
          0.7
        ],
        "anchorChild": [
          -1,
          0.34999999999999964,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-0-tool-joint",
        "name": "cell-0-tool interface",
        "parent": "cell-0-wrist",
        "child": "cell-0-tool",
        "type": "prismatic",
        "anchorParent": [
          1.1,
          -0.4000000000000008,
          0.6000000000000001
        ],
        "anchorChild": [
          0,
          0.26249999999999973,
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
      "cell-0-shoulder",
      "cell-0-elbow",
      "cell-0-wrist",
      "cell-0-tool"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 冲击响应读数（h3-exp-d1-arm-1-dynamic）

Rapier 实际采样轨迹中的最大平移位移是多少？按四位小数报告。

能力：冲击响应读数；形式：single-choice；证据：Rapier。

- A：0
- B：1.0101
- C：0.0101
- D：0.2101

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.010063099601191903
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.0021642251665198965
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.0004107058123938101
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.00008316375308431003
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.000015199535029238195
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.000010136295160999924
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.000009856957628387987
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.00000988071717505555
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.00000988071717505555
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.00000988071717505555
      },
      {
        "time": 1,
        "displacement": 0.00000988071717505555
      }
    ],
    "impulse": [
      10,
      1.8,
      3.5
    ],
    "nominalDrift": 0.0068548004921294555,
    "scope": "采样轨迹极值，非连续时间极值；不代表实物安全阈值"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 关节限位推理（h3-exp-d1-arm-1-kinematic）

下列目标位置/角度中哪些在关节声明限位内（含边界）？

能力：关节限位推理；形式：multiple-choice；证据：model-state。

- A：-0.6
- B：0
- C：-1.1
- D：1.1

```json
{
  "input": {
    "joint": "cell-0-elbow-joint",
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

### 约束故障诊断（h3-exp-d1-arm-1-diagnosis）

已检测到端点和约束类型如下，选择匹配的全部关节。

能力：约束故障诊断；形式：multiple-choice；证据：model-state。

- A：cell-0-mount-joint
- B：cell-0-shoulder-joint
- C：cell-0-elbow-joint
- D：cell-0-tool-joint

```json
{
  "input": {
    "endpoints": [
      "cell-0-wrist",
      "cell-0-tool"
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
        "id": "cell-0-shoulder-joint",
        "name": "cell-0-shoulder interface",
        "parent": "cell-0-mount",
        "child": "cell-0-shoulder",
        "type": "revolute",
        "anchorParent": [
          -1.7,
          0.6500000000000001,
          0
        ],
        "anchorChild": [
          0,
          0,
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
      },
      {
        "id": "cell-0-elbow-joint",
        "name": "cell-0-elbow interface",
        "parent": "cell-0-shoulder",
        "child": "cell-0-elbow",
        "type": "revolute",
        "anchorParent": [
          0,
          0.6499999999999999,
          0
        ],
        "anchorChild": [
          -0.75,
          -1.1999999999999997,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-0-wrist-joint",
        "name": "cell-0-wrist interface",
        "parent": "cell-0-elbow",
        "child": "cell-0-wrist",
        "type": "revolute",
        "anchorParent": [
          0.75,
          1.2000000000000006,
          0.7
        ],
        "anchorChild": [
          -1,
          0.34999999999999964,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.6,
          0.6
        ]
      },
      {
        "id": "cell-0-tool-joint",
        "name": "cell-0-tool interface",
        "parent": "cell-0-wrist",
        "child": "cell-0-tool",
        "type": "prismatic",
        "anchorParent": [
          1.1,
          -0.4000000000000008,
          0.6000000000000001
        ],
        "anchorChild": [
          0,
          0.26249999999999973,
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
      "D"
    ]
  }
}
```

### 主动检查收益（h3-exp-d1-arm-1-information-gain）

均匀先验四个世界，选择信息增益/成本最大的全部检查。

能力：主动检查收益；形式：multiple-choice；证据：finite-world。

- A：query-1
- B：query-2
- C：query-0

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
    "module": "cell-0-tool",
    "worlds": [
      "normal",
      "jammed",
      "reversed",
      "loose"
    ]
  },
  "answer": {
    "choiceIds": [
      "B"
    ]
  }
}
```

### 不确定性与弃答（h3-exp-d1-arm-1-abstention）

所有相容世界是否允许同一个后续动作？选择继续执行或请求检查。

能力：不确定性与弃答；形式：single-choice；证据：finite-world。

- A：inspect
- B：commit

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
    "choiceId": "A"
  }
}
```

### 观测后信念更新（h3-exp-d1-arm-1-posterior）

均匀先验，得到给定观测后，jammed 世界的后验概率是多少？

能力：观测后信念更新；形式：single-choice；证据：finite-world。

- A：0
- B：0.25
- C：0.3333333333333333
- D：0.5

```json
{
  "input": {
    "module": "cell-0-tool",
    "worlds": [
      "normal",
      "jammed",
      "reversed",
      "loose"
    ],
    "observationByWorld": [
      "negative",
      "positive",
      "positive",
      "negative"
    ],
    "observed": "positive"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 多目标工程权衡（h3-exp-d1-arm-1-pareto）

最小成本、最小质量、最大刚度，选择完整非支配集合。

能力：多目标工程权衡；形式：multiple-choice；证据：model-state。

- A：stock-1
- B：stock-2
- C：stock-3
- D：stock-0

```json
{
  "input": {
    "alternatives": [
      {
        "id": "stock-0",
        "cost": 7,
        "stiffness": 6,
        "mass": 1.7
      },
      {
        "id": "stock-1",
        "cost": 4,
        "stiffness": 4,
        "mass": 1.2
      },
      {
        "id": "stock-2",
        "cost": 7,
        "stiffness": 11,
        "mass": 1.6
      },
      {
        "id": "stock-3",
        "cost": 5,
        "stiffness": 10,
        "mass": 0.5
      }
    ]
  },
  "answer": {
    "choiceIds": [
      "A",
      "B",
      "C"
    ]
  }
}
```

### 依赖装配（h3-exp-d1-arm-1-assembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖装配；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [],
    "initialModules": [],
    "actions": [
      {
        "id": "place:cell-0-shoulder",
        "label": "安装 cell-0-shoulder",
        "requires": [
          "present:cell-0-mount"
        ],
        "forbids": [
          "present:cell-0-shoulder"
        ],
        "adds": [
          "present:cell-0-shoulder"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-shoulder",
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
      },
      {
        "id": "place:cell-0-wrist",
        "label": "安装 cell-0-wrist",
        "requires": [
          "present:cell-0-elbow"
        ],
        "forbids": [
          "present:cell-0-wrist"
        ],
        "adds": [
          "present:cell-0-wrist"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-wrist",
          "visible": true
        }
      },
      {
        "id": "place:cell-0-tool",
        "label": "安装 cell-0-tool",
        "requires": [
          "present:cell-0-wrist"
        ],
        "forbids": [
          "present:cell-0-tool"
        ],
        "adds": [
          "present:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool",
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
        "id": "place:cell-0-elbow",
        "label": "安装 cell-0-elbow",
        "requires": [
          "present:cell-0-shoulder"
        ],
        "forbids": [
          "present:cell-0-elbow"
        ],
        "adds": [
          "present:cell-0-elbow"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elbow",
          "visible": true
        }
      }
    ],
    "goalFacts": [
      "present:foundation",
      "present:cell-0-mount",
      "present:cell-0-shoulder",
      "present:cell-0-elbow",
      "present:cell-0-wrist",
      "present:cell-0-tool"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "place:foundation",
      "place:cell-0-mount",
      "place:cell-0-shoulder",
      "place:cell-0-elbow",
      "place:cell-0-wrist",
      "place:cell-0-tool"
    ]
  }
}
```

### 依赖拆解（h3-exp-d1-arm-1-disassembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖拆解；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "present:foundation",
      "present:cell-0-mount",
      "present:cell-0-shoulder",
      "present:cell-0-elbow",
      "present:cell-0-wrist",
      "present:cell-0-tool"
    ],
    "initialModules": [
      "foundation",
      "cell-0-mount",
      "cell-0-shoulder",
      "cell-0-elbow",
      "cell-0-wrist",
      "cell-0-tool"
    ],
    "actions": [
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
        "id": "remove:cell-0-elbow",
        "label": "拆除 cell-0-elbow",
        "requires": [
          "present:cell-0-elbow"
        ],
        "forbids": [
          "present:cell-0-wrist"
        ],
        "adds": [
          "removed:cell-0-elbow"
        ],
        "deletes": [
          "present:cell-0-elbow"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-elbow",
          "visible": false
        }
      },
      {
        "id": "remove:cell-0-shoulder",
        "label": "拆除 cell-0-shoulder",
        "requires": [
          "present:cell-0-shoulder"
        ],
        "forbids": [
          "present:cell-0-elbow"
        ],
        "adds": [
          "removed:cell-0-shoulder"
        ],
        "deletes": [
          "present:cell-0-shoulder"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-shoulder",
          "visible": false
        }
      },
      {
        "id": "remove:cell-0-wrist",
        "label": "拆除 cell-0-wrist",
        "requires": [
          "present:cell-0-wrist"
        ],
        "forbids": [
          "present:cell-0-tool"
        ],
        "adds": [
          "removed:cell-0-wrist"
        ],
        "deletes": [
          "present:cell-0-wrist"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-wrist",
          "visible": false
        }
      },
      {
        "id": "remove:cell-0-tool",
        "label": "拆除 cell-0-tool",
        "requires": [
          "present:cell-0-tool"
        ],
        "forbids": [],
        "adds": [
          "removed:cell-0-tool"
        ],
        "deletes": [
          "present:cell-0-tool"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool",
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
          "present:cell-0-shoulder"
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
      "removed:cell-0-tool",
      "removed:cell-0-wrist",
      "removed:cell-0-elbow",
      "removed:cell-0-shoulder",
      "removed:cell-0-mount",
      "removed:foundation"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "remove:cell-0-tool",
      "remove:cell-0-wrist",
      "remove:cell-0-elbow",
      "remove:cell-0-shoulder",
      "remove:cell-0-mount",
      "remove:foundation"
    ]
  }
}
```

### 承载维修（h3-exp-d1-arm-1-service-repair）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：承载维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:cell-0-tool",
      "closed:cell-0-tool"
    ],
    "initialModules": [
      "foundation",
      "cell-0-mount",
      "cell-0-shoulder",
      "cell-0-elbow",
      "cell-0-wrist",
      "cell-0-tool"
    ],
    "actions": [
      {
        "id": "release:cell-0-tool",
        "label": "release cell-0-tool",
        "requires": [
          "done:close:cell-0-tool"
        ],
        "forbids": [
          "done:release:cell-0-tool"
        ],
        "adds": [
          "done:release:cell-0-tool",
          "repaired:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "replace:cell-0-tool",
        "label": "replace cell-0-tool",
        "requires": [
          "done:remove:cell-0-tool"
        ],
        "forbids": [
          "done:replace:cell-0-tool"
        ],
        "adds": [
          "done:replace:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool",
          "visible": true
        }
      },
      {
        "id": "remove:cell-0-tool",
        "label": "remove cell-0-tool",
        "requires": [
          "done:open:cell-0-tool"
        ],
        "forbids": [
          "done:remove:cell-0-tool"
        ],
        "adds": [
          "done:remove:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool",
          "visible": false
        }
      },
      {
        "id": "open:cell-0-tool",
        "label": "open cell-0-tool",
        "requires": [
          "done:support:cell-0-tool"
        ],
        "forbids": [
          "done:open:cell-0-tool"
        ],
        "adds": [
          "done:open:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "verify:cell-0-tool",
        "label": "verify cell-0-tool",
        "requires": [
          "done:replace:cell-0-tool"
        ],
        "forbids": [
          "done:verify:cell-0-tool"
        ],
        "adds": [
          "done:verify:cell-0-tool"
        ],
        "deletes": [
          "fault:cell-0-tool"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "support:cell-0-tool",
        "label": "support cell-0-tool",
        "requires": [
          "fault:cell-0-tool"
        ],
        "forbids": [
          "done:support:cell-0-tool"
        ],
        "adds": [
          "done:support:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "close:cell-0-tool",
        "label": "close cell-0-tool",
        "requires": [
          "done:verify:cell-0-tool"
        ],
        "forbids": [
          "done:close:cell-0-tool"
        ],
        "adds": [
          "done:close:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      }
    ],
    "goalFacts": [
      "repaired:cell-0-tool"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:cell-0-tool",
      "open:cell-0-tool",
      "remove:cell-0-tool",
      "replace:cell-0-tool",
      "verify:cell-0-tool",
      "close:cell-0-tool",
      "release:cell-0-tool"
    ]
  }
}
```

### 复合编辑验证（h3-exp-d1-arm-1-compound-edit）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：复合编辑验证；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:cell-0-tool",
      "closed:cell-0-tool"
    ],
    "initialModules": [
      "foundation",
      "cell-0-mount",
      "cell-0-shoulder",
      "cell-0-elbow",
      "cell-0-wrist",
      "cell-0-tool"
    ],
    "actions": [
      {
        "id": "release:cell-0-tool",
        "label": "release cell-0-tool",
        "requires": [
          "done:close:cell-0-tool"
        ],
        "forbids": [
          "done:release:cell-0-tool"
        ],
        "adds": [
          "done:release:cell-0-tool",
          "repaired:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "open:cell-0-tool",
        "label": "open cell-0-tool",
        "requires": [
          "done:support:cell-0-tool"
        ],
        "forbids": [
          "done:open:cell-0-tool"
        ],
        "adds": [
          "done:open:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "recolor:cell-0-tool",
        "label": "recolor cell-0-tool",
        "requires": [
          "done:open:cell-0-tool"
        ],
        "forbids": [
          "done:recolor:cell-0-tool"
        ],
        "adds": [
          "done:recolor:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool",
          "color": "#ea7635"
        }
      },
      {
        "id": "verify:cell-0-tool",
        "label": "verify cell-0-tool",
        "requires": [
          "done:recolor:cell-0-tool"
        ],
        "forbids": [
          "done:verify:cell-0-tool"
        ],
        "adds": [
          "done:verify:cell-0-tool"
        ],
        "deletes": [
          "fault:cell-0-tool"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "support:cell-0-tool",
        "label": "support cell-0-tool",
        "requires": [
          "fault:cell-0-tool"
        ],
        "forbids": [
          "done:support:cell-0-tool"
        ],
        "adds": [
          "done:support:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "close:cell-0-tool",
        "label": "close cell-0-tool",
        "requires": [
          "done:verify:cell-0-tool"
        ],
        "forbids": [
          "done:close:cell-0-tool"
        ],
        "adds": [
          "done:close:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      }
    ],
    "goalFacts": [
      "repaired:cell-0-tool"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:cell-0-tool",
      "open:cell-0-tool",
      "recolor:cell-0-tool",
      "verify:cell-0-tool",
      "close:cell-0-tool",
      "release:cell-0-tool"
    ]
  }
}
```

### 跨区域联合维修（h3-exp-d1-arm-1-multi-fault）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：跨区域联合维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:cell-0-tool",
      "closed:cell-0-tool"
    ],
    "initialModules": [
      "foundation",
      "cell-0-mount",
      "cell-0-shoulder",
      "cell-0-elbow",
      "cell-0-wrist",
      "cell-0-tool"
    ],
    "actions": [
      {
        "id": "release:cell-0-tool",
        "label": "release cell-0-tool",
        "requires": [
          "done:close:cell-0-tool"
        ],
        "forbids": [
          "done:release:cell-0-tool"
        ],
        "adds": [
          "done:release:cell-0-tool",
          "repaired:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "replace:cell-0-tool",
        "label": "replace cell-0-tool",
        "requires": [
          "done:remove:cell-0-tool"
        ],
        "forbids": [
          "done:replace:cell-0-tool"
        ],
        "adds": [
          "done:replace:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool",
          "visible": true
        }
      },
      {
        "id": "remove:cell-0-tool",
        "label": "remove cell-0-tool",
        "requires": [
          "done:open:cell-0-tool"
        ],
        "forbids": [
          "done:remove:cell-0-tool"
        ],
        "adds": [
          "done:remove:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool",
          "visible": false
        }
      },
      {
        "id": "open:cell-0-tool",
        "label": "open cell-0-tool",
        "requires": [
          "done:support:cell-0-tool"
        ],
        "forbids": [
          "done:open:cell-0-tool"
        ],
        "adds": [
          "done:open:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "verify:cell-0-tool",
        "label": "verify cell-0-tool",
        "requires": [
          "done:replace:cell-0-tool"
        ],
        "forbids": [
          "done:verify:cell-0-tool"
        ],
        "adds": [
          "done:verify:cell-0-tool"
        ],
        "deletes": [
          "fault:cell-0-tool"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "support:cell-0-tool",
        "label": "support cell-0-tool",
        "requires": [
          "fault:cell-0-tool"
        ],
        "forbids": [
          "done:support:cell-0-tool"
        ],
        "adds": [
          "done:support:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "close:cell-0-tool",
        "label": "close cell-0-tool",
        "requires": [
          "done:verify:cell-0-tool"
        ],
        "forbids": [
          "done:close:cell-0-tool"
        ],
        "adds": [
          "done:close:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      }
    ],
    "goalFacts": [
      "repaired:cell-0-tool"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:cell-0-tool",
      "open:cell-0-tool",
      "remove:cell-0-tool",
      "replace:cell-0-tool",
      "verify:cell-0-tool",
      "close:cell-0-tool",
      "release:cell-0-tool"
    ]
  }
}
```

### 多工位资源调度（h3-exp-d1-arm-1-scheduling）

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
        "module": "cell-0-shoulder",
        "duration": 1,
        "resource": "test-bench",
        "after": [
          "job-0"
        ]
      },
      {
        "id": "job-3",
        "module": "cell-0-elbow",
        "duration": 3,
        "resource": "technician",
        "after": [
          "job-1"
        ]
      }
    ],
    "deadline": 6
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

### 检查后条件策略（h3-exp-d1-arm-1-policy）

提交一个检查及 observation→action 决策表，在所有相容世界中采取正确动作。

能力：检查后条件策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "cell-0-tool",
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

### 局部坐标变换（h3-exp-d1-arm-1-local-frame）

将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。

能力：局部坐标变换；形式：single-choice；证据：model-state。

- A：[2.9,3.65,1.3]
- B：[1.9,4.65,2.3]
- C：[0.9,3.65,1.3]
- D：[1,0.2625,0]

```json
{
  "input": {
    "localPoint": [
      1,
      0.26249999999999973,
      0
    ],
    "rotationXYZW": [
      0,
      1,
      0,
      6.123233995736766e-17
    ],
    "translation": [
      1.9,
      3.3875,
      1.3
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 正交视图投影（h3-exp-d1-arm-1-projection）

按公开视图坐标约定，选择该世界点投影后的二维坐标。

能力：正交视图投影；形式：single-choice；证据：model-state。

- A：[2,3]
- B：[0,0]
- C：[-3,5]
- D：[5,2]

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
    "choiceId": "C"
  }
}
```

### 空间相对关系（h3-exp-d1-arm-1-relative-order）

比较B相对A在指定世界轴上的模块原点坐标。

能力：空间相对关系；形式：single-choice；证据：model-state。

- A：less
- B：equal
- C：greater

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
      "id": "cell-0-tool",
      "position": [
        1.9,
        3.3875,
        1.3
      ]
    },
    "axis": "y"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 约束自由度（h3-exp-d1-arm-1-joint-axis）

仅考虑这一声明约束，不计闭环、马达与限位激活，保留多少相对运动自由度？弹簧仅施力、不消除自由度。

能力：约束自由度；形式：single-choice；证据：model-state。

- A：6
- B：1
- C：0
- D：3

```json
{
  "input": {
    "joint": {
      "id": "cell-0-shoulder-joint",
      "name": "cell-0-shoulder interface",
      "parent": "cell-0-mount",
      "child": "cell-0-shoulder",
      "type": "revolute",
      "anchorParent": [
        -1.7,
        0.6500000000000001,
        0
      ],
      "anchorChild": [
        0,
        0,
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
    "choiceId": "B"
  }
}
```

### 维修间隙预算（h3-exp-d1-arm-1-clearance-margin）

给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？

能力：维修间隙预算；形式：single-choice；证据：model-state。

- A：blocked
- B：feasible

```json
{
  "input": {
    "module": "cell-0-tool",
    "aperture": 0.39999999999999997,
    "toolWidth": 0.35,
    "eachSideMargin": 0.05
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 载荷力矩（h3-exp-d1-arm-1-load-moment）

绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。

能力：载荷力矩；形式：single-choice；证据：model-state。

- A：[0,0,-3]
- B：[0,0,3]
- C：[0,0,0]
- D：[0,-1,0]

```json
{
  "input": {
    "module": "cell-0-tool",
    "lever": [
      1,
      2,
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
    "choiceId": "A"
  }
}
```

### 非均匀先验更新（h3-exp-d1-arm-1-weighted-posterior）

先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。

能力：非均匀先验更新；形式：single-choice；证据：finite-world。

- A：0.6363636363636364
- B：0
- C：1
- D：0.7777777777777778

```json
{
  "input": {
    "module": "cell-0-tool",
    "worlds": [
      "normal",
      "jammed",
      "loose"
    ],
    "weights": [
      2,
      7,
      2
    ],
    "compatible": [
      "normal",
      "jammed"
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 风险最小决策（h3-exp-d1-arm-1-expected-loss）

继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。

能力：风险最小决策；形式：single-choice；证据：finite-world。

- A：repair
- B：continue

```json
{
  "input": {
    "faultProbability": 0.7,
    "repairCost": 4,
    "failureLoss": 7,
    "module": "cell-0-tool"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 轨迹阈值判定（h3-exp-d1-arm-1-trace-threshold）

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
        "displacement": 0.010063099601191903
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.0021642251665198965
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.0004107058123938101
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.00008316375308431003
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.000015199535029238195
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.000010136295160999924
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.000009856957628387987
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.00000988071717505555
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.00000988071717505555
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.00000988071717505555
      },
      {
        "time": 1,
        "displacement": 0.00000988071717505555
      }
    ],
    "threshold": 0.008050479680953522
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 安全联锁维修（h3-exp-d1-arm-1-guarded-repair）

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
        "id": "release:cell-0-tool",
        "label": "release cell-0-tool",
        "requires": [
          "done:relock:cell-0-tool"
        ],
        "forbids": [
          "done:release:cell-0-tool"
        ],
        "adds": [
          "done:release:cell-0-tool",
          "ready:cell-0-tool",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "relock:cell-0-tool",
        "label": "relock cell-0-tool",
        "requires": [
          "done:verify:cell-0-tool"
        ],
        "forbids": [
          "done:relock:cell-0-tool"
        ],
        "adds": [
          "done:relock:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "verify:cell-0-tool",
        "label": "verify cell-0-tool",
        "requires": [
          "done:replace:cell-0-tool"
        ],
        "forbids": [
          "done:verify:cell-0-tool"
        ],
        "adds": [
          "done:verify:cell-0-tool"
        ],
        "deletes": [
          "fault:cell-0-tool",
          "misaligned:cell-0-tool"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "replace:cell-0-tool",
        "label": "replace cell-0-tool",
        "requires": [
          "done:unlock:cell-0-tool"
        ],
        "forbids": [
          "done:replace:cell-0-tool"
        ],
        "adds": [
          "done:replace:cell-0-tool"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "unlock:cell-0-tool",
        "label": "unlock cell-0-tool",
        "requires": [
          "done:support:cell-0-tool"
        ],
        "forbids": [
          "done:unlock:cell-0-tool"
        ],
        "adds": [
          "done:unlock:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "support:cell-0-tool",
        "label": "support cell-0-tool",
        "requires": [
          "done:isolate:cell-0-tool"
        ],
        "forbids": [
          "done:support:cell-0-tool"
        ],
        "adds": [
          "done:support:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "isolate:cell-0-tool",
        "label": "isolate cell-0-tool",
        "requires": [
          "tool:free",
          "fault:cell-0-tool"
        ],
        "forbids": [
          "done:isolate:cell-0-tool"
        ],
        "adds": [
          "done:isolate:cell-0-tool"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:cell-0-tool"
    ],
    "initialModules": [
      "foundation",
      "cell-0-mount",
      "cell-0-shoulder",
      "cell-0-elbow",
      "cell-0-wrist",
      "cell-0-tool"
    ],
    "goalFacts": [
      "ready:cell-0-tool"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 8
  },
  "answer": {
    "actionIds": [
      "isolate:cell-0-tool",
      "support:cell-0-tool",
      "unlock:cell-0-tool",
      "replace:cell-0-tool",
      "verify:cell-0-tool",
      "relock:cell-0-tool",
      "release:cell-0-tool"
    ]
  }
}
```

### 失败状态回退（h3-exp-d1-arm-1-rollback）

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
        "id": "resume:cell-0-tool",
        "label": "resume cell-0-tool",
        "requires": [
          "done:verify:cell-0-tool"
        ],
        "forbids": [
          "done:resume:cell-0-tool"
        ],
        "adds": [
          "done:resume:cell-0-tool",
          "ready:cell-0-tool",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "verify:cell-0-tool",
        "label": "verify cell-0-tool",
        "requires": [
          "done:align:cell-0-tool"
        ],
        "forbids": [
          "done:verify:cell-0-tool"
        ],
        "adds": [
          "done:verify:cell-0-tool"
        ],
        "deletes": [
          "fault:cell-0-tool",
          "misaligned:cell-0-tool"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "align:cell-0-tool",
        "label": "align cell-0-tool",
        "requires": [
          "done:undo:cell-0-tool"
        ],
        "forbids": [
          "done:align:cell-0-tool"
        ],
        "adds": [
          "done:align:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool",
          "visible": true
        }
      },
      {
        "id": "undo:cell-0-tool",
        "label": "undo cell-0-tool",
        "requires": [
          "done:isolate:cell-0-tool"
        ],
        "forbids": [
          "done:undo:cell-0-tool"
        ],
        "adds": [
          "done:undo:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool",
          "visible": false
        }
      },
      {
        "id": "isolate:cell-0-tool",
        "label": "isolate cell-0-tool",
        "requires": [
          "tool:free",
          "fault:cell-0-tool"
        ],
        "forbids": [
          "done:isolate:cell-0-tool"
        ],
        "adds": [
          "done:isolate:cell-0-tool"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:cell-0-tool",
      "misaligned:cell-0-tool"
    ],
    "initialModules": [
      "foundation",
      "cell-0-mount",
      "cell-0-shoulder",
      "cell-0-elbow",
      "cell-0-wrist",
      "cell-0-tool"
    ],
    "goalFacts": [
      "ready:cell-0-tool"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 5
  },
  "answer": {
    "actionIds": [
      "isolate:cell-0-tool",
      "undo:cell-0-tool",
      "align:cell-0-tool",
      "verify:cell-0-tool",
      "resume:cell-0-tool"
    ]
  }
}
```

### 共享工具协同维修（h3-exp-d1-arm-1-resource-repair）

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
        "id": "release:cell-0-tool",
        "label": "release cell-0-tool",
        "requires": [
          "done:relock:cell-0-tool"
        ],
        "forbids": [
          "done:release:cell-0-tool"
        ],
        "adds": [
          "done:release:cell-0-tool",
          "ready:cell-0-tool",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "relock:cell-0-tool",
        "label": "relock cell-0-tool",
        "requires": [
          "done:verify:cell-0-tool"
        ],
        "forbids": [
          "done:relock:cell-0-tool"
        ],
        "adds": [
          "done:relock:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "verify:cell-0-tool",
        "label": "verify cell-0-tool",
        "requires": [
          "done:replace:cell-0-tool"
        ],
        "forbids": [
          "done:verify:cell-0-tool"
        ],
        "adds": [
          "done:verify:cell-0-tool"
        ],
        "deletes": [
          "fault:cell-0-tool",
          "misaligned:cell-0-tool"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "replace:cell-0-tool",
        "label": "replace cell-0-tool",
        "requires": [
          "done:unlock:cell-0-tool"
        ],
        "forbids": [
          "done:replace:cell-0-tool"
        ],
        "adds": [
          "done:replace:cell-0-tool"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "unlock:cell-0-tool",
        "label": "unlock cell-0-tool",
        "requires": [
          "done:support:cell-0-tool"
        ],
        "forbids": [
          "done:unlock:cell-0-tool"
        ],
        "adds": [
          "done:unlock:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "support:cell-0-tool",
        "label": "support cell-0-tool",
        "requires": [
          "done:isolate:cell-0-tool"
        ],
        "forbids": [
          "done:support:cell-0-tool"
        ],
        "adds": [
          "done:support:cell-0-tool"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "isolate:cell-0-tool",
        "label": "isolate cell-0-tool",
        "requires": [
          "tool:free",
          "fault:cell-0-tool"
        ],
        "forbids": [
          "done:isolate:cell-0-tool"
        ],
        "adds": [
          "done:isolate:cell-0-tool"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-tool"
        }
      },
      {
        "id": "release:cell-0-wrist",
        "label": "release cell-0-wrist",
        "requires": [
          "done:relock:cell-0-wrist"
        ],
        "forbids": [
          "done:release:cell-0-wrist"
        ],
        "adds": [
          "done:release:cell-0-wrist",
          "ready:cell-0-wrist",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-wrist"
        }
      },
      {
        "id": "relock:cell-0-wrist",
        "label": "relock cell-0-wrist",
        "requires": [
          "done:verify:cell-0-wrist"
        ],
        "forbids": [
          "done:relock:cell-0-wrist"
        ],
        "adds": [
          "done:relock:cell-0-wrist"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-wrist"
        }
      },
      {
        "id": "verify:cell-0-wrist",
        "label": "verify cell-0-wrist",
        "requires": [
          "done:replace:cell-0-wrist"
        ],
        "forbids": [
          "done:verify:cell-0-wrist"
        ],
        "adds": [
          "done:verify:cell-0-wrist"
        ],
        "deletes": [
          "fault:cell-0-wrist",
          "misaligned:cell-0-wrist"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-wrist"
        }
      },
      {
        "id": "replace:cell-0-wrist",
        "label": "replace cell-0-wrist",
        "requires": [
          "done:unlock:cell-0-wrist"
        ],
        "forbids": [
          "done:replace:cell-0-wrist"
        ],
        "adds": [
          "done:replace:cell-0-wrist"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "cell-0-wrist"
        }
      },
      {
        "id": "unlock:cell-0-wrist",
        "label": "unlock cell-0-wrist",
        "requires": [
          "done:support:cell-0-wrist"
        ],
        "forbids": [
          "done:unlock:cell-0-wrist"
        ],
        "adds": [
          "done:unlock:cell-0-wrist"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-wrist"
        }
      },
      {
        "id": "support:cell-0-wrist",
        "label": "support cell-0-wrist",
        "requires": [
          "done:isolate:cell-0-wrist"
        ],
        "forbids": [
          "done:support:cell-0-wrist"
        ],
        "adds": [
          "done:support:cell-0-wrist"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-wrist"
        }
      },
      {
        "id": "isolate:cell-0-wrist",
        "label": "isolate cell-0-wrist",
        "requires": [
          "tool:free",
          "fault:cell-0-wrist"
        ],
        "forbids": [
          "done:isolate:cell-0-wrist"
        ],
        "adds": [
          "done:isolate:cell-0-wrist"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cell-0-wrist"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:cell-0-wrist",
      "fault:cell-0-tool"
    ],
    "initialModules": [
      "foundation",
      "cell-0-mount",
      "cell-0-shoulder",
      "cell-0-elbow",
      "cell-0-wrist",
      "cell-0-tool"
    ],
    "goalFacts": [
      "ready:cell-0-wrist",
      "ready:cell-0-tool"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 16
  },
  "answer": {
    "actionIds": [
      "isolate:cell-0-tool",
      "support:cell-0-tool",
      "unlock:cell-0-tool",
      "replace:cell-0-tool",
      "verify:cell-0-tool",
      "relock:cell-0-tool",
      "release:cell-0-tool",
      "isolate:cell-0-wrist",
      "support:cell-0-wrist",
      "unlock:cell-0-wrist",
      "replace:cell-0-wrist",
      "verify:cell-0-wrist",
      "relock:cell-0-wrist",
      "release:cell-0-wrist"
    ]
  }
}
```

### 预算约束检查策略（h3-exp-d1-arm-1-budget-policy）

提交预算内、对所有相容世界均正确的检查决策表。

能力：预算约束检查策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "cell-0-tool",
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
        "cost": 2,
        "returns": {
          "nominal": "pass",
          "fault": "fail"
        }
      },
      {
        "id": "probe",
        "cost": 0,
        "returns": {
          "nominal": "pass",
          "fault": "pass"
        }
      },
      {
        "id": "thermal",
        "cost": 3,
        "returns": {
          "nominal": "pass",
          "fault": "fail"
        }
      }
    ],
    "budget": 2
  },
  "answer": {
    "queryId": "visual",
    "decisions": {
      "pass": "continue",
      "fail": "tighten"
    }
  }
}
```
